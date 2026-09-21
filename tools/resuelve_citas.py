#!/usr/bin/env python3
"""Resuelve una cita `RES-####` / `CORR-####` AL MOMENTO EN QUE SE ESCRIBIO.

ACTO `GEN2-TUBERIA-RES-LLAVE-1`, P4. Firma de mesa 21/sep/2026.

Por que existe
==============
`RES-####` era POSICIONAL (`corrida0.py`, `RES-{i:04d}`) y `CORR-####` iba por
orden de grupo. MEDIDO sobre la historia completa de los dos derivados: 135 de
208 llaves logicas han tenido mas de un numero, y 82 de 86 numeros `CORR` han
nombrado mas de un instrumento. Una spec SELLADA no se puede reescribir (E.3),
asi que su cita quedo apuntando a otro slot **en silencio**: el numero cambio
de dueño debajo del texto.

Desde este acto el numero se congela (`data/corrida0/registro-res.tsv`), asi
que el problema deja de CRECER. Lo que ya se escribio se arregla de la unica
forma honesta: resolviendo cada cita contra la demanda **del commit que fijo
esa spec por ultima vez**, y guardando el resultado en
`data/corrida0/pines-sellados-resueltos.tsv`.

`CORR` no tiene llave natural -- su unica identidad inyectiva es el conjunto de
llaves de sus slots, y ese conjunto cambia en cuanto un slot entra al grupo.
Por eso una cita `CORR` se resuelve a **las llaves que el grupo tenia en ese
momento**, y un slot que entro despues ya no recibe credito (D-r2, firmada).

Lo que este modulo NO hace
==========================
No edita ninguna spec (estan selladas), no numera nada, no adopta nada. Lee
historia de git y escribe una sola tabla derivada.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

# `data/corrida0/corridas.tsv` trae campos enormes (listas de inputs de una
# corrida): el limite por defecto de `csv` los rompe.
csv.field_size_limit(10_000_000)

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools"))

import pines_mesa  # noqa: E402

CORRIDAS_DIR = RAIZ / "data" / "corrida0"
SALIDA = CORRIDAS_DIR / "pines-sellados-resueltos.tsv"
DEMANDA_RES = "data/corrida0/demanda-resultados.tsv"
DEMANDA_CORR = "data/corrida0/demanda-corridas.tsv"

RE_RES = re.compile(r"\bRES-(\d{4})\b")
RE_CORR = re.compile(r"\bCORR-(\d{4})\b")

CABECERA_DERIVADO = "# DERIVADO — NO EDITAR"
COLUMNAS = ["calc_id", "spec", "token", "commit_spec", "fecha_commit",
            "llave_logica", "numero_hoy", "difiere_de_hoy"]

NO_RESUELVE = "NO-RESUELVE-EN-ESE-COMMIT"


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(RAIZ), *args],
                          capture_output=True, text=True, check=True).stdout


def _tsv(texto: str) -> list[dict]:
    lineas = [l for l in texto.splitlines(True) if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


_CACHE: dict = {}


def demanda_en(commit: str) -> tuple[dict, dict]:
    """`(RES -> llave_logica, CORR -> [llaves])` tal como estaban en `commit`.

    Un consumidor cuyo archivo no tenia espacio logico en ese momento se
    devuelve con su consumidor crudo entre `<>`: es informacion, no un hueco.
    """
    if commit in _CACHE:
        return _CACHE[commit]
    try:
        res_txt = _git("show", f"{commit}:{DEMANDA_RES}")
    except subprocess.CalledProcessError:
        _CACHE[commit] = ({}, {})
        return _CACHE[commit]
    por_res: dict[str, str] = {}
    por_corr: dict[str, list] = {}
    for f in _tsv(res_txt):
        consumidor = f.get("consumidor") or ""
        try:
            llave = pines_mesa.llave_logica(consumidor)
        except pines_mesa.PinInvalido:
            llave = f"<{consumidor}>"
        por_res[f["resultado_id"]] = llave
        corr = (f.get("corrida_natural") or "").strip()
        if corr:
            por_corr.setdefault(corr, []).append(llave)
    _CACHE[commit] = (por_res, por_corr)
    return _CACHE[commit]


def resuelve(token: str, commit: str) -> list[str]:
    """Las llaves que `token` nombraba en `commit`. Vacio si no resolvia."""
    por_res, por_corr = demanda_en(commit)
    if token.startswith("RES-"):
        llave = por_res.get(token)
        return [llave] if llave else []
    return list(por_corr.get(token, ()))


def _specs_de(calc_id: str) -> list[Path]:
    d = CORRIDAS_DIR / calc_id
    return sorted(p for p in (d / "spec.md", d / "spec.yaml") if p.exists())


def calc_sellados() -> list[str]:
    """CALC cuyo `estado` en `data/corrida0/corridas.tsv` empieza por SELLADA
    o SUPERADO -- una spec sellada es la que ya no se puede reescribir."""
    txt = (CORRIDAS_DIR / "corridas.tsv").read_text(encoding="utf-8")
    ids = []
    for f in _tsv(txt):
        if f.get("origen") != "OFERTA":
            continue
        if str(f.get("estado") or "").startswith(("SELLADA", "SUPERADO")):
            ids.append(f["spec_id"])
    return sorted(dict.fromkeys(ids))


def _commit_de(ruta: Path) -> tuple[str, str]:
    rel = str(ruta.relative_to(RAIZ))
    salida = _git("log", "-1", "--format=%H\t%ad", "--date=short", "--", rel)
    if not salida.strip():
        return ("SIN-COMMIT", "")
    sha, _, fecha = salida.strip().partition("\t")
    return (sha, fecha)


def construye_tabla() -> list[dict]:
    hoy_res, hoy_corr = demanda_en("HEAD")
    hoy_por_llave = {v: k for k, v in hoy_res.items()}
    filas: list[dict] = []
    for calc in calc_sellados():
        # Una fila por CITA, es decir por par (CALC, token): `spec.md` y
        # `spec.yaml` son la MISMA spec, y una cita que aparece en los dos no
        # es dos citas. El campo `spec` lista los archivos que la llevan.
        donde: dict[str, list[Path]] = {}
        for spec in _specs_de(calc):
            texto = spec.read_text(encoding="utf-8", errors="replace")
            for token in ({f"RES-{n}" for n in RE_RES.findall(texto)} |
                          {f"CORR-{n}" for n in RE_CORR.findall(texto)}):
                donde.setdefault(token, []).append(spec)
        for token in sorted(donde):
            archivos = donde[token]
            # El commit que fijo la spec por ULTIMA vez entre los archivos que
            # llevan la cita: es el momento contra el que se resuelve.
            anclas = [_commit_de(p) for p in archivos]
            commit, fecha = max(anclas, key=lambda cf: cf[1])
            spec = ";".join(str(p.relative_to(RAIZ)) for p in archivos)
            llaves = resuelve(token, commit)
            if not llaves:
                filas.append({
                    "calc_id": calc, "spec": spec,
                    "token": token, "commit_spec": commit,
                    "fecha_commit": fecha, "llave_logica": NO_RESUELVE,
                    "numero_hoy": "", "difiere_de_hoy": "NO-VERIFICABLE"})
                continue
            if token.startswith("RES-"):
                numero_hoy = hoy_por_llave.get(llaves[0], "")
                difiere = "SI" if numero_hoy != token else "NO"
            else:
                hoy = set(hoy_corr.get(token, ()))
                difiere = "SI" if hoy != set(llaves) else "NO"
                numero_hoy = token if difiere == "NO" else ""
            filas.append({
                "calc_id": calc, "spec": spec,
                "token": token, "commit_spec": commit,
                "fecha_commit": fecha,
                "llave_logica": ";".join(llaves),
                "numero_hoy": numero_hoy, "difiere_de_hoy": difiere})
    return filas


def lee_tabla(ruta: Path = SALIDA) -> list[dict]:
    if not Path(ruta).exists():
        return []
    return _tsv(Path(ruta).read_text(encoding="utf-8"))


def escribe_tabla(filas: list[dict], ruta: Path = SALIDA) -> None:
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with Path(ruta).open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(CABECERA_DERIVADO + "\n")
        fh.write("# Una fila por CITA `RES`/`CORR` en la spec de un CALC "
                 "SELLADO, resuelta contra la demanda del commit que fijo esa "
                 "spec.\n")
        fh.write("# Lo escribe `python3 tools/resuelve_citas.py tabla "
                 "--escribe`. Las specs NO se tocan: estan selladas.\n")
        fh.write("\t".join(COLUMNAS) + "\n")
        for f in filas:
            fh.write("\t".join(str(f.get(c, "")) for c in COLUMNAS) + "\n")


def cmd_tabla(args) -> int:
    filas = construye_tabla()
    difieren = [f for f in filas if f["difiere_de_hoy"] == "SI"]
    print(f"filas = {len(filas)}")
    print(f"citas_RES = {sum(1 for f in filas if f['token'].startswith('RES'))}")
    print(f"citas_CORR = "
          f"{sum(1 for f in filas if f['token'].startswith('CORR'))}")
    print(f"specs = {len({f['spec'] for f in filas})}")
    print(f"difieren_de_lo_que_el_numero_nombra_hoy = {len(difieren)}")
    for f in difieren:
        print(f"  {f['calc_id']}  {f['token']}  -> {f['llave_logica']}")
    if args.escribe:
        escribe_tabla(filas)
        print(f"\nESCRITO: {SALIDA.relative_to(RAIZ)}")
    else:
        print("\nDIAGNOSTICO: nada escrito. Para escribir, `--escribe`.")
    return 0


def cmd_que_nombraba(args) -> int:
    """«Que nombraba `RES-X` (o `CORR-X`) en tal commit/fecha.»

    Sale gratis: es la misma funcion que construye la tabla.
    """
    ref = args.ref
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", ref):
        salida = _git("rev-list", "-1", f"--before={ref} 23:59:59", "HEAD")
        if not salida.strip():
            print(f"NO-ENCONTRADO: ningun commit de HEAD anterior a {ref}")
            return 1
        ref = salida.strip()
    llaves = resuelve(args.token, ref)
    corto = _git("rev-parse", "--short=8", ref).strip()
    if not llaves:
        print(f"{args.token} en {corto}: {NO_RESUELVE} -- el numero no existia "
              f"en la demanda de ese commit")
        return 1
    print(f"{args.token} en {corto} nombraba:")
    for l in llaves:
        print(f"  {l}")
    return 0


def construye_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    subs = p.add_subparsers(dest="subcomando", required=True)
    t = subs.add_parser("tabla", help="construye pines-sellados-resueltos.tsv")
    t.add_argument("--escribe", action="store_true")
    t.set_defaults(func=cmd_tabla)
    q = subs.add_parser("que-nombraba",
                        help="que nombraba un RES/CORR en un commit o fecha")
    q.add_argument("token", help="RES-0027 o CORR-0009")
    q.add_argument("ref", help="commit, o fecha AAAA-MM-DD")
    q.set_defaults(func=cmd_que_nombraba)
    return p


def main(argv=None) -> int:
    args = construye_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
