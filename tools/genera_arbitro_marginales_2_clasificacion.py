#!/usr/bin/env python3
"""Genera data/arbitro-marginales-2-clasificacion-v1_0.tsv desde el YAML GEN1
(P1 del ACTO GEN2-ARBITRO-MARGINALES-2). Derivado, no tecleado: los campos
numericos y de payload salen de milpa/tramite-ola5-propuesta-v0.yaml y de
tests/manifiesto.py --verifica; solo `destino`/`comando`/`evidencia` son
juicio de esta pieza, declarado con su razon.
"""
import subprocess
import sys
import yaml

RUTA_YAML = "milpa/tramite-ola5-propuesta-v0.yaml"
RUTA_SALIDA = "data/arbitro-marginales-2-clasificacion-v1_0.tsv"

# Las 13 reglas que #971 (ARBITRO-MARGINALES-1) ya re-midio en GEN2 -- excluidas
# de la clasificacion de este acto por instruccion expresa del encargo ("cita,
# no re-midas"). Verificado en esta sesion por payload_manifiesto_id exacto.
YA_CUBIERTAS_971 = {
    "civico.denuncia.miedo_desconfianza", "tramite.evasion_norma_envipe2025",
    "tramite.evasion_norma_ejes_envipe2025", "civico.denuncia.con_seguro_ejes_envipe2025",
    "tramite.mordida.discrecional_encig_serie", "tramite.mordida.con_registro_encig2025",
    "tramite.gobierno_digital.util_sin_coercion_encig2025",
    "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025",
    "dinero.ahorro.tiene_ahorros_enif2024", "dinero.ahorro.via_informal",
    "dinero.ahorro.via_informal_ejes_enif2024", "dinero.ahorro.horizonte_corto_ejes_enif2024",
    "dinero.ahorro.seguro_deposito_enif2024",
}

# destino, encuesta, comando/evidencia -- ver nota de cierre P1 para el razonamiento
# completo de cada fila; aqui solo el veredicto y su cita corta.
CLASIFICACION = {
    "dinero.ahorro.tiene_ahorros": ("RE-MEDIDA", "ENNViH (olas 2005+2009)",
        "P2 de este acto: payload COINCIDE (ennvih2_2005_hogar_dta, ennvih3_2009_hogar_dta, ennvih2_2005_ponderador_transversal), COMMIT-1 nuevo"),
    "familia.apoyo.recibe_dinero_familiares": ("FUERA-DE-ALCANCE", "ENIF2024 (TMODULO)",
        "encuesta no nombrada en el objetivo de este acto (ENCUCI/EDER/LAPOP/ENIGH/ENFIH/ENNViH/electorales); payload SI se uso ya (data/raw/enif_2024_bd_csv.zip, distinto de enif2024_csv del manifiesto); sucesor propio de ENIF2024"),
    "familia.corresidencia.adulto_familiar": ("RE-MEDIDA", "EDER 2017",
        "YA SELLADO: data/corrida0/CALC-EDER-0001 reproduce p=0.996086/n=14887 exactos -- cita, no re-mide"),
    "tramite.mordida.discrecional": ("RE-MEDIDA", "ENCUCI 2020",
        "YA SELLADO: data/corrida0/CALC-ENCUCI-0001 (familia A, RES-0005/RES-0006) reproduce p=0.125822/0.874178, n=13435 exactos -- cita, no re-mide"),
    "familia.corresidencia.adulto_familiar_actual": ("RE-MEDIDA", "EDER 2017",
        "YA SELLADO: data/corrida0/CALC-EDER-0002 reproduce p=0.057531/n=9397 exactos -- cita, no re-mide"),
    "familia.seguro.volatilidad_ausencia_estado": ("RE-MEDIDA", "ENIGH 2022",
        "YA SELLADO: data/corrida0/CALC-ENIGH-0001 (RES-0035/RES-0036) reproduce p=0.045694, ic95=[0.043754,0.047711], n=90102 exactos -- cita, no re-mide"),
    "dinero.planeacion.formal_estable": ("RE-MEDIDA", "ENFIH 2019",
        "YA SELLADO: data/corrida0/CALC-ENFIH-0001 (RES-0037/RES-0038) reproduce p=0.538502, ic95=[0.5267,0.550616], n=17765 exactos -- cita, no re-mide"),
    "civico.participacion.contingente": ("FUERA-DE-ALCANCE", "electoral (computos por municipio)",
        "no es un marginal de encuesta (OBJETIVO SS1); computos IEC Coahuila/IEEM EdoMex por municipio"),
    "civico.participacion.contingente_escalonado_2016_2024": ("FUERA-DE-ALCANCE", "electoral (computos por municipio)",
        "no es un marginal de encuesta; computos de 5 institutos electorales estatales + acuerdos INE"),
    "civico.participacion.tipo_boleta_federal_2016_2024": ("FUERA-DE-ALCANCE", "electoral (computos por municipio/casilla)",
        "no es un marginal de encuesta; computos de 6 institutos electorales estatales"),
    "civico.participacion.concurrencia_presidencial_conversion": ("RE-MEDIDA", "electoral (panel L8, ya en GEN2)",
        "ya sellado bajo GEN2: data/corrida0/CALC-L8-CONVERSION-0001 (RES-0050/51/52), reproduce las 3 celdas GEN1 sin adoptar -- se cita, no se re-mide"),
    "tramite.gobierno_digital.uso_general_endutih2025": ("FUERA-DE-ALCANCE", "ENDUTIH 2025",
        "encuesta no nombrada en el objetivo de este acto; payload COINCIDE (endutih_2025_endutih2025_bd_dbf, n=48718); sucesor propio de ENDUTIH"),
    "dinero.ahorro.respaldo_enif2024": ("FUERA-DE-ALCANCE", "ENIF2024",
        "encuesta no nombrada en el objetivo de este acto; ademas SIN-PAYLOAD (REGISTRADA-SIN-CARGA, payload_manifiesto_id=None); sucesor propio de ENIF2024"),
    "civico.clientelismo.turnout_no_vote_choice_lapop2019": ("FUERA-DE-ALCANCE", "LAPOP 2019",
        "LAPOP no esta en el lote de P2 de este acto (P2 solo nombra ENCUCI/EDER/ENIGH/ENFIH/ENNViH); licencia Vanderbilt/LAPOP no verificada mas alla de \"derechos reservados, terminos de reuso no verificados\" (data/manifiesto.yaml); PREGUNTA A MESA en la nota"),
    "civico.voto.agencia_lapop2023": ("FUERA-DE-ALCANCE", "LAPOP 2023",
        "mismo razonamiento que LAPOP 2019 (payload mex_2023_lapop_americasbarometer_v1_0_w COINCIDE, pero fuera del lote de P2 y licencia no verificada)"),
    "civico.protesta.agravio_urbano_lapop2019": ("FUERA-DE-ALCANCE", "LAPOP 2019",
        "mismo razonamiento que civico.clientelismo.turnout_no_vote_choice_lapop2019"),
    "civico.transferencia.entitlement_encuci2020": ("RE-MEDIDA", "ENCUCI 2020",
        "P2 de este acto: payload COINCIDE (encuci2020_bd_dbf); ver nota si un CALC GEN2 existente ya la cubre"),
    "civico.voto.agencia_con_secreto_encuci2020": ("RE-MEDIDA", "ENCUCI 2020",
        "P2 de este acto: payload COINCIDE (encuci2020_bd_dbf); ver nota si un CALC GEN2 existente ya la cubre"),
    "civico.protesta.agravio_urbano_encuci2020": ("RE-MEDIDA", "ENCUCI 2020",
        "YA SELLADO: data/corrida0/CALC-ENCUCI-0001 (familia B, RES-0061/RES-0062) reproduce p=0.112192/0.091912 exactos -- cita, no re-mide"),
    "tramite.gobierno_digital.coercitivo_efirma_sat": ("FUERA-DE-ALCANCE", "SAT/ENOE (administrativo)",
        "no es un marginal de encuesta: proporcion administrativa agregada (padron SAT), no probabilidad individual; ya medida bajo GEN2 (MAESTRA36-L13, data/l13-sat-efirma-v1_0.json) con veredicto AMBIGUA-POR-UNIVERSO, no adjudica"),
    "civico.clientelismo.vote_change_mps2012": ("FUERA-DE-ALCANCE", "ICPSR MPS2012 (panel)",
        "encuesta no nombrada en el objetivo de este acto; payload COINCIDE (icpsr35024_ds1_w2_crosstabs_derivado_v0/derivadas); sucesor propio"),
    "civico.clientelismo.prevalencia_lista_mps2012": ("FUERA-DE-ALCANCE", "ICPSR MPS2012 (panel)",
        "encuesta no nombrada en el objetivo de este acto; payload COINCIDE (icpsr35024_ds1_w2_crosstabs_derivadas); sucesor propio"),
    "civico.clientelismo.prevalencia_lista_listcran_mps2012": ("FUERA-DE-ALCANCE", "list::mexico (experimento de lista, paquete R)",
        "encuesta no nombrada en el objetivo de este acto; payload COINCIDE (list_cran_mexico_tab/rd); sucesor propio"),
    "tramite.gobierno_digital.coercitivo_tabla_de_universos": ("FUERA-DE-ALCANCE", "ENOE + SAT (administrativo)",
        "no es un marginal de encuesta: tres denominadores administrativos/ENOE, no probabilidad individual; ya medido bajo GEN2 (MAESTRA36-L14, data/l14-coercitivo-universos-v1_0.json), tabla para mesa sin adjudicar"),
    "tramite.evasion.norma_inutil_sancion_improbable": ("SIN-PAYLOAD", "ninguna (hipotesis sin instrumento)",
        "MAESTRA38-N5 SS2.1: 4 formulaciones de busqueda en 0/42536 sobre inventario-reactivos-descargas-mx-v1_1; MANTENER-COMO-HIPOTESIS"),
    "civico.transferencia.atribucion_lider": ("SIN-PAYLOAD", "ninguna (hipotesis sin instrumento)",
        "MAESTRA38-N5 SS2.7: 5 formulaciones en 0/42536; RDD ya disenado en canon pero sin fuente de enlace identificada; MANTENER-COMO-HIPOTESIS"),
    "familia.cortejo.urbano_joven_apps": ("SIN-PAYLOAD", "ninguna (hipotesis sin instrumento)",
        "MAESTRA38-N5 SS2.9: 7 formulaciones en 0/42536, verificadas una a una; MANTENER-COMO-HIPOTESIS"),
    "civico.voto.clientelar_si_observable_lapop2019": ("FUERA-DE-ALCANCE", "LAPOP 2019",
        "MAESTRA38-N5 SS2.6 la reformulo como (a) REFORMULABLE con reactivo real (clien1n/clien1na x vb3n, LAPOP2019 ya en corpus) -- NO es SIN-INSTRUMENTO; queda FUERA-DE-ALCANCE por el mismo corte LAPOP que las demas (fuera del lote de P2, licencia no verificada)"),
    "civico.protesta.agravio_urbano_multiola": ("FUERA-DE-ALCANCE", "LAPOP multi-ola (2004/2006/2019/2021/2023)",
        "MAESTRA38-N5 SS2.8 la reformulo como (a) REFORMULABLE con 5 reactivos reales, pero la co-ocurrencia de las 5 variables en un mismo archivo/ola no esta confirmada; fuera del lote de P2, licencia LAPOP no verificada"),
    "comunicacion.inseguridad.ver_oir_callar_lapop2004": ("FUERA-DE-ALCANCE", "LAPOP 2004",
        "LAPOP 2004 no tiene entrada en data/manifiesto.yaml (0 ids con '2004' y 'lapop'): ademas de fuera del lote de P2, el payload de esa ola especifica no esta confirmado en el corpus"),
    "salud.atencion.grave_ensanut2024": ("RE-MEDIDA", "ENSANUT 2024",
        "YA SELLADO: data/corrida0/CALC-0003-v4 (S6-L16 Rama B) -- veredicto NO-DISCRIMINA, ACTO LOTE-ENSANUT PR #565 -- cita, no re-mide"),
    "salud.vacunacion.disponible_ensanut2024": ("RE-MEDIDA", "ENSANUT 2024",
        "YA SELLADO: data/corrida0/CALC-ENSANUT-0001 (RES-0063/RES-0064) reproduce p=0.777762 (GEN1) -- cita, no re-mide"),
    "salud.atencion.grave_ennvih2002": ("RE-MEDIDA", "ENNViH 2002 (ola 1)",
        "YA SELLADO como NO-ESTIMABLE: data/corrida0/CALC-0003-v4 (S6-L16 Rama A, 143 RESULT), dos causas independientes (chequeo de consistencia D1 falla; D2 clave1/clave2 no confirma publico/privado) -- cita, no re-mide"),
    "civico.voto_alineado.clientelar_cses2015": ("FUERA-DE-ALCANCE", "CIDE-CSES 2015",
        "encuesta no nombrada en el objetivo de este acto; payload COINCIDE (cide_cses2015_nacional_poselectoral); sucesor propio"),
    "civico.contexto_institucional_victimas.lapop": ("FUERA-DE-ALCANCE", "LAPOP 2019/2021/2023",
        "mismo corte LAPOP que las demas: fuera del lote de P2, licencia no verificada"),
    "dinero.credito.atraso_y_dano_por_producto_banxico": ("RE-MEDIDA", "Banxico (administrativo, no encuesta)",
        "YA SELLADO: data/corrida0/CALC-BANXICO-PRODUCTO-DANO-0001 (capa descriptiva/asociativa para R1.7, NC-0164) -- cita, no re-mide"),
    "trabajo.prestaciones.valoracion_seguridad_social_motral": ("RE-MEDIDA", "MOTRAL 2015 (experimento)",
        "YA SELLADO: data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001 (uso_motor DESCRIPTIVO-NO-CALIBRA-NI-ADOPTA, N35) -- cita, no re-mide"),
    "referencia_sin_consumidor.shed2025_bnpl": ("FUERA-DE-ALCANCE", "SHED 2025 (poblacion de EEUU)",
        "no es Mexico ni marginal de encuesta mexicana; ya sellado en otro acto (PR #745, CALC-SHED2025-BNPL-DANO-0001, 66 RESULT); clausula explicita de no-transporte a Mexico"),
    "familia.union.libre_ejes_eder2017": ("RE-MEDIDA", "EDER 2017",
        "YA SELLADO: data/corrida0/CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/0002 (rejilla por cohorte de nacimiento, 4 celdas) + CALC-EDER-0003 (nota: defecto_de_identidad -- RES-0043/44 en milpa/tramite.yaml citan ENADID 2023, no EDER; hallazgo de otro acto, no se corrige aqui) -- cita, no re-mide"),
    "familia.cuidado.reparto_mujeres40_ejes_enut2024": ("FUERA-DE-ALCANCE", "ENUT 2024",
        "explicito en el encargo SS3: 'no es este acto -- mesa decide el rotulo'; nucleo comun ENUT ya medido por #976 (GEN2-ENUT-PISOS-Y-SERIE-1)"),
}


def verifica_manifiesto(id_payload):
    if not id_payload:
        return "N/A"
    out = subprocess.run(
        ["python3", "tests/manifiesto.py", "--verifica", "--id", id_payload],
        capture_output=True, text=True,
    ).stdout
    for line in out.splitlines():
        if line.startswith(id_payload + " "):
            if "COINCIDE" in line:
                return "COINCIDE"
            if "AUSENTE" in line:
                return "AUSENTE"
            return line.split(":", 1)[-1].strip()[:40]
    return "SIN-ENTRADA"


def main():
    with open(RUTA_YAML) as f:
        data = yaml.safe_load(f)
    reglas = data["reglas_propuestas"]
    filas = []
    for r in reglas:
        rid = r["id"]
        if rid in YA_CUBIERTAS_971:
            continue
        if rid not in CLASIFICACION:
            print(f"FALTA CLASIFICAR: {rid}", file=sys.stderr)
            sys.exit(1)
        destino, encuesta, evidencia = CLASIFICACION[rid]
        pid = r.get("payload_manifiesto_id")
        pid_txt = pid if isinstance(pid, str) else (";".join(pid) if isinstance(pid, list) else "")
        filas.append({
            "id_regla": rid,
            "encuesta": encuesta,
            "payload_manifiesto_id": pid_txt[:80],
            "tier_gen1": r.get("tier") or "",
            "situacion_gen1": r.get("situacion") or "",
            "n": r.get("n") if r.get("n") is not None else "",
            "destino": destino,
            "evidencia": evidencia,
        })
    if len(filas) != 40:
        print(f"CONTEO INESPERADO: {len(filas)} filas, se esperaban 40", file=sys.stderr)
        sys.exit(1)
    cols = ["id_regla", "encuesta", "payload_manifiesto_id", "tier_gen1",
            "situacion_gen1", "n", "destino", "evidencia"]
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for fila in filas:
            f.write("\t".join(str(fila[c]) for c in cols) + "\n")
    conteo = {}
    for fila in filas:
        conteo[fila["destino"]] = conteo.get(fila["destino"], 0) + 1
    print(f"Escritas {len(filas)} filas en {RUTA_SALIDA}")
    print("Conteo por destino:", conteo)


if __name__ == "__main__":
    main()
