"""GEN2-CORPUS-LICENCIAS-1 · escritura por línea del campo `licencia` (ningún otro campo).

Reglas por dominio (una por portal). Hoy solo inegi.org.mx: página de términos leída
2026-09-28 (GET 200, 10442 B, sha256 97e97599169f75f455877e85edffcf941d512f56c5c00197ebfec783d802c67a,
el mismo que leyó GEN2-ADQ-F6-DIRIGIDA-1 el 22/sep). Además unifica la grafía sin acento.
Verifica tras escribir: yaml.safe_load antes/después difiere solo en `licencia`.
Uso: python3 forense/analisis/corpus-licencias-1/aplica_licencias.py [--aplica]
"""
import re, sys, yaml
P = "data/manifiesto.yaml"
INEGI = "Términos de Libre Uso de la Información del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
VIEJA = "Terminos de Libre Uso de la Informacion del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
REGLAS = {"inegi.org.mx": INEGI}

def sin_licencia(v):
    v = str(v or "").strip().lower()
    return v in ("", "none") or "no declarada" in v

def nueva(e):
    lic = e.get("licencia")
    if lic == VIEJA:
        return INEGI
    if sin_licencia(lic):
        host = re.sub(r"^https?://", "", str(e.get("url_origen") or "")).split("/")[0]
        for dom, val in REGLAS.items():
            if host == dom or host.endswith("." + dom):
                return val
    return None

def main():
    txt = open(P, encoding="utf-8").read()
    antes = yaml.safe_load(txt)
    cambios = {e["id"]: nueva(e) for e in antes if nueva(e)}
    lines = txt.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        m = re.match(r"^- id: *(.+?) *$", lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        j = i + 1
        while j < n and not lines[j].startswith("- ") and not (lines[j] and not lines[j][0].isspace()):
            j += 1
        bloque = lines[i:j]
        eid = yaml.safe_load(lines[i][2:])["id"]
        if eid in cambios:
            val = "  licencia: " + yaml.safe_dump(cambios[eid], allow_unicode=True, width=10**6).strip().removesuffix("\n...").removesuffix("...").strip()
            k = next((x for x, l in enumerate(bloque) if l.startswith("  licencia:")), None)
            if k is None:
                fin = len(bloque)
                while fin > 1 and bloque[fin - 1].strip() in ("",) or (fin > 1 and bloque[fin - 1].lstrip().startswith("#")):
                    fin -= 1
                bloque = bloque[:fin] + [val] + bloque[fin:]
            else:
                e = k + 1
                while e < len(bloque) and bloque[e].startswith("    "):
                    e += 1
                bloque = bloque[:k] + [val] + bloque[e:]
        out.extend(bloque); i = j
    nuevo = "\n".join(out)
    despues = yaml.safe_load(nuevo)
    assert len(antes) == len(despues)
    for a, d in zip(antes, despues):
        assert {k: v for k, v in a.items() if k != "licencia"} == {k: v for k, v in d.items() if k != "licencia"}, a["id"]
        assert d.get("licencia") == cambios.get(a["id"], a.get("licencia")), a["id"]
    print(f"entradas={len(antes)} cambiadas={len(cambios)} verificado=solo-licencia")
    if "--aplica" in sys.argv:
        open(P, "w", encoding="utf-8").write(nuevo)
main()
