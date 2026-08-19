#!/usr/bin/env python3
"""Deriva el expediente de tareas semánticas de BARRIDO-2 sobre material E2.

Este módulo es la entrada del camino fail-closed de capa 4 (ADR-92(a) inciso 5):
`integrate_barrido2.py` exige un expediente tarea->reporte->ledger->baseline y
aquí es donde ese expediente nace.  No adjudica: no escribe `veredicto_a4`, no
elige objeto lógico y no toca `relaciones.tsv`.

Dos fases, en el orden que impone el §17 del encargo:

* `fuentes`  — resuelve, por reglas declaradas y con evidencia por fila, qué
  payloads observados corresponden a cada fuente canónica.  Producto
  versionable y compacto; la regla que resolvió cada fila queda escrita.
* `paquetes` — proyecta el índice E2 privado completo en fragmentos por payload
  y arma el paquete de lectura de cada curador.  Todo bajo `.barrido2/private/`,
  nunca versionado: el curador lee el índice completo, no el recorte de 160.

La fase que convierte la elección del curador en `tareas-barrido2.tsv` vive en
`tareas`, y sólo acepta lo que puede volver a verificar por hash.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from .semantic_run import normalized
except ImportError:  # ejecución directa
    from semantic_run import normalized


SCHEMA_VERSION = "BARRIDO2-TAREAS-1.0"

# Cabecera del expediente que `integrate_barrido2.preflight` vuelve a validar.
# `tarea_id` identifica la tarea semántica; `material_tarea_id` nombra el
# descriptor de inspección material del que hereda su hash.  Separarlos es lo
# que permite que dos relaciones se apoyen en la misma representación sin
# colisionar, cosa que el universo real exige: ENVIPE sola tiene 76.
TASK_FIELDS = [
    "tarea_id", "relacion_id", "reporte_id", "reporte_record_id",
    "reporte_record_sha256", "e2_record_id", "e2_record_sha256",
    "payload_id", "representacion_id", "sha256", "objeto_logico_id",
    "necesidad_id", "reactivo_id", "fuente_canonica", "frontera_semantica",
    "material_tarea_id", "material_task_sha256", "material_baseline_sha256",
    "curador_id", "fecha",
]

# Dos tablas, no una. Los productos durables de este acto —ledger y reportes—
# no tienen una sola celda por encima de 160 caracteres, y la cobertura de
# fuentes no va a ser la excepción: el resumen por fuente lleva conteos y el
# hash de cada lista, y las listas viven desnormalizadas en la tabla de
# detalle, una fila por elemento. Todo versionado, ninguna celda larga.
COVERAGE_FIELDS = [
    "fuente_canonica", "regla_resolucion", "payloads_n", "payloads_sha256",
    "representaciones", "objetos_e2", "evidencia_resolucion", "relaciones_n",
    "relaciones_sha256", "estado_cobertura",
]

DETAIL_FIELDS = ["fuente_canonica", "tipo", "valor"]

LIMITE_DURABLE = 160

# Reglas de resolución, en orden de precedencia.  Cada una deja su nombre en la
# fila; ninguna adivina: la que no puede demostrar el enganche no lo declara.
REGLA_LEDGER = "R1-ID-MANIFIESTO-EN-LEDGER"
REGLA_ALIAS = "R2-ALIAS-FUENTE-CURADO"
REGLA_MANIFIESTO = "R3-TOKEN-CONTRA-ID-MANIFIESTO"
REGLA_RUTA = "R4-TOKEN-CONTRA-PAYLOAD-O-RUTA"
# Las cuatro reglas anteriores son léxicas sobre el id y la ruta, y por eso se
# les escapa el material cuyo nombre de archivo no dice de dónde viene: GDELT
# vive como `20260813130000_export_csv`. La procedencia real está en otros dos
# campos del manifiesto —`url_origen` y `usado_para`—, porque el manifiesto NO
# tiene campo `fuente`. Estas cuatro reglas leen esos campos.
REGLA_USADO_PARA = "R5-CADENA-CANONICA-EN-USADO-PARA"
REGLA_SLUG = "R7-SLUG-DE-PROGRAMA-INEGI"
REGLA_CARPETA = "R8-PREFIJO-DE-CARPETA-EN-ARCHIVO"
REGLA_NINGUNA = "R0-SIN-CANDIDATO-MATERIAL"
REGLA_APERTURA = "R10-PAYLOAD-DECLARADO-EN-LISTA-APERTURA"

TOKEN_MINIMO = 4


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    """Escribe TSV plano.  No usa csv.writer: este repositorio guarda tabuladores
    sin comillas y el escritor estándar reescribe celdas que contienen `"`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(fields)]
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            if "\t" in value or "\n" in value or "\r" in value:
                raise ValueError(f"celda con separador crudo en {field}: {value[:60]!r}")
            cells.append(value)
        lines.append("\t".join(cells))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _lista_sha256(values: list[str]) -> str:
    """Hash estable de una lista de identificadores, para que el resumen por
    fuente sea verificable contra la tabla de detalle sin cargarla entera."""
    if not values:
        return "NO-APLICA"
    payload = "\x1f".join(values).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _durable(value: str) -> str:
    text = " ".join((value or "").split()) or "NO-APLICA"
    return text if len(text) <= LIMITE_DURABLE else text[: LIMITE_DURABLE - 1] + "…"


def manifest_ids(path: Path) -> list[str]:
    """Lee sólo los `id:` del manifiesto.  No necesita yaml ni el payload."""
    return re.findall(r"^- id:\s*(\S+)\s*$", path.read_text(encoding="utf-8"), re.M)


_CAMPO_RE = re.compile(r"^\s{2}([a-z_]+):\s*(.*)$")


def manifest_records(path: Path) -> dict[str, dict[str, str]]:
    """Lee el manifiesto como registros planos, sin yaml.

    Sólo se necesitan cuatro campos y todos son de una línea. Evitar yaml aquí
    mantiene esta vía barata y sin dependencia, igual que `manifest_ids`.
    """
    registros: dict[str, dict[str, str]] = {}
    actual: dict[str, str] | None = None
    for linea in path.read_text(encoding="utf-8").split("\n"):
        inicio = re.match(r"^- id:\s*(\S+)\s*$", linea)
        if inicio:
            actual = {"id": inicio.group(1)}
            registros[inicio.group(1)] = actual
            continue
        if actual is None:
            continue
        campo = _CAMPO_RE.match(linea)
        if campo and campo.group(1) in {"archivo", "url_origen", "url_origen_procedencia", "usado_para", "nota", "raiz"}:
            actual[campo.group(1)] = campo.group(2).strip().strip('"\'')
    return registros


def _host(url: str) -> str:
    match = re.match(r"https?://([^/]+)", (url or "").strip())
    return match.group(1).casefold() if match else ""


def mapa_host_fuente(repo: Path) -> dict[str, str]:
    """Deriva host -> fuente canónica desde los mapas externos ya versionados.

    NO se usa como regla de resolución, y la razón está medida: de los 15 hosts
    que los mapas mapean, sólo 5 apuntan a un nombre que exista en el registro;
    el manifiesto usa `data.gdeltproject.org` donde el mapa dice
    `www.gdeltproject.org`; los nombres del mapa son descriptivos
    (`GDELT_2_0_EVENT_DATABASE`) y no canónicos (`GDELT`); y un host como
    `www.banxico.org.mx` sirve a 17 entradas de varias fuentes distintas, de modo
    que host -> fuente no es una función. Se conserva porque es el insumo que un
    curador necesita para decidir esos casos a mano, que es donde el §17 los
    pone.
    """
    reclamos: dict[str, set[str]] = defaultdict(set)
    for relativa in ("data/mapa-ext-general-2026-08-06.tsv", "data/mapa-ext-academico-2026-08-06.tsv"):
        ruta = repo / relativa
        if not ruta.is_file():
            continue
        for fila in read_tsv(ruta):
            nombre = fila.get("nombre_fuente") or fila.get("fuente") or fila.get("nombre") or ""
            url = fila.get("URL_primaria") or fila.get("url_primaria") or ""
            host = _host(url)
            if host and nombre:
                reclamos[host].add(normalized(nombre))
    return {host: next(iter(nombres)) for host, nombres in reclamos.items() if len(nombres) == 1}


def _split_ids(value: str) -> list[str]:
    parts = (value or "").replace(";", ",").split(",")
    return [p.strip() for p in parts if p.strip() and p.strip() not in {"NO-APLICA", "NO_DETERMINADO", ""}]


def resolve_sources(
    relations: list[dict[str, str]],
    ledger: list[dict[str, str]],
    aliases: list[dict[str, str]],
    manifest_path: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Resuelve fuente canónica -> payloads observados, con regla y evidencia.

    Devuelve el resumen por fuente y su detalle desnormalizado.
    """
    by_payload: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ledger:
        if row["payload_id"] not in {"", "NO-APLICA"}:
            by_payload[row["payload_id"]].append(row)
    payload_norm = {pid: normalized(pid) for pid in by_payload}
    route_norm = {row["representacion_id"]: normalized(row["ruta_relativa"]) for row in ledger}
    rep_by_payload = {pid: [r["representacion_id"] for r in rows] for pid, rows in by_payload.items()}
    manifest = manifest_ids(manifest_path)
    manifest_norm = {mid: normalized(mid) for mid in manifest}
    alias_payload: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for row in aliases:
        parts = row.get("base_identidad", "").split("|")
        if len(parts) >= 2 and parts[1] in by_payload:
            alias_payload[row["fuente_canonica_normalizada"]].append((parts[1], row["alias_fuente"]))

    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in relations:
        by_source[row["fuente_canonica_normalizada"]].append(row)

    registros = manifest_records(manifest_path)
    # Índices inversos fuente -> payloads observados, uno por regla no léxica.
    por_usado_para: dict[str, set[str]] = defaultdict(set)
    por_slug: dict[str, set[str]] = defaultdict(set)
    por_carpeta: dict[str, set[str]] = defaultdict(set)
    fuentes_norm = {normalized(s): s for s in by_source}
    for mid, registro in registros.items():
        if mid not in by_payload:
            continue
        texto = normalized(" ".join(
            registro.get(campo, "") for campo in ("usado_para", "nota")
        ))
        for clave in fuentes_norm:
            if len(clave) >= 8 and clave in texto:
                por_usado_para[clave].add(mid)
        url = registro.get("url_origen", "") or registro.get("url_origen_procedencia", "")
        slug = re.search(r"inegi\.org\.mx/(?:contenidos/)?programas/([a-z0-9_]+)", url or "", re.I)
        if slug:
            por_slug[normalized(slug.group(1))].add(mid)
        carpeta = (registro.get("archivo", "") or "").split("/")[0]
        if carpeta and carpeta != registro.get("archivo", ""):
            por_carpeta[normalized(carpeta)].add(mid)

    out: list[dict[str, str]] = []
    detalle: list[dict[str, str]] = []
    for source in sorted(by_source):
        rows = by_source[source]
        declared = sorted({i for row in rows for i in _split_ids(row.get("id_manifiesto", ""))})
        token = normalized(source)
        payloads: list[str] = []
        rule = REGLA_NINGUNA
        evidence = "NO-APLICA"

        hit = [i for i in declared if i in by_payload]
        if hit:
            payloads, rule = sorted(hit), REGLA_LEDGER
            evidence = "ledger:payload_id=" + ";".join(payloads[:4])
        elif source in alias_payload:
            payloads = sorted({p for p, _ in alias_payload[source]})
            rule = REGLA_ALIAS
            evidence = "aliases-fuentes.tsv:" + ";".join(sorted({a for _, a in alias_payload[source]}))
        elif len(token) >= TOKEN_MINIMO:
            manifest_hit = sorted(
                mid for mid, norm in manifest_norm.items()
                if mid in by_payload and (norm == token or norm.startswith(token + "_") or re.match(rf"^{re.escape(token)}\d", norm))
            )
            if manifest_hit:
                payloads, rule = manifest_hit, REGLA_MANIFIESTO
                evidence = "manifiesto:id=" + ";".join(manifest_hit[:4])
            else:
                route_hit = sorted({
                    pid for pid, norm in payload_norm.items()
                    if token in norm or any(token in route_norm[rep] for rep in rep_by_payload[pid])
                })
                if route_hit:
                    payloads, rule = route_hit, REGLA_RUTA
                    evidence = "token=" + token + " en payload_id/ruta_relativa"
        if not payloads and len(token) >= 8 and token in por_usado_para:
            payloads, rule = sorted(por_usado_para[token]), REGLA_USADO_PARA
            evidence = "manifiesto:usado_para nombra la fuente canonica literal"
        if not payloads and token in por_slug:
            payloads, rule = sorted(por_slug[token]), REGLA_SLUG
            evidence = "manifiesto:url_origen slug inegi.org.mx/programas/" + token.casefold()
        if not payloads and token in por_carpeta:
            payloads, rule = sorted(por_carpeta[token]), REGLA_CARPETA
            evidence = "manifiesto:archivo carpeta " + token.casefold() + "/"

        # Unión declarada R1 ∪ R7 -- ACTO B2-SEMANTICO, 18/ago/2026.
        #
        # La cascada de arriba es de primer match: para una fuente cuyas
        # relaciones ya declaran un `id_manifiesto` observado, R1 acierta y
        # corta, de modo que R7 (que vive detrás de `if not payloads`) nunca
        # llega a correr.  Medido: ENFIH y ENBIARE se resolvían a UN payload
        # cada una mientras el ledger tiene DOS, porque la segunda entrada de
        # programa (`enfih2019_bd_csv_zip`, `enbiare2021_bd_csv_zip`) no la
        # cita ninguna relación.
        #
        # Esa segunda entrada es justamente la que ADR-93 exige poder evaluar
        # ("la gemela se enlaza SOLO si su objeto es evidenciable con una
        # entrada distinta del manifiesto"), así que sin ella los pares de
        # FP-46 son inadjudicables por evidencia.  La unión es mecánica y no
        # decide semántica: el slug sale de `url_origen` declarado en el
        # manifiesto, cada payload queda listado en el detalle y la regla
        # compuesta queda escrita en `regla_resolucion`.
        extra_slug = sorted(por_slug.get(token, set()) - set(payloads))
        if extra_slug:
            payloads = sorted(set(payloads) | set(extra_slug))
            rule = REGLA_SLUG if rule == REGLA_NINGUNA else f"{rule}+{REGLA_SLUG}"
            evidence = (
                f"{evidence} | union R7 slug programas/{token.casefold()}: "
                + ";".join(extra_slug[:3])
            )

        reps = sorted({rep for pid in payloads for rep in rep_by_payload[pid]})
        relaciones = sorted(r["relacion_id"] for r in rows)
        out.append({
            "fuente_canonica": source,
            "regla_resolucion": rule,
            "payloads_n": str(len(payloads)),
            "payloads_sha256": _lista_sha256(payloads),
            "representaciones": str(len(reps)),
            "objetos_e2": "PENDIENTE-PROYECCION",
            "evidencia_resolucion": _durable(evidence),
            "relaciones_n": str(len(relaciones)),
            "relaciones_sha256": _lista_sha256(relaciones),
            "estado_cobertura": "CON-MATERIAL" if payloads else "SIN-MATERIAL-OBSERVADO",
        })
        detalle.extend({"fuente_canonica": source, "tipo": "PAYLOAD", "valor": p} for p in payloads)
        detalle.extend({"fuente_canonica": source, "tipo": "RELACION", "valor": r} for r in relaciones)
    return out, detalle


def _nombre_fragmento(payload: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", payload)[:180]


def project_index(
    index_path: Path, wanted: set[str], shard_root: Path
) -> tuple[dict[str, int], dict[str, str]]:
    """Recorre el índice E2 una sola vez y lo parte por payload.

    Sólo escribe los payloads pedidos.  El fragmento conserva el registro
    íntegro: el curador no debe leer el recorte durable de 160 caracteres.
    """
    shard_root.mkdir(parents=True, exist_ok=True)
    handles: dict[str, Any] = {}
    counts: Counter[str] = Counter()
    try:
        with index_path.open(encoding="utf-8") as source:
            for line in source:
                start = line.find('"payload_id":')
                if start < 0:
                    continue
                match = re.search(r'"payload_id":\s*"((?:[^"\\]|\\.)*)"', line)
                if not match:
                    continue
                payload = json.loads('"' + match.group(1) + '"')
                if payload not in wanted:
                    continue
                handle = handles.get(payload)
                if handle is None:
                    safe = _nombre_fragmento(payload)
                    handle = handles[payload] = (shard_root / f"{safe}.jsonl").open("w", encoding="utf-8")
                handle.write(line if line.endswith("\n") else line + "\n")
                counts[payload] += 1
    finally:
        for handle in handles.values():
            handle.close()
    hashes = {
        payload: sha256_file(shard_root / f"{_nombre_fragmento(payload)}.jsonl")
        for payload in counts
    }
    return dict(counts), hashes


def _detalle_path(output: Path) -> Path:
    return output.with_name(output.stem + "-detalle" + output.suffix)


def cmd_fuentes(args: argparse.Namespace) -> int:
    registry, universe = args.registry.resolve(), args.universe.resolve()
    output = args.output.resolve()
    coverage, detalle = resolve_sources(
        read_tsv(registry / "relaciones.tsv"),
        read_tsv(universe / "ledger-inspecciones-barrido2.tsv"),
        read_tsv(registry / "aliases-fuentes.tsv"),
        args.manifest.resolve(),
    )
    write_tsv(output, COVERAGE_FIELDS, coverage)
    write_tsv(_detalle_path(output), DETAIL_FIELDS, detalle)
    largas = [
        (row["fuente_canonica"], field)
        for row in coverage for field, value in row.items() if len(value) > LIMITE_DURABLE
    ]
    if largas:
        raise ValueError(f"celda durable por encima de {LIMITE_DURABLE}: {largas[:3]}")
    summary = {
        "schema_version": SCHEMA_VERSION,
        "fuentes": len(coverage),
        "filas_detalle": len(detalle),
        "por_regla": dict(sorted(Counter(row["regla_resolucion"] for row in coverage).items())),
        "relaciones_con_material": sum(
            int(row["relaciones_n"]) for row in coverage if row["estado_cobertura"] == "CON-MATERIAL"
        ),
        "relaciones_sin_material": sum(
            int(row["relaciones_n"]) for row in coverage if row["estado_cobertura"] == "SIN-MATERIAL-OBSERVADO"
        ),
        "salida_sha256": sha256_file(output),
        "detalle_sha256": sha256_file(_detalle_path(output)),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def payloads_de_apertura(apertura_path: Path | None, ledger_payloads: set[str]) -> dict[str, list[str]]:
    """relacion_id -> payloads que `lista-apertura` declara y el ledger observa.

    El §18 del encargo madre manda unir las 17 aperturas absorbidas "por
    identidad vigente, no por subcadena", y su fuente de verdad es la columna
    `ids_manifiesto_que_lo_proveen` de la propia lista -- NO la cobertura por
    fuente canónica.  Medido: 16 de las 17 declaran un payload que la
    cobertura de su fuente no ofrece (`116334_v1` bajo MICROCREDIT_*,
    `cses5_*` bajo COMPARATIVE_STUDY_*, `dataverse_files` bajo
    MASS_MOBILIZATION_*, `za5900_*`/`za6980_*` bajo ISSP), de modo que sin
    esta vía el curador leería fragmentos que no son los suyos.
    """
    if apertura_path is None or not apertura_path.is_file():
        return {}
    declarados: dict[str, list[str]] = {}
    for fila in read_tsv(apertura_path):
        ids = [i for i in _split_ids(fila.get("ids_manifiesto_que_lo_proveen", ""))
               if i in ledger_payloads]
        if ids:
            declarados[fila["relacion_id"]] = sorted(set(ids))
    return declarados


def escribe_paquetes_de_relacion(
    registry: Path, coverage: list[dict[str, str]], detalle: list[dict[str, str]],
    counts: dict[str, int], shard_root: Path, pack_root: Path,
    apertura: dict[str, list[str]] | None = None,
) -> dict[str, int]:
    """Arma el expediente de lectura de cada relación.

    El curador recibe el índice E2 COMPLETO de sus payloads candidatos — no el
    reporte durable recortado a 160, que el §9 prohíbe usar como única base y
    que además está redactado en el 63 % de sus campos. El paquete no adjudica:
    no propone veredicto ni elige objeto lógico.
    """
    relaciones = {row["relacion_id"]: row for row in read_tsv(registry / "relaciones.tsv")}
    # La tabla trae 37 filas para 33 necesidades: N16/N17/N19/N27 declaran DOS
    # objetos de modelo cada una.  Indexarla como dict por `necesidad_id` se
    # quedaba con la última y perdía la otra mitad; se acumulan las dos.
    # La columna es `objeto_modelo_origen` -- leerla como `descripcion` o
    # `objeto_modelo` (nombres que esta tabla nunca tuvo) dejaba las 199 fichas
    # con `necesidad_texto = NO-DETERMINADO`, es decir al curador sin el
    # enunciado de lo que tiene que adjudicar.
    necesidades: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(registry / "necesidad-objeto-modelo.tsv"):
        necesidades[row["necesidad_id"]].append(row)
    evidencias: dict[str, dict[str, str]] = {}
    for row in read_tsv(registry / "evidencias.tsv"):
        evidencias.setdefault(row["relacion_id"], row)
    por_fuente_payload: dict[str, list[str]] = defaultdict(list)
    por_fuente_relacion: dict[str, list[str]] = defaultdict(list)
    for row in detalle:
        destino = por_fuente_payload if row["tipo"] == "PAYLOAD" else por_fuente_relacion
        destino[row["fuente_canonica"]].append(row["valor"])
    resumen = {"paquetes": 0, "con_material": 0, "sin_material": 0}
    pack_root.mkdir(parents=True, exist_ok=True)
    apertura = apertura or {}
    for fila in coverage:
        fuente = fila["fuente_canonica"]
        payloads_fuente = por_fuente_payload.get(fuente, [])
        for relacion_id in por_fuente_relacion.get(fuente, []):
            relacion = relaciones.get(relacion_id)
            if relacion is None:
                continue
            # Unión por relación: cobertura de la fuente + lo que
            # `lista-apertura` declara para ESTA relación (§18.3).
            declarados = apertura.get(relacion_id, [])
            payloads = sorted(set(payloads_fuente) | set(declarados))
            filas_necesidad = necesidades.get(relacion["necesidad_id"], [])
            objetos_modelo = [
                fila["objeto_modelo_origen"] for fila in filas_necesidad
                if fila.get("objeto_modelo_origen")
            ]
            reservas = sorted({
                fila["reserva"] for fila in filas_necesidad
                if fila.get("reserva") and fila["reserva"] != "NINGUNA"
            })
            paquete = {
                "schema_version": SCHEMA_VERSION,
                "relacion_id": relacion_id,
                "necesidad_id": relacion["necesidad_id"],
                "necesidad_texto": ";".join(objetos_modelo) or "NO-DETERMINADO",
                "necesidad_reserva": ";".join(reservas) or "NINGUNA",
                "fuente_canonica": fuente,
                "regla_resolucion": (
                    fila["regla_resolucion"] + ("+" + REGLA_APERTURA if declarados else "")),
                "evidencia_resolucion": fila["evidencia_resolucion"],
                "capa2_manifiesto": relacion.get("capa2_manifiesto", ""),
                "capa3_disco_real": relacion.get("capa3_disco_real", ""),
                "capa4_actual": relacion.get("capa4_apertura_mapeo", ""),
                "clasificacion_relacion": relacion.get("clasificacion_relacion", ""),
                "evidencia_previa": {
                    campo: evidencias.get(relacion_id, {}).get(campo, "")
                    for campo in ("variable_reactivo_tabla", "texto_evidencia", "unidad_observacion",
                                  "periodo", "universo_muestra", "parte_necesidad_no_cubierta")
                },
                "payloads_candidatos": [
                    {
                        "payload_id": payload,
                        "objetos_e2": counts.get(payload, 0),
                        "fragmento": str((shard_root / f"{_nombre_fragmento(payload)}.jsonl").relative_to(shard_root.parent)),
                    }
                    for payload in payloads
                ],
                "instruccion": (
                    "Lee los fragmentos completos. Elige, si existe, el objeto lógico que responde a la "
                    "necesidad y escribe su record_id y record_sha256 como evidencia. Si no existe, declara "
                    "la frontera de lo que sí revisaste. No inventes payload_id ni objeto_logico_id."
                ),
            }
            (pack_root / f"{relacion_id}.json").write_text(
                json.dumps(paquete, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8"
            )
            resumen["paquetes"] += 1
            resumen["con_material" if payloads else "sin_material"] += 1
    return resumen


def cmd_paquetes(args: argparse.Namespace) -> int:
    coverage_path = args.coverage.resolve()
    coverage = read_tsv(coverage_path)
    por_fuente: dict[str, list[str]] = defaultdict(list)
    for row in read_tsv(_detalle_path(coverage_path)):
        if row["tipo"] == "PAYLOAD":
            por_fuente[row["fuente_canonica"]].append(row["valor"])
    ledger_payloads = {
        r["payload_id"] for r in read_tsv(args.registry.resolve().parent
                                          / "curacion-universo"
                                          / "ledger-inspecciones-barrido2.tsv")
        if r["payload_id"] not in {"", "NO-APLICA"}
    }
    apertura = payloads_de_apertura(args.apertura.resolve() if args.apertura else None,
                                    ledger_payloads)
    wanted = {p for payloads in por_fuente.values() for p in payloads}
    wanted |= {p for payloads in apertura.values() for p in payloads}
    counts, hashes = project_index(args.index.resolve(), wanted, args.shard_root.resolve())
    for row in coverage:
        payloads = por_fuente.get(row["fuente_canonica"], [])
        row["objetos_e2"] = str(sum(counts.get(p, 0) for p in payloads))
    write_tsv(coverage_path, COVERAGE_FIELDS, coverage)
    resumen_packs = escribe_paquetes_de_relacion(
        args.registry.resolve(), coverage, read_tsv(_detalle_path(coverage_path)),
        counts, args.shard_root.resolve(), args.pack_root.resolve(), apertura,
    )
    manifest_out = {
        "schema_version": SCHEMA_VERSION,
        "paquetes_de_relacion": resumen_packs,
        "payloads_proyectados": len(counts),
        "objetos_proyectados": sum(counts.values()),
        "fragmentos_sha256": hashes,
        "indice_sha256": sha256_file(args.index.resolve()),
    }
    (args.shard_root.resolve() / "fragmentos.json").write_text(
        json.dumps(manifest_out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in manifest_out.items() if k != "fragmentos_sha256"},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 0



# ───────────────────────────────────────────────────────────────
# Fase `tareas` · convierte la elección del curador en expediente
#
# ACTO B2-SEMANTICO, 18/ago/2026.  El docstring de este módulo la declaraba
# desde el principio y nunca se escribió: es el eslabón que faltaba entre
# `paquetes` (lo que el curador lee) e `integrate_barrido2.preflight` (lo que
# el integrador vuelve a verificar).
#
# NO adjudica y NO enumera candidatos: recibe la elección ya hecha y sólo
# acepta lo que puede volver a verificar por hash.  Cada campo del expediente
# se REDERIVA del registro E2 elegido y de los productos durables; ninguno se
# copia de la elección salvo los tres que son del curador (el registro que
# eligió, el reactivo que nombra y la frontera que declara).
#
# Cadena de verificación por fila:
#   e2_record_id  -> presente en el fragmento del payload candidato
#                 -> record_sha256 coincide con el declarado
#   registro E2   -> (representacion, objeto_tipo, estado, privacidad,
#                     frontera) identifica UNA fila de reporte durable
#   representacion-> fila de ledger con mismo payload_id y sha256
#   representacion-> descriptor material TASK-B2-*.json, hasheado en vivo
# ───────────────────────────────────────────────────────────────

ELECCION_FIELDS = [
    "relacion_id", "curador_id", "estado_eleccion", "e2_record_id",
    "e2_record_sha256", "reactivo_id", "frontera_semantica", "nota",
]

_GRUPO_REPORTE = (
    "representacion_id", "objeto_tipo", "estado", "privacidad", "frontera_inspeccion",
)


def _indice_descriptores(task_root: Path) -> dict[str, tuple[str, str]]:
    """representacion_id -> (material_tarea_id, sha256 del descriptor).

    El ledger no nombra el descriptor (su `reporte_neutral_ref` es el lote
    E2B-*), así que la correspondencia se toma del propio descriptor, que sí
    declara su `representacion_id`.
    """
    indice: dict[str, tuple[str, str]] = {}
    for ruta in sorted(task_root.glob("*.json")):
        descriptor = json.loads(ruta.read_text(encoding="utf-8"))
        indice[descriptor["representacion_id"]] = (
            descriptor["tarea_id"], sha256_file(ruta),
        )
    return indice


def _registros_de_payloads(shard_root: Path, payloads: Iterable[str]) -> dict[str, dict[str, Any]]:
    registros: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        fragmento = shard_root / f"{_nombre_fragmento(payload)}.jsonl"
        if not fragmento.is_file():
            continue
        with fragmento.open(encoding="utf-8") as handle:
            for linea in handle:
                registro = json.loads(linea)
                registros[registro["record_id"]] = registro
    return registros


def derivar_tareas(
    registry: Path, ledger_path: Path, reports_path: Path,
    material_baseline_path: Path, material_task_root: Path,
    coverage_path: Path, shard_root: Path, elecciones_path: Path,
    apertura_path: Path | None, fecha: str,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    relaciones = {r["relacion_id"]: r for r in read_tsv(registry / "relaciones.tsv")}
    ledger = {r["representacion_id"]: r for r in read_tsv(ledger_path)}
    reportes: dict[tuple[str, ...], dict[str, str]] = {}
    for fila in read_tsv(reports_path):
        reportes.setdefault(tuple(fila[c] for c in _GRUPO_REPORTE), fila)
    por_fuente: dict[str, list[str]] = defaultdict(list)
    for fila in read_tsv(_detalle_path(coverage_path)):
        if fila["tipo"] == "PAYLOAD":
            por_fuente[fila["fuente_canonica"]].append(fila["valor"])

    apertura = payloads_de_apertura(
        apertura_path, {r["payload_id"] for r in ledger.values()
                        if r["payload_id"] not in {"", "NO-APLICA"}})
    descriptores = _indice_descriptores(material_task_root)
    baseline_sha = sha256_file(material_baseline_path)

    tareas: list[dict[str, str]] = []
    rechazos: list[dict[str, str]] = []
    sin_objeto: list[str] = []

    for eleccion in read_tsv(elecciones_path):
        relacion_id = eleccion["relacion_id"]
        relacion = relaciones.get(relacion_id)

        def rechaza(motivo: str) -> None:
            rechazos.append({"relacion_id": relacion_id, "motivo": motivo})

        if relacion is None:
            rechaza("RELACION_INEXISTENTE")
            continue
        if eleccion["estado_eleccion"] != "ELEGIDO":
            sin_objeto.append(relacion_id)
            continue

        # Mismo universo que vio el curador en su ficha: cobertura de la
        # fuente MÁS lo que `lista-apertura` declara para esta relación (§18.3).
        payloads = sorted(set(por_fuente.get(relacion["fuente_canonica_normalizada"], []))
                          | set(apertura.get(relacion_id, [])))
        registros = _registros_de_payloads(shard_root, payloads)
        registro = registros.get(eleccion["e2_record_id"])
        if registro is None:
            rechaza("REGISTRO_E2_FUERA_DE_LOS_PAYLOADS_CANDIDATOS")
            continue
        if registro["record_sha256"] != eleccion["e2_record_sha256"]:
            rechaza("REGISTRO_E2_SHA_DIVERGENTE")
            continue

        reporte = reportes.get(tuple(str(registro[c]) for c in _GRUPO_REPORTE))
        if reporte is None:
            rechaza("SIN_FILA_DE_REPORTE_DURABLE_PARA_EL_GRUPO")
            continue

        fila_ledger = ledger.get(registro["representacion_id"])
        if fila_ledger is None or fila_ledger["payload_id"] != registro["payload_id"] \
                or fila_ledger["sha256"] != registro["sha256"]:
            rechaza("LEDGER_NO_CONFIRMA_LA_REPRESENTACION")
            continue

        descriptor = descriptores.get(registro["representacion_id"])
        if descriptor is None:
            rechaza("SIN_DESCRIPTOR_MATERIAL")
            continue

        tareas.append({
            "tarea_id": stable_id("TSEM-B2-", relacion_id, registro["record_id"]),
            "relacion_id": relacion_id,
            "reporte_id": reporte["reporte_id"],
            "reporte_record_id": reporte["record_id"],
            "reporte_record_sha256": reporte["record_sha256"],
            "e2_record_id": registro["record_id"],
            "e2_record_sha256": registro["record_sha256"],
            "payload_id": registro["payload_id"],
            "representacion_id": registro["representacion_id"],
            "sha256": registro["sha256"],
            "objeto_logico_id": registro["objeto_logico_id"],
            "necesidad_id": relacion["necesidad_id"],
            "reactivo_id": eleccion["reactivo_id"] or registro["objeto_logico_id"],
            "fuente_canonica": relacion["fuente_canonica_normalizada"] or "NO-APLICA",
            "frontera_semantica": _durable(
                eleccion["frontera_semantica"] or registro["frontera_inspeccion"]),
            "material_tarea_id": descriptor[0],
            "material_task_sha256": descriptor[1],
            "material_baseline_sha256": baseline_sha,
            "curador_id": eleccion["curador_id"],
            "fecha": fecha,
        })

    resumen = {
        "schema_version": SCHEMA_VERSION,
        "elecciones_leidas": len(tareas) + len(rechazos) + len(sin_objeto),
        "tareas": len(tareas),
        "sin_objeto": len(sin_objeto),
        "rechazos": rechazos,
        "relaciones": len({t["relacion_id"] for t in tareas}),
        "payloads": sorted({t["payload_id"] for t in tareas}),
        "material_baseline_sha256": baseline_sha,
    }
    return tareas, resumen


def stable_id(prefix: str, *parts: str) -> str:
    return prefix + hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def cmd_tareas(args: argparse.Namespace) -> int:
    tareas, resumen = derivar_tareas(
        args.registry.resolve(), args.ledger.resolve(), args.reports.resolve(),
        args.material_baseline.resolve(), args.material_task_root.resolve(),
        args.coverage.resolve(), args.shard_root.resolve(),
        args.elecciones.resolve(),
        args.apertura.resolve() if args.apertura else None, args.fecha,
    )
    write_tsv(args.output.resolve(), TASK_FIELDS, tareas)
    resumen["salida_sha256"] = sha256_file(args.output.resolve())
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if resumen["rechazos"] else 0



# ───────────────────────────────────────────────────────────────
# Fase `propuestas` · el producto del §17
#
# ACTO B2-SEMANTICO, 18/ago/2026.  Escribe `propuestas-barrido2.tsv` con las 22
# columnas exactas que el §17 fija y que `integrate_barrido2.PROPOSAL_FIELDS` y
# `barrido2-semantic-proposal.schema.json` ya tenían congeladas sin que nadie
# las escribiera nunca.
#
# La propuesta NO se inventa: sale de una tarea (identidad material verificada
# por hash) más el veredicto supervisado de esa relación.  `evidencia_ref` se
# construye como `e2_record_id:e2_record_sha256` porque el preflight del
# integrador exige esa cadena EXACTA y no otra.
#
# Sobre FP-24, que es donde se pierde la gente: la unidad es LA PROPUESTA, no
# la relación ni la fuente (ADR-92(c) y §17), y está prohibido derivar la
# dependencia de pertenecer a la lista histórica de 20.  `dependencia_fp24=SI`
# sólo si aceptar ESA propuesta exige resolver antes la regla de pares
# pendiente; si puede decidirse con evidencia de la fuente o del objeto, es NO
# aunque la relación sea una de las 20.  El bicondicional del §17
# (dependencia=SI <-> requiere=SI y decision=FP-24) se impone aquí, no se
# confía al que escribe: `FP-24/ADR-93` es un valor imposible, el enum sólo
# admite `FP-24` o `NO-APLICA`.
# ───────────────────────────────────────────────────────────────

VEREDICTO_FIELDS = [
    "relacion_id", "veredicto_a4", "confianza", "estado_supervision",
    "supervisor_id", "dependencia_fp24", "razon_gate",
]

PROPOSAL_FIELDS_17 = [
    "propuesta_id", "tarea_id", "reporte_id", "payload_id", "representacion_id",
    "sha256", "objeto_logico_id", "necesidad_id", "reactivo_id",
    "accion_propuesta", "relacion_id_actual", "veredicto_a4", "evidencia_ref",
    "frontera_semantica", "confianza", "requiere_decision_mesa",
    "decision_mesa_id", "dependencia_fp24", "razon_gate", "estado_supervision",
    "supervisor_id", "fecha",
]

_VEREDICTO_A_CAPA4 = {
    "EXISTE-SATISFACE": "EXISTE-SATISFACE",
    "EXISTE-NO-SATISFACE": "EXISTE-NO-SATISFACE",
    "NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO": "NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO",
    "NO-ACCESIBLE": "NO-ACCESIBLE",
    "NO-DETERMINADO": "NO-DETERMINADO",
}


def _accion(veredicto: str, capa4_actual: str) -> str:
    """Regla mecánica y declarada, no juicio.

    El destino de capa4 es el propio veredicto. Si ya está ahí, no hay cambio
    que proponer; si el veredicto es un negativo de universo con frontera, la
    celda cierra como terminal; en lo demás, es un CAMBIO de capa4.
    """
    destino = _VEREDICTO_A_CAPA4.get(veredicto, "NO-DETERMINADO")
    if capa4_actual == destino:
        return "SIN_CAMBIO"
    if veredicto == "NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO":
        return "TERMINAL"
    if veredicto in ("NO-ACCESIBLE", "NO-DETERMINADO"):
        return "SIN_CAMBIO"
    return "CAMBIO"


def derivar_propuestas(
    registry: Path, tasks_path: Path, veredictos_path: Path, fecha: str,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    relaciones = {r["relacion_id"]: r for r in read_tsv(registry / "relaciones.tsv")}
    veredictos = {v["relacion_id"]: v for v in read_tsv(veredictos_path)}
    propuestas: list[dict[str, str]] = []
    rechazos: list[dict[str, str]] = []

    for tarea in read_tsv(tasks_path):
        relacion_id = tarea["relacion_id"]
        veredicto = veredictos.get(relacion_id)
        if veredicto is None:
            rechazos.append({"tarea_id": tarea["tarea_id"], "motivo": "SIN_VEREDICTO_SUPERVISADO"})
            continue
        relacion = relaciones.get(relacion_id)
        if relacion is None:
            rechazos.append({"tarea_id": tarea["tarea_id"], "motivo": "RELACION_INEXISTENTE"})
            continue

        dep = veredicto["dependencia_fp24"]
        if dep not in ("SI", "NO"):
            rechazos.append({"tarea_id": tarea["tarea_id"], "motivo": "DEPENDENCIA_FP24_NO_DECLARADA"})
            continue
        # El bicondicional se impone, no se copia.
        requiere = "SI" if dep == "SI" else "NO"
        decision_mesa = "FP-24" if dep == "SI" else "NO-APLICA"
        estado = veredicto["estado_supervision"]
        if dep == "SI":
            estado = "REQUIERE_DECISION_FP24"

        propuestas.append({
            "propuesta_id": stable_id("PROP-B2-", tarea["tarea_id"]),
            "tarea_id": tarea["tarea_id"],
            "reporte_id": tarea["reporte_id"],
            "payload_id": tarea["payload_id"],
            "representacion_id": tarea["representacion_id"],
            "sha256": tarea["sha256"],
            "objeto_logico_id": tarea["objeto_logico_id"],
            "necesidad_id": tarea["necesidad_id"],
            "reactivo_id": tarea["reactivo_id"],
            "accion_propuesta": _accion(veredicto["veredicto_a4"],
                                        relacion.get("capa4_apertura_mapeo", "")),
            "relacion_id_actual": relacion_id,
            "veredicto_a4": veredicto["veredicto_a4"],
            # Cadena exacta que exige integrate_barrido2.preflight.
            "evidencia_ref": f"{tarea['e2_record_id']}:{tarea['e2_record_sha256']}",
            "frontera_semantica": tarea["frontera_semantica"],
            "confianza": veredicto["confianza"],
            "requiere_decision_mesa": requiere,
            "decision_mesa_id": decision_mesa,
            "dependencia_fp24": dep,
            "razon_gate": _durable(veredicto["razon_gate"]),
            "estado_supervision": estado,
            "supervisor_id": veredicto["supervisor_id"],
            "fecha": fecha,
        })

    resumen = {
        "schema_version": SCHEMA_VERSION,
        "propuestas": len(propuestas),
        "rechazos": rechazos,
        "por_accion": dict(sorted(Counter(p["accion_propuesta"] for p in propuestas).items())),
        "por_veredicto": dict(sorted(Counter(p["veredicto_a4"] for p in propuestas).items())),
        "por_supervision": dict(sorted(Counter(p["estado_supervision"] for p in propuestas).items())),
        "dependencia_fp24_SI": sum(1 for p in propuestas if p["dependencia_fp24"] == "SI"),
    }
    return propuestas, resumen


def cmd_propuestas(args: argparse.Namespace) -> int:
    propuestas, resumen = derivar_propuestas(
        args.registry.resolve(), args.tasks.resolve(),
        args.veredictos.resolve(), args.fecha,
    )
    write_tsv(args.output.resolve(), PROPOSAL_FIELDS_17, propuestas)
    resumen["salida_sha256"] = sha256_file(args.output.resolve())
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if resumen["rechazos"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="comando", required=True)

    f = sub.add_parser("fuentes", help="resuelve fuente canónica -> payloads observados")
    f.add_argument("--registry", type=Path, required=True)
    f.add_argument("--universe", type=Path, required=True)
    f.add_argument("--manifest", type=Path, required=True)
    f.add_argument("--output", type=Path, required=True)
    f.set_defaults(func=cmd_fuentes)

    p = sub.add_parser("paquetes", help="proyecta el índice E2 por payload")
    p.add_argument("--coverage", type=Path, required=True)
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--shard-root", type=Path, required=True)
    p.add_argument("--pack-root", type=Path, required=True)
    p.add_argument("--registry", type=Path, required=True)
    p.add_argument("--apertura", type=Path, default=None)
    p.set_defaults(func=cmd_paquetes)

    t = sub.add_parser("tareas", help="convierte la elección del curador en expediente de tareas")
    t.add_argument("--registry", type=Path, required=True)
    t.add_argument("--ledger", type=Path, required=True)
    t.add_argument("--reports", type=Path, required=True)
    t.add_argument("--material-baseline", type=Path, required=True)
    t.add_argument("--material-task-root", type=Path, required=True)
    t.add_argument("--coverage", type=Path, required=True)
    t.add_argument("--shard-root", type=Path, required=True)
    t.add_argument("--elecciones", type=Path, required=True)
    t.add_argument("--apertura", type=Path, default=None)
    t.add_argument("--fecha", required=True)
    t.add_argument("--output", type=Path, required=True)
    t.set_defaults(func=cmd_tareas)

    pr = sub.add_parser("propuestas", help="escribe propuestas-barrido2.tsv (§17)")
    pr.add_argument("--registry", type=Path, required=True)
    pr.add_argument("--tasks", type=Path, required=True)
    pr.add_argument("--veredictos", type=Path, required=True)
    pr.add_argument("--fecha", required=True)
    pr.add_argument("--output", type=Path, required=True)
    pr.set_defaults(func=cmd_propuestas)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
