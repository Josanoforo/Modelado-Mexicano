#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P2 · /adquiere §5-§6: asienta en el registro de la cola el
resultado de cada fila `CORPUS-COMPLETO-1:` caminada por descarga.py y registrada por
registra.py. Nada se teclea: el estado se deriva de la bitácora y del manifiesto.

- todos los archivos del (programa, ola) con id en el manifiesto -> OBTENIDO
- algunos                                                        -> OBTENIDO-PARCIAL
- ninguno y >=1 intento en bitácora                              -> NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)
- sin intento: la fila queda PENDIENTE (no se toca)

Escritor canónico `tsv_crudo.upsert_fila`; después regenerar la vista con
`python3 tools/vista_cola_adquisicion.py`.
Uso: python3 cierra_cola.py [--escribe]
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "curador_registro"))
from tsv_crudo import leer_dicts, leer_lineas, upsert_fila  # noqa: E402

D = ROOT / "forense/analisis/corpus-completo"
REGISTRO = ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv"
PREFIJO = "CORPUS-COMPLETO-1:"


def lee(path: Path) -> list[dict]:
    lineas = path.read_text(encoding="utf-8").splitlines()
    i = 1 if lineas[0].startswith("#") else 0
    cab = lineas[i].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[i + 1:]]


def main() -> int:
    escribe = "--escribe" in sys.argv
    clave = lambda p, o: f"{p}_{o}".replace(" ", "-")  # noqa: E731
    urls = defaultdict(set)
    for c in lee(D / "catalogo-v1_0.tsv"):
        if c["clase"] == "ARCHIVO" and c["en_manifiesto"] == "NO":
            urls[clave(c["programa"], c["ola"])].add(c["url"])
    man = [e for e in yaml.safe_load((ROOT / "data/manifiesto.yaml").read_text(encoding="utf-8"))
           if isinstance(e, dict) and "id" in e]
    id_por_url = {e.get("url_origen"): e["id"] for e in man}
    id_por_sha = {e.get("sha256"): e["id"] for e in man if e.get("sha256")}
    intentos, ultimo, fallo = defaultdict(int), {}, {}
    ok_sha = {}
    for b in lee(D / "bitacora-descargas.tsv"):
        k = clave(b["programa"], b["ola"])
        intentos[k] += 1
        ultimo[k] = max(ultimo.get(k, ""), b["fecha_utc"][:10])
        if b["resultado"] == "OK":
            ok_sha[b["url"]] = b["sha256_1"]
        else:
            fallo[b["url"]] = f"{b['resultado']} {b['http_code']} {b['nota']}".strip()[:120]
    campos = leer_lineas(REGISTRO)[0].rstrip("\n").split("\t")
    cuenta = defaultdict(int)
    for f in leer_dicts(REGISTRO):
        if not f["fila_origen"].startswith(PREFIJO) or f["estado_A4A5"] != "PENDIENTE":
            continue
        k = f["fuente_canonica"]
        if not intentos.get(k):
            continue
        ids = []
        for u in sorted(urls[k]):
            i = id_por_url.get(u) or id_por_sha.get(ok_sha.get(u, "-"))
            if i:
                ids.append(i)
        n = len(urls[k])
        base = f["nota"].split(" /adquiere ")[0]
        if ids and len(ids) == n:
            estado, extra = "OBTENIDO", f"{n}/{n} archivos; doble descarga A.7 idéntica y estructura verificada"
        elif ids:
            faltan = [f"{u} [{fallo.get(u, 'sin intento')}]" for u in sorted(urls[k])
                      if not (id_por_url.get(u) or id_por_sha.get(ok_sha.get(u, "-")))]
            estado = "OBTENIDO-PARCIAL"
            extra = f"{len(ids)}/{n} archivos; faltan: " + "; ".join(faltan)[:600]
        else:
            estado = f"NO-OBTENIDO-POR-ESTE-AGENTE({intentos[k]} intentos)"
            extra = ("RECETA: bajar a mano desde " + f["url_conocida"] + " y dejar en Descargas MX; fallos: "
                     + "; ".join(sorted({v for u, v in fallo.items() if u in urls[k]}))[:400])
        nueva = dict(f, estado_A4A5=estado, ids_manifiesto=";".join(ids),
                     nota=f"{base} /adquiere {ultimo[k]} (GEN2-CORPUS-COMPLETO-1 P2): intento efectivo "
                          f"{ultimo[k]}; {extra}")
        cuenta[estado.split("(")[0]] += 1
        if escribe:
            upsert_fila(REGISTRO, nueva, campos)
    print(dict(cuenta), "(escrito)" if escribe else "(sin --escribe: sólo reporte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
