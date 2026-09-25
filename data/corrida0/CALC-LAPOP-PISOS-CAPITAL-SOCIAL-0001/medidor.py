#!/usr/bin/env python3
"""CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001 · pisos por segmento LAPOP México (reactivos nuevos).

ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONFIANZA-LAPOP-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre estos reactivos.

Olas LAPOP en corpus: 2004, 2006, 2019, 2021, 2023. 2023 es la más reciente y queda
RESERVADA para los reactivos de este CALC (E.6): no es input. 2021 (CATI, RDD móvil) queda
fuera por ruptura de modo y porque no trae `q1`/`ed`/`ur` ni casi ningún reactivo de la lista
(declarado en la spec). Diseño por ola: el mismo de `LAPOP-PISOS-OLAS-spec-v1_0.md`
(ASTRA5-U3-POLITICA-COMPLETAR). FIRMAS-15 T: LAPOP sin serie hasta dictamen de equivalencia
→ cada ola es un piso propio; ni τ² ni IC calibrado.
"""
from __future__ import annotations

import types


P = "RESULT-LAPOP-PISOS-CS"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
PAYS = {"2004": "642348348mexico_2004_export_version",
        "2006": "518939279mexico_lapop_final_2006_data_set_092906",
        "2019": "mexico_lapop_americasbarometer_2019_v1_0_w"}

A7 = ([6, 7], [1, 2, 3, 4, 5])          # confianza 1–7: 6 ó 7 (mismo corte sellado para b18/b21)
MES = ([1, 2], [3, 4])                  # asiste semanal o mensual vs. anual/nunca
T10 = ([6, 7, 8, 9, 10], [1, 2, 3, 4, 5])  # mitad superior de 1–10 (mismo corte sellado para d1–d4)
BASE = {
    "CONFIANZA-INTERPERSONAL": ("bin", "it1", [1, 2], [3, 4]),
    "CONFIA-FFAA": ("bin", "b12", *A7),
    "CONFIA-CONGRESO": ("bin", "b13", *A7),
    "CONFIA-IGLESIA-CATOLICA": ("bin", "b20", *A7),
    "CONFIA-MEDIOS": ("bin", "b37", *A7),
    "ASISTE-ORG-RELIGIOSA": ("bin", "cp6", *MES),
    "ASISTE-ASOC-PADRES": ("bin", "cp7", *MES),
    "ASISTE-COMITE-MEJORAS": ("bin", "cp8", *MES),
    "ASISTE-PARTIDO": ("bin", "cp13", *MES),
    "GOLPE-JUSTIFICADO-DELINCUENCIA": ("bin", "jc10", [1], [2]),
    "GOLPE-JUSTIFICADO-CORRUPCION": ("bin", "jc13", [1], [2]),
    "APRUEBA-HOMOSEXUALES-CANDIDATOS": ("bin", "d5", *T10),
}
SOLO_0406 = {
    "CONFIA-JUSTICIA": ("bin", "b10a", *A7),
    "CONFIA-GOBIERNO": ("bin", "b14", *A7),
    "ASISTE-ASOC-PROFESIONAL": ("bin", "cp9", *MES),
    "AYUDO-RESOLVER-PROBLEMA-COMUNIDAD": ("bin", "cp5", [1], [2]),
    "LIDER-FUERTE-NO-ELEGIDO": ("bin", "aut1", [1], [2]),
    "APRUEBA-JUSTICIA-PROPIA-MANO": ("bin", "e16", *T10),
}
SOLO_2019 = {
    "RELIGION-MUY-IMPORTANTE": ("bin", "q5b", [1], [2, 3, 4]),
    "ASISTE-SERVICIO-MENSUAL": ("bin", "q5a", [1, 2, 3], [4, 5]),
}
# ola -> (peso, estrato, upm, {conducta: regla})
OLAS = {
    "2004": (None, "mestrat", ("mprov", "msec"), {**BASE, **SOLO_0406}),
    "2006": (None, "estratopri", "upm", {**BASE, **SOLO_0406}),
    "2019": ("wt", "estratopri", "upm", {**BASE, **SOLO_2019}),
}
ESCOL = (("HASTA-PRIMARIA", 0, 6), ("SECUNDARIA", 7, 9), ("MEDIA-SUPERIOR", 10, 12), ("SUPERIOR", 13, 30))
CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
        "ESCOLARIDAD": tuple(c for c, _, _ in ESCOL), "UR": ("URBANO", "RURAL")}


def ejes_de(ola):
    return dict(CATS)


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
        if "2023" in k or "2021" in k:
            raise ParoDeGuardia("ola reservada (2023) o excluida (2021) entre los inputs")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"{k} sin bytes: se exige origen repo")


def mide_ola(ola, frame, R, M, replicas, semilla):
    peso, est, upm, conductas = OLAS[ola]
    out = {f"{P}-{ola}-G-FILAS-LEIDAS": int(len(frame))}
    f, etiqueta, _ = M.prepara_diseno(frame, peso=peso, estrato=est, upm=upm)
    out[f"{P}-{ola}-G-FILAS-DISENO-VALIDO"] = int(len(f))
    ejes = {"SEXO": (M.eje_mapa(f, "q1", {"HOMBRE": [1], "MUJER": [2]}), CATS["SEXO"]),
            "EDAD": (M.edad(f, "q2"), CATS["EDAD"]),
            "ESCOLARIDAD": (M.eje_rango(f, "ed", ESCOL), CATS["ESCOLARIDAD"]),
            "UR": (M.eje_mapa(f, "ur", {"URBANO": [1], "RURAL": [2]}), CATS["UR"])}
    universo = M.num(f["q2"]) >= 18
    out[f"{P}-{ola}-G-FILAS-18-MAS"] = int(universo.sum())
    out.update(M.mide_ola(R, f, conductas, ejes, P, ola, replicas, semilla, universo=universo))
    out[f"{P}-{ola}-G-DISENO"] = etiqueta
    return out


def compone(frames, R, M, replicas, semilla):
    out = {}
    for ola in OLAS:
        out.update(mide_ola(ola, frames[ola], R, M, replicas, semilla))
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    M = _modulo_desde_bytes("motor_pisos_confianza", inputs["motor_pisos_confianza"]["bytes"])
    frames = {}
    for ola, (peso, est, upm, conductas) in OLAS.items():
        ups = (upm,) if isinstance(upm, str) else tuple(upm)
        cols = [r[1] for r in conductas.values()] + [c for c in (peso, est) if c] + list(ups) + ["q1", "q2", "ed", "ur"]
        frames[ola] = M.lee(inputs[PAYS[ola]]["ruta_absoluta"], cols)
    out = compone(frames, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "LAPOP 2023 RESERVADA para estos reactivos (E.6); 2021 fuera por ruptura de modo; sin serie (FIRMAS-15 T)"
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
              for k in ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-18-MAS")]
        f += M.esquema_ola(P, ola, t[3], ejes_de(ola))
        f += [M.fila(f"{P}-{ola}-G-DISENO", "texto", "etiqueta de diseño")]
    f += [M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"), M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
