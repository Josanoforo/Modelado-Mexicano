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


def escribe_paquetes_de_relacion(
    registry: Path, coverage: list[dict[str, str]], detalle: list[dict[str, str]],
    counts: dict[str, int], shard_root: Path, pack_root: Path,
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
    for fila in coverage:
        fuente = fila["fuente_canonica"]
        payloads = por_fuente_payload.get(fuente, [])
        for relacion_id in por_fuente_relacion.get(fuente, []):
            relacion = relaciones.get(relacion_id)
            if relacion is None:
                continue
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
                "regla_resolucion": fila["regla_resolucion"],
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
    wanted = {p for payloads in por_fuente.values() for p in payloads}
    counts, hashes = project_index(args.index.resolve(), wanted, args.shard_root.resolve())
    for row in coverage:
        payloads = por_fuente.get(row["fuente_canonica"], [])
        row["objetos_e2"] = str(sum(counts.get(p, 0) for p in payloads))
    write_tsv(coverage_path, COVERAGE_FIELDS, coverage)
    resumen_packs = escribe_paquetes_de_relacion(
        args.registry.resolve(), coverage, read_tsv(_detalle_path(coverage_path)),
        counts, args.shard_root.resolve(), args.pack_root.resolve(),
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
    p.set_defaults(func=cmd_paquetes)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
