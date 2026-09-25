"""P3/P4 de GEN2-CLASE-AMAI-2 · calibración 2024 y cobertura por clase v1.1.

Derivado determinista de los `resultados.json` sellados: los seis
`CALC-AMAI-NSE-*-0001` de CLASE-AMAI-1 y `CALC-AMAI-NSE-ENIGH-2024-0001`, más
las filas `EJE-NSE` que `tools/marcador_segmento.py::filas_eje_nse` deriva.
No lee microdato; no adopta. No reescribe ningún archivo v1_0.
Uso: python3 -m tools.dominios.amai.calibracion
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

from tools.dominios.amai import cobertura as COB
from tools.dominios.amai import regla as R

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/clase-amai"
sys.path.insert(0, str(ROOT / "tools"))
import marcador_segmento as MS  # noqa: E402

REF = "ENIGH-2024"
GRUPOS = R.ORDEN_GRUPOS
# Firma A4 (FIRMAS-16) por instrumento-ola; lo no listado queda FUERA.
A4 = {"ENIGH-2022": "EJE", "ENIF-2024": "EJE", "ENDUTIH-2023": "EJE-APROXIMACION",
      "ENDUTIH-2024": "FUERA-DESVIADA", "ENDUTIH-2025": "FUERA-DESVIADA",
      "ENIF-2021": "FUERA-SIN-CONDUCTA-ADOPTABLE"}


def _valores(io: str) -> dict:
    return MS._valores_calc(f"CALC-AMAI-NSE-{io}-0001")


def calibracion() -> list[dict]:
    ref = _valores(REF)
    filas = []
    for io in (REF,) + COB.CALCS:
        v = _valores(io)
        pref = f"RESULT-AMAI-NSE-{io}"
        fila = {"calc": f"CALC-AMAI-NSE-{io}-0001", "eje_marcador_a4":
                "REFERENCIA-CALIBRACION" if io == REF else A4[io],
                "validacion_figura1": v[pref + "-VALIDACION-ESTADO"],
                "desvio_max_grupo_figura1_pp": v[pref + "-DESVIO-MAX-GRUPO-PP"]}
        d = []
        for g in GRUPOS:
            p = v[f"{pref}-DIST-{g}-P"]
            fila[f"dist_{g.lower()}"] = p
            if io != REF:
                dg = (p - ref[f"RESULT-AMAI-NSE-{REF}-DIST-{g}-P"]) * 100
                fila[f"desvio_{g.lower()}_vs_2024_pp"] = dg
                d.append(abs(dg))
            else:
                fila[f"desvio_{g.lower()}_vs_2024_pp"] = None
        fila["desvio_max_grupo_vs_2024_pp"] = max(d) if d else None
        filas.append(fila)
    return filas


def cobertura_v1_1() -> tuple[list[dict], dict]:
    datos = COB.carga()
    pisos = COB.tabla_pisos(datos)
    cob, resumen = COB.cobertura_u1(pisos)
    eje = MS.filas_eje_nse()
    en_eje = {(f["instrumento"].split()[0], f["regla_o_eje_origen"]) for f in eje}
    for f in cob:
        conductas = COB.MAPA_U1.get((f["instrumento"], f["conducta_u1"]), [])
        f["eje_nse_marcador"] = ("SI" if conductas and all((f["instrumento"], c) in en_eje
                                                          for c in conductas) else "NO")
    resumen["identidades_u1_en_eje_nse"] = sum(f["eje_nse_marcador"] == "SI" for f in cob)
    resumen["filas_eje_nse"] = len(eje)
    resumen["filas_eje_nse_por_estado"] = dict(Counter(f["estado"] for f in eje))
    resumen["filas_eje_nse_por_instrumento"] = dict(Counter(f["instrumento"] for f in eje))
    return cob, resumen


def _escribe(nombre: str, filas: list[dict]) -> None:
    with (OUT / nombre).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in filas:
            w.writerow({k: ("" if v is None else repr(v) if isinstance(v, float) else v)
                        for k, v in r.items()})


def _pp(x) -> str:
    return "—" if x is None else f"{x:.2f}"


def _md(cal: list[dict], resumen: dict) -> str:
    r24 = cal[0]
    lin = ["# Cobertura por clase AMAI v1.1 · calibración ENIGH 2024 y eje NSE del marcador · "
           "GEN2-CLASE-AMAI-2 · RETROSPECTIVA",
           "",
           "Generado por `python3 -m tools.dominios.amai.calibracion` desde los `resultados.json` "
           "sellados; sucede a `cobertura-por-clase-v1_0.md` (que no se toca). Tablas: "
           "`calibracion-2024-v1_0.tsv`, `cobertura-u1-por-clase-v1_1.tsv`, `resumen-p4-v1_1.json`.",
           "",
           "## 1 · Distribución NSE nacional por hogares, ENIGH 2024 (apertura acotada C7)",
           "",
           f"`{r24['calc']}`: BAJO {100 * r24['dist_bajo']:.1f} % · MEDIO "
           f"{100 * r24['dist_medio']:.1f} % · ALTO {100 * r24['dist_alto']:.1f} %; contra la "
           f"Figura 1 de AMAI (ENIGH 2022, la única publicada): desvío máximo por grupo "
           f"{_pp(r24['desvio_max_grupo_figura1_pp'])} pp → **{r24['validacion_figura1']}** "
           "(umbral 5.0 pp, congelado en COMMIT-1). Masa de BAJO a MEDIO y ALTO en dos años: "
           "deriva de bienes y de red (internet), no error del medidor.",
           "",
           "## 2 · Calibración de cada instrumento contra ENIGH 2024 (descriptiva)",
           "",
           "| CALC | Eje (firma A4) | Validación Figura 1 | Desvío máx. grupo vs Figura 1 (pp) "
           "| vs ENIGH 2024 (pp) |",
           "|---|---|---|---:|---:|"]
    for f in cal[1:]:
        lin.append(f"| `{f['calc']}` | {f['eje_marcador_a4']} | {f['validacion_figura1']} | "
                   f"{_pp(f['desvio_max_grupo_figura1_pp'])} | "
                   f"{_pp(f['desvio_max_grupo_vs_2024_pp'])} |")
    est = resumen["filas_eje_nse_por_estado"]
    lin += ["",
            "## 3 · Eje NSE en el marcador (P3)",
            "",
            f"`tools/marcador_segmento.py::filas_eje_nse` deriva **{resumen['filas_eje_nse']}** "
            "filas de tipo `EJE-NSE` (instrumento · conducta · grupo), R e IC por id de los CALC "
            "sellados: " + " · ".join(f"{k} {v}" for k, v in
                                      sorted(resumen["filas_eje_nse_por_instrumento"].items()))
            + ". Por estado: " + " · ".join(f"`{k}` {v}" for k, v in sorted(est.items()))
            + ". ENDUTIH 2024–25 y ENIF 2021 no entran (A4). `internet` y `celular` de ENDUTIH "
            "llevan `-CIRCULAR` (el NSE contiene internet fijo). No son marginales t-1: no hay ola "
            "anterior con NSE; ningún contador de piso ni `celdas_validadas` se mueve.",
            "",
            "## 4 · Cobertura del catálogo U1 por clase",
            "",
            f"Identidades U1 de conducta: {resumen['identidades_conducta']}; con piso por NSE: "
            f"{resumen['con_piso_nse']}; **en el eje NSE del marcador: "
            f"{resumen['identidades_u1_en_eje_nse']}**. Celdas conducta × grupo publicables: "
            f"{resumen['celdas_publicables']} de {resumen['celdas_conducta_x_grupo']}. Sin cambio "
            "respecto de v1.0 en lo que no tiene corte AMAI (ENVIPE, ENCIG: NO-CONSTRUIBLE).",
            "",
            "## Auditoría de rigor extremo",
            "",
            "El eje compara grupos de bienes y escolaridad del hogar, no clases sociológicas; cada "
            "fila es asociación descriptiva de la misma ola (A-bis), RETROSPECTIVA, unidad de su "
            "conducta (hogar en ENIGH, persona en ENIF y ENDUTIH) y nunca se promedia entre "
            "unidades. La calibración contra 2024 mezcla deriva real con el error de "
            "aproximación de cada instrumento; no se separan aquí.",
            ""]
    return "\n".join(lin)


def genera() -> dict:
    cal = calibracion()
    cob, resumen = cobertura_v1_1()
    resumen["calibracion_2024"] = {f["calc"]: f["desvio_max_grupo_vs_2024_pp"] for f in cal[1:]}
    _escribe("calibracion-2024-v1_0.tsv", cal)
    _escribe("cobertura-u1-por-clase-v1_1.tsv", cob)
    (OUT / "resumen-p4-v1_1.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "cobertura-por-clase-v1_1.md").write_text(_md(cal, resumen), encoding="utf-8")
    return resumen


if __name__ == "__main__":
    print(json.dumps(genera(), ensure_ascii=False, indent=1, sort_keys=True))
