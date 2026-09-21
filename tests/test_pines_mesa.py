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


# ── P1 (TANDA-4) · guarda (a) por EJE, un caso por token del vocabulario ──
#
# Que defecto atrapa: `CALC-B-0001` esta SELLADA, cuenta_gen2 = SI y su
# replay dice `REPLICA-RESULTADO · CONTEXTO-DISTINTO` -- el numero volvio a
# salir igual y lo unico que cambio fue `tools/baseline_temporal.py` en
# 67aa13d, ajeno a la lectura. Con la guarda vieja (prefijo `REPRODUCE`) las
# tres lecturas M de ENIGH quedaban en legacy por un cambio de contexto. Con
# la guarda floja al reves, un `NO-REPRODUCE · CONTEXTO-DISTINTO` entraria
# por parecerse. Los dos errores cuestan lo mismo al lector: el contador
# miente en una direccion o en la otra.

# El universo se DERIVA del vocabulario real, no se teclea: si manana
# `corrida0` acuna un veredicto nuevo, este test falla hasta que alguien
# decida de que lado del eje cae.
VOCABULARIO_REPLAY = pines_mesa.vocabulario_replay() | {"NO-EJECUTABLE"}


def _corridas_con_replay(valor: str) -> dict:
    return {"CALC-REPLAY": {"estado": "SELLADA", "cuenta_gen2": "SI",
                            "resultado_replay": valor,
                            "resultados_ids": {"RESULT-REPLAY-P"}}}


def test_vocabulario_afirmativo_se_deriva_y_no_se_teclea():
    afirmativos = pines_mesa.veredictos_afirmativos_en_resultado()
    assert afirmativos == {"REPRODUCE",
                           "REPLICA-RESULTADO · CONTEXTO-DISTINTO"}, afirmativos
    # `NO-EJECUTABLE` no esta en el vocabulario CONCLUYENTE de corrida0 (E.3:
    # es limitacion de la sesion, no hallazgo sobre el numero) y por tanto
    # tampoco puede colarse como afirmativo.
    assert "NO-EJECUTABLE" not in pines_mesa.vocabulario_replay()
    assert "NO-EJECUTABLE" not in afirmativos


def test_cada_token_del_vocabulario_real_por_las_dos_vias():
    """Un caso por token de `forense/replay-evidencia.tsv`, por via (i) y por
    via (ii): la (i) solo acepta `REPRODUCE`; la (ii) acepta el eje."""
    afirmativos = pines_mesa.veredictos_afirmativos_en_resultado()
    conductas = {"RESULT-REPLAY-P": "milpa/tramite.yaml:r:c"}
    for token in sorted(VOCABULARIO_REPLAY):
        corridas = _corridas_con_replay(token)
        fila_i = dict(PIN_VALIDO, calc_gen2="CALC-REPLAY",
                      result_gen2="RESULT-REPLAY-P", via=pines_mesa.VIA_CRUDO)
        estado_i, motivo_i = pines_mesa.valida_pin(
            fila_i, corridas, {"CALC-REPLAY": CON_CRUDO}, conductas)
        esperado_i = (pines_mesa.ACEPTADO if token == "REPRODUCE"
                      else "RECHAZADO-CALC-NO-REPRODUCE")
        assert estado_i == esperado_i, f"via (i) · {token}: {estado_i} {motivo_i}"

        fila_ii = dict(fila_i, via=pines_mesa.VIA_CONDUCTA)
        estado_ii, motivo_ii = pines_mesa.valida_pin(
            fila_ii, corridas, {"CALC-REPLAY": CON_CRUDO}, conductas)
        esperado_ii = (pines_mesa.ACEPTADO if token in afirmativos
                       else "RECHAZADO-CALC-NO-REPRODUCE")
        assert estado_ii == esperado_ii, \
            f"via (ii) · {token}: {estado_ii} {motivo_ii}"
        if estado_ii != pines_mesa.ACEPTADO:
            assert token in motivo_ii, "el rechazo debe decir POR QUE"


# ── P3 (TANDA-4) · clase (iii) `iii-DERIVADO-DE-GEN2` ─────────────────────
#
# Que defecto atrapa: sin la clase, un derivado determinista de un RESULT
# GEN2 -- RES-0028, q = 1 - p -- queda en legacy para siempre, porque la
# guarda (d) rechaza toda ingestion sin mirar la generacion de lo ingerido.
# Y sin las cuatro condiciones, la misma puerta deja pasar un derivado de un
# derivado o uno que mezcla un numero de GEN1, que es exactamente lo que 4.1
# prohibe. La clase es estrecha a proposito.

_PADRE_CRUDO = {"estado": "SELLADA", "cuenta_gen2": "SI",
                "resultado_replay": "REPRODUCE",
                "resultados_ids": {"RESULT-PADRE-P"}}
_DERIVADO = {"estado": "SELLADA", "cuenta_gen2": "SI",
             "resultado_replay": "REPRODUCE",
             "resultados_ids": {"RESULT-DERIVADO-Q"}}
CORRIDAS_III = {
    "CALC-PADRE": dict(_PADRE_CRUDO),
    "CALC-PADRE-NO-CUENTA": dict(_PADRE_CRUDO, cuenta_gen2="PENDIENTE-DE-MESA"),
    "CALC-PADRE-DERIVADO": dict(_PADRE_CRUDO),
    "CALC-HIJO": dict(_DERIVADO),
    "CALC-NIETO": dict(_DERIVADO),
    "CALC-HIJO-DE-NO-CUENTA": dict(_DERIVADO),
    "CALC-HIJO-MESTIZO": dict(_DERIVADO),
}


def _ingiriendo(*rutas):
    return {"inputs": [{"id": f"IN-{i}", "origen": "repo", "ruta": r}
                       for i, r in enumerate(rutas)]}


SPECS_III = {
    "CALC-PADRE": CON_CRUDO,
    "CALC-PADRE-NO-CUENTA": CON_CRUDO,
    "CALC-PADRE-DERIVADO": _ingiriendo(
        "data/corrida0/CALC-PADRE/resultados.json"),
    "CALC-HIJO": _ingiriendo("data/corrida0/CALC-PADRE/resultados.json",
                             "data/corrida0/CALC-PADRE/spec.yaml",
                             "data/corrida0/CALC-PADRE/sello.json"),
    "CALC-NIETO": _ingiriendo(
        "data/corrida0/CALC-PADRE-DERIVADO/resultados.json"),
    "CALC-HIJO-DE-NO-CUENTA": _ingiriendo(
        "data/corrida0/CALC-PADRE-NO-CUENTA/resultados.json"),
    "CALC-HIJO-MESTIZO": _ingiriendo(
        "data/corrida0/CALC-PADRE/resultados.json",
        "forense/prereg-duelo-v2/L-extraido-v1_2.tsv"),
}


def _valida_iii(calc, result):
    fila = dict(PIN_VALIDO, llave_logica="tramite::una.regla::una_conducta",
                via=pines_mesa.VIA_DERIVADO, calc_gen2=calc,
                result_gen2=result)
    return pines_mesa.valida_pin(fila, CORRIDAS_III, SPECS_III, {})


def test_iii_acepta_derivado_de_padre_gen2():
    estado, motivo = _valida_iii("CALC-HIJO", "RESULT-DERIVADO-Q")
    assert estado == pines_mesa.ACEPTADO, motivo


def test_iii_rechaza_derivado_cuyo_padre_no_cuenta():
    estado, motivo = _valida_iii("CALC-HIJO-DE-NO-CUENTA", "RESULT-DERIVADO-Q")
    assert estado == "RECHAZADO-DERIVADO-PADRE-NO-CUENTA-GEN2", motivo


def test_iii_rechaza_derivado_de_derivado():
    estado, motivo = _valida_iii("CALC-NIETO", "RESULT-DERIVADO-Q")
    assert estado == "RECHAZADO-DERIVADO-DE-DERIVADO", motivo


def test_iii_rechaza_derivado_que_ademas_ingiere_gen1():
    """La condicion que NO se puede relajar (PARO (b) del encargo): un
    derivado que mezcla un numero de GEN1 no entra, tenga hash o no."""
    estado, motivo = _valida_iii("CALC-HIJO-MESTIZO", "RESULT-DERIVADO-Q")
    assert estado == "RECHAZADO-DERIVADO-INGIERE-AJENO", motivo
    assert "L-extraido-v1_2.tsv" in motivo


def test_iii_no_afloja_la_guarda_d_para_las_otras_vias():
    """La clase (iii) es una puerta NUEVA, no un boquete en la vieja: el
    mismo CALC-HIJO por via (i) o (ii) sigue rechazado por ingestion."""
    for via in (pines_mesa.VIA_CRUDO, pines_mesa.VIA_CONDUCTA):
        fila = dict(PIN_VALIDO, llave_logica="tramite::una.regla::una_conducta",
                    via=via, calc_gen2="CALC-HIJO",
                    result_gen2="RESULT-DERIVADO-Q")
        estado, motivo = pines_mesa.valida_pin(fila, CORRIDAS_III, SPECS_III, {})
        assert estado.startswith("RECHAZADO-"), f"{via}: {estado} {motivo}"


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


def test_los_210_consumidores_de_hoy_se_traducen_sin_excepcion():
    """Con el espacio `cortes-C1` declarado (D-r3, firma de mesa 21/sep/2026)
    NO queda ningun consumidor sin llave. Antes quedaban seis --
    `milpa/src/celdas.py:CORTES_C1:*` --, y eran justo los unicos que habrian
    seguido con numero posicional cuando `RES` se congelo como alias de la
    llave (ACTO GEN2-TUBERIA-RES-LLAVE-1).
    """
    _, _, _, v = _contexto_real()
    consumidores = sorted({u["consumidor"] for u in v["usos"]})
    sin_llave = [c for c in consumidores if not _traducible(c)]
    assert sin_llave == [], (
        f"{len(sin_llave)} consumidores sin espacio logico: {sin_llave[:5]}")
    indice = pines_mesa.indice_llaves(consumidores)
    assert len(indice) == len(consumidores)


def test_espacio_cortes_c1_no_repite_el_nombre_de_la_tabla():
    """Mesa firmo `cortes-C1::<corte>`, no `cortes-C1::CORTES_C1::<corte>`."""
    assert pines_mesa.llave_logica(
        "milpa/src/celdas.py:CORTES_C1:formalidad") == "cortes-C1::formalidad"
    # La absorcion es solo del token declarado y solo al principio: un campo
    # que se llame igual mas adentro NO se borra.
    assert pines_mesa.llave_logica(
        "milpa/src/celdas.py:CORTES_C1:CORTES_C1") == "cortes-C1::CORTES_C1"
    # Y no se absorbe en otro espacio.
    assert pines_mesa.llave_logica(
        "milpa/tramite.yaml:CORTES_C1:x") == "tramite::CORTES_C1::x"


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

    def _carga(calc: str) -> dict:
        ruta = RAIZ / "data" / "corrida0" / calc / "spec.yaml"
        specs[calc] = (yaml.safe_load(ruta.read_text(encoding="utf-8"))
                       if ruta.exists() else {})
        return specs[calc]

    filas = pines_mesa.lee_pines()
    for f in filas:
        spec = _carga(f["calc_gen2"])
        # La clase (iii) consulta ademas la spec del PADRE (para saber si el
        # padre ingiere a su vez). Se carga por derivacion de los inputs, no
        # por una lista a mano.
        for padre in pines_mesa._calcs_ingeridos(spec)[0]:
            _carga(padre)
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
