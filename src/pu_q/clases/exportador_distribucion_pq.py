"""CSV de p_q(t) y del desglose en el tiempo final."""

import csv

import numpy as np


class ExportadorDistribucionPq:
    """Guarda la probabilidad de cada N=2q y su aportacion en t_final."""

    def exportar(self, ruta_todo, ruta_final, datos):
        K = datos["K"]
        numero_total = 2 * np.arange(2 * K + 1, dtype=int)
        prob_q = datos["p_q"]

        with ruta_todo.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["t"] + [f"p_N_{n}" for n in numero_total])
            for t, fila in zip(datos["t"], prob_q):
                escritor.writerow(
                    [f"{float(t):.12g}"] + [f"{float(v):.12g}" for v in fila]
                )

        fila_final = prob_q[-1]
        cola = np.cumsum(fila_final[::-1])[::-1]
        with ruta_final.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                ["q", "N_total", "p_q", "aporte_a_N", "aporte_a_N2", "P_N_mayor_igual"]
            )
            for q, n in enumerate(numero_total):
                prob = fila_final[q]
                escritor.writerow(
                    [
                        q,
                        int(n),
                        f"{prob:.12g}",
                        f"{(n * prob):.12g}",
                        f"{(n * n * prob):.12g}",
                        f"{cola[q]:.12g}",
                    ]
                )
