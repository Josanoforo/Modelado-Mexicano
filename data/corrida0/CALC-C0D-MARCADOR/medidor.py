"""`CALC-C0D-MARCADOR` — el marcador GEN2: la pareada `L_SOLO ↔ L_CORPUS`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-C0-D`, ANTES DE CALCULAR UNA
SOLA CIFRA. Spec sellada que lo gobierna:
`forense/prereg-caja/C0D-MARCADOR-spec-v1_0.md` (`prereg-caja-C0D-MARCADOR`).

NO mide ninguna regla y ninguna cifra suya entra a un veredicto (`T9`). No toca
capturas, ni motor, ni `CALC` previos, ni la banda `z` primaria del duelo.

La maquinaria de bootstrap NO se reimplementa: se ejecuta desde los BYTES que
`preflight` ya verifico por sha256 de `forense/prereg-duelo-v2/scoring-adv1-m3.py`
(`origen: repo`), mismo patron que `CALC-B-0001` usa con su selector.
"""
from __future__ import annotations

import json
import statistics
import sys
import types

CORREDORES = ("L_SOLO", "L_CORPUS", "M")
_SUFIJO = {"L_SOLO": "L-SOLO", "L_CORPUS": "L-CORPUS", "M": "M"}


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _num_declarado(v):
    """`(numero_o_None, literal_si_no_era_numero)`.

    Un RESULT de `CALC-B-0001` puede traer un ESTADO en texto donde esta spec
    espera una cifra (`SIN_BASELINE`, `NO-ADOPTABLE-POR-GRANO`). Eso NO es un
    crash de la corrida ni un `null` mudo: el numero sale `None` y el literal
    viaja en la cita, para que el estado se vea en el resultado."""
    if v is None:
        return None, None
    if isinstance(v, str):
        try:
            return _num(float(v)), None
        except ValueError:
            return None, v
    return _num(v), None


def _json(inputs, iid):
    return json.loads(inputs[iid]["bytes"].decode("utf-8"))


def _scoring(inputs):
    """Modulo del scoring sellado, ejecutado desde los bytes verificados.

    Se registra en `sys.modules` ANTES del `exec`: mismo patron que
    `_carga_medidor` de `tools/corrida0.py` y que `CALC-B-0001::_selector`."""
    nombre = "scoring_adv1_m3_calc_c0d"
    mod = types.ModuleType(nombre)
    sys.modules[nombre] = mod
    exec(compile(inputs["IN-SCORING-M3"]["bytes"], "scoring-adv1-m3.py", "exec"),
         mod.__dict__)
    return mod


def _celdas_del_marco(inputs):
    """Las 14 filas de `marco-M-sorteado-v1_3.tsv`, en su orden de archivo.

    §5 del procedimiento sellado excluye `grado_DD == VERIFICACION-NO-PUNTUA`;
    la exclusion se APLICA aqui aunque §0.4 de la sellada ya verifico que hoy
    no retira ninguna — una guardia que solo funciona si el arbol no cambia no
    es una guardia."""
    crudo = inputs["IN-MARCO-V1-3"]["bytes"].decode("utf-8")
    lineas = crudo.splitlines()
    cab = lineas[0].split("\t")
    i_id, i_dd = cab.index("id"), cab.index("grado_DD")
    i_enc, i_ola = cab.index("encuesta"), cab.index("ola")
    i_esc = cab.index("escala")
    fuera = []
    for ln in lineas[1:]:
        if not ln.strip():
            continue
        c = ln.split("\t")
        if c[i_dd].strip() == "VERIFICACION-NO-PUNTUA":
            continue
        fuera.append({"id": c[i_id].strip(), "encuesta": c[i_enc].strip(),
                      "ola": c[i_ola].strip(), "escala": c[i_esc].strip()})
    return fuera


def _punto_l(inputs, cid, tag, variante):
    """Media de `valor_extraido` sobre las replicas no nulas de las 8.

    Regla verbatim de `agregado_v1_1._leer_l_variante`: si CERO de las 8 trae
    valor, el punto es NO-DISPONIBLE — no se sustituye por 0 ni por nada."""
    valores, n_ex = [], 0
    for k in range(1, 9):
        iid = f"IN-L-{tag}-{cid}-{k:02d}"
        if iid not in inputs:
            continue
        n_ex += 1
        d = json.loads(inputs[iid]["bytes"].decode("utf-8"))
        if d.get("variante") != variante:
            raise ValueError(f"{iid}: variante inesperada {d.get('variante')!r}")
        v = d.get("valor_extraido")
        if v is not None:
            valores.append(float(v))
    if not valores:
        return None, n_ex, 0
    return statistics.fmean(valores), n_ex, len(valores)


def _ic_bootstrap(sc, scope_id, valores):
    """Media + IC95 por bootstrap sobre celdas, con la maquinaria sellada."""
    n = len(valores)
    if n == 0:
        return None, None, None
    seed = sc.derivar_seed_scope(42, scope_id)
    indices = sc.generar_indices_bootstrap(n, 10000, seed)
    replicas = sorted(statistics.fmean(valores[i] for i in rep) for rep in indices)
    cola = (1.0 - 0.95) / 2.0
    return (statistics.fmean(valores),
            sc._cuantil_7(replicas, cola),
            sc._cuantil_7(replicas, 1.0 - cola))


# ── el marcador ───────────────────────────────────────────────────────────

def medir(inputs, contrato):
    P = contrato["parametros"]
    N_MIN = int(P["n_minimo_pareada"])
    K_CONM = float(P["k_umbral_conmensurabilidad"])
    TOL_CONV = float(P["tolerancia_convergencia_L"])
    CORTE = str(P["fecha_corte_alcance"])
    SCOPES = P["scopes_bootstrap"]
    sc = _scoring(inputs)
    out = {}

    # --- 1) puntos por celda ---------------------------------------------
    celdas = _celdas_del_marco(inputs)
    reg = {}
    for c in celdas:
        cid = c["id"]
        r = _json(inputs, f"IN-R-{cid}")
        R = r["R"] if r.get("estado") == "COMPUTADO" else None
        EE = r.get("EE_R") if r.get("estado") == "COMPUTADO" else None
        m = _json(inputs, f"IN-M-{cid}")
        p_solo, _, _ = _punto_l(inputs, cid, "SOLO", "L-solo")
        p_corp, _, _ = _punto_l(inputs, cid, "CORPUS", "L+corpus")
        fila = {"R": _num(R), "EE_R": _num(EE),
                "L_SOLO": _num(p_solo), "L_CORPUS": _num(p_corp),
                "M": _num(m.get("valor_punto")),
                "encuesta": c["encuesta"], "ola": c["ola"]}
        for a in CORREDORES:
            fila[f"err_{a}"] = (100.0 * (fila[a] - fila["R"])
                                if (fila[a] is not None and fila["R"] is not None)
                                else None)
        fila["d"] = (abs(fila["err_L_CORPUS"]) - abs(fila["err_L_SOLO"])
                     if (fila["err_L_CORPUS"] is not None
                         and fila["err_L_SOLO"] is not None) else None)
        reg[cid] = fila
        out[f"RESULT-C0D-{cid}-R"] = fila["R"]
        out[f"RESULT-C0D-{cid}-EE-R"] = fila["EE_R"]
        for a in CORREDORES:
            out[f"RESULT-C0D-{cid}-ERRPP-{_SUFIJO[a]}"] = fila[f"err_{a}"]
        out[f"RESULT-C0D-{cid}-D-PAREADA"] = fila["d"]

    orden = [c["id"] for c in celdas]

    # --- 2) control de convergencia contra el agregado sellado ------------
    agg = _json(inputs, "IN-AGREGADO-V1-3-RESULTADO").get("celdas", {})
    diverge, maxdif, n_cmp = [], 0.0, 0
    for cid in orden:
        for a, clave in (("L_SOLO", "L_solo"), ("L_CORPUS", "L_corpus")):
            mio, suyo = reg[cid][a], agg.get(cid, {}).get(clave)
            if mio is None and suyo is None:
                n_cmp += 1
                continue
            if mio is None or suyo is None:
                diverge.append(f"{cid}:{a}:uno-ausente")
                n_cmp += 1
                continue
            n_cmp += 1
            dif = abs(float(mio) - float(suyo))
            maxdif = max(maxdif, dif)
            if dif > TOL_CONV:
                diverge.append(f"{cid}:{a}:{dif:.3e}")
    out["RESULT-C0D-CONTROL-CONVERGENCIA-L"] = (
        "CONVERGE" if not diverge else "DIVERGE:" + ",".join(diverge))
    out["RESULT-C0D-CONTROL-MAXDIF-L"] = maxdif
    out["RESULT-C0D-CONTROL-N-PUNTOS-L"] = n_cmp

    # --- 3) universos: marginal por corredor, y el comun ------------------
    marg = {a: [cid for cid in orden
                if reg[cid]["R"] is not None and reg[cid][a] is not None]
            for a in CORREDORES}
    comun = [cid for cid in orden
             if reg[cid]["R"] is not None
             and all(reg[cid][a] is not None for a in CORREDORES)]
    identicos = len({tuple(marg[a]) for a in CORREDORES}) == 1
    out["RESULT-C0D-UNIVERSOS-IDENTICOS"] = "SI" if identicos else "NO"
    out["RESULT-C0D-N-UNIVERSO-COMUN"] = len(comun)

    mae = {}
    for fam, universo in (("MARGINAL", marg), ("COMUN", {a: comun for a in CORREDORES})):
        clave_scope = "mae_marginal" if fam == "MARGINAL" else "mae_comun"
        for a in CORREDORES:
            U = universo[a]
            errs = [abs(reg[cid][f"err_{a}"]) for cid in U]
            punto, lo, hi = _ic_bootstrap(sc, SCOPES[clave_scope].format(corredor=a), errs)
            mae[(fam, a)] = punto
            s = _SUFIJO[a]
            out[f"RESULT-C0D-MAE-{fam}-{s}"] = punto
            out[f"RESULT-C0D-MAE-{fam}-{s}-IC-LO"] = lo
            out[f"RESULT-C0D-MAE-{fam}-{s}-IC-HI"] = hi
            out[f"RESULT-C0D-MAE-{fam}-{s}-N"] = len(U)

    def _ranking(fam):
        """SOLO los nombres, de menor a mayor error. Es lo que §5.1 compara:
        el ORDEN de los corredores, no sus cifras -- dos cadenas que llevaran
        los valores dentro siempre diferirian y la rama nunca podria caer."""
        vivos = [(mae[(fam, a)], a) for a in CORREDORES if mae[(fam, a)] is not None]
        return tuple(a for _, a in sorted(vivos))

    def _orden(fam):
        vivos = [(mae[(fam, a)], a) for a in CORREDORES if mae[(fam, a)] is not None]
        return " < ".join(f"{a}={v:.4f}" for v, a in sorted(vivos))

    rank_marginal, rank_comun = _ranking("MARGINAL"), _ranking("COMUN")
    out["RESULT-C0D-ORDEN-MARGINAL"] = _orden("MARGINAL") or "SIN-CORREDORES"
    out["RESULT-C0D-ORDEN-COMUN"] = _orden("COMUN") or "SIN-CORREDORES"

    # --- 4) las tres pareadas --------------------------------------------
    U_LL = [cid for cid in orden if reg[cid]["d"] is not None]
    pareadas = [
        ("PRIMARIA-LCORPUS-LSOLO", SCOPES["pareada_primaria"], U_LL,
         lambda f: abs(f["err_L_CORPUS"]) - abs(f["err_L_SOLO"])),
        ("SEC-LSOLO-M", SCOPES["pareada_sec_lsolo_m"], comun,
         lambda f: abs(f["err_L_SOLO"]) - abs(f["err_M"])),
        ("SEC-LCORPUS-M", SCOPES["pareada_sec_lcorpus_m"], comun,
         lambda f: abs(f["err_L_CORPUS"]) - abs(f["err_M"])),
    ]
    ic_primaria = (None, None, None)
    for etiqueta, scope, U, fn in pareadas:
        difs = [fn(reg[cid]) for cid in U]
        punto, lo, hi = _ic_bootstrap(sc, scope, difs)
        if etiqueta.startswith("PRIMARIA"):
            ic_primaria = (punto, lo, hi)
        out[f"RESULT-C0D-PAREADA-{etiqueta}-PUNTO"] = punto
        out[f"RESULT-C0D-PAREADA-{etiqueta}-IC-LO"] = lo
        out[f"RESULT-C0D-PAREADA-{etiqueta}-IC-HI"] = hi
        out[f"RESULT-C0D-PAREADA-{etiqueta}-N"] = len(U)

    ds = sorted(((abs(reg[cid]["d"]), cid) for cid in U_LL), reverse=True)[:3]
    out["RESULT-C0D-CELDAS-DOMINANTES"] = (
        " · ".join(f"{cid} d={reg[cid]['d']:+.4f}pp" for _, cid in ds) or "SIN-CELDAS")

    # --- 5) el piso B, con su guardia de conmensurabilidad ----------------
    B = _json(inputs, "IN-B-RESULTADOS")["resultados"]
    for cid, ola in P["piso_B"]["celdas"].items():
        f = reg[cid]
        for brazo in ("PERSISTENCIA", "OPERATIVO"):
            rid = f"RESULT-B-{brazo}-{ola}-P"
            pb, literal = _num_declarado(B.get(rid))
            out[f"RESULT-C0D-B-{cid}-{brazo}-CITA"] = (
                rid if literal is None else f"{rid} [estado declarado: {literal}]")
            out[f"RESULT-C0D-B-{cid}-{brazo}-P"] = pb
            out[f"RESULT-C0D-B-{cid}-{brazo}-ERRPP"] = (
                100.0 * (pb - f["R"]) if (pb is not None and f["R"] is not None) else None)
        obs, _lit_obs = _num_declarado(B.get(f"RESULT-B-ENIGH-{ola}-P"))
        brecha = (100.0 * (obs - f["R"])
                  if (obs is not None and f["R"] is not None) else None)
        out[f"RESULT-C0D-B-{cid}-BRECHA-OBSERVADAS"] = brecha
        if obs is None or f["R"] is None or not f["EE_R"]:
            out[f"RESULT-C0D-B-{cid}-CONMENSURABLE"] = "PISO-NO-CONMENSURABLE"
        else:
            dentro = abs(obs - f["R"]) <= K_CONM * float(f["EE_R"])
            out[f"RESULT-C0D-B-{cid}-CONMENSURABLE"] = (
                "PISO-CONMENSURABLE" if dentro else "PISO-NO-CONMENSURABLE")
    out["RESULT-C0D-B-COBERTURA"] = str(P["piso_B"]["cobertura_sellada"])
    out["RESULT-C0D-B-VEREDICTO"] = "NO-ADJUDICA-POR-N (n=2) · PISO-CITADO-COBERTURA-PARCIAL"

    # --- 6) alcance ------------------------------------------------------
    crudo = inputs["IN-MANIFIESTO"]["bytes"].decode("utf-8")
    posteriores = 0
    for ln in crudo.splitlines():
        s = ln.strip()
        if s.startswith("fecha_descarga:"):
            val = s.split(":", 1)[1].strip().strip('"').strip("'")
            if val > CORTE:
                posteriores += 1
    out["RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES"] = posteriores
    una = _json(inputs, "IN-L-CORPUS-" + orden[0] + "-01")
    out["RESULT-C0D-ALCANCE-CORPUS-CAPTURA"] = (
        "brazo L+corpus: fecha_congelacion="
        + str((una.get("params") or {}).get("fecha_congelacion", "sin-params"))
        + " · ts_ejemplo=" + str(una.get("timestamp"))
        + " · modelo=" + str((una.get("params") or {}).get(
            "modelo_id", una.get("modelo_real", "sin-declarar")))
        + " · corte_alcance=" + CORTE)

    # --- 7) veredicto de la pareada, por la precedencia de §4 -------------
    punto, lo, hi = ic_primaria
    n_LL = len(U_LL)
    if n_LL < N_MIN:
        veredicto = "NO-ESTIMABLE-POR-COBERTURA"
    elif lo > 0:
        veredicto = "CORPUS-ESTORBA"
    elif hi < 0:
        veredicto = "CORPUS-AYUDA"
    else:
        veredicto = "NO-DISCRIMINA"
    out["RESULT-C0D-VEREDICTO-PAREADA"] = veredicto

    # --- 8) adjudicacion del hallazgo, por la precedencia de §5 -----------
    if diverge:
        adj = "NO-ADJUDICA-POR-CONTROL"
    elif veredicto == "NO-ESTIMABLE-POR-COBERTURA":
        adj = "NO-ESTIMABLE-POR-COBERTURA"
    elif (not identicos) and (rank_marginal != rank_comun):
        adj = "EXPLICADO-POR-UNIVERSO"
    elif veredicto == "NO-DISCRIMINA":
        adj = "EXPLICADO-POR-METRICA"
    elif veredicto == "CORPUS-ESTORBA":
        adj = "CONFIRMADO-CON-ALCANCE"
    else:
        adj = "EXPLICADO-POR-METRICA"
    out["RESULT-C0D-ADJUDICACION-HALLAZGO"] = adj
    out["RESULT-C0D-ADJUDICACION-SUCESOR"] = (
        str(P["ramas_adjudicacion_pre_declaradas"]["sucesor_de_5_3"])
        if adj == "CONFIRMADO-CON-ALCANCE" else "NO-APLICA")

    return out
