#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ya_medido.py — ¿esta regla ya se midió, en algún lado del repo?

Uso:
    python3 tools/ya_medido.py <id-de-regla|R-n>

Nace de ACTO MAESTRA38-N9 · YA-MEDIDO (5/sep/2026) para instrumentar un
defecto que ya ocurrió dos veces en la misma semana, con el mismo patrón —
clasificar una regla como si no tuviera medición sin cruzar las fuentes
que sí la miden:

  (1) MAESTRA38-N5 clasificó `civico.voto.agencia_con_secreto` (R7.3) y
      `dinero.ahorro.seguro_deposito_atenua_aversion` (R1.5) como
      SIN-INSTRUMENTO cuando ambas ya tenían entrada medida en
      `milpa/tramite-ola5-propuesta-v0.yaml`/`canon/modelo-decision-v4_0.md`
      §7 — corregido por MAESTRA38-N6 (`FP-298`).
  (2) MAESTRA38-N7 recibió un encargo que llamaba «territorio virgen» a
      `civico.voto.clientelar_si_observable` (R7.6) y
      `civico.protesta.agravio_urbano` (R7.4), pese a que
      `MAESTRA35-L9`/`L11` ya habían pre-registrado y corrido falsaciones
      reales sobre esos mismos dos ids dos días antes.

Este script no reemplaza el juicio de mesa ni el de quien clasifica — solo
hace mecánico lo que en los dos casos de arriba se saltó: cruzar, por id o
por R-n, las fuentes del repo donde una medición real dejaría rastro.

Fuentes cruzadas (todas leídas del árbol de trabajo, ninguna de memoria):
    - milpa/tramite.yaml                        (el motor cargado)
    - milpa/tramite-ola5-propuesta-v0.yaml      (propuesta, por id)
    - canon/modelo-decision-v4_0.md §7          (enmiendas por regla)
    - forense/notas/*-L*-*.md                   (celdas y veredictos, espacio L)
    - forense/prereg-caja/S*-spec-*.md          (specs de caja selladas)
    - data/corrida0/<CALC>/                     (RESULT, ejecución y sello)

Además, `canon/registro-rotulos.tsv` se cruza como fuente de ALIAS ya
existentes (nunca inventados aquí): si un habitante de espacio (L, M, ...)
ya registró ahí, en su propia prosa, el id/R-n consultado, esa fila se
reporta también.

Sin heurística de parecido. El match es por id exacto (subcadena literal)
y por R-n exacto — ambos tal como el propio canon los declara. La única
equivalencia id↔R-n que este script conoce es la que ya vive en el propio
repo: el registro congelado de `tests/validador_registro_ids.py`
(ancla cada R-n a una subcadena estable de su regla en `canon/
modelo-decision-v4_0.md` §3) cruzado con el tag `**id:** \\`...\\`` que esa
misma regla ya trae. Si esa equivalencia no está registrada, el script NO
adivina — busca solo el término tal como se lo dieron.

Salida: por cada fuente, cada aparición con archivo:línea y los campos
situacion/tier/veredicto/p que traiga; las referencias exactas a RESULT se
resuelven hasta ejecución exitosa y sello válido; al final, una sola línea:
`NUNCA-MEDIDA` o `MEDIDA-EN: <lista>`. `MEDIDA-EN` acredita que hubo una
ejecución (incluido un intento `NO-ESTIMABLE`), no que la medición sea válida,
adoptada ni favorable a la regla.

Control positivo (verificado al escribir este script): `civico.voto.
clientelar_si_observable` y `civico.protesta.agravio_urbano` devuelven
`MEDIDA-EN: L9, L11`. Control negativo: `familia.cortejo.urbano_joven_apps`
devuelve `NUNCA-MEDIDA` (la única aparición con veredicto real ausente;
lo único que hay es la hipótesis que MAESTRA38-N6 cargó por FP-298).
"""
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUTA_TRAMITE = os.path.join(ROOT, "milpa", "tramite.yaml")
RUTA_PROPUESTA = os.path.join(ROOT, "milpa", "tramite-ola5-propuesta-v0.yaml")
RUTA_CANON_MODELO = os.path.join(ROOT, "canon", "modelo-decision-v4_0.md")
RUTA_REGISTRO_ROTULOS = os.path.join(ROOT, "canon", "registro-rotulos.tsv")
GLOB_NOTAS_L = os.path.join(ROOT, "forense", "notas", "*-L*-*.md")
GLOB_PREREG_CAJA = os.path.join(ROOT, "forense", "prereg-caja", "S*-spec-*.md")
RUTA_VALIDADOR = os.path.join(ROOT, "tests", "validador_registro_ids.py")
RUTA_CORRIDA0 = os.path.join(ROOT, "data", "corrida0")

RN_RE = re.compile(r"^R\d+(?:\.\d+)?$")
TIER_RE = re.compile(r"`(\[[^\]]+\])`")
ID_TAG_RE = re.compile(r"\*\*id:\*\*\s*((?:`[^`]+`(?:\s*\*\*\+\*\*\s*)?)+)")
TOKEN_EN_BACKTICKS_RE = re.compile(r"`([^`]+)`")
ENTRADA_YAML_RE = re.compile(r"^\s*-\s*id:\s*(\S+)")
SITUACION_RE = re.compile(r"\bsituacion:\s*([^\s#]+)")
TIER_YAML_RE = re.compile(r"\btier:\s*([^\s#]+)")
VEREDICTO_CAMPO_RE = re.compile(r"\b(veredicto[a-zA-Z_]*)\s*:\s*([^\s#\"]+)")
P_CAMPO_RE = re.compile(r"(?<![a-zA-Z_])p:\s*([0-9.]+)")
RESULTADO_REF_RE = re.compile(
    r"\bcorrida0_resultado_id:\s*[\"']?([A-Za-z0-9._-]+)"
)
CLASE_MEDIDA_RE = re.compile(r"\bclase:\s*[\"']?MEDIDO(?:·|\b)")
CAMPO_YAML_RE = re.compile(r"^(\s*)(?:-\s*)?([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")

# Solo estos campos declaran que una entrada con id distinto representa la
# misma regla. Una mención en comentario/notas no crea un alias.
CAMPOS_ALIAS_YAML = {
    "alias_de",
    "enmienda_de",
    "misma_regla_motor",
    "referida_a",
    "regla_base",
}

# Vocabulario B-bis de veredictos REALES (una falsación corrió y produjo
# esto) — más largos primero, para no cortar "CONTRARIA-REPLICADA" en
# "CONTRARIA". "NO-APLICA" deliberadamente NO está aquí: es el sentinela
# que el propio repo usa para "no corrido todavía".
VEREDICTOS_REALES = [
    "CONTRARIA-REPLICADA",
    "CORROBORADA-REPLICADA",
    "CORROBORADA-PARCIAL",
    "AMBIGUA-ENTRE-INSTRUMENTOS",
    "AMBIGUA-POR-UNIVERSO",
    "REFUTADA-COMO-CAUSAL",
    "NO-DISCRIMINA",
    "NO-ESTIMABLE",
    "CORROBORADA",
    "CONTRARIA",
]


def _relpath(ruta):
    return os.path.relpath(ruta, ROOT)


def _lineas(ruta):
    with io.open(ruta, encoding="utf-8") as f:
        return f.read().split("\n")


def _cargar_validador():
    spec = importlib.util.spec_from_file_location(
        "validador_registro_ids", RUTA_VALIDADOR
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _construye_mapa_rn_id():
    """R-n <-> id, derivado sin heurística: el registro congelado de
    tests/validador_registro_ids.py (REGISTRO) ancla cada R-n a una
    subcadena estable de su propia regla dentro de canon/modelo-decision-
    v4_0.md §3; de esa misma regla se lee el tag `**id:**` que ya trae.
    Si el ancla no aparece exactamente una vez en su sección, no se
    resuelve — nunca se adivina cuál regla es."""
    validador = _cargar_validador()
    rules = validador.parse_rules(RUTA_CANON_MODELO)
    por_seccion = {}
    for ln, sec, tier, texto in rules:
        por_seccion.setdefault(sec, []).append((ln, tier, texto))

    rn_a_ids, id_a_rn = {}, {}
    for rid, sec, _tier_esperado, ancla in validador.REGISTRO:
        candidatos = [r for r in por_seccion.get(sec, []) if ancla in r[2]]
        if len(candidatos) != 1:
            continue
        _ln, _tier, texto = candidatos[0]
        m = ID_TAG_RE.search(texto)
        if not m:
            continue
        ids = TOKEN_EN_BACKTICKS_RE.findall(m.group(1))
        if ids:
            rn_a_ids[rid] = ids
            for i in ids:
                id_a_rn[i] = rid
    return rn_a_ids, id_a_rn


def resuelve_terminos(token):
    """Términos de búsqueda: el propio token, más — solo si el registro
    congelado del canon ya declara la equivalencia — su contraparte R-n/id.
    Ninguna otra forma de alias se inventa aquí."""
    rn_a_ids, id_a_rn = _construye_mapa_rn_id()
    terminos = [token]
    notas = []
    if RN_RE.match(token):
        for i in rn_a_ids.get(token, []):
            if i not in terminos:
                terminos.append(i)
                notas.append(
                    f"{token} -> id `{i}` "
                    "(canon/modelo-decision-v4_0.md §3, tag **id:**)"
                )
    else:
        rn = id_a_rn.get(token)
        if rn:
            terminos.append(rn)
            notas.append(
                f"{token} -> {rn} "
                "(canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)"
            )
    return terminos, notas


def _contiene_token_exacto(texto, token):
    """Match de identidad, no de parecido ni de prefijo/sufijo."""
    patron = rf"(?<![A-Za-z0-9_.-]){re.escape(token)}(?![A-Za-z0-9_.-])"
    return re.search(patron, texto) is not None


def _contiene_algun_termino_exacto(texto, terminos):
    return any(_contiene_token_exacto(texto, t) for t in terminos)


def _campos_yaml(texto):
    """Devuelve campos YAML con su escalar plegado, sin parsear el archivo.

    El parser deliberadamente pequeño basta para delimitar campos de una
    entrada ya separada por ``- id:``. No interpreta comentarios ni busca
    fuera de esa entrada.
    """
    lineas = texto.splitlines()
    campos = []
    for i, linea in enumerate(lineas):
        m = CAMPO_YAML_RE.match(linea)
        if not m:
            continue
        sangria = len(m.group(1))
        nombre = m.group(2)
        partes = [m.group(3)]
        for siguiente in lineas[i + 1 :]:
            if siguiente.strip():
                sangria_siguiente = len(siguiente) - len(siguiente.lstrip())
                if sangria_siguiente <= sangria:
                    break
            partes.append(siguiente.strip())
        campos.append((nombre, " ".join(p for p in partes if p)))
    return campos


def _identidad_bloque_yaml(eid, bloque, terminos):
    if eid in terminos:
        return True
    for nombre, valor in _campos_yaml(bloque):
        if nombre in CAMPOS_ALIAS_YAML and _contiene_algun_termino_exacto(
            valor, terminos
        ):
            return True
    return False


def _referencias_corrida(texto):
    return sorted(set(RESULTADO_REF_RE.findall(texto)))


def _tiene_veredicto_real(texto):
    for v in VEREDICTOS_REALES:
        if v in texto:
            return v
    for _campo, valor in VEREDICTO_CAMPO_RE.findall(texto):
        if valor not in ("NO-APLICA", ""):
            return valor
    return None


def _evidencia_yaml(bloque):
    """Clasifica evidencia sustantiva dentro de UNA entrada YAML.

    ``p`` o una palabra MEDIDO en prosa no bastan. Una tasa requiere el campo
    estructurado ``clase: MEDIDO...`` y procedencia de ejecución; una
    falsación/NO-ESTIMABLE requiere un veredicto de resultado y procedencia.
    Las referencias corrida0 se confirman por separado contra sus artefactos.
    """
    campos = _campos_yaml(bloque)
    por_nombre = {}
    for nombre, valor in campos:
        por_nombre.setdefault(nombre, []).append(valor)

    tiene_medido_en = bool(por_nombre.get("medido_en"))
    tiene_sello_legacy = bool(por_nombre.get("sha256_payload")) and (
        bool(re.search(r"(?<![A-Za-z_])n:\s*\d+", bloque))
        or bool(por_nombre.get("ponderador"))
    )
    # Una referencia RESULT declarada se valida fuera de esta función contra
    # resultados + ejecución + sello. Por sí sola no es procedencia.
    procedencia = tiene_medido_en or tiene_sello_legacy

    veredicto = None
    for nombre, valores in por_nombre.items():
        if not nombre.startswith("veredicto"):
            continue
        for valor in valores:
            veredicto = _tiene_veredicto_real(valor)
            if veredicto:
                break
        if veredicto:
            break

    situacion = " ".join(por_nombre.get("situacion", []))
    if procedencia and (veredicto == "NO-ESTIMABLE" or "NO-ESTIMABLE" in situacion):
        return "INTENTO-NO-ESTIMABLE"
    if procedencia and veredicto:
        return veredicto
    if procedencia and CLASE_MEDIDA_RE.search(bloque):
        return "TASA-EJECUTADA"
    return None


def _extrae_campos(texto):
    campos = {}
    m = SITUACION_RE.search(texto)
    if m:
        campos["situacion"] = m.group(1)
    m = TIER_YAML_RE.search(texto)
    if m:
        campos["tier"] = m.group(1)
    else:
        m = TIER_RE.search(texto)
        if m:
            campos["tier"] = m.group(1)
    veredictos = VEREDICTO_CAMPO_RE.findall(texto)
    if veredictos:
        campos["veredicto"] = "; ".join(f"{n}={v}" for n, v in veredictos)
    m = P_CAMPO_RE.search(texto)
    if m:
        campos["p"] = m.group(1)
    return campos


def _bloques_yaml(ruta):
    """Parte un YAML de milpa/ en bloques por cada '- id: ...' de lista;
    cada bloque va de su propio '- id:' a la línea antes del siguiente."""
    lineas = _lineas(ruta)
    inicios = [
        (i, m.group(1))
        for i, l in enumerate(lineas)
        for m in [ENTRADA_YAML_RE.match(l)]
        if m
    ]
    bloques = []
    for idx, (i, eid) in enumerate(inicios):
        fin = inicios[idx + 1][0] if idx + 1 < len(inicios) else len(lineas)
        bloques.append((i + 1, eid, "\n".join(lineas[i:fin])))
    return bloques


def busca_en_yaml(ruta, terminos):
    ocurrencias = []
    habitante = os.path.basename(ruta)
    for ln, eid, bloque in _bloques_yaml(ruta):
        if _identidad_bloque_yaml(eid, bloque, terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(ruta),
                    "linea": ln,
                    "contexto": f"id: {eid}",
                    "campos": _extrae_campos(bloque),
                    "veredicto_real": _evidencia_yaml(bloque),
                    "referencias_corrida": _referencias_corrida(bloque),
                    "habitante": habitante,
                }
            )
    return ocurrencias


def busca_en_canon_s7(terminos):
    lineas = _lineas(RUTA_CANON_MODELO)
    inicio = fin = None
    for i, l in enumerate(lineas):
        if inicio is None and l.startswith("## 7 "):
            inicio = i
        elif inicio is not None and l.startswith("## 8 "):
            fin = i
            break
    if inicio is None:
        return []
    if fin is None:
        fin = len(lineas)
    ocurrencias = []
    for i in range(inicio, fin):
        l = lineas[i]
        if _contiene_algun_termino_exacto(l, terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(RUTA_CANON_MODELO),
                    "linea": i + 1,
                    "contexto": l.strip()[:200],
                    "campos": _extrae_campos(l),
                    # §7 es una vista de adopción/clasificación y puede citar
                    # varias reglas en una sola enmienda. Se lista, pero la
                    # ejecución debe acreditarse en la fuente sustantiva.
                    "veredicto_real": None,
                    "habitante": "canon§7",
                }
            )
    return ocurrencias


def _habitante_de_nota_l(ruta):
    base = os.path.basename(ruta)
    m = re.search(r"MAESTRA\d+-([A-Z]{1,3}\d+)", base)
    return m.group(1) if m else base


def _habitante_de_prereg(ruta):
    base = os.path.basename(ruta)
    m = re.match(r"^([A-Z]\d+)-", base)
    return m.group(1) if m else base


def busca_en_prosa(ruta, terminos, habitante, acredita=True):
    ocurrencias = []
    for i, l in enumerate(_lineas(ruta)):
        if _contiene_algun_termino_exacto(l, terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(ruta),
                    "linea": i + 1,
                    "contexto": l.strip()[:200],
                    "campos": _extrae_campos(l),
                    "veredicto_real": (
                        _tiene_veredicto_real(l) if acredita else None
                    ),
                    "habitante": habitante,
                }
            )
    return ocurrencias


def busca_alias_registro_rotulos(terminos):
    """Alias — únicamente los que canon/registro-rotulos.tsv ya declara:
    si un habitante de espacio ya escribió, en su propia prosa censada, el
    id/R-n consultado, esa fila cuenta como evidencia adicional. No se
    inventa ningún alias que no viva ya en este archivo."""
    ocurrencias = []
    for i, l in enumerate(_lineas(RUTA_REGISTRO_ROTULOS)):
        if _contiene_algun_termino_exacto(l, terminos):
            campos_tsv = l.split("\t")
            espacio = campos_tsv[0] if len(campos_tsv) > 0 else ""
            valor = campos_tsv[1] if len(campos_tsv) > 1 else ""
            # mismo estilo corto que _habitante_de_nota_l (L9, no MAESTRA35-L9)
            # para que la misma corrida no aparezca dos veces con dos etiquetas
            m_corto = re.search(r"MAESTRA\d+-([A-Z]{1,3}\d+)", valor)
            habitante = m_corto.group(1) if m_corto else (valor or espacio)
            ocurrencias.append(
                {
                    "archivo": _relpath(RUTA_REGISTRO_ROTULOS),
                    "linea": i + 1,
                    "contexto": f"{espacio}\t{valor}",
                    "campos": _extrae_campos(l),
                    # El registro declara identidad/procedencia; no acredita
                    # por sí solo que una medición se ejecutó.
                    "veredicto_real": None,
                    "habitante": habitante,
                }
            )
    return ocurrencias


def _sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _linea_de(ruta, texto):
    for i, linea in enumerate(_lineas(ruta), 1):
        if texto in linea:
            return i
    return 1


def _sello_corrida_valido(directorio, sello):
    for nombre in ("resultados.json", "ejecucion.json"):
        esperado = sello.get(nombre)
        ruta = os.path.join(directorio, nombre)
        if not esperado or not os.path.isfile(ruta) or _sha256(ruta) != esperado:
            return False
    ruta_sello = os.path.join(directorio, "sello.json")
    ruta_sidecar = os.path.join(directorio, "sello.sha256")
    if not os.path.isfile(ruta_sidecar):
        return False
    with io.open(ruta_sidecar, encoding="utf-8") as f:
        esperado_sidecar = f.read().split()
    return bool(esperado_sidecar) and _sha256(ruta_sello) == esperado_sidecar[0]


def busca_referencias_corrida(referencias, raiz_corrida0=RUTA_CORRIDA0):
    """Resuelve ids RESULT exactos hasta artefactos ejecutados y sellados."""
    pendientes = set(referencias)
    ocurrencias = []
    for directorio in sorted(glob.glob(os.path.join(raiz_corrida0, "*"))):
        if not pendientes:
            break
        if not os.path.isdir(directorio):
            continue
        rutas = {
            nombre: os.path.join(directorio, nombre)
            for nombre in ("resultados.json", "ejecucion.json", "sello.json")
        }
        if not all(os.path.isfile(r) for r in rutas.values()):
            continue
        try:
            with io.open(rutas["resultados.json"], encoding="utf-8") as f:
                resultados_doc = json.load(f)
            with io.open(rutas["ejecucion.json"], encoding="utf-8") as f:
                ejecucion = json.load(f)
            with io.open(rutas["sello.json"], encoding="utf-8") as f:
                sello = json.load(f)
        except (OSError, ValueError):
            continue
        resultados = resultados_doc.get("resultados", {})
        presentes = pendientes.intersection(resultados)
        if not presentes:
            continue
        ids_ejecutados = set(ejecucion.get("resultado_ids", []))
        sello_valido = _sello_corrida_valido(directorio, sello)
        calc = os.path.basename(directorio)
        for ref in sorted(presentes):
            ejecutado = ejecucion.get("exit_code") == 0 and ref in ids_ejecutados
            verificado = ejecutado and sello_valido
            valor = resultados[ref]
            linea_ejecucion = _linea_de(rutas["ejecucion.json"], '"exit_code"')
            linea_sello = _linea_de(rutas["sello.json"], '"resultados.json"')
            tipo = (
                "INTENTO-NO-ESTIMABLE"
                if isinstance(valor, str) and "NO-ESTIMABLE" in valor
                else "TASA-EJECUTADA"
            )
            ocurrencias.append(
                {
                    "archivo": _relpath(rutas["resultados.json"]),
                    "linea": _linea_de(rutas["resultados.json"], f'"{ref}"'),
                    "contexto": (
                        f"{ref}={valor!r}; "
                        f"ejecucion={_relpath(rutas['ejecucion.json'])}:"
                        f"{linea_ejecucion}; "
                        f"sello={_relpath(rutas['sello.json'])}:"
                        f"{linea_sello}"
                    ),
                    "campos": {
                        "resultado_id": ref,
                        "ejecutado": "SI" if ejecutado else "NO",
                        "sello": "VALIDO" if sello_valido else "INVALIDO",
                    },
                    "veredicto_real": tipo if verificado else None,
                    "habitante": calc,
                    "referencia_corrida": ref,
                }
            )
            if verificado:
                pendientes.remove(ref)
    return ocurrencias


def vincula_evidencia_corrida(ocurrencias_yaml, ocurrencias_corrida):
    verificadas = {
        o["referencia_corrida"]: o["veredicto_real"]
        for o in ocurrencias_corrida
        if o["veredicto_real"]
    }
    for ocurrencia in ocurrencias_yaml:
        tipos = [
            verificadas[r]
            for r in ocurrencia.get("referencias_corrida", [])
            if r in verificadas
        ]
        if tipos:
            ocurrencia["veredicto_real"] = (
                "INTENTO-NO-ESTIMABLE"
                if "INTENTO-NO-ESTIMABLE" in tipos
                else "TASA-EJECUTADA"
            )


def _imprime_seccion(titulo, ocurrencias):
    print(f"-- {titulo} --")
    if not ocurrencias:
        print("  (sin apariciones)")
    for o in ocurrencias:
        campos_str = " ".join(f"{k}={v}" for k, v in o["campos"].items())
        marca = f"  [{o['veredicto_real']}]" if o["veredicto_real"] else ""
        print(f"  {o['archivo']}:{o['linea']}  {campos_str}{marca}")
        if o.get("contexto"):
            print(f"      {o['contexto']}")
    print()


def main(argv):
    if len(argv) != 2:
        print(
            "uso: python3 tools/ya_medido.py <id-de-regla|R-n>", file=sys.stderr
        )
        return 2
    token = argv[1]

    terminos, notas_resolucion = resuelve_terminos(token)

    print(f"=== ya_medido: {token} ===")
    for n in notas_resolucion:
        print(f"  resuelto por canon: {n}")
    print(f"  términos de búsqueda (match exacto): {', '.join(terminos)}")
    print()

    todas = []

    def seccion(titulo, ocurrencias):
        todas.extend(ocurrencias)
        _imprime_seccion(titulo, ocurrencias)

    ocurrencias_tramite = busca_en_yaml(RUTA_TRAMITE, terminos)
    ocurrencias_propuesta = busca_en_yaml(RUTA_PROPUESTA, terminos)
    ocurrencias_yaml = ocurrencias_tramite + ocurrencias_propuesta
    referencias = {
        ref
        for o in ocurrencias_yaml
        for ref in o.get("referencias_corrida", [])
    }
    ocurrencias_corrida = busca_referencias_corrida(referencias)
    vincula_evidencia_corrida(ocurrencias_yaml, ocurrencias_corrida)

    seccion("milpa/tramite.yaml", ocurrencias_tramite)
    seccion(
        "milpa/tramite-ola5-propuesta-v0.yaml", ocurrencias_propuesta
    )
    seccion(
        "data/corrida0 (RESULT + ejecución + sello)", ocurrencias_corrida
    )
    seccion("canon/modelo-decision-v4_0.md §7", busca_en_canon_s7(terminos))

    ocurrencias_notas = []
    for ruta in sorted(glob.glob(GLOB_NOTAS_L)):
        base = os.path.basename(ruta).lower()
        acredita = any(
            marca in base for marca in ("resultados", "veredicto", "cierre")
        )
        ocurrencias_notas.extend(
            busca_en_prosa(
                ruta, terminos, _habitante_de_nota_l(ruta), acredita=acredita
            )
        )
    seccion("forense/notas/*-L*-*.md", ocurrencias_notas)

    ocurrencias_prereg = []
    for ruta in sorted(glob.glob(GLOB_PREREG_CAJA)):
        ocurrencias_prereg.extend(
            busca_en_prosa(
                ruta, terminos, _habitante_de_prereg(ruta), acredita=False
            )
        )
    seccion("forense/prereg-caja/S*-spec-*.md", ocurrencias_prereg)

    seccion(
        "canon/registro-rotulos.tsv (alias)",
        busca_alias_registro_rotulos(terminos),
    )

    habitantes_medidos = sorted(
        {o["habitante"] for o in todas if o["veredicto_real"]}
    )

    print("=" * 40)
    if habitantes_medidos:
        print(f"MEDIDA-EN: {', '.join(habitantes_medidos)}")
    else:
        print("NUNCA-MEDIDA")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
