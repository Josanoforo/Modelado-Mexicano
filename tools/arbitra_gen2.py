#!/usr/bin/env python3
"""Adaptador GEN2 del corredor R -- `tools/arbitra.py` envuelto para que cada
celda R nazca como `CALC-R-<celda>` con inputs de manifiesto.

ACTO GEN2-E7 · READINESS-2 · Pieza A, A2.

## Qué cambia respecto de `tools/arbitra.py`

`arbitra.main()` camina un marco y, por cada fila, llama
`localiza_payload(manifiesto, encuesta, ola)`: una **heurística de substring**
sobre `id` + `archivo` de cada entrada del manifiesto que devuelve una LISTA
de candidatos. Cuando devuelve más de uno, el JSON que se escribe registra
`payload_id_candidatos` -- en plural -- y la identidad del insumo de esa celda
queda sin fijar.

Este adaptador **no importa ni llama a `localiza_payload`**. El `payload_id`
de una celda sale de una sola fuente, exacta y ya versionada: la columna
`payload_id` de `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`, que es la
misma fila que declara `tabla`, `variable`, `codificacion`, `ponderador`,
`estrato` y `upm`. La ruta física de ese id la resuelve
`tests/payload_resolver.resolver_payload` -- import directo, nunca por
subproceso, mismo resolver único que `tools/corrida0.py` ya usa para todo
input `origen: manifiesto`. No hay "mejor archivo": hay el archivo del id, o
no hay corrida.

## Qué NO hace este acto

**No corre R.** R necesita corpus (microdato bajo `data/raw/`), y el corpus no
vive en NUBE: la corrida de R va a caja, en E5 o después. Este archivo entrega
la resolución, la spec y el `medir()` -- readiness, no cifras. Por eso este
acto **no** deposita ningún `data/corrida0/CALC-R-*/`: emitir la spec es una
función que se ejerce sobre un destino que el llamador da (y que los tests
ejercen sobre un directorio temporal).

`estado_resolucion` viaja SIEMPRE en la spec emitida. `RAIZ_NO_CONFIGURADA`
(el entorno no tiene esa raíz montada) y `AUSENTE` no son excepciones ni
bloqueos de este módulo: son el estado declarado de un insumo que
`corrida0.py preflight` bloqueará cuando llegue el momento de correr, con su
propio veredicto y su propio mensaje.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CODIFICACION = RAIZ / "forense" / "prereg-duelo-v2" / "codificacion-R-v1_0.tsv"

# Mismo patrón de import que `tools/corrida0.py`: el resolver único, directo.
sys.path.insert(0, str(RAIZ / "tests"))
import payload_resolver as _PR  # noqa: E402


class SinPayloadDeclarado(LookupError):
    """La celda no declara `payload_id` en la tabla de codificación. No se
    busca uno parecido: se levanta."""


def lee_codificacion(ruta: Path | None = None) -> dict[str, dict]:
    """`{id_celda: fila}` de `codificacion-R-v1_0.tsv`. La cabecera de ese
    archivo empieza con `#`; se limpia sin reescribir el archivo."""
    ruta = Path(ruta) if ruta else CODIFICACION
    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    fuera = {}
    for fila in filas:
        limpia = {(k or "").lstrip("#"): v for k, v in fila.items()}
        if limpia.get("id"):
            fuera[limpia["id"]] = limpia
    return fuera


def payload_id_de(id_celda: str, tabla_codif: dict[str, dict]) -> str:
    """El `payload_id` EXACTO de la celda. Sin fallback, sin substring, sin
    "el más parecido": si la fila no existe o la columna viene vacía, esta
    celda no tiene insumo declarado y no hay corrida que preparar."""
    fila = tabla_codif.get(id_celda)
    if fila is None:
        raise SinPayloadDeclarado(
            f"{id_celda}: sin fila en {CODIFICACION.name} -- este adaptador no "
            f"busca un payload por encuesta/ola (esa es la heuristica de "
            f"arbitra.localiza_payload, que aqui no se usa)")
    pid = (fila.get("payload_id") or "").strip()
    if not pid:
        raise SinPayloadDeclarado(
            f"{id_celda}: columna payload_id vacia en {CODIFICACION.name}")
    return pid


def resuelve_celda(id_celda: str, tabla_codif: dict[str, dict] | None = None) -> dict:
    """`{id_celda, payload_id, estado, ruta_absoluta, raiz_logica, sha256_*}`.

    Puro: no abre microdato, no escribe, no decide veredictos. El `estado` es
    el que devuelve el resolver único, tal cual."""
    tabla_codif = tabla_codif if tabla_codif is not None else lee_codificacion()
    pid = payload_id_de(id_celda, tabla_codif)
    r = _PR.resolver_payload(pid)
    return {
        "id_celda": id_celda,
        "payload_id": pid,
        "estado": r["estado"],
        "ruta_absoluta": r["ruta_absoluta"],
        "raiz_logica": r["raiz_logica"],
        "sha256_esperado": r["sha256_esperado"],
        "sha256_actual": r["sha256_actual"],
        "resuelto_por": "tests/payload_resolver.resolver_payload",
        "heuristica_usada": "NINGUNA -- payload_id exacto de "
                            f"{CODIFICACION.name}, columna payload_id",
    }


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def spec_de_celda(id_celda: str, ruta_marco: str,
                  tabla_codif: dict[str, dict] | None = None) -> dict:
    """La `spec.yaml` de `CALC-R-<celda>` como dict. El payload entra como
    input `origen: manifiesto` con su id EXACTO -- que es precisamente lo que
    `corrida0._resuelve_inputs` sabe resolver y verificar."""
    tabla_codif = tabla_codif if tabla_codif is not None else lee_codificacion()
    r = resuelve_celda(id_celda, tabla_codif)
    fila = tabla_codif[id_celda]
    calc_id = f"CALC-R-{id_celda}"
    return {
        "calc_id": calc_id,
        "spec_md": "spec.md",
        "spec_md_sha256": "PENDIENTE -- lo fija quien deposite el spec.md",
        "script": "tools/arbitra_gen2.py",
        "etiquetas": {
            "generacion": "GEN2",
            "tipo": "CORREDOR-R-ADAPTADO",
            "cuenta_gen2": "PENDIENTE-DE-MESA",
            "validacion_independiente": "NO-HECHA",
            "estado_resolucion_al_emitir": r["estado"],
            "heuristica_usada": r["heuristica_usada"],
        },
        "inputs": [
            {"id": r["payload_id"], "origen": "manifiesto"},
            {"id": "IN-CODIFICACION-R-V1-0", "origen": "repo",
             "ruta": "forense/prereg-duelo-v2/codificacion-R-v1_0.tsv",
             "sha256": _sha256(CODIFICACION)},
            {"id": "IN-MARCO", "origen": "repo", "ruta": ruta_marco,
             "sha256": _sha256(RAIZ / ruta_marco)},
        ],
        "variables": [fila.get("variable")] if fila.get("variable") else [],
        "universo": fila.get("universo_filtro") or "NO-APLICA",
        "filtros": fila.get("universo_filtro") or "NO-APLICA",
        "ponderador": fila.get("ponderador") or "NO-APLICA",
        "transformacion": fila.get("codificacion") or "NO-APLICA",
        "estimando": f"proporcion ponderada de {fila.get('variable')} "
                     f"segun la codificacion binaria declarada",
        "dependencias_materiales": ["pandas"],
        "parametros": {
            "id_celda": id_celda,
            "tabla": fila.get("tabla"),
            "estrato": fila.get("estrato"),
            "upm": fila.get("upm"),
        },
        "seed": {"aplica": False},
        "tolerancia": {
            "tipo": "flotante", "abs": 1.0e-10,
            "razon": "R no es estocastico; la tolerancia cubre el redondeo "
                     "float64 de la proporcion ponderada.",
        },
        "resultados": [
            {"id": f"RESULT-R-{id_celda}-PUNTO", "tipo": "proporcion",
             "unidad": "proporcion ponderada del universo [0,1]",
             "permite_no_estimable": True},
            {"id": f"RESULT-R-{id_celda}-EE", "tipo": "flotante",
             "unidad": "error estandar en proporcion",
             "permite_no_estimable": True},
            {"id": f"RESULT-R-{id_celda}-N", "tipo": "entero",
             "unidad": "n no ponderado", "permite_no_estimable": True},
            {"id": f"RESULT-R-{id_celda}-ESTADO", "tipo": "texto",
             "unidad": "estado del calculo (CALCULADO / motivo de abstencion)"},
        ],
    }


def medir(inputs: dict, contrato: dict) -> dict:
    """Interfaz estable de `corrida0.py`. Delega el cálculo en
    `arbitra.calcula_desde_tabla` -- la aritmética de R **no cambia** en este
    acto; lo que cambia es de dónde sale el insumo.

    NO SE EJERCE EN ESTE ACTO: R necesita corpus y va a caja (E5 o después).
    Un input de manifiesto que no esté en `COINCIDE` ya fue bloqueado por
    `preflight` antes de llegar aquí; si aun así llega, se abstiene con
    motivo en vez de calcular sobre un archivo cuya identidad no cuadra."""
    id_celda = str(contrato["parametros"]["id_celda"])
    entrada = next((e for e in inputs.values()
                    if e.get("origen") == "manifiesto"), None)
    if entrada is None:
        raise RuntimeError(
            f"{id_celda}: ningun input `origen: manifiesto` en el snapshot -- "
            f"una celda R sin payload declarado no se calcula")
    if entrada.get("estado") != "COINCIDE":
        return {
            f"RESULT-R-{id_celda}-PUNTO": None,
            f"RESULT-R-{id_celda}-EE": None,
            f"RESULT-R-{id_celda}-N": None,
            f"RESULT-R-{id_celda}-ESTADO":
                f"ABSTENCION -- payload {entrada.get('id')} en estado "
                f"{entrada.get('estado')}",
        }

    spec_mod = importlib.util.spec_from_file_location(
        "arbitra_para_gen2", RAIZ / "tools" / "arbitra.py")
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules[spec_mod.name] = mod
    spec_mod.loader.exec_module(mod)

    tabla_codif = mod.lee_codificacion()
    manifiesto = mod.carga_manifiesto()
    resultado, motivo, _adv = mod.calcula_desde_tabla(
        id_celda, tabla_codif, manifiesto, mod._correr_r())
    if resultado is None:
        return {
            f"RESULT-R-{id_celda}-PUNTO": None,
            f"RESULT-R-{id_celda}-EE": None,
            f"RESULT-R-{id_celda}-N": None,
            f"RESULT-R-{id_celda}-ESTADO": f"ABSTENCION -- {motivo}",
        }
    return {
        f"RESULT-R-{id_celda}-PUNTO": float(resultado["punto"]),
        f"RESULT-R-{id_celda}-EE": float(resultado["ee"]),
        f"RESULT-R-{id_celda}-N": int(resultado["n"]),
        f"RESULT-R-{id_celda}-ESTADO": "CALCULADO",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--resuelve", metavar="ID_CELDA",
                   help="Imprime la resolucion exacta de la celda (sin abrir microdato).")
    p.add_argument("--emite-spec", metavar="ID_CELDA",
                   help="Imprime la spec.yaml de CALC-R-<celda> como JSON.")
    p.add_argument("--marco", default="forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv",
                   help="Marco vigente que la spec declara como input.")
    args = p.parse_args()
    if args.resuelve:
        print(json.dumps(resuelve_celda(args.resuelve), ensure_ascii=False, indent=1))
        return 0
    if args.emite_spec:
        print(json.dumps(spec_de_celda(args.emite_spec, args.marco),
                         ensure_ascii=False, indent=1))
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
