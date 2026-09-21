#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_tuberia_ids_union.py -- las tres guardas de
`ACTO GEN2-TUBERIA-SUCESOR-1` (21/sep/2026), ejercidas POR MUTACIÓN.

Una guarda que no se puede disparar no es una guarda. Cada caso de aquí
rompe algo a propósito y exige que la guarda lo vea; y cada guarda tiene
además su control positivo (el árbol sano pasa), porque un test que sólo
comprueba que algo falla no distingue una guarda de un `assert False`.

  A · T15 con TRES aserciones (firma D-3) -- cinco mutaciones:
      A0 control: registro sano -> sin FAIL.
      A1 HUECO ACEPTADO: id acuñado con salto y conteo reconciliado -> sin
         FAIL (el bloque de huecos se retiró a propósito).
      A2 ADR duplicado -> FAIL.
      A3 conteo mal citado (el defecto del 29/jul/2026, 32 contra 37) -> FAIL.
      A4 cita a un ADR inexistente -> FAIL.
      A5 LA MEDICIÓN QUE JUSTIFICA LA FIRMA: con sólo DOS aserciones
         -sin el cotejo de conteo- el defecto del 29/jul sale VERDE.
         Por eso la firma dice tres y no dos.

  B · T46, la guarda de salto de línea final -- por mutación y contra el
      caso real:
      B0 control: `.gitattributes` real del repo -> sin FAIL.
      B1 archivo union sin `\n` final -> FAIL.
      B2 universo derivado: un TERCER archivo que entra a `merge=union`
         queda cubierto solo, sin tocar el test.
      B3 REPRODUCCIÓN DEL DEFECTO con git de verdad, en un repo temporal:
         sin `\n` final, dos ramas que apendican fusionan SIN conflicto y
         dejan dos filas deformadas, perdiendo la fila compartida; con el
         archivo bien terminado, la misma fusión sale limpia. Esto prueba
         que la guarda vigila un defecto real y no un fantasma.

  C · La gramática de id `FP`, dos épocas (firma D-2):
      C1 acepta la época vieja (`FP-###`, espacio CERRADO).
      C2 acepta la época nueva (`FP-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`).
      C3 RECHAZA una tercera época inventada.
      C4 `tools/nc_por_clase.py` clasifica con UN ID DE CADA ÉPOCA PINADO
         EN EL MISMO CASO -- un patrón ensanchado probado sólo contra ids
         viejos no prueba nada.

Corre sola, sin dependencias:
    python3 tests/test_tuberia_ids_union.py
"""
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

FALLAS = []


def ok(caso, cond, detalle=""):
    print(("  OK   " if cond else "  FALLA") + f" {caso}" + (f" -- {detalle}" if detalle else ""))
    if not cond:
        FALLAS.append(caso)


def _carga_check():
    """`tests/check.py` como módulo fresco, con `FAILS`/`WARNS` propios.

    Se recarga en cada caso a propósito: las listas de veredicto son estado
    de módulo, y reutilizar una instancia haría que el caso N viera los FAIL
    del caso N-1.
    """
    spec = importlib.util.spec_from_file_location(
        "check_bajo_mutacion", os.path.join(ROOT, "tests", "check.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ─────────────────────────────────────────────────────────────────────
# A · T15
# ─────────────────────────────────────────────────────────────────────
def _arbol_gobernanza(tmp, entradas, extra_canon=""):
    """Un `canon/` mínimo: `gobernanza` con las entradas dadas y una cita
    de conteo que, por defecto, es la correcta."""
    os.makedirs(os.path.join(tmp, "canon"), exist_ok=True)
    cuerpo = "\n".join(f"**ADR-{n}** — entrada de prueba {n}\n" for n in entradas)
    with open(os.path.join(tmp, "canon", "gobernanza-v1_15.md"), "w", encoding="utf-8") as f:
        f.write(f"# Gobernanza de prueba\n\n**{len(set(entradas))} ADR**\n\n{cuerpo}\n{extra_canon}\n")


def _t15(tmp):
    m = _carga_check()
    m.ROOT = tmp
    m.t15_adr_count()
    return [f for f in m.FAILS if f[0] == "T15"]


def caso_A():
    print("A · T15, tres aserciones y huecos aceptados")
    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza(tmp, [1, 2, 3, 4])
        ok("A0 control: registro sano pasa", _t15(tmp) == [], str(_t15(tmp)))

    with tempfile.TemporaryDirectory() as tmp:
        # id acuñado con salto (1,2,4): hueco en 3, conteo reconciliado a 3.
        _arbol_gobernanza(tmp, [1, 2, 4])
        f = _t15(tmp)
        ok("A1 hueco ACEPTADO (con el conteo reconciliado)", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza(tmp, [1, 2, 3, 3])
        f = _t15(tmp)
        ok("A2 ADR duplicado FALLA", any("repetido" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # El defecto del 29/jul/2026: la prosa cita 32 donde hay 37 únicos.
        _arbol_gobernanza(tmp, list(range(1, 38)))
        g = os.path.join(tmp, "canon", "gobernanza-v1_15.md")
        s = open(g, encoding="utf-8").read().replace("**37 ADR**", "**32 ADR**")
        open(g, "w", encoding="utf-8").write(s)
        f = _t15(tmp)
        ok("A3 conteo mal citado FALLA (32 contra 37)",
           any("cita 32 ADR" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza(tmp, [1, 2, 3], extra_canon="\nVer `ADR-999` para el detalle.\n")
        f = _t15(tmp)
        ok("A4 cita a ADR inexistente FALLA",
           any("ADR-999" in x[1] for x in f), str(f))

    # A5 · la medición que justifica la firma: DOS aserciones dejan pasar
    # el defecto del 29/jul. Se simula la variante de dos corriendo la
    # aserción (1) y la (3) -- sin el cotejo de conteo -- sobre el mismo
    # árbol que A3 rompe.
    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza(tmp, list(range(1, 38)))
        g = os.path.join(tmp, "canon", "gobernanza-v1_15.md")
        s = open(g, encoding="utf-8").read().replace("**37 ADR**", "**32 ADR**")
        open(g, "w", encoding="utf-8").write(s)
        nums = [int(n) for n in re.findall(r"^\*\*ADR-(\d+)", s, re.M)]
        dup = [n for n in set(nums) if nums.count(n) > 1]
        colgantes = [int(n) for n in re.findall(r"\bADR-(\d+)\b", s) if int(n) not in set(nums)]
        ok("A5 con DOS aserciones el defecto del 29/jul sale VERDE "
           "(por eso la firma dice tres)", dup == [] and colgantes == [],
           f"dup={dup} colgantes={colgantes}")


# ─────────────────────────────────────────────────────────────────────
# B · T46
# ─────────────────────────────────────────────────────────────────────
def _t46(tmp):
    m = _carga_check()
    m.ROOT = tmp
    m.t46_union_newline()
    return [f for f in m.FAILS if f[0] == "T46"]


def _arbol_union(tmp, archivos, gitattributes):
    with open(os.path.join(tmp, ".gitattributes"), "w", encoding="utf-8") as f:
        f.write(gitattributes)
    for rel, contenido in archivos.items():
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(contenido)


def caso_B():
    print("B · T46, la guarda de salto de línea final")
    # B0 · control sobre el `.gitattributes` REAL del repo.
    f = _t46(ROOT)
    ok("B0 control: el árbol real pasa", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_union(tmp,
                     {"forense/hallazgos.md": "- una\n- dos"},      # sin \n final
                     "forense/hallazgos.md merge=union\n")
        f = _t46(tmp)
        ok("B1 archivo union sin salto de línea FALLA",
           any("NO termina en salto" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # El universo se DERIVA: un tercer archivo entra a union y queda
        # cubierto sin tocar el test. El comentario que menciona `union`
        # en prosa no debe contarse como declaración.
        _arbol_union(tmp,
                     {"forense/hallazgos.md": "- una\n",
                      "forense/bitacora.md": "- dos\n",
                      "forense/tercero.md": "- tres"},
                     "# hitoD-preregistro-v2_0.md NO entra a union, a propósito\n"
                     "forense/hallazgos.md merge=union\n"
                     "forense/bitacora.md merge=union\n"
                     "forense/tercero.md merge=union\n")
        f = _t46(tmp)
        ok("B2 universo derivado: el tercer archivo queda cubierto solo",
           len(f) == 1 and "tercero.md" in f[0][1], str(f))


def _git(cwd, *args):
    return subprocess.run(("git",) + args, cwd=cwd, capture_output=True, text=True)


def _repro_union(tmp, con_salto_final):
    """Reproducción del defecto con git de verdad, receta de §3 del encargo:
    base de tres líneas, `merge=union`, dos ramas que apendican, main fusiona
    X y luego Y. Devuelve (hubo_conflicto, líneas_finales)."""
    _git(tmp, "init", "-q", "-b", "main")
    _git(tmp, "config", "user.email", "t@t"); _git(tmp, "config", "user.name", "t")
    open(os.path.join(tmp, ".gitattributes"), "w").write("bitacora.md merge=union\n")
    base = "- PRIMERA\n- SEGUNDA\n- ULTIMA COMPARTIDA" + ("\n" if con_salto_final else "")
    open(os.path.join(tmp, "bitacora.md"), "w").write(base)
    _git(tmp, "add", "-A"); _git(tmp, "commit", "-qm", "base")
    for rama, entrada in (("x", "- entrada de X"), ("y", "- entrada de Y")):
        _git(tmp, "checkout", "-q", "-b", rama, "main")
        with open(os.path.join(tmp, "bitacora.md"), "a") as f:
            f.write(entrada + "\n")
        _git(tmp, "add", "-A"); _git(tmp, "commit", "-qm", rama)
    _git(tmp, "checkout", "-q", "main")
    conflicto = False
    for rama in ("x", "y"):
        r = _git(tmp, "merge", "--no-edit", "-q", rama)
        if r.returncode != 0:
            conflicto = True
            _git(tmp, "merge", "--abort")
    return conflicto, open(os.path.join(tmp, "bitacora.md")).read().split("\n")


def caso_B3():
    print("B3 · reproducción del defecto con git de verdad")
    if _git(ROOT, "--version").returncode != 0:
        ok("B3 git disponible", False, "git no ejecutable en este entorno")
        return
    with tempfile.TemporaryDirectory() as tmp:
        conflicto, lineas = _repro_union(tmp, con_salto_final=False)
        deformadas = [l for l in lineas if l.count("- ") > 1]
        compartida_sola = "- ULTIMA COMPARTIDA" in lineas
        ok("B3a sin salto final: fusiona SIN conflicto y deforma filas",
           not conflicto and len(deformadas) == 2 and not compartida_sola,
           f"conflicto={conflicto} deformadas={deformadas} compartida_sola={compartida_sola}")
    with tempfile.TemporaryDirectory() as tmp:
        conflicto, lineas = _repro_union(tmp, con_salto_final=True)
        deformadas = [l for l in lineas if l.count("- ") > 1]
        ok("B3b con salto final: la misma fusión sale limpia",
           not conflicto and not deformadas and "- ULTIMA COMPARTIDA" in lineas
           and "- entrada de X" in lineas and "- entrada de Y" in lineas,
           f"conflicto={conflicto} lineas={lineas}")


# ─────────────────────────────────────────────────────────────────────
# C · gramática de id FP, dos épocas
# ─────────────────────────────────────────────────────────────────────
VIEJOS = ["FP-67", "FP-402", "FP-403"]
NUEVOS = ["FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01",
          "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02"]
TERCERA_EPOCA_INVENTADA = [
    "FP-2609",                                    # fecha truncada: ni vieja ni nueva
    "FP-26092",                                   # idem
    "FP-260921-TUBERIA-SUCESOR-1-6e60-01",        # sin `GEN2-`: E.1 no admite suponerla
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6E60-01",   # hex en mayúscula: no es un short hash
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-1",    # secuencia de un dígito
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60g-01",  # hex de cinco
    "FP-",
    "FP-abc",
]


def caso_C():
    print("C · gramática de id FP, dos épocas")
    import nc_por_clase as NPC
    ok("C1 acepta la época vieja (espacio CERRADO)",
       all(re.fullmatch(NPC.RE_FP, t) for t in VIEJOS),
       str([t for t in VIEJOS if not re.fullmatch(NPC.RE_FP, t)]))
    ok("C2 acepta la época nueva (raíz de acto)",
       all(re.fullmatch(NPC.RE_FP, t) for t in NUEVOS),
       str([t for t in NUEVOS if not re.fullmatch(NPC.RE_FP, t)]))
    ok("C3 RECHAZA una tercera época inventada",
       not any(re.fullmatch(NPC.RE_FP, t) for t in TERCERA_EPOCA_INVENTADA),
       str([t for t in TERCERA_EPOCA_INVENTADA if re.fullmatch(NPC.RE_FP, t)]))
    # El id nuevo no se parte en dos por la rama vieja de la alternancia.
    ok("C3-bis el id nuevo no se parte en un `FP-###` fantasma",
       re.findall(NPC.RE_FP, f"cita {NUEVOS[0]} aquí") == [NUEVOS[0]],
       str(re.findall(NPC.RE_FP, f"cita {NUEVOS[0]} aquí")))


def caso_C4():
    print("C4 · nc_por_clase con UN ID DE CADA ÉPOCA en el mismo caso")
    import nc_por_clase as NPC
    fps = {"FP-402": "ABIERTA", NUEVOS[0]: "ABIERTA", "FP-403": "FIRMADA"}
    enc, notas = {}, {}

    r_vieja = {"sucesor": "FP-402", "razon": "DECISIÓN-DE-MESA-PENDIENTE: espera FP-402"}
    r_nueva = {"sucesor": NUEVOS[0], "razon": f"DECISIÓN-DE-MESA-PENDIENTE: espera {NUEVOS[0]}"}
    r_ambas = {"sucesor": NUEVOS[0], "razon": f"espera FP-402 y {NUEVOS[0]}"}

    t_v, d_v, _ = NPC.clasifica(r_vieja, fps, enc, notas)
    t_n, d_n, _ = NPC.clasifica(r_nueva, fps, enc, notas)
    t_a, d_a, det_a = NPC.clasifica(r_ambas, fps, enc, notas)

    ok("C4a la FP vieja se ve -> ESPERA-FIRMA", t_v == NPC.T_FIRMA, f"{t_v} · {d_v}")
    ok("C4b la FP NUEVA se ve -> ESPERA-FIRMA (antes: invisible, SIN-ASIGNAR)",
       t_n == NPC.T_FIRMA and NUEVOS[0] in d_n, f"{t_n} · {d_n}")
    ok("C4c las DOS épocas en la misma fila se ven a la vez",
       t_a == NPC.T_FIRMA and "FP-402" in det_a and NUEVOS[0] in det_a,
       f"{t_a} · {det_a}")

    # Control negativo: si la FP nueva ya está FIRMADA, deja de bloquear.
    fps2 = dict(fps); fps2[NUEVOS[0]] = "FIRMADA"
    t2, d2, _ = NPC.clasifica(r_nueva, fps2, enc, notas)
    ok("C4d control negativo: FP nueva FIRMADA ya no bloquea",
       t2 != NPC.T_FIRMA, f"{t2} · {d2}")


def main():
    print("═" * 72)
    print("  GEN2-TUBERIA-SUCESOR-1 · guardas por mutación")
    print("═" * 72)
    caso_A(); caso_B(); caso_B3(); caso_C(); caso_C4()
    print("─" * 72)
    if FALLAS:
        print(f"  {len(FALLAS)} FALLA(S): " + " · ".join(FALLAS))
        return 1
    print("  TODO VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
