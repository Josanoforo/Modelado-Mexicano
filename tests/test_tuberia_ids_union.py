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

  D · T47, ids únicos en los registros donde este acto acuña:
      D0 control: los registros reales del repo pasan.
      D1 huecos y las dos épocas conviviendo NO fallan (sólo unicidad).
      D2 EL DEFECTO REAL DEL 21/sep/2026: `FP-406` duplicado con contenido
         contradictorio -> FALLA. Lo produjo el propio merge de este acto
         (conservar ambos lados de una fila que `main` MODIFICÓ en vez de
         apendicar) y lo cazó una persona, no la suite.
      D3 id `NC` duplicado -> FALLA.
      D4 cero registros examinados no es un negativo (A.13).

  C · La gramática de id `FP`, dos épocas (firma D-2):
      C1 acepta la época vieja (`FP-###`, espacio CERRADO).
      C2 acepta la época nueva (`FP-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`).
      C3 RECHAZA una tercera época inventada.
      C4 `tools/nc_por_clase.py` clasifica con UN ID DE CADA ÉPOCA PINADO
         EN EL MISMO CASO -- un patrón ensanchado probado sólo contra ids
         viejos no prueba nada.

  E · T15 con `ADR` de dos épocas (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`,
      21/sep/2026, P-C.3) -- UN `ADR` DE CADA ÉPOCA EN EL MISMO CASO:
      E0 control: sólo época vieja -> sin FAIL (igual que caso A).
      E1 sólo época nueva (raíz de acto), conteo `N ADR` ausente -> sin
         FAIL (la aserción (2) no aplica sin espacio numérico vigente).
      E2 LAS DOS ÉPOCAS CONVIVIENDO en el mismo `gobernanza` -> sin FAIL.
      E3 cita a una raíz de acto que NO existe -> FALLA.
      E4 UNA RAÍZ NUEVA NO SE LEE COMO UN `ADR-260921` FANTASMA: sin esta
         alternancia, `(\\d+)` a secas leería `ADR-260921-GEN2-X-1-6e60-01`
         como el número de ADR 260921 y citaría un "260921 ADR" falso.
      E5 raíz de acto duplicada -> FALLA.

  G · P-D, `union` sólo donde la mutación lo justifique -- reproducción
      REAL con git (no simulada) contra los cuatro candidatos, el caso
      exacto: una rama edita EN SU SITIO la última fila/entrada, otra
      AÑADE debajo, se fusiona con `union`:
      G1 no-corrido.tsv / firmas-pendientes.tsv: T47 atrapa el resultado
         (id repetido, contenido contradictorio) -> ENTRAN a union.
      G2 gobernanza-v1_15.md: T15 atrapa el ADR repetido por NÚMERO
         (aunque el texto de las dos copias difiera) -> ENTRA a union.
      G3 registro-rotulos.tsv: la fila SÍ queda duplicada con contenido
         contradictorio (el riesgo es real) pero NINGUNA guarda de la
         suite lo vigila hoy -> QUEDA FUERA de union hasta el sucesor.

  H · T50, la guarda de líneas repetidas en archivos `union` (P-D.3):
      H0 control, H1 línea >= 200 caracteres repetida FALLA, H2 línea
      corta repetida NO dispara (umbral), H3 sin universo declarado ->
      WARN, no FAIL.

  F · T48/T49, las dos guardas permanentes de la L0 (P-A.4) -- la mutación
      de prueba es EXACTAMENTE el caso de las ramas en vuelo: fusionar una
      rama con la línea `L0` vieja (~27 MB, aquí un análogo sintético >1 MB
      para no cargar 27 MB reales al test) sobre la línea reparada,
      conservando ambos lados -- las DOS guardas deben fallar A LA VEZ:
      F0 control: árbol sano (línea corta, hash fijado) -> sin FAIL en
         ninguna de las dos.
      F1 T48 sola: una línea de `canon/` > 1 MB -> FALLA, con el mensaje
         que dice qué hacer.
      F2 T49 sola: `HISTORICO.md` tocado (hash ya no casa) -> FALLA, con
         el mensaje que dice qué hacer.
      F3 LA MUTACIÓN EXACTA: "conservar ambos lados" de una rama con la
         L0 vieja sobre la reparada dispara T48 (línea > 1 MB) y T49
         (`HISTORICO.md` ya no es el mismo) A LA VEZ.
      F4 T48 examina cero archivos no es un negativo (A.13).

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


ADR_VIEJOS = ["ADR-67", "ADR-402", "ADR-591"]
ADR_NUEVOS = ["ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1-2707-01",
              "ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1-2707-02"]
ADR_TERCERA_EPOCA_INVENTADA = [
    "ADR-2609",
    "ADR-26092",
    "ADR-260921-TUBERIA-CIERRE-SIN-CHOQUE-1-2707-01",   # sin `GEN2-`
    "ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1-2707-1",  # NN de un dígito
    "ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1-2707g-01",  # hex de cinco
    "ADR-",
    "ADR-abc",
]


def caso_C_adr():
    """P-C.3: `tools/estado_comun.py::RE_ADR` -- el test de gramática de
    este archivo se extiende a `ADR`, mismo mecanismo que caso C para `FP`."""
    print("C-ADR · gramática de id ADR, dos épocas")
    import estado_comun as EC
    ok("C-ADR1 acepta la época vieja (espacio CERRADO)",
       all(re.fullmatch(EC.RE_ADR, t) for t in ADR_VIEJOS),
       str([t for t in ADR_VIEJOS if not re.fullmatch(EC.RE_ADR, t)]))
    ok("C-ADR2 acepta la época nueva (raíz de acto)",
       all(re.fullmatch(EC.RE_ADR, t) for t in ADR_NUEVOS),
       str([t for t in ADR_NUEVOS if not re.fullmatch(EC.RE_ADR, t)]))
    ok("C-ADR3 RECHAZA una tercera época inventada",
       not any(re.fullmatch(EC.RE_ADR, t) for t in ADR_TERCERA_EPOCA_INVENTADA),
       str([t for t in ADR_TERCERA_EPOCA_INVENTADA if re.fullmatch(EC.RE_ADR, t)]))
    ok("C-ADR3-bis el id nuevo no se parte en un `ADR-######` fantasma",
       re.findall(EC.RE_ADR, f"cita {ADR_NUEVOS[0]} aquí") == [ADR_NUEVOS[0]],
       str(re.findall(EC.RE_ADR, f"cita {ADR_NUEVOS[0]} aquí")))


# ─────────────────────────────────────────────────────────────────────
# D · T47, ids únicos en los registros
# ─────────────────────────────────────────────────────────────────────
def _t47(tmp):
    m = _carga_check()
    m.ROOT = tmp
    m.t47_ids_unicos()
    return [f for f in m.FAILS if f[0] == "T47"]


def _arbol_registros(tmp, nc_filas, fp_filas):
    os.makedirs(os.path.join(tmp, "forense"), exist_ok=True)
    with open(os.path.join(tmp, "forense", "no-corrido.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tfecha\n" + "".join(l + "\n" for l in nc_filas))
    with open(os.path.join(tmp, "forense", "firmas-pendientes.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tqué_se_firma\n" + "".join(l + "\n" for l in fp_filas))


def caso_D():
    print("D · T47, ids únicos en no-corrido.tsv y firmas-pendientes.tsv")
    # D0 · control sobre los registros REALES del repo.
    f = _t47(ROOT)
    ok("D0 control: los registros reales pasan", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # Las dos épocas conviven y los huecos son legítimos: no debe fallar.
        _arbol_registros(tmp,
                         ["NC-0001\ta", "NC-0007\tb", f"NC-260921-GEN2-X-1-6e60-01\tc"],
                         ["FP-67\ta", "FP-402\tb", NUEVOS[0] + "\tc"])
        f = _t47(tmp)
        ok("D1 huecos y dos épocas conviviendo NO fallan", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # EL DEFECTO REAL DEL 21/sep/2026: FP-406 duplicado con contenido
        # contradictorio (misma fila salvo el ADR citado, 575 contra 574)
        # porque el merge conservó ambos lados de una fila que main MODIFICÓ.
        _arbol_registros(tmp, ["NC-0001\ta"],
                         ["FP-406\tRETIRADA (... PR #938, ADR-575): ...",
                          "FP-406\tRETIRADA (... PR #938, ADR-574): ..."])
        f = _t47(tmp)
        ok("D2 id FP duplicado con contenido contradictorio FALLA",
           any("FP-406" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_registros(tmp, ["NC-0001\ta", "NC-0001\tb"], ["FP-67\ta"])
        f = _t47(tmp)
        ok("D3 id NC duplicado FALLA", any("NC-0001" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # A.13: sin registros que examinar, el veredicto no es un negativo.
        os.makedirs(os.path.join(tmp, "forense"), exist_ok=True)
        f = _t47(tmp)
        ok("D4 cero registros examinados no es un negativo (A.13)",
           any("A.13" in x[1] or "no se pudo leer" in x[1] for x in f), str(f))


# ─────────────────────────────────────────────────────────────────────
# E · T15 con `ADR` de dos épocas
# ─────────────────────────────────────────────────────────────────────
ADR_RAIZ_1 = "ADR-260921-GEN2-X-1-6e60-01"
ADR_RAIZ_2 = "ADR-260921-GEN2-X-1-6e60-02"


def _arbol_gobernanza_raw(tmp, cuerpo_lineas, n_adr=None, extra_canon=""):
    os.makedirs(os.path.join(tmp, "canon"), exist_ok=True)
    cab = f"**{n_adr} ADR**\n\n" if n_adr is not None else "\n"
    with open(os.path.join(tmp, "canon", "gobernanza-v1_15.md"), "w", encoding="utf-8") as f:
        f.write("# Gobernanza de prueba\n\n" + cab +
                "\n".join(cuerpo_lineas) + f"\n{extra_canon}\n")


def caso_E():
    print("E · T15 con `ADR` de dos épocas, una en cada caso")
    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza(tmp, [1, 2, 3])
        f = _t15(tmp)
        ok("E0 control: sólo época vieja pasa", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza_raw(tmp, [f"**{ADR_RAIZ_1}** — entrada de raíz"])
        f = _t15(tmp)
        ok("E1 sólo época nueva, sin conteo numérico vigente -> sin FAIL",
           f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza_raw(
            tmp,
            ["**ADR-3** — entrada vieja 3", "**ADR-2** — entrada vieja 2",
             "**ADR-1** — entrada vieja 1", f"**{ADR_RAIZ_1}** — entrada de raíz"],
            n_adr=3)
        f = _t15(tmp)
        ok("E2 las dos épocas conviviendo -> sin FAIL", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza_raw(
            tmp, [f"**{ADR_RAIZ_1}** — entrada de raíz"],
            extra_canon=f"\nVer `ADR-260921-GEN2-X-1-6e60-99` (no existe).\n")
        f = _t15(tmp)
        ok("E3 cita a una raíz de acto inexistente FALLA",
           any("6e60-99" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        # Sin la alternancia, `(\d+)\s*ADR\b` leería la raíz nueva como si
        # citara "260921 ADR" -- un número de ADR fantasma de seis dígitos.
        _arbol_gobernanza_raw(tmp, [f"**{ADR_RAIZ_1}** — entrada de raíz"])
        f = _t15(tmp)
        ok("E4 la raíz nueva NO se lee como una cita `260921 ADR` fantasma",
           not any("260921 ADR" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_gobernanza_raw(tmp, [f"**{ADR_RAIZ_1}** — a", f"**{ADR_RAIZ_1}** — b (duplicada)"])
        f = _t15(tmp)
        ok("E5 raíz de acto duplicada FALLA",
           any(ADR_RAIZ_1 in x[1] for x in f), str(f))


# ─────────────────────────────────────────────────────────────────────
# F · T48/T49, las dos guardas permanentes de la L0
# ─────────────────────────────────────────────────────────────────────
def _t48(tmp):
    m = _carga_check()
    m.ROOT = tmp
    m.t48_canon_linea_1mb()
    return [f for f in m.FAILS if f[0] == "T48"]


def _t49(tmp, sha_fijado=None):
    m = _carga_check()
    m.ROOT = tmp
    if sha_fijado is not None:
        m.SHA256_L0_HISTORICO_FIJADO = sha_fijado
    m.t49_l0_historico_fijado()
    return [f for f in m.FAILS if f[0] == "T49"]


def _sha256_de(texto):
    import hashlib
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _arbol_l0(tmp, estado_texto, historico_texto):
    os.makedirs(os.path.join(tmp, "canon", "L0"), exist_ok=True)
    with open(os.path.join(tmp, "canon", "estado-programa-v1_14.md"), "w", encoding="utf-8") as f:
        f.write(estado_texto)
    with open(os.path.join(tmp, "canon", "L0", "HISTORICO.md"), "w", encoding="utf-8") as f:
        f.write(historico_texto)


L0_SANA = "**L0 · Gobierno — completo y al día.** 3 ADR — histórico en `canon/L0/HISTORICO.md`.\n"
HISTORICO_SANO = "**L0 · Gobierno — completo y al día.** 3 ADR (contenido de prueba, corto)*---\n"
# Análogo sintético de la línea vieja de 27 MB -- no se cargan 27 MB reales
# al test; basta con superar el tope de 1 MB para ejercer la guarda con el
# mismo mecanismo (una línea de `canon/` fuera de tamaño).
L0_VIEJA_SINTETICA = "**L0 · Gobierno — completo y al día.** 3 ADR (" + ("X" * (1024 * 1024 + 10)) + ")*---\n"


def _repro_union_edita_y_apendica(tmp, nombre, base_texto, texto_editado_por_a, linea_nueva_de_b):
    """(P-D.2) LA MUTACIÓN EXACTA de los cuatro candidatos: una rama edita
    EN SU SITIO la última fila/entrada; otra rama AÑADE debajo; se fusiona
    con `union`. Devuelve el texto resultante tras fusionar main<-A<-B (o
    conflicto=True si `merge=union` no evitó un conflicto real)."""
    _git(tmp, "init", "-q", "-b", "main")
    _git(tmp, "config", "user.email", "t@t"); _git(tmp, "config", "user.name", "t")
    open(os.path.join(tmp, ".gitattributes"), "w").write(f"{nombre} merge=union\n")
    ruta = os.path.join(tmp, nombre)
    open(ruta, "w", encoding="utf-8").write(base_texto)
    _git(tmp, "add", "-A"); _git(tmp, "commit", "-qm", "base")

    _git(tmp, "checkout", "-q", "-b", "a", "main")
    open(ruta, "w", encoding="utf-8").write(texto_editado_por_a)
    _git(tmp, "add", "-A"); _git(tmp, "commit", "-qm", "a edita en su sitio")

    _git(tmp, "checkout", "-q", "-b", "b", "main")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(linea_nueva_de_b)
    _git(tmp, "add", "-A"); _git(tmp, "commit", "-qm", "b apendica")

    _git(tmp, "checkout", "-q", "main")
    conflicto = False
    for rama in ("a", "b"):
        r = _git(tmp, "merge", "--no-edit", "-q", rama)
        if r.returncode != 0:
            conflicto = True
            _git(tmp, "merge", "--abort")
    return conflicto, open(ruta, encoding="utf-8").read()


def caso_G():
    """P-D: `union` sólo donde la mutación lo justifique -- reproducción
    real con git para los CUATRO candidatos. `decisiones.tsv` e
    `hitoD-preregistro` quedan FUERA sin discusión (P-D.1, ya excluidos)."""
    print("G · P-D, la mutación exacta contra los cuatro candidatos")

    # G1 · forense/no-corrido.tsv, forense/firmas-pendientes.tsv: T47 sí
    # atrapa el resultado (id repetido con contenido contradictorio) -- LA
    # MISMA reproducción del defecto real del 21/sep/2026.
    for nombre, prefijo in (("no-corrido.tsv", "NC"), ("firmas-pendientes.tsv", "FP")):
        with tempfile.TemporaryDirectory() as tmp:
            base = f"id\testado\n{prefijo}-0001\tABIERTA\n"
            editado = f"id\testado\n{prefijo}-0001\tCERRADA\n"
            nueva = f"{prefijo}-0002\tABIERTA\n"
            conflicto, resultado = _repro_union_edita_y_apendica(tmp, nombre, base, editado, nueva)
            os.makedirs(os.path.join(tmp, "forense"), exist_ok=True)
            with open(os.path.join(tmp, "forense", nombre), "w", encoding="utf-8") as f:
                f.write(resultado)
            m = _carga_check()
            m.ROOT = tmp
            m.t47_ids_unicos()
            fails = [f for f in m.FAILS if f[0] == "T47"]
            ok(f"G1 {nombre}: sin conflicto real + T47 atrapa el resultado -> ENTRA a union",
               not conflicto and any(f"{prefijo}-0001" in x[1] for x in fails),
               f"conflicto={conflicto} T47={fails} resultado={resultado!r}")

    # G2 · canon/gobernanza-v1_15.md: T15 (dup por NÚMERO, sin importar que
    # el texto difiera) sí atrapa el resultado -> ENTRA a union.
    with tempfile.TemporaryDirectory() as tmp:
        base = "# Gobernanza\n\n**1 ADR**\n\n**ADR-1** — texto original de la entrada\n"
        editado = "# Gobernanza\n\n**1 ADR**\n\n**ADR-1** — texto EDITADO en su sitio por A\n"
        nueva = "**ADR-2** — entrada nueva de B\n"
        conflicto, resultado = _repro_union_edita_y_apendica(tmp, "gobernanza-v1_15.md", base, editado, nueva)
        os.makedirs(os.path.join(tmp, "canon"), exist_ok=True)
        with open(os.path.join(tmp, "canon", "gobernanza-v1_15.md"), "w", encoding="utf-8") as f:
            f.write(resultado)
        m = _carga_check()
        m.ROOT = tmp
        m.t15_adr_count()
        fails = [f for f in m.FAILS if f[0] == "T15"]
        ok("G2 gobernanza-v1_15.md: sin conflicto real + T15 atrapa el ADR "
           "repetido (mismo número, texto distinto) -> ENTRA a union",
           not conflicto and any("repetido" in x[1] for x in fails),
           f"conflicto={conflicto} T15={fails} resultado={resultado!r}")

    # G3 · canon/registro-rotulos.tsv: NINGUNA guarda existente vigila
    # filas repetidas de este TSV (T25 vigila OTROS archivos citando
    # rótulos pelados, no duplicados dentro de este archivo) -> QUEDA
    # FUERA de union hasta el sucesor -- se comprueba corriendo TODA la
    # suite sobre el árbol mutado y verificando que ningún FAIL nombra el
    # archivo ni "rótulo" repetido.
    with tempfile.TemporaryDirectory() as tmp:
        base = "espacio\tvalor\tque_significa\tdonde_vive\nE\tGEN2-X\toriginal\tsitio-a\n"
        editado = "espacio\tvalor\tque_significa\tdonde_vive\nE\tGEN2-X\tEDITADO por A\tsitio-a\n"
        nueva = "E\tGEN2-Y\tnueva\tsitio-b\n"
        conflicto, resultado = _repro_union_edita_y_apendica(tmp, "registro-rotulos.tsv", base, editado, nueva)
        lineas_gen2_x = [l for l in resultado.split("\n") if l.startswith("E\tGEN2-X\t")]
        ok("G3 registro-rotulos.tsv: sin conflicto real, y la fila SÍ queda "
           "duplicada con contenido contradictorio (el mecanismo del defecto "
           "existe) pero NINGUNA guarda de la suite lo vigila -> QUEDA FUERA",
           not conflicto and len(lineas_gen2_x) == 2,
           f"conflicto={conflicto} filas={lineas_gen2_x}")


def _t50(tmp):
    m = _carga_check()
    m.ROOT = tmp
    m.t50_union_lineas_repetidas()
    return [f for f in m.FAILS if f[0] == "T50"]


def caso_H():
    """T50 -- guarda de líneas repetidas en archivos `union` (P-D.3)."""
    print("H · T50, líneas repetidas en archivos union")
    linea_larga = "X" * 250

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_union(tmp, {"canon/gobernanza-v1_15.md": f"{linea_larga}\notra línea corta\n"},
                     "canon/gobernanza-v1_15.md merge=union\n")
        f = _t50(tmp)
        ok("H0 control: línea larga UNA sola vez -> sin FAIL", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_union(tmp, {"canon/gobernanza-v1_15.md": f"{linea_larga}\n{linea_larga}\n"},
                     "canon/gobernanza-v1_15.md merge=union\n")
        f = _t50(tmp)
        ok("H1 línea >= 200 caracteres repetida FALLA",
           any("aparece 2 veces" in x[1] for x in f), str(f))

    with tempfile.TemporaryDirectory() as tmp:
        corta = "corta"
        _arbol_union(tmp, {"canon/gobernanza-v1_15.md": f"{corta}\n{corta}\n{corta}\n"},
                     "canon/gobernanza-v1_15.md merge=union\n")
        f = _t50(tmp)
        ok("H2 línea corta repetida NO dispara (umbral 200)", f == [], str(f))

    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(tmp, exist_ok=True)
        open(os.path.join(tmp, ".gitattributes"), "w").write("# nada declarado\n")
        f = _t50(tmp)
        ok("H3 sin ningún merge=union declarado -> WARN, no FAIL", f == [], str(f))


def caso_F():
    print("F · T48/T49, las dos guardas permanentes de la L0")
    with tempfile.TemporaryDirectory() as tmp:
        _arbol_l0(tmp, L0_SANA, HISTORICO_SANO)
        f48 = _t48(tmp)
        f49 = _t49(tmp, sha_fijado=_sha256_de(HISTORICO_SANO))
        ok("F0 control: árbol sano -> sin FAIL en T48 ni T49",
           f48 == [] and f49 == [], f"T48={f48} T49={f49}")

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_l0(tmp, L0_VIEJA_SINTETICA, HISTORICO_SANO)
        f48 = _t48(tmp)
        ok("F1 línea de canon/ > 1 MB FALLA (T48), con qué hacer",
           any("canon/L0/<tu ADR>.md" in x[1] for x in f48), str(f48))

    with tempfile.TemporaryDirectory() as tmp:
        _arbol_l0(tmp, L0_SANA, HISTORICO_SANO + "\n")  # HISTORICO.md tocado
        f49 = _t49(tmp, sha_fijado=_sha256_de(HISTORICO_SANO))
        ok("F2 HISTORICO.md tocado FALLA (T49), con qué hacer",
           any("no edites HISTORICO.md" in x[1] for x in f49), str(f49))

    with tempfile.TemporaryDirectory() as tmp:
        # LA MUTACIÓN EXACTA (P-A.4): "conservar ambos lados" de la rama en
        # vuelo con la L0 vieja sobre la línea reparada -- dispara las DOS
        # guardas a la vez.
        estado_conservando_ambos = L0_SANA + L0_VIEJA_SINTETICA
        historico_tocado = HISTORICO_SANO + "\nrama en vuelo coló contenido aquí\n"
        _arbol_l0(tmp, estado_conservando_ambos, historico_tocado)
        f48 = _t48(tmp)
        f49 = _t49(tmp, sha_fijado=_sha256_de(HISTORICO_SANO))
        ok("F3 'conservar ambos lados' dispara T48 Y T49 a la vez",
           f48 != [] and f49 != [], f"T48={f48} T49={f49}")

    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "canon"), exist_ok=True)
        f48 = _t48(tmp)
        ok("F4 cero archivos canon/ examinados no es un negativo (A.13)",
           any("A.13" in x[1] for x in f48), str(f48))


def main():
    print("═" * 72)
    print("  GEN2-TUBERIA-SUCESOR-1 · guardas por mutación")
    print("═" * 72)
    caso_A(); caso_B(); caso_B3(); caso_C(); caso_C4(); caso_C_adr(); caso_D(); caso_E(); caso_F(); caso_G(); caso_H()
    print("─" * 72)
    if FALLAS:
        print(f"  {len(FALLAS)} FALLA(S): " + " · ".join(FALLAS))
        return 1
    print("  TODO VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
