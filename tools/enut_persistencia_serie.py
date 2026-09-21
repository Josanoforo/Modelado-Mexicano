#!/usr/bin/env python3
"""P4 del acto GEN2-ENUT-PISOS-Y-SERIE-1 (21/sep/2026): calificación de la
persistencia 2019→2024, serie 2009-2024 y origen móvil RETROSPECTIVA-MECÁNICA
del núcleo común de cuidado, con las reglas fijadas en
`forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md` §5 ANTES de ver dato.

Lee SÓLO los `resultados.json` sellados de los tres CALC (nunca los edita) y
escribe dos tablas derivadas:

  data/corrida0/enut-persistencia-serie-v1_0.tsv     una fila por celda ×
      objetivo × método (V1 persistencia, V2 tendencia 2 olas, V3 tendencia
      serie) con pronóstico, R observado, IC, error y coberturas; más las
      filas DELTA-INSTRUMENTO (CONCP − NUCLEO por eje, 2024).
  data/corrida0/enut-persistencia-dictamen-v1_0.tsv  una fila por conducta
      (variante × escala, más C1) con las métricas y el dictamen en una
      palabra: PERSISTE · TENDENCIA · CAMBIO-DE-INSTRUMENTO · NO-DECIDIBLE.

Uso: python3 tools/enut_persistencia_serie.py [--escribe]   (sin flag: sólo
imprime el dictamen y no toca el árbol).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CALCS = {"2024": "CALC-ENUT2024-NUCLEO-EJES-0001", "2019": "CALC-ENUT2019-NUCLEO-EJES-0001",
         "2014": "CALC-ENUT-SERIE-2009-2014-NUCLEO-0001", "2009": "CALC-ENUT-SERIE-2009-2014-NUCLEO-0001"}
SALIDA_SERIE = RAIZ / "data" / "corrida0" / "enut-persistencia-serie-v1_0.tsv"
SALIDA_DICTAMEN = RAIZ / "data" / "corrida0" / "enut-persistencia-dictamen-v1_0.tsv"

EJES = {"NACIONAL": ["NAC"], "SEXO": ["HOMBRE", "MUJER"], "EDAD": ["12-17", "18-29", "30-39", "40-59", "60-MAS"],
        "ESCOLARIDAD": ["HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"],
        "LOCALIDAD": ["URBANO", "RURAL"]}
OLAS_DE = {"NUCLEO": ["2014", "2019", "2024"], "MIN": ["2009", "2014", "2019", "2024"]}
ANIO = {"2009": 2009, "2014": 2014, "2019": 2019, "2024": 2024}

COLS_SERIE = ["variante", "escala", "eje", "categoria", "objetivo", "metodo", "olas_previas",
              "pronostico", "observado", "ic_lo", "ic_hi", "n", "error", "error_relativo",
              "cobertura_ic_piso", "cobertura_proxy", "piso_ic_lo", "piso_ic_hi", "nota"]
COLS_DICT = ["conducta", "variante", "escala", "objetivo", "n_celdas", "cobertura_v1_k", "cobertura_v1_n",
             "cobertura_v1", "cp95_lo", "cp95_hi", "mae_v1", "mae_v2", "mae_v3", "cobertura_proxy_v1",
             "cobertura_proxy_v2", "cobertura_proxy_v3", "dictamen", "regla_aplicada"]


def _carga() -> dict:
    out = {}
    for ola, calc in CALCS.items():
        p = RAIZ / "data" / "corrida0" / calc / "resultados.json"
        out[ola] = json.loads(p.read_text(encoding="utf-8"))["resultados"]
    return out


def _celda(r: dict, ola: str, variante: str, escala: str, eje: str, cat: str) -> dict | None:
    if escala == "media":
        base = f"RESULT-ENUT{ola}-{variante}-{eje}-{cat}"
    else:
        base = f"RESULT-ENUT{ola}-RAZON-{variante}-NACIONAL"
    if base + "-P" not in r:
        return None
    return {"p": r[base + "-P"], "lo": r[base + "-IC-LO"], "hi": r[base + "-IC-HI"], "n": r[base + "-N"]}


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """IC exacto binomial por bisección sobre la CDF (n pequeño; sin scipy)."""
    if n == 0:
        return (float("nan"), float("nan"))

    def cdf(p, kk):
        return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(kk + 1))

    def solve(f, lo, hi):
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    # límite inferior: mayor p tal que P(X ≥ k | p) ≤ α/2  ⇔ 1 − CDF(k−1) ≤ α/2
    if k == 0:
        lo = 0.0
    else:
        lo = solve(lambda p: alpha / 2 - (1 - cdf(p, k - 1)), 0.0, 1.0)
    # límite superior: menor p tal que P(X ≤ k | p) ≤ α/2
    if k == n:
        hi = 1.0
    else:
        hi = solve(lambda p: cdf(p, k) - alpha / 2, 0.0, 1.0)
    return (lo, hi)


def _ols(xs: list[float], ys: list[float], x0: float) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my + b * (x0 - mx)


def _pronosticos(serie: dict[str, dict], objetivo: str, variante: str) -> list[tuple[str, str, float | None]]:
    """[(metodo, olas_previas, ŷ)] para el objetivo, con las olas previas
    disponibles de la variante (todas las variantes, todas juntas)."""
    previas = [o for o in OLAS_DE[variante] if ANIO[o] < ANIO[objetivo] and serie.get(o) and serie[o]["p"] is not None]
    out = []
    if not previas:
        return out
    t = ANIO[objetivo]
    y1, t1 = serie[previas[-1]]["p"], ANIO[previas[-1]]
    out.append(("V1-PERSISTENCIA", previas[-1], y1))
    if len(previas) >= 2:
        y2, t2 = serie[previas[-2]]["p"], ANIO[previas[-2]]
        out.append(("V2-TENDENCIA-2-OLAS", "+".join(previas[-2:]), y1 + (y1 - y2) * (t - t1) / (t1 - t2)))
    else:
        out.append(("V2-TENDENCIA-2-OLAS", "", None))
    if len(previas) >= 3:
        out.append(("V3-TENDENCIA-SERIE", "+".join(previas),
                    _ols([ANIO[o] for o in previas], [serie[o]["p"] for o in previas], t)))
    else:
        out.append(("V3-TENDENCIA-SERIE", "", None))
    return out


def _f(x) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    if isinstance(x, bool):
        return "1" if x else "0"
    if isinstance(x, int):
        return str(x)
    return f"{x:.6f}"


def deriva(r: dict) -> tuple[list[dict], list[dict]]:
    filas, dict_filas = [], []
    for variante in ("NUCLEO", "MIN"):
        for escala in ("media", "razon"):
            celdas = [(e, c) for e, cs in EJES.items() for c in cs] if escala == "media" else [("NACIONAL", "NAC")]
            for objetivo in ("2019", "2024"):
                por_metodo: dict[str, dict] = {}
                n_def = 0
                for eje, cat in celdas:
                    serie = {o: _celda(r[o], o, variante, escala, eje, cat) for o in OLAS_DE[variante]}
                    obs = serie.get(objetivo)
                    if not obs or obs["p"] is None:
                        continue
                    pron = _pronosticos(serie, objetivo, variante)
                    if not pron:
                        continue
                    n_def += 1
                    semi = (obs["hi"] - obs["lo"]) / 2
                    piso = serie[pron[0][1]]
                    for metodo, previas, yhat in pron:
                        fila = {"variante": variante, "escala": escala, "eje": eje, "categoria": cat,
                                "objetivo": objetivo, "metodo": metodo, "olas_previas": previas,
                                "pronostico": yhat, "observado": obs["p"], "ic_lo": obs["lo"], "ic_hi": obs["hi"],
                                "n": obs["n"], "error": None, "error_relativo": None,
                                "cobertura_ic_piso": None, "cobertura_proxy": None,
                                "piso_ic_lo": piso["lo"] if metodo == "V1-PERSISTENCIA" else None,
                                "piso_ic_hi": piso["hi"] if metodo == "V1-PERSISTENCIA" else None, "nota": ""}
                        if yhat is None:
                            fila["nota"] = "NO-APLICA: olas previas insuficientes"
                        else:
                            err = obs["p"] - yhat
                            fila["error"] = err
                            fila["error_relativo"] = err / yhat if yhat else None
                            fila["cobertura_proxy"] = abs(err) <= semi
                            if metodo == "V1-PERSISTENCIA":
                                fila["cobertura_ic_piso"] = piso["lo"] <= obs["p"] <= piso["hi"]
                            m = por_metodo.setdefault(metodo, {"abs": [], "proxy": [], "piso": []})
                            m["abs"].append(abs(err))
                            m["proxy"].append(fila["cobertura_proxy"])
                            if metodo == "V1-PERSISTENCIA":
                                m["piso"].append(fila["cobertura_ic_piso"])
                        filas.append(fila)
                if n_def == 0:
                    continue
                dict_filas.append(_dictamen(r, variante, escala, objetivo, n_def, por_metodo))
    # tamaño del cambio de instrumento: CONCP − NUCLEO por eje, 2024
    for eje, cs in EJES.items():
        for cat in cs:
            a = _celda(r["2024"], "2024", "CONCP", "media", eje, cat)
            b = _celda(r["2024"], "2024", "NUCLEO", "media", eje, cat)
            if a and b and a["p"] is not None and b["p"] is not None:
                filas.append({"variante": "CONCP-vs-NUCLEO", "escala": "media", "eje": eje, "categoria": cat,
                              "objetivo": "2024", "metodo": "DELTA-INSTRUMENTO", "olas_previas": "2024",
                              "pronostico": b["p"], "observado": a["p"], "ic_lo": a["lo"], "ic_hi": a["hi"],
                              "n": a["n"], "error": a["p"] - b["p"], "error_relativo": (a["p"] - b["p"]) / b["p"],
                              "cobertura_ic_piso": None, "cobertura_proxy": None, "piso_ic_lo": b["lo"],
                              "piso_ic_hi": b["hi"], "nota": "horas que la definición sellada añade al núcleo (emocionales + esperas + pasivo presente)"})
    a = _celda(r["2024"], "2024", "CONCP", "razon", "NACIONAL", "NAC")
    b = _celda(r["2024"], "2024", "NUCLEO", "razon", "NACIONAL", "NAC")
    filas.append({"variante": "CONCP-vs-NUCLEO", "escala": "razon", "eje": "NACIONAL", "categoria": "NAC",
                  "objetivo": "2024", "metodo": "DELTA-INSTRUMENTO", "olas_previas": "2024",
                  "pronostico": b["p"], "observado": a["p"], "ic_lo": a["lo"], "ic_hi": a["hi"], "n": a["n"],
                  "error": a["p"] - b["p"], "error_relativo": (a["p"] - b["p"]) / b["p"], "cobertura_ic_piso": None,
                  "cobertura_proxy": None, "piso_ic_lo": b["lo"], "piso_ic_hi": b["hi"], "nota": "razón: escala [0,1]"})
    # C1: las 21 celdas del marcador, por texto
    dict_filas.append({"conducta": "C1 horas_cuidado CON_CP (21 celdas del marcador)", "variante": "CONCP", "escala": "media+razon",
                       "objetivo": "2024", "n_celdas": 21, "cobertura_v1_k": None, "cobertura_v1_n": None, "cobertura_v1": None,
                       "cp95_lo": None, "cp95_hi": None, "mae_v1": None, "mae_v2": None, "mae_v3": None,
                       "cobertura_proxy_v1": None, "cobertura_proxy_v2": None, "cobertura_proxy_v3": None,
                       "dictamen": "CAMBIO-DE-INSTRUMENTO",
                       "regla_aplicada": "§5.3 por texto: ADR-557 + P1 (C1 2019/2014/2009 = CAMBIO-DE-INSTRUMENTO); sin piso"})
    return filas, dict_filas


def _dictamen(r: dict, variante: str, escala: str, objetivo: str, n: int, m: dict) -> dict:
    def mae(k):
        return (sum(m[k]["abs"]) / len(m[k]["abs"])) if k in m and m[k]["abs"] else None

    def proxy(k):
        return (sum(m[k]["proxy"]) / len(m[k]["proxy"])) if k in m and m[k]["proxy"] else None
    v1, v2, v3 = "V1-PERSISTENCIA", "V2-TENDENCIA-2-OLAS", "V3-TENDENCIA-SERIE"
    k = sum(m[v1]["piso"]) if v1 in m else 0
    nn = len(m[v1]["piso"]) if v1 in m else 0
    lo, hi = clopper_pearson(k, nn) if nn else (None, None)
    fila = {"conducta": f"{'C2' if variante == 'NUCLEO' else 'C3'} {variante} {escala}", "variante": variante,
            "escala": escala, "objetivo": objetivo, "n_celdas": n, "cobertura_v1_k": k, "cobertura_v1_n": nn,
            "cobertura_v1": (k / nn) if nn else None, "cp95_lo": lo, "cp95_hi": hi,
            "mae_v1": mae(v1), "mae_v2": mae(v2), "mae_v3": mae(v3),
            "cobertura_proxy_v1": proxy(v1), "cobertura_proxy_v2": proxy(v2), "cobertura_proxy_v3": proxy(v3)}
    if escala == "media":
        if n < 4:
            d, regla = "NO-DECIDIBLE", "§5.3 media: n < 4 celdas definidas"
        else:
            tend = (fila["mae_v2"] is not None and fila["mae_v1"] is not None and fila["mae_v2"] <= 0.5 * fila["mae_v1"])
            if lo is not None and lo >= 0.5:
                if tend and (fila["cobertura_proxy_v2"] or 0) > (fila["cobertura_proxy_v1"] or 0):
                    d, regla = "TENDENCIA", "§5.3 media: CP95_lo ≥ 0.5 pero MAE_V2 ≤ 0.5·MAE_V1 y proxy_V2 > proxy_V1"
                else:
                    d, regla = "PERSISTE", "§5.3 media: CP95_lo de la cobertura V1 ≥ 0.5"
            else:
                if tend:
                    d, regla = "TENDENCIA", "§5.3 media: CP95_lo < 0.5 y MAE_V2 ≤ 0.5·MAE_V1"
                else:
                    d, regla = "NO-DECIDIBLE", "§5.3 media: CP95_lo < 0.5 y la tendencia no reduce el MAE a la mitad"
    else:
        olas = OLAS_DE[variante]
        s = {o: _celda(r[o], o, variante, "razon", "NACIONAL", "NAC") for o in olas}
        prev = [o for o in olas if ANIO[o] < ANIO[objetivo]]
        o1 = prev[-1]
        obs, piso = s[objetivo], s[o1]
        mutuo = piso["lo"] <= obs["p"] <= piso["hi"] and obs["lo"] <= piso["p"] <= obs["hi"]
        if mutuo:
            d, regla = "PERSISTE", "§5.3 razón: R dentro del IC del piso y piso dentro del IC del R"
        elif len(prev) >= 2:
            o2 = prev[-2]
            d1, d2 = piso["p"] - s[o2]["p"], obs["p"] - piso["p"]
            semi1, semi2 = (piso["hi"] - piso["lo"]) / 2, (obs["hi"] - obs["lo"]) / 2
            if d1 * d2 > 0 and abs(d1) > semi1 and abs(d2) > semi2:
                d, regla = "TENDENCIA", "§5.3 razón: dos cambios consecutivos del mismo signo, cada uno mayor que la semi-anchura del IC destino"
            else:
                d, regla = "NO-DECIDIBLE", "§5.3 razón: sin cobertura mutua y sin dos cambios consecutivos del mismo signo fuera de IC"
        else:
            d, regla = "NO-DECIDIBLE", "§5.3 razón: sin cobertura mutua y sin tercera ola para evaluar tendencia"
    fila["dictamen"], fila["regla_aplicada"] = d, regla
    return fila


def escribe(filas: list[dict], ruta: Path, cols: list[str]) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in filas:
            f.write("\t".join(_f(r.get(c)) if not isinstance(r.get(c), str) else r[c] for c in cols) + "\n")


def main(argv: list[str]) -> int:
    r = _carga()
    filas, dic = deriva(r)
    for d in dic:
        print(f"{d['conducta']:40s} objetivo={d['objetivo']} n={d['n_celdas']:>2} cob_V1={_f(d['cobertura_v1']):>8} "
              f"CP95=[{_f(d['cp95_lo'])},{_f(d['cp95_hi'])}] MAE V1={_f(d['mae_v1'])} V2={_f(d['mae_v2'])} "
              f"V3={_f(d['mae_v3'])} → {d['dictamen']}")
    if "--escribe" in argv:
        escribe(filas, SALIDA_SERIE, COLS_SERIE)
        escribe(dic, SALIDA_DICTAMEN, COLS_DICT)
        print(f"escrito: {SALIDA_SERIE.relative_to(RAIZ)} ({len(filas)} filas) · "
              f"{SALIDA_DICTAMEN.relative_to(RAIZ)} ({len(dic)} filas)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
