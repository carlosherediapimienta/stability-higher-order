"""Evolucion unitaria exacta del Hamiltoniano truncado."""

import numpy as np
from scipy.sparse.linalg import expm_multiply

from pu_q.clases.sistema_truncado import SistemaTruncado


class EvolucionUnitaria:
    """Evoluciona |0,0> con H_K y devuelve los observables en la malla temporal."""

    def __init__(self, K, omega1, omega2, lam, hbar):
        self.sistema = SistemaTruncado(K, omega1, omega2, lam, hbar)

    def evolucionar(self, tiempos):
        sistema = self.sistema
        psi0 = np.zeros(sistema.dimension, dtype=np.complex128)
        psi0[0] = 1.0

        generador = (-1j / sistema.hbar) * sistema.H
        psi_t = expm_multiply(
            generador,
            psi0,
            start=float(tiempos[0]),
            stop=float(tiempos[-1]),
            num=len(tiempos),
            endpoint=True,
            traceA=generador.diagonal().sum(),
        )
        if psi_t.ndim == 1:
            psi_t = psi_t[None, :]

        p = np.abs(psi_t) ** 2
        norma = p.sum(axis=1)
        numero_medio = p @ sistema.ocup_total
        numero_cuadrado = p @ (sistema.ocup_total.astype(float) ** 2)
        varianza_numero = np.maximum(0.0, numero_cuadrado - numero_medio**2)
        prob_vacio = p[:, 0]
        prob_borde = p[:, sistema.mask_borde].sum(axis=1)
        ocupacion_borde = p[:, sistema.mask_borde] @ sistema.ocup_total[sistema.mask_borde]

        Hpsi = (sistema.H @ psi_t.T).T
        energia = np.real(np.sum(psi_t.conj() * Hpsi, axis=1))

        return {
            "t": np.array(tiempos),
            "N": numero_medio,
            "N2": numero_cuadrado,
            "varN": varianza_numero,
            "P0": prob_vacio,
            "B": prob_borde,
            "N_borde": ocupacion_borde,
            "norma": norma,
            "energia": energia,
            "E0": sistema.c,
            "K": sistema.K,
            "dimension": sistema.dimension,
        }
