#!/usr/bin/env python3
"""ACTO MAESTRA35-L6 · P2 · respaldo personal x adopción de producto formal, ENIF 2024.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L6-spec.md` §2 (COMMIT-1).

QUÉ MIDE, Y QUÉ NO. El bullet del motor (`canon/modelo-decision-v4_0.md:501`,
ids `dinero.ahorro.informal_sin_puente` + `con_puente_y_respaldo`) tiene DOS
condiciones: un **canal personal** por el que llega el producto, y un
**respaldo**. El censo P0 §6.2 estableció que el CANAL sólo se observa entre
quienes ya adoptaron (`P5_15_2` está gateado en tener el producto Y haber
comparado), así que la mitad de canal es inobservable y NO se mide aquí.

El RESPALDO sí: `P4_9_4` se le pregunta a las 13 502 personas del universo, sin
gate.

CORRECCIÓN HACIA ADELANTE (COMMIT-3): `D1` usaba el mismo operador que `D2`/`D3`
y salía degenerada (`p=1` por construcción). `P5_6_*` es subpregunta de `P5_4_*`
y codifica su "no" en blanco. `D1'` cuenta el blanco como cero. Dos guardias
nuevas PARAN si un desenlace no cubre el universo o si `p` satura. Esto mide la asociación entre respaldo declarado disponible y tenencia de
producto formal. Es ASOCIACIÓN dentro de una corrida (A-bis 1/2), no efecto, y
mide UNA de las dos condiciones del bullet: acota la regla, no la cierra.

Ponderador `FAC_PER`, diseño `EST_DIS × UPM_DIS`, bootstrap conglomerado
n_boot=10000 seed=42.
"""
import hashlib
import io
import json
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP = os.path.join(RAW, "enif_2024_bd_csv.zip")
TABLA = "TMODULO.csv"

EJE = "P4_9_4"          # respaldo: prestamo de familiares o amistades
CONTROL_RIQUEZA = "P4_9_1"   # sensibilidad C: podria con sus propios ahorros
FORMAL = [f"P5_6_{i}" for i in range(1, 10)]    # D1' PRINCIPAL: ahorro formal
CUENTA = [f"P5_4_{i}" for i in range(1, 10)]    # D2
CREDITO = [f"P6_2_{i}" for i in range(1, 10)]   # D3
DISENO = ["FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V"]

DESENLACES = [("D1_ahorro_formal", FORMAL, "PRINCIPAL"),
              ("D2_tenencia_cuenta", CUENTA, "secundario"),
              ("D3_credito_formal", CREDITO, "secundario")]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def paro(msg):
    raise SystemExit(f"PARO · {msg}")


def carga():
    with zipfile.ZipFile(ZIP) as z, z.open(TABLA) as f:
        df = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1",
                         dtype=str, low_memory=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    necesarias = [EJE, CONTROL_RIQUEZA] + FORMAL + CUENTA + CREDITO + DISENO
    faltan = [c for c in necesarias if c not in df.columns]
    if faltan:
        paro(f"faltan columnas en {TABLA}: {faltan}")
    for c in necesarias:
        df[c] = df[c].astype(str).str.strip().str.strip('"')

    edad = pd.to_numeric(df["EDAD_V"], errors="coerce")
    if edad.isna().any() or (edad < 18).any():
        paro("EDAD_V inválida o menor de 18 -- el universo declarado es 18+")
    w = pd.to_numeric(df["FAC_PER"], errors="coerce")
    if w.isna().any() or (w <= 0).any():
        paro("FAC_PER no numérico positivo")
    return df


def indicador(df, cols, blanco_es_cero=False):
    """1 si alguna vale '1'; 0 si todas valen '2'; None si hay otra cosa.

    `blanco_es_cero=True` (spec COMMIT-3 §2, sólo para D1'): el 0 es
    "cualquier otro caso", blanco incluido. `P5_6_*` es subpregunta de
    `P5_4_*` y codifica su "no" en blanco, no como '2'; no tener la cuenta
    implica no tener ahorro formal en esa institución.
    """
    es_uno = (df[cols] == "1").any(axis=1)
    if blanco_es_cero:
        return pd.Series(es_uno.astype(float), index=df.index)
    todas_dos = (df[cols] == "2").all(axis=1)
    val = pd.Series([None] * len(df), dtype="object", index=df.index)
    val[todas_dos] = 0.0
    val[es_uno] = 1.0
    return val


def celda(sub, y, etiqueta):
    ok = y.notna()
    sub = sub[ok]
    d = y[ok].astype(float).to_numpy()
    if len(d) == 0:
        paro(f"{etiqueta}: universo vacío")
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d, pd.to_numeric(sub["FAC_PER"]).to_numpy(),
        sub["EST_DIS"].tolist(), sub["UPM_DIS"].tolist())
    if p in (0.0, 1.0):   # guardia 2 de COMMIT-3 §3
        paro(f"{etiqueta}: p degenerada ({p}) sobre n={n}. Una proporcion que "
             f"satura no es una medicion: es una definicion mal puesta.")
    return {"celda": etiqueta, "p": p, "ic95": [lo, hi], "n": n,
            "numerador": int(d.sum()), "estratos": n_est, "upm": n_cl}


def sin_traslape(a, b):
    return a["ic95"][1] < b["ic95"][0] or b["ic95"][1] < a["ic95"][0]


def veredicto(con, sin_):
    """B-bis §2: la regla predice adopción MAYOR con respaldo."""
    if not sin_traslape(con, sin_):
        return "NO-DISCRIMINA"
    return "CORROBORADA" if con["p"] > sin_["p"] else "CONTRARIA"


def main():
    df = carga()
    salida = {"acto": "MAESTRA35-L6", "pieza": "P2",
              "spec": ("forense/notas/2026-09-02-MAESTRA35-L6-spec.md §2, con D1 reemplazada por D1' en forense/notas/2026-09-02-MAESTRA35-L6-spec-3.md §2"),
              "payload": os.path.relpath(ZIP, RAIZ), "tabla": TABLA,
              "sha256_payload": sha256(ZIP),
              "estimador": "wprop_ic_conglomerado (n_boot=10000, seed=42)",
              "eje": (f"{EJE} -- 4.9 ... ¿podria aprovecharla con el prestamo "
                      f"de familiares o amistades? (universo COMPLETO, sin gate)"),
              "escala": "proporcion ponderada de personas de 18+ por celda del eje",
              "limite": ("ASOCIACION dentro de una corrida (A-bis 1/2), no efecto. "
                         "Mide UNA de las dos condiciones del bullet (respaldo); "
                         "el canal personal es inobservable (censo P0 §6.2)."),
              "n_universo": int(len(df)),
              "desenlaces": [], "sensibilidad_C_control_riqueza": []}

    con_r = df[df[EJE] == "1"]
    sin_r = df[df[EJE] == "2"]
    fuera = len(df) - len(con_r) - len(sin_r)
    salida["eje_reparto"] = {"respaldo_si": int(len(con_r)),
                             "respaldo_no": int(len(sin_r)),
                             "fuera_de_eje": int(fuera)}

    for nombre, cols, papel in DESENLACES:
        y = indicador(df, cols, blanco_es_cero=(nombre == "D1_ahorro_formal"))
        # guardia 1 de COMMIT-3 §3 -- los tres desenlaces se declaran sobre el
        # universo completo; si no lo cubren, la definicion esta mal puesta.
        cobertura = int(y.notna().sum())
        if cobertura != len(df):
            paro(f"{nombre}: desenlace definido en {cobertura} filas de "
                 f"{len(df)} declaradas. La spec lo declara universal.")
        a = celda(con_r, y.loc[con_r.index], f"{nombre} | respaldo=SI")
        b = celda(sin_r, y.loc[sin_r.index], f"{nombre} | respaldo=NO")
        v = veredicto(a, b)
        salida["desenlaces"].append(
            {"desenlace": nombre, "papel": papel, "variables": cols,
             "con_respaldo": a, "sin_respaldo": b,
             "brecha_pp": (a["p"] - b["p"]) * 100.0,
             "ic95_sin_traslape": sin_traslape(a, b),
             "veredicto_Bbis": v})
        print(f"[{nombre}] respaldo=SI p={a['p']:.6f} {a['ic95']} n={a['n']} | "
              f"respaldo=NO p={b['p']:.6f} {b['ic95']} n={b['n']} -> {v}",
              flush=True)

    # Sensibilidad C: el mismo contraste de D1 DENTRO de cada estrato de P4_9_1
    y1 = indicador(df, FORMAL, blanco_es_cero=True)
    for val, etiq in (("1", "podria_con_sus_ahorros=SI"),
                      ("2", "podria_con_sus_ahorros=NO")):
        est = df[df[CONTROL_RIQUEZA] == val]
        a = celda(est[est[EJE] == "1"], y1.loc[est[est[EJE] == "1"].index],
                  f"D1 | {etiq} | respaldo=SI")
        b = celda(est[est[EJE] == "2"], y1.loc[est[est[EJE] == "2"].index],
                  f"D1 | {etiq} | respaldo=NO")
        salida["sensibilidad_C_control_riqueza"].append(
            {"estrato": etiq, "con_respaldo": a, "sin_respaldo": b,
             "brecha_pp": (a["p"] - b["p"]) * 100.0,
             "ic95_sin_traslape": sin_traslape(a, b),
             "veredicto_Bbis": veredicto(a, b)})
        print(f"[C · {etiq}] SI p={a['p']:.6f} n={a['n']} | "
              f"NO p={b['p']:.6f} n={b['n']} -> "
              f"{veredicto(a, b)}", flush=True)

    # Veredicto del acto, derivado por codigo y no a ojo (spec §2):
    # precedencia CONTRARIA; ACOTADA si D1 sostiene el signo y los
    # secundarios no lo sostienen.
    d1 = next(d for d in salida["desenlaces"] if d["papel"] == "PRINCIPAL")
    secundarios = [d["veredicto_Bbis"] for d in salida["desenlaces"]
                   if d["papel"] != "PRINCIPAL"]
    if d1["veredicto_Bbis"] == "CONTRARIA":
        final = "CONTRARIA"
    elif (d1["veredicto_Bbis"] == "CORROBORADA"
          and any(v != "CORROBORADA" for v in secundarios)):
        final = "ACOTADA"
    else:
        final = d1["veredicto_Bbis"]
    salida["veredicto_del_acto"] = final
    salida["veredicto_D1"] = d1["veredicto_Bbis"]
    salida["veredicto_secundarios"] = secundarios

    destino = os.path.join(RAIZ, "data", "l6-respaldo-enif2024-v1_0.json")
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\nveredicto del acto (D1, precedencia CONTRARIA): "
          f"{salida['veredicto_del_acto']}")
    print(f"escrito: {os.path.relpath(destino, RAIZ)}")


if __name__ == "__main__":
    main()
