#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_corrida0_oro.py` -- ARNÉS DE ORO de `tools/corrida0.py`.

ACTO GEN2-CORRIDA0-RENDIMIENTO-1 (20/sep/2026), P0.

QUÉ ES. Una red de seguridad para cambios que se declaran *de rendimiento*:
graba la salida byte a byte de las invocaciones de `corrida0` contra un árbol
de referencia (`--sella`) y después comprueba que el árbol de hoy produce
exactamente los mismos bytes (`--verifica`). Cubre, por invocación:

  · `stdout` completo (bytes),
  · `stderr` completo (bytes),
  · el código de salida,
  · el sha256 de LOS VEINTE TSV derivados de `data/corrida0/` tras la corrida,
  · y el CONTENIDO COMPLETO de los TSV que la invocación reescribe
    (`demanda` reescribe `demanda-corridas.tsv` y `demanda-resultados.tsv`).

QUÉ NO ES. No es un test de corrección: no sabe qué *debería* derivar
`corrida0`, sólo que deriva lo mismo que antes. Un cambio de derivación
intencional lo pone ROJO por construcción -- eso es lo que se le pide. No
adivina el arnés: sin `CORRIDA0_ORO` apuntando a un directorio sellado sale
`SALTADO-SIN-ARNES` y lo dice, nunca VERDE por omisión (A.13: todo negativo
declara cuántos archivos examinó).

POR QUÉ EL ARNÉS VIVE FUERA DEL ÁRBOL. Los TSV derivados pesan >15 MB y
cambian con cada acto que sella una corrida; congelarlos en el repo los
convertiría en una segunda copia del registro que caduca sola. El arnés se
sella contra `origin/main` en un directorio temporal, se consume en la misma
sesión y se tira. Por eso este test no corre en `check.py`: no tiene
arnés que leer ahí.

NO ESCRIBE NADA QUE NO RESTAURE. `demanda` reescribe TSV del árbol. Antes de
cada invocación este arnés lee a memoria los bytes de los veinte TSV y los
vuelve a poner tal cual al terminar -- no usa `git checkout`, así que un
árbol sucio termina igual de sucio, no limpio.

USO

    # 1. sellar contra el árbol de referencia (p.ej. una copia en origin/main)
    python3 tests/test_corrida0_oro.py --sella /tmp/oro --arbol /tmp/copia-main

    # 2. verificar el árbol de trabajo contra ese sello
    CORRIDA0_ORO=/tmp/oro python3 tests/test_corrida0_oro.py
    # o:  python3 tests/test_corrida0_oro.py --verifica /tmp/oro

Salida: `0` VERDE (o SALTADO-SIN-ARNES) · `1` ROJO (alguna salida difiere).
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CORRIDA0 = RAIZ / "tools" / "corrida0.py"
DERIVADOS = "data/corrida0"

# Las seis invocaciones que todo el aparato paga. `registro --escribe` entra
# porque es la única que materializa las tres vistas de verdad: si una
# optimización cambiara lo que se escribe, aquí se ve.
INVOCACIONES = (
    ("status", ["status"]),
    ("status___json", ["status", "--json"]),
    ("demanda", ["demanda"]),
    ("registro", ["registro"]),
    ("registro___fuentes", ["registro", "--fuentes"]),
    ("registro___escribe", ["registro", "--escribe"]),
)


def _tsvs(arbol: Path) -> list[Path]:
    return sorted((arbol / DERIVADOS).glob("*.tsv"))


def _sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as fh:
        for bloque in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _huella_tsv(arbol: Path) -> bytes:
    """`sha256sum` de los TSV derivados, en rutas relativas al árbol."""
    lineas = [f"{_sha256(p)}  {p.relative_to(arbol).as_posix()}\n" for p in _tsvs(arbol)]
    return "".join(lineas).encode("utf-8")


def _corre(arbol: Path, argv: list[str]) -> tuple[bytes, bytes, int, bytes, dict]:
    """Corre una invocación restaurando después los TSV que toque.

    Devuelve `(stdout, stderr, exit, huella_tsv, {basename: bytes})` donde el
    diccionario trae sólo los TSV cuyos bytes cambiaron por esta invocación.
    """
    antes = {p.name: p.read_bytes() for p in _tsvs(arbol)}
    r = subprocess.run([sys.executable, str(arbol / "tools" / "corrida0.py"), *argv],
                       cwd=arbol, capture_output=True)
    huella = _huella_tsv(arbol)
    despues = {p.name: p.read_bytes() for p in _tsvs(arbol)}
    cambiados = {n: b for n, b in despues.items() if antes.get(n) != b}
    for nombre, bytes_ in antes.items():
        destino = arbol / DERIVADOS / nombre
        if destino.read_bytes() != bytes_:
            destino.write_bytes(bytes_)
    for nombre in despues:
        if nombre not in antes:
            (arbol / DERIVADOS / nombre).unlink()
    return r.stdout, r.stderr, r.returncode, huella, cambiados


def sella(oro: Path, arbol: Path) -> int:
    oro.mkdir(parents=True, exist_ok=True)
    for nombre, argv in INVOCACIONES:
        out, err, rc, huella, cambiados = _corre(arbol, argv)
        (oro / f"{nombre}.out").write_bytes(out)
        (oro / f"{nombre}.err").write_bytes(err)
        (oro / f"{nombre}.exit").write_text(f"{rc}\n", encoding="utf-8")
        (oro / f"{nombre}.tsvsha").write_bytes(huella)
        destino = oro / f"{nombre}.tsv"
        destino.mkdir(exist_ok=True)
        for tsv, bytes_ in cambiados.items():
            (destino / tsv).write_bytes(bytes_)
        print(f"SELLADO {nombre}: exit={rc} out={len(out)}B err={len(err)}B "
              f"tsv_reescritos={len(cambiados)}")
    print(f"ARNÉS SELLADO en {oro} · árbol de referencia {arbol} · "
          f"{len(INVOCACIONES)} invocaciones · {len(_tsvs(arbol))} TSV derivados")
    return 0


def verifica(oro: Path, arbol: Path) -> int:
    fallas: list[str] = []
    examinados = 0
    for nombre, argv in INVOCACIONES:
        esperado_out = oro / f"{nombre}.out"
        if not esperado_out.exists():
            fallas.append(f"{nombre}: el arnés no trae `{esperado_out.name}`")
            continue
        out, err, rc, huella, cambiados = _corre(arbol, argv)
        examinados += 1
        rc_oro = int((oro / f"{nombre}.exit").read_text(encoding="utf-8").strip())
        for etiqueta, hoy, ayer in (
            ("stdout", out, esperado_out.read_bytes()),
            ("stderr", err, (oro / f"{nombre}.err").read_bytes()),
            ("sha256 de los TSV derivados", huella, (oro / f"{nombre}.tsvsha").read_bytes()),
        ):
            if hoy != ayer:
                fallas.append(f"{nombre}: {etiqueta} difiere "
                              f"(arnés {len(ayer)}B, hoy {len(hoy)}B)\n"
                              f"    {_primera_diferencia(ayer, hoy)}")
        if rc != rc_oro:
            fallas.append(f"{nombre}: exit {rc} != {rc_oro} del arnés")
        dir_tsv = oro / f"{nombre}.tsv"
        esperados = {p.name: p.read_bytes() for p in sorted(dir_tsv.glob("*.tsv"))} if dir_tsv.is_dir() else {}
        if set(esperados) != set(cambiados):
            fallas.append(f"{nombre}: reescribe {sorted(cambiados)} y el arnés "
                          f"registra {sorted(esperados)}")
        for tsv in sorted(set(esperados) & set(cambiados)):
            if esperados[tsv] != cambiados[tsv]:
                fallas.append(f"{nombre}: `{tsv}` reescrito difiere del arnés\n"
                              f"    {_primera_diferencia(esperados[tsv], cambiados[tsv])}")
        print(f"  [{nombre}] exit={rc} out={len(out)}B err={len(err)}B "
              f"tsv_reescritos={len(cambiados)}")
    if fallas:
        print(f"\nROJO T-CORRIDA0-ORO · {len(fallas)} diferencia(s) · "
              f"{examinados} de {len(INVOCACIONES)} invocaciones examinadas")
        for f in fallas:
            print(f"  FAIL {f}")
        return 1
    print(f"\nVERDE T-CORRIDA0-ORO · salidas byte-idénticas al arnés en "
          f"{examinados} de {len(INVOCACIONES)} invocaciones · "
          f"{len(_tsvs(arbol))} TSV derivados cotejados por sha256")
    return 0


def _primera_diferencia(ayer: bytes, hoy: bytes) -> str:
    limite = min(len(ayer), len(hoy))
    for i in range(limite):
        if ayer[i] != hoy[i]:
            ini = max(0, i - 60)
            return (f"primer byte distinto en offset {i}: "
                    f"arnés …{ayer[ini:i + 60]!r} · hoy …{hoy[ini:i + 60]!r}")
    return f"idénticos hasta el byte {limite}; difieren sólo en longitud"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sella", metavar="DIR",
                    help="graba el arnés de oro en DIR desde --arbol")
    ap.add_argument("--verifica", metavar="DIR",
                    help="compara --arbol contra el arnés de DIR "
                         "(default: $CORRIDA0_ORO)")
    ap.add_argument("--arbol", metavar="DIR", default=str(RAIZ),
                    help="árbol de trabajo sobre el que se corre corrida0 "
                         f"(default: {RAIZ})")
    args = ap.parse_args(argv)

    arbol = Path(args.arbol).resolve()
    if not (arbol / "tools" / "corrida0.py").is_file():
        print(f"ROJO: `{arbol}` no parece un árbol del repo "
              f"(sin `tools/corrida0.py`)")
        return 1

    if args.sella:
        return sella(Path(args.sella).resolve(), arbol)

    oro = args.verifica or os.environ.get("CORRIDA0_ORO") or ""
    if not oro:
        print("SALTADO-SIN-ARNES · 0 invocaciones examinadas.\n"
              "  El arnés de oro vive FUERA del árbol por diseño (>15 MB de TSV\n"
              "  derivados que cambian con cada acto que sella una corrida).\n"
              "  Para sellarlo contra origin/main y verificar el árbol de hoy:\n"
              "    git worktree add /tmp/oro-main origin/main\n"
              "    python3 tests/test_corrida0_oro.py --sella /tmp/oro "
              "--arbol /tmp/oro-main\n"
              "    CORRIDA0_ORO=/tmp/oro python3 tests/test_corrida0_oro.py")
        return 0
    ruta_oro = Path(oro).resolve()
    if not ruta_oro.is_dir():
        print(f"ROJO: el arnés `{ruta_oro}` NO-ENCONTRADO (0 archivos examinados)")
        return 1
    print(f"T-CORRIDA0-ORO · arnés {ruta_oro} · árbol {arbol}")
    return verifica(ruta_oro, arbol)


if __name__ == "__main__":
    sys.exit(main())
