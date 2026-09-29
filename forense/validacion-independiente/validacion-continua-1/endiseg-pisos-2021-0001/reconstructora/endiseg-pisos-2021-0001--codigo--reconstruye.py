"""Reconstrucción independiente CALC-ENDISEG-PISOS-2021-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo): python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
CSV = os.path.join(PAQ, "datos", "tmodulo.csv")
ESQ = os.path.join(PAQ, "esquema-identidades.tsv")

IDENTIDAD = {
    "paquete": "endiseg-pisos-2021-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "abb596fb21b81b422a2d297fbe8627bd6c63107e976b0829e8335908bd3b2c36",
}

# Columnas autorizadas (y únicas que exige la spec).
COLS = ["P8_1", "P9_1", "P7_1", "P7_1A", "NIV", "P4_2", "P4_7", "P4_4", "ENT",
        "P4_1", "FACTOR", "EST_DIS", "UPM_DIS"]

SEMILLA = 20260926
N_REP = 2000
BLOQUE = 50


def num(s):
    return pd.to_numeric(s.str.strip(), errors="coerce")


def carga():
    d = pd.read_csv(CSV, usecols=COLS, dtype=str, keep_default_na=False)
    n_total = len(d)
    edad = num(d["P4_1"])
    w = num(d["FACTOR"])
    est = d["EST_DIS"].str.strip()
    upm = d["UPM_DIS"].str.strip()
    excl = {}
    m_edad = edad.between(15, 96)
    excl["P4_1_fuera_15_96"] = int((~m_edad).sum())
    m_w = w > 0
    excl["FACTOR_no_positivo_o_vacio"] = int((m_edad & ~m_w).sum())
    m_dis = (est != "") & (upm != "")
    excl["EST_DIS_o_UPM_DIS_vacio"] = int((m_edad & m_w & ~m_dis).sum())
    d = d[m_edad & m_w & m_dis].reset_index(drop=True)
    return d, {"n_filas_archivo": n_total, "n_universo": len(d), "exclusiones_universo": excl}


def conductas(d):
    """Devuelve dict conducta -> Serie float (1.0 / 0.0 / NaN fuera)."""
    p81 = num(d["P8_1"])
    p91 = num(d["P9_1"])
    p71 = num(d["P7_1"])
    p71a = num(d["P7_1A"])
    niv = num(d["NIV"])
    p42 = num(d["P4_2"])
    nan = np.nan

    def codifica(x, unos, ceros):
        y = pd.Series(nan, index=x.index)
        y[x.isin(unos)] = 1.0
        y[x.isin(ceros)] = 0.0
        return y

    ori = codifica(p81, [1, 2, 3, 6], [4, 5])
    ide = pd.Series(nan, index=d.index)
    ide[p91.isin([3, 4, 5])] = 1.0
    bin_ = p91.isin([1, 2]) & p71.isin([1, 2])
    ide[bin_ & (p91 != p71)] = 1.0
    ide[bin_ & (p91 == p71)] = 0.0
    lgbt = pd.Series(nan, index=d.index)
    lgbt[(ori == 0) & (ide == 0)] = 0.0
    lgbt[(ori == 1) | (ide == 1)] = 1.0
    y = {
        "orientacion-no-heterosexual": ori,
        "identidad-no-cisgenero": ide,
        "lgbt": lgbt,
        "variacion-intersexual": codifica(p71a, [1], [2]),
        "media-superior-o-mas": codifica(niv, list(range(6, 11)), list(range(0, 6))),
        "soltero": codifica(p42, [6], [1, 2, 3, 4, 5]),
        "union-libre": codifica(p42, [1], [2, 3, 4, 5, 6]),
        "casado": codifica(p42, [2], [1, 3, 4, 5, 6]),
    }
    return y


def causas_exclusion(d, conducta, y, mask):
    """Conteo de exclusiones (y indefinida) dentro del dominio, por causa."""
    fuera = mask & y[conducta].isna()
    if not fuera.any():
        return {}

    def vc(col, m):
        s = d.loc[m, col].str.strip().replace("", "<blanco>")
        return {f"{col}={k}": int(v) for k, v in s.value_counts().sort_index().items()}

    if conducta == "orientacion-no-heterosexual":
        return vc("P8_1", fuera)
    if conducta == "variacion-intersexual":
        return vc("P7_1A", fuera)
    if conducta == "media-superior-o-mas":
        return vc("NIV", fuera)
    if conducta in ("soltero", "union-libre", "casado"):
        return vc("P4_2", fuera)
    if conducta == "identidad-no-cisgenero":
        p91 = num(d["P9_1"])
        r = {}
        a = fuera & ~p91.isin([1, 2, 3, 4, 5])
        if a.any():
            r.update({"P9_1 " + k: v for k, v in vc("P9_1", a).items()})
        b = fuera & p91.isin([1, 2])
        if b.any():
            r.update({"P9_1 binario con " + k: v for k, v in vc("P7_1", b).items()})
        return r
    if conducta == "lgbt":
        ori, ide = y["orientacion-no-heterosexual"], y["identidad-no-cisgenero"]
        return {
            "orientacion_indefinida_e_identidad_CERO": int((fuera & ori.isna() & (ide == 0)).sum()),
            "identidad_indefinida_y_orientacion_CERO": int((fuera & ide.isna() & (ori == 0)).sum()),
            "ambas_indefinidas": int((fuera & ori.isna() & ide.isna()).sum()),
        }
    return {"indefinida": int(fuera.sum())}


def dominios(d, y):
    edad = num(d["P4_1"])
    niv = num(d["NIV"])
    p42 = num(d["P4_2"])
    p71 = num(d["P7_1"])
    p47 = num(d["P4_7"])
    p44 = num(d["P4_4"])
    ent = num(d["ENT"])
    lg = y["lgbt"]
    dom = {
        ("TOTAL", "TODOS"): pd.Series(True, index=d.index),
        ("SEXO", "AL-NACER-HOMBRE"): p71 == 1,
        ("SEXO", "AL-NACER-MUJER"): p71 == 2,
        ("EDAD", "15-19"): edad.between(15, 19),
        ("EDAD", "20-29"): edad.between(20, 29),
        ("EDAD", "30-44"): edad.between(30, 44),
        ("EDAD", "45-59"): edad.between(45, 59),
        ("EDAD", "60-MAS"): edad.between(60, 96),
        ("ESCOLARIDAD", "HASTA-PRIMARIA"): niv.between(0, 2),
        ("ESCOLARIDAD", "SECUNDARIA"): niv.between(3, 5),
        ("ESCOLARIDAD", "MEDIA-SUPERIOR"): niv.between(6, 7),
        ("ESCOLARIDAD", "SUPERIOR"): niv.between(8, 10),
        ("CONYUGAL", "UNIDO"): p42.isin([1, 2]),
        ("CONYUGAL", "ALGUNA-VEZ-UNIDO"): p42.isin([3, 4, 5]),
        ("CONYUGAL", "SOLTERO"): p42 == 6,
        ("INDIGENA", "AUTOADSCRITO-SI"): p47 == 1,
        ("INDIGENA", "AUTOADSCRITO-NO"): p47 == 2,
        ("AFRO", "AUTOADSCRITO-SI"): p44 == 1,
        ("AFRO", "AUTOADSCRITO-NO"): p44 == 2,
        ("LGBT", "SI"): lg == 1,
        ("LGBT", "NO"): lg == 0,
    }
    for e in range(1, 33):
        dom[("ENTIDAD", f"{e:02d}")] = ent == e
    return {k: v.fillna(False).astype(bool).to_numpy() for k, v in dom.items()}


def disenio(d):
    """Índices de UPM (estrato, UPM) y estructura por estrato, en orden lexicográfico."""
    est = d["EST_DIS"].str.strip()
    upm = d["UPM_DIS"].str.strip()
    claves = pd.DataFrame({"e": est, "u": upm}).drop_duplicates().sort_values(["e", "u"])
    claves = claves.reset_index(drop=True)
    idx_map = {(e, u): i for i, (e, u) in enumerate(zip(claves["e"], claves["u"]))}
    upm_idx = np.array([idx_map[(e, u)] for e, u in zip(est, upm)], dtype=np.int64)
    estratos = []
    for e, g in claves.groupby("e", sort=True):
        estratos.append((e, g.index.to_numpy()))
    return upm_idx, len(claves), estratos


def multiplicadores(n_upm, estratos):
    """Genera N_REP x n_upm multiplicadores de bootstrap, en bloques de BLOQUE."""
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    M = np.empty((N_REP, n_upm), dtype=np.float64)
    for b0 in range(0, N_REP, BLOQUE):
        for r in range(b0, b0 + BLOQUE):
            m = np.ones(n_upm)
            for _, ids in estratos:
                nh = ids.size
                if nh < 2:
                    continue  # UPM única del estrato = de certeza
                draw = rng.integers(0, nh, size=nh)
                m[ids] = np.bincount(draw, minlength=nh)
            M[r] = m
    return M


def main():
    d, diag_univ = carga()
    y = conductas(d)
    dom = dominios(d, y)
    w = num(d["FACTOR"]).to_numpy(dtype=np.float64)
    upm_idx, n_upm, estratos = disenio(d)
    n_cert = sum(1 for _, ids in estratos if ids.size < 2)
    diag_univ.update({"n_estratos": len(estratos), "n_upm": n_upm,
                      "n_estratos_upm_unica_certeza": n_cert})

    esq = pd.read_csv(ESQ, sep="\t", dtype=str, keep_default_na=False)
    specs = []
    for _, r in esq.iterrows():
        k = (r["eje"], r["segmento"])
        specs.append((r, k))

    # Agregados por UPM: numerador y denominador por llave.
    K = len(specs)
    NUM = np.zeros((n_upm, K))
    DEN = np.zeros((n_upm, K))
    info = []
    for j, (r, k) in enumerate(specs):
        yy = y[r["conducta"]].to_numpy()
        md = dom.get(k)
        if md is None or r["ola"] != "2021":
            info.append(None)
            continue
        val = md & ~np.isnan(yy)
        NUM[:, j] = np.bincount(upm_idx, weights=np.where(val, w * np.nan_to_num(yy), 0.0), minlength=n_upm)
        DEN[:, j] = np.bincount(upm_idx, weights=np.where(val, w, 0.0), minlength=n_upm)
        info.append({
            "n_dominio": int(md.sum()),
            "n_valido": int(val.sum()),
            "n_uno": int((val & (yy == 1)).sum()),
            "n_upm_con_validos": int(np.unique(upm_idx[val]).size),
            "exclusiones_por_causa": causas_exclusion(d, r["conducta"], y, pd.Series(md, index=d.index)),
        })

    M = multiplicadores(n_upm, estratos)
    RN = M @ NUM
    RD = M @ DEN

    filas, diag_llaves = [], []
    for j, (r, k) in enumerate(specs):
        fila = {"llave": r["llave"], "unidad": r["unidad"]}
        dg = {"llave": r["llave"], "conducta": r["conducta"], "eje": r["eje"], "segmento": r["segmento"]}
        if info[j] is None:
            fila.update({"estado": "NO-RECALCULABLE-DESDE-SPEC",
                         "motivo": f"eje/segmento/ola ({r['eje']}, {r['segmento']}, {r['ola']}) no definido en la spec humana"})
            filas.append(fila)
            diag_llaves.append(dg)
            continue
        dg.update(info[j])
        den = DEN[:, j].sum()
        if info[j]["n_valido"] == 0 or den <= 0:
            fila.update({"estado": "DENOMINADOR-CERO",
                         "motivo": "dominio sin observaciones válidas (Σw = 0) en el universo filtrado"})
            filas.append(fila)
            diag_llaves.append(dg)
            continue
        p = NUM[:, j].sum() / den
        fila.update({"estado": "RECONSTRUIDO", "punto": repr(float(p))})
        n_deg = int((RD[:, j] <= 0).sum())
        dg["replicas_degeneradas"] = n_deg
        if n_deg > 0:
            fila.update({"estado_ic": "NO-IDENTIFICADA",
                         "motivo_ic": f"{n_deg} de {N_REP} réplicas bootstrap con denominador cero en el dominio; "
                                      "contrato conservador de la spec: una réplica degenerada → sin EE ni IC"})
        else:
            reps = RN[:, j] / RD[:, j]
            lo, hi = np.percentile(reps, [2.5, 97.5])
            fila.update({"estado_ic": "CALCULADO", "ic95_inf": repr(float(lo)), "ic95_sup": repr(float(hi))})
            dg["ee_bootstrap"] = repr(float(np.std(reps, ddof=1)))
        filas.append(fila)
        diag_llaves.append(dg)

    resultado = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
        f.write("\n")

    diagnostico = {
        "identidad": IDENTIDAD,
        "universo": diag_univ,
        "bootstrap": {"generador": f"numpy PCG64({SEMILLA})", "replicas": N_REP, "bloque": BLOQUE,
                      "percentiles": [2.5, 97.5], "metodo_percentil": "numpy.percentile lineal (default)"},
        "decisiones": DECISIONES,
        "llaves": diag_llaves,
        "conteo_estados": pd.Series([f["estado"] + "/" + f.get("estado_ic", "-") for f in filas]).value_counts().to_dict(),
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diagnostico, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(diagnostico["universo"])
    print(diagnostico["conteo_estados"])


DECISIONES = [
    {"decision": "Unidad de remuestreo = par (EST_DIS, UPM_DIS); estratos y número de UPM por estrato se cuentan sobre el universo filtrado completo (no por dominio), y las mismas 2000 réplicas se usan para todas las llaves.",
     "frase": "Bootstrap de UPM `UPM_DIS` dentro de estrato `EST_DIS`. Válido: peso > 0, estrato y UPM no vacíos."},
    {"decision": "Bootstrap ingenuo con reemplazo: en cada estrato con n_h ≥ 2 se sortean n_h UPM (no n_h−1, sin reescalado Rao-Wu); el peso replicado es FACTOR × veces que la UPM fue sorteada.",
     "frase": "Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato"},
    {"decision": "Estrato con una sola UPM: la UPM entra en todas las réplicas con multiplicador 1 y no consume sorteos del generador.",
     "frase": "(UPM única del estrato = de certeza)"},
    {"decision": "Orden de sorteos: réplicas 0..1999 en 40 bloques consecutivos de 50; dentro de cada réplica, estratos en orden lexicográfico de EST_DIS y UPM en orden lexicográfico de UPM_DIS; un rng.integers(0, n_h, size=n_h) por estrato. Los bloques no alteran la secuencia.",
     "frase": "`PCG64(20260926)`, 2 000 réplicas, bloques de 50"},
    {"decision": "Réplica degenerada = réplica en la que el denominador Σw* del dominio (válidos de la conducta) es 0; si hay al menos una, la llave queda RECONSTRUIDO con estado_ic NO-IDENTIFICADA.",
     "frase": "contrato conservador (una réplica degenerada → sin EE ni IC)"},
    {"decision": "IC = percentiles 2.5 y 97.5 de las 2000 razones replicadas con numpy.percentile (interpolación lineal por defecto).",
     "frase": "percentiles 2.5/97.5"},
    {"decision": "Punto = razón con los pesos originales de la muestra completa (no media de réplicas).",
     "frase": "Razón ponderada Σw·y/Σw"},
    {"decision": "LGBT = UNO si al menos una de orientación/identidad es UNO aunque la otra sea indefinida; CERO sólo si ambas son CERO; en otro caso fuera. El eje LGBT usa esa misma derivada (SI=UNO, NO=CERO).",
     "frase": "LGBT | derivada: UNO si cualquiera de las dos anteriores es UNO; CERO si ambas son CERO"},
    {"decision": "IDENTIDAD-NO-CISGENERO con P9_1 ∈ {1,2} y P7_1 fuera de {1,2} queda fuera (no puede compararse); P9_1 ∈ {3,4,5} es UNO sin importar P7_1.",
     "frase": "`P9_1` ∈ {3,4,5}, o `P9_1` ∈ {1,2} distinto de `P7_1` | `P9_1` = `P7_1`"},
    {"decision": "El denominador de cada llave son las personas del dominio con la conducta en UNO/CERO; los códigos fuera (p.ej. P7_1A 3 y 9) se excluyen del numerador y del denominador.",
     "frase": "Todo otro código (no entiende, no especificado, blanco) queda fuera."},
    {"decision": "Personas con la variable del eje fuera de los códigos de segmento (p.ej. P4_7=9 No sabe) no pertenecen a ningún segmento de ese eje; EDAD 60-MAS = P4_1 60–96.",
     "frase": "INDIGENA-AUTOADSCRITO (`P4_7` ... 1/2) · EDAD (`P4_1`: 15–19, 20–29, 30–44, 45–59, 60+)"},
    {"decision": "Esquema: eje SEXO ≡ SEXO-AL-NACER (segmentos AL-NACER-HOMBRE=P7_1 1, AL-NACER-MUJER=2); INDIGENA/AFRO ≡ *-AUTOADSCRITO (AUTOADSCRITO-SI=1, -NO=2); ENTIDAD segmento NN = ENT NN.",
     "frase": "SEXO-AL-NACER (`P7_1`) · INDIGENA-AUTOADSCRITO · AFRO-AUTOADSCRITO (`P4_4` 1/2) · ENTIDAD (`ENT` 01–32)"},
    {"decision": "Códigos leídos como texto y convertidos a número tras strip (NIV '00'→0, ENT '01'→1).",
     "frase": "«4.11 ... - NIVEL» (`NIV` 00–10) | 06–10 | 00–05"},
    {"decision": "No se suprime ninguna celda por tamaño; se reporta n válido en diagnóstico.",
     "frase": "(encargo) No suprimas celdas por publicabilidad."},
]


if __name__ == "__main__":
    main()
