"""p_q(t_final) y la aportacion N p_q al numero medio, una curva por corte."""


class GraficadorDistribucionFinal:
    """Compara la cola de ocupacion en el ultimo tiempo entre varios K."""

    def graficar(self, resultados, ruta_prob, ruta_aporte, titulo):
        import matplotlib.pyplot as plt
        import numpy as np

        fig, eje = plt.subplots(figsize=(9.5, 5.5))
        for K, datos in sorted(resultados.items()):
            numero = 2 * np.arange(2 * K + 1)
            prob_q = datos["p_q"][-1]
            mascara = (numero > 0) & (prob_q > 0)
            eje.semilogy(numero[mascara], prob_q[mascara], label=f"K={K}", linewidth=1.6)
        eje.set_xlabel("Numero total de excitaciones N=2q")
        eje.set_ylabel(r"$p_q(t_{final})$")
        eje.set_title(titulo + ": probabilidad por ocupacion (sin vacio)")
        eje.grid(alpha=0.25)
        eje.legend()
        fig.tight_layout()
        fig.savefig(ruta_prob, dpi=180)
        plt.close(fig)

        fig, eje = plt.subplots(figsize=(9.5, 5.5))
        for K, datos in sorted(resultados.items()):
            numero = 2 * np.arange(2 * K + 1)
            aporte = numero * datos["p_q"][-1]
            mascara = (numero > 0) & (aporte > 0)
            eje.semilogy(numero[mascara], aporte[mascara], label=f"K={K}", linewidth=1.6)
        eje.set_xlabel("Numero total de excitaciones N=2q")
        eje.set_ylabel(r"Contribucion $N p_q(t_{final})$ a $\langle N\rangle$")
        eje.set_title(titulo + ": contribuciones al numero medio")
        eje.grid(alpha=0.25)
        eje.legend()
        fig.tight_layout()
        fig.savefig(ruta_aporte, dpi=180)
        plt.close(fig)
