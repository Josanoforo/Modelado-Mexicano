#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/marcador_segmento.py` -- deriva `data/corrida0/marcador-segmento.tsv`.

ACTO GEN2-MARCADOR-REDISENO-1 (encargo + adenda de dirección, 19/sep/2026),
sobre el diseño de mesa `MARCADOR-SEGMENTO-diseno-direccion-v1_0` +
delta v1.1 (firma de mesa 17/sep/2026, §9).

CERO CIFRAS NUEVAS. Este tool no mide nada: lee valores YA SELLADOS en
cuatro fuentes y los proyecta a una tabla derivada:

  1. `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv` (ADR-536) --
     97 celdas NACIONALES/compuestas del censo de identidad emisor<->arbitro.
  2. `milpa/tramite-ola5-propuesta-v0.yaml`, los SIETE ids con sufijo
     `_ejes_` -- celdas MARGINALES del árbitro por eje.
  3. `data/curacion-registro/celdas-d/*.yaml` con `champion_actual: C2` --
     las 20 celdas de CRUCE piloteadas (ADR-538/ADR-542), con sus RESULT
     sellados leídos de `data/corrida0/CALC-*-EMISIONES-0001/resultados.json`.
  4. `data/corrida0/decisiones.tsv` -- el veto de mesa a los cuatro
     `CALC-PISOS-*` (objeto `veto:pisos-866`, 19/sep/2026): si la fila
     existe, esos cuatro directorios se EXCLUYEN POR NOMBRE como fuente de
     piso, incondicionalmente, sin leer su contenido.

Piso: el diseño (§9(2)) dicta MARGINAL-SIN-INTERACCION para las celdas de
cruce ya piloteadas (así lo declara `regla_composicion` en la celda-D misma)
y PERSISTENCIA(t-1) por eje donde exista un CALC sellado -- hoy NINGUNO
pasa la guardia: los cuatro `CALC-PISOS-*` están vetados por nombre, y
`CALC-TRIADA-B-PISO-0001` serializa sus RESULT con otro formato de id
(`RESULT-TBP-*`, no uno por-celda-D) -- no calza con lo que este lector
une por identidad exacta, y se reporta SIN-PISO en vez de forzar el parseo.

Salida: `data/corrida0/marcador-segmento.tsv` (`# DERIVADO -- NO EDITAR`)
y, en P2, `milpa/estimadores-por-segmento.yaml` con las celdas adoptadas.

Uso:
    python3 tools/marcador_segmento.py            # deriva e imprime resumen
    python3 tools/marcador_segmento.py --escribe   # además escribe los TSV/YAML
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CENSO_TSV = RAIZ / "forense" / "notas" / "2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv"
PROPUESTA_OLA5 = RAIZ / "milpa" / "tramite-ola5-propuesta-v0.yaml"
CELDAS_D_DIR = RAIZ / "data" / "curacion-registro" / "celdas-d"
DECISIONES_TSV = RAIZ / "data" / "corrida0" / "decisiones.tsv"
CORRIDA0_DIR = RAIZ / "data" / "corrida0"
MARCADOR_TSV = CORRIDA0_DIR / "marcador-segmento.tsv"
ESTIMADORES_YAML = RAIZ / "milpa" / "estimadores-por-segmento.yaml"

# Los cuatro CALC-PISOS-* que el veto de mesa 19/sep/2026 (objeto
# `veto:pisos-866`) excluye por nombre -- ver decisiones.tsv.
CALC_PISOS_VETADOS = [
    "CALC-PISOS-ENVIPE2024-EJES-0001",
    "CALC-PISOS-ENCIG2023-EJES-0001",
    "CALC-PISOS-ENCIG2023-EJES-0001-v1_1",
    "CALC-PISOS-ENIF2021-EJES-0001",
]

# NC-0328: "edad x dominio" dentro de tramite.evasion_norma_ejes_envipe2025
# corrió exploratoriamente sin COMMIT-1 -- reserva consumida sin piloto.
NC_0328_PAR_CONSUMIDO = ("tramite.evasion_norma_ejes_envipe2025",
                          frozenset({"edad", "dominio_urbano_rural"}))

COLS = [
    "celda_id", "tipo", "regla_o_eje_origen", "instrumento",
    "eje_o_par", "categoria", "unidad_dato", "unidad_objetivo",
    "estado", "piso", "R", "R_ic95inf", "R_ic95sup",
    "M", "IC95_inf", "IC95_sup", "tipo_incertidumbre",
    "resultado_id", "decision_ref", "emisor_vs_arbitro", "fuente",
]


def _yaml(ruta: Path):
    return yaml.safe_load(ruta.read_text(encoding="utf-8"))


def _lee_decisiones() -> dict:
    if not DECISIONES_TSV.exists():
        return {}
    out = {}
    with DECISIONES_TSV.open(encoding="utf-8") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            out[f["objeto"]] = f
    return out


# ── (2) universo NACIONAL/compuesto -- censo ADR-536 (97 filas) ───────────

def filas_nacionales() -> list[dict]:
    filas = []
    with CENSO_TSV.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    for f in csv.DictReader(lineas, delimiter="\t"):
        veredicto = f["veredicto"]
        emisor_vs_arbitro = "EMISOR=ARBITRO" if veredicto == "IDENTICO" else veredicto
        filas.append({
            "celda_id": f"NAC::{f['regla']}::{f['salida']}::{f['celda']}",
            "tipo": "NACIONAL",
            "regla_o_eje_origen": f["regla"],
            "instrumento": f["instrumento_ola_arbitro"],
            "eje_o_par": "NACIONAL",
            "categoria": f["celda"],
            "unidad_dato": "NO-DECLARADO-EN-CENSO",
            "unidad_objetivo": "persona",
            "estado": "IDENTICO" if veredicto == "IDENTICO" else "DIAGNOSTICO",
            "piso": "NO-APLICA",
            "R": f["p_arbitro"], "R_ic95inf": "", "R_ic95sup": "",
            "M": f["p_emisor"] if veredicto == "IDENTICO" else "",
            "IC95_inf": "", "IC95_sup": "",
            "tipo_incertidumbre": "NO-DECLARADO-EN-CENSO",
            "resultado_id": "",
            "decision_ref": "marcador:emisor-fuera",
            "emisor_vs_arbitro": emisor_vs_arbitro,
            "fuente": f["origen_linea"],
        })
    return filas


# ── (1) universo MARGINAL -- los 7 ids `_ejes_` de la propuesta ola5 ──────

def _camina_ejes(nodo):
    """Genérico: cualquier dict con `eje` + `celdas` es un eje marginal,
    sin importar la profundidad de anidamiento (`ejes:` plano o
    `desenlaces: {principal, secundario}: {ejes: [...]}`)."""
    if isinstance(nodo, dict):
        if "eje" in nodo and "celdas" in nodo:
            yield nodo
        for v in nodo.values():
            yield from _camina_ejes(v)
    elif isinstance(nodo, list):
        for e in nodo:
            yield from _camina_ejes(e)


# ── piso de persistencia v2 -- nota de dirección 19/sep/2026 (post-cierre) ──
# `GEN2-PISOS-REJILLA-CLI-1` (Codex, rama codex/gen2-marcador-adopcion-cli-1)
# va a sellar `CALC-PISOS-*-EJES-0002`: un RESULT POR CELDA (no la "TABLA"
# serializada de los cuatro `-EJES-0001` vetados), con sufijos de id
# `-P` (punto), `-IC-LO`/`-IC-HI` (IC95), `-N` (tamaño) y `-DEN-W`
# (denominador ponderado). Hoy NINGÚN `CALC-PISOS-*-EJES-0002` existe en
# el árbol (`git ls-tree -r --name-only origin/main -- data/corrida0/ | grep
# EJES-0002` → vacío) -- este lector se deja LISTO para unir por identidad
# exacta contra ese esquema, pero la convención exacta del `resultado_id`
# no puede verificarse contra un CALC real todavía. Se documenta la
# convención asumida (ver `_id_piso_v2`) y se prueba con un fixture
# SINTÉTICO (`tests/test_marcador_segmento.py::t_piso_v2_fixture_sintetico`).
# Cuando REJILLA fusione, basta re-correr `marcador_segmento.py`; si el id
# real difiere de la convención asumida, ajustar solo `_id_piso_v2` --el
# resto del lector (unión por identidad, nunca la rama "tabla", exclusión
# de los vetados) no cambia.

def _id_piso_v2(eje: str, categoria: str, sufijo: str) -> str:
    """Convención ASUMIDA (no verificada contra un CALC real -- ver nota
    arriba): `RESULT-PISOS-<EJE>-<CATEGORIA>-<SUFIJO>`, con eje/categoria
    en mayúsculas y separadores no alfanuméricos vueltos `_`."""
    def _slug(s: str) -> str:
        return "".join(c if c.isalnum() else "_" for c in str(s)).strip("_").upper()
    return f"RESULT-PISOS-{_slug(eje)}-{_slug(categoria)}-{sufijo}"


def _calc_pisos_v2_dirs() -> list[Path]:
    """Directorios `CALC-PISOS-*-EJES-0002` (o cualquier sucesor no
    vetado) presentes en el árbol, excluyendo SIEMPRE los cuatro
    `CALC_PISOS_VETADOS` por nombre -- el veto de mesa manda
    incondicionalmente, sin importar el sufijo de versión."""
    if not CORRIDA0_DIR.exists():
        return []
    return [p for p in sorted(CORRIDA0_DIR.glob("CALC-PISOS-*"))
            if p.is_dir() and p.name not in CALC_PISOS_VETADOS]


def _lee_piso_v2(eje: str, categoria: str) -> dict | None:
    """Une por identidad exacta (eje, categoría) contra un RESULT por celda
    en cualquier `CALC-PISOS-*` no vetado. Nunca lee la rama "tabla"
    (formato de los cuatro `-EJES-0001` vetados): si `resultados.json` no
    trae los cinco ids esperados (`-P`/`-IC-LO`/`-IC-HI`/`-N`/`-DEN-W`)
    para esta celda, no hay match y se devuelve `None` -- no se fuerza el
    parseo."""
    id_p = _id_piso_v2(eje, categoria, "P")
    id_lo = _id_piso_v2(eje, categoria, "IC-LO")
    id_hi = _id_piso_v2(eje, categoria, "IC-HI")
    id_n = _id_piso_v2(eje, categoria, "N")
    id_den = _id_piso_v2(eje, categoria, "DEN-W")
    for calc_dir in _calc_pisos_v2_dirs():
        rj = calc_dir / "resultados.json"
        if not rj.exists():
            continue
        try:
            resultados = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(resultados, dict) or id_p not in resultados:
            continue
        if id_lo not in resultados or id_hi not in resultados:
            continue
        return {
            "punto": resultados[id_p],
            "ic95inf": resultados.get(id_lo),
            "ic95sup": resultados.get(id_hi),
            "n": resultados.get(id_n),
            "den_w": resultados.get(id_den),
            "resultado_id": id_p,
            "fuente": calc_dir.name,
        }
    return None


def filas_marginales(vetados: bool) -> tuple[list[dict], dict]:
    d = _yaml(PROPUESTA_OLA5)
    reglas_ejes = [r for r in d["reglas_propuestas"] if "_ejes_" in r.get("id", "")]
    filas = []
    n_ejes = 0
    for r in reglas_ejes:
        for bloque in _camina_ejes(r):
            n_ejes += 1
            eje = bloque.get("eje")
            for c in (bloque.get("celdas") or []):
                piso_v2 = None if vetados else _lee_piso_v2(eje, c.get("celda"))
                if piso_v2:
                    estado, piso = "SOLO-PISO", "PERSISTENCIA(t-1)"
                else:
                    estado = "SIN-PISO"
                    piso = "VETADO:CALC-PISOS" if vetados else "SIN-CALC-SELLADO-POR-EJE"
                filas.append({
                    "celda_id": f"MARG::{r['id']}::{eje}::{c.get('celda')}",
                    "tipo": "MARGINAL",
                    "regla_o_eje_origen": r["id"],
                    "instrumento": r.get("payload", ""),
                    "eje_o_par": eje,
                    "categoria": c.get("celda"),
                    "unidad_dato": _unidad_dato(r["id"]),
                    "unidad_objetivo": "persona",
                    "estado": estado,
                    "piso": piso,
                    "R": c.get("p"), "R_ic95inf": (c.get("ic95") or [None, None])[0],
                    "R_ic95sup": (c.get("ic95") or [None, None])[1],
                    "M": piso_v2["punto"] if piso_v2 else "",
                    "IC95_inf": piso_v2["ic95inf"] if piso_v2 else "",
                    "IC95_sup": piso_v2["ic95sup"] if piso_v2 else "",
                    "tipo_incertidumbre": ("PERSISTENCIA-T1-REPLICA" if piso_v2
                                            else "SIN-PISO"),
                    "resultado_id": piso_v2["resultado_id"] if piso_v2 else "",
                    "decision_ref": "veto:pisos-866" if vetados else "",
                    "emisor_vs_arbitro": "N/A-MARGINAL",
                    "fuente": f"{PROPUESTA_OLA5.name}:{r['id']}",
                })
    universo = {"n_reglas_ejes": len(reglas_ejes), "n_ejes": n_ejes, "n_celdas": len(filas)}
    return filas, universo


def _unidad_dato(regla_id: str) -> str:
    """(c) de la adenda: las celdas TRA son proporción de delitos, universo
    restringido a delitos -- NO se hereda `persona` para esas filas."""
    if regla_id.startswith("tramite.evasion_norma") or regla_id.startswith("TRA."):
        return "delito"
    return "persona"


# ── (3) universo de CRUCE -- 20 celdas C2 piloteadas + reservadas ─────────

def _celda_d(ruta: Path) -> dict:
    """Todas las celdas-D reales anidan bajo la clave `celda_d:`."""
    return (_yaml(ruta) or {}).get("celda_d") or {}


def _celdas_d_c2() -> list[Path]:
    return [p for p in sorted(CELDAS_D_DIR.glob("*.yaml"))
            if _celda_d(p).get("champion_actual") == "C2"]


def filas_cruce_adoptadas(decisiones: dict) -> list[dict]:
    filas = []
    tiene_adopcion = "adopcion:piso-C2-20-celdas" in decisiones
    for ruta in _celdas_d_c2():
        d = _celda_d(ruta)
        celda_id_base = d["id"]
        # el bloque de sub-celdas vive en `adjudicacion_por_celda`
        # (esquema real de las dos celdas-D con champion C2).
        sub = d.get("adjudicacion_por_celda")
        if not isinstance(sub, dict):
            continue
        calc_ids = {v.get("calc") for v in sub.values() if isinstance(v, dict)}
        resultados: dict[str, float] = {}
        for calc_id in calc_ids:
            if not calc_id:
                continue
            rj = CORRIDA0_DIR / calc_id / "resultados.json"
            if rj.exists():
                resultados.update(json.loads(rj.read_text(encoding="utf-8"))
                                   .get("resultados", {}))
        for sub_celda, info in sub.items():
            if not isinstance(info, dict) or info.get("id_candidato") != "C2":
                continue
            rid_p = info.get("resultado_puntual")
            rid_inf = info.get("ic95inf")
            rid_sup = info.get("ic95sup")
            filas.append({
                "celda_id": f"CRUCE::{celda_id_base}::{sub_celda}",
                "tipo": "CRUCE",
                "regla_o_eje_origen": celda_id_base,
                "instrumento": info.get("calc", ""),
                "eje_o_par": sub_celda,
                "categoria": sub_celda,
                "unidad_dato": _unidad_dato(celda_id_base),
                "unidad_objetivo": "persona",
                "estado": ("ADOPTADO-POR-FIRMA" if tiene_adopcion
                           else "PISO-ADMISIBLE-NO-ADOPTADO"),
                "piso": "MARGINAL-SIN-INTERACCION",
                "R": "", "R_ic95inf": "", "R_ic95sup": "",
                "M": resultados.get(rid_p, ""),
                "IC95_inf": resultados.get(rid_inf, ""),
                "IC95_sup": resultados.get(rid_sup, ""),
                "tipo_incertidumbre": "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS",
                "resultado_id": rid_p or "",
                "decision_ref": info.get("decision_ref", ""),
                "emisor_vs_arbitro": "N/A-CRUCE",
                "fuente": str(ruta.relative_to(RAIZ)),
            })
    return filas


def filas_cruce_reservadas() -> tuple[list[dict], dict]:
    """Combinaciones de eje-par que los 7 ids `_ejes_` habilitan pero que
    NO están piloteadas (no tienen celda-D con champion C2). Se agrupan por
    par de ejes -- no se enumera celda por celda -- porque el diseño exige
    que TODA celda de cruce no piloteada de las siete entradas `_ejes_`
    nazca RESERVADA sin R (§9(3)); las tres ya consumidas por NC-0328 se
    marcan aparte."""
    d = _yaml(PROPUESTA_OLA5)
    reglas_ejes = [r for r in d["reglas_propuestas"] if "_ejes_" in r.get("id", "")]
    piloteadas = {r["regla_o_eje_origen"] for r in filas_cruce_adoptadas(_lee_decisiones())}
    # pares de ejes ya piloteados (por regla): se infieren de las celdas-D
    pares_piloteados = set()
    for p in _celdas_d_c2():
        cid = _celda_d(p)["id"]
        if cid.startswith("DIN."):
            pares_piloteados.add(("dinero.ahorro.via_informal_ejes_enif2024",
                                  frozenset({"localidad", "edad"})))
        elif cid.startswith("TRA."):
            pares_piloteados.add(("tramite.evasion_norma_ejes_envipe2025",
                                  frozenset({"escolaridad_proxy", "dominio_urbano_rural"})))
    filas = []
    total_reservadas = 0
    total_consumidas = 0
    for r in reglas_ejes:
        ejes_por_bloque: dict[str, int] = {}
        for bloque in _camina_ejes(r):
            eje = bloque.get("eje")
            n = len(bloque.get("celdas") or [])
            ejes_por_bloque[eje] = max(ejes_por_bloque.get(eje, 0), n)
        nombres = sorted(ejes_por_bloque)
        for i in range(len(nombres)):
            for j in range(i + 1, len(nombres)):
                a, b = nombres[i], nombres[j]
                par = frozenset({a, b})
                n_celdas = ejes_por_bloque[a] * ejes_por_bloque[b]
                clave = (r["id"], par)
                if clave in pares_piloteados:
                    continue
                if clave == NC_0328_PAR_CONSUMIDO:
                    estado = "CONSUMIDA-SIN-PILOTO"
                    total_consumidas += n_celdas
                    decision = "NC-0328"
                else:
                    estado = "RESERVADA"
                    total_reservadas += n_celdas
                    decision = ""
                filas.append({
                    "celda_id": f"CRUCE-GRUPO::{r['id']}::{a}x{b}",
                    "tipo": "CRUCE",
                    "regla_o_eje_origen": r["id"],
                    "instrumento": r.get("payload", ""),
                    "eje_o_par": f"{a}x{b}",
                    "categoria": f"{n_celdas} celdas agrupadas",
                    "unidad_dato": _unidad_dato(r["id"]),
                    "unidad_objetivo": "persona",
                    "estado": estado,
                    "piso": "SIN-PISO" if estado == "RESERVADA" else "SIN-PISO",
                    "R": "", "R_ic95inf": "", "R_ic95sup": "",
                    "M": "", "IC95_inf": "", "IC95_sup": "",
                    "tipo_incertidumbre": "RESERVADA-SIN-R",
                    "resultado_id": "",
                    "decision_ref": decision,
                    "emisor_vs_arbitro": "N/A-CRUCE",
                    "fuente": f"{PROPUESTA_OLA5.name}:{r['id']}",
                })
    universo = {"n_grupos_reservados": sum(1 for f in filas if f["estado"] == "RESERVADA"),
                "n_celdas_reservadas": total_reservadas,
                "n_grupos_consumidos": sum(1 for f in filas if f["estado"] == "CONSUMIDA-SIN-PILOTO"),
                "n_celdas_consumidas": total_consumidas}
    return filas, universo


# ── ensamblado + cuatro números derivados al pie ──────────────────────────

def deriva() -> dict:
    decisiones = _lee_decisiones()
    veto_activo = "veto:pisos-866" in decisiones

    nacionales = filas_nacionales()
    marginales, uni_marginal = filas_marginales(vetados=veto_activo)
    cruce_adoptadas = filas_cruce_adoptadas(decisiones)
    cruce_reservadas, uni_reservadas = filas_cruce_reservadas()

    todas = nacionales + marginales + cruce_adoptadas + cruce_reservadas

    # cuatro números derivados al pie del diseño §4
    n_con_piso = sum(1 for f in todas if f["piso"] not in ("", "NO-APLICA", "SIN-PISO")
                      and not str(f["piso"]).startswith("SIN-CALC")
                      and not str(f["piso"]).startswith("VETADO"))
    n_evaluadas = len(cruce_adoptadas)  # las que tienen M sellado (== 20)
    n_universo_117 = uni_marginal["n_celdas"] + len(cruce_adoptadas) + \
        uni_reservadas["n_grupos_reservados"] + uni_reservadas["n_grupos_consumidos"]
    n_con_valor_anadido = 0  # M vs R: hoy sin comparación legítima (FP-383)
    n_adoptadas = sum(1 for f in cruce_adoptadas if f["estado"] == "ADOPTADO-POR-FIRMA")
    n_sin_piso = sum(1 for f in todas if f["estado"] == "SIN-PISO")

    resumen = {
        "veto_pisos_activo": veto_activo,
        "universo_i_marginal_ejes": uni_marginal,
        "universo_ii_nacional_censo": len(nacionales),
        "universo_iii_cruce": {
            "adoptadas_c2": len(cruce_adoptadas),
            **uni_reservadas,
        },
        "cobertura_de_piso": n_con_piso,
        "evaluadas": n_evaluadas,
        "universo_marginal_mas_cruce_grupos": n_universo_117,
        "valor_anadido": n_con_valor_anadido,
        "estimador_adoptado": n_adoptadas,
        "sin_piso": n_sin_piso,
        "total_filas": len(todas),
    }
    return {"filas": todas, "resumen": resumen, "decisiones": decisiones}


def escribe_tsv(filas: list[dict]) -> None:
    MARCADOR_TSV.parent.mkdir(parents=True, exist_ok=True)
    with MARCADOR_TSV.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# DERIVADO — NO EDITAR (tools/marcador_segmento.py, "
                 "ACTO GEN2-MARCADOR-REDISENO-1)\n")
        w = csv.DictWriter(fh, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for f in filas:
            w.writerow({k: f.get(k, "") for k in COLS})
    print(f"ESCRITO {MARCADOR_TSV.relative_to(RAIZ)}: {len(filas)} filas")


def escribe_estimadores_yaml(filas: list[dict]) -> None:
    """P2 (adenda): SOLO las celdas con `champion_actual` C2 y RESULT
    sellado -- nunca desde CALC-PISOS vetados ni desde la rama reservada."""
    adoptadas = [f for f in filas if f["tipo"] == "CRUCE"
                 and f["estado"] == "ADOPTADO-POR-FIRMA" and f["resultado_id"]]
    payload = {
        "_comentario": ("DERIVADO por tools/marcador_segmento.py — NO EDITAR. "
                        "ACTO GEN2-MARCADOR-REDISENO-1 (19/sep/2026). Fuente: "
                        "celdas-D con champion_actual=C2 y sus RESULT sellados; "
                        "cita adopcion:piso-C2-20-celdas de decisiones.tsv."),
        "decision_ref": "adopcion:piso-C2-20-celdas",
        "n_celdas": len(adoptadas),
        "celdas": {
            f["celda_id"]: {
                "regla_origen": f["regla_o_eje_origen"],
                "resultado_id": f["resultado_id"],
                "punto": f["M"],
                "ic95_inf": f["IC95_inf"],
                "ic95_sup": f["IC95_sup"],
                "unidad_dato": f["unidad_dato"],
                "tipo_incertidumbre": f["tipo_incertidumbre"],
            }
            for f in adoptadas
        },
    }
    ESTIMADORES_YAML.write_text(
        "# DERIVADO — NO EDITAR (tools/marcador_segmento.py, "
        "ACTO GEN2-MARCADOR-REDISENO-1)\n" +
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    print(f"ESCRITO {ESTIMADORES_YAML.relative_to(RAIZ)}: {len(adoptadas)} celdas")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribe", action="store_true",
                     help="escribe marcador-segmento.tsv y estimadores-por-segmento.yaml; "
                          "sin la bandera, solo deriva e imprime el resumen")
    ap.add_argument("--json", action="store_true", help="resumen en JSON")
    args = ap.parse_args()

    v = deriva()
    if args.escribe:
        escribe_tsv(v["filas"])
        escribe_estimadores_yaml(v["filas"])
    if args.json:
        print(json.dumps(v["resumen"], ensure_ascii=False, indent=2, sort_keys=True))
    else:
        r = v["resumen"]
        print(f"veto_pisos_activo={r['veto_pisos_activo']}")
        print(f"universo (i) marginal _ejes_: {r['universo_i_marginal_ejes']}")
        print(f"universo (ii) nacional/compuesto (censo ADR-536): {r['universo_ii_nacional_censo']}")
        print(f"universo (iii) cruce: {r['universo_iii_cruce']}")
        print(f"cobertura_de_piso={r['cobertura_de_piso']}")
        print(f"valor_anadido={r['valor_anadido']}")
        print(f"estimador_adoptado={r['estimador_adoptado']}")
        print(f"sin_piso={r['sin_piso']}")
        print(f"total_filas={r['total_filas']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
