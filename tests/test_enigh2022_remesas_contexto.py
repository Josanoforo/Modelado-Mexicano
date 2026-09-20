#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import io
import json
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUTA = ROOT / "data/corrida0/CALC-ENIGH2022-REMESAS-CONTEXTO-0001/medidor.py"
S = importlib.util.spec_from_file_location("remctx", RUTA)
M = importlib.util.module_from_spec(S); S.loader.exec_module(M)


def fila(v, w, r, y, loc="1", ests="1", dis="D1", upm="U1"):
    return [v, "1", w, r, y, loc, ests, dis, upm]


def mide(filas, replicas=40):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.zip"
        s = io.StringIO(newline=""); wr = csv.writer(s); wr.writerow(M.COLUMNAS); wr.writerows(filas)
        with zipfile.ZipFile(p, "w") as z: z.writestr(M.MIEMBRO, s.getvalue().encode("latin-1"))
        total_w = sum(float(x[2]) for x in filas if str(x[3]).strip() not in ("", "nan") and float(x[3]) >= 0)
        rec_w = sum(float(x[2]) for x in filas if str(x[3]).strip() not in ("", "nan") and float(x[3]) > 0)
        c = {"parametros": {"bootstrap_replicas": replicas, "tolerancia_componente_pesos": .01,
             "tolerancia_controles": 99, "controles_nacionales": {"prevalencia": rec_w/total_w}},
             "seed": {"valor": 20260919}}
        return M.medir({M.ZIP_ID: {"ruta_absoluta": str(p)}}, c)


def tabla(r): return json.loads(r[M.P + "TABLA-JSON"])


def test_desconocidos_negativos_y_cero_no_se_reclasifican():
    r = mide([fila("1", 1, "", 10, loc="9"), fila("2", 2, -1, 10, loc="9"),
              fila("3", 3, 0, 10, loc="9"), fila("4", 4, 5, 10, loc="1", upm="U2")])
    t = tabla(r); total = t[0]; resid = next(x for x in t if x["eje"]=="tam_loc" and x["codigo"]=="RESIDUO")
    assert total["remesas_no_validas_n"] == 2 and total["receptores_n"] == 1
    assert resid["elegibles_n"] == 3 and resid["remesas_validas_n"] == 1
    assert any(x["estado"] == "VACIA" for x in t)


def test_mediana_inversa_izquierda():
    assert M.mediana_ponderada([20, 10, 30], [1, 1, 2]) == 20
    assert M.mediana_ponderada([5, 5, 10], [1, 2, 3]) == 5


def test_reconstruccion_usa_masas_y_razones_no_se_intercambian():
    r = mide([fila("1", 1, 10, 10, loc="1", ests="1"),
              fila("2", 9, 10, 100, loc="4", ests="4", upm="U2"),
              fila("3", 5, 0, 50, loc="4", ests="4", upm="U3")])
    t = tabla(r); total=t[0]
    assert abs(total["participacion_media"] - .19) < 1e-12
    assert abs(total["participacion_agregada"] - 100/910) < 1e-12
    assert total["participacion_media"] != total["participacion_agregada"]
    rec = json.loads(r[M.P+"RECONSTRUCCION-JSON"])
    assert abs(rec["tam_loc"]["prevalencia_reconstruida"] - total["prevalencia"]) < 1e-12


def test_contrastes_comparten_replicas_y_direccion_congelada():
    r = mide([fila("1", 1, 10, 20, loc="1", ests="4", upm="U1"),
              fila("2", 1, 0, 20, loc="1", ests="4", upm="U2"),
              fila("3", 1, 10, 10, loc="4", ests="1", upm="U3"),
              fila("4", 1, 10, 20, loc="4", ests="1", upm="U4")])
    c = json.loads(r[M.P+"CONTRASTES-JSON"])
    lp = next(x for x in c if x["eje"]=="tam_loc" and x["estimando"]=="prevalencia")
    assert lp["codigo_a"] == "4" and lp["codigo_b"] == "1"
    assert abs(lp["diferencia"] - .5) < 1e-12 and lp["replicas_validas"] > 0


def test_incompatibilidad_se_reporta_sin_eliminar():
    r = mide([fila("1", 1, 11, 10), fila("2", 1, 0, 20, upm="U2")])
    total = tabla(r)[0]
    assert total["r_mayor_y_n"] == 1
    assert total["estado"] == "REPORTADO-CON-INCOMPATIBILIDAD"
    assert total["participacion_media"] == 1.1


if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_"): f()
    print("OK test_enigh2022_remesas_contexto")
