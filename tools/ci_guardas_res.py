#!/usr/bin/env python3
"""Las seis guardas de identidad `RES`/llave lógica (G1..G6).

ACTO `GEN2-TUBERIA-RES-LLAVE-1`, P6. Firma de mesa 21/sep/2026.

Cada guarda con el defecto REAL que atrapa (§1: el aparato tiene costo)
=====================================================================
  G1 registro inmutable    un par llave->numero de la base que cambia en el
                           PR. Defecto: la deriva medida -- 135 de 208 llaves
                           han tenido mas de un numero.
  G2 sin reuso             un numero retirado reasignado. Defecto: un pin
                           viejo que re-apunta a un slot nuevo.
  G3 citas nuevas          una spec añadida o tocada que cita un `RES` que no
                           existe en el registro de la BASE, o que cita
                           `CORR`. Defecto: las 19 citas selladas que hoy
                           nombran otra cosa.
  G4 sin citas colgantes   una llave citada por `pines-de-mesa.tsv` o por la
                           tabla de P4 que no existe vigente ni se resuelve
                           por un alias declarado. Defecto: los 4 renombres.
  G5 tabla completa        una cita `RES`/`CORR` en una spec sellada sin fila
                           en la tabla de P4. Defecto: una spec sellada que
                           la vista no sabe leer.
  G6 biyeccion             una llave vigente con dos numeros, un numero con
                           dos llaves, o una llave vigente que es a la vez
                           alias de otra. Defecto: el registro del diff v1.0,
                           donde el nombre viejo y el nuevo quedaban vivos
                           apuntando al mismo numero.

Historia y base
===============
G2, G4, G5 y G6 NO necesitan historia de git. G1 y G3 SI necesitan la ref
base, porque comparan contra el registro de `main`. En CI corren en un job con
su propio clonado que la traiga: este modulo **nunca hace `fetch`** (D-23, una
herramienta de verificacion no muta el clon que verifica). Si la ref base no
esta disponible, G1 y G3 devuelven `NO-VERIFICABLE-AQUI` -- que no es un
aprobado y no se degrada a uno (A.4).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools"))

import corrida0  # noqa: E402
import pines_mesa  # noqa: E402
import resuelve_citas  # noqa: E402

RUTA_REGISTRO = "data/corrida0/registro-res.tsv"
NO_VERIFICABLE = "NO-VERIFICABLE-AQUI"


class Guarda:
    """Resultado de una guarda: PASA, FALLA o NO-VERIFICABLE-AQUI."""

    def __init__(self, id_: str, estado: str, motivos=()):
        self.id = id_
        self.estado = estado
        self.motivos = list(motivos)

    def __repr__(self):
        return f"<{self.id} {self.estado} {len(self.motivos)}>"


def _git(*args, repo: Path = None):
    return subprocess.run(["git", "-C", str(repo or RAIZ), *args],
                          capture_output=True, text=True)


def _registro_de_la_base(base: str, repo: Path = None) -> dict | None:
    r = _git("show", f"{base}:{RUTA_REGISTRO}", repo=repo)
    if r.returncode != 0:
        return None
    return _parsea_registro(r.stdout)


def _parsea_registro(texto: str) -> dict:
    """`llave -> (numero, estado)` con el estado de la ULTIMA fila."""
    estado: dict[str, tuple] = {}
    lineas = [l for l in texto.splitlines() if l and not l.startswith("#")]
    if not lineas:
        return estado
    cols = lineas[0].split("\t")
    for linea in lineas[1:]:
        f = dict(zip(cols, linea.split("\t")))
        if not f.get("llave_logica"):
            continue
        estado[f["llave_logica"]] = (f["resultado_id"], f.get("estado", ""))
    return estado


# ── G1 ─────────────────────────────────────────────────────────────────────

def g1_registro_inmutable(base: str, repo: Path = None,
                          registro_actual: dict = None) -> Guarda:
    """Ningun par llave->numero que YA estaba en la base cambia en el PR.

    Una llave nueva, o una que pasa de vigente a retirada, no es un cambio de
    PAR: lo prohibido es que la misma llave cambie de NUMERO.
    """
    de_base = _registro_de_la_base(base, repo)
    if de_base is None:
        return Guarda("G1", NO_VERIFICABLE,
                      [f"no se pudo leer {RUTA_REGISTRO} en {base!r} -- este "
                       f"job necesita un clon con la ref base, y esta "
                       f"herramienta no hace fetch (D-23)"])
    if registro_actual is None:
        registro_actual = _parsea_registro(
            (RAIZ / RUTA_REGISTRO).read_text(encoding="utf-8")
            if (RAIZ / RUTA_REGISTRO).exists() else "")
    motivos = []
    for llave, (numero, _) in de_base.items():
        ahora = registro_actual.get(llave)
        if ahora is None:
            motivos.append(f"G1: {llave} estaba en la base con {numero} y "
                           f"DESAPARECIO del registro -- el registro es "
                           f"solo-añadir, una llave se retira, no se borra")
        elif ahora[0] != numero:
            motivos.append(f"G1: {llave} cambio de {numero} a {ahora[0]} -- "
                           f"un par llave->numero de la base no cambia")
    return Guarda("G1", "FALLA" if motivos else "PASA", motivos)


# ── G2 ─────────────────────────────────────────────────────────────────────

def g2_sin_reuso(filas: list = None) -> Guarda:
    """Un numero retirado no se reasigna NUNCA."""
    filas = filas if filas is not None else corrida0.lee_registro_res()
    retirados: dict[str, str] = {}   # numero -> llave que lo retiro
    motivos = []
    for f in filas:
        numero, llave, estado = f["resultado_id"], f["llave_logica"], f["estado"]
        if estado == corrida0.REG_RETIRADO:
            retirados[numero] = llave
        elif numero in retirados and retirados[numero] != llave:
            motivos.append(
                f"G2: {numero} se retiro de {retirados[numero]} y se "
                f"reasigno a {llave} -- un numero retirado no se reusa")
    return Guarda("G2", "FALLA" if motivos else "PASA", motivos)


# ── G3 ─────────────────────────────────────────────────────────────────────

def _specs_tocadas(base: str, repo: Path = None) -> list[str] | None:
    r = _git("diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD",
             repo=repo)
    if r.returncode != 0:
        return None
    return [l for l in r.stdout.splitlines()
            if re.fullmatch(r"data/corrida0/[^/]+/spec\.(md|yaml)", l)]


def g3_citas_nuevas(base: str, repo: Path = None) -> Guarda:
    """Una spec AÑADIDA O TOCADA no cita un `RES` que no exista en el registro
    de la base, y no cita `CORR` en absoluto (D-r2: `CORR` dejo de ser
    citable). Una spec que el PR no toca no se juzga: sus citas viejas viven
    en la tabla de P4."""
    tocadas = _specs_tocadas(base, repo)
    if tocadas is None:
        return Guarda("G3", NO_VERIFICABLE,
                      [f"no se pudo diffear contra {base!r} -- este job "
                       f"necesita un clon con la ref base (D-23)"])
    de_base = _registro_de_la_base(base, repo)
    # Si la BASE aun no tiene registro (el commit anterior a este acto), la
    # mitad `RES` de G3 no se puede juzgar y se declara -- pero la mitad
    # `CORR` si, porque no depende del registro. No se colapsan (A.4).
    vigentes_base = (None if de_base is None else
                     {n for n, e in de_base.values()
                      if e == corrida0.REG_VIGENTE})
    motivos = []
    sin_juzgar = []
    for rel in tocadas:
        ruta = (repo or RAIZ) / Path(rel)
        if not ruta.exists():
            continue
        texto = ruta.read_text(encoding="utf-8", errors="replace")
        for n in sorted(set(resuelve_citas.RE_CORR.findall(texto))):
            motivos.append(
                f"G3: {rel} cita CORR-{n} -- `CORR` dejo de ser citable "
                f"(D-r2, firmada 21/sep/2026): no tiene llave natural, su "
                f"conjunto de slots cambia. Cita los slots por llave.")
        for n in sorted(set(resuelve_citas.RE_RES.findall(texto))):
            token = f"RES-{n}"
            if vigentes_base is None:
                sin_juzgar.append(f"{rel}:{token}")
            elif token not in vigentes_base:
                motivos.append(
                    f"G3: {rel} cita {token}, que no existe vigente en el "
                    f"registro de la base -- un slot nuevo se cita POR LLAVE "
                    f"hasta que su numero entra a main; si otro PR fusiona "
                    f"antes, el numero provisional cambia")
    if motivos:
        return Guarda("G3", "FALLA", motivos)
    if sin_juzgar:
        return Guarda("G3", NO_VERIFICABLE,
                      [f"la base {base!r} no tiene {RUTA_REGISTRO}: la mitad "
                       f"`CORR` de G3 PASA, la mitad `RES` no se juzgo sobre "
                       f"{len(sin_juzgar)} cita(s): {sin_juzgar[:5]}"])
    return Guarda("G3", "PASA", [])


# ── G4 ─────────────────────────────────────────────────────────────────────

def g4_sin_citas_colgantes(vigentes: dict = None, retiradas: dict = None,
                           alias: dict = None, pines: list = None,
                           tabla: list = None) -> Guarda:
    """Toda llave citada por `pines-de-mesa.tsv` o por la tabla de P4 existe
    vigente, o se resuelve por un alias declarado por su consumidor."""
    if vigentes is None:
        vigentes, _, retiradas = corrida0.estado_registro_res()
    retiradas = retiradas if retiradas is not None else {}
    alias = (alias if alias is not None
             else corrida0.alias_declarados_por_consumidores())
    # llave VIEJA -> llave VIGENTE que la declara como alias
    sucedida = {vieja: nueva for nueva, viejas in alias.items()
                for vieja in viejas}
    pines = pines if pines is not None else pines_mesa.lee_pines()
    tabla = tabla if tabla is not None else resuelve_citas.lee_tabla()

    def resuelve(llave: str) -> bool:
        if llave in vigentes:
            return True
        return sucedida.get(llave) in vigentes

    motivos = []
    for fila in pines:
        llave = fila["llave_logica"]
        if not resuelve(llave):
            motivos.append(
                f"G4: pines-de-mesa.tsv cita {llave}, que no existe vigente "
                f"ni la sucede un alias declarado por su consumidor")
    for fila in tabla:
        crudo = fila.get("llave_logica") or ""
        if crudo == resuelve_citas.NO_RESUELVE:
            continue
        for llave in crudo.split(";"):
            if not llave or llave.startswith("<"):
                continue
            if not resuelve(llave):
                motivos.append(
                    f"G4: {fila['calc_id']}/{fila['token']} resuelve a "
                    f"{llave}, que no existe vigente ni la sucede un alias "
                    f"declarado -- un consumidor renombro sin declararlo")
    return Guarda("G4", "FALLA" if motivos else "PASA", motivos)


# ── G5 ─────────────────────────────────────────────────────────────────────

def g5_tabla_completa(tabla: list = None, sellados: list = None) -> Guarda:
    """Toda cita `RES`/`CORR` de una spec SELLADA tiene fila en la tabla."""
    tabla = tabla if tabla is not None else resuelve_citas.lee_tabla()
    tiene = {(f["calc_id"], f["token"]) for f in tabla}
    sellados = (sellados if sellados is not None
                else resuelve_citas.calc_sellados())
    motivos = []
    for calc in sellados:
        for spec in resuelve_citas._specs_de(calc):
            texto = spec.read_text(encoding="utf-8", errors="replace")
            tokens = ({f"RES-{n}" for n in resuelve_citas.RE_RES.findall(texto)}
                      | {f"CORR-{n}"
                         for n in resuelve_citas.RE_CORR.findall(texto)})
            for token in sorted(tokens):
                if (calc, token) not in tiene:
                    motivos.append(
                        f"G5: {calc} cita {token} en "
                        f"{spec.relative_to(RAIZ)} y no tiene fila en la "
                        f"tabla de citas selladas -- la vista no sabe leer "
                        f"esa spec. Re-derivala: "
                        f"`python3 tools/resuelve_citas.py tabla --escribe`")
    return Guarda("G5", "FALLA" if motivos else "PASA", motivos)


# ── G6 ─────────────────────────────────────────────────────────────────────

def g6_biyeccion(vigentes: dict = None, alias: dict = None) -> Guarda:
    """Entre las llaves VIGENTES: una llave, un numero; un numero, una llave;
    y una llave vigente no es ademas alias de otra llave vigente."""
    if vigentes is None:
        vigentes, _, _ = corrida0.estado_registro_res()
    alias = (alias if alias is not None
             else corrida0.alias_declarados_por_consumidores())
    motivos = []
    por_numero: dict[str, list] = {}
    for llave, numero in vigentes.items():
        por_numero.setdefault(numero, []).append(llave)
    for numero, llaves in sorted(por_numero.items()):
        if len(llaves) > 1:
            motivos.append(
                f"G6: {numero} apunta a {len(llaves)} llaves vigentes: "
                f"{sorted(llaves)} -- un numero, una llave")
    for nueva, viejas in sorted(alias.items()):
        for vieja in viejas:
            if vieja in vigentes and nueva in vigentes:
                motivos.append(
                    f"G6: {vieja} esta VIGENTE y ademas {nueva} la declara "
                    f"como alias -- el nombre viejo y el nuevo no pueden "
                    f"estar vivos a la vez")
    return Guarda("G6", "FALLA" if motivos else "PASA", motivos)


# ── corredor ───────────────────────────────────────────────────────────────

SIN_HISTORIA = ("G2", "G4", "G5", "G6")
CON_HISTORIA = ("G1", "G3")


def corre(base: str = "", repo: Path = None) -> list[Guarda]:
    guardas = [g2_sin_reuso(), g4_sin_citas_colgantes(), g5_tabla_completa(),
               g6_biyeccion()]
    if base:
        guardas = [g1_registro_inmutable(base, repo),
                   g3_citas_nuevas(base, repo)] + guardas
    return sorted(guardas, key=lambda g: g.id)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--base", default="",
                   help="ref base para G1 y G3 (p. ej. origin/main). Sin "
                        "ella, G1 y G3 no corren y se declara por que.")
    args = p.parse_args(argv)
    guardas = corre(args.base)
    fallas = 0
    for g in guardas:
        print(f"[{g.estado}] {g.id}")
        for m in g.motivos:
            print(f"    {m}")
        if g.estado == "FALLA":
            fallas += 1
    if not args.base:
        print(f"\nG1 y G3 NO CORRIERON: necesitan la ref base "
              f"(`--base origin/main`) en un job con su propio clonado; esta "
              f"herramienta no hace fetch (D-23).")
    print(f"\nguardas_corridas = {len(guardas)} · fallas = {fallas}")
    return 1 if fallas else 0


if __name__ == "__main__":
    raise SystemExit(main())
