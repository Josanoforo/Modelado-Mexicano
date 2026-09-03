#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L11 · ROBUSTECE-L9 — segundo instrumento (ENCUCI 2020) para
las piezas (b) R7.3/R7.6 y (c) R7.4 de `forense/notas/2026-09-02-MAESTRA35-L9-spec.md`.

Hermano de `tools/medidor_clientelismo_lapop.py` (a-bis) y
`tools/medidor_protesta_lapop.py` (b): importa el estimador (bootstrap de
conglomerado + control de regresión por linealización) sin tocarlos. Ningún
medidor de L9 se edita en este acto -- control de regresión trivial: L9
reproduce byte a byte porque este script no cambia una sola línea de los
suyos.

Las specs de L9 (desenlaces, dicotomizaciones, reglas de veredicto §3.1/§4.1,
precedencia CONTRARIA) se HEREDAN verbatim; la única sustitución es el
instrumento (ENCUCI 2020 en vez de LAPOP) y sus campos de diseño
(FAC_SEL/EST_DIS/UPM_DIS en vez de wt/estratopri/upm).

Pieza (a) R7.7 NO se mide con ENCUCI: no existe un ítem de oferta PERSONAL de
dádiva (sólo AP8_1_1/AP8_1_2, "¿conoce a alguien que recibió...?", que es
exposición de red, no recepción propia) ni un ítem de POR QUIÉN votó en 2018
(sólo AP7_13/AP7_13A, simpatía de partido, contemporánea a la encuesta y no al
voto de 2018). Los dos elementos que la spec §2 exige están ausentes:
EXISTE-NO-SATISFACE, declarado en el censo P0, no forzado aquí.

Latinobarometro 2024 NO trae ningún ítem de compra de voto, secreto del voto,
protesta/agravio ni transferencia condicionada (censo P0, búsqueda por
etiqueta sobre las 332 columnas de `Latinobarometro_2024_Stata_esp`):
EXISTE-NO-SATISFACE para las tres piezas. No se abre en este módulo.

Uso:
    python3 tools/medidor_l11_encuci2020.py --censo
    python3 tools/medidor_l11_encuci2020.py --mide --json data/l11-encuci2020-v1_0.json
"""
import argparse, hashlib, json, os, sys, zipfile
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbfmini  # noqa: E402
from medidor_clientelismo_lapop import _celda, _dif, REPLICAS, SEED  # noqa: E402

ZIP = "data/raw/BD_ENCUCI2020_dbf.zip"
SEC_678 = "ENCUCI_2020_SEC_6_7_8.dbf"
SEC_45 = "ENCUCI_2020_SEC_4_5.dbf"
SD = "ENCUCI_2020_SD.dbf"
PAYLOAD_ID = "encuci2020_bd_dbf"


def _extrae():
    tmp = os.environ.get("TMPDIR", "/tmp")
    z = zipfile.ZipFile(ZIP)
    for n in (SEC_678, SEC_45, SD):
        d = os.path.join(tmp, n)
        if not os.path.exists(d):
            z.extract(n, tmp)
    return (os.path.join(tmp, SEC_678), os.path.join(tmp, SEC_45),
            os.path.join(tmp, SD))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _n(v):
    """AP*/DOMINIO llegan como float-str o str. -> int|None (DOMINIO se deja str)."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def carga():
    """Une SEC_6_7_8 + SEC_4_5 + SD por ID_PER. El join se censa, no se supone:
    si `sin_par` no es 0, el lector devolvio vacio en silencio en alguna de las
    dos tablas de contenido."""
    p678, p45, psd = _extrae()
    dis = {}
    for r in dbfmini.read_dbf(psd, wanted_fields=["ID_PER", "FAC_SEL", "EST_DIS",
                                                  "UPM_DIS", "DOMINIO"]):
        dis[str(r["ID_PER"]).strip()] = r
    sec45 = {}
    for r in dbfmini.read_dbf(p45, wanted_fields=["ID_PER", "AP4_3_2"]):
        sec45[str(r["ID_PER"]).strip()] = r

    filas, sin_par = [], 0
    for r in dbfmini.read_dbf(p678, wanted_fields=["ID_PER", "AP6_10", "AP7_13",
                                                   "AP7_15", "AP7_3_5"]):
        k = str(r["ID_PER"]).strip()
        d = dis.get(k)
        s45 = sec45.get(k)
        if d is None or s45 is None:
            sin_par += 1
            continue
        try:
            w = float(str(d["FAC_SEL"]).strip())
        except (ValueError, TypeError):
            sin_par += 1
            continue
        filas.append({
            "est": str(d["EST_DIS"]).strip(), "upm": str(d["UPM_DIS"]).strip(),
            "w": w, "dominio": str(d["DOMINIO"]).strip(),
            "ap6_10": _n(r["AP6_10"]), "ap7_13": str(r["AP7_13"]).strip(),
            "ap7_15": _n(r["AP7_15"]), "ap7_3_5": _n(r["AP7_3_5"]),
            "ap4_3_2": _n(s45["AP4_3_2"]),
        })
    return filas, sin_par


def censo():
    filas, sin_par = carga()
    print(f"ENCUCI 2020 · {PAYLOAD_ID}\n  zip sha256 {sha256(ZIP)}")
    print(f"  SEC_6_7_8 x SEC_4_5 x SD por ID_PER: emparejadas {len(filas)} · "
          f"sin par {sin_par}")
    for var in ("ap6_10", "ap7_15", "ap7_3_5", "dominio", "ap4_3_2"):
        marg = Counter(f[var] for f in filas)
        print(f"    {var:10s} marginal={dict(sorted(marg.items(), key=lambda x: str(x[0])))}")
    print("  AP7_13 (simpatia de partido, sin gate previo)")
    marg13 = Counter(f["ap7_13"] for f in filas)
    print(f"    {dict(sorted(marg13.items()))}")
    print("\n  Denominador del eje (b): AP6_10 x AP7_15, sin tocar AP7_13")
    den = Counter((f["ap6_10"], f["ap7_15"]) for f in filas)
    for k in sorted(den, key=lambda x: (x[0] is None, x[1] is None, x)):
        print(f"    {k}: n={den[k]}")
    print("\n  Denominador del eje (c): DOMINIO(urbano=U/C, rural=R) x AP4_3_2, sin tocar AP7_3_5")
    denc = Counter((("urbano" if f["dominio"] in ("U", "C") else "rural"), f["ap4_3_2"])
                   for f in filas)
    for k in sorted(denc, key=str):
        print(f"    {k}: n={denc[k]}")
    return filas


# ─────────────────────── P1 · medicion (COMMIT-2) ───────────────────────
# Reglas de veredicto HEREDADAS verbatim de spec §3.1 (pieza b) y §4.1 (pieza c).
# El unico cambio es el instrumento y sus campos de diseño.

GUARDIA_FILAS = 21519
GUARDIA_SIN_PAR = 0


def _guardia(nombre, obtenido, esperado):
    if obtenido != esperado:
        raise SystemExit(f"PARO (guardia de lectura §0.5): {nombre} = {obtenido}, "
                         f"esperado {esperado}.")
    return True


def _tup(sub, y_fn):
    return [(f["est"], f["upm"], f["w"], y_fn(f)) for f in sub]


def _pieza_b(filas):
    """R7.3/R7.6 sobre ENCUCI 2020 -- hereda spec §3.1 verbatim.

    Antecedente : AP6_10 (transferencia/beneficiario de programa social,
                  ultimos 12 meses) -- el mismo antecedente que la pieza (c)
                  de L9 (AP6_10), no la dadiva de R7.7 (esa NO existe aqui).
    Moderador   : AP7_15 ("cree que su voto es secreto o se puede descubrir
                  por quien ha votado"). rama SECRETO = 1 (n_val abajo),
                  rama OBSERVABLE = 2 ("se puede descubrir"). Se excluye 9
                  (NS/NR), simetrico a countfair3 en L9.
    Desenlace   : AP7_13 == '07' (simpatiza con MORENA, el partido en el
                  gobierno desde dic-2018) -- analogo declarado de vb20 de
                  LAPOP 2023 ("votaria por el partido del presidente actual"):
                  las dos son PROSPECTIVAS/actitudinales, no el voto emitido.
                  AP7_13A (variante gateada de la misma pregunta, solo 5 725
                  casos) NO se usa: cubre menos y el censo no explica el gate.
                  Universo: AP7_13 in {01..09}, excluye blanco y 99=NS/NR.
    """
    univ = [f for f in filas
            if f["ap6_10"] in (1, 2) and f["ap7_15"] in (1, 2)
            and f["ap7_13"] not in ("", "99")]
    cobertura = len(univ) / len(filas)

    def y13(f):
        return 1 if f["ap7_13"] == "07" else 0

    ramas = {"SECRETO": (1,), "OBSERVABLE": (2,)}
    out_ramas = {}
    for rama, cods in ramas.items():
        fa = _tup([f for f in univ if f["ap6_10"] == 1 and f["ap7_15"] in cods], y13)
        fb = _tup([f for f in univ if f["ap6_10"] == 2 and f["ap7_15"] in cods], y13)
        ca = _celda(fa, f"simpatiza MORENA | transferencia=Si, {rama}")
        cb = _celda(fb, f"simpatiza MORENA | transferencia=No, {rama}")
        out_ramas[rama] = {"transferencia_si": ca, "transferencia_no": cb,
                           "delta": _dif(fa, fb, f"Δ_{rama}", ca, cb)}
    ds = out_ramas["SECRETO"]["delta"]
    do = out_ramas["OBSERVABLE"]["delta"]
    if ds.get("estado") == "ESTIMADA" and do.get("estado") == "ESTIMADA":
        delta_diferencia = {"valor": do["d"] - ds["d"],
                            "nota": "diferencia de dos diferencias; spec §3.1 no "
                                    "pre-registro IC para ella"}
    else:
        delta_diferencia = {"estado": "NO-ESTIMABLE"}

    # veredicto B-bis, precedencia heredada verbatim de spec §3.1
    def excluye_arriba(d):
        return d.get("estado") == "ESTIMADA" and d["ic95"][0] > 0
    def excluye_abajo(d):
        return d.get("estado") == "ESTIMADA" and d["ic95"][1] < 0
    def contiene(d):
        return d.get("estado") != "ESTIMADA" or (d["ic95"][0] <= 0 <= d["ic95"][1])

    if ds.get("estado") != "ESTIMADA" or do.get("estado") != "ESTIMADA":
        veredicto = "NO-DISCRIMINA"
        motivo = "alguna celda cayo bajo la guardia de numerador"
    elif excluye_arriba(ds) and excluye_arriba(do):
        veredicto = "CONTRARIA"
        motivo = ("las dos ramas dan Δ>0 limpio: la separacion que el par afirma "
                  "(agencia se conserva bajo secreto) no aparece")
    elif contiene(ds) and excluye_arriba(do):
        veredicto = "CORROBORADA"
        motivo = "Δ_SECRETO contiene 0 y Δ_OBSERVABLE excluye 0 por arriba"
    elif excluye_abajo(do):
        veredicto = "CONTRARIA"
        motivo = "Δ_OBSERVABLE excluye 0 por abajo"
    else:
        veredicto = "NO-DISCRIMINA"
        motivo = "los dos IC95 contienen 0"

    return {"pieza": "b", "reglas": ["R7.3", "R7.6"],
           "id_modelo": ["civico.voto.agencia_con_secreto",
                         "civico.voto.clientelar_si_observable"],
           "fuente": "ENCUCI 2020", "spec_heredada": "§3.1 (L9)",
           "n_total": len(filas), "n_universo": len(univ), "cobertura": cobertura,
           "universo_restringido": cobertura < 0.90,
           "ramas": out_ramas, "delta_diferencia": delta_diferencia,
           "veredicto_Bbis": veredicto, "motivo_veredicto": motivo}


def _pieza_c(filas):
    """R7.4 sobre ENCUCI 2020 -- hereda spec §4.1 verbatim, con dos
    sustituciones declaradas frente a LAPOP 2019:

    Agravio  : AP4_3_2 ("en su colonia/localidad han tenido problemas de
               pandillerismo, robos o delincuencia") -- percepcion de
               inseguridad EN EL ENTORNO, no victimizacion PERSONAL (vic1ext
               de LAPOP). Sustitucion declarada: es lo unico en el corpus que
               se acerca a "agravio" y no exige re-extraccion.
    Entorno  : DOMINIO (U=Urbano, C=Complemento urbano, R=Rural) -- urbano =
               U+C, rural = R. No es literalmente "ur" de LAPOP pero es la
               misma particion urbano/rural que el diseño muestral usa.
    Desenlace: AP7_3_5 ("alguna vez en su vida ha participado en una
               protesta") -- NO se usa AP7_4_5 (ultimos 12 meses): esta
               gateada DENTRO de AP7_3_5==1 (n=1748 de 21519, 8.1%), asi que
               no es un desenlace de poblacion. AP7_3_5 es de por vida, no de
               2019/12-meses como prot3 de LAPOP: la ventana temporal difiere,
               declarado.
    """
    univ = [f for f in filas if f["ap7_3_5"] in (1, 2) and f["ap4_3_2"] in (1, 2)]
    cobertura = len(univ) / len(filas)

    def y(f):
        return 1 if f["ap7_3_5"] == 1 else 0

    nom = {("urbano", 1): "urbano-agravio", ("urbano", 2): "urbano-sin-agravio",
          ("rural", 1): "rural-agravio", ("rural", 2): "rural-sin-agravio"}
    celdas, filas_por_celda = {}, {}
    for f in univ:
        f["_dom"] = "urbano" if f["dominio"] in ("U", "C") else "rural"
    for (dom, agr), lab in nom.items():
        sub = [f for f in univ if f["_dom"] == dom and f["ap4_3_2"] == agr]
        filas_por_celda[lab] = _tup(sub, y)
        celdas[lab] = _celda(filas_por_celda[lab], lab)

    contrastes = {
        "C1_entorno_con_agravio": _dif(filas_por_celda["urbano-agravio"],
                                       filas_por_celda["rural-agravio"],
                                       "C1 = urbano-agravio - rural-agravio",
                                       celdas["urbano-agravio"], celdas["rural-agravio"]),
        "C2_agravio_en_urbano": _dif(filas_por_celda["urbano-agravio"],
                                     filas_por_celda["urbano-sin-agravio"],
                                     "C2 = urbano-agravio - urbano-sin-agravio",
                                     celdas["urbano-agravio"], celdas["urbano-sin-agravio"]),
    }

    c1, c2 = contrastes["C1_entorno_con_agravio"], contrastes["C2_agravio_en_urbano"]
    def limpio_pos(c):
        return c.get("estado") == "ESTIMADA" and c["ic95"][0] > 0
    def limpio_neg(c):
        return c.get("estado") == "ESTIMADA" and c["ic95"][1] < 0
    def no_estimable(c):
        return c.get("estado") != "ESTIMADA"

    if no_estimable(c1) and no_estimable(c2):
        veredicto = "NO-ESTIMABLE"
        motivo = "las dos celdas de agravio cayeron bajo la guardia"
    elif no_estimable(c1):
        veredicto = "CORROBORADA" if limpio_pos(c2) else ("CONTRARIA" if limpio_neg(c2) else "NO-DISCRIMINA")
        motivo = "C1 no estimable; veredicto sale de C2 solo (spec §4.1); el contraste de entorno NO se midio"
    elif no_estimable(c2):
        veredicto = "CORROBORADA" if limpio_pos(c1) else ("CONTRARIA" if limpio_neg(c1) else "NO-DISCRIMINA")
        motivo = "C2 no estimable; veredicto sale de C1 solo"
    elif limpio_pos(c1) and limpio_pos(c2):
        veredicto = "CORROBORADA"
        motivo = "los dos contrastes limpios en el signo esperado"
    elif (limpio_pos(c1) and limpio_neg(c2)) or (limpio_neg(c1) and limpio_pos(c2)):
        veredicto = "CONTRARIA"
        motivo = "C1 y C2 discrepan en signo, ambos limpios: precedencia CONTRARIA"
    elif limpio_neg(c1) or limpio_neg(c2):
        veredicto = "CONTRARIA"
        motivo = "algun contraste limpio en signo opuesto al esperado"
    elif (limpio_pos(c1) and not limpio_pos(c2)) or (limpio_pos(c2) and not limpio_pos(c1)):
        veredicto = "CORROBORADA-PARCIAL"
        motivo = ("un contraste limpio en el signo esperado, el otro no discrimina -- "
                  "a diferencia de L9 (donde C1 cayo por guardia de numerador), aqui "
                  "los dos son ESTIMABLES: uno discrimina, el otro no")
    else:
        veredicto = "NO-DISCRIMINA"
        motivo = "IC95 traslapados en los dos contrastes"

    return {"pieza": "c", "reglas": ["R7.4"],
           "id_modelo": ["civico.protesta.agravio_urbano"],
           "fuente": "ENCUCI 2020", "spec_heredada": "§4.1 (L9)",
           "n_total": len(filas), "n_universo": len(univ), "cobertura": cobertura,
           "universo_restringido": cobertura < 0.90,
           "eje_principal": celdas, "contrastes": contrastes,
           "veredicto_Bbis": veredicto, "motivo_veredicto": motivo,
           "no_dice_nada_sobre": "R7.5 ni el veredicto D de ADR-158 (evento, no persona)",
           "sustitucion_declarada": {
               "agravio": "AP4_3_2 (percepcion de inseguridad en la colonia), no "
                          "victimizacion personal (vic1ext de LAPOP no existe en ENCUCI)",
               "desenlace": "AP7_3_5 (alguna vez, de por vida), no AP7_4_5 (ultimos 12 "
                            "meses: gateada dentro de AP7_3_5==1, n=1748/21519=8.1%, "
                            "no sirve como desenlace de poblacion)"}}


def mide(ruta_json=None):
    filas, sin_par = carga()
    _guardia("ENCUCI 2020 filas emparejadas (SEC_6_7_8 x SEC_4_5 x SD)",
             len(filas), GUARDIA_FILAS)
    _guardia("ENCUCI 2020 sin par", sin_par, GUARDIA_SIN_PAR)
    print("guardias de lectura §0.5 (heredadas + join de 3 tablas): OK")

    pb = _pieza_b(filas)
    pc = _pieza_c(filas)

    out = {"acto": "MAESTRA35-L11 · ROBUSTECE-L9",
          "spec": "forense/notas/2026-09-02-MAESTRA35-L9-spec.md (heredada verbatim)",
          "instrumento": "ENCUCI 2020",
          "payload": {"id": PAYLOAD_ID, "sha256_zip": sha256(ZIP)},
          "estimador": f"proporcion ponderada (FAC_SEL); IC95 bootstrap de conglomerado, "
                       f"{REPLICAS} replicas, seed {SEED}, UPM_DIS dentro de EST_DIS "
                       f"(identico a medidor_clientelismo_lapop.prop_bootstrap)",
          "piezas": [pb, pc]}
    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)

    def f(c):
        if c.get("estado") != "ESTIMADA":
            return f"NO-ESTIMABLE ({c.get('motivo')})"
        if "p" in c:
            return f"p={c['p']:.6f} IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}] n={c['n']} num={c['numerador']}"
        return (f"d={c['d']:+.6f} IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}] "
                f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")

    print(f"\n{'='*74}\nPIEZA b · R7.3/R7.6 · ENCUCI 2020 (cobertura {pb['cobertura']:.4%})")
    for rama in ("SECRETO", "OBSERVABLE"):
        print(f"  {rama}")
        for k in ("transferencia_si", "transferencia_no"):
            print(f"    {k:20s} {f(pb['ramas'][rama][k])}")
        print(f"    {'Δ':20s} {f(pb['ramas'][rama]['delta'])}")
    print(f"  veredicto_Bbis = {pb['veredicto_Bbis']} ({pb['motivo_veredicto']})")

    print(f"\n{'='*74}\nPIEZA c · R7.4 · ENCUCI 2020 (cobertura {pc['cobertura']:.4%})")
    for lab, c in pc["eje_principal"].items():
        print(f"  {lab:20s} {f(c)}")
    for k, d in pc["contrastes"].items():
        print(f"  {k:26s} {f(d)}")
    print(f"  veredicto_Bbis = {pc['veredicto_Bbis']} ({pc['motivo_veredicto']})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        censo()
        return
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
