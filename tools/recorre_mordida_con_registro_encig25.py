#!/usr/bin/env python3
"""ACTO MAESTRA35-L1 · P1 · `tramite.mordida.con_registro` recorrida SIN deduplicar.

Ejecuta la spec CONGELADA en `forense/notas/2026-09-02-MAESTRA35-L1-spec.md`
(COMMIT-1), seccion §2. Firma de mesa `d1` = `FP-238`.

Que corrige. `MAESTRA34-L1` (`PR #451`) midio esta cifra deduplicando `sec_7`
por `ID_TRA` bajo la creencia -- escrita en `TRA-M-13` -- de que las filas
repetidas eran "duplicados EXACTOS". El censo `P0` de este acto conto que no
lo eran: son EVENTOS de tramite distintos del mismo tipo hechos por la misma
persona, distinguidos por `NT_TIPO`, y 501 `ID_TRA` repetidos traen `P7_3`
distinto entre sus filas. La deduplicacion borro 3 835 eventos del universo.

Que NO corrige. El encargo pedia unir por `(ID_TRA, NT_TIPO)`. No se puede:
`sec_8` no trae `NT_TIPO` y no puede traerlo -- es la rejilla persona x tipo
(40 136 x 27 = 1 083 672) donde `ID_TRA` **es** llave unica. El join por
`ID_TRA` es exacto y uno-a-muchos por construccion. La sustancia de `d1` queda
intacta: lo que se corrige es la deduplicacion, no la llave.

Unidad = TRAMITE. `FAC_TRA` expande tramites: quien hizo el mismo tramite tres
veces aporta tres eventos. Ponderador `FAC_TRA`, diseno `EST_DIS x UPM_DIS`,
bootstrap conglomerado n_boot=10000 seed=42 reutilizando
`wprop_ic_conglomerado` (no se reescribe el estimador).

Este script solo IMPRIME.

Uso: python3 tools/recorre_mordida_con_registro_encig25.py
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import (  # noqa: E402
    leer_csv_cr, wprop_ic_conglomerado)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP = os.path.join(RAW, "encig25_base_datos_csv.zip")
T7 = "encig2025_04_sec_7.csv"
T8 = "encig2025_05_sec_8.csv"

# Cifra SELLADA que este acto recorre (milpa/tramite.yaml:139-142 y
# milpa/tramite-ola5-propuesta-v0.yaml:tramite.mordida.con_registro_encig2025).
SELLADA_DIGITAL = 0.027358
SELLADA_PRESENCIAL = 0.116000
SELLADA_RAZON = SELLADA_PRESENCIAL / SELLADA_DIGITAL

# Los dos mapeos de canal, ambos pre-declarados en la spec §2.
MAPEOS = {
    "principal (MAESTRA34-L1: digital {3,4,5})": ({"3", "4", "5"}, {"1"}),
    "sensibilidad A (MAESTRA34-L5: digital {4,5}, 3 fuera)": ({"4", "5"}, {"1"}),
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lee(member):
    df = leer_csv_cr(ZIP, member, encoding="utf-8")
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    return df


def carga():
    """Une sec_7 x sec_8 por ID_TRA, SIN deduplicar. Las dos guardias de la
    spec §2 PARAN el script en vez de dejarlo producir una cifra."""
    s7, s8 = lee(T7), lee(T8)
    for tabla, df, cols in ((T7, s7, ["ID_TRA", "NT_TIPO", "P7_3", "FAC_TRA",
                                      "EST_DIS", "UPM_DIS"]),
                            (T8, s8, ["ID_TRA", "P8_4"])):
        faltan = [c for c in cols if c not in df.columns]
        if faltan:
            raise SystemExit(f"PARO · faltan columnas en {tabla}: {faltan}")

    # GUARDIA 1 (spec §2): ID_TRA tiene que ser llave unica de sec_8, o el
    # join deja de ser uno-a-muchos exacto y la cifra no significa nada.
    if s8["ID_TRA"].nunique() != len(s8):
        raise SystemExit(
            f"PARO · ID_TRA no es llave unica en {T8}: "
            f"{s8['ID_TRA'].nunique():,} distintos para {len(s8):,} filas.")

    # GUARDIA 2 (spec §2): ni un solo evento de sec_7 puede quedar huerfano.
    huerf = len(set(s7["ID_TRA"]) - set(s8["ID_TRA"]))
    if huerf:
        raise SystemExit(
            f"PARO · {huerf:,} ID_TRA de {T7} sin fila en {T8}.")

    s8v = s8[s8["P8_4"].isin(["0", "1"])]
    m = s7.merge(s8v[["ID_TRA", "P8_4"]], on="ID_TRA", how="inner")
    if len(m) < len(s8v):
        raise SystemExit(
            f"PARO · el join perdio filas: {len(m):,} < {len(s8v):,}.")
    return s7, s8, s8v, m


def estima(m, canal, etiqueta):
    sub = m[m["P7_3"].isin(canal)].copy()
    sub["d"] = (sub["P8_4"] == "1").astype(float)
    sub["w"] = sub["FAC_TRA"].astype(float)
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        sub["d"].to_numpy(), sub["w"].to_numpy(),
        sub["EST_DIS"].tolist(), sub["UPM_DIS"].tolist())
    return {"etiqueta": etiqueta, "p": p, "lo": lo, "hi": hi, "n": n,
            "n_num": int(sub["d"].sum()), "n_est": n_est, "n_upm": n_cl,
            "n_id_tra": sub["ID_TRA"].nunique(),
            "pobl": float(sub["w"].sum())}


def fmt(r):
    return (f"  {r['etiqueta']}\n"
            f"    p̂ = {r['p']:.6f}   IC95 = [{r['lo']:.6f}, {r['hi']:.6f}]\n"
            f"    n = {r['n']:,} EVENTOS de tramite "
            f"(en {r['n_id_tra']:,} ID_TRA) · con mordida = {r['n_num']:,}\n"
            f"    estratos = {r['n_est']} · UPM = {r['n_upm']:,} · "
            f"poblacion expandida = {r['pobl']:,.0f}")


def main():
    print("ACTO MAESTRA35-L1 · P1 · con_registro recorrida SIN deduplicar")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    s7, s8, s8v, m = carga()
    print(f"sec_7    : {len(s7):,} filas · ID_TRA distintos "
          f"{s7['ID_TRA'].nunique():,} · (ID_TRA,NT_TIPO) grupos "
          f"{s7.groupby(['ID_TRA','NT_TIPO']).ngroups:,}")
    print(f"sec_8    : {len(s8):,} filas · ID_TRA llave unica (guardia 1 OK)")
    print(f"universo : P8_4 in {{0,1}} = {len(s8v):,} filas de sec_8; "
          f"al grano de EVENTO -> {len(m):,} en {m['ID_TRA'].nunique():,} ID_TRA")
    print(f"           una deduplicacion por ID_TRA descartaria "
          f"{len(m) - m['ID_TRA'].nunique():,} eventos: no se deduplica.")
    print()
    resultados = {}
    for etiq, (dig, pres) in MAPEOS.items():
        print(f"MAPEO {etiq}")
        rd = estima(m, dig, f"DIGITAL/REGISTRADO · P7_3 in {sorted(dig)}")
        rp = estima(m, pres, f"PRESENCIAL · P7_3 in {sorted(pres)}")
        print(fmt(rd))
        print(fmt(rp))
        razon = rp["p"] / rd["p"]
        traslape = not (rd["hi"] < rp["lo"] or rp["hi"] < rd["lo"])
        print(f"    RAZON presencial/digital = {razon:.4f}x  "
              f"(signo: presencial {'MAYOR' if razon > 1 else 'MENOR'})")
        print(f"    IC95 se traslapan: {traslape}")
        resultados[etiq] = (rd, rp, razon)
        print()

    rd, rp, razon = resultados[list(MAPEOS)[0]]
    print("=" * 74)
    print("VEREDICTO CONGELADO EN LA SPEC §2.1 (mapeo principal)")
    dentro = rd["lo"] <= SELLADA_DIGITAL <= rd["hi"]
    print(f"  cifra sellada del canal digital : {SELLADA_DIGITAL}")
    print(f"  IC95 nuevo del canal digital    : "
          f"[{rd['lo']:.6f}, {rd['hi']:.6f}]")
    print(f"  el IC95 nuevo contiene la sellada: {dentro}")
    print(f"  -> {'CORRECCION SIN CAMBIO MATERIAL' if dentro else 'CIFRA SELLADA VENCIDA EN ALCANCE -- re-sello de mesa (FP-241)'}")
    print()
    print(f"  contra-hipotesis: razon sellada {SELLADA_RAZON:.4f}x, "
          f"razon nueva {razon:.4f}x")
    print(f"  -> {'ACOTADO: el hallazgo de MAESTRA34-L1 cae por debajo de 2x' if razon < 2 else 'el hallazgo de MAESTRA34-L1 NO queda acotado (razon >= 2x)'}")
    return resultados


if __name__ == "__main__":
    main()
