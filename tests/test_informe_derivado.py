#!/usr/bin/env python3
"""T-INFORME-DERIVADO -- toda cifra citada en el informe del programa vigente
(`canon/informe-programa-v*.md`, el más nuevo por versión semántica) trae un
comentario `<!-- comando: ... -->` en la misma sección, y ese comando se
re-ejecuta aquí contra el árbol real: si no corre (exit != 0) o no produce
salida, el test falla.

Mismo mecanismo y misma limitación declarada que `test_estado_derivado.py`
(ACTO GEN2-ESTADO-V16-1, 23/sep/2026): no compara el número citado contra la
salida del comando -- un parser por tipo de cifra (pp, conteo, IC, RESULT-*)
no lo mantendría ninguna sesión futura (D-14). Lo que atrapa: un comando que
cambió de nombre, una ruta que se movió, un archivo que se borró. Nace con
`ACTO GEN2-INFORME-V1-3-1`, 24/sep/2026: es la contraparte de
`informe-programa` del mismo patrón que `estado-programa` ya tenía.

Uso:
    python3 tests/test_informe_derivado.py
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_MIN_COMANDOS = 20
_TIMEOUT_S = 120  # `corrida0.py status` por sí solo tarda ~75s (mismo aviso que estado)

_PATRON_COMANDO = re.compile(r"<!--\s*comando:\s*(.+?)\s*-->")


def newest_informe():
    """Mismo criterio que `newest_estado()` de test_estado_derivado.py: ordena
    por versión semántica extraída del nombre, no por string -- para que
    `v1_3` no ordene antes de `v1_10` como texto si algún día existe."""
    hits = glob.glob(os.path.join(ROOT, "canon", "informe-programa-v*.md"))
    hits = [h for h in hits if not os.path.basename(h).endswith("-ANEXO.md")]

    def _version_key(h):
        m = re.search(r"v(\d+)[._](\d+)", os.path.basename(h))
        version = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
        return (version, os.path.basename(h))

    hits.sort(key=_version_key)
    return hits[-1] if hits else None


def main():
    ruta = newest_informe()
    if not ruta:
        print("FAIL T-INFORME-DERIVADO: no se encontró `canon/informe-programa-v*.md`")
        return 1

    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    comandos = _PATRON_COMANDO.findall(texto)
    if len(comandos) < _MIN_COMANDOS:
        print(
            f"FAIL T-INFORME-DERIVADO: {len(comandos)} comentarios "
            f"`<!-- comando: ... -->` en {os.path.relpath(ruta, ROOT)} "
            f"(mínimo {_MIN_COMANDOS})"
        )
        return 1

    fallos = []
    for cmd in comandos:
        try:
            # `bash -o pipefail` -- mismo motivo que test_estado_derivado.py:
            # sin esto un pipe con el primer comando fallando en silencio no
            # propaga el error bajo `shell=True` simple.
            r = subprocess.run(
                ["bash", "-o", "pipefail", "-c", cmd], cwd=ROOT,
                capture_output=True, text=True, timeout=_TIMEOUT_S,
            )
        except Exception as exc:
            fallos.append((cmd, f"excepción: {type(exc).__name__}: {exc}"))
            continue
        if r.returncode != 0:
            fallos.append((cmd, f"exit {r.returncode}: {r.stderr.strip()[:200]}"))
        elif not r.stdout.strip():
            fallos.append((cmd, "salida vacía"))

    if fallos:
        print(
            f"FAIL T-INFORME-DERIVADO: {len(fallos)}/{len(comandos)} comandos "
            f"citados en {os.path.relpath(ruta, ROOT)} no reprodujeron:"
        )
        for cmd, why in fallos:
            print(f"  - `{cmd}` -> {why}")
        return 1

    print(
        f"OK T-INFORME-DERIVADO: {len(comandos)} comandos citados en "
        f"{os.path.relpath(ruta, ROOT)} reprodujeron sin error."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
