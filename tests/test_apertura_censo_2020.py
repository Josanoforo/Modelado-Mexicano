"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de la muestra censal para el expediente de
apertura del Censo 2020 (contendientes EIC 2015 y CCPV 2010).

Esquemas: los de los medidores sellados (`COLS_CRUDAS` de EIC: TIPOHOG, JEFE_SEXO, TAMLOC, ENT, FACTOR, ESTRATO,
UPM; `COLS_VIV`/`COLS_PER` de CCPV: ent, id_viv, tipohog, numpers, factor, estrato, upm, tam_loc; sexo, edad,
parent, nivacad). Se fabrican dos ZIP estatales `Censo2020_CA_<ent>_csv.zip` con `Viviendas<ee>.CSV`,
`Personas<ee>.CSV` y `Migrantes<ee>.CSV` y se corre la lectura real. Ramas: con soporte (columnas con el
nombre de la ola del piso); nombres 2020 (PARENTESCO en lugar de parent, sin tam_loc: esas conductas y
ejes salen sin soporte, R None); categoría vacía; estructura ausente → PARO. Toda salida pasa
`corrida0._valida_outputs`, sin no finitos, dictamen del vocabulario; auditoría AST limpia y mutaciones.
"""
from __future__ import annotations

import importlib.util
import io
import math
import os
import sys
import zipfile

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402

REL = "forense/prereg-aperturas/CENSO-2020/medidor_apertura_censo_2020.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AP = _load(REL, "ap_censo_2020_t")


def _ok(out):
    assert corrida0._valida_outputs({"resultados": AP.esquema_resultados()}, out) == []
    assert out[f"{AP.P}-DICTAMEN"] in AP.G.VOCABULARIO
    assert out[f"{AP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _entidad(rng, ent, nv, nombres_piso=True, jefe_sexo=None, quitar_viv=()):
    npers = rng.integers(1, 7, nv)
    viv = pd.DataFrame({"ENT": ent, "ID_VIV": [f"{ent:02d}{i:07d}" for i in range(nv)],
                        "TIPOHOG": rng.choice([1, 2, 3, 5, 6, 9], nv), "NUMPERS": npers,
                        "FACTOR": rng.integers(5, 40, nv), "ESTRATO": rng.integers(1, 30, nv),
                        "UPM": rng.integers(1, 300, nv), "TAMLOC": rng.integers(1, 6, nv),
                        "JEFE_SEXO": (np.full(nv, jefe_sexo) if jefe_sexo else rng.choice([1, 3], nv))})
    filas = []
    for i, k in enumerate(npers):
        for j in range(k):
            filas.append({"ENT": ent, "ID_VIV": viv["ID_VIV"][i], "SEXO": int(rng.choice([1, 3])),
                          "EDAD": int(rng.integers(0, 95)), "PAR": 1 if j == 0 else int(rng.integers(2, 10)),
                          "NIVACAD": int(rng.integers(0, 13)), "FACTOR": int(viv["FACTOR"][i]),
                          "ESTRATO": int(viv["ESTRATO"][i]), "UPM": int(viv["UPM"][i]), "TAMLOC": int(viv["TAMLOC"][i])})
    per = pd.DataFrame(filas)
    if nombres_piso:
        viv["TAM_LOC"] = rng.integers(1, 5, nv)
        per = per.rename(columns={"PAR": "PARENT"})
        per["TAM_LOC"] = 1
    else:
        per = per.rename(columns={"PAR": "PARENTESCO"})
    return viv.drop(columns=list(quitar_viv)), per


def _zip(tmp_path, ent, viv, per):
    abrev = AP.ABREV[ent - 1]
    ruta = tmp_path / f"Censo2020_CA_{abrev}_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        for nombre, df in ((f"Viviendas{ent:02d}.CSV", viv), (f"Personas{ent:02d}.CSV", per)):
            buf = io.StringIO()
            df.to_csv(buf, index=False)
            z.writestr(nombre, buf.getvalue())
        z.writestr(f"Migrantes{ent:02d}.CSV", "ENT,ID_VIV\n")
    return str(ruta)


def _corre(tmp_path, **kw):
    SE, SC, R, M, pe, pc = AP.sellados()
    rng = np.random.default_rng(2020)
    rutas = {f"{e:02d}": _zip(tmp_path, e, *_entidad(rng, e, 800, **kw)) for e in (1, 9)}
    viv, per = AP.lee_payload_reservado(SE, SC, R, rutas)
    return AP.E.salida(AP.P, AP.filas(SE, SC, M, AP.mide_r_eic(SE, M, viv), AP.mide_r_ccpv(SC, R, viv, per), pe, pc))


def test_censo_con_soporte(tmp_path):
    out = _corre(tmp_path)
    _ok(out)
    assert out[f"{AP.P}-N"] > 0
    assert out[f"{AP.P}-EIC15-HOGAR-NUCLEAR-TOTAL-TODOS-R"] is not None
    assert out[f"{AP.P}-CCPV10-HOG-JEFA-MUJER-TOTAL-TODOS-R"] is not None
    assert out[f"{AP.P}-CCPV10-HOG-TAMANO-MEDIO-TOTAL-TODOS-R"] > 1.0          # media, no proporción
    assert out[f"{AP.P}-CCPV10-PER60-VIVE-SOLO-SEXO-MUJER-R"] is not None


def test_censo_nombres_2020_sin_soporte_y_categoria_vacia(tmp_path):
    out = _corre(tmp_path, nombres_piso=False, jefe_sexo=1)
    _ok(out)
    assert out[f"{AP.P}-CCPV10-HOG-JEFA-MUJER-TOTAL-TODOS-R"] is None        # parent ausente
    assert out[f"{AP.P}-CCPV10-HOG-TRES-GENERACIONES-TOTAL-TODOS-R"] is None
    assert out[f"{AP.P}-CCPV10-HOG-NUCLEAR-TLOC-MENOS-2500-R"] is None       # tam_loc ausente
    assert out[f"{AP.P}-CCPV10-HOG-NUCLEAR-TOTAL-TODOS-R"] is not None
    assert out[f"{AP.P}-EIC15-HOGAR-NUCLEAR-JEFATURA-MUJER-R"] is None        # categoría vacía
    assert out[f"{AP.P}-EIC15-HOGAR-NUCLEAR-ENTIDAD-05-R"] is None


def test_censo_estructura_ausente_es_paro(tmp_path):
    SE, SC, R, _M, _pe, _pc = AP.sellados()
    rng = np.random.default_rng(1)
    ruta = _zip(tmp_path, 1, *_entidad(rng, 1, 20, quitar_viv=("FACTOR",)))
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(SE, SC, R, {"01": ruta})


def test_censo_entidad_mal_resuelta_es_paro(tmp_path):
    SE, SC, R, _M, _pe, _pc = AP.sellados()
    ruta = _zip(tmp_path, 1, *_entidad(np.random.default_rng(2), 1, 20))
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(SE, SC, R, {"09": ruta})


def test_censo_auditoria_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert AP.G.auditoria_ast(src) == []
    for mut in AP.E.MUTACIONES:
        assert AP.G.auditoria_ast(src + "\n\n" + mut), mut


def test_censo_vistas_son_celdas_y_no_puntuan():
    SE, SC, _R, M, pe, pc = AP.sellados()
    fl = AP.filas(SE, SC, M, {}, {}, pe, pc)
    ids = {f["id"] for f in fl}
    assert AP.VISTAS <= ids
    assert all(f["lo"] is None and f["hi"] is None for f in fl if f["id"] in AP.VISTAS)
    assert sum(f["lo"] is not None for f in fl) > 0
