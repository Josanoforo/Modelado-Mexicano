#!/usr/bin/env python3
"""Prepara, congela, ejecuta y resume FP-373 sin abrir FP-374/F6.

Contrato vigente: F5-documental-ejecucion-v1_1.md (sucesion de v1_0; transporte
corregido por (a)-(d)). El ledger v1_0 se arrastra sin reiniciar; plan y sonda
se escriben como v1_1 y los archivos v1_0 quedan intactos.

NC-0208 (ACTO GEN2-CAJA-SUCESORES-1, 15/sep/2026): `sha256_manifiesto_fuentes`
sucede a F5-documental-ejecucion-v1_2.md (`sha256_manifiesto_fuentes_v1_2`,
A.7) -- acota el hash a las 8 entradas de `data/manifiesto.yaml` que el duelo
usa, no al archivo entero. No reabre ningun veredicto ni la firma
(F5-documental-firma-v1_0.md sigue vigente)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import random
import subprocess
import sys
import zlib
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import yaml
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "forense/prereg-duelo-v2"
ACTO_DIR = DIR / "F5-documental-v1_0"
SPEC_L = DIR / "L-spec-v1_4.json"
SPEC_ESTUDIO = DIR / "F5-panel-viabilidad-presupuesto-spec-v1_0.md"
MANIFIESTO_CONTEXTO = DIR / "paquete-corpus-F5-v2_0/manifiesto-F5-v2_0.json"
MANIFIESTO_FUENTES = ROOT / "data/manifiesto.yaml"
MANIFIESTO_TRANSPORTE = ACTO_DIR / "F5-documental-materializacion-v1_0.json"
PLAN = ACTO_DIR / "F5-documental-plan-v1_2.json"
SALIDAS = ACTO_DIR / "capturas"
SONDA = ACTO_DIR / "sonda-transporte-v1_1.json"
LEDGER = ACTO_DIR / "solicitudes-ledger-v1_0.json"
MCP = ROOT / "tools/f5_documental_mcp.py"

RAW_PREDETERMINADO = ROOT.parent / "mm-corpus/raw"
PAQUETE_PREDETERMINADO = ROOT.parent / "mm-corpus/f5-documental-v1_0"
CELDAS = ("DIN-M-01", "TRA-M-07")
BRAZOS = ("CONTEXTUAL-v2", "FUENTE-DIRIGIDA-v1")
K = 8
SEMILLA = 20260911
MODELO = "claude-opus-5"
PROVEEDOR = "Anthropic firstParty"
MAX_REINTENTOS = 2
# (c) v1_1: --max-turns no existe en el cliente (2.1.270 y 2.1.272); el freno tecnico es --max-budget-usd.
MAX_BUDGET_USD = 2.00
# (c) v1_1: reserva contable previa a cada invocacion (3 turnos observados + 1 de margen); no es flag del CLI.
CARGO_RESERVA = 4
# (a) v1_1: tope de salida admitido a cualquier modelo auxiliar distinto de MODELO en modelUsage.
AUX_TOPE_SALIDA = 200
HERRAMIENTA = "mcp__f5docs__weighted_distribution"
# Firma de mesa (14/sep/2026, ACTO GEN2-F5-DOCUMENTAL-RUN-2): «termina el encargo entonces, ese techo es un estimado».
# El techo de 96 (spec 4.4: 32 llamadas x 3 intentos, una solicitud por llamada) se re-dimensiona en la unidad que
# v1_1 (c) carga -- turnos reales, 3 por invocacion minima --: 32 x 3 x 3 = 288. El ledger v1_0 sigue arrastrado.
TECHO_SOLICITUDES = 288
TIMEOUT = 600
MERGE_720 = "6cda0282079e9623425529f51c2bea171657b0cf"
MERGE_722 = "5f4bfeac2350597c0f66b8f66a14c07befa18a53"
SISTEMA = (
    "Responde solo con el objeto estructurado solicitado. No uses conocimiento externo, "
    "web ni archivos fuera del paquete. No sustituyas encuesta, ola, reactivo, universo, "
    "evento o ponderador. Si el paquete no permite derivar el punto, abstente."
)
ESQUEMA = {
    "type": "object",
    "properties": {
        "estado": {"type": "string", "enum": ["PUNTO", "ABSTENCION"]},
        "punto_porcentaje": {"type": ["number", "null"], "minimum": 0, "maximum": 100},
        "fuente_documental": {"type": "array", "items": {"type": "string"}},
        "derivacion": {"type": "string"},
        "sustitucion_semantica": {"type": "boolean"},
        "nota": {"type": "string"},
    },
    "required": ["estado", "punto_porcentaje", "fuente_documental", "derivacion", "sustitucion_semantica", "nota"],
    "additionalProperties": False,
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_archivo(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def sha256_manifiesto_fuentes_v1_2(fuentes: dict[str, dict], ids_del_duelo: list[str]) -> str:
    """FP-373 v1.2 (`F5-documental-ejecucion-v1_2.md`, A.7): acota el hash a
    las entradas de `data/manifiesto.yaml` que el duelo usa, no al archivo
    entero -- que crece con cada adquisicion ajena. Un id ausente es PARO,
    no una fila que se salta. Serializacion canonica declarada en el
    contrato: orden por `id` ascendente, `json.dumps(sort_keys=True,
    ensure_ascii=False, separators=(',', ':'))`, sha256 en UTF-8."""
    sel = [fuentes[i] for i in ids_del_duelo]
    assert len(sel) == len(ids_del_duelo)
    canon = json.dumps(sorted(sel, key=lambda e: e["id"]),
                        sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha_bytes(canon.encode("utf-8"))


def json_publico(path: Path, datos: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cargar_modulo(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(modulo)
    return modulo


def manifiesto_por_id() -> dict[str, dict]:
    filas = yaml.safe_load(MANIFIESTO_FUENTES.read_text(encoding="utf-8"))
    out = {}
    for fila in filas:
        ident = fila.get("id")
        if ident in out:
            raise RuntimeError(f"id de fuente duplicado: {ident}")
        out[ident] = fila
    return out


def validar_fuente(raw: Path, entrada: dict) -> Path:
    ruta = raw / entrada["archivo"]
    if not ruta.is_file():
        raise RuntimeError(f"FUENTE-AUSENTE: {entrada['id']} ({ruta})")
    if ruta.stat().st_size != int(entrada["tamano_bytes"]):
        raise RuntimeError(f"tamano distinto: {entrada['id']}")
    if sha_archivo(ruta) != entrada["sha256"]:
        raise RuntimeError(f"hash distinto: {entrada['id']}")
    return ruta


def texto_pdf(path_or_bytes: Path | bytes) -> str:
    lector = PdfReader(path_or_bytes if isinstance(path_or_bytes, Path) else BytesIO(path_or_bytes))
    texto = "\n\n".join((p.extract_text() or "") for p in lector.pages)
    if not texto.strip():
        raise RuntimeError("PDF sin texto extraible")
    return texto


def escribir_texto(path: Path, texto: str) -> dict:
    data = texto.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"ruta_logica": path.name, "bytes": len(data), "chars": len(data.decode()), "sha256": sha_bytes(data)}


def escribir_tsv(path: Path, filas: list[dict], columnas: list[str]) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    return {"ruta_logica": path.name, "bytes": path.stat().st_size, "filas": len(filas),
            "columnas": columnas, "sha256": sha_archivo(path)}


def _dta_zip(path: Path, miembro: str, columnas: list[str]) -> pd.DataFrame:
    with ZipFile(path) as z:
        return pd.read_stata(BytesIO(z.read(miembro)), convert_categoricals=False, columns=columnas)


def validar_miembro_extraido(archive: Path, miembro: str, extraido: Path) -> bytes:
    if not extraido.is_file():
        raise RuntimeError(f"FUENTE-AUSENTE: miembro extraido {miembro}")
    with ZipFile(archive) as z:
        meta = z.getinfo(miembro)
    bruto = extraido.read_bytes()
    if len(bruto) != meta.file_size or (zlib.crc32(bruto) & 0xFFFFFFFF) != meta.CRC:
        raise RuntimeError(f"miembro extraido no coincide por tamano/CRC32: {miembro}")
    return bruto


def materializar(raw: Path, paquete: Path, escribir_manifiesto: bool = True) -> dict:
    fuentes = manifiesto_por_id()
    ids = {
        "DIN-M-01": ["ennvih1_2002_hogar_q", "ennvih1_2002_hogar_cb", "ennvih1_2002_hogar_dta",
                     "ennvih1_2002_ponderador", "ennvih1_muestra_diseno"],
        "TRA-M-07": ["encig2021_cuestionario_pdf", "encig2021_estructura_base_datos_pdf",
                     "encig_2021_encig21_base_datos_csv"],
    }
    rutas = {i: validar_fuente(raw, fuentes[i]) for grupo in ids.values() for i in grupo}
    ensamblador = cargar_modulo("construye_corpus_f5_v2", ROOT / "tools/construye_corpus_f5_v2.py")
    contexto_m = json.loads(MANIFIESTO_CONTEXTO.read_text(encoding="utf-8"))
    celdas = {}
    for cid in CELDAS:
        base_control = paquete / cid / "CONTEXTUAL-v2"
        base_dirigido = paquete / cid / "FUENTE-DIRIGIDA-v1"
        contexto = ensamblador.contexto_desde_entrada(contexto_m["celdas"][cid])
        if sha_bytes(contexto.encode()) != contexto_m["celdas"][cid]["sha256_contenido_entregado"]:
            raise RuntimeError(f"paquete contextual alterado: {cid}")
        contexto_info = escribir_texto(base_control / "contextual.txt", contexto)
        escribir_texto(base_dirigido / "contextual.txt", contexto)
        docs = []
        if cid == "DIN-M-01":
            bruto_q = validar_miembro_extraido(rutas["ennvih1_2002_hogar_q"], "ehh02q_b3b.pdf",
                                                raw / "ennvih/doc/ehh02q_b3b.pdf")
            bruto_cb = validar_miembro_extraido(rutas["ennvih1_2002_hogar_cb"], "ehh02cb_b3b.pdf",
                                                 raw / "ennvih/doc/ehh02cb_b3b.pdf")
            docs.append(escribir_texto(base_dirigido / "cuestionario-book3b.txt", texto_pdf(bruto_q)))
            docs.append(escribir_texto(base_dirigido / "codebook-book3b.txt", texto_pdf(bruto_cb)))
            docs.append(escribir_texto(base_dirigido / "diseno-muestral.txt", texto_pdf(rutas["ennvih1_muestra_diseno"])))
            cr = _dta_zip(rutas["ennvih1_2002_hogar_dta"],
                          "ehh02dta_all/ehh02dta_b3b/iiib_cr.dta", ["folio", "ls", "cr27"])
            wt = _dta_zip(rutas["ennvih1_2002_ponderador"],
                          "ehh02w_all/ehh02w_b3b.dta", ["folio", "ls", "fac_3b"])
            cr["folio"] = cr["folio"].astype("Int64").astype(str).str.zfill(8)
            cr["ls"] = cr["ls"].astype("Int64")
            wt["folio"] = wt["folio"].astype(str).str.zfill(8)
            wt["ls"] = wt["ls"].astype("Int64")
            unido = cr.merge(wt, on=["folio", "ls"], how="left", validate="one_to_one")
            if unido["fac_3b"].isna().any():
                raise RuntimeError("DIN: faltan ponderadores tras llave folio+ls")
            if not set(cr["cr27"].dropna().astype(int).unique()) <= {1, 3, 7}:
                raise RuntimeError("DIN: codigos cr27 inesperados")
            def entero(v):
                return "" if pd.isna(v) else str(int(v))
            filas = [{"folio": x.folio, "ls": entero(x.ls), "cr27": entero(x.cr27), "fac_3b": entero(x.fac_3b)}
                     for x in unido.itertuples(index=False)]
            tabla = escribir_tsv(base_dirigido / "analysis.tsv", filas, ["folio", "ls", "cr27", "fac_3b"])
            receta = "union uno-a-uno de iiib_cr.dta y ehh02w_b3b.dta por folio+ls; sin filtrar ni agregar"
        else:
            docs.append(escribir_texto(base_dirigido / "cuestionario-encig2021.txt", texto_pdf(rutas["encig2021_cuestionario_pdf"])))
            docs.append(escribir_texto(base_dirigido / "estructura-encig2021.txt", texto_pdf(rutas["encig2021_estructura_base_datos_pdf"])))
            miembro = "encig2021_01_sec1_A_3_4_5_8_9_10.csv"
            columnas = ["ID_PER", "ID_VIV", "P8_3_1", "FAC_P18", "EST_DIS", "UPM_DIS"]
            with ZipFile(rutas["encig_2021_encig21_base_datos_csv"]) as z:
                df = pd.read_csv(z.open(miembro), usecols=columnas, dtype=str, keep_default_na=False)
            if not set(df["P8_3_1"].unique()) <= {"1", "2", "9"}:
                raise RuntimeError("TRA: codigos P8_3_1 inesperados")
            filas = df[columnas].to_dict(orient="records")
            tabla = escribir_tsv(base_dirigido / "analysis.tsv", filas, columnas)
            receta = f"seleccion mecanica de seis campos de {miembro}; todas las filas, sin filtrar ni agregar"
        celdas[cid] = {
            "contextual": contexto_info,
            "documentos_texto": docs,
            "tabla_analisis": tabla,
            "receta_tabla": receta,
            "fuentes": [{k: fuentes[i].get(k) for k in ("id", "archivo", "sha256", "tamano_bytes", "formato", "licencia")}
                        for i in ids[cid]],
            "orden_dirigido": ["tarjeta", "contextual.txt", *[d["ruta_logica"] for d in docs], "analysis.tsv (via MCP)"],
        }
        if cid == "DIN-M-01":
            celdas[cid]["discrepancias_transporte"] = [
                "El codebook PDF imprime NS=8; el DTA transportado usa 7 para la categoria no valida. "
                "El estimando admite exclusivamente 1=Si y 3=No, por lo que ambos codigos NS quedan fuera."
            ]
    snapshot = DIR / "snapshot-M-gen2-explicito-v1_1.json"
    snapshot_data = json.loads(snapshot.read_text(encoding="utf-8"))
    manifest = {
        "acto": "GEN2-F5-DOCUMENTAL-EJECUCION",
        "version": "v1_0",
        "celdas": celdas,
        "extraccion_pdf": f"pypdf {__import__('pypdf').__version__}; texto completo por pagina en orden",
        "pandas": pd.__version__,
        "sha256_manifiesto_fuentes": sha256_manifiesto_fuentes_v1_2(
            fuentes, sorted({i for grupo in ids.values() for i in grupo})),
        "sha256_manifiesto_contexto": sha_archivo(MANIFIESTO_CONTEXTO),
        "contrato_720": {
            "merge": MERGE_720,
            "seleccion": "SELECCION-TEMPORAL-v1 / seleccionar_transferencia / seleccion_transferencia",
            "snapshot": str(snapshot.relative_to(ROOT)),
            "snapshot_schema_version": snapshot_data["schema_version"],
            "snapshot_sha256": sha_archivo(snapshot),
        },
        "dependencia_722_merge": MERGE_722,
        "prohibicion": "No contiene punto R, tabulacion objetivo ni resultados de capturas.",
    }
    if escribir_manifiesto:
        json_publico(MANIFIESTO_TRANSPORTE, manifest)
    return manifest


def tarjeta(cid: str) -> dict:
    datos = json.loads(SPEC_L.read_text(encoding="utf-8"))
    return next(x for x in datos["celdas"] if x["id"] == cid)


def prompt(cid: str, brazo: str, paquete: Path, manifest: dict) -> str:
    card = tarjeta(cid)
    base = paquete / cid / brazo
    partes = [
        "# Tarjeta congelada\n" + json.dumps({k: card[k] for k in (
            "id", "encuesta", "ola", "universo", "evento_L", "unidad_observacion", "escala", "pregunta_L")}, ensure_ascii=False),
        "# Contexto contemporaneo autorizado\n" + (base / "contextual.txt").read_text(encoding="utf-8"),
    ]
    if brazo == "FUENTE-DIRIGIDA-v1":
        partes.append("# Documentos fuente-nativos, serializacion textual completa")
        for info in manifest["celdas"][cid]["documentos_texto"]:
            p = base / info["ruta_logica"]
            partes.append(f"## {p.name}\n" + p.read_text(encoding="utf-8"))
        tabla = manifest["celdas"][cid]["tabla_analisis"]
        partes.append(
            "# Tabla fuente-nativa accesible con la unica herramienta\n"
            f"Ruta: analysis.tsv; columnas: {tabla['columnas']}; filas: {tabla['filas']}; sha256: {tabla['sha256']}.\n"
            "Usa weighted_distribution si los documentos te permiten identificar la columna de respuesta, "
            "sus codigos validos y el ponderador. La herramienta recorre el TSV completo."
        )
        if manifest["celdas"][cid].get("discrepancias_transporte"):
            partes.append("# Discrepancias fuente-nativas verificadas\n" +
                          "\n".join(manifest["celdas"][cid]["discrepancias_transporte"]))
    partes.append(
        "# Tarea\nResponde la pregunta de la tarjeta. Un PUNTO exige derivacion documental pertinente y trazable; "
        "una cifra aproximada o de otro estimando es ABSTENCION. fuente_documental debe nombrar los archivos usados. "
        "punto_porcentaje debe ser null cuando estado=ABSTENCION. Marca sustitucion_semantica=true ante cualquier cambio de objeto."
    )
    return "\n\n".join(partes)


def version_cliente() -> str:
    p = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True, timeout=15)
    return p.stdout.strip() or p.stderr.strip()


def comprobar_ancestros() -> None:
    for sha in (MERGE_720, MERGE_722):
        p = subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT)
        if p.returncode:
            raise RuntimeError(f"HEAD no desciende de {sha}")


def verificar_autorizacion(path: Path) -> dict:
    try:
        relativa = path.resolve().relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError("la firma debe estar archivada dentro del repositorio") from exc
    if tuple(relativa.parts[:3]) == ("forense", "encargos", "cola"):
        raise RuntimeError("una cola o propuesta no constituye firma")
    texto = path.read_text(encoding="utf-8")
    if "FIRMA DE JONÁS" not in texto and "FIRMA DE MESA" not in texto:
        raise RuntimeError("falta marcador explicito FIRMA DE JONÁS/FIRMA DE MESA")
    requisitos = ("Autorizo el encargo 31 y FP-373", "32 posiciones", "máximo 96 solicitudes", "No autorizo FP-374 ni F6")
    faltan = [x for x in requisitos if x not in texto]
    if faltan:
        raise RuntimeError(f"firma no coincide con alcance esperado; faltan: {faltan}")
    return {"ruta_archivada": str(relativa), "sha256": sha_archivo(path), "bytes": path.stat().st_size}


def posiciones(cliente: str, paquete: Path, manifest: dict) -> list[dict]:
    out = []
    for cid in CELDAS:
        for brazo in BRAZOS:
            p = prompt(cid, brazo, paquete, manifest)
            for replica in range(1, K + 1):
                base = {"id_celda": cid, "brazo": brazo, "replica": replica, "cliente_version": cliente,
                        "modelo_exacto": MODELO, "sha256_prompt": sha_bytes(p.encode()),
                        "sha256_materializacion": sha_archivo(MANIFIESTO_TRANSPORTE)}
                ident = sha_bytes(json.dumps(base, sort_keys=True).encode())
                out.append({**base, "identidad": ident,
                            "ruta": str((SALIDAS / f"{cid}__{brazo}__{replica:02d}.json").relative_to(ROOT)),
                            "prompt_chars": len(p), "prompt_bytes": len(p.encode())})
    random.Random(SEMILLA).shuffle(out)
    return out


def verificar_paquete(paquete: Path, manifest: dict) -> None:
    for cid in CELDAS:
        por_brazo = {
            "CONTEXTUAL-v2": [manifest["celdas"][cid]["contextual"]],
            "FUENTE-DIRIGIDA-v1": [manifest["celdas"][cid]["contextual"],
                                    *manifest["celdas"][cid]["documentos_texto"],
                                    manifest["celdas"][cid]["tabla_analisis"]],
        }
        for brazo, infos in por_brazo.items():
            for info in infos:
                ruta = paquete / cid / brazo / info["ruta_logica"]
                if not ruta.is_file() or ruta.stat().st_size != info["bytes"] or sha_archivo(ruta) != info["sha256"]:
                    raise RuntimeError(f"paquete alterado: {cid}/{brazo}/{info['ruta_logica']}")


def verificar_plan_integridad(plan: dict, paquete: Path, manifest: dict) -> None:
    comprobar_ancestros()
    if plan["sha256_parser_runner"] != sha_archivo(Path(__file__)) or plan["sha256_mcp"] != sha_archivo(MCP):
        raise RuntimeError("runner o herramienta MCP cambiaron desde la congelacion")
    verificar_paquete(paquete, manifest)
    actual = posiciones(plan["cliente_version"], paquete, manifest)
    if actual != plan["posiciones"]:
        raise RuntimeError("posiciones/prompts no reproducen el plan congelado")


def congelar_plan(paquete: Path, autorizacion: Path) -> dict:
    comprobar_ancestros()
    firma = verificar_autorizacion(autorizacion)
    manifest = json.loads(MANIFIESTO_TRANSPORTE.read_text(encoding="utf-8"))
    cliente = version_cliente()
    ps = posiciones(cliente, paquete, manifest)
    plan = {
        "acto": "GEN2-F5-DOCUMENTAL-EJECUCION", "version": "v1_2", "firma": firma,
        "repo_head_precongelacion": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "cliente_version": cliente, "proveedor": PROVEEDOR, "cuenta": "claude.ai Max; firstParty; sin identificador personal",
        "modelo_exacto": MODELO, "endpoint_modalidad": "Claude Code CLI print sobre claude.ai; stdin + MCP stdio local aislado",
        "herramientas": [HERRAMIENTA], "web": False,
        "parametros": {"temperatura": "no expuesta por CLI", "top_p": "no expuesto por CLI", "seed_modelo": "no expuesta",
                       "max_turns": "no expuesto por el cliente (v1_1 c)", "max_budget_usd": MAX_BUDGET_USD,
                       "cargo_reserva": CARGO_RESERVA, "aux_tope_salida": AUX_TOPE_SALIDA,
                       "output_schema": ESQUEMA, "timeout_s": TIMEOUT},
        "k": K, "semilla_orden": SEMILLA, "max_reintentos_tecnicos": MAX_REINTENTOS,
        "techo_solicitudes_proveedor": TECHO_SOLICITUDES, "n_posiciones": len(ps), "posiciones": ps,
        "coste": "suscripcion Max; modelUsage.costUSD se registra como base de lista, no como cargo monetario observado",
        "sha256_spec_estudio": sha_archivo(SPEC_ESTUDIO), "sha256_parser_runner": sha_archivo(Path(__file__)),
        "sha256_mcp": sha_archivo(MCP), "fecha_congelacion_utc": datetime.now(timezone.utc).isoformat(),
    }
    json_publico(PLAN, plan)
    return plan


def comando_mcp(paquete_celda: Path) -> list[str]:
    config = {"mcpServers": {"f5docs": {"type": "stdio", "command": sys.executable,
                                          "args": [str(MCP), "--root", str(paquete_celda)]}}}
    return ["claude", "-p", "--model", MODELO, "--output-format", "json", "--json-schema", json.dumps(ESQUEMA),
            "--system-prompt", SISTEMA, "--tools", HERRAMIENTA, "--allowedTools", HERRAMIENTA,
            "--max-budget-usd", f"{MAX_BUDGET_USD:.2f}", "--strict-mcp-config", "--mcp-config", json.dumps(config), "--disable-slash-commands",
            "--no-session-persistence", "--prompt-suggestions", "false", "--permission-prompts", "none", "--restricted"]


def modelos(sobre: dict | None) -> set[str]:
    uso = sobre.get("modelUsage", {}) if isinstance(sobre, dict) else {}
    return {str(v.get("canonicalModel") or k) for k, v in uso.items() if isinstance(v, dict)}


def uso_modelo(sobre: dict | None, modelo: str) -> dict | None:
    uso = sobre.get("modelUsage", {}) if isinstance(sobre, dict) else {}
    for k, v in uso.items():
        if isinstance(v, dict) and (v.get("canonicalModel") or k) == modelo:
            return v
    return None


def identidad_modelo(sobre: dict | None) -> dict:
    """Regla (a) v1_1: usage de nivel superior reconcilia exacto con modelUsage[MODELO]; auxiliares <= AUX_TOPE_SALIDA."""
    pares = (("input_tokens", "inputTokens"), ("output_tokens", "outputTokens"),
             ("cache_creation_input_tokens", "cacheCreationInputTokens"), ("cache_read_input_tokens", "cacheReadInputTokens"))
    usage = sobre.get("usage", {}) if isinstance(sobre, dict) else {}
    primario = uso_modelo(sobre, MODELO)
    comparados = [{"campo_usage": a, "campo_modelUsage": b, "usage": usage.get(a) if isinstance(usage, dict) else None,
                   "modelUsage": primario.get(b) if primario else None} for a, b in pares]
    reconcilia = primario is not None and isinstance(usage, dict) and all(
        x["usage"] is not None and x["usage"] == x["modelUsage"] for x in comparados)
    auxiliares = []
    uso = sobre.get("modelUsage", {}) if isinstance(sobre, dict) else {}
    for k, v in uso.items():
        if isinstance(v, dict) and (v.get("canonicalModel") or k) != MODELO:
            salida = v.get("outputTokens")
            auxiliares.append({"modelo": v.get("canonicalModel") or k, "outputTokens": salida,
                               "tope": AUX_TOPE_SALIDA, "admitido": isinstance(salida, int) and salida <= AUX_TOPE_SALIDA})
    return {"reconciliacion_usage_modelo": {"ok": reconcilia, "modelo": MODELO, "pares": comparados},
            "modelos_auxiliares": auxiliares,
            "ok": reconcilia and all(a["admitido"] for a in auxiliares)}


def cargo_solicitudes(sobre: dict | None) -> int:
    """(c) v1_1: carga el num_turns real, sin recorte hacia abajo. Sin sobre (invocacion fallida) se conserva la
    reserva; con sobre pero num_turns invalido o ausente se sanea hacia arriba a 1."""
    if not isinstance(sobre, dict):
        return CARGO_RESERVA
    turnos = sobre.get("num_turns")
    if not isinstance(turnos, int) or turnos < 1:
        return 1
    return turnos


def leer_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"acto": "GEN2-F5-DOCUMENTAL-EJECUCION", "techo": TECHO_SOLICITUDES, "consumidas_conservadoras": 0, "eventos": []}


def reservar_invocacion(ledger: dict, clase: str, ident: str) -> int:
    reservar_o_parar(ledger)
    ledger["consumidas_conservadoras"] += CARGO_RESERVA
    ledger["eventos"].append({"timestamp_reserva_utc": datetime.now(timezone.utc).isoformat(), "clase": clase,
                              "identidad": ident, "cargo": CARGO_RESERVA, "estado": "RESERVADA-SIN-SOBRE"})
    json_publico(LEDGER, ledger)
    return len(ledger["eventos"]) - 1


def cerrar_reserva(ledger: dict, indice: int, sobre: dict | None) -> int:
    cargo = cargo_solicitudes(sobre)
    evento = ledger["eventos"][indice]
    if evento.get("estado") != "RESERVADA-SIN-SOBRE":
        raise RuntimeError("reserva de solicitudes ya cerrada")
    ledger["consumidas_conservadoras"] -= CARGO_RESERVA - cargo
    evento.update({"timestamp_cierre_utc": datetime.now(timezone.utc).isoformat(), "cargo": cargo,
                   "num_turns_reportado": (sobre or {}).get("num_turns"), "cargo_real_turnos": cargo,
                   "total_cost_usd": (sobre or {}).get("total_cost_usd"), "estado": "CERRADA"})
    json_publico(LEDGER, ledger)
    return cargo


def reservar_o_parar(ledger: dict) -> None:
    if ledger["consumidas_conservadoras"] + CARGO_RESERVA > TECHO_SOLICITUDES:
        raise RuntimeError("TECHO-SOLICITUDES: no hay margen para reservar una invocacion")


def invocar(texto: str, cwd: Path) -> tuple[dict | None, dict]:
    inicio = datetime.now(timezone.utc).isoformat()
    try:
        p = subprocess.run(comando_mcp(cwd), input=texto, capture_output=True, text=True, timeout=TIMEOUT, cwd=cwd)
        intento = {"inicio_utc": inicio, "fin_utc": datetime.now(timezone.utc).isoformat(), "returncode": p.returncode,
                   "stdout_original": p.stdout, "stderr_original": p.stderr}
        try:
            sobre = json.loads(p.stdout)
        except json.JSONDecodeError:
            sobre = None
        if p.returncode or not isinstance(sobre, dict) or sobre.get("is_error"):
            return None, intento
        return sobre, intento
    except subprocess.TimeoutExpired as exc:
        return None, {"inicio_utc": inicio, "fin_utc": datetime.now(timezone.utc).isoformat(), "error": "TimeoutExpired",
                      "stdout_original": exc.stdout, "stderr_original": exc.stderr}


def sonda_transporte(paquete: Path, autorizacion: Path) -> dict:
    verificar_autorizacion(autorizacion)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan["cliente_version"] != version_cliente():
        raise RuntimeError("cliente cambio desde el plan")
    manifest = json.loads(MANIFIESTO_TRANSPORTE.read_text(encoding="utf-8"))
    cid = "TRA-M-07"
    tabla = manifest["celdas"][cid]["tabla_analisis"]
    marcador = sha_bytes((tabla["sha256"] + plan["firma"]["sha256"]).encode())
    texto = prompt(cid, "FUENTE-DIRIGIDA-v1", paquete, manifest) + (
        "\n\n# SONDA, NO ES REPLICA\nUsa weighted_distribution sobre analysis.tsv con P8_3_1 y FAC_P18. "
        f"Luego responde estado=ABSTENCION, punto_porcentaje=null y copia este marcador en nota: {marcador}"
    )
    verificar_plan_integridad(plan, paquete, manifest)
    ledger = leer_ledger(); reserva = reservar_invocacion(ledger, "SONDA_TRANSPORTE", marcador)
    sobre, intento = invocar(texto, paquete / cid / "FUENTE-DIRIGIDA-v1")
    cargo = cerrar_reserva(ledger, reserva, sobre)
    estructurada = (sobre or {}).get("structured_output")
    identidad = identidad_modelo(sobre)
    denegadas = [d.get("tool_name") for d in ((sobre or {}).get("permission_denials") or []) if isinstance(d, dict)]
    coste = (sobre or {}).get("total_cost_usd")
    condiciones = {
        "1_marcador_en_nota": isinstance(estructurada, dict) and marcador in estructurada.get("nota", ""),
        "2_identidad_modelo": identidad["ok"],
        "3_herramienta_no_denegada": sobre is not None and HERRAMIENTA not in denegadas,
        "4_coste_bajo_presupuesto": isinstance(coste, (int, float)) and coste <= MAX_BUDGET_USD,
        "5_cargo_real_registrado": sobre is not None and cargo == cargo_solicitudes(sobre) and cargo >= 1,
    }
    ok = all(condiciones.values())
    registro = {"acto": "GEN2-F5-DOCUMENTAL-EJECUCION", "version": "v1_1",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "estado": "TRANSPORTE-VALIDADO" if ok else "TRANSPORTE-NO-VALIDADO", "marcador": marcador,
                "sha256_tabla": tabla["sha256"], "condiciones": condiciones, "modelos_reportados": sorted(modelos(sobre)),
                "reconciliacion_usage_modelo": identidad["reconciliacion_usage_modelo"],
                "modelos_auxiliares": identidad["modelos_auxiliares"], "permission_denials": denegadas,
                "total_cost_usd": coste, "max_budget_usd": MAX_BUDGET_USD,
                "num_turns": (sobre or {}).get("num_turns"), "cargo_real_turnos": cargo,
                "consumidas_conservadoras_tras_sonda": ledger["consumidas_conservadoras"], "techo": TECHO_SOLICITUDES,
                "sobre_cli_original": sobre, "intento": intento}
    json_publico(SONDA, registro)
    if not ok:
        raise RuntimeError("TRANSPORTE-NO-VALIDADO")
    return registro


def error_sistemico(intento: dict) -> bool:
    texto = str(intento.get("stdout_original", "")) + "\n" + str(intento.get("stderr_original", ""))
    return any(x in texto.lower() for x in ("auth", "quota", "rate limit", "credit", "login", "usage limit", "hit your limit"))


def ejecutar(paquete: Path, autorizacion: Path) -> dict:
    firma = verificar_autorizacion(autorizacion)
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if firma["sha256"] != plan["firma"]["sha256"] or version_cliente() != plan["cliente_version"]:
        raise RuntimeError("firma o cliente distintos del plan")
    if not SONDA.exists() or json.loads(SONDA.read_text(encoding="utf-8")).get("estado") != "TRANSPORTE-VALIDADO":
        raise RuntimeError("falta sonda TRANSPORTE-VALIDADO")
    manifest = json.loads(MANIFIESTO_TRANSPORTE.read_text(encoding="utf-8"))
    verificar_plan_integridad(plan, paquete, manifest)
    prompts = {(c, b): prompt(c, b, paquete, manifest) for c in CELDAS for b in BRAZOS}
    ledger = leer_ledger(); consecutivos_sistemicos = 0; nuevas = reanudadas = errores = 0
    for pos in plan["posiciones"]:
        ruta = ROOT / pos["ruta"]
        if ruta.exists():
            previo = json.loads(ruta.read_text(encoding="utf-8"))
            if previo.get("identidad") != pos["identidad"]:
                raise RuntimeError(f"colision de identidad: {ruta}")
            if previo.get("estado_captura") in {"PUNTO", "ABSTENCION", "MALFORMADA"}:
                reanudadas += 1; continue
        intentos = []
        sobre = None
        for numero in range(1, MAX_REINTENTOS + 2):
            reserva = reservar_invocacion(ledger, "POSICION", pos["identidad"])
            sobre, intento = invocar(prompts[(pos["id_celda"], pos["brazo"])],
                                      paquete / pos["id_celda"] / pos["brazo"])
            intento["numero"] = numero; intentos.append(intento)
            cerrar_reserva(ledger, reserva, sobre)
            if sobre is not None:
                consecutivos_sistemicos = 0
                break
            if error_sistemico(intento):
                consecutivos_sistemicos += 1
                if consecutivos_sistemicos >= 2:
                    break
            else:
                consecutivos_sistemicos = 0
        estructura = (sobre or {}).get("structured_output")
        identidad = identidad_modelo(sobre)
        if sobre is None:
            estado = "ERROR_TECNICO"
        elif not identidad["ok"]:
            estado = "ERROR_IDENTIDAD"
        elif not isinstance(estructura, dict):
            estado = "MALFORMADA"
        else:
            estado = estructura.get("estado", "MALFORMADA")
            if estado == "PUNTO" and not isinstance(estructura.get("punto_porcentaje"), (int, float)):
                estado = "MALFORMADA"
        registro = {**pos, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "estado_captura": estado,
                    "respuesta_estructurada": estructura, "modelos_reportados": sorted(modelos(sobre)),
                    "reconciliacion_usage_modelo": identidad["reconciliacion_usage_modelo"],
                    "modelos_auxiliares": identidad["modelos_auxiliares"],
                    "cargo_real_turnos": sum(e["cargo"] for e in ledger["eventos"] if e["identidad"] == pos["identidad"]),
                    "total_cost_usd": (sobre or {}).get("total_cost_usd"),
                    "sobre_cli_original": sobre, "intentos": intentos}
        json_publico(ruta, registro)
        if estado in {"ERROR_TECNICO", "ERROR_IDENTIDAD"}: errores += 1
        else: nuevas += 1
        if estado == "ERROR_IDENTIDAD" or consecutivos_sistemicos >= 2:
            break
    return {"nuevas_resueltas": nuevas, "reanudadas": reanudadas, "errores": errores,
            "solicitudes_conservadoras": ledger["consumidas_conservadoras"]}


def resumen() -> dict:
    if not PLAN.exists():
        return {"estado": "SIN-PLAN-CONGELADO"}
    plan = json.loads(PLAN.read_text(encoding="utf-8")); detalle = {}
    for cid in CELDAS:
        detalle[cid] = {}
        for brazo in BRAZOS:
            regs = []
            for p in plan["posiciones"]:
                if p["id_celda"] == cid and p["brazo"] == brazo and (ROOT / p["ruta"]).exists():
                    regs.append(json.loads((ROOT / p["ruta"]).read_text(encoding="utf-8")))
            estados = {x: sum(r.get("estado_captura") == x for r in regs) for x in
                       ("PUNTO", "ABSTENCION", "MALFORMADA", "ERROR_TECNICO", "ERROR_IDENTIDAD")}
            trazables = sum(r.get("estado_captura") == "PUNTO" and
                            not (r.get("respuesta_estructurada") or {}).get("sustitucion_semantica", True)
                            for r in regs)
            detalle[cid][brazo] = {"ejecutadas": len(regs), **estados, "puntos_sin_sustitucion_pendientes_revision_traza": trazables}
    return {"acto": plan["acto"], "detalle": detalle,
            "solicitudes_conservadoras": leer_ledger()["consumidas_conservadoras"] if LEDGER.exists() else 0,
            "nota": "La trazabilidad documental requiere revision de las 32 derivaciones antes del veredicto final."}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", type=Path, default=RAW_PREDETERMINADO)
    ap.add_argument("--package-root", type=Path, default=PAQUETE_PREDETERMINADO)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prepare", action="store_true")
    g.add_argument("--verify", action="store_true")
    g.add_argument("--freeze-plan", action="store_true")
    g.add_argument("--transport-probe", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--summary", action="store_true")
    ap.add_argument("--authorization-file", type=Path)
    args = ap.parse_args()
    if args.prepare:
        out = materializar(args.raw_root, args.package_root, True)
        print(json.dumps({c: {"tabla": out["celdas"][c]["tabla_analisis"], "docs": out["celdas"][c]["documentos_texto"]}
                          for c in CELDAS}, ensure_ascii=False, indent=2)); return 0
    if args.verify:
        esperado = materializar(args.raw_root, args.package_root, False)
        actual = json.loads(MANIFIESTO_TRANSPORTE.read_text(encoding="utf-8"))
        if esperado != actual: raise RuntimeError("materializacion no reproduce manifiesto")
        comprobar_ancestros(); print("OK: fuentes, paquetes y ancestros reproducen"); return 0
    if args.summary:
        print(json.dumps(resumen(), ensure_ascii=False, indent=2)); return 0
    if args.authorization_file is None:
        raise SystemExit("--authorization-file es obligatorio para congelar o llamar al proveedor")
    if args.freeze_plan:
        print(json.dumps(congelar_plan(args.package_root, args.authorization_file), ensure_ascii=False, indent=2)); return 0
    if args.transport_probe:
        print(json.dumps(sonda_transporte(args.package_root, args.authorization_file), ensure_ascii=False, indent=2)); return 0
    print(json.dumps(ejecutar(args.package_root, args.authorization_file), ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
