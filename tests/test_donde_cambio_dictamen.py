"""Sintético del dictamen DONDE-CAMBIO (spec v1.0 §2-§4): cada rama del vocabulario."""
import math
from tools.series import dictamen as D

CAB = "serie_id\tinstrumento\tdominio\tconducta\tconducta_texto\teje\tsegmento\tunidad\tola\tcalc\tresult_p\tresult_lo\tresult_hi\tpar_con_anterior\tcita_par\tmarca_2020\tnota"


def _mapa(series):
    L, vals = [CAB], {}
    for sid, olas in series.items():
        for i, (ola, p, est) in enumerate(olas):
            r = f"R-{sid}-{ola}"
            vals[r + "-P"], vals[r + "-LO"], vals[r + "-HI"] = p, p * 0.98, min(p * 1.02, 0.999)
            L.append("\t".join([sid, "X", "d", "c", "c", "E", "s", "P", ola, "C",
                                r + "-P", r + "-LO", r + "-HI",
                                "PRIMERA" if i == 0 else est, "", "NO", ""]))
    return D.lee_mapa("\n".join(L)), vals


def _corre(series, tau=None):
    filas, vals = _mapa(series)
    return D.evalua(filas, vals, tau)[0]


def test_ramas():
    C, X = "COMPARABLE", "CAMBIO-DOCUMENTADO"
    out = _corre({
        "EST": [("1", .30, C), ("2", .30, C), ("3", .30, C)],
        "SOS": [("1", .20, C), ("2", .40, C), ("3", .60, C)],
        "SAL": [("1", .30, C), ("2", .30, C), ("3", .60, X)],
        "SSE": [("1", .30, C), ("2", .30, C), ("3", .60, C)],
        "COR": [("1", .30, C), ("2", .30, "NO-DOCUMENTADO"), ("3", .30, C)],
    }, tau={"E": 0.001})
    assert out["EST"]["dictamen"] == "ESTABLE"
    assert out["SOS"]["dictamen"] == "CAMBIO-SOSTENIDO" and out["SOS"]["direccion"] == "SUBE"
    assert out["SAL"]["dictamen"] == "SALTO-DE-INSTRUMENTO"
    assert out["SSE"]["dictamen"] == "SALTO-SIN-EXPLICAR"
    assert out["COR"]["dictamen"] == "SIN-SERIE" and out["COR"]["k"] == 2
    assert set(r["dictamen"] for r in out.values()) <= set(D.VOCAB)


def test_tau_calculado_excluye_documentado():
    C, X = "COMPARABLE", "CAMBIO-DOCUMENTADO"
    filas, vals = _mapa({"A": [("1", .3, C), ("2", .4, C), ("3", .9, X)]})
    _, tau, fuente = D.evalua(filas, vals, None)
    assert fuente == "CALCULADO-AQUI"
    assert math.isclose(tau["E"], (D._logit(.4) - D._logit(.3)) ** 2)


def test_mixto_empate_no_es_sostenido():
    C = "COMPARABLE"
    out = _corre({"M": [("1", .2, C), ("2", .5, C), ("3", .2, C), ("4", .5, C), ("5", .2, C)]},
                 tau={"E": 0.001})
    assert out["M"]["dictamen"] == "SALTO-SIN-EXPLICAR"


def test_medir_celdas_de_tabla_por_calc():
    """Misma RESULT-*-TABLA en dos CALC; valor con '/' y '&' escapado; ic95[i]."""
    import json
    from urllib.parse import quote
    from tools.series import calc_serie as S
    seg = quote("15-29/a&b", safe="")
    L = [CAB]
    for i, (ola, calc) in enumerate([("1", "CALC-A"), ("2", "CALC-B"), ("3", "CALC-C")]):
        d = f"RESULT-T-TABLA#resultado=r&eje=edad&categoria={seg}"
        L.append("\t".join(["S", "X", "d", "c", "c", "edad", "s", "P", ola, calc,
                            d + "/p", d + "/ic95[0]", d + "/ic95[1]",
                            "PRIMERA" if i == 0 else "COMPARABLE", "", "NO", "CELDA-DE-TABLA"]))
    def src(p):
        celdas = [{"resultado": "r", "eje": "edad", "categoria": "15-29/a&b",
                   "p": p, "ic95": [p - .01, p + .01]},
                  {"resultado": "r", "eje": "edad", "categoria": "otra",
                   "p": .9, "ic95": [.89, .91]}]
        return {"bytes": json.dumps({"resultados": {"RESULT-T-TABLA": json.dumps(celdas)}}).encode()}
    inputs = {"MAPA": {"bytes": "\n".join(L).encode()},
              "SRC-CALC-A": src(.30), "SRC-CALC-B": src(.30), "SRC-CALC-C": src(.30)}
    out = S.medir(inputs, {"parametros": {"instrumento": "X", "prefijo": "RESULT-X"}})
    assert out["RESULT-X-S-K"] == 3 and out["RESULT-X-S-DICTAMEN"] == "ESTABLE"
    assert json.loads(out["RESULT-X-TABLA"])[0]["dictamen"] == "ESTABLE"
    assert out["RESULT-X-N-SERIES"] == 1
    decl = {i for i, _, _ in S.ids_resultado("\n".join(L), {"X"}, "RESULT-X")}
    assert decl == set(out), decl ^ set(out)


if __name__ == "__main__":
    test_ramas(); test_tau_calculado_excluye_documentado(); test_mixto_empate_no_es_sostenido()
    test_medir_celdas_de_tabla_por_calc()
    print("OK")
