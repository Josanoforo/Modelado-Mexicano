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
por R-n, las cinco fuentes del repo donde una medición real dejaría rastro.

Fuentes cruzadas (todas leídas del árbol de trabajo, ninguna de memoria):
    - milpa/tramite.yaml                        (el motor cargado)
    - milpa/tramite-ola5-propuesta-v0.yaml      (propuesta, por id)
    - canon/modelo-decision-v4_0.md §7          (enmiendas por regla)
    - forense/notas/*-L*-*.md                   (celdas y veredictos, espacio L)
    - forense/prereg-caja/S*-spec-*.md          (specs de caja selladas)

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

Salida: por cada una de las cinco fuentes (más el alias de
registro-rotulos), cada aparición con archivo:línea y los campos
situacion/tier/veredicto/p que la aparición traiga; al final, una sola
línea: `NUNCA-MEDIDA` o `MEDIDA-EN: <lista>`.

Control positivo (verificado al escribir este script): `civico.voto.
clientelar_si_observable` y `civico.protesta.agravio_urbano` devuelven
`MEDIDA-EN: L9, L11`. Control negativo: `familia.cortejo.urbano_joven_apps`
devuelve `NUNCA-MEDIDA` (la única aparición con veredicto real ausente;
lo único que hay es la hipótesis que MAESTRA38-N6 cargó por FP-298).
"""
import glob
import importlib.util
import io
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

RN_RE = re.compile(r"^R\d+(?:\.\d+)?$")
TIER_RE = re.compile(r"`(\[[^\]]+\])`")
ID_TAG_RE = re.compile(r"\*\*id:\*\*\s*((?:`[^`]+`(?:\s*\*\*\+\*\*\s*)?)+)")
TOKEN_EN_BACKTICKS_RE = re.compile(r"`([^`]+)`")
ENTRADA_YAML_RE = re.compile(r"^\s*-\s*id:\s*(\S+)")
SITUACION_RE = re.compile(r"\bsituacion:\s*([^\s#]+)")
TIER_YAML_RE = re.compile(r"\btier:\s*([^\s#]+)")
VEREDICTO_CAMPO_RE = re.compile(r"\b(veredicto[a-zA-Z_]*)\s*:\s*([^\s#\"]+)")
P_CAMPO_RE = re.compile(r"(?<![a-zA-Z_])p:\s*([0-9.]+)")

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
    return io.open(ruta, encoding="utf-8").read().split("\n")


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


def _tiene_veredicto_real(texto):
    for v in VEREDICTOS_REALES:
        if v in texto:
            return v
    for _campo, valor in VEREDICTO_CAMPO_RE.findall(texto):
        if valor not in ("NO-APLICA", ""):
            return valor
    return None


def _ventana_de_terminos(texto, terminos, radio=260):
    """Recorta `texto` a una ventana centrada en la aparición del término —
    para no atribuirle a una regla el veredicto de OTRA regla que un bloque
    largo (entrada de YAML con comentario final ajeno, o un párrafo-enmienda
    de §7 que cita varias reglas de un jalón) también menciona más lejos."""
    pos = min((texto.find(t) for t in terminos if t in texto), default=-1)
    if pos < 0:
        return texto
    ini = max(0, pos - radio)
    fin = min(len(texto), pos + radio)
    return texto[ini:fin]


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
        if any(t in bloque for t in terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(ruta),
                    "linea": ln,
                    "contexto": f"id: {eid}",
                    "campos": _extrae_campos(bloque),
                    "veredicto_real": _tiene_veredicto_real(
                        _ventana_de_terminos(bloque, terminos)
                    ),
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
        if any(t in l for t in terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(RUTA_CANON_MODELO),
                    "linea": i + 1,
                    "contexto": l.strip()[:200],
                    "campos": _extrae_campos(l),
                    "veredicto_real": _tiene_veredicto_real(
                        _ventana_de_terminos(l, terminos)
                    ),
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


def busca_en_prosa(ruta, terminos, habitante):
    ocurrencias = []
    for i, l in enumerate(_lineas(ruta)):
        if any(t in l for t in terminos):
            ocurrencias.append(
                {
                    "archivo": _relpath(ruta),
                    "linea": i + 1,
                    "contexto": l.strip()[:200],
                    "campos": _extrae_campos(l),
                    "veredicto_real": _tiene_veredicto_real(
                        _ventana_de_terminos(l, terminos)
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
        if any(t in l for t in terminos):
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
                    "veredicto_real": _tiene_veredicto_real(
                        _ventana_de_terminos(l, terminos)
                    ),
                    "habitante": habitante,
                }
            )
    return ocurrencias


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

    seccion("milpa/tramite.yaml", busca_en_yaml(RUTA_TRAMITE, terminos))
    seccion(
        "milpa/tramite-ola5-propuesta-v0.yaml",
        busca_en_yaml(RUTA_PROPUESTA, terminos),
    )
    seccion("canon/modelo-decision-v4_0.md §7", busca_en_canon_s7(terminos))

    ocurrencias_notas = []
    for ruta in sorted(glob.glob(GLOB_NOTAS_L)):
        ocurrencias_notas.extend(
            busca_en_prosa(ruta, terminos, _habitante_de_nota_l(ruta))
        )
    seccion("forense/notas/*-L*-*.md", ocurrencias_notas)

    ocurrencias_prereg = []
    for ruta in sorted(glob.glob(GLOB_PREREG_CAJA)):
        ocurrencias_prereg.extend(
            busca_en_prosa(ruta, terminos, _habitante_de_prereg(ruta))
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
