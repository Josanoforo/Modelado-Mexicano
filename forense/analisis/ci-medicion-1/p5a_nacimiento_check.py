#!/usr/bin/env python3
"""P5 (insumo) · extrae, para cada test registrado en tests/check.py::main(),
el bloque de comentarios inmediatamente anterior a su `def` (el "nacimiento":
ACTO/NC/PR/ADR que lo motivó) y su docstring. Puramente mecánico -- no
juzga mantener/abaratar/eliminar, eso lo hace el informe.
"""
import re

SRC = "tests/check.py"

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

# localizar la lista de tests registrados en main()
main_start = next(i for i, l in enumerate(lines) if l.startswith("def main():"))
main_end = next(i for i, l in enumerate(lines) if l.startswith("if __name__"))
main_body = "".join(lines[main_start:main_end])

registrados = re.findall(r'\("([^"]+)",\s*\n?\s*(t[0-9a-z_]+)\)', main_body)
# T16 va aparte (append condicional)
m16 = re.search(r'tests\.append\(\("([^"]+)",\s*(\w+)\)\)', main_body)
if m16:
    registrados.append((m16.group(1), m16.group(2)))

print(f"# {len(registrados)} tests registrados")

def_line = {}
for i, l in enumerate(lines):
    mm = re.match(r"^def (t[0-9a-z_]+)\(", l)
    if mm:
        def_line[mm.group(1)] = i

out = []
for label, fn in registrados:
    if fn not in def_line:
        out.append((label, fn, -1, "FUNCION-NO-ENCONTRADA", ""))
        continue
    idx = def_line[fn]
    # subir hasta encontrar una línea en blanco no-comentario o el tope
    start = idx
    while start > 0 and (lines[start - 1].startswith("#") or lines[start - 1].strip() == ""):
        start -= 1
        if start > 0 and lines[start - 1].strip() == "" and not lines[start].startswith("#"):
            break
    bloque_comentario = "".join(lines[start:idx]).strip()
    # docstring (primeras líneas tras el def)
    doc_lines = []
    j = idx + 1
    if j < len(lines) and '"""' in lines[j]:
        doc_lines.append(lines[j])
        if lines[j].count('"""') < 2:
            j += 1
            while j < len(lines) and '"""' not in lines[j]:
                doc_lines.append(lines[j])
                j += 1
            if j < len(lines):
                doc_lines.append(lines[j])
    docstring = "".join(doc_lines).strip()
    citas = re.findall(
        r"(ACTO [A-Z0-9Ñ][A-Z0-9\-Ñ]*(?:\s*·\s*[A-Z0-9\-]+)?|NC-[0-9]{4,}|FP-[0-9]{3,}|PR ?#[0-9]+|ADR-[0-9]+)",
        bloque_comentario + " " + docstring,
    )
    out.append((label, fn, idx + 1, bloque_comentario[:600], "; ".join(sorted(set(citas)))))

with open("nacimiento-check-tests.tsv", "w", encoding="utf-8") as f:
    f.write("label\tfuncion\tlinea\tcitas\tcomentario\n")
    for label, fn, ln, com, citas in out:
        com_flat = com.replace("\t", " ").replace("\n", " | ")
        f.write(f"{label}\t{fn}\t{ln}\t{citas}\t{com_flat}\n")

print("Escrito nacimiento-check-tests.tsv")
