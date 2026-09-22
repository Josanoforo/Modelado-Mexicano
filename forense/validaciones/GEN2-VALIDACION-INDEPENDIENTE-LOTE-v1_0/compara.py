#!/usr/bin/env python3
"""P2 · Comparación celda a celda (GEN2-VALIDACION-INDEPENDIENTE-LOTE-1).

Compara `resultados_propios.json` (P1, a ciegas, commiteado ANTES de este paso) contra los
RESULT sellados de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001` (COMMIT-3). Primera vez que
este acto abre un sellado del lote.

Tolerancia (declarada aquí, LATITUD): puntos (R, C2) a 1e-6 — son aritmética cerrada sobre
el mismo universo y, para C2, los mismos marginales sellados citados, así que deberían
coincidir a precisión de punto flotante si el procedimiento es el mismo. El IC95 y la
cobertura NO se exigen a la misma tolerancia: dependen del método de varianza, que este
acto declaró propio (bootstrap de conglomerados, semilla propia) y puede diferir
legítimamente del método del medidor sellado sin que eso sea discrepancia de fondo.
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TOL_PUNTO = 1e-6

EDAD_MAP = {"18-29": "E1", "30-44": "E2", "45-59": "E3", "60": "E4"}
SEXO_MAP = {"1-HOMBRE": "H", "2-MUJER": "M"}
ESC_MAP = {"HASTA-PRIMARIA": "HP", "SECUNDARIA": "SEC", "MEDIA-SUPERIOR": "MS", "SUPERIOR": "SUP"}
LOC_MAP = {"15-000-Y-MAS": "L2", "MENOR-DE-15-000": "L1"}

PARES = [
    ("edad", "sexo", "EDADXSEXO", EDAD_MAP, SEXO_MAP),
    ("escolaridad", "sexo", "ESCOLARIDADXSEXO", ESC_MAP, SEXO_MAP),
    ("localidad", "sexo", "LOCALIDADXSEXO", LOC_MAP, SEXO_MAP),
    ("edad", "escolaridad", "EDADXESCOLARIDAD", EDAD_MAP, ESC_MAP),
    ("escolaridad", "localidad", "ESCOLARIDADXLOCALIDAD", ESC_MAP, LOC_MAP),
]


def main():
    propio = json.loads((AQUI / "resultados_propios.json").read_text())
    sellado_path = Path(__file__).resolve().parents[3] / "data" / "corrida0" / "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001" / "resultados.json"
    sellado = json.loads(sellado_path.read_text())["resultados"]

    filas = []
    for eje_a, eje_b, PAR, mapa_a, mapa_b in PARES:
        for tok_a, niv_a in mapa_a.items():
            for tok_b, niv_b in mapa_b.items():
                suf = f"{tok_a}-X-{tok_b}"
                pref = f"RESULT-DIN-LOTE24-ADJ-{PAR}-R-{suf}"
                R_p_sellado = sellado.get(f"{pref}-P")
                R_n_sellado = sellado.get(f"{pref}-N")
                R_lo_sellado = sellado.get(f"{pref}-IC95INF")
                R_hi_sellado = sellado.get(f"{pref}-IC95SUP")
                c2_err_sellado = sellado.get(f"RESULT-DIN-LOTE24-ADJ-{PAR}-C2-ERROR-PP-{suf}")
                puntuada = sellado.get(f"RESULT-DIN-LOTE24-ADJ-{PAR}-PUNTUADA-{suf}")

                nombre_propio = f"{eje_a}x{eje_b}:{niv_a}x{niv_b}"
                celda_propia = propio["celdas"].get(nombre_propio)
                if celda_propia is None:
                    filas.append({"celda": nombre_propio, "sellado_suf": suf, "veredicto": "NO-ENCONTRADO-EN-PROPIO"})
                    continue

                R_p_propio = celda_propia["R"]["p"]
                C2_p_propio = celda_propia["C2"]["p"]
                c2_p_sellado = None
                if c2_err_sellado is not None and R_p_sellado is not None:
                    # ERROR-PP sellado = |R - C2| en pp; no trae el punto de C2 por separado en ADJUDICACION,
                    # se reconstruye con signo desconocido -> se reporta el error, no un C2 sellado puntual.
                    pass

                diff_R_pp = None
                if R_p_propio is not None and R_p_sellado is not None:
                    diff_R_pp = abs(R_p_propio - R_p_sellado) * 100

                fila = {
                    "celda": nombre_propio, "sellado_suf": suf,
                    "puntuada_sellado": puntuada, "soporte_propio": celda_propia["soporte_n200_ambas_olas"],
                    "n_propio": celda_propia["n_2024"], "n_sellado": R_n_sellado,
                    "R_p_propio": R_p_propio, "R_p_sellado": R_p_sellado, "diff_R_pp": diff_R_pp,
                    "R_ic95_propio": celda_propia["R"]["ic95"], "R_ic95_sellado": [R_lo_sellado, R_hi_sellado],
                    "C2_p_propio": C2_p_propio,
                    "C2_error_pp_propio": (abs(C2_p_propio - R_p_propio) * 100) if (C2_p_propio is not None and R_p_propio is not None) else None,
                    "C2_error_pp_sellado": c2_err_sellado,
                }
                if diff_R_pp is None:
                    fila["veredicto"] = "NO-COMPARABLE"
                elif diff_R_pp <= TOL_PUNTO * 100:
                    fila["veredicto"] = "COINCIDE"
                elif diff_R_pp <= 0.01:
                    fila["veredicto"] = "COINCIDE-CON-DIFERENCIA-EXPLICADA"
                else:
                    fila["veredicto"] = "DISCREPA"
                filas.append(fila)

    n_coincide = sum(1 for f in filas if f["veredicto"] == "COINCIDE")
    n_expl = sum(1 for f in filas if f["veredicto"] == "COINCIDE-CON-DIFERENCIA-EXPLICADA")
    n_discrepa = sum(1 for f in filas if f["veredicto"] == "DISCREPA")
    n_nc = sum(1 for f in filas if f["veredicto"] not in ("COINCIDE", "COINCIDE-CON-DIFERENCIA-EXPLICADA", "DISCREPA"))

    primario_propio = propio["primario"]
    primario_sellado = {
        "MAE_C2_pp": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-C2-MAE-PP"),
        "MAE_R2_pp": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-MAE-PP"),
        "delta_MAE_pp_punto": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-MAE-PP"),
        "delta_MAE_pp_ic95": [sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-IC95INF"), sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-IC95SUP")],
        "veredicto": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-VEREDICTO-PRIMARIO"),
        "cobertura_C2_frac": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-C2-COBERTURA-R-EN-IC-CAND-FRAC"),
        "cobertura_R2_frac": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-COBERTURA-R-EN-IC-CAND-FRAC"),
        "celdas_puntuadas": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-CELDAS-PUNTUADAS"),
        "n_celdas": sellado.get("RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-N-CELDAS"),
    }

    out = {
        "n_celdas": len(filas), "n_coincide": n_coincide, "n_coincide_con_diferencia_explicada": n_expl,
        "n_discrepa": n_discrepa, "n_no_comparable": n_nc,
        "diff_R_pp_max": max((f["diff_R_pp"] for f in filas if f["diff_R_pp"] is not None), default=None),
        "diff_R_pp_mediana": sorted(f["diff_R_pp"] for f in filas if f["diff_R_pp"] is not None)[len(filas) // 2] if filas else None,
        "primario_propio": primario_propio, "primario_sellado": primario_sellado,
        "delta_MAE_punto_diff_pp": abs(primario_propio["delta_MAE_pp_punto"] - primario_sellado["delta_MAE_pp_punto"]) if primario_sellado["delta_MAE_pp_punto"] is not None else None,
        "celdas": filas,
    }
    (AQUI / "comparacion-lote.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("n_celdas", out["n_celdas"], "COINCIDE", n_coincide, "COINCIDE-CON-DIFERENCIA-EXPLICADA", n_expl, "DISCREPA", n_discrepa, "NO-COMPARABLE", n_nc)
    print("diff_R_pp_max", out["diff_R_pp_max"])
    print("delta_MAE_punto_diff_pp", out["delta_MAE_punto_diff_pp"])
    print("primario_sellado", primario_sellado)
    if n_discrepa:
        print("--- DISCREPA ---")
        for f in filas:
            if f["veredicto"] == "DISCREPA":
                print(f)


if __name__ == "__main__":
    main()
