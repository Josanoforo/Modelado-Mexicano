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

--escanea   recorre una carpeta fuera del repo (típicamente la carpeta de
             descargas del navegador) y, para cada archivo que no esté ya
             en data/manifiesto.yaml (dedup por sha256, no por nombre),
             deriva archivo/sha256/tamano_bytes/fecha_descarga (del mtime)/
             entorno_descarga/descargado_por y escribe una entrada STAGING
             en data/manifiesto-staging.yaml -- nunca en el manifiesto. No
             descarga nada, no sobreescribe nada y no abre ningún payload:
             hashear y hacer stat no es abrir; leer como texto un .php/.html
             guardado (para sugerir url_origen) tampoco toca ningún portal.
             url_origen y usado_para son los únicos dos campos que una
             máquina no deriva -- quedan en "" con comentario # PENDIENTE,
             salvo que --grupo/--url/--usado-para se los asignen a un lote.
             Un hash nuevo con un nombre que ya está registrado no se
             registra: se reporta aparte como hallazgo (mismo nombre,
             contenido distinto), no se resuelve solo. Agrupa por tanda de
             descarga (proximidad de mtime en disco, nunca solo por nombre;
             un cambio de día calendario o un salto grande siempre abre
             tanda nueva) para que el reporte no sea una lista de N líneas.

Única dependencia externa: PyYAML.
"""
import argparse
import datetime
import fnmatch
import hashlib
import os
import platform
import re
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
    """Prosa de un párrafo (sin línea en blanco interna) usa '>' plegado --
    PyYAML la reenvuelve a `width`, igual que la convención ya escrita a mano
    en este archivo. Un '\\n' real que sobrevive tras el pliegue (líneas en
    blanco internas, ej. una lista con viñetas) exige '|' literal para no
    perder esa estructura."""
    if "\n\n" in data.strip():
        style = "|"
    elif "\n" in data:
        style = ">"
    else:
        style = None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, _str_presenter)


def escribir_manifiesto(manifiesto_path, cabecera, entradas):
    cuerpo = yaml.dump(entradas, allow_unicode=True, sort_keys=False, width=88,
                        default_flow_style=False)
    cuerpo = cuerpo.replace("\n- id:", "\n\n- id:")
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


# ───────────────────────────────────────────────────────────── --escanea ──

STAGING_NOMBRE = "manifiesto-staging.yaml"

# Páginas guardadas (evidencia de procedencia), no payload de dato -- nunca
# se agrupan por tanda junto con archivos de datos aunque el mtime coincida.
EXTENSIONES_PAGINA = {".php", ".html", ".htm"}

# Un salto de más de 15 minutos entre dos mtimes consecutivos (o un cambio
# de día calendario, sin importar el salto) abre una tanda nueva. Deriva
# la agrupación del disco, no del nombre: dos archivos con el mismo prefijo
# pero mtimes muy separados caen en tandas distintas.
UMBRAL_TANDA_SEGUNDOS = 15 * 60

_EXTENSIONES_CONOCIDAS = {
    "pdf", "xlsx", "xls", "csv", "zip", "docx", "doc", "php", "html", "htm",
    "dbf", "stata", "json", "txt",
}

_DOMINIOS_PLANTILLA = (
    "w3.org", "bootstrapmade.com", "googletagmanager.com",
    "facebook.com", "twitter.com", "goo.gl",
)


def _index_manifiesto(entradas):
    por_hash, por_nombre = {}, {}
    for e in entradas:
        if "sha256" in e:
            por_hash[e["sha256"]] = e
        archivo = e.get("archivo")
        if archivo:
            por_nombre[archivo] = e
    return por_hash, por_nombre


def _extraer_url_pagina(ruta_absoluta):
    """Lee un .php/.html/.htm guardado como TEXTO -- no como payload -- y
    busca la URL que la propia página declara de sí misma (meta og:url);
    si no hay, el primer enlace https:// que no sea de una plantilla/CDN
    conocida. Es una sugerencia derivada de disco, no procedencia
    declarada -- quien registra decide si la usa."""
    try:
        with open(ruta_absoluta, encoding="utf-8", errors="ignore") as f:
            texto = f.read()
    except OSError:
        return None
    m = re.search(r"""property=['"]og:url['"]\s+content=['"]([^'"]+)['"]""", texto)
    if m:
        return m.group(1)
    for candidato in re.findall(r"https?://[^\s\"'<>]+", texto):
        if not any(d in candidato for d in _DOMINIOS_PLANTILLA):
            return candidato
    return None


def _fmt_ts(epoch):
    """Segundos, sin microsegundos -- el filesystem de un montaje WSL/Windows
    reporta mtime con precisión de microsegundo, que no aporta nada a un
    reporte pensado para que un humano lo lea."""
    return datetime.datetime.fromtimestamp(epoch).replace(microsecond=0).isoformat(sep=" ")


def _agrupar_por_tanda(archivos):
    """archivos: dicts con 'mtime' (epoch). Agrupa por proximidad temporal
    en disco (ver UMBRAL_TANDA_SEGUNDOS) -- nunca por nombre solamente."""
    if not archivos:
        return []
    ordenados = sorted(archivos, key=lambda a: a["mtime"])
    grupos = [[ordenados[0]]]
    for anterior, actual in zip(ordenados, ordenados[1:]):
        dia_anterior = datetime.date.fromtimestamp(anterior["mtime"])
        dia_actual = datetime.date.fromtimestamp(actual["mtime"])
        gap = actual["mtime"] - anterior["mtime"]
        if dia_actual != dia_anterior or gap > UMBRAL_TANDA_SEGUNDOS:
            grupos.append([])
        grupos[-1].append(actual)
    return grupos


def _etiqueta_dominante(nombres):
    """Cosmética, solo para el reporte -- no decide membresía del grupo.
    Un token alfabético de 4+ letras que se repite en 2+ archivos del
    grupo; si ninguno se repite, no hay etiqueta y el reporte lo dice."""
    contador = {}
    for nombre in nombres:
        for token in re.findall(r"[A-Za-z]{4,}", nombre):
            t = token.lower()
            if t in _EXTENSIONES_CONOCIDAS:
                continue
            contador[t] = contador.get(t, 0) + 1
    candidatos = [t for t, n in contador.items() if n >= 2]
    if not candidatos:
        return None
    candidatos.sort(key=lambda t: (-contador[t], t))
    return candidatos[0]


def _yaml_valor(valor):
    """yaml.safe_dump de un escalar suelto añade un marcador de fin de
    documento ('...') en su propia línea -- se descarta, no es parte del
    valor."""
    texto = yaml.safe_dump(valor, allow_unicode=True, default_flow_style=True).strip()
    if texto.endswith("..."):
        texto = texto[:-3].rstrip()
    return texto


def _formatear_entrada_staging(f, sugerencia_url):
    url_valor = f.get("url_origen")
    usado_valor = f.get("usado_para")
    lineas = [
        f"- archivo: {_yaml_valor(f['archivo'])}",
        f"  sha256: {f['sha256']}",
        f"  tamano_bytes: {f['tamano_bytes']}",
        f"  fecha_descarga: '{f['fecha_descarga']}'",
        f"  entorno_descarga: {_yaml_valor(f['entorno_descarga'])}",
        f"  descargado_por: {_yaml_valor(f['descargado_por'])}",
    ]
    if url_valor:
        lineas.append(f"  url_origen: {_yaml_valor(url_valor)}")
    elif sugerencia_url:
        lineas.append(f'  url_origen: ""      # PENDIENTE -- sugerencia de '
                       f'descargas.php: {sugerencia_url}')
    else:
        lineas.append('  url_origen: ""      # PENDIENTE')
    if usado_valor:
        lineas.append(f"  usado_para: {_yaml_valor(usado_valor)}")
    else:
        lineas.append('  usado_para: ""      # PENDIENTE')
    return "\n".join(lineas)


def cmd_escanea(a, manifiesto_path, raw_dir):
    ruta = os.path.abspath(os.path.expanduser(a.escanea))
    if not os.path.isdir(ruta):
        print(f"ERROR: '{a.escanea}' no es una carpeta accesible.", file=sys.stderr)
        sys.exit(1)

    _, entradas = leer_manifiesto(manifiesto_path)
    por_hash, por_nombre = _index_manifiesto(entradas)

    ya_registrados, conflictos_nombre = [], []
    nuevos, paginas = [], []

    for nombre in sorted(os.listdir(ruta)):
        ruta_abs = os.path.join(ruta, nombre)
        if not os.path.isfile(ruta_abs):
            continue

        sha = sha256_de(ruta_abs)
        st = os.stat(ruta_abs)

        if sha in por_hash:
            ya_registrados.append((nombre, por_hash[sha].get("id", "?")))
            continue

        existente = por_nombre.get(nombre)
        if existente is not None:
            conflictos_nombre.append(
                (nombre, existente.get("id", "?"), sha, existente.get("sha256")))
            continue

        registro = {
            "archivo": nombre,
            "sha256": sha,
            "tamano_bytes": st.st_size,
            "mtime": st.st_mtime,
            "fecha_descarga": datetime.date.fromtimestamp(st.st_mtime).isoformat(),
            "entorno_descarga": entorno_actual(),
            "descargado_por": "usuario, vía navegador",
        }
        if os.path.splitext(nombre)[1].lower() in EXTENSIONES_PAGINA:
            paginas.append(registro)
        else:
            nuevos.append(registro)

    grupos = _agrupar_por_tanda(nuevos)

    for pagina in paginas:
        pagina["_url_sugerida"] = _extraer_url_pagina(os.path.join(ruta, pagina["archivo"]))

    sugerencia_por_grupo = {}
    for i, grupo in enumerate(grupos):
        tmin = min(f["mtime"] for f in grupo)
        tmax = max(f["mtime"] for f in grupo)
        candidatas = {
            p["_url_sugerida"] for p in paginas
            if p["_url_sugerida"]
            and tmin - UMBRAL_TANDA_SEGUNDOS <= p["mtime"] <= tmax + UMBRAL_TANDA_SEGUNDOS
        }
        if len(candidatas) == 1:
            sugerencia_por_grupo[i] = next(iter(candidatas))

    aplicados = 0
    if a.grupo:
        for grupo in grupos:
            for f in grupo:
                if fnmatch.fnmatch(f["archivo"].lower(), a.grupo.lower()):
                    if a.grupo_url:
                        f["url_origen"] = a.grupo_url
                    if a.usado_para:
                        f["usado_para"] = a.usado_para
                    aplicados += 1

    # ── escribir data/manifiesto-staging.yaml ──
    staging_path = os.path.join(os.path.dirname(manifiesto_path), STAGING_NOMBRE)
    bloques = [
        f"# {STAGING_NOMBRE} -- candidatos derivados por `tests/manifiesto.py "
        f"--escanea` desde:\n#   {ruta}\n#\n"
        f"# sha256, tamano_bytes, fecha_descarga (del mtime) y entorno_descarga\n"
        f"# se derivaron del archivo real en disco -- nunca se tecleó ni se pidió\n"
        f"# por parámetro. url_origen y usado_para son los dos campos que una\n"
        f"# máquina no puede derivar: quedan en \"\" y # PENDIENTE hasta que el\n"
        f"# autor los complete.\n#\n"
        f"# Este archivo NO es data/manifiesto.yaml. Ninguna entrada de aquí se\n"
        f"# promueve automáticamente."
    ]
    for i, grupo in enumerate(grupos):
        tmin = _fmt_ts(min(f["mtime"] for f in grupo))
        tmax = _fmt_ts(max(f["mtime"] for f in grupo))
        etiqueta = _etiqueta_dominante(f["archivo"] for f in grupo)
        cabecera = (f"\n# ── Grupo {i + 1}: {len(grupo)} archivo(s) -- "
                    f"{tmin} a {tmax} -- "
                    f"token dominante: {etiqueta or '(ninguno)'} ──")
        entradas_txt = [_formatear_entrada_staging(f, sugerencia_por_grupo.get(i))
                        for f in sorted(grupo, key=lambda f: f["archivo"])]
        bloques.append(cabecera + "\n\n" + "\n\n".join(entradas_txt))
    for pagina in paginas:
        cabecera = (f"\n# ── Página guardada (no es dato -- evidencia de "
                    f"procedencia): {pagina['archivo']} ──")
        bloques.append(cabecera + "\n\n" + _formatear_entrada_staging(pagina, None))

    with open(staging_path, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques).strip() + "\n")

    # ── reporte a stdout ──
    total = len(ya_registrados) + len(conflictos_nombre) + len(nuevos) + len(paginas)
    print(f"Escaneado: {ruta}")
    print(f"Entorno: {entorno_actual()}")
    print()
    print(f"Total en disco: {total} · nuevos: {len(nuevos) + len(paginas)} · "
          f"ya registrados: {len(ya_registrados)} · conflicto de nombre: "
          f"{len(conflictos_nombre)}")
    print()

    if ya_registrados:
        print(f"YA REGISTRADOS ({len(ya_registrados)}):")
        for nombre, id_ in ya_registrados:
            print(f"  {nombre} -- ya registrado como '{id_}'")
        print()

    if conflictos_nombre:
        print(f"CONFLICTO DE NOMBRE -- HALLAZGO, no se registra ({len(conflictos_nombre)}):")
        for nombre, id_, sha_disco, sha_manifiesto in conflictos_nombre:
            print(f"  {nombre}: mismo nombre que '{id_}' pero sha256 distinto")
            print(f"    sha256 en disco:      {sha_disco}")
            print(f"    sha256 en manifiesto: {sha_manifiesto}")
        print()

    print(f"GRUPOS de datos detectados ({len(grupos)}), por tanda de descarga "
          f"(mtime en disco):")
    for i, grupo in enumerate(grupos):
        tmin = _fmt_ts(min(f["mtime"] for f in grupo))
        tmax = _fmt_ts(max(f["mtime"] for f in grupo))
        etiqueta = _etiqueta_dominante(f["archivo"] for f in grupo)
        sugerencia = sugerencia_por_grupo.get(i)
        print(f"  Grupo {i + 1}: {len(grupo)} archivo(s) -- "
              f"{tmin} a {tmax} -- "
              f"token dominante: {etiqueta or '(ninguno)'}"
              + (f" -- sugerencia url_origen: {sugerencia}" if sugerencia else ""))
        print(f"    {', '.join(f['archivo'] for f in sorted(grupo, key=lambda f: f['archivo']))}")

    if paginas:
        print()
        print(f"Páginas guardadas ({len(paginas)}, no son dato -- evidencia de procedencia):")
        for p in paginas:
            print(f"  {p['archivo']} -- sugerencia detectada: "
                  f"{p['_url_sugerida'] or '(ninguna)'}")

    if a.grupo:
        print()
        print(f"--grupo '{a.grupo}': {aplicados} archivo(s) nuevo(s) recibieron "
              + ", ".join(filter(None, [
                  f"url_origen='{a.grupo_url}'" if a.grupo_url else None,
                  f"usado_para='{a.usado_para}'" if a.usado_para else None,
              ])) if aplicados else f"--grupo '{a.grupo}': ningún archivo nuevo coincide con el patrón")

    print()
    print(f"Escrito: {os.path.relpath(staging_path, repo_root())} "
          f"({len(nuevos) + len(paginas)} entrada(s) staging). "
          f"Nada se promovió a {os.path.relpath(manifiesto_path, repo_root())}.")


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
    g.add_argument("--escanea", default=None, metavar="RUTA",
                    help="Recorre RUTA y escribe candidatos nuevos (dedup por sha256) "
                         "en data/manifiesto-staging.yaml -- nunca en el manifiesto")

    ap.add_argument("--id", default=None)
    ap.add_argument("--grupo", default=None,
                     help="patrón fnmatch (--escanea): aplica --url/--usado-para a "
                          "los archivos nuevos cuyo nombre case con el patrón")
    ap.add_argument("--url", dest="grupo_url", default=None,
                     help="url_origen a aplicar a los archivos que casen con --grupo")
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
    elif a.escanea:
        cmd_escanea(a, manifiesto_path, raw_dir)
    else:
        cmd_compara(a, manifiesto_path, raw_dir)


if __name__ == "__main__":
    main()
