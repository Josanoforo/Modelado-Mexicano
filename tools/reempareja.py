#!/usr/bin/env python3
# ACTO MAESTRA32-E4 · RE-EMPAREJA -- elevacion a tools/ del bloque de
# re-corrida que vivia solo dentro de
# forense/notas/2026-08-30-etiqueta-v1_2-cierre.md:110-399 (ACTO
# MAESTRA32-E6 · ETIQUETA-v1_2, COMMIT-2), que a su vez es la re-corrida
# VERBATIM de la busqueda mecanica y los criterios de
# forense/notas/2026-08-28-empareja-spec.md (COMMIT-1 de MAESTRA32-E2),
# identica a "el script de COMMIT-2, integro" pegado en
# forense/notas/2026-08-28-empareja-cierre.md §3. NINGUN
# termino/criterio/DESCARTES/prioridad cambia de significado frente al
# bloque de E6. Los UNICOS cambios frente a ese bloque, declarados en
# forense/notas/2026-08-30-reempareja-spec.md COMMIT-1(c):
#   (1) se lee una tabla mas: data/inventario-reactivos-ext-v1_0.tsv
#       (ACTO MAESTRA32-E3 v2), ademas de data/inventario-reactivos-v1_2.tsv
#       y data/inventario-fd-v1_1.tsv -- universo = v1_2 UNION ext-v1_0,
#       concatenadas como entradas separadas de TABLAS (mismo esquema de 9
#       columnas, sin deduplicar por diseño: un mismo payload_id no aparece
#       en ambas) para que cada fila candidata conserve su tabla de origen
#       real en la columna `tabla` -- necesario para el reporte de deltas
#       por tabla de origen (v1_2 vs ext) que exige COMMIT-2 de este acto;
#   (2) el archivo de salida es data/emparejamiento-motor-v1_2.tsv (no
#       v1_1.tsv) y su cabecera de comentario cita este acto en vez de E6.
# DESCARTES/PARES/TERMINOS_*/BATERIA_CIRCULAR_G5/norm/load/descarte_razon/
# recorte/buscar/veredicto_par: copiados sin editar ni una letra, incluidas
# las dos claves DESCARTES ya re-clavadas por E6 de "(raiz)" a
# "censo2020"/"enut2019" (no se re-tocan aqui).
import csv
import sys
import unicodedata

ROOT = "/home/user/Modelado-Mexicano"


def norm(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def load(fn):
    path = f"{ROOT}/{fn}"
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if not l.startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    return rows


REACTIVOS = load("data/inventario-reactivos-v1_2.tsv")
REACTIVOS_EXT = load("data/inventario-reactivos-ext-v1_0.tsv")
FD = load("data/inventario-fd-v1_1.tsv")
TABLAS = [
    ("inventario-reactivos-v1_2", REACTIVOS),
    ("inventario-reactivos-ext-v1_0", REACTIVOS_EXT),
    ("inventario-fd-v1_1", FD),
]

TERMINOS_ESTATUS = [
    "estatus", "status", "prestigio", "prestigiosa", "prestigioso",
    "imagen social", "que dirán", "que diran", "aparentar",
    "apariencia social", "ostentar", "ostentación", "ostentacion",
    "posición social", "posicion social", "nivel social", "envidia",
    "comparación social", "comparacion social",
]
DESENLACE_G2 = [
    "ansiedad de estatus", "ansiedad social", "estrés social",
    "estres social", "consumo compensatorio", "consumo conspicuo",
    "gasto en imagen", "compra por estatus", "compra por status",
    "deuda por aparentar", "gasto ostentoso", "compra impulsiva",
]
TERMINOS_AVERSION = [
    "aversión al riesgo", "aversion al riesgo", "tolerancia al riesgo",
    "preferencia por seguridad", "evitar riesgo", "evita el riesgo",
    "riesgo financiero", "disposición a arriesgar",
    "disposicion a arriesgar", "prefiere no arriesgar",
    "toma de riesgos",
]
DESENLACE_G3 = [
    "horizonte corto", "corto plazo", "ahorro informal", "tanda",
    "cundina", "guardadito", "debajo del colchón", "debajo del colchon",
    "sin cuenta bancaria", "ahorro en efectivo", "no planea a futuro",
    "sin planeación", "sin planeacion",
]
TERMINOS_HORIZONTE = [
    "horizonte temporal", "planeación a futuro", "planeacion a futuro",
    "corto plazo", "largo plazo", "futuro cercano",
    "expectativas a futuro", "orientación al futuro",
    "orientacion al futuro",
]
DESENLACE_G4 = [
    "conducta defensiva", "evita salir", "deja de salir",
    "restringe sus salidas", "evita lugares", "miedo a salir",
    "cambió de ruta", "cambio de ruta", "cambio de rutina",
    "retracción", "retraccion", "espacio público", "espacio publico",
    "deja de frecuentar", "autoconfinamiento", "evita transitar",
]
TERMINOS_FAMILISMO_APOYO = [
    "apoyo familiar", "ayuda económica de familiares",
    "ayuda economica de familiares", "dinero de familiares",
    "préstamo familiar", "prestamo familiar", "apoyo de la familia",
    "remesas familiares", "ayuda entre parientes",
    "transferencias familiares",
]
DESENLACE_G5 = [
    "pooling", "corresidencia", "vive con", "hogar extendido",
    "cuidado de familiares", "carga de cuidado", "cuidador", "cuida a",
    "comparte gastos del hogar", "hogar compartido",
    "mudarse con la familia", "se mudó con", "se mudo con",
]
TERMINOS_FAMILISMO_OBLIGACION = [
    "obligación familiar", "obligacion familiar",
    "deber con la familia", "responsabilidad familiar",
    "compromiso familiar", "deber moral con los padres",
    "obligado a ayudar a la familia", "debe cuidar a", "debe mantener a",
]
TERMINOS_RADIO_CONFIANZA = [
    "radio de confianza", "confía en", "confia en",
    "personas que conoce", "vecinos de su colonia", "desconocidos",
    "confianza interpersonal", "círculo de confianza",
    "circulo de confianza",
]
TERMINOS_DEFERENCIA = [
    "deferencia", "obediencia", "obedece", "respeto a la autoridad",
    "no cuestiona", "acata órdenes", "acata ordenes", "sumisión",
    "sumision", "subordinación", "subordinacion",
]
DESENLACE_G6 = [
    "iniciativa suprimida", "no toma la iniciativa",
    "espera instrucciones", "no opina", "se abstiene de proponer",
    "paternalismo", "decisiones tomadas por otros",
    "no participa en las decisiones",
]

BATERIA_CIRCULAR_G5 = {f"p9_9_{i}" for i in range(1, 7)}

PARES = [
    ("G5", "familismo_apoyo", TERMINOS_FAMILISMO_APOYO, DESENLACE_G5),
    ("G5", "radio_confianza", TERMINOS_RADIO_CONFIANZA, DESENLACE_G5),
    ("G5", "familismo_obligacion", TERMINOS_FAMILISMO_OBLIGACION, DESENLACE_G5),
    ("G2", "sens_estatus", TERMINOS_ESTATUS, DESENLACE_G2),
    ("G2", "aversion_riesgo", TERMINOS_AVERSION, DESENLACE_G2),
    ("G3", "aversion_riesgo", TERMINOS_AVERSION, DESENLACE_G3),
    ("G4", "horizonte_temporal", TERMINOS_HORIZONTE, DESENLACE_G4),
    ("G4", "sens_estatus", TERMINOS_ESTATUS, DESENLACE_G4),
    ("G6", "deferencia", TERMINOS_DEFERENCIA, DESENLACE_G6),
]

PLACEHOLDER_INSTRUMENTOS = {"(raiz)", "(sin-instrumento-derivable)"}

# ---------------------------------------------------------------------
# Excepciones DESCARTADO-con-razón: identicas a empareja-cierre.md, salvo
# las DOS claves re-clavadas de "(raiz)" al instrumento ya resuelto por
# ACTO MAESTRA32-E6 (declarado en el preambulo de este archivo). Este acto
# no re-clava ninguna clave nueva.
# ---------------------------------------------------------------------
DESCARTES = {
    ("ESTATUS", "ADQ15_ENAFIN_2024_RNM_INEGI", "estatus"): "homónimo administrativo: campo de estatus de registro/trámite, no sensibilidad al estatus social",
    ("Estatus del cambio", None, "estatus"): "homónimo administrativo: campo de estatus de registro de cambio (ENOE/ENIGH), no sensibilidad al estatus social",
    ("Estatus", None, "estatus"): "homónimo administrativo: campo de estatus de registro/trámite (sin más calificador en el nombre de columna, mismo patrón que las demás variantes ESTATUS*), no sensibilidad al estatus social",
    ("ESTATUS", None, "estatus"): "homónimo administrativo: campo de estatus de registro/trámite, no sensibilidad al estatus social",
    ("code_status", None, "status"): "homónimo administrativo: código de estatus de procesamiento, no sensibilidad al estatus social",
    ("estatus_casilla", None, "estatus"): "homónimo administrativo: estatus de casilla electoral, no sensibilidad al estatus social",
    ("ESTATUS_ ACTA", None, "estatus"): "homónimo administrativo: estatus de acta/documento, no sensibilidad al estatus social",
    ("ESTATUS_ACTA", None, "estatus"): "homónimo administrativo: estatus de acta/documento, no sensibilidad al estatus social",
    ("Estatus: APROBADO", None, "estatus"): "homónimo administrativo: estatus de aprobación de trámite, no sensibilidad al estatus social",
    ("2.2.2.2._BREMS", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal",
    ("2.1.1.2.Valores_bancarios", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "corto plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal",
    ("2.1.1.3.Valores_privados", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "corto plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal / ahorro informal",
    ("3.3.1.Créditos", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de crédito externo agregado (macro), no horizonte temporal personal",
    ("3.3.2.Emisión_de_deuda_de_mexicanos_en_el_extranjero", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de deuda agregada (macro), no horizonte temporal personal",
    ("https://www.elystandard.co.uk/news/26460266.man-due-court-deaths-women-a10-crash-near-ely/", "(sin-instrumento-derivable)", "tanda"): "colisión de subcadena espuria: \"tanda\" cae dentro de \"standard\" en una URL de noticia ajena al corpus de reactivos, no es contenido de reactivo",
    ("P28B. Dígame si está usted de acuerdo o en desacuerdo con las siguientes frases Si uno no se cuida a sí mismo la gente se aprovechará", "encup2012", "cuida a"): "homónimo: ítem de autocuidado/confianza generalizada (\"si uno no se cuida a sí mismo la gente se aprovechará\"), no carga de cuidado familiar",
    ("U_POB_ELAB_CUL", "censo2020", "cuida a"): "homónimo: cuidado de animales/cultivo agrícola, no cuidado de personas -- re-clavado de '(raiz)' a 'censo2020' (ACTO MAESTRA32-E6, Censo2020_CAAS_descriptor_bd.xlsx ya resuelto por la regla v1_1 aplicada por primera vez a la capa FD)",
    ("P2_6_3", "enut2019", "cuidador"): "mide contratación de cuidador(a) remunerado(a) externo (sustituye a la familia), polo opuesto de \"carga de cuidado\" recayendo en la familia -- re-clavado de '(raiz)' a 'enut2019' (ACTO MAESTRA32-E6, enut2019_fd.xlsx ya resuelto por la regla v1_1 aplicada por primera vez a la capa FD)",
    ("P2_1", "mociba2016", "desconocidos"): "homónimo: exposición a spam/virus/contacto de desconocidos en internet (uso de TIC), no radio de confianza interpersonal",
}


def descarte_razon(vid, inst, termino):
    for key in ((vid, inst, termino), (vid, None, termino)):
        if key in DESCARTES:
            return DESCARTES[key]
    return None


def recorte(s, n=200):
    s = (s or "").replace("\t", " ").replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def buscar(terminos, lado, gen, coef):
    salida = []
    n_hits_id = 0
    n_hits_texto = 0
    terminos_norm = [(t, norm(t)) for t in terminos]
    for nombre_tabla, filas in TABLAS:
        for row in filas:
            vid = row.get("variable_id", "")
            vid_n = norm(vid)
            texto = row.get("texto_reactivo", "")
            texto_n = norm(texto)
            inst = row.get("instrumento", "")
            for via, haystack_n in (("id", vid_n), ("texto", texto_n)):
                hit = next((t for t, tn in terminos_norm if tn in haystack_n), None)
                if not hit:
                    continue
                if via == "id":
                    n_hits_id += 1
                else:
                    n_hits_texto += 1
                veredicto = "CANDIDATO"
                razon = ""
                if lado == "desenlace" and gen == "G5" and vid.strip().lower() in BATERIA_CIRCULAR_G5:
                    veredicto = "CIRCULAR-EXCLUIDO"
                    razon = "misma batería ENIF P9_9_1..6 que opera la θ de familismo_apoyo -- marca C3, milpa/procedencia.yaml:314-319"
                else:
                    r = descarte_razon(vid, inst, hit)
                    if r:
                        veredicto = "DESCARTADO-con-razón"
                        razon = r
                salida.append(dict(
                    gen=gen, coef=coef, lado=lado, variable_id=vid,
                    instrumento=inst, texto=recorte(texto), via=via,
                    tabla=nombre_tabla, termino=hit,
                    veredicto_candidato=veredicto, razon=razon,
                ))
    return salida, n_hits_id, n_hits_texto


def veredicto_par(n_theta, n_desenlace, co):
    if co:
        return "EXISTE-SATISFACE"
    if n_theta > 0 or n_desenlace > 0:
        return "EXISTE-NO-SATISFACE"
    return "NO-ENCONTRADO"


if __name__ == "__main__":
    todas_filas = []
    resumen = []
    for gen, coef, terminos_theta, terminos_desenlace in PARES:
        filas_theta, hid_t, htx_t = buscar(terminos_theta, "theta", gen, coef)
        filas_desenlace, hid_d, htx_d = buscar(terminos_desenlace, "desenlace", gen, coef)
        todas_filas.extend(filas_theta)
        todas_filas.extend(filas_desenlace)
        print(f"# {gen}.{coef}: theta hits id={hid_t} texto={htx_t} | "
              f"desenlace hits id={hid_d} texto={htx_d}", file=sys.stderr)
        resumen.append((gen, coef, filas_theta, filas_desenlace))

    with open(f"{ROOT}/data/emparejamiento-motor-v1_2.tsv", "w", newline="", encoding="utf-8") as f:
        f.write("# data/emparejamiento-motor-v1_2.tsv -- ACTO MAESTRA32-E4 · RE-EMPAREJA, COMMIT-2\n")
        f.write("# Re-corrida VERBATIM de la especificacion congelada de MAESTRA32-E2\n"
                "# (forense/notas/2026-08-28-empareja-spec.md, COMMIT-1), elevada a\n"
                "# tools/reempareja.py desde el bloque de ACTO MAESTRA32-E6 (dentro de\n"
                "# forense/notas/2026-08-30-etiqueta-v1_2-cierre.md), sobre el universo\n"
                "# ampliado de este acto: data/inventario-reactivos-v1_2.tsv UNION\n"
                "# data/inventario-reactivos-ext-v1_0.tsv (ACTO MAESTRA32-E3 v2), mas\n"
                "# data/inventario-fd-v1_1.tsv. Ningun termino/criterio de\n"
                "# CANDIDATO/circularidad/co-observacion/prioridad cambio frente a E2/E6.\n"
                "# Detalle de la re-corrida y de las tres tablas: "
                "forense/notas/2026-08-30-reempareja-spec.md,\n"
                "# forense/notas/2026-08-30-reempareja-cierre.md.\n")
        w = csv.writer(f, delimiter="\t")
        w.writerow(["gen", "coef", "lado", "variable_id", "instrumento", "texto",
                    "via", "veredicto_candidato", "razon", "tabla", "termino"])
        for row in todas_filas:
            w.writerow([row["gen"], row["coef"], row["lado"], row["variable_id"],
                        row["instrumento"], row["texto"], row["via"],
                        row["veredicto_candidato"], row["razon"], row["tabla"],
                        row["termino"]])

    print("\n# ===== veredicto A.4 por par (co-observación exige instrumento "
          "identificado, NO '(raiz)'/'(sin-instrumento-derivable)') =====",
          file=sys.stderr)
    deltas = []
    for gen, coef, ft, fd in resumen:
        cand_theta = sorted({r["instrumento"] for r in ft
                              if r["veredicto_candidato"] == "CANDIDATO"
                              and r["instrumento"] not in PLACEHOLDER_INSTRUMENTOS})
        cand_desenlace = sorted({r["instrumento"] for r in fd
                                  if r["veredicto_candidato"] == "CANDIDATO"
                                  and r["instrumento"] not in PLACEHOLDER_INSTRUMENTOS})
        cand_theta_raiz = sorted({r["instrumento"] for r in ft
                                   if r["veredicto_candidato"] == "CANDIDATO"
                                   and r["instrumento"] in PLACEHOLDER_INSTRUMENTOS})
        cand_desenlace_raiz = sorted({r["instrumento"] for r in fd
                                       if r["veredicto_candidato"] == "CANDIDATO"
                                       and r["instrumento"] in PLACEHOLDER_INSTRUMENTOS})
        co = sorted(set(cand_theta) & set(cand_desenlace))
        n_theta_candidato = sum(1 for r in ft if r["veredicto_candidato"] == "CANDIDATO")
        n_desenlace_candidato = sum(1 for r in fd if r["veredicto_candidato"] == "CANDIDATO")
        v = veredicto_par(n_theta_candidato, n_desenlace_candidato, co)
        print(f"{gen}.{coef}: theta_candidatos_reales={n_theta_candidato} "
              f"(instrumentos={cand_theta}, +placeholder={cand_theta_raiz}) | "
              f"desenlace_candidatos_reales={n_desenlace_candidato} "
              f"(instrumentos={cand_desenlace}, +placeholder={cand_desenlace_raiz}) | "
              f"co_observacion_instrumento_identificado={co} | veredicto={v}", file=sys.stderr)
        deltas.append((gen, coef, v, co))
    print(f"\n# total filas escritas en data/emparejamiento-motor-v1_2.tsv: {len(todas_filas)}",
          file=sys.stderr)
    print("\n# FILAS_EXAMINADAS_POR_TABLA (A.13)", file=sys.stderr)
    print(f"# inventario-reactivos-v1_2: {len(REACTIVOS)}", file=sys.stderr)
    print(f"# inventario-reactivos-ext-v1_0: {len(REACTIVOS_EXT)}", file=sys.stderr)
    print(f"# inventario-fd-v1_1: {len(FD)}", file=sys.stderr)
    print("\n# DELTAS_JSON", file=sys.stderr)
    import json
    print(json.dumps(deltas, ensure_ascii=False), file=sys.stderr)
