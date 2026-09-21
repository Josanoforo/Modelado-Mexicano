#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/estado_comun.py -- primitivas de estado operativo compartidas entre
`tools/digesto_tramite.py`, `tools/tablero_programa.py` y `tests/check.py`
(T22), para dejar de tener implementaciones divergentes de conceptos
puramente mecánicos.

ACTO AUTOMATIZA-1-E2 · ESTADO-COMUN, 7/sep/2026
(`forense/encargos/2026-09-07-AUTOMATIZA-1-E2-ESTADO-COMUN.md`,
ELEMENTO 2). Defecto real medido antes de esta pieza: `tools/tablero_programa.py`
comparaba `estado == "ABIERTA"` (ciego a la glosa `ABIERTA -- pendiente...`)
mientras `tools/digesto_tramite.py` ya usaba `^ABIERTA(\\s|$)` -- sobre el
árbol real del 7/sep/2026, el digesto contaba 4 filas `ABIERTA`
(`FP-263, FP-288, FP-303, FP-326`) y el tablero sólo 2 (`FP-288, FP-326`):
`FP-263`/`FP-303` traen glosa y el tablero las perdía.

Sin clases, sin estado global: funciones puras con argumentos explícitos
(`raiz`, la ruta del clon). No es un framework ni una capa de gobernanza --
es exactamente las cinco primitivas que el encargo autoriza, movidas desde
donde ya vivían (mayormente `tools/digesto_tramite.py`), no reinventadas.

`tests/check.py::t15_adr_count()` NO usa `adr_max()` de aquí: es el vigía
de duplicados/huecos/secuencia de ADR y conserva su propia derivación --
duplicación deliberada de verificación, no deuda (T15 verificaría este
mismo módulo si `adr_max()` tuviera un defecto, y un vigía que comparte
implementación con lo que vigila deja de vigilar nada).
"""
import os
import re
import subprocess


def es_abierta(estado):
    """`estado` es `ABIERTA` con o sin glosa (`ABIERTA -- pendiente de...`).
    Comparar con `==` es ciego a la glosa y subcuenta las filas `ABIERTA`
    del tablero -- defecto real, medido (ver cabecera de este módulo).
    `estado.split()[0]` no basta (colisiona con la exactitud de otros
    estados de una sola palabra que empiecen igual, si los hubiera); el
    ancla `^ABIERTA(\\s|$)` es la comparación correcta, movida sin
    reinterpretar desde `tools/digesto_tramite.py`. No usa `startswith`:
    `ABIERTA-RECIBO` no es `ABIERTA`."""
    return bool(re.match(r"^ABIERTA(\s|$)", estado or ""))


# Tokens de cierre admitidos en la columna `estado` de
# `forense/no-corrido.tsv`. `CERRADA-POR-DISEÑO` la autoriza la FIRMA DE
# MESA del 15/sep/2026 (OBJETO 11 de la HOJA DE FIRMAS DE MESA 2026-09-15,
# `NC-0073`): una NC cuyo sucesor es `n/a -- por diseño` no está diferida
# ni desistida ni declinada -- nunca hubo trabajo pendiente que hacer, y
# escribirla como `CERRADA` a secas borra esa distinción. El token se
# admite aquí ANTES de usarse en el TSV para que ninguna receta lo lea
# como estado desconocido.
CIERRES_ADMITIDOS = (
    "CERRADA",
    "CERRADA-DESISTIDA",
    "CERRADA-DECLINADA",
    "CERRADA-POR-DISEÑO",
)


def es_cerrada(estado):
    """`estado` es uno de los cierres admitidos, con o sin glosa. Contraparte
    exacta de `es_abierta`: mismo anclaje `^TOKEN(\\s|$)`, por las mismas
    razones (una glosa no cambia el estado, y `startswith` pelado haría que
    `CERRADA-POR-DISEÑO` contara también como `CERRADA`, duplicándola)."""
    for token in CIERRES_ADMITIDOS:
        if re.match(rf"^{re.escape(token)}(\s|$)", estado or ""):
            return True
    return False


def lee_tablero(raiz):
    """(ruta, filas, n_lineas). TSV con cabecera, sin comillas -- el
    tablero se lee, no se parsea con `csv`, porque sus celdas ya traen
    comillas literales de firmas verbatim (semántica CSV cambiaría ese
    contenido). Movido sin reinterpretar desde
    `tools/digesto_tramite.py::lee_tablero`."""
    ruta = os.path.join(raiz, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(ruta):
        return ruta, None, 0
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip()]
    if not lineas:
        return ruta, [], 0
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    return ruta, filas, len(lineas)


def _corre(cmd, raiz, timeout=60):
    """Ejecuta y devuelve (rc, salida). Nunca lanza: un comando que no
    corre es un hallazgo, no una caída. Mismo contrato que
    `tools/digesto_tramite.py::corre`, reimplementado aquí (no importado
    de digesto) para que digesto pueda importar DE este módulo sin crear
    un ciclo."""
    try:
        p = subprocess.run(cmd, cwd=raiz, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError as e:
        return 127, f"comando no encontrado: {e}"
    except subprocess.TimeoutExpired:
        return 124, f"tiempo agotado ({timeout}s)"


def ramas_remotas_presentes(raiz):
    """(ramas, fuente). Todas las ramas remotas presentes en `origin`
    (incluida `main`, sin filtrar -- el filtro es decisión de cada
    llamador). Nombre `presentes`, no `vivas`: una rama en origin no
    implica PR abierto ni trabajo sin fusionar; esta función informa lo
    que sabe, no lo que eso significa. Estrategia movida sin reinterpretar
    desde `tools/digesto_tramite.py::seccion_c`: `git ls-remote --heads
    origin`; si no responde, `git for-each-ref refs/remotes/origin`
    (refleja el último `fetch` de este clon, no necesariamente el remoto
    de ahora)."""
    rc, salida = _corre(["git", "ls-remote", "--heads", "origin"], raiz)
    if rc == 0 and salida.strip():
        fuente = "`git ls-remote --heads origin` (estado vivo del remoto)"
        ramas = sorted({l.split("refs/heads/", 1)[1].strip()
                        for l in salida.splitlines() if "refs/heads/" in l})
    else:
        rc2, salida2 = _corre(["git", "for-each-ref", "--format=%(refname:short)",
                               "refs/remotes/origin"], raiz)
        fuente = ("`git for-each-ref refs/remotes/origin` (RESPALDO: `ls-remote` no "
                  f"respondió, rc={rc}) — refleja el último `fetch` de este clon, "
                  "no necesariamente el remoto de ahora")
        ramas = sorted({l.strip().split("origin/", 1)[-1]
                        for l in salida2.splitlines() if l.strip()
                        and not l.strip().endswith("/HEAD")})
    return ramas, fuente


def ramas_remotas_detalle(raiz):
    """(detalle, fuente). Por cada rama remota presente en `origin` distinta
    de `main`: nombre, commits delante/detrás de `origin/main`, fecha del
    último commit. Construida para `tools/tablero_programa.py` P1 (ACTO
    GEN2-TABLERO-SENAL-1): el tablero ya derivaba `ramas_remotas_presentes`
    pero el bloque renderizado no las pintaba -- una rama Codex sin PR quedó
    invisible para mesa durante horas (defecto real, 19/sep/2026)."""
    ramas, fuente = ramas_remotas_presentes(raiz)
    # Refresca los objetos de TODAS las ramas remotas antes de comparar --
    # `ramas_remotas_presentes()` puede listar (via `ls-remote`, sin objetos)
    # una rama mas nueva que el ultimo `fetch` de este clon; sin este paso,
    # `rev-list` sobre `origin/<rama>` falla en silencio y el detalle sale
    # `None` para una rama que sí existe (A.13: un negativo de un comando
    # que no trajo los objetos que iba a examinar no es un negativo).
    _corre(["git", "fetch", "--prune", "origin",
            "+refs/heads/*:refs/remotes/origin/*"], raiz, timeout=120)
    detalle = []
    for nombre in ramas:
        if nombre == "main":
            continue
        rc, salida = _corre(
            ["git", "rev-list", "--left-right", "--count",
             f"origin/main...origin/{nombre}"], raiz)
        if rc == 0 and salida.strip():
            partes = salida.strip().split()
            detras, delante = (int(partes[0]), int(partes[1])) if len(partes) == 2 else (None, None)
        else:
            detras = delante = None
        rc2, fecha = _corre(
            ["git", "log", "-1", "--format=%ad", "--date=short",
             f"origin/{nombre}"], raiz)
        detalle.append({
            "nombre": nombre,
            "delante_de_main": delante,
            "detras_de_main": detras,
            "fecha_ultimo_commit": fecha.strip() if rc2 == 0 else None,
        })
    return detalle, f"{fuente}; delante/detrás con `git rev-list --left-right --count origin/main...origin/<rama>`, fecha con `git log -1 --format=%ad --date=short origin/<rama>`"


def adr_max(raiz):
    """Máximo ADR NUMÉRICO actual, derivado de `canon/gobernanza-v1_15.md`
    -- mismo comando de la casa que ya usan `tools/tablero_programa.py` y
    la cascada de `/acto`, reimplementado en Python en vez de `grep`
    encadenado. Para tablero, E3 y consumidores productivos -- NO para
    T15 (ver cabecera del módulo).

    P-C.3 (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`, 21/sep/2026): sólo
    cuenta la época VIEJA (numérica) -- la nueva (`ADR-<AAMMDD>-<RÓTULO>-
    <hhhh>-<NN>`, raíz de acto) es un espacio aparte que nunca se
    renumera y no participa de este máximo. `(?![\\d-])`, no sólo
    `(?!-)`: un `\\d+` codicioso retrocede dígito a dígito, y cada dígito
    intermedio de una raíz nueva (`260921-GEN2-…`) está seguido de OTRO
    dígito -- sin el retroceso bloqueado, `ADR-260921-GEN2-X-1-6e60-01`
    se leía como el ADR numérico fantasma 260921 (o, tras retroceder,
    26092)."""
    ruta = os.path.join(raiz, "canon", "gobernanza-v1_15.md")
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    nums = [int(n) for n in re.findall(r"^\*\*ADR-(\d+)(?![\d-])", texto, re.M)]
    return max(nums) if nums else 0


# Dos épocas de id `ADR` (firma de mesa D-2, 21/sep/2026 · `ACTO
# GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1` · P-C): mismo mecanismo que
# `RE_FP_NUEVA`/`RE_FP_VIEJA` de `tools/nc_por_clase.py`. La época nueva
# va PRIMERO en la alternancia -- un id nuevo empieza por dígitos que la
# rama vieja casaría como prefijo.
RE_ADR_NUEVA = r"ADR-\d{6}-GEN2(?:-[A-Z0-9]+)+-[0-9a-f]{4}-\d{2}"
# Ancho `{1,3}`, derivado igual que en `tests/check.py::RE_ADR_VIEJA` (99 de
# ancho 2, 492 de ancho 3, ninguno más ancho, 21/sep/2026) -- sin el tope,
# un `ADR-2609` de 4 dígitos pasaba como numérico válido.
RE_ADR_VIEJA = r"ADR-\d{1,3}(?![\d\-A-Za-z])"
RE_ADR = rf"(?:{RE_ADR_NUEVA}|{RE_ADR_VIEJA})"


def adr_raiz_candidato(raiz, rotulo, commit_0bis, hoy=None):
    """Deriva el candidato de `ADR` con raíz de acto: `ADR-<AAMMDD>-
    <RÓTULO>-<hhhh>-<NN>` (P-C.1/P-C.2). `hhhh` son los 4 primeros hex del
    commit de 0-bis, que YA EXISTE antes de acuñar (D-17: el 0-bis es el
    primer commit del acto). `NN` es `max+1` sobre las raíces ya acuñadas
    con el MISMO prefijo `<AAMMDD>-<RÓTULO>-<hhhh>` en `gobernanza` -- el
    mismo patrón que ya usan `NC`/`FP` (D-2). No escribe nada: el humano
    redacta la entrada; este comando sólo deriva el id disponible."""
    import datetime
    hoy = hoy or datetime.date.today()
    aammdd = hoy.strftime("%y%m%d")
    hhhh = (commit_0bis or "")[:4]
    prefijo = f"ADR-{aammdd}-{rotulo}-{hhhh}"
    ruta = os.path.join(raiz, "canon", "gobernanza-v1_15.md")
    existentes = []
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            texto = f.read()
        existentes = re.findall(rf"^\*\*({re.escape(prefijo)}-(\d{{2}}))", texto, re.M)
    nn = max((int(n) for _, n in existentes), default=0) + 1
    return f"{prefijo}-{nn:02d}"


def fp_max(raiz):
    """Máximo FP NUMÉRICO actual, primera columna de
    `forense/firmas-pendientes.tsv`. E3 la necesita y no debe crear una
    segunda implementación.

    `ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2` (21/sep/2026, cierre de
    `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-04`): mismo `(?![\\d-])` que
    `adr_max`, que P-C.3 de `#962` puso ahí y aquí NO. Sin él, las 17
    filas de raíz de acto (`FP-260921-GEN2-…`) entraban al máximo y esta
    función devolvía el FP fantasma **260921** -- medido en este acto,
    no supuesto. La época de raíz nunca se renumera y no tiene máximo."""
    ruta = os.path.join(raiz, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    nums = [int(n) for n in re.findall(r"^FP-(\d+)(?![\d-])", texto, re.M)]
    return max(nums) if nums else 0
