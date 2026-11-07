"""Matriz de (a + a^dagger)^2 en la base de Fock par."""

import numpy as np
from scipy import sparse


class MatrizX2Par:
    """Matriz de (a+a^dagger)^2 sobre |0>, |2>, ..., |2K>."""

    def __init__(self, K):
        if K < 1:
            raise ValueError("Se requiere K>=1.")
        self.K = int(K)

    def construir(self):
        k = np.arange(self.K + 1, dtype=float)
        diagonal = 4.0 * k + 1.0
        superior = np.sqrt((2.0 * k[:-1] + 1.0) * (2.0 * k[:-1] + 2.0))
        return sparse.diags(
            [superior, diagonal, superior], [-1, 0, 1], format="csr"
        )
