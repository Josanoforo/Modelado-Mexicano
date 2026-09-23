"""Inventario conducta × ola × ámbito desde RESULT sellados y exclusiones documentales."""

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/dominios/genero/endireh-matriz-conducta-ola-ambito.tsv"
CALCS = [
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004",
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001",
    "CALC-ENDIREH-PISOS-2021-AYUDA-0001",
    "CALC-ENDIREH-PISOS-2021-DECISIONES-0001",
    "CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001",
    "CALC-ENDIREH-PISOS-2021-FAMILIAR-0001",
    "CALC-ENDIREH-PISOS-2021-ESCOLAR-0001",
    "CALC-ENDIREH-PISOS-2021-LABORAL-0001",
    "CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001",
    "CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001",
    "CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002",
    "CALC-ENDIREH-PISOS-2016-RESTANTES-0001",
    "CALC-ENDIREH-PISOS-2011-MODULOS-0001",
    "CALC-ENDIREH-PISOS-2006-MODULOS-0002",
]
FIELDS = ("conducta", "ola", "ambito", "ventana", "instrumento", "dictamen",
          "publicacion_nacional", "calc_id", "result_id", "resultados_sha256", "evidencia")


def ambit(name, calc):
    if "DISCRIMINACION" in calc:
        return "discriminacion_laboral"
    if "NOFISICA" in calc:
        return "pareja_servicios" if name.startswith(("ayuda", "denuncia", "institucion", "razon")) else "pareja"
    if name.startswith(("pareja_", "emocional_", "economica_", "sexual_", "fisica_")) or "PAREJA" in calc:
        return "pareja"
    if name.startswith(("externo_", "despojo_")):
        return "externo/familiares u otros"
    if name.startswith(("discriminacion_", "prueba_", "perjuicio_")):
        return "discriminacion_laboral"
    if name.startswith(("decision_", "dinero_", "permiso_")):
        return "economia_decisiones"
    for prefix, domain in (("escolar", "escolar"), ("laboral", "laboral_interpersonal"),
                           ("comunitaria", "comunitario"), ("familiar", "familiar")):
        if name.startswith(prefix):
            return domain
    if "AYUDA" in calc:
        return "pareja_servicios"
    return "instrumento_especifico"


def main():
    out = []
    for calc in CALCS:
        raw = (ROOT / "data/corrida0" / calc / "resultados.json").read_bytes()
        payload = json.loads(raw)["resultados"]
        result_id = next(k for k in payload if k.endswith("TABLA"))
        rows = json.loads(payload[result_id])
        year = calc.split("-")[3]
        seen = set()
        for row in rows:
            if row.get("eje") != "nacional" or row.get("categoria") != "MX":
                continue
            name = row["resultado"]
            window = row.get("ventana", "")
            key = (name, window)
            if key in seen:
                continue
            seen.add(key)
            out.append(dict(conducta=name, ola=year, ambito=ambit(name, calc), ventana=window,
                            instrumento="A/B/C según spec; cortes de situación en tabla",
                            dictamen="MEDIDO", publicacion_nacional=row["estado"],
                            calc_id=calc, result_id=result_id,
                            resultados_sha256=hashlib.sha256(raw).hexdigest(),
                            evidencia="spec.md + RESULT sellado"))
    exclusions = [
        ("pareja_vida", "2003", "pareja", "vida de relación", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Cuestionario 2003 capítulo VIII pregunta últimos 12 meses; vida no preguntada"),
        ("pareja_anual", "2003", "pareja", "últimos 12 meses", "pareja residente", "DEPENDENCIA_EXTERNA", "Faltan UPM/estrato por registro o pesos replicados para IC; dictamen 2003"),
        ("pareja_otros_estados", "2003", "pareja", "cualquiera", "sin pareja residente", "EXCLUIDO_POR_DISEÑO", "Elegibilidad del cuestionario 2003"),
        ("escolar", "2003", "escolar", "cualquiera", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Sin módulo de violencia escolar separado en 2003"),
        ("laboral_interpersonal", "2003", "laboral_interpersonal", "cualquiera", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Sin módulo de violencia laboral separado en 2003"),
        ("comunitaria", "2003", "comunitario", "cualquiera", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Sin módulo comunitario separado en 2003"),
        ("familiar_fuera_pareja", "2003", "familiar", "cualquiera", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Sin módulo familiar separado en 2003"),
        ("discriminacion_laboral_8_3", "2003", "discriminacion_laboral", "cualquiera", "pareja residente", "EXCLUIDO_POR_DISEÑO", "Reactivos 8.3 de 2021 no existen en 2003"),
        ("pareja_denuncia_institucional_C", "2011", "pareja", "vida", "C soltera", "EXCLUIDO_POR_DISEÑO", "C 6.4 pregunta ayuda e informó a familiares; sin resultado separado de denuncia institucional"),
        ("pareja_decisiones_actuales_B", "2011", "economia_decisiones", "entrevista", "B alguna vez unida", "EXCLUIDO_POR_DISEÑO", "B 7.1 mide dinero libre, sin decisiones con pareja actual"),
        ("pareja_ayuda_institucional_C", "2006", "pareja", "vida", "MS soltera", "EXCLUIDO_POR_DISEÑO", "MS P28_2 pregunta aviso/denuncia a familiares; sin bloque P7.7"),
        ("pareja_reciente_C", "2006", "pareja", "año", "MS soltera", "EXCLUIDO_POR_DISEÑO", "MS P28_1 no tiene pares de frecuencia anual P7.4"),
        ("pareja_vida_sin_relacion_C2", "2021", "pareja", "vida", "C2", "EXCLUIDO_POR_DISEÑO", "C2 nunca tuvo relación de pareja elegible"),
        ("embarazo_no_ocurrido_como_no_discriminacion", "2021", "discriminacion_laboral", "2016–entrevista", "no embarazada", "EXCLUIDO_POR_DISEÑO", "Código 3 de 8.3 indica no estuvo embarazada, fuera del denominador entre embarazadas"),
    ]
    for name, year, domain, window, instrument, status, evidence in exclusions:
        out.append(dict(conducta=name, ola=year, ambito=domain, ventana=window,
                        instrumento=instrument, dictamen=status, publicacion_nacional="NO_APLICA",
                        calc_id="", result_id="", resultados_sha256="", evidencia=evidence))
    out.sort(key=lambda r: (r["ola"], r["ambito"], r["conducta"], r["ventana"]))
    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(out)
    print(f"{OUT.relative_to(ROOT)}: {len(out)} dictámenes")


if __name__ == "__main__":
    main()
