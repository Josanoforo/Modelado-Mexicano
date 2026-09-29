"""GEN2-MAPA-DOMINIOS-Y-LICENCIAS-1 · P2 (continuación, 29/sep/2026) · licencia por página de términos sellada.

Compuerta del encargo: «Licencia solo con página de términos sellada» (protege borrar/adoptar; PARO c: inventar
una licencia). Esta es la vía de escritura de P2: cada regla vive en `terminos-sellados/reglas-p2.tsv` (D-15: el
parámetro no se repite aquí) y solo se aplica si su evidencia existe en `terminos-sellados/paginas/`, su sha256
coincide con `terminos-sellados/indice.tsv` y su `cita_verbatim` está en el texto de la página. La regla NO-APLICA
no cita página: exige que la entrada no tenga archivo, sha256 ni url_origen (no distribuye ningún dato).
Solo escribe `licencia`, y solo donde hoy no hay (vacía, `none` o «no declarada»); si la entrada traía una nota
propia, se conserva al final («la nota es dato»). Verifica con yaml.safe_load, antes y después, que solo difiere
`licencia` (mecanismo copiado de forense/analisis/corpus-licencias-1/aplica_licencias.py).
`--escribe-base` reescribe la línea base (`sin-licencia-base.tsv`) con lo que siga sin licencia: solo puede encoger.
Uso: python3 forense/analisis/mapa-dominios-1-2/aplica_licencias_p2.py [--aplica] [--escribe-base] | --resumen [--por-regla]
"""
import csv, hashlib, html, re, sys, yaml
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
P = RAIZ / "data/manifiesto.yaml"
D = AQUI / "terminos-sellados"
BASE = RAIZ / "forense/analisis/corpus-licencias-1/sin-licencia-base.tsv"
csv.field_size_limit(10**9)


NOTA_PREVIA = " — nota previa del registro: "


def sin_licencia(v):
    """Vacía, `none` o «no declarada» en la CABEZA del valor: la nota previa que P2 conserva tras NOTA_PREVIA es dato
    histórico y no vuelve a contar como carencia (misma regla en tests/test_corpus_licencias.py)."""
    v = str(v or "").split(NOTA_PREVIA)[0].strip().lower()
    return v in ("", "none") or "no declarada" in v


def lee_tsv(p):
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def texto_visible(raw, sep=" "):
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return norm(html.unescape(re.sub(r"(?s)<[^>]+>", sep, t)))


def verifica_evidencia(reglas, indice):
    """Aborta si una regla cita algo que la página sellada no respalda.
    `cita_verbatim` admite varias citas separadas por « || »: todas deben estar en alguna de las páginas de `evidencia`.
    Un NO-DETERMINABLE sin `evidencia` solo se admite si `base_atribucion` declara el universo (origen no identificable:
    no hay página que sellar)."""
    idx = {r["archivo"]: r for r in indice}
    for r in reglas:
        if r["veredicto"] == "NO-APLICA":
            continue
        archivos = [a for a in r["evidencia"].split(";") if a]
        if not archivos:
            assert r["veredicto"] == "NO-DETERMINABLE" and r["base_atribucion"].strip(), (r["regla_id"], "sin evidencia")
            continue
        textos = []
        for a in archivos:
            assert a in idx, (r["regla_id"], a, "sin fila en indice.tsv")
            b = (D / "paginas" / a).read_bytes()
            assert hashlib.sha256(b).hexdigest() == idx[a]["sha256"], (r["regla_id"], a, "sha256 discordante")
            assert len(b) == int(idx[a]["bytes"]), (r["regla_id"], a, "bytes discordantes")
            raw = b.decode("utf-8", "replace")
            textos.append((norm(raw), texto_visible(raw), texto_visible(raw, "")))
        citas = [norm(c) for c in r["cita_verbatim"].split(" || ") if c.strip()]
        assert citas, (r["regla_id"], "sin cita")
        for c in citas:
            assert any(c in a or c in b or c in d for a, b, d in textos), (r["regla_id"], "cita verbatim ausente de la evidencia sellada", c[:60])


def alcanza(r, e):
    v = r["valor"]
    if r["ambito"] == "url_prefijo":  # alternativas separadas por «|»
        return str(e.get("url_origen") or "").startswith(tuple(v.split("|")))
    if r["ambito"] == "url_exacta":  # igualdad, alternativas separadas por «|»
        return str(e.get("url_origen") or "") in set(v.split("|"))
    if r["ambito"] == "id":
        return e["id"] in {x.strip() for x in v.split(",")}
    if r["ambito"] == "archivo_prefijo":
        return str(e.get("archivo") or "").startswith(tuple(v.split("|")))
    raise ValueError(r["ambito"])


def nueva(e, reglas):
    if not sin_licencia(e.get("licencia")):
        return None
    for r in reglas:
        if not alcanza(r, e):
            continue
        if r["veredicto"] == "NO-APLICA" and any(e.get(k) for k in ("archivo", "sha256", "url_origen")):
            continue
        actual = str(e.get("licencia") or "").strip()
        previa = actual.split(NOTA_PREVIA, 1)[1] if NOTA_PREVIA in actual else actual  # re-aplicar sustituye la cabeza, no anida
        if previa and previa.lower() != "none":
            return r["licencia"] + NOTA_PREVIA + previa, r["regla_id"]
        return r["licencia"], r["regla_id"]
    return None


def dominio(e):
    """Misma convención que la línea base de CORPUS-LICENCIAS-1: token de url_origen antes del primer «/» (sin esquema)."""
    u = str(e.get("url_origen") or "").strip()
    return re.sub(r"^https?://", "", u).split("/")[0] or "<sin>"


def reescribe(txt, cambios):
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
    return "\n".join(out)


def resumen():
    """Solo lectura: cuántas entradas lleva cada regla y cada veredicto (regla de texto más largo si dos comparten prefijo)."""
    reglas = lee_tsv(D / "reglas-p2.tsv")
    es = yaml.safe_load(P.read_text(encoding="utf-8"))
    por_regla, por_ver = {}, {}
    for e in es:
        v = str(e.get("licencia") or "")
        cand = [r for r in reglas if v.startswith(r["licencia"])]
        if cand:
            r = max(cand, key=lambda r: len(r["licencia"]))
            por_regla[r["regla_id"]] = por_regla.get(r["regla_id"], 0) + 1
            por_ver[r["veredicto"]] = por_ver.get(r["veredicto"], 0) + 1
    resto = [e for e in es if sin_licencia(e.get("licencia"))]
    print(f"entradas={len(es)} con licencia de una regla P2={sum(por_regla.values())} sin resolver (regla del test)={len(resto)}")
    for k, n in sorted(por_ver.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {k}")
    if "--por-regla" in sys.argv:
        for k, n in sorted(por_regla.items(), key=lambda kv: -kv[1]):
            print(f"    {n:4d}  {k}")


def main():
    reglas = lee_tsv(D / "reglas-p2.tsv")
    verifica_evidencia(reglas, lee_tsv(D / "indice.tsv"))
    txt = P.read_text(encoding="utf-8")
    antes = yaml.safe_load(txt)
    res = {e["id"]: nueva(e, reglas) for e in antes}
    cambios = {i: v[0] for i, v in res.items() if v}
    por_regla = {}
    for i, v in res.items():
        if v:
            por_regla[v[1]] = por_regla.get(v[1], 0) + 1
    nuevo = reescribe(txt, cambios)
    despues = yaml.safe_load(nuevo)
    assert len(antes) == len(despues)
    for a, d in zip(antes, despues):
        assert {k: v for k, v in a.items() if k != "licencia"} == {k: v for k, v in d.items() if k != "licencia"}, a["id"]
        assert d.get("licencia") == cambios.get(a["id"], a.get("licencia")), a["id"]
    print(f"reglas={len(reglas)} evidencia=verificada entradas={len(antes)} cambiadas={len(cambios)} verificado=solo-licencia")
    for rid, c in sorted(por_regla.items()):
        print(f"  {c:4d}  {rid}")
    resto = [e for e in despues if sin_licencia(e.get("licencia"))]
    print(f"sin licencia (regla del test) antes={sum(1 for e in antes if sin_licencia(e.get('licencia')))} después={len(resto)}")
    if "--aplica" in sys.argv:
        P.write_text(nuevo, encoding="utf-8")
    if "--escribe-base" in sys.argv:
        with open(BASE, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["id", "dominio", "licencia_actual"])
            for e in resto:
                w.writerow([e["id"], dominio(e), re.sub(r"\s+", " ", str(e.get("licencia") or ""))])


if __name__ == "__main__":
    resumen() if "--resumen" in sys.argv else main()
