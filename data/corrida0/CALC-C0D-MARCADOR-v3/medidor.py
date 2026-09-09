"""`CALC-C0D-MARCADOR-v3` — el marcador GEN2, con el mapa de adjudicacion corregido.

Sucede a `CALC-C0D-MARCADOR-v2` (`repite_de`), cuyas cifras son correctas y cuyos
bytes quedan INTACTOS. UNA clase de diferencia y ninguna mas: **a donde va el
veredicto**, no cual es.

Que cambia, y por que (spec sellada `C0D-MARCADOR-spec-v1_2.md` §0.5):
  (a) el VETO DE UNIVERSO desaparece de la adjudicacion -- `v2:378` dejaba que el
      ranking de `M` vetara una pareada `L<->L` en la que `M` no participa;
  (b) `NO-DISCRIMINA` deja de llamarse `EXPLICADO-POR-METRICA` y se llama
      `INCONCLUSO` -- un IC95 que cruza cero no explica nada;
  (c) el `else` mudo de `v2:384` desaparece -- `CORPUS-AYUDA`, que es la
      REFUTACION inequivoca, tiene rama propia (`REFUTADO-CON-ALCANCE`).
Ademas: la guardia §3.5 contrasta `id_celda` e `indice` ademas de `variante`
(`v2` los tomaba del nombre del archivo), el sucesor de alcance se separa del
signo del veredicto (§5.4), el efecto de universo baja a diagnostico (§5-bis),
el mapa se falsa corriendolo (§5-ter) y un control exige que NINGUNA cifra de
`v2` se mueva (§5-quater).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-C0-D-CORRECTIVO`, ANTES DE
CORRER. Spec sellada que lo gobierna:
`forense/prereg-caja/C0D-MARCADOR-spec-v1_2.md` (`prereg-caja-C0D-MARCADOR`).

NO mide ninguna regla y ninguna cifra suya entra a un veredicto (`T9`). No toca
capturas, ni motor, ni `CALC` previos, ni la banda `z` primaria del duelo.

La maquinaria de bootstrap NO se reimplementa: se ejecuta desde los BYTES que
`preflight` ya verifico por sha256 de `forense/prereg-duelo-v2/scoring-adv1-m3.py`
(`origen: repo`), y sus `scope_id` conservan el sufijo `c0d_v1_0` a proposito --
cambiarlos cambiaria la semilla derivada y por tanto las cifras.
"""
from __future__ import annotations

import json
import statistics
import sys
import types

CORREDORES = ("L_SOLO", "L_CORPUS", "M")
_SIN_DESTINO = object()

# §5.3 de la sellada: el mapa es un DICCIONARIO, no una escalera. Sus tres
# claves son exactamente las tres ramas no-guardia de §4. No hay `else`, no hay
# destino por defecto, y una clave ausente levanta excepcion y para la corrida.
MAPA_ADJUDICACION = {
    "CORPUS-ESTORBA": "CONFIRMADO-CON-ALCANCE",
    "CORPUS-AYUDA": "REFUTADO-CON-ALCANCE",
    "NO-DISCRIMINA": "INCONCLUSO",
}
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


def _tabla_l(inputs, n_filas_esperadas):
    """`(id_celda, variante) -> [valores EXTRAIBLE]`, desde `L-extraido-v1_2.tsv`.

    Regla verbatim de `agregado_v1_2._cargar_l_tsv_v1_2`, que es la que CORRE:
    `agregado_v1_2.py` sobreescribe `_leer_l_variante` del modulo base por
    monkeypatch, porque `valor_extraido` es `null` en las 224 capturas crudas
    -- por diseno, y declarado por el propio agregado en
    `hallazgo_declarado.nota_v1_2`. La spec `v1.0` cito la regla del modulo
    BASE y por eso su corrida PARO; `v1.1` escribe la fuente vigente.

    El conteo de filas se ASEVERA, igual que el original: un TSV que no traiga
    224 filas no es el TSV que esta spec congelo."""
    crudo = inputs["IN-L-EXTRAIDO-V1-2"]["bytes"].decode("utf-8")
    lineas = [l for l in crudo.splitlines() if l.strip()]
    cab = lineas[0].split("\t")
    i_cel, i_var = cab.index("id_celda"), cab.index("variante")
    i_idx, i_val, i_est = cab.index("indice"), cab.index("valor"), cab.index("estado")
    tabla, llaves, n_filas = {}, set(), 0
    for ln in lineas[1:]:
        c = ln.split("\t")
        n_filas += 1
        llaves.add((c[i_cel].strip(), c[i_var].strip(), int(c[i_idx])))
        if c[i_est].strip() != "EXTRAIBLE":
            continue
        tabla.setdefault((c[i_cel].strip(), c[i_var].strip()), []).append(float(c[i_val]))
    if n_filas != n_filas_esperadas:
        raise AssertionError(
            f"esperaba {n_filas_esperadas} filas en L-extraido-v1_2.tsv, encontre {n_filas}")
    return tabla, llaves


def _punto_l(tabla, cid, variante):
    """Media de las replicas EXTRAIBLE. Si ninguna lo es, NO-DISPONIBLE --
    no se sustituye por 0 ni por el otro brazo."""
    valores = tabla.get((cid, variante), [])
    if not valores:
        return None, 8, 0
    return statistics.fmean(valores), 8, len(valores)


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


def _adjudica(veredicto, convergencia, correspondencia, posteriores, sucesor):
    """§5 de la sellada `v1.2`: dos guardias de insumo y luego el MAPA.

    Funcion PURA -- no toca `out`, no lee `inputs`, no depende de nada mas que
    de sus cinco argumentos. Es lo que hace que §5-ter pueda falsarla con casos
    sinteticos ajenos al dato observado.

    Devuelve `(adjudicacion, sucesor_de_alcance)`.

    Lo que esta funcion NO hace, y es el defecto que corrige: **no mira el
    universo, ni el ranking de `M`, ni los marginales.** La primaria se deriva
    solo de `L<->L` sobre `U_LL`; ningun diagnostico puede vetarla.
    """
    if str(convergencia).startswith("DIVERGE") or correspondencia != "CORRESPONDE":
        adj = "NO-ADJUDICA-POR-CONTROL"                       # §5.1
    elif veredicto == "NO-ESTIMABLE-POR-COBERTURA":
        adj = "NO-ESTIMABLE-POR-COBERTURA"                    # §5.2
    else:
        adj = MAPA_ADJUDICACION.get(veredicto, _SIN_DESTINO)  # §5.3
        if adj is _SIN_DESTINO:
            raise ValueError(
                f"veredicto sin destino en el mapa de §5.3: {veredicto!r}. "
                f"El mapa es exhaustivo sobre las tres ramas no-guardia de §4 "
                f"({sorted(MAPA_ADJUDICACION)}) y NO tiene destino por defecto: "
                f"una rama nueva se declara en la spec, no se absorbe en un else.")
    # §5.4 -- el sucesor de alcance es MATERIAL, no de signo: depende de si
    # entro corpus despues de la ventana de captura, y de nada mas. `v2` lo
    # ataba a CONFIRMADO-CON-ALCANCE, de modo que solo una confirmacion podia
    # nombrarlo; el corpus que estaba delante del corredor es el mismo
    # cualquiera que sea el signo del intervalo.
    return adj, (sucesor if int(posteriores) > 0 else "NO-APLICA")


def _corre_falsadores(P, sucesor):
    """§5-ter: el mapa es codigo y se falsa corriendolo, no argumentando.

    Casos SINTETICOS y ajenos al dato observado: valen por la estructura del
    `if`, no por lo que salio. A y B son los dos contraejemplos de la revision
    adversarial de `PR #649`."""
    limpio = ("CONVERGE", "CORRESPONDE")
    obtenido = {}

    # A -- primaria concluyente (CORPUS-ESTORBA) con universos distintos y
    #      orden cambiado. `v2` habria dicho EXPLICADO-POR-UNIVERSO: el veto.
    #      Que este medidor no reciba siquiera el ranking es la prueba.
    obtenido["A-VETO-UNIVERSO"] = _adjudica("CORPUS-ESTORBA", *limpio, 0, sucesor)[0]
    # B -- corpus-ayuda inequivoco. `v2` lo habria mandado al `else` mudo.
    obtenido["B-CORPUS-AYUDA"] = _adjudica("CORPUS-AYUDA", *limpio, 0, sucesor)[0]
    # C -- el caso real de este acto.
    obtenido["C-NO-DISCRIMINA"] = _adjudica("NO-DISCRIMINA", *limpio, 0, sucesor)[0]
    # D -- guardia de insumo: precede al mapa aunque la primaria concluya.
    obtenido["D-CONTROL"] = _adjudica(
        "CORPUS-ESTORBA", "DIVERGE:sintetico", "CORRESPONDE", 0, sucesor)[0]
    # E -- guardia de cobertura: precede al mapa.
    obtenido["E-COBERTURA"] = _adjudica(
        "NO-ESTIMABLE-POR-COBERTURA", *limpio, 0, sucesor)[0]
    # F -- exhaustividad: una rama ajena a las cuatro no tiene destino.
    try:
        _adjudica("RAMA-QUE-NO-EXISTE-EN-§4", *limpio, 0, sucesor)
        obtenido["F-EXHAUSTIVO"] = "NO-LEVANTO-EXCEPCION"
    except ValueError:
        obtenido["F-EXHAUSTIVO"] = "LEVANTA-EXCEPCION"
    # G -- el sucesor no depende del signo: corpus-ayuda con posteriores > 0
    #      lo nombra igual que lo nombraria una confirmacion.
    obtenido["G-SUCESOR-SIN-SIGNO"] = _adjudica(
        "CORPUS-AYUDA", *limpio, 1, sucesor)[1]

    esperado = dict(P["falsadores_pre_declarados"])
    fallidos = [f"{k}: esperaba {esperado.get(k)!r}, obtuve {v!r}"
                for k, v in sorted(obtenido.items()) if esperado.get(k) != v]
    if fallidos:
        raise AssertionError(
            "FALSADOR DEL MAPA DE ADJUDICACION EN ROJO -- la corrida PARA, el "
            "mapa no se corrige al vuelo: " + " · ".join(fallidos))
    return obtenido


def _cifras_intactas(out, previos, autorizados):
    """§5-quater: la correccion no puede mover una cifra de `v2`.

    Tolerancia `0.0` -- identidad EXACTA, no aproximacion. Es el control que
    separa «corregi el mapa» de «volvi a medir hasta que saliera otra cosa».
    Los `RESULT` que `v1.2` reescribe o anade por NOMBRE quedan fuera de la
    comparacion; cualquier OTRA diferencia es `MOVIDAS` y para la corrida."""
    movidas = []
    for rid, antes in sorted(previos.items()):
        if rid in autorizados or rid not in out:
            continue
        ahora = out[rid]
        if ahora != antes:
            movidas.append(f"{rid}:{antes!r}->{ahora!r}")
    comunes = sum(1 for r in previos if r not in autorizados and r in out)
    if movidas:
        return ("MOVIDAS:" + ",".join(movidas[:6])
                + (f",+{len(movidas) - 6}" if len(movidas) > 6 else "")), comunes
    return "INTACTAS", comunes


# ── el marcador ───────────────────────────────────────────────────────────

def medir(inputs, contrato):
    P = contrato["parametros"]
    N_MIN = int(P["n_minimo_pareada"])
    K_CONM = float(P["k_umbral_conmensurabilidad"])
    TOL_CONV = float(P["tolerancia_convergencia_L"])
    CORTE = str(P["fecha_corte_alcance"])
    SCOPES = P["scopes_bootstrap"]
    N_FILAS_L = int(P["n_filas_l_tsv"])
    sc = _scoring(inputs)
    out = {}
    tabla_l, llaves_tsv = _tabla_l(inputs, N_FILAS_L)

    # --- 1) puntos por celda ---------------------------------------------
    celdas = _celdas_del_marco(inputs)
    reg = {}
    for c in celdas:
        cid = c["id"]
        r = _json(inputs, f"IN-R-{cid}")
        R = r["R"] if r.get("estado") == "COMPUTADO" else None
        EE = r.get("EE_R") if r.get("estado") == "COMPUTADO" else None
        m = _json(inputs, f"IN-M-{cid}")
        p_solo, _, _ = _punto_l(tabla_l, cid, "L-solo")
        p_corp, _, _ = _punto_l(tabla_l, cid, "L+corpus")
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

    # --- 1-bis) guardia §3.5: el TSV describe capturas que EXISTEN --------
    #
    # `v1.0` leyo un campo que el agregado ya no usa y no lo supo hasta el
    # control. Esta guardia mira el mismo defecto desde el otro lado: que
    # cada fila del TSV tenga su captura y cada captura su fila.
    # `v2` construia la llave como `(cid, variante, k)` con `cid` y `k` sacados
    # del NOMBRE del input, y solo contrastaba `variante` contra el contenido.
    # Una captura cuyo `id_celda` o `indice` internos no coincidieran con su
    # propio nombre de archivo pasaba sin ruido -- y el punto `L` de esa celda
    # se habria formado con replicas de otra. `v1.2` §3.5 contrasta las TRES,
    # leidas del contenido: la identidad la declara el JSON, no el rotulo.
    llaves_captura, discordancias = set(), []
    for cid in orden:
        for tag, variante in (("SOLO", "L-solo"), ("CORPUS", "L+corpus")):
            for k in range(1, 9):
                iid = f"IN-L-{tag}-{cid}-{k:02d}"
                if iid not in inputs:
                    continue
                d = json.loads(inputs[iid]["bytes"].decode("utf-8"))
                declarado = (d.get("id_celda"), d.get("variante"), d.get("indice"))
                esperado = (cid, variante, k)
                for campo, dec, esp in zip(("id_celda", "variante", "indice"),
                                           declarado, esperado):
                    if dec != esp:
                        discordancias.append(f"{iid}:{campo}={dec!r}!={esp!r}")
                llaves_captura.add(declarado if not discordancias else esperado)
    solo_tsv = sorted(llaves_tsv - llaves_captura)
    solo_cap = sorted(llaves_captura - llaves_tsv)
    if discordancias or solo_tsv or solo_cap:
        out["RESULT-C0D-CONTROL-CORRESPONDENCIA"] = (
            "DISCORDA:identidad=" + str(len(discordancias))
            + ",solo_en_tsv=" + str(len(solo_tsv))
            + ",solo_en_capturas=" + str(len(solo_cap))
            + ",ejemplo_identidad=" + (discordancias[0] if discordancias else "-")
            + ",ejemplo_tsv=" + (str(solo_tsv[0]) if solo_tsv else "-")
            + ",ejemplo_captura=" + (str(solo_cap[0]) if solo_cap else "-"))
    else:
        out["RESULT-C0D-CONTROL-CORRESPONDENCIA"] = "CORRESPONDE"

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

    # --- 8) diagnostico de universo -- §5-bis: JAMAS adjudicacion ---------
    #
    # `v2` usaba esto como rama de adjudicacion (`EXPLICADO-POR-UNIVERSO`) y
    # ademas la ponia ANTES de mirar la pareada: el ranking de `M` vetaba una
    # comparacion `L<->L` en la que `M` no participa. Aqui es descriptivo de
    # las tres cifras MARGINALES y no toca la adjudicacion.
    if identicos:
        diag = "UNIVERSOS-IDENTICOS"
    elif rank_marginal == rank_comun:
        diag = "ORDEN-ESTABLE"
    else:
        diag = ("ORDEN-CAMBIA:" + "<".join(rank_marginal)
                + "->" + "<".join(rank_comun))
    out["RESULT-C0D-DIAGNOSTICO-UNIVERSO"] = diag

    # --- 9) adjudicacion del hallazgo -- §5, funcion pura, sin `else` -----
    adj, sucesor = _adjudica(
        veredicto,
        out["RESULT-C0D-CONTROL-CONVERGENCIA-L"],
        out["RESULT-C0D-CONTROL-CORRESPONDENCIA"],
        out["RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES"],
        str(P["sucesor_alcance"]))
    out["RESULT-C0D-ADJUDICACION-HALLAZGO"] = adj
    out["RESULT-C0D-ADJUDICACION-SUCESOR"] = sucesor

    # --- 10) §5-ter: los falsadores del mapa, EJECUTADOS ------------------
    for etiqueta, valor in _corre_falsadores(P, str(P["sucesor_alcance"])).items():
        out[f"RESULT-C0D-FALSADOR-{etiqueta}"] = valor

    # --- 11) §5-quater: ninguna cifra de `v2` se mueve --------------------
    previos = _json(inputs, "IN-V2-RESULTADOS")["resultados"]
    estado, n_comparados = _cifras_intactas(
        out, previos, set(P["result_autorizados_a_diferir"]))
    out["RESULT-C0D-CONTROL-CIFRAS-INTACTAS"] = estado
    out["RESULT-C0D-CONTROL-N-CIFRAS-COMPARADAS"] = n_comparados
    if estado != "INTACTAS":
        raise AssertionError(
            "CIFRAS-INTACTAS EN ROJO -- esta correccion solo puede cambiar el "
            "DESTINO del veredicto, nunca una cifra. La corrida PARA: " + estado)

    return out
