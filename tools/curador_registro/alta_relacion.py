#!/usr/bin/env python3
"""Alta transaccional de UNA relación nueva en las tres tablas acopladas del
registro (`relaciones.tsv`, `evidencias.tsv`, `utilidad-modelo.tsv`), más el
recifrado de `baseline.json`.

Automatiza el procedimiento humano descrito en `GUIA-CURADOR-REGISTRO.md`
§ "alta de fuente nueva en tres tablas": las tres invariantes de
`validar_baseline()` están acopladas (toda relación tiene ≥1 procedencia;
`utilidad-modelo.tsv` es proyección 1:1 de `relaciones.tsv`; la diferencia
`evidencias − relaciones` se explica solo por fusiones declaradas), así que
las tres filas nuevas se escriben en una sola operación, sobre una copia
CANDIDATA aislada, validada dos veces (candidata y post-reemplazo) antes de
tocar el registro real, con reemplazo atómico y rollback si algo falla a
mitad de camino.

Qué NO hace este script (léase antes de usarlo o de tocarlo):

* No es exclusión mutua completa contra otros escritores del registro. El
  `fcntl.flock` sobre `.alta-relacion.lock` protege solo la ventana del
  intercambio atómico final (el `os.replace` de los 8 archivos vía
  `integrate_barrido2._replace_with_rollback`); si otro proceso escribe el
  registro por fuera de este lock (p. ej. `integrate_barrido2.py` corriendo
  bajo su propio `.barrido2-integrate.lock`), esta alta no lo ve mientras
  construye la candidata. El chequeo `REGISTRO_CAMBIO_DURANTE_ALTA` detecta
  el caso más común (alguien escribió mientras se construía la candidata,
  antes de tomar el lock) pero no es una garantía general de concurrencia.
* No decide `CANDIDATA` → `CONFIRMADA` ni ninguna transición de
  `clasificacion_relacion`: ese valor viene siempre, verbatim, de
  `entrada["relacion"]["clasificacion_relacion"]` /
  `entrada["evidencia"]["clasificacion_relacion"]`. El script no interpreta,
  no mejora, no corrige ese campo.
* No trata parecido nominal como identidad. La resolución de fuente contra
  `aliases-fuentes.tsv` es coincidencia EXACTA contra el índice construido
  por `registra_cola_adquisicion.build_alias_index`, nunca por similitud de
  texto; si el nombre no aparece en ese índice, el script exige
  `alias_decidido` explícito en la entrada — nunca infiere la equivalencia.
* No trata presencia física como satisfacción semántica. Este script no
  toca disco fuera del propio registro y `data/manifiesto.yaml`: no llama a
  `via_capa2.py`, no verifica `capa3_disco_real` contra el corpus. La única
  verificación que hace sobre `id_manifiesto` es ESTRUCTURAL — que cada id
  citado exista como `id` de nivel superior en `data/manifiesto.yaml` —
  nunca afirma `capa2_manifiesto = SI` ni compara sha256/tamaño en disco.
* No convierte evidencia en parámetro de modelo: `confianza`,
  `conflicto_material`, `capa4_apertura_mapeo` vienen verbatim de la
  entrada, sin normalizar ni puntuar.
* No asigna una `N` (necesidad_id) nueva. Si la necesidad no existe en
  `necesidad-objeto-modelo.tsv`, el script para — eso es un alta de otro
  tipo (deriva de necesidad), fuera de esta operación.
* No fusiona relaciones ni admite forzar un alta duplicada: si la terna
  (necesidad, fuente, objeto) ya produce un `relacion_id` existente, el
  script para SIEMPRE. No hay bandera para saltarse este chequeo en v1.

Nota sobre escritura de TSV: este módulo NUNCA reserializa una fila que ya
existe en el archivo real. `relaciones.tsv` trae campos con comillas `"`
literales (dato, no delimitador CSV — el proyecto guarda tabuladores sin
comillas), y un round-trip por `csv.DictReader` + `csv.DictWriter` despoja
esas comillas de filas que nadie tocó (medido aquí mismo antes de escribir
este script, y ya documentado dos veces en este proyecto con
`firmas-pendientes.tsv`). Por eso el alta lee la tabla como texto plano,
conserva cada línea existente byte a byte, y solo AÑADE una línea nueva al
final, construida campo a campo contra la cabecera real del archivo.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import yaml

try:
    from .baseline import (
        ARCHIVOS_TSV, NO_DETERMINADO, leer_tsv, objeto_evidencia_id,
        procedencia_id, relacion_id, sha256, validar_baseline,
    )
    from .integrate_barrido2 import _replace_with_rollback
    from .registra_cola_adquisicion import build_alias_index
    from .sync_bootstrap import _freeze_manifest
except ImportError:  # ejecución directa (`python3 tools/curador_registro/alta_relacion.py`)
    from baseline import (
        ARCHIVOS_TSV, NO_DETERMINADO, leer_tsv, objeto_evidencia_id,
        procedencia_id, relacion_id, sha256, validar_baseline,
    )
    from integrate_barrido2 import _replace_with_rollback
    from registra_cola_adquisicion import build_alias_index
    from sync_bootstrap import _freeze_manifest


# Columnas de cada tabla NO cubiertas por los ids derivados
# (relacion_id/procedencia_id/necesidad_id/fuente_canonica_normalizada/
# objeto_evidencia_id_canonico), confirmadas contra la cabecera REAL de
# `data/curacion-registro/*.tsv` — no son una reconstrucción a ciegas.
RELACION_SUBCAMPOS = [
    "fuente_nombre", "tipo_fuente", "id_manifiesto", "sha256_fuente",
    "capa1_universo_indexado", "capa2_manifiesto", "capa3_disco_real",
    "capa4_apertura_mapeo", "clasificacion_relacion", "reason_code",
    "evidencia_ref", "evidencia_textual_breve", "confianza",
    "conflicto_material", "nota",
]
EVIDENCIA_SUBCAMPOS = [
    "procedencia_necesidad_id", "procedencia_fuente",
    "procedencia_objeto_evidencia_id", "accion_normalizacion",
    "clasificacion_relacion", "tipo_evidencia", "evidencia_ref",
    "evidencia_localizador", "variable_reactivo_tabla", "texto_evidencia",
    "unidad_observacion", "periodo", "universo_muestra", "codificacion",
    "parte_necesidad_cubierta", "parte_necesidad_no_cubierta",
    "uso_potencial_modelo", "transformacion_requerida", "incertidumbre",
    "siguiente_accion", "objeto_modelo_origen", "objeto_modelo_origen_ref",
]
UTILIDAD_SUBCAMPOS = [
    "estado_productivo", "uso_actual", "evidencia_disponible", "reserva",
    "verificacion_requerida", "requiere_decision", "decision_id",
    "siguiente_accion", "evidencia_ref",
]

RELACIONES_TSV = ARCHIVOS_TSV["relaciones"]
EVIDENCIAS_TSV = ARCHIVOS_TSV["evidencias"]
UTILIDAD_TSV = ARCHIVOS_TSV["utilidad_modelo"]
NECESIDAD_TSV = "necesidad-objeto-modelo.tsv"
ALIASES_TSV = ARCHIVOS_TSV["aliases_fuentes"]
BASELINE_JSON = "baseline.json"
LOCK_NAME = ".alta-relacion.lock"


class AltaRelacionError(Exception):
    """Aborto controlado: mensaje claro en stderr, nada escrito en el registro real."""


# ────────────────────────────── entrada ──────────────────────────────

def _cargar_entrada(path: Path) -> dict[str, Any]:
    texto = path.read_text(encoding="utf-8")
    sufijo = path.suffix.lower()
    if sufijo == ".json":
        datos = json.loads(texto)
    elif sufijo in (".yaml", ".yml"):
        datos = yaml.safe_load(texto)
    else:
        # extensión desconocida: intenta JSON, si falla intenta YAML.
        try:
            datos = json.loads(texto)
        except json.JSONDecodeError:
            datos = yaml.safe_load(texto)
    if not isinstance(datos, dict):
        raise AltaRelacionError(f"la entrada no es un mapeo YAML/JSON válido: {path}")
    return datos


# ─────────────────────── escritura sin csv.writer ───────────────────────

def _leer_tabla_cruda(path: Path) -> tuple[str, list[str], list[str]]:
    """(línea de cabecera cruda, campos, líneas de datos crudas) sin parsear."""
    texto = path.read_text(encoding="utf-8")
    lineas = texto.split("\n")
    if not lineas or not lineas[0]:
        raise AltaRelacionError(f"tabla sin cabecera: {path}")
    cabecera = lineas[0]
    resto = lineas[1:]
    if resto and resto[-1] == "":
        resto = resto[:-1]  # el archivo termina en "\n"
    return cabecera, cabecera.split("\t"), resto


def _fila_a_linea(campos: list[str], fila: dict[str, str]) -> str:
    celdas = []
    for campo in campos:
        if campo not in fila:
            raise AltaRelacionError(f"ENTRADA_INCOMPLETA: falta el campo '{campo}'")
        valor = str(fila[campo])
        if "\t" in valor or "\n" in valor or "\r" in valor:
            raise AltaRelacionError(f"celda con separador crudo en '{campo}': {valor[:60]!r}")
        celdas.append(valor)
    return "\t".join(celdas)


def _append_fila(path: Path, fila: dict[str, str]) -> None:
    """Añade UNA línea nueva a `path`, preservando cada línea existente byte
    a byte (ver nota del docstring del módulo sobre por qué NO se usa
    `csv.DictWriter` para esto)."""
    cabecera, campos, cuerpo = _leer_tabla_cruda(path)
    nueva = _fila_a_linea(campos, fila)
    path.write_text("\n".join([cabecera, *cuerpo, nueva]) + "\n", encoding="utf-8")


# ───────────────────────────── preflight ─────────────────────────────

def _resolver_fuente(entrada: dict[str, Any], aliases_path: Path) -> str:
    fuente = entrada.get("fuente_canonica_normalizada")
    alias_decidido = entrada.get("alias_decidido")
    if not fuente:
        if not alias_decidido:
            raise AltaRelacionError(
                "fuente_canonica_normalizada o alias_decidido son requeridos en la entrada."
            )
        fuente = alias_decidido
    indice = build_alias_index(leer_tsv(aliases_path))
    reconocida = fuente in indice.values()
    if not reconocida and not alias_decidido:
        raise AltaRelacionError(
            "fuente sin alias resuelto y sin `alias_decidido` en la entrada; "
            "el script no decide equivalencias por parecido."
        )
    return fuente


def _resolver_objeto(entrada: dict[str, Any], fuente: str) -> str:
    objeto = entrada.get("objeto_evidencia_id_canonico")
    if objeto:
        return objeto
    descripcion = entrada.get("descripcion_objeto")
    if not descripcion:
        raise AltaRelacionError(
            "objeto_evidencia_id_canonico ausente y descripcion_objeto también "
            "ausente: no hay cómo derivar el id del objeto de evidencia."
        )
    return objeto_evidencia_id(fuente, descripcion)


def _preflight(entrada: dict[str, Any], registro: Path) -> tuple[str, str, str, str]:
    """Devuelve (necesidad_id, fuente, objeto, relacion_id_) o levanta AltaRelacionError.

    Ningún archivo se toca en esta función: solo lectura del registro real."""
    necesidad_id = entrada.get("necesidad_id")
    if not necesidad_id:
        raise AltaRelacionError("necesidad_id es requerido en la entrada.")
    necesidades = {f.get("necesidad_id", "") for f in leer_tsv(registro / NECESIDAD_TSV)}
    if necesidad_id not in necesidades:
        raise AltaRelacionError(
            "necesidad_id no existe: nunca se asigna una N nueva automáticamente "
            f"({necesidad_id})."
        )

    fuente = _resolver_fuente(entrada, registro / ALIASES_TSV)
    objeto = _resolver_objeto(entrada, fuente)
    relacion_id_ = relacion_id(necesidad_id, fuente, objeto)

    existentes = {f.get("relacion_id", "") for f in leer_tsv(registro / RELACIONES_TSV)}
    if relacion_id_ in existentes:
        raise AltaRelacionError(
            f"relación duplicada: {relacion_id_} ya existe; una fusión/procedencia "
            "adicional no es una alta nueva y está fuera de esta operación."
        )
    return necesidad_id, fuente, objeto, relacion_id_


# ─────────────────────────── construir filas ───────────────────────────

def _fila_relacion(
    necesidad_id: str, fuente: str, objeto: str, relacion_id_: str, entrada: dict[str, Any],
) -> dict[str, str]:
    sub = entrada.get("relacion")
    if not isinstance(sub, dict):
        raise AltaRelacionError("la entrada requiere un mapeo `relacion` con las columnas propias de relaciones.tsv.")
    faltan = [c for c in RELACION_SUBCAMPOS if c not in sub]
    if faltan:
        raise AltaRelacionError(f"ENTRADA_INCOMPLETA en `relacion`: faltan columnas {faltan}")
    fila = {
        "relacion_id": relacion_id_,
        "necesidad_id": necesidad_id,
        "fuente_canonica_normalizada": fuente,
        "objeto_evidencia_id_canonico": objeto,
    }
    fila.update({c: str(sub[c]) for c in RELACION_SUBCAMPOS})
    return fila


def _fila_evidencia(
    necesidad_id: str, fuente: str, objeto: str, relacion_id_: str, entrada: dict[str, Any],
) -> dict[str, str]:
    sub = entrada.get("evidencia")
    if not isinstance(sub, dict):
        raise AltaRelacionError("la entrada requiere un mapeo `evidencia` con las columnas propias de evidencias.tsv.")
    faltan = [c for c in EVIDENCIA_SUBCAMPOS if c not in sub]
    if faltan:
        raise AltaRelacionError(f"ENTRADA_INCOMPLETA en `evidencia`: faltan columnas {faltan}")
    evidencia_ref = str(sub["evidencia_ref"])
    procedencia_id_ = procedencia_id(
        relacion_id_, str(sub["procedencia_fuente"]),
        str(sub["procedencia_objeto_evidencia_id"]), evidencia_ref,
    )
    fila = {
        "procedencia_id": procedencia_id_,
        "relacion_id": relacion_id_,
        "necesidad_id": necesidad_id,
        "fuente_canonica_normalizada": fuente,
        "objeto_evidencia_id_canonico": objeto,
    }
    fila.update({c: str(sub[c]) for c in EVIDENCIA_SUBCAMPOS})
    return fila


def _fila_utilidad(
    necesidad_id: str, fuente: str, objeto: str, relacion_id_: str, entrada: dict[str, Any],
) -> dict[str, str]:
    sub = entrada.get("utilidad")
    if not isinstance(sub, dict):
        raise AltaRelacionError("la entrada requiere un mapeo `utilidad` con las columnas propias de utilidad-modelo.tsv.")
    faltan = [c for c in UTILIDAD_SUBCAMPOS if c not in sub]
    if faltan:
        raise AltaRelacionError(f"ENTRADA_INCOMPLETA en `utilidad`: faltan columnas {faltan}")
    relacion_sub = entrada.get("relacion") or {}
    if "clasificacion_relacion" not in relacion_sub:
        raise AltaRelacionError("`relacion.clasificacion_relacion` es requerido: utilidad-modelo.tsv lo comparte.")
    fila = {
        "relacion_id": relacion_id_,
        "necesidad_id": necesidad_id,
        "fuente_canonica_normalizada": fuente,
        "objeto_evidencia_id_canonico": objeto,
        "clasificacion_relacion": str(relacion_sub["clasificacion_relacion"]),
    }
    fila.update({c: str(sub[c]) for c in UTILIDAD_SUBCAMPOS})
    return fila


def _verificar_ids_manifiesto(id_manifiesto: str, manifiesto_path: Path) -> None:
    """Chequeo ESTRUCTURAL únicamente: el id citado existe en el manifiesto.
    Nunca verifica sha256/tamaño/presencia en disco — eso es `via_capa2.py`."""
    if not id_manifiesto or id_manifiesto == NO_DETERMINADO:
        return
    citados = [i for i in id_manifiesto.split(";") if i]
    if not citados:
        return
    if not manifiesto_path.is_file():
        raise AltaRelacionError(f"id_manifiesto cita id(s) pero no existe {manifiesto_path}")
    datos = yaml.safe_load(manifiesto_path.read_text(encoding="utf-8")) or []
    conocidos = {e["id"] for e in datos if isinstance(e, dict) and "id" in e}
    faltantes = [i for i in citados if i not in conocidos]
    if faltantes:
        raise AltaRelacionError(
            f"id_manifiesto cita id(s) ausentes de {manifiesto_path.name}: {faltantes}"
        )


# ────────────────────────────── resumen ──────────────────────────────

def _imprimir_resumen(resultado: dict[str, Any]) -> None:
    print(
        f"ALTA_RELACION relacion_id={resultado.get('relacion_id')} "
        f"dry_run={resultado.get('dry_run')} applied={resultado.get('applied')}"
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True, default=str))


# ─────────────────────────────── run() ───────────────────────────────

def run(entrada_path: Path, registro: Path, *, dry_run: bool) -> dict[str, Any]:
    entrada = _cargar_entrada(entrada_path)
    necesidad_id, fuente, objeto, relacion_id_ = _preflight(entrada, registro)

    fila_relacion = _fila_relacion(necesidad_id, fuente, objeto, relacion_id_, entrada)
    fila_evidencia = _fila_evidencia(necesidad_id, fuente, objeto, relacion_id_, entrada)
    fila_utilidad = _fila_utilidad(necesidad_id, fuente, objeto, relacion_id_, entrada)

    procedencia_nota = entrada.get("procedencia_nota")
    if not procedencia_nota:
        raise AltaRelacionError("procedencia_nota es requerida en la entrada.")

    nombres = [*ARCHIVOS_TSV.values(), BASELINE_JSON]
    antes_inicio = {n: sha256(registro / n) for n in nombres}

    with tempfile.TemporaryDirectory(prefix=".alta-relacion-", dir=registro.parent) as temp_nombre:
        candidata = Path(temp_nombre) / "registro"
        candidata.mkdir()
        for nombre in nombres:
            (candidata / nombre).write_bytes((registro / nombre).read_bytes())

        _append_fila(candidata / RELACIONES_TSV, fila_relacion)
        _append_fila(candidata / EVIDENCIAS_TSV, fila_evidencia)
        _append_fila(candidata / UTILIDAD_TSV, fila_utilidad)

        template = json.loads((registro / BASELINE_JSON).read_text(encoding="utf-8"))
        procedencia = dict(template.get("procedencia") or {})
        origen_previo = procedencia.get("origen", "")
        procedencia["origen"] = f"{origen_previo} {procedencia_nota}".strip()
        template = {**template, "procedencia": procedencia}

        _freeze_manifest(candidata, template)
        resultado_validacion = validar_baseline(candidata)
        if not resultado_validacion["ok"]:
            raise AltaRelacionError(
                "BASELINE_CANDIDATO_INVALIDO:" + ";".join(resultado_validacion["errores"])
            )

        _verificar_ids_manifiesto(fila_relacion["id_manifiesto"], registro.parent / "manifiesto.yaml")

        candidata_sha = {n: sha256(candidata / n) for n in nombres}

        lock_path = registro / LOCK_NAME
        with lock_path.open("a+") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)

            antes_lock = {n: sha256(registro / n) for n in nombres}
            if antes_lock != antes_inicio:
                raise AltaRelacionError("REGISTRO_CAMBIO_DURANTE_ALTA")

            if dry_run:
                resultado = {
                    "ok": True, "dry_run": True, "applied": False,
                    "relacion_id": relacion_id_,
                    "candidato": {
                        "relacion": fila_relacion,
                        "evidencia": fila_evidencia,
                        "utilidad": fila_utilidad,
                    },
                    "validacion_candidata": resultado_validacion,
                }
                _imprimir_resumen(resultado)
                return resultado

            outputs = {registro / n: (candidata / n).read_bytes() for n in nombres}
            _replace_with_rollback(outputs, registro)

            despues = {n: sha256(registro / n) for n in nombres}
            if despues != candidata_sha:
                raise AltaRelacionError("RELECTURA_POST_INTEGRACION_DIVERGENTE")

            cambiados = sorted(n for n in nombres if antes_inicio.get(n) != despues.get(n))

            baseline_script = Path(__file__).with_name("baseline.py")
            proceso = subprocess.run(
                [sys.executable, str(baseline_script), str(registro)],
                capture_output=True, text=True,
            )
            try:
                baseline_subproceso: Any = json.loads(proceso.stdout)
            except json.JSONDecodeError:
                baseline_subproceso = {
                    "returncode": proceso.returncode,
                    "stdout": proceso.stdout,
                    "stderr": proceso.stderr,
                }

            journal = {
                "relacion_id": relacion_id_,
                "before_sha256": antes_inicio,
                "after_sha256": despues,
                "changed": cambiados,
                "baseline_subproceso": baseline_subproceso,
                "recomendacion": (
                    "Antes de abrir PR: correr `python3 tests/check.py --baseline` completo "
                    "(no solo baseline.py) — en particular T21 (biyección capa2<->capa3 en "
                    "relaciones.tsv), que esta alta puede romper si capa2_manifiesto/"
                    "capa3_disco_real no llevan el vocabulario que exige."
                ),
            }
            journal_path = registro.parent / f"alta-relacion-journal-{relacion_id_}.json"
            journal_path.write_text(
                json.dumps(journal, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            resultado = {
                "ok": True, "dry_run": False, "applied": True,
                "relacion_id": relacion_id_,
                "changed": cambiados,
                "journal_path": str(journal_path),
                "validacion_candidata": resultado_validacion,
            }
            _imprimir_resumen(resultado)
            return resultado


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entrada", type=Path, help="ruta a la entrada YAML o JSON del alta.")
    parser.add_argument("--registro", type=Path, default=Path("data/curacion-registro"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        resultado = run(args.entrada.resolve(), args.registro.resolve(), dry_run=args.dry_run)
    except Exception as exc:  # aborto controlado o inesperado: mismo trato, stderr + exit != 0
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0 if resultado.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
