#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS.

L13 (ADR-312) midio `p` = e.firma / padron del SAT y salio AMBIGUA-POR-UNIVERSO:
las dos cotas cayeron en tramos distintos del falsador. Mesa no autoriza sellar
sobre el padron del SAT —una SUBPOBLACION— contra una regla poblacional, y pide
el universo poblacional. Este acto MIDE Y NO ADJUDICA: agrega una tercera lectura
de universo (ENOE, poblacion ocupada) y entrega a mesa la tabla de las tres.

  lectura A  denominador POBLACIONAL   ocupados totales (ENOE)
  lectura A' puente                    ocupados FORMALES (ENOE)
  lectura B  padron amplio (L13)       Total del padron activo del SAT
  lectura C  padron obligado (L13)     Total - Asalariados (PF)

B y C se RE-CITAN de data/l13-sat-efirma-v1_0.json; NO se recalculan.

ESCALA DECLARADA (A-bis 3). Numerador ADMINISTRATIVO sobre denominador de
ENCUESTA: dos fuentes cuyos universos no coinciden exactamente. Lo que sale es
un CAMPO del entorno, no una probabilidad individual de conducta (precedente:
firma p1 de mesa, 2/sep/2026, MAESTRA34-L6, propagada por ADR-299). Comparable
con el 0.09 asignado SOLO en signo y orden de magnitud; NUNCA como «difiere en Z %».
Este modulo NO emite fila de veredicto: no hay tramo, no hay adjudicacion.

Uso:
    python3 tools/medidor_l14_coercitivo_universos.py --censo
    python3 tools/medidor_l14_coercitivo_universos.py --mide --json data/l14-coercitivo-universos-v1_0.json
"""
import argparse, csv, hashlib, io, json, math, os, re, sys, zipfile
from collections import defaultdict

RAICES_LOCAL = "data/raices.local.yaml"
MANIFIESTO = "data/manifiesto.yaml"
L13_JSON = "data/l13-sat-efirma-v1_0.json"

# ══════════════════════ SPEC CONGELADA — COMMIT-1 ══════════════════════
#
# Escrita y commiteada ANTES de calcular cifra alguna. El censo A.4 abre el zip
# para leer ESTRUCTURA (nombres de campo, diccionario, catalogos de claves); no
# suma ningun ponderador ni calcula ningun cociente.
#
# TRIMESTRE DE CORTE. El encargo deja la eleccion a P0 entre 2025-4T y 2026-1T,
#   «el que exista con COE y SDEM». LOS DOS existen con COE1/COE2/SDEM/HOG/VIV en
#   el corpus, asi que la existencia NO desempata y hace falta un criterio, que se
#   declara aqui antes de medir: se toma 2025-4T porque su periodo de referencia
#   (oct-dic 2025) CONTIENE el corte del numerador del SAT (2025-12, L13). Emparejar
#   el numerador de diciembre-2025 con un denominador de ene-mar 2026 metaria un
#   desfase de un trimestre sin ninguna ganancia. Se declara la eleccion y su razon;
#   no se mide el otro trimestre «para ver cual sale mejor».
#
# PAYLOAD. id `enoe_2025_4t_csv` de data/manifiesto.yaml, raiz `data_raw`. Se abre
#   por IDENTIDAD (sha256 contra el manifiesto), no por nombre: si el sha no calza,
#   PARO.
#
# TABLA. SDEM (`conjunto_de_datos_sdem_enoe_2025_4t.csv`), una fila por persona.
#
# FILTRO (poblacion en universo). Los tres codigos se leen del catalogo del propio
#   zip y se comparan contra los de aqui; DISCORDANCIA -> PARO.
#     r_def == 0     entrevista completa (r_def.csv: «0,Entrevista completa»)
#     c_res in {1,3} residente habitual o nuevo residente; se excluye 2 «ausente
#                    definitivo» (c_res.csv)
#     eda 15..98     poblacion de 15 y mas (la ENOE 15ymas ya recorta, el filtro es
#                    guardia explicita; 99 = no especificado, fuera)
#     clase2 == 1    poblacion OCUPADA (clase2.csv: «1,Poblacion ocupada»)
#
# PONDERADOR. fac_tri (diccionario SDEM: «Ponderador trimestral», N, 1-999999).
#   Los totales son SUMA de fac_tri sobre las filas del filtro.
#
# TRES DENOMINADORES.
#   (a) D_ocupados   = filtro
#   (b) D_informales = filtro & emp_ppal == 1   (emp_ppal.csv: «1,Empleo informal»)
#       D_formales   = filtro & emp_ppal == 2   («2,Empleo formal»)
#   (c) D_formal_noasal = filtro & emp_ppal == 2 & pos_ocu in {2,3}
#       (pos_ocu.csv: «2,Empleadores», «3,Trabajadores por cuenta propia»);
#       es la APROXIMACION ENOE del «obligado» a e.firma: excluye a los
#       subordinados y remunerados (1), a los sin pago (4) y al no especificado (5).
#   Guardia de particion: (b) informales + formales debe reconstruir (a) salvo las
#   filas con emp_ppal == 0; el residuo se reporta, no se esconde.
#
# IC95 POR DISENO. Estimador de conglomerado ultimo (ultimate cluster) sobre el
#   diseno estratificado bietapico de la ENOE: estrato = est_d_tri, UPM = upm.
#     v(Y) = SUM_h  n_h/(n_h-1) * SUM_a (y_ha - ybar_h)^2      y_ha = total de la UPM
#   Estratos con una sola UPM aportan 0 y SE CUENTAN en el JSON (no se colapsan en
#   silencio). IC95 = Y +- 1.96*sqrt(v). El IC de la razon p = N/D con N constante
#   administrativa se obtiene invirtiendo el IC del denominador: el limite inferior
#   de p usa el limite SUPERIOR de D. No hay varianza del numerador: es un censo.
#
# NUMERADOR (unico para las cuatro razones). N = 32 331 680, contribuyentes con
#   PRIMER certificado de e.firma acumulados 2004-01..2025-12 (`firelenumcontri`,
#   L13/ADR-312), re-citado de data/l13-sat-efirma-v1_0.json. GUARDIA DE PREMISA
#   AJENA: el encargo lo llama «e.firma VIGENTE al corte»; la fuente NO dice eso —
#   el certificado caduca a los 4 anos y el acumulado no da de baja a quien salio.
#   N es COTA SUPERIOR del stock vigente, y por tanto las cuatro p son cotas
#   SUPERIORES de la adopcion vigente. Se mide con la premisa corregida y se declara.
#
# SIN VEREDICTO. Este modulo no evalua ningun tramo del falsador B-bis y no escribe
#   ninguna clave `veredicto`. La comparacion con el 0.09 asignado se limita al
#   orden de magnitud, en la nota. La pregunta «a quien describe coercitivo» es de
#   mesa, no del ejecutor.
#
#   «el primer resultado que produzca este procedimiento es el que se reporta»
# ═══════════════════════════════════════════════════════════════════════

PAYLOAD_ID = "enoe_2025_4t_csv"
TRIMESTRE = "2025_4t"
ARCHIVO = "conjunto_de_datos_enoe_2025_4t_csv.zip"
BASE = "conjunto_de_datos_sdem_enoe_%s" % TRIMESTRE
P_DATOS = "%s/conjunto_de_datos/%s.csv" % (BASE, BASE)
P_DICC = "%s/diccionario_de_datos/diccionario_datos_sdem_enoe_%s.csv" % (BASE, TRIMESTRE)
P_CAT = "%s/catalogos/%%s.csv" % BASE

# Claves que la spec de arriba usa. El censo y --mide las verifican contra el
# catalogo del zip; discordancia -> PARO (lo exige el encargo, literal).
CLAVES = {
    "r_def":    {"0": "Entrevista completa"},
    "c_res":    {"1": "Residente habitual", "3": "Nuevo residente"},
    "clase2":   {"1": "Poblacion ocupada"},
    "emp_ppal": {"1": "Empleo informal", "2": "Empleo formal"},
    "pos_ocu":  {"2": "Empleadores", "3": "Trabajadores por cuenta propia"},
}
CAMPOS = ["r_def", "c_res", "eda", "clase2", "emp_ppal", "pos_ocu",
          "fac_tri", "upm", "est_d_tri"]

Z196 = 1.959963984540054


def raiz(nombre="data_raw"):
    """Resuelve una raiz de data/manifiesto.yaml. PARA si no esta configurada: un
    worktree nuevo nace sin data/raices.local.yaml, y un «no existe» que en realidad
    es «no configurada» es el falso negativo que A.13 persigue."""
    if os.path.islink("data/raw") or os.path.isdir("data/raw"):
        if nombre == "data_raw":
            return "data/raw"
    if not os.path.exists(RAICES_LOCAL):
        raise SystemExit("PARO: falta %s y data/raw no esta enlazada." % RAICES_LOCAL)
    for linea in open(RAICES_LOCAL, encoding="utf-8"):
        linea = linea.split("#")[0].strip()
        if linea.startswith(nombre + ":"):
            return linea.split(":", 1)[1].strip()
    raise SystemExit("PARO: %s no define '%s'." % (RAICES_LOCAL, nombre))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_manifiesto(pid):
    txt = open(MANIFIESTO, encoding="utf-8").read()
    for ent in re.split(r"\n(?=- id: )", txt):
        m = re.match(r"- id: (\S+)", ent)
        if m and m.group(1) == pid:
            s = re.search(r"\n  sha256: (\S+)", ent)
            return s.group(1) if s else None
    return None


def abre_zip():
    """(ZipFile, ruta, sha_disco, sha_manifiesto). Identidad, no nombre."""
    path = os.path.join(raiz(), ARCHIVO)
    if not os.path.exists(path):
        raise SystemExit("PARO: payload ausente en disco: %s (id %s)" % (path, PAYLOAD_ID))
    sd, sm = sha256(path), sha_manifiesto(PAYLOAD_ID)
    if sm and sd != sm:
        raise SystemExit("PARO: sha256 del payload no calza con el manifiesto.\n"
                         "  disco      %s\n  manifiesto %s" % (sd, sm))
    return zipfile.ZipFile(path), path, sd, sm


def dec(b):
    """Los .csv del zip mezclan codificaciones: los catalogos y el diccionario
    vienen en UTF-8 y el microdato en latin-1. Se prueba UTF-8 y se cae a
    latin-1; adivinar una sola y decodificar mal es como un acento convierte una
    guardia de catalogo en un PARO falso."""
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def lee_catalogo(z, nombre):
    txt = dec(z.read(P_CAT % nombre))
    out = {}
    for fila in csv.reader(io.StringIO(txt)):
        if len(fila) >= 2 and fila[0].strip().upper() != "CVE":
            out[fila[0].strip()] = fila[1].strip()
    return out


def verifica_claves(z):
    """Compara los codigos de la SPEC contra el catalogo del zip. PARO si discuerdan.
    Compara por PREFIJO normalizado porque el .csv viene en latin-1 y la casa no
    adivina acentos: «Poblacion ocupada» vs «Poblacion ocupada» con tilde."""
    def norm(s):
        s = s.lower()
        for a, b in zip("áéíóúñ", "aeioun"):
            s = s.replace(a, b)
        return re.sub(r"[^a-z0-9]+", " ", s).strip()

    reporte, discordes = [], []
    for campo, esperado in CLAVES.items():
        cat = lee_catalogo(z, campo)
        for cve, desc in esperado.items():
            real = cat.get(cve)
            ok = real is not None and norm(real) == norm(desc)
            reporte.append({"campo": campo, "cve": cve, "spec": desc,
                            "catalogo": real, "concuerda": ok})
            if not ok:
                discordes.append("%s=%s: spec «%s» vs catalogo «%s»"
                                 % (campo, cve, desc, real))
    if discordes:
        raise SystemExit("PARO: discordancia con el catalogo ENOE:\n  "
                         + "\n  ".join(discordes))
    return reporte


def campos_del_diccionario(z):
    txt = dec(z.read(P_DICC))
    out = {}
    for fila in csv.reader(io.StringIO(txt)):
        if len(fila) >= 4:
            out[fila[3].strip().lower()] = {"desc": fila[0].strip(),
                                            "tipo": fila[2].strip(),
                                            "rango": fila[-1].strip()}
    return out


# ─────────────────────────── estimacion ───────────────────────────

class Acumulador:
    """Total ponderado + varianza de conglomerado ultimo, en una sola pasada."""

    def __init__(self):
        self.total = 0.0
        self.n_filas = 0
        self.upm = defaultdict(float)      # (estrato, upm) -> total de la UPM

    def agrega(self, estrato, upm, w):
        self.total += w
        self.n_filas += 1
        self.upm[(estrato, upm)] += w

    def varianza(self):
        """v(Y) = SUM_h n_h/(n_h-1) SUM_a (y_ha - ybar_h)^2. Estratos con una sola
        UPM aportan 0 y se cuentan aparte: colapsarlos en silencio es lo que la
        casa no hace."""
        por_estrato = defaultdict(list)
        for (h, _a), y in self.upm.items():
            por_estrato[h].append(y)
        v, solitarios = 0.0, 0
        for h, ys in por_estrato.items():
            n = len(ys)
            if n < 2:
                solitarios += 1
                continue
            m = sum(ys) / n
            v += (n / (n - 1.0)) * sum((y - m) ** 2 for y in ys)
        return v, len(por_estrato), solitarios

    def ic95(self):
        v, n_est, solit = self.varianza()
        ee = math.sqrt(v)
        return {"total": self.total, "filas_muestra": self.n_filas,
                "upm_distintas": len(self.upm), "estratos": n_est,
                "estratos_una_upm": solit, "ee": ee,
                "ic95_inf": self.total - Z196 * ee,
                "ic95_sup": self.total + Z196 * ee,
                "cv": (ee / self.total) if self.total else None}


def mide(z):
    acc = {k: Acumulador() for k in
           ("ocupados", "informales", "formales", "formal_noasal")}
    emp_ppal_otro = 0.0
    pos_ocu_formales = defaultdict(float)
    leidas = descartadas = 0

    with z.open(P_DATOS) as fh:
        rdr = csv.DictReader(io.TextIOWrapper(fh, encoding="latin-1", newline=""))
        faltan = [c for c in CAMPOS if c not in rdr.fieldnames]
        if faltan:
            raise SystemExit("PARO: faltan campos en SDEM: %s" % faltan)
        for fila in rdr:
            leidas += 1
            if fila["r_def"].strip() not in ("0", "00"):
                descartadas += 1
                continue
            if fila["c_res"].strip() not in ("1", "3"):
                descartadas += 1
                continue
            try:
                eda = int(fila["eda"])
            except ValueError:
                descartadas += 1
                continue
            if not (15 <= eda <= 98):
                descartadas += 1
                continue
            if fila["clase2"].strip() != "1":
                descartadas += 1
                continue
            w = float(fila["fac_tri"])
            h, u = fila["est_d_tri"].strip(), fila["upm"].strip()
            acc["ocupados"].agrega(h, u, w)
            emp = fila["emp_ppal"].strip()
            pos = fila["pos_ocu"].strip()
            if emp == "1":
                acc["informales"].agrega(h, u, w)
            elif emp == "2":
                acc["formales"].agrega(h, u, w)
                pos_ocu_formales[pos] += w
                if pos in ("2", "3"):
                    acc["formal_noasal"].agrega(h, u, w)
            else:
                emp_ppal_otro += w

    # ── guardias marginales: un lector nuevo devuelve VACIO, no error ──
    if leidas == 0:
        raise SystemExit("PARO: SDEM leido con 0 filas.")
    if acc["ocupados"].n_filas == 0:
        raise SystemExit("PARO: 0 filas pasan el filtro de ocupados — lector vacio.")
    for k, a in acc.items():
        if a.total <= 0:
            raise SystemExit("PARO: denominador '%s' es 0." % k)
    residuo = acc["ocupados"].total - acc["informales"].total - acc["formales"].total
    if abs(residuo - emp_ppal_otro) > 1.0:
        raise SystemExit("PARO: la particion informal/formal no cierra: residuo %.1f "
                         "vs emp_ppal fuera de {1,2} %.1f" % (residuo, emp_ppal_otro))
    if acc["formal_noasal"].total >= acc["formales"].total:
        raise SystemExit("PARO: formales no asalariados >= formales; el filtro pos_ocu "
                         "no discrimina.")

    out = {k: a.ic95() for k, a in acc.items()}
    out["_particion"] = {"residuo_emp_ppal_fuera_de_1_2": emp_ppal_otro,
                         "filas_leidas": leidas, "filas_descartadas": descartadas,
                         "pos_ocu_dentro_de_formales":
                             {k: v for k, v in sorted(pos_ocu_formales.items())}}
    return out


def numerador_l13():
    """Re-cita N, p_B y p_C de L13. NO recalcula: el encargo lo prohibe."""
    d = json.load(open(L13_JSON, encoding="utf-8"))
    ult = d["serie"][-1]
    return {
        "N": ult["n_acumulado_primeras_efirma"],
        "corte": "%d-12" % ult["ano"],
        "fuente": "data/l13-sat-efirma-v1_0.json (ADR-312), id firelenumcontri",
        "p_B": d["p_inf"], "p_C": d["p_sup"],
        "D_B_padron_total": ult["padron_total"],
        "D_C_padron_obligado": ult["padron_obligado_aprox"],
        "cota_superior_declarada": d["cota_superior_declarada"],
    }


def razon(N, est):
    """p = N/D con N constante administrativa. El IC se invierte: el limite
    inferior de p usa el limite SUPERIOR de D."""
    return {"p": N / est["total"],
            "p_ic95_inf": N / est["ic95_sup"],
            "p_ic95_sup": N / est["ic95_inf"]}


# ─────────────────────────── incompatibilidades ───────────────────────────
#
# Cada una con SIGNO sobre p_A: «+» la infla, «-» la desinfla. Congeladas aqui.
INCOMPATIBILIDADES = [
    {"clave": "personas_morales_en_el_numerador",
     "que": "N cuenta contribuyentes PF y PM; el denominador ENOE cuenta PERSONAS "
            "ocupadas. Cada PM con e.firma suma arriba sin poder sumar abajo.",
     "signo": "+ (infla p_A)",
     "cota": "acotable con PorTipoContribuyente: las PM son ~7% del padron activo; "
             "no se resta aqui porque L13 no separo N por tipo de persona."},
    {"clave": "acumulado_no_es_stock_vigente",
     "que": "N acumula primeras e.firma desde 2004-01 y no da de baja al que caduco "
            "o salio del padron; el denominador es un stock de un trimestre.",
     "signo": "+ (infla p_A)",
     "cota": "no acotada por este acto; es la cota superior que L13 ya declaro."},
    {"clave": "menores_de_15_fuera_del_denominador",
     "que": "La ENOE 15ymas no observa a la poblacion menor de 15; un menor con "
            "e.firma (rara pero posible via representante) suma arriba y no abajo.",
     "signo": "+ (infla p_A), magnitud despreciable"},
    {"clave": "no_ocupados_con_efirma",
     "que": "Desocupados, PNEA, jubilados y arrendadores pueden tener e.firma y "
            "estan FUERA de los cuatro denominadores ENOE (todos exigen clase2==1).",
     "signo": "+ (infla las cuatro p de ENOE)",
     "cota": "el denominador crece si se abre a toda la poblacion de 15 y mas; "
             "esa quinta lectura NO se mide aqui porque el encargo pide tres."},
    {"clave": "residentes_en_el_extranjero",
     "que": "Contribuyentes residentes fuera de Mexico estan en el padron del SAT y "
            "no en el marco muestral de la ENOE (viviendas en territorio nacional).",
     "signo": "+ (infla p_A)"},
    {"clave": "subdeclaracion_de_informalidad_en_registro",
     "que": "El ocupado informal (emp_ppal==1) puede aun asi tener RFC y e.firma: "
            "informalidad laboral no es ausencia de registro fiscal.",
     "signo": "- sobre la LECTURA, no sobre p: rompe la equivalencia "
              "«formal == obligado», que es por que (c) es aproximacion y no medida."},
    {"clave": "unidad_de_observacion",
     "que": "El SAT cuenta CONTRIBUYENTES (uno puede tener varias actividades); la "
            "ENOE cuenta PERSONAS por su ocupacion PRINCIPAL (emp_ppal es de la "
            "primera actividad). Un ocupado con dos empleos aporta 1 abajo.",
     "signo": "ambiguo; afecta la asignacion entre (b) y (c), no el total (a)."},
]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--censo", action="store_true",
                    help="P0: estructura, diccionario y verificacion de claves. No agrega.")
    ap.add_argument("--mide", action="store_true", help="P0+P1: denominadores y razones.")
    ap.add_argument("--json", help="ruta de salida del JSON de --mide")
    a = ap.parse_args()
    if not (a.censo or a.mide):
        ap.error("elige --censo o --mide")

    z, path, sd, sm = abre_zip()
    print("payload   %s" % path)
    print("sha256    %s  (manifiesto: %s)" % (sd, "IGUAL" if sd == sm else sm))
    print("trimestre %s  — elegido por contener el corte del numerador (2025-12)" % TRIMESTRE)

    dicc = campos_del_diccionario(z)
    print("\ncampos de la spec, segun el diccionario del propio zip:")
    for c in CAMPOS:
        d = dicc.get(c)
        print("  %-10s %-3s %-28s %s" % (c, d["tipo"], d["rango"][:28], d["desc"][:52])
              if d else "  %-10s AUSENTE DEL DICCIONARIO" % c)

    rep = verifica_claves(z)
    print("\nclaves de la spec contra el catalogo (discordancia -> PARO):")
    for r in rep:
        print("  %-9s %s  %-40s %s" % (r["campo"], r["cve"], r["catalogo"],
                                       "OK" if r["concuerda"] else "DISCORDA"))
    print("  -> las %d concuerdan; no hay PARO por catalogo." % len(rep))

    if a.censo:
        info = z.getinfo(P_DATOS)
        print("\nSDEM %s: %d bytes sin comprimir. El censo NO agrega ninguna cifra."
              % (P_DATOS.split("/")[-1], info.file_size))
        return

    est = mide(z)
    l13 = numerador_l13()
    N = l13["N"]

    lecturas = {
        "A_ocupados_totales": {
            "denominador": "ENOE ocupados totales (clase2==1, 15+)",
            "estimacion": est["ocupados"], **razon(N, est["ocupados"])},
        "A_prima_ocupados_formales": {
            "denominador": "ENOE ocupados con empleo formal (emp_ppal==2)",
            "estimacion": est["formales"], **razon(N, est["formales"])},
        "A_bis_formales_no_asalariados": {
            "denominador": "ENOE ocupados formales no asalariados (pos_ocu in {2,3})",
            "estimacion": est["formal_noasal"], **razon(N, est["formal_noasal"])},
        "B_padron_amplio_L13": {
            "denominador": "SAT padron activo Total (re-citado de L13, no recalculado)",
            "estimacion": {"total": l13["D_B_padron_total"], "ic95_inf": None,
                           "ic95_sup": None, "nota": "censo administrativo: sin IC muestral"},
            "p": l13["p_B"], "p_ic95_inf": None, "p_ic95_sup": None},
        "C_padron_obligado_L13": {
            "denominador": "SAT Total - Asalariados PF (re-citado de L13, no recalculado)",
            "estimacion": {"total": l13["D_C_padron_obligado"], "ic95_inf": None,
                           "ic95_sup": None, "nota": "censo administrativo: sin IC muestral"},
            "p": l13["p_C"], "p_ic95_inf": None, "p_ic95_sup": None},
    }

    salida = {
        "acto": "MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS",
        "regla": "tramite.gobierno_digital.coercitivo",
        "prior": {"rechaza_servicio": 0.91, "adopta": 0.09,
                  "clase": "ASIGNADO", "tier": "MEDIA-FUERTE"},
        "no_adjudica": "Este acto MIDE Y NO ADJUDICA: no evalua tramo del falsador "
                       "B-bis, no emite veredicto y no sella. La eleccion de lectura "
                       "es de mesa.",
        "escala": "numerador administrativo sobre denominador de encuesta — CAMPO del "
                  "entorno, no probabilidad individual de conducta; comparable con el "
                  "0.09 asignado SOLO en signo y orden de magnitud.",
        "trimestre_de_corte": TRIMESTRE,
        "razon_del_trimestre": "oct-dic 2025 contiene el corte 2025-12 del numerador; "
                               "2026-1T existe con COE y SDEM pero desfasa un trimestre.",
        "numerador": l13,
        "denominadores_enoe": est,
        "lecturas": lecturas,
        "incompatibilidades_de_universo": INCOMPATIBILIDADES,
        "cota": "Las cuatro p de ENOE son COTAS SUPERIORES de la adopcion vigente, "
                "porque N es acumulado de primeras e.firma y no stock vigente (L13).",
        "fuentes": [
            {"id": PAYLOAD_ID, "archivo": ARCHIVO, "sha256": sd,
             "papel": "denominadores poblacionales (SDEM, fac_tri)"},
            {"id": "firelenumcontri", "papel": "numerador, re-citado de L13",
             "via": L13_JSON},
        ],
    }

    print("\n%-42s %16s %16s %10s %s" % ("lectura", "denominador", "IC95", "p", "IC95 de p"))
    for k, v in lecturas.items():
        e = v["estimacion"]
        ic = ("[%s, %s]" % (f"{e['ic95_inf']:,.0f}", f"{e['ic95_sup']:,.0f}")
              if e.get("ic95_inf") else "sin IC (censo)")
        icp = ("[%.4f, %.4f]" % (v["p_ic95_sup"], v["p_ic95_inf"])
               if v.get("p_ic95_inf") else "sin IC (censo)")
        print("%-42s %16s %26s %8.4f  %s"
              % (k, f"{e['total']:,.0f}", ic, v["p"], icp))
    print("\nN (unico) = %s  · corte %s · COTA SUPERIOR del stock vigente"
          % (f"{N:,.0f}", l13["corte"]))
    p = est["_particion"]
    print("particion: leidas %s · descartadas %s · residuo emp_ppal fuera de {1,2} %s"
          % (f"{p['filas_leidas']:,}", f"{p['filas_descartadas']:,}",
             f"{p['residuo_emp_ppal_fuera_de_1_2']:,.0f}"))
    print("SIN fila de veredicto: este acto no adjudica.")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(salida, f, ensure_ascii=False, indent=1, sort_keys=False)
            f.write("\n")
        print("\nescrito %s" % a.json)


if __name__ == "__main__":
    main()
