#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_nc_cierre_hacia_atras.py -- A.14 ampliada (v2.17.1) en
`tools/cierre_acto.py` (ACTO GEN2-PENDIENTES-3 · P1, 28/sep/2026).

Defecto real que atrapa: el libro `forense/no-corrido.tsv` llegó a 497 NC
ABIERTAS; 75 cuyo sucesor ya había corrido sin dictaminarlas y 117 cierres
sin acto declarado (inventario v4, `forense/analisis/pendientes-3/`).

Casos sintéticos (sin git, sin red, stdlib):
  (A) un acto cuyo nombre aparece en el `sucesor` de una NC ABIERTA -> FALTA-DICTAMEN.
  (B) la misma NC con `CERRADA (producto: …)` + `fecha_cierre` -> pasa.
  (C) CERRADA sin `cerrado_por` / sin fecha -> falla; con `cerrado_por` del acto
      pero sin forma de dictamen -> falla.
  (D) SIGUE-ABIERTA reasignada a un encargo archivado -> pasa; a un nombre
      inexistente -> falla.
  (E) ruta nueva DIFERIDO-A / FUERA-DE-PERÍMETRO sin sucesor archivado ni en
      vuelo -> RUTA-SIN-SUCESOR; con archivado o en vuelo -> entra; filas
      viejas (en la base) no se re-juzgan.
  (F) frontera de nombre: `GEN2-E4` nombra a `GEN2-E4-LIMPIEZA-C2-PODA`, no a
      `GEN2-E41-X`; una familia ambigua no nombra a nadie.

Modo `--libro` (no corre en CI): verifica sobre el libro REAL que toda NC
ABIERTA tiene `sucesor` de la lista cerrada de dueños de GEN2-PENDIENTES-3
(`RE_DUENO`, abajo) y que todo `CAJA (…)` apunta a un encargo que existe.

Corre sola:
    python3 tests/test_nc_cierre_hacia_atras.py
    python3 tests/test_nc_cierre_hacia_atras.py --libro
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cierre_acto as CA  # noqa: E402

FAILS = []

# Lista cerrada de dueños al cierre (encargo GEN2-PENDIENTES-3 §1 P4) más
# EN-CURSO (§4/§5: filas de un acto en vuelo se citan con su rama).
RE_DUENO = re.compile(
    r"^(?:MESA \(\d{4}-\d{2}-\d{2}\)"
    r"|CAJA \((forense/encargos/[^)\s]+\.md)\)"
    r"|ADQUISICION \([^)]+\)"
    r"|APERTURA \([^)]+\)"
    r"|EN-CURSO \([^)]+ · rama [^)\s]+\))")


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)




def fila(fid, razon, sucesor, estado="ABIERTA", cerrado_por="NO-APLICA", fecha_cierre="NO-APLICA"):
    return {"id": fid, "razon": razon, "sucesor": sucesor, "estado": estado,
            "cerrado_por": cerrado_por, "fecha_cierre": fecha_cierre}


IDX = {
    "GEN2-ACTO-SINTETICO-1": "ARCHIVADO",
    "GEN2-DESTINO-ARCHIVADO-1": "ARCHIVADO",
    "GEN2-E4-LIMPIEZA-C2-PODA": "ARCHIVADO",
    "GEN2-E41-X": "ARCHIVADO",
    "GEN2-TUBERIA-3": "EN-VUELO:claude/new-session-x",
    "GEN2-TUBERIA-CI-1": "ARCHIVADO",
}
ACTO = "GEN2-ACTO-SINTETICO-1"


def caso_a_b_c():
    base = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO} (cierra el hueco)")]
    d = CA.dictamen_hacia_atras(ACTO, base, base, IDX)
    afirma(len(d["falta"]) == 1 and d["falta"][0][0] == "NC-S-01", f"(A) sin dictamen debe fallar: {d}")

    ok = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO}", "CERRADA",
               f"{ACTO} · CERRADA (producto: tools/x.py · python3 tools/x.py --json)", "2026-09-28")]
    d = CA.dictamen_hacia_atras(ACTO, ok, base, IDX)
    afirma(not d["falta"] and d["dictaminadas"] == [("NC-S-01", "CERRADA")], f"(B) con dictamen pasa: {d}")

    so = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO}", "CERRADA",
               f"{ACTO} · SIN-OBJETO (forense/hallazgos.md línea 9)", "2026-09-28")]
    afirma(not CA.dictamen_hacia_atras(ACTO, so, base, IDX)["falta"], "(B) SIN-OBJETO con cita pasa")

    sin_cp = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO}", "CERRADA", "NO-APLICA", "2026-09-28")]
    afirma(CA.dictamen_hacia_atras(ACTO, sin_cp, base, IDX)["falta"], "(C) CERRADA sin cerrado_por falla")
    sin_fecha = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO}", "CERRADA",
                      f"{ACTO} · CERRADA (producto: a · b)", "")]
    afirma(CA.dictamen_hacia_atras(ACTO, sin_fecha, base, IDX)["falta"], "(C) CERRADA sin fecha falla")
    sin_forma = [fila("NC-S-01", "DIFERIDO-A: x", f"{ACTO}", "CERRADA", f"{ACTO}", "2026-09-28")]
    afirma(CA.dictamen_hacia_atras(ACTO, sin_forma, base, IDX)["falta"],
           "(C) cerrado_por del acto sin forma de dictamen falla")


def caso_d():
    base = [fila("NC-S-02", "FUERA-DE-PERÍMETRO: y", f"{ACTO}")]
    re_ok = [fila("NC-S-02", "FUERA-DE-PERÍMETRO: y", "CAJA (GEN2-DESTINO-ARCHIVADO-1)")]
    d = CA.dictamen_hacia_atras(ACTO, re_ok, base, IDX)
    afirma(not d["falta"] and d["dictaminadas"] == [("NC-S-02", "SIGUE-ABIERTA")], f"(D) reasignada pasa: {d}")
    re_mal = [fila("NC-S-02", "FUERA-DE-PERÍMETRO: y", "GEN2-NO-EXISTE-9")]
    afirma(CA.dictamen_hacia_atras(ACTO, re_mal, base, IDX)["falta"], "(D) reasignada a inexistente falla")


def caso_e():
    base = [fila("NC-VIEJA", "DIFERIDO-A: z", "SIN-ASIGNAR")]
    head = base + [
        fila("NC-N-01", "DIFERIDO-A: sin dueño", "SIN-ASIGNAR"),
        fila("NC-N-02", "FUERA-DE-PERÍMETRO: de otro", "GEN2-INVENTADO-7"),
        fila("NC-N-03", "DIFERIDO-A: ok", "GEN2-DESTINO-ARCHIVADO-1"),
        fila("NC-N-04", "FUERA-DE-PERÍMETRO: en vuelo", "GEN2-TUBERIA-3 (rama)"),
        fila("NC-N-05", "NO-VERIFICABLE-AQUÍ: no es ruta", "SIN-ASIGNAR"),
        fila("NC-N-06", "DIFERIDO-A: se nombra a sí mismo", ACTO),
    ]
    malas = {m[0] for m in CA.rutas_sin_sucesor(head, base, IDX, ACTO)}
    afirma(malas == {"NC-N-01", "NC-N-02", "NC-N-06"}, f"(E) rutas rechazadas: {sorted(malas)}")


def caso_f():
    afirma(CA.actos_nombrados("DIFERIDO a GEN2-E4 cuando corra", IDX) == {"GEN2-E4-LIMPIEZA-C2-PODA"},
           "(F) GEN2-E4 resuelve por frontera")
    afirma("GEN2-E4-LIMPIEZA-C2-PODA" not in CA.actos_nombrados("GEN2-E41", IDX), "(F) GEN2-E41 no es GEN2-E4")
    afirma(CA.actos_nombrados("la familia GEN2-TUBERIA", IDX) == set(), "(F) familia ambigua no nombra")
    afirma(CA.actos_nombrados("FP-260928-GEN2-ACTO-SINTETICO-1-abcd-01", IDX) == set(),
           "(F) un id FP no nombra al acto que lo acuñó")
    afirma(CA.rotulo_de_encargo("forense/encargos/2026-09-28-GEN2-PENDIENTES-3-ADENDA-2.md")
           == "GEN2-PENDIENTES-3", "(F) rótulo de encargo quita fecha y adenda")


def libro():
    """Modo `--libro`: el «hecho» de GEN2-PENDIENTES-3 sobre el libro real."""
    filas = CA.lee_nc(CA._leer(os.path.join(ROOT, "forense", "no-corrido.tsv")))
    abiertas = [f for f in filas if (f.get("estado") or "").strip() == "ABIERTA"]
    fuera = []
    for f in abiertas:
        m = RE_DUENO.match((f.get("sucesor") or "").strip())
        if not m:
            fuera.append((f["id"], "sucesor fuera de la lista cerrada"))
        elif m.group(1) and not os.path.exists(os.path.join(ROOT, m.group(1))):
            fuera.append((f["id"], f"CAJA apunta a {m.group(1)} que no existe"))
    print(f"libro: {len(filas)} filas · {len(abiertas)} ABIERTA · fuera de la lista cerrada: {len(fuera)}")
    for fid, motivo in fuera[:40]:
        print(f"  {fid}: {motivo}")
    return 1 if fuera else 0


def main():
    if "--libro" in sys.argv:
        return libro()
    caso_a_b_c()
    caso_d()
    caso_e()
    caso_f()
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        return 1
    print("OK test_nc_cierre_hacia_atras (A-F)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
