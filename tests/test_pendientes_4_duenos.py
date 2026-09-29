#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_pendientes_4_duenos.py -- lista cerrada de dueños del libro de NC y plantilla de los
encargos PROPUESTOS (ACTO GEN2-PENDIENTES-4 · P2/P3, 28/sep/2026).

Defecto real que atrapa (D-14): de las 334 NC ABIERTA, 239 decían «MESA (2026-10-05)» aunque solo
unas pocas eran decisiones de mesa: 171 pedían un encargo por escribir, 39 eran recetas personales,
18 esperaban al canal o a una hoja; el tablero contaba un 72 % de espera a mesa que no era de mesa
(inventario v5 §B, `forense/analisis/pendientes-4/PENDIENTES-PROGRAMA-v5.md`). Además, 42 filas
decían EN-CURSO de actos ya fusionados (#1294, #1299, #1302, #1304): un bloqueador vencido que
nadie re-verificó (A.17). A un lector le habría costado creer una cifra de espera que no medía
espera de mesa y perseguir actos que ya habían corrido.

Casos sintéticos (sin git, sin red, stdlib):
  (A) cada dueño de la lista cerrada pasa con su forma exacta; `MESA (fecha)` a secas y un
      dueño sin detalle fallan (mutación de la propia regex).
  (B) DIRECCION-ENCARGO cuyo encargo no existe falla; con encargo archivado pasa.
  (C) MESA-DECISION cuya ancla no existe en la hoja falla; una hoja sin «Opciones» o sin
      «Texto de firma» falla.
  (D) las frases «encargo por escribir» y «cierre por diseño propuesto» dentro de un `sucesor`
      ABIERTA fallan (también dentro de un `· antes:` heredado).
  (E) plantilla v2.2: un encargo sano pasa; le falta una sección / un rótulo de premisa / trae un
      verbo de funcionamiento sobre [EXISTE] / un campo por rellenar / no lista una NC que lo
      nombra → falla.
  (F) los tokens de la regex estricta y las claves de `nc_por_clase.DUENO_A_CLASE` coinciden.

Sobre el árbol real (corre en CI y no falla por trabajo de otros actos): cada encargo de
`forense/encargos/cola/PROPUESTOS/` tiene su sidecar `.cuerpo.sha256` que coincide, pasa la
plantilla y lista toda NC ABIERTA que lo nombra. Modo `--libro` (NO corre en CI): el «hecho» de
P3 sobre el libro real (dueños de la lista cerrada; frases prohibidas; MESA-DECISION ≤ renglones
de la hoja).

Corre sola:
    python3 tests/test_pendientes_4_duenos.py
    python3 tests/test_pendientes_4_duenos.py --libro
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cierre_acto as CA  # noqa: E402
import nc_por_clase as NPC  # noqa: E402

FAILS = []
PROPUESTOS = os.path.join(ROOT, "forense", "encargos", "cola", "PROPUESTOS")
HOJA = "forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md"

# Lista cerrada de dueños (encargo GEN2-PENDIENTES-4 §1 P3) más EN-CURSO para un acto que de
# verdad esté en vuelo (§4). `MESA (fecha)` a secas YA NO es un dueño: escondía tres cosas.
RE_DUENO_ESTRICTO = re.compile(
    r"^(?:DIRECCION-ENCARGO \((?P<enc>[A-Z0-9][A-Za-z0-9-]*)\)"
    r"|MESA-ACCION \((?P<fecha>\d{4}-\d{2}-\d{2})\)"
    r"|MESA-DECISION \((?P<hoja>forense/analisis/[^)\s]+\.md)#(?P<ancla>D\d+)\)"
    r"|CANAL \((?P<rama>[^)\s]+)\)"
    r"|CAJA \((?P<caja>forense/encargos/[^)\s]+\.md)\)"
    r"|ADQUISICION \([^)]+\)"
    r"|APERTURA \([^)]+\)"
    r"|EN-CURSO \([^)]+ · rama [^)\s]+\))")
FRASES_PROHIBIDAS = ("encargo por escribir", "cierre por diseño propuesto")
TOKENS_ESTRICTOS = {"DIRECCION-ENCARGO", "MESA-ACCION", "MESA-DECISION", "CANAL", "CAJA",
                    "ADQUISICION", "APERTURA", "EN-CURSO"}

SECCIONES = (r"^## 1 · OBJETIVO", r"^## 2 · FIRMAS DE MESA", r"^## 3 · LO QUE DIRECCIÓN SABE",
             r"^## 4 · YA HECHO / YA DECIDIDO", r"^## 5 · PIEZAS", r"^## 6 · LATITUD",
             r"^## 7 · PAROS", r"^## 8 · COMPUERTAS", r"^## 9 · PERÍMETRO Y CONCURRENCIA",
             r"^## 10 · LO QUE NO HACE")
RE_ROTULO_PREMISA = re.compile(r"^\s*-\s*\[(EJECUTADO|LEÍDO|EXISTE|SUPUESTO|REPORTADO)\]")
RE_VERBO_FUNC = re.compile(r"\b(mide|miden|cubre|cubren|congela|congelan|autoriza|autorizan|reproduce|reproducen)\b", re.I)


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def encargos_archivados():
    """{rótulo} de todo `forense/encargos/**/*.md` (misma indexación que la guardia de rutas)."""
    return {CA.rotulo_de_encargo(p) for p in glob.glob(os.path.join(ROOT, "forense", "encargos", "**", "*.md"),
                                                      recursive=True)}


def dueno_valido(sucesor, encargos, anclas):
    """(ok, motivo). `encargos`: rótulos archivados; `anclas`: {(ruta, 'D1'), ...} de la hoja."""
    s = (sucesor or "").strip()
    m = RE_DUENO_ESTRICTO.match(s)
    if not m:
        return False, "sucesor fuera de la lista cerrada de dueños"
    if m.group("enc") and m.group("enc").upper() not in encargos:
        return False, f"DIRECCION-ENCARGO apunta a {m.group('enc')}, sin encargo archivado"
    if m.group("caja") and CA.rotulo_de_encargo(m.group("caja")) not in encargos:
        return False, f"CAJA apunta a {m.group('caja')}, sin encargo archivado"
    if m.group("hoja") and (m.group("hoja"), m.group("ancla")) not in anclas:
        return False, f"MESA-DECISION apunta a {m.group('hoja')}#{m.group('ancla')}, ancla ausente"
    return True, ""


def frase_prohibida(sucesor):
    t = (sucesor or "").lower()
    return next((f for f in FRASES_PROHIBIDAS if f in t), None)


def parsea_hoja(texto):
    """{'D1': {'opciones': bool, 'firma': bool}} por renglón `## D<n> ·` de la hoja de decisiones."""
    out, actual = {}, None
    for linea in texto.split("\n"):
        m = re.match(r"^## (D\d+) ·", linea)
        if m:
            actual = m.group(1)
            out[actual] = {"opciones": False, "firma": False}
            continue
        if actual and re.search(r"\bOpciones\b", linea):
            out[actual]["opciones"] = True
        if actual and re.search(r"Texto de firma", linea):
            out[actual]["firma"] = True
    return out


def plantilla_fallas(texto, ncs_que_lo_nombran=()):
    """Comprobaciones mecánicas de PLANTILLA-ENCARGO-v2_2 sobre el cuerpo de un encargo."""
    f = []
    lineas = texto.split("\n")
    if not lineas or not lineas[0].startswith("# ENCARGO · ACTO "):
        f.append("primera línea no es «# ENCARGO · ACTO <RÓTULO> · …»")
    if not re.search(r"^> ENTORNO: \*\*(NUBE|CAJA)\*\*", texto, re.M):
        f.append("sin línea «> ENTORNO: **NUBE|CAJA**»")
    if not re.search(r"MODO: \*\*(ABIERTO|RÍGIDO|AUTÓNOMO-AMPLIO)\*\*", texto):
        f.append("CABECERA sin «MODO: **ABIERTO|RÍGIDO|AUTÓNOMO-AMPLIO**»")
    for c in ("SHA de redacción", "MODELO"):
        if c not in texto:
            f.append(f"CABECERA sin «{c}»")
    for pat in SECCIONES:
        if not re.search(pat, texto, re.M):
            f.append(f"falta la sección {pat[3:]}")
    if "Si te encuentras escribiendo fuera de esta lista, PARA." not in texto:
        f.append("§9 sin la frase «Si te encuentras escribiendo fuera de esta lista, PARA.»")
    if "ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO" not in texto:
        f.append("§9 sin «ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO»")
    s3 = re.search(r"^## 3 · LO QUE DIRECCIÓN SABE(.*?)^## 4 ", texto, re.M | re.S)
    premisas = [l for l in (s3.group(1).split("\n") if s3 else []) if re.match(r"^\s*-\s", l)]
    if not premisas:
        f.append("§3 sin premisas rotuladas")
    for l in premisas:
        if not RE_ROTULO_PREMISA.match(l):
            f.append(f"premisa sin rótulo válido: {l.strip()[:60]}")
        elif re.match(r"^\s*-\s*\[(EXISTE|SUPUESTO|REPORTADO)\]", l) and RE_VERBO_FUNC.search(l):
            f.append(f"verbo de funcionamiento sobre premisa {l.strip()[:40]}…")
    if "___" in texto or re.search(r"^(PR|ESTADO|BITACORA)\s*:", texto, re.M):
        f.append("campo por rellenar o línea de estado en el cuerpo (rompe el sello, A.3)")
    if re.search(r"^## (CONSUMIDO|NO-CORRIDO)", texto, re.M):
        f.append("trae ## CONSUMIDO / ## NO-CORRIDO: los añade /acto al archivarlo")
    obj = re.search(r"^## 1 · OBJETIVO(.*?)^## 2 ", texto, re.M | re.S)
    if not obj or not re.search(r"`(python3|git|rg|grep|jq|yq|wc)\b[^`]*`", obj.group(1)):
        f.append("§1: «Hecho» sin un comando verificable entre comillas invertidas")
    for nc in ncs_que_lo_nombran:
        if nc not in texto:
            f.append(f"no lista la NC que lo nombra: {nc}")
    return f


CUERPO_SANO = """# ENCARGO · ACTO GEN2-SINTETICO-1 · prueba

> ENTORNO: **NUBE** — libro de NC.

CABECERA · SHA de redacción `abc` · una sola sesión · MODELO: **Opus** · MODO: **ABIERTO**

## 1 · OBJETIVO
Algo. «Hecho»: `python3 tools/nc_por_clase.py --json` → 0.

## 2 · FIRMAS DE MESA
Ninguna.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] corrí `wc -l` → 3.
- [EXISTE] el archivo está en la ruta.

## 4 · YA HECHO / YA DECIDIDO
NC-S-01 absorbida.

## 5 · PIEZAS
P1.

## 6 · LATITUD
Del ejecutor.

## 7 · PAROS
Lista cerrada.

## 8 · COMPUERTAS
«x» protege: borrar.

## 9 · PERÍMETRO Y CONCURRENCIA
ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO: ninguno verificado.
«Si te encuentras escribiendo fuera de esta lista, PARA.» Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · LO QUE NO HACE
Nada.
"""


def caso_a():
    enc = {"GEN2-CALC-ALTERNOS-LOTE-2", "GEN2-DESTINO-ARCHIVADO-1"}
    anc = {(HOJA, "D1")}
    buenos = [
        "DIRECCION-ENCARGO (GEN2-CALC-ALTERNOS-LOTE-2) · antes: algo",
        "MESA-ACCION (2026-10-05) · receta",
        f"MESA-DECISION ({HOJA}#D1) · antes: algo",
        "CANAL (derivados/auto-36495085433) · espera el [deriva]",
        "CAJA (forense/encargos/2026-09-28-GEN2-DESTINO-ARCHIVADO-1.md)",
        "ADQUISICION (ENCIG tasa nacional)",
        "APERTURA (ENVIPE 2026, firma pendiente)",
        "EN-CURSO (GEN2-ACTO-VIVO · rama acto/gen2-acto-vivo)",
    ]
    for s in buenos:
        ok, why = dueno_valido(s, enc, anc)
        afirma(ok, f"(A) debe pasar: {s[:50]} -> {why}")
    malos = [
        "MESA (2026-10-05) · encargo por escribir",
        "MESA (2026-10-05)",
        "CANAL",
        "CANAL ()",
        "MESA-ACCION (pronto)",
        "MESA-ACCION (2026-10-5)",
        "DIRECCION-ENCARGO ()",
        "DIRECCION-ENCARGO (gen2 x)",
        "EN-CURSO (GEN2-X)",
        "SIN-ASIGNAR",
        "",
        "prosa sin dueño",
    ]
    for s in malos:
        ok, _ = dueno_valido(s, enc, anc)
        afirma(not ok, f"(A) debe fallar: {s[:50]!r}")


def caso_b():
    enc = {"GEN2-DESTINO-ARCHIVADO-1"}
    ok, _ = dueno_valido("DIRECCION-ENCARGO (GEN2-DESTINO-ARCHIVADO-1)", enc, set())
    afirma(ok, "(B) DIRECCION-ENCARGO con encargo archivado pasa")
    ok, _ = dueno_valido("DIRECCION-ENCARGO (GEN2-NO-EXISTE-9)", enc, set())
    afirma(not ok, "(B) DIRECCION-ENCARGO a encargo inexistente falla")
    ok, _ = dueno_valido("CAJA (forense/encargos/2026-09-28-GEN2-NO-EXISTE-9.md)", enc, set())
    afirma(not ok, "(B) CAJA a encargo inexistente falla")


def caso_c():
    ok, _ = dueno_valido(f"MESA-DECISION ({HOJA}#D2)", set(), {(HOJA, "D1")})
    afirma(not ok, "(C) MESA-DECISION con ancla ausente falla")
    ok, _ = dueno_valido(f"MESA-DECISION ({HOJA}#D1)", set(), {(HOJA, "D1")})
    afirma(ok, "(C) MESA-DECISION con ancla presente pasa")
    h = parsea_hoja("## D1 · x\n**Opciones:** (a) y (b)\n**Texto de firma:** «z»\n## D2 · sin firma\n**Opciones:** (a)\n"
                    "## D3 · sin opciones\nTexto de firma: q\n")
    afirma(h["D1"] == {"opciones": True, "firma": True}, f"(C) D1 completo: {h['D1']}")
    afirma(h["D2"] == {"opciones": True, "firma": False}, f"(C) D2 sin firma detectado: {h['D2']}")
    afirma(h["D3"] == {"opciones": False, "firma": True}, f"(C) D3 sin opciones detectado: {h['D3']}")


def caso_d():
    afirma(frase_prohibida("MESA (2026-10-05) · encargo por escribir: x") == "encargo por escribir", "(D) frase 1")
    afirma(frase_prohibida("CANAL (r) · antes: MESA · Cierre por diseño propuesto") == "cierre por diseño propuesto",
           "(D) frase 2 dentro de un «antes:» y con mayúscula")
    afirma(frase_prohibida("DIRECCION-ENCARGO (GEN2-X-2) · antes: redactar el encargo pendiente") is None,
           "(D) sin frase prohibida pasa")


def caso_e():
    afirma(plantilla_fallas(CUERPO_SANO, ("NC-S-01",)) == [], f"(E) cuerpo sano: {plantilla_fallas(CUERPO_SANO, ('NC-S-01',))}")
    muts = {
        "sin sección 7": CUERPO_SANO.replace("## 7 · PAROS", "## 7 · OTRA COSA"),
        "premisa sin rótulo": CUERPO_SANO.replace("- [EXISTE]", "- "),
        "verbo sobre EXISTE": CUERPO_SANO.replace("el archivo está en la ruta", "el archivo mide la ruta"),
        "campo por rellenar": CUERPO_SANO + "\nPR: ___\n",
        "trae CONSUMIDO": CUERPO_SANO + "\n## CONSUMIDO\n",
        "sin frase de perímetro": CUERPO_SANO.replace("Si te encuentras escribiendo fuera de esta lista, PARA.", ""),
        "hecho sin comando": CUERPO_SANO.replace("`python3 tools/nc_por_clase.py --json`", "una revisión"),
        "sin MODO": CUERPO_SANO.replace("**ABIERTO**", "libre"),
    }
    for nombre, cuerpo in muts.items():
        afirma(plantilla_fallas(cuerpo, ("NC-S-01",)), f"(E) mutación debe fallar: {nombre}")
    afirma(plantilla_fallas(CUERPO_SANO, ("NC-S-99",)), "(E) NC que lo nombra y no lista debe fallar")


HISTORICOS = {"MESA", "DIRECCION"}   # los clasifica `nc_por_clase` (filas históricas o de otro acto); la guardia estricta los rechaza


def caso_f():
    conocidos = set(NPC.DUENO_A_CLASE)
    afirma(conocidos - TOKENS_ESTRICTOS == HISTORICOS,
           f"(F) el clasificador conoce tokens que la regex estricta no admite y no son los históricos declarados: "
           f"{conocidos - TOKENS_ESTRICTOS - HISTORICOS} (históricos esperados {HISTORICOS})")
    afirma(TOKENS_ESTRICTOS <= conocidos,
           f"(F) la regex estricta admite un token que el clasificador no clasifica: {TOKENS_ESTRICTOS - conocidos}")
    for h in HISTORICOS:
        ok, _ = dueno_valido(f"{h} (2026-10-05) · x", set(), set())
        afirma(not ok, f"(F) el token histórico {h} debe ser rechazado por la guardia estricta")


def _filas_libro():
    return CA.lee_nc(CA._leer(os.path.join(ROOT, "forense", "no-corrido.tsv")))


def arbol_real():
    """PROPUESTOS del árbol: sidecar, plantilla y NC listadas (no falla por trabajo ajeno)."""
    if not os.path.isdir(PROPUESTOS):
        return
    filas = _filas_libro()
    for p in sorted(glob.glob(os.path.join(PROPUESTOS, "*.md"))):
        rel = os.path.relpath(p, ROOT)
        rotulo = CA.rotulo_de_encargo(p)
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "sella_sha256.py"), "--verifica", "--cuerpo", p],
                           capture_output=True, text=True)
        afirma(r.returncode == 0 and "SELLO_COINCIDE" in r.stdout, f"(árbol) sidecar de cuerpo no coincide: {rel}: {r.stdout[:80]}{r.stderr[:80]}")
        texto = open(p, encoding="utf-8").read()
        nombran = [f["id"] for f in filas if (f.get("estado") or "").strip() == "ABIERTA"
                   and re.match(rf"^DIRECCION-ENCARGO \({re.escape(rotulo)}\)", (f.get("sucesor") or "").strip())]
        for falla in plantilla_fallas(texto, nombran):
            afirma(False, f"(árbol) {rel}: {falla}")


def libro():
    """Modo `--libro`: el «hecho» de P3 sobre el libro real."""
    filas = _filas_libro()
    abiertas = [f for f in filas if (f.get("estado") or "").strip() == "ABIERTA"]
    enc = encargos_archivados()
    hoja_txt = ""
    ruta_hoja = os.path.join(ROOT, HOJA)
    if os.path.exists(ruta_hoja):
        hoja_txt = open(ruta_hoja, encoding="utf-8").read()
    h = parsea_hoja(hoja_txt)
    anclas = {(HOJA, k) for k in h}
    fuera, frases, decision = [], [], 0
    for f in abiertas:
        s = (f.get("sucesor") or "").strip()
        ok, why = dueno_valido(s, enc, anclas)
        if not ok:
            fuera.append((f["id"], why))
        fr = frase_prohibida(s)
        if fr:
            frases.append((f["id"], fr))
        if s.startswith("MESA-DECISION"):
            decision += 1
    incompletas = [k for k, v in h.items() if not (v["opciones"] and v["firma"])]
    print(f"libro: {len(filas)} filas · {len(abiertas)} ABIERTA · fuera de la lista cerrada: {len(fuera)} · "
          f"con frase prohibida: {len(frases)} · MESA-DECISION {decision} ≤ renglones de la hoja {len(h)} · "
          f"renglones sin opciones/firma: {len(incompletas)}")
    for fid, why in fuera[:40]:
        print(f"  fuera: {fid}: {why}")
    for fid, fr in frases[:20]:
        print(f"  frase: {fid}: «{fr}»")
    for k in incompletas:
        print(f"  hoja: {k} sin opciones o sin texto de firma")
    mal = bool(fuera or frases or incompletas or decision > len(h))
    if decision > len(h):
        print(f"  MESA-DECISION {decision} > renglones {len(h)}")
    return 1 if mal else 0


def plantilla_cli(args):
    """`--plantilla <archivo.md> [NC-id ...]`: comprobaciones mecánicas de PLANTILLA v2.2 sobre un borrador."""
    if not args:
        print("uso: --plantilla <archivo.md> [NC-id ...]")
        return 2
    texto = open(args[0], encoding="utf-8").read()
    fallas = plantilla_fallas(texto, tuple(args[1:]))
    for f in fallas:
        print("FALLA:", f)
    print(f"plantilla v2.2 · {args[0]} · {len(fallas)} falla(s) · NC exigidas {len(args) - 1}")
    return 1 if fallas else 0


def main():
    if "--plantilla" in sys.argv:
        return plantilla_cli(sys.argv[sys.argv.index("--plantilla") + 1:])
    if "--libro" in sys.argv:
        return libro()
    caso_a()
    caso_b()
    caso_c()
    caso_d()
    caso_e()
    caso_f()
    arbol_real()
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        return 1
    print("OK test_pendientes_4_duenos (A-F + árbol real)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
