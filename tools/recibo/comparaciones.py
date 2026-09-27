#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/recibo/comparaciones.py` -- recibo de un lote de validacion
independiente (C1 de ASTRA-6): lee las comparaciones congeladas y produce la
tabla llave x estado x efecto, el rotulo de ceguera por paquete y el resumen.

ACTO GEN2-RECIBO-ASTRA6-1 (encargo
`forense/encargos/2026-09-26-GEN2-RECIBO-ASTRA6-1.md`, §5). Reutilizable en
los lotes siguientes: todo lo que depende del lote entra por `--lote`.

QUE LEE (nunca escribe fuera de `--salida`; cero microdato, cero red):
- `<lote>/entregas.json`, `<lote>/comparaciones/*--comparacion.json`,
  `<lote>/tabla-estimadores.tsv`, `<lote>/efectos-discrepancias.tsv`,
  `<lote>/hallazgos-spec.tsv`, `<lote>/dictamenes-publicabilidad.tsv`,
  `<lote>/reconstrucciones/<paquete>/*` (recibo, sesion, pruebas de commit).
- El paquete archivado (`*-entradas*.tar.gz` bajo
  `forense/validacion-independiente/`), localizado por su SHA-256 de
  contenedor; se listan y leen sus miembros (spec humana, estimandos), nunca
  el raw.
- `data/corrida0/<CALC>/spec.yaml` (tolerancia preexistente y numero de
  replicas) y `data/corrida0/<CALC>/resultados.json` (valor sellado, solo
  para magnitudes: ancho del IC, CV).
- `canon/catalogo-del-mexicano-v1_2.tsv` y `canon/tabla-de-piso-v1_1.tsv`
  (fila que cita cada llave).

REGLAS DECLARADAS (fijadas en este codigo, no por llave):
1. Estado por llave = el del comparador con la tolerancia PREEXISTENTE del
   CALC, citada de su spec.yaml; si la tolerancia del comparador no es la de
   la spec, la llave queda `TOLERANCIA-NO-CITADA` y no recibe estado.
   Se recomputa `dentro = |delta| <= abs` y se cuenta todo desacuerdo con el
   comparador (artefacto del comparador).
2. IC que discrepa con punto dentro de tolerancia, cuando la razon de la
   tolerancia es de replay ("semilla y sumas deterministas") y el IC es
   aleatorio (bootstrap) -> componente IC, artefacto
   `TOLERANCIA-DE-REPLAY-SOBRE-IC-ALEATORIO`: la vara no mide equivalencia
   inferencial; el estado sigue DISCREPA (no se inventa otra tolerancia).
3. Causa de un punto que discrepa: comparacion.json no la trae; la hipotesis
   del ejecutor (efectos-discrepancias.tsv) se copia como hipotesis y la
   causa del recibo es `CAUSA-NO-DETERMINABLE` salvo contrafactual archivado.
4. Publicabilidad (regla de la spec: ancho IC <= 0.20 y CV <= 0.30):
   margen relativo = min((0.30-CV)/0.30, (0.20-ancho)/0.20) sobre el valor
   sellado; banda de ruido Monte Carlo = 2/sqrt(2(R-1)) con R replicas de la
   spec (2 errores estandar relativos del EE bootstrap). Margen <= banda ->
   ACOTAR (publicabilidad fragil al RNG); margen > banda -> PROPONER-SUSPENDER.
5. Punto que discrepa -> ACOTAR (no corroborado independientemente); con
   |delta| > 0.05 (5 pp en una proporcion: fuera de toda lectura de redondeo
   o de NS/NR marginal) -> PROPONER-SUSPENDER. Umbral fijado por el recibo
   GEN2-RECIBO-ASTRA6-1 DESPUES de ver la distribucion del lote 1
   (RETROSPECTIVA); los lotes siguientes lo heredan fijo. IC
   solo -> SOSTENER. COINCIDE -> SOSTENER. NO-RECALCULABLE -> SOSTENER sin
   corroboracion (la carencia es de la spec, D-15).
6. Ceguera por paquete, por evidencia: CIEGA-POR-SEPARACION exige (a)
   contenedor archivado con el sha entregado y commiteado antes de la entrada
   de la sesion, (b) manifiesto casa y ningun miembro trae valores esperados
   ni codigo productor, (c) sesion con un solo mensaje y sin comandos hacia
   clon/red/esperados, (d) commit de la reconstruccion con oid recomputable y
   fecha anterior a la revelacion, (e) congelacion anterior a la revelacion.
   Falla cualquiera -> REIMPLEMENTACION-INDEPENDIENTE-NO-CIEGA.
7. Spec insuficiente: si el motivo es de ventana/horizonte y la celda
   sellada SI trae `ventana` pero el `estimandos.tsv` del paquete no tiene
   esa columna -> `PAQUETE-SIN-IDENTIDAD-DE-VENTANA` (defecto del preparador,
   no D-15); recodificacion NIV ausente -> `D15-RECODIFICACION-AUSENTE`;
   identidad contradictoria -> `D15-IDENTIDAD-CONTRADICTORIA`.

Uso:
    python3 tools/recibo/comparaciones.py \
        --lote forense/validacion-independiente/catalogo-1-ejecucion-lote1 \
        --salida forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1
    (sin --salida: solo imprime el resumen)
"""
from __future__ import annotations

import argparse
import base64
import csv
import glob
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import tarfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
CATALOGO = RAIZ / "canon" / "catalogo-del-mexicano-v1_2.tsv"
PISO = RAIZ / "canon" / "tabla-de-piso-v1_1.tsv"
MIEMBROS_PERMITIDOS = {"encargo.md", "estimandos.tsv", "faltantes.json",
                       "insumos.json", "manifiesto.json", "metodo.md",
                       "tolerancia.json", "conductas.md"}
PREFIJOS_PERMITIDOS = ("cuestionario-", "fd-")
COLS_VALOR = {"punto", "p", "ic95", "ic95_inf", "ic95_sup", "valor",
              "replicas", "esperado", "se", "cv"}
PATRON_FUGA = re.compile(
    r"(https?://|curl |wget |git clone|github|requests\.|urllib|/home/|"
    r"/mnt/|/root/|resultados\.json|sello\.json|--comparacion)")
UMBRAL_CV, UMBRAL_ANCHO = 0.30, 0.20
UMBRAL_PUNTO = 0.05
COLS_TABLA = [
    "llave", "paquete", "calc", "result_id", "celda", "estado_comparador",
    "estado_recibo", "componente", "efecto", "artefacto", "causa_recibo",
    "hipotesis_ejecutor", "delta_punto", "delta_ic_max", "ancho_ic_sellado",
    "delta_ic_rel_ancho", "cv_sellado", "margen_publicabilidad", "banda_mc",
    "tolerancia_citada", "fila_catalogo_v1_2", "fila_piso_v1_1",
    "causa_spec", "recomendacion",
]
COLS_CEGUERA = [
    "paquete", "contenedor", "contenedor_commit_utc", "entrada_utc",
    "a_contenedor_antes", "b_miembros_limpios", "c_sesion_limpia",
    "d_commit_antes_revelacion", "e_congelado_antes", "autorotulo_validador",
    "red_aislada_por_sandbox", "normalizacion", "rotulo_recibo", "evidencia",
]


def _tsv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(
        timezone.utc)


def _git_fecha_alta(ruta: Path) -> datetime | None:
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%cI", "--", str(ruta)],
        cwd=RAIZ, capture_output=True, text=True).stdout.split()
    return _utc(out[-1]) if out else None


def _replicas(spec: dict) -> int | None:
    pila = [spec]
    while pila:
        x = pila.pop()
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "bootstrap_replicas" and isinstance(v, int):
                    return v
                pila.append(v)
        elif isinstance(x, list):
            pila.extend(x)
    return None


class Calc:
    """Tolerancia, replicas y tabla sellada de un CALC (solo lectura)."""

    def __init__(self, calc: str):
        d = RAIZ / "data" / "corrida0" / calc
        self.spec = yaml.safe_load((d / "spec.yaml").read_text("utf-8"))
        self.tolerancia = self.spec.get("tolerancia") or {}
        self.replicas = _replicas(self.spec)
        self._res = json.loads((d / "resultados.json").read_text("utf-8"))
        self._tablas: dict[str, list] = {}

    def celda(self, rid: str, celda: int) -> dict | None:
        if rid not in self._tablas:
            v = self._res["resultados"].get(rid)
            self._tablas[rid] = json.loads(v) if isinstance(v, str) else v
        t = self._tablas[rid]
        return t[celda] if t and 0 <= celda < len(t) else None


def _filas_por_llave(ruta: Path) -> dict[str, int]:
    """llave -> numero de fila de datos (1 = primera fila tras cabecera)."""
    out = {}
    if not ruta.exists():
        return out
    with ruta.open(encoding="utf-8", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh, delimiter="\t"), 1):
            out[r["llave"]] = i
    return out


def _tar_por_sha() -> dict[str, Path]:
    idx = {}
    for f in glob.glob(str(RAIZ / "forense" / "validacion-independiente" /
                           "**" / "*.tar.gz"), recursive=True):
        idx[hashlib.sha256(Path(f).read_bytes()).hexdigest()] = Path(f)
    return idx


def _blob(prueba: dict, ruta_sufijo: str) -> str | None:
    for a in prueba.get("archivos", []):
        if a["ruta"].endswith(ruta_sufijo) and "blob_content_base64" in a:
            b = base64.b64decode(a["blob_content_base64"])
            if hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest() != \
                    a["blob_oid"]:
                return None
            return b.decode("utf-8")
    return None


def _commit(prueba: dict) -> tuple[bool, datetime]:
    raw = base64.b64decode(prueba["commit_content_base64"])
    ok = hashlib.sha1(b"commit %d\0" % len(raw) + raw).hexdigest() == \
        prueba["commit_oid"]
    linea = [l for l in raw.decode("utf-8").split("\n")
             if l.startswith("committer ")][0].split()
    return ok, datetime.fromtimestamp(int(linea[-2]), timezone.utc)


def ceguera(lote: Path, entrega: dict, tars: dict[str, Path]) -> dict:
    p = entrega["paquete"]
    rec = lote / "reconstrucciones" / p
    ev = []
    ent = _utc(entrega["entrada_registrada_utc"])
    rev = _utc(entrega["revelacion_utc"])
    tar = tars.get(entrega["sha256_contenedor"])
    alta = _git_fecha_alta(tar) if tar else None
    a = bool(tar and alta and alta < ent)
    ev.append(f"a:{tar.relative_to(RAIZ) if tar else 'CONTENEDOR-NO-ENCONTRADO'}"
              f"@{alta.isoformat() if alta else '-'}")
    b = False
    cab_estimandos: list[str] = []
    if tar:
        with tarfile.open(tar) as t:
            miembros = {os.path.basename(m.name): m for m in t.getmembers()
                        if m.isfile()}
            raros = [n for n in miembros if n not in MIEMBROS_PERMITIDOS and
                     not n.startswith(PREFIJOS_PERMITIDOS)]
            man = json.load(t.extractfile(miembros["manifiesto.json"]))
            sha_man = hashlib.sha256(
                t.extractfile(miembros["manifiesto.json"]).read()).hexdigest()
            malos = [n for n, s in man.get("archivos", {}).items()
                     if n in miembros and hashlib.sha256(
                         t.extractfile(miembros[n]).read()).hexdigest() != s]
            cab = t.extractfile(miembros["estimandos.tsv"]).readline() \
                .decode("utf-8").strip().split("\t")
            cols = sorted(COLS_VALOR & set(cab))
            cab_estimandos = cab
        b = (not raros and not malos and not cols and
             sha_man == entrega["paquete_sha256"])
        ev.append(f"b:miembros={len(miembros)} raros={raros} "
                  f"sha_malos={malos} cols_valor={cols} "
                  f"manifiesto={'COINCIDE' if sha_man == entrega['paquete_sha256'] else 'DISCORDA'}")
    ses = json.loads(next(rec.glob("*--sesion-sin-outputs-raw.json"))
                     .read_text("utf-8"))
    fugas = sorted({m.group(0) for c in ses.get("comandos", [])
                    for m in PATRON_FUGA.finditer(
                        c.get("input", "") if isinstance(c, dict) else str(c))
                    # el propio recibo del validador puede citar la palabra
                    if "No se consult" not in (c.get("input", "") if
                                               isinstance(c, dict) else "")})
    c = len(ses.get("mensajes_usuario", [])) == 1 and not fugas
    ev.append(f"c:mensajes={len(ses.get('mensajes_usuario', []))} "
              f"comandos={len(ses.get('comandos', []))} fugas={fugas}")
    d = True
    for f in sorted(rec.glob("*--prueba-commit*.json")):
        pr = json.loads(f.read_text("utf-8"))
        ok, t_commit = _commit(pr)
        d = d and ok and t_commit < rev
        ev.append(f"d:{pr['commit_oid'][:8]} oid_ok={ok} "
                  f"{t_commit.isoformat()}<rev={t_commit < rev}")
    e = _utc(entrega["congelacion_recibida_utc"]) < rev
    auto = "NO-CIEGA" if any(
        "NO-CIEGA" in f.read_text("utf-8", errors="ignore")
        for f in rec.rglob("*") if f.is_file() and f.suffix in
        (".md", ".json")) else "sin-rotulo"
    lanza = RAIZ / "tools" / "validacion" / "astra6_lote1" / "lanza.sh"
    red = "--unshare-net" in lanza.read_text("utf-8") if lanza.exists() \
        else None
    norm = "NINGUNA"
    orig = list(rec.glob("*--prueba-commit-original.json"))
    if orig:
        o = _blob(json.loads(orig[0].read_text("utf-8")), "reconstruccion.tsv")
        n = _blob(json.loads(next(rec.glob("*--prueba-commit.json"))
                             .read_text("utf-8")), "reconstruccion-canonica.tsv")
        if o is None or n is None:
            norm = "NO-VERIFICABLE"
        else:
            O = list(csv.DictReader(io.StringIO(o), delimiter="\t"))
            N = list(csv.DictReader(io.StringIO(n), delimiter="\t"))
            dif = sum(1 for x, y in zip(O, N) if x["llave"] != y["llave"] or
                      any(x.get(k, "") != y.get(k, "")
                          for k in ("punto", "ic95_inf", "ic95_sup")))
            norm = ("SOLO-ESTADO-PRE-REVELACION" if dif == 0 and
                    len(O) == len(N) and d else f"CIFRAS-CAMBIADAS:{dif}")
    rot = ("CIEGA-POR-SEPARACION" if a and b and c and d and e and
           not norm.startswith("CIFRAS") else
           "REIMPLEMENTACION-INDEPENDIENTE-NO-CIEGA")
    return {"paquete": p, "contenedor": entrega["sha256_contenedor"],
            "contenedor_commit_utc": alta.isoformat() if alta else "",
            "entrada_utc": ent.isoformat(), "a_contenedor_antes": a,
            "b_miembros_limpios": b, "c_sesion_limpia": c,
            "d_commit_antes_revelacion": d, "e_congelado_antes": e,
            "autorotulo_validador": auto,
            "red_aislada_por_sandbox": red, "normalizacion": norm,
            "rotulo_recibo": rot, "evidencia": " | ".join(ev),
            "_cab_estimandos": cab_estimandos}


def _causa_spec(motivo: str, sellada: dict, cab: set[str]) -> str:
    """Regla 7: la ventana que el sello SI trae y el paquete no -> defecto de
    empaquetado, no D-15. Lo demas se clasifica por el motivo declarado."""
    m = motivo.lower()
    if (any(k in m for k in ("ventana", "horizonte", "temporal")) and
            sellada.get("ventana") and "ventana" not in cab):
        return "PAQUETE-SIN-IDENTIDAD-DE-VENTANA"
    if "niv" in m and ("recodific" in m or "niv ->" in m):
        return "D15-RECODIFICACION-AUSENTE"
    if "contradictoria" in m:
        return "D15-IDENTIDAD-CONTRADICTORIA"
    return "D15-OTRA"


def _cubo(x: float, cortes: list[float]) -> str:
    for c in cortes:
        if x <= c:
            return f"<={c:g}"
    return f">{cortes[-1]:g}"


def recibe(lote: Path) -> tuple[list[dict], list[dict], dict]:
    entregas = json.loads((lote / "entregas.json").read_text("utf-8"))
    tars = _tar_por_sha()
    ceg = [ceguera(lote, e, tars) for e in entregas]
    estim = {r["llave"]: r for r in _tsv(lote / "tabla-estimadores.tsv")}
    efectos = {r["llave"]: r for r in _tsv(lote / "efectos-discrepancias.tsv")}
    publ = {r["llave"]: r for r in
            _tsv(lote / "dictamenes-publicabilidad.tsv")}
    hall = {r["llave"]: r for r in _tsv(lote / "hallazgos-spec.tsv")}
    cab = {c["paquete"]: set(c["_cab_estimandos"]) for c in ceg}
    cat, piso = _filas_por_llave(CATALOGO), _filas_por_llave(PISO)
    calcs: dict[str, Calc] = {}
    filas, artef_comp, sha_comp = [], 0, {}
    for e in entregas:
        f = lote / e["comparacion"]
        sha_comp[e["paquete"]] = (hashlib.sha256(f.read_bytes()).hexdigest()
                                  == e["comparacion_sha256"])
        comp = json.loads(f.read_text("utf-8"))
        tol = comp["tolerancia"]
        for r in comp["resultados"]:
            ll = r["llave"]
            est = estim[ll]
            if est["calc"] not in calcs:
                calcs[est["calc"]] = Calc(est["calc"])
            calc = calcs[est["calc"]]
            t_spec = calc.tolerancia
            citada = (t_spec.get("tipo") == tol.get("tipo") and
                      float(t_spec.get("abs", -1)) == float(tol.get("abs")))
            campos = r.get("campos") or {}
            for k, v in campos.items():
                if (abs(v["delta"]) <= float(tol["abs"])) != v["dentro"]:
                    artef_comp += 1
            s = calc.celda(est["result_id"], int(est["celda"])) or {}
            ancho = (s["ic95"][1] - s["ic95"][0]) if s.get("ic95") else None
            cv = (s["se"] / s["p"]) if s.get("se") and s.get("p") else None
            dp = campos.get("punto", {}).get("delta")
            dic = max((abs(campos[k]["delta"]) for k in
                       ("ic95_inf", "ic95_sup") if k in campos), default=None)
            fila = dict.fromkeys(COLS_TABLA, "")
            fila.update(
                llave=ll, paquete=e["paquete"], calc=est["calc"],
                result_id=est["result_id"], celda=est["celda"],
                estado_comparador=r["estado"],
                delta_punto="" if dp is None else repr(dp),
                delta_ic_max="" if dic is None else repr(dic),
                ancho_ic_sellado="" if ancho is None else repr(ancho),
                delta_ic_rel_ancho=("" if dic is None or not ancho
                                    else repr(dic / ancho)),
                cv_sellado="" if cv is None else repr(cv),
                tolerancia_citada=(f"{tol['tipo']} abs={tol['abs']} "
                                   f"(spec.yaml: {t_spec.get('razon', '')})"
                                   if citada else "TOLERANCIA-NO-CITADA"),
                fila_catalogo_v1_2=cat.get(ll, ""),
                fila_piso_v1_1=piso.get(ll, ""))
            if not citada:
                fila.update(estado_recibo="TOLERANCIA-NO-CITADA",
                            recomendacion="SIN-ESTADO")
            elif ll in publ:
                banda = (2 / math.sqrt(2 * (calc.replicas - 1))
                         if calc.replicas else None)
                margen = min(
                    (UMBRAL_CV - cv) / UMBRAL_CV if cv is not None else 1,
                    (UMBRAL_ANCHO - ancho) / UMBRAL_ANCHO
                    if ancho is not None else 1)
                fila.update(
                    estado_recibo="DISCREPA", componente="PUBLICABILIDAD",
                    efecto="alcance", causa_recibo="CAUSA-NO-DETERMINABLE",
                    hipotesis_ejecutor=publ[ll]["motivo"],
                    margen_publicabilidad=repr(margen),
                    banda_mc="" if banda is None else repr(banda),
                    recomendacion=("ACOTAR" if banda is not None and
                                   margen <= banda else "PROPONER-SUSPENDER"))
            elif r["estado"] == "COINCIDE":
                fila.update(estado_recibo="COINCIDE", componente="PUNTO+IC",
                            efecto="ninguno", recomendacion="SOSTENER")
            elif r["estado"] == "NO-RECALCULABLE-DESDE-SPEC":
                fila.update(estado_recibo="NO-RECALCULABLE-DESDE-SPEC",
                            componente="SPEC", efecto="ninguno (sin cifra)",
                            hipotesis_ejecutor=hall.get(ll, {}).get(
                                "motivo", ""),
                            causa_spec=_causa_spec(
                                hall.get(ll, {}).get("motivo", ""), s,
                                cab.get(e["paquete"], set())),
                            recomendacion="SOSTENER-SIN-CORROBORACION")
            elif campos.get("punto", {}).get("dentro"):
                aleatorio = "semilla" in str(t_spec.get("razon", ""))
                fila.update(
                    estado_recibo="DISCREPA", componente="IC",
                    efecto="incertidumbre",
                    artefacto=("TOLERANCIA-DE-REPLAY-SOBRE-IC-ALEATORIO"
                               if aleatorio else ""),
                    causa_recibo="CAUSA-NO-DETERMINABLE",
                    hipotesis_ejecutor=efectos.get(ll, {}).get(
                        "causa_o_hipotesis", ""),
                    recomendacion="SOSTENER")
            else:
                fila.update(
                    estado_recibo="DISCREPA", componente="PUNTO",
                    efecto="cifra", causa_recibo="CAUSA-NO-DETERMINABLE",
                    hipotesis_ejecutor=efectos.get(ll, {}).get(
                        "causa_o_hipotesis", ""),
                    recomendacion=("PROPONER-SUSPENDER"
                                   if dp is not None and abs(dp) > UMBRAL_PUNTO
                                   else "ACOTAR"))
            filas.append(fila)
    # resumen
    por_paq = defaultdict(Counter)
    for f in filas:
        por_paq[f["paquete"]][f"{f['estado_recibo']}|{f['componente']}"] += 1
    puntos = [f for f in filas if f["componente"] == "PUNTO"]
    ics = [f for f in filas if f["componente"] == "IC"]
    resumen = {
        "lote": str(lote.relative_to(RAIZ)),
        "llaves": len(filas),
        "sin_estado": sum(1 for f in filas if not f["estado_recibo"] or
                          f["estado_recibo"] == "TOLERANCIA-NO-CITADA"),
        "comparacion_sha_casa": sha_comp,
        "artefacto_comparador_dentro_recomputado_distinto": artef_comp,
        "por_estado_componente": dict(Counter(
            f"{f['estado_recibo']}|{f['componente']}" for f in filas)),
        "por_paquete": {k: dict(v) for k, v in sorted(por_paq.items())},
        "puntos_por_hipotesis": dict(Counter(
            f["hipotesis_ejecutor"].split(":")[0] for f in puntos)),
        "puntos_por_paquete_hipotesis": dict(Counter(
            f"{f['paquete']}|{f['hipotesis_ejecutor'].split(':')[0]}"
            for f in puntos)),
        "puntos_abs_delta": dict(Counter(
            _cubo(abs(float(f["delta_punto"])), [1e-4, 1e-3, 1e-2, 5e-2])
            for f in puntos)),
        "ic_delta_rel_ancho": dict(Counter(
            _cubo(float(f["delta_ic_rel_ancho"]), [0.01, 0.05, 0.10, 0.25])
            for f in ics if f["delta_ic_rel_ancho"])),
        "ic_artefacto": dict(Counter(f["artefacto"] for f in ics)),
        "recomendacion": dict(Counter(f["recomendacion"] for f in filas)),
        "spec_por_causa": dict(Counter(
            f"{f['paquete']}|{f['causa_spec']}" for f in filas
            if f["componente"] == "SPEC")),
        "publicabilidad": [
            {k: f[k] for k in ("llave", "cv_sellado", "ancho_ic_sellado",
                               "margen_publicabilidad", "banda_mc",
                               "fila_catalogo_v1_2", "fila_piso_v1_1",
                               "recomendacion")}
            for f in filas if f["componente"] == "PUBLICABILIDAD"],
        "ceguera": {c["paquete"]: c["rotulo_recibo"] for c in ceg},
    }
    return filas, ceg, resumen


def _escribe(ruta: Path, cols: list[str], filas: list[dict]) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lote", required=True)
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    lote = (RAIZ / a.lote).resolve()
    filas, ceg, resumen = recibe(lote)
    if a.salida:
        s = RAIZ / a.salida
        s.mkdir(parents=True, exist_ok=True)
        # prefijo = carpeta: T02 no admite dos `resumen.json` en el repo
        pre = s.name.lower()
        _escribe(s / f"{pre}--tabla-result-estado-efecto.tsv", COLS_TABLA,
                 filas)
        _escribe(s / f"{pre}--ceguera.tsv", COLS_CEGUERA, ceg)
        (s / f"{pre}--resumen.json").write_text(
            json.dumps(resumen, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
    print(json.dumps({k: v for k, v in resumen.items()
                      if k not in ("publicabilidad",)},
                     ensure_ascii=False, indent=1))
    return 0 if resumen["sin_estado"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
