#!/usr/bin/env python3
"""Barrido de vocabulario por regla sobre los tres inventarios vigentes.

ACTO MAESTRA38-N23-N25. Un patron por regla, aplicado a los campos
`variable_id` + `texto_reactivo` de cada fila. NO abre microdato: solo lee
los TSV de inventario (metadato de reactivo).

Uso:  python3 tools/barrido_negativos_m38.py [--regla R7.4]
Salida: bloque por regla con conteo de filas, conteo de aciertos y el
desglose por (instrumento, archivo_miembro).
"""
import argparse
import csv
import re
import sys
from collections import Counter

INVENTARIOS = [
    "data/inventario-reactivos-v1_2.tsv",
    "data/inventario-reactivos-descargas-mx-v1_2.tsv",
    "data/inventario-reactivos-ext-v1_0.tsv",
]

# Un patron por regla. Vocabulario amplio a proposito: el falso positivo se
# cuenta y se declara; el falso negativo es el que sella un negativo en falso.
PATRONES = {
    "R7.4": r"MARCHA|PROTEST|MANIFEST|PLANTON|PLANTÓN|MITIN|BLOQUEO|HUELGA|PARO |PETICION|PETICIÓN",
    "R7.4-victimizacion": r"VICTIMA|VÍCTIMA|DELITO|ROBO|ASALT|EXTORSION|EXTORSIÓN|SECUESTR",
    "R4.5": r"SELLO|ETIQUETADO|OCTAGON|OCTÁGON|EXCESO DE (AZUCAR|AZÚCAR|CALORIAS|CALORÍAS|SODIO|GRASA)|ADVERTENCIA.{0,20}(AZUCAR|AZÚCAR|CALORIA|CALORÍA|SODIO|GRASA)",
    # Complemento de R4.5: el patron por vocabulario NO alcanza el modulo ETI de
    # ENSANUT 2024 en su miembro .csv (sin etiquetas); el prefijo de nombre si.
    "R4.5-ETI-prefijo": r"^ETI",
    "R9.3": r"LE CREE|CREE MAS EN|CREE MÁS EN|CONFIA MAS EN|CONFÍA MÁS EN|CREDIBILIDAD|NO CREE EN NADA",
    # Las ocho que se sostienen -- se recuentan para dejar el numero en la nota.
    "coercitivo": r"COERCI|COACC|OBLIG.{0,10}A LA FUERZA|AMENAZ.{0,15}(PARA QUE|SI NO)",
    "G4.horizonte_temporal": r"HORIZONTE TEMPORAL|DESCUENTO (TEMPORAL|INTERTEMPORAL)|PREFER.{0,15}TEMPORAL|LARGO PLAZO VS|INTERTEMPORAL",
    "R6.1": r"PUNTUAL|A TIEMPO|LLEG.{0,10}TARDE|IMPUNTUAL|RETRASO",
    "R6.2": r"CUMPL.{0,15}COMPROMISO|COMPROMISO ADQUIRIDO|PROMES.{0,10}CUMPL",
    "R6.4": r"RECORDATORIO|RECUERD|AVISO PREVIO|LE RECORD",
    "R10.1": r"RECHAZO|RECHAZ",
    "R10.2": r"RETROALIMENTACION|RETROALIMENTACIÓN|CRITICA CONSTRUCTIVA|CRÍTICA CONSTRUCTIVA|CENSUR",
    "R2.1": r"INICIATIVA|AUTONOM|POR SU PROPIA CUENTA|SIN QUE (LE|LO) DIGAN",
    "R4.2": r"PERMISO|AUTORIZACION|AUTORIZACIÓN|PEDIR.{0,15}PERMISO|POR QUE NO ACUDIO|POR QUÉ NO ACUDIÓ",
    "R8.2": r"TANDA|CUNDINA|CAJA DE AHORRO|AHORRO ROTATIVO",
    "R6.3": r"BOMBERAZO|URGENCIA|EMERGENCIA|ULTIMO MOMENTO|ÚLTIMO MOMENTO",
}


def filas():
    for ruta in INVENTARIOS:
        with open(ruta, encoding="utf-8", newline="") as fh:
            lineas = (l for l in fh if not l.startswith("#"))
            for fila in csv.DictReader(lineas, delimiter="\t"):
                fila["_inventario"] = ruta
                yield fila


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regla", action="append", help="limita a esta(s) regla(s)")
    args = ap.parse_args()
    reglas = args.regla or list(PATRONES)

    universo = list(filas())
    print(f"UNIVERSO: {len(universo)} filas de {len(INVENTARIOS)} inventarios")
    for ruta in INVENTARIOS:
        print(f"  {ruta}: {sum(1 for f in universo if f['_inventario'] == ruta)}")

    for regla in reglas:
        patron = re.compile(PATRONES[regla], re.IGNORECASE)
        aciertos = [
            f for f in universo
            if patron.search(f.get("variable_id") or "")
            or patron.search(f.get("texto_reactivo") or "")
        ]
        print(f"\n=== {regla} · patron: {PATRONES[regla]}")
        print(f"    aciertos: {len(aciertos)} / {len(universo)}")
        for (inst, miembro), n in Counter(
            (f.get("instrumento", ""), f.get("archivo_miembro", "")) for f in aciertos
        ).most_common(25):
            print(f"    {n:6d}  {inst} :: {miembro}")

    if not args.regla:
        detalle_r74(universo)
        detalle_items(universo, r"etiquetado_ensanut2924_w\.dta", r"^eti", "R4.5 -- modulo ETI de ENSANUT 2024 (.dta, con etiquetas)")
        detalle_items(universo, r"sociedaddelainformacion", r"^p53_\d+$", "R9.3 -- bateria p53, Sociedad de la Informacion (UNAM-IIJ)")
        detalle_items(universo, r"medioambiente", r"^p33_\d+$", "R9.3 -- bateria p33, Medio Ambiente (corroboracion secundaria)")


# --- Detalle 2: tabla de existencia por termino de regla y por encuesta (R7.4) ---

ENCUESTAS_R74 = {
    "ENCUP 2012": r"ENCUP",
    "losmexicanos Cultura Politica": r"losmexicanos_unam_iij/culturapolitica",
    "Cultura Constitucional 3a": r"cultura_constitucional_unam_iij",
}
TERMINOS_R74 = {
    "PROTESTA": r"MARCHA|PROTEST|MANIFEST|PLANTON|MITIN|BLOQUEO|HUELGA",
    "VICTIMA": r"VICTIM|DELITO|DELINCUEN|ROBO|ROBAR|ASALT|EXTORSI|SECUESTR|"
               r"INSEGURID|LE HA PASADO|HA SUFRIDO|FUE OBJETO|CRIMEN",
    "FALLA_ESTATAL": r"CONFIAN|CONFÍA|CONFIA|JUEC|JUSTICIA|MINISTERIO P|POLIC|"
                     r"TRIBUNAL|AUTORIDAD",
    "RED_PREVIA": r"ORGANIZACI|ASOCIACI|AGRUPACI|SINDICAT|VECINAL|PERTENEC|COMIT",
    "URBANO_RURAL": r"RURAL|URBAN|ESTRATO|LOCALIDAD|TAMA.O DE|AMBITO|ÁMBITO",
    "PONDERADOR": r"FACTOR|PONDER|WEIGHT|FEXP|PESO|EXPANSION|EXPANSIÓN",
}


def detalle_r74(universo):
    print("\n\n########## DETALLE R7.4 -- existencia por termino y por encuesta")
    for enc, epat in ENCUESTAS_R74.items():
        sub = [f for f in universo if re.search(epat, f["archivo_miembro"], re.I)]
        print(f"\n--- {enc}: {len(sub)} filas de inventario")
        for tn, tp in TERMINOS_R74.items():
            p = re.compile(tp, re.I)
            u = {}
            for f in sub:
                if p.search(f.get("variable_id") or "") or p.search(f.get("texto_reactivo") or ""):
                    u.setdefault(f["variable_id"], f.get("texto_reactivo") or "")
            print(f"    {tn}: {len(u)} variables unicas")
            for k, v in list(u.items())[:20]:
                print(f"        {k}\t{v[:120]}")


def detalle_items(universo, fpat, vpat, titulo):
    print(f"\n\n########## DETALLE {titulo}")
    fp, vp = re.compile(fpat, re.I), re.compile(vpat, re.I)
    best = {}
    for f in universo:
        if fp.search(f["archivo_miembro"] or "") and vp.search(f.get("variable_id") or ""):
            k = f["variable_id"]
            t = f.get("texto_reactivo") or ""
            if len(t) > len(best.get(k, "")):
                best[k] = t
    for k in sorted(best):
        print(f"    {k}\t{best[k]}")


if __name__ == "__main__":
    sys.exit(main())
