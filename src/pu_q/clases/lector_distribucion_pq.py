"""Lectura del CSV ancho de p_q(t) escrito por ExportadorDistribucionPq."""

import numpy as np


class LectorDistribucionPq:
    """Devuelve la malla temporal y p_q, con columnas N=0,2,4,...,4K."""

    def leer(self, ruta):
        tabla = np.loadtxt(ruta, delimiter=",", skiprows=1)
        if tabla.ndim == 1:
            tabla = tabla[None, :]
        return tabla[:, 0], tabla[:, 1:]
