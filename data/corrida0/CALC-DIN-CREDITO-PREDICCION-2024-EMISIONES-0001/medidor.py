from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Emisiones de predicción 2024 (marginales, P1) de las conductas de crédito
que el encargo declara entrando (K1, K2-DEPARTAMENTAL, K2-NOMINA,
K2-AUTOMOTRIZ, K3, K4A-AUTOEXCLUSION, K4B-OFERTA, K5, K6-P-TENEDORES), por
las 18 celdas de eje ya selladas en los cuatro pisos de crédito
(2012/2015/2018/2021-recorte1870). NO abre ningún microdato: aritmética
entre RESULT- ya sellados, en escala logit. NUNCA lee `enif2024_csv` ni
ninguna variable de la sección de crédito de ENIF 2024 (PARO a del
encargo) -- las predicciones de este CALC son sobre lo que el programa
predice, no sobre lo que ENIF 2024 midió.

Cuatro contendientes por (conducta, celda), IMPORTADOS por bytes (sha256)
de `tools/encig_origen_movil.py` (`#972`) -- mismo procedimiento
determinista, sin copiar su lógica, sólo sus primitivas de bajo nivel
(`_logit`, `_expit`, `_ee_logit`, `pesos`, `predice`, `PISOS`,
`MINIMO_OLAS`): PERSISTENCIA (mín. 1 ola), TENDENCIA-2 (mín. 2),
TENDENCIA-3 (mín. 3), TENDENCIA-SERIE (mín. 2, todas las disponibles).
T2/T3/T-serie sólo entran si la (conducta, celda) tiene >= 3 puntos
utilizables tras filtrar celdas raras (spec.md §2) -- la comparabilidad
mínima que el encargo pide para no ajustar una recta degenerada de 2
puntos.

Para P3 (ensayo y oro) el mismo procedimiento se corre en modo
"backtest": predice cada ola histórica (2015, 2018, 2021) SOLO con sus
propias olas anteriores y compara contra el valor real ya sellado de esa
ola -- exactamente como si esa ola fuera la nueva, reproduciendo el
patrón de auto-validación de `tools/encig_origen_movil.py::origen_movil`
sin reusar su código (prefijo RESULT- distinto, imposible de monkeypatch
porque el suyo está en un f-string, no en un nombre de módulo
asignable) -- ver spec.md §4.

Spec: DIN-CREDITO-PREDICCION-2024-EMISIONES-spec-v1_0.md.
"""
import json
import types
from pathlib import Path

PREFIJO = "DIN-CREDITO-PREDICCION-2024"

ENTERING = ["K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ", "K3",
            "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES"]
CELLS = ["NACIONAL-TODOS", "SEXO-1", "SEXO-2",
         "EDAD-18-29", "EDAD-30-44", "EDAD-45-59", "EDAD-60-MAS",
         "ESCOLARIDAD-HASTA-PRIMARIA", "ESCOLARIDAD-SECUNDARIA",
         "ESCOLARIDAD-MEDIA-SUPERIOR", "ESCOLARIDAD-SUPERIOR",
         "LOCALIDAD-15-000-Y-MAS", "LOCALIDAD-MENOR-DE-15-000",
         "CUENTA-CON-CUENTA", "CUENTA-SIN-CUENTA",
         "FORMALIDAD-CON-SEGURIDAD-SOCIAL", "FORMALIDAD-SIN-SEGURIDAD-SOCIAL",
         "UNIVERSO-UNIVERSO-TRABAJA"]
WAVES = ("2012", "2015", "2018", "2021")
TARGETS = (2015.0, 2018.0, 2021.0, 2024.0)
WAVE_PREFIJO = {
    "2012": "DIN-CREDITO-PISOS-ENIF2012",
    "2015": "DIN-CREDITO-PISOS-ENIF2015",
    "2018": "DIN-CREDITO-PISOS-ENIF2018",
    "2021": "DIN-CREDITO-PISOS-ENIF2021-RECORTE1870",
}
WAVE_INPUT_ID = {"2012": "PISO-2012", "2015": "PISO-2015", "2018": "PISO-2018", "2021": "PISO-2021"}


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_om(inputs):
    src = _bytes(inputs["MEDIDOR-TENDENCIA-ORIGEN-MOVIL"])
    mod = types.ModuleType("encig_origen_movil_importado")
    exec(compile(src, "encig_origen_movil_importado", "exec"), mod.__dict__)
    return mod


def _resultados_ola(inputs, ola):
    d = json.loads(_bytes(inputs[WAVE_INPUT_ID[ola]]).decode("utf-8"))
    return d.get("resultados", d)


def _punto(wave_r, ola, cid, cell):
    """(anio, p, lo, hi) o None + motivo. Celda rara (lo<=0 o hi>=1, logit
    indefinido) se excluye y se declara -- no se inventa un valor."""
    pref = WAVE_PREFIJO[ola]
    b = f"RESULT-{pref}-{cid}-{cell}"
    p, lo, hi = wave_r[ola].get(b + "-P"), wave_r[ola].get(b + "-IC-LO"), wave_r[ola].get(b + "-IC-HI")
    if p is None or lo is None or hi is None:
        return None, "SIN-CELDA"
    if lo <= 0.0 or hi >= 1.0:
        return None, "CELDA-RARA-LOGIT-INDEFINIDO"
    return (float(ola), p, lo, hi), "OK"


def _serie(wave_r, cid, cell):
    """Serie completa 2012-2021 y el registro de exclusiones por celda rara."""
    puntos = []
    raras = []
    for ola in WAVES:
        pt, motivo = _punto(wave_r, ola, cid, cell)
        if pt is not None:
            puntos.append(pt)
        elif motivo == "CELDA-RARA-LOGIT-INDEFINIDO":
            raras.append(ola)
    return puntos, raras


def medir(inputs, contrato):
    om = _modulo_om(inputs)
    wave_r = {ola: _resultados_ola(inputs, ola) for ola in WAVES}
    out = {}
    mae_por_cid_piso = {cid: {p: [] for p in om.PISOS} for cid in ENTERING}
    cobre_por_cid_piso = {cid: {p: [] for p in om.PISOS} for cid in ENTERING}

    for cid in ENTERING:
        for cell in CELLS:
            serie, raras = _serie(wave_r, cid, cell)
            base_diag = f"RESULT-{PREFIJO}-{cid}-{cell}"
            out[f"{base_diag}-CELDAS-RARAS-EXCLUIDAS"] = ",".join(raras) if raras else "NINGUNA"
            out[f"{base_diag}-N-CELDAS-RARAS-EXCLUIDAS"] = len(raras)

            for target in TARGETS:
                prev = [s for s in serie if s[0] < target]
                actual = [s for s in serie if s[0] == target]
                base_t = f"{base_diag}-{int(target)}"
                out[f"{base_t}-N-OLAS-PREVIAS"] = len(prev)
                out[f"{base_t}-OLAS-PREVIAS"] = ",".join(str(int(a)) for a, *_ in prev) if prev else "NINGUNA"
                if not prev:
                    continue
                anios = [s[0] for s in prev]
                logits = [om._logit(s[1]) for s in prev]
                ees = [om._ee_logit(s[2], s[3]) for s in prev]
                # Umbral propio de esta spec (spec.md §2): T2/T3/T-serie
                # sólo con >= 3 puntos previos, aunque om.pesos() por sí
                # solo aceptaría T2/T-serie con 2 (ajuste degenerado).
                pisos_habilitados = (om.PISOS if len(prev) >= 3 else ("PERSISTENCIA",))
                for piso in om.PISOS:
                    base_p = f"{base_t}-{piso}"
                    pr = (om.predice(piso, anios, logits, ees, target, (prev[-1][2], prev[-1][3]))
                          if piso in pisos_habilitados else None)
                    out[f"{base_p}-P"] = pr["p"] if pr else None
                    out[f"{base_p}-IC-LO"] = pr["lo"] if pr else None
                    out[f"{base_p}-IC-HI"] = pr["hi"] if pr else None
                    if actual:
                        # -ERROR-PP/-CUBRE existen siempre que hay un valor
                        # real que comparar (backtest), con o sin predicción
                        # -- None declarado, no ausente (D-22 punto 3).
                        if pr is not None:
                            R = actual[0][1]
                            err = 100.0 * (pr["p"] - R)
                            cubre = pr["lo"] <= R <= pr["hi"]
                            out[f"{base_p}-ERROR-PP"] = err
                            out[f"{base_p}-CUBRE"] = "SI" if cubre else "NO"
                            mae_por_cid_piso[cid][piso].append(abs(err))
                            cobre_por_cid_piso[cid][piso].append(cubre)
                        else:
                            out[f"{base_p}-ERROR-PP"] = None
                            out[f"{base_p}-CUBRE"] = None

    # Backtest agregado por conducta (P3: ensayo y oro; spec.md §4).
    for cid in ENTERING:
        mejor = None
        for piso in om.PISOS:
            errs = mae_por_cid_piso[cid][piso]
            cobs = cobre_por_cid_piso[cid][piso]
            b = f"RESULT-{PREFIJO}-{cid}-{piso}"
            mae = sum(errs) / len(errs) if errs else None
            out[f"{b}-MAE-BACKTEST-PP"] = mae
            out[f"{b}-N-BACKTEST"] = len(errs)
            out[f"{b}-COBERTURA-BACKTEST"] = (sum(cobs) / len(cobs)) if cobs else None
            if mae is not None and (mejor is None or mae < mejor[1]):
                mejor = (piso, mae)
        out[f"RESULT-{PREFIJO}-{cid}-MEJOR-CONTENDIENTE-BACKTEST"] = mejor[0] if mejor else "SIN-BACKTEST"
        serie_nacional, _ = _serie(wave_r, cid, "NACIONAL-TODOS")
        out[f"RESULT-{PREFIJO}-{cid}-N-OLAS-COMPARABLES-NACIONAL"] = len(serie_nacional)

    return out
