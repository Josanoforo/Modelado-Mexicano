"""Genera `data/corrida0/CALC-<INST>-SERIE-DICTAMEN-0001/{spec.yaml,medidor.py}`
(DONDE-CAMBIO spec v1.0 §6) a partir del mapa congelado, sin leer valores.

Uso: PYTHONPATH=. python3 tools/series/genera_calcs.py
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from tools.series import calc_serie as S
from tools.series import dictamen as D

RAIZ = Path(__file__).resolve().parents[2]
MAPA = RAIZ / "forense/analisis/donde-cambio/mapa"
SPEC_MD = RAIZ / "forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md"
TAU_SELLADO = {"ENIF": "CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001",
               "ENCIG": "CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001"}
FRAGMENTO = {"ENVIPE": "envipe", "ENCIG": "encig", "ENIF": "enif", "ENUT": "enut",
             "ENIGH": "enigh", "ENOE": "resto", "ENDIREH": "resto", "MOCIBA": "resto"}
OTROS = ["BANXICO", "EDER", "ENCUCI", "ENFIH", "ENNVIH", "ENSANUT", "LAPOP", "MOTRAL"]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _rel(p):
    return str(Path(p).resolve().relative_to(RAIZ))


def _entrada(i, funcion, ruta):
    return f"  - {{id: {i}, origen: repo, funcion: {funcion}, ruta: {_rel(ruta)}, sha256: {_sha(ruta)}}}"


def genera(nombre, instrumentos, fragmento):
    calc = f"CALC-{nombre}-SERIE-DICTAMEN-0001"
    pref = f"RESULT-DC-{nombre}"
    mapa = MAPA / f"{fragmento}.tsv"
    texto = mapa.read_text(encoding="utf-8")
    filas = [f for f in D.lee_mapa(texto) if f["instrumento"] in instrumentos]
    calcs = sorted({f["calc"] for f in filas})
    d = RAIZ / "data/corrida0" / calc
    d.mkdir(parents=True, exist_ok=True)
    (d / "medidor.py").write_text(
        '"""Entrada corrida0 de DONDE-CAMBIO (spec v1.0 §6)."""\n'
        "from tools.series.calc_serie import medir\n\n__all__ = [\"medir\"]\n",
        encoding="utf-8")
    inst = instrumentos[0] if len(instrumentos) == 1 else instrumentos
    ins = [_entrada("MEDIDOR-CALC-SERIE", "CODIGO", RAIZ / "tools/series/calc_serie.py"),
           _entrada("MEDIDOR-DICTAMEN", "CODIGO", RAIZ / "tools/series/dictamen.py"),
           _entrada("MAPA", "METADATO", mapa)]
    if isinstance(inst, str) and inst in TAU_SELLADO:
        ins.append(_entrada("TAU2-SELLADO", "DATO",
                            RAIZ / "data/corrida0" / TAU_SELLADO[inst] / "resultados.json"))
    ins += [_entrada(f"SRC-{c}", "DATO", RAIZ / "data/corrida0" / c / "resultados.json")
            for c in calcs]
    res = []
    for i, tipo, nulo in S.ids_resultado(texto, set(instrumentos), pref):
        unidad = {"entero": "conteo", "texto": "texto", "flotante":
                  ("segundo momento en escala logit" if "-TAU2-" in i else "puntos porcentuales")}[tipo]
        extra = ", permite_no_estimable: true" if nulo else ""
        res.append(f"  - {{id: {i}, tipo: {tipo}, unidad: \"{unidad}\"{extra}}}")
    inst_yaml = f"\"{inst}\"" if isinstance(inst, str) else "[" + ", ".join(f'"{x}"' for x in inst) + "]"
    y = f"""# El primer resultado que produzca este procedimiento es el que se reporta.
calc_id: {calc}
spec_md: ../../../{_rel(SPEC_MD)}
spec_md_sha256: {_sha(SPEC_MD)}
script: data/corrida0/{calc}/medidor.py
etiquetas:
  generacion: GEN2
  tipo: DICTAMEN-SERIE-RETROSPECTIVA
  cuenta_gen2: SI
  adopta: 'NO'
  origen_numerico: NUEVO
  origen_numerico_detalle: dictamen sobre RESULT sellados de {len(calcs)} CALC; sin microdato
  exposicion_historica: SIN-VALORES-PRE-FREEZE; mapa congelado en forense/analisis/donde-cambio/mapa/CONGELADO.md
inputs:
{chr(10).join(ins)}
variables: []
universo: "Series (instrumento, conducta, eje, segmento) del mapa congelado con instrumento en {instrumentos}."
filtros: "tramo = corrida mas larga de olas unidas por COMPARABLE o CAMBIO-DOCUMENTADO con p, lo, hi en (0,1); spec §2."
ponderador: "el de cada CALC origen; esta corrida consume sus RESULT"
transformacion: "spec §3-§4: piso t-1 cubre t si p_b en expit(logit p_a +/- 1.959964 sqrt(ee_a^2 + tau2)); dictamen por la primera regla que se cumpla."
estimando: "Dictamen cerrado por serie: SIN-SERIE, CAMBIO-SOSTENIDO, SALTO-DE-INSTRUMENTO, SALTO-SIN-EXPLICAR, ESTABLE. RETROSPECTIVA."
seed: {{aplica: false, nota: "determinista, sin remuestreo"}}
parametros:
  instrumento: {inst_yaml}
  prefijo: {pref}
  z_95: 1.959964
  tau2_fuente: "{('SELLADO ' + TAU_SELLADO[inst]) if isinstance(inst, str) and inst in TAU_SELLADO else 'CALCULADO-AQUI spec §3.3'}"
dependencias_materiales: []
resultados:
{chr(10).join(res)}
tolerancia: {{tipo: flotante, abs: 1.0e-10}}
"""
    (d / "spec.yaml").write_text(y, encoding="utf-8")
    return calc, len(filas), len(res)


def main():
    lotes = [(k, [k], v) for k, v in FRAGMENTO.items()] + [("OTROS", OTROS, "resto")]
    for nombre, insts, frag in lotes:
        print(*genera(nombre, insts, frag))


if __name__ == "__main__":
    main()
