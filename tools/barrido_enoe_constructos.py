#!/usr/bin/env python3
"""ADQ-ENOE-PRE2019 · T2. Barre las olas pre-2019 contra los 9 constructos
con los terminos que COMMIT A (`bbis-adq-enoe-pre2019` §4) congelo.

Tres universos, los tres con su cardinalidad declarada (A.13):

  A  · cuestionarios y descriptores de instrumento (PDF), texto completo.
  B1 · inventario de VARIABLES de las olas adquiridas, leido de los CSV.
  B2 · el mismo inventario para las olas post-2019 ya en disco, para el
       diferencial pre-vs-post: una variable presente antes y ausente
       despues es, literalmente, "lo que las olas viejas traen y las
       nuevas no". Es la pregunta del encargo, contestada por conjunto y
       no por muestreo.

Salidas (TSV, escritas con join('\t') plano -- el modulo csv corrompe los
TSV de este proyecto, `ADR-123(h)`):
  data/barrido-enoe-constructos-universoA.tsv
  data/barrido-enoe-variables-pre-vs-post.tsv
"""
import io, os, re, subprocess, sys, unicodedata, zipfile

CORPUS = "/home/pc0/mm-corpus/raw"

# ── §4 de COMMIT A, verbatim ────────────────────────────────────────────
FILAS = [
 ("aversion_riesgo", "riesgo·arriesg·incertidumbre·apost·azar·loteria·sorteo·garantizado·asegurad·seguro de·preferiria·perdida·precautorio"),
 ("confianza_institucional[seguridad]", "policia·ejercito·marina·guardia nacional·seguridad publica"),
 ("confianza_institucional[educacion]", "escuela·maestro·profesor·sep·educacion publica"),
 ("confianza_institucional[salud]", "imss·issste·hospital·clinica·centro de salud·medico·seguro popular·insabi"),
 ("confianza_institucional[electoral]", "ine·ife·eleccion·partido politico·voto·campana electoral"),
 ("confianza_institucional[justicia-policia]", "juez·ministerio publico·tribunal·fiscalia·denuncia·juzgado"),
 ("confianza_institucional[financiera]", "banco·banca·afore·caja de ahorro·sofom·cooperativa de ahorro·financiera"),
 ("deferencia", "obedec·autoridad·jerarqui·acatar·permiso de·jefe·mandar·sumis·respetar a"),
 ("exposicion_violencia", "violencia·delito·robo·asalto·agresion·inseguridad·victima·amenaza·extorsion·homicidio·secuestro·golpe"),
 ("familismo_apoyo", "ayuda de·apoyo de·pariente·familiar·remesa·red de apoyo·presta·cuidado de·se hacen cargo"),
 ("familismo_obligacion", "obligacion·deber de·mantener a·responsable de·cuidar a·hacerse cargo·sostener a·manutencion"),
 ("horizonte_temporal", "ahorr·futuro·plazo·planea·planific·jubilac·retiro·pension·afore·prevision·meta·proyecto de vida"),
 ("radio_confianza", "confia·confianza·vecino·desconocido·extrano·comunidad·la mayoria de la gente·amistad"),
 ("sens_estatus", "estatus·posicion social·prestigio·clase social·nivel socioeconomico·apariencia·que diran·respetad·vergüenza·pena"),
]

# Universo A: los 6 cuestionarios ya en disco (los que CAL-ENOE Fase A leyo,
# y que gobiernan 2016-2019) + los 10 descriptores de instrumento que este
# acto adquirio, incluidas las dos eras que CAL-ENOE nunca abrio.
PDFS = ["c_amp_v5.pdf", "c_amp_v6a.pdf", "c_bas_v5.pdf", "c_bas_v7.pdf",
        "c_sdem_v4.pdf", "c_sdem_v5a.pdf",
        "fd_c_amp_v1.pdf", "fd_c_amp_v2.pdf", "fd_c_amp_v3.pdf", "fd_c_amp_v4.pdf",
        "fd_c_bas_v1.pdf", "fd_c_bas_v2.pdf", "fd_c_bas_amp_conapo.pdf",
        "fd_c_bas_amp_15ymas.pdf", "enoe_123_fd_c_bas_amp.pdf",
        "enoe_325_fd_c_bas_amp.pdf"]


def plegar(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def texto_pdf(path):
    """Dos extractores independientes; se devuelve la UNION. Un termino que
    solo uno de los dos ve cuenta igual: el objetivo es no perder aciertos."""
    partes = []
    r = subprocess.run(["pdftotext", "-layout", path, "-"],
                       capture_output=True, text=True, errors="replace")
    if r.returncode == 0:
        partes.append(r.stdout)
    try:
        import pypdf
        partes.append("\n".join((p.extract_text() or "")
                                for p in pypdf.PdfReader(path).pages))
    except Exception as e:
        partes.append("")
        print(f"    (pypdf fallo en {os.path.basename(path)}: {e})", file=sys.stderr)
    return partes


def universo_a():
    filas, censo = [], []
    for nombre in PDFS:
        p = os.path.join(CORPUS, nombre)
        if not os.path.exists(p):
            censo.append((nombre, "AUSENTE", 0, 0)); continue
        pt, pp = texto_pdf(p)
        censo.append((nombre, "LEIDO", len(pt), len(pp)))
        union = plegar(pt + "\n" + pp)
        for fila, terminos in FILAS:
            for t in terminos.split("·"):
                tp = plegar(t)
                n = union.count(tp)
                if n:
                    i = union.find(tp)
                    ctx = re.sub(r"\s+", " ", union[max(0, i-70):i+len(tp)+70]).strip()
                    filas.append((fila, t, nombre, n, ctx))
    return filas, censo


def variables_de_zip(path):
    """Nombres de variable por TABLA, normalizados entre los dos empaquetados.

    `/microdatos/` (pre-2019):  COE1T116.csv          -> COE1
    `/datosabiertos/` (post):   conjunto_de_datos_<t>_enoe_YYYY_Nt/
                                conjunto_de_datos/conjunto_de_datos_<t>_enoe_YYYY_Nt.csv
    Se ignoran `catalogos/`, `diccionario_de_datos/` y `bitacora_de_cambios`:
    no son tablas de dato, y contarlos inventa variables que no existen.
    """
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            low = n.lower()
            if not low.endswith(".csv"):
                continue
            base = os.path.basename(low)[:-4]
            if "/catalogos/" in low or "/diccionario_de_datos/" in low:
                continue
            if base.startswith("bitacora_de_cambios"):
                continue
            m = re.match(r"^conjunto_de_datos_(coe1|coe2|hog|sdem|viv)_enoen?_\d{4}_\dt$", base)
            if m:
                tabla = m.group(1).upper()
            else:
                m2 = re.match(r"^(coe1t|coe2t|hogt|sdemt|vivt)\d+$", base)
                if not m2:
                    continue
                tabla = m2.group(1).upper().rstrip("T") if m2.group(1) in ("hogt", "sdemt", "vivt") \
                        else m2.group(1)[:-1].upper()
            with z.open(n) as f:
                linea = io.TextIOWrapper(f, encoding="latin-1").readline()
            linea = linea.lstrip("\ufeff")
            cols = []
            for c in linea.split(","):
                c = c.strip().strip('"').strip()
                c = c.lstrip("\ufeff")
                # BOM UTF-8 leido como latin-1
                if c.startswith("\xef\xbb\xbf") or c.startswith("\u00ef\u00bb\u00bf"):
                    c = c[3:]
                if c:
                    cols.append(c.upper())
            out.setdefault(tabla, set()).update(cols)
    return out


def _filas_y_hash(path):
    """(variables, n_filas, sha256_del_contenido) por tabla de un ZIP."""
    import hashlib
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            low = n.lower()
            if not low.endswith(".csv") or "/catalogos/" in low or "/diccionario_de_datos/" in low:
                continue
            base = os.path.basename(low)[:-4]
            if base.startswith("bitacora_de_cambios"):
                continue
            m = re.match(r"^conjunto_de_datos_(coe1|coe2|hog|sdem|viv)_enoen?_\d{4}_\dt$", base) \
                or re.match(r"^(coe1t|coe2t|hogt|sdemt|vivt)\d+$", base)
            if not m:
                continue
            tabla = m.group(1).upper().rstrip("T") if m.group(1).endswith("t") else m.group(1).upper()
            crudo = z.read(n)
            out[tabla] = (crudo.count(b"\n"), hashlib.sha256(crudo).hexdigest())
    return out


def puente_distribucion():
    """La MISMA ola por las dos rutas de INEGI. Mide la costura pre-post en
    vez de suponerla: si las dos rutas sirven lo mismo, se ve aqui."""
    a = os.path.join(CORPUS, "2018trim4_csv.zip")
    b = os.path.join(CORPUS, "conjunto_de_datos_enoe_2018_4t_csv.zip")
    if not (os.path.exists(a) and os.path.exists(b)):
        return []
    va, vb = variables_de_zip(a), variables_de_zip(b)
    fa, fb = _filas_y_hash(a), _filas_y_hash(b)
    filas = []
    for tb in sorted(set(va) | set(vb)):
        x, y = va.get(tb, set()), vb.get(tb, set())
        na, ha = fa.get(tb, (0, "")); nb, hb = fb.get(tb, (0, ""))
        filas.append((tb, len(x), len(y), len(x - y), len(y - x), na, nb,
                      "IDENTICO" if ha == hb else "DIFIERE", ha[:16], hb[:16]))
    return filas


def sonda_eras():
    """Diferencial exhaustivo por ola-sonda contra TODO el post-2019."""
    post = sorted(f for f in os.listdir(CORPUS)
                  if re.match(r"conjunto_de_datos_enoen?_20\d\d_[1-4]t_csv\.zip$", f))
    ipost = {}
    for a in post:
        for tb, c in variables_de_zip(os.path.join(CORPUS, a)).items():
            ipost.setdefault(tb, set()).update(c)
    filas = []
    for ola in ("2005trim1", "2008trim1", "2012trim1", "2014trim1", "2016trim1", "2018trim4"):
        p = os.path.join(CORPUS, ola + "_csv.zip")
        if not os.path.exists(p):
            continue
        for tb, c in sorted(variables_de_zip(p).items()):
            solo = sorted(c - ipost.get(tb, set()))
            filas.append((ola, tb, len(c), len(solo), " ".join(solo) if solo else "-"))
    return filas, len(post)


def main():
    print("── UNIVERSO A · PDF ──")
    filas_a, censo = universo_a()
    for n, e, a, b in censo:
        print(f"  {e:8s} {n:32s} pdftotext={a:>8,}  pypdf={b:>8,}")
    leidos = sum(1 for c in censo if c[1] == "LEIDO")
    chars = sum(c[2] + c[3] for c in censo)
    print(f"  → {leidos}/{len(PDFS)} PDF leidos · {chars:,} caracteres examinados")

    with open("data/barrido-enoe-constructos-universoA.tsv", "w", encoding="utf-8") as f:
        f.write("fila\ttermino\tarchivo\tn_aciertos\tcontexto_primer_acierto\n")
        for r in sorted(filas_a):
            f.write("\t".join(str(x) for x in r) + "\n")
    con = {r[0] for r in filas_a}
    print(f"  → {len(filas_a)} aciertos brutos en {len(con)}/14 filas")
    for fila, _ in FILAS:
        if fila not in con:
            print(f"     CERO ACIERTOS: {fila}")

    print("\n── UNIVERSO B · inventario de variables ──")
    pre = sorted(f for f in os.listdir(CORPUS) if re.match(r"20(1[678])trim[1-4]_csv\.zip$", f))
    post = sorted(f for f in os.listdir(CORPUS) if re.match(r"conjunto_de_datos_enoen?_20\d\d_[1-4]t_csv\.zip$", f))
    print(f"  pre  = {len(pre)} olas · post = {len(post)} olas")

    def inventario(archivos):
        inv = {}
        for a in archivos:
            for tabla, cols in variables_de_zip(os.path.join(CORPUS, a)).items():
                inv.setdefault(tabla, set()).update(cols)
        return inv

    ipre, ipost = inventario(pre), inventario(post)
    tablas = sorted(set(ipre) | set(ipost))
    with open("data/barrido-enoe-variables-pre-vs-post.tsv", "w", encoding="utf-8") as f:
        f.write("tabla\tvariable\tpresente_pre_2019\tpresente_post_2019\tclase\n")
        tot = {"SOLO_PRE": 0, "SOLO_POST": 0, "AMBAS": 0}
        for t in tablas:
            a, b = ipre.get(t, set()), ipost.get(t, set())
            for v in sorted(a | b):
                cl = "AMBAS" if v in a and v in b else ("SOLO_PRE" if v in a else "SOLO_POST")
                tot[cl] += 1
                f.write(f"{t}\t{v}\t{'si' if v in a else 'no'}\t{'si' if v in b else 'no'}\t{cl}\n")
    print(f"  tablas: {', '.join(tablas)}")
    print(f"  SOLO_PRE={tot['SOLO_PRE']}  SOLO_POST={tot['SOLO_POST']}  AMBAS={tot['AMBAS']}")
    print("\n  ── VARIABLES SOLO EN PRE-2019 (candidatas de 'lo que las nuevas no traen') ──")
    hubo = False
    for t in tablas:
        solo = sorted(ipre.get(t, set()) - ipost.get(t, set()))
        if solo:
            hubo = True
            print(f"  {t}: {' '.join(solo)}")
    if not hubo:
        print("  NINGUNA en las 5 tablas.")

    print("\n── PUENTE DE DISTRIBUCION · 2018T4 por las dos rutas de INEGI ──")
    pf = puente_distribucion()
    with open("data/barrido-enoe-puente-distribucion.tsv", "w", encoding="utf-8") as f:
        f.write("tabla\tvars_microdatos\tvars_datosabiertos\tsolo_microdatos\tsolo_datosabiertos"
                "\tfilas_microdatos\tfilas_datosabiertos\tcontenido\tsha_micro16\tsha_abier16\n")
        for r in pf:
            f.write("\t".join(str(x) for x in r) + "\n")
            print(f"  {r[0]:5s} vars {r[1]}/{r[2]} (solo_micro={r[3]} solo_abier={r[4]}) · "
                  f"filas {r[5]:,}/{r[6]:,} · contenido {r[7]}")

    print("\n── SONDA DE ERAS · cada ola contra TODO el post-2019 ──")
    sf, npost = sonda_eras()
    with open("data/barrido-enoe-sonda-eras.tsv", "w", encoding="utf-8") as f:
        f.write("ola\ttabla\tn_variables\tn_ausentes_del_post\tvariables_ausentes_del_post\n")
        for r in sf:
            f.write("\t".join(str(x) for x in r) + "\n")
    huerfanas = sum(r[3] for r in sf)
    olas = sorted({r[0] for r in sf})
    print(f"  {len(olas)} olas-sonda ({', '.join(olas)}) contra {npost} olas post-2019")
    print(f"  variables presentes en una ola pre-2019 y AUSENTES de todo el post-2019: {huerfanas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
