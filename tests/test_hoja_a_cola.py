#!/usr/bin/env python3
"""ACTO GEN2-ASTRA5-U5-ADQUISICION-1 · guardia de P1/P2 (tools/dominios/hoja_a_cola.py).

Defecto que atrapa (real, del propio encargo): la hoja de adquisición del mapa
ASTRA5-U0 tenía 163 filas ADQUIRIR en texto libre que ninguna tabla leía; la
cola de /adquiere sólo se escribe por registro -> vista. Este test comprueba,
sin red ni corpus:

1 · la vista data/cola-adquisicion-v1_0.tsv se reproduce byte a byte desde el
    registro (P1: «la vista se reproduce byte a byte desde el registro»);
2 · el registro y las constancias contienen exactamente lo que el script
    deriva hoy (--verifica), de modo que editar la hoja, las reglas o la firma
    sin re-escribir la cola falla aquí;
3 · cada fila ADQUIRIR cae en exactamente una clase declarada, y toda
    (instrumento, ola) MICRODATO tiene fila de cola (propia o ya existente);
4 · caso sintético: el orden de las reglas manda (una fila que nombra ENCIG
    2023 y Research Land cae en ENCIG) y lo que no casa ninguna regla
    específica cae en la regla por defecto DOCUMENTO.

Uso: python3 tests/test_hoja_a_cola.py   (sale 0 si todo pasa)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "dominios"))

import hoja_a_cola as h  # noqa: E402
import vista_cola_adquisicion as v  # noqa: E402

fallos = 0


def check(nombre: str, ok: bool, detalle: str = "") -> None:
    global fallos
    print(f"{'PASS' if ok else 'FAIL'} · {nombre}" + (f" · {detalle}" if detalle and not ok else ""))
    if not ok:
        fallos += 1


# 1 · vista byte a byte
vista_disco = (ROOT / "data/cola-adquisicion-v1_0.tsv").read_text(encoding="utf-8")
check("1 · la vista se reproduce byte a byte desde el registro",
      v.build(ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv") == vista_disco)

# 2 · registro y constancias = lo derivado
r = subprocess.run([sys.executable, str(ROOT / "tools/dominios/hoja_a_cola.py"), "--verifica"],
                   capture_output=True, text=True, cwd=ROOT)
check("2 · hoja_a_cola.py --verifica sale 0", r.returncode == 0, r.stdout[-400:] + r.stderr[-400:])

# 3 · cobertura de la clasificación
hoja = [f for f in h.lee_tsv(h.HOJA) if f["estado_hoja"] == "ADQUIRIR"]
pares = h.clasifica(hoja, h.lee_tsv(h.REGLAS))
check("3a · cada fila ADQUIRIR recibe exactamente una regla",
      len(pares) == len(hoja) and len({f["id_afirmacion"] for f, _ in pares}) == len(hoja),
      f"{len(pares)} pares para {len(hoja)} filas")
check("3b · toda clase está en el vocabulario cerrado",
      all(reg["clase"] in h.CLASES for _, reg in pares))
filas, _, _ = h.deriva()
registro = {x["fila_origen"] for x in h.leer_dicts(h.REGISTRO)}
fuentes = {x["fuente_canonica"] for x in h.leer_dicts(h.REGISTRO)}
huerfanas = []
for f, reg in pares:
    if reg["clase"] != "MICRODATO":
        continue
    if reg["fuente_existente"]:
        if reg["fuente_existente"] not in fuentes:
            huerfanas.append(f["id_afirmacion"])
        continue
    for ola in reg["olas"].split(";"):
        if f"ASTRA5-U5:{h.clave(reg['instrumento'], ola)}" not in registro:
            huerfanas.append(f["id_afirmacion"])
check("3c · toda (instrumento, ola) MICRODATO tiene fila en la cola", not huerfanas, str(huerfanas))

# 4 · sintético: orden de reglas y regla por defecto
sint = [
    {"id_afirmacion": "SINT-1", "instrumento_ola": "ENCIG 2023 (citado por el report) y ENCOAP",
     "pieza_o_razon": "documento de Research Land (2026)", "prioridad": "3"},
    {"id_afirmacion": "SINT-2", "instrumento_ola": "Fulano et al. (2031), revista inventada",
     "pieza_o_razon": "artículo", "prioridad": "3"},
]
res = {f["id_afirmacion"]: reg for f, reg in h.clasifica(sint, h.lee_tsv(h.REGLAS))}
check("4a · el orden de reglas manda (ENCIG antes que Research Land)",
      res["SINT-1"]["instrumento"] == "ENCIG-ENCOAP", res["SINT-1"]["instrumento"])
check("4b · lo que no casa una regla específica cae en DOCUMENTO por defecto",
      res["SINT-2"]["clase"] == "DOCUMENTO" and res["SINT-2"]["orden"] == "999")

print(f"{'VERDE' if not fallos else 'ROJO'} · {fallos} fallo(s)")
sys.exit(1 if fallos else 0)
