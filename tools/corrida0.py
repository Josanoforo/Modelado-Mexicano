#!/usr/bin/env python3
"""`corrida0` -- CLI del registro GEN2 (PLAN-FINAL-GEN2 v2.0, B-1).

Este archivo nacio en `ACTO GEN2-E2 · C0-A DEMANDA` con un solo subcomando
implementado, `demanda`, y los demas declarados vacios.

`ACTO GEN2-E3 · AUTOMATIZA-GEN2-1` (7/sep/2026) llena SEIS de esos huecos,
`ACTO GEN2-E6 · AUTOMATIZA-GEN2-2` (8/sep/2026) llena dos mas, y
`ACTO GEN2-PRE-E5 · CABLEADO-Y-AUTOMATIZACION-FINAL` (8/sep/2026) añade
`estado` (P1, estado unico de un CALC):

  IMPLEMENTADOS  demanda (E2) · spec-check · negativo · preflight · run ·
                 verify (E3/E3.1) · registro · status (E6) · estado (PRE-E5)
  DECLARADOS Y VACIOS  vigencia · delta  (los llena E7; invocarlos sale con
                       codigo 2 y el rotulo NO-IMPLEMENTADO)

El nucleo de corrida (`preflight` -> `run` -> `verify`) obedece la regla que
firmo la propuesta externa aprobada, verbatim: «El humano decide que medir.
La maquina registra, verifica y conecta mecanicamente lo que efectivamente
ocurrio.» De ahi salen tres propiedades que no son negociables en el codigo
de abajo:

  · Ninguna funcion elige un reactivo, corrige una spec ni convierte un
    NO-ENCONTRADO en hallazgo. `spec-check` SUGIERE (WARN) y sigue diciendo
    FAIL; nunca edita la spec.
  · Los estados no se colapsan. `verify` da REPRODUCE / NO-REPRODUCE /
    NO-EJECUTABLE, y el tercero no es un NO-REPRODUCE piadoso. `preflight`
    reporta el `spec.md` frente a `origin/main` en tres estados
    (EN-MAIN-COINCIDE / EN-MAIN-DISCORDA / NO-EN-MAIN) porque la primera
    corrida de una spec ocurre, por definicion, antes de que este fusionada.
  · A.13: todo negativo declara cuantos archivos y cuantas filas examino el
    comando que lo produjo.

El medidor tiene UNA interfaz, `medir(inputs, contrato) -> {"RESULT-…": valor}`
(plan v2.0 §4, B-1; `contrato` normalizado por `contrato_ejecutable()` desde
`ACTO GEN2-E3-1 · READINESS-DEL-RUNNER`, P2 -- el medidor no abre
`spec.yaml`). Un script que no la exponga es NO-EJECUTABLE: no se adivina
otra entrada ni se llama a `main()` por si acaso.

`demanda` (= C0-A) NO MIDE NADA. Recorre por LECTURA los consumidores
activos del registro GEN1, deriva que resultado habria que volver a medir y
con que corrida, y emite dos TSV derivados. No reconstruye recetas desde
notas (solo lee lo que el propio registro declara en el archivo que lo
sostiene), no escribe `valor_gen2`, y no decide agrupaciones ambiguas: las
lista al final por `stderr` y las cuenta la nota del acto.

Orden de recorrido (fija los ids; dos corridas sobre el mismo SHA dan bytes
identicos):

  (a) cada conducta con `p:` de cada regla de `milpa.src.emisor.cargar_reglas()`
      -- MEDIDO y ASIGNADO, en el orden en que el motor las devuelve;
  (b) coeficientes que `B` lee por `valor_ejecutable` y pares que caen a
      `asignados_coeficiente.detalle` -- misma resolucion que
      `tests/test_matriz_sellados.py`;
  (c) `asignados_probabilidad`;
  (d) cada celda del marco sorteado vigente (v1.3) con su R, su M, su L (las
      dos variantes de corredor que el agregado v1.3 distingue) y el
      agregado por celda como derivado.

Escalera causal (`orden_causal`, 1-7). Es una taxonomia DECLARADA, no una
profundidad inventada; el grafo de `depende_de` se verifica contra ella
(ninguna arista retrocede de peldano) y se verifica aciclico. Dos
consumidores del MISMO valor -- la `p` ASIGNADO de una regla y su entrada en
`asignados_probabilidad` -- caen en el mismo peldano: ahi la garantia
estricta la da la aciclicidad, no la escalera. Cualquiera de las dos
verificaciones que falle => PARO sin escribir nada.

  1 tasa base / `p` de conducta MEDIDO desde microdato
  2 coeficiente de generador medido (beta-sombrero) desde microdato
  3 valor ASIGNADO sin medicion -- no hay corrida posible hasta que haya spec
  4 R por celda (estimacion arbitrada contra microdato)
  5 M por celda (emision del motor; depende de 1)
  6 L por celda (captura de corredor)
  7 agregado por celda (depende de 4, 5 y 6)
"""
from __future__ import annotations

import argparse
import csv
import datetime
import difflib
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml  # noqa: E402

from milpa.src.emisor import cargar_reglas  # noqa: E402

# ACTO GEN2-T9: los seis ejes del vector de atributos de
# `canon/modelo-decision-v4_0.md` §1.1.A se LEEN del modulo que los declara --
# no se re-escriben aqui, que es como dos listas se separan sin que nadie lo
# note. `clases.py` no abre ningun archivo al importarse.
from milpa.src.clases import EJES as EJES_MODELO  # noqa: E402
from milpa.src.clases import EJES_HOGAR as EJES_HOGAR_MODELO  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
TRAMITE = RAIZ / "milpa" / "tramite.yaml"
PROCEDENCIA = RAIZ / "milpa" / "procedencia.yaml"
PROPUESTA = RAIZ / "milpa" / "tramite-ola5-propuesta-v0.yaml"
PREREG = RAIZ / "forense" / "prereg-duelo-v2"
MARCO_VIGENTE = PREREG / "marco-M-sorteado-v1_3.tsv"
AGREGADO_VIGENTE = PREREG / "agregado-v1_3-resultado.json"
SALIDA = RAIZ / "data" / "corrida0"

CABECERA_DERIVADO = "# DERIVADO — NO EDITAR"
NO_DECLARADO = "NO-DECLARADO-EN-EL-REGISTRO"

COLS_RESULTADOS = [
    "resultado_id", "consumidor", "tipo", "valor_legacy", "escala_legacy",
    "clase_legacy", "acto_legacy", "fecha_legacy", "payload_ids_legacy",
    "sha256_legacy", "script_legacy", "spec_legacy", "spec_sha_legacy",
    "receta_legacy", "depende_de", "corrida_natural", "estado", "vigencia",
    "validacion_independiente",
]
COLS_CORRIDAS = [
    "corrida_id", "instrumento", "payload_ids", "medidor_o_spec_candidato",
    "n_resultados", "resultados_ids", "entorno_requerido", "receta",
    "orden_causal",
]

# Peldanos de la escalera causal por tipo de consumidor.
ORDEN_CAUSAL = {
    # 0 · la malla DECLARADA del motor matricial (`ADR-91` M1): los cortes por
    # eje que `pi.construir_pi` exige y las celdas-D del disco. Es estructura,
    # y precede a toda medicion -- por eso peldano 0 y no un peldano nuevo al
    # final: `ACTO GEN2-T9` NO renumera los siete peldanos ya declarados.
    "corte_pi": 0,
    "celda_D": 0,
    "conducta_p_medido": 1,
    # 1 · un momento del catalogo es un estadistico OBSERVADO del instrumento,
    # de la misma naturaleza que una tasa base: mismo peldano.
    "momento": 1,
    "coeficiente_ejecutable": 2,
    # 2 · Theta y B se consumen JUNTOS por `matriz.g(B, theta(x))`: la
    # condicional medida cae en el mismo peldano que el coeficiente medido.
    "condicional_theta": 2,
    "conducta_p_asignado": 3,
    "coeficiente_asignado": 3,
    "asignado_probabilidad": 3,
    "celda_R": 4,
    "celda_M": 5,
    "celda_L": 6,
    "celda_AGREGADO": 7,
}

# Campos de receta que se exigen para llamar OK a una cadena legacy.
CAMPOS_RECETA = ["payload_ids_legacy", "sha256_legacy", "script_legacy",
                 "spec_legacy", "spec_sha_legacy"]

RE_ID_PAYLOAD = re.compile(r"[A-Za-z0-9_.\-]+")
RE_ACTO = re.compile(r"ACTO\s+[A-Z0-9][^,;]*?(?=,|\s+\d{1,2}/|$)")
RE_FECHA = re.compile(r"\b\d{1,2}/[a-z]{3}/\d{4}\b")


# ── utilidades de lectura ──────────────────────────────────────────────────

def _leer_tsv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _json(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def _acto_y_fecha(texto) -> tuple[str, str]:
    """Extrae acto y fecha DE UN TEXTO YA LEIDO del registro.

    No consulta notas ni reconstruye nada: si el campo que sostiene el valor
    no dice acto o fecha, la columna queda NO-DECLARADO.
    """
    if not isinstance(texto, str):
        return NO_DECLARADO, NO_DECLARADO
    acto = RE_ACTO.search(texto)
    fecha = RE_FECHA.search(texto)
    return (acto.group(0).strip() if acto else NO_DECLARADO,
            fecha.group(0) if fecha else NO_DECLARADO)


def _es_id_payload(valor: str) -> bool:
    """Un `payload_manifiesto_id` que no es un id no cuenta como receta.

    Dos entradas de `tramite.yaml` traen prosa en ese campo (declaran que el
    payload NO se localizo). Se copia verbatim a la columna -- este acto no
    edita el registro -- pero no se cuenta como cadena declarada.
    """
    return valor != NO_DECLARADO and bool(RE_ID_PAYLOAD.fullmatch(valor))


def _receta(fila: dict) -> str:
    faltan = [c.replace("_legacy", "") for c in CAMPOS_RECETA
              if fila[c] == NO_DECLARADO]
    if "payload_ids" not in faltan and not _es_id_payload(fila["payload_ids_legacy"]):
        faltan.insert(0, "payload_ids")
    if not faltan:
        return "OK"
    if len(faltan) == len(CAMPOS_RECETA):
        return "SIN-RECETA"
    return "PARCIAL:" + "+".join(faltan)


def _sha_de(ruta: Path) -> str:
    """SHA declarado en un `.sha256` hermano ya commiteado (lectura)."""
    if not ruta.exists():
        return NO_DECLARADO
    primera = ruta.read_text(encoding="utf-8").strip().split()
    return primera[0] if primera else NO_DECLARADO


def _fila(**kw) -> dict:
    fila = {c: NO_DECLARADO for c in COLS_RESULTADOS}
    fila.update(estado="PENDIENTE", vigencia="PENDIENTE",
                validacion_independiente="NO-HECHA", depende_de="")
    fila.update({k: v for k, v in kw.items() if v is not None})
    for c in COLS_RESULTADOS:
        if fila[c] == "" and c not in ("depende_de",):
            fila[c] = NO_DECLARADO
    return fila


# ── (a) conductas con p ────────────────────────────────────────────────────

def _enmiendas_por_conducta(crudo: dict) -> dict[str, dict]:
    """Una `enmienda_*` de `tramite.yaml` declara a que conductas aplica.

    Se lee `aplica_a` tal cual (lista de nombres de conducta) y se prefiere el
    payload/sha de la enmienda sobre el de la regla para esas conductas. Es
    lectura del propio registro, no reconstruccion desde notas.
    """
    mapa = {}
    for clave in sorted(crudo):
        if not clave.startswith("enmienda_"):
            continue
        bloque = crudo[clave]
        if not isinstance(bloque, dict):
            continue
        for conducta in (bloque.get("aplica_a") or []):
            mapa[str(conducta)] = bloque
    return mapa


def _consumidores_conductas(crudo_tramite, ambiguas) -> list[dict]:
    por_id = {r["id"]: r for r in crudo_tramite["reglas"]}
    filas = []
    for regla in cargar_reglas(TRAMITE):
        crudo = por_id[regla.id]
        fuente = crudo.get("fuente") or []
        acto, fecha = _acto_y_fecha(" | ".join(str(f) for f in fuente))
        payload = crudo.get("payload_manifiesto_id") or NO_DECLARADO
        sha = crudo.get("sha256_payload") or NO_DECLARADO
        escala = crudo.get("escala") or (
            "p (proporcion ponderada)" if crudo.get("ic95") else NO_DECLARADO)
        enmiendas = _enmiendas_por_conducta(crudo)
        for salida in regla.entonces:
            if salida.p is None:
                continue
            clase = salida.clase or NO_DECLARADO
            medido = str(clase).startswith("MEDIDO")
            enmienda = enmiendas.get(salida.conducta)
            payload_c = (enmienda or {}).get("payload_manifiesto_id") or payload
            sha_c = (enmienda or {}).get("sha256_payload") or sha
            acto_c, fecha_c = acto, fecha
            if enmienda is not None:
                acto_e, fecha_e = _acto_y_fecha(
                    " | ".join(str(enmienda.get(k, "")) for k in
                               ("sellada_por", "origen")))
                acto_c = acto_e if acto_e != NO_DECLARADO else acto
                fecha_c = fecha_e if fecha_e != NO_DECLARADO else fecha
            filas.append(_fila(
                consumidor=f"milpa/tramite.yaml:{regla.id}:{salida.conducta}",
                tipo="conducta_p_medido" if medido else "conducta_p_asignado",
                valor_legacy=repr(salida.p),
                escala_legacy=escala,
                clase_legacy=clase,
                acto_legacy=acto_c, fecha_legacy=fecha_c,
                payload_ids_legacy=payload_c, sha256_legacy=sha_c,
            ))
        if not medido_alguno(regla) and crudo.get("sha256_payload"):
            ambiguas.append(
                f"{regla.id}: declara sha256_payload pero ninguna conducta "
                f"suya se rotula MEDIDO -- a que corrida pertenece el payload "
                f"no lo dice el registro")
    return filas


def medido_alguno(regla) -> bool:
    return any(str(s.clase or "").startswith("MEDIDO") for s in regla.entonces)


# ── (b) coeficientes ───────────────────────────────────────────────────────

def _consumidores_coeficientes(crudo_proc, ambiguas) -> list[dict]:
    sellados = crudo_proc["coeficientes_generador_sellados"]
    medidos = crudo_proc.get("coeficientes_generador_medidos") or {}
    pares_sellados = {(e["gen"], e["coef"]) for e in sellados}

    asignado_de = {}
    for detalle in crudo_proc["asignados_coeficiente"]["detalle"]:
        for nombre, valor in detalle["coefs"].items():
            asignado_de[(detalle["gen"], nombre)] = valor

    filas = []
    for e in sellados:
        if "valor_ejecutable" not in e:
            ambiguas.append(
                f"coeficiente {e['gen']}.{e['coef']}: sellado sin "
                f"valor_ejecutable -- B no lo lee por override y el registro "
                f"no dice si su corrida es la del sellado o la del fallback")
            continue
        origen = e.get("fuente", "")
        acto, fecha = _acto_y_fecha(str(origen))
        # `fuente` de un sellado apunta a la entrada de
        # coeficientes_generador_medidos que lo sostiene: se lee esa entrada,
        # no se reconstruye desde notas.
        clave = str(origen).split(".", 1)[-1].split(",")[0].strip()
        detalle = medidos.get(clave, {})
        acto_m, fecha_m = _acto_y_fecha(str(detalle.get("fuente", "")))
        filas.append(_fila(
            consumidor=f"milpa/procedencia.yaml:coeficientes_generador_sellados:"
                       f"{e['gen']}.{e['coef']}",
            tipo="coeficiente_ejecutable",
            valor_legacy=repr(e["valor_ejecutable"]),
            escala_legacy=e.get("escala") or NO_DECLARADO,
            clase_legacy=e.get("rotulo") or e.get("clase") or NO_DECLARADO,
            acto_legacy=acto if acto != NO_DECLARADO else acto_m,
            fecha_legacy=fecha if fecha != NO_DECLARADO else fecha_m,
        ))
    for (gen, coef), valor in sorted(asignado_de.items()):
        if (gen, coef) in pares_sellados:
            continue
        filas.append(_fila(
            consumidor=f"milpa/procedencia.yaml:asignados_coeficiente:{gen}.{coef}",
            tipo="coeficiente_asignado",
            valor_legacy=repr(valor),
            escala_legacy=NO_DECLARADO,
            clase_legacy="ASIGNADO",
        ))
    return filas


# ── (c) asignados_probabilidad ─────────────────────────────────────────────

def _consumidores_asignados_prob(crudo_proc, indice_conductas) -> list[dict]:
    filas = []
    for entrada in crudo_proc["asignados_probabilidad"]:
        regla = entrada.get("regla", NO_DECLARADO)
        valores = entrada.get("valores")
        depende = [rid for (rid, cons) in indice_conductas
                   if cons.startswith(f"milpa/tramite.yaml:{regla}:")]
        filas.append(_fila(
            consumidor=f"milpa/procedencia.yaml:asignados_probabilidad:{regla}",
            tipo="asignado_probabilidad",
            valor_legacy=repr(valores) if valores is not None else NO_DECLARADO,
            escala_legacy=NO_DECLARADO,
            clase_legacy="ASIGNADO",
            depende_de=";".join(depende),
        ))
    return filas


# ── (d) celdas del marco sorteado vigente ──────────────────────────────────

def _m_vigente(id_celda: str) -> Path | None:
    """Resolucion declarada: el M de la version del marco vigente gana."""
    for nombre in (f"M-{id_celda}__v1_3.json", f"M-{id_celda}__v1_2.json",
                   f"M-{id_celda}.json"):
        ruta = PREREG / "corridas-M" / nombre
        if ruta.exists():
            return ruta
    return None


def _consumidores_celdas(indice_conductas, ambiguas) -> list[dict]:
    marco = _leer_tsv(MARCO_VIGENTE)
    agregado = _json(AGREGADO_VIGENTE)
    l_spec = PREREG / "L-spec-v1_2.json"
    l_sha = _sha_de(PREREG / "L-spec-v1_2.sha256")
    espec_r = PREREG / "espec-R-ciega-v1_2.tsv"
    filas = []
    for celda in marco:
        cid = celda["id"]
        base = f"forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:{cid}"
        ids_locales = {}

        # R
        ruta_r = PREREG / "corridas-R" / f"{cid}.json"
        r = _json(ruta_r) if ruta_r.exists() else {}
        filas.append(_fila(
            consumidor=f"{base}:R", tipo="celda_R",
            valor_legacy=repr(r.get("R")) if "R" in r else NO_DECLARADO,
            escala_legacy=celda.get("escala") or NO_DECLARADO,
            clase_legacy=r.get("estado") or NO_DECLARADO,
            payload_ids_legacy=r.get("payload_id") or NO_DECLARADO,
            sha256_legacy=r.get("payload_sha256") or NO_DECLARADO,
            script_legacy=r.get("script") or "tools/arbitra.py",
            spec_legacy=(f"forense/prereg-duelo-v2/{espec_r.name}"
                         if espec_r.exists() else NO_DECLARADO),
            spec_sha_legacy=NO_DECLARADO,
        ))
        ids_locales["R"] = len(filas) - 1

        # M
        ruta_m = _m_vigente(cid)
        candidatos = sorted(p.name for p in (PREREG / "corridas-M").glob(f"M-{cid}*.json"))
        if len(candidatos) > 1:
            ambiguas.append(
                f"celda {cid}: {len(candidatos)} archivos M ({', '.join(candidatos)}) "
                f"-- se toma el de la version del marco vigente; el registro no "
                f"declara cual sustituye a cual")
        m = _json(ruta_m) if ruta_m else {}
        acto_m, fecha_m = _acto_y_fecha(str(m.get("fuente", "")))
        dep_m = [rid for (rid, cons) in indice_conductas
                 if cons == f"milpa/tramite.yaml:{m.get('regla')}:{m.get('conducta')}"]
        filas.append(_fila(
            consumidor=f"{base}:M", tipo="celda_M",
            valor_legacy=repr(m.get("valor_punto")) if "valor_punto" in m else NO_DECLARADO,
            escala_legacy=celda.get("escala") or NO_DECLARADO,
            clase_legacy=m.get("clase") or m.get("estado_M") or NO_DECLARADO,
            acto_legacy=acto_m, fecha_legacy=fecha_m,
            script_legacy=m.get("script_invocador") or "tools/emite_m.py",
            depende_de=";".join(dep_m),
        ))
        ids_locales["M"] = len(filas) - 1

        # L, una fila por corredor que el agregado vigente distingue
        celda_agg = agregado.get("celdas", {}).get(cid, {})
        for variante, clave in (("L-solo", "L_solo"), ("L+corpus", "L_corpus")):
            capturas = sorted((PREREG / "corridas-L").glob(
                f"L-{cid}-M__{variante}__*.json"))
            filas.append(_fila(
                consumidor=f"{base}:L:{variante}", tipo="celda_L",
                valor_legacy=repr(celda_agg.get(clave)) if clave in celda_agg
                else NO_DECLARADO,
                escala_legacy=celda.get("escala") or NO_DECLARADO,
                clase_legacy=f"CAPTURA-CORREDOR ({len(capturas)} replicas)",
                script_legacy="forense/prereg-duelo-v2/runner_l_cli.py",
                spec_legacy=(f"forense/prereg-duelo-v2/{l_spec.name}"
                             if l_spec.exists() else NO_DECLARADO),
                spec_sha_legacy=l_sha,
            ))
            ids_locales[variante] = len(filas) - 1

        # agregado por celda (derivado)
        filas.append(_fila(
            consumidor=f"{base}:AGREGADO", tipo="celda_AGREGADO",
            valor_legacy=json.dumps(
                {k: celda_agg[k] for k in sorted(celda_agg)
                 if k.startswith("z_")}, ensure_ascii=False)
            if celda_agg else NO_DECLARADO,
            escala_legacy="z (marcador)",
            clase_legacy="DERIVADO de R, M y L -- sin IC propio",
            script_legacy="forense/prereg-duelo-v2/agregado_v1_3.py",
            depende_de="",  # se completa abajo con los ids ya asignados
        ))
        ids_locales["AGREGADO"] = len(filas) - 1
        filas[ids_locales["AGREGADO"]]["_dep_locales"] = [
            ids_locales[k] for k in ("R", "M", "L-solo", "L+corpus")]
    return filas


# ── ensamblado ─────────────────────────────────────────────────────────────

# ── (e) el MOTOR MATRICIAL · ACTO GEN2-T9, D11 revocada ────────────────────
#
# `ADR-91` (17/ago/2026, `PR #246`), firma de mesa verbatim: «M1 computo
# matricial como definicion del ejecutable». El ejecutable sellado es
# `milpa/src/{motor,matriz,theta,pi,celdas,momentos}.py`, y `C0-A` (`ACTO
# GEN2-E2`) NO lo recorrio: sus 162 filas salieron del emisor y del marcador,
# nunca del motor. `D11` de `ACTO GEN2-E3-1` (`ADR-396`) declaro ese ejecutable
# «scaffold historico» -- dictado contra el arbol, sin cotejarlo con `ADR-91`.
# `ACTO GEN2-T9` lo revoca y cuenta lo que faltaba. NADA SE RECALCULA: estas
# filas se AÑADEN al final, de modo que ningun `RES-` ya emitido cambia de id.
#
# Las cuatro familias se LEEN de los modulos, no de memoria -- exigencia
# literal del encargo. De ahi que los conteos salgan de `celdas.CORTES_C1`,
# `motor.celdas_semilla()`, `momentos.cargar_catalogo()` y del mismo recorrido
# de `procedencia._recorrer` que `theta.Theta.desde` consume.


def _limpia(valor) -> str:
    """Un TSV no admite tabulador ni salto de linea DENTRO de un campo.

    Los `clase:` de `milpa/procedencia.yaml` traen parrafos enteros (`GATE·ID-X`
    arrastra uno) y el `REFUTADO-POR-COTA` arrastra un comentario de tres
    lineas. Se colapsa el blanco; no se trunca el contenido.
    """
    return " ".join(str(valor).split()) or NO_DECLARADO


def _entradas_procedencia(crudo_proc) -> list[tuple[tuple, str]]:
    """`(ruta_yaml, clase_cruda)` por cada entrada con `clase:`.

    Mismo recorrido que `milpa.src.procedencia._recorrer`, reimplementado aqui
    por LECTURA y no importado, por una razon medida y no supuesta: hoy
    `procedencia.cargar()` LANZA `ClaseDesconocida` sobre este mismo archivo
    (dos valores de `clase:` que `milpa/src/clases.py` no conoce --
    `REFUTADO-POR-COTA` y `EVIDENCIA_EXPERIMENTAL_TERCEROS`), y el registro no
    puede quedarse sin contar la demanda del motor porque el cargador del motor
    este roto. El defecto se declara, no se parchea: `milpa/src/**` esta fuera
    del perimetro de `ACTO GEN2-T9` (el motor se corre, no se edita).
    """
    salida: list[tuple[tuple, str]] = []

    def rec(nodo, camino):
        if isinstance(nodo, dict):
            if isinstance(nodo.get("clase"), str):
                salida.append((tuple(str(c) for c in camino), nodo["clase"]))
            for k, v in nodo.items():
                rec(v, camino + [k])
        elif isinstance(nodo, list):
            for i, v in enumerate(nodo):
                rec(v, camino + [i])

    rec(crudo_proc, [])
    return salida


def _consumidores_cortes_pi(ambiguas) -> list[dict]:
    """Un corte por eje de los que `pi.construir_pi` exige sellados.

    `celdas.CORTES_C1` es el dato: cuatro ejes con corte sellado bajo M2 y dos
    `None` -- `edad` y `migracion` -- que el propio modulo declara PENDIENTE
    (`FP-53`) y que `construir_pi` rechaza por `CortesNoSellados`. Los seis
    entran a la demanda: un corte PENDIENTE es demanda no cubierta, que es
    exactamente lo que este TSV existe para contar.
    """
    from milpa.src.celdas import CORTES_C1

    filas = []
    for eje in EJES_MODELO:
        if eje not in CORTES_C1.por_eje:
            ambiguas.append(
                f"corte_pi {eje}: es uno de los seis ejes de §1.1.A pero no "
                f"aparece en `celdas.CORTES_C1.por_eje` -- el registro no "
                f"decide si falta el corte o falta el eje")
            continue
        valor = CORTES_C1.por_eje[eje]
        sellado = valor is not None
        filas.append(_fila(
            consumidor=f"milpa/src/celdas.py:CORTES_C1:{eje}",
            tipo="corte_pi",
            valor_legacy=_limpia(valor) if sellado else NO_DECLARADO,
            escala_legacy=("HOGAR" if eje in EJES_HOGAR_MODELO else "PERSONA"),
            clase_legacy="SELLADO·M2" if sellado else "PENDIENTE·FP-53",
            acto_legacy="ACTO LANE-A-E0-E5 C1",
            script_legacy="milpa/src/pi.py",
            spec_legacy="milpa/src/celdas.py",
        ))
    return filas


def _consumidores_celdas_d(ambiguas) -> list[dict]:
    """Una fila por celda-D del disco. `motor.celdas_semilla()` las enumera."""
    from milpa.src import motor as _motor

    filas = []
    for nombre, celda_d in _motor.celdas_semilla():
        cid = str(celda_d.get("id", NO_DECLARADO))
        estado = str(celda_d.get("estado_operativo", NO_DECLARADO))
        if estado != "LISTO":
            ambiguas.append(
                f"celda_D {cid}: `estado_operativo` = {estado} -- el registro "
                f"no decide si su corrida es exigible hoy")
        filas.append(_fila(
            consumidor=f"data/curacion-registro/celdas-d/{nombre}:{cid}",
            tipo="celda_D",
            valor_legacy=NO_DECLARADO,
            escala_legacy=_limpia(celda_d.get("nivel", NO_DECLARADO)),
            clase_legacy=_limpia(celda_d.get("tipo_adjudicacion", NO_DECLARADO)),
            acto_legacy=_limpia(celda_d.get("estado_operativo", NO_DECLARADO)),
            script_legacy="milpa/src/motor.py",
            spec_legacy=f"data/curacion-registro/celdas-d/{nombre}",
        ))
    return filas


def _consumidores_momentos(ambiguas) -> list[dict]:
    """Una fila por momento del catalogo sellado, con su `rol_calibracion`.

    El muro `AJUSTE`/`HOLDOUT` viaja en la fila (`clase_legacy`): un `HOLDOUT`
    esta en la demanda -- hay que medirlo alguna vez -- pero `momentos.valor_de`
    lanza si se lee hoy, y eso es el pre-registro, no un hueco del registro.
    """
    from milpa.src import momentos as _momentos

    catalogo = _momentos.cargar_catalogo()
    filas = []
    for m in catalogo.momentos:
        if m.estatus_disponibilidad and "POR DECLARAR" in m.estatus_disponibilidad.upper():
            ambiguas.append(
                f"momento {m.id_momento}: `universo_candidatos` POR DECLARAR "
                f"-- el registro no elige el reactivo")
        filas.append(_fila(
            consumidor=f"milpa/catalogo-momentos-v0_1.tsv:{m.id_momento}",
            tipo="momento",
            valor_legacy=NO_DECLARADO,
            escala_legacy=_limpia(m.nivel),
            clase_legacy=_limpia(m.rol_calibracion),
            acto_legacy=_limpia(m.objeto_modelo),
            # `universo_instrumento` NO es un `payload_manifiesto_id` y no se
            # mete en esa columna: es la declaracion del universo, no la del
            # payload. Viaja aparte y `_instrumento()` la lee para agrupar la
            # corrida -- meterla en `payload_ids_legacy` habria producido 22
            # falsas "ambiguedades de payload" sobre un campo que nunca
            # pretendio ser un id.
            _instrumento_declarado=_limpia(m.universo_instrumento),
            script_legacy="milpa/src/momentos.py",
            spec_legacy="milpa/catalogo-momentos-v0_1.tsv",
        ))
    return filas


def _consumidores_theta(crudo_proc, indice_cortes, ambiguas) -> list[dict]:
    """Una fila por condicional Theta MEDIDA sobre atributos, con clase y eje.

    El numerador es el de la FORMULA OFICIAL, no uno nuevo:
    `procedencia.contador_condicionales_medidas()` cuenta exactamente las dos
    clases `MEDIDO·PARCIAL` y `MEDIDO·NACIONAL`, y `tests/check.py` (T19b/T19c)
    deriva la misma cifra sobre texto crudo. Aqui se emite UNA FILA por cada
    una de esas entradas -- ni una mas.

    `depende_de`: una `MEDIDO·PARCIAL(x)` no puede segmentarse por un eje cuyo
    corte no este sellado (`procedencia.segmentar` -> `EjeNoDeclarado`), asi
    que la fila depende de la fila `corte_pi` de cada eje que declara. Es una
    arista LEIDA del contrato, no una inventada.
    """
    from milpa.src.clases import Clase, clasificar, ejes_declarados

    filas = []
    for camino, crudo in _entradas_procedencia(crudo_proc):
        try:
            clase, _ = clasificar(crudo)
        except Exception:
            # Una `clase:` que `milpa/src/clases.py` no conoce NO se adivina y
            # NO se cuenta como Theta: se lista y sigue.
            ambiguas.append(
                f"condicional_theta {'/'.join(camino)}: `clase:` "
                f"{_limpia(crudo)[:60]!r} no casa con ningun prefijo de "
                f"`milpa/src/clases.py` -- `procedencia.cargar()` LANZA sobre "
                f"ella y el motor no arranca")
            continue
        if clase not in (Clase.MEDIDO_PARCIAL, Clase.MEDIDO_NACIONAL):
            continue
        ejes = ejes_declarados(crudo)
        deps = [indice_cortes[e] for e in ejes if e in indice_cortes]
        faltantes = [e for e in ejes if e not in indice_cortes]
        if faltantes:
            ambiguas.append(
                f"condicional_theta {'/'.join(camino)}: declara los ejes "
                f"{faltantes} que no tienen fila `corte_pi` -- el registro no "
                f"decide si el eje sobra en la clase o falta en los cortes")
        filas.append(_fila(
            consumidor=f"milpa/procedencia.yaml:{'/'.join(camino)}",
            tipo="condicional_theta",
            valor_legacy=NO_DECLARADO,
            escala_legacy=(",".join(ejes) if ejes else "x = 0/vacio (NACIONAL)"),
            clase_legacy=_limpia(crudo)[:200],
            script_legacy="milpa/src/theta.py",
            spec_legacy="milpa/procedencia.yaml",
            depende_de=";".join(deps),
        ))
    return filas


def _asigna_ids(filas: list[dict]) -> None:
    for i, fila in enumerate(filas, start=1):
        fila["resultado_id"] = f"RES-{i:04d}"


def _resuelve_dependencias_locales(filas: list[dict]) -> None:
    for fila in filas:
        locales = fila.pop("_dep_locales", None)
        if locales:
            fila["depende_de"] = ";".join(filas[i]["resultado_id"] for i in locales)


def _verifica_grafo(filas: list[dict]) -> None:
    por_id = {f["resultado_id"]: f for f in filas}
    for fila in filas:
        for dep in filter(None, fila["depende_de"].split(";")):
            if dep not in por_id:
                raise SystemExit(
                    f"PARO: {fila['resultado_id']} depende de {dep}, que no existe")
            if ORDEN_CAUSAL[por_id[dep]["tipo"]] > ORDEN_CAUSAL[fila["tipo"]]:
                raise SystemExit(
                    f"PARO: arista {dep} -> {fila['resultado_id']} retrocede en la "
                    f"escalera causal declarada (peldanos "
                    f"{ORDEN_CAUSAL[por_id[dep]['tipo']]} -> "
                    f"{ORDEN_CAUSAL[fila['tipo']]})")
    # Aciclico: DFS con marcas.
    estado = {}

    def visita(nid, pila):
        if estado.get(nid) == "listo":
            return
        if estado.get(nid) == "en-curso":
            raise SystemExit("PARO: ciclo en depende_de -> " + " -> ".join(pila + [nid]))
        estado[nid] = "en-curso"
        for dep in filter(None, por_id[nid]["depende_de"].split(";")):
            visita(dep, pila + [nid])
        estado[nid] = "listo"

    for fila in filas:
        visita(fila["resultado_id"], [])


def _instrumento(fila: dict, crudo_tramite, marco_por_consumidor) -> str:
    # ACTO GEN2-T9: un momento del catalogo declara su propio universo de
    # instrumento; es lo que agrupa su corrida.
    if fila["tipo"] == "momento":
        return fila.get("_instrumento_declarado", NO_DECLARADO)
    if fila["tipo"].startswith("celda_") and fila["tipo"] != "celda_D":
        return marco_por_consumidor.get(fila["consumidor"].split(":")[1],
                                        NO_DECLARADO)
    if fila["tipo"].startswith("conducta_"):
        rid = fila["consumidor"].split(":")[1]
        for r in crudo_tramite["reglas"]:
            if r["id"] == rid:
                fuentes = [str(f) for f in (r.get("fuente") or [])]
                for f in fuentes:
                    if re.fullmatch(r"[A-Z][A-Z0-9]{2,}[0-9]{4}", f):
                        return f
                return fuentes[0] if fuentes else NO_DECLARADO
    return NO_DECLARADO


def _entorno(fila: dict) -> str:
    """Derivado: un payload declarado exige la caja; lo que solo relee el
    repo cabe en la nube; sin ninguna de las dos cosas, el registro no lo
    decide."""
    peldano = ORDEN_CAUSAL[fila["tipo"]]
    if _es_id_payload(fila["payload_ids_legacy"]):
        return "CAJA"
    if peldano in (5, 6, 7):
        return "NUBE"
    if peldano == 3:
        return "INDECIDIBLE-SIN-SPEC"
    return "INDECIDIBLE-SIN-PAYLOAD-DECLARADO"


PEOR_RECETA = {"OK": 0, "PARCIAL": 1, "SIN-RECETA": 2}


def _peor(recetas: list[str]) -> str:
    return max(recetas, key=lambda r: (PEOR_RECETA[r.split(":")[0]], r))


def _corridas(filas: list[dict], crudo_tramite, marco_por_consumidor) -> list[dict]:
    grupos: dict[tuple, list[dict]] = {}
    orden: list[tuple] = []
    for fila in filas:
        clave = (ORDEN_CAUSAL[fila["tipo"]],
                 _instrumento(fila, crudo_tramite, marco_por_consumidor),
                 fila["payload_ids_legacy"],
                 fila["spec_legacy"],
                 fila["script_legacy"])
        if clave not in grupos:
            grupos[clave] = []
            orden.append(clave)
        grupos[clave].append(fila)

    corridas = []
    for i, clave in enumerate(orden, start=1):
        peldano, instrumento, payload, spec, script = clave
        miembros = grupos[clave]
        cid = f"CORR-{i:04d}"
        for fila in miembros:
            fila["corrida_natural"] = cid
        candidato = script if script != NO_DECLARADO else spec
        corridas.append({
            "corrida_id": cid,
            "instrumento": instrumento,
            "payload_ids": payload,
            "medidor_o_spec_candidato": candidato if candidato != NO_DECLARADO
            else "SIN-CANDIDATO-EN-EL-REGISTRO",
            "n_resultados": len(miembros),
            "resultados_ids": ";".join(f["resultado_id"] for f in miembros),
            "entorno_requerido": _entorno(miembros[0]),
            "receta": _peor([f["receta_legacy"] for f in miembros]),
            "orden_causal": peldano,
        })
    return corridas


def _escribe(ruta: Path, columnas: list[str], filas: list[dict]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(CABECERA_DERIVADO + "\n")
        fh.write("\t".join(columnas) + "\n")
        for fila in filas:
            fh.write("\t".join(str(fila[c]) for c in columnas) + "\n")


# ── subcomando `demanda` ───────────────────────────────────────────────────

DECISIONES = SALIDA / "decisiones.tsv"


def _firma_de_decision(objeto: str) -> str:
    """La firma de mesa bajo la que se decidio `objeto`, leida de la columna
    `fuente` de `decisiones.tsv`. No se infiere del nombre del objeto."""
    if not DECISIONES.exists():
        return NO_DECLARADO
    for f in _leer_tsv(DECISIONES):
        if f["objeto"] == objeto:
            return (f.get("fuente") or NO_DECLARADO).split("(")[0].strip()
    return NO_DECLARADO


def _lee_decisiones() -> dict:
    """Lee `data/corrida0/decisiones.tsv` (edicion manual de mesa, D9/D10 ·
    FP-339): objeto -> decision. Un objeto ausente del archivo sigue sin
    decidir -- `cmd_demanda` no inventa decisiones que mesa no firmo."""
    if not DECISIONES.exists():
        return {}
    return {f["objeto"]: f["decision"] for f in _leer_tsv(DECISIONES)}


def cmd_demanda(args) -> int:
    crudo_tramite = yaml.safe_load(TRAMITE.read_text(encoding="utf-8"))
    crudo_proc = yaml.safe_load(PROCEDENCIA.read_text(encoding="utf-8"))
    ambiguas: list[str] = []

    filas = _consumidores_conductas(crudo_tramite, ambiguas)
    _asigna_ids(filas)
    indice_conductas = [(f["resultado_id"], f["consumidor"]) for f in filas]

    filas += _consumidores_coeficientes(crudo_proc, ambiguas)
    filas += _consumidores_asignados_prob(crudo_proc, indice_conductas)
    filas += _consumidores_celdas(indice_conductas, ambiguas)

    # (e) ACTO GEN2-T9 · el motor matricial de `ADR-91`, que `C0-A` no
    # recorrio. Se AÑADE al final a proposito: asi ningun `RES-` ya emitido
    # cambia de id -- «nada se recalcula: solo se cuenta lo que faltaba».
    filas += _consumidores_cortes_pi(ambiguas)
    filas += _consumidores_celdas_d(ambiguas)
    filas += _consumidores_momentos(ambiguas)
    _asigna_ids(filas)
    indice_cortes = {
        f["consumidor"].rsplit(":", 1)[1]: f["resultado_id"]
        for f in filas if f["tipo"] == "corte_pi"}
    filas += _consumidores_theta(crudo_proc, indice_cortes, ambiguas)

    _asigna_ids(filas)
    _resuelve_dependencias_locales(filas)

    for fila in filas:
        fila["receta_legacy"] = _receta(fila)

    # D10 · FP-339 (mesa, FIRMADA 2026-09-07): estas celdas quedan
    # SIN-RECETA por decision -- no se reconstruyen aunque algun campo
    # legacy este declarado -- la decision de decisiones.tsv PISA la
    # receta calculada por `_receta` (que aqui vendria PARCIAL).
    decisiones = _lee_decisiones()
    for fila in filas:
        if decisiones.get(fila["consumidor"]) == "receta_legacy=SIN-RECETA":
            fila["receta_legacy"] = "SIN-RECETA"

    _verifica_grafo(filas)

    ids_manifiesto = {e.get("id") for e in
                      yaml.safe_load((RAIZ / "data" / "manifiesto.yaml")
                                     .read_text(encoding="utf-8"))
                      if isinstance(e, dict)}
    for fila in filas:
        valor = fila["payload_ids_legacy"]
        if valor == NO_DECLARADO:
            continue
        if not _es_id_payload(valor):
            ambiguas.append(
                f"{fila['resultado_id']} ({fila['consumidor']}): "
                f"payload_manifiesto_id no es un id, es prosa -- "
                f"a que payload apunta la corrida no lo decide el registro")
        elif valor not in ids_manifiesto:
            ambiguas.append(
                f"{fila['resultado_id']} ({fila['consumidor']}): payload "
                f"'{valor}' no esta en data/manifiesto.yaml")

    # D9/D10 · FP-339 (mesa, FIRMADA 2026-09-07): decisiones.tsv resuelve
    # exactamente los 7 casos que este subcomando listaba como ambiguos --
    # (1)-(3) el M vivo de TRA-M-02/03/07 es el __v1_3 (ya la regla del
    # codigo, ahora tambien DECLARADA en el registro); (4)-(7) las celdas
    # DIN/FAM de dinero.ahorro.tiene_ahorros y familia.apoyo.recibe_dinero_
    # familiares quedan SIN-RECETA por decision de mesa, no se reconstruyen.
    # Lo que decisiones.tsv NO cubre sigue listandose como ambiguo: este
    # subcomando sigue sin decidir nada por su cuenta.
    def _decidida(linea: str) -> bool:
        for objeto, decision in decisiones.items():
            if decision == "M_vivo=__v1_3" and linea.startswith(f"celda {objeto}:"):
                return True
            if decision == "receta_legacy=SIN-RECETA" and f"({objeto}):" in linea:
                return True
        return False

    ambiguas = [linea for linea in ambiguas if not _decidida(linea)]

    marco_por_consumidor = {
        c["id"]: f"{c['encuesta']} {c['ola']}" for c in _leer_tsv(MARCO_VIGENTE)}
    corridas = _corridas(filas, crudo_tramite, marco_por_consumidor)

    _escribe(SALIDA / "demanda-resultados.tsv", COLS_RESULTADOS, filas)
    _escribe(SALIDA / "demanda-corridas.tsv", COLS_CORRIDAS, corridas)

    payloads = sorted({f["payload_ids_legacy"] for f in filas
                       if _es_id_payload(f["payload_ids_legacy"])})
    print(f"N_resultados_activos = {len(filas)}")
    print(f"N_corridas_requeridas = {len(corridas)}")
    print(f"N_resultados_pendientes = "
          f"{sum(1 for f in filas if f['estado'] == 'PENDIENTE')}")
    print(f"clausura_activa_de_payloads = {len(payloads)}")
    if decisiones:
        # ACTO GEN2-T9: `decisiones.tsv` dejo de ser la tabla de UNA firma
        # (FP-339) para ser la tabla de las firmas de mesa sobre objetos del
        # registro -- D-1 añadio las suyas. El contador se declara generico y
        # con desglose, en vez de rotularlo con una sola firma que ya no lo
        # describe.
        print(f"decisiones_aplicadas = {len(decisiones)}")
        for firma in sorted({_firma_de_decision(o) for o in decisiones}):
            n = sum(1 for o in decisiones if _firma_de_decision(o) == firma)
            print(f"decisiones_aplicadas[{firma}] = {n}")
    if ambiguas:
        print("\nAGRUPACIONES / RESOLUCIONES QUE EL REGISTRO NO DECIDE "
              f"({len(ambiguas)}) -- se listan, no se deciden:", file=sys.stderr)
        for linea in ambiguas:
            print("  - " + linea, file=sys.stderr)
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# GEN2-E3 · nucleo de corrida: preflight / run / verify + spec-check +
# negativo (ACTO GEN2-E3 · AUTOMATIZA-GEN2-1, plan v2.0 §4/§8 Fase I).
#
# Regla que gobierna todo lo de abajo, verbatim de la propuesta aprobada:
# «El humano decide que medir. La maquina registra, verifica y conecta
# mecanicamente lo que efectivamente ocurrio.» Ninguna funcion de aqui
# elige un reactivo, corrige una spec, ni convierte un NO-ENCONTRADO en
# hallazgo: cuando el registro no alcanza, se DECLARA el hueco.
# ═══════════════════════════════════════════════════════════════════════════

CORRIDAS = RAIZ / "data" / "corrida0"

# Los TRES inventarios canonicos VIGENTES. `v1_0`/`v1_1` estan superados y
# NO se consultan: leer un inventario superado es exactamente la clase de
# error que `spec-check` existe para no cometer.
INVENTARIOS_VIGENTES = [
    RAIZ / "data" / "inventario-reactivos-v1_2.tsv",
    RAIZ / "data" / "inventario-reactivos-descargas-mx-v1_2.tsv",
    RAIZ / "data" / "inventario-reactivos-ext-v1_0.tsv",
]

# Tolerancia por defecto para flotantes (encargo P1). Los enteros se
# comparan EXACTO; `bootstrap` solo se declara exacto cuando la spec fija
# seed + RNG + codigo, y si no, cae a la tolerancia absoluta declarada.
TOL_FLOTANTE_DEFECTO = 1e-10

SELLA_PY = RAIZ / "tools" / "sella_sha256.py"
ENTORNO_PY = RAIZ / "tools" / "entorno.py"

# P1 (ACTO GEN2-E3-1 · READINESS-DEL-RUNNER): resolver unico de payload,
# importado DIRECTO -- mismo patron que `tests/corpus.py` ya usa para
# reutilizar `tests/manifiesto.py` -- nunca por subproceso. El objeto que
# devuelve (`ruta_absoluta`, `sha256`, `raiz_logica`) es el mismo que
# alimenta al medidor: ningun medidor busca su propio payload por su cuenta.
sys.path.insert(0, str(RAIZ / "tests"))
import payload_resolver as _PR  # noqa: E402

CAMPOS_SPEC_OBLIGATORIOS = ["calc_id", "spec_md", "spec_md_sha256", "script",
                            "inputs", "parametros", "seed", "tolerancia",
                            "resultados"]

# P3 (ACTO GEN2-E3-1): los cuatro tipos de RESULT que un `spec.yaml`
# endurecido puede declarar. Cerrado, sin JSON Schema universal.
TIPOS_VALIDOS_RESULT = {"entero", "flotante", "proporcion", "texto"}

# P2 (ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER): las dimensiones
# sustantivas que una spec del esquema endurecido declara EXPLICITAMENTE.
# El valor puede ser `NO-APLICA` -- lo que no puede es faltar. Antes de este
# acto, `contrato_ejecutable()` rellenaba con `"NO-APLICA"` por omision, y un
# campo OLVIDADO quedaba indistinguible de un `NO-APLICA` DECLARADO.
DIMENSIONES_SUSTANTIVAS = ["variables", "universo", "filtros", "ponderador",
                           "transformacion", "estimando", "parametros", "seed",
                           "dependencias_materiales", "resultados", "tolerancia"]

# Compatibilidad de lectura, EXPLICITA y por marca ya existente en el arbol
# (no un esquema nuevo): las specs legado traen `etiquetas.generacion:
# LEGACY-GEN1` -- es lo que `CALC-SMOKE-0001` y `CALC-SMOKE-0002` ya declaran,
# ambas selladas. Solo esas quedan exentas del endurecimiento P2/P3; toda
# spec nueva que pretenda `PRE-FLIGHT: VERDE` declara sus dimensiones.
GENERACION_LEGADO = "LEGACY-GEN1"


def _esquema_endurecido(spec: dict) -> bool:
    """VERDADERO salvo que la spec se declare legado por su propia etiqueta.
    El default es el esquema endurecido: una spec que no dice nada es nueva."""
    etiquetas = spec.get("etiquetas") or {}
    return str(etiquetas.get("generacion", "")) != GENERACION_LEGADO


class BloqueoPreflight(Exception):
    """Se levanta solo dentro de `preflight` para cortar sin escribir."""


# ── utilidades comunes ─────────────────────────────────────────────────────

def _sha256_archivo(ruta: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with ruta.open("rb") as fh:
            for bloque in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloque)
        return h.hexdigest()
    except OSError:
        return None


def _git_salida(*args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True,
                           text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        return 1, f"ERROR:{type(exc).__name__}"
    return r.returncode, (r.stdout if r.returncode == 0 else r.stderr)


def _sha256_blob_en(ref: str, ruta_rel: str) -> str | None:
    """sha256 del CONTENIDO que `ref` tiene en `ruta_rel` (no el blob-sha de
    git, que es sha1 con cabecera: dos hashes distintos y no intercambiables)."""
    try:
        r = subprocess.run(["git", "show", f"{ref}:{ruta_rel}"], cwd=RAIZ,
                           capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):  # pragma: no cover
        return None
    if r.returncode != 0:
        return None
    return hashlib.sha256(r.stdout).hexdigest()


def _rel(ruta: Path) -> str:
    try:
        return str(ruta.resolve().relative_to(RAIZ))
    except ValueError:
        return str(ruta)


def _dir_calc(calc_id: str) -> Path:
    return CORRIDAS / calc_id


def _carga_spec(calc_id: str) -> tuple[Path, dict]:
    d = _dir_calc(calc_id)
    ruta = d / "spec.yaml"
    if not ruta.exists():
        raise BloqueoPreflight(f"spec_yaml_ausente={_rel(ruta)}")
    with ruta.open(encoding="utf-8") as fh:
        datos = yaml.safe_load(fh) or {}
    if not isinstance(datos, dict):
        raise BloqueoPreflight(f"spec_yaml_no_es_mapa={_rel(ruta)}")
    return d, datos


def _distancia_edicion(a: str, b: str) -> int:
    """Levenshtein sin dependencias. Solo se usa para SUGERIR (WARN); una
    sugerencia nunca se da por hallada ni edita la spec."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    previa = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        actual = [i]
        for j, cb in enumerate(b, 1):
            actual.append(min(previa[j] + 1, actual[j - 1] + 1,
                              previa[j - 1] + (ca != cb)))
        previa = actual
    return previa[-1]


# ── inventarios (P2/P3) ────────────────────────────────────────────────────

_CACHE_INVENTARIO: dict[tuple, list[dict]] = {}


def _lee_inventario(ruta: Path) -> list[dict]:
    """Un inventario a filas. Se parte por tabulador a mano en vez de con
    `csv.DictReader`: son ~318 000 filas entre los tres vigentes y el
    DictReader multiplica por seis el costo de una lectura que la suite hace
    en cada corrida. El formato lo permite -- estos TSV no traen comillas de
    citacion (`csv` no aporta nada que ganar aqui), y una fila con un numero
    de campos distinto al de la cabecera se DECLARA truncada/rellenada, no se
    descarta en silencio."""
    if not ruta.exists():
        return []
    etiqueta = _rel(ruta)
    filas: list[dict] = []
    with ruta.open(encoding="utf-8") as fh:
        cabecera = None
        for linea in fh:
            if linea.startswith("#"):
                continue
            campos = linea.rstrip("\n").split("\t")
            if cabecera is None:
                cabecera = campos
                continue
            if len(campos) < len(cabecera):
                campos += [""] * (len(cabecera) - len(campos))
            fila = dict(zip(cabecera, campos))
            fila["_inventario"] = etiqueta
            filas.append(fila)
    return filas


def _filas_inventario(rutas=None):
    """Filas de los inventarios VIGENTES, con `_inventario` anotado. No abre
    microdato: un inventario es metadato de reactivo.

    Cachea por juego de rutas dentro del proceso. Es cache de LECTURA de
    archivos versionados durante una sola invocacion -- nadie los reescribe a
    media corrida -- y sin ella `tests/check.py` releeria 318 000 filas una
    vez por caso de prueba."""
    llave = tuple(str(r) for r in (rutas or INVENTARIOS_VIGENTES))
    if llave not in _CACHE_INVENTARIO:
        filas: list[dict] = []
        for ruta in (rutas or INVENTARIOS_VIGENTES):
            filas.extend(_lee_inventario(Path(ruta)))
        _CACHE_INVENTARIO[llave] = filas
    return iter(_CACHE_INVENTARIO[llave])


def _basename(valor: str) -> str:
    return (valor or "").replace("\\", "/").rsplit("/", 1)[-1]


def _mismo_archivo(archivo_miembro: str, declarado: str) -> bool:
    """El archivo de la spec identifica una fila del inventario si es la ruta
    completa o un SUFIJO DE RUTA de `archivo_miembro`. Declarar `iiib_hs.dta`
    alcanza las tres olas que traen ese miembro (y las etiquetas distintas de
    cada una salen a la vista); declarar `ehh05dta_b3b/iiib_hs.dta` alcanza
    solo la de 2005. Nunca es coincidencia parcial de nombre: el corte es por
    separador de ruta."""
    a = (archivo_miembro or "").replace("\\", "/")
    b = (declarado or "").replace("\\", "/").strip("/")
    return bool(b) and (a == b or a.endswith("/" + b))


# ═══════════════ P2 · spec-check ═══════════════════════════════════════════

def spec_check(calc_id: str, universo=None) -> dict:
    """Para cada (archivo, variable) que la spec declara, consulta SOLO los
    inventarios canonicos vigentes.

    FAIL si la variable no existe EN ESE ARCHIVO EXACTO -- que exista en otro
    archivo del mismo instrumento no la da por hallada: el defecto que este
    check persigue es justamente ese (`iiib_hs.dta::hs02g` es `b3b` y
    `p_hs.dta::hs02g` es `bx`; mismo nombre de variable, etiqueta distinta,
    archivos distintos).

    WARN, nunca hallazgo: la etiqueta mas cercana por distancia de edicion
    <= 2 se SUGIERE (`IMMS` -> «¿IMSS?») y ahi se acaba -- no se da por
    hallada, no se edita la spec, no se sustituye en el resultado."""
    _d, spec = _carga_spec(calc_id)
    declaradas = spec.get("variables") or []
    filas = list(_filas_inventario(universo))
    print(f"SPEC-CHECK {calc_id}")
    print(f"  inventarios consultados ({len(INVENTARIOS_VIGENTES)}) -- solo los "
          f"vigentes, nunca v1_0/v1_1 superados:")
    from collections import Counter as _Counter
    por_inventario = _Counter(f["_inventario"] for f in filas)
    for inv in INVENTARIOS_VIGENTES:
        etiqueta = _rel(Path(inv))
        print(f"    {etiqueta}: {por_inventario.get(etiqueta, 0)} filas" +
              ("" if Path(inv).exists() else "   [AUSENTE EN ESTE ARBOL]"))
    print(f"  filas examinadas (A.13): {len(filas)}")
    print(f"  pares (archivo, variable) declarados en la spec: {len(declaradas)}")

    # instrumento -> secciones (basenames de archivo_miembro) presentes en el
    # inventario. Una pasada, no una por par declarado.
    por_instrumento: dict[str, set] = {}
    for f in filas:
        por_instrumento.setdefault(f.get("instrumento", ""), set()).add(
            _basename(f.get("archivo_miembro")))

    resultados = []
    for par in declaradas:
        archivo = str(par.get("archivo", ""))
        variable = str(par.get("variable", ""))
        patron = f"archivo_miembro basename == {archivo!r} AND variable_id == {variable!r} (exacto, sin normalizar)"
        del_archivo = [f for f in filas
                       if _mismo_archivo(f.get("archivo_miembro"), archivo)]
        exactas = [f for f in del_archivo if (f.get("variable_id") or "") == variable]
        item = {"archivo": archivo, "variable": variable, "patron": patron,
                "filas_examinadas": len(filas),
                "filas_del_archivo": len(del_archivo)}
        if exactas:
            etiquetas = sorted({(f.get("texto_reactivo") or "").strip() for f in exactas})
            item["estado"] = "OK"
            item["etiqueta"] = etiquetas[0] if len(etiquetas) == 1 else etiquetas
            item["instrumento"] = sorted({f.get("instrumento", "") for f in exactas})
            print(f"\n  [ OK ] {archivo} :: {variable}")
            print(f"         patron: {patron}")
            print(f"         filas del archivo en inventario: {len(del_archivo)}")
            for e in etiquetas:
                print(f"         etiqueta: {e[:200]}")
            for inst in item["instrumento"]:
                print(f"         instrumento: {inst}")
        else:
            item["estado"] = "FAIL"
            cercanas = sorted(
                ({(f.get("variable_id") or "") for f in del_archivo}),
                key=lambda v: (_distancia_edicion(v.upper(), variable.upper()), v))
            sugeridas = [v for v in cercanas
                         if _distancia_edicion(v.upper(), variable.upper()) <= 2]
            item["sugerencias_warn"] = sugeridas[:5]
            print(f"\n  [FAIL] {archivo} :: {variable} -- NO EXISTE en ese archivo exacto")
            print(f"         patron: {patron}")
            print(f"         filas del archivo en inventario: {len(del_archivo)}")
            if sugeridas:
                for v in sugeridas[:5]:
                    texto = next((f.get("texto_reactivo") or "" for f in del_archivo
                                  if f.get("variable_id") == v), "")
                    print(f"         [WARN] ¿{v}?  (distancia "
                          f"{_distancia_edicion(v.upper(), variable.upper())}) "
                          f"-- SUGERENCIA, no se da por hallada ni se edita la spec")
                    if texto:
                        print(f"                etiqueta de la sugerencia: {texto[:180]}")
            else:
                print("         [WARN] ninguna variable a distancia <= 2 en ese archivo")
        # Las secciones del instrumento presentes en el inventario -- para que
        # el FAIL diga contra que universo se midio, no solo que fallo. El
        # indice se construye UNA vez para todos los pares (abajo): recorrer
        # 318 000 filas por par declarado hacia que un spec-check de dos
        # lineas costara medio minuto.
        insts = sorted({f.get("instrumento", "") for f in del_archivo})
        secciones = sorted({s for i in insts for s in por_instrumento.get(i, ())})
        item["secciones_del_instrumento"] = secciones
        if secciones:
            print(f"         secciones del instrumento en el inventario ({len(secciones)}): "
                  + ", ".join(secciones[:40]) + (" …" if len(secciones) > 40 else ""))
        resultados.append(item)

    n_fail = sum(1 for r in resultados if r["estado"] == "FAIL")
    print(f"\nSPEC-CHECK: {len(resultados) - n_fail} OK · {n_fail} FAIL "
          f"· {len(filas)} filas examinadas")
    return {"calc_id": calc_id, "items": resultados, "n_fail": n_fail,
            "filas_examinadas": len(filas)}


def cmd_spec_check(args) -> int:
    try:
        r = spec_check(args.calc_id)
    except BloqueoPreflight as exc:
        print(f"SPEC-CHECK: NO-EJECUTABLE {exc}", file=sys.stderr)
        return 2
    return 1 if r["n_fail"] else 0


# ═══════════════ P3 · negativo ═════════════════════════════════════════════

def negativo(patron: str, archivos: str | None = None, universo=None) -> dict:
    """Barrido declarativo (generaliza `tools/barrido_negativos_m38.py`).

    A.13 verbatim: un negativo producido por un comando que no examino
    archivos no es un negativo. Por eso esta funcion imprime SIEMPRE el
    patron, el universo, cuantos archivos y cuantas filas examino, y la
    linea lista para pegar en el recibo -- tambien (y sobre todo) cuando el
    resultado es cero aciertos."""
    filas = list(_filas_inventario(universo))
    rp = re.compile(patron, re.IGNORECASE)
    ra = re.compile(archivos, re.IGNORECASE) if archivos else None
    if ra is not None:
        filas = [f for f in filas if ra.search(f.get("archivo_miembro") or "")]
    archivos_vistos = sorted({f.get("archivo_miembro") or "" for f in filas})
    aciertos = [f for f in filas
                if rp.search(f.get("variable_id") or "")
                or rp.search(f.get("texto_reactivo") or "")]

    print(f"NEGATIVO · patron: {patron}")
    print(f"  universo: {len(INVENTARIOS_VIGENTES)} inventarios vigentes")
    for inv in INVENTARIOS_VIGENTES:
        print(f"    {_rel(Path(inv))}" +
              ("" if Path(inv).exists() else "   [AUSENTE EN ESTE ARBOL]"))
    print(f"  filtro de archivos: {archivos or '(ninguno -- todo el universo)'}")
    print(f"  archivos examinados: {len(archivos_vistos)}")
    print(f"  filas examinadas: {len(filas)}")
    print(f"  aciertos: {len(aciertos)}")
    for f in aciertos[:200]:
        print(f"    {f['_inventario']} :: {f.get('instrumento','')} :: "
              f"{f.get('archivo_miembro','')} :: {f.get('variable_id','')}"
              f"\t{(f.get('texto_reactivo') or '')[:160]}")
    if len(aciertos) > 200:
        print(f"    … y {len(aciertos) - 200} aciertos mas (no truncados en el JSON)")
    veredicto = "SIN-COBERTURA" if not aciertos else "CON-ACIERTOS"
    linea = (f"{veredicto} · patron={patron} · filtro_archivos={archivos or 'TODOS'}"
             f" · inventarios={len(INVENTARIOS_VIGENTES)} vigentes"
             f" · archivos_examinados={len(archivos_vistos)}"
             f" · filas_examinadas={len(filas)} · aciertos={len(aciertos)}")
    print("\nLINEA PARA EL RECIBO (A.13):")
    print(f"  {linea}")
    return {"patron": patron, "filtro_archivos": archivos,
            "archivos_examinados": len(archivos_vistos),
            "filas_examinadas": len(filas), "aciertos": len(aciertos),
            "veredicto": veredicto, "linea_recibo": linea,
            "detalle": [{k: v for k, v in f.items()} for f in aciertos]}


def cmd_negativo(args) -> int:
    negativo(args.patron, args.archivos)
    return 0


# ═══════════════ P1 · preflight ════════════════════════════════════════════

def _resuelve_inputs(spec: dict) -> list[dict]:
    """P1 (GEN2-E3-1-1): resolucion UNICA de los inputs de una spec. Devuelve
    el SNAPSHOT -- una lista de entradas con `{id, origen, ruta_absoluta,
    raiz_logica, sha256, estado}` -- y nada mas: no imprime, no bloquea, no
    decide veredictos. Quien lo llama (preflight, verify) lo hace UNA vez por
    intento y le pasa ese mismo objeto a todo lo que necesite identidad de
    input; nadie vuelve a mirar manifiesto ni disco despues.

      `origen: repo`        insumo VERSIONADO -- se leen los bytes UNA vez, se
                            hashean, y el snapshot se queda con esos MISMOS
                            bytes (`bytes`): el medidor recibe exactamente lo
                            que el SHA verificado identifica, no lo que el
                            disco traiga un instante despues.
      `origen: manifiesto`  payload del corpus -- lo resuelve
                            `resolver_payload` (`tests/payload_resolver.py`),
                            una vez por id, import directo (nunca subproceso).

    Defecto que cierra (A.8 D1): antes, `preflight` resolvia para verificar y
    `_inputs_para_medidor` volvia a resolver por su cuenta -- entre las dos
    lecturas cabia un cambio de disco, y `ejecucion.json` podia registrar los
    bytes X que verifico el preflight mientras el medidor midio los bytes Y.
    """
    fuera = []
    for ent in spec.get("inputs") or []:
        iid = str(ent.get("id", ""))
        if ent.get("origen") == "repo":
            ruta = RAIZ / str(ent.get("ruta", ""))
            try:
                crudo = ruta.read_bytes()
            except OSError:
                crudo, real = None, None
            else:
                real = hashlib.sha256(crudo).hexdigest()
            declarado = str(ent.get("sha256", ""))
            if real is None:
                estado = "AUSENTE"
            elif declarado and real != declarado:
                estado = "DISCORDA"
            elif not declarado:
                estado = "SIN-SHA-DECLARADO"
            else:
                estado = "COINCIDE"
            cod, _ = _git_salida("ls-files", "--error-unmatch",
                                 str(ent.get("ruta", "")))
            fuera.append({"id": iid, "origen": "repo", "ruta": str(ent.get("ruta")),
                          "ruta_absoluta": str(ruta), "raiz_logica": None,
                          "sha256": real, "sha256_declarado": declarado,
                          "estado": estado, "commiteado": cod == 0,
                          "bytes": crudo})
        else:
            r = _PR.resolver_payload(iid)
            fuera.append({"id": iid, "origen": "manifiesto", "estado": r["estado"],
                          "ruta_absoluta": r["ruta_absoluta"],
                          "raiz_logica": r["raiz_logica"],
                          "sha256": r["sha256_actual"] or r["sha256_esperado"],
                          "sha256_esperado": r["sha256_esperado"],
                          "sha256_actual": r["sha256_actual"],
                          "tamano": r["tamano"], "bytes": None})
    return fuera


def _bloqueos_de_inputs(snapshot: list[dict], bloqueos: list[str],
                        imprime: bool = True) -> None:
    """Los VEREDICTOS sobre el snapshot de `_resuelve_inputs` -- separados de
    la resolucion a proposito: se juzga lo ya resuelto, no se vuelve a
    resolver para juzgar. `preflight` queda VERDE solo si CADA input activo
    esta en `COINCIDE` y, si es `origen: repo`, ademas commiteado."""
    for e in snapshot:
        iid, estado = e["id"], e["estado"]
        if e["origen"] == "repo":
            if estado == "AUSENTE":
                bloqueos.append(f"input_repo_ausente={iid}:{e.get('ruta')}")
            elif estado == "DISCORDA":
                bloqueos.append(f"input_repo_sha_discorda={iid}")
            elif estado == "SIN-SHA-DECLARADO":
                bloqueos.append(f"input_repo_sin_sha_declarado={iid}")
            if not e.get("commiteado"):
                # Un insumo versionado que no esta commiteado no es versionado.
                bloqueos.append(f"input_repo_no_commiteado={iid}")
                estado = f"{estado}+NO-COMMITEADO"
            if imprime:
                print(f"    [{estado}] {iid}  origen=repo  ruta={e.get('ruta')}")
                print(f"              sha256 real     = {e['sha256']}")
                print(f"              sha256 declarado= "
                      f"{e.get('sha256_declarado') or '(ninguno)'}")
        else:
            if estado != "COINCIDE":
                bloqueos.append(f"input_manifiesto_{estado}={iid}")
            if imprime:
                print(f"    [{estado}] {iid}  origen=manifiesto  "
                      f"raiz={e['raiz_logica']}")
                print(f"              ruta_absoluta   = {e['ruta_absoluta']}")
                print(f"              sha256 esperado = {e.get('sha256_esperado')}")
                print(f"              sha256 actual   = {e.get('sha256_actual')}")
                print(f"              tamano          = {e.get('tamano')}")


def _bloqueos_de_dimensiones(spec: dict, bloqueos: list[str]) -> None:
    """P2 (GEN2-E3-1-1): toda dimension sustantiva se DECLARA. `ponderador:
    NO-APLICA` es una declaracion valida; `ponderador` ausente es un campo
    olvidado, y el runner ya no lo convierte en `NO-APLICA` por su cuenta.

    Nota sobre el test de presencia: `campo in spec`, no `spec.get(campo)`.
    `variables: []` y `dependencias_materiales: []` son vacios DECLARADOS
    (es lo que ambos smokes traen) y no pueden confundirse con ausencia."""
    for campo in DIMENSIONES_SUSTANTIVAS:
        if campo not in spec:
            bloqueos.append(f"campo_sustantivo_ausente={campo}")


def _bloqueos_de_seed(spec: dict, bloqueos: list[str], endurecido: bool) -> None:
    """P2: `seed` acepta DOS formas y ninguna mas --
        seed: {aplica: false}
        seed: {aplica: true, valor: 42, rng: numpy.PCG64}
    Si `aplica: true` y falta `valor` o falta `rng`: BLOQUEADO. No se inventa
    un RNG por omision: una corrida estocastica sin RNG declarado no es
    reproducible, y decir que lo es seria el defecto, no el bloqueo.

    Un `seed` escalar (`seed: 42`) solo lo admite el esquema legado -- es el
    unico formato que `CALC-SMOKE-0001` trae, y ese CALC no se toca."""
    seed = spec.get("seed")
    if "seed" not in spec or seed is None:
        bloqueos.append("seed_no_declarado")
        return
    if not isinstance(seed, dict):
        if endurecido:
            bloqueos.append(f"seed_escalar_sin_forma={seed!r}")
        return
    if "aplica" not in seed:
        bloqueos.append("seed_dict_sin_aplica")
        return
    if seed.get("aplica") is not True:
        return
    if "valor" not in seed:
        bloqueos.append("seed_aplica_sin_valor")
    if endurecido and not seed.get("rng"):
        bloqueos.append("seed_aplica_sin_rng")


def _bloqueos_de_resultados(spec: dict, bloqueos: list[str]) -> None:
    """P2: la DECLARACION del schema de outputs se valida ANTES de abrir
    microdato -- id no vacio, tipo permitido, unidad no vacia,
    `permite_no_estimable` booleano si aparece. (La validacion de los VALORES
    producidos sigue siendo de `run`, en `_valida_outputs`: son dos cosas
    distintas y no se colapsan.) La unicidad de ids ya la comprueba el paso 3
    de `preflight`, comun a inputs y resultados; aqui no se repite."""
    for i, r in enumerate(spec.get("resultados") or []):
        if not isinstance(r, dict):
            bloqueos.append(f"resultado_no_es_mapa=#{i}:{r!r}")
            continue
        rid = str(r.get("id", "")).strip()
        etiqueta = rid or f"#{i}"
        if not rid:
            bloqueos.append(f"resultado_sin_id=#{i}")
        if r.get("tipo") not in TIPOS_VALIDOS_RESULT:
            bloqueos.append(f"resultado_tipo_invalido={etiqueta}:{r.get('tipo')!r}")
        if not str(r.get("unidad", "")).strip():
            bloqueos.append(f"resultado_sin_unidad={etiqueta}")
        if "permite_no_estimable" in r and \
                not isinstance(r["permite_no_estimable"], bool):
            bloqueos.append(f"resultado_permite_no_estimable_no_booleano={etiqueta}")


def preflight(calc_id: str, imprime: bool = True) -> dict:
    """Comprobacion previa. No mide, no escribe, no arregla nada: contesta
    VERDE o BLOQUEADO y dice por que, con el comando a la vista.

    El estado de `spec.md` frente a `origin/main` se reporta en TRES estados
    sin colapsar -- `EN-MAIN-COINCIDE`, `EN-MAIN-DISCORDA` (bloquea: alguien
    movio la spec bajo los pies de la corrida) y `NO-EN-MAIN` (no bloquea y
    se DECLARA: la primera corrida de una spec nueva ocurre por definicion
    antes de que la spec este fusionada; llamarlo VERDE a secas seria
    mentir, y bloquearlo haria imposible cualquier primera corrida)."""
    bloqueos: list[str] = []
    avisos: list[str] = []
    d, spec = _carga_spec(calc_id)
    if imprime:
        print(f"PRE-FLIGHT {calc_id}   ({_rel(d)})")

    for campo in CAMPOS_SPEC_OBLIGATORIOS:
        if spec.get(campo) in (None, "", [], {}):
            bloqueos.append(f"spec_sin_{campo}")
    if spec.get("calc_id") and spec["calc_id"] != calc_id:
        bloqueos.append(f"calc_id_discorda(spec={spec['calc_id']}, dir={calc_id})")

    # 1 · spec.md y spec.yaml existen y estan commiteados
    md = d / str(spec.get("spec_md", "spec.md"))
    yml = d / "spec.yaml"
    for ruta in (md, yml):
        if not ruta.exists():
            bloqueos.append(f"ausente={_rel(ruta)}")
            continue
        cod, _ = _git_salida("ls-files", "--error-unmatch", _rel(ruta))
        estado = "COMMITEADO" if cod == 0 else "NO-COMMITEADO"
        if cod != 0:
            bloqueos.append(f"no_commiteado={_rel(ruta)}")
        if imprime:
            print(f"  [{estado}] {_rel(ruta)}")

    # 2 · sha del md declarado en el yaml vs arbol vs origin/main
    sha_declarado = str(spec.get("spec_md_sha256", ""))
    sha_arbol = _sha256_archivo(md)
    sha_main = _sha256_blob_en("origin/main", _rel(md))
    if sha_arbol is None:
        estado_md = "NO-EJECUTABLE"
    elif sha_declarado != sha_arbol:
        estado_md = "ARBOL-DISCORDA"
        bloqueos.append("spec_md_sha256_discorda_arbol")
    elif sha_main is None:
        estado_md = "NO-EN-MAIN"
        avisos.append("spec_md_no_esta_en_origin_main -- primera corrida de una "
                      "spec aun no fusionada; se DECLARA, no se da por fusionada")
    elif sha_main != sha_declarado:
        estado_md = "EN-MAIN-DISCORDA"
        bloqueos.append("spec_md_sha256_discorda_origin_main")
    else:
        estado_md = "EN-MAIN-COINCIDE"
    if imprime:
        print(f"  [{estado_md}] spec_md_sha256")
        print(f"              declarado en spec.yaml = {sha_declarado or '(ninguno)'}")
        print(f"              arbol                  = {sha_arbol}")
        print(f"              origin/main            = {sha_main or 'NO-EN-MAIN'}")

    # 3 · ids unicos
    ids_res = [str(r.get("id", "")) for r in (spec.get("resultados") or [])]
    ids_in = [str(i.get("id", "")) for i in (spec.get("inputs") or [])]
    for nombre, ids in (("resultados", ids_res), ("inputs", ids_in)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            bloqueos.append(f"ids_{nombre}_duplicados={dup}")
        if imprime:
            print(f"  [{'DUPLICADOS' if dup else 'UNICOS'}] ids de {nombre}: "
                  f"{len(ids)} declarados" + (f" · duplicados: {dup}" if dup else ""))

    # 4 · script existe
    script = RAIZ / str(spec.get("script", ""))
    if not script.exists():
        bloqueos.append(f"script_ausente={spec.get('script')}")
    if imprime:
        print(f"  [{'EXISTE' if script.exists() else 'AUSENTE'}] script "
              f"{spec.get('script')}")
        print(f"              script_blob_sha256 = {_sha256_archivo(script)}")

    # 5 · inputs -- RESOLUCION UNICA (P1): este snapshot es el que sale en
    # `pre["inputs_resueltos"]` y el que `run` le pasa al medidor y al recibo.
    if imprime:
        print(f"  inputs declarados: {len(spec.get('inputs') or [])}")
    detalle_inputs = _resuelve_inputs(spec)
    _bloqueos_de_inputs(detalle_inputs, bloqueos, imprime=imprime)

    # 5-bis · FP-352: el detector aprende la diferencia. Un `AUSENTE` de
    # manifiesto con `raiz_logica` CONFIGURADA es AMBIGUO -- puede ser un
    # archivo genuinamente ausente bajo una raiz que SI resuelve, o puede
    # ser que la raiz misma no resuelve DESDE ESTE PROCESO (el caso
    # sandbox//mnt/c: la raiz esta configurada en la maquina, pero el
    # proceso que corre este `preflight` no la ve). Solo el primero
    # bloquea preflight; el segundo es `NO-VISIBLE-EN-ESTE-CONTEXTO` --
    # aviso con instruccion, nunca `BLOQUEADO` falso. (`raiz_logica is
    # None` -- id ausente del manifiesto -- no entra aqui: eso sigue
    # siendo `AUSENTE` real, sin ambiguedad.)
    for e in detalle_inputs:
        if e["origen"] != "manifiesto" or e["estado"] != "AUSENTE" \
                or not e.get("raiz_logica"):
            continue
        etiqueta_bloqueo = f"input_manifiesto_AUSENTE={e['id']}"
        if etiqueta_bloqueo not in bloqueos:
            continue
        raiz_fisica = _PR.M.resolver_raiz(e["raiz_logica"], _PR.M.repo_root(),
                                          _PR.M.rutas(_PR.M.repo_root())[1])
        raiz_visible = raiz_fisica is not None and Path(raiz_fisica).is_dir()
        if raiz_visible:
            continue
        bloqueos.remove(etiqueta_bloqueo)
        avisos.append(
            f"input_manifiesto_NO-VISIBLE-EN-ESTE-CONTEXTO={e['id']} "
            f"(raiz_logica={e['raiz_logica']} configurada, pero su raiz "
            f"fisica no resuelve desde este proceso -- correr fuera del "
            f"sandbox, FP-352)")
        if imprime:
            print(f"    [NO-VISIBLE-EN-ESTE-CONTEXTO] {e['id']}  "
                  f"raiz_logica={e['raiz_logica']}  raiz_fisica={raiz_fisica!r}"
                  f" -- no resuelve desde este proceso; correr fuera del "
                  f"sandbox (no bloquea, FP-352)")

    # 6 · parametros, tolerancia, seed y dimensiones sustantivas declarados
    endurecido = _esquema_endurecido(spec)
    tol = spec.get("tolerancia") or {}
    if not isinstance(tol, dict) or not tol.get("tipo"):
        bloqueos.append("tolerancia_sin_tipo")
    _bloqueos_de_seed(spec, bloqueos, endurecido)
    if endurecido:
        # P2: una spec del esquema endurecido declara TODA dimension
        # sustantiva y el schema completo de sus outputs. El esquema legado
        # (`etiquetas.generacion: LEGACY-GEN1`) queda exento por lectura, no
        # por olvido -- es lo que los dos smokes sellados ya declaran.
        _bloqueos_de_dimensiones(spec, bloqueos)
        _bloqueos_de_resultados(spec, bloqueos)
    if imprime:
        print(f"  [{'ENDURECIDO' if endurecido else 'LEGADO'}] esquema de spec"
              f"   (etiquetas.generacion = "
              f"{(spec.get('etiquetas') or {}).get('generacion', '(ninguna)')})")
        print(f"  [DECLARADO] parametros = {json.dumps(spec.get('parametros'), sort_keys=True)}")
        print(f"  [DECLARADO] tolerancia = {json.dumps(tol, sort_keys=True)}")
        print(f"  [DECLARADO] seed       = {spec.get('seed')}")

    # 7 · arbol limpio
    _cod, porcelain = _git_salida("status", "--porcelain")
    sucio = porcelain.strip() != ""
    if sucio:
        bloqueos.append("working_tree_dirty=SI")
    if imprime:
        print(f"  [{'SUCIO' if sucio else 'LIMPIO'}] git status --porcelain "
              f"({len(porcelain.strip().splitlines()) if sucio else 0} lineas)")
        for linea in porcelain.strip().splitlines()[:20]:
            print(f"              | {linea}")

    # 8 · P4: CALC-INMUTABLE -- un sello previo valido bloquea, no avisa.
    # «Una corrida sellada es evidencia historica. No se reescribe.»
    sello_json, sello_sha = d / "sello.json", d / "sello.sha256"
    estado_sello = "SIN-SELLO-PREVIO"
    if sello_sha.exists():
        r = subprocess.run([sys.executable, str(SELLA_PY), "--verifica",
                            str(sello_json)], cwd=RAIZ, capture_output=True, text=True)
        estado_sello = {0: "SELLO_COINCIDE", 2: "SIDACAR_AUSENTE",
                        3: "SELLO_NO_COINCIDE"}.get(r.returncode, f"exit={r.returncode}")
        if estado_sello == "SELLO_COINCIDE":
            bloqueos.append("calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO")
        elif r.returncode != 0:
            bloqueos.append(f"sello_previo_incompatible={estado_sello}")
    if imprime:
        print(f"  [{estado_sello}] sello previo   [python3 tools/sella_sha256.py "
              f"--verifica {_rel(sello_json)}]")

    veredicto = "BLOQUEADO" if bloqueos else "VERDE"
    if imprime:
        for a in avisos:
            print(f"  [AVISO] {a}")
        print(f"\nPRE-FLIGHT: {veredicto}" +
              ("" if not bloqueos else " " + " ".join(bloqueos)))
    return {"calc_id": calc_id, "veredicto": veredicto, "bloqueos": bloqueos,
            "avisos": avisos, "spec": spec, "dir": str(d),
            # P1: UN solo snapshot, bajo su nombre canonico. `inputs` se
            # conserva como alias del MISMO objeto (mismos elementos, no una
            # copia) para no romper a quien ya lo leia por ese nombre.
            "inputs_resueltos": detalle_inputs, "inputs": detalle_inputs,
            "esquema_endurecido": endurecido, "spec_md_estado": estado_md,
            "sello_previo": estado_sello,
            "script_blob_sha256": _sha256_archivo(script)}


def cmd_preflight(args) -> int:
    try:
        r = preflight(args.calc_id)
    except BloqueoPreflight as exc:
        print(f"PRE-FLIGHT: BLOQUEADO {exc}")
        return 1
    return 0 if r["veredicto"] == "VERDE" else 1


# ═══════════════ P1 · run ══════════════════════════════════════════════════

def _carga_medidor(script: Path):
    """Interfaz estable, unica y sin alternativas:
        medir(inputs, contrato) -> {"RESULT-…": valor}
    Un medidor que no la exponga es NO-EJECUTABLE -- no se adivina otra
    entrada ni se llama a `main()` por si acaso."""
    spec_mod = importlib.util.spec_from_file_location(
        f"medidor_{script.stem}", script)
    if spec_mod is None or spec_mod.loader is None:
        raise RuntimeError(f"no se pudo cargar {script}")
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules[spec_mod.name] = mod
    spec_mod.loader.exec_module(mod)
    if not hasattr(mod, "medir"):
        raise RuntimeError(
            f"{_rel(script)} no expone `medir(inputs, contrato)` -- interfaz "
            f"estable del plan v2.0 §4 (B-1)")
    return mod.medir


def _inputs_para_medidor(spec: dict, inputs_resueltos: list[dict]) -> dict:
    """P1: TRANSFORMA el snapshot al formato que espera `medir()`; no vuelve a
    resolver nada. `inputs_resueltos` es el objeto que `preflight` (o `verify`)
    produjo UNA vez en este intento, y de el salen `ruta_absoluta`, `sha256` y
    `raiz_logica` -- ni el manifiesto ni el disco se vuelven a mirar aqui para
    decidir identidad, que es exactamente el defecto D1 que este acto cierra.

    Un input DECLARADO en la spec que no aparezca en el snapshot es un error
    de cableado, no algo que se resuelva sobre la marcha: se levanta."""
    por_id = {e["id"]: e for e in inputs_resueltos}
    fuera = {}
    for ent in spec.get("inputs") or []:
        iid = str(ent.get("id", ""))
        r = por_id.get(iid)
        if r is None:
            raise RuntimeError(
                f"input `{iid}` declarado en la spec y ausente del snapshot "
                f"resuelto -- P1 prohibe resolverlo aqui por segunda vez")
        d = dict(ent)
        d["ruta_absoluta"] = r["ruta_absoluta"]
        d["sha256"] = r["sha256"]
        d["raiz_logica"] = r["raiz_logica"]
        d["estado"] = r["estado"]
        if r.get("bytes") is not None:
            # `origen: repo`: los MISMOS bytes que el SHA verificado
            # identifica -- el medidor no tiene que reabrir el archivo.
            d["bytes"] = r["bytes"]
        fuera[iid] = d
    return fuera


def _seed_normalizado(seed) -> dict:
    """P2: la spec declara `seed: {aplica: false}` o `{aplica: true, valor:
    …, rng: …}`. Retrocompatible con un valor suelto (`seed: 42`, el unico
    formato que `CALC-SMOKE-0001` trae y que este acto no toca): se envuelve
    como `{aplica: true, valor: <el mismo>}` sin inventar nada nuevo."""
    if isinstance(seed, dict):
        return seed
    if seed is None:
        return {"aplica": False}
    return {"aplica": True, "valor": seed}


def contrato_ejecutable(spec: dict) -> dict:
    """P2: `{variables, universo, filtros, ponderador, transformacion,
    estimando, parametros, seed}` -- el medidor recibe SIEMPRE este contrato
    normalizado, nunca la spec cruda; no abre `spec.yaml`. Cada dimension
    sustantiva la DECLARA la spec, y `preflight` ya bloqueo la spec endurecida
    a la que le faltara alguna (`campo_sustantivo_ausente=…`, P2 de
    GEN2-E3-1-1). Este contrato solo COPIA lo declarado.

    El relleno `"NO-APLICA"` que queda abajo es, desde este acto, unicamente
    la cara legible del esquema LEGADO -- las dos specs `LEGACY-GEN1` que ya
    estan selladas y que no se tocan. Para una spec nueva es inalcanzable:
    `preflight` no la deja llegar aqui con un campo ausente, asi que un campo
    OLVIDADO ya no puede disfrazarse de `NO-APLICA` DECLARADO."""
    return {
        "variables": spec.get("variables") or [],
        "universo": spec.get("universo", "NO-APLICA"),
        "filtros": spec.get("filtros", "NO-APLICA"),
        "ponderador": spec.get("ponderador", "NO-APLICA"),
        "transformacion": spec.get("transformacion", "NO-APLICA"),
        "estimando": spec.get("estimando", "NO-APLICA"),
        "parametros": dict(spec.get("parametros") or {}),
        "seed": _seed_normalizado(spec.get("seed")),
    }


def _firma_entorno() -> dict:
    """P3 incorporada a `ejecucion.json`. Se importa por ruta -- `tools/` no
    es un paquete y no se vuelve uno por esto."""
    spec_mod = importlib.util.spec_from_file_location("entorno_gen2", ENTORNO_PY)
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules[spec_mod.name] = mod
    spec_mod.loader.exec_module(mod)
    return mod.firma(sonda=False)


def _dependencias_materiales_calc(spec: dict) -> dict:
    """P2: `dependencias_materiales: [numpy, pandas, …]` declaradas POR
    ESTE CALC -- `tools/entorno.py` resuelve sus versiones instaladas.
    Vacio declarado (no `firma_entorno`, que trae la lista fija general) si
    la spec no declara ninguna."""
    spec_mod = importlib.util.spec_from_file_location("entorno_gen2_calc", ENTORNO_PY)
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules[spec_mod.name] = mod
    spec_mod.loader.exec_module(mod)
    return mod.dependencias_materiales_de(spec.get("dependencias_materiales") or [])


def _ejecuta(spec: dict, inputs_resueltos: list[dict]) -> tuple[dict, int, str]:
    """P1: `inputs_resueltos` es OBLIGATORIO y viene de quien ya resolvio el
    snapshot en este intento (`preflight` en `run`, la resolucion unica de
    `verify`). No tiene valor por defecto a proposito: un llamador que no
    traiga snapshot es un llamador que iba a resolver por segunda vez."""
    script = RAIZ / str(spec.get("script", ""))
    try:
        medir = _carga_medidor(script)
        valores = medir(_inputs_para_medidor(spec, inputs_resueltos),
                        contrato_ejecutable(spec))
    except Exception as exc:  # el fallo es un HECHO de la corrida, no un crash
        return {}, 1, f"{type(exc).__name__}: {exc}"
    if not isinstance(valores, dict):
        return {}, 1, "medir() no devolvio un dict {\"RESULT-…\": valor}"
    return valores, 0, ""


def _valida_outputs(spec: dict, valores: dict) -> list[str]:
    """P3: antes de escribir nada. `set(resultado.keys()) ==
    set(outputs_declarados)` EXACTO; cada output declara `tipo` (uno de
    `TIPOS_VALIDOS_RESULT`) y `unidad`; se valida tipo, finitud, rango (solo
    `proporcion`, en [0, 1]) y `null` solo si la spec permite `NO-ESTIMABLE`
    para ese output (`permite_no_estimable: true`). Devuelve la lista de
    problemas -- vacia significa outputs validos."""
    declarados = spec.get("resultados") or []
    ids_declarados = {str(r.get("id", "")) for r in declarados}
    ids_devueltos = set(valores)
    problemas = []
    faltan = sorted(ids_declarados - ids_devueltos)
    sobran = sorted(ids_devueltos - ids_declarados)
    if faltan:
        problemas.append(f"outputs_faltantes={faltan}")
    if sobran:
        problemas.append(f"outputs_no_declarados={sobran}")
    for r in declarados:
        rid = str(r.get("id", ""))
        if rid not in valores:
            continue
        valor = valores[rid]
        tipo = r.get("tipo")
        if tipo not in TIPOS_VALIDOS_RESULT:
            problemas.append(f"{rid}: tipo_declarado_invalido={tipo!r} "
                              f"(debe ser uno de {sorted(TIPOS_VALIDOS_RESULT)})")
            continue
        if not r.get("unidad"):
            problemas.append(f"{rid}: unidad_no_declarada")
        if valor is None:
            if not r.get("permite_no_estimable"):
                problemas.append(f"{rid}: valor_null_sin_NO-ESTIMABLE_permitido")
            continue
        if tipo == "entero":
            if isinstance(valor, bool) or not isinstance(valor, int):
                problemas.append(f"{rid}: tipo_entero_pero_valor={valor!r}")
        elif tipo in ("flotante", "proporcion"):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                problemas.append(f"{rid}: tipo_{tipo}_pero_valor={valor!r}")
            else:
                fv = float(valor)
                if fv != fv or fv in (float("inf"), float("-inf")):
                    problemas.append(f"{rid}: valor_no_finito={valor!r}")
                elif tipo == "proporcion" and not (0.0 <= fv <= 1.0):
                    problemas.append(f"{rid}: proporcion_fuera_de_rango={valor!r}")
        elif tipo == "texto":
            if not isinstance(valor, str):
                problemas.append(f"{rid}: tipo_texto_pero_valor={valor!r}")
    return problemas


def _calc_ya_sellado(d: Path) -> bool:
    """P4: CALC-INMUTABLE solo si los TRES artefactos existen y el sello
    verifica -- un `sello.sha256` huerfano (sin ejecucion.json/resultados.json)
    no es un sello valido."""
    if not (d / "ejecucion.json").exists() or not (d / "resultados.json").exists() \
            or not (d / "sello.sha256").exists():
        return False
    r = subprocess.run([sys.executable, str(SELLA_PY), "--verifica", str(d / "sello.json")],
                       cwd=RAIZ, capture_output=True, text=True)
    return r.returncode == 0


def _medidor_vive_en_calc(script_abs: Path, d: Path) -> bool:
    try:
        script_abs.resolve().relative_to(d.resolve())
        return True
    except ValueError:
        return False


def _fallas_run(spec: dict, valores: dict, exit_code: int, error: str) -> list[str]:
    """P3: fallo antes de outputs validos -> ningun archivo se escribe. Un
    `exit_code != 0` es un fallo por si mismo (`valores` puede venir vacio o
    a medias, no se valida); si el medidor si corrio, se validan los
    outputs declarados (`_valida_outputs`). Lista vacia = puede sellar."""
    if exit_code != 0:
        return [f"medidor_fallo:{error}"]
    return _valida_outputs(spec, valores)


def _construye_ejecucion(calc_id: str, spec: dict, d: Path, pre: dict, commit: str,
                          valores: dict, exit_code: int, error: str) -> dict:
    md = d / str(spec.get("spec_md", "spec.md"))
    firma_entorno = _firma_entorno()  # P3: UNA sola vez, reusada abajo.
    return {
        "corrida_id": f"{calc_id}--{commit.strip()[:12]}",
        "spec_id": calc_id,
        "fecha": datetime.datetime.now(datetime.timezone.utc)
                 .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": commit.strip(),
        "script_path": str(spec.get("script")),
        "script_blob_sha256": pre["script_blob_sha256"],
        "spec_yaml_sha256": _sha256_archivo(d / "spec.yaml"),
        "spec_md_sha256": _sha256_archivo(md),
        "input_ids": [str(i.get("id", "")) for i in (spec.get("inputs") or [])],
        # P1: del MISMO snapshot que alimento al medidor -- no de una
        # segunda lectura de disco.
        "input_sha256": {e["id"]: e.get("sha256")
                         for e in pre["inputs_resueltos"]},
        "parametros": spec.get("parametros"),
        "seed": spec.get("seed"),
        "python_version": platform.python_version(),
        "dependencias_materiales": firma_entorno["dependencias_materiales"],
        "dependencias_materiales_calc": _dependencias_materiales_calc(spec),
        "firma_entorno": firma_entorno,
        "exit_code": exit_code,
        "error": error or None,
        "resultado_ids": sorted(valores),
        "tolerancia": spec.get("tolerancia"),
        "etiquetas": spec.get("etiquetas") or {},
        "spec_md_estado": pre["spec_md_estado"],
    }


def _construye_sello(d: Path, spec: dict) -> dict:
    """P4: sello.json cubre spec.yaml, ejecucion.json, resultados.json y --
    si vive dentro del CALC -- el propio medidor. Requiere que ejecucion.json
    y resultados.json ya esten escritos en disco."""
    sello = {"spec.yaml": _sha256_archivo(d / "spec.yaml"),
             "ejecucion.json": _sha256_archivo(d / "ejecucion.json"),
             "resultados.json": _sha256_archivo(d / "resultados.json")}
    script_abs = RAIZ / str(spec.get("script"))
    if _medidor_vive_en_calc(script_abs, d):
        sello[script_abs.name] = _sha256_archivo(script_abs)
    return sello


def run(calc_id: str, imprime: bool = True) -> dict:
    """Ejecucion sellada. Corre `preflight` primero SIEMPRE: una corrida
    lanzada sobre un preflight bloqueado es exactamente el registro que este
    CLI existe para no volver a producir.

    P4, verbatim de la firma de mesa: «Una corrida sellada es evidencia
    historica. No se reescribe.» Si el CALC ya esta sellado y el sello
    verifica, `run` NO llama siquiera a `preflight`: termina de inmediato,
    sin tocar un byte, con `CALC-INMUTABLE · YA-SELLADO`. No existe
    `--force`/`--overwrite`/`--replace`; una reejecucion es un CALC-Y nuevo
    con `repite_de`/`sucesor_de` declarado en su propia spec."""
    d = _dir_calc(calc_id)
    if _calc_ya_sellado(d):
        if imprime:
            print(f"\nRUN {calc_id}")
            print("RUN: CALC-INMUTABLE · YA-SELLADO -- una corrida sellada es "
                  "evidencia historica, no se reescribe; bytes intactos. Para "
                  "reejecutar, crea un CALC-Y nuevo con repite_de/sucesor_de.")
        return {"veredicto": "CALC-INMUTABLE", "calc_id": calc_id}

    pre = preflight(calc_id, imprime=imprime)
    if pre["veredicto"] != "VERDE":
        if imprime:
            print("\nRUN: NO-EJECUTADO -- preflight BLOQUEADO "
                  + " ".join(pre["bloqueos"]))
        return {"veredicto": "NO-EJECUTADO", "preflight": pre}

    spec, d = pre["spec"], Path(pre["dir"])
    _cod, commit = _git_salida("rev-parse", "HEAD")
    # P1: el snapshot que `preflight` acaba de verificar es el que corre.
    inputs_resueltos = pre["inputs_resueltos"]
    valores, exit_code, error = _ejecuta(spec, inputs_resueltos)

    problemas = _fallas_run(spec, valores, exit_code, error)
    if problemas:
        if imprime:
            print(f"\nRUN {calc_id}\nRUN: FALLO -- nada se sella:")
            for p in problemas:
                print(f"  {p}")
        return {"veredicto": "FALLO", "error": "; ".join(problemas),
                "preflight": pre}

    ejecucion = _construye_ejecucion(calc_id, spec, d, pre, commit, valores,
                                     exit_code, error)
    _escribe_json(d / "ejecucion.json", ejecucion)
    _escribe_json(d / "resultados.json",
                  {"spec_id": calc_id, "resultados": valores})

    sello = _construye_sello(d, spec)
    _escribe_json(d / "sello.json", sello)
    r = subprocess.run([sys.executable, str(SELLA_PY), str(d / "sello.json")],
                       cwd=RAIZ, capture_output=True, text=True)

    # P4 (GEN2-E3-1-1): el veredicto lo cierra el SELLO, no el medidor. Antes
    # de este acto, `run` devolvia `EJECUTADO` mirando solo `exit_code` del
    # medidor -- un `sella_sha256.py` que fallara dejaba un CALC declarado
    # ejecutado y sin sello valido. Se exige lo uno Y lo otro: que el sellador
    # termine en 0, y que el sello RECIEN escrito verifique con el mecanismo
    # que ya existe (`_verifica_sello`: sidecar + cada archivo que cubre).
    estado_sello_nuevo, razon_sello_nuevo = (
        ("NO-CREADO", f"sella_sha256.py exit={r.returncode} "
                      f"{(r.stderr or r.stdout or '').strip()}")
        if r.returncode != 0 else _verifica_sello(d))
    sellado = estado_sello_nuevo == "COINCIDE"
    if imprime:
        print(f"\nRUN {calc_id}")
        print(f"  corrida_id     = {ejecucion['corrida_id']}")
        print(f"  git_commit     = {ejecucion['git_commit']}")
        print(f"  script         = {ejecucion['script_path']}")
        print(f"  script_blob_sha256 = {ejecucion['script_blob_sha256']}")
        print(f"  spec_yaml_sha256   = {ejecucion['spec_yaml_sha256']}")
        print(f"  spec_md_sha256     = {ejecucion['spec_md_sha256']}")
        print(f"  exit_code      = {exit_code}" + (f"  error={error}" if error else ""))
        print(f"  resultado_ids  = {ejecucion['resultado_ids']}")
        print(f"  sello cubre    = {sorted(sello)}")
        print(f"  escritos: {_rel(d / 'ejecucion.json')} · "
              f"{_rel(d / 'resultados.json')} · {_rel(d / 'sello.sha256')}")
        print(f"  sella_sha256 exit={r.returncode} {(r.stdout or '').strip()}")
        print(f"  [{estado_sello_nuevo}] sello nuevo -- {razon_sello_nuevo}")
    if not sellado:
        if imprime:
            print("\nRUN: FALLO-SELLADO -- el CALC NO queda sellado ni "
                  "inmutable. Los JSON intermedios quedan como intento "
                  "incompleto: al no existir sello valido, `run` puede "
                  "reintentar sobre ellos (no hay sidecar de rescate).")
        return {"veredicto": "FALLO-SELLADO", "error": razon_sello_nuevo,
                "sello": estado_sello_nuevo, "ejecucion": ejecucion,
                "resultados": valores, "preflight": pre}
    return {"veredicto": "EJECUTADO", "sello": estado_sello_nuevo,
            "ejecucion": ejecucion, "resultados": valores, "preflight": pre}


def _escribe_json(ruta: Path, datos) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")


def cmd_run(args) -> int:
    r = run(args.calc_id)
    return 0 if r["veredicto"] == "EJECUTADO" else 1


# ═══════════════ P1 · verify ═══════════════════════════════════════════════

def _compara(valor_a, valor_b, tol: dict) -> tuple[bool, object]:
    """Tolerancias POR TIPO (encargo P1):
      entero     -- exacto, sin epsilon: un entero que no cuadra no cuadra.
      flotante   -- abs(delta) <= `abs` declarado (1e-10 por defecto).
      bootstrap  -- EXACTO solo si la spec fijo seed + RNG + codigo (lo cual
                    `run` ya registra); si no, cae a la tolerancia absoluta.
    """
    tipo = (tol or {}).get("tipo", "flotante")
    if isinstance(valor_a, bool) or isinstance(valor_b, bool):
        return valor_a == valor_b, None
    if tipo == "entero":
        return valor_a == valor_b, (None if valor_a == valor_b
                                    else f"{valor_a!r} != {valor_b!r}")
    if isinstance(valor_a, (int, float)) and isinstance(valor_b, (int, float)):
        delta = abs(float(valor_a) - float(valor_b))
        if tipo == "bootstrap" and (tol or {}).get("exacto_por_seed") is True:
            return valor_a == valor_b, delta
        limite = float((tol or {}).get("abs", TOL_FLOTANTE_DEFECTO))
        return delta <= limite, delta
    if isinstance(valor_a, dict) and isinstance(valor_b, dict):
        if set(valor_a) != set(valor_b):
            return False, f"claves distintas: {sorted(set(valor_a) ^ set(valor_b))}"
        peor, ok_total = None, True
        for k in valor_a:
            ok, delta = _compara(valor_a[k], valor_b[k], tol)
            ok_total = ok_total and ok
            if isinstance(delta, float) and (peor is None or not isinstance(peor, float) or delta > peor):
                peor = delta
            elif not ok and not isinstance(delta, float):
                peor = f"{k}: {delta}"
        return ok_total, peor
    if isinstance(valor_a, list) and isinstance(valor_b, list):
        if len(valor_a) != len(valor_b):
            return False, f"longitudes {len(valor_a)} != {len(valor_b)}"
        peor, ok_total = None, True
        for x, y in zip(valor_a, valor_b):
            ok, delta = _compara(x, y, tol)
            ok_total = ok_total and ok
            if isinstance(delta, float) and (peor is None or not isinstance(peor, float) or delta > peor):
                peor = delta
        return ok_total, peor
    return valor_a == valor_b, (None if valor_a == valor_b else "valores no numericos distintos")


def _canoniza_llaves(o):
    """FP-353: `ejecucion.json` paso por JSON, que convierte TODA llave de
    mapping en cadena; `spec.yaml` viene recien parseado del YAML, que
    conserva `29` como int. Comparar los dos lados crudos hace
    `CONTEXTO: IDENTICO` INALCANZABLE -- en cualquier arbol, sin que nada
    haya cambiado -- para toda spec cuyos parametros traigan un mapping de
    llaves no-cadena. Medido en CALC-0001 (12 llaves enteras entre
    `crosswalk_partido` y `coaliciones`: `spec.yaml` sale IDENTICO y
    `parametros` sale DISTINTO en la misma corrida); control positivo
    CALC-0002, cero llaves enteras, salio `CONTEXTO=IDENTICO`.

    Canoniza a la forma que SOBREVIVE el viaje por JSON: llaves a cadena,
    recursivo, y el mapping como lista ordenada de pares -- no como dict --
    para que dos llaves que colapsan a la misma cadena (`{1: 'a', '1': 'b'}`)
    sigan siendo dos. Colapsarlas afirmaria una igualdad que no se comprobo,
    que es el mismo defecto al reves."""
    if isinstance(o, dict):
        return sorted(((str(k), _canoniza_llaves(v)) for k, v in o.items()),
                      key=lambda par: (par[0], repr(par[1])))
    if isinstance(o, (list, tuple)):
        return [_canoniza_llaves(v) for v in o]
    return o


def _compara_result(previo, hoy, decl: dict, tol: dict) -> tuple[bool, object]:
    """P3 (GEN2-E3-1-1): el tipo AUTORITATIVO es el que declara la entrada de
    `resultados:` para ESE id -- nunca `spec["tolerancia"]["tipo"]`, que es
    global y no puede hablar por cada RESULT. Defecto que cierra (A.8 D3):
    con `tolerancia: {tipo: flotante, abs: 1e-10}`, un RESULT declarado
    `entero` cuyo replay devolviera `1.0` contra un `1` sellado caia en la
    rama numerica y reproducia dentro de la tolerancia -- el cambio de tipo
    quedaba invisible.

        entero      int de Python (no bool), comparacion EXACTA
        texto       str, comparacion EXACTA
        flotante    finito, abs(delta) <= tolerancia declarada
        proporcion  finito, en [0, 1], abs(delta) <= tolerancia declarada

    La tolerancia sigue siendo global como MAGNITUD (`tol["abs"]`, que es
    como las specs de hoy la declaran); lo que ya no sale de ella es la
    SEMANTICA de la comparacion. Un RESULT sin declaracion en la spec cae al
    comparador general `_compara`, que no cambia."""
    tipo = (decl or {}).get("tipo")
    if tipo not in TIPOS_VALIDOS_RESULT:
        return _compara(previo, hoy, tol)

    # FP-354: `None` es un valor que la propia spec puede AUTORIZAR
    # (`permite_no_estimable: true`), que `_valida_outputs` respeta y que
    # `run` sella sin problema. Sin esta rama, `_compara_result` y
    # `_valida_outputs` implementaban contratos CONTRADICTORIOS sobre el
    # mismo valor: un output NO-ESTIMABLE sellado y hoy NO-ESTIMABLE otra
    # vez -- reproduccion perfecta -- se contaba `NO-REPRODUCE` con el
    # mensaje "tipo declarado `flotante` y sellado=None". Medido: 22 de 54
    # en CALC-0001 y 4 de 29 en CALC-0002, con `sellado == hoy` en los 26.
    if previo is None or hoy is None:
        if previo is None and hoy is None:
            if (decl or {}).get("permite_no_estimable"):
                return True, None
            return False, ("sellado y hoy son None y la spec no declara "
                           "`permite_no_estimable: true` para este RESULT")
        return False, (f"NO-ESTIMABLE contra valor: sellado={previo!r} · "
                       f"hoy={hoy!r}")

    if tipo == "entero":
        for etiqueta, v in (("sellado", previo), ("hoy", hoy)):
            if isinstance(v, bool) or not isinstance(v, int):
                return False, (f"tipo declarado `entero` y {etiqueta}="
                               f"{v!r} ({type(v).__name__})")
        return previo == hoy, (None if previo == hoy else f"{previo!r} != {hoy!r}")

    if tipo == "texto":
        for etiqueta, v in (("sellado", previo), ("hoy", hoy)):
            if not isinstance(v, str):
                return False, (f"tipo declarado `texto` y {etiqueta}="
                               f"{v!r} ({type(v).__name__})")
        return previo == hoy, (None if previo == hoy else f"{previo!r} != {hoy!r}")

    # flotante | proporcion
    for etiqueta, v in (("sellado", previo), ("hoy", hoy)):
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return False, (f"tipo declarado `{tipo}` y {etiqueta}="
                           f"{v!r} ({type(v).__name__})")
        fv = float(v)
        if fv != fv or fv in (float("inf"), float("-inf")):
            return False, f"{etiqueta} no finito: {v!r}"
        if tipo == "proporcion" and not (0.0 <= fv <= 1.0):
            return False, f"{etiqueta} fuera de [0,1]: {v!r}"
    delta = abs(float(previo) - float(hoy))
    limite = float((tol or {}).get("abs", TOL_FLOTANTE_DEFECTO))
    return delta <= limite, delta


TOL_ADOPCION_NO_APLICA = "NO-APLICA"


def _texto_tol_adopcion(valor) -> str:
    """Serializa `tolerancia_adopcion` para el TSV. Cadena vacia == sin
    declarar == defecto (grano del consumidor); `NO-APLICA` es un valor y
    viaja como tal."""
    if valor is None or valor == "":
        return ""
    return str(valor)


def _tol_adopcion_de(fila: dict):
    """Lee del renglon de la vista lo que `_compara_adopcion` espera:
    `None` si no hay declaracion, la cadena `NO-APLICA`, o un numero."""
    crudo = (fila or {}).get("tolerancia_adopcion", "")
    if crudo in ("", None, NO_DECLARADO, "PENDIENTE"):
        return None
    if str(crudo).strip().upper() == TOL_ADOPCION_NO_APLICA:
        return TOL_ADOPCION_NO_APLICA
    try:
        return float(crudo)
    except (TypeError, ValueError):
        return str(crudo)


def _grano_decimales(valor) -> int | None:
    """Con cuantos decimales materializa el consumidor su cifra.

    El grano no se declara en ningun lado: esta en la cifra misma que
    `milpa/` escribe (`p: 0.045694` son SEIS decimales). Se lee del literal
    y no de una convencion, porque es el consumidor -- no la spec -- quien
    decide cuanta precision publica.

    Devuelve `None` cuando la pregunta no aplica (no es flotante, o el
    repr sale en notacion exponencial y el literal ya no dice el grano);
    quien llama cae entonces a la tolerancia de reproducibilidad, que es el
    comportamiento estricto de siempre."""
    if isinstance(valor, bool) or not isinstance(valor, float):
        return None
    texto = repr(float(valor))
    if "e" in texto or "E" in texto:
        return None
    if "." not in texto:
        return 0
    return len(texto.split(".", 1)[1])


def _compara_adopcion(previo, hoy, decl: dict, tol: dict,
                      tol_adopcion=None) -> tuple[bool, object, str]:
    """NC-0069 / FP-365: la comparacion de ADOPCION, separada de la de
    REPRODUCIBILIDAD.

    `tolerancia.abs` servia hoy a dos preguntas distintas:

      1. *"esta corrida se reproduce a si misma?"* -- `1e-10` es la
         respuesta correcta y aflojarla un decimal es perder sensibilidad.
         Esa pregunta la sigue contestando `_compara_result`, intacta.
      2. *"el consumidor materializa este RESULT?"* -- el grano NO lo fija
         la corrida sino `milpa/`, que publica seis decimales. Medido en
         `ACTO GEN2-C0-B` §5.4: `RESULT-B-ENIGH-2022-P` = 0.04569409956405095
         contra el `p: 0.045694` del motor, `delta = 9.956e-08`. Reproduce
         al grano con que el consumidor materializa y NO reproduce a `1e-10`
         -- y como T35 (c) usaba la segunda, escribir la cita metia un FAIL
         falso. Esa es la pregunta que contesta esta funcion.

    Tres modos, en este orden:

      `tolerancia_adopcion` numerica declarada por la spec -> se usa tal cual.
      `tolerancia_adopcion: NO-APLICA`                     -> se exige la
          tolerancia de reproducibilidad (el estricto de siempre); es un
          VALOR declarable, no la ausencia del campo.
      sin declarar (defecto)                               -> se compara el
          RESULT REDONDEADO al grano del consumidor contra la cifra
          materializada, EXACTO.

    El redondeo es lo que hace al falsador honesto: `0.045694` adopta, y un
    valor genuinamente distinto en el sexto decimal (`0.045695`) sigue
    fallando, porque `round(0.04569409956405095, 6)` no es `0.045695`.

    Devuelve `(igual, delta, modo)`; `modo` va al mensaje de T35 para que la
    linea diga con que vara se comparo y no haya que adivinarlo."""
    tipo = (decl or {}).get("tipo")
    if tipo not in ("flotante", "proporcion") or previo is None or hoy is None:
        # entero / texto / NO-ESTIMABLE: el grano no significa nada ahi y la
        # comparacion exacta por tipo ya es la correcta.
        igual, delta = _compara_result(previo, hoy, decl, tol)
        return igual, delta, "EXACTO-POR-TIPO"

    if isinstance(tol_adopcion, str) and tol_adopcion.strip().upper() == TOL_ADOPCION_NO_APLICA:
        igual, delta = _compara_result(previo, hoy, decl, tol)
        return igual, delta, f"NO-APLICA -> reproducibilidad ({(tol or {}).get('abs', TOL_FLOTANTE_DEFECTO)})"

    if tol_adopcion is not None:
        try:
            limite = float(tol_adopcion)
        except (TypeError, ValueError):
            igual, delta = _compara_result(previo, hoy, decl, tol)
            return igual, delta, (f"tolerancia_adopcion ilegible ({tol_adopcion!r}) "
                                  f"-> reproducibilidad")
        igual, delta = _compara_result(previo, hoy, decl, {"abs": limite})
        return igual, delta, f"tolerancia_adopcion={limite}"

    grano = _grano_decimales(hoy)
    if grano is None:
        igual, delta = _compara_result(previo, hoy, decl, tol)
        return igual, delta, "SIN-GRANO -> reproducibilidad"

    # La validacion de tipo/finitud/[0,1] la sigue haciendo `_compara_result`;
    # si no pasa, no hay grano que valga.
    valido, motivo = _compara_result(previo, hoy, decl, {"abs": float("inf")})
    if not valido:
        return False, motivo, f"grano={grano} (rechazado por tipo)"
    redondeado = round(float(previo), grano)
    igual = redondeado == float(hoy)
    delta = abs(float(previo) - float(hoy))
    return igual, delta, f"grano del consumidor = {grano} decimales"


def _verifica_sello(d: Path) -> tuple[str, str]:
    """P5(1): valida el sello del recibo COMPLETO -- el sidecar de
    `sello.json` (via `sella_sha256.py --verifica`) Y que cada archivo que
    `sello.json` declara cubrir siga coincidiendo con los bytes de disco.
    Sin esto, un `sello.json` reescrito a mano con hashes frescos pasaria el
    sidecar (que solo cubre `sello.json` mismo) y no se notaria."""
    sello_json = d / "sello.json"
    if not (d / "sello.sha256").exists():
        return "AUSENTE", "sin sello.sha256 -- no hay recibo sellado que verificar"
    r = subprocess.run([sys.executable, str(SELLA_PY), "--verifica", str(sello_json)],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        return "NO-COINCIDE", f"sidecar de sello.json no valida (exit={r.returncode})"
    try:
        sello = json.loads(sello_json.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return "NO-COINCIDE", f"sello.json ilegible: {exc}"
    for nombre, sha_declarado in sello.items():
        real = _sha256_archivo(d / nombre)
        if real != sha_declarado:
            return "NO-COINCIDE", f"{nombre}: sello declara {sha_declarado}, arbol trae {real}"
    return "COINCIDE", "sello y todos los archivos que cubre coinciden"


def _evalua_contexto(d: Path, spec: dict, ejec: dict, inputs_resueltos=None,
                     imprime: bool = False) -> tuple[str, list[str]]:
    """P5 (2)+(3)+(4): `spec_yaml_sha256` · inputs de manifiesto re-resueltos
    con `resolver_payload` (P1) · `script_blob_sha256`, parametros, seed,
    dependencias -> `CONTEXTO ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE}` con sus
    razones. `NO-VERIFICABLE` cuando algo no se puede ni siquiera comprobar
    (un input fuera de perimetro/raiz no configurada) -- nunca se degrada a
    `DISTINTO`, que afirmaria un cambio que en realidad no se pudo confirmar
    ni descartar.

    FP-358: `git_commit` se reporta (informativo) pero NUNCA gatea. Lo que
    identifica una corrida es lo que la hace reproducible -- el codigo, la
    spec, los inputs, las dependencias -- no cuantos commits ajenos cayeron
    despues del sello, cosa que el propio protocolo del acto OBLIGA a que
    pase (COMMIT-2, cascada, merge). Antes de este acto, `CONTEXTO: IDENTICO`
    era inalcanzable para TODA corrida sellada en cuanto avanzaba un commit
    mas -- las 12 de 12 corridas selladas del arbol lo median."""
    sha_yaml_hoy = _sha256_archivo(d / "spec.yaml")
    yaml_igual = sha_yaml_hoy == ejec.get("spec_yaml_sha256")
    if imprime:
        print(f"  [2/5 SPEC.YAML] {'IDENTICO' if yaml_igual else 'CAMBIADO'}"
              f"  sellado={ejec.get('spec_yaml_sha256')}  hoy={sha_yaml_hoy}")
    razones_contexto = [] if yaml_igual else ["spec_yaml_cambiado"]

    # P1: los inputs vienen del snapshot que `verify` resolvio UNA vez en esta
    # invocacion -- el mismo que va a alimentar la reejecucion. Resolver aqui
    # para el CONTEXTO y otra vez para el medidor es el defecto D1 de nuevo,
    # esta vez en `verify`. `inputs_resueltos=None` solo lo usan los llamadores
    # que no traen snapshot (tests de contexto puro sobre specs sin inputs).
    if inputs_resueltos is None:
        inputs_resueltos = _resuelve_inputs(spec)
    no_verificable_inputs = False
    for e in inputs_resueltos:
        iid = e["id"]
        sellado = (ejec.get("input_sha256") or {}).get(iid)
        if e["origen"] == "repo":
            hoy = e["sha256"]
            ok = hoy is not None and hoy == sellado
            if imprime:
                print(f"  [3/5 INPUT {'COINCIDE' if ok else 'DISCORDA'}] {iid} (repo)"
                      f"  sellado={sellado}  hoy={hoy}")
            if not ok:
                razones_contexto.append(f"input_cambiado={iid}")
        else:
            if imprime:
                print(f"  [3/5 INPUT {e['estado']}] {iid} (manifiesto)"
                      f"  sellado={sellado}  actual={e.get('sha256_actual')}")
            if e["estado"] in ("RAIZ_NO_CONFIGURADA", "FUERA_DE_PERIMETRO"):
                no_verificable_inputs = True
                razones_contexto.append(f"input_no_verificable={iid}:{e['estado']}")
            elif e["estado"] != "COINCIDE" or e.get("sha256_actual") != sellado:
                razones_contexto.append(f"input_cambiado={iid}")

    sha_script_hoy = _sha256_archivo(RAIZ / str(spec.get("script", "")))
    script_igual = sha_script_hoy == ejec.get("script_blob_sha256")
    if not script_igual:
        razones_contexto.append("codigo_distinto")
    # FP-358: el commit es dato INFORMATIVO, nunca criterio. Antes,
    # `CONTEXTO: IDENTICO` era inalcanzable para toda corrida sellada en
    # cuanto caia UN commit mas -- cosa que el propio protocolo del acto
    # OBLIGA a hacer (COMMIT-2, cascada, merge). Lo que identifica la
    # corrida es el blob del medidor, el spec.yaml, los inputs y las
    # dependencias -- no el numero de commits que cayeron despues, ajenos
    # o no, a la corrida sellada. Se sigue calculando y reportando (una
    # sesion que audite CUANDO se corrio algo lo necesita) pero nunca
    # gatea CONTEXTO ni fuerza NO-VERIFICABLE.
    cod_commit, commit_hoy = _git_salida("rev-parse", "HEAD")
    commit_hoy = commit_hoy.strip() if cod_commit == 0 else None
    # FP-353: los dos lados se canonizan ANTES de compararse -- `spec` viene
    # del YAML (llaves int) y `ejec` del JSON (esas mismas llaves, cadena).
    # Sin esto, `parametros_distintos` es un falso positivo permanente.
    parametros_igual = (_canoniza_llaves(spec.get("parametros"))
                        == _canoniza_llaves(ejec.get("parametros")))
    if not parametros_igual:
        razones_contexto.append("parametros_distintos")
    if spec.get("seed") != ejec.get("seed"):
        razones_contexto.append("seed_distinto")
    deps_hoy = _dependencias_materiales_calc(spec)
    deps_igual = (_canoniza_llaves(deps_hoy)
                  == _canoniza_llaves(ejec.get("dependencias_materiales_calc")))
    if not deps_igual:
        razones_contexto.append("dependencias_distintas")
    if imprime:
        commit_informativo = ("NO-VERIFICABLE" if commit_hoy is None
                              else ("IDENTICO" if commit_hoy == ejec.get("git_commit")
                                    else "DISTINTO"))
        print(f"  [4/5 CONTEXTO] codigo={'IDENTICO' if script_igual else 'CAMBIADO'}"
              f"  commit_informativo={commit_informativo}  (FP-358: no gatea)"
              f"  parametros={'IDENTICO' if parametros_igual else 'DISTINTO'}"
              f"  seed={'IDENTICO' if spec.get('seed') == ejec.get('seed') else 'DISTINTO'}"
              f"  dependencias={'IDENTICO' if deps_igual else 'DISTINTO'}")

    if no_verificable_inputs:
        contexto = "NO-VERIFICABLE"
    elif razones_contexto:
        contexto = "DISTINTO"
    else:
        contexto = "IDENTICO"
    return contexto, razones_contexto


def verify(calc_id: str, imprime: bool = True) -> dict:
    """P5: en orden y en DOS EJES, sin colapsar. (1) sello del recibo; (2)
    `spec_yaml_sha256`; (3) re-resuelve inputs de manifiesto con
    `resolver_payload` (P1) y compara SHA; (4) `script_blob_sha256`, commit,
    parametros, seed, dependencias -> `CONTEXTO` con razon; (5) reejecuta y
    compara por RESULT con la tolerancia declarada -> `RESULTADO`.

    `REPRODUCE` solo con `CONTEXTO=IDENTICO`; `REPLICA-RESULTADO ·
    CONTEXTO-DISTINTO` si los RESULT coinciden con contexto distinto;
    `NO-REPRODUCE` con contexto identico es el caso material; `NO-
    VERIFICABLE` no se degrada a ningun otro veredicto. No escribe NINGUN
    artefacto canonico -- ni aqui ni en ninguna rama de esta funcion."""
    d = _dir_calc(calc_id)
    if imprime:
        print(f"VERIFY {calc_id}   ({_rel(d)})")
    try:
        ejec = json.loads((d / "ejecucion.json").read_text(encoding="utf-8"))
        previos = json.loads((d / "resultados.json").read_text(encoding="utf-8"))["resultados"]
    except (OSError, ValueError, KeyError) as exc:
        if imprime:
            print(f"VERIFY: NO-EJECUTABLE -- sin corrida sellada que verificar "
                  f"({type(exc).__name__})")
        return {"veredicto": "NO-EJECUTABLE", "razon": f"sin corrida sellada: {exc}"}

    _d, spec = _carga_spec(calc_id)

    # (1) sello del recibo -- completo (sidecar + cada archivo que cubre).
    estado_sello, razon_sello = _verifica_sello(d)
    if imprime:
        print(f"  [1/5 SELLO] {estado_sello} -- {razon_sello}")
    if estado_sello != "COINCIDE":
        if imprime:
            print(f"\nVERIFY: NO-VERIFICABLE -- {razon_sello}")
        return {"veredicto": "NO-VERIFICABLE", "contexto": "NO-VERIFICABLE",
                "resultado": None, "razones_contexto": [razon_sello]}

    # P1: UNA resolucion de inputs por invocacion de `verify`. Este mismo
    # snapshot alimenta la comparacion de CONTEXTO y la reejecucion del
    # medidor -- no se resuelve una vez para cada cosa.
    inputs_resueltos = _resuelve_inputs(spec)

    # (2)+(3)+(4) -> CONTEXTO, con razon.
    contexto, razones_contexto = _evalua_contexto(d, spec, ejec, inputs_resueltos,
                                                  imprime=imprime)
    if imprime:
        print(f"  CONTEXTO: {contexto}" +
              (f"  razon: {'; '.join(razones_contexto)}" if razones_contexto else ""))

    # (5) reejecuta y compara POR RESULT segun el tipo que declara la spec
    # para CADA id (P3), no segun el `tipo` global de `tolerancia`.
    valores, exit_code, error = _ejecuta(spec, inputs_resueltos)
    deltas, faltan, problemas_replay = {}, [], []
    if exit_code != 0:
        resultado = "NO-EJECUTABLE"
        if imprime:
            print(f"  [5/5 RESULT] NO-EJECUTABLE -- la reejecucion fallo: {error}")
    else:
        # P3: los outputs REEJECUTADOS pasan el mismo contrato que `run` le
        # exige a una corrida antes de sellarla. Una salida que viola el
        # contrato no puede llamarse `REPRODUCE` aunque los numeros cuadren:
        # lo que reprodujo seria algo que la spec no autoriza a producir.
        problemas_replay = _valida_outputs(spec, valores)
        if problemas_replay:
            resultado = "NO-EJECUTABLE"
            if imprime:
                print("  [5/5 RESULT] NO-EJECUTABLE -- los outputs de la "
                      "reejecucion violan el contrato de la spec:")
                for pb in problemas_replay:
                    print(f"      {pb}")
        else:
            tol = spec.get("tolerancia") or {}
            decl_por_id = {str(r.get("id", "")): r
                           for r in (spec.get("resultados") or [])
                           if isinstance(r, dict)}
            faltan = sorted(set(previos) ^ set(valores))
            reproduce = not faltan
            for k in sorted(set(previos) & set(valores)):
                ok, delta = _compara_result(previos[k], valores[k],
                                            decl_por_id.get(k), tol)
                deltas[k] = delta
                reproduce = reproduce and ok
                if imprime:
                    tipo_k = (decl_por_id.get(k) or {}).get("tipo", "(no declarado)")
                    print(f"  [5/5 RESULT {'REPRODUCE' if ok else 'NO-REPRODUCE'}] "
                          f"{k} (tipo={tipo_k}): sellado={previos[k]!r} · "
                          f"hoy={valores[k]!r} · delta={delta!r}")
            if faltan and imprime:
                print(f"  [5/5 RESULT NO-REPRODUCE] ids que aparecen en una corrida "
                      f"y no en la otra: {faltan}")
            resultado = "REPRODUCE" if reproduce else "NO-REPRODUCE"

    # Combinacion final (P5, verbatim de la firma de mesa).
    if contexto == "NO-VERIFICABLE":
        veredicto = "NO-VERIFICABLE"
    elif resultado == "NO-EJECUTABLE":
        veredicto = "NO-EJECUTABLE"
    elif contexto == "IDENTICO" and resultado == "REPRODUCE":
        veredicto = "REPRODUCE"
    elif contexto == "DISTINTO" and resultado == "REPRODUCE":
        veredicto = "REPLICA-RESULTADO · CONTEXTO-DISTINTO"
    elif contexto == "IDENTICO" and resultado == "NO-REPRODUCE":
        veredicto = "NO-REPRODUCE"
    else:
        veredicto = "NO-REPRODUCE · CONTEXTO-DISTINTO"

    if imprime:
        print(f"\nVERIFY: {veredicto}   (CONTEXTO={contexto} · RESULTADO={resultado})")
    return {"veredicto": veredicto, "contexto": contexto, "resultado": resultado,
            "razones_contexto": razones_contexto, "deltas": deltas,
            "ids_faltantes": faltan, "problemas_replay": problemas_replay,
            "tolerancia": spec.get("tolerancia") or {}}


def cmd_verify(args) -> int:
    r = verify(args.calc_id)
    v = r["veredicto"]
    if v == "REPRODUCE":
        return 0
    if v in ("NO-VERIFICABLE", "NO-EJECUTABLE"):
        return 2
    return 1



# ── subcomandos `registro` y `status` ─────────────────────────────────────
#
# ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 (8/sep/2026). `registro` une los DOS
# LADOS del plan v2.0 §5 -- la DEMANDA que `cmd_demanda` derivo (que habria
# que volver a medir) y la OFERTA que las carpetas `data/corrida0/CALC-*/`
# demuestran (que se ejecuto de verdad) -- y emite las TRES vistas
# derivadas. `status` lee esas mismas filas en memoria (no los TSV en
# disco: un contador derivado de un archivo que alguien no re-derivo es
# exactamente el defecto que este aparato existe para no repetir).
#
# Lo que NO hace, declarado: no mide, no ejecuta medidores, no reejecuta
# microdato y no decide adopcion. `resultado_replay`/`contexto_replay`
# salen de `verify()` SOLO con `--verifica` explicito; sin esa bandera
# valen `NO-VERIFICADO`, que es lo que el registro sabe de verdad.

DEMANDA_RESULTADOS = CORRIDAS / "demanda-resultados.tsv"
DEMANDA_CORRIDAS = CORRIDAS / "demanda-corridas.tsv"
VISTA_CORRIDAS = CORRIDAS / "corridas.tsv"
VISTA_RESULTADOS = CORRIDAS / "resultados.tsv"
VISTA_USOS = CORRIDAS / "usos.tsv"
NO_CORRIDO_TSV = RAIZ / "forense" / "no-corrido.tsv"

NO_VERIFICADO = "NO-VERIFICADO"
NO_CORRIDA = "NO-CORRIDA"
NO_COMPARABLE = "NO-COMPARABLE"

COLS_VISTA_CORRIDAS = [
    "corrida_id", "origen", "spec_id", "estado", "generacion", "cuenta_gen2",
    # ACTO GEN2-T9 · P1: la marca de la regla E.1, en su propia columna --
    # un corredor envuelto se ve en el TSV sin re-derivar la regla.
    "envuelto_legacy", "motivo_cuenta_gen2",
    "spec_yaml_sha256", "script_path", "script_blob_sha256", "codigo_commit",
    "fecha", "n_resultados", "resultados_ids", "input_ids",
    "input_sha256_efectivos", "sello", "resultado_replay", "contexto_replay",
    "sucesor", "entorno_requerido", "receta", "orden_causal",
]
COLS_VISTA_RESULTADOS = [
    "resultado_id", "origen", "corrida_id", "spec_id", "valor", "tipo",
    "unidad", "estado", "generacion", "cuenta_gen2", "tolerancia",
    # NC-0069 / FP-365: la vara de ADOPCION, separada de la de
    # reproducibilidad (`tolerancia`). Vacia = defecto (grano del consumidor).
    "tolerancia_adopcion",
    "validacion_independiente", "valor_legacy", "delta_legacy", "sello",
    "depende_de", "n_usos", "sucesor",
]
COLS_VISTA_USOS = [
    "resultado_id", "consumidor", "tipo_uso", "activo", "reglas_impacto",
    "generacion_leida", "corrida0_generacion", "corrida0_resultado_id",
    "valor_materializado",
]


class ParoRegistro(Exception):
    """Validacion que PARA (plan v2.0 §5). No se escribe ninguna vista."""


def _leer_tsv_derivado(ruta: Path) -> list[dict]:
    """Como `_leer_tsv`, pero saltando la cabecera `# DERIVADO — NO EDITAR`
    que `_escribe` pone antes de la fila de columnas."""
    with ruta.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _dirs_calc() -> list[Path]:
    """Las carpetas de OFERTA, en orden determinista."""
    if not CORRIDAS.exists():
        return []
    return sorted((d for d in CORRIDAS.iterdir()
                   if d.is_dir() and d.name.startswith("CALC-")),
                  key=lambda d: d.name)


def _etiqueta(spec: dict, clave: str, defecto: str) -> str:
    etiquetas = spec.get("etiquetas") or {}
    valor = etiquetas.get(clave)
    return defecto if valor is None else str(valor)


def _regla_de(consumidor: str) -> str:
    """`milpa/tramite.yaml:<regla>:<conducta>` -> `<regla>`. Un consumidor
    que no trae regla (una celda del marco, p. ej.) declara su propio id."""
    partes = consumidor.split(":")
    return partes[1] if len(partes) >= 3 else (partes[-1] if partes else "")


# Campos por los que un consumidor MATERIALIZA la cifra que lee. `p` es la
# probabilidad de una conducta del motor; los otros dos, un coeficiente.
CAMPOS_VALOR_MATERIALIZADO = ["p", "valor_ejecutable", "valor"]


def _ids_corrida0_declarados() -> dict[str, dict]:
    """Consumidores que YA declaran `corrida0_resultado_id` y/o
    `corrida0_generacion` (plan v1.5 P2; plan v2.0 §2). Devuelve
    `consumidor -> {resultado_id, generacion, valor}`, con el MISMO formato
    de consumidor que `cmd_demanda` escribe, para que las dos vistas se
    puedan cruzar. El `valor` es la cifra MATERIALIZADA en el archivo del
    consumidor: es lo que `T-REPRO` compara contra el RESULT sellado
    (`p: 0.083742` + `corrida0_resultado_id: RESULT-0001`).

    `corrida0_generacion` (namespaced, ACTO GEN2-PRE-E5 · P2) es la SEÑAL
    INDEPENDIENTE de generacion: antes de esta correccion, "GEN2" se leia
    de la mera presencia de `corrida0_resultado_id`, lo que volvia
    circular al check que debia detectar un GEN2 SIN esa marca (T35(d) no
    podia construir el caso que decia vigilar). Los dos campos se
    recolectan por separado y un consumidor puede traer uno sin el otro
    -- es justo lo que T35 usa para avisar de una cadena incompleta. Un
    consumidor LEGACY existente no se toca solo para rellenar la marca
    nueva: los dos campos son opcionales y su ausencia es LEGACY, no error.

    Hoy el arbol no trae ninguno de los dos: `dependencias_numericas_
    legacy_activas` == `N_resultados_activos` es la lectura correcta, no
    un error. La funcion existe para que el dia que E5 selle la primera
    cifra GEN2 el registro la vea sin tocar codigo."""
    declarados: dict[str, dict] = {}
    for ruta in (TRAMITE, PROCEDENCIA):
        if not ruta.exists():
            continue
        try:
            crudo = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        rel = _rel(ruta)

        def _camina(nodo, contexto: list[str]) -> None:
            if isinstance(nodo, dict):
                marca_id = nodo.get("corrida0_resultado_id")
                marca_gen = nodo.get("corrida0_generacion")
                if marca_id or marca_gen:
                    nombre = (nodo.get("conducta") or nodo.get("id")
                              or nodo.get("clave") or "")
                    ruta_c = [c for c in contexto if c] + ([nombre] if nombre else [])
                    valor = next((nodo[c] for c in CAMPOS_VALOR_MATERIALIZADO
                                  if c in nodo), None)
                    declarados[f"{rel}:{':'.join(ruta_c)}"] = {
                        "resultado_id": str(marca_id) if marca_id else "",
                        "generacion": str(marca_gen) if marca_gen else "",
                        "valor": NO_DECLARADO if valor is None else valor,
                    }
                propio = nodo.get("id")
                for clave, valor in nodo.items():
                    if clave == "entonces":
                        _camina(valor, contexto + [str(propio or "")])
                    else:
                        _camina(valor, contexto)
            elif isinstance(nodo, list):
                for elemento in nodo:
                    _camina(elemento, contexto)

        _camina(crudo, [])
    return declarados


def _resultados_citados_en(ruta: Path) -> set[str]:
    """ids de RESULT citados por `corrida0_resultado_id` en cualquier nodo
    de `ruta` (ACTO GEN2-PRE-E5 · P3). Recorrido generico -- no asume la
    forma de `tramite.yaml`/`procedencia.yaml` -- para usarse sobre
    `milpa/tramite-ola5-propuesta-v0.yaml`: TODO el archivo es, por su
    propio encabezado, una propuesta `PENDIENTE-DE-MESA` que el motor no
    carga, asi que cualquier cita ahi cuenta como pendiente de adopcion
    (P3), nunca como consumidor activo."""
    if not ruta.exists():
        return set()
    try:
        crudo = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return set()
    citados: set[str] = set()

    def _camina(nodo) -> None:
        if isinstance(nodo, dict):
            marca = nodo.get("corrida0_resultado_id")
            if marca:
                citados.add(str(marca))
            for valor in nodo.values():
                _camina(valor)
        elif isinstance(nodo, list):
            for elemento in nodo:
                _camina(elemento)

    _camina(crudo)
    return citados


ESTADOS_CALC = ["BORRADOR", "SPEC-FIJADA", "PRE-FLIGHT-VERDE",
                "EJECUTADA-NO-SELLADA", "SELLADA"]


def estado_calc(calc_id: str, evalua_preflight: bool = False) -> dict:
    """Estado derivado UNICO de un CALC (ACTO GEN2-PRE-E5 ·
    CABLEADO-Y-AUTOMATIZACION-FINAL, P1; cierra NC-0010). Funcion PURA:
    no escribe ni lee ningun archivo de estado propio, solo deriva de los
    artefactos reales bajo `data/corrida0/<calc_id>/`.

        sin spec.yaml                              -> BORRADOR
        spec.yaml, sin ejecucion                   -> SPEC-FIJADA
        (evalua_preflight=True y preflight VERDE)  -> PRE-FLIGHT-VERDE
        ejecucion/resultados sin sello valido       -> EJECUTADA-NO-SELLADA
        sello completo valido                       -> SELLADA

    `SUPERADO→<sucesor>` NO es un estado de esta funcion: un CALC no sabe
    por si mismo si algo lo sucedio -- eso sigue siendo una propiedad que
    `registro()` deriva por encima, de la cadena `repite_de` (plan v1.5,
    P1: "no duplicarla dentro del CALC")."""
    d = _dir_calc(calc_id)
    ruta_spec = d / "spec.yaml"
    if not ruta_spec.exists():
        return {"calc_id": calc_id, "estado": "BORRADOR"}
    try:
        spec = yaml.safe_load(ruta_spec.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return {"calc_id": calc_id, "estado": "BORRADOR",
                "motivo": f"spec.yaml ilegible: {exc}"}
    if not isinstance(spec, dict):
        return {"calc_id": calc_id, "estado": "BORRADOR",
                "motivo": "spec.yaml no es un mapa"}

    ruta_ejec = d / "ejecucion.json"
    if not ruta_ejec.exists():
        detalle = {"calc_id": calc_id, "estado": "SPEC-FIJADA"}
        if evalua_preflight:
            try:
                pre = preflight(calc_id, imprime=False)
            except BloqueoPreflight as exc:
                detalle["motivo"] = f"preflight no evalua: {exc}"
                return detalle
            detalle["preflight"] = pre
            if pre.get("veredicto") == "VERDE":
                detalle["estado"] = "PRE-FLIGHT-VERDE"
        return detalle

    ejec = json.loads(ruta_ejec.read_text(encoding="utf-8"))
    ruta_res = d / "resultados.json"
    valores = (json.loads(ruta_res.read_text(encoding="utf-8")).get("resultados", {})
               if ruta_res.exists() else {})
    sello, razon_sello = _verifica_sello(d)
    if valores and sello == "COINCIDE":
        return {"calc_id": calc_id, "estado": "SELLADA"}
    return {"calc_id": calc_id, "estado": "EJECUTADA-NO-SELLADA",
            "sello": sello, "razon_sello": razon_sello, "ejec": ejec}


def cmd_estado(args) -> int:
    r = estado_calc(args.calc_id, evalua_preflight=getattr(args, "preflight", False))
    if getattr(args, "json", False):
        print(json.dumps(r, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    else:
        print(f"{r['calc_id']}: {r['estado']}")
        if r.get("motivo"):
            print(f"  motivo: {r['motivo']}")
    return 0


# ── ACTO GEN2-REGISTRO-REPLAY · P2 · evidencia de replay ──────────────────
#
# NC-0094, en una linea: `resultado_replay`/`contexto_replay` mezclaban DOS
# preguntas distintas -- «que dijo el replay» (evidencia, historica) y
# «puede esta sesion replayar» (capacidad, de hoy). Con las dos en la misma
# celda, regenerar el registro desde una caja sin corpus borraba veredictos
# ajenos: 23 corridas / 46 campos al SHA 66eed1b, incluidos NO-REPRODUCE
# (CALC-MOTOR-celdas-semilla) y NO-EJECUTABLE. Cambiar `NO-REPRODUCE` por
# «no verificado ahora» no demuestra que la discrepancia desaparecio.
#
# La separacion, sin inventar otra maquina de estados: los DOS EJES de E.3
# conservan su vocabulario sellado y son EVIDENCIA; la limitacion de la
# sesion presente se reporta APARTE (avisos y `registro --fuentes`), nunca
# sobreescribiendo la evidencia.
#
# La FUENTE de esa evidencia es `forense/replay-evidencia.tsv`. No es un
# TSV derivado y no se deriva de las vistas: es un asiento versionado que
# un acto escribe con cita. Se eligio archivo aparte porque la identidad
# que `sello.json`/`ejecucion.json` ya traen (corrida, hashes, spec,
# codigo, inputs, fecha, entorno) NO alcanza -- les faltan los DOS EJES con
# sus razones -- y los bytes sellados no se editan para alojar metadatos
# (E.3). Las vistas siguen siendo derivadas de esta fuente; los TSV
# derivados NO se vuelven su propia fuente.
#
# VIGENCIA: la evidencia vale para la identidad que se verifico. Si la spec,
# el blob del script o los SHA de los inputs efectivos cambian, el
# comprobante deja de ser vigente para el objeto nuevo -- no se arrastra, no
# se degrada a otro veredicto: se declara NO-VERIFICADO con la razon.
# `codigo_commit`, `fecha` y `entorno` se asientan como descripcion, no como
# llave: un commit distinto con el mismo blob no cambia lo que se ejecuto.

REPLAY_EVIDENCIA = RAIZ / "forense" / "replay-evidencia.tsv"

COLS_REPLAY_EVIDENCIA = [
    "calc_id", "corrida_id", "resultado_replay", "contexto_replay",
    "razones", "spec_yaml_sha256", "script_blob_sha256",
    "input_sha256_efectivos", "codigo_commit", "fecha_verificacion",
    "entorno", "procedencia", "alcance", "nota",
]

# Veredictos que CONCLUYEN sobre la reproducibilidad. Los de fuera de esta
# lista (`NO-EJECUTABLE`, `NO-VERIFICABLE`) dicen que la sesion no pudo
# pronunciarse -- son limitacion, no hallazgo sobre el numero -- y por eso
# no pisan un veredicto anterior.
VEREDICTOS_CONCLUYENTES = frozenset({
    "REPRODUCE", "NO-REPRODUCE",
    "REPLICA-RESULTADO · CONTEXTO-DISTINTO",
    "NO-REPRODUCE · CONTEXTO-DISTINTO",
})


def _lee_evidencia_replay() -> dict:
    """`calc_id -> fila` de `forense/replay-evidencia.tsv`. Ausente = {}:
    sin asiento no hay evidencia que proyectar, y eso NO es un error."""
    if not REPLAY_EVIDENCIA.exists():
        return {}
    filas = {}
    for f in _leer_tsv(REPLAY_EVIDENCIA):
        if f.get("calc_id"):
            filas[f["calc_id"]] = f
    return filas


def _identidad_replay(ejec: dict) -> tuple[str, str, str]:
    """La terna que hace vigente (o no) un comprobante: spec, codigo e
    inputs efectivamente verificados. Mismo formato que la vista, para que
    un humano pueda comparar las dos columnas a ojo."""
    sha_inputs = (ejec or {}).get("input_sha256") or {}
    return (
        (ejec or {}).get("spec_yaml_sha256") or NO_DECLARADO,
        (ejec or {}).get("script_blob_sha256") or NO_DECLARADO,
        ",".join(f"{i}={sha_inputs[i]}" for i in sorted(sha_inputs)) or "PENDIENTE",
    )


def _evidencia_vigente(ev: dict, ejec: dict) -> tuple[bool, str]:
    """`(vigente, razon)`. Un cambio de identidad NO invalida la evidencia
    como historia -- invalida presentarla como vigente para ESTE objeto."""
    spec_sha, script_sha, inputs = _identidad_replay(ejec)
    difieren = []
    for campo, hoy in (("spec_yaml_sha256", spec_sha),
                       ("script_blob_sha256", script_sha),
                       ("input_sha256_efectivos", inputs)):
        asentado = (ev.get(campo) or "").strip()
        if asentado and asentado != hoy:
            difieren.append(f"{campo}: asentado={asentado} · hoy={hoy}")
    if difieren:
        return False, " ; ".join(difieren)
    return True, ""


def _proyecta_replay(calc_id: str, ejec: dict, fresco: dict | None,
                     evidencia: dict) -> tuple[str, str, dict, list[str]]:
    """El nucleo de NC-0094. Devuelve `(replay, contexto, fuente, avisos)`.

    Precedencia DECLARADA, y ninguna rama borra evidencia:

      1. un veredicto CONCLUYENTE de esta sesion (`--verifica`) manda --
         es observacion de hoy sobre la misma identidad. Si contradice al
         asiento, se avisa con AMBOS: conservar historia no privilegia el
         ultimo exito, y un `NO-REPRODUCE` nuevo no queda escondido detras
         de un `REPRODUCE` viejo;
      2. si esta sesion NO pudo pronunciarse (`NO-EJECUTABLE` /
         `NO-VERIFICABLE`, tipicamente por falta de corpus) y hay asiento
         vigente, se proyecta el ASIENTO y la limitacion de la sesion se
         reporta APARTE. Esta es la rama que impide que una caja sin
         microdato borre lo que otra si midio;
      3. asiento vigente sin verificacion de hoy -> se proyecta el asiento;
      4. asiento NO vigente (cambio de spec/codigo/inputs) -> NO-VERIFICADO
         con la razon: la evidencia anterior no es del objeto de hoy;
      5. nada de lo anterior -> lo que la sesion sepa, y si no sabe nada,
         `NO-VERIFICADO`, que sigue siendo la verdad cuando no hay fuente.
    """
    avisos: list[str] = []
    ev = evidencia.get(calc_id)
    vigente, razon_no_vigente = (False, "")
    if ev:
        vigente, razon_no_vigente = _evidencia_vigente(ev, ejec)

    def _fuente(clase, **extra):
        f = {"calc_id": calc_id, "clase": clase}
        f.update(extra)
        return f

    if fresco is not None:
        v = fresco.get("veredicto", NO_VERIFICADO)
        ctx = fresco.get("contexto", NO_VERIFICADO)
        if v in VEREDICTOS_CONCLUYENTES:
            if ev and vigente and ev["resultado_replay"] != v:
                avisos.append(
                    f"REPLAY-CONTRADICE-ASIENTO: {calc_id} -- esta sesion "
                    f"observa {v}/{ctx}; el asiento vigente dice "
                    f"{ev['resultado_replay']}/{ev['contexto_replay']} "
                    f"({ev.get('fecha_verificacion') or 'sin fecha'}). Se "
                    f"proyecta lo observado hoy; el asiento NO se borra: "
                    f"actualizalo con cita en la nota de cierre del lote")
            return v, ctx, _fuente("VERIFICADO-EN-ESTA-SESION",
                                   veredicto=v, contexto=ctx), avisos
        # (2) la sesion no pudo pronunciarse.
        if ev and vigente:
            avisos.append(
                f"REPLAY-NO-VERIFICABLE-HOY: {calc_id} -- esta sesion no pudo "
                f"replayar ({v}); NO degrada la evidencia asentada "
                f"{ev['resultado_replay']}/{ev['contexto_replay']}, que se "
                f"proyecta como evidencia historica")
            return (ev["resultado_replay"], ev["contexto_replay"],
                    _fuente("EVIDENCIA-HISTORICA", asiento=ev,
                            limitacion_sesion=v), avisos)
        avisos.append(
            f"REPLAY-SIN-EVIDENCIA: {calc_id} -- esta sesion observa {v} y no "
            f"hay asiento vigente en {_rel(REPLAY_EVIDENCIA)}")
        return v, ctx, _fuente("OBSERVACION-SIN-ASIENTO", veredicto=v), avisos

    if ev and vigente:
        return (ev["resultado_replay"], ev["contexto_replay"],
                _fuente("EVIDENCIA-HISTORICA", asiento=ev), avisos)
    if ev and not vigente:
        avisos.append(
            f"EVIDENCIA-NO-VIGENTE: {calc_id} -- hay asiento "
            f"({ev['resultado_replay']}/{ev['contexto_replay']}, "
            f"{ev.get('fecha_verificacion') or 'sin fecha'}) pero la identidad "
            f"cambio, asi que NO se presenta como vigente -> {NO_VERIFICADO}. "
            f"{razon_no_vigente}")
        return NO_VERIFICADO, NO_VERIFICADO, _fuente(
            "ASIENTO-NO-VIGENTE", asiento=ev, razon=razon_no_vigente), avisos
    return NO_VERIFICADO, NO_VERIFICADO, _fuente("SIN-FUENTE"), avisos


def _lee_oferta(verifica: bool) -> list[dict]:
    """Un registro por carpeta `CALC-*/`. Levanta `ParoRegistro` en las
    validaciones que el plan declara bloqueantes."""
    evidencia = _lee_evidencia_replay()
    oferta = []
    for d in _dirs_calc():
        calc_id = d.name
        ruta_spec = d / "spec.yaml"
        if not ruta_spec.exists():
            raise ParoRegistro(f"CALC-SIN-SPEC: {_rel(d)} no trae spec.yaml")
        try:
            spec = yaml.safe_load(ruta_spec.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise ParoRegistro(f"CALC-SIN-SPEC: {_rel(ruta_spec)} ilegible: {exc}")
        if not isinstance(spec, dict):
            raise ParoRegistro(f"CALC-SIN-SPEC: {_rel(ruta_spec)} no es un mapa")

        ejec, valores = None, {}
        ruta_ejec, ruta_res = d / "ejecucion.json", d / "resultados.json"
        if ruta_ejec.exists():
            ejec = json.loads(ruta_ejec.read_text(encoding="utf-8"))
        if ruta_res.exists():
            valores = json.loads(ruta_res.read_text(encoding="utf-8")).get("resultados", {})

        sello, razon_sello = _verifica_sello(d)
        # PARA: hay RESULT materializados y el sello no los respalda. Un
        # numero sellado a medias es peor que un numero ausente.
        if valores and sello != "COINCIDE":
            raise ParoRegistro(f"RESULT-SIN-SELLO: {calc_id} trae "
                               f"resultados.json y su sello dice {sello} "
                               f"({razon_sello})")
        generacion = _etiqueta(spec, "generacion", "GEN2")
        # ACTO GEN2-T9 · P1: la etiqueta de la spec ya no es la ultima
        # palabra. Manda la firma de mesa (`decisiones.tsv`), y en su
        # ausencia la regla E.1 sobre los inputs declarados.
        cuenta, motivo_cuenta = _cuenta_gen2_resuelto(calc_id, spec, _lee_decisiones())
        # Misma maquina que `estado_calc()` (P1, NC-0010): no una segunda
        # implementacion del mismo estado. `spec.yaml` ya existe (se
        # verifico arriba) y `evalua_preflight` por defecto es False, asi
        # que aqui solo salen SPEC-FIJADA / EJECUTADA-NO-SELLADA / SELLADA.
        estado = estado_calc(calc_id)["estado"]

        faltan: list[str] = []
        if estado == "SELLADA":
            faltan = [c for c in ("spec_yaml_sha256", "script_blob_sha256")
                      if not (ejec or {}).get(c)]
            sha_inputs = (ejec or {}).get("input_sha256") or {}
            faltan += [f"input_sha256[{i}]" for i in ((ejec or {}).get("input_ids") or [])
                       if not sha_inputs.get(i)]
        # PARA solo si la corrida CUENTA como GEN2. Un replay LEGACY-GEN1
        # sellado antes de que `ACTO GEN2-E3-1` endureciera el esquema no
        # puede traer campos que en su momento no existian, y su sello no se
        # reescribe para complacer a este registro: se avisa y se cuenta
        # aparte. Es el caso medido de `CALC-SMOKE-0001`, sellado por E3 sin
        # `spec_yaml_sha256` -- "linea base congela GEN1".
        if faltan and cuenta == "SI":
            raise ParoRegistro(f"HASH-AUSENTE: {calc_id} sellada sin "
                               f"{', '.join(faltan)}")

        # ACTO GEN2-REGISTRO-REPLAY · P2 (NC-0094). Antes esta rama era
        # `NO_VERIFICADO` salvo `--verifica`, y por eso una regeneracion
        # desde una caja sin corpus borraba veredictos ajenos. Ahora la
        # evidencia tiene fuente propia y la capacidad de ESTA sesion se
        # reporta aparte; ninguna rama pisa un veredicto anterior.
        fuente_replay: dict = {"calc_id": calc_id, "clase": "NO-CORRIDA"}
        avisos_replay: list[str] = []
        if estado != "SELLADA":
            replay, contexto = NO_CORRIDA, NO_CORRIDA
        else:
            fresco = verify(calc_id, imprime=False) if verifica else None
            replay, contexto, fuente_replay, avisos_replay = _proyecta_replay(
                calc_id, ejec or {}, fresco, evidencia)

        oferta.append({
            "calc_id": calc_id, "spec": spec, "ejec": ejec or {},
            "valores": valores, "sello": sello, "estado": estado,
            "generacion": generacion, "cuenta_gen2": cuenta,
            "motivo_cuenta_gen2": motivo_cuenta,
            "envuelto_legacy": "SI" if _inputs_legacy_de(spec) else "NO",
            "replay": replay, "contexto": contexto,
            "fuente_replay": fuente_replay, "avisos_replay": avisos_replay,
            "hashes_faltantes": faltan,
            "repite_de": str(spec.get("repite_de") or ""),
        })

    # ACTO GEN2-T9 · P1: el cierre transitivo corre DESPUES de leer todas
    # las specs -- antes no se puede saber si el padre es envuelto -- y
    # re-resuelve `cuenta_gen2` de quien se vuelva envuelto por cadena. La
    # firma de mesa en `decisiones.tsv` sigue mandando sobre ambos.
    _propaga_envuelto(oferta)
    decisiones = _lee_decisiones()
    for o in oferta:
        if o["envuelto_legacy"] == "SI" and o.get("_via_cadena"):
            if not decisiones.get(o["calc_id"], "").startswith("cuenta_gen2="):
                o["cuenta_gen2"] = "NO"
                o["motivo_cuenta_gen2"] = (
                    f"regla E.1 por CADENA: consume RESULT de "
                    f"{o['_via_cadena']}, que es corredor envuelto LEGACY")
    return oferta


# ── ACTO GEN2-T9 · P1 · D-1 de mesa, ejecutable ────────────────────────────
#
# Firma de mesa verbatim (8/sep/2026): «decision 1 no cuentan como Gen2, no
# cometamos un error sobre los 600 PR's que ya cagamos».
#
# LA REGLA, con nombre (E.1): NINGUN `CALC` cuyo input resuelva a
# `milpa/tramite.yaml`, `milpa/procedencia.yaml` o `corridas-R/M/L` cuenta
# como GEN2, POR COMPLETA QUE SEA SU CADENA. Un corredor envuelto puede tener
# spec endurecida, sello valido y `verify REPRODUCE/IDENTICO` -- y aun asi el
# numero que emite viene del aparato GEN1. La calidad de la envoltura no
# cambia la procedencia del numero.
#
# Se aplica MECANICAMENTE sobre los inputs DECLARADOS de la spec: no se
# edita ningun `spec.yaml` sellado (E.3), y `decisiones.tsv` es donde mesa
# firma el caso por caso.
INSUMOS_LEGACY_GEN1 = (
    "milpa/tramite.yaml",
    "milpa/procedencia.yaml",
    "forense/prereg-duelo-v2/corridas-R/",
    "forense/prereg-duelo-v2/corridas-M/",
    "forense/prereg-duelo-v2/corridas-L/",
)


def _inputs_legacy_de(spec: dict) -> list[str]:
    """Los inputs DECLARADOS de la spec que caen bajo la regla E.1.

    Lee `inputs[].ruta` -- lo que la spec declara --, no el disco: una spec
    que no declara su insumo ya falla antes, en `_resuelve_inputs`.
    """
    malos = []
    for entrada in (spec.get("inputs") or []):
        if not isinstance(entrada, dict):
            continue
        ruta = str(entrada.get("ruta") or "")
        for patron in INSUMOS_LEGACY_GEN1:
            if ruta == patron or ruta.startswith(patron):
                malos.append(f"{entrada.get('id') or '?'}={ruta}")
                break
    return malos


RE_CALC_RESULTADOS = re.compile(
    r"^data/corrida0/(CALC-[A-Za-z0-9_.\-]+)/resultados\.json$")


def _propaga_envuelto(oferta: list[dict]) -> None:
    """Cierre TRANSITIVO de la regla E.1 sobre la cadena de CALC.

    «...por completa que sea su cadena» no es una figura retorica: un
    agregado cuyos inputs son `RESULT-*` de un corredor envuelto hereda la
    procedencia de esos numeros. `CALC-AGG-marco-M-sorteado-v1_3` no nombra
    `milpa/tramite.yaml` en ningun input -- consume
    `CALC-M-.../resultados.json` --, y sin este cierre habria pasado por GEN2
    limpio leyendo cifras del emisor GEN1. Es exactamente el error que D-1
    manda no repetir.

    Punto fijo sobre el grafo declarado de inputs; termina porque el conjunto
    de envueltos solo crece y esta acotado por el numero de CALC.
    """
    por_id = {o["calc_id"]: o for o in oferta}
    cambio = True
    while cambio:
        cambio = False
        for o in oferta:
            if o["envuelto_legacy"] == "SI":
                continue
            for entrada in (o["spec"].get("inputs") or []):
                if not isinstance(entrada, dict):
                    continue
                m = RE_CALC_RESULTADOS.match(str(entrada.get("ruta") or ""))
                if not m:
                    continue
                padre = por_id.get(m.group(1))
                if padre is not None and padre["envuelto_legacy"] == "SI":
                    o["envuelto_legacy"] = "SI"
                    o["_via_cadena"] = m.group(1)
                    cambio = True
                    break


def _cuenta_gen2_resuelto(calc_id: str, spec: dict,
                          decisiones: dict) -> tuple[str, str]:
    """`(cuenta_gen2, motivo)`. Precedencia DECLARADA, no inventada:

      1. la firma de mesa en `data/corrida0/decisiones.tsv` (D-1);
      2. la regla E.1 sobre los inputs declarados -- mecanica;
      3. la etiqueta de la propia spec;
      4. el default por `generacion`.

    `PENDIENTE-DE-MESA` sobrevive como valor propio cuando ni mesa ni la
    regla lo resuelven: no se colapsa a `NO` por comodidad del contador.
    """
    generacion = _etiqueta(spec, "generacion", "GEN2")
    decision = decisiones.get(calc_id, "")
    if decision.startswith("cuenta_gen2="):
        valor = decision.split("=", 1)[1].split("·")[0].strip()
        return valor, f"decision de mesa (`decisiones.tsv`): {_limpia(decision)}"
    legacy = _inputs_legacy_de(spec)
    if legacy:
        return "NO", ("regla E.1 (ACTO GEN2-T9, D-1): input LEGACY GEN1 "
                      + ", ".join(legacy))
    etiqueta = _etiqueta(spec, "cuenta_gen2", None)
    if etiqueta is not None:
        return etiqueta, "etiqueta de la spec"
    return ("NO" if generacion == GENERACION_LEGADO else "SI"), "default por generacion"


def _filas_registro(verifica: bool = False) -> dict:
    """Deriva las tres vistas. Devuelve `{corridas, resultados, usos,
    avisos}`; levanta `ParoRegistro` sin escribir nada si una validacion
    bloqueante falla."""
    if not DEMANDA_RESULTADOS.exists() or not DEMANDA_CORRIDAS.exists():
        raise ParoRegistro("DEMANDA-AUSENTE: falta `demanda-resultados.tsv` o "
                           "`demanda-corridas.tsv` -- corre `corrida0 demanda` primero")
    demanda_res = _leer_tsv_derivado(DEMANDA_RESULTADOS)
    demanda_corr = _leer_tsv_derivado(DEMANDA_CORRIDAS)
    oferta = _lee_oferta(verifica)
    marcas = _ids_corrida0_declarados()
    avisos: list[str] = []
    # ACTO GEN2-REGISTRO-REPLAY · P2: la limitacion de ESTA sesion viaja
    # como aviso, APARTE de la columna de evidencia. Es la mitad del arreglo
    # de NC-0094 que no se ve en el TSV -- y por eso tiene que verse aqui.
    fuentes_replay = {}
    for o in oferta:
        avisos.extend(o.get("avisos_replay") or [])
        if o.get("fuente_replay"):
            fuentes_replay[o["calc_id"]] = o["fuente_replay"]

    sucesor_de = {o["repite_de"]: o["calc_id"] for o in oferta if o["repite_de"]}

    filas_corridas, filas_resultados, filas_usos = [], [], []
    vistos_corrida, vistos_resultado = set(), set()

    def _unico(coleccion: set, clave: str, donde: str) -> None:
        if clave in coleccion:
            raise ParoRegistro(f"ID-DUPLICADO: {clave} aparece dos veces en {donde}")
        coleccion.add(clave)

    # ── lado DEMANDA ──────────────────────────────────────────────────────
    for c in demanda_corr:
        _unico(vistos_corrida, c["corrida_id"], "corridas")
        filas_corridas.append({
            "corrida_id": c["corrida_id"], "origen": "DEMANDA",
            "spec_id": c["medidor_o_spec_candidato"], "estado": "PENDIENTE",
            "generacion": "GEN2-PENDIENTE", "cuenta_gen2": "SI",
            # Una corrida DEMANDADA todavia no tiene spec: no hay inputs
            # declarados sobre los que la regla E.1 pueda pronunciarse.
            "envuelto_legacy": "PENDIENTE",
            "motivo_cuenta_gen2": "demanda sin spec: la regla E.1 se evalua "
                                  "cuando la spec declare sus inputs",
            "spec_yaml_sha256": "PENDIENTE", "script_path": "PENDIENTE",
            "script_blob_sha256": "PENDIENTE", "codigo_commit": "PENDIENTE",
            "fecha": "PENDIENTE", "n_resultados": c["n_resultados"],
            "resultados_ids": c["resultados_ids"],
            "input_ids": c["payload_ids"], "input_sha256_efectivos": "PENDIENTE",
            "sello": "PENDIENTE", "resultado_replay": NO_CORRIDA,
            "contexto_replay": NO_CORRIDA, "sucesor": "",
            "entorno_requerido": c["entorno_requerido"], "receta": c["receta"],
            "orden_causal": c["orden_causal"],
        })

    usos_por_resultado: dict[str, int] = {}
    for r in demanda_res:
        rid = r["resultado_id"]
        _unico(vistos_resultado, (r["corrida_natural"], rid), "resultados")
        if r["corrida_natural"] not in vistos_corrida:
            raise ParoRegistro(f"RESULT-SIN-CALC: {rid} apunta a la corrida "
                               f"{r['corrida_natural']}, que no existe")
        marca = marcas.get(r["consumidor"]) or {}
        generacion_declarada = marca.get("generacion", "")
        filas_resultados.append({
            "resultado_id": rid, "origen": "DEMANDA",
            "corrida_id": r["corrida_natural"], "spec_id": "PENDIENTE",
            "valor": "PENDIENTE", "tipo": r["tipo"], "unidad": NO_DECLARADO,
            "estado": r["estado"], "generacion": "GEN2-PENDIENTE",
            "cuenta_gen2": "SI", "tolerancia": "PENDIENTE",
            "tolerancia_adopcion": "PENDIENTE",
            "validacion_independiente": r["validacion_independiente"],
            "valor_legacy": r["valor_legacy"], "delta_legacy": NO_COMPARABLE,
            "sello": "PENDIENTE", "depende_de": r["depende_de"],
            "n_usos": 1, "sucesor": "",
        })
        usos_por_resultado[rid] = 1
        filas_usos.append({
            "resultado_id": rid, "consumidor": r["consumidor"],
            "tipo_uso": r["tipo"], "activo": "SI",
            "reglas_impacto": _regla_de(r["consumidor"]),
            # `generacion_leida` se deriva de `corrida0_generacion`, una
            # señal INDEPENDIENTE de si `corrida0_resultado_id` esta
            # presente (P2, ACTO GEN2-PRE-E5): sin `corrida0_generacion:
            # GEN2` el consumidor sigue leyendo la cifra GEN1 materializada
            # y es una dependencia legacy activa, tenga o no una marca de
            # resultado (una marca sin generacion es cadena incompleta,
            # que T35 avisa aparte -- no basta para contar como GEN2).
            "generacion_leida": ("GEN2" if generacion_declarada == "GEN2"
                                 else GENERACION_LEGADO),
            "corrida0_generacion": generacion_declarada,
            "corrida0_resultado_id": marca.get("resultado_id", ""),
            "valor_materializado": marca.get("valor", NO_DECLARADO),
        })

    # ── lado OFERTA ───────────────────────────────────────────────────────
    for o in oferta:
        calc_id, ejec, spec = o["calc_id"], o["ejec"], o["spec"]
        sucesor = sucesor_de.get(calc_id, "")
        estado = f"SUPERADO→{sucesor}" if sucesor else o["estado"]
        corrida_id = ejec.get("corrida_id") or calc_id
        _unico(vistos_corrida, corrida_id, "corridas")
        ids_res = sorted(o["valores"])
        sha_inputs = ejec.get("input_sha256") or {}
        decl_res = {str(d.get("id")): d for d in (spec.get("resultados") or [])
                    if isinstance(d, dict)}
        tol = spec.get("tolerancia") or {}
        # NC-0069: `tolerancia_adopcion` se declara por RESULT o, si no, una
        # vez para toda la spec. Ausente NO es un defecto: es el defecto
        # (grano del consumidor). `NO-APLICA` es un VALOR -- exige la
        # tolerancia de reproducibilidad -- y por eso se distingue de vacio.
        tol_adop_spec = spec.get("tolerancia_adopcion")
        filas_corridas.append({
            "corrida_id": corrida_id, "origen": "OFERTA", "spec_id": calc_id,
            "estado": estado, "generacion": o["generacion"],
            "cuenta_gen2": o["cuenta_gen2"],
            "envuelto_legacy": o["envuelto_legacy"],
            "motivo_cuenta_gen2": o["motivo_cuenta_gen2"],
            "spec_yaml_sha256": ejec.get("spec_yaml_sha256") or NO_DECLARADO,
            "script_path": ejec.get("script_path") or str(spec.get("script") or NO_DECLARADO),
            "script_blob_sha256": ejec.get("script_blob_sha256") or NO_DECLARADO,
            "codigo_commit": ejec.get("git_commit") or NO_DECLARADO,
            "fecha": ejec.get("fecha") or NO_DECLARADO,
            "n_resultados": len(ids_res),
            "resultados_ids": ",".join(ids_res),
            "input_ids": ",".join(ejec.get("input_ids") or []),
            "input_sha256_efectivos": ",".join(
                f"{i}={sha_inputs[i]}" for i in sorted(sha_inputs)) or "PENDIENTE",
            "sello": o["sello"], "resultado_replay": o["replay"],
            "contexto_replay": o["contexto"], "sucesor": sucesor,
            "entorno_requerido": "NUBE-O-CAJA", "receta": "OK",
            "orden_causal": NO_DECLARADO,
        })
        for rid in ids_res:
            # La unicidad de un RESULT es POR CORRIDA. Un replay declarado
            # (`repite_de`) reproduce los mismos ids a proposito -- es lo que
            # significa replicar. Lo que si para es el mismo id en dos
            # corridas SIN cadena de sucesion, que se verifica abajo.
            _unico(vistos_resultado, (corrida_id, rid), "resultados")
            decl = decl_res.get(rid, {})
            filas_resultados.append({
                "resultado_id": rid, "origen": "OFERTA",
                "corrida_id": corrida_id, "spec_id": calc_id,
                "valor": o["valores"][rid],
                "tipo": str(decl.get("tipo") or NO_DECLARADO),
                "unidad": str(decl.get("unidad") or NO_DECLARADO),
                "estado": estado, "generacion": o["generacion"],
                "cuenta_gen2": o["cuenta_gen2"],
                "tolerancia": json.dumps(tol, ensure_ascii=False, sort_keys=True,
                                         default=str) if tol else NO_DECLARADO,
                "tolerancia_adopcion": _texto_tol_adopcion(
                    decl.get("tolerancia_adopcion", tol_adop_spec)),
                "validacion_independiente": _etiqueta(spec, "validacion_independiente",
                                                      "NO-HECHA"),
                "valor_legacy": NO_COMPARABLE, "delta_legacy": NO_COMPARABLE,
                "sello": o["sello"], "depende_de": "", "n_usos": 0,
                "sucesor": sucesor,
            })
        if o["hashes_faltantes"]:
            avisos.append(f"HASH-AUSENTE-EN-LEGACY: {calc_id} "
                          f"({o['generacion']}, cuenta_gen2={o['cuenta_gen2']}) "
                          f"no trae {', '.join(o['hashes_faltantes'])} -- sellada "
                          f"antes del esquema endurecido de ACTO GEN2-E3-1; su "
                          f"sello NO se reescribe")
        if o["cuenta_gen2"] == "SI" and estado.startswith("SELLADA"):
            avisos.append(f"CALC-SIN-CONSUMIDOR-ACTIVO: {calc_id} esta sellada "
                          f"y ningun consumidor activo la cita todavia")

    # PARA: el mismo RESULT en dos corridas que NO son la misma cadena de
    # replay. `repite_de` es lo unico que autoriza repetir un id.
    repite_de = {o["calc_id"]: o["repite_de"] for o in oferta}

    def _raiz(calc: str) -> str:
        visto = set()
        while repite_de.get(calc) and calc not in visto:
            visto.add(calc)
            calc = repite_de[calc]
        return calc

    por_id: dict[str, list[dict]] = {}
    for f in filas_resultados:
        por_id.setdefault(f["resultado_id"], []).append(f)
    for rid, filas in por_id.items():
        raices = {_raiz(f["spec_id"]) for f in filas}
        if len(filas) > 1 and len(raices) > 1:
            raise ParoRegistro(
                f"ID-DUPLICADO: {rid} aparece en "
                f"{', '.join(sorted(f['corrida_id'] for f in filas))} sin "
                f"cadena `repite_de` que las una")

    # El indice de resolucion prefiere la corrida VIGENTE: un uso resuelve
    # al RESULT que no fue superado.
    indice_resultados: dict[str, dict] = {}
    for f in filas_resultados:
        previo = indice_resultados.get(f["resultado_id"])
        if previo is None or str(previo["estado"]).startswith("SUPERADO"):
            indice_resultados[f["resultado_id"]] = f

    # ── validaciones que PARAN sobre el grafo ya unido ─────────────────────
    for u in filas_usos:
        if u["resultado_id"] not in indice_resultados:
            raise ParoRegistro(f"USO-A-RESULT-INEXISTENTE: {u['consumidor']} "
                               f"usa {u['resultado_id']}, que no existe")
        marca = u["corrida0_resultado_id"]
        if marca:
            destino = indice_resultados.get(marca)
            if destino is None:
                raise ParoRegistro(f"USO-A-RESULT-INEXISTENTE: {u['consumidor']} "
                                   f"declara corrida0_resultado_id={marca}, "
                                   f"que no existe")
            if destino["generacion"] == GENERACION_LEGADO:
                raise ParoRegistro(f"CONSUMIDOR-ACTIVO-A-LEGACY: {u['consumidor']} "
                                   f"es GEN2 y resuelve a {marca}, que es "
                                   f"{GENERACION_LEGADO}")
    _verifica_ciclos(filas_resultados)

    # ── avisos (no paran) ─────────────────────────────────────────────────
    for f in filas_resultados:
        n_usos = usos_por_resultado.get(f["resultado_id"], 0)
        if n_usos == 0:
            avisos.append(f"RESULT-SIN-CONSUMIDOR: {f['resultado_id']} "
                          f"({f['spec_id']}) no lo cita ningun consumidor")
        # `legacy sin sucesor` avisa de una cifra GEN1 que alguien SIGUE
        # leyendo y nadie va a remedir. Un replay que nadie consume ya lo
        # dice RESULT-SIN-CONSUMIDOR; repetirlo aqui es ruido, no señal.
        elif f["generacion"] == GENERACION_LEGADO and not f["sucesor"]:
            avisos.append(f"LEGACY-SIN-SUCESOR: {f['resultado_id']} es "
                          f"{GENERACION_LEGADO} y no declara sucesor")
    return {"corridas": filas_corridas, "resultados": filas_resultados,
            "usos": filas_usos, "avisos": avisos,
            "fuentes_replay": fuentes_replay}


def _verifica_ciclos(filas: list[dict]) -> None:
    """El grafo `depende_de` de las vistas unidas sigue siendo aciclico.
    `cmd_demanda` ya lo verifico sobre su propio lado; aqui se re-verifica
    sobre la union, que es un grafo distinto."""
    hijos = {f["resultado_id"]: [d for d in str(f["depende_de"]).split(",") if d]
             for f in filas}
    estado: dict[str, int] = {}

    def visita(nodo: str, pila: list[str]) -> None:
        if estado.get(nodo) == 2:
            return
        if estado.get(nodo) == 1:
            ciclo = " -> ".join(pila[pila.index(nodo):] + [nodo])
            raise ParoRegistro(f"CICLO: {ciclo}")
        estado[nodo] = 1
        for h in hijos.get(nodo, []):
            if h in hijos:
                visita(h, pila + [nodo])
        estado[nodo] = 2

    for nodo in hijos:
        visita(nodo, [])


def _texto_vista(columnas: list[str], filas: list[dict]) -> str:
    """Los MISMOS bytes que `_escribe` pondria en disco -- sin escribir
    nada. `registro(escribe=False)` lo usa para poder diferenciar contra lo
    que ya existe sin tocar el arbol."""
    partes = [CABECERA_DERIVADO, "\t".join(columnas)]
    partes.extend("\t".join(str(fila[c]) for c in columnas) for fila in filas)
    return "\n".join(partes) + "\n"


def _imprime_diff_vista(ruta: Path, columnas: list[str], filas: list[dict]) -> None:
    """FP-359: la fotocopiadora se desarma -- sin `--escribe`, `registro`
    imprime el diff que ESCRIBIRIA, nunca lo escribe. `ruta` puede no
    existir (primera derivacion): el diff sale contra `""`, no contra un
    intento de leer un archivo ausente."""
    actual = ruta.read_text(encoding="utf-8") if ruta.exists() else ""
    nuevo = _texto_vista(columnas, filas)
    if actual == nuevo:
        print(f"SECO {_rel(ruta)}: sin diferencia con el archivo en disco "
              f"({len(filas)} filas)")
        return
    diff = list(difflib.unified_diff(
        actual.splitlines(keepends=True), nuevo.splitlines(keepends=True),
        fromfile=f"a/{_rel(ruta)}", tofile=f"b/{_rel(ruta)} (lo que --escribe pondria)"))
    print(f"SECO {_rel(ruta)}: {len(filas)} filas -- diff que `--escribe` "
          f"pondria ({sum(1 for l in diff if l.startswith('+') and not l.startswith('+++'))} "
          f"+ / {sum(1 for l in diff if l.startswith('-') and not l.startswith('---'))} -):")
    for linea in diff:
        print(f"  {linea}", end="" if linea.endswith("\n") else "\n")


# ── ACTO GEN2-REGISTRO-REPLAY · P1 · la contencion, mecanica ──────────────
#
# La adenda de NC-0094 pedia a mano lo que sigue: pegar el diff antes de
# escribir y parar si tocaba corridas ajenas. Aqui deja de depender de que
# alguien se acuerde. `registro --escribe` calcula el diff de los DOS EJES
# contra las vistas PUBLICADAS antes de tocar ningun TSV; si una corrida
# AJENA al lote autorizado cambiaria de veredicto, se niega, lista los ids
# con sus transiciones y termina sin escribir. No hay `--force` y no hay
# borrado silencioso: la unica forma de mover un veredicto ajeno es
# nombrarlo en `--lote`, que es exactamente la «razon explicita» que la
# validacion de aceptacion (a) exige.
#
# Una corrida que NO esta en la vista publicada no tiene veredicto que
# pisar: registrar un lote nuevo nunca cae en esta proteccion.


class ReplayPisado(ParoRegistro):
    """P1: la escritura borraria o cambiaria evidencia de replay ajena al
    lote autorizado. Hereda de `ParoRegistro` para que `cmd_registro` ya la
    trate como lo que es: un PARO que no escribe ninguna vista."""


def _lote_autorizado(lote) -> set:
    """`--lote CALC-A,CALC-B` o `--lote CALC-A --lote CALC-B`. Sin lote, el
    conjunto autorizado es VACIO: ninguna transicion de veredicto pasa sin
    que alguien la nombre."""
    ids = set()
    for item in (lote or []):
        ids.update(x.strip() for x in str(item).split(",") if x.strip())
    return ids


def _transiciones_replay(filas_corridas: list[dict]) -> list[tuple]:
    """`(corrida_id, campo, publicado, propuesto)` para cada eje que
    cambiaria respecto de la vista publicada. Solo compara filas que YA
    existen: una corrida nueva no tiene evidencia que perder."""
    if not VISTA_CORRIDAS.exists():
        return []
    publicado = {f["corrida_id"]: f for f in _leer_tsv_derivado(VISTA_CORRIDAS)}
    cambios = []
    for fila in filas_corridas:
        anterior = publicado.get(fila["corrida_id"])
        if anterior is None:
            continue
        for campo in ("resultado_replay", "contexto_replay"):
            if anterior.get(campo) != fila[campo]:
                cambios.append((fila["corrida_id"], campo,
                                anterior.get(campo), fila[campo]))
    return cambios


def _para_si_pisa_replay(filas_corridas: list[dict], lote: set) -> None:
    """PARA antes de escribir. `lote` se compara contra el `spec_id` de la
    fila (el `CALC-*`) y tambien contra el `corrida_id` completo, para que
    autorizar un lote no exija copiar el sufijo de hash."""
    por_id = {f["corrida_id"]: f for f in filas_corridas}
    ajenas = []
    for corrida_id, campo, antes, ahora in _transiciones_replay(filas_corridas):
        spec_id = (por_id.get(corrida_id) or {}).get("spec_id", "")
        if corrida_id in lote or spec_id in lote:
            continue
        ajenas.append((corrida_id, campo, antes, ahora))
    if not ajenas:
        return
    ids = sorted({a[0] for a in ajenas})
    detalle = "\n".join(
        f"    {cid} · {campo}: {antes} -> {ahora}"
        for cid, campo, antes, ahora in sorted(ajenas))
    raise ReplayPisado(
        f"REPLAY-PISADO (NC-0094): escribir borraria o cambiaria evidencia de "
        f"replay de {len(ids)} corrida(s) AJENA(s) al lote autorizado "
        f"({len(ajenas)} campo(s)). No se escribio ninguna vista.\n"
        f"{detalle}\n"
        f"  Si el cambio es intencional, nombra las corridas en "
        f"`--lote {','.join(ids)}` y di por que en la nota de cierre del "
        f"lote. No existe `--force`: un veredicto ajeno no se mueve sin "
        f"razon explicita.")


def registro(escribe: bool = False, verifica: bool = False,
             imprime: bool = True, lote=None, fuentes: bool = False) -> dict:
    """FP-359: la fotocopiadora se desarma -- `escribe` por defecto es
    `False`. Escribir las tres vistas en disco exige el `True` explicito
    (`--escribe` en la CLI); sin el, esta funcion deriva, valida y --si
    `imprime`-- muestra el diff que escribiria, pero no toca ningun TSV.
    Antes, `registro()` escribia por defecto y el UNICO procedimiento
    documentado para "simular sin escribir" (`ADR-410`) escribia de todos
    modos como efecto colateral (`FP-359`) -- publico una firma que mesa
    nunca dio."""
    vistas = _filas_registro(verifica)
    if fuentes and imprime:
        _imprime_fuentes_replay(vistas["fuentes_replay"])
    if escribe:
        # P1 (NC-0094): el diff de los dos ejes se calcula ANTES de tocar
        # el primer TSV. Si pisa evidencia ajena, esto levanta y no se
        # escribe nada -- ni la primera de las tres vistas.
        _para_si_pisa_replay(vistas["corridas"], _lote_autorizado(lote))
        _escribe(VISTA_CORRIDAS, COLS_VISTA_CORRIDAS, vistas["corridas"])
        _escribe(VISTA_RESULTADOS, COLS_VISTA_RESULTADOS, vistas["resultados"])
        _escribe(VISTA_USOS, COLS_VISTA_USOS, vistas["usos"])
        if imprime:
            for ruta, clave in ((VISTA_CORRIDAS, "corridas"),
                                (VISTA_RESULTADOS, "resultados"),
                                (VISTA_USOS, "usos")):
                print(f"ESCRITO {_rel(ruta)}: {len(vistas[clave])} filas")
    elif imprime:
        for ruta, cols, clave in ((VISTA_CORRIDAS, COLS_VISTA_CORRIDAS, "corridas"),
                                  (VISTA_RESULTADOS, COLS_VISTA_RESULTADOS, "resultados"),
                                  (VISTA_USOS, COLS_VISTA_USOS, "usos")):
            _imprime_diff_vista(ruta, cols, vistas[clave])
    if imprime:
        for a in sorted(set(vistas["avisos"])):
            print(f"AVISO · {a}", file=sys.stderr)
        print(f"AVISOS: {len(set(vistas['avisos']))}", file=sys.stderr)
    return vistas


def _imprime_fuentes_replay(fuentes: dict) -> None:
    """P2: de donde sale CADA veredicto proyectado. Es la cita que el
    encargo pide -- el registro no se limita a mostrar el veredicto, dice
    quien lo sostiene, con que fecha y con que alcance."""
    print(f"FUENTES DE REPLAY  ({_rel(REPLAY_EVIDENCIA)})")
    for calc_id in sorted(fuentes):
        f = fuentes[calc_id]
        asiento = f.get("asiento") or {}
        linea = f"  {calc_id}: {f['clase']}"
        if asiento:
            linea += (f" · {asiento['resultado_replay']}/"
                      f"{asiento['contexto_replay']}"
                      f" · fecha={asiento.get('fecha_verificacion') or 'DESCONOCIDA'}"
                      f" · entorno={asiento.get('entorno') or 'NO-DECLARADO'}"
                      f" · alcance={asiento.get('alcance') or 'NO-DECLARADO'}")
            if asiento.get("nota"):
                linea += f" · nota={asiento['nota']}"
        if f.get("limitacion_sesion"):
            linea += f" · limitacion de ESTA sesion: {f['limitacion_sesion']}"
        if f.get("razon"):
            linea += f" · {f['razon']}"
        print(linea)


def cmd_registro(args) -> int:
    try:
        registro(escribe=getattr(args, "escribe", False),
                 verifica=getattr(args, "verifica", False),
                 lote=getattr(args, "lote", None),
                 fuentes=getattr(args, "fuentes", False))
    except ParoRegistro as exc:
        print(f"PARO · {exc}", file=sys.stderr)
        print("no se escribio ninguna vista", file=sys.stderr)
        return 1
    return 0


def _no_corrido_abiertas() -> int:
    """`no_corrido_abiertas` (A.14): filas ABIERTA de `forense/no-corrido.tsv`."""
    if not NO_CORRIDO_TSV.exists():
        return 0
    return sum(1 for f in _leer_tsv(NO_CORRIDO_TSV)
               if (f.get("estado") or "").strip() == "ABIERTA")


def status(imprime: bool = True) -> dict:
    """§9 del plan v2.0. TODO derivado de las vistas en memoria: ningun
    numero se teclea aqui y ninguno se lee de un TSV que quiza no se
    re-derivo. Un replay GEN1 nunca incrementa `N_resultados_sellados`."""
    v = _filas_registro(verifica=False)
    corridas, resultados, usos = v["corridas"], v["resultados"], v["usos"]

    def gen2(filas):
        return [f for f in filas if f["cuenta_gen2"] == "SI"]

    sellada = lambda f: str(f["estado"]).startswith(("SELLADA", "SUPERADO"))
    activos = [f for f in resultados if f["origen"] == "DEMANDA"]
    usos_activos = [u for u in usos if u["activo"] == "SI"]

    # ACTO GEN2-PRE-E5 · P3: separar MEDICION de ADOPCION. Medir (sellar un
    # RESULT) y adoptar (que un consumidor activo lo lea) son eventos
    # distintos que hoy pueden separarse por actos enteros -- E5 sella,
    # mesa adopta despues. `dependencias_numericas_legacy_activas` sigue
    # midiendo SOLO lo que el consumidor activo lee de verdad: sellar un
    # RESULT no la mueve un bit por si solo.
    #   SELLADO: RESULT de una corrida con cuenta_gen2=SI y sello valido.
    #   PENDIENTE_ADOPCION: SELLADO citado en la propuesta PENDIENTE-DE-
    #     MESA, pero todavia no por un consumidor activo GEN2.
    #   ADOPTADO_ACTIVO: SELLADO citado por un consumidor activo con
    #     corrida0_generacion=GEN2 Y corrida0_resultado_id=<ese RESULT>.
    sellados_gen2 = [f for f in resultados if f["origen"] == "OFERTA"
                     and f["cuenta_gen2"] == "SI" and sellada(f)]
    ids_sellados_gen2 = {f["resultado_id"] for f in sellados_gen2}
    ids_adoptados = {u["corrida0_resultado_id"] for u in usos_activos
                     if u["generacion_leida"] == "GEN2" and u["corrida0_resultado_id"]}
    ids_adoptados &= ids_sellados_gen2
    ids_pendientes = _resultados_citados_en(PROPUESTA) & ids_sellados_gen2
    ids_pendientes -= ids_adoptados

    c = {
        "N_corridas_requeridas": sum(1 for f in corridas if f["origen"] == "DEMANDA"),
        "N_corridas_selladas": sum(1 for f in gen2(corridas)
                                   if f["origen"] == "OFERTA" and sellada(f)),
        "N_resultados_activos": len(activos),
        "N_resultados_sellados": sum(1 for f in gen2(resultados)
                                     if f["origen"] == "OFERTA" and sellada(f)),
        "N_resultados_pendientes": sum(1 for f in activos if f["estado"] == "PENDIENTE"),
        "dependencias_numericas_legacy_activas": sum(
            1 for u in usos_activos if u["generacion_leida"] == GENERACION_LEGADO),
        "N_resultados_gen2_sellados": len(ids_sellados_gen2),
        "N_resultados_gen2_pendientes_adopcion": len(ids_pendientes),
        "N_resultados_gen2_adoptados_activos": len(ids_adoptados),
        "resultados_con_validacion_independiente": sum(
            1 for f in resultados if f["validacion_independiente"] == "PASA"),
        # `delta` (B-7) es de E7: sin criterio de materialidad firmado y sin
        # `valor_gen2` que comparar, el conteo derivado es 0 -- y su razon
        # se declara, no se calla.
        "diferencias_materiales": sum(
            1 for f in resultados
            if f["delta_legacy"] not in (NO_COMPARABLE, "PENDIENTE", "")),
        "no_corrido_abiertas": _no_corrido_abiertas(),
        # Fuera del nucleo §9: los replays LEGACY-GEN1 que sostienen el
        # aparato pero NO cuentan como medicion GEN2.
        "replays_legacy_sellados": sum(1 for f in corridas
                                       if f["origen"] == "OFERTA"
                                       and f["cuenta_gen2"] == "NO"
                                       and f["envuelto_legacy"] != "SI"
                                       and sellada(f)),
        # ACTO GEN2-T9 · P1 · D-1: los corredores ENVUELTOS -- spec GEN2,
        # sello valido, `verify REPRODUCE`, y aun asi cero GEN2 porque su
        # insumo es el aparato GEN1 (regla E.1). Se cuentan APARTE y nunca
        # entran a `N_corridas_selladas`: es el contador que evita repetir
        # sobre los corredores el error que ya se pago en 600 PR.
        "corredores_envueltos_legacy": sum(
            1 for f in corridas
            if f["origen"] == "OFERTA" and f["envuelto_legacy"] == "SI"),
    }
    if imprime:
        for clave, valor in c.items():
            print(f"{clave}={valor}")
        print(f"# derivado de {len(corridas)} corridas · {len(resultados)} "
              f"resultados · {len(usos)} usos", file=sys.stderr)
    return c


def cmd_status(args) -> int:
    try:
        c = status(imprime=not getattr(args, "json", False))
    except ParoRegistro as exc:
        print(f"PARO · {exc}", file=sys.stderr)
        return 1
    if getattr(args, "json", False):
        print(json.dumps(c, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


# ── subcomandos que siguen declarados y vacios (los llena GEN2-E7) ─────────

PENDIENTES_E3 = [
    ("vigencia", "B-6 · CANDIDATO-VENCIDO por fecha e instrumento"),
    ("delta", "B-7 · valor_legacy vs valor_gen2 y su materialidad"),
]


def _no_implementado(nombre):
    def _cmd(args):
        print(f"NO-IMPLEMENTADO: `corrida0 {nombre}` se declara aqui y lo "
              f"llena ACTO GEN2-E3 (PLAN-FINAL-GEN2 v2.0 §4, B-1).",
              file=sys.stderr)
        return 2
    return _cmd


def construye_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="corrida0", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subs = p.add_subparsers(dest="subcomando", required=True)
    d = subs.add_parser("demanda", help="C0-A: deriva que hay que volver a medir")
    d.set_defaults(func=cmd_demanda)

    # GEN2-E3 · AUTOMATIZA-GEN2-1: el nucleo de corrida deja de ser un hueco.
    sc = subs.add_parser("spec-check",
                         help="B-2 · cada (archivo, variable) contra los inventarios vigentes")
    sc.add_argument("calc_id", help="p. ej. CALC-SMOKE-0001")
    sc.set_defaults(func=cmd_spec_check)

    ng = subs.add_parser("negativo",
                         help="B-3 · barrido declarativo de NO-ENCONTRADO / SIN-COBERTURA")
    ng.add_argument("--patron", required=True, help="regex sobre variable_id + texto_reactivo")
    ng.add_argument("--archivos", default=None,
                    help="regex sobre archivo_miembro; sin el, todo el universo vigente")
    ng.set_defaults(func=cmd_negativo)

    for nombre, ayuda, fn in (
            ("preflight", "B-1 · comprobacion previa a ejecutar una corrida", cmd_preflight),
            ("run", "B-1 · ejecucion sellada de una corrida", cmd_run),
            ("verify", "B-1 · reejecucion con tolerancia declarada", cmd_verify)):
        s = subs.add_parser(nombre, help=ayuda)
        s.add_argument("calc_id", help="p. ej. CALC-SMOKE-0001")
        s.set_defaults(func=fn)
    # GEN2-E6 · AUTOMATIZA-GEN2-2: las tres vistas y los contadores.
    rg = subs.add_parser("registro",
                         help="B-1 · une demanda y oferta -> corridas/resultados/usos.tsv")
    rg.add_argument("--verifica", action="store_true",
                    help="ademas corre `verify` por CALC sellado para llenar "
                         "resultado_replay/contexto_replay (reejecuta el medidor)")
    rg.add_argument("--escribe", action="store_true",
                    help="FP-359: sin esta bandera, `registro` deriva, valida "
                         "e imprime el diff que escribiria SIN tocar ningun "
                         "TSV -- con ella, escribe las tres vistas de verdad")
    # ACTO GEN2-REGISTRO-REPLAY (NC-0094).
    rg.add_argument("--lote", action="append", metavar="CALC-A,CALC-B",
                    help="corridas cuyo veredicto de replay SI puede cambiar "
                         "en esta escritura (la 'razon explicita'). Sin ella, "
                         "ninguna transicion de resultado_replay/contexto_replay "
                         "sobre una corrida ya publicada pasa: `--escribe` PARA "
                         "y lista los ids. No existe `--force`")
    rg.add_argument("--fuentes", action="store_true",
                    help="imprime de donde sale cada veredicto de replay "
                         "proyectado (asiento, fecha, entorno, alcance, nota) "
                         "y la limitacion de esta sesion, aparte de la columna")
    rg.set_defaults(func=cmd_registro)

    st = subs.add_parser("status", help="B-11 · contadores GEN2, todos derivados")
    st.add_argument("--json", action="store_true", help="mismo contenido, JSON")
    st.set_defaults(func=cmd_status)

    # ACTO GEN2-PRE-E5 · CABLEADO-Y-AUTOMATIZACION-FINAL, P1: estado unico
    # de un CALC, derivado de artefactos (cierra NC-0010).
    es = subs.add_parser("estado", help="P1 · estado derivado unico de un CALC")
    es.add_argument("calc_id", help="p. ej. CALC-0001")
    es.add_argument("--preflight", action="store_true",
                    help="si la spec esta fijada sin ejecutar, corre preflight "
                         "para distinguir PRE-FLIGHT-VERDE de SPEC-FIJADA")
    es.add_argument("--json", action="store_true", help="mismo contenido, JSON")
    es.set_defaults(func=cmd_estado)

    for nombre, ayuda in PENDIENTES_E3:
        s = subs.add_parser(nombre, help=f"[NO-IMPLEMENTADO] {ayuda}")
        s.set_defaults(func=_no_implementado(nombre))
    return p


def main(argv=None) -> int:
    args = construye_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
