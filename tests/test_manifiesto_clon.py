#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_manifiesto_clon.py -- un clon git = un objeto en `--escanea`
(tests/manifiesto.py). ACTO MAESTRA38-CENSO-CLON.

Defecto real que fija (forense/hallazgos.md, 6/sep/2026): un clon completo
de un repositorio (L2-LISTA) dejado dentro de una carpeta escaneada se
trataba archivo por archivo -- 136 residuos del clon contados como
"nuevos" en el censo del día. `--escanea` recorre árboles arbitrarios de
disco, no solo carpetas de datos; una carpeta que contiene `.git/` no es
un montón de archivos sueltos, es UN objeto (el checkout de un commit) y
así debe reportarse.

test_carpeta_con_git_es_un_clon_no_archivos_sueltos
    Reproduce la condición del hallazgo con una fixture mínima (tempfile,
    sin red ni corpus): una carpeta con `.git/HEAD` (un sha de 40 hex,
    como lo dejaría cualquier checkout) y tres archivos -- uno ya en
    data/manifiesto.yaml, dos no. Exige exactamente lo que COMMIT-2
    declara: 1 línea CLON en el reporte, 0 archivos nuevos, 1 ya
    registrado (listado bajo el CLON, no suelto) -- y que el staging no
    reciba ninguna entrada por los archivos del clon.

Corre solo:
    python3 tests/test_manifiesto_clon.py
"""
import argparse
import contextlib
import io
import os
import sys
import tempfile

sys.path.insert(0, "tests")
import manifiesto  # noqa: E402

_HEAD_SHA = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"


def _preparar_root(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "data", "raw"), exist_ok=True)
    return root


def _escanear(root, **kwargs):
    valores = {"escanea": RAIZ_INTEGRADA, "grupo": None, "grupo_n": None,
               "grupo_url": None, "usado_para": None}
    valores.update(kwargs)
    args = argparse.Namespace(**valores)
    manifiesto_path, raw_dir = manifiesto.rutas(root)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        manifiesto.cmd_escanea(args, manifiesto_path, raw_dir)
    return salida.getvalue()


RAIZ_INTEGRADA = manifiesto.RAIZ_INTEGRADA


def test_carpeta_con_git_es_un_clon_no_archivos_sueltos():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        manifiesto_path, raw_dir = manifiesto.rutas(root)

        clon = os.path.join(raw_dir, "l2-lista")
        os.makedirs(os.path.join(clon, ".git"), exist_ok=True)
        with open(os.path.join(clon, ".git", "HEAD"), "w", encoding="utf-8") as f:
            f.write(_HEAD_SHA + "\n")

        registrado = os.path.join(clon, "registrado.csv")
        with open(registrado, "wb") as f:
            f.write(b"contenido-registrado")
        for nombre in ("nuevo_a.csv", "nuevo_b.csv"):
            with open(os.path.join(clon, nombre), "wb") as f:
                f.write(nombre.encode())

        sha_registrado = manifiesto.sha256_de(registrado)
        cabecera, _ = manifiesto.leer_manifiesto(manifiesto_path)
        manifiesto.escribir_manifiesto(manifiesto_path, cabecera, [{
            "id": "l2-lista-registrado",
            "archivo": os.path.join("l2-lista", "registrado.csv"),
            "raiz": RAIZ_INTEGRADA,
            "sha256": sha_registrado,
            "tamano_bytes": os.path.getsize(registrado),
            "fecha_descarga": "2026-09-01",
            "entorno_descarga": "prueba",
            "descargado_por": "prueba",
            "usado_para": "prueba",
            "url_origen": "https://example.mx/x",
        }])

        salida = _escanear(root)

        assert "CLONES (1):" in salida, salida
        assert f"CLON l2-lista · commit {_HEAD_SHA} · 3 archivos" in salida, salida
        assert "nuevos: 0" in salida, salida
        assert "ya registrados: 1" in salida, salida
        assert "l2-lista-registrado" in salida, salida
        assert "nuevo_a.csv" not in salida
        assert "nuevo_b.csv" not in salida

        staging_path = os.path.join(os.path.dirname(manifiesto_path),
                                     manifiesto.STAGING_NOMBRE)
        _, staging = manifiesto.leer_manifiesto(staging_path)
        assert staging == [], (
            f"el staging no debe recibir entradas por archivos del clon, quedó: {staging}")


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
