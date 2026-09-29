"""GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · el mapa v1.2 solo cambia columnas de estado.

Defecto que atrapa: el mapa v1.1 citaba como «ninguna corrida» afirmaciones con
RESULT GEN2 ya registrados en la vista, y el tablero de carriles lo heredaba. Un
v1.2 que pierda o añada filas, cambie dominio/report/texto de una afirmación, o
marque `gen2_existente` sin fila en la vista (E.7), le cambiaría el carril a un
lector sin que nadie lo decidiera.
"""
import csv
import pathlib
import sys

import pytest  # invocador pytest en ci_guardias: sin `__main__`, como script saldría 0 sin correr nada

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "forense/analisis/mapa-dominios-1-2"))
csv.field_size_limit(10**9)

ESTADO = {"dictamen", "gen2_existente", "siguiente_operacion"}


def _lee(rel):
    with (RAIZ / rel).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_llaves_y_columnas_no_de_estado_identicas():
    v11, v12 = _lee("canon/mapa-dominios-v1_1.tsv"), _lee("canon/mapa-dominios-v1_2.tsv")
    assert len(v11) == len(v12) == 1396
    assert [x["id_afirmacion"] for x in v11] == [y["id_afirmacion"] for y in v12]
    assert list(v12[0])[: len(v11[0])] == list(v11[0])
    for x, y in zip(v11, v12):
        for c in v11[0]:
            if c in ESTADO:
                continue
            assert x[c] == y[c], (x["id_afirmacion"], c)
        if x["dictamen"] != y["dictamen"]:
            assert "dictamen" in y["cambio_v1_2"], x["id_afirmacion"]


def test_gen2_existente_solo_y_siempre_con_fila_en_la_vista():
    import deriva_mapa_v1_2 as d

    usada = (RAIZ / "forense/analisis/mapa-dominios-1-2/vista-usada.txt").read_text().strip()
    if d.tc.blob("data/corrida0/resultados.tsv") != usada:
        pytest.skip("la vista cambió desde la derivación de v1.2: VENCIDO EN ALCANCE (A.10); re-derivar en v1.3")

    mapa = _lee("canon/mapa-dominios-v1_1.tsv")
    pats = d.patrones_tablero(d.lee(d.V11))
    union = d.union(mapa, pats, d.indice_calc(d.vista().keys(), pats))
    v12 = {y["id_afirmacion"]: y for y in _lee("canon/mapa-dominios-v1_2.tsv")}
    faltantes = [a for a, c in union.items() if c and not v12[a]["gen2_existente"].startswith("VISTA:")]
    sin_vista = [a for a, y in v12.items() if y["gen2_existente"].startswith("VISTA:") and not union[a]]
    assert not faltantes, f"afirmaciones con RESULT en la vista sin gen2_existente: {faltantes[:10]}"
    assert not sin_vista, f"gen2_existente VISTA sin fila en la vista: {sin_vista[:10]}"


def test_tablero_lee_v1_2():
    # GEN2-TUBERIA-TABLERO-UNICO-1: la versión ya no se teclea en tablero_carriles.py; se resuelve de la serie más alta.
    # La intención de este guardia (el tablero lee el mapa v1_2 o uno posterior) se conserva por comportamiento.
    import re
    import sys
    sys.path.insert(0, str(RAIZ / "tools"))
    import tablero_carriles as TC
    m = re.fullmatch(r"canon/mapa-dominios-v(\d+)_(\d+)\.tsv", TC.FUENTES["F1"])
    assert m and (int(m.group(1)), int(m.group(2))) >= (1, 2), TC.FUENTES["F1"]
