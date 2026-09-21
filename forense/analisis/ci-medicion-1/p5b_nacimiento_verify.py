#!/usr/bin/env python3
"""P5 (insumo) · para cada paso (`- name:`) de .github/workflows/verify.yml,
extrae el job al que pertenece y el bloque de comentarios `#` inmediatamente
anterior (el "nacimiento" citado en el propio workflow). Mecánico.
"""
import re

SRC = ".github/workflows/verify.yml"
with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

job_re = re.compile(r"^  ([a-z][a-z0-9_-]*):\s*$")
step_re = re.compile(r"^      - name: (.+)$")

rows = []
current_job = None
i = 0
while i < len(lines):
    l = lines[i]
    mj = job_re.match(l)
    if mj and l.startswith("  ") and not l.startswith("    "):
        current_job = mj.group(1)
    ms = step_re.match(l)
    if ms:
        nombre = ms.group(1)
        # los comentarios de cada paso van DESPUES de "- name:" y ANTES de "run:"
        j = i + 1
        com = []
        while j < len(lines) and lines[j].strip().startswith("#"):
            com.append(lines[j].strip())
            j += 1
        bloque = " ".join(com)
        citas = re.findall(
            r"(ACTO [A-Z0-9Ñ][A-Z0-9\-Ñ]*(?:\s*·\s*[A-Z0-9\-]+)?|NC-[0-9]{4,}|FP-[0-9]{3,}|PR ?#[0-9]+|ADR-[0-9]+)",
            bloque,
        )
        rows.append((current_job, nombre, i + 1, "; ".join(sorted(set(citas))), bloque[:500]))
    i += 1

with open("nacimiento-verify-steps.tsv", "w", encoding="utf-8") as f:
    f.write("job\tpaso\tlinea\tcitas\tcomentario\n")
    for job, nombre, ln, citas, com in rows:
        f.write(f"{job}\t{nombre}\t{ln}\t{citas}\t{com}\n")

print(f"{len(rows)} pasos extraidos -> nacimiento-verify-steps.tsv")
