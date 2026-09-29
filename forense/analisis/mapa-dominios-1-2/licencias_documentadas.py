"""GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · P2 · licencias con documento ya registrado en el repo (sin red).
Dos fuentes, las únicas halladas en los 598 sin licencia (barrido de todos los campos no-licencia por
licen*/términos/terms/CC/dominio público/copyright; 28 con pista, 2 reales):
  * ENNViH/MxFLS — declaración verbatim de la portada de https://ennvih-mxfls.org, leída por fetch directo
    el 30/jul/2026 y confirmada desde otra máquina el mismo día, asentada en la entrada del manifiesto
    `ennvih_mxfls_licencia` (campo `hecho`). Cubre «los datos y la documentación». Se aplica a la propia nota,
    a `ennvih1_muestra_diseno` (url en ennvih-mxfls.org) y a los 24 cuestionarios/codebooks `ennvih/doc/*.pdf`.
  * AEA / openICPSR 116334 — LICENSE.txt del paquete, registrado como payload `license`
    (sha256 df9617509f34b9cbe7e8112356cb9f2a3152daeea5921c6c31df17b98518c0c2, 14 974 B), contenido asentado
    en su `usado_para` por REG-LOTE3. Se aplica al propio archivo y a `116334_v1`.
Mecanismo de escritura y verificación (solo cambia `licencia`): copiado de
forense/analisis/corpus-licencias-1/aplica_licencias.py.
Uso: python3 forense/analisis/mapa-dominios-1-2/licencias_documentadas.py [--aplica]
"""
import re, sys, yaml
P = "data/manifiesto.yaml"
INEGI = "Términos de Libre Uso de la Información del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
VIEJA = "Terminos de Libre Uso de la Informacion del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
ENNVIH = ("Dominio público — declaración de ENNViH/MxFLS en https://ennvih-mxfls.org (portada, leída por fetch "
          "30/jul/2026; cita verbatim en manifiesto:ennvih_mxfls_licencia): «La ENNViH es de dominio público. Los datos "
          "y la documentación de la encuesta se pueden descargar sin costo alguno para el usuario.» Citar ENNViH/MxFLS.")
AEA = ("BSD modificada + CC BY 4.0, copyright AEA 2015 — LICENSE.txt del paquete openICPSR 116334, registrado como "
       "payload `license` (sha256 df9617509f34…, 14 974 B); contenido según su registro (REG-LOTE3), no re-leído aquí.")

def sin_licencia(v):
    v = str(v or "").strip().lower()
    return v in ("", "none") or "no declarada" in v

def nueva(e):
    if not sin_licencia(e.get("licencia")):
        return None
    if e["id"] in ("ennvih_mxfls_licencia", "ennvih1_muestra_diseno") or str(e.get("archivo") or "").startswith("ennvih/doc/"):
        return ENNVIH
    if e["id"] in ("license", "116334_v1"):
        return AEA
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
