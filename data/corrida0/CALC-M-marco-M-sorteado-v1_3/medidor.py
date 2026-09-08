#!/usr/bin/env python3
"""Medidor de CALC-M-marco-M-sorteado-v1_3 -- corredor M envuelto para GEN2.

ACTO GEN2-E7 · READINESS-2 · A1. Lo que este medidor hace y lo que NO hace:

  HACE   marco vigente (`marco-M-sorteado-v1_3.tsv`, input `origen: repo`,
         bytes verificados por `preflight`) -> una fila por celda ->
         `tools/emite_m.py::emite_celda` -> RESULT-M-<CELDA>-P / -GRADO-DD.

  NO HACE  no llama `emite_m.camina()` (el `regenera_todos()` historico:
         escribe `corridas-M/M-<id>.json`, saltea lo ya existente y depende
         de un marco CABLEADO -- `v1_1`); no escribe un solo byte fuera de
         lo que `corrida0.py run` sella; no abre `corridas-M/`,
         `corridas-R/`, `corridas-L/` ni `agregado_v1_3.py`.

`ciego_a_R` no se DECLARA aqui: se VERIFICA. Un `sys.addaudithook` sobre el
evento `open` registra toda apertura del proceso durante la emision y
RESULT-M-CIEGO-A-R reporta el conteo de aperturas prohibidas -- si alguna
ruta cae bajo `corridas-R/` (o bajo el resto del legado GEN1) el medidor
levanta y `run` no sella. La cadena de la afirmacion es el hook, no el
comentario.

Este acto NO produce un numero nuevo del modelo: cada `p` que sale de aqui
es el que `milpa/src/emisor.py` ya emitia. Lo nuevo es que nace con spec,
contrato, snapshot de inputs, recibo y sello.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]

# El legado GEN1 que NINGUNA parte de este medidor puede abrir. Es la lista
# que el check LEGACY-NO-LEIDO de la Pieza B tambien usa -- misma prohibicion,
# comprobada en dos lados: aqui en la corrida, alla en el Go/No-Go.
LEGADO_PROHIBIDO = (
    "forense/prereg-duelo-v2/corridas-R",
    "forense/prereg-duelo-v2/corridas-M",
    "forense/prereg-duelo-v2/corridas-L",
    "forense/prereg-duelo-v2/agregado_v1_3.py",
    "forense/prereg-duelo-v2/agregado-v1_3-resultado.json",
)

MARCO_VIGENTE = "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv"
COLUMNA_ELEGIBLE = "elegible_v1_1"

# Los campos del registro de `emite_celda` que ESTE medidor consume. No se
# comprueba el esquema completo contra `corridas-M/M-TRA-M-01.json` como hace
# `emite_m.camina()`: ese archivo es legado GEN1 y LEGACY-NO-LEIDO lo prohibe.
# Se comprueba lo que se usa, que es lo unico que este CALC puede afirmar.
CAMPOS_QUE_ESTE_MEDIDOR_CONSUME = {"p", "grado_DD", "estado_M", "ciego_a_R"}


class AperturaProhibida(RuntimeError):
    """Una apertura bajo el legado GEN1 durante la emision. No es un aviso."""


class _Auditor:
    """Registra aperturas y marca las prohibidas. Se arma ANTES de importar
    `emite_m` y de tocar el marco: si el propio import abriera legado, se ve.

    `sys.addaudithook` es irreversible por diseno de CPython -- por eso el
    hook no decide nada por su cuenta: solo acumula. Quien levanta es el
    medidor, y solo mientras `activo` este encendido (fuera de la ventana de
    emision, `corrida0.py` abre lo que necesite sin que esto le aplique)."""

    def __init__(self) -> None:
        self.activo = False
        self.aperturas = 0
        self.prohibidas: list[str] = []

    def __call__(self, evento: str, args) -> None:
        if not self.activo or evento != "open":
            return
        crudo = args[0]
        if isinstance(crudo, (bytes, bytearray)):
            crudo = crudo.decode("utf-8", "replace")
        if not isinstance(crudo, str):
            return  # descriptor numerico: no es una ruta que podamos juzgar
        self.aperturas += 1
        plana = crudo.replace("\\", "/")
        for prohibido in LEGADO_PROHIBIDO:
            if prohibido in plana:
                self.prohibidas.append(plana)
                return


def _texto(entrada: dict) -> str:
    """Los bytes que el SHA verificado identifica -- no una relectura de disco.
    `_resuelve_inputs` de `corrida0.py` ya los trae en el snapshot (P1)."""
    crudo = entrada.get("bytes")
    if crudo is None:
        raise RuntimeError(
            f"input {entrada.get('id')!r} llego sin `bytes` -- este medidor "
            f"solo consume insumos `origen: repo` del snapshot resuelto")
    return crudo.decode("utf-8")


def _importa_emite_m(entrada: dict):
    """Importa `tools/emite_m.py` por ruta y COMPRUEBA que el archivo del
    arbol es el mismo que la spec declara. La comprobacion no sobra: entre el
    `preflight` y este import no hay nada que lo garantice."""
    ruta = RAIZ / "tools" / "emite_m.py"
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != entrada["sha256"]:
        raise RuntimeError(
            f"tools/emite_m.py cambio bajo la corrida: snapshot="
            f"{entrada['sha256']} arbol={real}")
    spec = importlib.util.spec_from_file_location("emite_m_gen2", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _id_result(id_celda: str, sufijo: str) -> str:
    return f"RESULT-M-{id_celda}-{sufijo}"


def medir(inputs: dict, contrato: dict) -> dict:
    auditor = _Auditor()
    sys.addaudithook(auditor)

    marco_txt = _texto(inputs["IN-MARCO-M-SORTEADO-V1-3"])
    filas = list(csv.DictReader(io.StringIO(marco_txt), delimiter="\t"))

    auditor.activo = True
    try:
        emite_m = _importa_emite_m(inputs["IN-EMITE-M"])
        reglas_por_id = {r.id: r for r in emite_m.cargar_reglas()}
        lineas_tramite = emite_m.RUTA_TRAMITE.read_text(
            encoding="utf-8").splitlines()
        candidatos = emite_m.leer_por_id(emite_m.RUTA_CANDIDATOS_V1_1)

        valores: dict = {}
        emitidas, ps = 0, []
        for fila in filas:
            id_celda = fila["id"]
            if (fila.get(COLUMNA_ELEGIBLE) or "").strip().upper() != "SI":
                valores[_id_result(id_celda, "P")] = None
                valores[_id_result(id_celda, "GRADO-DD")] = "NO-ELEGIBLE"
                continue
            registro = emite_m.emite_celda(
                fila, reglas_por_id, lineas_tramite, candidatos,
                fuente_acto=str(contrato["parametros"]["fuente_acto"]),
                marco_nombre=Path(MARCO_VIGENTE).name)
            faltan = CAMPOS_QUE_ESTE_MEDIDOR_CONSUME - set(registro)
            if faltan:
                raise RuntimeError(
                    f"{id_celda}: el registro de emite_celda no trae "
                    f"{sorted(faltan)}")
            valores[_id_result(id_celda, "P")] = float(registro["p"])
            valores[_id_result(id_celda, "GRADO-DD")] = str(registro["grado_DD"])
            emitidas += 1
            ps.append(round(float(registro["p"]), 12))
    finally:
        auditor.activo = False

    if auditor.prohibidas:
        raise AperturaProhibida(
            "el corredor M abrio legado GEN1 durante la emision: "
            + ", ".join(sorted(set(auditor.prohibidas))))

    valores["RESULT-M-N-CELDAS"] = len(filas)
    valores["RESULT-M-N-EMITIDAS"] = emitidas
    # El numero del paso 3 (A5): cuantos valores DISTINTOS de `p` produce el
    # marco. Si es menor que el numero de celdas, la unidad de celda vigente
    # (regla x ola x instrumento) esta emitiendo el MISMO punto para celdas
    # que el marco distingue. Este medidor lo MIDE; no lo decide.
    valores["RESULT-M-P-DISTINTOS"] = len(set(ps))
    valores["RESULT-M-CIEGO-A-R"] = (
        f"VERIFICADO-POR-AUDITHOOK: {auditor.aperturas} aperturas durante la "
        f"emision, 0 bajo {' | '.join(LEGADO_PROHIBIDO)}")
    valores["RESULT-M-MARCO"] = MARCO_VIGENTE
    return valores
