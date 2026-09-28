#!/usr/bin/env python3
"""arma_dictamen.py -- ACTO GEN2-PENDIENTES-3: arma `dictamen-pendientes-3.tsv` y
`decididas-por-delegacion.tsv` a partir de la evidencia por fila
(`evidencia/prop-A*.tsv`, recolectada por ejecutores de lectura) y de la
ADJUDICACIÓN del auditor, que vive aquí como código: reglas por propuesta más
las excepciones fila por fila, cada una con su razón.

La evidencia propone; este archivo decide. Nada se cierra sin cita: un cierre
lleva ruta+comando (producto), firma, id duplicado o decisión delegada.

    python3 forense/analisis/pendientes-3/arma_dictamen.py
"""
import glob
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ROT = "GEN2-PENDIENTES-3"
MESA = "MESA (2026-10-05)"   # plazo: una semana desde el barrido

# Actos en vuelo por rama (verificado por `git diff --name-only origin/main...origin/<rama>
# -- forense/encargos`, 28/sep/2026). Sus NC no se cierran: EN-CURSO con la rama.
EN_VUELO = {
    "GEN2-CALC-ALTERNOS-LOTE-1": "acto/gen2-calc-alternos-lote-1",
    "GEN2-C1-SUCESORES-Y-LOTE-3": "acto/GEN2-C1-SUCESORES-Y-LOTE-3",
    "GEN2-PISOS-DOMINIOS-Y-REGLAS-1": "acto/gen2-pisos-dominios-y-reglas-1",
    "GEN2-TUBERIA-3": "claude/new-session-5j6lbu",
    "GEN2-RECIBO-ASTRA6-N-v2": "claude/new-session-5j6lbu",
    "GEN2-TABLERO-CARRILES-1": "claude/new-session-9hwjgo",
}

# ── Excepciones del auditor, fila por fila ────────────────────────────
# CERRADA-POR-FIRMA propuesta, pero la firma EXIGE un producto que no existe y
# ningún acto archivado lo cubre -> no se cierra: dueño MESA (encargo por escribir).
FIRMA_CON_PRODUCTO_PENDIENTE = {
    "NC-260927-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1-3a1f-01": "R17 exige pasada editorial C3",
    "NC-0037": "R45 asignó dueño; falta el producto (sonda del ledger)",
    "NC-0164": "R16 (b): falta buscar fuente MX BNPL/CAT/daño",
    "NC-0324": "R36: falta el enlace científico pre-R",
    "NC-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-04": "R50 (a): licencias residuales a CORPUS-LICENCIAS-2, sin encargo",
    "NC-260922-GEN2-TRAMITE-COLA-VIEJA-1-0eca-02": "R55: falta el acto COLA-VIEJA-2 que anote las 14 filas",
    "NC-260925-GEN2-CORPUS-COMPLETO-1-7813-03": "R09 (a): falta mover payloads fuera de reserva_respondentes (manifiesto, fuera de perímetro)",
    "NC-260924-GEN2-CONTADORES-CONSUMO-2-749c-03": "R80: falta verificar que el canal publica vista >100 MB",
    "NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-01": "R20: falta el trámite posterior por contrato",
    "NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-03": "R14: falta la etapa 1 (inventario de miembros)",
    "NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01": "R06: falta excluir el módulo 7 de la caché parquet",
}
# CERRADA-POR-FIRMA propuesta cuyo producto viaja en un acto en vuelo (A.12) -> EN-CURSO.
FIRMA_VIAJA_EN = {
    "NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-03": "GEN2-CALC-ALTERNOS-LOTE-1",
    "NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-04": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260927-GEN2-RECIBO-ASTRA6-2-627e-07": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260927-GEN2-RECIBO-ASTRA6-2-627e-08": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-03": "GEN2-C1-SUCESORES-Y-LOTE-3",
    "NC-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-02": "GEN2-CALC-ALTERNOS-LOTE-1",
    "NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-04": "GEN2-CALC-ALTERNOS-LOTE-1",
}
# CERRADA-POR-FIRMA que es en rigor DUPLICADA de otra fila.
FIRMA_ES_DUPLICADA = {
    "NC-260924-GEN2-TRAMITE-FIRMAS-15-0c38-06": "NC-260923-GEN2-TRAMITE-FIRMAS-14-9556-07",
}
# DECIDIR-REVERSIBLE: el auditor decide por delegación (§2 (a)). Las de esta lista
# se CIERRAN con la opción recomendada por la evidencia (cerrar/aceptar estado
# estable/fuera por diseño); todas las demás quedan con dueño MESA (el acto que
# ejecutaría la opción no tiene encargo archivado).
DECIDE_Y_CIERRA = {
    "NC-260926-GEN2-TUBERIA-CABLEADO-SESIONES-1-0038-04", "NC-260928-GEN2-TRAMITE-HOJA-FIRMAS-21-1-9739-01",
    "NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-04", "NC-260922-GEN2-VALIDACION-INDEPENDIENTE-LOTE-1-41d6-01",
    "NC-260923-GEN2-RECIBO-ASTRA-1-4e74-02", "NC-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-04",
    "NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-04", "NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-05",
    "NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-01", "NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-03",
    "NC-260922-GEN2-TUBERIA-EFICIENCIA-1-0d1b-01", "NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-12",
    "NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-01", "NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-07",
    "NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-06", "NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-04",
    "NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-05", "NC-260926-GEN2-COLA-LOTE-1-3a49-05",
    "NC-260927-GEN2-CIERRE-SEMANAL-2-facd-01", "NC-260927-GEN2-RECIBO-ASTRA6-2-627e-04",
    "NC-260927-GEN2-RECIBO-ASTRA6-2-627e-01", "NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-06",
    "NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-04", "NC-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01",
    "NC-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-02", "NC-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-02",
    "NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-04", "NC-260927-GEN2-RECIBO-ASTRA6-2-627e-06",
    "NC-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-02", "NC-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02",
}
# Propuestas de ejecutor que el auditor corrige (razón en el valor).
CORRIGE = {
    # la vista publicó cuenta_gen2=NO por decisión de mesa y la fila pedía SI:
    # el producto existe pero no es el pedido -> no se cierra.
    "NC-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01": (
        "DUENO", "MESA (2026-10-05) · la vista publica -0002 con cuenta_gen2=NO por decisión de mesa; "
                 "la fila pedía SI: mesa confirma NO y se cierra por firma",
        "producto distinto del pedido"),
    "NC-0026": ("DUENO", "MESA (2026-10-05) · cierre por diseño propuesto; la firma de MARCADOR-REDISENO-1 no la nombra: mesa confirma", "firma no nombra la fila"),
    "NC-0070": ("DUENO", "MESA (2026-10-05) · cierre por diseño propuesto; la firma de MARCADOR-REDISENO-1 no la nombra: mesa confirma", "firma no nombra la fila"),
    "NC-0218": ("DUENO", "MESA (2026-10-05) · cierre por diseño propuesto sin verificar que el informe v1_5 absorba el objeto", "absorción no verificada"),
    "NC-0029": ("DUENO", "MESA (2026-10-05) · fila paraguas: descomponer residuales L/motor antes de cerrar (vencidas-dictamen de PENDIENTES-2)", "paraguas"),
    "NC-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-01": ("DUENO", "MESA (2026-10-05) · cierre por cita propuesto sin re-verificar los criterios por comando", "producto no re-verificado"),
    "NC-260921-GEN2-RELEVO-TANDA-4-dedd-01": ("DUENO", "MESA (2026-10-05) · cierre por cita propuesto sin re-verificar los criterios por comando", "producto no re-verificado"),
}
# EN-CURSO propuesto hacia la rama [deriva] (canal automático, no un acto): el
# producto se publica al fusionar el [deriva]; hasta entonces dueño MESA.
RE_DERIVA = re.compile(r"derivados/|\[deriva\]", re.I)


# NC nacidas en main DURANTE el barrido (actos en vuelo que fusionaron: PISOS-DOMINIOS,
# CALC-ALTERNOS, TABLERO-CARRILES, C1-SUCESORES). Su sucesor no tiene encargo
# archivado ni rama en vuelo (`cierre_acto.indice_actos`, 28/sep tras merge) -> MESA.
NUEVAS_TRAS_MERGE = {
    **{f"NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-0{i}": "GEN2-PISOS-DOMINIOS-Y-REGLAS-2" for i in (1, 2, 3, 4, 6)},
    "NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-05": "CALC-PDR1-ENCUCI2020-0002 (sustituto)",
    **{f"NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-0{i}": "GEN2-CALC-ALTERNOS-LOTE-2" for i in range(1, 9)},
    "NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-09": "GEN2-OBTENCION-EXTERNA-2",
    "NC-260928-GEN2-TABLERO-CARRILES-1-e2eb-01": "GEN2-TABLERO-CARRILES-2 o /tramite",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01": "GEN2-ASTRA6-C1-LOTE-4",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-02": "GEN2-C1-SUCESORES-2011-2021-1",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-03": "GEN2-SPEC-ENBIARE-ESCALAS-1",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-04": "firma FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-05": "GEN2-CIERRE-SEMANAL-3",
    "NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-06": "GEN2-RELEVO-TRAMITE-CAJA-2",
}


def _dueno_en_curso(texto):
    for acto, rama in EN_VUELO.items():
        if acto in texto:
            return f"EN-CURSO ({acto} · rama {rama})"
    return None


def adjudica(p):
    fid, prop = p["id"], p["propuesta"]
    ruta, cmd, sal, nuevo, nota = (sin_parentesis(p[k]) for k in ("ruta", "comando", "salida", "nuevo_sucesor", "nota"))
    nuevo_crudo = p["nuevo_sucesor"]
    if fid in CORRIGE:
        return CORRIGE[fid]
    if prop == "CERRADA-POR-PRODUCTO":
        return "CERRAR", f"{ROT} · CERRADA (producto: {ruta} · {cmd})", "producto verificado por comando"
    if prop == "CERRADA-POR-DISEÑO":
        return "CERRAR", f"{ROT} · CERRADA (diseño: {ruta or nota[:120]})", "objeto retirado"
    if prop == "SIN-OBJETO":
        return "CERRAR", f"{ROT} · SIN-OBJETO ({ruta or nota[:120]})", "sin objeto accionable"
    if prop == "DUPLICADA":
        return "CERRAR", f"{ROT} · CERRADA (duplicada: {nuevo or ruta})", "duplicada"
    if prop == "CERRADA-POR-FIRMA":
        if fid in FIRMA_ES_DUPLICADA:
            return "CERRAR", f"{ROT} · CERRADA (duplicada: {FIRMA_ES_DUPLICADA[fid]})", "duplicada"
        if fid in FIRMA_VIAJA_EN:
            a = FIRMA_VIAJA_EN[fid]
            return "DUENO", f"EN-CURSO ({a} · rama {EN_VUELO[a]})", "firma dada; producto viaja en acto en vuelo"
        if fid in FIRMA_CON_PRODUCTO_PENDIENTE:
            return "DUENO", f"{MESA} · encargo por escribir: {FIRMA_CON_PRODUCTO_PENDIENTE[fid]}", \
                "firma dada; producto sin acto"
        return "CERRAR", f"{ROT} · CERRADA (firma: {ruta})", "firma ya dada"
    if prop == "EN-CURSO":
        d = _dueno_en_curso(f"{nuevo} {nota}")
        if d and not RE_DERIVA.search(nuevo):
            return "DUENO", d, "acto en vuelo"
        return "DUENO", f"{MESA} · cerrable al fusionar el [deriva] o su acto: {nuevo[:120]}", \
            "EN-CURSO propuesto sin acto en vuelo verificable"
    if prop == "REASIGNAR":
        m = re.search(r"forense/encargos/\S+?\.md", f"{nuevo} {ruta}")
        if m and os.path.exists(os.path.join(RAIZ, m.group(0))):
            return "DUENO", f"CAJA ({m.group(0)})", "reasignada a encargo archivado"
        return "DUENO", f"{MESA} · encargo por escribir: {nota[:120]}", "reasignación sin encargo archivado"
    if prop == "ESPERA-APERTURA":
        return "DUENO", nuevo_crudo if nuevo_crudo.startswith("APERTURA (") else f"APERTURA ({nuevo or ruta})", "ola reservada"
    if prop == "ESPERA-ADQUISICION":
        return "DUENO", nuevo_crudo if nuevo_crudo.startswith("ADQUISICION (") else f"ADQUISICION ({nuevo or ruta})", \
            "dato no adquirido"
    if prop == "HUMANO":
        return "DUENO", f"{MESA} · HUMANO: {nota[:160]}", "acción con identidad real"
    if prop == "HOJA-MESA":
        return "DUENO", f"{MESA} · hoja de irreversibles", "irreversible: a la hoja"
    if prop == "DECIDIR-REVERSIBLE":
        if fid in DECIDE_Y_CIERRA:
            return "CERRAR", f"{ROT} · CERRADA (firma: delegación de mesa 28/sep, "\
                             f"forense/analisis/pendientes-3/decididas-por-delegacion.tsv#{fid})", \
                "decidida por delegación y cerrada"
        return "DUENO", f"{MESA} · encargo por escribir (decidida por delegación: "\
                        f"decididas-por-delegacion.tsv)", "decidida por delegación; el acto no existe"
    return "DUENO", f"{MESA} · sin determinar por la evidencia: {nota[:120]}", "NO-DETERMINADO"


def limpia(s):
    return re.sub(r"[\t\r\n]+", " ", s or "").strip()


def sin_parentesis(s):
    """La cita va dentro de `CERRADA (…)`: un paréntesis interno cortaría el
    dictamen que `cierre_acto._RE_DICTAMEN_CIERRE` lee."""
    return s.replace("(", "[").replace(")", "]")


def main():
    props = []
    for f in sorted(glob.glob(os.path.join(AQUI, "evidencia", "prop-A*.tsv"))):
        ls = [l for l in open(f, encoding="utf-8").read().split("\n") if l.strip()]
        cab = ls[0].split("\t")
        for l in ls[1:]:
            props.append(dict(zip(cab, l.split("\t"))))
    out, dele, vistos = [], [], set()
    for p in props:
        if p["id"] in vistos:
            sys.exit(f"id repetido en la evidencia: {p['id']}")
        vistos.add(p["id"])
        acc, val, porque = adjudica({k: limpia(v) for k, v in p.items()})
        out.append([p["id"], p["propuesta"], acc,
                    val if acc == "CERRAR" else "", val if acc == "DUENO" else "", porque])
        if p["propuesta"] == "DECIDIR-REVERSIBLE":
            dele.append([p["id"], "CIERRA" if acc == "CERRAR" else "DUEÑO-MESA", limpia(p["nota"])[:600]])
    for fid, suc in NUEVAS_TRAS_MERGE.items():
        out.append([fid, "NUEVA-TRAS-MERGE", "DUENO", "", f"{MESA} · encargo por escribir: {suc}",
                    "nacida durante el barrido; sucesor sin encargo archivado"])
    with open(os.path.join(AQUI, "dictamen-pendientes-3.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\tpropuesta_evidencia\taccion\tcerrado_por\tnuevo_sucesor\tporque\n")
        for r in out:
            fh.write("\t".join(r) + "\n")
    with open(os.path.join(AQUI, "decididas-por-delegacion.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\topcion\trazon\n")
        for r in dele:
            fh.write("\t".join(r) + "\n")
    from collections import Counter
    print(f"{len(out)} filas · " + " · ".join(f"{k} {v}" for k, v in Counter(r[2] for r in out).items()))
    print("dueños:", dict(Counter(r[4].split(" (")[0] for r in out if r[2] == "DUENO")))


if __name__ == "__main__":
    main()
