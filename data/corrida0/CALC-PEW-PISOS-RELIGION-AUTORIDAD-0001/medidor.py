#!/usr/bin/env python3
"""CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001 · pisos por segmento Pew Global Attitudes, México.

ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONFIANZA-PEW-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre PEW.

Olas en corpus con México: 2013, 2015, 2017, 2018, 2023, 2024, 2025. 2025 es la más
reciente y queda RESERVADA (E.6): este código no la lee ni la nombra como input. Se abren
las seis históricas, filas de México por la variable de país de cada ola.

Diseño por ola (spec §3): estrato y UPM donde el archivo los trae; si la UPM declarada falta
en alguna fila de México, esa ola se estima sin conglomerados (se reporta la etiqueta).
IC calibrado de persistencia (receta ENIF-PERSISTENCIA) sólo para las series con texto
idéntico en ≥ 3 olas: RELIGION-MUY-IMPORTANTE (6 olas) y la batería de sistemas de gobierno
(2017, 2023, 2024); se aplica a la última ola abierta de cada serie.
"""
from __future__ import annotations

import types

import numpy as np

P = "RESULT-PEW-PISOS"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
PAYS = {o: f"pew_gas_spring{o}" for o in ("2013", "2015", "2017", "2018", "2023", "2024")}

ESCOL = {"HASTA-PRIMARIA": [1, 2, 3], "SECUNDARIA": [4, 5], "MEDIA-SUPERIOR": [6, 7, 8, 9],
         "SUPERIOR": [10, 11, 12]}
RELIG = ([1], [2, 3, 4])
ORA5 = ([1, 2], [3, 4, 5])
ORA7 = ([1, 2], [3, 4, 5, 6, 7])
POL = ([1, 2], [3, 4])
# ola -> (país, peso, estrato, upm, sexo, edad, escolaridad, {conducta: regla})
OLAS = {
    "2013": (("COUNTRY", 25), "WEIGHT", None, None, "Q164", "Q165", None, {
        "RELIGION-MUY-IMPORTANTE": ("bin", "Q178", *RELIG),
        "ORA-DIARIO": ("bin", "Q176", *ORA5)}),
    "2015": (("COUNTRY", 21), "WEIGHT", "STRATUM_MEX", "PSU", "Q145", "Q146", None, {
        "RELIGION-MUY-IMPORTANTE": ("bin", "Q152", *RELIG),
        "ORA-DIARIO": ("bin", "Q151", *ORA5)}),
    "2017": (("Country", 20), "weight", "STRATUM_MEX", "PSU_MEX", "sex", "age", "d_educ_mexico_2017", {
        "RELIGION-MUY-IMPORTANTE": ("bin", "religion_import", *RELIG),
        "ORA-DIARIO": ("bin", "pray_several", *ORA7),
        "CONFIANZA-INTERPERSONAL": ("bin", "trustpeople", [1], [2, 3]),
        "CONFIA-GOBIERNO-NACIONAL": ("bin", "trust_gov", [1, 2], [3, 4]),
        "GOBIERNO-MILITAR-BUENO": ("bin", "polsys_junta", *POL),
        "LIDER-FUERTE-BUENO": ("bin", "polsys_autocracy", *POL),
        "EXPERTOS-DECIDEN-BUENO": ("bin", "polsys_technocracy", *POL)}),
    "2018": (("COUNTRY", 15), "weight", "STRATUM_MEX", "PSU_MEX", "sex", "age", "d_educ_mexico_2017", {
        "RELIGION-MUY-IMPORTANTE": ("bin", "religion_import", *RELIG),
        "ORA-DIARIO": ("bin", "pray_several", *ORA7)}),
    "2023": (("country", 24), "weight", None, None, "sex", "age", "d_educ_mexico", {
        "RELIGION-MUY-IMPORTANTE": ("bin", "religion_import", *RELIG),
        "ORA-DIARIO": ("bin", "pray_several", *ORA7),
        "GOBIERNO-MILITAR-BUENO": ("bin", "polsys_junta", *POL),
        "LIDER-FUERTE-BUENO": ("bin", "polsys_autocracy", *POL),
        "EXPERTOS-DECIDEN-BUENO": ("bin", "polsys_technocracy", *POL)}),
    "2024": (("country", 35), "weight", None, None, "gender", "age", "d_educ_mexico", {
        "RELIGION-MUY-IMPORTANTE": ("bin", "religion_import", *RELIG),
        "CONFIA-GOBIERNO-NACIONAL": ("bin", "trust_gov", [1, 2], [3, 4]),
        "GOBIERNO-MILITAR-BUENO": ("bin", "polsys_junta", *POL),
        "LIDER-FUERTE-BUENO": ("bin", "polsys_autocracy", *POL),
        "EXPERTOS-DECIDEN-BUENO": ("bin", "polsys_technocracy", *POL)}),
}
SERIES = {  # conducta -> olas con texto idéntico (≥ 3)
    "RELIGION-MUY-IMPORTANTE": ("2013", "2015", "2017", "2018", "2023", "2024"),
    "GOBIERNO-MILITAR-BUENO": ("2017", "2023", "2024"),
    "LIDER-FUERTE-BUENO": ("2017", "2023", "2024"),
    "EXPERTOS-DECIDEN-BUENO": ("2017", "2023", "2024"),
}
CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
        "ESCOLARIDAD": tuple(ESCOL)}


def ejes_de(ola):
    return {e: CATS[e] for e in (("SEXO", "EDAD", "ESCOLARIDAD") if OLAS[ola][6] else ("SEXO", "EDAD"))}


def ejes_serie(conducta):
    comunes = None
    for o in SERIES[conducta]:
        e = set(ejes_de(o))
        comunes = e if comunes is None else comunes & e
    return ["TOTAL"] + [e for e in CATS if e in comunes]


class ParoDeGuardia(RuntimeError):
    pass


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | set(PAYS.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for k in PAYS.values():
        if not inputs[k].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{k}` sin ruta resuelta")
        if "2025" in k:
            raise ParoDeGuardia("ola reservada 2025 entre los inputs")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"{k} sin bytes: se exige origen repo")


def mide_ola(ola, frame, R, M, replicas, semilla):
    pais, peso, est, upm, sexo, edad, educ, conductas = OLAS[ola]
    out = {f"{P}-{ola}-G-FILAS-MEXICO": int(len(frame))}
    if upm is not None and M.num(frame[upm.lower()]).size and not np.all(np.isfinite(M.num(frame[upm.lower()]))):
        upm = None  # UPM declarada con faltantes en México → sin conglomerados (spec §3)
    f, etiqueta, _ = M.prepara_diseno(frame, peso=peso, estrato=est, upm=upm)
    out[f"{P}-{ola}-G-FILAS-DISENO-VALIDO"] = int(len(f))
    ejes = {"SEXO": (M.eje_mapa(f, sexo, {"HOMBRE": [1], "MUJER": [2]}), CATS["SEXO"]),
            "EDAD": (M.edad(f, edad), CATS["EDAD"])}
    if educ:
        ejes["ESCOLARIDAD"] = (M.eje_mapa(f, educ, ESCOL), CATS["ESCOLARIDAD"])
    universo = M.num(f[edad.lower()]) >= 18
    out[f"{P}-{ola}-G-FILAS-18-MAS"] = int(universo.sum())
    out.update(M.mide_ola(R, f, conductas, ejes, P, ola, replicas, semilla, universo=universo))
    out[f"{P}-{ola}-G-DISENO"] = etiqueta
    return out


def compone(frames, R, M, replicas, semilla):
    out = {}
    for ola in OLAS:
        out.update(mide_ola(ola, frames[ola], R, M, replicas, semilla))
    for c, olas in SERIES.items():
        for eje in ejes_serie(c):
            cats = ("TODOS",) if eje == "TOTAL" else CATS[eje]
            out.update(M.persistencia_icc(R, out, P, c, olas, eje, cats))
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    M = _modulo_desde_bytes("motor_pisos_confianza", inputs["motor_pisos_confianza"]["bytes"])
    frames = {}
    for ola, (pais, peso, est, upm, sexo, edad, educ, conductas) in OLAS.items():
        cols = [r[1] for r in conductas.values()] + [c for c in (peso, est, upm, sexo, edad, educ) if c]
        frames[ola] = M.lee(inputs[PAYS[ola]]["ruta_absoluta"], cols, miembro_sufijo=".sav", pais=pais)
    out = compone(frames, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "PEW 2025 RESERVADA (E.6): no es input de este CALC"
    return out


def esquema_resultados():
    import importlib.util
    import pathlib
    ruta = pathlib.Path(__file__).resolve().parents[3] / "tools/dominios/confianza/motor_pisos.py"
    spec = importlib.util.spec_from_file_location("motor_pisos_confianza", ruta)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    f = []
    for ola, t in OLAS.items():
        f += [M.fila(f"{P}-{ola}-G-{k}", "entero", "filas")
              for k in ("FILAS-MEXICO", "FILAS-DISENO-VALIDO", "FILAS-18-MAS")]
        f += M.esquema_ola(P, ola, t[7], ejes_de(ola))
        f += [M.fila(f"{P}-{ola}-G-DISENO", "texto", "etiqueta de diseño")]
    for c, olas in SERIES.items():
        for eje in ejes_serie(c):
            f += M.esquema_persistencia(P, c, olas[-1], eje, ("TODOS",) if eje == "TOTAL" else CATS[eje])
    f += [M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"), M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
