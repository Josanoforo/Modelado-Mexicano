#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/manifiesto.py — procedencia de dato externo (data/manifiesto.yaml).

--registra   añade una entrada NUEVA para un archivo que ya está en data/raw/.
             sha256, tamaño y entorno_descarga se derivan del archivo real y
             del proceso en ejecución -- ninguno se teclea ni se pide por
             parámetro. No sobreescribe: un id que ya existe es error. Tampoco
             duplica por contenido: si el sha256 ya está en el manifiesto bajo
             OTRO id, aborta y dice cuál -- misma dedup que --escanea ya hacía,
             ahora simétrica (30/jul: su ausencia aquí es justo lo que dejó
             pasar dos entradas para el mismo PDF de ENCIG bajo dos ids, de
             dos sesiones que no se vieron).

--verifica   recomputa sha256 y tamaño del archivo que una entrada declara
             (campo `archivo`) y los compara contra lo que el manifiesto
             registra, resolviendo la raíz real por el campo `raiz` de la
             entrada (ausente = data_raw). Sin --id, verifica todas las
             entradas con payload. Un archivo ausente de su raíz se
             reporta AUSENTE -- no es un error del script, es un hecho
             sobre el entorno (el payload nunca se commitea; puede faltar
             sin que nada esté roto). Cada línea declara la raíz junto al
             id ([data_raw], [descargas_mx], [downloads]...) y el resumen
             final tabula por raíz SIN COLAPSAR -- un AUSENTE en
             `downloads` no es el mismo hecho que un AUSENTE en
             `data_raw`, y una raíz que este entorno no tiene configurada
             en data/raices.local.yaml se reporta aparte, no como AUSENTE.

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

RAÍCES (30/jul, corrección de diseño): hay tres, nunca dos.
    data_raw      repo/data/raw/ -- lo que baja un agente. Integrada:
                  se resuelve por código, nunca por archivo.
    descargas_mx  carpeta de descargas curada por el autor.
    downloads     destino por defecto del navegador -- NO es una carpeta
                  de datos: tiene archivos ajenos al proyecto.
Las rutas reales de descargas_mx/downloads (y cualquier otra que se
declare) viven en data/raices.local.yaml, gitignorado -- cada máquina
define las suyas; una ruta literal nunca se commitea, ni ahí (ese archivo
no se versiona) ni en una entrada del manifiesto (campo `raiz`: el NOMBRE
de la raíz, nunca la ruta). Las 53 entradas de payload anteriores a este
campo no tienen `raiz` -- su ausencia SIGNIFICA data_raw; no se les
migra un valor retroactivo que nadie declaró entonces.

--escanea   recorre RECURSIVAMENTE una RAÍZ POR NOMBRE (nunca una ruta --
             ver arriba); `archivo` es la ruta relativa a la raíz, con
             subcarpeta si la hay ('Descargas Manuales/x.dta'), misma
             convención que tests/corpus.py -- desde ADR-310. Y,
             para cada archivo que no esté ya en data/manifiesto.yaml
             (dedup por sha256, no por nombre),
             deriva archivo/raiz/sha256/tamano_bytes/fecha_descarga (del
             mtime)/entorno_descarga/descargado_por y escribe una entrada
             STAGING en data/manifiesto-staging.yaml -- nunca en el
             manifiesto. `raiz` es el nombre de la raíz escaneada; el
             reporte también lo declara siempre, por nombre -- un staging
             que no dice de dónde salió es el mismo defecto de procedencia,
             una capa más abajo. Sobre `downloads` EXIGE --grupo o
             --grupo-n (si no, aborta): esa raíz no es de datos y un
             escaneo completo mete ruido que alguien limpiaría a mano.
             Sobre data_raw/descargas_mx el escaneo completo sigue
             permitido. No descarga nada, no sobreescribe nada y no abre
             ningún payload: hashear y hacer stat no es abrir; leer como
             texto un .php/.html guardado (para sugerir url_origen)
             tampoco toca ningún portal.

             ALCANCE DE DATO en raíces no curadas (hoy solo `downloads`,
             corrección de MAP-1b -- forense/notas/2026-08-06-map1b-censo-
             raices.md): antes de esta corrección, --grupo/--grupo-n exigido
             sobre `downloads` acotaba solo a qué archivos se les asignaba
             url_origen/usado_para -- el recorrido SÍ hasheaba y staged todo
             el contenido de la carpeta, extensión aparte, incluidos
             archivos personales ajenos al proyecto (fotos, exports de
             WhatsApp/Instagram, respaldos completos de Google Takeout de
             decenas de GiB). Ahora, sobre una raíz que exige --grupo, un
             archivo cuya extensión no está en EXTENSIONES_DATO_RAICES_NO_CURADAS
             (el mismo filtro de 8 extensiones que el censo MAP-1b declaró y
             aplicó a mano) se excluye ANTES de leerlo/hashearlo -- no
             aparece en staging, no se cuenta como "nuevo", y el reporte
             solo declara cuántos y con qué extensiones, nunca sus nombres
             (mismo criterio que MAP-1b usó para no transcribir ruido
             personal). `data_raw`/`descargas_mx` no llevan este filtro --
             son carpetas curadas de datos del proyecto, sin el riesgo que
             `downloads` (destino por defecto del navegador) sí tiene.

             url_origen y usado_para son los
             únicos dos campos que una máquina no deriva -- quedan en ""
             con comentario # PENDIENTE, salvo que --grupo/--grupo-n +
             --url/--usado-para se los asignen a un lote (--grupo-n
             selecciona una tanda ENTERA por su número, sin depender del
             nombre; --grupo, un patrón fnmatch, acota un subconjunto --
             solo o dentro de una tanda ya elegida con --grupo-n).
             Un hash nuevo con un nombre que ya está registrado no se
             registra: se reporta aparte como hallazgo (mismo nombre,
             contenido distinto), no se resuelve solo. Agrupa por tanda de
             descarga (proximidad de mtime en disco, nunca solo por nombre;
             un cambio de día calendario o un salto grande siempre abre
             tanda nueva) para que el reporte no sea una lista de N líneas.
             Además del campo `url_origen` (con su comentario # PENDIENTE),
             cada entrada staging trae `url_origen_sugerida` -- la misma
             sugerencia pero en un campo YAML real, no solo en un comentario,
             para que --promueve pueda leerla sin re-escanear la carpeta.

--promueve   mueve entradas de data/manifiesto-staging.yaml a
             data/manifiesto.yaml aunque url_origen no esté confirmada por
             el autor. CORRECCIÓN DE DISEÑO (30/jul): bloquear el registro
             por dos campos que una máquina no deriva (url_origen,
             usado_para) dejaba archivos con sha256/tamaño reales
             *invisibles* a --verifica -- un archivo sin registrar no se
             audita. Un archivo registrado con un campo marcado como no
             confirmado sí se audita: por eso el manifiesto existe. Lo único
             irrecuperable es la ausencia de sha256/tamano_bytes -- eso sí
             bloquea la promoción de esa entrada; una URL no confirmada no.
             Escribe url_origen (la sugerencia derivada de una página
             guardada si la hay, el valor que --escanea --grupo/--url le
             haya asignado, o "no determinada" si no hay ninguna de las
             dos) junto con `url_origen_procedencia`, que declara de dónde
             salió y dice explícitamente NO CONFIRMADA POR EL AUTOR --
             nunca se calla ese hecho ni se hace pasar la sugerencia por
             procedencia declarada. `usado_para` deja de bloquear: si
             --escanea/--grupo no le asignó uno, se registra como "sin uso
             asignado — registro de inventario". Una página guardada
             (.php/.html/.htm) nunca se promueve -- no es dato, es rastro
             de procedencia. Lo que no se promueve (por ser página, por
             faltarle hash/tamaño, o por quedar fuera de un --grupo) se
             reescribe en data/manifiesto-staging.yaml; lo que sí se
             promovió sale de staging.

Única dependencia externa: PyYAML.
"""
import argparse
import datetime
import fnmatch
import hashlib
import os
import platform
import re
import sys

import yaml


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rutas(root):
    return (os.path.join(root, "data", "manifiesto.yaml"),
            os.path.join(root, "data", "raw"))


RAIZ_INTEGRADA = "data_raw"  # resuelta por código (rutas()); nunca por archivo


def raices_configuradas(root):
    """Mapa nombre->ruta real de raíces EXTERNAS al repo (todo salvo
    RAIZ_INTEGRADA). Vive en data/raices.local.yaml, gitignorado -- cada
    máquina declara sus propias rutas; una ruta literal nunca se commitea,
    ni aquí ni en una entrada del manifiesto (campo `raiz`: el NOMBRE,
    nunca la ruta)."""
    ruta_config = os.path.join(root, "data", "raices.local.yaml")
    if not os.path.exists(ruta_config):
        return {}
    with open(ruta_config, encoding="utf-8") as f:
        datos = yaml.safe_load(f) or {}
    return {k: v for k, v in datos.items() if k != RAIZ_INTEGRADA}


def resolver_raiz(nombre, root, raw_dir):
    """None si `nombre` no es RAIZ_INTEGRADA ni está en
    data/raices.local.yaml -- este entorno no la tiene configurada (puede
    ser válida en otra máquina; no es un error del manifiesto)."""
    if nombre == RAIZ_INTEGRADA:
        return raw_dir
    return raices_configuradas(root).get(nombre)


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
    """Derivado del proceso en ejecución -- nunca pedido por parámetro.

    No incluye `host` hacia adelante (ENCARGO MT-mantenimiento, 5/ago/2026,
    ADR-62): ~190 entradas ya escritas en data/manifiesto.yaml exponen
    hostname bajo la versión anterior de esta función y se quedan tal cual
    -- append-only, no se reescriben retroactivamente. SO y Python se
    conservan."""
    return (f"{platform.system()} {platform.release()} ({platform.machine()}) "
            f"· Python {platform.python_version()}")


def buscar(entradas, id_):
    for e in entradas:
        if e.get("id") == id_:
            return e
    return None


def _id_unico(valor, comando):
    """--id ahora acumula (action='append') para que --verifica pueda recibir
    varios sin que argparse se quede callado con el último y descarte el
    resto (ENCARGO MT-mantenimiento, 5/ago/2026; forense/hallazgos.md
    4/ago). Los comandos de un solo id (--registra, --compara) no tienen uso
    para más de uno -- fallan ruidoso en vez de tomar el último en silencio,
    que es exactamente el defecto que este helper cierra."""
    if valor is None:
        return None
    if len(valor) > 1:
        print(f"ERROR: {comando} no admite --id repetido (recibió {len(valor)}): "
              f"{', '.join(valor)}. Cada invocación de {comando} opera sobre un "
              f"solo id.", file=sys.stderr)
        sys.exit(1)
    return valor[0]


# ───────────────────────────────────────────────────────────── --registra ──

def cmd_registra(a, manifiesto_path, raw_dir):
    a.id = _id_unico(a.id, "--registra")
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

    sha = sha256_de(ruta_absoluta)
    por_hash, _ = _index_manifiesto(entradas)
    if sha in por_hash:
        print(f"ERROR: este archivo ya está registrado -- mismo sha256 que la "
              f"entrada '{por_hash[sha].get('id', '?')}' (archivo "
              f"'{por_hash[sha].get('archivo', '?')}'). --escanea dedupica por "
              f"hash; --registra hace lo mismo desde aquí -- no escribe una "
              f"segunda entrada para el mismo contenido bajo un id distinto. Si "
              f"el archivo cambió de verdad, es un id nuevo para un sha256 "
              f"nuevo, no este caso.", file=sys.stderr)
        sys.exit(1)

    entrada = {
        "id": a.id,
        "usado_para": a.usado_para,
        "url_origen": a.url_origen,
        "fecha_descarga": a.fecha_descarga or datetime.date.today().isoformat(),
        "descargado_por": a.descargado_por,
        "archivo": a.archivo,
        "sha256": sha,
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
    root = os.path.dirname(os.path.dirname(manifiesto_path))
    _, entradas = leer_manifiesto(manifiesto_path)
    con_payload = [e for e in entradas if "sha256" in e]

    if a.id:
        # --id ahora es action='append': varios --id en la misma invocación
        # verifican TODOS, no solo el último (defecto documentado en
        # forense/hallazgos.md 4/ago -- TANDA-4 de la maestra lo esquivó a
        # mano). Un id pedido que no existe es error explícito y ruidoso, no
        # un silencio parcial: se listan TODOS los faltantes antes de salir,
        # no solo el primero.
        ids_pedidos = list(dict.fromkeys(a.id))  # dedup preservando orden
        objetivo = []
        faltantes = []
        for id_pedido in ids_pedidos:
            coincidencias = [e for e in con_payload if e.get("id") == id_pedido]
            if not coincidencias:
                existe_sin_payload = buscar(entradas, id_pedido) is not None
                razon = ("existe pero no tiene payload (sha256) -- es una entrada de "
                          "nota/documentación" if existe_sin_payload else "no existe")
                faltantes.append((id_pedido, razon))
            else:
                objetivo.extend(coincidencias)
        if faltantes:
            for id_pedido, razon in faltantes:
                print(f"ERROR: id '{id_pedido}' {razon} en el manifiesto.", file=sys.stderr)
            sys.exit(1)
    else:
        objetivo = con_payload

    print(f"Entorno de verificación: {entorno_actual()}")
    print()

    exit_code = 0
    # Tres estados por raíz, sin colapsar -- AUSENTE en 'downloads' no es lo
    # mismo que AUSENTE en 'data_raw', y una tabla que solo dijera "AUSENTE"
    # los volvería indistinguibles.
    por_raiz = {}
    for entrada in objetivo:
        id_ = entrada.get("id", "?")
        archivo = entrada.get("archivo")
        nombre_raiz = entrada.get("raiz", RAIZ_INTEGRADA)
        tally = por_raiz.setdefault(nombre_raiz, {"coincide": 0, "no_coincide": 0,
                                                     "ausente": 0, "sin_raiz": 0})
        if not archivo:
            print(f"{id_} [{nombre_raiz}]: SIN CAMPO 'archivo' en el manifiesto -- "
                  f"no se puede localizar el payload (omitido, no cuenta como falla)")
            continue

        base_dir = resolver_raiz(nombre_raiz, root, raw_dir)
        if base_dir is None:
            tally["sin_raiz"] += 1
            print(f"{id_} [{nombre_raiz}]: RAÍZ NO CONFIGURADA -- este entorno no "
                  f"define '{nombre_raiz}' en data/raices.local.yaml; no se puede "
                  f"verificar (no es un error del manifiesto, puede ser válida en "
                  f"otra máquina)")
            continue

        ruta = os.path.join(base_dir, archivo)
        if not os.path.exists(ruta):
            tally["ausente"] += 1
            print(f"{id_} [{nombre_raiz}]: AUSENTE -- {archivo} no está en la raíz "
                  f"'{nombre_raiz}' (no es un error: el payload no se commitea)")
            continue

        sha_real = sha256_de(ruta)
        tam_real = os.path.getsize(ruta)
        sha_ok = sha_real == entrada.get("sha256")
        tam_ok = tam_real == entrada.get("tamano_bytes")

        if sha_ok and tam_ok:
            tally["coincide"] += 1
            print(f"{id_} [{nombre_raiz}]: COINCIDE -- sha256 y tamaño "
                  f"({tam_real} bytes) verificados contra data/manifiesto.yaml")
        else:
            tally["no_coincide"] += 1
            exit_code = 1
            print(f"{id_} [{nombre_raiz}]: NO COINCIDE")
            if not sha_ok:
                print(f"    sha256 manifiesto: {entrada.get('sha256')}")
                print(f"    sha256 real:       {sha_real}")
            if not tam_ok:
                print(f"    tamano_bytes manifiesto: {entrada.get('tamano_bytes')}")
                print(f"    tamano_bytes real:       {tam_real}")

    print()
    print("Por raíz (sin colapsar):")
    for nombre_raiz in sorted(por_raiz):
        t = por_raiz[nombre_raiz]
        print(f"  {nombre_raiz}: coincide={t['coincide']} · "
              f"no_coincide={t['no_coincide']} · ausente={t['ausente']} · "
              f"sin_configurar={t['sin_raiz']}")

    derivadas = [e for e in entradas if e.get("url_origen_procedencia")]
    print()
    print(f"Procedencia derivada, NO confirmada por el autor: {len(derivadas)} "
          f"entrada(s) de {len(entradas)} en el manifiesto (cuenta el manifiesto "
          f"completo, no solo lo verificado arriba):")
    for e in derivadas:
        print(f"  {e.get('id', '?')} [{e.get('raiz', RAIZ_INTEGRADA)}] "
              f"({e.get('archivo', '?')}): {e['url_origen_procedencia']}")

    sys.exit(exit_code)


# ───────────────────────────────────────────────────────────── --escanea ──

STAGING_NOMBRE = "manifiesto-staging.yaml"

# Páginas guardadas (evidencia de procedencia), no payload de dato -- nunca
# se agrupan por tanda junto con archivos de datos aunque el mtime coincida.
EXTENSIONES_PAGINA = {".php", ".html", ".htm"}

# Alcance de dato para raíces NO curadas (ver RAICES_QUE_EXIGEN_GRUPO): mismo
# filtro de 8 extensiones que ENCARGO MAP-1b declaró y aplicó a mano el
# 2026-08-06 (forense/notas/2026-08-06-map1b-censo-raices.md, PASO 2) al
# censar 'downloads' -- ahí se dejaron 1763 de 2141 archivos fuera del
# filtro, dominados por contenido ajeno al proyecto (.md/.docx/.png/.html
# personales) y, más grave, 37 archivos `takeout-*` de Google (52 GiB,
# exportación personal completa de una cuenta). Esa nota excluyó esos 37 de
# HASHEARSE explícitamente ("no se hashean -- hacerlo habría dominado el
# tiempo de corrida por valor forense nulo") -- una protección de privacidad
# real que ese censo aplicó a mano, fuera del repo, y que --escanea nunca
# heredó: antes de este filtro, --grupo/--grupo-n solo acotaba a qué
# archivos se les asignaba url_origen/usado_para (línea ~683 más abajo) --
# el barrido de sha256_de() sobre CADA archivo de 'downloads', incluidos
# esos 37 respaldos personales, ocurría de todas formas, antes de cualquier
# filtro. La corrección de alcance: el filtro de extensión decide qué se
# LEE, no solo qué se etiqueta -- se aplica previo a recorrer el barrido
# (antes de sha256_de), no después.
EXTENSIONES_DATO_RAICES_NO_CURADAS = {
    ".zip", ".csv", ".dta", ".dbf", ".xlsx", ".pdf", ".sav", ".xml",
}

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
    valor.

    `width` grande a propósito (MAESTRA36-A1, 2026-09-02): sus siete
    llamadores arman a mano una línea `  clave: <valor>` de
    data/manifiesto-staging.yaml, y el ancho por defecto de safe_dump (80)
    parte un escalar largo en varias líneas con sangría de DOS espacios --
    la misma que la clave. El resultado es YAML inválido: la continuación
    se lee como una clave nueva sin ':'. Medido contra 9af8407 con un
    --url de 105 caracteres: `--escanea` escribía el staging y `--promueve`
    reventaba después con ScannerError. El manifiesto real nunca tuvo este
    defecto porque escribir_manifiesto usa yaml.dump sobre la estructura
    entera, que sangra las continuaciones más que la clave.
    """
    texto = yaml.safe_dump(valor, allow_unicode=True, default_flow_style=True,
                            width=10 ** 9).strip()
    if texto.endswith("..."):
        texto = texto[:-3].rstrip()
    return texto


def _formatear_entrada_staging(f, sugerencia_url):
    url_valor = f.get("url_origen")
    usado_valor = f.get("usado_para")
    lineas = [
        f"- archivo: {_yaml_valor(f['archivo'])}",
        f"  raiz: {_yaml_valor(f.get('raiz', RAIZ_INTEGRADA))}",
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
    # Mismo dato que el comentario de arriba, pero en un campo YAML real --
    # --promueve lee esto; un comentario lo pierde el parser.
    lineas.append(f"  url_origen_sugerida: {_yaml_valor(sugerencia_url or '')}")
    if usado_valor:
        lineas.append(f"  usado_para: {_yaml_valor(usado_valor)}")
    else:
        lineas.append('  usado_para: ""      # PENDIENTE')
    return "\n".join(lineas)


RAICES_QUE_EXIGEN_GRUPO = {"downloads"}


def _archivos_recursivos(ruta):
    """Rutas relativas a `ruta` de TODOS los archivos del árbol, no solo del
    nivel superior. Misma convención que tests/corpus.py (os.walk +
    normpath(relpath)) -- que es la que ya tienen las 49 entradas
    'Descargas Manuales/...' del manifiesto desde la corrección T2 del
    18/ago/2026, así que el campo `archivo` que sale de aquí y el que
    corpus.py compara son el mismo objeto.

    Antes de ADR-310 esto era os.listdir + isfile: una subcarpeta entera
    quedaba invisible para --escanea. Medido por MAESTRA36-A1 (P0,
    2026-09-02) sobre la raíz descargas_mx: 224 archivos en el árbol, de
    los que os.listdir veía 148 -- los 76 de 'Descargas Manuales/' no eran
    ni "nuevos" ni "ya registrados", simplemente no existían para este
    comando, mientras corpus.py sí los recorría y los contaba huérfanos.
    Esa asimetría entre los dos recorridos es lo que hizo que a mesa se le
    volvieran a pedir descargas que ya había hecho.

    os.walk no sigue enlaces simbólicos a directorios (followlinks=False):
    un symlink autorreferente no abre un bucle aquí.
    """
    for dirpath, _dirnames, filenames in os.walk(ruta):
        for fn in filenames:
            ruta_abs = os.path.join(dirpath, fn)
            if not os.path.isfile(ruta_abs):
                continue
            yield os.path.normpath(os.path.relpath(ruta_abs, ruta))


def cmd_escanea(a, manifiesto_path, raw_dir):
    root = os.path.dirname(os.path.dirname(manifiesto_path))
    nombre_raiz = a.escanea
    ruta = resolver_raiz(nombre_raiz, root, raw_dir)
    if ruta is None:
        disponibles = [RAIZ_INTEGRADA] + sorted(raices_configuradas(root))
        print(f"ERROR: raíz '{nombre_raiz}' no configurada. --escanea recibe un "
              f"NOMBRE de raíz, nunca una ruta. '{RAIZ_INTEGRADA}' es integrada; "
              f"el resto se declara en data/raices.local.yaml (gitignorado -- cada "
              f"máquina define sus propias rutas). Disponibles aquí: "
              f"{', '.join(disponibles)}.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(ruta):
        print(f"ERROR: la raíz '{nombre_raiz}' apunta a una ruta que no es una "
              f"carpeta accesible en esta máquina.", file=sys.stderr)
        sys.exit(1)
    if nombre_raiz in RAICES_QUE_EXIGEN_GRUPO and not (a.grupo or a.grupo_n is not None):
        print(f"ERROR: --escanea sobre la raíz '{nombre_raiz}' exige --grupo o "
              f"--grupo-n. No es una carpeta de datos del proyecto -- tiene "
              f"archivos ajenos, y un escaneo completo metería ruido al staging "
              f"que alguien tendría que limpiar a mano, que es justo el trabajo "
              f"que este comando existe para quitar.", file=sys.stderr)
        sys.exit(1)

    _, entradas = leer_manifiesto(manifiesto_path)
    por_hash, por_nombre = _index_manifiesto(entradas)

    ya_registrados, conflictos_nombre = [], []
    nuevos, paginas = [], []
    fuera_de_alcance = []

    for nombre in sorted(_archivos_recursivos(ruta)):
        ruta_abs = os.path.join(ruta, nombre)

        extension = os.path.splitext(nombre)[1].lower()
        if (nombre_raiz in RAICES_QUE_EXIGEN_GRUPO
                and extension not in EXTENSIONES_DATO_RAICES_NO_CURADAS
                and extension not in EXTENSIONES_PAGINA):
            # Riesgo de privacidad (MAP-1b, 2026-08-06): 'downloads' no es
            # una carpeta de datos, tiene archivos ajenos al proyecto -- se
            # excluye ANTES de leer/hashear, no solo antes de etiquetar.
            fuera_de_alcance.append(nombre)
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
            "raiz": nombre_raiz,
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
    if a.grupo or a.grupo_n is not None:
        if a.grupo_n is not None:
            if not (1 <= a.grupo_n <= len(grupos)):
                print(f"ERROR: --grupo-n {a.grupo_n} fuera de rango -- hay "
                      f"{len(grupos)} tanda(s) detectada(s).", file=sys.stderr)
                sys.exit(1)
            candidatos_tandas = [grupos[a.grupo_n - 1]]
        else:
            candidatos_tandas = grupos
        for grupo in candidatos_tandas:
            for f in grupo:
                if a.grupo and not fnmatch.fnmatch(f["archivo"].lower(), a.grupo.lower()):
                    continue
                if a.grupo_url:
                    f["url_origen"] = a.grupo_url
                if a.usado_para:
                    f["usado_para"] = a.usado_para
                aplicados += 1

    # ── escribir data/manifiesto-staging.yaml ──
    # Fusiona, no reemplaza: con tres raíces, escanear 'downloads' hoy no
    # puede borrar lo que 'descargas_mx' dejó staged ayer. Lo de esta
    # corrida reemplaza SOLO las entradas de la raíz que se está escaneando
    # (una tanda vieja de la MISMA raíz sí debe refrescarse); lo de otras
    # raíces se preserva tal cual, en un bloque aparte (sin mtime -- no se
    # re-escanea su disco -- así que no se reconstruye su agrupación).
    staging_path = os.path.join(os.path.dirname(manifiesto_path), STAGING_NOMBRE)
    _, staging_previo = leer_manifiesto(staging_path)
    de_otras_raices = [e for e in staging_previo
                       if e.get("raiz", RAIZ_INTEGRADA) != nombre_raiz]

    bloques = [
        f"# {STAGING_NOMBRE} -- candidatos derivados por `tests/manifiesto.py "
        f"--escanea`, fusionados por raíz (última corrida por raíz reemplaza "
        f"solo esa raíz).\n#\n"
        f"# sha256, tamano_bytes, fecha_descarga (del mtime) y entorno_descarga\n"
        f"# se derivaron del archivo real en disco -- nunca se tecleó ni se pidió\n"
        f"# por parámetro. url_origen y usado_para son los dos campos que una\n"
        f"# máquina no puede derivar: quedan en \"\" y # PENDIENTE hasta que el\n"
        f"# autor los complete. `raiz` es el NOMBRE de la raíz -- la ruta real\n"
        f"# vive en data/raices.local.yaml, gitignorado, nunca aquí.\n#\n"
        f"# Este archivo NO es data/manifiesto.yaml. Ninguna entrada de aquí se\n"
        f"# promueve automáticamente."
    ]
    bloques.append(f"\n# ══ Raíz '{nombre_raiz}' -- corrida actual ══")
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

    if de_otras_raices:
        bloques.append(f"\n# ══ Preservado de otra(s) raíz(ces) -- de una corrida "
                        f"anterior, no de esta ══")
        entradas_txt = [_formatear_entrada_staging(e, e.get("url_origen_sugerida"))
                        for e in sorted(de_otras_raices,
                                        key=lambda e: (e.get("raiz", RAIZ_INTEGRADA), e["archivo"]))]
        bloques.append("\n\n".join(entradas_txt))

    with open(staging_path, "w", encoding="utf-8") as f:
        f.write("\n".join(bloques).strip() + "\n")

    # ── reporte a stdout ──
    total = len(ya_registrados) + len(conflictos_nombre) + len(nuevos) + len(paginas) + len(fuera_de_alcance)
    print(f"Escaneado: raíz '{nombre_raiz}' ({ruta})")
    print(f"Entorno: {entorno_actual()}")
    print()
    print(f"Total en disco: {total} · nuevos: {len(nuevos) + len(paginas)} · "
          f"ya registrados: {len(ya_registrados)} · conflicto de nombre: "
          f"{len(conflictos_nombre)} · fuera de alcance de dato: {len(fuera_de_alcance)}")
    print()

    if fuera_de_alcance:
        extensiones_vistas = sorted({os.path.splitext(n)[1].lower() or "(sin extensión)" for n in fuera_de_alcance})
        print(f"FUERA DE ALCANCE DE DATO ({len(fuera_de_alcance)}) -- ni leídos ni hasheados, "
              f"riesgo de privacidad (MAP-1b): extensión ajena al filtro de '{nombre_raiz}' "
              f"({sorted(EXTENSIONES_DATO_RAICES_NO_CURADAS)}). No se transcriben los nombres "
              f"aquí (pueden ser archivos personales ajenos al proyecto, mismo criterio que "
              f"forense/notas/2026-08-06-map1b-censo-raices.md aplicó a los 28 grupos de ruido "
              f"personal). Extensiones distintas vistas: {extensiones_vistas}")
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

    if a.grupo or a.grupo_n is not None:
        print()
        descriptor = " + ".join(filter(None, [
            f"tanda {a.grupo_n}" if a.grupo_n is not None else None,
            f"patrón '{a.grupo}'" if a.grupo else None,
        ]))
        if aplicados:
            print(f"--grupo-n/--grupo ({descriptor}): {aplicados} archivo(s) nuevo(s) "
                  f"recibieron " + ", ".join(filter(None, [
                      f"url_origen='{a.grupo_url}'" if a.grupo_url else None,
                      f"usado_para='{a.usado_para}'" if a.usado_para else None,
                  ])))
        else:
            print(f"--grupo-n/--grupo ({descriptor}): ningún archivo nuevo coincide")

    if de_otras_raices:
        print()
        print(f"Preservadas {len(de_otras_raices)} entrada(s) de otra(s) raíz(ces) "
              f"(de una corrida anterior de --escanea, no de esta):")
        por_raiz_previa = {}
        for e in de_otras_raices:
            por_raiz_previa.setdefault(e.get("raiz", RAIZ_INTEGRADA), 0)
            por_raiz_previa[e.get("raiz", RAIZ_INTEGRADA)] += 1
        for r in sorted(por_raiz_previa):
            print(f"  {r}: {por_raiz_previa[r]}")

    print()
    print(f"Escrito: {os.path.relpath(staging_path, repo_root())} "
          f"({len(nuevos) + len(paginas)} entrada(s) staging de la raíz "
          f"'{nombre_raiz}' + {len(de_otras_raices)} preservada(s) de otras). "
          f"Nada se promovió a {os.path.relpath(manifiesto_path, repo_root())}.")


# ───────────────────────────────────────────────────────────── --promueve ──

def _derivar_id(nombre_archivo, ids_existentes):
    """Slug mecánico del nombre de archivo -- nunca tecleado. Si colisiona
    con un id ya existente (u otro derivado en el mismo lote), se
    desambigua con un sufijo numérico, nunca sobreescribiendo.

    Del BASENAME, no de la ruta (MAESTRA36-A1, 2026-09-02): desde ADR-310
    `archivo` puede traer subcarpeta, y slugificar la ruta entera daría
    ids como 'descargas_manuales_ingresostributarios'. Las 49 entradas
    con prefijo 'Descargas Manuales/' que ya existen derivan todas su id
    del basename ('mex_2010_iepep_v01_m_v01_a_puf', no
    'descargas_manuales_mex_2010_...'), así que tomar la ruta entera
    habría abierto dos convenciones de id en la misma raíz. La colisión
    entre dos basenames iguales en carpetas distintas la resuelve el
    sufijo numérico de abajo, que ya existía.
    """
    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    slug = re.sub(r"[^a-z0-9]+", "_", base.lower()).strip("_")
    slug = re.sub(r"_+", "_", slug) or "archivo"
    candidato = slug
    n = 2
    while candidato in ids_existentes:
        candidato = f"{slug}_{n}"
        n += 1
    return candidato


def _reescribir_staging_restante(staging_path, restantes):
    """Tras --promueve, staging solo debe listar lo que sigue sin estar en
    el manifiesto: páginas guardadas, entradas sin hash/tamaño, o lo que
    quedó fuera de un --grupo. No hay mtime disponible aquí (no se
    re-escanea el disco), así que no se reconstruye la agrupación por
    tanda -- una lista plana es honesta con lo que este paso sí sabe."""
    if not restantes:
        with open(staging_path, "w", encoding="utf-8") as f:
            f.write(f"# {STAGING_NOMBRE} -- vacío: no quedan candidatos sin "
                     f"promover a data/manifiesto.yaml.\n")
        return
    cabecera = (
        f"# {STAGING_NOMBRE} -- candidatos que --promueve dejó sin promover\n"
        f"# (página guardada -- no es dato --, hash/tamaño faltante, o fuera\n"
        f"# del --grupo de la última corrida). url_origen y usado_para siguen\n"
        f"# siendo los dos campos que una máquina no deriva."
    )
    entradas_txt = [_formatear_entrada_staging(e, e.get("url_origen_sugerida"))
                     for e in sorted(restantes, key=lambda e: e["archivo"])]
    with open(staging_path, "w", encoding="utf-8") as f:
        f.write(cabecera + "\n\n" + "\n\n".join(entradas_txt) + "\n")


def cmd_promueve(a, manifiesto_path, raw_dir):
    staging_path = os.path.join(os.path.dirname(manifiesto_path), STAGING_NOMBRE)
    if not os.path.exists(staging_path):
        print(f"ERROR: no existe {os.path.relpath(staging_path, repo_root())} -- "
              f"nada que promover. Corre --escanea primero.", file=sys.stderr)
        sys.exit(1)

    _, staging_entradas = leer_manifiesto(staging_path)
    if not staging_entradas:
        print(f"{os.path.relpath(staging_path, repo_root())} no tiene candidatos "
              f"pendientes. Nada que promover.")
        return

    cabecera, entradas = leer_manifiesto(manifiesto_path)
    por_hash, _ = _index_manifiesto(entradas)
    ids_existentes = {e.get("id") for e in entradas if e.get("id")}

    if a.grupo:
        objetivo = [e for e in staging_entradas
                    if fnmatch.fnmatch(e["archivo"].lower(), a.grupo.lower())]
        fuera_de_grupo = [e for e in staging_entradas if e not in objetivo]
    else:
        objetivo = list(staging_entradas)
        fuera_de_grupo = []

    promovidas, no_promovidas, restantes = [], [], list(fuera_de_grupo)

    for e in objetivo:
        ext = os.path.splitext(e["archivo"])[1].lower()
        if ext in EXTENSIONES_PAGINA:
            no_promovidas.append((e, "página guardada, no es dato -- no se promueve"))
            restantes.append(e)
            continue

        if e.get("sha256") in por_hash:
            no_promovidas.append(
                (e, f"ya registrado externamente como "
                    f"'{por_hash[e['sha256']].get('id', '?')}' -- no se duplica"))
            continue

        if not e.get("sha256") or not e.get("tamano_bytes"):
            no_promovidas.append(
                (e, "falta sha256 o tamano_bytes -- irrecuperable, no se promueve"))
            restantes.append(e)
            continue

        url_valor = e.get("url_origen") or ""
        sugerida = e.get("url_origen_sugerida") or ""
        if url_valor and sugerida and url_valor == sugerida:
            procedencia = "derivada de descargas.php por --escanea, NO confirmada por el autor"
        elif url_valor:
            procedencia = "asignada vía --grupo/--url en --escanea, NO confirmada por el autor"
        elif sugerida:
            url_valor = sugerida
            procedencia = "derivada de descargas.php por --escanea, NO confirmada por el autor"
        else:
            url_valor = "no determinada"
            procedencia = "no derivada -- --escanea no encontró sugerencia, NO confirmada por el autor"

        usado_valor = e.get("usado_para") or "sin uso asignado — registro de inventario"

        id_ = _derivar_id(e["archivo"], ids_existentes)
        ids_existentes.add(id_)

        nueva = {
            "id": id_,
            "usado_para": usado_valor,
            "url_origen": url_valor,
            "url_origen_procedencia": procedencia,
            "fecha_descarga": e["fecha_descarga"],
            "descargado_por": e["descargado_por"],
            "archivo": e["archivo"],
            "raiz": e.get("raiz", RAIZ_INTEGRADA),
            "sha256": e["sha256"],
            "tamano_bytes": e["tamano_bytes"],
            "entorno_descarga": e["entorno_descarga"],
        }
        entradas.append(nueva)
        por_hash[nueva["sha256"]] = nueva
        promovidas.append(nueva)

    escribir_manifiesto(manifiesto_path, cabecera, entradas)
    _reescribir_staging_restante(staging_path, restantes)

    print(f"Promovidas {len(promovidas)} entrada(s) a "
          f"{os.path.relpath(manifiesto_path, repo_root())}:")
    for n in promovidas:
        print(f"  {n['id']} <- {n['archivo']} [{n['raiz']}]")
        print(f"    url_origen: {n['url_origen']}")
        print(f"    url_origen_procedencia: {n['url_origen_procedencia']}")
        print(f"    usado_para: {n['usado_para']}")

    if no_promovidas:
        print()
        print(f"No promovidas ({len(no_promovidas)}):")
        for e, razon in no_promovidas:
            print(f"  {e['archivo']}: {razon}")

    print()
    print(f"Quedan {len(restantes)} entrada(s) en "
          f"{os.path.relpath(staging_path, repo_root())}.")


# ───────────────────────────────────────────────────────────── --compara ──

def cmd_compara(a, manifiesto_path, raw_dir):
    a.id = _id_unico(a.id, "--compara")
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
    g.add_argument("--escanea", default=None, metavar="RAIZ",
                    help="Nombre de una raíz (data_raw / lo que declare "
                         "data/raices.local.yaml) -- NUNCA una ruta. Escribe "
                         "candidatos nuevos (dedup por sha256) en "
                         "data/manifiesto-staging.yaml -- nunca en el manifiesto. "
                         "Sobre una raíz marcada como no-datos (p.ej. 'downloads') "
                         "exige --grupo o --grupo-n")
    g.add_argument("--promueve", action="store_true",
                    help="Mueve candidatos de data/manifiesto-staging.yaml a "
                         "data/manifiesto.yaml aunque url_origen no esté confirmada "
                         "(queda marcada con url_origen_procedencia)")

    ap.add_argument("--id", action="append", default=None,
                     help="repetible. --verifica corre sobre TODOS los --id dados; "
                          "--registra/--compara exigen exactamente uno")
    ap.add_argument("--grupo", default=None,
                     help="patrón fnmatch sobre la RUTA RELATIVA A LA RAÍZ, no sobre "
                          "el basename (desde ADR-310, cuando --escanea pasó a ser "
                          "recursivo): 'Descargas Manuales/*.dta' acota esa subcarpeta, "
                          "'academico/icpsr35024/crosstabs/*' esa otra, y '*.dta' sigue "
                          "casando en cualquier nivel porque fnmatch no trata '/' como "
                          "separador. Con --escanea: aplica --url/--usado-para a "
                          "los archivos nuevos cuya ruta case con el patrón (o, "
                          "combinado con --grupo-n, a un subconjunto DENTRO de esa "
                          "tanda). Con --promueve: limita la promoción a los que "
                          "casen (por defecto, --promueve procesa todo lo que hay en "
                          "staging)")
    ap.add_argument("--grupo-n", dest="grupo_n", type=int, default=None,
                     help="(--escanea) número de tanda -- 1-based, ver 'GRUPOS de "
                          "datos detectados' en el reporte -- para aplicar "
                          "--url/--usado-para a TODA la tanda, sin depender del "
                          "nombre. Se puede combinar con --grupo para un "
                          "subconjunto dentro de esa tanda")
    ap.add_argument("--url", dest="grupo_url", default=None,
                     help="url_origen a aplicar a los archivos que casen con "
                          "--grupo/--grupo-n (--escanea)")
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
    elif a.promueve:
        cmd_promueve(a, manifiesto_path, raw_dir)
    else:
        cmd_compara(a, manifiesto_path, raw_dir)


if __name__ == "__main__":
    main()
