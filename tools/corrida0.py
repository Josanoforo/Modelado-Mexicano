#!/usr/bin/env python3
"""`corrida0` -- CLI del registro GEN2 (PLAN-FINAL-GEN2 v2.0, B-1).

Este archivo nace en `ACTO GEN2-E2 · C0-A DEMANDA` con **un solo subcomando
implementado**, `demanda`. Los demas subcomandos del plan (§4, fila B-1) se
declaran aqui vacios, con su nombre y su fase, para que E3 los llene sin
tener que re-decidir la estructura -- no para que nadie los invoque hoy:
invocarlos sale con codigo 2 y el rotulo NO-IMPLEMENTADO.

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
import json
import re
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
    if ambiguas:
        print("\nAGRUPACIONES / RESOLUCIONES QUE EL REGISTRO NO DECIDE "
              f"({len(ambiguas)}) -- se listan, no se deciden:", file=sys.stderr)
        for linea in ambiguas:
            print("  - " + linea, file=sys.stderr)
    return 0


# ── subcomandos declarados y aun vacios (los llena GEN2-E3) ────────────────

PENDIENTES_E3 = [
    ("spec-check", "B-2 · cada (archivo, variable) contra el inventario canonico"),
    ("negativo", "B-3 · barrido declarativo de NO-ENCONTRADO / SIN-COBERTURA"),
    ("preflight", "B-1 · comprobacion previa a ejecutar una corrida"),
    ("run", "B-1 · ejecucion sellada de una corrida"),
    ("verify", "B-1 · reejecucion con tolerancia declarada"),
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
    for nombre, ayuda in PENDIENTES_E3:
        s = subs.add_parser(nombre, help=f"[NO-IMPLEMENTADO] {ayuda}")
        s.set_defaults(func=_no_implementado(nombre))
    return p


def main(argv=None) -> int:
    args = construye_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
