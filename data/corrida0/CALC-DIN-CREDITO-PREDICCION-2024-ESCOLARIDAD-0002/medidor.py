from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002 · ACTO
GEN2-DIN-CREDITO-ESCOLARIDAD-2 (22/sep/2026, CAJA). Sucesor de
`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001` para el eje
escolaridad (firma de mesa (a) sobre FP-260922-...-95ec-01). El `-0001` no
se edita (E.3) y sus 12 celdas no-escolaridad siguen vigentes; aquí son el
ORO de este CALC.

**Una sola corrección, nada más.** El `-0001` pasa `niv` (ENIF 2024, dos
dígitos "00".."11" + "99") por `_code()` de `CALC-PISOS-ENIF2021-EJES-0003`,
que quita el cero inicial: "01".."09" dejan de calzar contra el mapa de dos
dígitos y la celda SUPERIOR sólo capta "10"/"11". Aquí `niv` se lee con los
dos dígitos intactos (`_niv_dos_digitos`) y se asigna a cubo con
`NIV_A_ESCOLARIDAD_POR_TEXTO`, derivado del texto de
`catalogos/niv.csv` 2024 contra el de `catalogos/p3_1_1.csv` 2021 (el
árbitro de `_school()`), código por código -- ver spec.md §1.

**Todo lo demás es el código sellado del `-0001`, ejecutado por bytes**
(input `MEDIDOR-ADJ-0001`, sha256 fijado): la guardia de una variable
(`abre_conducta_2024`, que sigue siendo quien PARA con `ReservaRota` antes
de abrir el ZIP), `COLUMNA_2024`, `_desenlace`, `medir()` y el marco
`_cells`/`_estimate` (10 000 réplicas PCG64(42)). Este módulo sólo
reemplaza, en el espacio de nombres de ese módulo cargado, dos nombres:
`PREFIJO` (ids propios, para no chocar con los del `-0001` en el registro)
y `abre_conducta_2024` (envoltura: llama a la guardia sellada y después
reescribe SÓLO `ejes["escolaridad"]` y `codigos["niv"]`).

**Adjudicación: la regla sellada del `-0001`, con universo actualizado
(A.10).** `tools/duelo/credito_prediccion_2024.py` (commit_3 del `-0001`)
y `tools/duelo/cruces_familia.py` se ejecutan por bytes (sha256 fijado):
misma semilla PCG64(20260922), mismo orden de consumo, mismas 10 000
réplicas sintéticas, `umbral_vence_pp=inf`. El único cambio es
`ESCOLARIDAD_EXCLUIDA = ∅` -> 16 celdas puntuables en vez de 12 (bloque
`ADJ16`). El bloque `ORO12` corre la misma regla CON la exclusión original
sobre el R de este CALC: debe reproducir el veredicto del `-0001`.

**Oro de las 12 celdas sanas (E.5):** cada RESULT no-escolaridad del
`-0001` (input `R-ADJ-0001`, sha256 fijado) se compara contra el suyo de
este CALC con tolerancia absoluta `parametros.oro_tolerancia_abs`.
"""
import json
import math
import sys
import types
from pathlib import Path

import pandas as pd

PREFIJO = "DIN-CREDITO-PREDICCION-2024-ESC2"
PREFIJO_0001 = "DIN-CREDITO-PREDICCION-2024-ADJ"

# niv 2024 (catalogos/niv.csv, texto verbatim) -> cubo. Árbitro: el texto de
# catalogos/p3_1_1.csv 2021 y el mapa de _school() de -EJES-0003 (0-2
# hasta_primaria, 3 secundaria, 4-7 media_superior, 8-9 superior).
NIV_A_ESCOLARIDAD_POR_TEXTO = {
    "00": "hasta_primaria",   # Ninguno                                    == 2021 0
    "01": "hasta_primaria",   # Preescolar o kínder                        == 2021 1
    "02": "hasta_primaria",   # Primaria                                   == 2021 2
    "03": "secundaria",       # Secundaria                                 == 2021 3
    "04": "media_superior",   # Normal básica                              == 2021 5
    "05": "media_superior",   # Estudios técnicos con secundaria terminada == 2021 4
    "06": "media_superior",   # Preparatoria o bachillerato                == 2021 6
    "07": "media_superior",   # Estudios técnicos con preparatoria terminada == 2021 7
    "08": "superior",         # Licenciatura o ingeniería (profesional)    == 2021 8
    "09": "superior",         # Especialidad -- sin par textual en 2021; posgrado:
                              # sus dos homólogos posibles (8, 9) son ambos superior
    "10": "superior",         # Maestría                                   ⊂ 2021 9
    "11": "superior",         # Doctorado                                  ⊂ 2021 9
}                             # "99" No sabe -> sin cubo (igual que 2021 99)

CUBOS = ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR")
PISOS = ("PERSISTENCIA", "TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE")
RETADORES = PISOS[1:]


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _niv_dos_digitos(s: pd.Series) -> pd.Series:
    """niv con sus dos dígitos: se conserva tal cual; un dígito suelto se
    completa con cero a la izquierda (mismo código). Nunca quita ceros."""
    v = s.astype(str).str.strip()
    return v.where(~v.str.fullmatch(r"\d"), "0" + v)


def _modulo_0001(inputs):
    src = _bytes(inputs["MEDIDOR-ADJ-0001"])
    mod = types.ModuleType("medidor_adjudicacion_0001")
    exec(compile(src, "medidor_adjudicacion_0001", "exec"), mod.__dict__)
    original = mod.abre_conducta_2024

    def abre_conducta_2024(inputs_, conducta_id, contrato_):
        abierto = original(inputs_, conducta_id, contrato_)   # guardia sellada
        niv = _niv_dos_digitos(abierto["marco"]["niv"])
        abierto["codigos"]["niv"] = niv
        abierto["ejes"]["escolaridad"] = niv.map(NIV_A_ESCOLARIDAD_POR_TEXTO)
        return abierto

    mod.PREFIJO = PREFIJO
    mod.abre_conducta_2024 = abre_conducta_2024
    return mod


def _modulo_adjudicador(inputs):
    """credito_prediccion_2024.py (commit_3 del -0001) por bytes, con
    cruces_familia.py por bytes en su `import`. sys.modules/sys.path se
    restauran al salir."""
    previo_cf = sys.modules.get("cruces_familia")
    ruta_previa = list(sys.path)
    try:
        cf = types.ModuleType("cruces_familia")
        cf.__file__ = inputs["CRUCES-FAMILIA"].get("ruta_absoluta") or "cruces_familia.py"
        sys.modules["cruces_familia"] = cf
        exec(compile(_bytes(inputs["CRUCES-FAMILIA"]), "cruces_familia", "exec"), cf.__dict__)
        adj = types.ModuleType("credito_prediccion_2024_importado")
        adj.__file__ = inputs["ADJUDICADOR-0001"].get("ruta_absoluta") or "credito_prediccion_2024.py"
        exec(compile(_bytes(inputs["ADJUDICADOR-0001"]), "credito_prediccion_2024_importado", "exec"),
             adj.__dict__)
    finally:
        sys.path[:] = ruta_previa
        if previo_cf is None:
            sys.modules.pop("cruces_familia", None)
        else:
            sys.modules["cruces_familia"] = previo_cf
    return adj


def _como_0001(r_esc2: dict) -> dict:
    a, b = f"RESULT-{PREFIJO}-", f"RESULT-{PREFIJO_0001}-"
    return {(b + k[len(a):] if k.startswith(a) else k): v for k, v in r_esc2.items()}


def adjudica_bloque(adj, r_esc2: dict, emisiones: dict, excluye_escolaridad: bool) -> dict:
    """La regla sellada, conducta por conducta, con un generador nuevo de la
    misma semilla (mismo flujo de réplicas que el -0001)."""
    import numpy as np
    adj.ESCOLARIDAD_EXCLUIDA = (
        {f"ESCOLARIDAD-{c}" for c in CUBOS} if excluye_escolaridad else set())
    R_all = _como_0001(r_esc2)
    rng = np.random.Generator(np.random.PCG64(adj.SEED))
    return {cid: adj.adjudica_conducta(cid, R_all, emisiones, rng) for cid in adj.ENTERING}


def _aplana(res: dict, etiqueta: str, completo: bool) -> dict:
    out = {}
    for cid, r in res.items():
        b = f"RESULT-{PREFIJO}-{etiqueta}-{cid}"
        ret = r["retador_primario"]
        fila_p = r["adjudicacion_por_retador"].get(ret) if ret else None
        ic_p = fila_p["delta_ic95"] if fila_p else None
        out[f"{b}-RETADOR-PRIMARIO"] = ret or "NINGUNO-HABILITADO"
        out[f"{b}-VEREDICTO-PRIMARIO"] = (fila_p["veredicto"] if fila_p
                                          else "NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO")
        out[f"{b}-DELTA-MAE-PP"] = fila_p["delta_mae_pp"] if fila_p else None
        out[f"{b}-DELTA-IC95-LO"] = ic_p[0] if ic_p else None
        out[f"{b}-DELTA-IC95-HI"] = ic_p[1] if ic_p else None
        out[f"{b}-N-CELDAS-ELEGIBLES"] = int(r["n_celdas_elegibles"])
        if not completo:
            continue
        for piso in PISOS:
            m = r["mae_por_contendiente"][piso]
            out[f"{b}-{piso}-MAE-PP"] = m["mae_pp"]
            out[f"{b}-{piso}-N-CELDAS-PUNTUADAS"] = int(m["n_celdas_puntuadas"])
        for x in RETADORES:
            f = r["adjudicacion_por_retador"].get(x)
            ic = f["delta_ic95"] if f else None
            cob = f["cobertura"] if f else None
            w = cob["ic95_wilson"] if cob else None
            out[f"{b}-{x}-VEREDICTO"] = f["veredicto"] if f else "NO-HABILITADO"
            out[f"{b}-{x}-ROL"] = f["rol"] if f else "NO-HABILITADO"
            out[f"{b}-{x}-DELTA-MAE-PP"] = f["delta_mae_pp"] if f else None
            out[f"{b}-{x}-DELTA-IC95-LO"] = ic[0] if ic else None
            out[f"{b}-{x}-DELTA-IC95-HI"] = ic[1] if ic else None
            out[f"{b}-{x}-COBERTURA-N"] = int(cob["n_celdas"]) if cob else None
            out[f"{b}-{x}-COBERTURA-EXITOS"] = int(cob["exitos"]) if cob else None
            out[f"{b}-{x}-COBERTURA-P"] = cob["proporcion"] if cob else None
            out[f"{b}-{x}-COBERTURA-WILSON-LO"] = w[0] if w else None
            out[f"{b}-{x}-COBERTURA-WILSON-HI"] = w[1] if w else None
    return out


def _oro(r_esc2: dict, r_0001: dict, tol: float) -> dict:
    a, b = f"RESULT-{PREFIJO_0001}-", f"RESULT-{PREFIJO}-"
    ids = sorted(k for k in r_0001 if k.startswith(a) and "-ESCOLARIDAD-" not in k)
    malos, maxdiff = [], 0.0
    for k in ids:
        v0, v2 = r_0001[k], r_esc2.get(b + k[len(a):], "AUSENTE")
        if v0 is None and v2 is None:
            continue
        if v0 is None or v2 is None or v2 == "AUSENTE":
            malos.append(k)
            continue
        dif = abs(float(v0) - float(v2))
        maxdiff = max(maxdiff, dif)
        if not dif <= tol:
            malos.append(k)
    p = f"RESULT-{PREFIJO}-ORO"
    return {f"{p}-N-COMPARADOS": len(ids), f"{p}-N-DISCORDANTES": len(malos),
            f"{p}-MAX-ABS-DIFF": maxdiff,
            f"{p}-VEREDICTO": "REPRODUCE-ORO" if (ids and not malos) else "NO-REPRODUCE-ORO",
            f"{p}-PRIMEROS-DISCORDANTES": ",".join(malos[:10]) if malos else "NINGUNO"}


def medir(inputs: dict, contrato: dict) -> dict:
    m1 = _modulo_0001(inputs)
    r = m1.medir(inputs, contrato)              # medir() sellado del -0001, niv corregido
    out = dict(r)
    for cid in m1.CONDUCTAS_AUTORIZADAS:
        b = f"RESULT-{PREFIJO}-{cid}"
        out[f"{b}-ESCOLARIDAD-N-SIN-CUBO"] = int(
            r[f"{b}-NACIONAL-TODOS-N"] - sum(r[f"{b}-ESCOLARIDAD-{c}-N"] for c in CUBOS))

    r_0001 = json.loads(_bytes(inputs["R-ADJ-0001"]).decode("utf-8"))
    out.update(_oro(r, r_0001.get("resultados", r_0001),
                    float(contrato["parametros"]["oro_tolerancia_abs"])))

    emis = json.loads(_bytes(inputs["EMISIONES-0001"]).decode("utf-8"))
    emis = emis.get("resultados", emis)
    adj = _modulo_adjudicador(inputs)
    out.update(_aplana(adjudica_bloque(adj, r, emis, excluye_escolaridad=False), "ADJ16", True))
    out.update(_aplana(adjudica_bloque(adj, r, emis, excluye_escolaridad=True), "ORO12", False))
    return out


# ── esquema de resultados (de aquí sale `resultados:` del spec.yaml) ────────

CONDUCTAS = ("K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ", "K3",
             "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES")
CELDAS = ("NACIONAL-TODOS", "SEXO-1", "SEXO-2",
          "EDAD-18-29", "EDAD-30-44", "EDAD-45-59", "EDAD-60-MAS",
          "ESCOLARIDAD-HASTA-PRIMARIA", "ESCOLARIDAD-SECUNDARIA",
          "ESCOLARIDAD-MEDIA-SUPERIOR", "ESCOLARIDAD-SUPERIOR",
          "LOCALIDAD-MENOR-DE-15-000", "LOCALIDAD-15-000-Y-MAS",
          "FORMALIDAD-SIN-SEGURIDAD-SOCIAL", "FORMALIDAD-CON-SEGURIDAD-SOCIAL",
          "UNIVERSO-UNIVERSO-TRABAJA")


def esquema_resultados() -> list[dict]:
    def e(i, t, u, nulo=False):
        d = {"id": i, "tipo": t, "unidad": u}
        if nulo:
            d["permite_no_estimable"] = True
        return d

    S = []
    for cid in CONDUCTAS:
        b = f"RESULT-{PREFIJO}-{cid}"
        for c in CELDAS:
            S += [e(f"{b}-{c}-P", "proporcion", "marginal ponderado ENIF 2024 (universo 18-70), [0,1]", True),
                  e(f"{b}-{c}-IC-LO", "proporcion", "límite inferior IC95 bootstrap, [0,1]", True),
                  e(f"{b}-{c}-IC-HI", "proporcion", "límite superior IC95 bootstrap, [0,1]", True),
                  e(f"{b}-{c}-N", "entero", "n sin ponderar de la celda"),
                  e(f"{b}-{c}-DEN-W", "flotante", "denominador ponderado de la celda"),
                  e(f"{b}-{c}-B-VALIDAS", "entero", "réplicas bootstrap válidas")]
        S += [e(f"{b}-N-UNIVERSO", "entero", "filas con desenlace definido para esa conducta"),
              e(f"{b}-FILAS-18-70", "entero", "filas del marco tras el recorte de edad"),
              e(f"{b}-ESCOLARIDAD-N-SIN-CUBO", "entero",
                "n de NACIONAL-TODOS sin cubo de escolaridad (niv 99 o vacío)")]
    p = f"RESULT-{PREFIJO}-ORO"
    S += [e(f"{p}-N-COMPARADOS", "entero", "RESULT no-escolaridad del -0001 comparados"),
          e(f"{p}-N-DISCORDANTES", "entero", "comparados fuera de oro_tolerancia_abs"),
          e(f"{p}-MAX-ABS-DIFF", "flotante", "máxima diferencia absoluta contra el -0001"),
          e(f"{p}-VEREDICTO", "texto", "REPRODUCE-ORO | NO-REPRODUCE-ORO"),
          e(f"{p}-PRIMEROS-DISCORDANTES", "texto", "hasta 10 ids del -0001 discordantes, o NINGUNO")]
    for etiqueta, completo in (("ADJ16", True), ("ORO12", False)):
        for cid in CONDUCTAS:
            b = f"RESULT-{PREFIJO}-{etiqueta}-{cid}"
            S += [e(f"{b}-RETADOR-PRIMARIO", "texto", "TENDENCIA-X de menor MAE puntual, o NINGUNO-HABILITADO"),
                  e(f"{b}-VEREDICTO-PRIMARIO", "texto", "NADIE-VENCE | PROPUESTA-CON-RESERVA | NO-ADJUDICABLE | NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO"),
                  e(f"{b}-DELTA-MAE-PP", "flotante", "MAE(PERSISTENCIA)-MAE(retador primario), pp", True),
                  e(f"{b}-DELTA-IC95-LO", "flotante", "percentil 2.5 de ΔMAE sobre réplicas sintéticas, pp", True),
                  e(f"{b}-DELTA-IC95-HI", "flotante", "percentil 97.5 de ΔMAE sobre réplicas sintéticas, pp", True),
                  e(f"{b}-N-CELDAS-ELEGIBLES", "entero", "celdas con R y no excluidas")]
            if not completo:
                continue
            for piso in PISOS:
                S += [e(f"{b}-{piso}-MAE-PP", "flotante", "MAE puntual del contendiente, pp", True),
                      e(f"{b}-{piso}-N-CELDAS-PUNTUADAS", "entero", "celdas puntuadas del contendiente")]
            for x in RETADORES:
                S += [e(f"{b}-{x}-VEREDICTO", "texto", "veredicto contra PERSISTENCIA, o NO-HABILITADO"),
                      e(f"{b}-{x}-ROL", "texto", "PRIMARIA | SECUNDARIA | NO-HABILITADO"),
                      e(f"{b}-{x}-DELTA-MAE-PP", "flotante", "MAE(PERSISTENCIA)-MAE(retador), pp", True),
                      e(f"{b}-{x}-DELTA-IC95-LO", "flotante", "percentil 2.5 de ΔMAE, pp", True),
                      e(f"{b}-{x}-DELTA-IC95-HI", "flotante", "percentil 97.5 de ΔMAE, pp", True),
                      e(f"{b}-{x}-COBERTURA-N", "entero", "celdas puntuadas con R dentro/fuera del IC del candidato", True),
                      e(f"{b}-{x}-COBERTURA-EXITOS", "entero", "celdas con R dentro del IC del candidato", True),
                      e(f"{b}-{x}-COBERTURA-P", "proporcion", "proporción de cobertura, [0,1]", True),
                      e(f"{b}-{x}-COBERTURA-WILSON-LO", "proporcion", "IC95 Wilson de la cobertura, [0,1]", True),
                      e(f"{b}-{x}-COBERTURA-WILSON-HI", "proporcion", "IC95 Wilson de la cobertura, [0,1]", True)]
    return S
