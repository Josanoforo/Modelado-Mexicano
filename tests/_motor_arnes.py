#!/usr/bin/env python3
"""Arnés mínimo compartido por `tests/test_motor_*.py`.

No es un framework: es la mitad de uno, a propósito. El repo no usa `pytest` ni
`unittest` en ningún test, y meter una dependencia de estilo nueva junto con la
primera rebanada del motor mezclaría dos decisiones distintas en un commit.
Cada `test_motor_*.py` corre solo, imprime una línea por prueba y devuelve
código de salida.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


class Arnes:
    def __init__(self, titulo):
        self.titulo = titulo
        self.errores = []
        self.corridas = 0
        self.saltadas = 0

    def prueba(self, nombre, fn):
        self.corridas += 1
        try:
            fn()
        except _Salto as s:
            self.corridas -= 1
            self.saltadas += 1
            print(f"  {nombre}: skip -- {s}")
        except AssertionError as e:
            self.errores.append(f"{nombre}: {e}")
            print(f"  {nombre}: FAIL -- {e}")
        except Exception as e:  # noqa: BLE001 -- un error inesperado ES un fallo
            self.errores.append(f"{nombre}: {type(e).__name__}: {e}")
            print(f"  {nombre}: FAIL -- {type(e).__name__}: {e}")
        else:
            print(f"  {nombre}: ok")

    def cerrar(self):
        print()
        if self.errores:
            print(f"{self.titulo}: {len(self.errores)} fallo(s)")
            return 1
        print(f"{self.titulo}: {self.corridas} prueba(s) ok, "
              f"{self.saltadas} saltada(s)")
        return 0


class _Salto(Exception):
    pass


def saltar(razon):
    raise _Salto(razon)


def lanza(excepcion, fn, *args, **kwargs):
    """Afirma que `fn` lanza `excepcion`. Devuelve la excepción capturada."""
    try:
        fn(*args, **kwargs)
    except excepcion as e:
        return e
    except Exception as e:  # noqa: BLE001
        raise AssertionError(
            f"esperaba {excepcion.__name__}, llegó {type(e).__name__}: {e}"
        ) from None
    raise AssertionError(f"esperaba {excepcion.__name__} y no lanzó nada")


def igual(a, b, que=""):
    if a != b:
        raise AssertionError(f"{que} esperaba {b!r}, obtuvo {a!r}".strip())


def cierto(cond, que=""):
    if not cond:
        raise AssertionError(que or "condición falsa")


def codigo_efectivo(ruta):
    """El código de un `.py` SIN comentarios ni literales de texto.

    Necesario porque estas pruebas son estructurales ("ninguna fuente del motor
    llama a X"), y un docstring que MENCIONA X las haría fallar por hablar del
    tema. Se quita con `tokenize`, no con expresiones regulares: una regex
    sobre comillas se equivoca con las triples y con las anidadas.
    """
    import io
    import tokenize

    with open(ruta, encoding="utf-8") as fh:
        fuente = fh.read()
    piezas = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(fuente).readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            piezas.append(tok.string)
    except tokenize.TokenError:  # pragma: no cover
        return fuente
    return " ".join(piezas)
