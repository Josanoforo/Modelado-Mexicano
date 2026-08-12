#!/usr/bin/env python3
"""Validación de tests/manifiesto.py -- alcance de dato de `--escanea` sobre
raíces NO curadas (hoy solo `downloads`), corrección MAP-1b.

Encargo CABLEADO-100 (12/ago/2026), TAREA 4.3. Contexto: ENCARGO MAP-1b
(2026-08-06, forense/notas/2026-08-06-map1b-censo-raices.md) censó las tres
raíces del proyecto y encontró que `downloads` trae, junto a payloads reales,
1763 de 2141 archivos ajenos al proyecto y 37 respaldos completos de Google
Takeout (~52 GiB, exportación personal de una cuenta) -- ese censo los
excluyó de HASHEARSE a mano, fuera del repo, con un filtro de 8 extensiones
declarado ("no se hashean -- hacerlo habría dominado el tiempo de corrida
por valor forense nulo"). `tests/manifiesto.py --escanea downloads` nunca
heredó esa protección: `RAICES_QUE_EXIGEN_GRUPO` exigía `--grupo`/`--grupo-n`
para correr sobre `downloads`, pero ese requisito solo acotaba a qué
archivos se les asignaba `url_origen`/`usado_para` -- el recorrido hasheaba
(`sha256_de`, que lee el archivo completo) y volcaba a
`data/manifiesto-staging.yaml` TODO el contenido de la carpeta, extensión
aparte, antes de que `--grupo` tuviera oportunidad de filtrar nada. Ese es
el riesgo de privacidad: un script del repo leyendo por completo archivos
personales (fotos, exports de WhatsApp/Instagram, respaldos de cuenta) que
nunca pidió ver.

La corrección (tests/manifiesto.py, `EXTENSIONES_DATO_RAICES_NO_CURADAS`):
sobre una raíz que exige --grupo, un archivo cuya extensión no está en el
mismo filtro de 8 que MAP-1b declaró se excluye ANTES de leerlo/hashearlo
-- ni se abre, ni aparece en staging, ni se nombra en el reporte (mismo
criterio que esa nota usó para no transcribir ruido personal).

Qué prueban los dos casos de este archivo:
  1. test_personal_extension_is_neither_hashed_nor_staged -- el caso que
     justifica la corrección: sobre 'downloads', un archivo de extensión
     ajena al filtro NUNCA se pasa a sha256_de() (rastreado con un stub que
     envuelve la función real) ni aparece en el staging ni en el reporte;
     un archivo de extensión conocida (.csv) sí se hashea y se stagea
     normal.
  2. test_curated_roots_are_not_extension_filtered -- que la corrección no
     se pasó de alcance: 'descargas_mx' (raíz curada, no en
     RAICES_QUE_EXIGEN_GRUPO) sigue escaneando cualquier extensión sin
     filtro -- el propio manifiesto ya registra payloads reales en formatos
     fuera de las 8 (p.ej. un .docx de cuestionario ENSANUT, citado en la
     nota MAP-1b como hueco declarado del filtro original).

Corre solo:
    python3 tests/test_manifiesto_alcance.py
"""
import argparse
import contextlib
import io
import os
import sys
import tempfile

sys.path.insert(0, "tests")
import manifiesto  # noqa: E402


def _preparar_root(tmp, nombre_raiz_no_curada, ruta_raiz_no_curada):
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "data"), exist_ok=True)
    os.makedirs(ruta_raiz_no_curada, exist_ok=True)
    with open(os.path.join(root, "data", "raices.local.yaml"), "w", encoding="utf-8") as f:
        f.write(f"{nombre_raiz_no_curada}: {ruta_raiz_no_curada}\n")
    return root


def _escanear(root, **kwargs):
    valores = {"grupo": None, "grupo_n": None, "grupo_url": None, "usado_para": None}
    valores.update(kwargs)
    args = argparse.Namespace(**valores)
    manifiesto_path, raw_dir = manifiesto.rutas(root)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        manifiesto.cmd_escanea(args, manifiesto_path, raw_dir)
    return salida.getvalue()


def test_personal_extension_is_neither_hashed_nor_staged():
    with tempfile.TemporaryDirectory() as tmp:
        downloads = os.path.join(tmp, "downloads_personal")
        root = _preparar_root(tmp, "downloads", downloads)

        with open(os.path.join(downloads, "encuesta_real.csv"), "wb") as f:
            f.write(b"col_a,col_b\n1,2\n")
        nombre_personal = "google_takeout_backup_personal.txt"
        with open(os.path.join(downloads, nombre_personal), "wb") as f:
            f.write(b"contenido personal, ajeno al proyecto\n" * 100)

        hasheados = []
        original = manifiesto.sha256_de

        def rastreado(path, *a, **kw):
            hasheados.append(os.path.basename(path))
            return original(path, *a, **kw)

        manifiesto.sha256_de = rastreado
        try:
            reporte = _escanear(root, escanea="downloads", grupo="*.csv")
        finally:
            manifiesto.sha256_de = original

        assert "encuesta_real.csv" in hasheados, "el archivo de dato (.csv) debe hashearse"
        assert nombre_personal not in hasheados, (
            "el archivo personal (.txt, fuera del filtro) NUNCA debe pasar por sha256_de -- "
            "leerlo para hashearlo ES el riesgo de privacidad que MAP-1b encontró"
        )
        assert nombre_personal not in reporte, "el nombre del archivo personal no debe aparecer en el reporte"
        assert "fuera de alcance de dato: 1" in reporte, reporte

        staging_path = os.path.join(root, "data", manifiesto.STAGING_NOMBRE)
        with open(staging_path, encoding="utf-8") as f:
            staging = f.read()
        assert "encuesta_real.csv" in staging
        assert "google_takeout_backup_personal" not in staging, (
            "el archivo fuera de alcance no debe llegar a data/manifiesto-staging.yaml"
        )
        print("  OK -- .csv hasheado y en staging; .txt personal ni leído, ni en staging, ni nombrado en el reporte.")


def test_curated_roots_are_not_extension_filtered():
    with tempfile.TemporaryDirectory() as tmp:
        descargas_mx = os.path.join(tmp, "descargas_mx_curada")
        root = _preparar_root(tmp, "descargas_mx", descargas_mx)

        with open(os.path.join(descargas_mx, "cuestionario_ensanut.docx"), "wb") as f:
            f.write(b"payload real fuera de las 8 extensiones del filtro de raices no curadas\n")

        reporte = _escanear(root, escanea="descargas_mx")

        assert "fuera de alcance de dato: 0" in reporte, (
            "descargas_mx es raiz curada (no esta en RAICES_QUE_EXIGEN_GRUPO) -- "
            "el filtro de extensión no debe aplicarle, o un payload real como un "
            ".docx quedaria invisible al manifiesto"
        )
        staging_path = os.path.join(root, "data", manifiesto.STAGING_NOMBRE)
        with open(staging_path, encoding="utf-8") as f:
            staging = f.read()
        assert "cuestionario_ensanut.docx" in staging
        print("  OK -- descargas_mx (raíz curada) escanea .docx sin filtro de extensión.")


if __name__ == "__main__":
    test_personal_extension_is_neither_hashed_nor_staged()
    print()
    test_curated_roots_are_not_extension_filtered()
    print()
    print("Los dos casos de este archivo coinciden. Detalle del hallazgo y de la")
    print("corrección: encabezado de este archivo y tests/manifiesto.py")
    print("(EXTENSIONES_DATO_RAICES_NO_CURADAS).")
