#!/usr/bin/env python3
"""Arbitro generico de R por celda. ENCARGO MAESTRA33-C2 ARBITRO-R-1.

Lee un marco congelado (columnas encuesta/ola/universo/variable/estimador/
ponderador/escala por celda), localiza el payload declarado en
data/manifiesto.yaml por (encuesta, ola) y, cuando el marco trae lo
suficiente para calcular sin inventar nada, escribe corridas-R/<id>.json
con el mismo esquema que los archivos ya existentes (leido de uno de
ellos, no hardcodeado aqui).

Hallazgo de este acto (ver P3 / regresion): ni marco-M-congelado-v1_1.tsv
ni marco-congelado-piloto-v1_0.tsv declaran la codificacion binaria
(que valor es "si"/"1" y cual "no"/"0") ni el diseno real de muestreo
(estrato, upm) como columnas estructuradas -- la columna llamada
"estrato" en ambos marcos carga en realidad la etiqueta compuesta
dominio|grado_dependencia|dificultad, no una variable de diseno. Los R
que ya existen en corridas-R/ se calcularon leyendo el FD de cada
encuesta a mano (ver forense/prereg-duelo-v2/correr-R.py, funciones
celda_*). Esta herramienta NO inventa esa lectura: cuando falta,
escribe estado NO-EJECUTABLE-SIN-CODIFICACION declarando exactamente
que columna falta, en vez de adivinar.
"""
import csv
import hashlib
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRIDAS_R = os.path.join(RAIZ, "forense", "prereg-duelo-v2", "corridas-R")
MANIFIESTO = os.path.join(RAIZ, "data", "manifiesto.yaml")
COLA = os.path.join(RAIZ, "data", "cola-adquisicion-v1_0.tsv")


def _plano(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def lee_marco(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def esquema_de_referencia():
    """Claves del esquema de un corridas-R/*.json ya existente -- no hardcodeadas."""
    for nombre in sorted(os.listdir(CORRIDAS_R)):
        if nombre.endswith(".json") and not nombre.startswith("_"):
            with open(os.path.join(CORRIDAS_R, nombre), encoding="utf-8") as f:
                return sorted(json.load(f).keys())
    raise RuntimeError("no hay ningun corridas-R/*.json existente del que leer el esquema")


def carga_manifiesto():
    import yaml
    with open(MANIFIESTO, encoding="utf-8") as f:
        return yaml.safe_load(f)


def localiza_payload(manifiesto, encuesta, ola):
    """Heuristica de sustring sobre id/archivo del manifiesto -- NUNCA inventa
    un payload_id; si no hay entrada cuyo id/archivo contenga ambas piezas
    (encuesta normalizada + ola), devuelve None."""
    pe, po = _plano(encuesta), _plano(ola)
    candidatos = []
    for e in manifiesto:
        clave = _plano(e.get("id", "")) + _plano(e.get("archivo", ""))
        if pe and pe in clave and po and po in clave:
            candidatos.append(e)
    return candidatos


def sha256_de(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def encola_no_obtenido(id_celda, encuesta, ola):
    fila = f"{id_celda}\t{encuesta}\t{ola}\tarbitra.py: NO-OBTENIDO, sin payload en manifiesto.yaml para (encuesta,ola)\n"
    existe_ya = False
    if os.path.exists(COLA):
        with open(COLA, encoding="utf-8") as f:
            existe_ya = any(l.startswith(id_celda + "\t") for l in f)
    if not existe_ya:
        with open(COLA, "a", encoding="utf-8") as f:
            f.write(fila)


def procesa_fila(fila, manifiesto, esquema):
    id_celda = fila["id"]
    salida = os.path.join(CORRIDAS_R, f"{id_celda}.json")
    if os.path.exists(salida):
        return "YA-EXISTE", id_celda

    encuesta, ola = fila.get("encuesta", ""), fila.get("ola", "")
    candidatos = localiza_payload(manifiesto, encuesta, ola)
    if not candidatos:
        encola_no_obtenido(id_celda, encuesta, ola)
        return "NO-OBTENIDO", id_celda

    # Punto de bloqueo confirmado por P3: el marco no declara codificacion
    # binaria ni estrato/upm de diseno (ver docstring). Sin esos dos datos
    # no hay forma de aplicar el estimador sin inventar -- se declara.
    faltantes = []
    if not fila.get("estimador", "").strip():
        faltantes.append("estimador")
    if "codificacion" not in fila:
        faltantes.append("codificacion (columna no existe en este marco)")
    if "estrato_diseno" not in fila and "upm" not in fila:
        faltantes.append("estrato_diseno/upm (columna 'estrato' de este marco es una etiqueta compuesta, no diseno muestral)")

    doc = {k: None for k in esquema}
    doc.update({
        "id_celda": id_celda,
        "estado": "NO-EJECUTABLE-SIN-CODIFICACION",
        "encuesta": encuesta,
        "ola": ola,
        "universo": fila.get("universo"),
        "variable": fila.get("variable"),
        "ponderador": fila.get("ponderador"),
        "escala": fila.get("escala"),
        "payload_id_candidatos": [c.get("id") for c in candidatos],
        "faltantes": faltantes,
    })
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return "NO-EJECUTABLE-SIN-CODIFICACION", id_celda


def main(ruta_marco, columna_elegible=None, solo_ids=None):
    esquema = esquema_de_referencia()
    manifiesto = carga_manifiesto()
    filas = lee_marco(ruta_marco)
    if columna_elegible:
        filas = [f for f in filas if f.get(columna_elegible, "").strip().upper() == "SI"]
    if solo_ids:
        filas = [f for f in filas if f["id"] in solo_ids]

    resultados = {}
    for fila in filas:
        estado, id_celda = procesa_fila(fila, manifiesto, esquema)
        resultados.setdefault(estado, []).append(id_celda)

    for estado, ids in sorted(resultados.items()):
        print(f"{estado}: {len(ids)} -> {' '.join(ids)}")
    return resultados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"uso: {sys.argv[0]} <ruta-marco.tsv> [columna_elegible] [id1 id2 ...]")
        sys.exit(2)
    ruta = sys.argv[1]
    col = sys.argv[2] if len(sys.argv) > 2 else None
    solo = sys.argv[3:] or None
    main(ruta, col, solo)
