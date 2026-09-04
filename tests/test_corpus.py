#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_corpus.py -- fixture mínimo para la frontera misma-raíz/otra-raíz
de tests/corpus.py::c1_huerfanos (ENMIENDA 2, FP-259(iii), MAESTRA37-INFRA-2,
2026-09-03).

Regla de este proyecto (fallback declarado): "solo si el corpus real no
contiene ningún caso que permita verificar la frontera misma-raíz/otra-raíz,
añadir un fixture mínimo de una fila para ese único propósito". Medido contra
el corpus real de este repo al momento de este cambio: 0 casos genuinos de
`presente_bajo_otra_raiz` (ningún huérfano tiene un sha256 registrado bajo
una raíz DISTINTA a la suya) -- así que esa rama positiva no se puede
verificar contra datos reales. Este archivo es ese fixture, y nada más:
no reemplaza la medición contra el corpus real (ver `python3 tests/corpus.py`),
solo cubre la rama que el corpus real no ejercita hoy.

Casos, ambos con el MISMO contenido físico (mismo sha256), para aislar
exactamente la frontera que la ENMIENDA 2 introduce:
  1. Un archivo huérfano bajo una raíz DISTINTA a la que declara la entrada
     registrada con ese sha256 -> presente_bajo_otra_raiz, citando la raíz
     que sí lo declara (data_raw).
  2. Un archivo huérfano bajo la MISMA raíz (data_raw) que la entrada
     registrada con ese sha256 -> sin_registro, NUNCA presente_bajo_otra_raiz
     -- la regla central de la ENMIENDA: un duplicado dentro de la misma
     raíz no es "presente en otra raíz".

Corre solo:
    python3 tests/test_corpus.py
"""
import hashlib
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402
import manifiesto  # noqa: E402


def _preparar_root(tmp, nombre_raiz_externa, ruta_raiz_externa):
    """Mismo patrón que tests/test_manifiesto_alcance.py::_preparar_root --
    un root de repo aislado bajo tempfile.TemporaryDirectory, con
    data/raices.local.yaml declarando una única raíz externa. data_raw
    (RAIZ_INTEGRADA) se resuelve por código vía manifiesto.rutas(root), no
    por este archivo -- solo hace falta crear el directorio."""
    root = os.path.join(tmp, "repo")
    raw_dir = os.path.join(root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(ruta_raiz_externa, exist_ok=True)
    with open(os.path.join(root, "data", "raices.local.yaml"), "w", encoding="utf-8") as f:
        f.write(f"{nombre_raiz_externa}: {ruta_raiz_externa}\n")
    return root, raw_dir


def test_frontera_misma_raiz_vs_otra_raiz():
    with tempfile.TemporaryDirectory() as tmp:
        nombre_raiz_b = "raiz_ext"
        raiz_b_dir = os.path.join(tmp, "raiz_ext_dir")
        root, raw_dir = _preparar_root(tmp, nombre_raiz_b, raiz_b_dir)

        contenido = b"contenido de fixture para c1_huerfanos, frontera misma-raiz/otra-raiz\n"
        sha_real = hashlib.sha256(contenido).hexdigest()

        # Entrada registrada bajo raíz A (data_raw, por convención -- sin
        # campo 'raiz'), declarando UN archivo con este sha256.
        archivo_registrado = "registrado/archivo_a.bin"
        os.makedirs(os.path.join(raw_dir, "registrado"), exist_ok=True)
        with open(os.path.join(raw_dir, archivo_registrado), "wb") as f:
            f.write(contenido)

        with open(os.path.join(root, "data", "manifiesto.yaml"), "w", encoding="utf-8") as f:
            f.write(
                "- id: fixture_registrado\n"
                f"  archivo: {archivo_registrado}\n"
                f"  sha256: {sha_real}\n"
            )

        # Caso 1: huérfano bajo raíz B (distinta a la registrada, data_raw)
        # -> debe clasificar presente_bajo_otra_raiz.
        huerfano_otra_raiz = "huerfano_en_b.bin"
        with open(os.path.join(raiz_b_dir, huerfano_otra_raiz), "wb") as f:
            f.write(contenido)

        # Caso 2: huérfano bajo raíz A (data_raw, MISMA que la registrada)
        # -> debe clasificar sin_registro, no presente_bajo_otra_raiz.
        huerfano_misma_raiz = "huerfano_en_a.bin"
        with open(os.path.join(raw_dir, huerfano_misma_raiz), "wb") as f:
            f.write(contenido)

        entradas, raw_dir_cargado = corpus.cargar(root)
        assert len(entradas) == 1, "el fixture declara exactamente una entrada registrada"

        huerfanos = corpus.c1_huerfanos(root, entradas, raw_dir_cargado)

        # -- Caso 1: raíz B (raiz_ext) --
        clasif_b = huerfanos[nombre_raiz_b]
        assert clasif_b["sin_registro"] == [], clasif_b
        assert len(clasif_b["presente_bajo_otra_raiz"]) == 1, clasif_b
        rel_b, otras_raices_b = clasif_b["presente_bajo_otra_raiz"][0]
        assert rel_b == os.path.normpath(huerfano_otra_raiz)
        assert otras_raices_b == [manifiesto.RAIZ_INTEGRADA], (
            "el huérfano en raíz B debe citar data_raw como la raíz que SÍ lo declara, "
            f"no solo el hecho del match: otras_raices_b={otras_raices_b}"
        )

        # -- Caso 2: raíz A (data_raw) --
        clasif_a = huerfanos[manifiesto.RAIZ_INTEGRADA]
        assert clasif_a["presente_bajo_otra_raiz"] == [], (
            "un duplicado DENTRO de la misma raíz nunca debe clasificar como "
            f"presente_bajo_otra_raiz -- regla central de la ENMIENDA: {clasif_a}"
        )
        assert len(clasif_a["sin_registro"]) == 1, clasif_a
        rel_a, anotacion_a = clasif_a["sin_registro"][0]
        assert rel_a == os.path.normpath(huerfano_misma_raiz)
        assert anotacion_a == "sin_registro_pero_duplica_contenido_de(fixture_registrado)", anotacion_a

        # -- Total: 2 huérfanos en el fixture, uno en cada categoría --
        total = sum(
            len(v["presente_bajo_otra_raiz"]) + len(v["sin_registro"])
            for v in huerfanos.values()
        )
        assert total == 2, huerfanos

        print("  OK -- huérfano bajo raíz distinta a la registrada -> presente_bajo_otra_raiz "
              "(cita data_raw); huérfano bajo la MISMA raíz que la entrada registrada -> "
              "sin_registro (nunca presente_bajo_otra_raiz).")


if __name__ == "__main__":
    test_frontera_misma_raiz_vs_otra_raiz()
    print()
    print("El caso de este archivo coincide. Detalle del hallazgo y de la corrección:")
    print("tests/corpus.py (ENMIENDA 2 en la cabecera; c1_huerfanos / _indice_por_sha_y_raiz).")
