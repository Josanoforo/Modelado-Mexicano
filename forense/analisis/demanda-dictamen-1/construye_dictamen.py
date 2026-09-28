#!/usr/bin/env python3
"""ACTO GEN2-DEMANDA-DICTAMEN-1 · construye data/corrida0/demanda-dictamen-v1_0.tsv.

Lee (nunca escribe) la demanda de apertura derivada por `corrida0 demanda`
(copias en --entrada), los registros vivos y las firmas, y dictamina cada
RESULT y cada corrida con vocabulario cerrado (ver VOCAB). Cada dictamen
lleva `cita` a archivo:línea o id. No abre microdato.
Uso: python3 construye_dictamen.py --entrada <dir con demanda-*.tsv> [--escribe]
"""
import argparse, csv, re, sys
from pathlib import Path
import yaml

RAIZ = Path(__file__).resolve().parents[3]
SALIDA = RAIZ / "data/corrida0/demanda-dictamen-v1_0.tsv"

# Vocabulario cerrado, declarado antes de usarse (encargo §1 + §6 latitud).
# cierra_corrida: la corrida ya no se necesita por este RESULT.
# cierra_resultado: el RESULT deja de contarse como pendiente (sale por dictamen).
VOCAB = {
    "YA-RELEVADO-GEN2":              (True, True),
    "NO-RELEVAR-POR-REGLA-6":        (True, True),
    "NO-RELEVAR-θ":                  (True, True),
    "NO-RELEVAR-GENERADOR":          (True, True),
    "NO-RELEVAR-POR-FIRMA":          (True, True),
    "SIN-ESTIMANDO-RECONSTRUIBLE":   (True, True),
    "DIFERIDO-A-FAMILIAS-2027":      (True, True),
    "RELEVAR-DESDE-RESULT":          (True, False),
    "RELEVAR-COMO-PISO-DESCRIPTIVO": (True, False),
    "CELDA-D-ADJUDICADA":            (True, False),
    "CELDA-D-SIN-CHAMPION":          (True, False),
    "SIN-BASE-GEN2":                 (True, False),
    "ESPERA-FIRMA-HOLDOUT":          (True, False),
    "ESPERA-FIRMA-MESA":             (True, False),
    "SIN-PAYLOAD-EN-CORPUS":         (False, False),
    "DECIDIBLE":                     (False, False),
    "EN-CURSO":                      (False, False),
}
P = "milpa/procedencia.yaml"
def _gemelo(regla):
    ln = linea(P, f"- regla: {regla}")
    return f"{P}:{ln + 1} gemelo en asignados_probabilidad (- regla: {regla}) rotulo_relevo=ASIGNADO-CONSERVADO-H1 (FP e760-01, regla B1)"
L8 = "data/corrida0/CALC-L8-CONVERSION-0001/resultados.json"
_L8 = lambda k: (
    "RELEVAR-DESDE-RESULT",
    f"{L8}: RESULT-L8CONV-A-P-{k} (REPRODUCE-GEN1, delta 0.0; RESULT-L8CONV-A-ADOPCION=LISTADO-PARA-MESA-REPRODUCE); milpa/tramite.yaml:{linea('milpa/tramite.yaml', 'conducta: participa_p0_' + k.lower())}",
    "mesa (adopción listada) → pin en usos por el canal")
A1 = ("forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md letra A1; "
      "FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-01 ABIERTA")
_manual = lambda: {
    "RES-0001": ("SIN-BASE-GEN2", _gemelo("tramite.mordida.discrecional") + "; el hermano medido es SOLICITUD, no PAGO", "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0002": ("SIN-BASE-GEN2", _gemelo("tramite.mordida.discrecional") + "; complemento de RES-0001", "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0007": ("SIN-BASE-GEN2", _gemelo("tramite.mordida.con_registro") + "; el hermano medido es SOLICITUD, no PAGO", "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0008": ("SIN-BASE-GEN2", _gemelo("tramite.mordida.con_registro"), "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0017": ("SIN-BASE-GEN2", _gemelo("tramite.gobierno_digital.coercitivo") + "; sin conducta GEN2 de coercitivo (NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-02)", "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0018": ("SIN-BASE-GEN2", _gemelo("tramite.gobierno_digital.coercitivo") + "; complemento de RES-0017", "GEN2-RELEVO-CONSUMIDORES-4"),
    "RES-0023": ("ESPERA-FIRMA-MESA", f"milpa/tramite.yaml:{linea('milpa/tramite.yaml', 'conducta: evade_norma')} ASIGNADO; su momento es M05; {A1}", "GEN2-TRAMITE-FIRMAS-21 (A1)"),
    "RES-0024": ("ESPERA-FIRMA-MESA", f"milpa/tramite.yaml:{linea('milpa/tramite.yaml', 'conducta: cumple_norma')} ASIGNADO, complemento de RES-0023; {A1}", "GEN2-TRAMITE-FIRMAS-21 (A1)"),
    "RES-0029": ("ESPERA-FIRMA-MESA", f"milpa/tramite.yaml:{linea('milpa/tramite.yaml', 'conducta: tiene_ahorros,')} MEDIDO sin corrida0_resultado_id; payload olas 2-3 de ENNViH (ennvih2_2005_hogar_dta, ennvih3_2009_hogar_dta, ennvih2_2005_ponderador_transversal: 3/3 en data/manifiesto.yaml, 7198 ids examinados); ola 3 (2009) es la más reciente del programa → reservada (canon/MEMORIA-OPERATIVA.md:9); bifurcación B1 de la hoja", "GEN2-TRAMITE-FIRMAS-22 (B1)"),
    "RES-0030": ("ESPERA-FIRMA-MESA", "complemento de RES-0029; misma bifurcación B1 de la hoja (ola 3 de ENNViH reservada)", "GEN2-TRAMITE-FIRMAS-22 (B1)"),
    "RES-0050": _L8("MINIMO"), "RES-0051": _L8("MAXIMO"), "RES-0052": _L8("MEDIA"),
}
COLS = ["corrida_id", "resultado_id", "dictamen", "cita", "sucesor"]

REGLA6 = ("gobierno/PEGAR-EN-PROYECTO-v2_17.md:63 + canon/MEMORIA-OPERATIVA.md:10 "
          "(regla 6: sin retadores, pilotos ni duelos sobre olas vistas)")
THETA = ("gobierno/instrucciones-proyecto-v2_16.md §4 (θ y matriz.g generan "
         "retadores, no emiten) + " + REGLA6)
H3 = ("firma H3 (FIRMAS-18, FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-03): "
      "«HISTÓRICO-SIN-RELEVO las 42 lecturas L/AGREGADO de marco-M-sorteado-v1_3»")


def lee_tsv(p):
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")),
                                   delimiter="\t"))


def linea(ruta, patron, desde=1):
    """Primera línea (1-based) >= desde que contiene `patron`; 0 si no."""
    for i, l in enumerate((RAIZ / ruta).read_text(encoding="utf-8").splitlines(), 1):
        if i >= desde and patron in l:
            return i
    return 0


def gen2_en_tramite(regla_id, conducta):
    """(línea, RESULT) si la conducta de la regla declara corrida0_generacion GEN2."""
    lin = (RAIZ / "milpa/tramite.yaml").read_text(encoding="utf-8").splitlines()
    ini = linea("milpa/tramite.yaml", f"id: {regla_id}")
    if not ini:
        return None
    for i in range(ini, len(lin)):
        if i > ini and lin[i].lstrip().startswith("- id:"):
            return None
        if re.search(rf"conducta: {re.escape(conducta)}(\b|,)", lin[i]):
            j = i + 1
            while j < len(lin) and j < i + 12 and not lin[j].lstrip().startswith("- "):
                j += 1
            bloque = " ".join(lin[i:j])
            if "rol_uso: historico" in bloque:
                return i + 1, "HISTORICO"
            m = re.search(r"corrida0_resultado_id: (RESULT-[A-Z0-9-]+)", bloque)
            if m and "corrida0_generacion: GEN2" in bloque:
                return i + 1, m.group(1)
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--escribe", action="store_true")
    a = ap.parse_args()
    ent = Path(a.entrada)
    res = lee_tsv(ent / "demanda-resultados.tsv")
    cor = lee_tsv(ent / "demanda-corridas.tsv")
    usos = {r["resultado_id"]: r for r in lee_tsv(RAIZ / "data/corrida0/usos.tsv")}
    man = {e.get("id") for e in yaml.safe_load(
        (RAIZ / "data/manifiesto.yaml").read_text(encoding="utf-8")) if isinstance(e, dict)}
    corr_de = {r["resultado_id"]: r["corrida_natural"] for r in res}
    ent_de = {c["corrida_id"]: c for c in cor}
    momentos = {r["id_momento"]: r for r in lee_tsv(RAIZ / "milpa/catalogo-momentos-v0_1.tsv")}
    dict_res = {}
    MANUAL = _manual()

    def pon(rid, d, cita, suc):
        assert d.split(" ")[0] in VOCAB, d
        assert cita, rid
        dict_res[rid] = (d, cita, suc)

    for r in res:
        rid, tipo, cons = r["resultado_id"], r["tipo"], r["consumidor"]
        u = usos.get(rid, {})
        c = ent_de[r["corrida_natural"]]
        # (0) ya leído GEN2 por el consumidor (vista usos.tsv, derivada por el canal)
        if u.get("generacion_leida") == "GEN2" and u.get("corrida0_resultado_id"):
            pon(rid, "YA-RELEVADO-GEN2",
                f"data/corrida0/usos.tsv:{rid} generacion_leida=GEN2 "
                f"corrida0_resultado_id={u['corrida0_resultado_id']} via={u.get('via_relevo') or 'NO-DECLARADA'}",
                "NINGUNO (relevado)")
            continue
        if cons.startswith("milpa/tramite.yaml:"):
            _, regla, conducta = cons.split(":", 2)
            g = gen2_en_tramite(regla, conducta)
            if g and g[1] == "HISTORICO":
                pon(rid, "NO-RELEVAR-POR-FIRMA",
                    f"milpa/tramite.yaml:{g[0]} rol_uso: historico (uso_motor NO-ADOPTAR-NC-0107); firma B2 FP-260924-GEN2-RELEVO-MOTOR-34-1-a157-02 (rol_uso historico sale del consumo vivo); tools/corrida0.py:{linea('tools/corrida0.py', 'ROL_HISTORICO = ')}",
                    "NINGUNO (histórico)")
                continue
            if g:
                pon(rid, "YA-RELEVADO-GEN2",
                    f"milpa/tramite.yaml:{g[0]} corrida0_resultado_id={g[1]} corrida0_generacion=GEN2 "
                    f"(usos.tsv aún no lo refleja: {u.get('generacion_leida', 'SIN-FILA')})",
                    "canal [deriva] (usos.tsv se regenera)")
                continue
        if rid in MANUAL:
            pon(rid, *MANUAL[rid])
            continue
        # (P2) duelo v2
        if tipo in ("celda_L", "celda_AGREGADO", "celda_M", "celda_R"):
            celda = cons.split(":")[1]
            ln = linea("forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv", celda + "\t")
            base = f"forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:{ln} ({celda}, ola {c['instrumento']})"
            if tipo in ("celda_L", "celda_AGREGADO"):
                pon(rid, "NO-RELEVAR-POR-REGLA-6", f"{base}; {REGLA6}; {H3}", "NINGUNO (histórico)")
            else:
                pon(rid, "NO-RELEVAR-POR-REGLA-6",
                    f"{base}; retador M del duelo sobre ola vista; {REGLA6}", "NINGUNO (histórico)")
            continue
        if tipo == "condicional_theta":
            k = cons.split(":", 1)[1].split("/")[0]
            pon(rid, "NO-RELEVAR-θ", f"milpa/procedencia.yaml:{linea('milpa/procedencia.yaml', k)} ({cons.split(':',1)[1]}); {THETA}; nadie ocupó la fila de emisión (ningún consumidor emite θ)",
                "NINGUNO (retador de familias 2027 si se pre-registra)")
            continue
        if tipo == "coeficiente_ejecutable":
            k = cons.rsplit(":", 1)[1]
            pon(rid, "NO-RELEVAR-GENERADOR",
                f"milpa/procedencia.yaml:{linea('milpa/procedencia.yaml', 'coeficientes_generador_sellados')} ({k}; clase_legacy={r['clase_legacy'][:40]}); {THETA}",
                "NINGUNO (retador de familias 2027 si se pre-registra)")
            continue
        if tipo == "coeficiente_asignado":
            gen, co = cons.rsplit(":", 1)[1].split(".", 1) if "." in cons.rsplit(":", 1)[1] else (cons, "")
            ln = linea("milpa/procedencia.yaml", f"gen: {gen}, coefs")
            pon(rid, "NO-RELEVAR-POR-FIRMA",
                f"milpa/procedencia.yaml:{ln} historico_sin_relevo ({cons.rsplit(':',1)[1]}); firma H1 FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-01 FIRMADA",
                "NINGUNO (histórico)")
            continue
        if tipo == "corte_pi":
            pon(rid, "NO-RELEVAR-POR-FIRMA",
                f"forense/firmas-pendientes.tsv:{linea('forense/firmas-pendientes.tsv', 'FP-260924-GEN2-RELEVO-MOTOR-34-1-a157-03')} (B3: corte_pi fuera del contador); tools/corrida0.py:{linea('tools/corrida0.py', 'TIPOS_FUERA_DEL_CONTADOR = ')}",
                "NINGUNO")
            continue
        if tipo == "asignado_probabilidad":
            k = cons.rsplit(":", 1)[1]
            ln = linea("milpa/procedencia.yaml", f"- regla: {k}", linea("milpa/procedencia.yaml", "asignados_probabilidad:"))
            txt = (RAIZ / "milpa/procedencia.yaml").read_text(encoding="utf-8").splitlines()[ln - 1:ln + 14]
            fin = next((i for i, t in enumerate(txt) if i > 0 and t.lstrip().startswith("- regla:")), len(txt))
            txt = txt[:fin]
            m = next((re.search(r"corrida0_resultado_id: (RESULT-[A-Z0-9-]+)", t) for t in txt if "corrida0_resultado_id" in t), None)
            rot = next((i for i, t in enumerate(txt) if "rotulo_relevo" in t), None)
            if m:
                pon(rid, "RELEVAR-DESDE-RESULT",
                    f"milpa/procedencia.yaml:{ln} corrida0_resultado_id={m.group(1)} (valor legacy ya igual al RESULT; clase iii para el complemento)",
                    "GEN2-RELEVO-CONSUMIDORES-4 (pin en usos)")
            elif rot is not None:
                pon(rid, "SIN-BASE-GEN2",
                    f"milpa/procedencia.yaml:{ln + rot} rotulo_relevo=ASIGNADO-CONSERVADO-H1 (FP e760-01; regla B1: sin par GEN2); NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-01",
                    "GEN2-RELEVO-CONSUMIDORES-4")
            continue
        if tipo == "celda_D":
            f = cons.split(":")[0]
            d = yaml.safe_load((RAIZ / f).read_text(encoding="utf-8"))["celda_d"]
            ch, ve = str(d.get("champion_actual")), str(d.get("veredicto", d.get("tipo_adjudicacion")))
            cita = f"{f}:{linea(f, 'champion_actual')} champion_actual={ch} veredicto={ve} fecha_adjudicacion={d.get('fecha_adjudicacion')}"
            if ch in ("NINGUNO", "None"):
                pon(rid, "CELDA-D-SIN-CHAMPION", cita + "; NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-04",
                    "GEN2-TRAMITE-FIRMAS-21 (A1, evasión de norma)")
            else:
                pon(rid, "CELDA-D-ADJUDICADA", cita + "; NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-04",
                    "GEN2-RELEVO-CONSUMIDORES-4 (pin del champion)")
            continue
        if tipo == "momento":
            mid = cons.rsplit(":", 1)[1]
            m = momentos[mid]
            ln = linea("milpa/catalogo-momentos-v0_1.tsv", mid + "\t")
            base = f"milpa/catalogo-momentos-v0_1.tsv:{ln} ({mid}, rol={m['rol_calibracion']})"
            er = m.get("estado_relevo") or ""
            if m["valor_gen2"] and m["corrida0_resultado_id"]:
                pon(rid, "YA-RELEVADO-GEN2", f"{base} valor_gen2={m['corrida0_resultado_id']} {er[:40]}", "NINGUNO (relevado)")
            elif er.startswith("HISTÓRICO-SIN-RELEVO"):
                pon(rid, "NO-RELEVAR-POR-FIRMA", f"{base} estado_relevo={er[:60]}", "NINGUNO (histórico)")
            elif mid in ("M05", "M23"):
                pon(rid, "ESPERA-FIRMA-MESA" if m["rol_calibracion"] == "AJUSTE" else "ESPERA-FIRMA-HOLDOUT",
                    f"{base}; hoja forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md:{linea('forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md', '## A1')} letra A1; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-01 ABIERTA",
                    "GEN2-TRAMITE-FIRMAS-21 (A1)")
            elif m["rol_calibracion"] == "HOLDOUT":
                pon(rid, "ESPERA-FIRMA-HOLDOUT",
                    f"{base}; hoja forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md:{linea('forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md', '## A2')} letra A2; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-02 ABIERTA",
                    "GEN2-TRAMITE-FIRMAS-21 (A2)")
            elif mid == "M03":
                pon(rid, "SIN-ESTIMANDO-RECONSTRUIBLE",
                    f"{base} computo_pretendido=«reproducir la proporción declarada de la regla» e instrumentos_candidatos=POR DECLARAR; la proporción de la regla es ASIGNADO sin fuente (RES-0017/RES-0018); no hay RESULT GEN2 de coercitivo (NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-02)",
                    "GEN2-RELEVO-CONSUMIDORES-4 (NC 72d9-02)")
            continue
    return res, cor, dict_res, man, a


def filas_vista(res, cor, d):
    """Una fila por RESULT y una por corrida (resultado_id = «CORRIDA»)."""
    filas = []
    for c in cor:
        ids = c["resultados_ids"].split(";")
        toks = [d[i][0] for i in ids]
        abre = sorted({t for t in toks if not VOCAB[t][0]})
        cuenta = ", ".join(f"{t}={toks.count(t)}" for t in sorted(set(toks)))
        dic = ("CORRIDA-REQUERIDA:" + "+".join(abre)) if abre else "CORRIDA-NO-REQUERIDA"
        filas.append({"corrida_id": c["corrida_id"], "resultado_id": "CORRIDA",
                      "dictamen": dic,
                      "cita": f"demanda-corridas de apertura ({c['entorno_requerido']}, {c['medidor_o_spec_candidato']}); dictamen de sus {len(ids)} RESULT: {cuenta}",
                      "sucesor": "lotes de caja" if abre else "NINGUNO (sale de N_corridas_requeridas por dictamen)"})
    for r in res:
        t, ci, su = d[r["resultado_id"]]
        filas.append({"corrida_id": r["corrida_natural"], "resultado_id": r["resultado_id"],
                      "dictamen": t, "cita": ci, "sucesor": su})
    return filas


if __name__ == "__main__":
    res, cor, d, man, a = main()
    faltan = [r for r in res if r["resultado_id"] not in d]
    for r in faltan:
        print("SIN-DICTAMEN", r["resultado_id"], r["corrida_natural"], r["tipo"], r["consumidor"][:90])
    filas = filas_vista(res, cor, d)
    import collections
    print(len(d), "RESULT dictaminados;", len(faltan), "sin dictamen;", len(cor), "corridas")
    print(collections.Counter(f["dictamen"] for f in filas if f["resultado_id"] == "CORRIDA"))
    if a.escribe and not faltan:
        with SALIDA.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write("# DERIVADO por forense/analisis/demanda-dictamen-1/construye_dictamen.py "
                     "(ACTO GEN2-DEMANDA-DICTAMEN-1) sobre la demanda de apertura en 723b62c1/16ba3d02.\n")
            fh.write("# Vocabulario cerrado y qué cierra: ver VOCAB en el script y "
                     "forense/analisis/demanda-dictamen-1/hoja-para-mesa-demanda-dictamen-1.md. La leen `corrida0 demanda` y los lotes de caja.\n")
            w = csv.DictWriter(fh, COLS, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(filas)
        print("ESCRITO", SALIDA.relative_to(RAIZ), len(filas), "filas")
