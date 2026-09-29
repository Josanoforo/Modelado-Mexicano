"""GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · P2 · unificación de grafías puras de la licencia INEGI.
Solo `licencia`; solo entradas con url_origen en inegi.org.mx cuya licencia es EXACTAMENTE una
grafía de la misma referencia sin anotación propia (las variantes con nota de procedencia se
conservan: la nota es dato). Regla sellada por GEN2-CORPUS-LICENCIAS-1 (página de términos
sha256 97e97599169f75f455877e85edffcf941d512f56c5c00197ebfec783d802c67a). Mecanismo de escritura
y verificación (yaml.safe_load antes/después difiere solo en `licencia`): copiado de
forense/analisis/corpus-licencias-1/aplica_licencias.py.
Uso: python3 forense/analisis/mapa-dominios-1-2/licencias_grafias.py [--aplica]
"""
import re, sys, yaml
P = "data/manifiesto.yaml"
INEGI = "Términos de Libre Uso de la Información del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
VIEJA = "Terminos de Libre Uso de la Informacion del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
GRAFIAS = {
    "Términos de libre uso de la información del INEGI",
    "Términos de Libre Uso de la Información del INEGI",
    "Términos de Libre Uso de la Información del INEGI: https://www.inegi.org.mx/inegi/terminos.html",
    "Términos de uso INEGI",
}

def sin_licencia(v):
    v = str(v or "").strip().lower()
    return v in ("", "none") or "no declarada" in v

def nueva(e):
    host = re.sub(r"^https?://", "", str(e.get("url_origen") or "")).split("/")[0]
    if (host == "inegi.org.mx" or host.endswith(".inegi.org.mx")) and str(e.get("licencia") or "").strip() in GRAFIAS:
        return INEGI
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
