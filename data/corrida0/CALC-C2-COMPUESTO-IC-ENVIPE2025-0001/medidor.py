#!/usr/bin/env python3
"""Medidor de `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` (`COMMIT-2`).

ACTO `GEN2-GUARDIAN-ENVIPE-EJES-IC-1` (20/sep/2026). Contrato humano:
`forense/prereg-caja/C2-COMPUESTO-IC-ENVIPE2025-spec-v1_0.md`, congelado en
`COMMIT-1` junto con este archivo y con la extensión del guardián, ANTES de
abrir microdato. Firma de mesa (20/sep/2026): «2 si extendemos».

Interfaz estable del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> dict`.
El medidor no abre `spec.yaml`: recibe el contrato normalizado.

QUÉ ABRE, Y QUÉ NO
------------------
  · **ENVIPE 2025, SÓLO marginales de UN EJE** -- los cinco ejes del
    guardián extendido (`escolaridad_proxy`, `dominio_urbano_rural`,
    `nacional`, `sexo`, `edad`), cada uno por UNA llamada a `marginal()`,
    sobre UNA `replicas_compartidas` de la ola. Ningún otro payload.
  · **Cero cruces.** `cruce()` NO se llama (ni para probar la guardia: eso
    lo hace `tests/test_marginales_una_variable.py` con zips fabricados).
    La ola se carga `reservada=True`.

QUÉ EMITE
---------
  · Por cada una de las 38 celdas de los 4 pares del dictamen
    (`c2-compuesto-dictamen-v1_0.tsv`, ENVIPE 2025): PUNTO (= C2 sobre los
    marginales SELLADOS del árbitro, por `piso_log_aditivo` importada),
    IC95 por percentiles 2.5/97.5 de `C2_k = expit(logit p_k(a) + logit
    p_k(b) - logit p_k)` réplica a réplica, y RÉPLICAS-VÁLIDAS.
  · Dos controles de coherencia, los dos o el IC no se publica:
      (A) el punto reproduce el sellado en `CALC-C2-COMPUESTO-RESERVADAS-0001`
          (|Δ| <= umbral_control_punto);
      (B) los marginales de la réplica base (la muestra entera, punto e IC
          del árbitro por `wprop_ic_conglomerado`) reproducen los R sellados
          en `milpa/tramite-ola5-propuesta-v0.yaml` para los CINCO ejes,
          por `cotejo()` con las tolerancias del piloto 2.
    Si A o B falla, IC95INF/IC95SUP salen `null` en las 38 celdas y
    `…-G-IC-PUBLICADO` = "NO", con los deltas con signo a la vista. Nunca
    se ajusta nada.

`p_k ∈ {0, 1}` en cualquiera de los tres marginales de una réplica: la
réplica queda SIN-DEFINIR (descartada, contada); el IC sale de las válidas;
0 válidas -> IC `null`. Sin recorte, sin sustitución.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


mr = _importa("marginales_reproduccion",
              RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
_c2 = _importa("test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
piso_log_aditivo = _c2.piso_log_aditivo
MarginalDegenerado = _c2.MarginalDegenerado

P = "RESULT-C2IC25"
DESENLACE_ID = "evade_norma::BP1_20==2 AND BP1_23 in {04,05,06,08}"
ROTULO_SUPUESTO = "ausencia de interaccion en escala logit"
PREFIJO_SELLADO = "RESULT-C2COMP-"
OLA_TSV = "ENVIPE 2025"


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _marg(p):
    return {"desenlace_id": DESENLACE_ID, "p": float(p)}


def lee_tsv(ruta):
    """Lector propio: el módulo `csv` despoja comillas en los TSV de este
    proyecto. Líneas `#` fuera; cabecera = primera línea restante."""
    filas = []
    cab = None
    for linea in Path(ruta).read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.startswith("#"):
            continue
        campos = linea.split("\t")
        if cab is None:
            cab = campos
            continue
        filas.append(dict(zip(cab, campos)))
    return filas


def parte_par(par, ejes):
    """`escolaridad_proxyxsexo` -> (escolaridad_proxy, sexo): se parte por
    nombres de eje conocidos, nunca por la letra `x` (proxy la contiene)."""
    for a in ejes:
        if par.startswith(a + "x") and par[len(a) + 1:] in ejes:
            return a, par[len(a) + 1:]
    raise ValueError(f"par {par!r} no se parte en dos ejes de {ejes}")


def celdas_del_dictamen(ruta_emisiones, ejes):
    """Las 38 celdas de ENVIPE 2025 de `c2-compuesto-emisiones-v1_0.tsv`,
    en su orden, con su id sellado y sus dos celdas por nombre."""
    out = []
    for f in lee_tsv(ruta_emisiones):
        if f["ola"] != OLA_TSV:
            continue
        a, b = parte_par(f["par"], ejes)
        out.append({"rid": f["resultado_id"], "par": f["par"],
                    "eje_a": a, "eje_b": b,
                    "celda_a": f["celda_a"], "celda_b": f["celda_b"]})
    return out


def medir(inputs, contrato):
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    ola_reservada = int(par["ola_reservada"])
    tol_p, tol_ic = float(par["control_arbitro_tol_p"]), float(par["control_arbitro_tol_ic"])
    umbral_punto = float(par["umbral_control_punto"])
    ejes = tuple(par["ejes"])
    sell = par["marginales_sellados"]           # {eje: {celda: {p, ic95, n}}}
    out = {}

    out[f"{P}-G-INPUT-ENVIPE2025-CSV-SHA256"] = str(inputs["envipe2025_csv"]["sha256"])
    out[f"{P}-G-INPUT-C2-SELLADO-SHA256"] = str(inputs["IN-C2-SELLADO"]["sha256"])
    out[f"{P}-G-INPUT-C2-EMISIONES-SHA256"] = str(inputs["IN-C2-EMISIONES"]["sha256"])
    out[f"{P}-G-INPUT-ARBITRO-SHA256"] = str(inputs["IN-ARBITRO-MARGINALES"]["sha256"])

    # ── las celdas y los puntos sellados, del árbol ────────────────────────
    celdas = celdas_del_dictamen(inputs["IN-C2-EMISIONES"]["ruta_absoluta"], ejes)
    import json
    sellado = json.loads(Path(inputs["IN-C2-SELLADO"]["ruta_absoluta"])
                         .read_text(encoding="utf-8"))["resultados"]
    out[f"{P}-G-N-CELDAS-DICTAMEN"] = len(celdas)
    out[f"{P}-G-N-PARES-DICTAMEN"] = len({c["par"] for c in celdas})
    if len(celdas) != int(par["n_celdas_esperadas"]):
        raise mr.Paro(f"dictamen: {len(celdas)} celdas de ENVIPE 2025, la spec "
                      f"esperaba {par['n_celdas_esperadas']}")
    pares_vetados = {frozenset(p) for p in par["pares_vetados"]}
    for c in celdas:
        if frozenset({c["eje_a"], c["eje_b"]}) in pares_vetados:
            raise mr.Paro(f"el dictamen trae un par vetado: {c['par']}")

    # ── 2025 · RESERVADA · una ola, unas réplicas, cinco marginales ────────
    ola = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"], ola_reservada,
                       reservada=True)
    if not ola.reservada:                                    # pragma: no cover
        raise mr.ReservaRota("la ola tiene que cargarse reservada")
    rep = mr.replicas_compartidas(ola, semilla, n_rep)
    m = ola.meta
    out[f"{P}-G-RESERVA-OLA"] = str(ola_reservada)
    out[f"{P}-G-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-FILAS-BP1_20-FUERA"] = int(m["filas_bp1_20_fuera"])
    out[f"{P}-G-DELITOS-SIN-PERSONA"] = int(m["delitos_sin_persona"])
    out[f"{P}-G-ESCOLARIDAD-FUERA"] = int(m["escolaridad_fuera"])
    out[f"{P}-G-DOMINIO-FUERA"] = int(m["dominio_fuera"])
    out[f"{P}-G-SEXO-FUERA"] = int(m["sexo_fuera"])
    out[f"{P}-G-EDAD-FUERA"] = int(m["edad_fuera"])
    out[f"{P}-G-NUMERADOR"] = int(m["numerador"])
    out[f"{P}-G-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-UPM"] = int(m["upm"])
    out[f"{P}-G-ESTRATOS-UPM-UNICA"] = int(rep.estratos_upm_unica)
    out[f"{P}-G-ENCODING-TMODVIC"] = str(m["encoding_tmod_vic"])
    out[f"{P}-G-REPLICAS"] = int(rep.n_rep)
    out[f"{P}-G-SEED"] = int(rep.seed)

    marg = {}
    for eje in ejes:
        marg[eje] = mr.marginal(ola, eje, replicas=rep)      # UNA variable
        out[f"{P}-G-COBERTURA-{eje.upper()}"] = float(marg[eje]["cobertura"])
        out[f"{P}-G-FUERA-{eje.upper()}"] = int(marg[eje]["n_fuera"])

    # ── control B · la réplica base reproduce al árbitro, cinco ejes ──────
    peor_p, peor_ic, veredictos = 0.0, 0.0, []
    for eje in ejes:
        ct = mr.cotejo(marg[eje], sell[eje], tol_p, tol_ic)
        veredictos.append(ct["veredicto"])
        out[f"{P}-CTRL-ARBITRO-{eje.upper()}-VEREDICTO"] = ct["veredicto"]
        out[f"{P}-CTRL-ARBITRO-{eje.upper()}-DELTA-P-MAX"] = float(ct["delta_p_max"])
        out[f"{P}-CTRL-ARBITRO-{eje.upper()}-DELTA-IC-MAX"] = float(ct["delta_ic_max"])
        for k, fila in ct["filas"].items():
            rot = _rot(k)
            out[f"{P}-CTRL-ARBITRO-{eje.upper()}-{rot}-DELTA-P"] = fila.get("delta_p")
            out[f"{P}-CTRL-ARBITRO-{eje.upper()}-{rot}-DELTA-N"] = fila.get("delta_n")
        peor_p = max(peor_p, ct["delta_p_max"])
        peor_ic = max(peor_ic, ct["delta_ic_max"])
    out[f"{P}-CTRL-ARBITRO-DELTA-P-MAX"] = float(peor_p)
    out[f"{P}-CTRL-ARBITRO-DELTA-IC-MAX"] = float(peor_ic)
    ctrl_b = "REPRODUCE" if all(v == "REPRODUCE" for v in veredictos) else "NO-REPRODUCE"
    out[f"{P}-CTRL-ARBITRO-VEREDICTO"] = ctrl_b

    # ── por celda: punto (sellados), control A, IC por réplicas ───────────
    peor_punto, sin_def_total, no_constr = 0.0, 0, 0
    ics = {}
    for c in celdas:
        suf = c["rid"][len(PREFIJO_SELLADO):]
        pa, pb, pn = (sell[c["eje_a"]][c["celda_a"]]["p"],
                      sell[c["eje_b"]][c["celda_b"]]["p"],
                      sell["nacional"]["NAC"]["p"])
        try:
            punto = float(piso_log_aditivo(_marg(pa), _marg(pb), _marg(pn))["p"])
        except MarginalDegenerado:
            punto, no_constr = None, no_constr + 1
        out[f"{P}-P-{suf}"] = punto
        s = sellado.get(c["rid"])
        d = (punto - float(s)) if (punto is not None and s is not None) else None
        out[f"{P}-CTRL-PUNTO-DELTA-{suf}"] = d
        if d is None:
            peor_punto = float("inf")
        else:
            peor_punto = max(peor_punto, abs(d))

        ca, cb, cn = (marg[c["eje_a"]]["celdas"][c["celda_a"]],
                      marg[c["eje_b"]]["celdas"][c["celda_b"]],
                      marg["nacional"]["celdas"]["NAC"])
        try:
            out[f"{P}-P-REDERIVADO-{suf}"] = float(piso_log_aditivo(
                _marg(ca["p"]), _marg(cb["p"]), _marg(cn["p"]))["p"])
        except (MarginalDegenerado, TypeError):
            out[f"{P}-P-REDERIVADO-{suf}"] = None
        ra, rb, rn = ca["replicas"], cb["replicas"], cn["replicas"]
        ok = (np.isfinite(ra) & np.isfinite(rb) & np.isfinite(rn)
              & (ra > 0) & (ra < 1) & (rb > 0) & (rb < 1) & (rn > 0) & (rn < 1))
        sin_def = int((~ok).sum())
        sin_def_total += sin_def
        with np.errstate(all="ignore"):
            z = (np.log(ra / (1 - ra)) + np.log(rb / (1 - rb))
                 - np.log(rn / (1 - rn)))
        c2r = 1.0 / (1.0 + np.exp(-z[ok]))
        out[f"{P}-REPLICAS-VALIDAS-{suf}"] = int(ok.sum())
        out[f"{P}-REPLICAS-SIN-DEFINIR-{suf}"] = sin_def
        ics[suf] = (_pct(c2r, 2.5), _pct(c2r, 97.5))

    out[f"{P}-CTRL-PUNTO-DELTA-MAX-ABS"] = (None if peor_punto == float("inf")
                                            else float(peor_punto))
    ctrl_a = ("REPRODUCE" if peor_punto <= umbral_punto else "NO-REPRODUCE")
    out[f"{P}-CTRL-PUNTO-VEREDICTO"] = ctrl_a
    out[f"{P}-CTRL-PUNTO-N-CELDAS"] = len(celdas)

    publica = ctrl_a == "REPRODUCE" and ctrl_b == "REPRODUCE"
    n_con_ic = 0
    for suf, (lo, hi) in ics.items():
        if publica and lo is not None:
            out[f"{P}-IC95INF-{suf}"], out[f"{P}-IC95SUP-{suf}"] = lo, hi
            n_con_ic += 1
        else:
            out[f"{P}-IC95INF-{suf}"], out[f"{P}-IC95SUP-{suf}"] = None, None
    out[f"{P}-G-IC-PUBLICADO"] = "SI" if publica else "NO"
    out[f"{P}-G-N-CELDAS-CON-IC"] = int(n_con_ic)
    out[f"{P}-G-N-CELDAS-SIN-IC"] = int(len(celdas) - n_con_ic)
    out[f"{P}-G-C2-CELDAS-NO-CONSTRUIBLES"] = int(no_constr)
    out[f"{P}-G-REPLICAS-SIN-DEFINIR-TOTAL"] = int(sin_def_total)
    out[f"{P}-G-C2-DESENLACE-ID"] = DESENLACE_ID
    out[f"{P}-G-C2-ROTULO-SUPUESTO"] = ROTULO_SUPUESTO
    out[f"{P}-G-C2-FORMA"] = "expit(logit p25(a) + logit p25(b) - logit p25)"
    out[f"{P}-G-INCERTIDUMBRE"] = (
        "IC95 percentil 2.5/97.5 de replicas bootstrap de conglomerado "
        "estratificado, UN remuestreo de la ola compartido por los cinco "
        "marginales; mide ruido muestral del estimador log-aditivo, no el error "
        "del supuesto de no-interaccion")
    out[f"{P}-G-CRUCE-2025-DERIVADO"] = "NO"
    return out


def _rot(celda):
    """`1 Hombre` -> `1-HOMBRE`, `60+` -> `60`, `hasta primaria` -> `HASTA-PRIMARIA`:
    la misma normalización que los ids sellados de RESERVADAS-0001."""
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", celda).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").upper()
    return s
