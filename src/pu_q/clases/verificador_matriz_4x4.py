"""Comprobacion analitica del Hamiltoniano en la base minima."""

import numpy as np

from pu_q.clases.sistema_truncado import SistemaTruncado


class VerificadorMatriz4x4:
    """Contrasta H_K para K=1 con la matriz explicita de 4x4."""

    def verificar(self, omega1=1.0, omega2=2.0, lam=0.2, hbar=1.0):
        sistema = SistemaTruncado(1, omega1, omega2, lam, hbar)
        rt2 = np.sqrt(2.0)
        interaccion = sistema.c * np.array(
            [
                [1, rt2, rt2, 2],
                [rt2, 5, 2, 5 * rt2],
                [rt2, 2, 5, 5 * rt2],
                [2, 5 * rt2, 5 * rt2, 25],
            ],
            dtype=float,
        )
        esperada = np.diag([0.0, 2.0, -4.0, -2.0]) + interaccion
        np.testing.assert_allclose(
            sistema.H.toarray(), esperada, rtol=1e-13, atol=1e-13
        )
        print("Comprobacion de matriz 4x4: CORRECTA")
        print("Orden de la base: |0,0>, |2,0>, |0,2>, |2,2>")
        print(np.array2string(sistema.H.toarray(), precision=6, suppress_small=True))
        return sistema
