#!/usr/bin/env python3
"""CALC-ENVIPE-PERCEPCION-2024-0001 · percepción de inseguridad y cambio de hábitos, ENVIPE 2024.

ACTO GEN2-COLA-COMPLETA-1 (26/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/COLA-ENVIPE-PERCEPCION-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre estos reactivos de ENVIPE 2024.

ENVIPE 2026 queda RESERVADA (decisiones.tsv `reserva:envipe2026`); 2024 está abierta (piso de ejes
sellado en CALC-PISOS-ENVIPE2024-EJES-0001/-0002 sobre otras conductas). Este código sólo lee la
tabla de persona elegida (`tper_vic1`) y, por `ID_PER`, el nivel de escolaridad de `tsdem`.
Persona de 18+ con `FAC_ELE` > 0; bootstrap de UPM (`UPM_DIS`) dentro de estrato (`EST_DIS`).
"""
from __future__ import annotations

import types

P = "RESULT-ENVIPE-PERCEPCION-2024"
OLA = "2024"
PAY = "envipe2024_csv"
MIEMBRO_PER = "conjunto_de_datos_tper_vic1_envipe2024.csv"
MIEMBRO_SDEM = "conjunto_de_datos_tsdem_envipe2024.csv"
INPUTS_REPO = frozenset({"receta_pisos_salud", "motor_pisos_confianza"})
EXCLUIDOS_PREFIJO = ("envipe2026", "envipe_2026", "cc1_inegi_envipe_2026")

CONDUCTAS = {
    "ESTADO-INSEGURO": ("bin", "AP4_3_3", [2], [1]),
    "INSEGURO-CAMINAR-DE-NOCHE": ("bin", "AP4_4_A", [3, 4], [1, 2]),
    "DEJO-PERMITIR-MENORES-SALIR-SOLOS": ("bin", "AP4_10_02", [1], [2]),
}
MAPAS = {
    "SEXO": ("SEXO", {"HOMBRE": [1], "MUJER": [2]}),
    "ESCOLARIDAD": ("NIV", {"HASTA-PRIMARIA": [0, 1, 2], "SECUNDARIA": [3, 4, 5],
                            "MEDIA-SUPERIOR": [6, 7], "SUPERIOR": [8, 9]}),
    "ENTIDAD": ("CVE_ENT", {f"{e:02d}": [e] for e in range(1, 33)}),
}
EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97))
COLS_PER = ("ID_PER", "AP4_3_3", "AP4_4_A", "AP4_10_02", "SEXO", "EDAD", "CVE_ENT", "DOMINIO",
            "FAC_ELE", "EST_DIS", "UPM_DIS")
COLS_SDEM = ("ID_PER", "NIV")
EJES_CATS = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": tuple(c for c, _, _ in EDADES),
             "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
             "DOMINIO": ("URBANO", "COMPLEMENTO-URBANO", "RURAL"),
             "ENTIDAD": tuple(f"{e:02d}" for e in range(1, 33))}
_DIAG = ("FILAS-LEIDAS", "FILAS-DISENO-VALIDO", "FILAS-18-MAS", "FILAS-CON-NIV")


class ParoDeGuardia(RuntimeError):
    pass


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | {PAY}
    malos = {k for k in inputs if k.startswith(EXCLUIDOS_PREFIJO)}
    if malos or set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted((set(inputs) ^ esperados) | malos)}")
    if not inputs[PAY].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{PAY}` sin ruta resuelta")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"{k} sin bytes: se exige origen repo")


def columnas():
    return list(dict.fromkeys(COLS_PER + COLS_SDEM))


def une(per, sdem):
    """Añade `niv` de tsdem por `id_per` (persona elegida); sin pareja → NaN, se cuenta."""
    s = sdem[["id_per", "niv"]].copy()
    s["id_per"] = s["id_per"].astype(str).str.strip()
    s = s.drop_duplicates("id_per")
    f = per.copy()
    f["id_per"] = f["id_per"].astype(str).str.strip()
    return f.merge(s, on="id_per", how="left")


def mide(per, sdem, R, M, replicas, semilla):
    diag = {"FILAS-LEIDAS": int(len(per))}
    f, etiqueta, _ = M.prepara_diseno(une(per, sdem), peso="FAC_ELE", estrato="EST_DIS", upm="UPM_DIS")
    diag["FILAS-DISENO-VALIDO"] = int(len(f))
    diag["FILAS-CON-NIV"] = int((M.num(f["niv"]) >= 0).sum())
    ejes = {e: (M.eje_mapa(f, col, mapa), EJES_CATS[e]) for e, (col, mapa) in MAPAS.items()}
    ejes["EDAD"] = (M.eje_rango(f, "EDAD", EDADES), EJES_CATS["EDAD"])
    dom = f["dominio"].astype(str).str.strip().map({"U": "URBANO", "C": "COMPLEMENTO-URBANO", "R": "RURAL"})
    ejes["DOMINIO"] = (dom.to_numpy(dtype=object), EJES_CATS["DOMINIO"])
    ejes = {e: ejes[e] for e in EJES_CATS}
    edad = M.num(f["edad"])
    universo = (edad >= 18) & (edad <= 97)
    diag["FILAS-18-MAS"] = int(universo.sum())
    out = {f"{P}-G-{k}": v for k, v in diag.items()}
    out.update(M.mide_ola(R, f, CONDUCTAS, ejes, P, OLA, replicas, semilla, universo=universo))
    out[f"{P}-G-DISENO"] = etiqueta
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    M = _modulo_desde_bytes("motor_pisos_confianza", inputs["motor_pisos_confianza"]["bytes"])
    ruta = inputs[PAY]["ruta_absoluta"]
    per = R.lee_csv_zip(ruta, list(COLS_PER), miembro=f"tper_vic1_envipe2024/conjunto_de_datos/{MIEMBRO_PER}")
    sdem = R.lee_csv_zip(ruta, list(COLS_SDEM), miembro=f"tsdem_envipe2024/conjunto_de_datos/{MIEMBRO_SDEM}")
    out = mide(per, sdem, R, M, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    for k in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256"] = str(inputs[k].get("sha256"))
    out[f"{P}-G-OLA-ABIERTA"] = "ENVIPE 2024 -- abierta; 2026 RESERVADA (E.6), no es input; sin IC de persistencia"
    return out


def _motor():
    import importlib.util
    import pathlib
    ruta = pathlib.Path(__file__).resolve().parents[3] / "tools/dominios/confianza/motor_pisos.py"
    spec = importlib.util.spec_from_file_location("motor_pisos_confianza", ruta)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    return M


def esquema_resultados():
    M = _motor()
    f = [M.fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    f += M.esquema_ola(P, OLA, CONDUCTAS, EJES_CATS)
    f += [M.fila(f"{P}-G-DISENO", "texto", "etiqueta de diseño"),
          M.fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          M.fila(f"{P}-G-SEED", "entero", "semilla")]
    f += [M.fila(f"{P}-G-INPUT-{k.upper().replace('_', '-')}-SHA256", "texto", "sha256") for k in sorted(INPUTS_REPO)]
    f += [M.fila(f"{P}-G-OLA-ABIERTA", "texto", "declaración")]
    return f
