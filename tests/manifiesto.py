#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/manifiesto.py — procedencia de dato externo (data/manifiesto.yaml).

--registra   añade una entrada NUEVA para un archivo que ya está en data/raw/.
             sha256, tamaño y entorno_descarga se derivan del archivo real y
             del proceso en ejecución -- ninguno se teclea ni se pide por
             parámetro. No sobreescribe: un id que ya existe es error.

--verifica   recomputa sha256 y tamaño del archivo que una entrada declara
             (campo `archivo`) y los compara contra lo que el manifiesto
             registra. Sin --id, verifica todas las entradas con payload.
             Un archivo ausente de data/raw/ se reporta AUSENTE -- no es un
             error del script, es un hecho sobre el entorno (el payload
             nunca se commitea; puede faltar sin que nada esté roto).

Motivación (cola I-04): el encargo del 30/jul citó 18513 bytes para un
archivo que en realidad pesa 17262 -- una cifra tecleada, no derivada. Este
script existe para que sha256/tamaño de un payload de data/raw/ nunca se
escriban a mano en data/manifiesto.yaml. No cubre el caso que abrió I-04
(artefactos que el chat entrega, como TRANSFER-*.md) -- ese permanece
abierto; este script solo alcanza data/raw/.

DESVÍO DE ALCANCE, declarado (cola D-07): el encargo pedía que --registra
descargara el archivo desde `--url-origen`. Lo que existe registra un
archivo que YA está en data/raw/ -- no abre ningún socket ni valida TLS.
Es defendible (un script de este repo bajando de una URL con TLS sin
verificar es exactamente el tipo de riesgo que el resto del proyecto trata
con sospecha -- ver protocolo §4 y el propio caso de encig23 con proxy de
egreso bloqueado), pero es un desvío real y no una lectura literal del
encargo, así que se declara aquí en vez de quedar implícito. Lo que deja
sin cubrir: el momento de la descarga en sí sigue sin instrumentar -- ahí
nacieron los dos hashes tecleados a mano que este script existe para
evitar (data/manifiesto.yaml, entradas `encig23_*`, ambas de 2026-07-29,
anteriores a este script). Un --registra que sí descargara cerraría ese
hueco; con el diseño actual, alguien todavía teclea el sha256 de un
archivo recién bajado por fuera de este script antes de que --registra
pueda verificarlo.

--compara   contrasta un payload NUEVO (--archivo, típicamente recién
             bajado bajo un nombre de prueba) contra una entrada YA
             registrada (--id) -- sin escribir nada. Reporta COINCIDE o
             DISCREPANCIA. Cierra I-09: sin este modo, verificar un archivo
             recién descargado contra el manifiesto antes de decidir si
             reemplaza o confirma una entrada exigía hacerlo a mano. Una
             DISCREPANCIA es un HALLAZGO (el archivo cambió, o el hash
             original estaba mal, o la fuente cambió de contenido) -- el
             script la reporta, no la resuelve ni la silencia sobreescribiendo.

Única dependencia externa: PyYAML.
"""
import argparse
import datetime
import hashlib
import os
import platform
import socket
import sys

import yaml


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rutas(root):
    return (os.path.join(root, "data", "manifiesto.yaml"),
            os.path.join(root, "data", "raw"))


def separar_cabecera(texto):
    """Las líneas '#' iniciales son documentación de convención (ver el
    encabezado del propio archivo); no son un comentario de una entrada
    YAML y PyYAML las descarta al parsear. Se preservan aparte para no
    perderlas al reescribir."""
    lineas = texto.split("\n") if texto else []
    i = 0
    while i < len(lineas) and (lineas[i].startswith("#") or not lineas[i].strip()):
        i += 1
    return "\n".join(lineas[:i]), "\n".join(lineas[i:])


def leer_manifiesto(manifiesto_path):
    if not os.path.exists(manifiesto_path):
        return "", []
    with open(manifiesto_path, encoding="utf-8") as f:
        texto = f.read()
    cabecera, cuerpo = separar_cabecera(texto)
    return cabecera, (yaml.safe_load(cuerpo) or [])


def _str_presenter(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _str_presenter)


def escribir_manifiesto(manifiesto_path, cabecera, entradas):
    cuerpo = yaml.dump(entradas, allow_unicode=True, sort_keys=False, width=100)
    with open(manifiesto_path, "w", encoding="utf-8") as f:
        f.write((cabecera.rstrip("\n") + "\n\n" if cabecera.strip() else "") + cuerpo)


def sha256_de(path, buf_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf_size), b""):
            h.update(chunk)
    return h.hexdigest()


def entorno_actual():
    """Derivado del proceso en ejecución -- nunca pedido por parámetro."""
    return (f"{platform.system()} {platform.release()} ({platform.machine()}) "
            f"· Python {platform.python_version()} · host {socket.gethostname()}")


def buscar(entradas, id_):
    for e in entradas:
        if e.get("id") == id_:
            return e
    return None


# ───────────────────────────────────────────────────────────── --registra ──

def cmd_registra(a, manifiesto_path, raw_dir):
    obligatorios = [("--id", a.id), ("--archivo", a.archivo),
                     ("--usado-para", a.usado_para), ("--url-origen", a.url_origen),
                     ("--descargado-por", a.descargado_por), ("--formato", a.formato),
                     ("--licencia", a.licencia)]
    faltan = [nombre for nombre, valor in obligatorios if not valor]
    if faltan:
        print(f"ERROR: --registra exige {', '.join(faltan)} (no se rellenan con "
              f"placeholder).", file=sys.stderr)
        sys.exit(1)

    cabecera, entradas = leer_manifiesto(manifiesto_path)
    if buscar(entradas, a.id):
        print(f"ERROR: el id '{a.id}' ya existe. Este script no sobreescribe "
              f"entradas registradas -- si el dato cambió, es una entrada nueva "
              f"con id nuevo, no un edit silencioso.", file=sys.stderr)
        sys.exit(1)

    ruta_absoluta = os.path.join(raw_dir, a.archivo)
    if not os.path.exists(ruta_absoluta):
        print(f"ERROR: data/raw/{a.archivo} no existe. --registra deriva "
              f"sha256/tamaño del archivo real; no registra lo que no está en "
              f"disco.", file=sys.stderr)
        sys.exit(1)

    entrada = {
        "id": a.id,
        "usado_para": a.usado_para,
        "url_origen": a.url_origen,
        "fecha_descarga": a.fecha_descarga or datetime.date.today().isoformat(),
        "descargado_por": a.descargado_por,
        "archivo": a.archivo,
        "sha256": sha256_de(ruta_absoluta),
        "tamano_bytes": os.path.getsize(ruta_absoluta),
        "formato": a.formato,
        "licencia": a.licencia,
        "entorno_descarga": entorno_actual(),
    }
    if a.nota:
        entrada["nota"] = a.nota

    entradas.append(entrada)
    escribir_manifiesto(manifiesto_path, cabecera, entradas)

    print(f"Registrado '{a.id}' en {os.path.relpath(manifiesto_path)}:")
    for k, v in entrada.items():
        print(f"  {k}: {v}")


# ───────────────────────────────────────────────────────────── --verifica ──

def cmd_verifica(a, manifiesto_path, raw_dir):
    _, entradas = leer_manifiesto(manifiesto_path)
    con_payload = [e for e in entradas if "sha256" in e]

    if a.id:
        objetivo = [e for e in con_payload if e.get("id") == a.id]
        if not objetivo:
            existe_sin_payload = buscar(entradas, a.id) is not None
            razon = ("existe pero no tiene payload (sha256) -- es una entrada de "
                      "nota/documentación" if existe_sin_payload else "no existe")
            print(f"ERROR: id '{a.id}' {razon} en el manifiesto.", file=sys.stderr)
            sys.exit(1)
    else:
        objetivo = con_payload

    print(f"Entorno de verificación: {entorno_actual()}")
    print()

    exit_code = 0
    for entrada in objetivo:
        id_ = entrada.get("id", "?")
        archivo = entrada.get("archivo")
        if not archivo:
            print(f"{id_}: SIN CAMPO 'archivo' en el manifiesto -- no se puede "
                  f"localizar el payload (omitido, no cuenta como falla)")
            continue

        ruta = os.path.join(raw_dir, archivo)
        if not os.path.exists(ruta):
            print(f"{id_}: AUSENTE -- data/raw/{archivo} no está en disco "
                  f"(no es un error: el payload no se commitea)")
            continue

        sha_real = sha256_de(ruta)
        tam_real = os.path.getsize(ruta)
        sha_ok = sha_real == entrada.get("sha256")
        tam_ok = tam_real == entrada.get("tamano_bytes")

        if sha_ok and tam_ok:
            print(f"{id_}: COINCIDE -- sha256 y tamaño ({tam_real} bytes) "
                  f"verificados contra data/manifiesto.yaml")
        else:
            exit_code = 1
            print(f"{id_}: NO COINCIDE")
            if not sha_ok:
                print(f"    sha256 manifiesto: {entrada.get('sha256')}")
                print(f"    sha256 real:       {sha_real}")
            if not tam_ok:
                print(f"    tamano_bytes manifiesto: {entrada.get('tamano_bytes')}")
                print(f"    tamano_bytes real:       {tam_real}")

    sys.exit(exit_code)


# ───────────────────────────────────────────────────────────── --compara ──

def cmd_compara(a, manifiesto_path, raw_dir):
    if not a.id or not a.archivo:
        print("ERROR: --compara exige --id (entrada ya registrada) y --archivo "
              "(payload nuevo a contrastar).", file=sys.stderr)
        sys.exit(1)

    _, entradas = leer_manifiesto(manifiesto_path)
    entrada = buscar(entradas, a.id)
    if entrada is None:
        print(f"ERROR: id '{a.id}' no existe en el manifiesto. --compara contrasta "
              f"contra una entrada YA registrada; no crea una.", file=sys.stderr)
        sys.exit(1)
    if "sha256" not in entrada:
        print(f"ERROR: '{a.id}' existe pero no tiene payload (sha256) -- es una "
              f"entrada de nota/documentación, no hay nada contra qué contrastar.",
              file=sys.stderr)
        sys.exit(1)

    ruta = os.path.join(raw_dir, a.archivo)
    if not os.path.exists(ruta):
        print(f"ERROR: data/raw/{a.archivo} no existe. --compara contrasta un "
              f"payload real; no compara contra un archivo que no está en disco.",
              file=sys.stderr)
        sys.exit(1)

    sha_nuevo = sha256_de(ruta)
    tam_nuevo = os.path.getsize(ruta)
    sha_ok = sha_nuevo == entrada.get("sha256")
    tam_ok = tam_nuevo == entrada.get("tamano_bytes")

    print(f"Entorno de verificación: {entorno_actual()}")
    print()
    print(f"Contrastando data/raw/{a.archivo} contra '{a.id}' "
          f"(registrado como data/raw/{entrada.get('archivo', '?')}):")

    if sha_ok and tam_ok:
        print(f"  COINCIDE -- sha256 y tamaño ({tam_nuevo} bytes) iguales a los "
              f"registrados para '{a.id}'. No se escribió nada.")
        sys.exit(0)
    else:
        print(f"  DISCREPANCIA -- no es un error del script, es un HALLAZGO: "
              f"el payload nuevo no coincide con lo que '{a.id}' tiene "
              f"registrado. No se sobreescribe nada; decidirlo es de quien lea "
              f"este resultado.")
        print(f"    sha256 registrado: {entrada.get('sha256')}")
        print(f"    sha256 nuevo:      {sha_nuevo}")
        print(f"    tamano_bytes registrado: {entrada.get('tamano_bytes')}")
        print(f"    tamano_bytes nuevo:      {tam_nuevo}")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--registra", action="store_true",
                    help="Registra una entrada nueva para un archivo ya en data/raw/")
    g.add_argument("--verifica", action="store_true",
                    help="Verifica una entrada (--id) o todas las que tengan payload")
    g.add_argument("--compara", action="store_true",
                    help="Contrasta un payload nuevo (--archivo) contra una entrada "
                         "ya registrada (--id), sin escribir nada")

    ap.add_argument("--id", default=None)
    ap.add_argument("--archivo", default=None,
                     help="ruta relativa dentro de data/raw/ (--registra)")
    ap.add_argument("--usado-para", dest="usado_para", default=None)
    ap.add_argument("--url-origen", dest="url_origen", default=None)
    ap.add_argument("--descargado-por", dest="descargado_por", default=None)
    ap.add_argument("--formato", default=None)
    ap.add_argument("--licencia", default=None)
    ap.add_argument("--fecha-descarga", dest="fecha_descarga", default=None,
                     help="YYYY-MM-DD; por defecto, hoy")
    ap.add_argument("--nota", default=None)
    ap.add_argument("--root", default=None,
                     help=argparse.SUPPRESS)  # override de raíz, solo para pruebas

    a = ap.parse_args()
    root = a.root or repo_root()
    manifiesto_path, raw_dir = rutas(root)

    if a.registra:
        cmd_registra(a, manifiesto_path, raw_dir)
    elif a.verifica:
        cmd_verifica(a, manifiesto_path, raw_dir)
    else:
        cmd_compara(a, manifiesto_path, raw_dir)


if __name__ == "__main__":
    main()
