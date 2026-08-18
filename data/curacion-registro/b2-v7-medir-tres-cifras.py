#!/usr/bin/env python3
"""Procedimiento congelado de las tres cifras del bloque 2 de BARRIDO-2, generación v7.

Este archivo se commitea ANTES de producir un solo resultado. La especificación que
lo gobierna está en `b2-v7-especificacion-tres-cifras.md`, mismo commit. El primer
resultado que produzca este procedimiento es el que se reporta.

Vive bajo `data/curacion-registro/` y no bajo `tools/` por perímetro: el encargo de
ACTO B2-V7 abre `tools/` únicamente para su §1 (el driver de olas). Ponerlo aquí lo
deja en el árbol —que es lo que A.3 exige de un artefacto que produce una cifra
reportada— sin salirse del perímetro autorizado.

Una sola pasada por los 672 expedientes de `.barrido2/staging-v7/*/e2-neutral-index.jsonl`.
No abre microdatos, no escribe nada, no usa red: solo lee el índice E2 ya producido.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/pc0/Modelado-Mexicano-barrido2")
STAGING = REPO / ".barrido2/staging-v7"
REDACCION = "[REDACTADO-PRIVACIDAD]"

# Cifra 1 · el universo se selecciona por SUFIJO de `objeto_tipo`, no por `format`.
# Razón medida: `format` es el formato del CONTENEDOR, no del objeto. Un .sav dentro
# de un .zip lleva format=".zip", así que seleccionar por format perdería la mayoría
# de los value labels de SAV (9 204 registros con value_labels llevan format=".zip").
SUFIJO_SAV = "-SAV"
SUFIJO_DTA = "-DTA"


def conservada(entrada: str) -> bool:
    """Una entrada de value_labels está CONSERVADA si sobrevivió entera a la redacción."""
    return REDACCION not in entrada


def clave_documento_pdf(registro: dict) -> tuple[str, str]:
    """Unidad de conteo de la cifra 3: el DOCUMENTO PDF, no la página ni el archivo.

    Un PDF suelto cuelga de la representación (`localizador='pagina=12'`); un PDF
    dentro de un ZIP cuelga de su miembro (`localizador='zip!/miembro=4:x.pdf!/pagina=12'`).
    La clave es (representacion_id, prefijo del localizador antes de `pagina=`), que
    identifica el mismo documento en los dos casos sin privilegiar ninguno.
    """
    loc = str(registro.get("localizador", ""))
    corte = loc.rfind("pagina=")
    prefijo = loc[:corte] if corte >= 0 else loc
    return (str(registro.get("representacion_id", "")), prefijo)


def main() -> int:
    # --- Cifra 1 -----------------------------------------------------------------
    vl_total = {"SAV": 0, "DTA": 0}
    vl_conservadas = {"SAV": 0, "DTA": 0}
    vl_registros = {"SAV": 0, "DTA": 0}

    # --- Cifra 2 -----------------------------------------------------------------
    zip_miembros = 0
    zip_enteros = 0            # las cuatro claves presentes y sin redacción
    zip_con_zip_slip = 0       # solo la declaración zip_slip, que es la que el control nombra
    zip_slip_reparto: defaultdict[str, int] = defaultdict(int)

    # --- Cifra 3 -----------------------------------------------------------------
    pdf_docs: dict[tuple[str, str], dict[str, bool]] = {}

    # --- Estampa -----------------------------------------------------------------
    registros = 0
    expedientes = 0

    for resumen in sorted(STAGING.rglob("resumen.json")):
        indice = resumen.parent / "e2-neutral-index.jsonl"
        if not indice.is_file():
            continue
        expedientes += 1
        with indice.open(encoding="utf-8") as fh:
            for linea in fh:
                linea = linea.strip()
                if not linea:
                    continue
                r = json.loads(linea)
                registros += 1
                tipo = str(r.get("objeto_tipo", ""))

                etiquetas = r.get("value_labels") or []
                if etiquetas:
                    familia = "SAV" if tipo.endswith(SUFIJO_SAV) else (
                        "DTA" if tipo.endswith(SUFIJO_DTA) else None)
                    if familia:
                        vl_registros[familia] += 1
                        for entrada in etiquetas:
                            vl_total[familia] += 1
                            if conservada(str(entrada)):
                                vl_conservadas[familia] += 1

                if tipo == "MIEMBRO-ZIP":
                    zip_miembros += 1
                    d = str(r.get("definicion", ""))
                    if "zip_slip=" in d:
                        zip_con_zip_slip += 1
                        valor = d.split("zip_slip=", 1)[1].split(";", 1)[0]
                        zip_slip_reparto[valor] += 1
                    claves = ("bytes=", "comprimidos=", "crc=", "zip_slip=")
                    if REDACCION not in d and all(c in d for c in claves):
                        zip_enteros += 1

                if tipo == "PAGINA-PDF":
                    d = str(r.get("definicion", ""))
                    clave = clave_documento_pdf(r)
                    est = pdf_docs.setdefault(clave, {"cifrado": False, "abrio": False})
                    if "cifrado=SI-EXTRAIBLE" in d:
                        est["cifrado"] = True
                    if "texto_extraible=SI" in d:
                        est["abrio"] = True

    pdf_total = len(pdf_docs)
    pdf_cifrados = [k for k, v in pdf_docs.items() if v["cifrado"]]
    pdf_cifrados_abiertos = [k for k in pdf_cifrados if pdf_docs[k]["abrio"]]
    pdf_abiertos_todos = [k for k, v in pdf_docs.items() if v["abrio"]]

    def pct(num: int, den: int) -> str:
        return f"{100.0 * num / den:.2f}" if den else "NO-APLICA"

    salida = {
        "estampa_universo_A10": {
            "generacion": "v7",
            "expedientes_examinados": expedientes,
            "registros_indice_e2": registros,
            "procedimiento_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "cifra_1_value_labels_sav": {
            "escala": "PORCENTAJE-DE-CONSERVACION",
            "numerador": vl_conservadas["SAV"],
            "denominador": vl_total["SAV"],
            "denominador_es": "entradas de value_labels en registros con objeto_tipo terminado en -SAV",
            "registros_portadores": vl_registros["SAV"],
            "porcentaje": pct(vl_conservadas["SAV"], vl_total["SAV"]),
        },
        "cifra_1_contraste_dta": {
            "escala": "PORCENTAJE-DE-CONSERVACION",
            "numerador": vl_conservadas["DTA"],
            "denominador": vl_total["DTA"],
            "denominador_es": "entradas de value_labels en registros con objeto_tipo terminado en -DTA",
            "registros_portadores": vl_registros["DTA"],
            "porcentaje": pct(vl_conservadas["DTA"], vl_total["DTA"]),
            "referencia_declarada": "99.5",
        },
        "cifra_2_metadatos_zip": {
            "escala": "PORCENTAJE-DE-CONSERVACION",
            "numerador": zip_enteros,
            "denominador": zip_miembros,
            "denominador_es": "registros con objeto_tipo=MIEMBRO-ZIP",
            "criterio": "definicion sin redaccion y con las cuatro claves bytes=/comprimidos=/crc=/zip_slip=",
            "porcentaje": pct(zip_enteros, zip_miembros),
            "solo_zip_slip_presente": {
                "escala": "PORCENTAJE-DE-CONSERVACION",
                "numerador": zip_con_zip_slip,
                "denominador": zip_miembros,
                "porcentaje": pct(zip_con_zip_slip, zip_miembros),
            },
            "reparto_zip_slip": {
                "escala": "CONTEO-ABSOLUTO",
                "valores": dict(sorted(zip_slip_reparto.items())),
            },
        },
        "cifra_3_pdf_abiertos": {
            "escala": "CONTEO-ABSOLUTO-CON-PORCENTAJE",
            "unidad": "documento PDF (representacion_id + prefijo de localizador)",
            "universo_A_cifrados": len(pdf_cifrados),
            "universo_A_es": "documentos PDF con al menos una pagina cifrado=SI-EXTRAIBLE",
            "universo_B_abiertos_de_A": len(pdf_cifrados_abiertos),
            "universo_B_es": "los de A con al menos una pagina texto_extraible=SI",
            "porcentaje_B_sobre_A": pct(len(pdf_cifrados_abiertos), len(pdf_cifrados)),
            "denominador_ajeno_pdf_totales": pdf_total,
            "denominador_ajeno_pdf_abiertos_todos": len(pdf_abiertos_todos),
        },
    }
    print(json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
