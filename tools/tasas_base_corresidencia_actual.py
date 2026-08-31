#!/usr/bin/env python3
"""ACTO MAESTRA33-C1 · RE-SPEC-CORRESIDENCIA — COMMIT-2

Calcula p = proporcion ponderada de corresidencia ACTUAL con ascendiente
o suegro (ventana HOY, no "alguna vez en la vida"), sobre EDER 2017,
segun la spec congelada en
forense/notas/2026-08-31-c1-respec-corresidencia-spec.md (COMMIT-1).

Hereda de tools/tasas_base_fase1.py::regla_familia_corresidencia() el
universo base (vivienda.tipo_adqui no blanco), el ponderador (factor de
vivienda.csv), el estimador (tasa base ponderada) y el metodo de IC
(bootstrap 10k replicas seed=42, FP-168 firmado) -- wprop_ic_bootstrap()
es codigo identico, duplicado por consistencia con el patron ya
establecido en este repo (tasas_base_fase1.py tampoco importa de
medicion_familismo.py pese a compartir universo/colapso).

Lo que cambia es la variable de desenlace: en vez de
historiavida.csv[padre_cor|madre_cor|hnos_cor|suegro_cor|suegra_cor]
(retrospectivo, sin ventana), usa persona.csv[parentesco] (roster ACTUAL
de la ENH 2017). Esa columna esta codificada relativo al jefe(a) de
hogar, no al entrevistado -- por eso el universo evaluable se restringe
a ego con parentesco propio en {Jefe, Conyuge} (unica traduccion limpia,
sin componentes tautologicos ni ambiguedad de catalogo; ver spec S2).

No escribe milpa/tramite.yaml ni milpa/procedencia.yaml. Solo lee
data/raw/eder2017/eder2017_bases_csv.zip. Imprime el resultado; quien
ejecuta el acto pega el output en milpa/tramite-ola5-propuesta-v0.yaml
y en la nota de cierre.

Uso:
    python3 tools/tasas_base_corresidencia_actual.py
"""
import hashlib
import os
import random
import zipfile

import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
SEED = 42
N_BOOT = 10000

# Codigos de persona.csv[parentesco], relativos al jefe(a) de hogar
# (eder2017_fd.pdf, entrada #8, Cuestionario basico Apartado B, pregunta 5).
COD_JEFE = "1"
COD_CONYUGE = "2"
COD_ASCENDIENTE = "6"  # "Madre o padre" (del jefe)
COD_SUEGRO = "7"       # "Suegra(o)" (del jefe)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wprop_ic_bootstrap(desenlace, peso, n_boot=N_BOOT, seed=SEED):
    """proporcion ponderada + IC95 por bootstrap (remuestreo de filas).

    Identica a tools/tasas_base_fase1.py::wprop_ic_bootstrap -- misma
    firma, mismos parametros, para heredar el metodo de IC sin desviar
    una coma (FP-168, seed=42 firmado por mesa).
    """
    d = list(desenlace)
    w = list(peso)
    n = len(d)
    assert n == len(w)
    sw = sum(w)
    p_hat = sum(wi * di for wi, di in zip(w, d)) / sw
    rng = random.Random(seed)
    boots = []
    idx = list(range(n))
    for _ in range(n_boot):
        sample = [idx[rng.randrange(n)] for _ in range(n)]
        sw_b = sum(w[i] for i in sample)
        sp_b = sum(w[i] * d[i] for i in sample)
        boots.append(sp_b / sw_b)
    boots.sort()
    lo = boots[int(0.025 * n_boot)]
    hi = boots[int(0.975 * n_boot) - 1]
    return p_hat, lo, hi, n


def regla_corresidencia_actual():
    zpath = os.path.join(RAW, "eder2017", "eder2017_bases_csv.zip")
    if not os.path.exists(zpath):
        return {"estado": "NO-ENCONTRADO", "razon": f"{zpath} no existe"}
    sha = sha256(zpath)
    z = zipfile.ZipFile(zpath)
    with z.open("vivienda.csv") as f:
        vivienda = pd.read_csv(f, encoding="latin-1", low_memory=False)
    with z.open("persona.csv") as f:
        persona = pd.read_csv(f, encoding="latin-1", low_memory=False)
    with z.open("historiavida.csv") as f:
        hv = pd.read_csv(f, encoding="latin-1", low_memory=False, usecols=lambda c: True)

    fv_col_v = [c for c in vivienda.columns if c.lower().endswith("folioviv")][0]
    fv_col_p = [c for c in persona.columns if c.lower().endswith("folioviv")][0]
    fv_col_h = [c for c in hv.columns if c.lower().endswith("folioviv")][0]

    # Universo respondiente EDER (spec S3): personas.csv[94101 filas, TODAS
    # las edades del hogar] no es el universo -- solo son elegibles quienes
    # tienen fila en historiavida.csv (20-54 anios, el modulo retrospectivo
    # de EDER; identico conjunto de ids que antecedentes.csv, verificado en
    # COMMIT-1 S2). Sin este filtro se cuentan integrantes de cualquier edad
    # que nunca fueron seleccionados para EDER -- error de universo, no de
    # ventana.
    ids_eder = set(
        zip(hv[fv_col_h].astype(str).str.strip(),
            hv["foliohog"].astype(str).str.strip(),
            hv["id_pobla"].astype(str).str.strip())
    )
    n_persona_total = len(persona)

    # Universo heredado de COMMIT-1 / tasas_base_fase1.py: vivienda con
    # tipo_adqui no blanco.
    vivienda["_tipo_adqui_ok"] = vivienda["tipo_adqui"].notna() & (
        vivienda["tipo_adqui"].astype(str).str.strip() != ""
    )
    universo_viv = vivienda[vivienda["_tipo_adqui_ok"]].copy()
    n_universo_viviendas = len(universo_viv)
    pesos_hogar = universo_viv.set_index(fv_col_v)["factor"]

    persona["parentesco"] = persona["parentesco"].astype(str).str.strip()
    persona["_hogar"] = list(zip(persona[fv_col_p], persona["foliohog"]))

    # Por hogar: ¿existe algun integrante con codigo 6 (ascendiente del
    # jefe) y/o codigo 7 (suegro del jefe)? Se calcula sobre el roster
    # COMPLETO (94,101 filas, todas las edades) -- NO restringido a
    # ids_eder: el padre/madre o suegro/a de un ego de 20-54 anios muy
    # plausiblemente tiene 55+ y por eso nunca tendria fila propia en
    # historiavida.csv, pero sigue viviendo en el hogar y debe contar.
    # Restringir esta tabla a ids_eder (como hacia la version anterior de
    # este script) subcontaba "ascendiente presente" -- bug encontrado y
    # corregido en revision antes de reportar ningun p, ver nota de cierre.
    por_hogar = persona.groupby("_hogar")["parentesco"].agg(
        _hay_cod6=lambda s: (s == COD_ASCENDIENTE).any(),
        _hay_cod7=lambda s: (s == COD_SUEGRO).any(),
    )

    persona["_id3"] = list(zip(
        persona[fv_col_p].astype(str).str.strip(),
        persona["foliohog"].astype(str).str.strip(),
        persona["id_pobla"].astype(str).str.strip(),
    ))
    persona_eder = persona[persona["_id3"].isin(ids_eder)]
    n_persona_universo_eder = len(persona_eder)

    ego = persona_eder[persona_eder["parentesco"].isin([COD_JEFE, COD_CONYUGE])].copy()
    n_ego_universo_eder = len(ego)

    ego = ego.join(por_hogar, on="_hogar")

    es_jefe = ego["parentesco"] == COD_JEFE
    es_conyuge = ego["parentesco"] == COD_CONYUGE

    # Jefe: codigo 6 de otro integrante = mi ascendiente; codigo 7 = mi suegro.
    # Conyuge: se invierte -- codigo 7 (suegro DEL JEFE) = mi ascendiente;
    #          codigo 6 (madre/padre DEL JEFE) = mi suegro.
    ascendiente_presente = (es_jefe & ego["_hay_cod6"]) | (es_conyuge & ego["_hay_cod7"])
    suegro_presente = (es_jefe & ego["_hay_cod7"]) | (es_conyuge & ego["_hay_cod6"])
    ego["_desenlace"] = (ascendiente_presente | suegro_presente).astype(int)

    ego["_peso"] = ego[fv_col_p].map(pesos_hogar)
    n_antes_de_peso = len(ego)
    ego = ego.dropna(subset=["_peso"])
    n_con_peso = len(ego)

    p, lo, hi, n = wprop_ic_bootstrap(ego["_desenlace"].tolist(), ego["_peso"].tolist())
    return {
        "estado": "MEDIDO",
        "sha256_payload": sha,
        "n_persona_csv_total_todas_edades": n_persona_total,
        "n_persona_universo_eder_20_54": n_persona_universo_eder,
        "n_universo_viviendas_tipo_adqui_no_blanco": n_universo_viviendas,
        "n_ego_jefe_o_conyuge_eder": n_ego_universo_eder,
        "n_antes_de_peso": n_antes_de_peso,
        "n_con_ponderador": n_con_peso,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
        "nota_ic": "sin campo de diseno UPM/estrato reproducible dentro del "
                   "perimetro de este acto -- bootstrap simple declarado, "
                   "heredado de tasas_base_fase1.py (FP-168, seed=42)",
    }


def fmt(r, nombre):
    print(f"\n=== {nombre} ===")
    if r["estado"] != "MEDIDO":
        print(f"  estado: {r['estado']} -- {r.get('razon')}")
        return
    print(f"  estado: MEDIDO")
    for k, v in r.items():
        if k in ("estado", "p", "ic95"):
            continue
        print(f"  {k}: {v}")
    print(f"  n = {r['n']}")
    print(f"  p = {r['p']:.6f}")
    print(f"  IC95 = [{r['ic95'][0]:.6f}, {r['ic95'][1]:.6f}]")


def main():
    r = regla_corresidencia_actual()
    fmt(r, "familia.corresidencia.adulto_familiar_actual")
    return r


if __name__ == "__main__":
    main()
