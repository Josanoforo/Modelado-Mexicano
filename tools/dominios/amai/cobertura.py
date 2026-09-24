"""P4 · pisos conducta × NSE × ola, potencia y cobertura del catálogo U1 por clase.

Derivado determinista de los `resultados.json` sellados de los seis CALC
AMAI-NSE (spec §7) y del inventario U1. No lee microdato; no adopta.
Uso: python3 -m tools.dominios.amai.cobertura
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/clase-amai"
INVENTARIO = ROOT / "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
CALCS = ("ENIGH-2022", "ENIF-2021", "ENIF-2024", "ENDUTIH-2023", "ENDUTIH-2024", "ENDUTIH-2025")
GRUPOS = ("BAJO", "MEDIO", "ALTO")
UNIDAD = {"ENIGH": "hogar", "ENIF": "persona elegida 18+", "ENDUTIH": "persona 6+"}
# Identidad U1 -> conductas con piso NSE en este acto (spec §5). Lo no listado
# no tiene piso NSE; la causa se asigna en `causa_sin_piso`.
MAPA_U1 = {
    ("ENIF", "tiene_ahorros_enif2024"): ["tiene_ahorros_enif2024"],
    ("ENIF", "no_tiene_ahorros_enif2024"): ["no_tiene_ahorros_enif2024"],
    ("ENIF", "informal_cualquiera"): ["informal_cualquiera"],
    ("ENIF", "formal_cualquiera"): ["formal_cualquiera"],
    ("ENIF", "ahorra_solo_informal"): ["ahorra_solo_informal"],
    ("ENIF", "ahorra_solo_formal"): ["ahorra_solo_formal"],
    ("ENIF", "ahorra_ambas_vias"): ["ahorra_ambas_vias"],
    ("ENIF", "no_ahorra"): ["no_ahorra"],
    ("ENIF", "horizonte_corto"): ["horizonte_corto_sin_ss", "horizonte_corto_con_ss"],
    ("ENIF", "horizonte_no_corto"): ["horizonte_no_corto_sin_ss", "horizonte_no_corto_con_ss"],
    ("ENIF", "desconfianza_o_mal_servicio_como_razon_principal_conoce_proteccion_enif2024"):
        ["desconfia_conoce_proteccion"],
    ("ENIF", "desconfianza_o_mal_servicio_como_razon_principal_no_conoce_enif2024"):
        ["desconfia_no_conoce_proteccion"],
    ("ENIF", "recibe_dinero_familiares_para_vejez"): ["recibe_dinero_familiares_para_vejez"],
    ("ENIF", "no_recibe_dinero_familiares_para_vejez"): ["no_recibe_dinero_familiares_para_vejez"],
    ("ENIF", "dinero.ahorro.horizonte_corto_ejes_enif2024"):
        ["horizonte_corto_sin_ss", "horizonte_corto_con_ss"],
    ("ENIF", "dinero.ahorro.via_informal_ejes_enif2024"): ["informal_cualquiera"],
    ("ENIGH", "recibe_remesas"): ["recibe_remesas"],
}
BASE_DE_EJES = {"dinero.ahorro.horizonte_corto_ejes_enif2024",
                "dinero.ahorro.via_informal_ejes_enif2024"}
NO_CONSTRUIBLE = {"ENVIPE", "ENCIG"}


def _valores(calc: str) -> dict:
    r = json.loads((ROOT / f"data/corrida0/CALC-AMAI-NSE-{calc}-0001/resultados.json")
                   .read_text(encoding="utf-8"))
    v = r.get("resultados", r)
    return {x["id"]: x.get("valor") for x in v} if isinstance(v, list) else v


def carga() -> dict:
    datos = {}
    for calc in CALCS:
        inst, ola = calc.split("-")
        v = _valores(calc)
        pref = f"RESULT-AMAI-NSE-{calc}"
        datos[calc] = {"inst": inst, "ola": ola, "pref": pref, "valores": v,
                       "doc": json.loads(v[pref + "-JSON"])}
    return datos


def tabla_pisos(datos: dict) -> list[dict]:
    filas = []
    for calc, d in datos.items():
        val = d["doc"]["validacion"]["estado"]
        for conducta, t in sorted(d["doc"]["pisos"].items()):
            for f in t["filas"]:
                filas.append({
                    "instrumento": d["inst"], "ola": d["ola"], "conducta": conducta,
                    "unidad": UNIDAD[d["inst"]], "grupo_nse": f["geografia"],
                    "punto": f["punto"], "ic95_inf": f["ic_inf"], "ic95_sup": f["ic_sup"],
                    "n": f["n"], "estado": f["estado"], "validacion_nse": val,
                    "result_punto": f"{d['pref']}-{conducta}-{f['geografia']}-P",
                    "calc": f"CALC-AMAI-NSE-{calc}-0001"})
    return filas


def potencia(datos: dict) -> list[dict]:
    """IC95 de ALTO − BAJO con las réplicas compartidas (mismo plan de UPM)."""
    filas = []
    for calc, d in datos.items():
        for conducta, t in sorted(d["doc"]["pisos"].items()):
            g = {f["geografia"]: f for f in t["filas"]}
            a, b = g["ALTO"], g["BAJO"]
            fila = {"instrumento": d["inst"], "ola": d["ola"], "conducta": conducta,
                    "diferencia_alto_menos_bajo": None, "ic95_inf": None, "ic95_sup": None,
                    "despeja_cero": "NO-ESTIMABLE",
                    "semiancho_ic_bajo": None, "semiancho_ic_medio": None,
                    "semiancho_ic_alto": None}
            for k in GRUPOS:
                if g[k]["estado"] == "PUBLICABLE":
                    fila[f"semiancho_ic_{k.lower()}"] = (g[k]["ic_sup"] - g[k]["ic_inf"]) / 2
            if a["estado"] == b["estado"] == "PUBLICABLE":
                diff = np.array(a["replicas_p"]) - np.array(b["replicas_p"])
                lo, hi = np.quantile(diff, [0.025, 0.975])
                fila.update(diferencia_alto_menos_bajo=a["punto"] - b["punto"],
                            ic95_inf=float(lo), ic95_sup=float(hi),
                            despeja_cero="SI" if lo > 0 or hi < 0 else "NO")
            filas.append(fila)
    return filas


def cobertura_u1(pisos: list[dict]) -> tuple[list[dict], dict]:
    publicables = defaultdict(set)
    for f in pisos:
        if f["estado"] == "PUBLICABLE" and f["instrumento"] in ("ENIF", "ENIGH"):
            publicables[(f["instrumento"], f["conducta"])].add(f["grupo_nse"])
    with INVENTARIO.open(newline="", encoding="utf-8") as fh:
        inv = list(csv.DictReader(fh, delimiter="\t"))
    ids = {}
    for r in inv:
        if r["estado_adopcion"].startswith(("PISO-HISTORICO", "SELLADO-CONTEXTO")):
            continue
        ids.setdefault((r["instrumento_ola"].split()[0], r["conducta"]), r["instrumento_ola"])
    filas = []
    for (inst, conducta), ola in sorted(ids.items()):
        pseudo = conducta == "R" or re.fullmatch(r"L\dxE\d", conducta) is not None
        grupos = set()
        for c in MAPA_U1.get((inst, conducta), []):
            g = publicables.get((inst, c), set())
            grupos = g if not grupos else grupos & g
        if pseudo:
            causa = "CELDA-O-INTERACCION-NO-CONDUCTA"
        elif (inst, conducta) in MAPA_U1:
            causa = ("BASE-NSE-MEDIDA;CRUCES-DE-EJES-NO-EXTENDIDOS" if conducta in BASE_DE_EJES
                     else "CON-PISO-NSE")
        elif inst in NO_CONSTRUIBLE:
            causa = "NSE-NO-CONSTRUIBLE-EN-EL-INSTRUMENTO"
        elif (inst, conducta) == ("ENIGH", "no_recibe_remesas"):
            causa = "COMPLEMENTO-DE-recibe_remesas-NO-MEDIDO-APARTE"
        else:
            causa = "INSTRUMENTO-FUERA-DEL-ALCANCE-AMAI-DE-ESTE-ACTO"
        filas.append({"instrumento": inst, "instrumento_ola_u1": ola, "conducta_u1": conducta,
                      "estado_nse": causa,
                      "grupos_publicables": ";".join(g for g in GRUPOS if g in grupos),
                      "n_grupos_publicables": len(grupos) if causa.startswith(("CON", "BASE")) else 0})
    conductas = [f for f in filas if f["estado_nse"] != "CELDA-O-INTERACCION-NO-CONDUCTA"]
    resumen = {
        "identidades_u1": len(filas),
        "identidades_conducta": len(conductas),
        "con_piso_nse": sum(f["estado_nse"].startswith(("CON", "BASE")) for f in conductas),
        "celdas_conducta_x_grupo": 3 * len(conductas),
        "celdas_publicables": sum(f["n_grupos_publicables"] for f in conductas),
        "por_estado": dict(Counter(f["estado_nse"] for f in filas)),
        "publicables_por_grupo": {g: sum(g in f["grupos_publicables"].split(";")
                                         for f in conductas) for g in GRUPOS},
    }
    return filas, resumen


def _escribe(nombre: str, filas: list[dict]) -> None:
    with (OUT / nombre).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in filas:
            w.writerow({k: ("" if v is None else repr(v) if isinstance(v, float) else v)
                        for k, v in r.items()})


def genera() -> dict:
    datos = carga()
    pisos = tabla_pisos(datos)
    pot = potencia(datos)
    cob, resumen = cobertura_u1(pisos)
    _escribe("pisos-nse-v1_0.tsv", pisos)
    _escribe("potencia-alto-bajo-v1_0.tsv", pot)
    _escribe("cobertura-u1-por-clase-v1_0.tsv", cob)
    endutih = [f for f in pisos if f["instrumento"] == "ENDUTIH"]
    resumen["endutih_celdas"] = len(endutih)
    resumen["endutih_publicables"] = sum(f["estado"] == "PUBLICABLE" for f in endutih)
    resumen["conductas_con_piso_nse"] = len({(f["instrumento"], f["conducta"]) for f in pisos
                                             if f["estado"] == "PUBLICABLE"})
    resumen["celdas_pisos_total"] = len(pisos)
    resumen["celdas_pisos_publicables"] = sum(f["estado"] == "PUBLICABLE" for f in pisos)
    resumen["potencia_despeja_cero"] = dict(Counter(f["despeja_cero"] for f in pot))
    resumen["validacion"] = {c: d["doc"]["validacion"]["estado"] for c, d in datos.items()}
    (OUT / "resumen-p4-v1_0.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1,
                                                         sort_keys=True) + "\n", encoding="utf-8")
    _tabla_md(pisos, pot, datos)
    return resumen


def _pp(x) -> str:
    return "—" if x is None else f"{100 * x:.1f}"


def _tabla_md(pisos: list[dict], pot: list[dict], datos: dict) -> None:
    g = {(f["instrumento"], f["ola"], f["conducta"], f["grupo_nse"]): f for f in pisos}
    lin = ["# Pisos por NSE · conducta × grupo × ola · RETROSPECTIVA",
           "",
           "Generado por `python3 -m tools.dominios.amai.cobertura` desde los `resultados.json` "
           "sellados de `CALC-AMAI-NSE-*-0001`. Porcentaje del denominador de cada conducta, "
           "IC95 percentil de 1 000 réplicas UPM; «—» = no publicable (estado en "
           "`pisos-nse-v1_0.tsv`). Δ = ALTO − BAJO en pp con IC95 de la diferencia por réplica "
           "compartida. La unidad es la de la conducta; no se comparan filas de unidades distintas.",
           "",
           "| Instrumento · ola (validación NSE) | Conducta | BAJO | MEDIO | ALTO | Δ ALTO−BAJO [IC95] |",
           "|---|---|---:|---:|---:|---:|"]
    for r in pot:
        k = (r["instrumento"], r["ola"], r["conducta"])
        celdas = []
        for grupo in GRUPOS:
            f = g[k + (grupo,)]
            celdas.append(f"{_pp(f['punto'])} [{_pp(f['ic95_inf'])}, {_pp(f['ic95_sup'])}]"
                          if f["estado"] == "PUBLICABLE" else "—")
        val = datos[f"{k[0]}-{k[1]}"]["doc"]["validacion"]["estado"]
        d = (f"{_pp(r['diferencia_alto_menos_bajo'])} [{_pp(r['ic95_inf'])}, {_pp(r['ic95_sup'])}]"
             if r["diferencia_alto_menos_bajo"] is not None else "—")
        lin.append(f"| {k[0]} {k[1]} ({val}) | `{k[2]}` | " + " | ".join(celdas) + f" | {d} |")
    lin.append("")
    (OUT / "tabla-conducta-nse-ola-v1_0.md").write_text("\n".join(lin), encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(genera(), ensure_ascii=False, indent=1, sort_keys=True))
