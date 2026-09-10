"""`CALC-ENCUCI-0001` — mordida (solicitud y entrega) y protesta por entorno ×
agravio, ENCUCI 2020.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-ENCUCI-1`, ANTES DE LEER
UN SOLO REGISTRO DE UN `.dbf`. Spec sellada que lo gobierna:
`forense/prereg-caja/ENCUCI-MORDIDA-PROTESTA-spec-v1_0.md`
(`prereg-caja-ENCUCI-MORDIDA-PROTESTA`, sha `33add378…`).

Lo único abierto al escribir este archivo: el manifiesto, el descriptor
`FD_ENCUCI2020.pdf`, la lista de miembros del ZIP y la CABECERA de cada `.dbf`
(los 32 bytes del encabezado y los descriptores de campo de 32 bytes: nombre,
tipo, ancho y decimales — metadato del archivo, no registros), los inventarios
de reactivos, `milpa/tramite.yaml` y `data/corrida0/demanda-*.tsv`.

Releva la demanda `CORR-0003` (`RES-0005`, `RES-0006`, `RES-0061`, `RES-0062`).
NO toca `milpa/tramite.yaml` ni ningún sello previo, y NO puentea nada a
ENCIG 2025.
"""
from __future__ import annotations

import io
import struct
import zipfile

import numpy as np

# ── constantes de la spec congelada ───────────────────────────────────────

ZIP_ID = "encuci2020_bd_dbf"
T45 = "ENCUCI_2020_SEC_4_5.dbf"
T678 = "ENCUCI_2020_SEC_6_7_8.dbf"

INCISOS_CONTACTO = [f"AP5_16_{i}" for i in range(1, 11)]
COLS_45 = (["ID_PER", "UPM", "VIV_SEL", "R_SEL"] + INCISOS_CONTACTO +
           ["AP5_17", "AP5_18", "AP4_3_2", "FAC_SEL", "EST_DIS", "UPM_DIS",
            "DOMINIO"])
COLS_678 = ["ID_PER", "UPM", "VIV_SEL", "R_SEL", "AP7_3_5", "DOMINIO",
            "FAC_SEL", "EST_DIS", "UPM_DIS"]

SEP = "␟"          # separador de llave compuesta: no aparece en el dato


# ── lectura de DBF (dBase III/IV) desde el ZIP ────────────────────────────

def _campos(buf: bytes):
    """Descriptores de campo de 32 bytes: (nombre, tipo, ancho, decimales).

    Se leen del encabezado, que es METADATO del archivo — es lo mismo que ya
    estaba abierto al congelar la spec."""
    nrec = struct.unpack("<I", buf[4:8])[0]
    hsize = struct.unpack("<H", buf[8:10])[0]
    rsize = struct.unpack("<H", buf[10:12])[0]
    campos, pos = [], 32
    while pos + 32 <= hsize:
        d = buf[pos:pos + 32]
        if d[0:1] == b"\x0d":
            break
        nombre = d[0:11].split(b"\x00")[0].decode("latin-1").strip()
        campos.append((nombre, d[11:12].decode("latin-1"), d[16], d[17]))
        pos += 32
    return nrec, hsize, rsize, campos


def _lee_dbf(buf: bytes, columnas):
    """(filas, faltantes). `filas` = lista de dicts con SOLO las columnas
    pedidas, texto crudo `strip()`eado, en el ORDEN DEL ARCHIVO.

    Los registros marcados como borrados (`*` en el byte 0) se saltan."""
    nrec, hsize, rsize, campos = _campos(buf)
    nombres = [c[0] for c in campos]
    faltantes = [c for c in columnas if c not in nombres]
    if faltantes:
        return [], faltantes
    # desplazamiento de cada campo dentro del registro (el byte 0 es la marca)
    off, tramos = 1, {}
    for nombre, _tipo, ancho, _dec in campos:
        if nombre in columnas:
            tramos[nombre] = (off, off + ancho)
        off += ancho
    filas = []
    for i in range(nrec):
        ini = hsize + i * rsize
        rec = buf[ini:ini + rsize]
        if len(rec) < rsize:
            break
        if rec[0:1] == b"\x2a":
            continue
        filas.append({c: rec[a:b].decode("latin-1").strip()
                      for c, (a, b) in tramos.items()})
    return filas, []


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _cod(s):
    """Código -> entero, o `None`.

    Normaliza las DOS formas en que este DBF guarda un código de un dígito:
    `'1'` (campos `C`) y `'1.000000000000000'` (campos `N` 19,15). Devuelve
    `None` para vacío, `'b'`, no numérico o valor con parte fraccionaria — que
    NO se imputan a ningún código."""
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")):
        return None
    e = int(f)
    return e if float(e) == f else None


def _flotante(s):
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _perfil(valores):
    """Perfil de una llave OPACA: longitudes con su conteo y si algún valor
    trae espacio en los bordes. Se emite como RESULT de texto pre-declarado —
    la lección de las llaves de diseño que el descriptor describe mal."""
    if not valores:
        return "SIN-VALORES"
    largos = {}
    bordes = 0
    for v in valores:
        largos[len(v.strip())] = largos.get(len(v.strip()), 0) + 1
        if v != v.strip():
            bordes += 1
    partes = ",".join(f"len{k}={largos[k]}" for k in sorted(largos))
    return f"{partes};con_espacio_en_bordes={bordes}"


def _unica(claves):
    return "SI" if len(set(claves)) == len(claves) else "NO"


def _p(desenlace, peso):
    sw = float(np.sum(peso))
    if sw <= 0:
        return None
    return float(np.sum(peso * desenlace) / sw)


def _bootstrap(celdas, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, conservando el número
    de UPM por estrato. `celdas` = {nombre: (mascara, desenlace, peso)} sobre
    el MISMO universo.

    Las réplicas se sortean UNA vez por estrato y se aplican a TODAS las
    celdas: por eso las diferencias entre celdas se pueden leer réplica a
    réplica (y no como resta de dos bootstraps independientes).

    Un estrato con UNA sola UPM se re-muestrea a sí mismo: aporta varianza
    cero, no se colapsa y no se descarta. Devuelve
    `(ps_por_celda, n_estratos, n_upm, n_estratos_upm_unica)`."""
    n = len(estrato)
    if n == 0:
        return {}, 0, 0, 0
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    n_upm = len(upm_unicas)
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    estratos = np.unique(estr_de_upm)

    agr = {}
    for nombre, (mask, d, w) in celdas.items():
        sw = np.bincount(inverso[mask], weights=w[mask], minlength=n_upm)
        swd = np.bincount(inverso[mask], weights=(w * d)[mask], minlength=n_upm)
        agr[nombre] = (sw, swd)

    rng = np.random.Generator(np.random.PCG64(semilla))
    acc = {k: [np.zeros(replicas), np.zeros(replicas)] for k in celdas}
    n_una = 0
    for e in estratos:                       # orden fijo: np.unique ordena
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_una += 1
            for nombre, (sw, swd) in agr.items():
                acc[nombre][0] += sw[pos[0]]
                acc[nombre][1] += swd[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        for nombre, (sw, swd) in agr.items():
            acc[nombre][0] += sw[pos][elegidas].sum(axis=1)
            acc[nombre][1] += swd[pos][elegidas].sum(axis=1)

    ps = {}
    for nombre, (a_sw, a_swd) in acc.items():
        with np.errstate(divide="ignore", invalid="ignore"):
            serie = np.where(a_sw > 0, a_swd / np.where(a_sw > 0, a_sw, 1.0),
                             np.nan)
        ps[nombre] = serie
    return ps, len(estratos), n_upm, n_una


def _pct(serie):
    if serie is None:
        return None, None
    v = serie[~np.isnan(serie)]
    if v.size == 0:
        return None, None
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


# ── medidor ───────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = float(par["umbral_replica_gen1"])
    grano = int(par["grano_milpa_decimales"])
    gen1 = par["valores_gen1_referencia"]
    n_gen1 = par["n_gen1_referencia"]
    cod = par["codificacion"]
    URB = set(cod["B_dominio_urbano"])
    RUR = set(cod["B_dominio_rural"])
    URB_ALT = set(cod["B_dominio_urbano_alt"])
    RUR_ALT = set(cod["B_dominio_rural_alt"])
    DOM_OK = set(cod["B_dominio_declarado"])
    A_DOM = set(cod["A_dominio_declarado"])

    P = "RESULT-ENCUCI-"
    out = {P + s: None for s in par["sufijos_result"]}
    # Un `entero` declarado NUNCA puede salir null: arranca en 0 y toda rama
    # de salida lo deja escrito. Un `texto` declarado arranca NO-ESTIMABLE.
    for s in par["sufijos_result"]:
        entero = (s.startswith(("G-N-", "A-N-", "B-N-")) or
                  s in ("A-DELTA-N-VS-GEN1", "B-DELTA-N-VS-GEN1"))
        texto = ("VEREDICTO" in s or "REPRODUCE" in s or "METODO-IC" in s or
                 s.startswith(("G-LLAVE", "G-PERFIL")) or
                 ("ADOPCION-P3" in s and not s.endswith("DELTA")))
        if entero:
            out[P + s] = 0
        elif texto:
            out[P + s] = "NO-ESTIMABLE"
    out[P + "B-VEREDICTO-CONTRASTES"] = "ASOCIACION-NO-CAUSAL"
    out[P + "A-ADOPCION-P3-COMPLEMENTO"] = "COMPLEMENTO-CON-DENOMINADOR-RECORTADO"

    def para(v_a, v_b=None):
        out[P + "A-VEREDICTO"] = v_a
        out[P + "B-VEREDICTO"] = v_b if v_b is not None else v_a
        for k in ("A-ADOPCION-P3", "B-ADOPCION-P3-URB", "B-ADOPCION-P3-RUR"):
            out[P + k] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G-1 · miembros del ZIP ────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    presentes = set(zf.namelist())
    faltan_m = [m for m in par["miembros_zip_declarados"] if m not in presentes]
    if faltan_m:
        return para("NO-ESTIMABLE-MIEMBRO-AUSENTE:" + ",".join(faltan_m))

    f45, faltan45 = _lee_dbf(zf.read(T45), COLS_45)
    f678, faltan678 = _lee_dbf(zf.read(T678), COLS_678)
    out[P + "G-N-FILAS-SEC45"] = len(f45)
    out[P + "G-N-FILAS-SEC678"] = len(f678)
    out[P + "B-N-FILAS-SEC678"] = len(f678)
    if faltan45 or faltan678:
        return para("NO-ESTIMABLE-COLUMNA-AUSENTE:" +
                    ",".join(faltan45 + faltan678))

    # ── G-3 · la trampa de tipo, MEDIDA (AP5_16_1 es N 19,15) ─────────────
    n_cadena = sum(1 for f in f45 if f["AP5_16_1"] == "1")
    n_numero = sum(1 for f in f45 if _cod(f["AP5_16_1"]) == 1)
    out[P + "G-N-AP5-16-1-CADENA-UNO"] = n_cadena
    out[P + "G-N-AP5-16-1-NUMERICO-UNO"] = n_numero
    if n_cadena and n_numero:
        out[P + "G-VEREDICTO-TIPO-AP5-16"] = "CADENA-Y-NUMERO-COINCIDEN" \
            if n_cadena == n_numero else "SOLO-NUMERO-ACIERTA"
    elif n_numero:
        out[P + "G-VEREDICTO-TIPO-AP5-16"] = "SOLO-NUMERO-ACIERTA"
    elif n_cadena:
        out[P + "G-VEREDICTO-TIPO-AP5-16"] = "SOLO-CADENA-ACIERTA"
    else:
        out[P + "G-VEREDICTO-TIPO-AP5-16"] = "NINGUNO-ACIERTA"

    # ── G-4 · llaves: se miden las DOS, no se adopta ninguna por autoridad ─
    id45 = [f["ID_PER"] for f in f45]
    id678 = [f["ID_PER"] for f in f678]
    ter45 = [f"{f['UPM']}{SEP}{f['VIV_SEL']}{SEP}{f['R_SEL']}" for f in f45]
    ter678 = [f"{f['UPM']}{SEP}{f['VIV_SEL']}{SEP}{f['R_SEL']}" for f in f678]
    out[P + "G-LLAVE-SEC45-IDPER-UNICA"] = _unica(id45)
    out[P + "G-LLAVE-SEC678-IDPER-UNICA"] = _unica(id678)
    out[P + "G-LLAVE-SEC45-TERNA-UNICA"] = _unica(ter45)
    out[P + "G-LLAVE-SEC678-TERNA-UNICA"] = _unica(ter678)
    idper_ok = (out[P + "G-LLAVE-SEC45-IDPER-UNICA"] == "SI" and
                out[P + "G-LLAVE-SEC678-IDPER-UNICA"] == "SI")
    terna_ok = (out[P + "G-LLAVE-SEC45-TERNA-UNICA"] == "SI" and
                out[P + "G-LLAVE-SEC678-TERNA-UNICA"] == "SI")
    if not idper_ok and not terna_ok:
        out[P + "G-VEREDICTO-ESTRUCTURA"] = "LLAVE-NO-UNICA"
    elif idper_ok and terna_ok:
        out[P + "G-VEREDICTO-ESTRUCTURA"] = "LLAVE-DECLARADA-Y-ID-PER-COINCIDEN"
    else:
        out[P + "G-VEREDICTO-ESTRUCTURA"] = "DESCRIPTOR-DISCORDA-CON-EL-ARCHIVO"

    # ── G-7/G-8 · diseño y perfil de las llaves opacas ────────────────────
    est45 = [f["EST_DIS"] for f in f45]
    upm45 = [f["UPM_DIS"] for f in f45]
    out[P + "G-PERFIL-EST-DIS"] = _perfil(est45)
    out[P + "G-PERFIL-UPM-DIS"] = _perfil(upm45)
    out[P + "G-N-EST-DIS-DISTINTOS"] = len({e.strip() for e in est45 if e.strip()})
    out[P + "G-N-UPM-DIS-DISTINTOS"] = len(
        {f"{e.strip()}{SEP}{u.strip()}" for e, u in zip(est45, upm45)
         if e.strip() and u.strip()})
    inv45 = sum(1 for f in f45
                if (_flotante(f["FAC_SEL"]) or 0) <= 0)
    inv678 = sum(1 for f in f678
                 if (_flotante(f["FAC_SEL"]) or 0) <= 0)
    out[P + "G-N-FAC-SEL-INVALIDO-SEC45"] = inv45
    out[P + "G-N-FAC-SEL-INVALIDO-SEC678"] = inv678
    con_dis = sum(1 for f in f45 if f["EST_DIS"].strip() and f["UPM_DIS"].strip())
    if con_dis == len(f45) and len(f45):
        out[P + "G-VEREDICTO-DISENO"] = "DISENO-IDENTIFICABLE"
    elif con_dis:
        out[P + "G-VEREDICTO-DISENO"] = "DISENO-INCOMPLETO"
    else:
        out[P + "G-VEREDICTO-DISENO"] = "DISENO-AUSENTE"

    # ══ FAMILIA A · mordida ═══════════════════════════════════════════════
    n_sin_pond = n_contacto = n_sin_contacto = 0
    n_nsnr17 = n_nsnr18 = n_bl17 = n_bl18 = n_fuera = 0
    n_sin_dis_a = 0
    u_a, u_pob, sin_dato = [], [], []
    for f in f45:
        w = _flotante(f["FAC_SEL"])
        if w is None or w <= 0:
            n_sin_pond += 1
            continue
        c17, c18 = _cod(f["AP5_17"]), _cod(f["AP5_18"])
        contacto = any(_cod(f[k]) == 1 for k in INCISOS_CONTACTO)
        e = f["EST_DIS"].strip()
        u = f["UPM_DIS"].strip()
        base = {"w": w, "e": e, "u": u}
        if not contacto:
            # Sin contacto no hay ocasion posible: 5.17 pregunta «DE ESOS
            # contactos…». El 0 es la logica del propio instrumento (por eso
            # 5.17/5.18 declaran codigo `b`), no una imputacion.
            n_sin_contacto += 1
            u_pob.append(dict(base, d=0.0))
            continue
        n_contacto += 1
        malo = False
        for c, es17 in ((c17, True), (c18, False)):
            if c == 9:
                if es17:
                    n_nsnr17 += 1
                else:
                    n_nsnr18 += 1
                malo = True
            elif c is None:
                if es17:
                    n_bl17 += 1
                else:
                    n_bl18 += 1
                malo = True
            elif c not in A_DOM:
                n_fuera += 1
                malo = True
        if malo:
            # CERO NUNCA SUSTITUYE FALTA DE DATO: una fila con contacto y con
            # 9/blanco NO entra a U_A_POB como 0 -- sale, y su peso se reporta
            # en A-P-RESIDUO-POBLACION.
            sin_dato.append(dict(base))
            continue
        if not e or not u:
            n_sin_dis_a += 1
        sol = 1.0 if c17 == 1 else 0.0
        ent = 1.0 if c18 == 1 else 0.0
        cual = 1.0 if (c17 == 1 or c18 == 1) else 0.0
        amb = 1.0 if (c17 == 1 and c18 == 1) else 0.0
        u_a.append(dict(base, sol=sol, ent=ent, cual=cual, amb=amb,
                        ssin=1.0 if (c17 == 1 and c18 == 2) else 0.0,
                        comp=1.0 if (c17 == 2 and c18 == 2) else 0.0))
        u_pob.append(dict(base, d=cual))

    out[P + "A-N-SIN-PONDERADOR"] = n_sin_pond
    out[P + "A-N-FILAS"] = len(f45) - n_sin_pond
    out[P + "A-N-CONTACTO"] = n_contacto
    out[P + "A-N-SIN-CONTACTO"] = n_sin_contacto
    out[P + "A-N-NSNR-17"] = n_nsnr17
    out[P + "A-N-NSNR-18"] = n_nsnr18
    out[P + "A-N-BLANCO-17"] = n_bl17
    out[P + "A-N-BLANCO-18"] = n_bl18
    out[P + "A-N-FUERA-DE-DOMINIO"] = n_fuera
    out[P + "A-N-SIN-DISENO"] = n_sin_dis_a
    out[P + "A-N-U"] = len(u_a)
    out[P + "A-N-U-POB"] = len(u_pob)
    out[P + "A-DELTA-N-VS-GEN1"] = len(u_a) - int(n_gen1["U_A"])

    if not u_a:
        para("NO-ESTIMABLE-UNIVERSO-VACIO")
    else:
        w = np.array([r["w"] for r in u_a], dtype=float)
        e = np.array([r["e"] for r in u_a])
        m = np.array([r["u"] for r in u_a])
        masa = float(np.sum(w))
        out[P + "A-MASA-FAC-SEL-U"] = _num(masa)
        if masa <= 0:
            para("NO-ESTIMABLE-COLUMNA-VACIA:FAC_SEL")
        else:
            d = {k: np.array([r[k] for r in u_a], dtype=float)
                 for k in ("sol", "ent", "cual", "amb", "ssin", "comp")}
            p_sol = _p(d["sol"], w)
            p_ent = _p(d["ent"], w)
            p_cual = _p(d["cual"], w)
            out[P + "A-P-SOLICITUD"] = _num(p_sol)
            out[P + "A-P-ENTREGA"] = _num(p_ent)
            out[P + "A-P-CUALQUIERA"] = _num(p_cual)
            out[P + "A-P-AMBAS"] = _num(_p(d["amb"], w))
            out[P + "A-P-SOLICITUD-SIN-ENTREGA"] = _num(_p(d["ssin"], w))
            p_comp = _p(d["comp"], w)
            out[P + "A-P-COMPLEMENTO-CUALQUIERA"] = _num(p_comp)
            out[P + "A-SUMA-CUALQUIERA"] = _num(
                None if (p_cual is None or p_comp is None) else p_cual + p_comp)

            # IC de las tres celdas, mismo bootstrap
            todo = np.ones(len(u_a), dtype=bool)
            if n_sin_dis_a == len(u_a):
                out[P + "A-METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
            else:
                ps, n_est, n_upm, n_una = _bootstrap(
                    {"sol": (todo, d["sol"], w),
                     "ent": (todo, d["ent"], w),
                     "cual": (todo, d["cual"], w)},
                    e, m, replicas, semilla)
                for k, suf in (("sol", "SOLICITUD"), ("ent", "ENTREGA"),
                               ("cual", "CUALQUIERA")):
                    lo, hi = _pct(ps.get(k))
                    out[P + f"A-IC-LO-{suf}"] = _num(lo)
                    out[P + f"A-IC-HI-{suf}"] = _num(hi)
                out[P + "A-N-ESTRATOS"] = int(n_est)
                out[P + "A-N-UPM"] = int(n_upm)
                out[P + "A-N-ESTRATOS-UPM-UNICA"] = int(n_una)
                out[P + "A-METODO-IC"] = ("IC-CON-ESTRATOS-DE-UPM-UNICA"
                                          if n_una > 0
                                          else "IC-BOOTSTRAP-UPM-EN-ESTRATO")

            # segundo denominador: la poblacion 15+ completa (sin contacto
            # = 0 por la logica del instrumento), EXCLUYENDO lo que sale por
            # falta de dato -- cuyo peso se reporta aparte.
            w_pob = np.array([r["w"] for r in u_pob], dtype=float)
            d_pob = np.array([r["d"] for r in u_pob], dtype=float)
            out[P + "A-P-CUALQUIERA-POBLACION"] = _num(_p(d_pob, w_pob))
            masa_sd = float(np.sum([r["w"] for r in sin_dato])) if sin_dato else 0.0
            masa_todo = float(np.sum(w_pob)) + masa_sd
            out[P + "A-P-RESIDUO-POBLACION"] = _num(
                (masa_sd / masa_todo) if masa_todo > 0 else None)

            # veredicto semántico (§4.2 de la sellada)
            if p_sol is None or p_ent is None or p_cual is None:
                out[P + "A-VEREDICTO-SEMANTICA"] = "NO-ESTIMABLE"
            elif abs(p_sol - p_ent) <= 1.0e-9:
                out[P + "A-VEREDICTO-SEMANTICA"] = "SOLICITUD-Y-ENTREGA-COINCIDEN"
            elif p_cual > p_sol and p_cual > p_ent:
                out[P + "A-VEREDICTO-SEMANTICA"] = "LA-UNION-EXCEDE-A-CADA-PARTE"
            elif p_ent > p_sol:
                out[P + "A-VEREDICTO-SEMANTICA"] = "ENTREGA-DOMINA"
            else:
                out[P + "A-VEREDICTO-SEMANTICA"] = "SOLICITUD-DOMINA"

            suma = out[P + "A-SUMA-CUALQUIERA"]
            residuo = (n_sin_contacto + n_nsnr17 + n_nsnr18 + n_bl17 + n_bl18
                       + n_fuera)
            if suma is None or abs(suma - 1.0) > 1.0e-9:
                out[P + "A-VEREDICTO-EXHAUSTIVIDAD"] = "NO-EXHAUSTIVAS"
            elif residuo > 0:
                out[P + "A-VEREDICTO-EXHAUSTIVIDAD"] = \
                    "EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U-A"
            else:
                out[P + "A-VEREDICTO-EXHAUSTIVIDAD"] = \
                    "EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO"

            # control positivo del PUNTO y adopción
            g5 = float(gen1["RES-0005"])
            g6 = float(gen1["RES-0006"])
            dl = p_cual - g5
            out[P + "A-DELTA-VS-GEN1"] = _num(dl)
            out[P + "A-REPRODUCE-GEN1"] = ("REPRODUCE" if abs(dl) <= tol
                                           else "NO-REPRODUCE")
            dlc = None if p_comp is None else p_comp - g6
            out[P + "A-DELTA-COMP-VS-GEN1"] = _num(dlc)
            out[P + "A-REPRODUCE-COMP-GEN1"] = (
                "NO-COMPARABLE" if dlc is None else
                ("REPRODUCE" if abs(dlc) <= tol else "NO-REPRODUCE"))
            dg = round(p_cual, grano) - g5
            out[P + "A-ADOPCION-P3-DELTA"] = _num(dg)
            if abs(dl) > tol:
                out[P + "A-ADOPCION-P3"] = "NO-ADOPTABLE-POR-DISCREPANCIA"
            elif abs(dg) > 0:
                out[P + "A-ADOPCION-P3"] = "NO-ADOPTABLE-POR-GRANO"
            else:
                out[P + "A-ADOPCION-P3"] = "ADOPTABLE-POR-REPLICA"
            out[P + "A-VEREDICTO"] = "TASA-REPORTADA"

    # ══ FAMILIA B · protesta ══════════════════════════════════════════════
    if not idper_ok:
        out[P + "B-VEREDICTO"] = "NO-ESTIMABLE-LLAVE-NO-UNICA"
        for k in ("B-ADOPCION-P3-URB", "B-ADOPCION-P3-RUR"):
            out[P + k] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    agr_de = {f["ID_PER"]: f["AP4_3_2"] for f in f45}
    fac_de = {f["ID_PER"]: f["FAC_SEL"] for f in f45}
    n_sin_par = n_pond_b = n_nsnr_b = n_bl_b = n_fuera_b = 0
    n_agr_ns = n_dom_fuera = n_sin_dis_b = n_fac_dif = 0
    n_dom = {"U": 0, "C": 0, "R": 0}
    u_b = []
    for f in f678:
        pid = f["ID_PER"]
        if pid not in agr_de:
            n_sin_par += 1
            continue
        w = _flotante(f["FAC_SEL"])
        if w is None or w <= 0:
            n_pond_b += 1
            continue
        w45 = _flotante(fac_de[pid])
        if w45 is not None and abs(w45 - w) > 1.0e-9:
            n_fac_dif += 1
        dom = f["DOMINIO"].strip()
        if dom in n_dom:
            n_dom[dom] += 1
        c = _cod(f["AP7_3_5"])
        if c == 9:
            n_nsnr_b += 1
            continue
        if c is None:
            n_bl_b += 1
            continue
        if c not in (1, 2):
            n_fuera_b += 1
            continue
        ca = _cod(agr_de[pid])
        if ca not in (1, 2):
            n_agr_ns += 1
            continue
        if dom not in DOM_OK:
            n_dom_fuera += 1
            continue
        e = f["EST_DIS"].strip()
        m = f["UPM_DIS"].strip()
        if not e or not m:
            n_sin_dis_b += 1
        u_b.append({"w": w, "e": e, "u": m, "dom": dom,
                    "agr": 1 if ca == 1 else 0,
                    "d": 1.0 if c == 1 else 0.0})

    out[P + "B-N-SIN-PAREJA"] = n_sin_par
    out[P + "B-COBERTURA-JOIN"] = _num(
        (len(f678) - n_sin_par) / len(f678) if f678 else None)
    out[P + "B-N-SIN-PONDERADOR"] = n_pond_b
    out[P + "B-N-NSNR"] = n_nsnr_b
    out[P + "B-N-BLANCO"] = n_bl_b
    out[P + "B-N-FUERA-DE-DOMINIO"] = n_fuera_b
    out[P + "B-N-AGRAVIO-NSNR"] = n_agr_ns
    out[P + "B-N-DOMINIO-U"] = n_dom["U"]
    out[P + "B-N-DOMINIO-C"] = n_dom["C"]
    out[P + "B-N-DOMINIO-R"] = n_dom["R"]
    out[P + "B-N-DOMINIO-FUERA"] = n_dom_fuera
    out[P + "B-N-SIN-DISENO"] = n_sin_dis_b
    out[P + "B-N-U"] = len(u_b)
    out[P + "G-N-FAC-SEL-DISCREPA-ENTRE-TABLAS"] = n_fac_dif
    out[P + "B-DELTA-N-VS-GEN1"] = len(u_b) - int(n_gen1["U_B"])

    if not u_b:
        out[P + "B-VEREDICTO"] = "NO-ESTIMABLE-UNIVERSO-VACIO"
        for k in ("B-ADOPCION-P3-URB", "B-ADOPCION-P3-RUR"):
            out[P + k] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    wb = np.array([r["w"] for r in u_b], dtype=float)
    db = np.array([r["d"] for r in u_b], dtype=float)
    eb = np.array([r["e"] for r in u_b])
    mb = np.array([r["u"] for r in u_b])
    dom = np.array([r["dom"] for r in u_b])
    agr = np.array([r["agr"] for r in u_b])
    out[P + "B-MASA-FAC-SEL-U"] = _num(float(np.sum(wb)))
    out[P + "B-P-U"] = _num(_p(db, wb))

    def celda(conj, con_agravio):
        return np.isin(dom, list(conj)) & (agr == (1 if con_agravio else 0))

    mascaras = {
        "URB-AGR": celda(URB, True), "RUR-AGR": celda(RUR, True),
        "URB-SIN": celda(URB, False), "RUR-SIN": celda(RUR, False),
    }
    alt = {
        "URB-AGR": celda(URB_ALT, True), "RUR-AGR": celda(RUR_ALT, True),
        "URB-SIN": celda(URB_ALT, False), "RUR-SIN": celda(RUR_ALT, False),
    }
    for nombre, mk in mascaras.items():
        out[P + f"B-N-{nombre}"] = int(mk.sum())
        out[P + f"B-P-{nombre}"] = _num(
            _p(db[mk], wb[mk]) if mk.any() else None)
    for nombre, mk in alt.items():
        out[P + f"B-ALT-P-{nombre}"] = _num(
            _p(db[mk], wb[mk]) if mk.any() else None)

    p_ua = out[P + "B-P-URB-AGR"]
    p_ra = out[P + "B-P-RUR-AGR"]
    p_us = out[P + "B-P-URB-SIN"]
    p_alt_ua = out[P + "B-ALT-P-URB-AGR"]
    out[P + "B-DIF-C1"] = _num(None if (p_ua is None or p_ra is None)
                               else p_ua - p_ra)
    out[P + "B-DIF-C2"] = _num(None if (p_ua is None or p_us is None)
                               else p_ua - p_us)
    out[P + "B-DELTA-AGRUPACION"] = _num(
        None if (p_ua is None or p_alt_ua is None) else p_ua - p_alt_ua)

    if n_sin_dis_b == len(u_b):
        out[P + "B-METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        ps, n_est_b, n_upm_b, n_una_b = _bootstrap(
            {k: (mk, db, wb) for k, mk in mascaras.items()},
            eb, mb, replicas, semilla)
        for nombre in mascaras:
            lo, hi = _pct(ps.get(nombre))
            out[P + f"B-IC-LO-{nombre}"] = _num(lo)
            out[P + f"B-IC-HI-{nombre}"] = _num(hi)
        # diferencias RÉPLICA A RÉPLICA, no resta de dos bootstraps
        for suf, a, b in (("C1", "URB-AGR", "RUR-AGR"),
                          ("C2", "URB-AGR", "URB-SIN")):
            sa, sb = ps.get(a), ps.get(b)
            if sa is None or sb is None:
                continue
            lo, hi = _pct(sa - sb)
            out[P + f"B-IC-LO-DIF-{suf}"] = _num(lo)
            out[P + f"B-IC-HI-DIF-{suf}"] = _num(hi)
        out[P + "B-N-ESTRATOS"] = int(n_est_b)
        out[P + "B-N-UPM"] = int(n_upm_b)
        out[P + "B-N-ESTRATOS-UPM-UNICA"] = int(n_una_b)
        out[P + "B-METODO-IC"] = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_una_b > 0
                                  else "IC-BOOTSTRAP-UPM-EN-ESTRATO")

    for suf, res, pv in (("URB", "RES-0061", p_ua), ("RUR", "RES-0062", p_ra)):
        g = float(gen1[res])
        if pv is None:
            out[P + f"B-REPRODUCE-{suf}-GEN1"] = "NO-COMPARABLE"
            out[P + f"B-ADOPCION-P3-{suf}"] = "NO-ADOPTABLE-NO-ESTIMABLE"
            continue
        dl = pv - g
        out[P + f"B-DELTA-{suf}-VS-GEN1"] = _num(dl)
        out[P + f"B-REPRODUCE-{suf}-GEN1"] = ("REPRODUCE" if abs(dl) <= tol
                                              else "NO-REPRODUCE")
        dg = round(pv, grano) - g
        out[P + f"B-ADOPCION-P3-{suf}-DELTA"] = _num(dg)
        if abs(dl) > tol:
            out[P + f"B-ADOPCION-P3-{suf}"] = "NO-ADOPTABLE-POR-DISCREPANCIA"
        elif abs(dg) > 0:
            out[P + f"B-ADOPCION-P3-{suf}"] = "NO-ADOPTABLE-POR-GRANO"
        else:
            out[P + f"B-ADOPCION-P3-{suf}"] = "ADOPTABLE-POR-REPLICA"

    out[P + "B-VEREDICTO"] = "TASA-REPORTADA"
    return out
