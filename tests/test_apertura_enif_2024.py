"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENIF 2024 (TMODULO) para el expediente de
apertura de los cruces reservados `informal_cualquiera` (forense/prereg-aperturas/ENIF-2024/).

Defecto real que atrapa: NC-0328 (reserva quemada por un cruce de scratch) y los actos perdidos del piloto 3
(D-22: un conducto que no acepta una rama terminal). Sin microdato: el zip es fabricado con las columnas que
`carga()` del árbitro exige. Ramas: todas con soporte, parcial (n < 200), cero puntuadas, réplica degenerada;
auditoría limpia, mutaciones detectadas ANTES de leer, celda fuera de la lista cerrada -> ParoDeGuardia.
"""
from __future__ import annotations

import importlib.util
import io
import json
import math
import os
import random
import sys
import zipfile

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402

REL = "forense/prereg-aperturas/ENIF-2024/medidor_apertura_enif_2024.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load(os.path.join(ROOT, REL), "ap_enif_2024_t")
G, E = M.G, M.E
FUENTE = open(os.path.join(ROOT, REL), encoding="utf-8").read()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": M.esquema_resultados()}, out) == []
    assert out[f"{M.P}-DICTAMEN"] in G.VOCABULARIO
    assert out[f"{M.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _zip(tmp_path, n, seed=7, nombre="enif_2024_bd_csv.zip"):
    """TMODULO.csv fabricado con la forma que lee `carga()` del árbitro."""
    A = M.arbitro()
    rng = random.Random(seed)
    filas = []
    for i in range(n):
        f = {"SEXO": rng.choice(["1", "2"]), "EDAD_V": str(rng.randint(18, 99)),
             "NIV": rng.choice(["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "99"]),
             "TLOC": rng.choice(["1", "2", "3", "4"]), "P3_13": rng.choice(["1", "2", "3", "7", ""]),
             "FAC_PER": str(rng.randint(50, 900)), "P7_1": rng.choice(["1", "2"]), "EST_DIS": f"{1 + i % 6:03d}", "UPM_DIS": f"{1 + (i // 3) % 40:04d}"}
        for c in A.INFORMAL:  # P(alguna == 1) ~ 0.56, del orden del nacional: la cobertura cae entre 0 y n
            f[c] = "1" if rng.random() < 0.128 else "2"
        for c in A.FORMAL:
            f[c] = rng.choice(["1", "2", "2", "2", ""])
        for c in A.CUENTAS:
            f[c] = rng.choice(["1", "2", "2", ""])
        filas.append(f)
    buf = io.StringIO()
    pd.DataFrame(filas).to_csv(buf, index=False)
    ruta = tmp_path / nombre
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("TMODULO.csv", buf.getvalue().encode("latin-1"))
    return str(ruta)


def _inputs(ruta):
    d = {k: {} for k, _r, _n in M.CONTRATO["repo"]}
    d[M.PAYLOAD] = {"ruta_absoluta": ruta}
    return d


# ── lista cerrada y rejilla ─────────────────────────────────────────────────
def test_lista_cerrada_es_la_del_contendiente_sellado():
    ic = json.load(open(os.path.join(ROOT, M.PISO_IC[1]), encoding="utf-8"))["resultados"]
    pre = "RESULT-C2IC-ENIF2024-INFORMAL-CUALQUIERA-"
    derivadas = {k[len(pre):-len("-IC95INF")] for k in ic if k.startswith(pre) and k.endswith("-IC95INF")}
    assert derivadas == set(M.CELDAS_AUTORIZADAS) and len(M.CELDAS_AUTORIZADAS) == 68
    assert {M._par_de(c) for c in M.CELDAS_AUTORIZADAS} == set(M.PARES)
    piso = M.piso_sellado()
    assert all(all(isinstance(v, float) for v in t) for t in piso.values())


def test_slug_y_ejes_del_arbitro_generan_exactamente_la_lista():
    A = M.arbitro()
    cats = {e.nombre: list(e.orden) for e in A.EJES_P2}
    cats["cuenta_formal"] = list(A.EJE_CUENTA_SECUNDARIO.orden)
    gen = {f"{par}-{M.slug(x)}-X-{M.slug(y)}" for par, (a, b) in M.PARES.items() for x in cats[a] for y in cats[b]}
    assert gen == set(M.CELDAS_AUTORIZADAS)


# ── guardia E.6 ─────────────────────────────────────────────────────────────
def test_auditoria_limpia_y_mutaciones_detectadas():
    assert G.auditoria_ast(FUENTE) == []
    for mut in E.MUTACIONES:
        assert G.auditoria_ast(FUENTE + "\n\n" + mut), mut


def test_mutacion_para_antes_de_leer(tmp_path):
    """La auditoría corre sobre el archivo antes de tocar el payload: con un cruce de dos llaves añadido,
    medir() levanta ParoDeGuardia aunque la ruta del payload no exista."""
    mutado = tmp_path / "medidor_mutado.py"
    mutado.write_text(FUENTE.replace('AQUI = os.path.dirname(os.path.abspath(__file__))',
                                     f'AQUI = {os.path.dirname(os.path.join(ROOT, REL))!r}') + "\n\n" + E.MUTACIONES[0],
                      encoding="utf-8")
    Mm = _load(str(mutado), "ap_enif_2024_mutado_t")
    with pytest.raises(Mm.G.ParoDeGuardia, match="auditoría AST"):
        Mm.medir(_inputs(str(tmp_path / "no-existe.zip")), {})


def test_celda_fuera_de_la_lista_levanta_paro():
    y, w = np.ones(3), np.ones(3)
    et = np.array(["EDADXSEXO-18-29-X-1-HOMBRE"] * 3, dtype=object)
    with pytest.raises(G.ParoDeGuardia):
        M.r_por_celda(y, w, et, ["AHORRA-SOLO-INFORMAL-EDADXSEXO-18-29-X-1-HOMBRE"])
    with pytest.raises(G.ParoDeGuardia):
        M.r_por_celda(y, w, et, ["EDADXFORMALIDAD-18-29-X-SIN-SEGURIDAD-SOCIAL"])


def test_etiqueta_no_autorizada_no_se_agrega():
    et = M.etiquetas_de_par("EDADXSEXO", ["18-29", "(fuera)", "18-29"], ["1 Hombre", "2 Mujer", "3 Otro"], "(fuera)")
    assert et.tolist() == ["EDADXSEXO-18-29-X-1-HOMBRE", None, None]


def test_medir_rechaza_input_ajeno():
    with pytest.raises(G.ParoDeGuardia):
        M.medir({"otro_payload": {"ruta_absoluta": "/nada"}}, {})


# ── conducto: medir() de punta a punta sobre zips fabricados ────────────────
def test_todas_con_soporte(tmp_path):
    out = M.medir(_inputs(_zip(tmp_path, 40000)), {})
    _ok(out)
    assert out[f"{M.P}-N"] == 68


def test_todas_con_soporte_y_cobertura_parcial(tmp_path):
    """Rama con 0 < k < n (R sintética movida hacia el piso)."""
    piso = M.piso_sellado()
    r = {c: (piso[c][0] if i % 2 else 0.99) for i, c in enumerate(M.CELDAS_AUTORIZADAS)}
    out = E.salida(M.P, M.filas(piso, r))
    _ok(out)
    assert 0 < out[f"{M.P}-K"] < out[f"{M.P}-N"] == 68


# Hallazgo del subagente (28/sep): wilson(0, 68) daba -3.5e-18; guardia_apertura.wilson ya acota a [0, 1].
def test_rama_k_cero_sella():
    piso = M.piso_sellado()
    out = E.salida(M.P, M.filas(piso, {c: 0.999 for c in M.CELDAS_AUTORIZADAS}))
    assert out[f"{M.P}-K"] == 0 and out[f"{M.P}-N"] == 68
    _ok(out)


def test_parcial(tmp_path):
    out = M.medir(_inputs(_zip(tmp_path, 4000, seed=8)), {})
    _ok(out)
    assert 0 < out[f"{M.P}-N"] < 68


def test_cero_puntuadas(tmp_path):
    out = M.medir(_inputs(_zip(tmp_path, 300, seed=9)), {})
    _ok(out)
    assert out[f"{M.P}-N"] == 0 and out[f"{M.P}-DICTAMEN"] == "NO-ESTIMABLE"


def test_guardia_del_arbitro_para(tmp_path):
    ruta = tmp_path / "enif_2024_bd_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("TMODULO.csv", "SEXO,EDAD_V\n1,30\n")
    with pytest.raises(G.ParoDeGuardia, match="guardia del árbitro"):
        M.medir(_inputs(str(ruta)), {})


def test_ramas_sinteticas_pasan_el_conducto():
    ramas = M.ramas_sinteticas()
    assert len(ramas) == 4
    for out in ramas:
        _ok(out)
    assert ramas[2][f"{M.P}-DICTAMEN"] == "NO-ESTIMABLE"


def test_modulo_7_no_sobrevive_a_la_lectura(tmp_path):
    A = M.arbitro()
    df = M.lee_payload_reservado(A, _zip(tmp_path, 50))
    assert not [c for c in df.columns if c.startswith("P7_")] and list(df.columns) == M.columnas_usadas(A)
