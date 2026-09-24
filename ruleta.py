#!/usr/bin/env python3
"""Ruleta de premios estilo casino para la terminal.

Cada giro cuesta fichas. La ruleta se detiene en una casilla elegida al azar
según el peso de cada premio: los premios grandes salen con menos frecuencia.

Uso:
    python3 ruleta.py                 # juego interactivo
    python3 ruleta.py --fichas 50     # empezar con 50 fichas
    python3 ruleta.py --probabilidades  # ver la tabla de premios y salir
"""

import argparse
import random
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Premio:
    nombre: str
    fichas: int  # fichas que se suman al saldo (0 si el premio es un objeto)
    peso: int    # cuanto mayor, más probable
    color: str   # código ANSI


ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CIAN = "\033[96m"
GRIS = "\033[90m"
NEGRITA = "\033[1m"
RESET = "\033[0m"

PREMIOS = [
    Premio("Sin premio", 0, 30, GRIS),
    Premio("+5 fichas", 5, 22, VERDE),
    Premio("+10 fichas", 10, 15, VERDE),
    Premio("Giro gratis", 0, 12, CIAN),
    Premio("+25 fichas", 25, 8, AZUL),
    Premio("Camiseta", 0, 6, MAGENTA),
    Premio("+50 fichas", 50, 4, AMARILLO),
    Premio("Cena para dos", 0, 2, ROJO),
    Premio("JACKPOT +200 fichas", 200, 1, AMARILLO + NEGRITA),
]

COSTO_GIRO = 10


def elegir_premio(rng: random.Random) -> Premio:
    return rng.choices(PREMIOS, weights=[p.peso for p in PREMIOS], k=1)[0]


def animar_giro(ganador: Premio, rng: random.Random, color: bool) -> None:
    """Muestra las casillas pasando cada vez más lento hasta caer en el ganador."""
    n = len(PREMIOS)
    inicio = rng.randrange(n)
    # Dos o tres vueltas completas y luego avanzar hasta la casilla ganadora.
    pasos = rng.randint(2, 3) * n + (PREMIOS.index(ganador) - inicio) % n

    for i in range(pasos + 1):
        premio = PREMIOS[(inicio + i) % len(PREMIOS)]
        texto = pintar(f"▶ {premio.nombre:^22} ◀", premio.color, color)
        sys.stdout.write("\r  " + texto)
        sys.stdout.flush()
        progreso = i / pasos
        time.sleep(0.03 + 0.35 * progreso ** 3)
    print()


def pintar(texto: str, codigo: str, color: bool) -> str:
    return f"{codigo}{texto}{RESET}" if color else texto


def mostrar_probabilidades() -> None:
    total = sum(p.peso for p in PREMIOS)
    print(f"{'Premio':<22} {'Probabilidad':>12}")
    print("-" * 35)
    for p in PREMIOS:
        print(f"{p.nombre:<22} {p.peso / total:>11.1%}")
    esperado = sum(p.fichas * p.peso for p in PREMIOS) / total
    print("-" * 35)
    print(f"Costo por giro: {COSTO_GIRO} fichas | "
          f"retorno medio en fichas: {esperado:.2f}")


def jugar(fichas: int, rng: random.Random, animar: bool, color: bool) -> None:
    objetos: list[str] = []
    giros_gratis = 0
    giros = 0

    print(pintar("\n  🎰  RULETA DE PREMIOS  🎰\n", NEGRITA, color))
    print(f"  Cada giro cuesta {COSTO_GIRO} fichas. "
          "Enter para girar, 'p' para ver probabilidades, 'q' para salir.\n")

    while True:
        if giros_gratis == 0 and fichas < COSTO_GIRO:
            print("  Te quedaste sin fichas suficientes para girar.")
            break

        estado = f"Fichas: {fichas}"
        if giros_gratis:
            estado += f" | Giros gratis: {giros_gratis}"
        try:
            orden = input(f"  [{estado}] > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if orden in ("q", "salir"):
            break
        if orden == "p":
            mostrar_probabilidades()
            continue
        if orden:
            print("  Opción no válida.")
            continue

        if giros_gratis:
            giros_gratis -= 1
        else:
            fichas -= COSTO_GIRO
        giros += 1

        premio = elegir_premio(rng)
        if animar:
            animar_giro(premio, rng, color)

        fichas += premio.fichas
        if premio.nombre == "Giro gratis":
            giros_gratis += 1
        elif premio.fichas == 0 and premio.nombre != "Sin premio":
            objetos.append(premio.nombre)

        if premio.nombre == "Sin premio":
            print("  Mala suerte, ¡inténtalo de nuevo!\n")
        else:
            print(pintar(f"  ¡Ganaste: {premio.nombre}!\n", premio.color, color))

    print("\n  ===== RESUMEN =====")
    print(f"  Giros realizados: {giros}")
    print(f"  Fichas finales:   {fichas}")
    if objetos:
        print("  Premios ganados:  " + ", ".join(objetos))
    print("  ¡Gracias por jugar!\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ruleta de premios de casino.")
    parser.add_argument("--fichas", type=int, default=100,
                        help="fichas iniciales (por defecto 100)")
    parser.add_argument("--semilla", type=int,
                        help="semilla aleatoria para resultados reproducibles")
    parser.add_argument("--sin-animacion", action="store_true",
                        help="mostrar el resultado sin animar la ruleta")
    parser.add_argument("--sin-color", action="store_true",
                        help="desactivar colores ANSI")
    parser.add_argument("--probabilidades", action="store_true",
                        help="mostrar la tabla de premios y salir")
    args = parser.parse_args()

    if args.probabilidades:
        mostrar_probabilidades()
        return

    rng = random.Random(args.semilla)
    color = not args.sin_color and sys.stdout.isatty()
    jugar(args.fichas, rng, animar=not args.sin_animacion, color=color)


if __name__ == "__main__":
    main()
