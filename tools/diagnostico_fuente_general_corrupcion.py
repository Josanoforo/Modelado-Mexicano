#!/usr/bin/env python3
"""Tabulaciones descriptivas de dos candidatos parciales para NC-0153.

No produce un estimando adoptable. Verifica la identidad de los payloads,
reconstruye la unidad trámite de ENEAC 2021 y tabula el reactivo general de
MCCI 2019--2024. Su propósito es impedir que una tasa estatal/empresarial o
una tasa por persona se confunda con el objeto nacional por evento y canal.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd


ENEAC_SHA = "7b66456fc5f4fa098a026cacc72d0bef84ebaea92f5a8b3b932a426871cb13d1"
MCCI_SHA = "ffa39bbb62e62a2dda0276f0120afbfeb37ad6c3c6b6e1f378a627642463372c"


def verifica(ruta: Path, esperado: str) -> None:
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != esperado:
        raise SystemExit(f"PARO: sha256 inesperado para {ruta}: {real}")


def eneac(ruta: Path) -> dict[str, object]:
    verifica(ruta, ENEAC_SHA)
    datos = pd.read_excel(ruta)
    familias = {
        prefijo: [c for c in datos.columns if c.startswith(prefijo)]
        for prefijo in ("TRAMITE", "p13.", "P16.", "P17.", "P18.")
    }
    if {k: len(v) for k, v in familias.items()} != {k: 21 for k in familias}:
        raise SystemExit("PARO: ENEAC dejó de contener 21 bloques de trámite")

    eventos: list[tuple[int | None, bool]] = []
    for i in range(21):
        for _, fila in datos.iterrows():
            if pd.isna(fila[familias["TRAMITE"][i]]):
                continue
            canal = fila[familias["p13."][i]]
            canal = int(canal) if pd.notna(canal) else None
            solicitud = any(
                fila[familias[p][i]] == 1 for p in ("P16.", "P17.", "P18.")
            )
            eventos.append((canal, solicitud))

    etiquetas = {
        1: "instalaciones_gobierno",
        2: "en_linea_internet_computadora",
        3: "personal_gobierno_en_negocio",
    }
    por_canal = {}
    for codigo, etiqueta in etiquetas.items():
        subconjunto = [y for c, y in eventos if c == codigo]
        por_canal[etiqueta] = {
            "denominador_eventos": len(subconjunto),
            "numerador_union_p16_p17_p18": sum(subconjunto),
            "proporcion_no_ponderada": sum(subconjunto) / len(subconjunto),
        }
    validos = [y for c, y in eventos if c in etiquetas]
    return {
        "alcance": "PARCIAL: Aguascalientes, microempresas SCIAN 46/72; no México nacional",
        "payload_sha256": ENEAC_SHA,
        "establecimientos": len(datos),
        "eventos_tramite_reportados": len(eventos),
        "eventos_canal_valido": len(validos),
        "eventos_canal_ns_nc": sum(c == 4 for c, _ in eventos),
        "ponderador_en_archivo": False,
        "por_canal": por_canal,
        "total_canal_valido": {
            "denominador_eventos": len(validos),
            "numerador_union_p16_p17_p18": sum(validos),
            "proporcion_no_ponderada": sum(validos) / len(validos),
        },
    }


def mcci(ruta: Path) -> dict[str, object]:
    verifica(ruta, MCCI_SHA)
    datos = pd.read_excel(ruta)
    requeridas = {"ano", "indice_ponderador", "mordida_encuestado"}
    if not requeridas.issubset(datos.columns):
        raise SystemExit("PARO: faltan columnas MCCI requeridas")
    salida = {}
    for ano, grupo in datos.groupby("ano", sort=True):
        validos = grupo[grupo["mordida_encuestado"].isin(["Sí", "No"])]
        pesos = validos["indice_ponderador"]
        si = validos["mordida_encuestado"].eq("Sí")
        salida[str(int(ano))] = {
            "denominador_personas_respuesta_valida": len(validos),
            "numerador_no_ponderado": int(si.sum()),
            "proporcion_ponderada": float(pesos[si].sum() / pesos.sum()),
        }
    return {
        "alcance": "PARCIAL: persona adulta, solicitud general; sin canal ni unidad evento",
        "payload_sha256": MCCI_SHA,
        "filas": len(datos),
        "por_ano": salida,
    }


def main() -> int:
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw/gen2_corrupcion_fuente_general")
    salida = {
        "etiqueta": "EXPLORATORIO-NO-ADOPTAR",
        "eneac_2021": eneac(raiz / "eneac2021-tramites-codigos.xlsx"),
        "mcci_2019_2024": mcci(raiz / "Encuesta-MCCI_2019-2024.xlsx"),
    }
    print(json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
