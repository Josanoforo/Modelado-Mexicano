#!/usr/bin/env python3
"""Reproduce por comando el conteo de estratos singleton ENOE2024T4 (#1222).

Fuente: forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json
(artefacto AGREGADO por estrato; no es el diseño muestral). Stdlib. No escribe nada.
Verifica: sha256 del artefacto contra enoe-producto.sha256; listas de singleton por
grupo (1=SEX1, 2=SEX2); unión, intersección y suma; coherencia con singleton_union y
singleton_detalle (upm_todas == 1).
"""
import hashlib, json, pathlib, sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
BASE = RAIZ / "forense/analisis/familias-2027-enoe-inferencia-1"
AUD = BASE / "diagnostico/enoe-auditoria.json"
MAN = BASE / "enoe-producto.sha256"

def main():
    crudo = AUD.read_bytes()
    sha = hashlib.sha256(crudo).hexdigest()
    rel = str(AUD.relative_to(RAIZ))
    reg = {l.split()[1]: l.split()[0] for l in MAN.read_text().splitlines() if l.strip()}
    print(f"artefacto: {rel}")
    print(f"sha256 calculado: {sha}")
    print(f"sha256 registrado: {reg.get(rel)} -> {'COINCIDE' if reg.get(rel)==sha else 'DISCORDANTE'}")
    d = json.loads(crudo)
    print(f"id oro: {d['id']} · archivo_sha256 oro: {d['archivo_sha256']}")
    s = {g: set(v["singleton"]) for g, v in d["grupos"].items()}
    for g in sorted(s):
        print(f"grupo {g}: singleton={len(s[g])} (lista) · estratos={d['grupos'][g]['estratos']}")
    u = set().union(*s.values()); i = set.intersection(*s.values())
    print(f"union={len(u)} interseccion={len(i)} suma_sin_deduplicar={sum(len(x) for x in s.values())}")
    print(f"singleton_union declarado={d['singleton_union']} -> {'COINCIDE' if d['singleton_union']==len(u) else 'DISCORDANTE'}")
    det = {x["estrato"] for x in d["singleton_detalle"] if x["upm_todas"] == 1}
    print(f"singleton_detalle upm_todas==1: {len(det)} · igual a union: {det == u}")
    print("marcos (filtrados, informativo):", {k: v["singleton"] for k, v in d["marcos"].items()})
    ok = reg.get(rel) == sha and len(u) == len(i) == d["singleton_union"] and det == u
    print("VEREDICTO:", "REPRODUCE" if ok else "NO-REPRODUCE")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
