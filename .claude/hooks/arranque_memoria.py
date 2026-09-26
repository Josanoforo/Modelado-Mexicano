#!/usr/bin/env python3
"""SessionStart: imprime la memoria operativa y el status recortado.

ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1, P3. Corre DESPUÉS de
`tools/entorno.py --arranque` (que no se toca). Imprime las primeras 15
líneas de canon/MEMORIA-OPERATIVA.md y las primeras 12 de
`corrida0.py status` con tope de TOPE s: status tardó > 60 s en nube
(medido al abrir este acto), así que si no termina a tiempo se dice y se
deja el comando; nunca bloquea el arranque.
"""
import os
import subprocess
import sys

TOPE = 8
raiz = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
mem = os.path.join(raiz, "canon", "MEMORIA-OPERATIVA.md")
print("== MEMORIA OPERATIVA (15 primeras líneas; completa importada por CLAUDE.md) ==")
try:
    with open(mem, encoding="utf-8") as f:
        for i, linea in enumerate(f):
            if i >= 15:
                break
            print(linea.rstrip("\n")[:200])
except OSError:
    print("memoria-operativa: AUSENTE (%s)" % mem)
print("== corrida0.py status (recortado a 12 líneas, tope %d s) ==" % TOPE)
try:
    r = subprocess.run(
        [sys.executable, os.path.join(raiz, "tools", "corrida0.py"), "status"],
        cwd=raiz, capture_output=True, text=True, timeout=TOPE,
    )
    for linea in (r.stdout or r.stderr).splitlines()[:12]:
        print(linea[:200])
except subprocess.TimeoutExpired:
    print("status: NO-TERMINÓ en %d s (no es PARO); córrelo a mano si lo necesitas: "
          "python3 tools/corrida0.py status | head -n 30" % TOPE)
except OSError as e:
    print("status: NO-EJECUTABLE (%s)" % e)
