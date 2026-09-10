#!/usr/bin/env python3
"""Planifica y ejecuta las 224 capturas prospectivas de F5 completa."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
SPEC_L = DIR / "L-spec-v1_4.json"
SPEC_ESTUDIO = DIR / "F5-completa-spec-v1_0.md"
MANIFIESTO_CORPUS = DIR / "paquete-corpus-F5-v2_0/manifiesto.json"
PLAN = DIR / "F5-completa-plan-v1_0.json"
SALIDAS = DIR / "corridas-L-completa-v1_0"
ENSAMBLADOR = ROOT / "tools/construye_corpus_f5_v2.py"

MODELO_ALIAS = "opus"
VERSION_CAPTURA = "f5-completa-v1_0"
SISTEMA = "Responde únicamente a la pregunta. No uses herramientas ni consultes fuentes fuera del contexto entregado."
FORMATO = """\n\nContrato de salida: razona brevemente si lo necesitas, pero termina con EXACTAMENTE una de estas dos líneas y nada después:\nESTIMACION_PUNTUAL=<número entre 0 y 100>%\nABSTENCION\nNo conviertas una cifra de contexto en la estimación solicitada."""
VARIANTES = ("L-solo", "L+corpus")
K = 8
SEMILLA = 42
MAX_REINTENTOS = 2
TIMEOUT = 300


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_archivo(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def cargar_ensamblador():
    spec = importlib.util.spec_from_file_location("corpus_f5_v2", ENSAMBLADOR)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(modulo)
    return modulo


def version_cliente() -> str:
    p = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True, timeout=15)
    return p.stdout.strip() or p.stderr.strip()


def comando() -> list[str]:
    return ["claude", "-p", "--model", MODELO_ALIAS, "--output-format", "json",
            "--system-prompt", SISTEMA, "--tools", "", "--max-turns", "1"]


def construir_posiciones(cliente: str) -> list[dict]:
    datos_l = json.loads(SPEC_L.read_text(encoding="utf-8"))
    manifiesto = json.loads(MANIFIESTO_CORPUS.read_text(encoding="utf-8"))
    ensamblador = cargar_ensamblador()
    posiciones = []
    for celda in datos_l["celdas"]:
        cid = celda["id"]
        entrada = manifiesto["celdas"][cid]
        contexto = ensamblador.contexto_desde_entrada(entrada)
        if sha_bytes(contexto.encode()) != entrada["sha256_contenido_entregado"]:
            raise RuntimeError(f"paquete alterado: {cid}")
        for variante in VARIANTES:
            bloque = "" if variante == "L-solo" else "\n\n## Contexto documental autorizado\n" + contexto
            prompt = celda["pregunta_L"] + bloque + FORMATO
            prompt_sha = sha_bytes(prompt.encode())
            for replica in range(1, K + 1):
                nombre = f"L-{cid}-M__{variante}__{replica:02d}__{VERSION_CAPTURA}.json"
                identidad_base = {
                    "id_celda": cid,
                    "variante": variante,
                    "replica": replica,
                    "cliente_version": cliente,
                    "modelo_alias_solicitado": MODELO_ALIAS,
                    "sha256_prompt": prompt_sha,
                    "sha256_spec_l": sha_archivo(SPEC_L),
                    "sha256_spec_estudio": sha_archivo(SPEC_ESTUDIO),
                    "sha256_manifiesto_corpus": sha_archivo(MANIFIESTO_CORPUS),
                    "sha256_paquete": None if variante == "L-solo" else entrada["sha256_contenido_entregado"],
                }
                identidad = sha_bytes(json.dumps(identidad_base, sort_keys=True).encode())
                posiciones.append({**identidad_base, "identidad": identidad, "ruta": str((SALIDAS / nombre).relative_to(ROOT)), "prompt": prompt})
    random.Random(SEMILLA).shuffle(posiciones)
    return posiciones


def plan_publico(posiciones: list[dict], cliente: str) -> dict:
    return {
        "acto": "GEN2-F5-COMPLETA", "version": VERSION_CAPTURA,
        "fecha_congelacion": "2026-09-10", "cliente_version": cliente,
        "modelo_alias_solicitado": MODELO_ALIAS, "modelo_real": "se registra por captura si el CLI lo reporta",
        "n_posiciones": len(posiciones), "n_celdas": 14, "variantes": list(VARIANTES), "k": K,
        "semilla_orden": SEMILLA, "max_reintentos_tecnicos": MAX_REINTENTOS,
        "sha256_spec_l": sha_archivo(SPEC_L), "sha256_spec_estudio": sha_archivo(SPEC_ESTUDIO),
        "sha256_manifiesto_corpus": sha_archivo(MANIFIESTO_CORPUS),
        "posiciones": [{k: v for k, v in p.items() if k != "prompt"} for p in posiciones],
    }


def congelar_plan() -> int:
    cliente = version_cliente()
    posiciones = construir_posiciones(cliente)
    if len(posiciones) != 224 or len({p["ruta"] for p in posiciones}) != 224 or len({p["identidad"] for p in posiciones}) != 224:
        raise RuntimeError("plan no contiene 224 posiciones únicas")
    PLAN.write_text(json.dumps(plan_publico(posiciones, cliente), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK: 224 posiciones únicas; cliente={cliente}; plan={PLAN.relative_to(ROOT)}")
    return 0


def verificar_plan() -> int:
    fijado = json.loads(PLAN.read_text(encoding="utf-8"))
    cliente = version_cliente()
    actual = plan_publico(construir_posiciones(cliente), cliente)
    if fijado != actual:
        raise RuntimeError("el plan congelado no coincide con cliente/spec/corpus actuales")
    print("OK: plan congelado reproduce 224 posiciones únicas y sus identidades")
    return 0


def invocar(prompt: str) -> tuple[dict | None, list[dict]]:
    intentos = []
    for numero in range(1, MAX_REINTENTOS + 2):
        inicio = datetime.now(timezone.utc).isoformat()
        try:
            p = subprocess.run(comando(), input=prompt, capture_output=True, text=True, timeout=TIMEOUT)
            intento = {"numero": numero, "inicio_utc": inicio, "fin_utc": datetime.now(timezone.utc).isoformat(),
                       "returncode": p.returncode, "stdout_original": p.stdout, "stderr_original": p.stderr}
            intentos.append(intento)
            if p.returncode != 0:
                continue
            try:
                return json.loads(p.stdout), intentos
            except json.JSONDecodeError:
                continue
        except subprocess.TimeoutExpired as exc:
            intentos.append({"numero": numero, "inicio_utc": inicio, "fin_utc": datetime.now(timezone.utc).isoformat(),
                             "error": "TimeoutExpired", "stdout_original": exc.stdout, "stderr_original": exc.stderr})
    return None, intentos


def ejecutar() -> int:
    verificar_plan()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    cliente = plan["cliente_version"]
    prompts = {p["identidad"]: p["prompt"] for p in construir_posiciones(cliente)}
    hechas = reanudadas = errores = 0
    for pos in plan["posiciones"]:
        ruta = ROOT / pos["ruta"]
        if ruta.exists():
            previo = json.loads(ruta.read_text(encoding="utf-8"))
            if previo.get("identidad") != pos["identidad"]:
                raise RuntimeError(f"colisión de reanudación: {ruta}")
            reanudadas += 1
            continue
        sobre, intentos = invocar(prompts[pos["identidad"]])
        texto = sobre.get("result") if isinstance(sobre, dict) else None
        modelos_uso = sorted((sobre.get("modelUsage") or {}).keys()) if isinstance(sobre, dict) and isinstance(sobre.get("modelUsage"), dict) else []
        registro = {
            **{k: v for k, v in pos.items() if k != "ruta"},
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "estado_captura": "OK" if sobre is not None else "ERROR_TECNICO",
            "texto_crudo": texto,
            "modelo_reportado": sobre.get("model") if isinstance(sobre, dict) else None,
            "modelos_en_uso_reportados": modelos_uso,
            "sobre_cli_original": sobre,
            "intentos": intentos,
        }
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if sobre is None:
            errores += 1
            # autenticación/cuota sistémica: no quemar el resto del lote
            ult = json.dumps(intentos[-1], ensure_ascii=False).lower()
            if any(x in ult for x in ("auth", "quota", "rate limit", "credit", "login")):
                print(f"PARO sistémico tras {ruta.name}")
                break
        else:
            hechas += 1
        print(f"{hechas+errores+reanudadas}/224 {ruta.name} {registro['estado_captura']}", flush=True)
    print(f"nuevas_ok={hechas} errores={errores} reanudadas={reanudadas}")
    return 0


def sonda_transporte() -> int:
    cliente = version_cliente()
    posiciones = construir_posiciones(cliente)
    mayor = max((p for p in posiciones if p["variante"] == "L+corpus"), key=lambda x: len(x["prompt"]))
    marcador = "\n\nSONDA DE TRANSPORTE, NO ES REPLICA: ignora la pregunta y responde solamente TRANSPORTE_OK."
    sobre, intentos = invocar(mayor["prompt"] + marcador)
    texto = sobre.get("result", "") if sobre else ""
    if "TRANSPORTE_OK" not in texto:
        raise RuntimeError(f"sonda no aceptada tras {len(intentos)} intentos")
    print(f"OK: paquete máximo aceptado ({len(mayor['prompt'])} chars); sonda no registrada como réplica")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--congelar-plan", action="store_true")
    g.add_argument("--verificar-plan", action="store_true")
    g.add_argument("--sonda-transporte", action="store_true")
    g.add_argument("--correr", action="store_true")
    args = ap.parse_args()
    if args.congelar_plan: return congelar_plan()
    if args.verificar_plan: return verificar_plan()
    if args.sonda_transporte: return sonda_transporte()
    return ejecutar()


if __name__ == "__main__":
    raise SystemExit(main())
