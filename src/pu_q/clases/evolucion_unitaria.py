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
        prob_q = self._probabilidad_por_numero_total(p)
        norma = p.sum(axis=1)
        numero_medio = p @ sistema.ocup_total
        numero_cuadrado = p @ (sistema.ocup_total.astype(float) ** 2)
        varianza_numero = np.maximum(0.0, numero_cuadrado - numero_medio**2)
        prob_vacio = p[:, 0]
        prob_borde = p[:, sistema.mask_borde].sum(axis=1)
        ocupacion_borde = p[:, sistema.mask_borde] @ sistema.ocup_total[sistema.mask_borde]
        self._comprobar_probabilidad_q(prob_q, norma, numero_medio, numero_cuadrado)

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
            "p_q": prob_q,
        }

    def _probabilidad_por_numero_total(self, probabilidad):
        """Suma p sobre los estados con N_a+N_b = 2q.

        La base es |2k, 2ell>, con k mas rapido que ell. En el bloque ell
        las columnas tienen q = ell, ell+1, ..., ell+K.
        """
        K = self.sistema.K
        dimension_1d = K + 1
        prob_q = np.zeros((probabilidad.shape[0], 2 * K + 1), dtype=float)
        for ell in range(dimension_1d):
            inicio = ell * dimension_1d
            prob_q[:, ell : ell + dimension_1d] += probabilidad[
                :, inicio : inicio + dimension_1d
            ]
        return prob_q

    def _comprobar_probabilidad_q(self, prob_q, norma, numero_medio, numero_cuadrado):
        numero_q = 2 * np.arange(prob_q.shape[1], dtype=float)
        np.testing.assert_allclose(prob_q.sum(axis=1), norma, rtol=1e-11, atol=1e-11)
        np.testing.assert_allclose(
            prob_q @ numero_q, numero_medio, rtol=1e-10, atol=1e-10
        )
        np.testing.assert_allclose(
            prob_q @ (numero_q**2), numero_cuadrado, rtol=1e-10, atol=1e-10
        )
