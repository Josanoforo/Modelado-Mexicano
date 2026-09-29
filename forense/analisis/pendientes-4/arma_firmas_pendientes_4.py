#!/usr/bin/env python3
"""arma_firmas_pendientes_4.py -- ACTO GEN2-PENDIENTES-4: apéndice a `forense/firmas-pendientes.tsv` (A.12).

Dos filas FIRMADA (las autorizaciones de ADENDA-1 y la delegación con A.14 que PENDIENTES-3 no asentó) y una fila
ABIERTA por cada renglón de `hoja-decisiones-pendientes-4.md` que NO tiene ya una FP («FP existente»).
Escribe POR LÍNEA al final del TSV (nunca reescribe filas ajenas) y es idempotente por id.

    python3 forense/analisis/pendientes-4/arma_firmas_pendientes_4.py            # dry-run
    python3 forense/analisis/pendientes-4/arma_firmas_pendientes_4.py --escribe
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FP = os.path.join(RAIZ, "forense", "firmas-pendientes.tsv")
HOJA_REL = "forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md"
HOJA = os.path.join(RAIZ, HOJA_REL)
RAIZ_ID = "FP-260928-GEN2-PENDIENTES-4-12d9-"
ENCARGO = "forense/encargos/2026-09-28-GEN2-PENDIENTES-4.md"
CREADO = "2026-09-29"
ADR = "ADR-260928-GEN2-PENDIENTES-4-12d9-01"


def limpia(t, n=None):
    t = re.sub(r"\s+", " ", (t or "").replace("\t", " ")).strip()
    return t[:n] if n else t


def renglones():
    """{'D1': {titulo, ncs, fp, opciones[(letra,texto)], recomendacion, firma}} desde la hoja."""
    out, cur = {}, None
    for l in open(HOJA, encoding="utf-8").read().split("\n"):
        m = re.match(r"^## (D\d+) · (.*)$", l)
        if m:
            cur = out.setdefault(m.group(1), {"titulo": m.group(2).strip(), "ncs": [], "fp": "", "opciones": [],
                                              "recomendacion": "", "firma": ""})
            continue
        if not cur:
            continue
        if l.startswith("**NC que decide"):
            cur["ncs"] = re.findall(r"`(NC-[^`]+)`", l)
        elif l.startswith("**FP existente:**"):
            m2 = re.search(r"`(FP-[^`]+)`", l)
            cur["fp"] = m2.group(1) if m2 else ""
        elif re.match(r"^- \*\*\(([a-zA-Z]+)\)\*\* ", l):
            m3 = re.match(r"^- \*\*\(([a-zA-Z]+)\)\*\* (.*?)(?: — \*Costo:\*.*)?$", l)
            cur["opciones"].append((m3.group(1), m3.group(2)))
        elif l.startswith("**Recomendación.**"):
            m4 = re.match(r"^\*\*Recomendación\.\*\* \(([^)]+)\)", l)
            cur["recomendacion"] = m4.group(1) if m4 else ""
        elif l.startswith("**Texto de firma.**"):
            cur["firma"] = l[len("**Texto de firma.** "):].strip()
    return out


def filas():
    f = [
        [RAIZ_ID + "01",
         "Las dos autorizaciones de GEN2-PENDIENTES-4: (a) el acto cierra por diseño, con cita, toda NC cuyo objeto sea GEN1 (E.1), "
         "un procedimiento retirado por regla 6, un archivo que ya no existe o un producto que otro acto ya entregó en main; (b) el "
         "acto redacta los encargos que piden las NC «encargo por escribir», agrupados y como PROPUESTOS en forense/encargos/cola/PROPUESTOS/, "
         "sin lanzarlos.",
         "forense/encargos/2026-09-28-GEN2-PENDIENTES-4-ADENDA-1.md",
         CREADO, "cierre por diseño de las NC GEN1 o retiradas y redacción de los encargos propuestos", "FIRMADA",
         "Mesa, 28/sep/2026, chat de dirección (maestra 54), en respuesta a la frase «autorizas cerrar por diseño lo GEN1 o retirado, y que el acto "
         "redacte los encargos como propuestos en cola»: «Ok con pendientes 4» (verbatim en la ADENDA-1 del encargo).",
         f"{ADR} (PR #1326)", ENCARGO],
        [RAIZ_ID + "02",
         "La delegación firmada en PENDIENTES-3 (el acto decide lo reversible y solo lo irreversible vuelve con opciones) y la regla A.14 "
         "(cierre hacia atrás: al cerrar, todo acto dictamina las NC que lo nombran como sucesor; rutas solo con sucesor archivado) siguen vigentes.",
         "forense/encargos/2026-09-28-GEN2-PENDIENTES-4-ADENDA-1.md (INTERPRETACIÓN-DECLARADA) y forense/encargos/2026-09-28-GEN2-PENDIENTES-3.md:17",
         CREADO, "todo cierre y toda asignación de dueño de las NC del libro", "FIRMADA",
         "Mesa, 28/sep/2026: la firma de PENDIENTES-3 (a delegación, b regla A.14) viajó en el chat de dirección y su ADENDA-1 no está archivada; "
         "«Ok con pendientes 4» la reafirma («Sigue vigente la delegación firmada en PENDIENTES-3 … y la regla nueva A.14») en la ADENDA-1 de este encargo.",
         f"{ADR} (PR #1326); asentada aquí porque PENDIENTES-3 no abrió su fila (A.12)", ENCARGO],
    ]
    n = 3
    for d, r in sorted(renglones().items(), key=lambda kv: int(kv[0][1:])):
        if r["fp"]:
            continue
        ops = " · ".join(f"({l}) " + (limpia(t, 150).rstrip(". ") + ("…" if len(limpia(t)) > 150 else "")) for l, t in r["opciones"])
        que = f"[{d} · {r['titulo']}] Opciones: {ops}. Recomendada: ({r['recomendacion']}). Texto de firma listo en la hoja."
        ncs = ", ".join(i.replace("NC-", "").split("-")[-2] + "-" + i.split("-")[-1] if i.startswith("NC-2") else i for i in r["ncs"])
        f.append([RAIZ_ID + f"{n:02d}", limpia(que, 1400), f"{HOJA_REL}#{d}", CREADO, f"cierre de las NC {ncs}", "ABIERTA", "", "", ENCARGO])
        n += 1
    return f


def main():
    escribe = "--escribe" in sys.argv
    txt = open(FP, encoding="utf-8").read()
    cab = txt.split("\n")[0].split("\t")
    assert cab == ["id", "qué_se_firma", "dónde", "creado", "gatea", "estado", "firmada_en", "ejecutada_en", "encargo"], cab
    ya = {l.split("\t")[0] for l in txt.split("\n")[1:] if l}
    nuevas = [f for f in filas() if f[0] not in ya]
    for f in nuevas:
        assert len(f) == 9 and all("\t" not in c and "\n" not in c for c in f), f[0]
    print(f"firmas: {len(filas())} previstas · {len(nuevas)} nuevas · {len(filas()) - len(nuevas)} ya presentes")
    if escribe and nuevas:
        sep = "" if txt.endswith("\n") else "\n"
        with open(FP, "a", encoding="utf-8", newline="") as fh:
            fh.write(sep + "\n".join("\t".join(f) for f in nuevas) + "\n")
        print("escrito:", os.path.relpath(FP, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
