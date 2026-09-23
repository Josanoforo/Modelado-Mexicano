"""Guardias de cobertura e integridad del corte documental ASTRA5-U0."""

import csv
import hashlib
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
    assert row["dictamen"] == "MEDIBLE-CON-ADQUISICIÓN"
    assert "BP1_20" in row["pregunta_textual_codigo_respuestas"]
    assert "no identifica tolerancia" in row["limite_inferencial"]
    assert "envipe2025_diseno_muestral_pdf" in row["documento_id_hash_pagina"]
    assert "#1089 RAMA, ausente de main" in row["documento_id_hash_pagina"]


def test_enut_documentos_en_main_y_limite_de_planeacion():
    row, = read("corte-tiempo-v1_0.tsv")
    assert row["estado_verificacion"] == "CERRADA"
    assert row["dictamen"] == "MEDIBLE-EN-CORPUS"
    assert "#1090 integrado en main 74b28f30" in row["documento_id_hash_pagina"]
    assert "TRAB_NO_REM_VOL" in row["pregunta_textual_codigo_respuestas"]
    assert "no miden directamente planeación" in row["limite_inferencial"]
    assert hashlib.sha256((ROOT / row["report"]).read_bytes()).hexdigest() == row["report_sha256"]


def test_lectura_tiempo_traza_los_15_hallazgos_sin_cierre_falso():
    rows = read("lectura-tiempo-v1_0.tsv")
    source = (ROOT / "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 15
    assert {row["id_lectura"] for row in rows} == {f"LECTURA-112051b2-{n:02d}" for n in range(1, 16)}
    for n, row in enumerate(rows, 1):
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
    assert len(rows) == 15
    assert {row["id_lectura"] for row in rows} == {f"LECTURA-d47463c2-{n:02d}" for n in range(1, 16)}
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
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
    assert len(rows) == 9
    assert {row["id_lectura"] for row in rows} == (
        {f"LECTURA-ed13e951-{n:02d}" for n in range(1, 5)}
        | {f"LECTURA-ea74603e-{n:02d}" for n in range(1, 6)}
    )
    for row in rows:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
        assert row["pregunta_documental_pendiente"]
        assert row["archivo_pieza_exacta"]
        assert row["propietario"] == "ASTRA5-MESA-DINERO"
        assert row["siguiente_operacion"]
    assert all(row["rol_fuente"] == "complemento_forense_credito_popular" for row in rows[4:])
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
    assert len(rows) == 14
    assert {row["id_lectura"] for row in rows[:4]} == {f"LECTURA-baa568e2-{n:02d}" for n in range(1, 5)}
    for row in rows[:4]:
        assert row["archivo_fuente_linea"] == f'{index[row["id_lectura"]]["ruta"]}:L{index[row["id_lectura"]]["linea"]}'
    source = (ROOT / "corpus/forense/Validación_Forense_del_Clientelismo_Electoral_en_México__Agencia_del_Votante__Programas_Sociales_y_Límites_de_la_Compra_de_Voto.md").read_text(encoding="utf-8").splitlines()
    for row in rows[4:]:
        assert source[int(row["archivo_fuente_linea"].rsplit(":L", 1)[1]) - 1].startswith("**CASO ")
    assert len({row["id_lectura"] for row in rows}) == 14
    assert all(row["propietario"] == "ASTRA5-U3" and row["siguiente_operacion"] for row in rows)
    assert "no tasa nacional" in rows[10]["componente_y_limite"]
