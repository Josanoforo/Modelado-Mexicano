#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de la publicación por trozos -- ACTO GEN2-TUBERIA-CI-TIEMPO-2
(27/sep/2026), P2 y P4.

Defecto que atrapa (run 36291122052): el lote de replay de 121 CALC no cabía
en los 30 min del job, el run se cortaba, la base no avanzaba y el lote
crecía con cada merge. El troceo sólo es aceptable si publicar por trozos da
EXACTAMENTE las mismas vistas que publicar el lote entero (E.7: trocear no es
excluir) y si posponer nunca retira algo ya publicado.

Casos:
  A · equivalencia byte a byte: tres CALC nuevos publicados en tres trozos
      (`lote=[X]`, `pospone=[resto]`) == los tres en un solo `--lote`.
  B · un trozo deja lo pospuesto AUSENTE de corridas.tsv (sigue pendiente).
  C · PARO si un id está en `--lote` y en `--pospone`.
  D · PARO si se pospone un CALC ya publicado.
  E · `parte_en_trozo`: trozo + resto == lote; n <= 0 es error.
  F · `linea_crecimiento_lote`: OK en el umbral, CRECE por encima.

Corre standalone (`python3 tests/test_ci_tiempo_2.py`) y expone `corre()`,
mismo patrón que `tests/test_registro_lote_estricto.py`.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _carga(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


C = _carga("corrida0_ci_tiempo_2", RAIZ / "tools" / "corrida0.py")
T = _carga("test_corrida0_ci_tiempo_2", RAIZ / "tests" / "test_corrida0.py")
T.C = C  # un solo módulo `corrida0` bajo prueba en todo este archivo.
sys.path.insert(0, str(RAIZ / "tools"))
L = _carga("lote_desde_asientos_ci_tiempo_2", RAIZ / "tools" / "lote_desde_asientos.py")
G = _carga("ci_guardias_ci_tiempo_2", RAIZ / "tools" / "ci_guardias.py")

FALLOS: list[str] = []
IDS = ["CALC-FIX-UNO", "CALC-FIX-DOS", "CALC-FIX-TRES"]


def _afirma(cond: bool, caso: str, msg: str) -> None:
    if not cond:
        FALLOS.append(f"{caso}: {msg}")


def _arbol():
    calcs = [{"calc_id": c, "valores": {f"RESULT-{i}": float(i)},
              "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}}
             for i, c in enumerate(IDS)]
    res = [T._fila_demanda(f"RES-{i:04d}", f"c:uno:{i}", f"CORR-{i:04d}")
           for i in range(3)]
    corr = [T._fila_corrida(f"CORR-{i:04d}", [f"RES-{i:04d}"]) for i in range(3)]
    return T._arbol_registro(res=res, corr=corr, calcs=calcs)


class _Vistas:
    """Apunta las tres vistas de `corrida0` al árbol temporal y las restaura."""

    def __init__(self, tmp: Path):
        self.tmp = tmp

    def __enter__(self):
        self.previas = (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)
        C.VISTA_CORRIDAS = self.tmp / "corridas.tsv"
        C.VISTA_RESULTADOS = self.tmp / "resultados.tsv"
        C.VISTA_USOS = self.tmp / "usos.tsv"
        return self

    def bytes(self) -> dict:
        return {p.name: p.read_bytes() for p in
                (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)}

    def borra(self) -> None:
        for p in (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS):
            p.unlink(missing_ok=True)

    def __exit__(self, *exc):
        C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS = self.previas
        return False


def _specs_publicadas() -> set:
    return {f["spec_id"] for f in C._leer_tsv_derivado(C.VISTA_CORRIDAS)}


def t_a_trozos_equivalen_byte_a_byte_al_lote_entero():
    caso = "t_a_trozos_equivalen_byte_a_byte_al_lote_entero"
    with _arbol() as tmp, _Vistas(tmp) as v:
        C.registro(escribe=True, imprime=False, lote=list(IDS))
        entero = v.bytes()
        v.borra()
        for k, calc in enumerate(IDS):
            resto = IDS[k + 1:]
            C.registro(escribe=True, imprime=False, lote=[calc],
                       pospone=[",".join(resto)] if resto else None)
        por_trozos = v.bytes()
        for nombre in entero:
            _afirma(entero[nombre] == por_trozos[nombre], caso,
                    f"{nombre} difiere entre lote entero y tres trozos")


def t_b_lo_pospuesto_sigue_pendiente():
    caso = "t_b_lo_pospuesto_sigue_pendiente"
    with _arbol() as tmp, _Vistas(tmp):
        C.registro(escribe=True, imprime=False, lote=[IDS[0]],
                   pospone=[",".join(IDS[1:])])
        pub = _specs_publicadas()
        _afirma(IDS[0] in pub, caso, "el trozo no se publicó")
        for calc in IDS[1:]:
            _afirma(calc not in pub, caso, f"{calc} pospuesto quedó publicado")


def t_c_paro_si_lote_y_pospone_se_cruzan():
    caso = "t_c_paro_si_lote_y_pospone_se_cruzan"
    with _arbol() as tmp, _Vistas(tmp):
        try:
            C.registro(escribe=True, imprime=False, lote=[IDS[0]], pospone=[IDS[0]])
            _afirma(False, caso, "no paró con el mismo id en --lote y --pospone")
        except C.ParoRegistro as exc:
            _afirma("POSPONE-EN-LOTE" in str(exc), caso, f"paro distinto: {exc}")
        _afirma(not C.VISTA_CORRIDAS.exists(), caso, "escribió pese al PARO")


def t_d_paro_si_se_pospone_lo_publicado():
    caso = "t_d_paro_si_se_pospone_lo_publicado"
    with _arbol() as tmp, _Vistas(tmp):
        C.registro(escribe=True, imprime=False, lote=list(IDS))
        antes = C.VISTA_CORRIDAS.read_bytes()
        try:
            C.registro(escribe=True, imprime=False, lote=[IDS[0]], pospone=[IDS[1]])
            _afirma(False, caso, "posponer un CALC publicado no paró")
        except C.ParoRegistro as exc:
            _afirma("POSPONE-PUBLICADA" in str(exc), caso, f"paro distinto: {exc}")
        _afirma(C.VISTA_CORRIDAS.read_bytes() == antes, caso,
                "la vista publicada cambió pese al PARO")


def t_e_parte_en_trozo_no_pierde_nada():
    caso = "t_e_parte_en_trozo_no_pierde_nada"
    ids = [f"CALC-{i}" for i in range(45)]
    for n in (1, 20, 45, 60):
        trozo, resto = L.parte_en_trozo(ids, n)
        _afirma(trozo + resto == ids, caso, f"n={n}: trozo+resto != lote")
        _afirma(len(trozo) == min(n, len(ids)), caso, f"n={n}: tamaño de trozo")
    try:
        L.parte_en_trozo(ids, 0)
        _afirma(False, caso, "n=0 no levantó")
    except ValueError:
        pass


def t_f_guardia_de_crecimiento():
    caso = "t_f_guardia_de_crecimiento"
    u = G.UMBRAL_LOTE_PENDIENTE
    _afirma(G.linea_crecimiento_lote(u).endswith("OK"), caso, "en el umbral debe ser OK")
    _afirma(G.linea_crecimiento_lote(u + 1).endswith("CRECE"), caso,
            "sobre el umbral debe ser CRECE")
    _afirma(G.linea_crecimiento_lote(121).startswith("LOTE-PENDIENTE: 121 CALC"),
            caso, "la línea no declara el tamaño")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def corre() -> list[str]:
    FALLOS.clear()
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:
            FALLOS.append(f"{fn.__name__}: EXCEPCION {type(exc).__name__}: {exc}")
    return list(FALLOS)


def test_ci_tiempo_2():
    fallos = corre()
    assert not fallos, "\n".join(fallos)


def main() -> int:
    fallos = corre()
    print(f"tests/test_ci_tiempo_2.py · {len(TESTS)} casos · {len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
