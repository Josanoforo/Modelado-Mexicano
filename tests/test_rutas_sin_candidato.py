import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rutas_reconcilia_universo_vivo(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "rutas_sin_candidato.py"),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=True,
    )
    with (tmp_path / "rutas.tsv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    reconciliation = json.loads((tmp_path / "reconciliacion.json").read_text())

    assert len(rows) == 153
    assert len({row["resultado_id"] for row in rows}) == 153
    assert Counter(row["tipo_uso"] for row in rows) == {
        "celda_L": 28,
        "celda_R": 14,
        "celda_M": 14,
        "celda_AGREGADO": 14,
        "momento": 22,
        "asignado_probabilidad": 13,
        "condicional_theta": 12,
        "conducta_p_asignado": 10,
        "coeficiente_asignado": 8,
        "coeficiente_ejecutable": 7,
        "corte_pi": 6,
        "celda_D": 3,
        "conducta_p_medido": 2,
    }
    assert reconciliation["por_causa_principal"] == {
        "DATO-O-DOCUMENTACION-FALTANTE": 2,
        "DECISION-O-ESTIMANDO-PENDIENTE": 34,
        "RESERVADO-O-YA-ENCARGADO": 117,
    }


def test_calc_homonimo_del_marcador_no_se_adopta_por_nombre(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "rutas_sin_candidato.py"),
            "--output-dir",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=True,
    )
    with (tmp_path / "rutas.tsv").open(encoding="utf-8") as fh:
        rows = {row["resultado_id"]: row for row in csv.DictReader(fh, delimiter="\t")}

    # CORR-0024 ve CALC-R-CIV-M-01 por una declaración desplazada. El
    # consumidor real es CIV-M-02:R; no se transforma en oferta por homonimia.
    row = rows["RES-0100"]
    assert row["consumidor"].endswith(":CIV-M-02:R")
    assert row["result_observado"] == ""
    assert row["subcausa"] == "MARCADOR-CALC-DE-OTRA-CORRESPONDENCIA-SIN-RESULT-FIJADO"
    assert row["paquete_propuesto"] == "NINGUNO"
