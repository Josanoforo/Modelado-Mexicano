#!/usr/bin/env python3
"""audita_leido_pendientes_4.py -- ACTO GEN2-PENDIENTES-4, P2: para cada premisa [LEÍDO] de un encargo abre las
líneas citadas (`ruta:línea[-línea]`) y comprueba que cada «cita» textual de 14 o más caracteres aparezca ahí
(sin distinguir espacios ni mayúsculas). Sale con código 1 si alguna cita no aparece.

Defecto real que atrapa (ya ocurrido en este acto): premisas [LEÍDO] con la cita parafraseada, con la línea
corrida o apuntando a una fila que ya no existe; el verbo de funcionamiento sobre una lectura falsa es lo que la
regla §0 prohíbe. No prueba que la premisa sea cierta: sólo que la cita está donde el encargo dice que está.

    python3 forense/analisis/pendientes-4/audita_leido_pendientes_4.py forense/encargos/cola/PROPUESTOS/2026-09-29-*.md
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
RE_TOKEN = re.compile(r"`([^`\s]+\.(?:md|py|tsv|yaml|yml|json|txt))((?::\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)?)`"
                      r"|`(:\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)`")


def norm(s):
    """Sin espacios repetidos, sin mayúsculas y sin el énfasis de markdown (`**`, `_`, comillas de código): una cita
    que omite el énfasis de la fuente es la misma cita."""
    s = re.sub(r"[*`]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def audita(ruta):
    """Devuelve (n_leido, n_sin_discrepancia, hallazgos[str])."""
    lineas = open(ruta, encoding="utf-8").read().split("\n")
    rotulo = os.path.basename(ruta)
    n = ok = 0
    hallazgos = []
    for i, l in enumerate(lineas, 1):
        if not re.match(r"^\s*-\s*\[LEÍDO\]", l):
            continue
        n += 1
        toks = []
        for path, rng, suelto in RE_TOKEN.findall(l):
            if path:
                toks.append((path, rng))
            elif toks:  # `:284` suelto: hereda la última ruta de la línea
                toks.append((toks[-1][0], suelto))
        citas = re.findall(r"«([^»]{14,})»", l)
        if not toks:
            hallazgos.append(f"{rotulo} L{i}: SIN-RUTA :: {l[:170]}")
            continue
        cuerpo = []
        for path, rng in toks:
            fp = os.path.join(RAIZ, path)
            if not os.path.exists(fp):
                cuerpo.append(f"[NO EXISTE {path}]")
                continue
            fuente = [re.sub(r"^\s*#+\s?", "", x) for x in
                      open(fp, encoding="utf-8", errors="replace").read().split("\n")]
            if rng:
                for parte in rng.lstrip(":").split(","):
                    a, _, b = parte.partition("-")
                    a = int(a)
                    b = int(b) if b else a
                    cuerpo.append(" ".join(fuente[max(0, a - 1):b]))
            else:
                cuerpo.append(" ".join(fuente))
        pajar = norm(" ".join(cuerpo))
        faltan = []
        for q in citas:
            for trozo in re.split(r"…|\.\.\.", q):
                trozo = norm(trozo).strip(" .,;:()«»")
                if len(trozo) >= 14 and trozo not in pajar:
                    faltan.append(trozo[:70])
        if faltan:
            hallazgos.append(f"{rotulo} L{i}: CITA-NO-HALLADA {faltan[:2]} :: {[a + b for a, b in toks][:3]}")
        else:
            ok += 1
    return n, ok, hallazgos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = sin = 0
    todos = []
    for ruta in sys.argv[1:]:
        n, ok, h = audita(ruta)
        total += n
        sin += ok
        todos += h
        print(f"{os.path.basename(ruta)}: {n} [LEÍDO] · {ok} sin discrepancia mecánica")
    for h in todos:
        print(h)
    print(f"TOTAL: {len(sys.argv) - 1} archivos · {total} [LEÍDO] · {sin} sin discrepancia · {len(todos)} con hallazgo")
    return 1 if todos else 0


if __name__ == "__main__":
    sys.exit(main())
