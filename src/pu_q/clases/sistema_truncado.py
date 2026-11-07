"""Hamiltoniano truncado y observables de la base par."""

import numpy as np
from scipy import sparse

from pu_q.clases.matriz_x2_par import MatrizX2Par


class SistemaTruncado:
    """H_K y operadores en el orden |2k, 2l>, con l exterior y k interior."""

    def __init__(self, K, omega1, omega2, lam, hbar):
        if K < 1 or omega1 <= 0 or omega2 <= 0 or hbar <= 0:
            raise ValueError("Se requiere K>=1 y frecuencias y hbar positivos.")

        self.K = int(K)
        self.omega1 = float(omega1)
        self.omega2 = float(omega2)
        self.lam = float(lam)
        self.hbar = float(hbar)

        d = self.K + 1
        k = np.arange(d, dtype=np.int64)
        self.ocup_a = np.tile(2 * k, d)
        self.ocup_b = np.repeat(2 * k, d)
        self.ocup_total = self.ocup_a + self.ocup_b

        H0_diag = self.hbar * (self.omega1 * self.ocup_a - self.omega2 * self.ocup_b)
        H0 = sparse.diags(H0_diag.astype(float), format="csr")
        self.c = self.lam * self.hbar**2 / (4.0 * self.omega1 * self.omega2)

        X = MatrizX2Par(self.K).construir()
        # Producto tensorial: |2l> (oscilador b) x |2k> (oscilador a).
        V = self.c * sparse.kron(X, X, format="csr")
        self.H = (H0 + V).tocsr()
        self.mask_borde = (self.ocup_a == 2 * self.K) | (self.ocup_b == 2 * self.K)
        self.dimension = d * d
