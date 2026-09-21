#!/usr/bin/env python3
"""Guardas de 4.1 y llave logica -- ACTO GEN2-RELEVO-TANDA-3, P1/P2.

Que defecto real atrapa (§1, el aparato tiene costo): el canal de pines es la
unica via por la que una lectura puede salir de `dependencias_numericas_
legacy_activas` sin que su consumidor escriba nada. Sin estas guardas, un pin
mal escrito baja el contador citando un numero que NO viene de GEN2 -- y el
contador es lo que mesa usa para dirigir. El caso testigo no es hipotetico:
`CALC-TRIADA-0001` esta SELLADA, cuenta_gen2 = SI y REPRODUCE, y aun asi sus
`RESULT-TRIADA-*-M` son una FOTO de los valores M tomada de
`snapshot-M-triada-v1_0.json`. Pinear a ellos habria relevado las 14 lecturas
M de un golpe sin que nadie volviera a medir nada.

Los casos se construyen POR MUTACION de un pin valido: cada uno cambia UNA
cosa y debe disparar SU rechazo. Un caso que pase por la razon equivocada no
prueba la guarda.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools"))

import pines_mesa  # noqa: E402
from tools import corrida0  # noqa: E402

FIRMA = "forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-3.md · 21/sep/2026"

# ── contexto sintetico: el arbol minimo que las guardas consultan ─────────
CORRIDAS = {
    "CALC-BUENO": {"estado": "SELLADA", "cuenta_gen2": "SI",
                   "resultado_replay": "REPRODUCE",
                   "resultados_ids": {"RESULT-BUENO-PUNTO"}},
    "CALC-SIN-SELLAR": {"estado": "DECLARADA", "cuenta_gen2": "SI",
                        "resultado_replay": "REPRODUCE",
                        "resultados_ids": {"RESULT-SIN-SELLAR-PUNTO"}},
    "CALC-NO-GEN2": {"estado": "SELLADA", "cuenta_gen2": "NO",
                     "resultado_replay": "REPRODUCE",
                     "resultados_ids": {"RESULT-NO-GEN2-PUNTO"}},
    "CALC-NO-REPRODUCE": {"estado": "SELLADA", "cuenta_gen2": "SI",
                          "resultado_replay": "NO-REPRODUCE",
                          "resultados_ids": {"RESULT-NR-PUNTO"}},
    "CALC-SIN-CRUDO": {"estado": "SELLADA", "cuenta_gen2": "SI",
                       "resultado_replay": "REPRODUCE",
                       "resultados_ids": {"RESULT-SC-PUNTO"}},
    "CALC-INGIERE": {"estado": "SELLADA", "cuenta_gen2": "SI",
                     "resultado_replay": "REPRODUCE",
                     "resultados_ids": {"RESULT-ING-M"}},
    "CALC-CONDUCTA": {"estado": "SELLADA", "cuenta_gen2": "SI",
                      "resultado_replay": "REPRODUCE",
                      "resultados_ids": {"RESULT-COND-P", "RESULT-COND-OTRO"}},
}
CON_CRUDO = {"inputs": [{"id": "micro", "origen": "manifiesto"}]}
SPECS = {
    "CALC-BUENO": CON_CRUDO,
    "CALC-SIN-SELLAR": CON_CRUDO,
    "CALC-NO-GEN2": CON_CRUDO,
    "CALC-NO-REPRODUCE": CON_CRUDO,
    "CALC-SIN-CRUDO": {"inputs": [{"id": "s", "origen": "repo",
                                   "ruta": "forense/x-spec-v1_0.md"}]},
    "CALC-INGIERE": {"inputs": [
        {"id": "capturas", "origen": "repo",
         "ruta": "forense/prereg-duelo-v2/manifiesto-capturas-P3-v1_0.tsv"},
        {"id": "snap", "origen": "repo",
         "ruta": "forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json"}]},
    "CALC-CONDUCTA": CON_CRUDO,
}
CONDUCTAS = {"RESULT-COND-P": "milpa/tramite.yaml:una.regla:una_conducta"}

PIN_VALIDO = {"llave_logica": "marco-M::CIV-M-01::R",
              "result_gen2": "RESULT-BUENO-PUNTO", "calc_gen2": "CALC-BUENO",
              "via": pines_mesa.VIA_CRUDO, "firma": FIRMA, "nota": ""}


def _valida(**cambios):
    fila = dict(PIN_VALIDO, **cambios)
    return pines_mesa.valida_pin(fila, CORRIDAS, SPECS, CONDUCTAS)


def test_pin_valido_pasa():
    assert _valida() == (pines_mesa.ACEPTADO, "")


def test_via_conducta_valida_pasa():
    estado, motivo = _valida(via=pines_mesa.VIA_CONDUCTA,
                             calc_gen2="CALC-CONDUCTA",
                             result_gen2="RESULT-COND-P")
    assert estado == pines_mesa.ACEPTADO, motivo


# ── guarda (a) · sello, cuenta_gen2 y replay ──────────────────────────────

def test_rechaza_calc_no_sellada():
    estado, _ = _valida(calc_gen2="CALC-SIN-SELLAR",
                        result_gen2="RESULT-SIN-SELLAR-PUNTO")
    assert estado == "RECHAZADO-CALC-NO-SELLADA"


def test_rechaza_calc_que_no_cuenta_gen2():
    estado, _ = _valida(calc_gen2="CALC-NO-GEN2",
                        result_gen2="RESULT-NO-GEN2-PUNTO")
    assert estado == "RECHAZADO-CALC-NO-CUENTA-GEN2"


def test_rechaza_calc_que_no_reproduce():
    estado, _ = _valida(calc_gen2="CALC-NO-REPRODUCE",
                        result_gen2="RESULT-NR-PUNTO")
    assert estado == "RECHAZADO-CALC-NO-REPRODUCE"


def test_rechaza_result_de_otro_calc():
    estado, _ = _valida(result_gen2="RESULT-COND-P")
    assert estado == "RECHAZADO-RESULT-AJENO-AL-CALC"


# ── guarda (b) · via (i) exige insumo crudo ───────────────────────────────

def test_rechaza_via_crudo_sin_manifiesto():
    estado, _ = _valida(calc_gen2="CALC-SIN-CRUDO",
                        result_gen2="RESULT-SC-PUNTO")
    assert estado == "RECHAZADO-SIN-INSUMO-CRUDO"


# ── guarda (c) · via (ii) exige conducta GEN2 HOY ─────────────────────────

def test_rechaza_via_conducta_cuando_la_conducta_no_es_gen2():
    estado, _ = _valida(via=pines_mesa.VIA_CONDUCTA,
                        calc_gen2="CALC-CONDUCTA",
                        result_gen2="RESULT-COND-OTRO")
    assert estado == "RECHAZADO-CONDUCTA-NO-GEN2"


# ── guarda (d) · nada ingerido releva ─────────────────────────────────────

def test_rechaza_result_ingerido_de_snapshot():
    """`CALC-INGIERE` trae manifiesto de capturas -- pasaria (b) -- y aun asi
    se rechaza: el snapshot manda. Es la forma sintetica de TRIADA."""
    estado, motivo = _valida(calc_gen2="CALC-INGIERE",
                             result_gen2="RESULT-ING-M")
    assert estado == "RECHAZADO-RESULT-INGERIDO", motivo


# ── higiene del canal ─────────────────────────────────────────────────────

def test_rechaza_via_desconocida():
    assert _valida(via="iii-POR-PARECIDO")[0] == "RECHAZADO-VIA-DESCONOCIDA"


def test_rechaza_pin_sin_firma():
    assert _valida(firma="  ")[0] == "RECHAZADO-SIN-FIRMA"


# ── casos REALES del arbol, contra el registro derivado ───────────────────

def _contexto_real():
    v = corrida0._filas_registro(verifica=False)
    corridas = {f["spec_id"]: {
        "estado": f["estado"], "cuenta_gen2": f["cuenta_gen2"],
        "resultado_replay": f["resultado_replay"],
        "resultados_ids": set(str(f["resultados_ids"]).split(",")),
    } for f in v["corridas"] if f["origen"] == "OFERTA"}
    marcas = corrida0._ids_corrida0_declarados()
    conductas = {m["resultado_id"]: c for c, m in marcas.items()
                 if m.get("generacion") == "GEN2" and m.get("resultado_id")
                 and c.startswith("milpa/tramite.yaml:")}
    import yaml
    specs = {}
    for calc in ("CALC-TRIADA-0001", "CALC-R-CIV-M-01"):
        specs[calc] = yaml.safe_load(
            (RAIZ / "data" / "corrida0" / calc / "spec.yaml").read_text(
                encoding="utf-8"))
    return corridas, specs, conductas, v


def test_result_triada_m_real_se_rechaza():
    """El caso testigo del encargo, contra el arbol real y no un doble.

    `CALC-TRIADA-0001` esta SELLADA, cuenta_gen2 = SI y REPRODUCE: las tres
    condiciones de (a). Si alguien afloja (d), este pin pasa y catorce
    lecturas M salen de legacy sin que nadie las remida.
    """
    corridas, specs, conductas, _ = _contexto_real()
    fila = dict(PIN_VALIDO, llave_logica="marco-M::CIV-M-01::M",
                calc_gen2="CALC-TRIADA-0001",
                result_gen2="RESULT-TRIADA-CIV_M_01-M")
    estado, motivo = pines_mesa.valida_pin(fila, corridas, specs, conductas)
    assert estado == "RECHAZADO-RESULT-INGERIDO", motivo


def test_din_m_01_m_no_es_pineable_por_conducta():
    """`DIN-M-01:M` consulta `tiene_ahorros` (milpa/tramite.yaml), que sigue
    GEN1 (ENNViH) y NO lleva `corrida0_generacion`. La firma del 21/sep lo
    excluye a proposito; esta prueba es la que impide que un acto futuro lo
    incluya por simetria con las otras trece."""
    corridas, specs, conductas, _ = _contexto_real()
    # El valor M de DIN-M-01 es el `p` de `tiene_ahorros`; ningun RESULT GEN2
    # lo declara hoy. Se prueba con el RESULT de la conducta HOMONIMA de otra
    # ola, que si es GEN2: citarlo seria pinear a una conducta distinta.
    fila = dict(PIN_VALIDO, llave_logica="marco-M::DIN-M-01::M",
                via=pines_mesa.VIA_CONDUCTA,
                calc_gen2="CALC-TRIADA-0001", result_gen2="RESULT-TIENE-AHORROS-INEXISTENTE")
    estado, motivo = pines_mesa.valida_pin(fila, corridas, specs, conductas)
    assert estado.startswith("RECHAZADO-"), motivo
    # Y, en el arbol, la conducta que DIN-M-01:M consulta no es GEN2:
    assert "milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:tiene_ahorros" \
        not in {c for c in conductas.values()}


# ── llave logica: ida y vuelta sobre TODOS los consumidores de hoy ────────

def test_llave_logica_ida_y_vuelta_sobre_el_registro():
    """La llave no lleva ruta, ni version, ni `RES-####`, y aun asi vuelve al
    MISMO consumidor. Si dos consumidores colapsaran en una llave, un pin
    firmado para uno relevaria al otro en silencio."""
    _, _, _, v = _contexto_real()
    consumidores = sorted({u["consumidor"] for u in v["usos"]})
    indice = pines_mesa.indice_llaves(consumidores)
    traducidos = [c for c in consumidores
                  if _traducible(c)]
    assert len(indice) == len(traducidos), (
        "colision de llaves: "
        f"{len(traducidos)} consumidores -> {len(indice)} llaves")
    for c in traducidos:
        llave = pines_mesa.llave_logica(c)
        assert indice[llave] == c
        # Sin RUTA: la llave no puede empezar por un directorio del repo. Un
        # `/` mas adentro es parte del NOMBRE del campo del consumidor
        # (`condicionales_confianza_institucional/salud`), no una ruta.
        assert not any(llave.startswith(p) for p in
                       ("milpa/", "forense/", "data/", "tools/"))
        assert "RES-" not in llave
        assert not any(t in llave for t in ("v1_3", "v1_2", "v0_1"))


def _traducible(consumidor: str) -> bool:
    try:
        pines_mesa.llave_logica(consumidor)
    except pines_mesa.PinInvalido:
        return False
    return True


def test_consumidor_sin_espacio_no_se_traduce_a_ojo():
    try:
        pines_mesa.llave_logica("un/archivo/nuevo.yaml:algo")
    except pines_mesa.PinInvalido as e:
        assert "CONSUMIDOR-SIN-ESPACIO-LOGICO" in str(e)
    else:
        raise AssertionError("un archivo desconocido no debe producir llave")


def test_pines_del_arbol_pasan_todos_sus_guardas():
    """Los pines que este acto escribio, validados contra el arbol REAL.

    Un pin que se escribe y luego no pasa es peor que no escribirlo: el
    contador no se mueve y nadie se entera. El canal vacio tambien pasa --
    este test no exige que haya pines, exige que los que haya sean validos.
    """
    v = corrida0._filas_registro(verifica=False)
    corridas = {f["spec_id"]: {
        "estado": f["estado"], "cuenta_gen2": f["cuenta_gen2"],
        "resultado_replay": f["resultado_replay"],
        "resultados_ids": set(str(f["resultados_ids"]).split(",")),
    } for f in v["corridas"] if f["origen"] == "OFERTA"}
    marcas = corrida0._ids_corrida0_declarados()
    conductas = {m["resultado_id"]: c for c, m in marcas.items()
                 if m.get("generacion") == "GEN2" and m.get("resultado_id")
                 and c.startswith("milpa/tramite.yaml:")}
    import yaml
    specs = {}
    filas = pines_mesa.lee_pines()
    for f in filas:
        calc = f["calc_gen2"]
        ruta = RAIZ / "data" / "corrida0" / calc / "spec.yaml"
        specs[calc] = (yaml.safe_load(ruta.read_text(encoding="utf-8"))
                       if ruta.exists() else {})
    _, rechazos = pines_mesa.pines_validados(
        corridas, specs, conductas, pines_mesa.RUTA_PINES)
    assert not rechazos, "pines escritos y rechazados:\n  " + "\n  ".join(rechazos)
    # Y toda llave firmada tiene que corresponder a un consumidor real.
    indice = pines_mesa.indice_llaves({u["consumidor"] for u in v["usos"]})
    huerfanos = [f["llave_logica"] for f in filas
                 if f["llave_logica"] not in indice]
    assert not huerfanos, f"pines sin consumidor en el registro: {huerfanos}"


def corre() -> list[str]:
    """Arnes de la casa (mismo contrato que `tests/test_corrida0.py`):
    devuelve la lista de fallos, vacia si todo pasa."""
    fallos: list[str] = []
    for nombre, fn in sorted(globals().items()):
        if not nombre.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
        except AssertionError as exc:
            fallos.append(f"{nombre}: {exc}")
        except Exception as exc:  # noqa: BLE001
            fallos.append(f"{nombre}: {type(exc).__name__}: {exc}")
    return fallos


if __name__ == "__main__":
    _fallos = corre()
    for _f in _fallos:
        print("FAIL", _f)
    print(f"{'FALLOS: ' + str(len(_fallos)) if _fallos else 'OK'}")
    sys.exit(1 if _fallos else 0)
