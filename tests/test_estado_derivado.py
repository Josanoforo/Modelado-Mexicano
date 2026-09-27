#!/usr/bin/env python3
"""T-ESTADO-DERIVADO -- toda cifra citada en el estado del programa vigente
(`canon/estado-programa-v*.md`, el más nuevo por versión semántica) trae un
comentario `<!-- comando: ... -->` en la misma sección, y ese comando se
re-ejecuta aquí contra el árbol real: si no corre (exit != 0) o no produce
salida, el test falla.

No compara el número citado contra la salida del comando -- eso exigiría un
parser por tipo de cifra que ninguna sesión futura mantendría vivo (D-14).
Lo que sí atrapa: un comando que cambió de nombre, una ruta que se movió, un
tool que se borró -- la clase de cifra "tecleada y nunca vuelta a correr"
que la Regla de Procedencia (§2) prohíbe. Nace con `ACTO GEN2-ESTADO-V16-1`,
23/sep/2026: v1.15 (#1006) sólo dejó una tabla `afirmación → comando` en
prosa, sin verificación automática; ninguna sesión anterior la re-corrió.

Uso:
    python3 tests/test_estado_derivado.py
"""
import glob
import os
import re
import subprocess
import tempfile
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# GEN2-FRONT-3-PORTADA-1: un comando sellado cuyo contenido salió de la portada
# se corre resuelto por archivo/INDICE.md (§Comandos reubicados); el texto sellado no se edita.
sys.path.insert(0, os.path.join(ROOT, "tools"))
import resuelve_cita  # noqa: E402

_MIN_COMANDOS = 10
_TIMEOUT_S = 120  # `corrida0.py status` por sí solo tarda ~75s (medido 23/sep/2026)

_PATRON_COMANDO = re.compile(r"<!--\s*comando:\s*(.+?)\s*-->")


def newest_estado():
    """Mismo criterio que `newest()` de tests/check.py: ordena por versión
    semántica extraída del nombre (v<major>[._]<minor>), no por string --
    para que `v1_16` no ordene antes de `v1_9` como texto."""
    hits = glob.glob(os.path.join(ROOT, "canon", "estado-programa-v*.md"))

    def _version_key(h):
        m = re.search(r"v(\d+)[._](\d+)", os.path.basename(h))
        version = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
        return (version, os.path.basename(h))

    hits.sort(key=_version_key)
    return hits[-1] if hits else None


def main():
    ruta = newest_estado()
    if not ruta:
        print("FAIL T-ESTADO-DERIVADO: no se encontró `canon/estado-programa-v*.md`")
        return 1

    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    comandos = _PATRON_COMANDO.findall(texto)
    if len(comandos) < _MIN_COMANDOS:
        print(
            f"FAIL T-ESTADO-DERIVADO: {len(comandos)} comentarios "
            f"`<!-- comando: ... -->` en {os.path.relpath(ruta, ROOT)} "
            f"(mínimo {_MIN_COMANDOS})"
        )
        return 1

    fallos = []
    # `corrida0.py status` tarda ~227s desde el 26/sep (202 900 resultados): se corre UNA vez
    # y cada comando la lee de un archivo (GEN2-CIERRE-SEMANAL-1, defecto adyacente D-21).
    cache = os.path.join(tempfile.mkdtemp(), "status.txt")
    if any("tools/corrida0.py status" in c for c in comandos):
        subprocess.run(f"python3 tools/corrida0.py status > {cache}", shell=True, cwd=ROOT, check=True)
    for cmd in comandos:
        cmd = re.sub(r"python3 tools/corrida0\.py status(?=\s*(\||$))", f"cat {cache}", cmd)
        try:
            # `bash -o pipefail` -- sin esto, `sh` (el shell de `shell=True`
            # en Linux) toma el exit code del ULTIMO comando de un pipe: un
            # `git log <ref-inexistente> | grep -c X` con `<ref-inexistente>`
            # fallando en silencio da exit 0 (o 1 por "0 matches", cita
            # aparte) en vez de propagar el fallo real -- descubierto en CI
            # (GEN2-ESTADO-V16-1, 24/sep/2026): el checkout de `guardias`
            # sólo trae `refs/remotes/origin/ci`, nunca `origin/main`, y
            # `git log ... origin/main | wc -l` reportaba "0" en vez de
            # fallar.
            r = subprocess.run(
                ["bash", "-o", "pipefail", "-c", resuelve_cita.comando(cmd)], cwd=ROOT,
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
            f"FAIL T-ESTADO-DERIVADO: {len(fallos)}/{len(comandos)} comandos "
            f"citados en {os.path.relpath(ruta, ROOT)} no reprodujeron:"
        )
        for cmd, why in fallos:
            print(f"  - `{cmd}` -> {why}")
        return 1

    print(
        f"OK T-ESTADO-DERIVADO: {len(comandos)} comandos citados en "
        f"{os.path.relpath(ruta, ROOT)} reprodujeron sin error."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
