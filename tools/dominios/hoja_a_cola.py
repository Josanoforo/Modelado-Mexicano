#!/usr/bin/env python3
"""ACTO GEN2-ASTRA5-U5-ADQUISICION-1 · P1+P2 · de la hoja de adquisición a la cola.

Entradas (todas versionadas):
- forense/analisis/dominios/hoja-adquisicion-derivada-v1_0.tsv (derivada por
  ensambla_mapa.py): sólo las filas estado_hoja=ADQUIRIR.
- tools/dominios/hoja_a_cola_reglas.tsv: tabla de reglas DECLARADA. Cada fila
  es una expresión regular sobre «instrumento_ola || pieza_o_razon»; gana la
  de menor `orden` que case. La regla 999 (`.`) es el defecto DOCUMENTO.
  Una regla con `olas` separadas por `;` reparte la afirmación en varias
  (instrumento, ola).
- tools/dominios/firma_astra5_2.tsv: las (instrumento, ola) que la firma de
  mesa F-ASTRA-5-2 pone primero (ENSANUT + ENCODAT y ENBIARE), con prioridad
  0; las afirmaciones del mapa que las requieren se derivan por `patron_mapa`
  sobre canon/mapa-dominios-v1_0.tsv, no se teclean.
- data/manifiesto.yaml: A.8 — una (instrumento, ola) cuyo payload ya está se
  asienta OBTENIDO con sus ids, no PENDIENTE.
- data/curacion-registro/cola-adquisicion-registro.tsv: una regla con
  `fuente_existente` apunta a una fila que ya está en la cola; no se duplica.

Salidas:
- filas MICRODATO del registro de la cola, clave `fila_origen` =
  `ASTRA5-U5:<INSTRUMENTO>_<OLA>` (escritor canónico `upsert_fila`);
- forense/analisis/dominios/constancias-v1_0.tsv: las (instrumento, ola)
  DOCUMENTO/TABULADO, que no entran a la cola de payloads.

Uso:
  python3 tools/dominios/hoja_a_cola.py            # deriva y reporta; no escribe (D-23)
  python3 tools/dominios/hoja_a_cola.py --escribe  # escribe registro + constancias
  python3 tools/dominios/hoja_a_cola.py --verifica # 0 si registro y constancias ya
                                                   # contienen exactamente lo derivado

Las filas ya escritas conservan su estado_A4A5, ids_manifiesto y nota cuando
/adquiere las haya caminado: --escribe sólo inserta filas que falten y nunca
reescribe una fila cuyo estado ya no sea el derivado (la cola es de /adquiere
desde que la fila nace). --verifica compara sólo las columnas que este script
gobierna (fuente, prioridad, url, origen).
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "curador_registro"))
from tsv_crudo import leer_dicts, upsert_fila  # noqa: E402

HOJA = ROOT / "forense/analisis/dominios/hoja-adquisicion-derivada-v1_0.tsv"
MAPA = ROOT / "canon/mapa-dominios-v1_0.tsv"
REGLAS = ROOT / "tools/dominios/hoja_a_cola_reglas.tsv"
FIRMA = ROOT / "tools/dominios/firma_astra5_2.tsv"
MANIFIESTO = ROOT / "data/manifiesto.yaml"
REGISTRO = ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv"
CONSTANCIAS = ROOT / "forense/analisis/dominios/constancias-v1_0.tsv"

CAMPOS_REGISTRO = ["fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
                   "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
                   "ids_manifiesto", "origen", "nota"]
GOBERNADAS = ["fuente_canonica", "fuente_canonica_normalizada", "prioridad",
              "url_conocida", "origen"]
CAMPOS_CONSTANCIA = ["id_constancia", "clase", "instrumento", "ola", "prioridad",
                     "afirmaciones", "url", "sha256", "archivo", "fecha", "estado"]
CLASES = ("MICRODATO", "TABULADO", "DOCUMENTO")
ACTO = "GEN2-ASTRA5-U5-ADQUISICION-1"


def lee_tsv(path: Path) -> list[dict]:
    csv.field_size_limit(10**9)
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, restval=""))


def clave(instrumento: str, ola: str) -> str:
    return re.sub(r"[^A-Z0-9-]+", "_", f"{instrumento}_{ola}".upper()).strip("_")


def limpio(texto: str) -> str:
    return re.sub(r"[\t\n\r]+", " ", texto).strip()


def ids_manifiesto() -> list[str]:
    return [e["id"] for e in yaml.safe_load(MANIFIESTO.read_text(encoding="utf-8"))
            if isinstance(e, dict) and "id" in e]


def clasifica(hoja: list[dict], reglas: list[dict]) -> list[tuple[dict, dict]]:
    """(fila, regla) por cada fila ADQUIRIR; la primera regla que casa, por orden."""
    reglas = sorted(reglas, key=lambda r: int(r["orden"]))
    compiladas = [(r, re.compile(r["patron"], re.I)) for r in reglas]
    salida = []
    for f in hoja:
        texto = f"{f['instrumento_ola']} || {f['pieza_o_razon']}"
        for r, rx in compiladas:
            if rx.search(texto):
                salida.append((f, r))
                break
        else:  # la regla 999 casa con todo: llegar aquí es un defecto de la tabla
            raise SystemExit(f"{f['id_afirmacion']}: ninguna regla casa (falta la regla por defecto)")
    return salida


def deriva() -> tuple[dict[str, dict], list[dict], dict]:
    hoja = [f for f in lee_tsv(HOJA) if f["estado_hoja"] == "ADQUIRIR"]
    reglas = lee_tsv(REGLAS)
    for r in reglas:
        if r["clase"] not in CLASES:
            raise SystemExit(f"regla {r['orden']}: clase {r['clase']!r} fuera de {CLASES}")
    manif = ids_manifiesto()
    manif_set = set(manif)
    existentes = {r["fuente_canonica"] for r in leer_dicts(REGISTRO)}

    grupos: dict[str, dict] = {}
    constancias: dict[str, dict] = {}
    ya_en_cola: dict[str, list[str]] = defaultdict(list)
    por_clase = defaultdict(int)
    for f, r in clasifica(hoja, reglas):
        por_clase[r["clase"]] += 1
        prio = int(f["prioridad"])
        if r["clase"] == "MICRODATO" and r["fuente_existente"]:
            if r["fuente_existente"] not in existentes:
                raise SystemExit(f"regla {r['orden']}: fuente_existente "
                                 f"{r['fuente_existente']!r} no está en el registro")
            ya_en_cola[r["fuente_existente"]].append(f["id_afirmacion"])
            continue
        for ola in r["olas"].split(";"):
            if r["clase"] == "MICRODATO":
                k = clave(r["instrumento"], ola)
                g = grupos.setdefault(k, {"instrumento": r["instrumento"], "ola": ola,
                                          "prioridad": prio, "afirmaciones": [],
                                          "url": r["url"], "propietario": r["propietario_dato"],
                                          "ids": [], "reserva": "", "firma": False,
                                          "notas": []})
                g["prioridad"] = min(g["prioridad"], prio)
                g["afirmaciones"].append(f["id_afirmacion"])
                g["url"] = g["url"] or r["url"]
                for i in filter(None, r["ids_manifiesto"].split(";")):
                    if i not in manif_set:
                        raise SystemExit(f"regla {r['orden']}: id {i!r} no está en el manifiesto")
                    if i not in g["ids"]:
                        g["ids"].append(i)
                if r["nota"] and r["nota"] not in g["notas"]:
                    g["notas"].append(r["nota"])
            else:
                if r["instrumento"] == "DOC":
                    k = f"DOC-{f['id_afirmacion']}"
                    inst, o = limpio(f["instrumento_ola"])[:160] or limpio(f["pieza_o_razon"])[:160], "SIN-OLA"
                else:
                    k, inst, o = clave(r["instrumento"], ola), r["instrumento"], ola
                c = constancias.setdefault(k, {"id_constancia": k, "clase": r["clase"],
                                               "instrumento": inst, "ola": o,
                                               "prioridad": prio, "afirmaciones": [],
                                               "url": r["url"]})
                c["prioridad"] = min(c["prioridad"], prio)
                c["afirmaciones"].append(f["id_afirmacion"])

    # P2 · firma F-ASTRA-5-2: prioridad 0, afirmaciones derivadas del mapa
    mapa = lee_tsv(MAPA)
    for r in lee_tsv(FIRMA):
        rx = re.compile(r["patron_mapa"], re.I)
        citadas = [m["id_afirmacion"] for m in mapa
                   if rx.search(" ".join([m["instrumento_ola"], m["datos_id_estado"],
                                          m["siguiente_operacion"], m["dictamen_razon"]]))]
        k = clave(r["instrumento"], r["ola"])
        g = grupos.setdefault(k, {"instrumento": r["instrumento"], "ola": r["ola"],
                                  "prioridad": int(r["prioridad"]), "afirmaciones": [],
                                  "url": r["url"], "propietario": r["propietario_dato"],
                                  "ids": [], "reserva": "", "firma": True, "notas": []})
        g["firma"] = True
        g["prioridad"] = min(g["prioridad"], int(r["prioridad"]))
        g["url"] = r["url"] or g["url"]
        g["reserva"] = r["reserva"]
        g["citadas_mapa"] = citadas
        if r["ids_patron"]:
            rxi = re.compile(r["ids_patron"])
            for i in manif:
                if rxi.search(i) and i not in g["ids"]:
                    g["ids"].append(i)
        if r["nota"]:
            g["notas"].append(r["nota"])

    filas: dict[str, dict] = {}
    for k, g in sorted(grupos.items()):
        origen = []
        if g["firma"]:
            cit = g.get("citadas_mapa", [])
            origen.append("F-ASTRA-5-2 (firma de mesa, verbatim en forense/encargos/"
                          "2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md §2); mapa: "
                          + (";".join(cit) if cit else "NINGUNA afirmación del mapa la nombra: "
                             "se adquiere por firma"))
        if g["afirmaciones"]:
            origen.append("ASTRA5-U0 " + ";".join(g["afirmaciones"]))
        estado = "OBTENIDO" if g["ids"] else "PENDIENTE"
        nota = [f"{ACTO} P1/P2 (hoja_a_cola.py): {g['instrumento']} ola {g['ola']}, "
                f"propietario {g['propietario'] or 'sin identificar'}."]
        if g["ids"]:
            nota.append("A.8: ya estaba en el manifiesto, no se repitió (2026-09-24).")
        if g["reserva"]:
            nota.append("Ola más reciente publicada: nace RESERVADA al entrar al manifiesto "
                        "(E.6; F-ASTRA-5-3); bajar y hashear no es abrir.")
        nota += g["notas"]
        filas[k] = {
            "fila_origen": f"ASTRA5-U5:{k}",
            "fuente_canonica": k,
            "fuente_canonica_normalizada": k,
            "discordancia_alias": "SIN_ALIAS",
            "estado_A4A5": estado,
            "prioridad": str(g["prioridad"]),
            "url_conocida": g["url"],
            "ids_manifiesto": ";".join(g["ids"]),
            "origen": limpio(" · ".join(origen)),
            "nota": limpio(" ".join(nota)),
        }
    choque = sorted(k for k in filas if k in existentes
                    and not any(r["fila_origen"] == f"ASTRA5-U5:{k}" for r in leer_dicts(REGISTRO)))
    if choque:
        raise SystemExit(f"fuente_canonica ya usada por otra fila del registro: {choque}")

    const = []
    for k, c in sorted(constancias.items()):
        const.append({"id_constancia": k, "clase": c["clase"], "instrumento": c["instrumento"],
                      "ola": c["ola"], "prioridad": str(c["prioridad"]),
                      "afirmaciones": ";".join(c["afirmaciones"]), "url": c["url"],
                      "sha256": "", "archivo": "", "fecha": "",
                      "estado": "IDENTIFICADA-SIN-COPIA"})
    resumen = {"adquirir": len(hoja), "por_clase": dict(por_clase),
               "microdato_desde_hoja": sum(1 for g in grupos.values() if g["afirmaciones"]),
               "desde_firma": sum(1 for g in grupos.values() if g["firma"]),
               "filas": len(filas), "constancias": len(const),
               "ya_en_cola": dict(ya_en_cola)}
    return filas, const, resumen


def tsv_constancias(const: list[dict]) -> str:
    buf = io.StringIO()
    buf.write("\t".join(CAMPOS_CONSTANCIA) + "\n")
    for c in const:
        buf.write("\t".join(limpio(c[k]) for k in CAMPOS_CONSTANCIA) + "\n")
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--escribe", action="store_true")
    g.add_argument("--verifica", action="store_true")
    a = ap.parse_args()

    filas, const, res = deriva()
    print(f"ADQUIRIR={res['adquirir']} · por clase {res['por_clase']} · "
          f"(instrumento, ola) MICRODATO desde la hoja={res['microdato_desde_hoja']} · "
          f"desde F-ASTRA-5-2={res['desde_firma']} · filas de cola={res['filas']} · "
          f"constancias={res['constancias']}")
    for fuente, ids in sorted(res["ya_en_cola"].items()):
        print(f"  ya en cola (no se duplica): {fuente} <- {';'.join(ids)}")
    for k, f in filas.items():
        print(f"  {f['fila_origen']}\tprio={f['prioridad']}\t{f['estado_A4A5']}")

    registro = {r["fila_origen"]: r for r in leer_dicts(REGISTRO)}
    if a.verifica:
        mal = []
        for k, f in filas.items():
            r = registro.get(f["fila_origen"])
            if r is None or any(r[c] != f[c] for c in GOBERNADAS):
                mal.append(f["fila_origen"])
        sobra = [k for k in registro if k.startswith("ASTRA5-U5:")
                 and k not in {f["fila_origen"] for f in filas.values()}]
        texto = CONSTANCIAS.read_text(encoding="utf-8") if CONSTANCIAS.exists() else ""
        con_ok = _constancias_compatibles(texto, const)
        if mal or sobra or not con_ok:
            print(f"DIFIERE: registro={mal} sobrantes={sobra} constancias_ok={con_ok}")
            return 1
        print("VERIFICA: registro y constancias contienen exactamente lo derivado")
        return 0
    if a.escribe:
        nuevas = 0
        for k, f in filas.items():
            r = registro.get(f["fila_origen"])
            if r is None:
                upsert_fila(REGISTRO, f, CAMPOS_REGISTRO)
                nuevas += 1
            elif any(r[c] != f[c] for c in GOBERNADAS):
                # la fila ya existe y la cola es de /adquiere: sólo se reescriben
                # las columnas que este script gobierna
                nueva = dict(r)
                nueva.update({c: f[c] for c in GOBERNADAS})
                upsert_fila(REGISTRO, nueva, CAMPOS_REGISTRO)
        if not CONSTANCIAS.exists() or not _constancias_compatibles(
                CONSTANCIAS.read_text(encoding="utf-8"), const):
            CONSTANCIAS.write_text(tsv_constancias(const), encoding="utf-8")
        print(f"ESCRITO: {nuevas} fila(s) nuevas en {REGISTRO.relative_to(ROOT)}; "
              f"{len(const)} constancias en {CONSTANCIAS.relative_to(ROOT)}")
    return 0


def _constancias_compatibles(texto: str, const: list[dict]) -> bool:
    """Las columnas derivadas coinciden; sha256/archivo/fecha/estado son de quien baje la copia."""
    if not texto:
        return False
    rows = list(csv.DictReader(io.StringIO(texto), delimiter="\t", quoting=csv.QUOTE_NONE))
    fijas = ["id_constancia", "clase", "instrumento", "ola", "prioridad", "afirmaciones", "url"]
    return [[r[c] for c in fijas] for r in rows] == [[limpio(c[k]) for k in fijas] for c in const]


if __name__ == "__main__":
    sys.exit(main())
