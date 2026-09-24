#!/usr/bin/env python3
"""`tools/consulta.py` -- una fila del repo en UNA linea, sin abrir la vista.

ACTO GEN2-TUBERIA-RENDIMIENTO-1 · P2
(`forense/encargos/2026-09-24-GEN2-TUBERIA-RENDIMIENTO-1.md`).

Defecto que ataca (D-14): una sesion que necesita un numero abre
`resultados.tsv` (65k filas) o `manifiesto.yaml` (15k+ lineas) completos y
se come el contexto. Este tool lee por lector CSV en streaming y se detiene
en la primera fila que casa; imprime una linea `clave=valor` separada por
` · `. Nunca escribe (D-23): no hay cache ni indice en disco.

Subcomandos:
  result  <RESULT-id>   data/corrida0/resultados.tsv
  corrida <CALC-id>     data/corrida0/corridas.tsv
  celda   <celda-id>    data/curacion-registro/celdas-d/<id>.yaml, o fila de
                        data/corrida0/marcador-segmento.tsv
  payload <id>          data/manifiesto.yaml
  fp      <FP-id>       forense/firmas-pendientes.tsv
  nc      <NC-id>       forense/no-corrido.tsv

Salida: 0 si encontro la fila; 1 con `NO-ENCONTRADO · <archivo> · filas
examinadas=N` (A.4/A.13) si no.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "data/corrida0/resultados.tsv"
CORRIDAS = RAIZ / "data/corrida0/corridas.tsv"
MARCADOR = RAIZ / "data/corrida0/marcador-segmento.tsv"
CELDAS_D = RAIZ / "data/curacion-registro/celdas-d"
MANIFIESTO = RAIZ / "data/manifiesto.yaml"
FIRMAS = RAIZ / "forense/firmas-pendientes.tsv"
NO_CORRIDO = RAIZ / "forense/no-corrido.tsv"

# `corridas.tsv` trae campos (listas de ids) de mas de 128 KB, el limite
# por defecto del modulo csv.
csv.field_size_limit(sys.maxsize)

_YAML_SAFE_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

CAMPOS = {
    "result": ("resultado_id", ["valor", "unidad", "tipo", "corrida_id", "sello",
                                "estado", "generacion", "cuenta_gen2",
                                "validacion_independiente", "n_usos"]),
    "corrida": ("corrida_id", ["spec_id", "estado", "generacion", "cuenta_gen2",
                               "sello", "n_resultados", "resultado_replay",
                               "contexto_replay", "fecha"]),
    "marcador": ("celda_id", ["tipo", "instrumento", "estado", "emision", "piso",
                              "R", "M", "resultado_id", "decision_ref",
                              "prospectividad"]),
    "fp": ("id", ["estado", "creado", "firmada_en", "ejecutada_en", "qué_se_firma"]),
    "nc": ("id", ["estado", "acto", "pr", "razon", "sucesor"]),
}
CAMPOS_CELDA = ["estimando", "unidad_objetivo", "estado_decidibilidad",
                "veredicto", "champion_actual", "estado_operativo",
                "fecha_adjudicacion", "commit_adjudicacion"]
CAMPOS_PAYLOAD = ["archivo", "sha256", "tamano_bytes", "fecha_descarga",
                  "estado_reserva"]
MAX_COL = 160


def _corta(v) -> str:
    s = " ".join(str(v).split())
    return s if len(s) <= MAX_COL else s[:MAX_COL - 1] + "…"


def _linea(clave: str, fila: dict, campos: list[str]) -> str:
    partes = [clave] + [f"{c}={_corta(fila.get(c, ''))}" for c in campos
                        if fila.get(c) not in (None, "")]
    return " · ".join(partes)


def busca_tsv(ruta: Path, col: str, valor: str) -> tuple[dict | None, int]:
    """Primera fila con `col == valor`; salta comentarios `#` de cabecera."""
    n = 0
    with ruta.open(encoding="utf-8", newline="") as fh:
        lineas = (l for l in fh if not l.startswith("#"))
        for fila in csv.DictReader(lineas, delimiter="\t"):
            n += 1
            if fila.get(col) == valor:
                return fila, n
    return None, n


def _no_encontrado(ruta: Path, n: int) -> int:
    print(f"NO-ENCONTRADO · {ruta.relative_to(RAIZ)} · filas examinadas={n}")
    return 1


def consulta_tsv(tipo: str, ruta: Path, ident: str) -> int:
    col, campos = CAMPOS[tipo]
    fila, n = busca_tsv(ruta, col, ident)
    if fila is None:
        return _no_encontrado(ruta, n)
    print(_linea(ident, fila, campos))
    return 0


def consulta_celda(ident: str) -> int:
    ruta = CELDAS_D / f"{ident}.yaml"
    if ruta.is_file():
        doc = yaml.load(ruta.read_text(encoding="utf-8"), Loader=_YAML_SAFE_LOADER) or {}
        c = doc.get("celda_d") or {}
        fila = dict(c)
        fila["n_candidatos"] = len(c.get("candidatos") or [])
        print(_linea(ident, fila, CAMPOS_CELDA + ["n_candidatos"]))
        return 0
    return consulta_tsv("marcador", MARCADOR, ident)


def consulta_payload(ident: str) -> int:
    doc = yaml.load(MANIFIESTO.read_text(encoding="utf-8"), Loader=_YAML_SAFE_LOADER) or []
    entradas = doc if isinstance(doc, list) else []
    for e in entradas:
        if isinstance(e, dict) and str(e.get("id")) == ident:
            print(_linea(ident, e, CAMPOS_PAYLOAD))
            return 0
    return _no_encontrado(MANIFIESTO, len(entradas))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("tipo", choices=["result", "corrida", "celda", "payload", "fp", "nc"])
    ap.add_argument("id")
    a = ap.parse_args(argv)
    if a.tipo == "result":
        return consulta_tsv("result", RESULTADOS, a.id)
    if a.tipo == "corrida":
        return consulta_tsv("corrida", CORRIDAS, a.id)
    if a.tipo == "celda":
        return consulta_celda(a.id)
    if a.tipo == "payload":
        return consulta_payload(a.id)
    if a.tipo == "fp":
        return consulta_tsv("fp", FIRMAS, a.id)
    return consulta_tsv("nc", NO_CORRIDO, a.id)


if __name__ == "__main__":
    sys.exit(main())
