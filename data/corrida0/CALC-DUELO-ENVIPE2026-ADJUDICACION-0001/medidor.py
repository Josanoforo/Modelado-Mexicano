#!/usr/bin/env python3
"""Cableado ENVIPE del duelo prospectivo: emisiones (COMMIT-2) y
adjudicación (COMMIT-3), parametrizados por ola.

ACTO `GEN2-DUELO-ENVIPE2026-COMMIT-1` (21/sep/2026). Contrato humano:
`forense/prereg-caja/DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md`. Diseño de
MOTOR v1.0 + enmienda v1.1 (F7 A/B/C, D-22 ampliada), archivados en
`forense/prereg-caja/DISENO-duelo-prospectivo-ENVIPE2026-*.md`.

Aquí vive TODO lo que sabe de ENVIPE: qué zip es qué ola, qué ejes hay, qué
rótulos de celda, qué está sellado. Lo genérico está fuera:
  · `tools/duelo/cruces_familia.py`      — familia C2/P/S1/Sλ/AP + regla v0.3
  · `tools/duelo/tendencia_nacional.py`  — K/T3/T5/TC, E+, origen móvil
  · `tools/celda_d/marginales_reproduccion.py` (ajeno, congelado) — el ÚNICO
    código que abre una ola de ENVIPE: guardia de UNA variable de agrupación,
    `cruce()` lanza `ReservaRota` sobre la ola reservada y sobre los pares
    vetados por nombre.
  · `data/corrida0/CALC-ENVIPE-SERIE-2022/medidor.py` (sellado) — el
    estimador de `p_c1_u1` (delito personal no denunciado), reutilizado para
    el R nacional de ese estimando en la ola nueva; reproduce la fila 2025 de
    la serie sellada a 1e-12 (comprobado antes de congelar).

Interfaz estable `medir(inputs, contrato) -> {"RESULT-…": valor}`;
`parametros.punto_de_entrada` ∈ {emisiones, adjudicacion, origen_movil}
elige la pieza. Este archivo se deposita BYTE A BYTE como `medidor.py` en
cada CALC del duelo (E.5: el sello cubre el código que mide; un test exige
la identidad byte a byte con `tools/duelo/envipe_duelo.py`), y el sha256 de
los módulos genéricos que importa se emite como RESULT en cada corrida. Los parámetros llegan por
`contrato["parametros"]`; nada de ENVIPE 2026 está cableado: `ola_nueva` es
un parámetro, y el mismo código corre «como si 2025 fuera la ola nueva»
(ensayo P3, D-22 ampliada).

QUÉ EMITE Y QUÉ NO, en emisiones (la ola nueva se carga `reservada=True`)
--------------------------------------------------------------------------
  · C2 por celda (punto e IC) — autorizado por el diseño (§2: «marginales de
    la misma ola»). NO emite los marginales crudos, el nacional ni el
    numerador de la ola nueva: eso es R y sale en COMMIT-3. Sólo conteos que
    no revelan el estimando (filas de archivo, universo, estratos, UPM).
  · K, T3, T5, TC nacionales por estimando, con IC — ciegos a la ola nueva
    por construcción (leen la serie sellada y las olas anteriores).
  · E+ por eje y variante para `evade_norma` (la guardia sólo mide ese
    desenlace; para `no-denunciado` no hay marginal por eje sellado → E+
    NO-CONSTRUIBLE, dicho).
  · La guardia se PRUEBA en cada corrida: `cruce()` sobre la ola nueva y el
    par vetado de 2025 tienen que lanzar `ReservaRota`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import math
import sys
import zipfile
from pathlib import Path

import numpy as np



def _raiz() -> Path:
    """Este archivo vive en `tools/duelo/` Y, byte a byte, como `medidor.py`
    dentro de cada CALC (E.5: el sello cubre el código que mide, no un shim).
    La raíz del repo se busca hacia arriba por `tools/corrida0.py`."""
    p = Path(__file__).resolve()
    for d in p.parents:
        if (d / "tools" / "corrida0.py").exists():
            return d
    raise RuntimeError("raíz del repo no encontrada desde " + str(p))


RAIZ = _raiz()


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


mr = _importa("marginales_reproduccion",
              RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
cf = _importa("cruces_familia", RAIZ / "tools" / "duelo" / "cruces_familia.py")
tn = _importa("tendencia_nacional", RAIZ / "tools" / "duelo" / "tendencia_nacional.py")

MODULOS_SHA = {
    "CRUCES-FAMILIA": RAIZ / "tools" / "duelo" / "cruces_familia.py",
    "TENDENCIA-NACIONAL": RAIZ / "tools" / "duelo" / "tendencia_nacional.py",
    "ENVIPE-DUELO": RAIZ / "tools" / "duelo" / "envipe_duelo.py",
    "MARGINALES-REPRODUCCION": RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py",
    "SERIE-COMPLETA-MEDIDOR": RAIZ / "data" / "corrida0" / "CALC-ENVIPE-SERIE-2022" / "medidor.py",
}

ESTIMANDOS = ("ND", "EN")          # ND = delito personal no denunciado (p_c1_u1)
ROT_ESTIMANDO = {"ND": "DELITO-PERSONAL-NO-DENUNCIADO (p_c1_u1, serie sellada)",
                 "EN": "evade_norma (BP1_20==2 AND BP1_23 in {04,05,06,08})"}
NACIONALES = tuple(tn.CONTENDIENTES)
VARIANTES_EMAS = ("T3", "T5", "TC")

# Ejes de la guardia y rótulos cortos de celda (los del piloto 2 y del
# guardián extendido: S/D/E/H-M).
EJE_CODIGO = {
    "escolaridad_proxy": ("S", list(mr.ORD_ESC)),
    "dominio_urbano_rural": ("D", list(mr.ORD_DOMINIO)),
    "edad": ("E", list(mr.ORD_EDAD)),
    "sexo": ("X", list(mr.ORD_SEXO)),
}
EJES_EMAS = ("escolaridad_proxy", "dominio_urbano_rural", "sexo", "edad")
PARES = {"SXD": ("escolaridad_proxy", "dominio_urbano_rural"),
         "EXD": ("edad", "dominio_urbano_rural")}
CANDIDATOS_CRUCE = tuple(cf.CANDIDATOS)


def _codigo_celda(eje, categoria):
    letra, orden = EJE_CODIGO[eje]
    if letra == "X":
        return {"1 Hombre": "H", "2 Mujer": "M"}[categoria]
    return f"{letra}{orden.index(categoria) + 1}"


def codigos_par(par: str) -> list[tuple]:
    """[(codigo_celda, (cat_a, cat_b))] en el orden del guardián."""
    ea, eb = PARES[par]
    return [(f"{_codigo_celda(ea, a)}x{_codigo_celda(eb, b)}", (a, b))
            for a in EJE_CODIGO[ea][1] for b in EJE_CODIGO[eb][1]]


def grupos_eje(eje: str) -> list[tuple]:
    return [(_codigo_celda(eje, c), c) for c in EJE_CODIGO[eje][1]]


def _sha(ruta: Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def _f(v):
    return None if v is None else float(v)


def _txt(v):
    return "NO-CONSTRUIBLE" if v is None else str(v)


# ══ serie sellada (TSV) → puntos ══════════════════════════════════════════

def lee_serie_tsv(crudo: bytes) -> list[dict]:
    """El TSV sellado, leído a mano (el módulo csv despoja comillas en este
    repo). Devuelve filas dict con las columnas del archivo."""
    texto = crudo.decode("utf-8").lstrip("﻿")
    lineas = [l for l in texto.replace("\r\n", "\n").split("\n") if l.strip()]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def serie_nd(filas: list[dict], comparabilidad_homogenea: str) -> list[tn.Punto]:
    """Puntos de `p_c1_u1` por `ola_encuesta`; comparable sólo si la columna
    `comparabilidad` trae el valor homogéneo declarado en la spec."""
    return [tn.Punto(ola=int(f["ola_encuesta"]), p=float(f["p_c1_u1"]),
                     lo=float(f["ic95_boot_lo"]), hi=float(f["ic95_boot_hi"]),
                     comparable=(f["comparabilidad"] == comparabilidad_homogenea))
            for f in filas]


# ══ olas de ENVIPE por la guardia ═════════════════════════════════════════

def _celda(c: dict) -> cf.Celda:
    return cf.Celda(p=_f(c["p"]), ic95=None if c["ic95"] is None else tuple(c["ic95"]),
                    replicas=c.get("replicas"), n=int(c["n"]))


class OlaCargada:
    """Una ola abierta por la guardia con sus réplicas compartidas y sus
    marginales de UN eje por llamada."""

    def __init__(self, zip_path, anio, reservada, seed, n_rep):
        self.anio = int(anio)
        self.ola = mr.carga_ola(zip_path, self.anio, reservada=reservada)
        self.rep = mr.replicas_compartidas(self.ola, seed, n_rep)
        self._marg = {}
        self._cruce = {}

    def marginal(self, eje: str) -> dict:
        if eje not in self._marg:
            m = mr.marginal(self.ola, eje, replicas=self.rep)
            self._marg[eje] = {k: _celda(v) for k, v in m["celdas"].items()}
        return self._marg[eje]

    def nacional(self) -> cf.Celda:
        return self.marginal("nacional")["NAC"]

    def marginales_par(self, par: str) -> cf.Marginales:
        ea, eb = PARES[par]
        return cf.Marginales(a=self.marginal(ea), b=self.marginal(eb),
                             nac=self.nacional(), orden_a=tuple(EJE_CODIGO[ea][1]),
                             orden_b=tuple(EJE_CODIGO[eb][1]))

    def cruce(self, par: str) -> dict:
        """Lanza `ReservaRota` si la ola está reservada o el par está vetado."""
        if par not in self._cruce:
            ea, eb = PARES[par]
            x = mr.cruce(self.ola, ea, eb, replicas=self.rep)
            self._cruce[par] = {k: _celda(v) for k, v in x["celdas"].items()}
        return self._cruce[par]

    def ola_anterior(self, par: str) -> cf.OlaAnterior:
        return cf.OlaAnterior(rotulo=str(self.anio), cruce=self.cruce(par),
                              marginales=self.marginales_par(par))


def _emite_conteos(out, P, w, oc: OlaCargada):
    m = oc.ola.meta
    out[f"{P}-G-{w}-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-{w}-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-{w}-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-{w}-UPM"] = int(m["upm"])
    out[f"{P}-G-{w}-ESTRATOS-UPM-UNICA"] = int(oc.rep.estratos_upm_unica)
    out[f"{P}-G-{w}-ENCODING-TMODVIC"] = str(m["encoding_tmod_vic"])
    out[f"{P}-G-{w}-DELITOS-SIN-PERSONA"] = int(m["delitos_sin_persona"])


def _emite_celda(out, base, c: cf.Celda, con_n=False):
    out[f"{base}-P"] = _f(c.p)
    ic = cf.ic95_de(c)
    out[f"{base}-IC95INF"] = None if ic is None else ic[0]
    out[f"{base}-IC95SUP"] = None if ic is None else ic[1]
    if con_n:
        out[f"{base}-N"] = None if c.n is None else int(c.n)


def _emite_pred(out, base, pr: tn.Prediccion):
    out[f"{base}-P"] = _f(pr.p)
    out[f"{base}-IC95INF"] = None if pr.ic95 is None else float(pr.ic95[0])
    out[f"{base}-IC95SUP"] = None if pr.ic95 is None else float(pr.ic95[1])
    out[f"{base}-ESTADO"] = pr.estado
    out[f"{base}-OLAS-USADAS"] = ",".join(str(o) for o in pr.olas_usadas) or "NINGUNA"
    out[f"{base}-PENDIENTE-LOGIT"] = _f(pr.pendiente_logit)


def _sin_definir(celdas: dict) -> int:
    return int(sum(0 if c.replicas is None else int((~np.isfinite(c.replicas)).sum())
                   for c in celdas.values()))


# ══ piezas compartidas por emisiones y adjudicación ═══════════════════════

def _carga_olas(inputs, par, seed, n_rep, reservada_nueva: bool) -> dict:
    """Abre las olas que el contrato nombra: `olas_zip` = {anio: input_id}.
    La ola nueva se carga con `reservada_nueva`; las demás abiertas."""
    olas = {}
    for anio, iid in sorted(par["olas_zip"].items()):
        anio = int(anio)
        olas[anio] = OlaCargada(inputs[iid]["ruta_absoluta"], anio,
                                reservada=(reservada_nueva and anio == int(par["ola_nueva"])),
                                seed=seed, n_rep=n_rep)
    return olas


def _serie_en(olas: dict, sellados: dict, tol: float, out, P) -> list[tn.Punto]:
    """Puntos nacionales de `evade_norma` por ola, re-derivados por la
    guardia (con IC) y cotejados contra el sellado del contrato."""
    puntos = []
    for anio in sorted(int(a) for a in sellados):
        oc = olas[anio]
        nac = oc.nacional()
        s = sellados[str(anio)] if str(anio) in sellados else sellados[anio]
        d = float(nac.p) - float(s["p"])
        out[f"{P}-NAC-EN-SERIE-{anio}-P"] = float(nac.p)
        out[f"{P}-NAC-EN-SERIE-{anio}-IC95INF"] = float(nac.ic95[0])
        out[f"{P}-NAC-EN-SERIE-{anio}-IC95SUP"] = float(nac.ic95[1])
        out[f"{P}-NAC-EN-SERIE-{anio}-DELTA-SELLADO"] = d
        out[f"{P}-NAC-EN-SERIE-{anio}-REPRODUCE"] = "SI" if abs(d) <= tol else "NO"
        puntos.append(tn.Punto(ola=anio, p=float(nac.p), lo=float(nac.ic95[0]),
                               hi=float(nac.ic95[1]), comparable=True))
    return puntos


def _familias(olas: dict, par_contrato: dict, ola_nueva: int) -> dict:
    """{par: salida de cf.familia} con las olas anteriores del contrato."""
    fam = {}
    m_t = {p: olas[ola_nueva].marginales_par(p) for p in PARES}
    for p, anteriores in par_contrato["olas_anteriores_por_par"].items():
        ants = [olas[int(a)].ola_anterior(p) for a in anteriores]
        fam[p] = cf.familia(m_t[p], ants)
    return fam


def _emite_familia(out, P, par, fam):
    meta = fam["meta"]
    lam = meta["lambda"]
    out[f"{P}-{par}-OLAS-ANTERIORES"] = ",".join(meta["olas_anteriores"])
    out[f"{P}-{par}-OLA-PERSISTENCIA"] = str(meta["ola_persistencia"])
    out[f"{P}-{par}-LAMBDA"] = _f(lam["lambda"])
    out[f"{P}-{par}-TAU2"] = _f(lam["tau2"])
    out[f"{P}-{par}-SIGMA2-MEDIO"] = _f(lam["sigma2_medio"])
    out[f"{P}-{par}-VAR-ENTRE"] = _f(lam["var_entre"])
    out[f"{P}-{par}-K-CELDAS-LAMBDA"] = int(lam["k"])
    for cid in CANDIDATOS_CRUCE:
        celdas = fam["candidatos"][cid]
        out[f"{P}-{par}-{cid}-REPLICAS-SIN-DEFINIR"] = _sin_definir(celdas)
        for cod, key in codigos_par(par):
            _emite_celda(out, f"{P}-{par}-{cid}-{cod}", celdas[key])
    for cod, key in codigos_par(par):
        punto, _ = meta["interaccion_media"][key]
        out[f"{P}-{par}-IBAR-{cod}"] = _f(punto)


def _n_por_ola_anteriores(fam_meta_olas, olas, par):
    """n por celda en cada ola anterior (soporte histórico)."""
    return {str(a): {k: c.n for k, c in olas[int(a)].cruce(par).items()}
            for a in fam_meta_olas}


# ══ COMMIT-2 · emisiones ══════════════════════════════════════════════════

def emisiones(inputs, contrato) -> dict:
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    ola_nueva = int(par["ola_nueva"])
    seed = int(contrato["seed"]["valor"])
    n_rep = int(par["bootstrap_replicas"])
    umbral = int(par["umbral_soporte_n"])
    out = {}

    for iid in inputs:
        out[f"{P}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid]["sha256"])
    for k, ruta in MODULOS_SHA.items():
        out[f"{P}-G-CODIGO-{k}-SHA256"] = _sha(ruta)
    out[f"{P}-G-OLA-NUEVA"] = str(ola_nueva)
    out[f"{P}-G-ROTULO-NIVEL-NACIONAL"] = "PROSPECTIVO-MECANICO (ciego a la ola nueva por construccion)"

    # ── nacional · ND desde la serie sellada ─────────────────────────────
    filas = lee_serie_tsv(inputs[par["serie_nd_input"]]["bytes"])
    s_nd = serie_nd(filas, par["comparabilidad_homogenea"])
    out[f"{P}-G-ND-OLAS-EN-SERIE"] = len(s_nd)
    out[f"{P}-G-ND-OLAS-NO-COMPARABLES"] = ",".join(str(q.ola) for q in s_nd if not q.comparable) or "NINGUNA"
    for cid in NACIONALES:
        _emite_pred(out, f"{P}-NAC-ND-{cid}", tn.predice(s_nd, ola_nueva, cid))

    # ── olas abiertas por la guardia (la nueva, reservada) ───────────────
    olas = _carga_olas(inputs, par, seed, n_rep, reservada_nueva=True)
    for anio, oc in olas.items():
        _emite_conteos(out, P, f"W{anio}", oc)
    nueva = olas[ola_nueva]
    out[f"{P}-G-RESERVA-OLA-CARGADA-RESERVADA"] = "SI" if nueva.ola.reservada else "NO -- DEFECTO"
    try:
        nueva.cruce("SXD")
        out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"] = "SI -- DEFECTO"
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = "NO-LANZO -- DEFECTO"
    except mr.ReservaRota as exc:
        out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"] = "NO"
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = f"ReservaRota: {exc}"
    veto = par.get("par_vetado_probar")          # p.ej. {"anio": 2025, "par": "EXD"}
    if veto:
        try:
            olas[int(veto["anio"])].cruce(veto["par"])
            out[f"{P}-G-VETO-{veto['par']}-{veto['anio']}-PROBADO"] = "NO-LANZO -- DEFECTO"
        except mr.ReservaRota as exc:
            out[f"{P}-G-VETO-{veto['par']}-{veto['anio']}-PROBADO"] = f"ReservaRota: {exc}"

    # ── nacional · EN desde las olas anteriores (control contra sellado) ─
    s_en = _serie_en(olas, par["en_nacional_sellado"], float(par["control_tol_p"]), out, P)
    for cid in NACIONALES:
        _emite_pred(out, f"{P}-NAC-EN-{cid}", tn.predice(s_en, ola_nueva, cid))
    k_en = tn.predice(s_en, ola_nueva, "K")
    cte = float(par["constante_motor_evade_norma"])
    out[f"{P}-G-EN-K-DELTA-CONSTANTE-MOTOR"] = None if k_en.p is None else float(k_en.p) - cte
    out[f"{P}-G-EN-K-COINCIDE-CONSTANTE-MOTOR"] = (
        "NO-CONSTRUIBLE" if k_en.p is None
        else ("SI" if abs(k_en.p - cte) <= float(par["constante_motor_tol"]) else "NO"))

    # ── E+ por eje y variante (EN) ────────────────────────────────────────
    prev = olas[int(par["ola_anterior_emas"])]
    rng = np.random.Generator(np.random.PCG64(seed))
    out[f"{P}-G-EMAS-ND-ESTADO"] = ("NO-CONSTRUIBLE -- no hay marginal por eje "
                                    "sellado del estimando no-denunciado; la guardia "
                                    "mide un solo desenlace (evade_norma)")
    for eje in EJES_EMAS:
        marg = prev.marginal(eje)
        nac = prev.nacional()
        for cod, cat in grupos_eje(eje):
            _emite_celda(out, f"{P}-PERS-{cod}", marg[cat], con_n=True)
            for var in VARIANTES_EMAS:
                t_star = tn.predice(s_en, ola_nueva, var)
                base = f"{P}-EMAS-{var}-{cod}"
                if t_star.p is None or marg[cat].p is None:
                    out[f"{base}-P"] = None
                    out[f"{base}-IC95INF"] = None
                    out[f"{base}-IC95SUP"] = None
                    continue
                out[f"{base}-P"] = tn.e_mas(marg[cat].p, nac.p, t_star.p)
                ee = None if t_star.ic95 is None else (t_star.ic95[1] - t_star.ic95[0]) / 3.92
                reps = tn.e_mas_replicas(marg[cat].replicas, nac.replicas, t_star.p, ee, rng)
                ic = cf.ic95_de(cf.Celda(p=None, replicas=reps))
                out[f"{base}-IC95INF"] = None if ic is None else ic[0]
                out[f"{base}-IC95SUP"] = None if ic is None else ic[1]

    # ── cruces · familia por par ──────────────────────────────────────────
    fam = _familias(olas, par, ola_nueva)
    for p in PARES:
        _emite_familia(out, P, p, fam[p])
        n_hist = _n_por_ola_anteriores(fam[p]["meta"]["olas_anteriores"], olas, p)
        punt = cf.puntuadas(n_hist, umbral)
        for cod, key in codigos_par(p):
            for a, ns in n_hist.items():
                out[f"{P}-{p}-N-{a}-{cod}"] = int(ns[key])
            out[f"{P}-{p}-SOPORTE-HISTORICO-{cod}"] = "SI" if punt[key] else "NO"

    # ── control contra sellado (sólo en el ensayo: el contrato lo trae) ───
    ctrl = par.get("control_sellado") or {}
    for p, cands in ctrl.items():
        for cid, celdas in cands.items():
            peor = 0.0
            for cod, key in codigos_par(p):
                v = fam[p]["candidatos"][cid][key].p
                s = celdas.get(cod)
                if v is None or s is None:
                    continue
                peor = max(peor, abs(float(v) - float(s)))
            out[f"{P}-CTRL-{p}-{cid}-DELTA-P-MAX"] = float(peor)
            out[f"{P}-CTRL-{p}-{cid}-REPRODUCE"] = "SI" if peor <= float(par["control_tol_c2"]) else "NO"
    return out


# ══ COMMIT-3 · adjudicación ═══════════════════════════════════════════════

def _serie_completa(inputs, par, ola_nueva: int, seed_serie: int) -> dict:
    """R nacional de ND en la ola nueva por el medidor sellado de la serie,
    con el miembro resuelto por sufijo (la ruta interna cambia de ola en ola)."""
    m = _importa("medidor_serie_completa", MODULOS_SHA["SERIE-COMPLETA-MEDIDOR"])
    iid = par["olas_zip"][str(ola_nueva)] if str(ola_nueva) in par["olas_zip"] else par["olas_zip"][ola_nueva]
    ruta = inputs[iid]["ruta_absoluta"]
    sufijo = f"conjunto_de_datos_tmod_vic_envipe{ola_nueva}.csv"
    with zipfile.ZipFile(ruta) as zf:
        cands = [n for n in zf.namelist() if n.lower().endswith(sufijo)]
    if len(cands) != 1:
        raise RuntimeError(f"{sufijo}: {len(cands)} miembros en el zip")
    p = dict(par["serie_completa_parametros"])
    p.update({"ola_encuesta": ola_nueva, "anio_hecho": ola_nueva - 1,
              "payload_id": iid, "tabla_miembro": cands[0], "formato": "CSV"})
    r = m.medir({iid: {"ruta_absoluta": ruta}},
                {"parametros": p, "seed": {"aplica": True, "valor": seed_serie}})
    Q = f"RESULT-ENVIPE-SERIE-{ola_nueva}-"
    return {"p": r[Q + "P-C1-U1"], "lo": r[Q + "IC-BOOT-LO-C1-U1"],
            "hi": r[Q + "IC-BOOT-HI-C1-U1"], "n": r[Q + "N-U1"],
            "estado": r[Q + "ESTADO"], "miembro": cands[0]}


def _bbis_nacional(errores: dict, ics: dict) -> str:
    """Lectura mecánica del B-bis (diseño §6) a nivel nacional. `despeja` =
    IC95 de los dos contendientes disjuntos. Manda la fila de arriba. NO es
    el veredicto: F7(A) lo lee mesa con el origen móvil a la vista."""
    def _despeja(a, b):
        ia, ib = ics.get(a), ics.get(b)
        if ia is None or ib is None:
            return False
        return ia[1] < ib[0] or ib[1] < ia[0]
    e = {k: v for k, v in errores.items() if v is not None}
    if "K" not in e:
        return "NO-LEGIBLE: K no construible"
    ts = [t for t in ("T3", "T5", "TC") if t in e]
    if not ts:
        return "NO-LEGIBLE: ninguna tendencia construible"
    if all(e["K"] < e[t] and _despeja("K", t) for t in ts):
        return "FILA-1 corroborada: K gana a las tendencias construibles con IC que despejan"
    gana = [t for t in ts if e[t] < e["K"] and _despeja(t, "K")]
    if gana:
        return f"FILA-2 corroborada: {','.join(gana)} gana a K con IC que despeja"
    mejor = [t for t in ts if e[t] < e["K"]]
    if mejor:
        return f"FILA-3 falsador debil: {','.join(mejor)} gana en punto, el IC no despeja"
    signos = {np.sign(v) for v in e.values()}
    return ("FILA-4 acotada: ningun contendiente se distingue de otro"
            + ("; FILA-6 candidata: todos yerran en el mismo sentido" if len(signos) == 1 else ""))


def adjudicacion(inputs, contrato) -> dict:
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    ola_nueva = int(par["ola_nueva"])
    seed = int(contrato["seed"]["valor"])
    n_rep = int(par["bootstrap_replicas"])
    umbral = int(par["umbral_soporte_n"])
    tol_rep = float(par["tol_reproduccion_emisiones"])
    out = {}

    for iid in inputs:
        out[f"{P}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid]["sha256"])
    for k, ruta in MODULOS_SHA.items():
        out[f"{P}-G-CODIGO-{k}-SHA256"] = _sha(ruta)
    out[f"{P}-G-OLA-NUEVA"] = str(ola_nueva)

    # ── emisiones selladas: se leen y se REPRODUCEN antes de abrir R ─────
    em = json.loads(inputs["emisiones_selladas"]["bytes"].decode("utf-8"))
    em_res = em["resultados"]
    PE = str(par["prefijo_emisiones"])
    out[f"{P}-G-EMISIONES-SPEC-ID"] = str(em.get("spec_id"))
    out[f"{P}-G-EMISIONES-RESERVA-CRUCE-DERIVADO"] = str(em_res.get(f"{PE}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"))

    olas = _carga_olas(inputs, par, seed, n_rep, reservada_nueva=False)
    nueva = olas[ola_nueva]
    out[f"{P}-G-OLA-NUEVA-ABIERTA"] = "SI" if not nueva.ola.reservada else "NO -- DEFECTO"
    fam = _familias(olas, par, ola_nueva)
    peor = 0.0
    for p in PARES:
        for cid in CANDIDATOS_CRUCE:
            for cod, key in codigos_par(p):
                v = fam[p]["candidatos"][cid][key].p
                s = em_res.get(f"{PE}-{p}-{cid}-{cod}-P")
                if v is None and s is None:
                    continue
                if v is None or s is None:
                    peor = float("inf")
                    continue
                peor = max(peor, abs(float(v) - float(s)))
    out[f"{P}-G-EMISIONES-DELTA-P-MAX"] = peor if math.isfinite(peor) else None
    reproducidas = math.isfinite(peor) and peor <= tol_rep
    out[f"{P}-G-EMISIONES-REPRODUCIDAS"] = "SI" if reproducidas else "NO"
    if not reproducidas:
        raise RuntimeError(f"PARO: las emisiones selladas no se reproducen "
                           f"(delta max {peor}); no se abre R")

    # ── nacional · R por estimando ────────────────────────────────────────
    r_nd = _serie_completa(inputs, par, ola_nueva, int(par["seed_serie_completa"]))
    out[f"{P}-R-ND-P"] = _f(r_nd["p"])
    out[f"{P}-R-ND-IC95INF"] = _f(r_nd["lo"])
    out[f"{P}-R-ND-IC95SUP"] = _f(r_nd["hi"])
    out[f"{P}-R-ND-N"] = int(r_nd["n"])
    out[f"{P}-R-ND-ESTADO"] = str(r_nd["estado"])
    out[f"{P}-R-ND-MIEMBRO"] = str(r_nd["miembro"])
    r_en = nueva.nacional()
    out[f"{P}-R-EN-P"] = _f(r_en.p)
    out[f"{P}-R-EN-IC95INF"] = float(r_en.ic95[0])
    out[f"{P}-R-EN-IC95SUP"] = float(r_en.ic95[1])
    out[f"{P}-R-EN-N"] = int(r_en.n)
    R_nac = {"ND": (r_nd["p"], (r_nd["lo"], r_nd["hi"])),
             "EN": (r_en.p, tuple(r_en.ic95))}
    for est in ESTIMANDOS:
        rp, ric = R_nac[est]
        errores, ics = {}, {}
        for cid in NACIONALES:
            pc = em_res.get(f"{PE}-NAC-{est}-{cid}-P")
            lo, hi = em_res.get(f"{PE}-NAC-{est}-{cid}-IC95INF"), em_res.get(f"{PE}-NAC-{est}-{cid}-IC95SUP")
            base = f"{P}-NAC-{est}-{cid}"
            if pc is None or rp is None:
                out[f"{base}-ERROR-PP"] = None
                out[f"{base}-ABS-ERROR-PP"] = None
                out[f"{base}-R-EN-IC-CAND"] = "NO-CONSTRUIBLE"
                out[f"{base}-CAND-EN-IC-R"] = "NO-CONSTRUIBLE"
                continue
            err = 100.0 * (float(pc) - float(rp))
            errores[cid] = abs(err)
            ics[cid] = None if lo is None or hi is None else (float(lo), float(hi))
            out[f"{base}-ERROR-PP"] = err
            out[f"{base}-ABS-ERROR-PP"] = abs(err)
            out[f"{base}-R-EN-IC-CAND"] = ("NO-DERIVABLE" if ics[cid] is None
                                           else ("SI" if ics[cid][0] <= rp <= ics[cid][1] else "NO"))
            out[f"{base}-CAND-EN-IC-R"] = "SI" if ric[0] <= float(pc) <= ric[1] else "NO"
        out[f"{P}-G-NAC-{est}-MEJOR-POR-ERROR"] = (min(errores, key=errores.get) if errores else "NINGUNO")
        out[f"{P}-G-NAC-{est}-B-BIS-LECTURA-MECANICA"] = _bbis_nacional(errores, ics)
        out[f"{P}-G-NAC-{est}-ADJUDICA-SOLO"] = "NO -- F7(A): se lee con el origen movil a la vista"

    # ── E+ · R marginal por eje en la ola nueva vs E+ y persistencia ─────
    perdidos = {v: 0 for v in VARIANTES_EMAS}
    comparables = {v: 0 for v in VARIANTES_EMAS}
    for eje in EJES_EMAS:
        marg = nueva.marginal(eje)
        for cod, cat in grupos_eje(eje):
            r = marg[cat]
            _emite_celda(out, f"{P}-R-{cod}", r, con_n=True)
            pp = em_res.get(f"{PE}-PERS-{cod}-P")
            e_pers = None if pp is None or r.p is None else 100.0 * abs(float(pp) - r.p)
            out[f"{P}-PERS-{cod}-ABS-ERROR-PP"] = e_pers
            for var in VARIANTES_EMAS:
                pe = em_res.get(f"{PE}-EMAS-{var}-{cod}-P")
                if pe is None or r.p is None or e_pers is None:
                    out[f"{P}-EMAS-{var}-{cod}-ABS-ERROR-PP"] = None
                    out[f"{P}-EMAS-{var}-{cod}-VS-PERSISTENCIA"] = "NO-CONSTRUIBLE"
                    continue
                e = 100.0 * abs(float(pe) - r.p)
                out[f"{P}-EMAS-{var}-{cod}-ABS-ERROR-PP"] = e
                v = "EMAS-GANA" if e < e_pers else ("PERSISTENCIA-GANA" if e > e_pers else "EMPATE")
                out[f"{P}-EMAS-{var}-{cod}-VS-PERSISTENCIA"] = v
                comparables[var] += 1
                perdidos[var] += v == "PERSISTENCIA-GANA"
    for var in VARIANTES_EMAS:
        out[f"{P}-G-EMAS-{var}-CELDAS-COMPARABLES"] = int(comparables[var])
        out[f"{P}-G-EMAS-{var}-CELDAS-PIERDE-VS-PERSISTENCIA"] = int(perdidos[var])

    # ── cruces · R y regla v0.3 por par ───────────────────────────────────
    for p in PARES:
        cods = codigos_par(p)
        try:
            R = nueva.cruce(p)
        except mr.ReservaRota as exc:
            out[f"{P}-G-{p}-ESTADO"] = f"NO-ADJUDICABLE-VETO: {exc}"
            out[f"{P}-G-{p}-CELDAS-PUNTUADAS"] = 0
            out[f"{P}-G-{p}-VEREDICTO-PRIMARIO"] = "NO-ADJUDICABLE"
            for cod, key in cods:
                for s in ("P", "IC95INF", "IC95SUP"):
                    out[f"{P}-R-{p}-{cod}-{s}"] = None
                out[f"{P}-R-{p}-{cod}-N"] = None
                out[f"{P}-{p}-PUNTUADA-{cod}"] = "NO-ADJUDICABLE"
                for cid in CANDIDATOS_CRUCE:
                    out[f"{P}-{p}-{cid}-ERROR-PP-{cod}"] = None
                    out[f"{P}-{p}-{cid}-DENTRO-IC-R-{cod}"] = "NO-ADJUDICABLE"
                    out[f"{P}-{p}-{cid}-R-DENTRO-IC-CAND-{cod}"] = "NO-ADJUDICABLE"
            for cid in CANDIDATOS_CRUCE:
                out[f"{P}-{p}-{cid}-MAE-PP"] = None
                out[f"{P}-{p}-{cid}-DELTA-MAE-PP"] = None
                out[f"{P}-{p}-{cid}-DELTA-IC95INF"] = None
                out[f"{P}-{p}-{cid}-DELTA-IC95SUP"] = None
                out[f"{P}-{p}-{cid}-VEREDICTO"] = "NO-ADJUDICABLE"
                out[f"{P}-{p}-{cid}-ROL"] = "PISO" if cid == cf.PISO else ("PRIMARIA" if cid == cf.RETADOR_PRIMARIO else "SECUNDARIA")
            continue
        out[f"{P}-G-{p}-ESTADO"] = "ADJUDICADO"
        n_hist = _n_por_ola_anteriores(fam[p]["meta"]["olas_anteriores"], olas, p)
        n_hist[str(ola_nueva)] = {k: c.n for k, c in R.items()}
        punt = cf.puntuadas(n_hist, umbral)
        adj = cf.adjudica(R, fam[p]["candidatos"], punt)
        out[f"{P}-G-{p}-CELDAS-PUNTUADAS"] = int(adj["celdas_puntuadas"])
        for cod, key in cods:
            r = R[key]
            out[f"{P}-R-{p}-{cod}-P"] = _f(r.p)
            out[f"{P}-R-{p}-{cod}-IC95INF"] = None if r.ic95 is None else float(r.ic95[0])
            out[f"{P}-R-{p}-{cod}-IC95SUP"] = None if r.ic95 is None else float(r.ic95[1])
            out[f"{P}-R-{p}-{cod}-N"] = int(r.n)
            out[f"{P}-{p}-PUNTUADA-{cod}"] = "SI" if punt[key] else "NO"
            for cid in CANDIDATOS_CRUCE:
                f_ = adj["candidatos"][cid]["celdas"][key]
                out[f"{P}-{p}-{cid}-ERROR-PP-{cod}"] = _f(f_["error_pp"])
                out[f"{P}-{p}-{cid}-DENTRO-IC-R-{cod}"] = _txt({True: "SI", False: "NO"}.get(f_["dentro_ic_R"]))
                out[f"{P}-{p}-{cid}-R-DENTRO-IC-CAND-{cod}"] = _txt({True: "SI", False: "NO"}.get(f_["R_dentro_ic_cand"]))
        for cid in CANDIDATOS_CRUCE:
            c = adj["candidatos"][cid]
            out[f"{P}-{p}-{cid}-MAE-PP"] = _f(c["mae_pp"])
            out[f"{P}-{p}-{cid}-DELTA-MAE-PP"] = _f(c["delta_mae_pp"])
            out[f"{P}-{p}-{cid}-DELTA-IC95INF"] = None if c["delta_ic95"] is None else c["delta_ic95"][0]
            out[f"{P}-{p}-{cid}-DELTA-IC95SUP"] = None if c["delta_ic95"] is None else c["delta_ic95"][1]
            out[f"{P}-{p}-{cid}-VEREDICTO"] = str(c["veredicto"])
            out[f"{P}-{p}-{cid}-ROL"] = str(c["rol"])
        out[f"{P}-G-{p}-VEREDICTO-PRIMARIO"] = str(adj["candidatos"][cf.RETADOR_PRIMARIO]["veredicto"])
    out[f"{P}-G-REGLA"] = ("v0.3: dMAE = MAE(C2) - MAE(retador) sobre PUNTUADAS, IC95 por replica; "
                           "VENCE-RETADOR si IC95inf > 0.5 pp; PROPUESTA-CON-RESERVA si 0 < IC95inf <= 0.5; "
                           "NADIE-VENCE si incluye 0. Retador primario: SL (interaccion encogida)")
    return out


# ══ P3(ii) · origen móvil sobre lo sellado (sin microdato) ════════════════

def _serie_en_sellada(inputs, par) -> list[tn.Punto]:
    """Puntos nacionales de `evade_norma` leídos de los sellos que el contrato
    cita: {anio: {input, id_p, id_lo?, id_hi?}}. Sin IC donde no se selló."""
    puntos = []
    for anio, cita in sorted(par["en_puntos_sellados"].items(), key=lambda kv: int(kv[0])):
        res = json.loads(inputs[cita["input"]]["bytes"].decode("utf-8"))["resultados"]
        p = float(res[cita["id_p"]])
        lo = float(res[cita["id_lo"]]) if cita.get("id_lo") else None
        hi = float(res[cita["id_hi"]]) if cita.get("id_hi") else None
        puntos.append(tn.Punto(ola=int(anio), p=p, lo=lo, hi=hi, comparable=True))
    return puntos


def _emite_origen_movil(out, P, est, om: dict):
    def _si(v):
        return "NO-DERIVABLE" if v is None else ("SI" if v else "NO")
    for t, fila in om["por_ola"].items():
        for cid, f_ in fila.items():
            b = f"{P}-OM-{est}-{t}-{cid}"
            out[f"{b}-ESTADO"] = str(f_["estado"])
            out[f"{b}-PRED"] = _f(f_["pred"])
            out[f"{b}-IC95INF"] = None if f_["ic95"] is None else float(f_["ic95"][0])
            out[f"{b}-IC95SUP"] = None if f_["ic95"] is None else float(f_["ic95"][1])
            out[f"{b}-ERROR-PP"] = _f(f_["error_pp"])
            out[f"{b}-ABS-ERROR-PP"] = _f(f_["abs_error_pp"])
            out[f"{b}-R-EN-IC-CAND"] = _si(f_["R_en_ic_cand"])
            out[f"{b}-CAND-EN-IC-R"] = _si(f_["cand_en_ic_R"])
    for cid, r in om["resumen"].items():
        for ambito, rr in r.items():
            b = f"{P}-OM-{est}-RESUMEN-{cid}-{ambito.upper().replace('_', '-')}"
            out[f"{b}-N-OLAS"] = int(rr["n_olas"])
            out[f"{b}-MAE-PP"] = _f(rr["mae_pp"])
            out[f"{b}-SESGO-PP"] = _f(rr["sesgo_pp"])
            out[f"{b}-COBERTURA-R-EN-IC-CAND"] = _f(rr["cobertura_R_en_ic_cand"])
            out[f"{b}-COBERTURA-IC95INF"] = None if rr["cobertura_ic95"] is None else float(rr["cobertura_ic95"][0])
            out[f"{b}-COBERTURA-IC95SUP"] = None if rr["cobertura_ic95"] is None else float(rr["cobertura_ic95"][1])
            out[f"{b}-N-COBERTURA"] = int(rr["n_cobertura"])
            out[f"{b}-CAND-EN-IC-R-FRAC"] = _f(rr["cand_en_ic_R_frac"])
    out[f"{P}-OM-{est}-VENTANA-COMUN"] = ",".join(str(t) for t in om["ventana_comun"]) or "NINGUNA"
    out[f"{P}-OM-{est}-OLAS-NO-COMPARABLES"] = ",".join(str(t) for t in om["olas_no_comparables"]) or "NINGUNA"


def origen_movil(inputs, contrato) -> dict:
    """RETROSPECTIVA-MECÁNICA sobre la serie sellada: cada ola predicha sólo
    con las anteriores, por K/T3/T5/TC, sin selección. Sólo insumos
    versionados (repo, con sha): no abre microdato."""
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    out = {}
    for iid in inputs:
        out[f"{P}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid]["sha256"])
    for k in ("TENDENCIA-NACIONAL", "ENVIPE-DUELO"):
        out[f"{P}-G-CODIGO-{k}-SHA256"] = _sha(MODULOS_SHA[k])
    out[f"{P}-G-ROTULO"] = "RETROSPECTIVA-MECANICA -- no selecciona variante (F7 A)"
    s_nd = serie_nd(lee_serie_tsv(inputs[par["serie_nd_input"]]["bytes"]),
                    par["comparabilidad_homogenea"])
    out[f"{P}-G-ND-OLAS-EN-SERIE"] = len(s_nd)
    _emite_origen_movil(out, P, "ND", tn.origen_movil(s_nd))
    s_en = _serie_en_sellada(inputs, par)
    out[f"{P}-G-EN-OLAS-EN-SERIE"] = len(s_en)
    _emite_origen_movil(out, P, "EN", tn.origen_movil(s_en))
    return out


PUNTOS_DE_ENTRADA = {"emisiones": emisiones, "adjudicacion": adjudicacion,
                     "origen_movil": origen_movil}


def medir(inputs, contrato) -> dict:
    """Interfaz estable del plan v2.0 §4 (B-1)."""
    pe = str(contrato["parametros"]["punto_de_entrada"])
    if pe not in PUNTOS_DE_ENTRADA:
        raise RuntimeError(f"punto_de_entrada {pe!r} no es uno de {sorted(PUNTOS_DE_ENTRADA)}")
    out = PUNTOS_DE_ENTRADA[pe](inputs, contrato)
    P = str(contrato["parametros"]["prefijo_result"])
    out[f"{P}-G-MEDIDOR-IDENTICO-A-TOOLS"] = (
        "SI" if _sha(Path(__file__).resolve()) == _sha(MODULOS_SHA["ENVIPE-DUELO"]) else "NO -- DEFECTO")
    return out
