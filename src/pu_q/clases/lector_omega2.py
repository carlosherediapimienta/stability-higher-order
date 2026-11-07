"""Interpretacion del argumento omega2 como lista de casos."""

import numpy as np


class LectorOmega2:
    """Traduce el argumento --omega2 a una lista de (etiqueta, valor)."""

    def interpretar(self, valor, omega1):
        if valor == "ambos":
            return [("sqrt2", omega1 * np.sqrt(2.0)), ("2", 2.0 * omega1)]
        if valor == "sqrt2":
            return [("sqrt2", omega1 * np.sqrt(2.0))]
        try:
            omega2 = float(valor)
        except ValueError as exc:
            raise ValueError("--omega2 debe ser ambos, sqrt2 o un numero") from exc
        if omega2 <= 0:
            raise ValueError("omega2 debe ser positivo")
        return [(f"{omega2:g}".replace(".", "p"), omega2)]
