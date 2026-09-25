#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P1 · catálogo de microdatos por comando.

Entradas (todas versionadas en este directorio o en el repo):
- crudo/inegi-descargamasiva-tipodocto4-*.json: el catálogo INEGI completo de microdatos,
  paginado por comando desde
  https://www.inegi.org.mx/app/api/descarga/componente/descargamasiva/lista/archivoscompaginacion
  (tipodocto=4, idBiinegi=0, páginas de 200; la última página vacía cierra la paginación).
- crudo/externos-inventario.tsv: el inventario por comando de las fuentes no INEGI.
- data/manifiesto.yaml: A.8 — un archivo del catálogo cuyo tronco de ruta ya está en un
  `url_origen` o `archivo` del manifiesto se marca `en_manifiesto=SI` y no se vuelve a bajar.
- canon/mapa-dominios-v1_0.tsv: prioridad = número de afirmaciones MEDIBLE-CON-ADQUISICIÓN
  que nombran el programa (patrón por programa en PATRON_MAPA, sobre instrumento_ola,
  datos_id_estado, dictamen_razon y siguiente_operacion).

Regla de reserva (E.6, F-ASTRA-5-3, decisiones.tsv reserva:ola-nueva-de-encuesta-con-historia):
un programa «con historia en el corpus» es el que ya tiene >=1 payload en el manifiesto
ANTES de este acto; su ola más reciente del catálogo, si no está ya en el manifiesto,
nace RESERVADA. Las olas históricas se abren. Un programa sin historia no reserva nada.

Salida: catalogo-v1_0.tsv (una fila por archivo del catálogo).
Uso:  python3 forense/analisis/corpus-completo/catalogo.py [--verifica]
"""
from __future__ import annotations

import csv
import glob
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "forense/analisis/corpus-completo"
SALIDA = D / "catalogo-v1_0.tsv"
INEGI = "https://www.inegi.org.mx"
LIC_INEGI = "Términos de Libre Uso de la Información del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
# orden de preferencia de formato: uno basta para el corpus (formato alterno, /adquiere §3.iii)
PREF = ["_csv.zip", "_dta.zip", "_sav.zip", "_dbf.zip", "_txt.zip", "_sas.zip", "_xlsx.zip", "_xls.zip"]
# alias de programa para contar afirmaciones del mapa; el resto usa la sigla del slug
PATRON_MAPA = {
    "ccpv": r"\bcenso de poblaci|\bCPV ?\d{4}|\bcenso (19|20)\d\d\b|\bcensal\b",
    "eic": r"\bintercensal 2025|\bEIC ?2025",
    "intercensal": r"\bintercensal 2015|\bEIC ?2015|\bintercensal\b",
    "biare": r"\bBIARE\b(?! b)|bienestar autorreportado",
    "enbiare": r"\bENBIARE\b",
    "dutih": r"\bENDUTIH\b|\bMODUTIH\b",
    "enigh": r"\bENIGH\b|ingreso y gasto de los hogares",
    "ce": r"\bcensos? econ[oó]mic",
    "mociba": r"\bMOCIBA\b|ciberacoso",
    "enoe": r"\bENOE\b|ocupaci[oó]n y empleo",
    "enadid": r"\bENADID\b|din[aá]mica demogr",
}


def lee_json_inegi() -> list[dict]:
    vistos, filas = set(), []
    for f in sorted(glob.glob(str(D / "crudo/inegi-descargamasiva-tipodocto4-*.json"))):
        for r in json.load(open(f, encoding="utf-8")):
            if r["idArchivo"] in vistos:
                continue
            vistos.add(r["idArchivo"])
            filas.append(r)
    return filas


def ola_de(r: dict) -> str:
    anios = [a for a in r["anioInformacion"].split("|") if a.strip()]
    base = anios[0].strip() if anios else ""
    p = r["pathLogico"]
    m = re.search(r"((?:19|20)\d\d)_?trim_?(\d)", p, re.I)
    if m:
        return f"{m.group(1)}T{m.group(2)}"
    if not base:
        m = re.search(r"(?:19|20)\d\d", p)
        base = m.group(0) if m else "SIN-AÑO"
    return base


def elige_formato(formato: str) -> tuple[str, str, str]:
    partes = [x.split("&") for x in formato.split("|") if x.strip()]
    por_suf = {x[0].strip(): (x[1].strip() if len(x) > 1 else "") for x in partes}
    for s in PREF:
        if s in por_suf:
            return s, por_suf[s], ";".join(por_suf)
    if por_suf:
        s = next(iter(por_suf))
        return s, por_suf[s], ";".join(por_suf)
    return "", "", ""


def manifiesto() -> list[dict]:
    # las entradas `cc1_*` las registra este mismo acto (P2): el catálogo es el estado ANTES del acto
    return [e for e in yaml.safe_load((ROOT / "data/manifiesto.yaml").read_text(encoding="utf-8"))
            if isinstance(e, dict) and "id" in e and not str(e["id"]).startswith("cc1_")]


def mapa_adq() -> list[str]:
    csv.field_size_limit(10**9)
    with (ROOT / "canon/mapa-dominios-v1_0.tsv").open(encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    return [(m["id_afirmacion"], " ".join([m["instrumento_ola"], m["datos_id_estado"],
                                         m["dictamen_razon"], m["siguiente_operacion"]]))
            for m in filas if m["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN"]


def patron(programa: str) -> re.Pattern:
    if programa in ("sin-programa", ""):
        return re.compile(r"(?!)")
    return re.compile(PATRON_MAPA.get(programa, rf"\b{re.escape(programa)}\b"), re.I)


def deriva() -> str:
    man = manifiesto()
    textos_man = [(e.get("url_origen") or "") + " " + (e.get("archivo") or "") for e in man]
    blob_man = "\n".join(textos_man).lower()
    mapa = mapa_adq()
    filas = []
    for r in lee_json_inegi():
        p = r["pathLogico"]
        partes = p.strip("/").split("/")
        prog = partes[1].lower() if len(partes) > 1 and partes[0] == "programas" else partes[0].lower()
        if not prog:  # entrada que sólo trae `url` a una ficha o página, sin pathLogico
            m = re.search(r"/(?:investigacion|programas)/([a-z0-9]+)/", r["url"]) if r["url"] else None
            prog = m.group(1) if m else "sin-programa"
        suf, tam, formatos = elige_formato(r["formato"])
        if r["url"]:
            url = r["url"] if r["url"].startswith("http") else INEGI + r["url"]
            clase = "PAGINA"
        else:
            url = f"{INEGI}/contenidos{p}{suf}"
            clase = "ARCHIVO"
        tronco = p.rstrip("/").split("/")[-1].lower()
        en_man = "SI" if clase == "ARCHIVO" and (f"{p.lower()}_" in blob_man
                                                or f"/{tronco}_" in blob_man) else "NO"
        filas.append({"fuente": "INEGI", "programa": prog.upper(), "ola": ola_de(r),
                      "id_archivo": r["idArchivo"], "titulo": re.sub(r"\s+", " ", r["titulo"].replace("|", " · ")).strip(),
                      "clase": clase, "url": url, "formato_elegido": suf, "formatos": formatos,
                      "tamano": tam, "licencia": LIC_INEGI, "en_manifiesto": en_man})
    ext = D / "crudo/externos-inventario.tsv"
    if ext.exists():
        with ext.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
                url = r["url"].strip()
                arch = (r.get("archivo") or "").strip()
                en_man = "SI" if (url and url.lower() in blob_man) or (arch and f"/{arch.lower()}" in blob_man) else "NO"
                filas.append({"fuente": "EXTERNO", "programa": r["programa"].strip().upper(),
                              "ola": r["ola"].strip(), "id_archivo": arch, "titulo": arch,
                              "clase": "ARCHIVO" if re.search(r"\.(zip|dta|sav|csv|rar|7z|xlsx?)$", url, re.I) else "PAGINA",
                              "url": url, "formato_elegido": r.get("formato", ""), "formatos": r.get("formato", ""),
                              "tamano": r.get("tamano", ""), "licencia": r.get("licencia_acceso", ""),
                              "en_manifiesto": en_man})
    # prioridad por programa: afirmaciones del mapa que lo nombran
    progs = sorted({f["programa"] for f in filas})
    citas = {p: [i for i, t in mapa if patron(p.lower()).search(t)] for p in progs}
    # historia (programa con >=1 payload en el manifiesto) y presencia de cada ola
    def rx_prog(p: str) -> re.Pattern:
        return re.compile(rf"(?:^|[^a-z]){re.escape(p.lower())}(?:[^a-z]|$)")
    man_txt = [((e.get("id") or "") + " " + (e.get("url_origen") or "") + " " + (e.get("archivo") or "")).lower()
               for e in man]
    man_res = [bool(e.get("estado_reserva")) for e in man]
    con_historia = {f["programa"] for f in filas if f["en_manifiesto"] == "SI"}
    for p in progs:
        if len(p) >= 3 and p != "SIN-PROGRAMA" and any(rx_prog(p).search(t) for t in man_txt):
            con_historia.add(p)

    def ola_en_manifiesto(p: str, ola: str) -> tuple[bool, bool]:
        """(presente, reservada) de la ola `ola` del programa `p` en el manifiesto, por texto."""
        if len(p) < 3:
            return False, False
        rp = rx_prog(p)
        m = re.match(r"((?:19|20)\d\d)(?:T(\d))?$", ola)
        if not m:
            return False, False
        anio, q = m.group(1), m.group(2)
        rq = re.compile(rf"{anio}[_-]?(?:t|trim|_trim)[_-]?{q}\b|{anio}{q}t\b") if q else None
        hit = [i for i, t in enumerate(man_txt) if rp.search(t) and anio in t and (rq is None or rq.search(t))]
        return bool(hit), any(man_res[i] for i in hit)
    olas = defaultdict(set)
    for f in filas:
        if f["clase"] == "ARCHIVO" and re.match(r"(19|20)\d\d", f["ola"]):
            olas[f["programa"]].add(f["ola"])
    for f in filas:
        p = f["programa"]
        f["prioridad"] = str(len(citas[p]))
        f["afirmaciones_mapa"] = ";".join(citas[p][:40]) + (";…" if len(citas[p]) > 40 else "")
        reciente = max(olas[p]) if olas[p] else ""
        f["historia_en_corpus"] = "SI" if p in con_historia else "NO"
        f["ola_mas_reciente"] = reciente
        presente, reservada = ola_en_manifiesto(p, f["ola"]) if f["ola"] == reciente else (False, False)
        if f["en_manifiesto"] == "SI":
            f["reserva_al_entrar"] = "YA-EN-MANIFIESTO"
        elif p in con_historia and f["ola"] == reciente and (reservada or not presente):
            # ola nueva (sin payload previo) o ya reservada: nace RESERVADA
            f["reserva_al_entrar"] = "RESERVADA"
        else:
            f["reserva_al_entrar"] = "ABIERTA"
    cols = ["fuente", "programa", "ola", "id_archivo", "titulo", "clase", "url", "formato_elegido",
            "formatos", "tamano", "licencia", "en_manifiesto", "prioridad", "historia_en_corpus",
            "ola_mas_reciente", "reserva_al_entrar", "afirmaciones_mapa"]
    filas.sort(key=lambda f: (-int(f["prioridad"]), f["fuente"], f["programa"], f["ola"], f["id_archivo"]))
    out = io.StringIO()
    out.write("# GENERADO por forense/analisis/corpus-completo/catalogo.py — no editar\n")
    out.write("\t".join(cols) + "\n")
    for f in filas:
        out.write("\t".join(re.sub(r"[\t\r\n]+", " ", str(f[c])) for c in cols) + "\n")
    return out.getvalue()


def main() -> int:
    texto = deriva()
    if "--verifica" in sys.argv:
        ok = SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == texto
        print("COINCIDE" if ok else "DIFIERE")
        return 0 if ok else 1
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"escrito {SALIDA.relative_to(ROOT)}: {texto.count(chr(10)) - 2} filas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
