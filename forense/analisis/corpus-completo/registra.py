#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P2 · de la bitácora de descargas al manifiesto.

Lee bitacora-descargas.tsv (filas OK) y registra en data/manifiesto.yaml cada payload que
todavía no esté (por sha256 ni por id). sha256 y tamaño se DERIVAN del archivo en disco —
nunca de la bitácora ni tecleados— y deben coincidir con los dos sha de la descarga A.7.

Escritura por APÉNDICE (mismo método que GEN2-ASTRA5-U5-ADQUISICION-1, nota §4): el volcado
canónico de tests/manifiesto.py re-envuelve ~90 líneas escritas a mano por otros actos. Antes
de anexar se valida la lista COMPLETA con tests/manifiesto._validar_manifiesto_completo,
eximiendo POR NOMBRE sólo las dos entradas del defecto heredado FP-260924-GEN2-ASTRA5-U5-
ADQUISICION-1-43d6-02 (estado_reserva fuera de vocabulario en enoe_2026_1t_*).

Ola RESERVADA → raiz: reserva_respondentes, estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L.

Uso: python3 registra.py [--escribe]   (sin --escribe: reporta lo que anexaría; D-23)
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
import manifiesto as M  # noqa: E402

D = ROOT / "forense/analisis/corpus-completo"
BITACORA = D / "bitacora-descargas.tsv"
CATALOGO = D / "catalogo-v1_0.tsv"
MANIF = ROOT / "data/manifiesto.yaml"
RAW = Path("/home/pc0/mm-corpus/raw")
RESERVA = Path("/home/pc0/mm-corpus/reservas-respondentes")
EXENTOS_FP_43D6_02 = {"enoe_2026_1t_csv", "enoe_2026_1t_microdatos"}
ACTO = "GEN2-CORPUS-COMPLETO-1"


def lee(path: Path) -> list[dict]:
    lineas = path.read_text(encoding="utf-8").splitlines()
    i = 1 if lineas[0].startswith("#") else 0
    cab = lineas[i].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[i + 1:]]


def id_de(r: dict) -> str:
    nombre = Path(r["destino"]).name
    tronco = re.sub(r"\.(zip|rar|pdf|7z|gz)$", "", nombre, flags=re.I)
    crudo = f"cc1_{r['fuente']}_{r['programa']}_{r['ola']}__{tronco}".lower()
    return re.sub(r"[^a-z0-9_]+", "_", crudo).strip("_")


def main() -> int:
    escribe = "--escribe" in sys.argv
    cat = {c["url"]: c for c in lee(CATALOGO)}
    texto = MANIF.read_text(encoding="utf-8")
    _, entradas = M.leer_manifiesto(str(MANIF))
    por_sha = {e.get("sha256"): e["id"] for e in entradas if e.get("sha256")}
    ids = {e["id"] for e in entradas}
    nuevas, vistos, dup = [], set(), []
    for r in lee(BITACORA):
        if r["resultado"] != "OK" or r["url"] in vistos:
            continue
        vistos.add(r["url"])
        p = Path(r["destino"])
        if not p.exists():
            raise SystemExit(f"ANTI-PR#77: {p} no está en el corpus compartido")
        s = M.sha256_de(str(p))
        if s != r["sha256_1"] or s != r["sha256_2"]:
            raise SystemExit(f"sha en disco {s} ≠ bitácora A.7 para {p}")
        if s in por_sha:
            dup.append((r["url"], por_sha[s]))
            continue
        i = id_de(r)
        if i in ids:
            raise SystemExit(f"id ya existe con otro sha: {i}")
        c = cat.get(r["url"], {})
        reservada = r["reserva"] == "RESERVADA"
        raiz = RESERVA if reservada else RAW
        e = {
            "id": i,
            "usado_para": (f"{ACTO} P2 · catálogo {r['fuente']} {r['programa']} ola {r['ola']}"
                           f" · {c.get('titulo', '')[:160]} · prioridad mapa={c.get('prioridad', '')}"),
            "url_origen": r["url"],
            "fecha_descarga": r["fecha_utc"][:10],
            "descargado_por": "agente Claude (Opus 5.5) en CAJA, curl directo del portal "
                              "(forense/analisis/corpus-completo/descarga.py)",
            "archivo": str(p.relative_to(raiz)),
            "sha256": s,
            "tamano_bytes": p.stat().st_size,
            "formato": f"{c.get('formato_elegido', '') or p.suffix} ({r['estructura']}); "
                       f"formatos publicados: {c.get('formatos', '')}",
            "licencia": c.get("licencia", "") or "no declarada por el catálogo",
            "nota": (f"A.7: dos descargas con sha256 idéntico; estructura {r['estructura']}; "
                     "no abierto (sólo sha, tamaño y directorio central)."),
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
    completas = [x for x in entradas if x.get("id") not in EXENTOS_FP_43D6_02] + nuevas
    M._validar_manifiesto_completo(completas)
    res = sum(1 for e in nuevas if e.get("estado_reserva"))
    print(f"nuevas={len(nuevas)} reservadas={res} duplicadas_por_sha={len(dup)}")
    for u, i in dup[:20]:
        print(f"  DUP-SHA {u} = {i}")
    if escribe and nuevas:
        cuerpo = yaml.dump(nuevas, allow_unicode=True, sort_keys=False, width=88,
                           default_flow_style=False).replace("\n- id:", "\n\n- id:")
        M._escribir_atomico(str(MANIF), texto.rstrip("\n") + "\n\n" + cuerpo)
        print(f"anexadas {len(nuevas)} entradas a {MANIF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
