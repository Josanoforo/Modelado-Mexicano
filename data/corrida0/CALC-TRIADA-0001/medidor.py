"""`CALC-TRIADA-0001` -- ACTO GEN2-F5-TRIADA-CALC (ENCARGO 5/5), P2: el computo.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-...": v}`.

EJECUTA, sin enmendarla, la spec sellada
`forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md`
(`sha256 db6b24c579e72dc705c772200ca2c4066bd9708cc6c06c85c5101d56b081b4f5`),
citada como input por hash: universo (`U0`/`UR`/regla de `U3`), tres
contendientes (`L_SOLO`, `L_CORPUS`, `M`), agregacion `L` por mediana de
replicas `EXTRAIBLE`, metrica en puntos porcentuales, `MAE_X`, las tres
`Delta(A,B)` pareadas, bootstrap pareado (`seed=42`, 10,000 replicas,
IC95, MISMOS indices de celda para los tres contendientes), banda
`delta = 0.5 pp`, escala pareada exhaustiva de Sec.4, escala global de
Sec.4, cobertura de Sec.5, secundaria TRANSFERENCIA de Sec.6 y rol
diagnostico de `B` de Sec.7.

QUE NO HACE, por prohibicion expresa del encargo y de la spec:
no quita outliers, no cambia la agregacion (la mediana ya estaba elegida
antes de este contrato), no pondera familias, no cuenta las 8 replicas como
8 tareas independientes, no elige la mejor replica, no vuelve a correr
ningun brazo, no calibra `M`, no completa `R`, no modifica el extractor y
no admite a `B` como cuarto contendiente. No abre `data/raw`, no llama a
ningun modelo, no escribe en ningun insumo.

CONTROLES DE IDENTIDAD Y CONTAMINACION (Sec.1.4 + Sec.4 fila
`NO-ADJUDICABLE-POR-CONTROL`), medidos aqui y no heredados:

  (a) IDENTIDAD DE CAPTURA. Cada una de las 224 capturas se coteja contra
      el manifiesto sellado de `F5-RECAPTURA-L`: `sha256` del snapshot ya
      verificado por `preflight` == `sha256_archivo` del manifiesto, y
      `id_celda`/`variante`/`indice` coincidiendo entre nombre de archivo,
      manifiesto y JSON. Un fallo es `ERROR-IDENTIDAD` -- defecto material,
      no "no se pudo extraer".
  (b) RE-DERIVACION DE LA EXTRACCION. El extractor v1.3 sellado se ejecuta
      aqui sobre las 224 capturas y su salida se compara, captura por
      captura, contra el manifiesto de extraccion sellado por `ENCARGO 1/5`.
      Toda discordancia se cuenta y se reporta; si hay al menos una, el
      veredicto global se fuerza a `NO-ADJUDICABLE-POR-CONTROL`.
  (c) FIREWALL DE `M`. Se lee `estado_firewall` por celda del snapshot
      sellado de `ENCARGO 4/5` y, ADEMAS, se corre un control propio de
      identidad numerica: `punto_M == R` (al grano de float) en una celda
      significaria que la cadena de `M` consumio el arbitro que la evalua.
  (d) MISMO `U3` PARA LAS TRES PAREADAS. Se construye UNA sola lista de
      celdas y las tres comparaciones y el bootstrap la usan; que las tres
      compartan universo se verifica y se reporta, no se supone.
"""
from __future__ import annotations

import json
import math
import re
import statistics
import sys
import types

# --- Constantes DECLARADAS tambien en spec.yaml (se asertan contra el
#     contrato normalizado: el medidor no puede divergir en silencio). -------
VARIANTES = (("L-solo", "L_SOLO"), ("L+corpus", "L_CORPUS"))
K = 8
CONTENDIENTES = ("L_SOLO", "L_CORPUS", "M")


def _exec_modulo_desde_bytes(nombre: str, crudo: bytes, ruta_declarada: str) -> types.ModuleType:
    """Ejecuta el CONTENIDO ya resuelto por el snapshot de `preflight` (los
    mismos bytes que el sha256 verificado identifica) -- el archivo no se
    reabre por segunda vez."""
    mod = types.ModuleType(nombre)
    mod.__file__ = ruta_declarada
    sys.modules[nombre] = mod
    exec(compile(crudo.decode("utf-8"), ruta_declarada, "exec"), mod.__dict__)
    return mod


def _json(inputs: dict, iid: str):
    return json.loads(inputs[iid]["bytes"].decode("utf-8"))


def _tsv(inputs: dict, iid: str) -> list[dict]:
    texto = inputs[iid]["bytes"].decode("utf-8")
    lineas = [l for l in texto.split("\n") if l != ""]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def _cuantil_7(ordenados: list[float], probabilidad: float) -> float:
    """Identico al de `scoring-adv1-m3.py::_cuantil_7` (tipo 7 de R)."""
    if len(ordenados) == 1:
        return float(ordenados[0])
    posicion = (len(ordenados) - 1) * probabilidad
    inferior, superior = math.floor(posicion), math.ceil(posicion)
    if inferior == superior:
        return float(ordenados[inferior])
    peso = posicion - inferior
    return float(ordenados[inferior] * (1 - peso) + ordenados[superior] * peso)


def _pref(cid: str) -> str:
    return f"RESULT-TRIADA-{cid.replace('-', '_')}"


def _id_captura(cid: str, variante: str, k: int) -> str:
    return f"cap_{cid}_{variante.replace('+', 'p').replace('-', '_')}_{k:02d}"


def _nombre_captura(cid: str, variante: str, k: int) -> str:
    return f"L-{cid}-M__{variante}__{k:02d}__v1_3.json"


def _anios(texto: str) -> list[int]:
    return [int(a) for a in re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", texto or "")]


def _veredicto_pareado(ic_lo, ic_hi, delta: float) -> str:
    """Escala pareada EXHAUSTIVA, Sec.4 de la spec sellada, copiada sin
    reinterpretar. `Delta(A,B) = media(error_A - error_B)`; negativo favorece
    A. Las cuatro filas son mutuamente excluyentes y cubren todo caso."""
    if ic_lo is None or ic_hi is None:
        return "SIN-UNIVERSO-PAREADO"
    if ic_hi < -delta:
        return "A-GANA"
    if ic_lo > delta:
        return "B-GANA"
    if -delta <= ic_lo and ic_hi <= delta:
        return "EMPATE-PRACTICO"
    return "INCONCLUSO"


def medir(inputs: dict, contrato: dict) -> dict:
    par = contrato["parametros"]
    SEED = int(contrato["seed"]["valor"])
    REPLICAS = int(par["bootstrap_replicas"])
    NIVEL_IC = float(par["nivel_ic"])
    DELTA = float(par["delta_banda_pp"])
    SCOPE = str(par["scope_id_bootstrap"])
    assert SEED == int(par["bootstrap_seed"]), "seed del contrato incoherente"
    assert int(par["k_replicas_l"]) == K, "k declarado != k del medidor"

    extrae = _exec_modulo_desde_bytes(
        "extrae_l_v1_3_triada", inputs["extrae_l_v1_3_py"]["bytes"],
        "tools/extrae_l_v1_3.py")
    pipeline = _exec_modulo_desde_bytes(
        "pipeline_l_adv1_m2_triada", inputs["pipeline_l_adv1_m2_py"]["bytes"],
        "forense/prereg-duelo-v2/pipeline-L-adv1-m2.py")
    motor = _exec_modulo_desde_bytes(
        "scoring_adv1_m3_triada", inputs["scoring_adv1_m3_py"]["bytes"],
        "forense/prereg-duelo-v2/scoring-adv1-m3.py")

    R: dict = {}

    # ── 1 · UNIVERSOS U0 y UR, del sidecar congelado (Sec.1.1/1.2) ─────────
    sidecar = _tsv(inputs, "universo_triada_v1_4")
    U0 = [f["id_celda"] for f in sidecar if f["en_U0"] == "SI"]
    UR = [f["id_celda"] for f in sidecar if f["en_UR"] == "SI"]
    side = {f["id_celda"]: f for f in sidecar}
    R["RESULT-TRIADA-U0-N"] = len(U0)
    R["RESULT-TRIADA-UR-N"] = len(UR)

    marco = {f["id"]: f for f in _tsv(inputs, "marco_m_sorteado_v1_3")}
    snap = {c["id_celda"]: c for c in _json(inputs, "snapshot_m")["celdas"]}
    manif_ext = _json(inputs, "manifiesto_extraccion_l_v1_3")["capturas"]
    manif_cap = _json(inputs, "manifiesto_capturas_p3")["capturas"]

    # ── 2 · Por celda: R, L (re-derivado), M, firewall ─────────────────────
    errores_identidad: list[str] = []
    discordancias_manifiesto: list[str] = []
    n_capturas_examinadas = 0
    cob = {c: {"EXTRAIBLE": 0, "NO-EXTRAIBLE": 0, "AMBIGUA": 0} for _, c in VARIANTES}

    punto: dict = {}          # cid -> {"L_SOLO":x|None,"L_CORPUS":x|None,"M":x|None}
    r_punto: dict = {}
    contaminadas: list[str] = []
    sin_punto = {"L_SOLO": [], "L_CORPUS": [], "M": []}

    for cid in U0:
        p = _pref(cid)
        rj = _json(inputs, f"calc_r_{cid}")["resultados"]
        r_val = rj[f"RESULT-R-{cid}-PUNTO"]
        ee_val = rj[f"RESULT-R-{cid}-EE"]
        r_punto[cid] = r_val
        R[f"{p}-R"] = r_val
        R[f"{p}-EE-R"] = ee_val

        # -- L: re-derivacion con el extractor v1.3 sellado ----------------
        agregados = {}
        for variante, clave in VARIANTES:
            valores: list[float] = []
            n_ext = 0
            for k in range(1, K + 1):
                iid = _id_captura(cid, variante, k)
                nombre = _nombre_captura(cid, variante, k)
                ent = inputs[iid]
                datos = json.loads(ent["bytes"].decode("utf-8"))
                n_capturas_examinadas += 1
                # (a) identidad de captura
                mc = manif_cap.get(nombre)
                if mc is None:
                    errores_identidad.append(f"{nombre}:AUSENTE-EN-MANIFIESTO-CAPTURAS")
                elif mc.get("sha256_archivo") != ent["sha256"]:
                    errores_identidad.append(f"{nombre}:SHA-DISCORDA-CON-MANIFIESTO")
                elif (mc.get("id_celda"), mc.get("variante"), mc.get("indice")) != (cid, variante, k):
                    errores_identidad.append(f"{nombre}:TRIPLETA-MANIFIESTO-DISCORDA")
                if (datos.get("id_celda"), datos.get("variante"), datos.get("indice")) != (cid, variante, k):
                    errores_identidad.append(f"{nombre}:TRIPLETA-JSON-DISCORDA")
                # (b) extraccion re-derivada y cotejada contra 1/5
                ext = extrae.extraer_valor(datos["texto_crudo"])
                sellada = manif_ext.get(nombre)
                if sellada is None:
                    discordancias_manifiesto.append(f"{nombre}:AUSENTE-EN-MANIFIESTO-EXTRACCION")
                else:
                    v_sell = sellada.get("valor_extraido")
                    v_sell = None if v_sell in ("", None) else float(v_sell)
                    if sellada.get("estado") != ext.estado:
                        discordancias_manifiesto.append(
                            f"{nombre}:ESTADO {sellada.get('estado')}!={ext.estado}")
                    elif (v_sell is None) != (ext.valor_extraido is None) or (
                            v_sell is not None
                            and abs(v_sell - ext.valor_extraido) > 1e-12):
                        discordancias_manifiesto.append(
                            f"{nombre}:VALOR {v_sell}!={ext.valor_extraido}")
                cob[clave][ext.estado] = cob[clave].get(ext.estado, 0) + 1
                if ext.estado == "EXTRAIBLE":
                    valores.append(ext.valor_extraido)
                    n_ext += 1
            # Agregacion heredada SIN CAMBIO: mediana de las replicas
            # EXTRAIBLE (`pipeline-L-adv1-m2.py::agregar_continua`).
            agg = pipeline.agregar_continua(valores)
            agregados[clave] = agg["mediana"]
            R[f"{p}-N-EXTRAIBLE-{clave.replace('_', '-')}"] = n_ext

        # -- M y firewall ---------------------------------------------------
        sc = snap.get(cid) or {}
        m_val = sc.get("punto_M") if sc.get("estado_M") == "EMITE" else None
        firewall = str(sc.get("estado_firewall") or "SIN-SNAPSHOT")
        # (c) control propio de identidad numerica M vs R
        if m_val is not None and r_punto[cid] == m_val:
            control_id = "CONTAMINADA-M-IGUAL-A-R"
        elif m_val is None:
            control_id = "NO-APLICA-SIN-PUNTO-M"
        else:
            control_id = "DISTINTO-DE-R"
        R[f"{p}-FIREWALL"] = firewall
        R[f"{p}-CONTROL-IDENTIDAD-M-VS-R"] = control_id
        contaminada = (firewall != "LIMPIO-DE-OBJETIVO") or (control_id == "CONTAMINADA-M-IGUAL-A-R")
        if contaminada and cid in UR:
            contaminadas.append(cid)

        punto[cid] = {"L_SOLO": agregados["L_SOLO"], "L_CORPUS": agregados["L_CORPUS"],
                      "M": m_val}
        for c in CONTENDIENTES:
            R[f"{p}-{c.replace('_', '-')}"] = punto[cid][c]
            if punto[cid][c] is None and cid in UR:
                sin_punto[c].append(cid)

    R["RESULT-TRIADA-COBERTURA-CAPTURAS-EXAMINADAS"] = n_capturas_examinadas
    R["RESULT-TRIADA-CONTROL-IDENTIDAD-CAPTURAS-FALLAS-N"] = len(errores_identidad)
    R["RESULT-TRIADA-CONTROL-IDENTIDAD-CAPTURAS-FALLAS"] = (
        "; ".join(errores_identidad[:20]) if errores_identidad else "NINGUNA")
    R["RESULT-TRIADA-CONTROL-REDERIVACION-EXTRACCION-DISCORDANCIAS-N"] = len(discordancias_manifiesto)
    R["RESULT-TRIADA-CONTROL-REDERIVACION-EXTRACCION-DISCORDANCIAS"] = (
        "; ".join(discordancias_manifiesto[:20]) if discordancias_manifiesto else "NINGUNA")
    for _, clave in VARIANTES:
        cl = clave.replace("_", "-")
        R[f"RESULT-TRIADA-COBERTURA-{cl}-REPLICAS-EXTRAIBLES"] = cob[clave]["EXTRAIBLE"]
        R[f"RESULT-TRIADA-COBERTURA-{cl}-REPLICAS-NO-EXTRAIBLES"] = cob[clave]["NO-EXTRAIBLE"]
        R[f"RESULT-TRIADA-COBERTURA-{cl}-REPLICAS-AMBIGUAS"] = cob[clave]["AMBIGUA"]

    # ── 3 · U3 = interseccion de Sec.1.3 (la UNICA puerta de entrada) ──────
    U3 = [cid for cid in UR
          if punto[cid]["L_SOLO"] is not None
          and punto[cid]["L_CORPUS"] is not None
          and punto[cid]["M"] is not None
          and cid not in contaminadas]
    R["RESULT-TRIADA-U3-N"] = len(U3)
    R["RESULT-TRIADA-U3-IDS"] = ", ".join(U3) if U3 else "VACIO"
    for c in CONTENDIENTES:
        cl = c.replace("_", "-")
        R[f"RESULT-TRIADA-COBERTURA-{cl}-CELDAS-CON-PUNTO"] = sum(
            1 for cid in UR if punto[cid][c] is not None)
        R[f"RESULT-TRIADA-EXCLUSIONES-SIN-PUNTO-{cl}-N"] = len(sin_punto[c])
        R[f"RESULT-TRIADA-EXCLUSIONES-SIN-PUNTO-{cl}-IDS"] = (
            ", ".join(sin_punto[c]) if sin_punto[c] else "NINGUNA")
    R["RESULT-TRIADA-EXCLUSIONES-POR-CONTAMINACION-N"] = len(contaminadas)
    R["RESULT-TRIADA-EXCLUSIONES-POR-CONTAMINACION-IDS"] = (
        ", ".join(contaminadas) if contaminadas else "NINGUNA")
    R["RESULT-TRIADA-EXCLUSIONES-POR-IDENTIDAD-N"] = len(errores_identidad)
    R["RESULT-TRIADA-EXCLUSIONES-POR-IDENTIDAD-IDS"] = (
        "; ".join(sorted({e.split(':')[0] for e in errores_identidad})) if errores_identidad
        else "NINGUNA")

    # ── 4 · Errores en pp, fila durable por celda (Sec.3) ──────────────────
    for cid in U0:
        p = _pref(cid)
        for c in CONTENDIENTES:
            v = punto[cid][c]
            R[f"{p}-ERROR-{c.replace('_', '-')}-PP"] = (
                abs(v - r_punto[cid]) * 100.0 if v is not None else None)
        en_u3 = "SI" if cid in U3 else "NO"
        R[f"{p}-EN-U3"] = en_u3
        if en_u3 == "SI":
            nota = "en U3: R sellado + punto valido de L_SOLO, L_CORPUS y M + no contaminada"
        else:
            faltan = [c for c in CONTENDIENTES if punto[cid][c] is None]
            razones = []
            if cid not in UR:
                razones.append("fuera de UR")
            if faltan:
                razones.append("sin punto valido de " + "/".join(faltan))
            if cid in contaminadas:
                razones.append("CONTAMINADA-POR-OBJETIVO")
            nota = "fuera de U3: " + "; ".join(razones) if razones else "fuera de U3"
        nota_side = (side.get(cid) or {}).get("nota", "")
        if "FP-371" in nota_side:
            nota += " | reserva FP-371 sobre EE/IC de R (no afecta el punto)"
        R[f"{p}-NOTA-DE-CORTE"] = nota

    # ── 5 · MAE y pareadas, MISMO U3 para las tres (Sec.3-4) ───────────────
    n = len(U3)
    errores = {c: [abs(punto[cid][c] - r_punto[cid]) * 100.0 for cid in U3]
               for c in CONTENDIENTES}
    for c in CONTENDIENTES:
        R[f"RESULT-TRIADA-MAE-{c.replace('_', '-')}"] = (
            statistics.fmean(errores[c]) if n else None)

    indices = None
    if n:
        seed_scope = motor.derivar_seed_scope(SEED, SCOPE)
        # MISMOS indices de celda para los tres contendientes: se generan UNA
        # vez y las tres pareadas los reutilizan (Sec.4, segunda vinieta).
        indices = motor.generar_indices_bootstrap(n, REPLICAS, seed_scope)
    cola = (1.0 - NIVEL_IC) / 2.0

    PAREADAS = (("LCORPUS-LSOLO", "L_CORPUS", "L_SOLO"),
                ("M-LSOLO", "M", "L_SOLO"),
                ("M-LCORPUS", "M", "L_CORPUS"))
    veredicto_par: dict = {}
    for etiqueta, a, b in PAREADAS:
        if not n:
            pt = lo = hi = None
        else:
            difs = [errores[a][i] - errores[b][i] for i in range(n)]
            pt = statistics.fmean(difs)
            reps = sorted(sum(difs[i] for i in rep) / n for rep in indices)
            lo = _cuantil_7(reps, cola)
            hi = _cuantil_7(reps, 1.0 - cola)
        v = _veredicto_pareado(lo, hi, DELTA)
        veredicto_par[etiqueta] = (v, a, b)
        R[f"RESULT-TRIADA-DELTA-{etiqueta}-PUNTO"] = pt
        R[f"RESULT-TRIADA-DELTA-{etiqueta}-IC-LO"] = lo
        R[f"RESULT-TRIADA-DELTA-{etiqueta}-IC-HI"] = hi
        R[f"RESULT-TRIADA-DELTA-{etiqueta}-VEREDICTO"] = v
    R["RESULT-TRIADA-BOOTSTRAP-INDICES-COMPARTIDOS"] = (
        "SI -- un solo vector de indices por replica, reutilizado por las tres pareadas"
        if n else "NO-APLICA-U3-VACIO")
    R["RESULT-TRIADA-PAREADAS-MISMO-U3"] = (
        "SI -- las tres Delta se computan sobre la misma lista U3 de "
        f"{n} celda(s)")

    # ── 6 · Ranking puntual y escala global (Sec.4) ────────────────────────
    if n:
        orden = sorted(CONTENDIENTES, key=lambda c: R[f"RESULT-TRIADA-MAE-{c.replace('_', '-')}"])
    else:
        orden = list(CONTENDIENTES)
    for i, c in enumerate(orden, start=1):
        R[f"RESULT-TRIADA-RANKING-{i}"] = c if n else "NO-ESTIMABLE-U3-VACIO"
    R["RESULT-TRIADA-RANKING-PUNTUAL"] = (
        " < ".join(f"{c} (MAE={R['RESULT-TRIADA-MAE-' + c.replace('_', '-')]:.4f} pp)"
                   for c in orden)
        if n else "NO-ESTIMABLE -- U3 vacio")

    cobertura_u3 = {c: R[f"RESULT-TRIADA-COBERTURA-{c.replace('_', '-')}-CELDAS-CON-PUNTO"]
                    for c in CONTENDIENTES}

    def _gana(x: str) -> bool:
        """Sec.4: `X` gana sus DOS comparaciones y no tiene menor cobertura
        de celdas sobre UR que sus dos rivales."""
        for etiqueta, a, b in PAREADAS:
            v = veredicto_par[etiqueta][0]
            if x == a and v != "A-GANA":
                return False
            if x == b and v != "B-GANA":
                return False
        return all(cobertura_u3[x] >= cobertura_u3[y] for y in CONTENDIENTES)

    control_roto = []
    if errores_identidad:
        control_roto.append("identidad de captura")
    if discordancias_manifiesto:
        control_roto.append("re-derivacion de extraccion discorda del manifiesto sellado de 1/5")
    if any(cid in contaminadas for cid in U3):
        control_roto.append("celda CONTAMINADA-POR-OBJETIVO dentro de U3")

    if control_roto:
        veredicto = "NO-ADJUDICABLE-POR-CONTROL"
        razon = ("control roto (Sec.4, tercera fila): " + "; ".join(control_roto))
    else:
        ganadores = [c for c in CONTENDIENTES if _gana(c)] if n else []
        if len(ganadores) == 1:
            veredicto = f"GANADOR-TRIADA-{ganadores[0]}"
            razon = (f"{ganadores[0]} gana sus dos comparaciones pareadas bajo la banda "
                     f"delta={DELTA} pp y no tiene menor cobertura de celdas sobre UR")
        else:
            veredicto = "SIN-GANADOR-UNICO"
            if not n:
                razon = ("U3 vacio: ninguna celda de UR reune punto valido de los tres "
                         "contendientes bajo la regla de Sec.1.3")
            else:
                razon = ("ningun contendiente gana sus dos comparaciones pareadas bajo la "
                         "banda delta=%s pp sobre U3=%d celda(s); veredictos pareados: %s"
                         % (DELTA, n, ", ".join(f"{e}={veredicto_par[e][0]}"
                                                for e, _, _ in PAREADAS)))
    R["RESULT-TRIADA-VEREDICTO-TRIADA"] = veredicto
    R["RESULT-TRIADA-VEREDICTO-RAZON"] = razon

    # ── 7 · Secundaria TRANSFERENCIA (Sec.6) ───────────────────────────────
    # `M` entra a la secundaria en una celda solo si su calibracion no usa una
    # ola posterior a la que la celda evalua; criterio mecanico heredado de
    # `F5 v1.0` Sec.2: cita con anio >= ola de la celda, o sin anio
    # determinable, EXCLUYE.
    m_no_comparable: list[str] = []
    for cid in UR:
        anio_celda = _anios((marco.get(cid) or {}).get("ola", ""))
        anios_cal = _anios((snap.get(cid) or {}).get("ola_calibracion", ""))
        if not anio_celda or not anios_cal or max(anios_cal) >= min(anio_celda):
            m_no_comparable.append(cid)
    universo_sec = [cid for cid in U3 if cid not in m_no_comparable]
    R["RESULT-TRIADA-SECUNDARIA-M-NO-COMPARABLE-N"] = len(m_no_comparable)
    R["RESULT-TRIADA-SECUNDARIA-M-NO-COMPARABLE-IDS"] = (
        ", ".join(m_no_comparable) if m_no_comparable else "NINGUNA")
    R["RESULT-TRIADA-SECUNDARIA-TRANSFERENCIA-UNIVERSO-N"] = len(universo_sec)
    R["RESULT-TRIADA-SECUNDARIA-TRANSFERENCIA-UNIVERSO-IDS"] = (
        ", ".join(universo_sec) if universo_sec else "VACIO")
    # La pareada L_CORPUS vs L_SOLO de la secundaria se computa sobre el
    # universo donde los cortes son comparables (Sec.6). Si ese universo es
    # vacio, se declara vacio -- no se sustituye por U3.
    ns = len(universo_sec)
    if ns:
        idx = [U3.index(cid) for cid in universo_sec]
        difs = [errores["L_CORPUS"][i] - errores["L_SOLO"][i] for i in idx]
        seed_sec = motor.derivar_seed_scope(SEED, SCOPE + "-secundaria-transferencia")
        ind_sec = motor.generar_indices_bootstrap(ns, REPLICAS, seed_sec)
        pt_s = statistics.fmean(difs)
        reps = sorted(sum(difs[i] for i in rep) / ns for rep in ind_sec)
        lo_s, hi_s = _cuantil_7(reps, cola), _cuantil_7(reps, 1.0 - cola)
    else:
        pt_s = lo_s = hi_s = None
    R["RESULT-TRIADA-SECUNDARIA-DELTA-LCORPUS-LSOLO-PUNTO"] = pt_s
    R["RESULT-TRIADA-SECUNDARIA-DELTA-LCORPUS-LSOLO-IC-LO"] = lo_s
    R["RESULT-TRIADA-SECUNDARIA-DELTA-LCORPUS-LSOLO-IC-HI"] = hi_s
    R["RESULT-TRIADA-SECUNDARIA-DELTA-LCORPUS-LSOLO-VEREDICTO"] = _veredicto_pareado(
        lo_s, hi_s, DELTA)
    R["RESULT-TRIADA-SECUNDARIA-ESTADO"] = (
        "SIN-UNIVERSO -- las %d celdas de UR quedan M-NO-COMPARABLE-EN-TRANSFERENCIA "
        "bajo la calibracion de M del snapshot sellado" % len(m_no_comparable)
        if not ns else
        "CALCULADA sobre %d celda(s) con cortes comparables" % ns)

    # ── 8 · `B`, piso diagnostico y nada mas (Sec.7) ───────────────────────
    b_res = _json(inputs, "calc_b_0001")["resultados"]
    filas_b_marco_m = sum(1 for k in b_res if re.search(r"CIV-M|TRA-M|FAM-M|DIN-M", k))
    R["RESULT-TRIADA-B-FILAS-MARCO-M"] = filas_b_marco_m
    coincidencias = []
    for cid in U3:
        for k, v in b_res.items():
            if k.endswith("-P") and isinstance(v, (int, float)) and v == r_punto[cid]:
                coincidencias.append(f"{cid}:R=={k}")
    R["RESULT-TRIADA-B-COINCIDENCIAS-CON-R"] = (
        "; ".join(coincidencias) if coincidencias else "NINGUNA")
    R["RESULT-TRIADA-B-DIAGNOSTICO"] = (
        "B no tiene fila por id_celda de marco-M (%d), consistente con "
        "procedimiento-scoring-v1_2.md Sec.4; las unicas cifras de CALC-B-0001 que "
        "tocan este panel son la serie ENIGH de remesas, y %s. B no entra a U3, ni al "
        "ranking, ni a la adjudicacion, ni tiene veto (Sec.7)."
        % (filas_b_marco_m,
           ("coinciden al grano de float con el propio R de las celdas de U3 (%s), de modo "
            "que no constituyen un piso independiente" % "; ".join(coincidencias))
           if coincidencias else "no coinciden con ningun R de U3"))

    return R
