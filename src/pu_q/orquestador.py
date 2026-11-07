"""Orquesta la verificacion, los cortes y la escritura de resultados."""

from pathlib import Path

import numpy as np

from pu_q.clases import (
    ContribucionColaRM,
    EscritorCSV,
    EvolucionUnitaria,
    ExportadorContribucionCola,
    ExportadorDistribucionPq,
    GraficadorContribucionCola,
    GraficadorDistribucionFinal,
    GraficadorPorCorte,
    LectorOmega2,
    ResumenCaso,
    VerificadorMatriz4x4,
)


class Orquestador:
    """Recorre frecuencias y cortes, y deja CSV, PNG y el resumen en consola."""

    def __init__(
        self,
        omega1=1.0,
        omega2="ambos",
        lam=0.2,
        hbar=1.0,
        cuts=None,
        tmax=6.0,
        nt=121,
        outdir=Path("resultados_pu_q"),
        quick=False,
    ):
        self.omega1 = omega1
        self.omega2 = omega2
        self.lam = lam
        self.hbar = hbar
        self.cuts = [12, 40, 60, 80, 100, 120, 140] if cuts is None else list(cuts)
        self.tmax = tmax
        self.nt = nt
        self.outdir = Path(outdir)
        self.quick = quick
        self.escritor = EscritorCSV()
        self.exportador_pq = ExportadorDistribucionPq()
        self.contribucion = ContribucionColaRM()
        self.exportador_rm = ExportadorContribucionCola()
        self.graficador = GraficadorPorCorte()
        self.graficador_distribucion = GraficadorDistribucionFinal()
        self.graficador_rm = GraficadorContribucionCola()
        self.lector = LectorOmega2()
        self.resumen = ResumenCaso()
        self.verificador = VerificadorMatriz4x4()

    def preparar(self):
        if self.quick:
            self.cuts = [1, 4, 8]
            self.tmax = 2.0
            self.nt = 41
        if self.nt < 2 or self.tmax <= 0 or min(self.cuts) < 1:
            raise ValueError("Se requiere nt>=2, tmax>0 y cortes K>=1.")
        self.outdir.mkdir(parents=True, exist_ok=True)

    def ejecutar(self):
        self.preparar()
        self.verificador.verificar()
        tiempos = np.linspace(0.0, self.tmax, self.nt)

        for etiqueta, omega2 in self.lector.interpretar(self.omega2, self.omega1):
            print(
                f"\nSimulando omega1={self.omega1:g}, omega2={omega2:.9g}, "
                f"lambda={self.lam:g}, hbar={self.hbar:g}"
            )
            resultados = {}
            curvas_rm = {}
            for K in sorted(set(self.cuts)):
                print(f"  Calculando K={K}, dimension={(K + 1) ** 2}...", flush=True)
                datos = EvolucionUnitaria(
                    K, self.omega1, omega2, self.lam, self.hbar
                ).evolucionar(tiempos)
                resultados[K] = datos
                base = f"pu_omega2_{etiqueta}_K_{K}"
                destino = self.outdir / f"{base}.csv"
                self.escritor.escribir(destino, datos)
                self.exportador_pq.exportar(
                    self.outdir / f"{base}_pq_todos_los_tiempos.csv",
                    self.outdir / f"{base}_pq_tfinal.csv",
                    datos,
                )
                curvas_rm[K] = self.contribucion.calcular(datos["p_q"])
                self.exportador_rm.exportar(
                    self.outdir / f"{base}_rm.csv", tiempos, curvas_rm[K]
                )
                print("  Archivo:", destino)

            self.resumen.imprimir(
                etiqueta, resultados, tiempos_referencia=[0, 0.1, 1, 2, 4, 6]
            )
            self._graficar_caso(etiqueta, omega2, resultados, tiempos, curvas_rm)

        print("\nArchivos guardados en:", self.outdir.resolve())
        print("RECORDATORIO: los resultados convergentes en tiempos finitos no")
        print("demuestran por si solos estabilidad/inestabilidad para todo t.")

    def _graficar_caso(self, etiqueta, omega2, resultados, tiempos, curvas_rm):
        sufijo = f"omega2_{etiqueta}"
        self.graficador_rm.graficar_en_tiempo(
            tiempos,
            curvas_rm,
            self.outdir / f"rm_tiempo_{sufijo}.png",
            rf"Contribucion de la cola ($\omega_2={omega2:.5g}$)",
        )
        self.graficador_rm.graficar_frente_a_umbral(
            curvas_rm,
            self.outdir / f"rm_umbral_{sufijo}.png",
            rf"$R_M$ en $t={self.tmax:g}$ ($\omega_2={omega2:.5g}$)",
        )
        self.graficador_distribucion.graficar(
            resultados,
            self.outdir / f"distribucion_{sufijo}.png",
            self.outdir / f"aporte_N_{sufijo}.png",
            rf"Distribucion en t={self.tmax:g} ($\omega_2={omega2:.5g}$)",
        )
        self.graficador.graficar(
            resultados,
            self.outdir / f"numero_{sufijo}.png",
            "N",
            r"$\langle N_a+N_b\rangle_t$",
            rf"Numero medio de excitaciones ($\omega_2={omega2:.5g}$)",
        )
        self.graficador.graficar(
            resultados,
            self.outdir / f"vacio_{sufijo}.png",
            "P0",
            r"$P_{0\to0}(t)$",
            rf"Supervivencia del vacio libre ($\omega_2={omega2:.5g}$)",
        )
        self.graficador.graficar(
            resultados,
            self.outdir / f"borde_{sufijo}.png",
            "B",
            r"$B_K(t)$",
            rf"Probabilidad en el borde ($\omega_2={omega2:.5g}$)",
        )
        self.graficador.graficar(
            resultados,
            self.outdir / f"varianza_{sufijo}.png",
            "varN",
            r"$\mathrm{Var}(N_a+N_b)$",
            rf"Varianza de excitaciones ($\omega_2={omega2:.5g}$)",
        )
