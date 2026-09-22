#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `tools/marcador_segmento.py` -- ACTO GEN2-MARCADOR-REDISENO-1.

Corre standalone (`python3 tests/test_marcador_segmento.py`) y expone
`corre() -> list[str]` (lista de fallos, vacía si pasa) para que un futuro
`tests/check.py` pueda cablearlo sin reimplementar nada -- mismo patrón que
`tests/test_corrida0.py`.

Tres guardias del diseño (§9(4)) + un caso de prueba que dispara cada una:
  T-RESERVA             ninguna fila RESERVADA trae R
  T-EMISOR-NO-COMPARA    ninguna fila IDENTICO se usa como si comparara
                         M contra R (columna `M` vacía en las 89 NACIONAL
                         IDENTICO -- el emisor es diagnóstico, no insumo)
  T-PISO-NO-CIRCULAR     ninguna fila MARGINAL trae piso
                         MARGINAL-SIN-INTERACCION (ese piso es SOLO de
                         cruce piloteado, nunca de una celda marginal)

ACTO GEN2-MARCADOR-PISOS-ENLACE-1 (19/sep/2026) añade la guardia D-14
`T-ENLACE-BIYECTIVO` (más T-PISO-NO-ES-M, T-UNIDAD-ARBITRO y
T-VETO-POR-NOMBRE) y retira `t_piso_v2_fixture_sintetico`: ese caso probaba
el lector por patrón de id (`_id_piso_v2`/`_lee_piso_v2`), que este acto
borró por no funcionar -- el enlace ahora va por la tabla de identidad.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "marcador_segmento_bajo_prueba", RAIZ / "tools" / "marcador_segmento.py")
M = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = M
_spec.loader.exec_module(M)

FALLOS: list[str] = []


def _falla(caso, msg):
    FALLOS.append(f"{caso}: {msg}")


def t_reserva_sin_r():
    v = M.deriva()
    for f in v["filas"]:
        if f["estado"] == "RESERVADA" and (f.get("R") not in ("", None)):
            _falla("T-RESERVA", f"{f['celda_id']} es RESERVADA y trae R={f['R']!r}")


def t_emisor_no_compara():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "NACIONAL" and f["emisor_vs_arbitro"] == "EMISOR=ARBITRO":
            # El emisor IDENTICO es diagnostico: no se usa como M que compite
            # contra R en una celda de cruce -- solo aparece en filas NACIONAL,
            # nunca en una fila CRUCE con piso.
            if f["tipo"] == "CRUCE":
                _falla("T-EMISOR-NO-COMPARA",
                       f"{f['celda_id']} es EMISOR=ARBITRO dentro de una fila CRUCE")


def t_piso_no_circular():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "MARGINAL" and f["piso_tipo"] == "MARGINAL-SIN-INTERACCION":
            _falla("T-PISO-NO-CIRCULAR",
                   f"{f['celda_id']} es MARGINAL con piso MARGINAL-SIN-INTERACCION "
                   f"(ese piso es solo de cruce piloteado)")


def t_veinte_adoptadas():
    # 20 (DIN 8 + TRA 12, ADR-538/ADR-542) + 16 (GOB.gobierno_digital.encig2025.
    # edad_x_escolaridad, piloto 3, A-bis 6, FIRMA DE MESA F3 21/sep/2026,
    # ACTO GEN2-TRAMITE-FIRMAS-5) = 36.
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "CRUCE"
            and f["resultado_id"] and f["estado"] in
            ("ADOPTADO-POR-FIRMA", "PISO-ADMISIBLE-NO-ADOPTADO"))
    if n != 36:
        _falla("T-VEINTE-ADOPTADAS", f"se esperaban 36 celdas C2 piloteadas, salieron {n}")


def t_universo_97_nacional():
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "NACIONAL")
    if n != 97:
        _falla("T-UNIVERSO-97", f"censo ADR-536 debía dar 97 filas NACIONAL, dio {n}")


def t_enlace_biyectivo():
    """GUARDIA D-14 de `ACTO GEN2-MARCADOR-PISOS-ENLACE-1` -- atrapa el
    defecto que ese acto corrige.

    Toda fila `CONSTRUIBLE` de la tabla de identidad de la rejilla
    (`forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`) debe
    enlazar con EXACTAMENTE UNA fila `MARGINAL` del marcador. Ni cero
    (el defecto de hoy: el lector por patrón de id no encontraba ninguna de
    las 53) ni más de una (el defecto gemelo: perder el `outcome` colapsaba
    dos desenlaces de ENIF en un solo `celda_id`).

    No se prueba "cuántas enlazan" contra una cifra escrita a mano: se
    prueba la BIYECCIÓN contra la tabla, que es la que manda."""
    v = M.deriva()
    marginales = [f for f in v["filas"] if f["tipo"] == "MARGINAL"]

    # 1 · ningún celda_id duplicado entre las marginales
    vistos = {}
    for f in marginales:
        vistos.setdefault(f["celda_id"], 0)
        vistos[f["celda_id"]] += 1
    for cid, n in vistos.items():
        if n > 1:
            _falla("T-ENLACE-BIYECTIVO", f"celda_id duplicado ({n} filas): {cid}")

    # 2 · cada CONSTRUIBLE de la tabla aparece en exactamente una marginal,
    #     identificada por su `resultado_id` (el `cell_id` de la tabla).
    construibles = [f for f in M.lee_tabla_identidad() if f["status"] == "CONSTRUIBLE"]
    if not construibles:
        _falla("T-ENLACE-BIYECTIVO",
               "la tabla de identidad no trae filas CONSTRUIBLE -- "
               "¿se movió o se vació el archivo?")
        return
    por_result = {}
    for f in marginales:
        if f["resultado_id"]:
            por_result.setdefault(f["resultado_id"], []).append(f["celda_id"])
    for f in construibles:
        enlazadas = por_result.get(f["cell_id"], [])
        if len(enlazadas) == 0:
            _falla("T-ENLACE-BIYECTIVO",
                   f"{f['cell_id']} es CONSTRUIBLE y no enlaza con ninguna "
                   f"fila MARGINAL (consumer={f['consumer']}, axis={f['axis']}, "
                   f"category={f['category']}, outcome={f['outcome']})")
        elif len(enlazadas) > 1:
            _falla("T-ENLACE-BIYECTIVO",
                   f"{f['cell_id']} enlaza con {len(enlazadas)} filas MARGINAL: "
                   f"{enlazadas}")

    # 3 · las NO-CONSTRUIBLE VIGENTES quedan SIN-PISO con la causa DE LA
    #     TABLA. `ACTO GEN2-MARCADOR-ENLACE-2` (20/sep/2026) acota la
    #     guardia a las VIGENTES: una fila sellada que una tabla más
    #     reciente SUCEDE ya no gobierna su celda, y exigir que su causa
    #     siga apareciendo obligaría al marcador a transportar una causa
    #     refutada. La fila sucedida no se edita ni se borra (A.10): sigue
    #     en su tabla, y `sucesiones_identidad()` la nombra.
    sucedidas = set(M.sucesiones_identidad())
    no_con = [f for f in M.lee_tabla_identidad()
              if f["status"] != "CONSTRUIBLE" and f["cell_id"] not in sucedidas]
    # el prefijo de `piso_fuente` es el status LITERAL de la tabla
    # (F-ENUT/F7, GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1, 22/sep/2026: antes
    # siempre "NO-CONSTRUIBLE:", ahora también "SIN-PISO-POR-DISEÑO:" —
    # la guardia busca la causa por status, no por un prefijo fijo.
    causas = {f["reason"] for f in no_con if f.get("reason")}
    sin_piso_con_causa = {
        f["piso_fuente"].split(":", 1)[-1].split(" · SUCEDE-A:", 1)[0]
        for f in marginales
        if f["estado"] == "SIN-PISO" and ":" in f["piso_fuente"]
    }
    for causa in causas:
        if causa not in sin_piso_con_causa:
            _falla("T-ENLACE-BIYECTIVO",
                   f"la causa NO-CONSTRUIBLE {causa!r} de la tabla no aparece "
                   f"en ninguna fila SIN-PISO del marcador")


def t_precedencia_entre_tablas():
    """GUARDIA D-14 de `ACTO GEN2-MARCADOR-ENLACE-2` (P1).

    El defecto que atrapa ya ocurrió: `GEN2-PISOS-ENIF2021-FORMALIDAD-1`
    (PR #915) selló seis pisos y el enlace PARÓ porque `indice_identidad()`
    indexaba con `setdefault` -- las cuatro filas NO-CONSTRUIBLE de la
    rejilla, más antiguas, ganaban por orden de lectura y los seis RESULT
    quedaban sin enlazar. Le habría costado a un lector del marcador seis
    celdas SIN-PISO que el repo ya mide.

    Tres cosas, ninguna con cifra a mano:
      (a) ninguna clave repetida DENTRO de una misma tabla (eso sí es
          defecto: no hay orden que lo desempate);
      (b) para cada colisión ENTRE tablas, la fila que gobierna el índice
          es la de la tabla MÁS RECIENTE de `TABLAS_IDENTIDAD`;
      (c) toda celda gobernada por una fila sucesora lo DICE en
          `piso_fuente` (`· SUCEDE-A:<cell_id sucedido>`).
    """
    malas = M.colisiones_dentro_de_una_tabla()
    if malas:
        _falla("T-PRECEDENCIA", f"clave repetida dentro de una misma tabla: {malas}")

    por_cell = {f["cell_id"]: f for f in M.lee_tabla_identidad()}
    idx = M.indice_identidad()
    suc = M.sucesiones_identidad()
    for sucedido, sucesor in suc.items():
        a, b = por_cell[sucedido], por_cell[sucesor]
        if M._clave_identidad(a) != M._clave_identidad(b):
            _falla("T-PRECEDENCIA",
                   f"{sucedido} y {sucesor} se declaran sucesión y no comparten clave")
            continue
        if b["_orden"] <= a["_orden"]:
            _falla("T-PRECEDENCIA",
                   f"{sucesor} sucede a {sucedido} pero su tabla no es más reciente "
                   f"({b['_tabla']} orden {b['_orden']} vs {a['_tabla']} orden {a['_orden']})")
        if idx[M._clave_identidad(b)]["cell_id"] != sucesor:
            _falla("T-PRECEDENCIA",
                   f"el índice no gobierna con {sucesor}, la fila más reciente")

    # (c) el marcador lo dice
    marginales = [f for f in M.deriva()["filas"] if f["tipo"] == "MARGINAL"]
    for sucedido, sucesor in suc.items():
        filas = [f for f in marginales if f["resultado_id"] == sucesor
                 or f"SUCEDE-A:{sucedido}" in f["piso_fuente"]]
        if not filas:
            _falla("T-PRECEDENCIA",
                   f"{sucesor} gobierna una celda y ninguna fila MARGINAL lo reporta")
            continue
        for f in filas:
            if f"SUCEDE-A:{sucedido}" not in f["piso_fuente"]:
                _falla("T-PRECEDENCIA",
                       f"{f['celda_id']} usa la fila sucesora y no nombra a "
                       f"{sucedido} en piso_fuente: {f['piso_fuente']!r}")


def t_contrato_de_columnas_de_las_tablas():
    """Toda tabla de `TABLAS_IDENTIDAD` cumple el MISMO contrato de
    columnas. `lee_tabla_identidad()` lo exige y se cae si no; esta guardia
    prueba que la lista declarada hoy lo cumple y que no está vacía (A.13:
    una guardia sobre cero tablas no prueba nada)."""
    if len(M.TABLAS_IDENTIDAD) < 2:
        _falla("T-CONTRATO-TABLAS",
               f"la lista declara {len(M.TABLAS_IDENTIDAD)} tabla(s): la "
               f"generalización no está probada contra nada")
    existentes = [t for t in M.TABLAS_IDENTIDAD if t.exists()]
    if len(existentes) != len(M.TABLAS_IDENTIDAD):
        faltan = [str(t) for t in M.TABLAS_IDENTIDAD if not t.exists()]
        _falla("T-CONTRATO-TABLAS", f"tablas declaradas y ausentes del árbol: {faltan}")
    try:
        filas = M.lee_tabla_identidad()
    except ValueError as e:
        _falla("T-CONTRATO-TABLAS", str(e))
        return
    vistas = {f["_tabla"] for f in filas}
    for t in existentes:
        rel = str(t.relative_to(M.RAIZ))
        if rel not in vistas:
            _falla("T-CONTRATO-TABLAS", f"{rel} está declarada y no aportó ninguna fila")


def t_piso_no_es_m():
    """Firma de mesa (GEN2-MARCADOR-PISOS-ENLACE-1): «un piso acota a los
    retadores; no identifica nada y no sustituye a R en la ola que R ya
    midió». Ninguna fila MARGINAL puede traer el piso en la columna `M`."""
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "MARGINAL" and f["M"] not in ("", None):
            _falla("T-PISO-NO-ES-M",
                   f"{f['celda_id']} es MARGINAL y trae M={f['M']!r}: "
                   f"el piso no sustituye a R ni compite como estimador")


def t_unidad_leida_del_arbitro():
    """La unidad del dato se LEE del `payload` del árbitro, no se infiere
    del prefijo del id. Defecto corregido: ENCIG 2025 declara
    `unidad = TRÁMITE` y el marcador rotulaba `persona`."""
    v = M.deriva()
    esperado = {
        "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025": "tramite",
        "civico.denuncia.con_seguro_ejes_envipe2025": "delito",
        "tramite.evasion_norma_ejes_envipe2025": "delito",
        "dinero.ahorro.via_informal_ejes_enif2024": "persona_elegida_18mas",
    }
    for f in v["filas"]:
        if f["tipo"] != "MARGINAL":
            continue
        quiere = esperado.get(f["regla_o_eje_origen"])
        if quiere and f["unidad_dato"] != quiere:
            _falla("T-UNIDAD-ARBITRO",
                   f"{f['celda_id']}: unidad_dato={f['unidad_dato']!r}, "
                   f"el árbitro declara {quiere!r} en su payload")


def t_vetados_nunca_se_leen():
    """El veto `veto:pisos-866` es POR NOMBRE y sigue vigente: ningún
    `CALC-PISOS-*-EJES-0001` puede aparecer como fuente de piso."""
    v = M.deriva()
    for f in v["filas"]:
        for vetado in M.CALC_PISOS_VETADOS:
            if vetado in str(f.get("piso_fuente", "")):
                _falla("T-VETO-POR-NOMBRE",
                       f"{f['celda_id']} cita el CALC vetado {vetado}")
    for nombre in M.CALC_PISOS_SELLADOS:
        if nombre in M.CALC_PISOS_VETADOS:
            _falla("T-VETO-POR-NOMBRE",
                   f"{nombre} está a la vez en SELLADOS y en VETADOS")


def t_error_piso_derivado():
    """Las columnas `error_piso_pp` y `clase_persistencia` se DERIVAN de
    los RESULT sellados de `CALC-PISO-PERSISTENCIA-ERROR-0001`; el marcador
    no las recalcula. La guardia prueba que el id que el marcador arma
    coincide con el que el CALC selló.

    `ACTO GEN2-MARCADOR-ENLACE-2` (20/sep/2026) corrige la FORMA de la
    prueba sin debilitarla. Antes pedía «toda fila SOLO-PISO trae clase»,
    lo que daba por supuesto que el universo del CALC de error cubre todo
    piso que exista -- premisa que caducó en cuanto `#915` selló seis pisos
    nuevos que ese CALC (más viejo) no midió, y que este acto declara
    expresamente fuera de perímetro («no mide el error de persistencia de
    las 6 celdas nuevas»; sucesor: CALC nuevo).

    Se prueba contra el UNIVERSO DEL CALC, que es lo que manda, y en los
    dos sentidos -- ninguno de los dos admite una cifra a mano:
      (a) todo RESULT `-CLASE` sellado es reclamado por EXACTAMENTE UNA
          fila SOLO-PISO. Si el marcador armara mal un id, su RESULT se
          quedaría huérfano y esto falla -- es el mismo defecto de antes;
      (b) toda fila SOLO-PISO trae la clase EXACTA de su RESULT, o no trae
          ninguna de las dos columnas, y entonces el CALC no tiene RESULT
          para ella (piso más reciente que el CALC de error).
    """
    import json as _json
    rj = M.CALC_ERROR_PISO / "resultados.json"
    if not rj.exists():
        return                       # CALC no sellado: nada que comprobar
    res = _json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    sellados = {k[:-len("-CLASE")] for k in res if k.endswith("-CLASE")}
    if not sellados:
        _falla("T-ERROR-PISO-DERIVADO",
               "el CALC de error no trae ningún RESULT -CLASE (A.13)")
        return
    por_cell = {f["cell_id"]: f for f in M.lee_tabla_identidad()}
    v = M.deriva()

    # ACTO GEN2-ARBITRO-MARGINALES-1 (21/sep/2026): una fila con R GEN2
    # sellado es `EVALUADA` y sus dos columnas se LEEN de
    # `CALC-ARBITRO-PERSISTENCIA-ERROR-0001` (adjudicación contra la
    # realidad GEN2), no del CALC contra GEN1. La guardia se prueba en los
    # dos universos, cada uno contra SU CALC, y en los dos sentidos: (a) todo
    # `-CLASE` sellado lo reclama exactamente UNA fila (SOLO-PISO o EVALUADA
    # para el CALC GEN1, cuyo id sigue teniendo que calzar; EVALUADA para el
    # GEN2); (b) la clase de cada fila es EXACTAMENTE la de su RESULT.
    res_g2 = {}
    rj2 = M.CALC_ERROR_ARBITRO / "resultados.json"
    if rj2.exists():
        res_g2 = _json.loads(rj2.read_text(encoding="utf-8")).get("resultados", {})
    sellados_g2 = {k[:-len("-CLASE")] for k in res_g2 if k.endswith("-CLASE")}

    reclamados: dict[str, list] = {}
    reclamados_g2: dict[str, list] = {}
    for f in v["filas"]:
        if f["tipo"] != "MARGINAL":
            continue
        if f["estado"] not in ("SOLO-PISO", "EVALUADA"):
            if f["clase_persistencia"]:
                _falla("T-ERROR-PISO-DERIVADO",
                       f"{f['celda_id']} no es SOLO-PISO ni EVALUADA y trae clase "
                       f"{f['clase_persistencia']!r}")
            continue
        t = por_cell.get(f["resultado_id"], {})
        base = ("RESULT-PISO-ERR-"
                f"{M._slug_result(t.get('source_instrument'))}-"
                f"{M._slug_result(t.get('outcome'))}-"
                f"{M._slug_result(f['eje_o_par'])}-"
                f"{M._slug_result(f['categoria'])}")
        if base in sellados:
            reclamados.setdefault(base, []).append(f["celda_id"])
        if f["estado"] == "EVALUADA":
            calc_r, cell_id_r = f["fuente"].split("/", 1)
            if calc_r not in M.CALC_ARBITRO_R:
                _falla("T-ERROR-PISO-DERIVADO",
                       f"{f['celda_id']} EVALUADA con fuente fuera de CALC_ARBITRO_R: {calc_r}")
            base2 = M.id_error_gen2(cell_id_r)
            if base2 in sellados_g2:
                reclamados_g2.setdefault(base2, []).append(f["celda_id"])
                if res_g2.get(f"{base2}-CLASE") != f["clase_persistencia"] \
                        or res_g2.get(f"{base2}-D-PP") != f["error_piso_pp"]:
                    _falla("T-ERROR-PISO-DERIVADO",
                           f"{f['celda_id']}: clase/error del marcador "
                           f"{f['clase_persistencia']!r}/{f['error_piso_pp']!r} != RESULT GEN2 "
                           f"{res_g2.get(base2 + '-CLASE')!r}/{res_g2.get(base2 + '-D-PP')!r}")
            elif f["clase_persistencia"] or f["error_piso_pp"]:
                _falla("T-ERROR-PISO-DERIVADO",
                       f"{f['celda_id']} EVALUADA trae clase/error y el CALC GEN2 no selló "
                       f"{base2}: el marcador estaría estimando")
            continue
        if base in sellados:
            if res.get(f"{base}-CLASE") != f["clase_persistencia"]:
                _falla("T-ERROR-PISO-DERIVADO",
                       f"{f['celda_id']}: clase del marcador "
                       f"{f['clase_persistencia']!r} != RESULT "
                       f"{res.get(base + '-CLASE')!r}")
        elif f["clase_persistencia"] or f["error_piso_pp"]:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{f['celda_id']} trae clase/error y el CALC no selló "
                   f"{base}: el marcador estaría estimando")

    # (a) ningún RESULT sellado queda huérfano ni lo reclaman dos filas
    for base in sorted(sellados):
        n = len(reclamados.get(base, []))
        if n == 0:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{base} está sellado y ninguna fila SOLO-PISO/EVALUADA lo reclama: "
                   f"el id que el marcador arma no calza")
        elif n > 1:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{base} lo reclaman {n} filas: {reclamados[base]}")
    for base in sorted(sellados_g2):
        n = len(reclamados_g2.get(base, []))
        if n != 1:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{base} (GEN2) lo reclaman {n} filas EVALUADA: {reclamados_g2.get(base, [])}")


def t_marginales_adopcion_por_instrumento():
    """ACTO GEN2-MARGINALES-ADOPCION-1 (22/sep/2026): con la firma
    `adopcion:piso-t1-marginales-por-instrumento` en decisiones.tsv, las 57
    marginales EVALUADA se reparten 15 ADOPTADO-POR-FIRMA (ENVIPE) / 42
    DIFERIDA-o-VETADA-EN-NIVEL (ENIF+ENCIG), y sólo ese estado exacto pasa a
    `estimadores-por-segmento.yaml::marginales`. Ninguna fila SOLO-PISO o
    SIN-PISO recibe `adopcion_marginal` -- no hay instrumento contra qué
    decidir sin R GEN2 sellado."""
    v = M.deriva()
    marginales = [f for f in v["filas"] if f["tipo"] == "MARGINAL"]
    decididas = [f for f in marginales if f.get("adopcion_marginal")]
    if not decididas:
        _falla("T-MARGINALES-ADOPCION",
               "decisiones.tsv trae adopcion:piso-t1-marginales-por-instrumento "
               "y ninguna fila MARGINAL quedó decidida")
        return
    for f in decididas:
        if f["estado"] != "EVALUADA":
            _falla("T-MARGINALES-ADOPCION",
                   f"{f['celda_id']} tiene adopcion_marginal con estado "
                   f"base {f['estado']!r}, no EVALUADA")
    adoptadas = [f for f in decididas if f["adopcion_marginal"] == "ADOPTADO-POR-FIRMA"]
    otras = [f for f in decididas if f["adopcion_marginal"] != "ADOPTADO-POR-FIRMA"]
    if len(adoptadas) != 15 or len(otras) != 42:
        _falla("T-MARGINALES-ADOPCION",
               f"se esperaban 15 adoptadas / 42 diferidas-o-vetadas, salieron "
               f"{len(adoptadas)} / {len(otras)}")
    for f in adoptadas:
        if not f["instrumento"].startswith("ENVIPE 2025"):
            _falla("T-MARGINALES-ADOPCION",
                   f"{f['celda_id']} es ADOPTADO-POR-FIRMA con instrumento "
                   f"{f['instrumento']!r}, no ENVIPE 2025")
    for f in otras:
        if f["instrumento"].startswith("ENVIPE 2025"):
            _falla("T-MARGINALES-ADOPCION",
                   f"{f['celda_id']} es {f['adopcion_marginal']} pero su "
                   f"instrumento es ENVIPE 2025")
    # Escribe a un YAML PROPIO, nunca a M.ESTIMADORES_YAML: ese derivado no
    # viaja committeado en el PR (P4 §2(2), firma de mesa 21/sep/2026 -- el
    # job del push a `main` lo re-deriva), así que leerlo del árbol en CI
    # da el archivo VIEJO de `origin/main` y esta guardia falla en falso.
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8", dir=str(M.RAIZ))
    tmp.close()
    ruta_tmp = Path(tmp.name)
    ruta_original = M.ESTIMADORES_YAML
    M.ESTIMADORES_YAML = ruta_tmp
    try:
        M.escribe_estimadores_yaml(v["filas"])
        yml = M._yaml(ruta_tmp)
    finally:
        M.ESTIMADORES_YAML = ruta_original
        ruta_tmp.unlink(missing_ok=True)
    marg_yaml = yml.get("marginales") or {}
    if len(marg_yaml) != 57:
        _falla("T-MARGINALES-ADOPCION",
               f"estimadores-por-segmento.yaml::marginales trae "
               f"{len(marg_yaml)} celdas, se esperaban 57")
    n_champion = sum(1 for x in marg_yaml.values() if x.get("champion") == "PERSISTENCIA(t-1)")
    if n_champion != 57:
        _falla("T-MARGINALES-ADOPCION",
               f"{n_champion}/57 celdas de marginales traen champion=PERSISTENCIA(t-1)")
    n_cobertura = sum(1 for x in marg_yaml.values() if "cobertura" in x)
    n_veto = sum(1 for x in marg_yaml.values() if "veto" in x)
    if n_cobertura != 15 or n_veto != 42:
        _falla("T-MARGINALES-ADOPCION",
               f"cobertura citada en {n_cobertura} (se esperaban 15), "
               f"veto citado en {n_veto} (se esperaban 42)")


CASOS = (t_reserva_sin_r, t_emisor_no_compara, t_piso_no_circular,
         t_veinte_adoptadas, t_universo_97_nacional,
         t_enlace_biyectivo, t_piso_no_es_m, t_unidad_leida_del_arbitro,
         t_vetados_nunca_se_leen, t_error_piso_derivado,
         t_precedencia_entre_tablas, t_contrato_de_columnas_de_las_tablas,
         t_marginales_adopcion_por_instrumento)


def corre() -> list[str]:
    FALLOS.clear()
    for caso in CASOS:
        caso()
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    if fallos:
        print(f"FALLA -- {len(fallos)} caso(s):")
        for f in fallos:
            print(f"  - {f}")
        return 1
    print(f"PASA -- {len(CASOS)} casos de tests/test_marcador_segmento.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
