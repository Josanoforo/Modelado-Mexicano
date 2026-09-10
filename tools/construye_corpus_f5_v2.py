#!/usr/bin/env python3
"""Construye el manifiesto del corpus F5 v2.0 sin mirar R ni resultados.

La elegibilidad temporal se hereda, celda por celda, del manifiesto v1.0
sellado. Sobre los documentos elegibles se aplica una regla prospectiva y
determinista: dividir Markdown desde cada encabezado hasta el encabezado
siguiente e incluir una sección cuando contiene al menos un término primario
de la familia. El paquete se materializa sólo en memoria; Git conserva
fuente+rango+hash y no duplica el texto de corpus/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "forense/prereg-duelo-v2/paquete-corpus-F5-v1_0/manifiesto.json"
SALIDA = ROOT / "forense/prereg-duelo-v2/paquete-corpus-F5-v2_0/manifiesto.json"

TERMINOS = {
    "CIV": ["no denuncia", "denuncia", "miedo al agresor", "desconfianza en la autoridad", "victimizacion"],
    "DIN": ["ahorro", "ahorros", "inclusion financiera"],
    "FAM_APOYO": ["vejez", "cuidado intergeneracional", "apoyo familiar"],
    "FAM_REMESAS": ["remesa", "remesas", "migracion"],
    "TRA": ["corrupcion", "mordida", "soborno", "dadiva"],
}

DIRECTA = {
    "CIV-M-01": ["envipe", "bp1_23"],
    "CIV-M-02": ["envipe", "bp1_23"],
    "CIV-M-04": ["envipe", "bp1_23"],
    "CIV-M-10": ["envipe", "bp1_23"],
    "CIV-M-12": ["envipe", "bp1_23"],
    "CIV-M-13": ["envipe", "bp1_23"],
    "DIN-M-01": ["ennvih", "cr27"],
    "FAM-M-01": ["enif", "p9_9_4"],
    "FAM-M-05": ["enigh", "remesas"],
    "FAM-M-06": ["enigh", "remesas"],
    "FAM-M-07": ["enigh", "remesas"],
    "TRA-M-02": ["encuci", "ap5_17", "ap5_18"],
    "TRA-M-03": ["encig", "p8_3", "2013"],
    "TRA-M-07": ["encig", "p8_3_1", "2021"],
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def familia(celda: str) -> str:
    if celda.startswith("CIV-"):
        return "CIV"
    if celda == "DIN-M-01":
        return "DIN"
    if celda == "FAM-M-01":
        return "FAM_APOYO"
    if celda.startswith("FAM-"):
        return "FAM_REMESAS"
    return "TRA"


def secciones(texto: str) -> list[dict]:
    lineas = texto.splitlines(keepends=True)
    encabezados: list[tuple[int, str]] = []
    for i, linea in enumerate(lineas):
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", linea.rstrip("\n"))
        if m:
            encabezados.append((i, m.group(1)))
    if not encabezados:
        return [{"linea_inicio": 1, "linea_fin": len(lineas), "encabezado": "DOCUMENTO", "texto": texto}]
    resultado = []
    for pos, (inicio, titulo) in enumerate(encabezados):
        fin = encabezados[pos + 1][0] if pos + 1 < len(encabezados) else len(lineas)
        resultado.append({
            "linea_inicio": inicio + 1,
            "linea_fin": fin,
            "encabezado": titulo,
            "texto": "".join(lineas[inicio:fin]),
        })
    return resultado


def contexto_desde_entrada(entrada: dict) -> str:
    partes = []
    for exc in entrada["extractos"]:
        ruta = ROOT / exc["fuente"]
        lineas = ruta.read_text(encoding="utf-8").splitlines(keepends=True)
        texto = "".join(lineas[exc["linea_inicio"] - 1:exc["linea_fin"]])
        if sha(texto.encode()) != exc["sha256_extracto"]:
            raise RuntimeError(f"extracto cambió: {exc['id_extracto']}")
        partes.append(f"\n\n=== {exc['id_extracto']} · {exc['encabezado']} ===\n\n{texto}")
    return "".join(partes)


def construir() -> dict:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    celdas = {}
    for celda, anterior in sorted(base["celdas"].items()):
        terminos = TERMINOS[familia(celda)]
        extractos = []
        sin_pertinencia = []
        for ruta_rel in sorted(anterior["documentos_incluidos"]):
            ruta = ROOT / ruta_rel
            bruto = ruta.read_bytes()
            texto = bruto.decode("utf-8")
            encontrados_documento = 0
            for sec in secciones(texto):
                normal = norm(sec["texto"])
                hits = sorted({t for t in terminos if t in normal})
                if not hits:
                    continue
                encontrados_documento += 1
                extracto_id = f"{celda}-X{len(extractos)+1:03d}"
                extractos.append({
                    "id_extracto": extracto_id,
                    "fuente": ruta_rel,
                    "sha256_fuente": sha(bruto),
                    "encabezado": sec["encabezado"],
                    "linea_inicio": sec["linea_inicio"],
                    "linea_fin": sec["linea_fin"],
                    "terminos_activados": hits,
                    "sha256_extracto": sha(sec["texto"].encode()),
                    "chars": len(sec["texto"]),
                    "bytes_utf8": len(sec["texto"].encode()),
                })
            if encontrados_documento == 0:
                sin_pertinencia.append(ruta_rel)
        entrada = {
            "encuesta": anterior["encuesta"],
            "ola": anterior["ola"],
            "regla_elegibilidad_temporal": "heredada byte a byte de paquete-corpus-F5-v1_0/manifiesto.json",
            "terminos_primarios_normalizados": terminos,
            "extractos": extractos,
            "documentos_elegibles_sin_seccion_pertinente": sin_pertinencia,
            "documentos_excluidos_por_corte": anterior.get("documentos_excluidos", []),
            "razones_exclusion_por_corte": anterior.get("razones_exclusion", {}),
        }
        contexto = contexto_desde_entrada(entrada)
        directo = all(t in norm(contexto) for t in DIRECTA[celda])
        entrada.update({
            "n_extractos": len(extractos),
            "n_fuentes": len({x["fuente"] for x in extractos}),
            "chars_entregados": len(contexto),
            "bytes_utf8_entregados": len(contexto.encode()),
            "palabras_aprox": len(contexto.split()),
            "sha256_contenido_entregado": sha(contexto.encode()),
            "evidencia_directa_evento": "SI" if directo else "NO",
            "nota_suficiencia": (
                "Contiene conjuntamente los identificadores mínimos del instrumento/evento; no implica que contenga el punto objetivo."
                if directo else
                "Sólo evidencia contextual: faltan uno o más identificadores mínimos del instrumento/evento."
            ),
        })
        celdas[celda] = entrada
    return {
        "acto": "GEN2-F5-COMPLETA",
        "version": "v2_0",
        "fecha": "2026-09-10",
        "base_elegibilidad": str(BASE.relative_to(ROOT)),
        "metodo": "sección Markdown entre un encabezado y el siguiente; inclusión si contiene >=1 término primario normalizado de la familia; orden fuente+línea",
        "independencia": "La regla no lee R, M, capturas ni resultados. Los términos proceden del tema declarado en L-spec-v1_4.",
        "conteo_tokens": "No se afirma conteo exacto: se registran bytes, caracteres y palabras aproximadas. La aceptación del cliente se prueba aparte como transporte, no como réplica.",
        "n_celdas": len(celdas),
        "celdas": celdas,
    }


def validar(manifiesto: dict) -> None:
    if len(manifiesto["celdas"]) != 14:
        raise RuntimeError("se esperaban 14 celdas")
    for celda, entrada in manifiesto["celdas"].items():
        contexto = contexto_desde_entrada(entrada)
        if not contexto:
            raise RuntimeError(f"paquete vacío: {celda}")
        if sha(contexto.encode()) != entrada["sha256_contenido_entregado"]:
            raise RuntimeError(f"hash de paquete no coincide: {celda}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", action="store_true", help="verifica el manifiesto comprometido sin escribir")
    args = ap.parse_args()
    if args.verificar:
        validar(json.loads(SALIDA.read_text(encoding="utf-8")))
        print("OK: 14 paquetes íntegros")
        return 0
    manifiesto = construir()
    validar(manifiesto)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for celda, e in manifiesto["celdas"].items():
        print(f"{celda}: {e['n_extractos']} extractos, {e['chars_entregados']} chars, directa={e['evidencia_directa_evento']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
