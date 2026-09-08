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

ENMIENDA (ACTO AUTOMATIZA-1-E1 · PERIMETRO-FISICO-DE-RAICES, 7/sep/2026):
`downloads` queda fuera del perímetro físico por diseño (`raiz_escaneable()`,
`tests/manifiesto.py`) -- `--escanea downloads` se rechaza ANTES de resolver
la raíz, mucho antes de que el filtro de extensión de MAP-1b tuviera
oportunidad de aplicarse. MAP-1b deja de tener superficie de ataque sobre
esta raíz: ya no hay ningún camino por el que `sha256_de()` pueda leer un
archivo bajo `downloads`, con o sin filtro de extensión, porque la raíz
misma ya no se recorre. El primer caso de este archivo se reescribe para
afirmar ese rechazo -- no se borra, porque el defecto de privacidad que
motivó MAP-1b sigue siendo el hecho histórico que da contexto a la nueva
frontera (`RAICES_QUE_EXIGEN_GRUPO` sigue viva pero inalcanzable desde
`--escanea`, ver `tests/manifiesto.py`).

Qué prueban los tres casos de este archivo:
  1. test_downloads_es_rechazada_antes_del_filtro_de_extension -- desde la
     frontera física, `--escanea downloads` se rechaza (`RAIZ_NO_ESCANEABLE`,
     código != 0) antes de resolver la raíz físicamente: cero llamadas a
     `sha256_de()`, cero staging, cero recorrido de directorio (rastreado con
     un monkeypatch de `os.walk` que envuelve la función real). El caso
     histórico de MAP-1b (archivo personal vs. archivo de dato) ya no aplica
     porque ninguno de los dos llega a examinarse.
  2. test_curated_roots_are_not_extension_filtered -- que la corrección no
     se pasó de alcance: 'descargas_mx' (raíz curada, escaneable, no en
     RAICES_QUE_EXIGEN_GRUPO) sigue escaneando cualquier extensión sin
     filtro -- el propio manifiesto ya registra payloads reales en formatos
     fuera de las 8 (p.ej. un .docx de cuestionario ENSANUT, citado en la
     nota MAP-1b como hueco declarado del filtro original).
  3. test_lock_propio_excluido_del_escaneo (ACTO GEN2-T11 · RUTINAS-FIX,
     8/sep/2026) -- el lock de escritura de la propia raíz compartida
     (ADR-399 D6, `ruta_lock_manifiesto`) vive desde entonces DENTRO de la
     raíz que --escanea recorre: sin exclusión, cada corrida se stagea a sí
     misma como candidato "nuevo" (medido en el censo real del 2026-09-08,
     `forense/censo-raiz/2026-09-08.txt`). `LOCK_PROPIO_BASENAME` lo excluye
     antes de clasificar, igual que un clon.

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


def _escanear_esperando_rechazo(root, **kwargs):
    """Igual que _escanear, pero para una raíz que se espera RAIZ_NO_ESCANEABLE
    (ACTO AUTOMATIZA-1-E1): captura stdout+stderr y el código de SystemExit en
    vez de dejarlo propagar. Devuelve (reporte, codigo)."""
    valores = {"grupo": None, "grupo_n": None, "grupo_url": None, "usado_para": None}
    valores.update(kwargs)
    args = argparse.Namespace(**valores)
    manifiesto_path, raw_dir = manifiesto.rutas(root)
    salida = io.StringIO()
    codigo = 0
    with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(salida):
        try:
            manifiesto.cmd_escanea(args, manifiesto_path, raw_dir)
        except SystemExit as exc:
            codigo = exc.code
    return salida.getvalue(), codigo


def test_downloads_es_rechazada_antes_del_filtro_de_extension():
    with tempfile.TemporaryDirectory() as tmp:
        downloads = os.path.join(tmp, "downloads_personal")
        root = _preparar_root(tmp, "downloads", downloads)

        with open(os.path.join(downloads, "encuesta_real.csv"), "wb") as f:
            f.write(b"col_a,col_b\n1,2\n")
        nombre_personal = "google_takeout_backup_personal.txt"
        with open(os.path.join(downloads, nombre_personal), "wb") as f:
            f.write(b"contenido personal, ajeno al proyecto\n" * 100)

        hasheados = []
        sha256_original = manifiesto.sha256_de

        def sha256_rastreado(path, *a, **kw):
            hasheados.append(os.path.basename(path))
            return sha256_original(path, *a, **kw)

        walks = []
        walk_original = os.walk

        def walk_rastreado(top, *a, **kw):
            walks.append(top)
            return walk_original(top, *a, **kw)

        manifiesto.sha256_de = sha256_rastreado
        os.walk = walk_rastreado
        try:
            reporte, codigo = _escanear_esperando_rechazo(root, escanea="downloads", grupo="*.csv")
        finally:
            manifiesto.sha256_de = sha256_original
            os.walk = walk_original

        assert codigo not in (0, None), f"--escanea downloads debe rechazarse (código != 0), salió {codigo!r}"
        assert "RAIZ_NO_ESCANEABLE" in reporte, reporte
        assert hasheados == [], (
            "ni el .csv de dato ni el .txt personal deben pasar por sha256_de() -- "
            f"la raíz se rechaza antes de resolver nada físico, se hashearon: {hasheados}"
        )
        assert walks == [], f"cero recorrido de directorio antes del rechazo, se caminó: {walks}"
        assert "encuesta_real.csv" not in reporte and nombre_personal not in reporte, (
            "ningún nombre físico debe aparecer en el reporte de una raíz rechazada"
        )

        staging_path = os.path.join(root, "data", manifiesto.STAGING_NOMBRE)
        assert not os.path.exists(staging_path), (
            "una raíz rechazada no debe producir ningún archivo de staging"
        )
        print("  OK -- 'downloads' se rechaza (RAIZ_NO_ESCANEABLE) antes de resolver la raíz: "
              "cero hashes, cero os.walk, cero staging -- el .csv de dato y el .txt personal "
              "por igual, MAP-1b ya no tiene superficie de ataque sobre esta raíz.")


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


def test_lock_propio_excluido_del_escaneo():
    """El lock de escritura de la raíz compartida (ADR-399 D6,
    tests/manifiesto.py::ruta_lock_manifiesto) vive DESDE ENTONCES dentro de
    la raíz que --escanea recorre -- sin esta exclusión cada corrida se
    stagea a sí misma como candidato "nuevo" (medido en el censo real del
    2026-09-08, forense/censo-raiz/2026-09-08.txt: uno de los 4 "nuevos" era
    el propio .manifiesto.lock, con mtime = hora de la propia corrida --
    ACTO GEN2-T11 · RUTINAS-FIX, pieza 2)."""
    with tempfile.TemporaryDirectory() as tmp:
        descargas_mx = os.path.join(tmp, "descargas_mx_curada")
        root = _preparar_root(tmp, "descargas_mx", descargas_mx)

        with open(os.path.join(descargas_mx, ".manifiesto.lock"), "wb") as f:
            f.write(b"")
        with open(os.path.join(descargas_mx, "payload_real.csv"), "wb") as f:
            f.write(b"col_a,col_b\n1,2\n")

        reporte = _escanear(root, escanea="descargas_mx")

        assert "nuevos: 1" in reporte, reporte
        assert "LOCK-PROPIO (excluido): 1" in reporte, reporte
        assert ".manifiesto.lock" in reporte, (
            "el nombre del lock sí puede citarse -- no es dato personal, "
            "a diferencia de FUERA DE ALCANCE (MAP-1b)"
        )

        staging_path = os.path.join(root, "data", manifiesto.STAGING_NOMBRE)
        with open(staging_path, encoding="utf-8") as f:
            staging = f.read()
        assert ".manifiesto.lock" not in staging, staging
        assert "payload_real.csv" in staging
        print("  OK -- .manifiesto.lock (lock propio de la raíz compartida) se excluye "
              "del escaneo: 0 nuevos por él, 0 entradas de staging, línea informativa "
              "LOCK-PROPIO (excluido).")


if __name__ == "__main__":
    test_downloads_es_rechazada_antes_del_filtro_de_extension()
    print()
    test_curated_roots_are_not_extension_filtered()
    print()
    test_lock_propio_excluido_del_escaneo()
    print()
    print("Los tres casos de este archivo coinciden. Detalle del hallazgo y de la")
    print("corrección: encabezado de este archivo y tests/manifiesto.py")
    print("(EXTENSIONES_DATO_RAICES_NO_CURADAS, LOCK_PROPIO_BASENAME).")
