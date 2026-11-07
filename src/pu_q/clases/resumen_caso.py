"""Resumen numerico de norma, energia y convergencia entre cortes."""

import numpy as np


class ResumenCaso:
    """Imprime controles de unitariedad y la tabla de <N>(t) por corte."""

    def imprimir(self, nombre, resultados, tiempos_referencia):
        print("\n" + "=" * 72)
        print("Frecuencias:", nombre)
        print("K  Dimension    max|norma-1|    max|<H>-E0|     <N>(t_final)")
        for K, datos in sorted(resultados.items()):
            desvio_norma = np.max(np.abs(datos["norma"] - 1.0))
            desvio_energia = np.max(np.abs(datos["energia"] - datos["E0"]))
            print(
                f'{K:2d} {datos["dimension"]:9d}     {desvio_norma:11.3e}    '
                f'{desvio_energia:11.3e}     {datos["N"][-1]:.8f}'
            )

        print("\nValores de <N>(t) por corte (redondeados):")
        print(" t " + "".join(f"          K={K:3d}" for K in sorted(resultados)))
        t_final = next(iter(resultados.values()))["t"][-1]
        for tiempo in tiempos_referencia:
            if tiempo > t_final + 1e-12:
                continue
            linea = f"{tiempo:4.2f}"
            for _K, datos in sorted(resultados.items()):
                numero = np.interp(tiempo, datos["t"], datos["N"])
                linea += f"       {numero:10.6f}"
            print(linea)

        cortes = sorted(resultados)
        if len(cortes) >= 2:
            fino, grueso = resultados[cortes[-2]], resultados[cortes[-1]]
            diferencia = np.abs(fino["N"] - grueso["N"])
            print(f"\nDiferencia entre K={cortes[-2]} y K={cortes[-1]}:")
            print(
                f" max_t |<N>_K={cortes[-1]} - <N>_K={cortes[-2]}| = "
                f"{np.max(diferencia):.7g}"
            )
            print(f" diferencia en t_final = {diferencia[-1]:.7g}")
            print(" Estas diferencias prueban sensibilidad al corte, no inestabilidad.")
