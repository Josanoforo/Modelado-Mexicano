#!/usr/bin/env python3
"""arma_hoja_decisiones_pendientes_4.py -- ACTO GEN2-PENDIENTES-4 · P3: arma
`hoja-decisiones-pendientes-4.md` (la hoja RH de mesa) y `decisiones-pendientes-4.json` (renglón -> NC).

Cada renglón es una DECISIÓN de mesa irreversible o que ningún ejecutor puede tomar (D-19): adoptar, editar
o retirar algo sellado o una firma, abrir una ola reservada, cambiar el criterio de adopción en bloque. Las
bifurcaciones reversibles no están aquí: las decidió el acto y las declara en
`decididas-por-delegacion-pendientes-4.tsv` (ADENDA-1). El renglón trae situación, opciones con costo,
recomendación con su razón, plazo y texto de firma (PLANTILLA v2.2 §5-bis: una recomendación sin opciones no
es hoja). Las opciones salen de los investigadores (evidencia/), releídas y adjudicadas por el supervisor; los
dos renglones marcados MANUAL los redactó el supervisor con los hechos verificados de las dos rondas.

    python3 arma_hoja_decisiones_pendientes_4.py <dir-res> <hoja.md> <decisiones.json>
"""
import csv
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# (título, [claves de NC], FP existente que ya cubre la decisión o "")
RENGLONES = {
    "D1": ("Régimen de aislamiento de la sesión ciega de C1 (767 identidades ENDIREH 2021)", ["ee49-03", "0c1f-04", "8c5c-10", "8c5c-03"], ""),
    "D2": ("Contratos nuevos de C1: escolaridad NIV-terminal-v1 y P14_22_14", ["157c-03"], ""),
    "D3": ("Margen de equivalencia y control simultáneo para los IC de C1", ["2385-04", "26a2-01"], "FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01"),
    "D4": ("Publicabilidad frágil de 10 celdas ENDIREH del lote 1", ["beee-07"], ""),
    "D5": ("Coercitivo digital (RES-0017/0018) y M03: HISTÓRICO-SIN-RELEVO", ["a157-09", "a157-10", "72d9-02"], "FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-02"),
    "D6": ("ITER del Censo 2020: levantar la reserva E.6", ["7cd0-02"], ""),
    "D7": ("Qué significa que una regla SI-ENTONCES «se confirma»", ["a3cc-03"], "FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01"),
    "D8": ("EDER 2025 (JUV-001/002): levantar la reserva E.6", ["7cd0-03"], ""),
    "D9": ("ENCO (ahorro percibido): medir P10 y aceptar un puente", ["NC-0318"], ""),
    "D10": ("Ahorro ENNViH (RES-0029/0030) y la ola 3 reservada", ["a157-15", "a157-16"], "FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01"),
    "D11": ("ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato", ["dd08-01"], ""),
    "D12": ("Familia F6 (transferencia de M): retirar o reactivar", ["NC-0161", "NC-0162", "NC-0324"], ""),
    "D13": ("Firma de contenido de los sucesores ENDIREH 2006 y 2016", ["fb50-02"], ""),
    "D14": ("G1-B: partir resultados.tsv ya sin objeto", ["247d-01"], ""),
    "D15": ("Guarda 4.1: relevo de champion compuesto que ingiere resultados ajenos", ["e760-06", "e760-07"], ""),
    "D16": ("Solicitud de microdato ENCRIGE 2020 al Laboratorio de INEGI", ["795b-09", "4b11-03"], ""),
    "D17": ("Legado explícito de RESULT-L8CONV en tramite.yaml", ["NC-0253"], ""),
    "D18": ("Latinobarómetro 2024: levantar la reserva E.6", ["7cd0-01"], ""),
    "D19": ("M12, M14, M15, M16 y M17: fecharlos o dejarlos sin fecha (R08 b)", ["795b-01", "795b-02", "795b-03", "795b-04", "795b-05"], ""),
    "D20": ("Cuarta condición del bin 1 de la regla de adopción en bloque", ["NC-0290"], ""),
    "D21": ("ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?", ["2a0e-07"], ""),
    "D22": ("Adendas de mesa sin rastro (19–21/sep): archivo retroactivo", ["3d08-02"], ""),
    "D23": ("Sidecar del insumo codex que cita un archivo ausente", ["3d08-01"], ""),
    "D24": ("Anexo A del lote ENIF 2024 archivado con otro sha256", ["a98a-04"], ""),
    "D25": ("Envoltura por celda de emite_m.py (regla de ola previa estricta)", ["NC-0026"], ""),
    "D26": ("[COLA] y [ADQ]: ¿categoría exenta o excepción rotulada aparte?", ["NC-0170"], ""),
    "D27": ("Auto-merge del [deriva] (P4 de GEN2-TUBERIA-3)", ["c6aa-01"], "FP-260928-GEN2-TUBERIA-3-f18c-01"),
    "D28": ("Regla del semáforo del tablero de carriles: SIN-UNION", ["c6aa-02"], "FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01"),
    "D29": ("Regla ROJO del tablero de carriles: ¿cuenta solo cifra adoptada?", ["8fdf-04"], "FP-260928-GEN2-MEDICION-CARRILES-2-8fdf-01"),
    "D30": ("Estado final de RES-0065 (ENIF, POB-P corto no trabaja): aceptar NO-DERIVABLE-DESDE-LA-SPEC o abrir un CALC sucesor con enlace declarado", ["NC-0212"], ""),
    "D31": ("Piso nacional de TRIADA-B (RESULT-TBP-*): unirlo al marcador por segmento o declarar SIN-PISO permanente", ["NC-0338"], ""),
}

# Renglones cuya decisión, opciones y recomendación YA viven en una FP ABIERTA: se citan verbatim (no se reescriben).
DESDE_FP = {"D27", "D28", "D29"}

MANUAL = {
    "D25": {
        "situacion": "`tools/emite_m.py` tiene dos funciones puras de «ola previa estricta», probadas y consumidas por el CALC de demostración, pero `emite_celda` no las consume: NC-0026 pide esa envoltura por celda. Su consumidor previsto (C0-D, el marcador por ola) lo sustituyó GEN2-MARCADOR-REDISENO-1, cuya firma (1) deriva el marcador del catálogo y las celdas-D, nunca del emisor. Cablearlas cambiaría la M que el emisor produce hoy y, con ella, las corridas-M. Dos verificadores independientes rechazaron cerrarla por diseño: la firma (5) de MARCADOR-REDISENO-1 cierra otras cuatro NC y omite ésta, y `emite_m` sigue vivo (ADR-520: sigue abierto que la M vigente no modula).",
        "opciones": [
            {"letra": "a", "texto": "No cablear: las dos funciones quedan puras y probadas; NC-0026 se cierra por firma de mesa citando la firma (1) de MARCADOR-REDISENO-1.", "costo": "Ninguno de código. La M vigente sigue sin modular (ya declarado en ADR-520); si algún día se quiere modular por ola, será un CALC nuevo."},
            {"letra": "b", "texto": "Encargar el cableado de la envoltura a `emite_celda`.", "costo": "Cambia la M emitida: hay que re-emitir corridas-M y adoptar en bloque (E.2): irreversible en la práctica. Mide sobre olas vistas (regla 6)."},
            {"letra": "c", "texto": "Retirar las dos funciones (E.1/regla 6).", "costo": "Toca código con un consumidor vivo (el CALC de demostración) y sellos asociados; no se puede hacer sin un CALC nuevo."},
        ],
        "recomendacion": "a",
        "porque": "El consumidor que la justificaba ya no existe y la vía prospectiva son las familias 2027; cablearla mediría sobre olas vistas, que la regla 6 no autoriza para retadores.",
        "plazo": "2026-10-05",
        "texto_firma": "«NC-0026: opción (a); las dos funciones de ola previa estricta de tools/emite_m.py quedan puras y no se cablean a emite_celda; se cierra citando la firma (1) de GEN2-MARCADOR-REDISENO-1.»",
    },
    "D30": {
        "situacion": "`CALC-ENIF-0002` está sellado y no se reescribe (E.3): ninguna spec sellada declara la pareja consumidor↔RESULT de `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P`, aunque la cita `corrida0_resultado_id` existe en `milpa/tramite.yaml` y es coherente. `data/corrida0/relevo-usos-v1_0.tsv` rotula RES-0065 `YA-ADOPTADO` con `control_c0=NO-DERIVABLE-DESDE-LA-SPEC`, y la validación independiente del RESULT dice PASA con ENLACE dentro de su alcance (`data/corrida0/validaciones-independientes.tsv:28`). La delegación de PENDIENTES-3 recomendó (a) pero dejó la fila con mesa (`opcion` DUEÑO-MESA en `decididas-por-delegacion.tsv`).",
        "opciones": [
            {"letra": "a", "texto": "Aceptar el rótulo `NO-DERIVABLE-DESDE-LA-SPEC` como estado final documentado de RES-0065 y cerrar NC-0212; `CALC-ENIF-0002` no se toca.", "costo": "Ninguno de código ni de sellos. Reversible: si mesa quiere el enlace declarado se abre una NC nueva."},
            {"letra": "b", "texto": "Encargar un CALC sucesor con el enlace declarado (`sucesion.json`) y su validación independiente.", "costo": "Un CALC nuevo y un replay; no cambia ninguna cifra, pero mueve la vista y añade un sello a un RESULT ya adoptado."},
        ],
        "recomendacion": "a",
        "porque": "La adopción no es falsa: está acreditada por un RESULT sellado y una validación independiente que PASA; reescribir o sustituir el sellado no añade evidencia (E.3).",
        "plazo": "2026-10-05",
        "texto_firma": "«NC-0212: opción (a); el rótulo NO-DERIVABLE-DESDE-LA-SPEC es el estado final documentado de RES-0065 y CALC-ENIF-0002 no se reescribe (E.3).»",
    },
    "D31": {
        "situacion": "`CALC-TRIADA-B-PISO-0001` trae 117 RESULT en el formato agregado del piloto B (`RESULT-TBP-*`), no un RESULT por (entrada de ejes, eje, categoría) serializado como las celdas-D. `tools/marcador_segmento.py` solo une por identidad exacta y reporta SIN-PISO sin inventar una correspondencia. Las nueve celdas que el encargo original citaba como piso son nacionales y el marcador es por eje: hoy las 97 filas NACIONAL de `data/corrida0/marcador-segmento.tsv` tienen `piso_tipo` NO-APLICA. No existe encargo `GEN2-MARCADOR-PISO-TRIADA-B-1`.",
        "opciones": [
            {"letra": "a", "texto": "Escribir un lector que una los `RESULT-TBP-*` a celdas nacionales del marcador, con la tabla de correspondencia declarada y firmada.", "costo": "Un encargo nuevo, una tabla de correspondencia que hay que firmar y una lectura más del marcador sobre un piloto de olas ya vistas (regla 6)."},
            {"letra": "b", "texto": "Declarar SIN-PISO permanente para esas nueve celdas nacionales.", "costo": "Ninguno de código; se pierde el piso nacional de la triada B, que el marcador por eje no usa."},
        ],
        "recomendacion": "b",
        "porque": "Las nueve celdas son nacionales y el marcador es por eje; el piso de un marginal es la ola anterior por eje (v2.16 §4), y la triada del duelo v2 quedó retirada por la regla 6, así que unirla no compra una comparación que se pueda emitir.",
        "plazo": "2026-10-05",
        "texto_firma": "«NC-0338: opción (b); las nueve celdas nacionales de TRIADA-B-PISO quedan SIN-PISO de forma permanente en el marcador por segmento.»",
    },
    "D26": {
        "situacion": "La firma del 16/sep encargó retro-sellar 18 EXCEPCIONES del censo de PR sin `## CONSUMIDO`: los 8 actos GEN2 reales ya están retro-sellados (#759, #795; NC-0227 CERRADA). Falta decidir el estatus de las 10 filas [COLA]/[ADQ] (PR cuyo título es `[COLA] …` o `[ADQ] …`, el mecanismo que entrega encargos): ¿una cuarta categoría exenta, como `censo/*` y `claude/tramite-*`? El censo ya las rotula EXCEPCIÓN-COLA/ADQ aparte, pero `tools/digesto_tramite.py` no las trata (0 coincidencias) y no existe una lista viva de exentos en tools, tests, .github, canon ni gobierno (1047 archivos examinados). Los verificadores rechazaron cerrarla por diseño: la fila pedía una firma entre dos opciones.",
        "opciones": [
            {"letra": "a", "texto": "Mantenerlas como EXCEPCIÓN EXPLÍCITA rotulada aparte, sin tocar canon.", "costo": "Reversible. Un acto de tubería debe hacer que el digesto lea la etiqueta EXCEPCIÓN-COLA/ADQ (hoy no la lee)."},
            {"letra": "b", "texto": "Sumarlas a la lista de exentas por ADR.", "costo": "Toca canon (regla de exentos) y las saca de todo control futuro: un PR [COLA] mal formado ya no se vería."},
            {"letra": "c", "texto": "Retro-sellar las 10 una por una con `## CONSUMIDO`.", "costo": "Diez ediciones sobre encargos ya archivados y sellados; choca con A.3 (el cuerpo no se toca) y con la firma ADENDAS."},
        ],
        "recomendacion": "a",
        "porque": "Es la única opción que no toca canon ni sellos y que conserva la visibilidad de los PR del mecanismo de entrega.",
        "plazo": "2026-10-05",
        "texto_firma": "«NC-0170: opción (a); [COLA] y [ADQ] no se suman a los exentos, quedan como EXCEPCIÓN-COLA/ADQ rotulada aparte, sin tocar canon.»",
    },
}


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    res, hoja_md, dec_json = sys.argv[1:4]
    libro = {r["id"]: r for r in csv.DictReader(open(os.path.join(RAIZ, "forense", "no-corrido.tsv"), newline="", encoding="utf-8"), delimiter="\t")}

    def find(k):
        r = [i for i in libro if i.endswith("-" + k) or i == k]
        if len(r) != 1:
            sys.exit(f"clave {k} resuelve a {r}")
        return r[0]

    mejor = {}
    for p in glob.glob(os.path.join(res, "*.research.json")):
        for r in json.load(open(p, encoding="utf-8")):
            h = r.get("hoja")
            if isinstance(h, dict) and h.get("opciones"):
                sc = len(json.dumps(h))
                if r["id"] not in mejor or sc > mejor[r["id"]][0]:
                    mejor[r["id"]] = (sc, h)
    out = ["# Hoja de decisiones de mesa · GEN2-PENDIENTES-4", "",
           "Generada por `arma_hoja_decisiones_pendientes_4.py` a partir de la evidencia archivada en `evidencia/` y adjudicada por el ejecutor. "
           "Cada renglón es una decisión que ningún ejecutor puede tomar (D-19): adoptar, editar o retirar algo sellado o una firma, abrir una ola reservada, o cambiar el criterio de adopción en bloque. "
           "Lo reversible ya lo decidió el acto por delegación y consta en `decididas-por-delegacion-pendientes-4.tsv`. "
           "Cada NC de estos renglones lleva `MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D<n>)` como dueño. "
           "Cuando la firma cae, el acto que la ejecuta cierra las NC del renglón citando la firma. Los renglones con «FP existente» ya tienen su ranura en `forense/firmas-pendientes.tsv`; los demás la reciben en este mismo PR (A.12).", ""]
    dec = {}
    for d, (titulo, claves, fp) in RENGLONES.items():
        ids = [find(k) for k in claves]
        dec[d] = {"titulo": titulo, "ids": ids, "fp_existente": fp}
        if d in DESDE_FP:
            fps = {r["id"]: r for r in csv.DictReader(open(os.path.join(RAIZ, "forense", "firmas-pendientes.tsv"), newline="", encoding="utf-8"), delimiter="\t")}
            f = fps[fp]
            nc = libro[ids[0]]
            h = {"situacion": (nc["que_no_se_corrio"] + " — " + nc["razon"]).replace("\n", " ")[:600],
                 "opciones": [{"letra": "FP", "texto": "Las que trae la firma pendiente, verbatim: «" + f["qué_se_firma"].replace("\n", " ")[:1100] + "»", "costo": "El de cada opción según el texto de la FP."}],
                 "recomendacion": "la que marca la FP", "porque": f"La decisión ya está formulada con sus opciones en `{fp}` (ABIERTA); este renglón la trae para que la hoja sea autónoma y no acuña otra ranura.",
                 "plazo": "2026-10-05", "texto_firma": f"«Firmo la opción (__) de {fp}.»"}
            fuente = "FP existente (verbatim)"
        elif d in MANUAL:
            h, fuente = MANUAL[d], "MANUAL (supervisor)"
        else:
            cand = [mejor[i] for i in ids if i in mejor]
            if not cand:
                sys.exit(f"{d}: sin hoja de investigador")
            h, fuente = max(cand, key=lambda x: x[0])[1], "investigador (adjudicada)"
        out += [f"## {d} · {titulo}", "",
                f"**NC que decide ({len(ids)}):** " + ", ".join(f"`{i}`" for i in ids), ""]
        if fp:
            out += [f"**FP existente:** `{fp}` (la decisión ya tiene su ranura; este renglón no acuña otra).", ""]
        out += [f"**Situación.** {h['situacion']}", "", "**Opciones.**", ""]
        for o in h["opciones"]:
            out.append(f"- **({o['letra']})** {o['texto']} — *Costo:* {o['costo']}")
        out += ["", f"**Recomendación.** ({h['recomendacion']}) {h['porque']}", "",
                f"**Plazo.** {h['plazo']}", "",
                f"**Texto de firma.** {h['texto_firma']}", "", f"*Fuente del renglón: {fuente}.*", ""]
    open(hoja_md, "w", encoding="utf-8").write("\n".join(out) + "\n")
    json.dump(dec, open(dec_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"hoja: {len(RENGLONES)} renglones · {sum(len(v['ids']) for v in dec.values())} NC → {hoja_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
