"""CSV de R_M(t) para varios umbrales M."""

import csv


class ExportadorContribucionCola:
    """Una fila por tiempo y una columna R_M por cada umbral."""

    def exportar(self, ruta, tiempos, curvas):
        umbrales = list(curvas)
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["t"] + [f"R_{umbral}" for umbral in umbrales])
            for i, tiempo in enumerate(tiempos):
                escritor.writerow(
                    [f"{float(tiempo):.12g}"]
                    + [f"{float(curvas[umbral][i]):.12g}" for umbral in umbrales]
                )
