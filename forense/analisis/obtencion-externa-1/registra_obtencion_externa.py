#!/usr/bin/env python3
"""ACTO GEN2-OBTENCION-EXTERNA-1 · de los lotes al manifiesto (append validado).

Lee lote-*.tsv (filas `estado=OBTENIDO` con `archivo`) y la bitácora A.7 del mismo lote
(bitacora-<lote>.tsv, escrita por baja.py). Por cada payload: sha256 y tamaño se DERIVAN del
archivo en disco (nunca de la tabla) y deben coincidir con la bitácora (sha256_1 == sha256_2, o
hash neutralizado idéntico en HTML con tokens: A.7); el archivo debe estar en el corpus
compartido (anti-PR#77). Dedup por sha contra el manifiesto: un sha ya registrado bajo otro id
no se duplica (se reporta YA-EN-CORPUS). Reserva: `reserva=RESERVADA` → raiz
reserva_respondentes + estado_reserva RESERVADA-NO-ABIERTA-NO-INDEXAR-L (E.6).

Escritura por APÉNDICE, igual que forense/analisis/corpus-completo/registra.py: se valida la
lista COMPLETA con tests/manifiesto._validar_manifiesto_completo eximiendo POR NOMBRE sólo las
dos entradas del defecto heredado FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-02.

Uso: python3 registra_obtencion_externa.py [--escribe]   (sin --escribe: reporta lo que anexaría; D-23)
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
import manifiesto as M  # noqa: E402

D = Path(__file__).resolve().parent
MANIF = ROOT / "data/manifiesto.yaml"
RAW = Path("/home/pc0/mm-corpus/raw")
RESERVA = Path("/home/pc0/mm-corpus/reservas-respondentes")
EXENTOS_FP_43D6_02 = {"enoe_2026_1t_csv", "enoe_2026_1t_microdatos"}
ACTO = "GEN2-OBTENCION-EXTERNA-1"


def lee(path: Path) -> list[dict]:
    lineas = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def main() -> int:
    escribe = "--escribe" in sys.argv
    texto = MANIF.read_text(encoding="utf-8")
    _, entradas = M.leer_manifiesto(str(MANIF))
    por_sha = {e.get("sha256"): e["id"] for e in entradas if e.get("sha256")}
    ids = {e["id"] for e in entradas}
    nuevas, ya, errores = [], [], []
    for lote in sorted(D.glob("lote-*.tsv")):
        clave = lote.stem.split("-", 1)[1]
        bit = {}
        bpath = D / f"bitacora-{clave}.tsv"
        if bpath.exists():
            for b in lee(bpath):
                if b["resultado"].startswith("OK"):
                    bit[b["destino"]] = b
        for r in lee(lote):
            if r.get("estado") != "OBTENIDO" or r.get("archivo", "-") in ("", "-"):
                continue
            reservada = r.get("reserva") == "RESERVADA"
            p = (RESERVA if reservada else RAW) / r["archivo"]
            if not p.is_file():
                errores.append(f"ANTI-PR#77 {clave}: {p} no está en el corpus compartido")
                continue
            s = M.sha256_de(str(p))
            b = bit.get(r["archivo"])
            if b is None:
                errores.append(f"SIN-BITACORA-A7 {clave}: {r['archivo']}")
                continue
            if s != b["sha256_1"] or not (b["sha256_2"] == s or b["sha256_neutro"] and "|" not in b["sha256_neutro"]):
                errores.append(f"A7 {clave}: sha disco {s[:12]} vs bitácora {b['sha256_1'][:12]}/{b['sha256_2'][:12]}")
                continue
            if s in por_sha:
                ya.append((r["id_propuesto"], por_sha[s]))
                continue
            i = r["id_propuesto"]
            if i in ids:
                errores.append(f"ID-EXISTE {i}")
                continue
            a7 = ("dos descargas con sha256 crudo idéntico" if b["sha256_2"] == s else
                  f"sha crudo difiere entre descargas; hash neutralizado idéntico {b['sha256_neutro'][:16]}…")
            e = {
                "id": i,
                "usado_para": r["usado_para"],
                "url_origen": r["url"],
                "fecha_descarga": b["fecha"],
                "descargado_por": ("agente Claude (Sonnet, lote " + clave + ", supervisado por Opus 5.5) en CAJA, curl "
                                   "directo (forense/analisis/obtencion-externa-1/baja.py)"),
                "archivo": str(p.relative_to(RESERVA if reservada else RAW)),
                "sha256": s,
                "tamano_bytes": p.stat().st_size,
                "formato": f"{p.suffix.lstrip('.') or 'sin-extension'} ({b['estructura']}; {b['content_type']})",
                "licencia": r["licencia"] if r["licencia"] not in ("", "-") else "NO-DECLARADA-EN-ORIGEN",
                "nota": (f"{ACTO} {clave}. A.7: {a7}; estructura {b['estructura']}; no abierto (sólo sha, "
                         f"tamaño y envoltura). {r['nota'] if r['nota'] != '-' else ''}").strip()[:1500],
                "entorno_descarga": M.entorno_actual(),
            }
            if reservada:
                e["raiz"] = "reserva_respondentes"
                e["estado_reserva"] = "RESERVADA-NO-ABIERTA-NO-INDEXAR-L"
            else:
                e["raiz"] = "data_raw"
            nuevas.append(e)
            ids.add(i)
            por_sha[s] = i
    for x in errores:
        print("ERROR", x)
    completas = [x for x in entradas if x.get("id") not in EXENTOS_FP_43D6_02] + nuevas
    M._validar_manifiesto_completo(completas)
    res = sum(1 for e in nuevas if e.get("estado_reserva"))
    print(f"nuevas={len(nuevas)} reservadas={res} ya_en_corpus_por_sha={len(ya)} errores={len(errores)}")
    for a, b in ya:
        print(f"  YA-EN-CORPUS {a} = {b}")
    if errores:
        return 1
    if escribe and nuevas:
        cuerpo = yaml.dump(nuevas, allow_unicode=True, sort_keys=False, width=88,
                           default_flow_style=False).replace("\n- id:", "\n\n- id:")
        M._escribir_atomico(str(MANIF), texto.rstrip("\n") + "\n\n" + cuerpo)
        print(f"anexadas {len(nuevas)} entradas a {MANIF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
