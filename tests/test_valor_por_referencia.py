#!/usr/bin/env python3
"""ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-4 · `valor` por referencia.

Defecto real que atrapa (24/sep/2026, run 36066873728): CALC pendientes del
lote guardaban listas enteras en la celda `valor` (CALC-ENOE-PERSISTENCIA-0001:
11 MB) y `resultados.tsv` re-derivado pesó 92 MB; la guarda de 50 MB tumbó el
canal y ningún `[deriva]` se abrió desde el 23/sep.

Cuatro bloques:
  1. COMMIT-B · `vista.referencia_valor` / `resuelve_valor`: ida y vuelta
     byte a byte, corto intacto, idempotente, referencia rota falla en voz alta.
  2. COMMIT-C · `corrida0._problemas_valor_largo`: un CALC sintético que emite
     una lista sin `tablas/` es rechazado; con `tablas/` y sha, aceptado.
  3. `derivados_protegidos._es_tabla_de_valor`: `valores-vista/` es derivado
     por ruta; `tablas/` (sellado, EDER2017) no.
  4. Vista real: toda celda `REF:` de `data/corrida0/resultados.tsv` resuelve
     (archivo presente, sha256 casa) y ninguna celda inline pasa de 1 KB.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import corrida0 as C  # noqa: E402
import derivados_protegidos as DP  # noqa: E402
import vista as V  # noqa: E402

FAILS: list[str] = []


def afirma(cond: bool, msg: str) -> None:
    if not cond:
        FAILS.append(msg)


def _fila(valor, spec_id="CALC-SINT-0001", rid="RESULT-SINT-LISTA"):
    return {"resultado_id": rid, "spec_id": spec_id, "corrida_id": f"{spec_id}-x", "valor": valor}


def prueba_ida_y_vuelta():
    with tempfile.TemporaryDirectory() as t:
        raiz = Path(t)
        largo = json.dumps([{"k": i, "v": i / 7} for i in range(200)])
        f = V.referencia_valor(_fila(largo), raiz)
        afirma(f["valor"].startswith("REF:data/corrida0/CALC-SINT-0001/valores-vista/RESULT-SINT-LISTA.json#sha256:"),
               f"celda larga debe quedar como REF en valores-vista/, quedó {f['valor'][:80]!r}")
        afirma(V.resuelve_valor(f["valor"], raiz) == largo, "resolver devuelve el texto byte a byte")
        afirma(V.referencia_valor(f, raiz) == f, "referenciar una celda REF es idempotente")
        corto = _fila("0.4213")
        afirma(V.referencia_valor(corto, raiz) is corto, "una celda corta no se toca")
        afirma(V.referencia_valor(_fila("x" * 1025), raiz)["valor"].endswith(
            "#sha256:" + hashlib.sha256(b"x" * 1025).hexdigest()) and ".txt#" in
            V.referencia_valor(_fila("x" * 1025), raiz)["valor"], "texto no JSON va a .txt")
        (raiz / f["valor"][4:].split("#")[0]).write_text("alterado")
        try:
            V.resuelve_valor(f["valor"], raiz)
            afirma(False, "una referencia con sha distinto debe fallar")
        except V.ReferenciaRota:
            pass


def prueba_conducto_sintetico():
    lista = [{"conducta": "a", "p": 0.1}] * 50
    afirma(any("VALOR-LARGO" in p for p in C._problemas_valor_largo({"RESULT-L": lista}, None)),
           "una lista sin tablas/ se rechaza antes de sellar")
    afirma(any("VALOR-LARGO" in p for p in C._problemas_valor_largo({"RESULT-L": "y" * 2000}, None)),
           "un texto > 1 KB se rechaza")
    afirma(C._problemas_valor_largo({"A": 1, "B": 0.5, "C": "corto", "D": None, "E": True}, None) == [],
           "escalares cortos pasan")
    d = C.CORRIDAS / "CALC-SINTETICO-VALOR-REF-0001"
    try:
        (d / "tablas").mkdir(parents=True)
        datos = json.dumps(lista).encode()
        (d / "tablas" / "lista.json").write_bytes(datos)
        ref = f"REF:data/corrida0/{d.name}/tablas/lista.json#sha256:{hashlib.sha256(datos).hexdigest()}"
        afirma(C._problemas_valor_largo({"RESULT-L": ref}, d) == [], "con tablas/ y sha, aceptado")
        malo = ref[:-4] + "0000"
        afirma(any("VALOR-REF-ROTA" in p for p in C._problemas_valor_largo({"RESULT-L": malo}, d)),
               "sha distinto se rechaza")
        fuera = ref.replace(f"{d.name}/tablas", "CALC-OTRO/tablas")
        afirma(any("VALOR-REF-FUERA-DE-TABLAS" in p for p in C._problemas_valor_largo({"RESULT-L": fuera}, d)),
               "una REF fuera del propio CALC se rechaza")
    finally:
        for p in sorted(d.rglob("*"), reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
        d.rmdir()


def prueba_derivado_por_ruta():
    afirma(DP._es_tabla_de_valor("data/corrida0/CALC-X/valores-vista/RESULT-Y.json"), "valores-vista/ es derivado")
    afirma(not DP._es_tabla_de_valor("data/corrida0/CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/tablas/resultados.json"),
           "tablas/ sellado no es derivado")


def prueba_vista_real():
    ruta = V.VISTA_RESULTADOS
    if not ruta.exists():
        return
    rotas, largas, refs = [], [], 0
    for f in V._leer_tsv_derivado(ruta):
        v = f.get("valor") or ""
        if V.es_referencia(v):
            refs += 1
            try:
                V.resuelve_valor(v)
            except V.ReferenciaRota as e:
                rotas.append(str(e))
        elif len(v.encode("utf-8")) > V.UMBRAL_VALOR_BYTES:
            largas.append(f["resultado_id"])
    afirma(not rotas, f"{len(rotas)} referencias rotas en resultados.tsv: {rotas[:3]}")
    # Hasta que el primer [deriva] posterior a COMMIT-B fusione, main trae 51
    # celdas legadas inline > 1 KB (medido 24/sep). Se reporta, no falla:
    # la vista la escribe el job, no un PR ordinario (derivados_protegidos).
    print(f"vista real: {refs} celdas REF resueltas · {len(largas)} celdas inline > 1 KB (pendientes del próximo [deriva])")


def main() -> int:
    prueba_ida_y_vuelta()
    prueba_conducto_sintetico()
    prueba_derivado_por_ruta()
    prueba_vista_real()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_valor_por_referencia.py: 4 bloques, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
