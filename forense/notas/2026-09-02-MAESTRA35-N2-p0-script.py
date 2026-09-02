#!/usr/bin/env python3
"""Script temporal de P0 (MAESTRA35-N2) -- linea base ANTES de tocar F-DD.

Re-deriva, con el emisor TAL COMO ESTA (sin editar tools/emite_m.py), las 13
celdas del sorteado v1_2 que ya tienen M mas M-TRA-M-01/02 (regresion() ya
definida en el modulo), y compara campo por campo contra el JSON comiteado
real (nombre de archivo real, con o sin sufijo __v1_2). No escribe nada.
Vive en forense/notas/ (mencionado en la nota de cierre P0), no en tools/.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tools.emite_m as em  # noqa: E402

CORRIDAS_M = em.CORRIDAS_M
RUTA_MARCO_V1_2 = em.DUELO / "marco-M-sorteado-v1_2.tsv"

CELDAS_ARCHIVO = {
    "CIV-M-01": "M-CIV-M-01.json",
    "CIV-M-02": "M-CIV-M-02__v1_2.json",
    "CIV-M-04": "M-CIV-M-04__v1_2.json",
    "CIV-M-10": "M-CIV-M-10__v1_2.json",
    "CIV-M-12": "M-CIV-M-12.json",
    "CIV-M-13": "M-CIV-M-13.json",
    "FAM-M-01": "M-FAM-M-01.json",
    "FAM-M-05": "M-FAM-M-05__v1_2.json",
    "FAM-M-06": "M-FAM-M-06__v1_2.json",
    "FAM-M-07": "M-FAM-M-07__v1_2.json",
    "TRA-M-02": "M-TRA-M-02.json",
    "TRA-M-03": "M-TRA-M-03.json",
    "TRA-M-07": "M-TRA-M-07.json",
}


def compara(id_celda: str, regenerado: dict, original: dict) -> str:
    """Devuelve OK / diverge-en-campo-exento / DRIFT:<detalle>."""
    drift = []
    exento = []
    for campo in sorted(set(regenerado) | set(original)):
        if campo not in original or campo not in regenerado:
            drift.append(f"{campo} (ausente en uno de los dos -- esquema)")
            continue
        if regenerado[campo] == original[campo]:
            continue
        if campo in ("fuente", "correcciones_aplicadas_por_referencia"):
            exento.append(campo)
            continue
        drift.append(f"{campo}: original={original[campo]!r} regenerado={regenerado[campo]!r}")
    if drift:
        return "DRIFT:" + " | ".join(drift)
    if exento:
        return "OK (diverge solo en campo(s) exento(s): " + ", ".join(exento) + ")"
    return "OK (identico)"


def main() -> int:
    reglas_por_id = {r.id: r for r in em.cargar_reglas()}
    lineas_tramite = em.RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()
    candidatos = em.leer_por_id(em.RUTA_CANDIDATOS_V1_1)
    filas_v1_2 = em.leer_por_id(RUTA_MARCO_V1_2)

    resultados = []

    print("=== P0 -- 13 celdas del sorteado v1_2 ===")
    for id_celda, nombre_archivo in CELDAS_ARCHIVO.items():
        fila = filas_v1_2[id_celda]
        original = json.loads((CORRIDAS_M / nombre_archivo).read_text(encoding="utf-8"))
        try:
            regenerado = em.emite_celda(
                fila, reglas_por_id, lineas_tramite, candidatos,
                fuente_acto="P0-linea-base (MAESTRA35-N2)",
                marco_nombre="marco-M-sorteado-v1_2.tsv",
            )
            veredicto = compara(id_celda, regenerado, original)
        except Exception as e:  # noqa: BLE001
            veredicto = f"EXCEPCION: {type(e).__name__}: {e}"
        print(f"{id_celda} [{nombre_archivo}] -> {veredicto}")
        resultados.append((id_celda, veredicto))

    print("\n=== P0 -- regresion() (M-TRA-M-01/02) tal como el modulo la define ===")
    ok = em.regresion()
    print(f"regresion() devolvio: {ok}")

    print("\n=== RESUMEN ===")
    n_ok = sum(1 for _, v in resultados if v.startswith("OK"))
    n_drift = sum(1 for _, v in resultados if v.startswith("DRIFT") or v.startswith("EXCEPCION"))
    print(f"celdas OK (identico o solo campo exento): {n_ok}/13")
    print(f"celdas con DRIFT/EXCEPCION real: {n_drift}/13")
    print(f"regresion() (M-TRA-M-01/02): {'PASA' if ok else 'FALLA'}")
    for id_celda, v in resultados:
        if v.startswith("DRIFT") or v.startswith("EXCEPCION"):
            print(f"  DRIFT -> {id_celda}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
