"""Guardias de cobertura e integridad del corte documental ASTRA5-U0."""

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "forense/analisis/dominios"


def read(name):
    with (DIR / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_censo_vivo_y_complemento():
    paths = list((ROOT / "corpus/reports").glob("*.md")) + list(
        (ROOT / "corpus/forense").glob("*.md")
    )
    rows = read("report-a-dominio-v1_0.tsv")
    assert len(paths) == len(rows) == 37
    assert {row["ruta"] for row in rows} == {str(p.relative_to(ROOT)) for p in paths}
    for row in rows:
        assert hashlib.sha256((ROOT / row["ruta"]).read_bytes()).hexdigest() == row["sha256_recalculado"]
    compass = [row for row in rows if row["ruta"].endswith("compass-4-e29a28d4-credito-popular-2026.md")]
    assert len(compass) == 1
    assert compass[0]["rol"] == "complemento_forense_credito_popular"


def test_candidatas_tienen_procedencia_y_no_son_dictamen():
    rows = read("candidatas-v1_0.tsv")
    assert {row["ruta"] for row in rows} == {row["ruta"] for row in read("report-a-dominio-v1_0.tsv")}
    for row in rows:
        path = ROOT / row["ruta"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_recalculado"]
        assert path.read_text(encoding="utf-8").splitlines()[int(row["linea"]) - 1].strip() == row["pasaje_candidato"]


def test_corte_enoe_no_confunde_medibilidad_y_reserva():
    rows = read("corte-enoe-v1_0.tsv")
    assert len(rows) == 3
    assert len({row["id_afirmacion"] for row in rows}) == len(rows)
    for row in rows:
        assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
        assert row["estado_verificacion"] == "CERRADA"
        assert "diseño muestral" in row["dictamen_razon"]
        assert "NO ABIERTO" in row["datos_id_estado"]
        assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_cortes_documentales_conservan_componentes_y_fuentes():
    files = ["corte-tecnologia-v1_0.tsv", "corte-endireh-v1_0.tsv", "corte-politica-v1_0.tsv"]
    for name in files:
        rows = read(name)
        assert len(rows) == 1
        row = rows[0]
        assert row["estado_verificacion"] == "CERRADA"
        assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
        assert row["componente_contrastable"] and row["limite_inferencial"]
        assert "NO ABIERTO" in row["datos_id_estado"] or "no recalculado" in row["datos_id_estado"]
        assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_corte_finanzas_usa_documento_ya_integrado_y_universos():
    rows = read("corte-finanzas-v1_0.tsv")
    assert len(rows) == 10
    assert len({row["id_afirmacion"] for row in rows}) == 10
    for row in rows:
        assert row["estado_verificacion"] == "CERRADA"
        assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
        assert "#1088 integrado en main 0edf93e2" in row["documento_id_hash_pagina"]
        assert "P" in row["pregunta_textual_codigo_respuestas"]
        assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_corte_seguridad_no_convierte_cifra_negra_en_motivo():
    row, = read("corte-seguridad-v1_0.tsv")
    assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
    assert "BP1_20" in row["pregunta_textual_codigo_respuestas"]
    assert "no identifica tolerancia" in row["limite_inferencial"]
    assert "envipe2025_diseno_muestral_pdf" in row["documento_id_hash_pagina"]
    assert "main e792419c" in row["documento_id_hash_pagina"]
    assert "no tiene RESULT adjudicado" in row["dictamen_razon"]


def test_enut_documentos_en_main_y_limite_de_planeacion():
    rows = read("corte-tiempo-v1_0.tsv")
    row = next(row for row in rows if row["id_afirmacion"] == "ASTRA5-U0-TIME-002")
    assert {row["id_afirmacion"] for row in rows[1:]} == {f"ASTRA5-U0-TIME-{n:03d}" for n in (3, 4, 5)}
    assert row["estado_verificacion"] == "CERRADA"
    assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
    assert "#1090 integrado en main 74b28f30" in row["documento_id_hash_pagina"]
    assert "TRAB_NO_REM_VOL" in row["pregunta_textual_codigo_respuestas"]
    assert "no miden directamente planeación" in row["limite_inferencial"]
    assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_lectura_tiempo_traza_los_15_hallazgos_sin_cierre_falso():
    rows = read("lectura-tiempo-v1_0.tsv")
    source = (ROOT / "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 16
    assert {row["id_lectura"] for row in rows[:15]} == {f"LECTURA-112051b2-{n:02d}" for n in range(1, 16)}
    assert rows[15]["id_lectura"] == "LECTURA-112051b2-INT-PM"
    for n, row in enumerate(rows[:15], 1):
        assert row["archivo_fuente_linea"].endswith(f":L{n + 12}")
        assert source[n + 11].startswith(f"{n}. ")
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"].startswith("ASTRA5-")
        assert row["siguiente_operacion"]
    assert rows[9]["estado_lectura"] == "NO-AFIRMACION-POSITIVA"
    assert "no tasa de descuento temporal" in rows[10]["componente_dictaminado_o_residual"]


def test_lectura_tecnologia_traza_15_hallazgos_y_separa_unidades():
    rows = read("lectura-tecnologia-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 18
    assert {row["id_lectura"] for row in rows[:15]} == {f"LECTURA-d47463c2-{n:02d}" for n in range(1, 16)}
    for row in rows[:15]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md").read_text(encoding="utf-8").splitlines()
    for row in rows[15:]:
        assert source[int(row["archivo_fuente_linea"].rsplit(":L", 1)[1]) - 1]
    for row in rows:
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"].startswith("ASTRA5-")
        assert row["siguiente_operacion"]
    assert "registros distintos" in rows[4]["componente_dictaminado_o_residual"]
    assert "COLA-MESA-SALUD" == rows[11]["estado_lectura"]


def test_lectura_finanzas_traza_13_hallazgos_y_conserva_contratos():
    rows = read("lectura-finanzas-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 13
    assert {row["id_lectura"] for row in rows} == {f"LECTURA-d6710e19-{n:02d}" for n in range(1, 14)}
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-MESA-DINERO"
        assert row["siguiente_operacion"]
    assert "ASTRA5-U0-FIN-004" in rows[9]["contrato_existente"]
    assert "ASTRA5-U0-FIN-006" in rows[9]["contrato_existente"]


def test_forense_credito_conserva_complemento_y_no_recuenta_casos():
    rows = read("lectura-credito-popular-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 24
    assert {row["id_lectura"] for row in rows[:9]} == (
        {f"LECTURA-ed13e951-{n:02d}" for n in range(1, 5)}
        | {f"LECTURA-ea74603e-{n:02d}" for n in range(1, 6)}
    )
    for row in rows[:9]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    sources = {p.name: p.read_text(encoding="utf-8").splitlines() for p in (ROOT / "corpus/forense").glob("*.md")}
    for row in rows[9:]:
        path, line = row["archivo_fuente_linea"].rsplit(":L", 1)
        assert sources[path.rsplit("/", 1)[-1]][int(line) - 1]
    for row in rows:
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-MESA-DINERO"
        assert row["siguiente_operacion"]
    assert all(row["rol_fuente"] == "complemento_forense_credito_popular" for row in rows[4:9])
    assert all(row["rol_fuente"] != "forense_base" for row in rows[9:])
    assert len({row["id_lectura"] for row in rows}) == len(rows)
    assert rows[2]["concepto_deduplicado"] == rows[8]["concepto_deduplicado"] == "CRPOP-COLAPSOS"


def test_lectura_politica_traza_14_hallazgos_y_distingue_ine():
    rows = read("lectura-politica-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 14
    assert {row["id_lectura"] for row in rows} == {f"LECTURA-8d989005-{n:02d}" for n in range(1, 15)}
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-U3"
        assert row["siguiente_operacion"]
    assert "61.04%" in rows[2]["componente_dictaminado_o_residual"]
    assert "12.86%" in rows[2]["componente_dictaminado_o_residual"]


def test_lectura_clientelismo_separa_cuatro_resumenes_y_diez_casos():
    rows = read("lectura-clientelismo-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 23
    assert {row["id_lectura"] for row in rows[:4]} == {f"LECTURA-baa568e2-{n:02d}" for n in range(1, 5)}
    for row in rows[:4]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/forense/Validación_Forense_del_Clientelismo_Electoral_en_México__Agencia_del_Votante__Programas_Sociales_y_Límites_de_la_Compra_de_Voto.md").read_text(encoding="utf-8").splitlines()
    for row in rows[4:14]:
        assert source[int(row["archivo_fuente_linea"].rsplit(":L", 1)[1]) - 1].startswith("**CASO ")
    for row in rows[14:]:
        first_line = row["archivo_fuente_linea"].rsplit(":L", 1)[1].split("-L", 1)[0]
        assert source[int(first_line) - 1]
    assert len({row["id_lectura"] for row in rows}) == len(rows)
    assert all(row["propietario"] == "ASTRA5-U3" and row["siguiente_operacion"] for row in rows)
    assert "no tasa nacional" in rows[10]["componente_y_limite"]


def test_lectura_confianza_y_cotejo_enoe_no_funden_universos():
    rows = read("lectura-confianza-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 15
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
        assert row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"]
        assert row["propietario"].startswith("ASTRA5-") and row["siguiente_operacion"]
    assert rows[4]["contrato_existente"] == "ASTRA5-U0-POL-002"
    assert "denuncias" in rows[4]["pregunta_documental_pendiente"]
    assert "incidentes" in rows[4]["pregunta_documental_pendiente"]
    cotejo = read("cotejo-result-enoe-v1_0.tsv")
    assert {row["id_afirmacion"] for row in cotejo} == {f"ASTRA5-U0-ENOE-{n:03d}" for n in range(1, 4)}
    assert all("INTEGRADO_MAIN_76b0e56b" in row["estado_main"] for row in cotejo)
    assert {row["dictamen_contraste"] for row in cotejo} == {
        "CONFIRMA-MAYORIA-TRIMESTRAL", "SIN-CONTRASTE-DIRECTO", "MATIZA-COMPONENTE-SEMANAL"
    }


def test_lectura_trabajo_traza_secciones_y_limita_mezclas():
    rows = read("lectura-trabajo-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 14
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
        assert row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-U1" and row["siguiente_operacion"]
    assert "ASTRA5-U0-ENOE-003" == rows[4]["contrato_existente"]
    assert "ASTRA5-U0-TIME-002" == rows[7]["contrato_existente"]
    inner = read("lectura-trabajo-interno-v1_0.tsv")
    source = (ROOT / "corpus/reports/Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md").read_text(encoding="utf-8").splitlines()
    assert len(inner) == 14
    for row in inner:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith("**Myth ") or source[line - 1].startswith(("**First**", "**Second**", "**Third**", "**Fourth**", "**Fifth**"))
        assert row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-U1" and row["siguiente_operacion"]


def test_forense_aspiracional_casos_no_son_contrafactuales():
    rows = read("lectura-aspiracional-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 19
    for row in rows[:4]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/forense/Consumo_Aspiracional_en_México__Validación_Forense_del_Modelo_Anti-Esencialista.md").read_text(encoding="utf-8").splitlines()
    for row in rows[4:17]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith(("#### Caso ", "### Par 1:", "### Regla "))
    for row in rows[17:]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith(("## (6)", "## Recomendaciones"))
    assert all(row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"] and row["siguiente_operacion"] for row in rows)
    assert all(row["propietario"] == "ASTRA5-MESA-DINERO" for row in rows)
    assert rows[10]["estado_lectura"] == "CORRECCION-TEST-CAUSAL"


def test_forense_credito_facil_deduplica_enif_y_separa_indicadores():
    rows = read("lectura-credito-facil-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 20
    for row in rows[:4]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/forense/Crédito_Fácil_y_Sobreendeudamiento_en_México__Escaneo_de_Indicadores_Adelantados_2025-2026.md").read_text(encoding="utf-8").splitlines()
    for row in rows[4:17]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith(("**Indicador ", "**Regla "))
    for row in rows[17:]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith("## ")
    assert all(row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"] and row["siguiente_operacion"] for row in rows)
    assert all(row["propietario"] == "ASTRA5-MESA-DINERO" for row in rows)
    assert rows[13]["contrato_o_concepto"] == "ASTRA5-U0-FIN-009"


def test_forense_apuestas_conserva_contradicciones_y_casos():
    rows = read("lectura-apuestas-v1_0.tsv")
    index = {row["id_lectura"]: row for row in read("afirmaciones-para-dictamen-v1_0.tsv")}
    assert len(rows) == 29
    for row in rows[:6]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/forense/Apuestas_Conductuales_sobre_el_Consumidor_Mexicano__Validación_Forense_de_Supuestos_contra_Desenlaces_Reales.md").read_text(encoding="utf-8").splitlines()
    for row in rows[6:25]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith(("**Caso ", "**PAR "))
    for row in rows[25:]:
        line = int(row["archivo_fuente_linea"].rsplit(":L", 1)[1])
        assert source[line - 1].startswith(("## ", "### "))
    assert all(row["pregunta_documental_pendiente"] and row["archivo_pieza_exacta"] and row["siguiente_operacion"] for row in rows)
    assert rows[3]["estado_lectura"] == "CONTRADICCION-FORENSES"
    assert rows[10]["concepto_deduplicado"] == "ASP-REGLAS-CONSUMO"


def test_cotejo_endutih_usa_ola_reactivo_y_universo_del_result():
    rows = read("cotejo-result-endutih-v1_0.tsv")
    assert len(rows) == 7
    path = ROOT / "data/corrida0/CALC-ENDUTIH-PISOS-2024-0001/resultados.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == rows[0]["resultados_sha256"]
    result = json.loads(json.loads(path.read_text(encoding="utf-8"))["resultados"]["RESULT-ENDUTIH-PISOS-2024-TABLA"])
    cells = {(cell["dominio"], cell["medida"]): cell for cell in result["celdas"]}
    for row in rows:
        assert row["estado_main"].startswith("INTEGRADO_MAIN_579462b3")
    assert abs(cells["TOTAL", "internet"]["punto"] - 0.8312233799456584) < 1e-12
    assert cells["TOTAL", "no_internet_acceso"]["n"] == 10840
    assert ("TOTAL", "no_internet_habilidad") not in cells
    assert rows[-1]["dictamen_contraste"] == "SIN-CONTRASTE-DIRECTO-9_5"


def test_cotejo_politica_mantiene_olas_y_universos_separados():
    rows = read("cotejo-result-politica-v1_0.tsv")
    assert len(rows) == 7
    locations = {
        "RESULT-INE-PISOS-2024-TABLA": "CALC-INE-PISOS-2024-0001",
        "RESULT-ENCUP-PISOS-2012-TABLA": "CALC-ENCUP-PISOS-2012-0003",
        "RESULT-LAPOP-PISOS-2019-TABLA": "CALC-LAPOP-PISOS-2019-0001",
    }
    for result_id, calc_id in locations.items():
        group = [row for row in rows if row["result_id"] == result_id]
        path = ROOT / f"data/corrida0/{calc_id}/resultados.json"
        assert group and all(row["calc_id"] == calc_id for row in group)
        assert all(row["resultados_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest() for row in group)
        assert all("ARCHIVO_MAIN_72595501" in row["estado_main"] for row in group)
    lapop = [row for row in rows if row["result_id"] == "RESULT-LAPOP-PISOS-2019-TABLA"]
    assert all("2018-19" in row["instrumento_ola"] for row in lapop)
    assert lapop[-1]["dictamen_contraste"] == "OTRA-OLA-NO-RESUELVE-CONTRATO"


def test_endutih_no_confunde_porcentaje_total_con_motivo_condicional():
    contracts = {r["id_afirmacion"]: r for r in read("mapa-parcial-v0_1.tsv")}
    assert len(contracts) == 102
    assert not {f"ASTRA5-U0-MER-{n:03d}" for n in range(1, 4)} & contracts.keys()
    assert all("enoe2026_t1_comunicado" not in str(row) for row in contracts.values())
    assert all(f"ASTRA5-U0-TEC-{n:03d}" in contracts for n in range(1, 11))
    for n in (2, 5, 6, 7):
        row = contracts[f"ASTRA5-U0-TEC-{n:03d}"]
        assert "todas las personas" in row["componente_contrastable"] or "sobre todas las personas" in row["componente_contrastable"]
        assert "P7_1=2" in row["componente_contrastable"]
        assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
    assert "9.5/16.9" in contracts["ASTRA5-U0-TEC-002"]["componente_contrastable"]
    assert "SIN RESULT" in contracts["ASTRA5-U0-TEC-003"]["gen2_existente"]
    assert "P4_4" in contracts["ASTRA5-U0-TEC-004"]["pregunta_textual_codigo_respuestas"]
    assert "EDAD" in contracts["ASTRA5-U0-TEC-008"]["pregunta_textual_codigo_respuestas"]
    assert "SEXO" in contracts["ASTRA5-U0-TEC-009"]["pregunta_textual_codigo_respuestas"]
    assert contracts["ASTRA5-U0-TEC-010"]["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN"
    assert "P3_12" in contracts["ASTRA5-U0-TEC-010"]["pregunta_textual_codigo_respuestas"]
    assert "P3_23" in contracts["ASTRA5-U0-TEC-010"]["pregunta_textual_codigo_respuestas"]
    cotejo = read("cotejo-result-endutih-v1_0.tsv")
    assert cotejo[-1]["id_afirmacion"] == "ASTRA5-U0-TEC-002"
    assert all(r["dictamen_contraste"] == "SIN-CONTRASTE-DIRECTO-86_9-68_5" for r in cotejo[1:3])


if __name__ == "__main__":
    import sys

    pruebas = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    fallos = 0
    for nombre, prueba in pruebas:
        try:
            prueba()
        except Exception as exc:  # noqa: BLE001 - se reporta y se cuenta
            fallos += 1
            print(f"FALLA {nombre}: {type(exc).__name__}: {exc}")
    print(f"{len(pruebas)} pruebas, {fallos} fallos")
    sys.exit(1 if fallos else 0)
