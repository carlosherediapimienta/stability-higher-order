"""Contribucion de la cola al numero medio de excitaciones."""

import numpy as np


class ContribucionColaRM:
    """R_M(t) = suma de 2q p_q(t) sobre los estados con 2q >= M.

    M=0 recupera <N>(t), porque el vacio no aporta al numero.
    """

    UMBRALES = (0, 2, 4, 8, 16, 32, 64, 128, 256)

    def calcular(self, prob_q, umbrales=None):
        if umbrales is None:
            umbrales = self.UMBRALES
        numero = 2.0 * np.arange(prob_q.shape[1])
        aporte = prob_q * numero
        cola = np.cumsum(aporte[:, ::-1], axis=1)[:, ::-1]
        curvas = {}
        for umbral in umbrales:
            q_minimo = int(np.ceil(float(umbral) / 2.0))
            if q_minimo <= 0:
                curvas[int(umbral)] = cola[:, 0].copy()
            elif q_minimo >= cola.shape[1]:
                curvas[int(umbral)] = np.zeros(cola.shape[0])
            else:
                curvas[int(umbral)] = cola[:, q_minimo].copy()
        return curvas
