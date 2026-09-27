#!/usr/bin/env python3
"""Integra las tres piezas; deriva conteos de decisiones y comprueba regeneración.
Protege el defecto material de contar juicios heredados como decisiones nuevas
(#1173) dejando a productores por pieza el control de evidencia y denominador.
No dicta juicios editoriales ni cuenta dígitos como afirmaciones cuantitativas.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PIEZAS = ("trabajo", "movilidad", "clase")

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def records(path):
    data = read(path)
    if isinstance(data, list):
        return data
    for key in ("afirmaciones", "decisiones", "filas", "registros"):
        if isinstance(data.get(key), list):
            return data[key]
    raise ValueError(f"No hay tabla de decisiones explícitas en {path}")

def resolve(path):
    candidate = (ROOT / path).resolve()
    if not candidate.is_relative_to(ROOT):
        raise ValueError("Ruta fuera del repositorio")
    return candidate

def inventory(summaries):
    paths = set(HERE.glob("*/*")) | {p for p in HERE.glob("*") if p.name not in ("entrega.json", "indice-local.md")}
    paths = {p for p in paths if p.is_file() and p.suffix in (".md", ".json", ".tsv", ".py", ".txt")}
    for summary in summaries:
        paths.add(resolve(summary["report"]))
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths)}

def products(summaries):
    rows=[]
    for summary in summaries:
        decisions = records(resolve(summary["decisiones"]))
        counts = Counter(row.get("dictamen", row.get("veredicto", "")) for row in decisions)
        valid={"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
        if set(counts) - valid:
            raise ValueError(f"Dictamen inválido: {counts}")
        if not decisions:
            raise ValueError("Pieza sin decisiones")
        row={"pieza":summary["pieza"], "report":summary["report"], "tabla":summary["decisiones"],
             "registros_editoriales":len(decisions), "dictamenes":dict(sorted(counts.items()))}
        rows.append(row)
    output={"corte_editorial":"1eeb855272b933642177e3f32d51adc89f1009a0",
            "unidad_conteo":"registros editoriales; no tesis únicas ni pruebas independientes",
            "piezas":rows, "objetos_sha256":inventory(summaries),
            "revision_humana":"SOLICITADA; no obtenida por este ejecutor",
            "recibo_independiente":"SOLICITADO por circuito PR; no concedido"}
    json_text=json.dumps(output,ensure_ascii=False,indent=2)+"\n"
    lines=["# Índice local · trabajo, movilidad y clase media", "",
           "Conteos derivados de decisiones explícitas. Los registros de procedencia pueden solaparse: no son tesis únicas ni observaciones independientes.", "",
           "| Pieza | Registros | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA |", "|---|---:|---:|---:|---:|---:|"]
    for row in rows:
        c=row["dictamenes"]
        lines.append(f"| [{row['pieza']}]({'../../../../'+row['report']}) | {row['registros_editoriales']} | {c.get('CONFIRMA',0)} | {c.get('MATIZA',0)} | {c.get('ROMPE',0)} | {c.get('SIN-CIFRA',0)} |")
    lines += ["", "Cada pieza tiene fuente editorial, tabla razonada, trazas cuantitativas y verificador propio. Las ROMPE no se infieren de ausencia de evidencia. La adopción se verifica por firma; los pisos ENOE/MMSI nuevos se rotulan provisionales.", "", "[Revisión humana solicitada](revision-para-mesa.md) · [Recibo solicitado](recibo-para-claude.md) · [Verificación y hashes](entrega.json)", "", "Comando: `python3 forense/analisis/reports-v2/trabajo-movilidad-1/verifica_lote.py --regenera --autoprueba`. Sin banderas comprueba productos y respaldo sin escribir.", "", "Sin medición nueva, adopción, apertura de microdato ni eficacia predictiva atribuida. La exposición incidental al reporte público reservado ENIGH 2024 está declarada y excluida de evidencia; mesa adjudica su efecto.", ""]
    return {HERE/"entrega.json":json_text, HERE/"indice-local.md":"\n".join(lines)}

def check_reserved_sources():
    # Defecto observado en este lote: un comunicado ENIGH2024 fue usado
    # como si ser público levantara la reserva. Sólo se conserva testimonio.
    for name in PIEZAS:
        data = read(HERE/name/"fuentes.json")
        rows = data if isinstance(data, list) else list(data.values())
        for row in rows:
            if "enigh2024" in str(row.get("url", "")).lower():
                if row.get("estado") != "EXCLUIDA-RESERVA":
                    raise ValueError(f"Fuente reservada activa en {name}: {row.get('id')}")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regenera", action="store_true")
    parser.add_argument("--autoprueba", action="store_true")
    args=parser.parse_args()
    summaries=[]
    check_reserved_sources()
    for name in PIEZAS:
        summary=read(HERE/name/"resumen.json")
        assert summary["pieza"]==name
        summaries.append(summary)
        if args.regenera:
            before=inventory([summary])
            subprocess.run(summary["comando_producir"],cwd=ROOT,check=True)
            after=inventory([summary])
            if before != after:
                raise ValueError(f"Regeneración cambió productos de {name}; revisar y volver a verificar")
        command=list(summary["comando_verificar"])
        if args.autoprueba and not any(flag in command for flag in ("--autoprueba", "--self-test")):
            command.append("--autoprueba")
        subprocess.run(command,cwd=ROOT,check=True)
    outputs=products(summaries)
    for path, expected in outputs.items():
        if args.regenera:
            path.write_text(expected,encoding="utf-8")
        elif not path.exists() or path.read_text(encoding="utf-8")!=expected:
            raise ValueError(f"Producto local desactualizado: {path}")
    print(json.dumps({"estado":"VERDE", "piezas":len(summaries), "conteos":read(HERE/"entrega.json")["piezas"]},ensure_ascii=False))

if __name__=="__main__":
    try:
        main()
    except (ValueError, AssertionError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}",file=sys.stderr)
        sys.exit(1)
