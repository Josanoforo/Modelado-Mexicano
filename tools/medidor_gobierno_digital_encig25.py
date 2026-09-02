#!/usr/bin/env python3
"""ACTO MAESTRA34-L5 · P1 · adopción de canal digital de gobierno, ENCIG 2025.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA34-L5-P1-spec.md` (COMMIT-1). Este script es el
COMMIT-2 de la pieza: no altera la spec, la ejecuta.

Regla `tramite.gobierno_digital.util_sin_coercion` (milpa/tramite.yaml:177-201,
clase ASIGNADO, `adopta p=0.71`, probabilidades declaradas NO CALIBRADAS por la
propia regla).

Unidad de análisis = TRÁMITE. Universo principal = `N_TRA=='01'` (pago ordinario
del servicio de luz), elegido por los tres criterios declarados en la spec §1.3.
`adopta = P7_3 in {4,5}`; no adopta = `{1,2,6}`; fuera `{3,7,8,9,blanco}`.
Llave `(ID_TRA, NT_TIPO)`, verificada única, SIN deduplicar (enmienda 1 de la
spec, §3): `ID_TRA` no es la llave y en `sec_7` no hay un solo duplicado exacto.
Ponderador `FAC_TRA`, diseño `EST_DIS × UPM_DIS`, bootstrap conglomerado
n_boot=10000 seed=42 reutilizando `wprop_ic_conglomerado` de
`tools/calibracion_mordida_encig_serie.py` (no se reescribe el estimador).
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
TABLA = "encig2025_04_sec_7.csv"

ADOPTA = {"4", "5"}          # Internet/app · cajero o kiosco inteligente
NO_ADOPTA = {"1", "2", "6"}  # instalaciones · banco/tienda · módulos móviles
TELEFONO = "3"               # fuera del universo (canal remoto atendido)

UNIVERSO_PRINCIPAL = {"01"}          # pago ordinario del servicio de luz
UNIVERSO_SENS_A = {"01", "10"}       # + registro civil (sensibilidad A)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga():
    """Lee sec_7 y verifica que (ID_TRA, NT_TIPO) sea llave única (spec §3.2,
    enmienda 1). NO deduplica: cada fila es un evento de trámite distinto y
    FAC_TRA expande trámites. Si la llave no fuera única: PARA."""
    df = leer_csv_cr(ZIP, TABLA, encoding="utf-8")
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    cols = ["ID_TRA", "NT_TIPO", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"]
    faltan = [c for c in cols if c not in df.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas en {TABLA}: {faltan}")

    n_filas = len(df)
    n_llaves = df.groupby(["ID_TRA", "NT_TIPO"]).ngroups
    if n_llaves != n_filas:
        raise SystemExit(
            f"PARO · (ID_TRA, NT_TIPO) no es llave única: {n_llaves:,} grupos "
            f"para {n_filas:,} filas (spec §3.2 exige parar).")
    n_id_tra = df["ID_TRA"].nunique()
    return df, n_filas, n_llaves, n_id_tra


def estima(df, universo, telefono_como_no_adopta, etiqueta):
    sub = df[df["N_TRA"].isin(universo)].copy()
    n_universo_tipo = len(sub)
    validos = set(ADOPTA) | set(NO_ADOPTA)
    if telefono_como_no_adopta:
        validos = validos | {TELEFONO}
    sub = sub[sub["P7_3"].isin(validos)].copy()
    sub["d"] = sub["P7_3"].isin(ADOPTA).astype(float)
    sub["w"] = sub["FAC_TRA"].astype(float)
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        sub["d"].to_numpy(), sub["w"].to_numpy(),
        sub["EST_DIS"].tolist(), sub["UPM_DIS"].tolist())
    return {
        "etiqueta": etiqueta, "p": p, "lo": lo, "hi": hi, "n": n,
        "n_tipo": n_universo_tipo, "n_estratos": n_est, "n_upm": n_cl,
        "n_adopta": int(sub["d"].sum()),
        "pobl": float(sub["w"].sum()),
    }


def fmt(r):
    return (f"  {r['etiqueta']}\n"
            f"    p̂ = {r['p']:.6f}   IC95 = [{r['lo']:.6f}, {r['hi']:.6f}]\n"
            f"    n = {r['n']:,} trámites en el universo "
            f"(de {r['n_tipo']:,} del tipo) · "
            f"adoptan = {r['n_adopta']:,}\n"
            f"    estratos = {r['n_estratos']} · UPM = {r['n_upm']:,} · "
            f"población expandida = {r['pobl']:,.0f}")


def main():
    print("ACTO MAESTRA34-L5 · P1 · util_sin_coercion · ENCIG 2025")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df, n_filas, n_llaves, n_id_tra = carga()
    print(f"tabla    : {TABLA} · {n_filas:,} filas · "
          f"llave (ID_TRA,NT_TIPO) única = {n_llaves:,} grupos · "
          f"ID_TRA distintos = {n_id_tra:,} · sin deduplicar (enmienda 1)")
    print()
    print("PRINCIPAL")
    r = estima(df, UNIVERSO_PRINCIPAL, False, "N_TRA=01 (pago de luz) · P7_3∈{4,5} vs {1,2,6}")
    print(fmt(r))
    print()
    print("SENSIBILIDADES PRE-DECLARADAS (spec §1.3 y §1.4)")
    ra = estima(df, UNIVERSO_SENS_A, False,
                "A · N_TRA∈{01,10} (+ registro civil)")
    print(fmt(ra))
    rb = estima(df, UNIVERSO_PRINCIPAL, True,
                "B · N_TRA=01, teléfono (P7_3=3) contado como NO adopción")
    print(fmt(rb))
    print()
    print(f"prior ASIGNADO a contrastar: adopta = 0.71 "
          f"(no calibrado por declaración de la propia regla)")
    print(f"razón p̂/prior = {r['p'] / 0.71:.4f}")
    return r


if __name__ == "__main__":
    main()
