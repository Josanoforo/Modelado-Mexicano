#!/usr/bin/env python3
"""Diagnóstico exploratorio de la unidad de canal en ENCIG 2025.

No produce un estimando adoptable ni modifica datos. Cuantifica el conflicto
entre la unidad de ``P8_4`` (``ID_TRA``) y la de ``P7_3``
(``ID_TRA, NT_TIPO``), y calcula una envolvente descriptiva que no desempata
los grupos con canales presencial/digital mezclados.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ESPERADO = "47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12"
S7 = "encig2025_04_sec_7.csv"
S8 = "encig2025_05_sec_8.csv"


def codigo(valor: str | None) -> int | None:
    try:
        return int((valor or "").strip())
    except ValueError:
        return None


def peso(valor: str | None) -> float:
    return float((valor or "").strip().replace(",", ""))


def clase(c: int | None) -> str:
    if c == 1:
        return "P"
    if c in {3, 4, 5}:
        return "D"
    if c in {2, 6}:
        return "R"
    return "X"


def filas(zf: zipfile.ZipFile, nombre: str):
    with zf.open(nombre) as bruto:
        texto = io.TextIOWrapper(bruto, encoding="latin-1", newline="")
        lector = csv.DictReader(texto)
        lector.fieldnames = [
            c.lstrip("\ufeff").lstrip("ï»¿").strip().upper()
            for c in (lector.fieldnames or [])
        ]
        yield from lector


def tasa(numerador: float, denominador: float) -> float:
    return numerador / denominador


def main() -> int:
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw/encig25_base_datos_csv.zip")
    huella = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if huella != ESPERADO:
        raise SystemExit(f"PARO: sha256 inesperado: {huella}")

    with zipfile.ZipFile(ruta) as zf:
        s7 = list(filas(zf, S7))
        s8_filas = list(filas(zf, S8))
    s8 = {r["ID_TRA"].strip(): r for r in s8_filas}
    if len(s8) != len(s8_filas):
        raise SystemExit("PARO: ID_TRA dejó de ser único en sec_8")

    grupos: dict[str, list[dict[str, str]]] = defaultdict(list)
    pares = set()
    for r in s7:
        llave = r["ID_TRA"].strip()
        par = (llave, r["NT_TIPO"].strip())
        if par in pares:
            raise SystemExit("PARO: (ID_TRA, NT_TIPO) dejó de ser único en sec_7")
        pares.add(par)
        grupos[llave].append(r)

    repetidos = {k: v for k, v in grupos.items() if len(v) > 1}
    discordantes = {
        k: v for k, v in repetidos.items()
        if len({codigo(r["P7_3"]) for r in v}) > 1
    }
    contenido_igual = {
        k: v for k, v in repetidos.items()
        if len({(r["P7_3"], r["FAC_TRA"], r["EST_DIS"], r["UPM_DIS"],
                 r["N_TRA"], r["ID_PER"]) for r in v}) == 1
    }

    observados = {
        k: v for k, v in grupos.items()
        if k in s8 and codigo(s8[k]["P8_4"]) in {0, 1}
    }
    c_n: Counter[str] = Counter()
    c_w: Counter[str] = Counter()
    c_pos: Counter[str] = Counter()
    for k, grupo in observados.items():
        pesos = {peso(r["FAC_TRA"]) for r in grupo}
        if len(pesos) != 1:
            raise SystemExit(f"PARO: FAC_TRA cambia dentro de ID_TRA={k}")
        clases = sorted({clase(codigo(r["P7_3"])) for r in grupo})
        etiqueta = "+".join(clases)
        w = pesos.pop()
        y = codigo(s8[k]["P8_4"])
        c_n[etiqueta] += 1
        c_w[etiqueta] += w
        c_pos[etiqueta] += w * y

    # Envolvente: si se obliga a asignar cada ID_TRA P+D a una sola de sus
    # clases observadas, asignar negativos/positivos por separado produce los
    # extremos marginales. No afirma cuál asignación es verdadera.
    amb_den = c_w["D+P"]
    amb_pos = c_pos["D+P"]
    amb_neg = amb_den - amb_pos
    sensibilidad = {}
    for etiqueta in ("P", "D"):
        den, num = c_w[etiqueta], c_pos[etiqueta]
        sensibilidad[etiqueta] = {
            "p_consistentes": tasa(num, den),
            "limite_inferior_asignando_ambiguos_negativos": tasa(num, den + amb_neg),
            "limite_superior_asignando_ambiguos_positivos": tasa(num + amb_pos, den + amb_pos),
            "n_id_tra_consistentes": c_n[etiqueta],
            "masa_consistente": den,
        }

    total_obs_w = sum(c_w.values())
    pd_w = c_w["P"] + c_w["D"] + c_w["D+P"]
    salida = {
        "etiqueta": "EXPLORATORIO-NO-ADOPTAR",
        "payload_sha256": huella,
        "sec_7": {
            "filas_evento": len(s7),
            "id_tra": len(grupos),
            "id_tra_repetidos": len(repetidos),
            "distribucion_eventos_por_id_tra": dict(sorted(Counter(map(len, grupos.values())).items())),
            "id_tra_repetidos_con_contenido_igual_salvo_nt_tipo": len(contenido_igual),
            "id_tra_repetidos_con_p7_3_discordante": len(discordantes),
        },
        "p8_4_observado": {
            "id_tra": len(observados),
            "filas_evento": sum(map(len, observados.values())),
            "id_tra_p7_3_discordante": sum(
                len({codigo(r["P7_3"]) for r in v}) > 1 for v in observados.values()
            ),
            "id_tra_clase_discordante": sum(
                len({clase(codigo(r["P7_3"])) for r in v}) > 1 for v in observados.values()
            ),
            "masa_clase_discordante": sum(
                c_w[k] for k in c_w if "+" in k
            ),
            "fraccion_masa_clase_discordante": sum(
                c_w[k] for k in c_w if "+" in k
            ) / total_obs_w,
            "por_clase": {
                k: {"n_id_tra": c_n[k], "masa": c_w[k], "masa_positiva": c_pos[k]}
                for k in sorted(c_n)
            },
        },
        "foco_presencial_digital": {
            "id_tra_ambiguos_p_d": c_n["D+P"],
            "masa_ambigua_p_d": amb_den,
            "fraccion_masa_ambigua_en_foco_p_d": amb_den / pd_w,
            "sensibilidad_asignacion_forzada": sensibilidad,
        },
    }
    print(json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
