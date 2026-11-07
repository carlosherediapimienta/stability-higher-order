"""Una curva por corte K de un mismo observable."""


class GraficadorPorCorte:
    """Dibuja un observable frente al tiempo, con una curva por cada K."""

    def graficar(self, resultados, ruta, variable, ylabel, titulo):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(9, 5.4))
        for K, datos in sorted(resultados.items()):
            plt.plot(
                datos["t"],
                datos[variable],
                linewidth=1.7,
                label=f"K={K} (hasta {2 * K} por oscilador)",
            )
        plt.xlabel(r"Tiempo $t$ (unidades de $1/\omega_1$ si $\omega_1=1$)")
        plt.ylabel(ylabel)
        plt.title(titulo)
        plt.grid(alpha=0.25)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.savefig(ruta, dpi=180)
        plt.close()
