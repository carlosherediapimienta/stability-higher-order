"""Argumentos de consola y arranque de la simulacion."""

import argparse
from pathlib import Path

from pu_q.orquestador import Orquestador


def construir_desde_argv(argv=None):
    """Construye el orquestador a partir de los argumentos de consola."""
    parser = argparse.ArgumentParser(
        description=(
            "Oscilador de Pais-Uhlenbeck con interaccion cuartica.\n\n"
            "H' = hbar*omega1*N_a - hbar*omega2*N_b + lambda*Q1^2*Q2^2.\n"
            "La evolucion es exacta para el Hamiltoniano truncado; no prueba\n"
            "estabilidad de la teoria de dimension infinita."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--omega1", type=float, default=1.0)
    parser.add_argument(
        "--omega2",
        type=str,
        default="ambos",
        help="ambos, sqrt2 o una frecuencia numerica (por defecto: ambos)",
    )
    parser.add_argument(
        "--lam", type=float, default=0.2, help="Acoplamiento lambda (por defecto: 0.2)"
    )
    parser.add_argument("--hbar", type=float, default=1.0)
    parser.add_argument(
        "--cuts",
        type=int,
        nargs="+",
        default=[12, 40, 60],
        help="Valores K: maxima ocupacion individual = 2K",
    )
    parser.add_argument("--tmax", type=float, default=6.0)
    parser.add_argument(
        "--nt",
        type=int,
        default=121,
        help="Numero de puntos temporales de 0 a tmax, incluidos",
    )
    parser.add_argument("--outdir", type=Path, default=Path("resultados_pu_q"))
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Prueba breve: cuts 1 4 8, tmax 2, nt 41",
    )
    args = parser.parse_args(argv)
    return Orquestador(
        omega1=args.omega1,
        omega2=args.omega2,
        lam=args.lam,
        hbar=args.hbar,
        cuts=args.cuts,
        tmax=args.tmax,
        nt=args.nt,
        outdir=args.outdir,
        quick=args.quick,
    )


def main(argv=None):
    import matplotlib

    matplotlib.use("Agg")
    try:
        construir_desde_argv(argv).ejecutar()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
