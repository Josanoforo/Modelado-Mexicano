#!/usr/bin/env python3
"""`tools/benchmark.py` -- la consulta del Benchmark, por el contrato `docs/consulta.md`.

ACTO GEN2-PRODUCTO-CONSULTA-1 (`forense/encargos/2026-09-26-GEN2-PRODUCTO-CONSULTA-1.md`).

Defecto que ataca: el programa tenía catálogo, motor y tablero, y ningún
camino por el que alguien de fuera haga una pregunta y reciba una respuesta
citable. Toda cifra que sale de aquí es una fila del catálogo vigente y se
comprueba contra el RESULT sellado que cita (`resuelve_sellado`); el test de
equivalencia lo hace sobre el catálogo entero.

Subcomandos:
  puntero                 catálogo vigente (N mayor) y su conteo de filas
  consulta …              `--conducta` | `--texto`, `--segmento eje=valor`,
                          `--instrumento`, `--ola`, `--json`, `--limite`
  verificar <llave>       cadena sello.sha256 → sello.json → resultados.json → fila
  exporta [--salida P]    deriva docs/data/catalogo-v1_N.json (Pages)

Nunca escribe salvo `exporta` (D-23), y nunca abre `data/raw`.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CANON = RAIZ / "canon"
CORRIDA = RAIZ / "data/corrida0"
AUX = RAIZ / "forense/analisis/catalogo/v1_1"
REGLAS = RAIZ / "milpa/tramite.yaml"
MANIFIESTO = RAIZ / "data/manifiesto.yaml"
DOCS_DATA = RAIZ / "docs/data"

TERMINOS = ("Términos: uso no comercial libre con atribución; uso comercial por acuerdo; "
            "contacto = correo de CITATION.cff.")

EJES = {
    "sexo": ("sexo", "SEXO"),
    "edad": ("edad", "EDAD"),
    "escolaridad": ("escolaridad", "ESCOLARIDAD", "ESC", "escolaridad_proxy"),
    "localidad": ("localidad", "TLOC", "ESTRATO", "dominio_urbano_rural"),
    "formalidad": ("formalidad", "cuenta_formal"),
    "region": ("entidad", "ENT"),
    "nse": ("NSE",),
    "nacional": ("nacional", "TOTAL"),
}
NO_ESTIMABLE = ("CELDA-SUPRIMIDA", "CELDA-NO-ESTIMABLE")


# ── lectura ────────────────────────────────────────────────────────────────
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return s.lower()


def lee(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def puntero() -> tuple[str, Path]:
    """Catálogo vigente: el `v1_N` de N mayor presente en canon/."""
    cands = []
    for p in CANON.glob("catalogo-del-mexicano-v*_*.tsv"):
        m = re.fullmatch(r"catalogo-del-mexicano-v(\d+)_(\d+)\.tsv", p.name)
        if m:
            cands.append(((int(m.group(1)), int(m.group(2))), p))
    if not cands:
        raise SystemExit("NO-ENCONTRADO · canon/catalogo-del-mexicano-v*_*.tsv · archivos examinados=0")
    (ma, mi), p = max(cands)
    return f"v{ma}_{mi}", p


@lru_cache(maxsize=1)
def catalogo() -> tuple[str, list[dict[str, str]]]:
    ver, p = puntero()
    return ver, lee(p)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def sellado(calc: str) -> tuple[dict, str, str]:
    """sello.sha256 → sello.json → resultados.json; devuelve (resultados, sha_res, sha_sello)."""
    d = CORRIDA / calc
    listado = (d / "sello.sha256").read_text().split()[0]
    sh = sha(d / "sello.json")
    if listado != sh:
        raise ValueError(f"CADENA-ROTA:sello.sha256 · {calc}")
    sello = json.loads((d / "sello.json").read_text())
    rh = sha(d / "resultados.json")
    if sello.get("resultados.json") != rh:
        raise ValueError(f"CADENA-ROTA:resultados.json · {calc}")
    return json.loads((d / "resultados.json").read_text())["resultados"], rh, sh


@lru_cache(maxsize=None)
def _tabla_de(calc: str, rid: str) -> list:
    v = sellado(calc)[0][rid]
    v = json.loads(v) if isinstance(v, str) else v
    return v["celdas"] if isinstance(v, dict) else v


def resuelve_sellado(fila: dict[str, str]) -> dict:
    """Valor del RESULT sellado que cita la fila (contrato §1)."""
    data, _, _ = sellado(fila["calc"])
    rid, celda = fila["result_id"], fila["celda"]
    if celda.isdigit():
        c = _tabla_de(fila["calc"], rid)[int(celda)]
        p = c.get("punto", c.get("p"))
        lo = c.get("ic95_lo", (c.get("ic95") or [None, None])[0])
        hi = c.get("ic95_hi", (c.get("ic95") or [None, None])[1])
        return {"punto": p, "ic95": [lo, hi], "registro": c}
    return {"punto": data[rid], "ic95": None, "registro": None}


def iguales(a, b: str) -> bool:
    if b == "" or a is None:
        return b == "" and a is None
    return float(a) == float(b)


@lru_cache(maxsize=1)
def hashes() -> dict[str, dict[str, str]]:
    return {r["calc"]: r for r in lee(AUX / "calcs.tsv")}


@lru_cache(maxsize=1)
def reglas() -> dict[str, dict]:
    import yaml  # noqa: PLC0415
    d = yaml.safe_load(REGLAS.read_text())
    return {r["id"]: r for r in d.get("reglas", []) if isinstance(r, dict) and "id" in r}


@lru_cache(maxsize=1)
def olas_reservadas() -> frozenset[tuple[str, str]]:
    """(instrumento, ola) de payloads RESERVADA* del manifiesto; sólo ids, nunca payloads."""
    out, iid = set(), None
    with MANIFIESTO.open(encoding="utf-8") as f:
        for linea in f:
            m = re.match(r"-\s+id:\s*['\"]?([^'\"\s]+)", linea)
            if m:
                iid = m.group(1)
            elif iid and re.match(r"\s+estado_reserva:\s*['\"]?RESERVADA", linea):
                ins = re.match(r"([a-z0-9]+?)(?:_|\d{4})", iid)
                ola = re.search(r"(?<!\d)(19|20)\d\d(?!\d)", iid)
                if ins and ola:
                    out.add((ins.group(1).upper(), ola.group(0)))
    return frozenset(out)


def tipo_ic(nat: str) -> str:
    n = nat.upper()
    if n.startswith("SIN-IC"):
        return "sin-ic"
    if "CALIBRADO" in n and "SIN-CALIBRACION" not in n:
        return "calibrado"
    if "SPEC" in n or "T-1" in n:
        return "ic-con-r"
    return "diseno"


# ── consulta ───────────────────────────────────────────────────────────────
def casa(fila, conducta, palabras, segs, instrumento, ola) -> bool:
    if conducta and fila["conducta"] != conducta:
        return False
    if palabras:
        hay = norm(" ".join((fila["conducta"], fila["dominio"], fila["instrumento"], fila["llave"])))
        hay = hay.replace("_", " ").replace("-", " ") + " " + hay
        if not all(w in hay for w in palabras):
            return False
    if instrumento and fila["instrumento"].upper() != instrumento.upper():
        return False
    if ola and fila["ola"] != ola:
        return False
    for eje, valor in segs:
        if fila["eje"] not in EJES[eje]:
            return False
        if valor.startswith("="):
            if norm(fila["segmento"]) != norm(valor[1:]):
                return False
        elif valor and norm(valor) not in norm(fila["segmento"]):
            return False
    return True


def respuesta(fila: dict[str, str], ver: str) -> dict:
    s = resuelve_sellado(fila)
    if not iguales(s["punto"], fila["punto"]):
        raise SystemExit(f"PARO-c · {fila['llave']}: catálogo {fila['punto']} ≠ sellado {s['punto']}")
    h = hashes().get(fila["calc"], {})
    _, rh, sh = sellado(fila["calc"])
    if h and (h["sha256_resultados"] != rh or h["sha256_sello"] != sh):
        raise SystemExit(f"CADENA-ROTA:calcs.tsv · {fila['calc']}")
    regla = None
    if fila["alcance"] == "PARAMETRO-DE-REGLA" and fila["segmento"] in reglas():
        r = reglas()[fila["segmento"]]
        regla = {"id": r["id"], "tier": r.get("tier"), "falsable_si": r.get("falsable_si")}
    ic = [float(fila["ic95_inf"]), float(fila["ic95_sup"])] if fila["ic95_inf"] and fila["ic95_sup"] else None
    return {
        "llave": fila["llave"], "conducta": fila["conducta"], "dominio": fila["dominio"],
        "instrumento": fila["instrumento"], "ola": fila["ola"], "eje": fila["eje"],
        "segmento": fila["segmento"], "punto": float(fila["punto"]), "ic95": ic,
        "tipo_ic": tipo_ic(fila["naturaleza_ic"]), "naturaleza_ic": fila["naturaleza_ic"],
        "unidad": fila["unidad"], "temporalidad": fila["temporalidad"],
        "origen_piso": fila["origen_piso"], "estado_adopcion": fila["estado_adopcion"],
        "alcance": fila["alcance"], "firma": fila["firma_fp"], "result": fila["result_id"],
        "celda": fila["celda"], "calc": fila["calc"], "sha256_resultados": rh,
        "sha256_sello": sh, "oferta": fila["oferta_exclusion"], "regla": regla,
        "reserva": fila["reserva"], "catalogo": ver, "terminos": TERMINOS,
    }


def _etiqueta_excluida(e: dict[str, str], calcs: set[str] | None = None) -> str:
    """Texto de una celda excluida: su llave y, si es registro de una TABLA sellada de un
    CALC en `calcs` (o `calcs is None`), la conducta que nombra el registro."""
    llave = e["llave"]
    if "#" in llave and (calcs is None or e["calc"] in calcs):
        base, i = llave.rsplit("#", 1)
        try:
            c = _tabla_de(e["calc"], base)[int(i)]
            return llave + " " + " ".join(str(c.get(k) or "") for k in ("conducta", "medida", "resultado"))
        except (KeyError, ValueError, IndexError, FileNotFoundError):
            return llave
    return llave


def _casa_excluida(etq: str, conducta: str | None, palabras: list[str]) -> bool:
    if conducta:
        return norm(conducta) in re.split(r"[\s#]+", etq) or f"-{norm(conducta)}-" in etq
    t = etq.replace("_", " ").replace("-", " ") + " " + etq
    return all(w in t for w in palabras)


def no_contesta(filas, conducta, palabras, segs_raw, instrumento, ola) -> list[dict]:
    out = []
    for eje, _ in segs_raw:
        if eje not in EJES:
            out.append({"razon": "EJE-NO-DISPONIBLE", "detalle": f"eje «{eje}»; disponibles: {', '.join(EJES)}"})
    if instrumento and ola and (instrumento.upper(), ola) in olas_reservadas():
        out.append({"razon": "OLA-RESERVADA", "detalle": f"{instrumento.upper()} {ola}: reservada en data/manifiesto.yaml (E.6); no se abre ni se consulta"})
    if conducta or palabras:
        calcs = {f["calc"] for f in filas}
        vistos = {}
        for e in lee(AUX / "excluidos.tsv"):
            if instrumento and instrumento.upper() not in e["calc"].upper():
                continue
            if not _casa_excluida(norm(_etiqueta_excluida(e, calcs)), conducta, palabras):
                continue
            razon = "SEGMENTO-NO-ESTIMABLE" if e["causa"].startswith(NO_ESTIMABLE) else "FUERA-POR-REGLA"
            vistos.setdefault((razon, e["causa"]), []).append(e["llave"])
        for (razon, causa), ll in sorted(vistos.items()):
            out.append({"razon": razon, "detalle": f"{causa}: {len(ll)} celda(s), p. ej. {ll[0]}"})
        if palabras:
            for c in lee(AUX / "cobertura-31.tsv"):
                if c["estado"] != "MEDIDO" and all(w in norm(c["dominio"] + " " + c["report"]).replace("_", " ") for w in palabras):
                    out.append({"razon": "DOMINIO-NO-MEDIDO", "detalle": f"{c['dominio']}: {c['estado']} ({c['report']})"})
    if not filas and not out:
        out.append({"razon": "SIN-COINCIDENCIA",
                    "detalle": "ninguna fila del catálogo vigente casa; universo = catálogo completo"})
    return out


def consulta(conducta=None, texto=None, segmentos=(), instrumento=None, ola=None, limite=None) -> dict:
    ver, filas = catalogo()
    palabras = [w for w in norm(texto or "").replace("_", " ").split() if w]
    segs_raw = [(norm(s.split("=", 1)[0]).strip(), s.split("=", 1)[1].strip() if "=" in s else "")
                for s in segmentos]
    segs = [(e, v) for e, v in segs_raw if e in EJES]
    # exacta si algún segmento del eje casa exacto; si no, subcadena (contrato §2)
    segs = [(e, "=" + v if v and any(f["eje"] in EJES[e] and norm(f["segmento"]) == norm(v) for f in filas) else v)
            for e, v in segs]
    elegidas = [] if len(segs) < len(segs_raw) else \
        [f for f in filas if casa(f, conducta, palabras, segs, instrumento, ola)]
    total = len(elegidas)
    if limite:
        elegidas = elegidas[:limite]
    return {
        "catalogo": ver,
        "consulta": {"conducta": conducta, "texto": texto, "segmento": list(segmentos),
                     "instrumento": instrumento, "ola": ola},
        "n": total,
        "respuestas": [respuesta(f, ver) for f in elegidas],
        "no_contesta": no_contesta(elegidas, conducta, palabras, segs_raw, instrumento, ola),
        "terminos": TERMINOS,
    }


def humano(r: dict) -> str:
    q = {k: v for k, v in r["consulta"].items() if v}
    ls = [f"catálogo {r['catalogo']} · consulta {q} · filas={r['n']} (mostradas {len(r['respuestas'])})"]
    for a in r["respuestas"]:
        ic = f"[{a['ic95'][0]:.6g}, {a['ic95'][1]:.6g}]" if a["ic95"] else "sin IC identificado"
        ls.append(f"\n{a['conducta']} · {a['instrumento']} {a['ola']} · {a['eje']}={a['segmento']}")
        ls.append(f"  punto {a['punto']:.6g} · IC95 {ic} ({a['tipo_ic']}: {a['naturaleza_ic']}) · unidad {a['unidad']}")
        ls.append(f"  {a['temporalidad']} · origen {a['origen_piso']} · {a['estado_adopcion']} · {a['alcance']}")
        ls.append(f"  cita {a['result']}{'#' + a['celda'] if a['celda'] else ''} · {a['calc']} · resultados {a['sha256_resultados'][:12]} · sello {a['sha256_sello'][:12]}")
        ls.append(f"  oferta: {a['oferta']}")
        if a["regla"]:
            ls.append(f"  regla {a['regla']['id']} · tier {a['regla']['tier']} · falsable si: {a['regla']['falsable_si']}")
        if a["reserva"]:
            ls.append(f"  reserva: {a['reserva']}")
    for n in r["no_contesta"]:
        ls.append(f"\nNO CONTESTA · {n['razon']} · {n['detalle']}")
    ls.append(f"\n{r['terminos']}")
    return "\n".join(ls)


# ── verificar ──────────────────────────────────────────────────────────────
def verificar(llave: str) -> tuple[bool, list[str]]:
    ver, filas = catalogo()
    fila = next((f for f in filas if f["llave"] == llave), None) or \
        next((f for f in filas if f["result_id"] == llave), None)
    if fila is None:
        return False, [f"NO-ENCONTRADO · {llave} · catálogo {ver} · filas examinadas={len(filas)}"]
    d = CORRIDA / fila["calc"]
    pasos = [f"fila {fila['llave']} · catálogo {ver} · {fila['calc']}"]
    try:
        _, rh, sh = sellado(fila["calc"])
    except ValueError as e:
        return False, pasos + [str(e)]
    pasos.append(f"[1] sha256(sello.json)={sh} = sello.sha256 · OK")
    pasos.append(f"[2] sello.json[resultados.json]={rh} = sha256(resultados.json) · OK")
    s = resuelve_sellado(fila)
    if not iguales(s["punto"], fila["punto"]):
        return False, pasos + [f"CADENA-ROTA:valor · sellado {s['punto']} ≠ catálogo {fila['punto']}"]
    pasos.append(f"[3] valor sellado {s['punto']!r} = punto del catálogo · OK")
    h = hashes().get(fila["calc"])
    if h is None or h["sha256_resultados"] != rh or h["sha256_sello"] != sh:
        return False, pasos + ["CADENA-ROTA:calcs.tsv"]
    pasos.append("[4] hashes = forense/analisis/catalogo/v1_1/calcs.tsv · OK")
    faltan = [n for n in ("spec.yaml", "ejecucion.json") if not (d / n).exists()]
    if faltan:
        return False, pasos + [f"CADENA-ROTA:faltan {faltan}"]
    pasos.append(f"[5] spec.yaml sha256={sha(d / 'spec.yaml')} · ejecucion.json presente · OK")
    pasos.append("CADENA-VERIFICADA (no recalcula: `python3 tools/corrida0.py verify "
                 f"{fila['calc']}` necesita el corpus)")
    return True, pasos


# ── exporta ────────────────────────────────────────────────────────────────
COLS = ("llave", "dominio", "instrumento", "ola", "conducta", "eje", "segmento", "unidad",
        "punto", "ic95_inf", "ic95_sup", "naturaleza_ic", "temporalidad", "origen_piso",
        "estado_adopcion", "alcance", "firma_fp", "result_id", "celda", "calc",
        "oferta_exclusion", "reserva")
DICC = ("dominio", "instrumento", "ola", "conducta", "eje", "segmento", "unidad", "naturaleza_ic",
        "temporalidad", "origen_piso", "estado_adopcion", "alcance", "firma_fp", "calc",
        "oferta_exclusion", "reserva", "result_id")


def exporta_dict() -> dict:
    """Columnar con diccionarios: los valores numéricos viajan como el texto del catálogo.
    `llave` viaja vacía cuando es `result_id#celda` o `result_id` (se reconstruye)."""
    ver, filas = catalogo()
    dic = {c: [] for c in DICC}
    idx = {c: {} for c in DICC}
    filas_out = []
    for f in filas:
        fila = []
        for c in COLS:
            v = f[c]
            if c in DICC:
                if v not in idx[c]:
                    idx[c][v] = len(dic[c])
                    dic[c].append(v)
                fila.append(idx[c][v])
            elif c == "llave":
                derivable = v == (f"{f['result_id']}#{f['celda']}" if f["celda"].isdigit() else f["result_id"])
                fila.append("" if derivable else v)
            else:
                fila.append(v)
        filas_out.append(fila)
    reg = {}
    for f in filas:
        if f["alcance"] == "PARAMETRO-DE-REGLA" and f["segmento"] in reglas():
            r = reglas()[f["segmento"]]
            reg[r["id"]] = {"tier": r.get("tier"), "falsable_si": r.get("falsable_si")}
    return {
        "catalogo": ver, "contrato": "docs/consulta.md v1.0", "terminos": TERMINOS,
        "deriva": "python3 tools/benchmark.py exporta", "columnas": list(COLS),
        "diccionarios": dic, "filas": filas_out,
        "hashes": {c: [h["sha256_resultados"], h["sha256_sello"]] for c, h in hashes().items()},
        "reglas": reg, "ejes": {k: list(v) for k, v in EJES.items()},
        "olas_reservadas": sorted(f"{i} {o}" for i, o in olas_reservadas()),
        "cobertura": [{"dominio": c["dominio"], "estado": c["estado"], "report": c["report"]}
                      for c in lee(AUX / "cobertura-31.tsv")],
        "excluidos": [[e["llave"], e["calc"], e["causa"], norm(_etiqueta_excluida(e))]
                      for e in lee(AUX / "excluidos.tsv")],
    }


EJEMPLOS = [
    ("TRABAJO", "¿Qué proporción de las mujeres ocupadas tiene empleo informal en el último trimestre medido?",
     dict(conducta="empleo_informal", segmentos=["sexo=mujer"], ola="2025T4")),
    ("GÉNERO", "¿Cuántas mujeres con escolaridad superior declaran violencia en el ámbito laboral (ENDIREH 2021)?",
     dict(conducta="laboral", segmentos=["escolaridad=superior"])),
    ("TECNOLOGÍA", "¿Qué proporción de la población usa internet, a nivel nacional, en la ENDUTIH más reciente?",
     dict(conducta="internet", instrumento="ENDUTIH", ola="2025", segmentos=["nacional="])),
    ("DINERO", "¿Quién ahorra solo por vías informales (ENIF 2024), y qué se sabe de la oferta?",
     dict(conducta="ahorra_solo_informal")),
    ("SALUD", "¿Qué proporción de quienes tuvieron un problema de salud buscó atención, en el estrato rural (ENSANUT 2024)?",
     dict(conducta="busco-atencion", ola="2024", segmentos=["localidad=rural"])),
    ("LÍMITE", "¿Y el empleo en la ENOE 2026? (ola reservada: la consulta debe negarse con su razón)",
     dict(texto="empleo", instrumento="ENOE", ola="2026")),
]


def ejemplos_md() -> str:
    ver, _ = catalogo()
    out = ["---", "title: Ejemplos de consulta", "---", "",
           "# Ejemplos de consulta", "",
           "[Portada]({{ '/' | relative_url }}) · [Consultar]({{ '/consultar.html' | relative_url }}) · "
           "[Contrato]({{ '/consulta.html' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})", "",
           f"Cinco preguntas reales, una por dominio, más un límite. Todo lo de abajo es salida cruda de "
           f"`python3 tools/benchmark.py` sobre el catálogo `{ver}`; esta página se regenera con "
           "`python3 tools/benchmark.py ejemplos` y un test comprueba que no se desfasa. Ninguna cifra está tecleada.", ""]
    for i, (dom, pregunta, kw) in enumerate(EJEMPLOS, 1):
        args = []
        if kw.get("conducta"):
            args.append(f"--conducta {kw['conducta']}")
        if kw.get("texto"):
            args.append(f"--texto {kw['texto']}")
        args += [f"--segmento {s}" for s in kw.get("segmentos", [])]
        args += [f"--{k} {kw[k]}" for k in ("instrumento", "ola") if kw.get(k)]
        r = consulta(**kw, limite=None)
        out += [f"## {i} · {dom}", "", f"**Pregunta.** {pregunta}", "",
                "```", f"python3 tools/benchmark.py consulta {' '.join(args)}", "```", "", "```", humano(r), "```", ""]
        if r["respuestas"]:
            ok, pasos = verificar(r["respuestas"][0]["llave"])
            out += ["**Verificación** de la primera fila:", "", "```",
                    f"python3 tools/benchmark.py verificar '{r['respuestas'][0]['llave']}'", "", *pasos, "```", ""]
            assert ok, pasos
    out += ["**Cómo leerlos.** Todas las filas son RETROSPECTIVAS y descriptivas de su ola; el IC es el que declara "
            "`tipo_ic`. Un gradiente por localidad, escolaridad o formalidad se lee primero como estructura y oferta, "
            "no como cultura (§3 de las instrucciones)."]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("puntero")
    c = sp.add_parser("consulta")
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--conducta")
    g.add_argument("--texto")
    c.add_argument("--segmento", action="append", default=[])
    c.add_argument("--instrumento")
    c.add_argument("--ola")
    c.add_argument("--limite", type=int, default=20)
    c.add_argument("--json", action="store_true")
    v = sp.add_parser("verificar")
    v.add_argument("llave")
    sp.add_parser("ejemplos")
    e = sp.add_parser("exporta")
    e.add_argument("--salida")
    a = ap.parse_args(argv)

    if a.cmd == "puntero":
        ver, filas = catalogo()
        print(f"catalogo={ver} · archivo=canon/catalogo-del-mexicano-{ver}.tsv · filas={len(filas)}")
        return 0
    if a.cmd == "consulta":
        r = consulta(a.conducta, a.texto, a.segmento, a.instrumento, a.ola, a.limite or None)
        print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else humano(r))
        return 0 if r["n"] else 1
    if a.cmd == "verificar":
        ok, pasos = verificar(a.llave)
        print("\n".join(pasos))
        return 0 if ok else 1
    if a.cmd == "ejemplos":
        (RAIZ / "docs/ejemplos.md").write_text(ejemplos_md(), encoding="utf-8")
        print("escrito=docs/ejemplos.md")
        return 0
    ver, _ = catalogo()
    out = Path(a.salida) if a.salida else DOCS_DATA / f"catalogo-{ver}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(exporta_dict(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if not a.salida:
        (DOCS_DATA / "catalogo-vigente.json").write_text(
            json.dumps({"catalogo": ver, "archivo": out.name}, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"exportado={out.relative_to(RAIZ) if out.is_relative_to(RAIZ) else out} · bytes={out.stat().st_size} · sha256={sha(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
