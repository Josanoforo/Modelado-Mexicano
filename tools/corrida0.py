#!/usr/bin/env python3
"""`corrida0` -- CLI del registro GEN2 (PLAN-FINAL-GEN2 v2.0, B-1).

Este archivo nacio en `ACTO GEN2-E2 · C0-A DEMANDA` con un solo subcomando
implementado, `demanda`, y los demas declarados vacios.

`ACTO GEN2-E3 · AUTOMATIZA-GEN2-1` (7/sep/2026) llena SEIS de esos huecos y
deja cuatro:

  IMPLEMENTADOS  demanda (E2) · spec-check · negativo · preflight · run · verify
  DECLARADOS Y VACIOS  registro · status · vigencia · delta  (los llena E6;
                       invocarlos sale con codigo 2 y el rotulo NO-IMPLEMENTADO)

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

RAIZ = Path(__file__).resolve().parents[1]
TRAMITE = RAIZ / "milpa" / "tramite.yaml"
PROCEDENCIA = RAIZ / "milpa" / "procedencia.yaml"
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
    "conducta_p_medido": 1,
    "coeficiente_ejecutable": 2,
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
    if fila["tipo"].startswith("celda_"):
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
        print(f"decisiones_aplicadas (FP-339) = {len(decisiones)}")
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

def _verifica_inputs(spec: dict, bloqueos: list[str]) -> list[dict]:
    """Dos origenes, dos mecanismos, sin colapsar uno en el otro.

      `origen: repo`        insumo VERSIONADO -- se rehashea el archivo del
                            arbol y se compara con el sha declarado.
      `origen: manifiesto`  payload del corpus -- lo resuelve
                            `resolver_payload` (P1, `tests/payload_
                            resolver.py`), UNA vez por id, import directo
                            (nunca subproceso). `preflight` queda VERDE solo
                            si CADA input activo resuelve en `COINCIDE`; el
                            objeto devuelto (`ruta_absoluta`, `sha256_actual`,
                            `raiz_logica`) es el mismo que `run` reusa para
                            alimentar al medidor y rellenar
                            `ejecucion.json.input_sha256`.
    """
    inputs = spec.get("inputs") or []
    fuera = []
    for ent in inputs:
        iid = str(ent.get("id", ""))
        origen = ent.get("origen", "manifiesto")
        if origen == "repo":
            ruta = RAIZ / str(ent.get("ruta", ""))
            real = _sha256_archivo(ruta)
            declarado = str(ent.get("sha256", ""))
            if real is None:
                bloqueos.append(f"input_repo_ausente={iid}:{ent.get('ruta')}")
                estado = "AUSENTE"
            elif declarado and real != declarado:
                bloqueos.append(f"input_repo_sha_discorda={iid}")
                estado = "DISCORDA"
            elif not declarado:
                bloqueos.append(f"input_repo_sin_sha_declarado={iid}")
                estado = "SIN-SHA-DECLARADO"
            else:
                estado = "COINCIDE"
            # Un insumo versionado que no esta commiteado no es versionado.
            cod, _ = _git_salida("ls-files", "--error-unmatch", str(ent.get("ruta", "")))
            if cod != 0:
                bloqueos.append(f"input_repo_no_commiteado={iid}")
                estado += "+NO-COMMITEADO"
            print(f"    [{estado}] {iid}  origen=repo  ruta={ent.get('ruta')}")
            print(f"              sha256 real     = {real}")
            print(f"              sha256 declarado= {declarado or '(ninguno)'}")
            fuera.append({"id": iid, "origen": "repo", "ruta": str(ent.get("ruta")),
                          "ruta_absoluta": str(ruta), "raiz_logica": None,
                          "sha256": real, "sha256_declarado": declarado,
                          "estado": estado})
        else:
            r = _PR.resolver_payload(iid)
            estado = r["estado"]
            if estado != "COINCIDE":
                bloqueos.append(f"input_manifiesto_{estado}={iid}")
            print(f"    [{estado}] {iid}  origen=manifiesto  raiz={r['raiz_logica']}")
            print(f"              ruta_absoluta   = {r['ruta_absoluta']}")
            print(f"              sha256 esperado = {r['sha256_esperado']}")
            print(f"              sha256 actual   = {r['sha256_actual']}")
            print(f"              tamano          = {r['tamano']}")
            fuera.append({"id": iid, "origen": "manifiesto", "estado": estado,
                          "ruta_absoluta": r["ruta_absoluta"],
                          "raiz_logica": r["raiz_logica"],
                          "sha256": r["sha256_actual"] or r["sha256_esperado"]})
    return fuera


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

    # 5 · inputs
    if imprime:
        print(f"  inputs declarados: {len(spec.get('inputs') or [])}")
    detalle_inputs = _verifica_inputs(spec, bloqueos)

    # 6 · parametros, tolerancia y seed declarados
    tol = spec.get("tolerancia") or {}
    if not isinstance(tol, dict) or not tol.get("tipo"):
        bloqueos.append("tolerancia_sin_tipo")
    seed = spec.get("seed")
    if "seed" not in spec or seed is None:
        bloqueos.append("seed_no_declarado")
    elif isinstance(seed, dict):
        # P2: `{aplica: false}` es una declaracion valida -- no se inventan
        # semillas para calculos deterministas. Solo se bloquea la forma
        # invalida (dict sin `aplica`, o `aplica: true` sin `valor`).
        if "aplica" not in seed:
            bloqueos.append("seed_dict_sin_aplica")
        elif seed.get("aplica") is True and "valor" not in seed:
            bloqueos.append("seed_aplica_sin_valor")
    if imprime:
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
            "inputs": detalle_inputs, "spec_md_estado": estado_md,
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


def _inputs_para_medidor(spec: dict) -> dict:
    """P1: el MISMO objeto que resolvio el payload alimenta al medidor --
    ningun medidor busca su propio archivo por su cuenta. `origen: repo`
    resuelve `ruta_absoluta` contra el arbol; `origen: manifiesto` la resuelve
    `resolver_payload` (una vez por id, import directo, nunca subproceso)."""
    fuera = {}
    for ent in spec.get("inputs") or []:
        iid = str(ent.get("id", ""))
        d = dict(ent)
        if ent.get("origen") == "repo":
            d["ruta_absoluta"] = str(RAIZ / str(ent.get("ruta", "")))
        else:
            r = _PR.resolver_payload(iid)
            d["ruta_absoluta"] = r["ruta_absoluta"]
            d["sha256"] = r["sha256_actual"]
            d["raiz_logica"] = r["raiz_logica"]
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
    sustantiva que la spec no declara llega como `"NO-APLICA"` -- la spec la
    declara explicita, este contrato solo la copia, nunca la inventa."""
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


def _ejecuta(spec: dict) -> tuple[dict, int, str]:
    script = RAIZ / str(spec.get("script", ""))
    try:
        medir = _carga_medidor(script)
        valores = medir(_inputs_para_medidor(spec), contrato_ejecutable(spec))
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
        "input_sha256": {e["id"]: e.get("sha256") for e in pre["inputs"]},
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
    valores, exit_code, error = _ejecuta(spec)

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
    return {"veredicto": "EJECUTADO" if exit_code == 0 else "FALLO",
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


def _evalua_contexto(d: Path, spec: dict, ejec: dict, imprime: bool = False) -> tuple[str, list[str]]:
    """P5 (2)+(3)+(4): `spec_yaml_sha256` · inputs de manifiesto re-resueltos
    con `resolver_payload` (P1) · `script_blob_sha256`, commit, parametros,
    seed, dependencias -> `CONTEXTO ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE}`
    con sus razones. `NO-VERIFICABLE` cuando algo no se puede ni siquiera
    comprobar (un input fuera de perimetro/raiz no configurada, o `git`
    mismo fallando) -- nunca se degrada a `DISTINTO`, que afirmaria un
    cambio que en realidad no se pudo confirmar ni descartar."""
    sha_yaml_hoy = _sha256_archivo(d / "spec.yaml")
    yaml_igual = sha_yaml_hoy == ejec.get("spec_yaml_sha256")
    if imprime:
        print(f"  [2/5 SPEC.YAML] {'IDENTICO' if yaml_igual else 'CAMBIADO'}"
              f"  sellado={ejec.get('spec_yaml_sha256')}  hoy={sha_yaml_hoy}")
    razones_contexto = [] if yaml_igual else ["spec_yaml_cambiado"]

    no_verificable_inputs = False
    for ent in spec.get("inputs") or []:
        iid = str(ent.get("id", ""))
        sellado = (ejec.get("input_sha256") or {}).get(iid)
        if ent.get("origen") == "repo":
            hoy = _sha256_archivo(RAIZ / str(ent.get("ruta", "")))
            ok = hoy is not None and hoy == sellado
            if imprime:
                print(f"  [3/5 INPUT {'COINCIDE' if ok else 'DISCORDA'}] {iid} (repo)"
                      f"  sellado={sellado}  hoy={hoy}")
            if not ok:
                razones_contexto.append(f"input_cambiado={iid}")
        else:
            r = _PR.resolver_payload(iid)
            if imprime:
                print(f"  [3/5 INPUT {r['estado']}] {iid} (manifiesto)"
                      f"  sellado={sellado}  actual={r['sha256_actual']}")
            if r["estado"] in ("RAIZ_NO_CONFIGURADA", "FUERA_DE_PERIMETRO"):
                no_verificable_inputs = True
                razones_contexto.append(f"input_no_verificable={iid}:{r['estado']}")
            elif r["estado"] != "COINCIDE" or r["sha256_actual"] != sellado:
                razones_contexto.append(f"input_cambiado={iid}")

    sha_script_hoy = _sha256_archivo(RAIZ / str(spec.get("script", "")))
    script_igual = sha_script_hoy == ejec.get("script_blob_sha256")
    if not script_igual:
        razones_contexto.append("script_cambiado")
    cod_commit, commit_hoy = _git_salida("rev-parse", "HEAD")
    commit_hoy = commit_hoy.strip()
    commit_no_verificable = cod_commit != 0
    if commit_no_verificable:
        razones_contexto.append("commit_no_verificable")
    elif commit_hoy != ejec.get("git_commit"):
        razones_contexto.append("commit_distinto")
    if spec.get("parametros") != ejec.get("parametros"):
        razones_contexto.append("parametros_distintos")
    if spec.get("seed") != ejec.get("seed"):
        razones_contexto.append("seed_distinto")
    deps_hoy = _dependencias_materiales_calc(spec)
    if deps_hoy != ejec.get("dependencias_materiales_calc"):
        razones_contexto.append("dependencias_distintas")
    if imprime:
        print(f"  [4/5 CONTEXTO] codigo={'IDENTICO' if script_igual else 'CAMBIADO'}"
              f"  commit={'NO-VERIFICABLE' if commit_no_verificable else ('IDENTICO' if commit_hoy == ejec.get('git_commit') else 'DISTINTO')}"
              f"  parametros={'IDENTICO' if spec.get('parametros') == ejec.get('parametros') else 'DISTINTO'}"
              f"  seed={'IDENTICO' if spec.get('seed') == ejec.get('seed') else 'DISTINTO'}"
              f"  dependencias={'IDENTICO' if deps_hoy == ejec.get('dependencias_materiales_calc') else 'DISTINTO'}")

    if no_verificable_inputs or commit_no_verificable:
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

    # (2)+(3)+(4) -> CONTEXTO, con razon.
    contexto, razones_contexto = _evalua_contexto(d, spec, ejec, imprime=imprime)
    if imprime:
        print(f"  CONTEXTO: {contexto}" +
              (f"  razon: {'; '.join(razones_contexto)}" if razones_contexto else ""))

    # (5) reejecuta y compara POR RESULT con la tolerancia del tipo (P3).
    valores, exit_code, error = _ejecuta(spec)
    deltas, faltan = {}, []
    if exit_code != 0:
        resultado = "NO-EJECUTABLE"
        if imprime:
            print(f"  [5/5 RESULT] NO-EJECUTABLE -- la reejecucion fallo: {error}")
    else:
        tol = spec.get("tolerancia") or {}
        faltan = sorted(set(previos) ^ set(valores))
        reproduce = not faltan
        for k in sorted(set(previos) & set(valores)):
            ok, delta = _compara(previos[k], valores[k], tol)
            deltas[k] = delta
            reproduce = reproduce and ok
            if imprime:
                print(f"  [5/5 RESULT {'REPRODUCE' if ok else 'NO-REPRODUCE'}] {k}: "
                      f"sellado={previos[k]!r} · hoy={valores[k]!r} · delta={delta!r}")
        if faltan and imprime:
            print(f"  [5/5 RESULT NO-REPRODUCE] ids que aparecen en una corrida y no "
                  f"en la otra: {faltan}")
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
            "ids_faltantes": faltan, "tolerancia": spec.get("tolerancia") or {}}


def cmd_verify(args) -> int:
    r = verify(args.calc_id)
    v = r["veredicto"]
    if v == "REPRODUCE":
        return 0
    if v in ("NO-VERIFICABLE", "NO-EJECUTABLE"):
        return 2
    return 1



# ── subcomandos que siguen declarados y vacios (los llena GEN2-E5/E6) ──────

PENDIENTES_E3 = [
    ("registro", "B-1 · vistas corridas.tsv / resultados.tsv / usos.tsv"),
    ("status", "B-11 · contadores GEN2 leidos del CLI"),
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
    for nombre, ayuda in PENDIENTES_E3:
        s = subs.add_parser(nombre, help=f"[NO-IMPLEMENTADO] {ayuda}")
        s.set_defaults(func=_no_implementado(nombre))
    return p


def main(argv=None) -> int:
    args = construye_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
