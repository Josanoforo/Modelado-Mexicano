#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_compara_sha.py -- comparar_sha_manifiesto / --compara-sha
(tests/manifiesto.py). ACTO AUTOMATIZA-2-E4 · PDN-COMPARA.

E4 es la frontera epistemológica: detecta identidad de bytes, no decide
que el recurso cambió conceptualmente. Sin red, sin data/raw real -- todo
sobre tempfile.

Qué defecto real fija cada caso (mapeo directo a los códigos 0-4 del
docstring de comparar_sha_manifiesto):

  test_sha_igual_coincide
      A: archivo real idéntico al registrado -> COINCIDE, código 0.

  test_sha_distinto_mismos_miembros_cambio_de_contenido
      B: dos .zip con los mismos miembros (mismo nombre/CRC32/tamaño, vía
      un comentario de zip distinto que sólo cambia los bytes del
      contenedor) pero sha256 total distinto -> CAMBIO-DE-CONTENIDO,
      miembros_zip=IGUAL, código 1. Es el caso que Enmienda 1 existe para
      distinguir: mismo contenido, envoltura distinta.

  test_miembro_cambiado_miembros_zip_distinto
      B': un miembro del .zip nuevo trae contenido distinto (CRC/tamaño
      distinto) del registrado -> miembros_zip=DISTINTO.

  test_id_inexistente_sin_referencia_univoca
      C: id que no está en absoluto en `entradas` -> SIN-REFERENCIA-
      UNIVOCA, código 2. Sin este caso, un typo de --id se leería como
      CAMBIO-DE-CONTENIDO en vez de como "no hay contra qué comparar".

  test_id_duplicado_sin_referencia_univoca
      C': dos entradas con el mismo id en `entradas` -> SIN-REFERENCIA-
      UNIVOCA, código 2. Enmienda 4: nunca se deriva "la más reciente" --
      una referencia ambigua es tan inútil como una ausente.

  test_referencia_sin_sha256
      D: la entrada existe (id único) pero no tiene campo sha256 (entrada
      de nota/documentación) -> SIN-SHA-EN-REFERENCIA, código 3.

  test_archivo_ilegible
      E: la entrada es válida pero `ruta_archivo` no se puede leer (aquí,
      un directorio) -> ARCHIVO-NO-LEGIBLE, código 4.

Corre solo:
    python3 tests/test_compara_sha.py
"""
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, "tests")
import manifiesto  # noqa: E402


def _preparar_root(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "data", "raw"), exist_ok=True)
    return root


def _zip_minimo(ruta, miembros, comentario=b""):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with zipfile.ZipFile(ruta, "w") as zf:
        for nombre, contenido in miembros:
            zf.writestr(nombre, contenido)
        zf.comment = comentario


def test_sha_igual_coincide():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        _, raw_dir = manifiesto.rutas(root)
        registrado = os.path.join(raw_dir, "ref.zip")
        _zip_minimo(registrado, [("a.txt", b"contenido-a")])
        sha_registrado = manifiesto.sha256_de(registrado)
        entradas = [{"id": "uno", "archivo": "ref.zip", "raiz": "data_raw",
                     "sha256": sha_registrado}]

        nuevo = os.path.join(tmp, "nuevo", "descargado.zip")
        _zip_minimo(nuevo, [("a.txt", b"contenido-a")])

        r = manifiesto.comparar_sha_manifiesto(entradas, "uno", nuevo,
                                                root=root, raw_dir=raw_dir)
        assert r["estado"] == "COINCIDE", r
        assert r["codigo"] == 0, r
        assert r["sha_real"] == sha_registrado, r
        assert r["miembros_zip"] == "IGUAL", r


def test_sha_distinto_mismos_miembros_cambio_de_contenido():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        _, raw_dir = manifiesto.rutas(root)
        registrado = os.path.join(raw_dir, "ref.zip")
        _zip_minimo(registrado, [("a.txt", b"contenido-a"), ("b.txt", b"contenido-b")])
        sha_registrado = manifiesto.sha256_de(registrado)
        entradas = [{"id": "uno", "archivo": "ref.zip", "raiz": "data_raw",
                     "sha256": sha_registrado}]

        # Mismos miembros (nombre/CRC32/tamaño); comentario de zip distinto
        # basta para cambiar los bytes totales del contenedor sin tocar
        # ningún miembro.
        nuevo = os.path.join(tmp, "nuevo", "descargado.zip")
        _zip_minimo(nuevo, [("a.txt", b"contenido-a"), ("b.txt", b"contenido-b")],
                    comentario=b"re-bajado distinto")

        r = manifiesto.comparar_sha_manifiesto(entradas, "uno", nuevo,
                                                root=root, raw_dir=raw_dir)
        assert r["sha_real"] != sha_registrado, "el comentario debía cambiar el sha256 total"
        assert r["estado"] == "CAMBIO-DE-CONTENIDO", r
        assert r["codigo"] == 1, r
        assert r["miembros_zip"] == "IGUAL", r


def test_miembro_cambiado_miembros_zip_distinto():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        _, raw_dir = manifiesto.rutas(root)
        registrado = os.path.join(raw_dir, "ref.zip")
        _zip_minimo(registrado, [("a.txt", b"contenido-a"), ("b.txt", b"contenido-b")])
        sha_registrado = manifiesto.sha256_de(registrado)
        entradas = [{"id": "uno", "archivo": "ref.zip", "raiz": "data_raw",
                     "sha256": sha_registrado}]

        nuevo = os.path.join(tmp, "nuevo", "descargado.zip")
        _zip_minimo(nuevo, [("a.txt", b"contenido-a"), ("b.txt", b"CAMBIADO")])

        r = manifiesto.comparar_sha_manifiesto(entradas, "uno", nuevo,
                                                root=root, raw_dir=raw_dir)
        assert r["estado"] == "CAMBIO-DE-CONTENIDO", r
        assert r["miembros_zip"] == "DISTINTO", r


def test_id_inexistente_sin_referencia_univoca():
    entradas = [{"id": "otro", "archivo": "x.zip", "sha256": "a" * 64}]
    r = manifiesto.comparar_sha_manifiesto(entradas, "uno", "/no/importa.zip")
    assert r["estado"] == "SIN-REFERENCIA-UNIVOCA", r
    assert r["codigo"] == 2, r
    assert r["sha_manifiesto"] is None, r


def test_id_duplicado_sin_referencia_univoca():
    entradas = [
        {"id": "uno", "archivo": "x.zip", "sha256": "a" * 64},
        {"id": "uno", "archivo": "y.zip", "sha256": "b" * 64},
    ]
    r = manifiesto.comparar_sha_manifiesto(entradas, "uno", "/no/importa.zip")
    assert r["estado"] == "SIN-REFERENCIA-UNIVOCA", r
    assert r["codigo"] == 2, r


def test_referencia_sin_sha256():
    entradas = [{"id": "nota", "usado_para": "sólo documentación, sin payload"}]
    r = manifiesto.comparar_sha_manifiesto(entradas, "nota", "/no/importa.zip")
    assert r["estado"] == "SIN-SHA-EN-REFERENCIA", r
    assert r["codigo"] == 3, r
    assert r["sha_manifiesto"] is None, r


def test_archivo_ilegible():
    with tempfile.TemporaryDirectory() as tmp:
        entradas = [{"id": "uno", "archivo": "x.zip", "sha256": "a" * 64}]
        # Un directorio no es un archivo legible (IsADirectoryError es OSError).
        r = manifiesto.comparar_sha_manifiesto(entradas, "uno", tmp)
        assert r["estado"] == "ARCHIVO-NO-LEGIBLE", r
        assert r["codigo"] == 4, r
        assert r["sha_manifiesto"] == "a" * 64, r
        assert r["sha_real"] is None, r


def main():
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"OK   {nombre}")
            except AssertionError as exc:
                fallos += 1
                print(f"FAIL {nombre}: {exc}")
    if fallos:
        print(f"\n{fallos} fallo(s)")
        return 1
    print("\ntodo OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
