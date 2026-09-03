#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA.

Mide `p` = adopcion de e.firma entre contribuyentes del padron activo del SAT,
contra el prior ASIGNADO de `milpa/tramite.yaml::tramite.gobierno_digital.coercitivo`
(`rechaza_servicio` 0.91 / `adopta` 0.09, MEDIA-FUERTE).

ESCALA DECLARADA (A-bis 3). Lo que este modulo produce es una PROPORCION
ADMINISTRATIVA AGREGADA — un CAMPO del entorno, no una probabilidad individual
de conducta. Precedente: firma p1 (mesa, 2/sep/2026, MAESTRA34-L6, propagada por
ADR-299), «tasa nacional ENDUTIH FUERTE como campo, no conducta». Comparable con
el 0.09 asignado SOLO en signo y orden de magnitud; NUNCA como «difiere en Z %».

No hay IC de diseno: es un censo administrativo, no una muestra. La incertidumbre
es de DEFINICION DE UNIVERSO y se cuantifica con dos cotas del denominador.

Uso:
    python3 tools/medidor_l13_sat_efirma.py --censo
    python3 tools/medidor_l13_sat_efirma.py --mide --json data/l13-sat-efirma-v1_0.json
"""
import argparse, hashlib, json, os, sys

RAICES_LOCAL = "data/raices.local.yaml"

# Los payloads que este acto abre, por id de data/manifiesto.yaml (ADR-310).
PAYLOADS = {
    "firelenumcontri":     "Descargas Manuales/FirEleNumcontri.xls",
    "firelenumcert":       "Descargas Manuales/FirEleNumcert.xls",
    "portipocontribuyente":"Descargas Manuales/PorTipoContribuyente.xls",
    "porentfed":           "Descargas Manuales/PorEntFed.xls",
    "decanuatipcon":       "Descargas Manuales/DecAnuaTipCon.xls",
    "ingresostributarios": "Descargas Manuales/IngresosTributarios.xls",
}

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# ══════════════════════ SPEC CONGELADA — COMMIT-1 ══════════════════════
#
# Escrita y commiteada ANTES de calcular cifra alguna. El censo A.4 de P0 abrio
# las hojas para leer ESTRUCTURA (encabezados, periodos, unidades) y las ultimas
# filas crudas de cada hoja; no calculo ningun acumulado ni ningun cociente.
#
# NUMERADOR (N). `firelenumcontri`, hoja unica, columnas «Personas Fisicas» +
#   «Personas Morales» del bloque «Contribuyentes que han obtenido el certificado
#   de e.firma (se considera el primer certificado emitido)». Es un FLUJO mensual
#   de ALTAS PRIMERAS; la clausula «primer certificado» garantiza que no hay doble
#   conteo por renovacion, asi que su SUMA ACUMULADA desde 2004-01 es el numero de
#   contribuyentes DISTINTOS que alguna vez obtuvieron e.firma.
#   NO es «e.firma vigente»: el certificado caduca (4 anos) y el acumulado no da
#   de baja al contribuyente que salio del padron. Por eso N es COTA SUPERIOR del
#   stock de vigentes, y se declara asi. `firelenumcert` (certificados emitidos,
#   CON renovaciones) NO se usa como numerador: cuenta certificados, no personas.
#
# DENOMINADOR (D), dos cotas — el .xls NO trae una columna de «obligados»:
#   D_amplio = «Total» del padron activo (`portipocontribuyente`), que INCLUYE a
#             los Asalariados (PF), quienes en general NO estan obligados a e.firma.
#             Denominador mas grande  ->  p mas chico  ->  p_inf.
#   D_obligado = «Total» - «Asalariados (PF)». Aproxima el universo obligado
#             (PF con actividad empresarial/profesional + PM + grandes
#             contribuyentes). Denominador mas chico  ->  p mas grande  ->  p_sup.
#   Los «Grandes Contribuyentes (PF)/(PM)» ya estan dentro del Total segun la
#   estructura de la hoja; NO se restan (se verifica por identidad aritmetica en
#   --mide y se reporta si no cierra).
#
# PERIODO. Ultimo ANO COMPLETO comun a las dos hojas = el maximo ano con mes
#   «Diciembre» presente en AMBAS. Corte en Diciembre de ese ano: N acumulado
#   2004-01..dic(ano), D leido en dic(ano). Serie por ano para todos los anos
#   completos comunes (>= 3 exigidos por el encargo; si son < 3 se declara).
#
# ═══════════ FALSADOR B-bis — CONGELADO (encargo, SHA ea45e01) ═══════════
#   La regla afirma `adopta` = 0.09 bajo coercion con riesgo fiscal.
#   (i)   p >= 0.50               -> CONTRARIA  (el propio falsable_si:
#                                    «adopcion masiva» rompe la regla)
#   (ii)  0.20 <= p < 0.50        -> ACOTADA    (no masiva, pero un orden de
#                                    magnitud sobre el prior)
#   (iii) p <  0.20               -> CORROBORADA-PARCIAL
#   PRECEDENCIA: si p_inf y p_sup caen en TRAMOS DISTINTOS -> AMBIGUA-POR-UNIVERSO,
#   y NO adjudica. Se evalua sobre el ultimo ano completo.
#
#   «el primer resultado que produzca este procedimiento es el que se reporta»
# ═══════════════════════════════════════════════════════════════════════

TRAMOS = [(0.50, "CONTRARIA"), (0.20, "ACOTADA"), (0.0, "CORROBORADA-PARCIAL")]


def tramo(p):
    """Tramo del falsador B-bis al que pertenece p. Congelado arriba."""
    for umbral, nombre in TRAMOS:
        if p >= umbral:
            return nombre
    raise ValueError(f"p fuera de rango: {p}")


def raiz(nombre="descargas_mx"):
    """Resuelve una raiz de data/manifiesto.yaml. PARA si no esta configurada:
    un worktree nuevo nace sin data/raices.local.yaml y un `no existe` que en
    realidad es `no configurada` es el falso negativo que A.13 persigue."""
    if not os.path.exists(RAICES_LOCAL):
        raise SystemExit(
            f"PARO: falta {RAICES_LOCAL}. La raiz '{nombre}' no esta configurada "
            f"en este worktree — esto NO es 'el payload no existe'.")
    for linea in open(RAICES_LOCAL, encoding="utf-8"):
        linea = linea.split("#")[0].strip()
        if linea.startswith(nombre + ":"):
            return linea.split(":", 1)[1].strip()
    raise SystemExit(f"PARO: {RAICES_LOCAL} no define '{nombre}'.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_manifiesto(pid):
    """El sha256 que data/manifiesto.yaml declara para ese id, o None."""
    import re
    txt = open("data/manifiesto.yaml", encoding="utf-8").read()
    for ent in re.split(r"\n(?=- id: )", txt):
        m = re.match(r"- id: (\S+)", ent)
        if m and m.group(1) == pid:
            s = re.search(r"\n  sha256: (\S+)", ent)
            return s.group(1) if s else None
    return None


def abre(pid):
    """(hoja, ruta, sha_disco, sha_manifiesto). Verifica identidad, no nombre."""
    import xlrd
    path = os.path.join(raiz(), PAYLOADS[pid])
    if not os.path.exists(path):
        raise SystemExit(f"PARO: payload ausente en disco: {path} (id {pid})")
    sh = xlrd.open_workbook(path).sheet_by_index(0)
    return sh, path, sha256(path), sha_manifiesto(pid)


def _cabecera(sh, fila):
    """Mapa {etiqueta: columna} de una fila de encabezado, saltando vacias."""
    out = {}
    for c in range(sh.ncols):
        v = str(sh.cell_value(fila, c)).strip()
        if v:
            out[v] = c
    return out


def serie_mensual(sh, fila0, col_ano, col_mes, cols):
    """{(ano, mes_idx): {etiqueta: float}} para las filas de datos.

    Guardia marginal ([[feedback_lector_nuevo_devuelve_vacio_no_error]]): PARA si
    el lector no produce ni una fila, en vez de devolver un dict vacio que aguas
    abajo se lee como un cero legitimo."""
    out = {}
    for r in range(fila0, sh.nrows):
        a = sh.cell_value(r, col_ano)
        m = str(sh.cell_value(r, col_mes)).strip()
        if not isinstance(a, float) or m not in MESES:
            continue
        vals = {}
        ok = True
        for etq, c in cols.items():
            v = sh.cell_value(r, c)
            if not isinstance(v, float):
                ok = False
                break
            vals[etq] = v
        if ok:
            out[(int(a), MESES.index(m) + 1)] = vals
    if not out:
        raise SystemExit("PARO: el lector no produjo ninguna fila (falso vacio).")
    return out


def carga_numerador():
    sh, path, shad, sham = abre("firelenumcontri")
    cab = _cabecera(sh, 5)          # fila 5: 'Personas Fisicas' | 'Personas Morales'
    faltan = [k for k in ("Personas Físicas", "Personas Morales") if k not in cab]
    if faltan:
        raise SystemExit(f"PARO: encabezado inesperado en firelenumcontri: faltan {faltan}; hay {list(cab)}")
    cols = {k: cab[k] for k in ("Personas Físicas", "Personas Morales")}
    return serie_mensual(sh, 6, 1, 2, cols), path, shad, sham


def carga_denominador():
    sh, path, shad, sham = abre("portipocontribuyente")
    cab = _cabecera(sh, 4)
    need = ("Personas Físicas", "Grandes Contribuyentes (PF)", "Asalariados (PF)",
            "Personas Morales", "Grandes Contribuyentes (PM)", "Total")
    faltan = [k for k in need if k not in cab]
    if faltan:
        raise SystemExit(f"PARO: encabezado inesperado en portipocontribuyente: faltan {faltan}; hay {list(cab)}")
    cols = {k: cab[k] for k in need}
    return serie_mensual(sh, 5, 1, 2, cols), path, shad, sham


def censo():
    """P0 — A.4 por objeto. Estructura y veredicto; no calcula ninguna tasa."""
    for pid in PAYLOADS:
        sh, path, shad, sham = abre(pid)
        print("=" * 72)
        print(f"id: {pid}")
        print(f"  archivo   : {PAYLOADS[pid]}")
        print(f"  sha256    : {shad[:16]}…  manifiesto: {(sham or 'AUSENTE')[:16]}…  "
              f"{'COINCIDE' if shad == sham else '¡DIFIERE!'}")
        print(f"  hoja      : '{sh.name}'  {sh.nrows} x {sh.ncols}")
        for r in range(min(sh.nrows, 6)):
            fila = [f"[{r},{c}] {str(sh.cell_value(r,c)).strip()[:60]!r}"
                    for c in range(sh.ncols) if str(sh.cell_value(r, c)).strip()]
            for f in fila:
                print("   ", f)
    return 0


def mide(destino):
    num, p_num, sha_num, shm_num = carga_numerador()
    den, p_den, sha_den, shm_den = carga_denominador()
    for pid, sd, sm in (("firelenumcontri", sha_num, shm_num),
                        ("portipocontribuyente", sha_den, shm_den)):
        if sd != sm:
            raise SystemExit(f"PARO: sha256 de {pid} no coincide con data/manifiesto.yaml.")

    # Anos completos comunes: diciembre presente en ambas hojas.
    anos = sorted({a for (a, m) in num if m == 12} & {a for (a, m) in den if m == 12})
    if not anos:
        raise SystemExit("PARO: ningun ano completo comun entre numerador y denominador.")

    serie = []
    for a in anos:
        # N = acumulado de altas primeras (PF+PM) desde el inicio de la hoja
        # hasta diciembre de `a`, inclusive.
        n = sum(v["Personas Físicas"] + v["Personas Morales"]
                for (aa, mm), v in num.items() if (aa, mm) <= (a, 12))
        d = den[(a, 12)]
        d_amplio = d["Total"]
        d_oblig = d["Total"] - d["Asalariados (PF)"]
        # Identidad aritmetica del Total declarada en la spec: los Grandes
        # Contribuyentes van DENTRO del Total, no aparte.
        suma_partes = d["Personas Físicas"] + d["Asalariados (PF)"] + d["Personas Morales"]
        serie.append({
            "ano": a,
            "n_acumulado_primeras_efirma": n,
            "padron_total": d_amplio,
            "padron_asalariados_pf": d["Asalariados (PF)"],
            "padron_obligado_aprox": d_oblig,
            "identidad_total_menos_partes": d_amplio - suma_partes,
            "p_inf": n / d_amplio,
            "p_sup": n / d_oblig,
        })

    ult = serie[-1]
    t_inf, t_sup = tramo(ult["p_inf"]), tramo(ult["p_sup"])
    veredicto = t_inf if t_inf == t_sup else "AMBIGUA-POR-UNIVERSO"

    out = {
        "acto": "MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA",
        "regla": "tramite.gobierno_digital.coercitivo",
        "prior": {"rechaza_servicio": 0.91, "adopta": 0.09, "clase": "ASIGNADO",
                  "tier": "MEDIA-FUERTE"},
        "escala": ("proporcion administrativa agregada — CAMPO del entorno, no "
                   "probabilidad individual de conducta (precedente: firma p1, "
                   "mesa 2/sep/2026, ADR-299). Comparable con 0.09 solo en signo "
                   "y orden de magnitud, nunca como «difiere en Z %»."),
        "sin_ic_de_diseno": ("censo administrativo: la incertidumbre es de "
                             "definicion de universo, no muestral; se cuantifica "
                             "con las dos cotas del denominador."),
        "fuentes": [
            {"id": "firelenumcontri", "archivo": PAYLOADS["firelenumcontri"],
             "sha256": sha_num, "papel": "numerador (altas primeras de e.firma, acumuladas)"},
            {"id": "portipocontribuyente", "archivo": PAYLOADS["portipocontribuyente"],
             "sha256": sha_den, "papel": "denominador (padron activo por tipo)"},
        ],
        "anos_completos_comunes": anos,
        "serie": serie,
        "ultimo_ano_completo": ult["ano"],
        "p_inf": ult["p_inf"], "p_sup": ult["p_sup"],
        "tramo_p_inf": t_inf, "tramo_p_sup": t_sup,
        "veredicto": veredicto,
        "falsador_congelado": {
            "commit_1": "spec y falsador escritos antes de calcular cifra alguna",
            "i": "p >= 0.50 -> CONTRARIA", "ii": "0.20 <= p < 0.50 -> ACOTADA",
            "iii": "p < 0.20 -> CORROBORADA-PARCIAL",
            "precedencia": "tramos distintos para p_inf y p_sup -> AMBIGUA-POR-UNIVERSO",
        },
        "cota_superior_declarada": (
            "N cuenta contribuyentes que ALGUNA VEZ obtuvieron su primer certificado "
            "de e.firma (2004-…), no vigencias: el certificado caduca y el acumulado "
            "no da de baja a quien salio del padron. N es cota SUPERIOR del stock "
            "vigente, y por tanto p_inf y p_sup son ambas cotas superiores de la "
            "adopcion VIGENTE."),
    }
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for r in serie:
        print(f"  {r['ano']}  N={r['n_acumulado_primeras_efirma']:>12,.0f}  "
              f"D_amplio={r['padron_total']:>12,.0f}  D_oblig={r['padron_obligado_aprox']:>12,.0f}  "
              f"p_inf={r['p_inf']:.4f}  p_sup={r['p_sup']:.4f}")
    print(f"\nULTIMO ANO COMPLETO: {ult['ano']}")
    print(f"  p_inf = {ult['p_inf']:.4f}  -> {t_inf}")
    print(f"  p_sup = {ult['p_sup']:.4f}  -> {t_sup}")
    print(f"  VEREDICTO: {veredicto}")
    print(f"\nescrito: {destino}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--censo", action="store_true", help="P0: A.4 por objeto, sin calcular nada")
    ap.add_argument("--mide", action="store_true", help="P1: estima p con las dos cotas")
    ap.add_argument("--json", default="data/l13-sat-efirma-v1_0.json")
    a = ap.parse_args()
    if a.censo:
        return censo()
    if a.mide:
        return mide(a.json)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
