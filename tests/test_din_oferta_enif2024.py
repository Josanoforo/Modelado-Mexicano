"""CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001 (acto GEN2-ASTRA6-C2-EJECUCION-1).

Defecto que atrapa: un medidor que abre otra ola o lee otro payload que el
fijado (E.6), y ramas terminales cuya salida el conducto no acepta (D-22(2)).
Sin corpus: ZIP sintético en tmp_path.
"""
import hashlib
import importlib.util
import io
import zipfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001"


def _mod(nombre, ruta):
    s = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = _mod("oferta2024", CALC / "medidor.py")
C = _mod("corrida0_oferta2024", ROOT / "tools/corrida0.py")
SPEC = yaml.safe_load((CALC / "spec.yaml").read_text())
CONTRATO = {"parametros": {"ola": "2024", "bootstrap_replicas": 50},
            "seed": {"valor": 20260909}}


def _zip(tmp_path, filas, cols=None, nombre="TMODULO.csv"):
    cols = cols or M.COLS
    buf = io.StringIO()
    buf.write(",".join(cols) + "\n")
    for r in filas:
        buf.write(",".join(str(r.get(c, "")) for c in cols) + "\n")
    p = tmp_path / "sint.zip"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr(nombre, buf.getvalue().encode("utf-8"))
    return p


def _filas(n=600, rama="total"):
    out = []
    for i in range(n):
        r = {"FAC_PER": "100", "EST_DIS": f"{i % 20:03d}", "UPM_DIS": f"{i % 120:05d}",
             "EDAD_V": str(18 + i % 80)}
        user = i % 3 == 0
        for v in M.TENENCIA:
            r[v] = "2"
        if user:
            r["P5_4_4"] = "1"
        else:
            r["P5_19"] = "1" if i % 5 == 0 else "2"
            r["P5_20"] = f"{1 + i % 10:02d}" if r["P5_19"] == "2" else ""
            r["P5_21"] = str(1 + i % 9) if r["P5_19"] == "1" else ""
        if rama == "singleton":
            r["UPM_DIS"] = r["EST_DIS"]
        if rama == "sin_pase" and not user:
            r["P5_19"] = ""
        if rama == "todos_usuarios":
            r["P5_4_1"] = "1"
        if rama == "peso_cero" and i == 1:
            r["FAC_PER"] = "0"
        if rama == "desconocido" and i == 2:
            r["P5_4_9"] = ""
        out.append(r)
    return out


def _inputs(p):
    return {M.ZIP_ID: {"origen": "manifiesto", "ruta_absoluta": str(p)}}


def _sin_guardia_de_sha(monkeypatch, p):
    monkeypatch.setattr(M, "ZIP_SHA", hashlib.sha256(p.read_bytes()).hexdigest())


@pytest.mark.parametrize("rama", ["total", "singleton", "sin_pase", "todos_usuarios",
                                  "peso_cero", "desconocido", "columna_ausente"])
def test_ramas_terminales_por_conducto(tmp_path, monkeypatch, rama):
    if rama == "columna_ausente":
        p = _zip(tmp_path, _filas(), cols=[c for c in M.COLS if c != "P5_21"])
    else:
        p = _zip(tmp_path, _filas(rama=rama))
    _sin_guardia_de_sha(monkeypatch, p)
    out = M.medir(_inputs(p), CONTRATO)
    assert C._valida_outputs(SPEC, out) == []
    estado = out[M.P + "ESTADO"]
    if rama == "columna_ausente":
        assert estado.startswith("NO-ESTIMABLE-COLUMNA-AUSENTE")
    elif rama == "todos_usuarios":
        assert estado == "NO-ESTIMABLE-COHORTE-VACIA"
    else:
        assert estado == "CONSTRUIBLE"
        s = sum(out[M.P + k + "-P"] for k in ("OFERTA", "PREFERENCIA", "OTRO-NS"))
        assert abs(s - 1.0) < 1e-12
    if rama == "sin_pase":
        assert out[M.P + "PASE-ESTRUCTURAL-P"] == 1.0
    if rama == "singleton":
        assert out[M.P + "METODO-IC"] == "IC-CON-ESTRATOS-DE-UPM-UNICA"


def test_clases_por_texto(tmp_path, monkeypatch):
    # un no usuario 'nunca' con 01 (sucursal lejos) es OFERTA; 06 (no la necesita) PREFERENCIA
    filas = _filas(40)
    for r in filas:
        if r.get("P5_19") == "2":
            r["P5_20"] = "01"
        if r.get("P5_19") == "1":
            r["P5_21"] = "3"
    p = _zip(tmp_path, filas)
    _sin_guardia_de_sha(monkeypatch, p)
    out = M.medir(_inputs(p), CONTRATO)
    nunca, ex = out[M.P + "NUNCA-N"], out[M.P + "EX-USUARIOS-N"]
    assert out[M.P + "OFERTA-P"] == pytest.approx(nunca / (nunca + ex))
    assert out[M.P + "PREFERENCIA-P"] == pytest.approx(ex / (nunca + ex))


@pytest.mark.parametrize("mutacion", ["otro_payload", "payload_extra", "ola", "sha_zip", "sha_base"])
def test_guardia_por_mutacion(tmp_path, monkeypatch, mutacion):
    p = _zip(tmp_path, _filas(30))
    _sin_guardia_de_sha(monkeypatch, p)
    inputs, contrato = _inputs(p), dict(CONTRATO)
    M.medir(inputs, contrato)  # control positivo: sin mutación corre
    if mutacion == "otro_payload":
        inputs = {"envipe2026_csv": inputs[M.ZIP_ID]}
    elif mutacion == "payload_extra":
        inputs["enif2027_csv"] = {"origen": "manifiesto", "ruta_absoluta": str(p)}
    elif mutacion == "ola":
        contrato = {**CONTRATO, "parametros": {**CONTRATO["parametros"], "ola": "2027"}}
    elif mutacion == "sha_zip":
        monkeypatch.setattr(M, "ZIP_SHA", "0" * 64)
    elif mutacion == "sha_base":
        monkeypatch.setattr(M, "BASE_SHA", "0" * 64)
    with pytest.raises(ValueError, match="GUARDIA"):
        M.medir(inputs, contrato)


def test_constantes_de_guardia_casan_con_spec_y_manifiesto():
    ins = {i["id"]: i for i in SPEC["inputs"]}
    assert set(ins) == {M.ZIP_ID, "MEDIDOR-BASE", "SPEC-HUMANA"}
    assert ins["MEDIDOR-BASE"]["sha256"] == M.BASE_SHA
    assert hashlib.sha256((ROOT / M.BASE).read_bytes()).hexdigest() == M.BASE_SHA
    assert SPEC["parametros"]["ola"] == M.OLA
