"""Tabla CSV de la serie temporal de un corte."""

import csv


class EscritorCSV:
    """Guarda t, numero, varianza, vacio, borde, norma y energia."""

    COLUMNAS = ("t", "N", "N2", "varN", "P0", "B", "N_borde", "norma", "energia")

    def escribir(self, ruta, datos):
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.COLUMNAS)
            for i in range(len(datos["t"])):
                escritor.writerow(
                    [f"{float(datos[clave][i]):.12g}" for clave in self.COLUMNAS]
                )
