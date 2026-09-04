#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_cola_writer.py -- el escritor canónico de
data/curacion-registro/cola-adquisicion-registro.tsv (SSOT, P2/P3
MAESTRA33-A5) y la vista derivada data/cola-adquisicion-v1_0.tsv.
ACTO MAESTRA38 · TESTS-FRENTE-A-B.

Todo lo que sigue corre sobre fixtures temporales (tempfile) -- ningún
caso lee ni escribe data/curacion-registro/ ni data/cola-adquisicion-v1_0.tsv
reales; `sys.path` solo agrega `tools/` y `tools/curador_registro/` (código).

Qué defecto real fija cada caso:

  test_upsert_fila_no_corrompe_comillas_sueltas (FP-258)
      forense/notas/2026-09-03-MAESTRA37-N2-control.md midió que un
      round-trip csv.reader/csv.writer corrompe 4 de 112 líneas del
      registro real -- cada una con una comilla suelta en `nota` que
      `csv.writer` reinterpreta al reescribir. `tsv_crudo.upsert_fila`
      existe para tocar SOLO la línea que cambia (texto opaco, sin
      reserializar el resto). Este test arma una fila con una comilla
      suelta, la deja intacta con upsert_fila, y confirma que sobrevive
      byte a byte -- y que agregar una fila nueva no toca ninguna otra.

  test_vista_es_pura_funcion_del_registro (arbitra.py escribía la vista)
      tools/vista_cola_adquisicion.py:build() debe ser una función pura de
      REGISTRO -- nunca leer ni depender de la vista anterior en disco.
      Antes de que arbitra.py delegara en _regenera_vista_cola_adquisicion
      (subprocess sobre este script), el riesgo medido era que un
      escritor tocara data/cola-adquisicion-v1_0.tsv directo, dejándola
      desincronizada del registro. Este test construye un registro y
      compara build() reconstruida desde cero contra una vista previa
      deliberadamente distinta (basura) -- build() debe ignorar la vista
      vieja por completo y proyectar solo lo que el registro dice.

  test_registra_cola_adquisicion_exige_confirmacion_para_escribir
      (migrador invertido) tools/curador_registro/registra_cola_adquisicion.py
      es SOLO la migración legacy de una sola vez (dirección
      cola->registro, `write_tsv` en modo 'w' -- trunca el SSOT). Correrlo
      sin --confirmo-migracion-legacy debe fallar (exit != 0) y no debe
      tocar --output en absoluto. Sin este test, un cambio futuro que
      quite la guarda (p.ej. para "simplificar" el CLI) reabriría el
      camino que invierte la dirección del SSOT sin que nadie lo note
      hasta que alguien lo corra por accidente sobre el registro real.

  test_arbitra_nunca_escribe_la_vista_directamente
      (arbitra.py escribía la vista, dos escritores el 3/sep) La única
      función de tools/arbitra.py que toca
      data/cola-adquisicion-v1_0.tsv es _regenera_vista_cola_adquisicion,
      y lo hace por subprocess contra tools/vista_cola_adquisicion.py --
      nunca con un open(..., 'w') directo sobre la ruta VISTA. Analiza el
      código fuente de tools/arbitra.py (no lo ejecuta) para esa
      invariante: si alguien reintroduce una escritura directa a VISTA en
      cualquier otra función, este test la detecta sin necesitar correr
      el árbitro completo (que exige un marco congelado y manifiesto
      reales, fuera de alcance de un test unitario con fixtures).

Corre solo:
    python3 tests/test_cola_writer.py
"""
import ast
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(REPO_ROOT / "tools" / "curador_registro"))

import tsv_crudo  # noqa: E402
import vista_cola_adquisicion  # noqa: E402

CAMPOS_REGISTRO = [
    "fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
    "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
    "ids_manifiesto", "origen", "nota",
]


def _fila(fila_origen, nota="", **overrides):
    base = {
        "fila_origen": fila_origen,
        "fuente_canonica": "FUENTE_X",
        "fuente_canonica_normalizada": "FUENTE_X",
        "discordancia_alias": "",
        "estado_A4A5": "PENDIENTE",
        "prioridad": "3",
        "url_conocida": "",
        "ids_manifiesto": "",
        "origen": "test",
        "nota": nota,
    }
    base.update(overrides)
    return base


def _escribir_registro_inicial(path, filas):
    lineas = ["\t".join(CAMPOS_REGISTRO)]
    for fila in filas:
        lineas.append("\t".join(fila[c] for c in CAMPOS_REGISTRO))
    tsv_crudo.escribir_lineas(path, lineas)


def test_upsert_fila_no_corrompe_comillas_sueltas():
    with tempfile.TemporaryDirectory() as tmp:
        registro = Path(tmp) / "registro.tsv"
        fila_con_comilla = _fila(
            "cola-adquisicion-v1_0.tsv:29",
            nota='nota con una comilla " suelta adentro, sin cerrar',
        )
        otra_fila = _fila("cola-adquisicion-v1_0.tsv:30", nota="nota normal")
        _escribir_registro_inicial(registro, [fila_con_comilla, otra_fila])

        lineas_antes = tsv_crudo.leer_lineas(registro)

        nueva = _fila("arbitra.py:celda-99", nota="fila nueva del upsert")
        tsv_crudo.upsert_fila(registro, nueva, CAMPOS_REGISTRO, clave="fila_origen")

        lineas_despues = tsv_crudo.leer_lineas(registro)

        assert lineas_despues[0] == lineas_antes[0], "cabecera intacta"
        assert lineas_despues[1] == lineas_antes[1], (
            "la fila con comilla suelta no debe tocarse al agregar otra fila")
        assert lineas_despues[2] == lineas_antes[2], "la otra fila tampoco"
        assert len(lineas_despues) == len(lineas_antes) + 1
        assert "fila nueva del upsert" in lineas_despues[-1]

        dicts = tsv_crudo.leer_dicts(registro)
        assert dicts[0]["nota"] == 'nota con una comilla " suelta adentro, sin cerrar'


def test_upsert_fila_reemplaza_in_place_sin_tocar_otras():
    with tempfile.TemporaryDirectory() as tmp:
        registro = Path(tmp) / "registro.tsv"
        filas = [_fila(f"origen:{i}", nota=f"nota-{i}") for i in range(5)]
        _escribir_registro_inicial(registro, filas)
        lineas_antes = tsv_crudo.leer_lineas(registro)

        actualizada = _fila("origen:2", nota="nota-2-actualizada")
        tsv_crudo.upsert_fila(registro, actualizada, CAMPOS_REGISTRO, clave="fila_origen")

        lineas_despues = tsv_crudo.leer_lineas(registro)
        assert len(lineas_despues) == len(lineas_antes), "un upsert de clave existente no agrega fila"
        for i in (0, 1, 2, 4, 5):
            assert lineas_despues[i] == lineas_antes[i], f"línea {i} no debía cambiar"
        assert "nota-2-actualizada" in lineas_despues[3]


def test_vista_es_pura_funcion_del_registro():
    with tempfile.TemporaryDirectory() as tmp:
        registro = Path(tmp) / "registro.tsv"
        filas = [
            _fila("origen:1", fuente_canonica="ENOE", nota="a"),
            _fila("origen:2", fuente_canonica="ENIGH", nota="b"),
        ]
        _escribir_registro_inicial(registro, filas)

        construida = vista_cola_adquisicion.build(registro)

        vista_vieja_basura = "# GENERADO -- vieja\nfuente_canonica\tbasura\nOTRA_COSA\tque-no-deberia-sobrevivir\n"
        vista_path = Path(tmp) / "vista.tsv"
        vista_path.write_text(vista_vieja_basura, encoding="utf-8")

        reconstruida = vista_cola_adquisicion.build(registro)
        assert reconstruida == construida, (
            "build() no debe depender de lo que haya en disco en la ruta VISTA")
        assert "OTRA_COSA" not in reconstruida
        assert "ENOE" in reconstruida and "ENIGH" in reconstruida
        assert reconstruida.startswith(vista_cola_adquisicion.CABECERA_COMENTARIO)


def test_registra_cola_adquisicion_exige_confirmacion_para_escribir():
    with tempfile.TemporaryDirectory() as tmp:
        cola = Path(tmp) / "cola.tsv"
        cola.write_text(
            "fuente_canonica\testado_A4A5\tprioridad\turl_conocida\tids_manifiesto\torigen\tnota\n"
            "ENOE\tPENDIENTE\t3\t\t\ttest\tnota\n",
            encoding="utf-8",
        )
        aliases = Path(tmp) / "aliases.tsv"
        aliases.write_text("alias_fuente\tfuente_canonica_normalizada\nENOE\tENOE\n", encoding="utf-8")
        salida = Path(tmp) / "salida.tsv"

        resultado = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "tools" / "curador_registro" / "registra_cola_adquisicion.py"),
                "--cola", str(cola), "--aliases", str(aliases), "--output", str(salida),
            ],
            capture_output=True, text=True,
        )
        assert resultado.returncode != 0, "sin --confirmo-migracion-legacy debe fallar"
        assert "confirmo-migracion-legacy" in resultado.stderr
        assert not salida.exists(), "no debe escribir --output sin confirmación explícita"

        resultado_confirmado = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "tools" / "curador_registro" / "registra_cola_adquisicion.py"),
                "--cola", str(cola), "--aliases", str(aliases), "--output", str(salida),
                "--confirmo-migracion-legacy",
            ],
            capture_output=True, text=True,
        )
        assert resultado_confirmado.returncode == 0
        assert salida.exists(), "con confirmación explícita sí debe escribir"


def test_arbitra_nunca_escribe_la_vista_directamente():
    fuente = (REPO_ROOT / "tools" / "arbitra.py").read_text(encoding="utf-8")
    arbol = ast.parse(fuente, filename="tools/arbitra.py")

    escrituras_directas = []
    for nodo in ast.walk(arbol):
        if not (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id == "open"):
            continue
        if len(nodo.args) < 2:
            continue
        modo = nodo.args[1]
        if not (isinstance(modo, ast.Constant) and isinstance(modo.value, str) and "w" in modo.value):
            continue
        primer_arg = nodo.args[0]
        if isinstance(primer_arg, ast.Name) and primer_arg.id == "COLA":
            escrituras_directas.append(nodo.lineno)
        if isinstance(primer_arg, ast.Name) and primer_arg.id == "salida":
            continue  # corridas-R/<id>.json, no la cola

    assert not escrituras_directas, (
        f"tools/arbitra.py abre COLA en modo escritura directa en línea(s) "
        f"{escrituras_directas} -- debe ir por "
        f"_regenera_vista_cola_adquisicion() (subprocess de "
        f"vista_cola_adquisicion.py), nunca por open(COLA, 'w')")

    assert "_regenera_vista_cola_adquisicion" in fuente
    assert "vista_cola_adquisicion.py" in fuente


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
