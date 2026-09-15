#!/usr/bin/env python3
"""ACTO GEN2-REACTIVOS-RESIDUALES-2 · P1 — censo derivado de los grupos ciegos de NC-0136.

Qué contesta, y por qué existe. `NC-0136` (abierta desde `ACTO
GEN2-DERIVADORES-FIX`, ampliada por `ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL`,
`PR #742`) arrastra dos objetos que hasta hoy sólo vivían como prosa: «los 81
grupos históricamente ciegos que quedan fuera del lote» y «sus residuales
acreditables». El 81 nunca había sido derivable con un comando: se heredaba de
nota en nota. Este script lo deriva, y de paso mide algo que la prosa no decía —
cuántos de esos grupos ciegos YA tienen el enunciado del reactivo publicado
dentro del propio repositorio, en la capa FD.

Definiciones, todas mecánicas (A.4, sin términos nuevos):

  universo         `data/inventario-reactivos-v1_2.tsv` + `data/inventario-reactivos-ext-v1_0.tsv`
                   — exactamente lo que `tools/busca_reactivos.py` recorre por
                   defecto bajo `--fuente ambas`, declarado en la cabecera de
                   `v1_2` como 241 591 filas.
  grupo            un valor de la columna `instrumento`. Es el grano en que la
                   cabecera de `v1_2` declaró la ceguera («102 de 116
                   instrumentos»), y por tanto el único grano en que el 81 es
                   comparable con lo ya publicado.
  ciego            el grupo tiene `texto_reactivo` vacío en el 100% de sus filas.
  lote prioritario las cinco familias que `ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL`
                   recorrió: ENVIPE, ENIF, ENCUCI, ENSAFI, ENNViH. Un grupo cae
                   en el lote por prefijo de su `instrumento`.
  fuera del lote   ciego y NO del lote. Son los 81.
  texto FD en repo filas con `texto_reactivo` no vacío para ese mismo
                   `instrumento` en `data/inventario-fd-v1_1.tsv` /
                   `data/inventario-fd-ext-v1_0.tsv` — la capa que el buscador
                   no consultaba (`ADR-215`/`ADR-216`).

El script NO extrae texto, no abre microdato, no toca ningún índice y no
escribe fuera de `--salida`. Es lectura y conteo.

Uso:
    python3 tools/censa_reactivos_ciegos.py                     # resumen a stdout
    python3 tools/censa_reactivos_ciegos.py --salida data/reactivos-ciegos-81-v1_0.tsv
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

UNIVERSO = [
    REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv",
    REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv",
]
# Las DOS capas FD no son del mismo grano, y el censo no las mezcla en silencio.
# `fd` (v1_1) viene de descriptores XLSX y da pares `variable -> enunciado` limpios.
# `fd_ext` (v1_0) viene de PDF/XLS y arrastra encabezados de tabla como si fueran
# reactivos (medido: 6 745 de sus 10 635 filas caen en tripletas
# (instrumento, variable_id, texto) repetidas; `elcos2012` es el caso extremo, con
# sus 29 filas iguales al encabezado «(2) | (1)» y CERO enunciados utilizables).
# Por eso un grupo cuya única ruta viene de `fd_ext` se rotula CANDIDATA-POR-VERIFICAR
# y no se promete como resuelto.
CAPA_FD_LIMPIA = REPO_ROOT / "data" / "inventario-fd-v1_1.tsv"
CAPA_FD_EXT = REPO_ROOT / "data" / "inventario-fd-ext-v1_0.tsv"
CAPA_FD = [CAPA_FD_LIMPIA, CAPA_FD_EXT]
MAPA19 = REPO_ROOT / "data" / "corrida0" / "mapa-demanda-19-corr-v1_0.tsv"
# El panel se sucede por versión (v1.0 -> v1.1 -> v1.2 -> …) y el censo debe leer
# la VIGENTE, no la que existía cuando se escribió este tool: apuntar a una versión
# fija haría que el censo declarara "NINGUNA-DECLARADA-HOY" sobre familias que el
# panel nuevo ya reclama, en silencio. Se resuelve por orden de nombre y se declara
# cuál se leyó (A.13). ACTO GEN2-PANEL-F6-EXPANSION-1 (ADR-518) publicó v1.2 con 27
# familias mientras este acto estaba en vuelo: ese es el caso que esta regla evita.
_PANEL_DIR = REPO_ROOT / "forense" / "prereg-duelo-v2"


def panel_f6_vigente() -> Path | None:
    """La versión más alta de F5-panel-candidatos-*.tsv presente en el árbol."""
    candidatos = sorted(_PANEL_DIR.glob("F5-panel-candidatos-v*.tsv"))
    return candidatos[-1] if candidatos else None

# Prefijos de `instrumento` de las cinco familias del lote prioritario.
LOTE = ("envipe", "enif", "encuci", "ensafi", "ennvih")


def lee_filas(path: Path) -> list[dict]:
    """TSV plano sin comillas CSV: líneas `#` fuera, luego csv.DictReader.
    Mismo convenio de lectura que tools/busca_reactivos.py::lee_filas."""
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t"))


def cuenta(paths: list[Path]) -> tuple[dict[str, list[int]], int, int]:
    """instrumento -> [filas, filas_con_texto]; más filas y archivos examinados (A.13)."""
    agg: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    filas = 0
    examinados = 0
    for p in paths:
        if not p.exists():
            continue
        examinados += 1
        for r in lee_filas(p):
            filas += 1
            k = r.get("instrumento") or "(sin-instrumento-derivable)"
            agg[k][0] += 1
            if (r.get("texto_reactivo") or "").strip():
                agg[k][1] += 1
    return agg, filas, examinados


def demanda_mapa19() -> dict[str, list[str]]:
    """instrumento plegado -> ids CORR que lo reclaman. Derivado del mapa, no tecleado.

    La columna `instrumento` del mapa es texto de mesa (`ENCIG2023`,
    `ENNViH/MxFLS_olas2-3`, y también rutas de archivo cuando la corrida no
    tiene instrumento). Se pliega a minúsculas y se compara por igualdad con el
    `instrumento` del índice: nunca por subcadena — `ACTO GEN2-F5-CIERRE-Y-PANEL-1`
    midió que la subcadena produce falsos positivos y falsos negativos en las dos
    direcciones, y aquí un falso positivo inventaría demanda que mesa no escribió.
    """
    out: dict[str, list[str]] = defaultdict(list)
    if not MAPA19.exists():
        return out
    for r in lee_filas(MAPA19):
        ins = (r.get("instrumento") or "").strip().lower()
        if ins:
            out[ins].append(r.get("corrida_id") or "?")
    return out


def demanda_panel_f6() -> dict[str, list[str]]:
    """prefijo de instrumento plegado -> familia_id del panel, sólo filas RETENIDA*.

    El panel nombra FAMILIAS (`MOCIBA`), no olas, y su `encuesta_fuente` trae
    prosa («MOCIBA (Modulo sobre Ciberacoso, INEGI)»). Se usa el primer token
    alfanumérico de `encuesta_fuente` como prefijo, y sólo para las filas que el
    panel declaró retenidas — una familia EXPUESTA no es demanda: está descartada.
    """
    out: dict[str, list[str]] = defaultdict(list)
    panel = panel_f6_vigente()
    if panel is None:
        return out
    for r in lee_filas(panel):
        if not (r.get("scope") or "").upper().startswith("RETENIDA"):
            continue
        token = ""
        for ch in (r.get("encuesta_fuente") or ""):
            if ch.isalnum():
                token += ch
            elif token:
                break
        if token:
            out[token.lower()].append(r.get("familia_id") or "?")
    return out


def censa() -> dict:
    uni, filas_uni, ex_uni = cuenta(UNIVERSO)
    fd, filas_fd, ex_fd = cuenta(CAPA_FD)
    fd_limpia, _, _ = cuenta([CAPA_FD_LIMPIA])
    d19 = demanda_mapa19()
    df6 = demanda_panel_f6()
    panel = panel_f6_vigente()

    ciegos = {k: v for k, v in uni.items() if v[1] == 0}
    fuera = {k: v for k, v in ciegos.items() if not k.lower().startswith(LOTE)}

    filas_out = []
    for k in sorted(fuera):
        fd_texto = fd.get(k, [0, 0])[1]
        fd_texto_limpio = fd_limpia.get(k, [0, 0])[1]
        reclama = list(d19.get(k.lower(), []))
        for pref, fams in df6.items():
            if k.lower().startswith(pref):
                reclama += fams
        if fd_texto_limpio > 0:
            ruta = "CABLEAR-CAPA-FD-YA-EN-REPO"
        elif fd_texto > 0:
            ruta = "CANDIDATA-FD-EXT-POR-VERIFICAR"
        else:
            ruta = "REQUIERE-FD-EN-CORPUS"
        filas_out.append({
            "instrumento": k,
            "filas_ciegas": uni[k][0],
            "fd_filas_con_texto": fd_texto,
            "fd_filas_totales": fd.get(k, [0, 0])[0],
            "fd_filas_capa_limpia": fd_texto_limpio,
            "ruta_recuperacion": ruta,
            "demanda_hoy": ",".join(reclama) if reclama else "NINGUNA-DECLARADA-HOY",
        })
    return {
        "filas": filas_out,
        "universo_filas": filas_uni,
        "universo_instrumentos": len(uni),
        "universo_archivos": ex_uni,
        "fd_filas": filas_fd,
        "fd_archivos": ex_fd,
        "ciegos": len(ciegos),
        "ciegos_en_lote": len(ciegos) - len(fuera),
        "panel_f6_leido": panel.name if panel else "AUSENTE",
    }


CABECERA = """# data/reactivos-ciegos-81-v1_0.tsv -- DERIVADO por tools/censa_reactivos_ciegos.py
# ACTO GEN2-REACTIVOS-RESIDUALES-2 (15/sep/2026, NUBE, sin corpus). NO se edita a mano: se re-genera.
#   python3 tools/censa_reactivos_ciegos.py --salida data/reactivos-ciegos-81-v1_0.tsv
# Una fila por grupo ciego (texto_reactivo vacio en el 100% de sus filas) FUERA de las cinco
# familias del lote prioritario (ENVIPE/ENIF/ENCUCI/ENSAFI/ENNViH). Es el objeto que NC-0136
# nombra como "los 81 grupos historicamente ciegos que quedan fuera del lote" -- aqui derivado.
# DOS CAPAS, DOS GRADOS DE PROMESA: `fd_filas_capa_limpia` cuenta solo el descriptor XLSX
# (data/inventario-fd-v1_1.tsv), que da pares variable->enunciado limpios. `fd_filas_con_texto`
# incluye ademas data/inventario-fd-ext-v1_0.tsv (PDF/XLS), que arrastra encabezados de tabla
# como si fueran reactivos: 6745 de sus 10635 filas caen en tripletas (instrumento, variable_id,
# texto) repetidas, y elcos2012 tiene sus 29 filas iguales al encabezado "(2) | (1)", con CERO
# enunciados utilizables. Por eso un grupo cuya unica ruta viene de esa capa sale
# CANDIDATA-FD-EXT-POR-VERIFICAR y no se presenta como resuelto.
# ALCANCE DEL NEGATIVO (A.15): `filas_ciegas` mide que el enunciado del reactivo no esta
# indexado en el universo del buscador; NO certifica que el reactivo no exista en la fuente real,
# ni suficiencia o insuficiencia cientifica de nada. La busqueda por variable_id SI cubre estos
# grupos. `demanda_hoy` se deriva por IGUALDAD de `instrumento` contra la columna homonima de
# data/corrida0/mapa-demanda-19-corr-v1_0.tsv y por prefijo contra las filas RETENIDA* de
# forense/prereg-duelo-v2/F5-panel-candidatos-v<N>.tsv (la version mas alta presente): NINGUNA-DECLARADA-HOY dice que ninguno de
# esos dos consumidores lo reclama hoy, no que el grupo sea prescindible.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", type=Path, default=None, help="TSV a escribir; sin ella, sólo resumen")
    args = ap.parse_args(argv)

    c = censa()
    cols = ["instrumento", "filas_ciegas", "fd_filas_con_texto", "fd_filas_totales",
            "fd_filas_capa_limpia", "ruta_recuperacion", "demanda_hoy"]

    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        with args.salida.open("w", encoding="utf-8", newline="") as f:
            f.write(CABECERA)
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
            w.writeheader()
            for r in c["filas"]:
                w.writerow(r)

    con_fd = [r for r in c["filas"] if r["ruta_recuperacion"] == "CABLEAR-CAPA-FD-YA-EN-REPO"]
    por_verificar = [r for r in c["filas"] if r["ruta_recuperacion"] == "CANDIDATA-FD-EXT-POR-VERIFICAR"]
    con_dem = [r for r in c["filas"] if r["demanda_hoy"] != "NINGUNA-DECLARADA-HOY"]
    print(f"UNIVERSO · {c['universo_filas']} filas · {c['universo_instrumentos']} instrumentos "
          f"· archivos examinados = {c['universo_archivos']} (A.13)")
    print(f"CAPA FD  · {c['fd_filas']} filas · archivos examinados = {c['fd_archivos']} (A.13)")
    print(f"PANEL F6 · leido: {c['panel_f6_leido']} (vigente por version, no fijado en el codigo)")
    print(f"CIEGOS   · {c['ciegos']} instrumentos ({c['ciegos_en_lote']} del lote prioritario)")
    print(f"GRUPOS FUERA DEL LOTE · {len(c['filas'])} · "
          f"{sum(r['filas_ciegas'] for r in c['filas'])} filas ciegas")
    print(f"  con texto FD limpio ya en el repo · {len(con_fd)} grupos · "
          f"{sum(r['filas_ciegas'] for r in con_fd)} filas ciegas con ruta sin corpus")
    print(f"  candidatas por fd_ext (PDF/XLS, con artefactos de encabezado) · "
          f"{len(por_verificar)} grupos · {sum(r['filas_ciegas'] for r in por_verificar)} filas ciegas")
    print(f"  reclamados hoy por mapa-19 o panel F6 · {len(con_dem)} grupos")
    for r in con_dem:
        print(f"    {r['instrumento']:<28} {r['demanda_hoy']:<22} "
              f"FD={r['fd_filas_con_texto']:>5} · {r['ruta_recuperacion']}")
    if args.salida:
        print(f"ESCRITO · {args.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
