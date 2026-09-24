#!/usr/bin/env python3
"""ASTRA5-U0 · ensambla el mapa canónico afirmación → pregunta → medición.

Entradas (todas en forense/analisis/dominios/ salvo el censo):
- mapa-parcial-v0_1.tsv: los 102 contratos cerrados por la sesión Codex (base, intactos).
- actualizaciones-contratos-v1_0.tsv: cambios explícitos a esos contratos (consumo de
  #1094 y #1098), cada uno con razón y evidencia; el ensamblador exige que el texto a
  sustituir exista exactamente una vez.
- complemento-base-v1_0.tsv: procedencia de evidencia y dominio de cada contrato base.
- lotes/<clave>-filas-v1_0.tsv y lotes/<clave>-cobertura-v1_0.tsv: dictamen por afirmación
  de cada archivo del censo (redactado por lote y auditado); las filas ENLACE sólo añaden
  procedencias a un contrato existente.
- fusiones-v1_0.tsv: deduplicación entre archivos (fila absorbida → fila canónica).
- resultado-por-afirmacion-v1_0.tsv: correspondencia exacta afirmación → RESULT.

Salidas:
- canon/mapa-dominios-v1_0.tsv (una fila por afirmación; ninguna PENDIENTE).
- proyeccion-cobertura-v1_0.tsv (por afirmación: medibilidad, autorización de apertura y
  existencia de RESULT, separadas) y proyeccion-dominios-v1_0.tsv (por dominio: fracción
  medida y pendientes).
- report-a-dominio-afirmaciones-v1_0.tsv (report × dominio, para ASTRA4-U1 y FRONT).
- cobertura-unidades-v1_0.tsv (cada unidad del censo → filas que la cubren o razón).

Uso: python3 forense/analisis/dominios/ensambla_mapa.py [--verifica]
Con --verifica no escribe: recalcula y compara byte a byte con lo publicado.
"""
from __future__ import annotations

import csv
import glob
import hashlib
import io
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "forense/analisis/dominios"
CANON = ROOT / "canon/mapa-dominios-v1_0.tsv"

COLS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "procedencias", "texto_vigente",
    "tier_report", "clase", "procedencia_evidencia", "componente_contrastable",
    "limite_inferencial", "falsador", "conducta_unidad_universo", "instrumento_ola",
    "documento_id_hash_pagina", "pregunta_textual_codigo_respuestas", "estado_verificacion",
    "dictamen", "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente", "propietario",
    "siguiente_operacion", "prioridad", "dominio", "busqueda_a13",
]
DICTAMENES = ("MEDIBLE-EN-CORPUS", "MEDIBLE-CON-ADQUISICIÓN", "NO-MEDIBLE-POR-DISEÑO")
LOTE_COLS = [
    "id_afirmacion", "fila_local", "unidades", "localizador", "texto_vigente", "tier_report", "clase",
    "procedencia_evidencia", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "dictamen", "dictamen_razon", "datos_id_estado",
    "reserva", "gen2_existente", "propietario_propuesto", "siguiente_operacion",
    "dedup_concepto", "contrato_existente", "busqueda_a13", "dominio", "falsador",
]


def lee(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def tsv(rows: list[list[str]]) -> str:
    out = io.StringIO()
    for r in rows:
        for c in r:
            if "\t" in c or "\n" in c or c.startswith('"'):
                raise SystemExit(f"campo inválido para TSV plano: {c[:80]!r}")
        out.write("\t".join(r) + "\n")
    return out.getvalue()


def ruta_de_clave() -> dict[str, dict]:
    return {r["clave"]: r for r in lee(D / "report-a-clave-v1_0.tsv")}


def prioridad(dictamen: str, tier: str, propietario: str) -> str:
    """1 = frente ASTRA5 activo con dato en corpus; 2 = medible en corpus con tier fuerte/sólido;
    3 = medible (corpus o adquisición) resto; 4 = no medible por diseño."""
    t = tier.upper()
    fuerte = any(k in t for k in ("FUERTE", "SÓLID", "SOLID"))
    if dictamen == "NO-MEDIBLE-POR-DISEÑO":
        return "4"
    if dictamen == "MEDIBLE-EN-CORPUS" and re.match(r"ASTRA5-U[1-4]\b", propietario):
        return "1"
    if dictamen == "MEDIBLE-EN-CORPUS" and fuerte:
        return "2"
    return "3"


def main(verifica: bool) -> int:
    claves = ruta_de_clave()
    base = lee(D / "mapa-parcial-v0_1.tsv")
    base_ids = [r["id_afirmacion"] for r in base]
    assert len(base_ids) == len(set(base_ids)) == 102, "la base Codex debe tener 102 contratos únicos"
    por_id = {r["id_afirmacion"]: dict(r) for r in base}

    # 1 · actualizaciones explícitas a la base
    for u in lee(D / "actualizaciones-contratos-v1_0.tsv"):
        fila = por_id[u["id_afirmacion"]]
        if u["operacion"] == "SUSTITUYE-TEXTO":
            n = fila[u["campo"]].count(u["buscar"])
            if n != 1:
                raise SystemExit(f"{u['id_afirmacion']}.{u['campo']}: texto a sustituir aparece {n} veces")
            fila[u["campo"]] = fila[u["campo"]].replace(u["buscar"], u["valor_nuevo"])
        elif u["operacion"] == "REEMPLAZA-CAMPO":
            fila[u["campo"]] = u["valor_nuevo"]
        else:
            raise SystemExit(f"operación desconocida {u['operacion']}")

    comp = {r["id_afirmacion"]: r for r in lee(D / "complemento-base-v1_0.tsv")}
    assert set(comp) == set(por_id), "complemento-base debe cubrir exactamente los 102 contratos"

    procedencias: dict[str, set[str]] = defaultdict(set)
    # fichas Codex que ya enlazaban contratos
    for f in sorted(D.glob("lectura-*.tsv")):
        for r in lee(f):
            for cid in re.findall(r"ASTRA5-U0-[A-Z]+-\d{3}", r.get("contrato_existente", "") or ""):
                procedencias[cid].add(r["id_lectura"])
            m = re.search(r"ASTRA5-U0-([A-Z]+)-(\d{3})\.\.(\d{3})", r.get("contrato_existente", "") or "")
            if m:
                for n in range(int(m.group(2)), int(m.group(3)) + 1):
                    procedencias[f"ASTRA5-U0-{m.group(1)}-{n:03d}"].add(r["id_lectura"])

    filas: list[dict] = []
    # 2 · lotes auditados
    cobertura: list[dict] = []
    for fl in sorted((D / "lotes").glob("*-filas-v1_0.tsv")):
        clave = fl.name[: -len("-filas-v1_0.tsv")]
        meta = claves[clave]
        rows = lee(fl)
        for r in rows:
            if set(r) != set(LOTE_COLS):
                raise SystemExit(f"{fl.name}: columnas inesperadas")
            unidades = [u for u in r["unidades"].split(";") if u.strip()]
            if r["clase"] == "ENLACE":
                for cid in re.findall(r"ASTRA5-U0-[A-Z]+-\d{3}", r["contrato_existente"]):
                    if cid not in por_id:
                        raise SystemExit(f"{fl.name}: ENLACE a contrato inexistente {cid}")
                    procedencias[cid].update(u.strip() for u in unidades)
                continue
            if r["dictamen"] not in DICTAMENES:
                raise SystemExit(f"{r['id_afirmacion']}: dictamen no cerrado {r['dictamen']!r}")
            prop = r["propietario_propuesto"]
            filas.append({
                "id_afirmacion": r["id_afirmacion"], "report": meta["ruta"],
                "report_sha256": meta["sha256"], "localizador": r["localizador"],
                "procedencias": ";".join(u.strip() for u in unidades), "texto_vigente": r["texto_vigente"],
                "tier_report": r["tier_report"], "clase": r["clase"],
                "procedencia_evidencia": r["procedencia_evidencia"],
                "componente_contrastable": r["componente_contrastable"],
                "limite_inferencial": r["limite_inferencial"], "falsador": r["falsador"],
                "conducta_unidad_universo": r["conducta_unidad_universo"],
                "instrumento_ola": r["instrumento_ola"],
                "documento_id_hash_pagina": r["documento_id_hash_pagina"],
                "pregunta_textual_codigo_respuestas": r["pregunta_textual_codigo_respuestas"],
                "estado_verificacion": "CERRADA", "dictamen": r["dictamen"],
                "dictamen_razon": r["dictamen_razon"], "datos_id_estado": r["datos_id_estado"],
                "reserva": r["reserva"], "gen2_existente": r["gen2_existente"], "propietario": prop,
                "siguiente_operacion": r["siguiente_operacion"],
                "prioridad": prioridad(r["dictamen"], r["tier_report"], prop),
                "dominio": r["dominio"], "busqueda_a13": r["busqueda_a13"],
            })
        cob = D / "lotes" / f"{clave}-cobertura-v1_0.tsv"
        for c in lee(cob):
            cobertura.append({"clave": clave, **c})

    # 3 · base Codex con procedencias, complemento y prioridad derivada
    for cid in base_ids:
        r = por_id[cid]
        extra = comp[cid]
        fila = {c: r.get(c, "") for c in COLS}
        fila["procedencias"] = ";".join(sorted(procedencias.get(cid, set()))) or extra["procedencias_minimas"]
        fila["procedencia_evidencia"] = extra["procedencia_evidencia"]
        fila["dominio"] = extra["dominio"]
        fila["falsador"] = extra["falsador"]
        fila["busqueda_a13"] = extra["busqueda_a13"]
        fila["prioridad"] = prioridad(r["dictamen"], r["tier_report"], r["propietario"])
        filas.append(fila)

    # 4 · fusiones entre archivos: la fila absorbida desaparece y sus procedencias pasan
    ids = {f["id_afirmacion"]: f for f in filas}
    fus_path = D / "fusiones-v1_0.tsv"
    absorbidas = {}
    if fus_path.exists():
        for fu in lee(fus_path):
            can, abs_ = fu["id_canonico"], fu["id_absorbido"]
            if can not in ids or abs_ not in ids:
                raise SystemExit(f"fusión con id inexistente: {can} ← {abs_}")
            a = ids[abs_]
            c = ids[can]
            c["procedencias"] = ";".join(sorted(set(c["procedencias"].split(";")) | set(a["procedencias"].split(";")) - {""}))
            c["localizador"] = c["localizador"] + f"; también {a['report'].split('/')[-1][:48]} {a['localizador']} ({abs_} fusionada)"
            absorbidas[abs_] = can
    filas = [f for f in filas if f["id_afirmacion"] not in absorbidas]

    # 5 · validaciones duras del mapa canónico
    vistos = Counter(f["id_afirmacion"] for f in filas)
    dup = [k for k, v in vistos.items() if v > 1]
    if dup:
        raise SystemExit(f"ids duplicados: {dup[:5]}")
    for f in filas:
        if f["estado_verificacion"] != "CERRADA" or f["dictamen"] not in DICTAMENES:
            raise SystemExit(f"{f['id_afirmacion']}: fila no cerrada")
        rep = ROOT / f["report"]
        if hashlib.sha256(rep.read_bytes()).hexdigest() != f["report_sha256"]:
            raise SystemExit(f"{f['id_afirmacion']}: sha del report no coincide")
    filas.sort(key=lambda f: (f["report"], f["id_afirmacion"]))

    salidas: dict[Path, str] = {}
    salidas[CANON] = tsv([COLS] + [[f[c] for c in COLS] for f in filas])

    # 6 · cobertura de unidades
    cob_rows = [["clave", "unidad", "tipo", "filas_o_contratos", "razon"]]
    for c in cobertura:
        destino = c["filas_o_contratos"]
        destino = ";".join(absorbidas.get(x, x) for x in destino.split(";") if x)
        cob_rows.append([c["clave"], c["unidad"], c["tipo"], destino, c.get("razon", "")])
    salidas[D / "cobertura-unidades-v1_0.tsv"] = tsv(cob_rows)

    # 7 · proyección: medibilidad, autorización y RESULT por separado
    res = {r["id_afirmacion"]: r for r in lee(D / "resultado-por-afirmacion-v1_0.tsv")}
    proy = [["id_afirmacion", "dominio", "report", "medibilidad", "autorizacion_apertura",
             "estado_result", "result_ids", "fecha_o_razon", "propietario"]]
    agg: dict[str, Counter] = defaultdict(Counter)
    reps: dict[str, set] = defaultdict(set)
    pend: dict[str, list] = defaultdict(list)
    for f in filas:
        rz = f["reserva"].upper()
        if "RESERVAD" in rz and "SIN RESERVA" not in rz:
            aut = "RESERVADA"
        elif any(k in rz for k in ("LICENCIA", "DERECHOS RESERVADOS", "RESTRING", "CLIC", "NO TRANSFERIBLE")):
            aut = "RESTRINGIDA-POR-LICENCIA"
        elif f["dictamen"] == "NO-MEDIBLE-POR-DISEÑO":
            aut = "NO-APLICA"
        else:
            aut = "SIN-RESERVA-IDENTIFICADA"
        rr = res.get(f["id_afirmacion"])
        if rr:
            est, rids, fecha = rr["estado_result"], rr["result_ids"], rr["fecha_o_razon"]
        else:
            est, rids = "SIN-RESULT", ""
            if f["dictamen"] == "NO-MEDIBLE-POR-DISEÑO":
                fecha = "no medible por diseño de los instrumentos recorridos"
            elif f["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN":
                fecha = "falta la pieza de adquisición indicada en el mapa"
            else:
                fecha = "medible en corpus; sin sesión de medición lanzada al corte (falta temporal de asignación, no defecto de diseño)"
        proy.append([f["id_afirmacion"], f["dominio"], f["report"], f["dictamen"], aut, est, rids, fecha, f["propietario"]])
        a = agg[f["dominio"]]
        a["n"] += 1
        a[f["dictamen"]] += 1
        a[est] += 1
        a[aut] += 1
        reps[f["dominio"]].add(f["report"].split("/")[-1])
        if est != "MEDIDO" and f["dictamen"] != "NO-MEDIBLE-POR-DISEÑO":
            pend[f["dominio"]].append(f["id_afirmacion"])
    salidas[D / "proyeccion-cobertura-v1_0.tsv"] = tsv(proy)
    dom = [["dominio", "afirmaciones", "medible_en_corpus", "medible_con_adquisicion",
            "no_medible_por_diseno", "medido", "en_medicion", "sin_result", "fraccion_medida",
            "reservadas", "reports", "pendientes_medibles"]]
    for d in sorted(agg):
        a = agg[d]
        dom.append([d, str(a["n"]), str(a["MEDIBLE-EN-CORPUS"]), str(a["MEDIBLE-CON-ADQUISICIÓN"]),
                    str(a["NO-MEDIBLE-POR-DISEÑO"]), str(a["MEDIDO"]), str(a["EN-MEDICIÓN"]),
                    str(a["SIN-RESULT"]), f"{a['MEDIDO']}/{a['n']}", str(a["RESERVADA"]),
                    str(len(reps[d])), ";".join(pend[d])])
    salidas[D / "proyeccion-dominios-v1_0.tsv"] = tsv(dom)

    # 8 · hoja de adquisición derivada del mapa (vocabulario del encargo), una fila por afirmación
    hoja = [["id_afirmacion", "dominio", "report", "estado_hoja", "existencia_documento", "pieza_o_razon",
             "instrumento_ola", "propietario", "prioridad"]]
    for f in filas:
        blob = " ".join([f["datos_id_estado"], f["dictamen_razon"], f["siguiente_operacion"]])
        if f["dictamen"] == "MEDIBLE-EN-CORPUS":
            estado, pieza = "REUTILIZAR", f["datos_id_estado"]
        elif f["dictamen"] == "NO-MEDIBLE-POR-DISEÑO":
            estado, pieza = "DESCARTAR-CON-RAZÓN", f["dictamen_razon"]
        else:
            m = re.search(r"faltante:\s*([^;]+)", blob, re.I)
            pieza = m.group(1).strip() if m else f["datos_id_estado"]
            dato = re.search(r"microdato|base de datos|\bdatos?\b|payload|encuesta|serie|tabulado|\bola\b", pieza, re.I)
            estado = "ADQUIRIR" if dato else "DOCUMENTACIÓN-SOLAMENTE"
        if "NO-ACCESIBLE-DESDE-SANDBOX" in blob.upper():
            existencia = "NO-ACCESIBLE-DESDE-SANDBOX"
        elif "EXISTENCIA-NO-COMPROBADA" in blob.upper():
            existencia = "NO-COMPROBADA"
        else:
            existencia = "COMPROBADA-O-NO-APLICA"
        hoja.append([f["id_afirmacion"], f["dominio"], f["report"], estado, existencia, pieza[:400],
                     f["instrumento_ola"][:200], f["propietario"], f["prioridad"]])
    salidas[D / "hoja-adquisicion-derivada-v1_0.tsv"] = tsv(hoja)

    rd = Counter((f["report"], f["dominio"]) for f in filas)
    rdr = [["report", "dominio", "afirmaciones"]] + [[r, d, str(n)] for (r, d), n in sorted(rd.items())]
    salidas[D / "report-a-dominio-afirmaciones-v1_0.tsv"] = tsv(rdr)

    difiere = []
    for p, txt in salidas.items():
        if verifica:
            if not p.exists() or p.read_text(encoding="utf-8") != txt:
                difiere.append(str(p.relative_to(ROOT)))
        else:
            p.write_text(txt, encoding="utf-8")
    c = Counter(f["dictamen"] for f in filas)
    print(f"mapa canónico: {len(filas)} afirmaciones · " + " · ".join(f"{k} {c[k]}" for k in DICTAMENES)
          + f" · fusionadas {len(absorbidas)} · unidades de cobertura {len(cob_rows) - 1}")
    if verifica and difiere:
        print("DIFIERE:", ", ".join(difiere))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifica" in sys.argv[1:]))
