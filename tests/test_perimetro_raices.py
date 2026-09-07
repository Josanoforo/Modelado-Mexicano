#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_perimetro_raices.py -- perímetro físico de raíces (ACTO
AUTOMATIZA-1-E1 · PERIMETRO-FISICO-DE-RAICES, 7/sep/2026,
`forense/encargos/2026-09-07-AUTOMATIZA-1-E1-PERIMETRO-FISICO.md`).

Hace cumplir por código que sólo `data_raw` y `descargas_mx` son raíces sobre
las que un automatismo general del corpus puede hacer I/O físico (caminar,
listar, `exists`/`stat`, hashear, abrir). `downloads` puede seguir existiendo
como nombre histórico (entradas antiguas del manifiesto -- hoy ninguna --,
`data/raices.local.yaml`), pero queda fuera por diseño: contuvo información
personal ajena al proyecto.

Siete casos, sin tocar el árbol real (todo bajo `tempfile.TemporaryDirectory`,
mismo patrón que `tests/test_manifiesto_alcance.py`/`tests/test_corpus.py`):
  1-3. `raiz_escaneable()` sobre las tres raíces conocidas.
  4. `--escanea downloads` se rechaza antes de resolver físicamente la raíz:
     código de salida != 0, imprime `RAIZ_NO_ESCANEABLE`, cero `os.walk`
     (rastreado con un monkeypatch que envuelve la función real).
  5. `--verifica` sobre una entrada de fixture `raiz: downloads` clasifica
     `FUERA_DE_PERIMETRO` sin llamar `os.path.exists` sobre esa ruta.
  6. `tests/corpus.py::c1_huerfanos` con `downloads` configurada en
     `raices.local.yaml` no la camina (no aparece en el resultado, cero
     `os.walk` sobre su carpeta) mientras sí camina una raíz escaneable.
  7. `tests/corpus.py::c3_entradas_sin_archivo` no llama `os.path.exists`
     sobre una entrada de raíz `downloads` y no la cuenta como AUSENTE.

Corre solo:
    python3 tests/test_perimetro_raices.py
"""
import argparse
import contextlib
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402
import manifiesto  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _preparar_root(tmp, nombre_raiz_externa, ruta_raiz_externa):
    """Mismo patrón que test_manifiesto_alcance.py/test_corpus.py."""
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "data"), exist_ok=True)
    os.makedirs(ruta_raiz_externa, exist_ok=True)
    with open(os.path.join(root, "data", "raices.local.yaml"), "w", encoding="utf-8") as f:
        f.write(f"{nombre_raiz_externa}: {ruta_raiz_externa}\n")
    return root


def prueba_raiz_escaneable_constantes():
    afirma(manifiesto.raiz_escaneable("data_raw") is True,
           "raiz_escaneable('data_raw') debe ser True")
    afirma(manifiesto.raiz_escaneable("descargas_mx") is True,
           "raiz_escaneable('descargas_mx') debe ser True")
    afirma(manifiesto.raiz_escaneable("downloads") is False,
           "raiz_escaneable('downloads') debe ser False")


def prueba_escanea_downloads_rechazado():
    with tempfile.TemporaryDirectory() as tmp:
        downloads = os.path.join(tmp, "downloads_personal")
        root = _preparar_root(tmp, "downloads", downloads)
        with open(os.path.join(downloads, "algo.csv"), "wb") as f:
            f.write(b"col_a,col_b\n1,2\n")

        manifiesto_path, raw_dir = manifiesto.rutas(root)
        args = argparse.Namespace(escanea="downloads", grupo=None, grupo_n=None,
                                   grupo_url=None, usado_para=None)

        walks = []
        walk_original = os.walk

        def walk_rastreado(top, *a, **kw):
            walks.append(top)
            return walk_original(top, *a, **kw)

        os.walk = walk_rastreado
        salida = io.StringIO()
        codigo = 0
        try:
            with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(salida):
                try:
                    manifiesto.cmd_escanea(args, manifiesto_path, raw_dir)
                except SystemExit as exc:
                    codigo = exc.code
        finally:
            os.walk = walk_original

        reporte = salida.getvalue()
        afirma(codigo not in (0, None),
               f"--escanea downloads debe salir con código != 0, salió {codigo!r}")
        afirma("RAIZ_NO_ESCANEABLE" in reporte,
               f"debe imprimir RAIZ_NO_ESCANEABLE: {reporte!r}")
        afirma(walks == [],
               f"cero llamadas a os.walk esperadas antes del rechazo, hubo {walks}")


def prueba_verifica_downloads_fuera_de_perimetro():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "repo")
        os.makedirs(os.path.join(root, "data", "raw"), exist_ok=True)
        manifiesto_path, raw_dir = manifiesto.rutas(root)
        with open(manifiesto_path, "w", encoding="utf-8") as f:
            f.write(
                "- id: fixture_downloads\n"
                "  archivo: recuerdo_personal.txt\n"
                "  raiz: downloads\n"
                "  sha256: " + ("0" * 64) + "\n"
                "  tamano_bytes: 10\n"
            )

        llamadas = []
        exists_original = os.path.exists

        def exists_rastreado(p):
            llamadas.append(p)
            return exists_original(p)

        os.path.exists = exists_rastreado
        salida = io.StringIO()
        try:
            with contextlib.redirect_stdout(salida):
                try:
                    manifiesto.cmd_verifica(argparse.Namespace(id=[]), manifiesto_path, raw_dir)
                except SystemExit:
                    pass
        finally:
            os.path.exists = exists_original

        reporte = salida.getvalue()
        afirma("FUERA_DE_PERIMETRO" in reporte,
               f"debe clasificar FUERA_DE_PERIMETRO: {reporte!r}")
        afirma(not any("recuerdo_personal.txt" in p for p in llamadas),
               f"cero exists() sobre la ruta física de downloads, hubo: {llamadas}")


def prueba_c1_no_camina_downloads():
    with tempfile.TemporaryDirectory() as tmp:
        downloads = os.path.join(tmp, "downloads_personal")
        root = _preparar_root(tmp, "downloads", downloads)
        raw_dir = os.path.join(root, "data", "raw")
        os.makedirs(raw_dir, exist_ok=True)
        with open(os.path.join(downloads, "residuo_personal.bin"), "wb") as f:
            f.write(b"contenido personal ajeno al proyecto\n")
        with open(os.path.join(raw_dir, "dato_del_proyecto.bin"), "wb") as f:
            f.write(b"dato real del proyecto\n")

        entradas, raw_dir_cargado = corpus.cargar(root)

        walks = []
        walk_original = os.walk

        def walk_rastreado(top, *a, **kw):
            walks.append(top)
            return walk_original(top, *a, **kw)

        os.walk = walk_rastreado
        try:
            huerfanos = corpus.c1_huerfanos(root, entradas, raw_dir_cargado)
        finally:
            os.walk = walk_original

        afirma("downloads" not in huerfanos,
               f"'downloads' no debe aparecer en el resultado de c1_huerfanos: {huerfanos.keys()}")
        afirma(not any(os.path.normpath(downloads) == os.path.normpath(w) for w in walks),
               f"cero os.walk sobre la carpeta de downloads, se caminó: {walks}")
        afirma(any(os.path.normpath(raw_dir) == os.path.normpath(w) for w in walks),
               f"data_raw (escaneable) sí debe caminarse -- si no, la prueba no discrimina nada: {walks}")


def prueba_c3_no_llama_exists_sobre_downloads():
    with tempfile.TemporaryDirectory() as tmp:
        downloads = os.path.join(tmp, "downloads_personal")
        root = _preparar_root(tmp, "downloads", downloads)
        raw_dir = os.path.join(root, "data", "raw")
        os.makedirs(raw_dir, exist_ok=True)
        manifiesto_path = os.path.join(root, "data", "manifiesto.yaml")
        with open(manifiesto_path, "w", encoding="utf-8") as f:
            f.write(
                "- id: fixture_downloads_ausente\n"
                "  archivo: no_deberia_mirarse.txt\n"
                "  raiz: downloads\n"
                "  sha256: " + ("1" * 64) + "\n"
                "  tamano_bytes: 5\n"
            )
        entradas, raw_dir_cargado = corpus.cargar(root)

        llamadas = []
        exists_original = os.path.exists

        def exists_rastreado(p):
            llamadas.append(p)
            return exists_original(p)

        os.path.exists = exists_rastreado
        try:
            sin_archivo = corpus.c3_entradas_sin_archivo(root, entradas, raw_dir_cargado)
        finally:
            os.path.exists = exists_original

        afirma(sin_archivo == [],
               f"la entrada de 'downloads' no debe contabilizarse como AUSENTE: {sin_archivo}")
        afirma(not any("no_deberia_mirarse.txt" in p for p in llamadas),
               f"cero exists() sobre la ruta de downloads, hubo: {llamadas}")


def main():
    prueba_raiz_escaneable_constantes()
    prueba_escanea_downloads_rechazado()
    prueba_verifica_downloads_fuera_de_perimetro()
    prueba_c1_no_camina_downloads()
    prueba_c3_no_llama_exists_sobre_downloads()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_perimetro_raices.py: 5 pruebas (7 puntos del encargo), 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
