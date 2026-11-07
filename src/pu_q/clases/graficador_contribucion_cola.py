"""Figuras de R_M^{(K)}(t) al variar el umbral y el corte."""


class GraficadorContribucionCola:
    """Dibuja la cola en el tiempo y su valor final frente a M."""

    def graficar_en_tiempo(self, tiempos, curvas_por_corte, ruta, titulo):
        import matplotlib.pyplot as plt

        umbrales = list(next(iter(curvas_por_corte.values())))
        columnas = 3
        filas = (len(umbrales) + columnas - 1) // columnas
        fig, ejes = plt.subplots(filas, columnas, figsize=(12.5, 3.2 * filas), sharex=True)
        ejes = ejes.ravel()
        for eje, umbral in zip(ejes, umbrales):
            for K, curvas in sorted(curvas_por_corte.items()):
                eje.plot(tiempos, curvas[umbral], linewidth=1.5, label=f"K={K}")
            eje.set_title(rf"$R_{{{umbral}}}(t)$")
            eje.set_xlabel(r"$t$")
            eje.set_ylabel(rf"$R_{{{umbral}}}^{{(K)}}(t)$")
            eje.grid(alpha=0.25)
            eje.legend(fontsize=8, loc="best")
        for eje in ejes[len(umbrales) :]:
            eje.axis("off")
        fig.suptitle(titulo)
        fig.tight_layout()
        fig.savefig(ruta, dpi=180)
        plt.close(fig)

    def graficar_frente_a_umbral(self, curvas_por_corte, ruta, titulo):
        import matplotlib.pyplot as plt

        fig, eje = plt.subplots(figsize=(9.5, 5.5))
        for K, curvas in sorted(curvas_por_corte.items()):
            umbrales = list(curvas)
            valores = [curvas[umbral][-1] for umbral in umbrales]
            eje.semilogy(umbrales, valores, marker="o", linewidth=1.5, label=f"K={K}")
        eje.set_xlabel(r"Umbral $M$")
        eje.set_ylabel(r"$R_M^{(K)}(t_{\mathrm{final}})$")
        eje.set_title(titulo)
        eje.grid(alpha=0.25, which="both")
        eje.legend(loc="best")
        fig.tight_layout()
        fig.savefig(ruta, dpi=180)
        plt.close(fig)
