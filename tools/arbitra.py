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


# ── CODIFICA-R-1 (P2): consume codificacion-R-v1_0.tsv, recalcula, compara ──
#
# El hallazgo de ARBITRO-R-1 (docstring de arriba) era que ningun marco trae
# codificacion binaria ni diseno real (estrato/upm) en forma legible por
# maquina. codificacion-R-v1_0.tsv (ENCARGO MAESTRA33-C3 CODIFICA-R-1) es esa
# tabla, poblada por codigo desde los R ya COMPUTADO. Lo de abajo la consume
# para recalcular una celda y comparar contra su corridas-R/<id>.json real --
# NUNCA reescribe un R existente (ver regresion()).
#
# Limite declarado, no oculto: `universo_filtro` en la tabla es prosa, no
# codigo. Este mecanismo NO aplica ningun filtro de universo mas alla de la
# codificacion binaria (uno/cero). Para celdas donde "la tabla ya es el
# universo" (sin filtro adicional, ej. DIN-11/SFT-04/TIC-08) el calculo es
# correcto. Para una celda que si necesite un filtro real (ej. DIN-05:
# TLOC=='4') este mecanismo produciria un numero distinto del real -- lo
# atrapa la propia regresion (no-coincide -> PARO), no una deteccion previa.
# Tampoco reproduce celdas cuya `tabla` declare un join (DIN-03/TIC-01/TIC-12):
# se declara explicitamente, no se adivina el join desde la prosa.

CODIFICACION = os.path.join(RAIZ, "forense", "prereg-duelo-v2", "codificacion-R-v1_0.tsv")

# (MAESTRA35-L2/P1c) marcador del motivo que produce() convierte en un JSON de
# abstencion con estado propio, en vez de dejar la celda sin rastro en disco.
LECTOR_AUSENTE = "NO-EJECUTABLE-LECTOR-AUSENTE"

_PATRON_BINARIO = re.compile(
    r"y=1\s+si\s+\S+=='([^']+)'.*?y=0\s+si=='([^']+)'", re.IGNORECASE | re.DOTALL
)
# Variante de conjunto: 'y=1 si VAR en {01,02,06} ...; y=0 si VAR en {03,...}'
# (CODIFICA-R-1/P3: la codificacion de BP1_23 es una union de varios codigos
# por lado, no un solo valor -- el patron de arriba no calza y no se toca).
_PATRON_BINARIO_SET = re.compile(
    r"y=1\s+si\s+\S+\s+en\s+\{([^}]+)\}.*?y=0\s+si\s+\S+\s+en\s+\{([^}]+)\}",
    re.IGNORECASE | re.DOTALL,
)

# ── ACTO MAESTRA35-L2 / P1 (a) y (b) ───────────────────────────────────────
# Dos codificaciones reales del sorteado v1_2 no son pertenencia a un conjunto
# de codigos y por eso salian None (el arbitro se abstenia, correctamente):
#   (a) UMBRAL numerico  -- 'y=1 si remesas > 0; y=0 si remesas == 0'
#       (FAM-M-05/06/07: remesas es monto continuo en pesos, 1313/1424/1389
#       valores distintos; no hay conjunto literal que escribir).
#   (b) COMPUESTO OR de dos variables -- 'y=1 si A=='1' o B=='1';
#       y=0 si A=='2' y B=='2'' (TRA-M-02).
# Ambos devuelven un CALLABLE (predicado sobre la fila completa), no un par de
# conjuntos: es la senal con la que calcula_desde_tabla despacha a
# estima(..., codifica=...). El orden de intento -- BINARIO, SET, UMBRAL,
# COMPUESTO -- garantiza que ninguna codificacion que ya calzaba cambie de
# rama; la regresion de 12 celdas lo mide, no lo supone.
_PATRON_UMBRAL = re.compile(
    r"y\s*=\s*1\s+si\s+(\w+)\s*(>=|<=|==|>|<)\s*(-?\d+(?:\.\d+)?)\s*;\s*"
    r"y\s*=\s*0\s+si\s+(\w+)\s*(>=|<=|==|>|<)\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
_PATRON_COMPUESTO_OR = re.compile(
    r"y\s*=\s*1\s+si\s+(\w+)\s*==\s*'([^']*)'\s+o\s+(\w+)\s*==\s*'([^']*)'\s*;\s*"
    r"y\s*=\s*0\s+si\s+(\w+)\s*==\s*'([^']*)'\s+y\s+(\w+)\s*==\s*'([^']*)'",
    re.IGNORECASE,
)

_COMPARA = {
    ">": lambda x, k: x > k,
    ">=": lambda x, k: x >= k,
    "<": lambda x, k: x < k,
    "<=": lambda x, k: x <= k,
    "==": lambda x, k: x == k,
}


def _numero(valor):
    """float o None. Vacio y no numerico -> None (n_codigo_no_valido), nunca 0."""
    try:
        return float(str(valor).strip())
    except (TypeError, ValueError):
        return None


def _predicado_umbral(var_uno, op_uno, k_uno, var_cero, op_cero, k_cero):
    """y=1 si <var_uno> <op> K ; y=0 si <var_cero> <op> K ; resto no valido.
    Los operadores se aplican EXACTAMENTE como estan escritos en la prosa."""
    cmp_uno, cmp_cero = _COMPARA[op_uno], _COMPARA[op_cero]

    def codifica(fila):
        x = _numero(fila.get(var_uno.lower()))
        if x is not None and cmp_uno(x, k_uno):
            return 1.0
        z = _numero(fila.get(var_cero.lower()))
        if z is not None and cmp_cero(z, k_cero):
            return 0.0
        return None

    return codifica


def _predicado_compuesto_or(a1, va1, b1, vb1, a0, va0, b0, vb0):
    """y=1 si A==va1 o B==vb1 ; y=0 si A==va0 y B==vb0 ; cualquier otra
    combinacion (incluidos vacios y no-respuesta) queda FUERA."""

    def codifica(fila):
        a = str(fila.get(a1.lower(), "")).strip()
        b = str(fila.get(b1.lower(), "")).strip()
        if a == va1 or b == vb1:
            return 1.0
        a0v = str(fila.get(a0.lower(), "")).strip()
        b0v = str(fila.get(b0.lower(), "")).strip()
        if a0v == va0 and b0v == vb0:
            return 0.0
        return None

    return codifica


def lee_codificacion(ruta=CODIFICACION):
    """codificacion-R-v1_0.tsv tiene cabecera '#id\\t...' -- se despoja el
    '#' para poder usar DictReader normal."""
    with open(ruta, encoding="utf-8") as f:
        campos = f.readline().rstrip("\n").lstrip("#").split("\t")
        return {fila["id"]: fila for fila in csv.DictReader(f, fieldnames=campos, delimiter="\t")}


def _correr_r():
    """Carga corridas-R/correr-R.py como modulo (el nombre trae un guion,
    no es importable con `import`). Reusa su estima()/csv_zip()/dbf_zip() --
    esta herramienta no reimplementa el calculo estadistico."""
    import importlib.util
    ruta = os.path.join(CORRIDAS_R, "correr-R.py")
    spec = importlib.util.spec_from_file_location("correr_R_modulo", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parsea_codificacion_binaria(texto):
    """Devuelve, en este orden de intento:
      · (uno, cero) -- par de CONJUNTOS, para 'y=1 si VAR==V1 ...; y=0 si==V2'
        y para 'y=1 si VAR en {..}; y=0 si VAR en {..}'  (comportamiento previo,
        intacto);
      · un CALLABLE codifica(fila)->1.0|0.0|None, para el umbral numerico
        (MAESTRA35-L2/P1a) y el compuesto OR de dos variables (P1b);
      · None si la prosa no calza ninguno de los cuatro patrones -- nunca
        adivina (p.ej. el patron categorico de TIC-12 no calza aqui, a
        proposito). Quien llama distingue las dos formas con callable()."""
    m = _PATRON_BINARIO.search(texto or "")
    if m:
        return {m.group(1)}, {m.group(2)}
    m = _PATRON_BINARIO_SET.search(texto or "")
    if m:
        uno = {v.strip() for v in m.group(1).split(",") if v.strip()}
        cero = {v.strip() for v in m.group(2).split(",") if v.strip()}
        return uno, cero
    m = _PATRON_UMBRAL.search(texto or "")
    if m:
        return _predicado_umbral(m.group(1), m.group(2), float(m.group(3)),
                                 m.group(4), m.group(5), float(m.group(6)))
    m = _PATRON_COMPUESTO_OR.search(texto or "")
    if m:
        return _predicado_compuesto_or(*m.groups())
    return None


def resuelve_miembro_zip(archivo, nombre_logico):
    """Dado un nombre de tabla LOGICO (el que trae el FD, p.ej. 'TMod_Vic'),
    busca dentro del zip el miembro cuyo nombre base lo contiene (sin
    distinguir mayusculas/guiones bajos). Devuelve (miembro, None) si hay
    exactamente un candidato, o (None, motivo) si hay 0 o mas de 1 -- nunca
    adivina entre varios.

    Si hay mas de un candidato por nombre, se descartan los que traen
    'diccionario' en la ruta (INEGI publica el diccionario de datos como un
    CSV aparte, con el mismo nombre de tabla en el nombre de archivo, junto
    al CSV de datos real bajo 'conjunto_de_datos/') -- es una distincion
    real y verificable en la ruta, no una eleccion arbitraria entre
    iguales."""
    import zipfile
    objetivo = _plano(nombre_logico)
    ruta_zip = os.path.join(RAIZ, "data", "raw", archivo)
    with zipfile.ZipFile(ruta_zip) as z:
        candidatos = [n for n in z.namelist() if not n.endswith("/") and objetivo in _plano(os.path.basename(n))]
    if len(candidatos) > 1:
        sin_diccionario = [n for n in candidatos if "diccionario" not in _plano(n)]
        if sin_diccionario:
            candidatos = sin_diccionario
    if len(candidatos) == 1:
        return candidatos[0], None
    if not candidatos:
        return None, f"ningun miembro de {archivo} contiene {nombre_logico!r} en su nombre"
    return None, f"{len(candidatos)} miembros de {archivo} contienen {nombre_logico!r} tras descartar diccionarios: {candidatos}"


def calcula_desde_tabla(id_celda, tabla_codif, manifiesto, mod_r):
    """Calcula (r, conteos, fila) para id_celda usando SOLO lo que
    codificacion-R-v1_0.tsv declara. Devuelve (resultado_o_None, motivo,
    advertencias)."""
    fila = tabla_codif.get(id_celda)
    if fila is None:
        return None, f"{id_celda}: sin fila en {os.path.basename(CODIFICACION)}", []

    tabla = fila["tabla"]
    if "join" in tabla.lower():
        return None, f"{id_celda}: tabla declara join ({tabla!r}), no reproducible desde la tabla de codificacion sola", []

    par = parsea_codificacion_binaria(fila["codificacion"])
    if par is None:
        return None, f"{id_celda}: codificacion no calza ningun patron binario reconocido: {fila['codificacion']!r}", []
    # (MAESTRA35-L2/P1) dos formas posibles: par de conjuntos (camino previo) o
    # predicado numerico/compuesto sobre la fila entera.
    if callable(par):
        codifica, uno, cero = par, None, None
    else:
        codifica, (uno, cero) = None, par

    entrada = next((e for e in manifiesto if e.get("id") == fila["payload_id"]), None)
    if entrada is None:
        return None, f"{id_celda}: payload_id {fila['payload_id']!r} no encontrado en manifiesto.yaml", []
    archivo = entrada["archivo"]

    advertencias = [
        f"{id_celda}: universo_filtro es informativo, NO se ejecuta como filtro "
        f"({fila['universo_filtro']!r}) -- si esta celda necesita un filtro real, "
        f"este calculo sera incorrecto y debe salir NO-COINCIDE."
    ]

    # `tabla` puede ser una ruta fisica ya conocida (trae '/' o termina en
    # .csv/.dbf) o un nombre LOGICO (el que cita el FD, p.ej. 'TMod_Vic'),
    # que hay que resolver dentro del zip -- nunca se adivina si hay 0 o
    # mas de 1 candidato.
    es_fisica = "/" in tabla or tabla.lower().endswith((".csv", ".dbf"))
    if es_fisica:
        miembro = tabla
    else:
        miembro, motivo = resuelve_miembro_zip(archivo, tabla)
        if miembro is None:
            return None, f"{id_celda}: {motivo}", advertencias
        advertencias.append(f"{id_celda}: tabla logica {tabla!r} resuelta a miembro fisico {miembro!r} dentro de {archivo}")

    # (MAESTRA35-L2/P1c) El lector se elige por el sufijo REAL del miembro y solo
    # entre los dos que existen. Antes, todo lo que no fuera .dbf caia en
    # csv_zip(): un miembro .dta o .sav se leia como CSV y producia una cifra
    # sin sentido en vez de una abstencion. No se anade lector .dta aqui
    # (fuera de alcance declarado del acto).
    sufijo = os.path.splitext(miembro)[1].lower()
    if sufijo == ".dbf":
        filas = mod_r.dbf_zip(archivo, miembro)
    elif sufijo == ".csv":
        filas = mod_r.csv_zip(archivo, miembro)
    else:
        return None, (f"{LECTOR_AUSENTE}: {id_celda}: el miembro {miembro!r} de {archivo} "
                      f"tiene sufijo {sufijo!r}; los unicos lectores disponibles son "
                      f".csv (csv_zip) y .dbf (dbf_zip)"), advertencias
    r, c = mod_r.estima(filas, fila["variable"].lower(), uno, cero,
                         fila["ponderador"].lower(), fila["estrato"].lower(), fila["upm"].lower(),
                         codifica=codifica)
    fila = dict(fila)
    fila["_tabla_resuelta"] = miembro
    return (r, c, fila), None, advertencias


CAMPOS_REGRESION = ["R", "EE_R", "n_efectivo", "n_estratos", "n_upm_total"]


def regresion(ids, tabla_codif=None, manifiesto=None, mod_r=None):
    """Recalcula ids EXISTENTES en corridas-R/ desde la tabla y diffea contra
    su JSON real. NUNCA escribe en corridas-R/. Devuelve (coincide_todos,
    detalle)."""
    tabla_codif = tabla_codif or lee_codificacion()
    manifiesto = manifiesto or carga_manifiesto()
    mod_r = mod_r or _correr_r()
    detalle, coincide_todos = [], True

    for id_celda in ids:
        ruta_existente = os.path.join(CORRIDAS_R, f"{id_celda}.json")
        if not os.path.exists(ruta_existente):
            detalle.append({"id": id_celda, "coincide": False, "motivo": f"no existe corridas-R/{id_celda}.json"})
            coincide_todos = False
            continue
        with open(ruta_existente, encoding="utf-8") as f:
            existente = json.load(f)

        resultado, motivo, advertencias = calcula_desde_tabla(id_celda, tabla_codif, manifiesto, mod_r)
        if resultado is None:
            detalle.append({"id": id_celda, "coincide": False, "motivo": motivo})
            coincide_todos = False
            continue

        r, c, _fila = resultado
        if r is None:
            detalle.append({"id": id_celda, "coincide": False, "motivo": "SIN_FILAS tras aplicar codificacion/ponderador"})
            coincide_todos = False
            continue
        cv = (r["se"] / r["p_hat"]) if r["p_hat"] else None
        nuevo = {"R": r["p_hat"], "EE_R": r["se"], "n_estratos": r["n_estratos"],
                 "n_upm_total": r["n_upm_total"], **c}

        campos, ok = {}, True
        for campo in CAMPOS_REGRESION:
            v_nuevo, v_viejo = nuevo.get(campo), existente.get(campo)
            if isinstance(v_nuevo, float) or isinstance(v_viejo, float):
                iguales = v_viejo is not None and v_nuevo is not None and abs(v_nuevo - v_viejo) < 1e-9
            else:
                iguales = v_nuevo == v_viejo
            campos[campo] = {"nuevo": v_nuevo, "existente": v_viejo, "coincide": iguales}
            ok = ok and iguales
        detalle.append({"id": id_celda, "coincide": ok, "campos": campos, "advertencias": advertencias})
        coincide_todos = coincide_todos and ok

    return coincide_todos, detalle


def _encuesta_ola_del_marco(ruta_marco, id_celda):
    """Lee SOLO encuesta/ola de la fila id_celda en un marco (solo lectura,
    nunca se escribe). Devuelve (encuesta, ola) o (None, None) si no esta."""
    for fila in lee_marco(ruta_marco):
        if fila.get("id") == id_celda:
            return fila.get("encuesta"), fila.get("ola")
    return None, None


def _escribe_abstencion(id_celda, ruta_marco, tabla_codif, estado, motivo):
    """(MAESTRA35-L2/P1c) JSON de una celda que NO produjo R, con el mismo
    esquema que los R reales (claves ausentes en None) para que quien lea
    corridas-R/ no tenga que distinguir dos formatos. Deja rastro en disco de
    por que se abstuvo: sin esto, una celda que revienta no aparece en ningun
    lado salvo el stdout de la corrida."""
    fila = tabla_codif.get(id_celda) or {}
    encuesta, ola = _encuesta_ola_del_marco(ruta_marco, id_celda)
    doc = {k: None for k in esquema_de_referencia()}
    doc.update({
        "id_celda": id_celda,
        "estado": estado,
        "encuesta": encuesta,
        "ola": ola,
        "payload_id": fila.get("payload_id"),
        "tabla": fila.get("tabla"),
        "variable": fila.get("variable"),
        "ponderador": fila.get("ponderador"),
        "estrato": fila.get("estrato"),
        "upm": fila.get("upm"),
        "codificacion": fila.get("codificacion"),
        "universo": fila.get("universo_filtro"),
        "motivo": motivo,
    })
    with open(os.path.join(CORRIDAS_R, f"{id_celda}.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return doc


def produce(ids, ruta_marco, tabla_codif=None, manifiesto=None, mod_r=None):
    """Calcula celdas NUEVAS (sin corridas-R/<id>.json todavia) desde la
    tabla y ESCRIBE el JSON, con el mismo esquema que los existentes.
    Rehusa sobreescribir un id que ya tiene JSON (eso es de regresion(),
    no de produce()). Devuelve detalle por id."""
    tabla_codif = tabla_codif or lee_codificacion()
    manifiesto = manifiesto or carga_manifiesto()
    mod_r = mod_r or _correr_r()
    detalle = []

    for id_celda in ids:
        ruta_salida = os.path.join(CORRIDAS_R, f"{id_celda}.json")
        if os.path.exists(ruta_salida):
            detalle.append({"id": id_celda, "escrito": False, "motivo": "YA-EXISTE, produce() nunca sobreescribe"})
            continue

        # (MAESTRA35-L2/P1c) Una excepcion en UNA celda ya no tumba el lote: se
        # registra en el JSON de esa celda y el lote sigue. Medido con DIN-M-01
        # por MAESTRA34-L2 (§4), donde una sola celda aborto la corrida entera.
        try:
            resultado, motivo, advertencias = calcula_desde_tabla(id_celda, tabla_codif, manifiesto, mod_r)
            if resultado is None:
                if motivo.startswith(LECTOR_AUSENTE):
                    doc = _escribe_abstencion(id_celda, ruta_marco, tabla_codif, LECTOR_AUSENTE, motivo)
                    detalle.append({"id": id_celda, "escrito": True, "estado": doc["estado"],
                                    "motivo": motivo, "advertencias": advertencias})
                else:
                    detalle.append({"id": id_celda, "escrito": False, "motivo": motivo,
                                    "advertencias": advertencias})
                continue

            r, c, fila = resultado
            encuesta, ola = _encuesta_ola_del_marco(ruta_marco, id_celda)
            spec = {"encuesta": encuesta, "ola": ola, "payload_id": fila["payload_id"],
                    "tabla": fila.get("_tabla_resuelta", fila["tabla"]), "variable": fila["variable"],
                    "ponderador": fila["ponderador"], "estrato": fila["estrato"], "upm": fila["upm"],
                    "codificacion": fila["codificacion"], "universo": fila["universo_filtro"]}
            doc = mod_r.escribe(id_celda, spec, r, c)
            detalle.append({"id": id_celda, "escrito": True, "estado": doc["estado"],
                             "R": doc.get("R"), "advertencias": advertencias})
        except Exception as e:
            traza = f"{type(e).__name__}: {e}"
            _escribe_abstencion(id_celda, ruta_marco, tabla_codif, "ERROR", traza)
            detalle.append({"id": id_celda, "escrito": True, "estado": "ERROR", "motivo": traza})

    return detalle


# ── ACTO MAESTRA35-L2 · PROYECCION CIEGA DEL MARCO ─────────────────────────
#
# Hallazgo que la obliga: marco-M-sorteado-v1_2.tsv incrusta el p/M del motor
# dentro de la columna de prosa `razon_DD` -- y lo hace para EXACTAMENTE las 4
# celdas que todavia no tienen R (FAM-M-05/06/07, TRA-M-02); las otras 10 estan
# limpias. Como /arbitra COMMIT-1 exige copiar la fila del marco VERBATIM para
# congelar la spec, cualquier sesion ciega que ejecute el procedimiento al pie
# de la letra se contamina en el paso mismo que la regla protege. No es un
# descuido de un ejecutor: es el procedimiento contra el artefacto.
#
# Esta proyeccion es la salida: un TSV derivado, generado por codigo (nunca a
# mano), con una LISTA BLANCA de columnas -- lo que el arbitro R necesita para
# congelar una spec y correr -- y sin ninguna columna de prosa del lado M. Se
# elige lista blanca y no lista negra a proposito: una columna nueva en una
# version futura del marco queda FUERA por omision, no dentro por descuido.
#
# `publicada` tambien queda fuera aunque hoy no traiga p: es la cifra contra la
# que se compara R, y el arbitro no la necesita para medir.

COLUMNAS_CIEGAS = [
    "id", "encuesta", "ola", "universo", "variable", "estimador",
    "ponderador", "escala", "cv_arbitro", "n_no_ponderado", "dominio",
    "en_corpus", "elegible", "elegible_v1_1",
]

# Cifra con forma de p/M/L: 'p: 0.62', 'p=0.62', 'emite 0.045694', o cualquier
# decimal de 4+ digitos suelto en la prosa.
_PATRON_CIFRA_MOTOR = re.compile(
    r"(?:\bp\s*[:=]\s*|\bemite\s+|\bp_?hat\s*=\s*)(\d+\.\d+)|\b(\d\.\d{4,})\b"
)


def _cifras_motor(texto):
    return [a or b for a, b in _PATRON_CIFRA_MOTOR.findall(texto or "")]


def proyecta_ciega(ruta_marco, ruta_salida):
    """Escribe la proyeccion ciega de `ruta_marco`. Devuelve (ok, informe).

    NO escribe si la proyeccion resultante contiene una sola cifra con forma de
    p/M -- y comprueba antes, sobre el marco ENTERO, que el detector encuentra
    al menos una (control positivo): un veredicto 'limpio' producido por un
    detector roto no es un veredicto.
    """
    filas = lee_marco(ruta_marco)
    if not filas:
        return False, {"error": f"{ruta_marco}: 0 filas"}
    todas = list(filas[0].keys())
    faltan = [c for c in COLUMNAS_CIEGAS if c not in todas]
    if faltan:
        return False, {"error": f"el marco no trae estas columnas de la lista blanca: {faltan}"}

    # Control positivo: el detector DEBE encontrar cifras en el marco completo.
    control = [(f["id"], c, len(_cifras_motor(v)))
               for f in filas for c, v in f.items() if _cifras_motor(v)]
    informe = {
        "marco": os.path.relpath(ruta_marco, RAIZ),
        "sha256_marco": sha256_de(ruta_marco),
        "filas": len(filas),
        "columnas_origen": len(todas),
        "columnas_conservadas": list(COLUMNAS_CIEGAS),
        "columnas_descartadas": [c for c in todas if c not in COLUMNAS_CIEGAS],
        "control_positivo_cifras_en_marco": sum(n for _, _, n in control),
        "control_positivo_celdas": sorted({i for i, _, _ in control}),
        "control_positivo_columnas": sorted({c for _, c, _ in control}),
    }
    if not control:
        informe["error"] = ("CONTROL POSITIVO FALLIDO: el detector no encontro ninguna cifra "
                            "de motor en el marco completo. O el marco ya esta limpio -- y "
                            "entonces esta proyeccion sobra -- o el detector se rompio. "
                            "No se escribe nada.")
        return False, informe

    # La proyeccion, y su propia verificacion.
    sucias = [(f["id"], c, _cifras_motor(f[c])) for f in filas for c in COLUMNAS_CIEGAS if _cifras_motor(f[c])]
    if sucias:
        informe["error"] = f"la lista blanca deja pasar cifras de motor: {sucias}"
        return False, informe

    with open(ruta_salida, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS_CIEGAS, delimiter="\t",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for f in filas:
            w.writerow({c: f[c] for c in COLUMNAS_CIEGAS})

    # Se relee del DISCO lo que quedo escrito -- no se declara limpio lo que se
    # tenia en memoria antes de escribir.
    escritas = lee_marco(ruta_salida)
    residuo = [(f["id"], c, _cifras_motor(v)) for f in escritas for c, v in f.items() if _cifras_motor(v)]
    informe.update({
        "salida": os.path.relpath(ruta_salida, RAIZ),
        "filas_escritas": len(escritas),
        "campos_examinados_tras_escribir": sum(len(f) for f in escritas),
        "cifras_de_motor_en_la_salida": len(residuo),
    })
    if residuo:
        os.remove(ruta_salida)
        informe["error"] = f"la salida contenia cifras de motor tras escribirse; se borro: {residuo}"
        return False, informe
    informe["sha256_salida"] = sha256_de(ruta_salida)
    return True, informe


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--regresion":
        ids = sys.argv[2:]
        if not ids:
            print("uso: arbitra.py --regresion <id1> [id2] [id3] ...")
            sys.exit(2)
        ok, detalle = regresion(ids)
        for d in detalle:
            print(f"{d['id']}: {'COINCIDE' if d['coincide'] else 'NO-COINCIDE'}")
            for campo, info in d.get("campos", {}).items():
                marca = "==" if info["coincide"] else "!="
                print(f"    {campo}: nuevo={info['nuevo']!r} {marca} existente={info['existente']!r}")
            if d.get("motivo"):
                print("    motivo:", d["motivo"])
            for a in d.get("advertencias", []):
                print("    advertencia:", a)
        sys.exit(0 if ok else 1)

    if len(sys.argv) >= 2 and sys.argv[1] == "--proyecta-ciego":
        if len(sys.argv) < 4:
            print("uso: arbitra.py --proyecta-ciego <marco.tsv> <salida.tsv>")
            sys.exit(2)
        ok, informe = proyecta_ciega(sys.argv[2], sys.argv[3])
        for k, v in informe.items():
            print(f"{k}: {v}")
        print("VEREDICTO:", "PROYECCION CIEGA ESCRITA" if ok else "NO SE ESCRIBIO")
        sys.exit(0 if ok else 1)

    if len(sys.argv) >= 3 and sys.argv[1] == "--produce":
        ruta_marco = sys.argv[2]
        ids = sys.argv[3:]
        if not ids:
            print("uso: arbitra.py --produce <marco.tsv> <id1> [id2] [id3] [id4]")
            sys.exit(2)
        detalle = produce(ids, ruta_marco)
        ok = True
        for d in detalle:
            print(f"{d['id']}: {'ESCRITO ' + d.get('estado', '') if d['escrito'] else 'NO-ESCRITO'}")
            if d['escrito']:
                print(f"    R={d.get('R')}")
            else:
                ok = False
            if d.get("motivo"):
                print("    motivo:", d["motivo"])
            for a in d.get("advertencias", []):
                print("    advertencia:", a)
        sys.exit(0 if ok else 1)

    if len(sys.argv) < 2:
        print(f"uso: {sys.argv[0]} <ruta-marco.tsv> [columna_elegible] [id1 id2 ...]")
        print(f"  o: {sys.argv[0]} --regresion <id1> [id2] [id3] ...")
        print(f"  o: {sys.argv[0]} --produce <marco.tsv> <id1> [id2] [id3] [id4]")
        print(f"  o: {sys.argv[0]} --proyecta-ciego <marco.tsv> <salida.tsv>")
        sys.exit(2)
    ruta = sys.argv[1]
    col = sys.argv[2] if len(sys.argv) > 2 else None
    solo = sys.argv[3:] or None
    main(ruta, col, solo)
