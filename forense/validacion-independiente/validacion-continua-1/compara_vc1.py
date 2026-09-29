#!/usr/bin/env python3
"""ACTO GEN2-VALIDACION-Y-2027-1 · P1 · de la salida archivada a la comparación, en este orden y
sin volver atrás (receta de C1-LOTE-3 / C1-SUCESORES):

  1. auditoría del transcript (CERO-LECTURAS-FUERA · SIN-RED · CAMPOS-DENTRO · SOLO-OPUS); la misma
     regla de `catalogo-1-lote3/audita_residuales.py`, con los campos de `<paq>--allowlist.json`;
  2. export = salida archivada (nombres originales, desde `<paq>--mapa-nombres.tsv`) + export-manifest;
  3. `runtime.py freeze-export` (ancla fuera del export) y `compare_v3 freeze` → sha congelado;
  4. SOLO ENTONCES se abre el sellado: referencia v3 desde data/corrida0/<CALC>/resultados.json
     (punto = <llave>; IC = <base>-IC-LO/-IC-HI si ambos existen; si no, SIN-IC);
  5. `compare_v3 compare` → `<paq>--comparacion.json`.
Uso: compara.py <REC> <paq> [<paq> ...]
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

R = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
V3 = R / "tools/validacion/astra6_ejecutor_v3"
TOL = R / "forense/validacion-independiente/catalogo-1-lote3/endireh-pisos-2016-pareja-fisica-0002/entrada/tolerancia-v2.json"
PERMITIDAS = ("/usr/", "/bin/", "/lib", "/etc/os-release", "/dev/null", "/proc/self", "/proc/version",
              "/dev/stdout", "/dev/stderr", "/proc/cpuinfo", "/proc/meminfo")
RED = re.compile(r"\b(curl|wget|pip3?|git|ssh|scp|nc|telnet|ftp)\b|urllib|requests|socket|http\.client")
RUTA = re.compile(r"(?<![\w.])(/[A-Za-z0-9_.@%+~-][A-Za-z0-9_./@%+~-]*)")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def audita(paq, allow, transcript, cwd, codigo_dir):
    aut = {c for cs in allow["campos_autorizados"].values() for c in cs}
    ev = [json.loads(l) for l in open(transcript, encoding="utf-8") if l.strip()]
    init = next((e for e in ev if e.get("type") == "system" and e.get("subtype") == "init"), {})
    res = next((e for e in reversed(ev) if e.get("type") == "result"), {})
    fuera, red, n = [], [], 0
    for e in ev:
        if e.get("type") != "assistant":
            continue
        for c in e["message"].get("content", []):
            if c.get("type") != "tool_use":
                continue
            n += 1
            arg = c["input"]
            textos = [arg.get("command", "")] if c["name"] == "Bash" else [str(arg[k]) for k in ("file_path", "path") if k in arg]
            if c["name"] == "Bash" and RED.search(arg.get("command", "")):
                red.append(arg["command"][:300])
            for t in textos:
                for r in RUTA.findall(t):
                    r = r.rstrip(".,;:)'\"")
                    if not (r == cwd or r.startswith(cwd + "/") or any(r.startswith(p) for p in PERMITIDAS)):
                        fuera.append(r)
    # tokens de columna en el código: los que coinciden con una columna REAL de algún archivo del
    # paquete (encabezados que la receptora conoce por el allowlist de su configuración) y no están autorizados
    tokens = set()
    for py in Path(codigo_dir).glob("*.py"):
        tokens |= set(re.findall(r"['\"]([A-Za-z][A-Za-z0-9_]{1,20})['\"]", py.read_text(encoding="utf-8", errors="replace")))
    vocab = set(json.loads((AQUI / "vocabulario-columnas.json").read_text()).get(paq, []))
    no_aut = sorted(t for t in tokens if t in vocab and t not in aut)
    modelos = sorted((res.get("modelUsage") or {}).keys())
    inf = {"paquete": paq, "session_id": init.get("session_id"),
           "init": {k: init.get(k) for k in ("model", "tools", "mcp_servers", "permissionMode", "claude_code_version", "cwd")},
           "resultado": {k: res.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "total_cost_usd", "permission_denials")},
           "modelos": modelos, "llamadas": n, "rutas_fuera_del_cwd": sorted(set(fuera)), "comandos_con_red": red,
           "columnas_reales_no_autorizadas_en_codigo": no_aut}
    inf["veredicto"] = {"CERO-LECTURAS-FUERA": not fuera, "SIN-RED": not red, "CAMPOS-DENTRO": not no_aut,
                        "SOLO-OPUS": bool(modelos) and all("opus" in m for m in modelos)}
    return inf


def run(*a):
    p = subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f"PARO · {a[0]} {a[1]}: {p.stderr.strip()[-600:]}")
    return p.stdout.strip()


def referencia(allow, esquema, out):
    calc = allow["calc"]
    sell = json.loads((R / "data/corrida0" / calc / "resultados.json").read_text())
    sell = sell.get("resultados", sell)
    filas = []
    for r in csv.DictReader(open(esquema, encoding="utf-8"), delimiter="\t"):
        k = r["llave"]
        v = sell.get(k)
        if isinstance(v, dict):
            v = v.get("valor", v.get("punto"))
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise SystemExit(f"PARO · {k} ausente o no numérica en el sellado de {calc}")
        f = {"llave": k, "unidad": r["unidad"], "estado": "RECONSTRUIDO", "punto": repr(float(v))}
        base = k[:-2] if k.endswith("-P") else None
        lo, hi = (sell.get(f"{base}-IC-LO"), sell.get(f"{base}-IC-HI")) if base else (None, None)
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            f.update(estado_ic="CALCULADO", ic95_inf=repr(float(lo)), ic95_sup=repr(float(hi)))
        else:
            f["estado_ic"] = "SIN-IC"
        filas.append(f)
    Path(out).write_text(json.dumps({"version": 3, "identidad": allow["identidad"], "filas": filas},
                                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(filas)


def compara(REC, paq):
    d = AQUI / paq
    allow = json.loads((d / "entrada" / f"{paq}--allowlist.json").read_text())
    canon = (d / "entrada" / f"{paq}--allowlist.canon.sha256").read_text().strip()
    rec = d / "reconstructora"
    cmp_dir = d / "comparacion"
    if cmp_dir.exists():
        raise SystemExit(f"PARO · ya comparado {cmp_dir}")
    mapa = list(csv.DictReader(open(rec / f"{paq}--mapa-nombres.tsv", encoding="utf-8"), delimiter="\t"))
    # 1 · auditoría
    work = REC / f"cmp-{paq}"
    if work.exists():
        raise SystemExit(f"PARO · ya existe {work}")
    exp = work / "export"
    (exp / "codigo").mkdir(parents=True)
    for m in mapa:
        if m["estado"] in ("SELLADO", "FUERA-DEL-SELLO"):
            dst = exp / m["original"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(rec / m["archivado"], dst)
    inf = audita(paq, allow, rec / f"{paq}--transcript.jsonl", str(REC / paq), exp / "codigo")
    cmp_dir.mkdir()
    (cmp_dir / f"{paq}--auditoria.json").write_text(json.dumps(inf, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(paq, "auditoría", json.dumps(inf["veredicto"]))
    # 2 · export
    files = sorted(p for p in exp.rglob("*") if p.is_file())
    man = {"version": 1, "input_manifest_sha256": canon,
           "files": [{"path": str(p.relative_to(exp)), "sha256": sha(p), "bytes": p.stat().st_size} for p in files]}
    (exp / "export-manifest.json").write_text(json.dumps(man, sort_keys=True, separators=(",", ":")) + "\n")
    # 3 · anclas y congelación, antes de abrir el sellado
    ancla = work / "ancla-exportacion.json"
    ident = work / "identidad.json"
    ident.write_text(json.dumps(allow["identidad"], sort_keys=True))
    run(V3 / "runtime.py", "freeze-export", "--export", exp, "--anchor", ancla, "--identity", ident,
        "--input-manifest-sha256", canon)
    frozen = work / "congelado"
    out = run(V3 / "compare_v3.py", "freeze", "--export", exp, "--export-anchor", ancla, "--tolerance", TOL, "--output", frozen)
    fsha = re.findall(r"[0-9a-f]{64}", out)[-1]
    (cmp_dir / f"{paq}--congelacion.sha256").write_text(fsha + "\n")
    shutil.copyfile(ancla, cmp_dir / f"{paq}--ancla-exportacion.json")
    with tarfile.open(cmp_dir / f"{paq}--congelado.tar.gz", "w:gz") as t:
        t.add(frozen, arcname="congelado")
    # 4 · sólo ahora: referencia desde el sellado
    ref = work / "referencia.json"
    n = referencia(allow, REC / paq / "paquete/esquema-identidades.tsv", ref)
    rsha = sha(ref)
    shutil.copyfile(ref, cmp_dir / f"{paq}--referencia.json")
    (cmp_dir / f"{paq}--referencia.sha256").write_text(rsha + "\n")
    # 5 · comparación
    comp = work / "comparacion.json"
    run(V3 / "compare_v3.py", "compare", "--frozen", frozen, "--expected-sha256", fsha, "--reference", ref,
        "--reference-sha256", rsha, "--output", comp)
    shutil.copyfile(comp, cmp_dir / f"{paq}--comparacion.json")
    c = json.loads(comp.read_text())
    est = {}
    for r in c.get("resultados", []):
        est[r["estado"]] = est.get(r["estado"], 0) + 1
    print(paq, n, "llaves · comparador", est)


if __name__ == "__main__":
    REC = Path(sys.argv[1])
    for paq in sys.argv[2:]:
        compara(REC, paq)
