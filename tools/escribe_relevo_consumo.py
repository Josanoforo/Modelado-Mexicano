#!/usr/bin/env python3
"""Escritor acotado del consumo GEN2 de trámite, desde pin firmado y RESULT.

V1 admite solo el caso revisado RES-0028. No firma pines ni decide adopción.
Uso: python3 tools/escribe_relevo_consumo.py [--apply]. Por defecto imprime
el diff seco. El merge de mesa del PR materializa la adopción.

V2 (ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4, 24/sep/2026) añade el modo «crear
regla desde propuesta»: crea en `milpa/tramite.yaml` una regla que hoy solo
vive en `milpa/tramite-ola5-propuesta-v0.yaml`, copiando VERBATIM (texto,
no re-serializado) el bloque `entonces:` y los demás campos medidos, y
rellenando los cuatro campos que la propuesta deja `PENDIENTE-DE-MESA`
(`situacion`/`si.disparadores`/`porque`/`tier`/`falsable_si`) desde un
archivo de redacción del ejecutor, rotulados `PROPUESTO-POR-EJECUTOR`.
Uso: python3 tools/escribe_relevo_consumo.py --crear-desde-propuesta
[--apply].
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# `tools/` no es paquete: los tests importan `tools.escribe_relevo_consumo`
# por namespace y ahí el directorio propio no entra solo en sys.path.
# Mismo patrón que tools/corrida0.py, para que las dos vías de import
# (dotted y bare) se resuelvan sin importar cómo se invoque este módulo.
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
TARGET = ROOT / "milpa/tramite.yaml"
EXPECTED_TARGET_SHA = "0bb0ba70dba1c8e77b8dc2676d09be3546327ac526bd0a362d8e62e9359659fe"
SLOT = "RES-0028"
CONSUMER = "milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon"
KEY = "tramite::civico.denuncia.miedo_desconfianza::denuncia_por_otra_razon"
CALC = "CALC-ENVIPE-RES0028-U4-DERIVADO-0001"
RESULT = "RESULT-ENVIPE-RES0028-Q-C2-U4"
OLD_P = "0.705687"

# ── V2 · modo «crear regla desde propuesta» ─────────────────────────────
PROPUESTA = ROOT / "milpa/tramite-ola5-propuesta-v0.yaml"
REDACCION = ROOT / "forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml"

IDS_CREAR_DESDE_PROPUESTA = (
    "civico.contexto_institucional_victimas.lapop",
    "dinero.credito.atraso_y_dano_por_producto_banxico",
    "trabajo.prestaciones.valoracion_seguridad_social_motral",
)

ACTO_V2 = "GEN2-ADOPCION-BLOQUE-Y-PINES-4"

# Cita de origen dentro de la propuesta: línea de la propia regla y la
# firma de mesa que autorizó que existiera ahí como proxy descriptivo
# (no la firma que autoriza promoverla al motor vivo -- esa es la misma
# para las tres, ver `_ENCABEZADO_PROMOCION` abajo).
_CITAS_ORIGEN_PROPUESTA = {
    "civico.contexto_institucional_victimas.lapop": (
        "líneas 3985-4025; OBJETO 8 de la HOJA DE FIRMAS DE MESA "
        "2026-09-15 (NC-0167), firma «Si a todas.», ACTO "
        "GEN2-FIRMAS-MESA-1, 15/sep/2026"
    ),
    "dinero.credito.atraso_y_dano_por_producto_banxico": (
        "líneas 4041-4067; OBJETO 9 de la HOJA DE FIRMAS DE MESA "
        "2026-09-15 (NC-0186 + NC-0164), firma «Si a todas.», ACTO "
        "GEN2-FIRMAS-MESA-1, 15/sep/2026"
    ),
    "trabajo.prestaciones.valoracion_seguridad_social_motral": (
        "líneas 4069-4089; OBJETO 9 de la HOJA DE FIRMAS DE MESA "
        "2026-09-15 (NC-0186 + NC-0164), firma «Si a todas.», ACTO "
        "GEN2-FIRMAS-MESA-1, 15/sep/2026"
    ),
}

_ENCABEZADO_PROMOCION = (
    "FIRMAS-7 (…369b-01, 21/sep/2026, bloque de diez RESULT ADOPTADOS) + "
    "Decisión 2 de ADOPCION-2 (W, 24/sep/2026: INTERPRETACIÓN-DECLARADA -- "
    "«regla existente» presuponía un hecho falso, la intención se "
    "preserva creando la regla) + cláusula de autonomía v1.0 (mesa, "
    "24/sep/2026, forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md §3)"
)


def _yaml_load(ruta: Path):
    import yaml  # noqa: PLC0415
    return yaml.safe_load(ruta.read_text(encoding="utf-8"))


def _propuesta_reglas() -> dict:
    doc = _yaml_load(PROPUESTA)
    return {r["id"]: r for r in doc["reglas_propuestas"]}


def _resultados_por_id() -> dict:
    from tools.vista import leer_resultados_join  # noqa: PLC0415
    return {f["resultado_id"]: f for f in leer_resultados_join()}


def _extraer_bloque_regla(lineas: list[str], rule_id: str) -> list[str]:
    """Devuelve, como lista de líneas CON su terminador, el bloque
    verbatim de `rule_id` dentro de un YAML con el esquema de
    `tramite.yaml`/`tramite-ola5-propuesta-v0.yaml`: desde su propia
    línea `  - id: <rule_id>` hasta (sin incluir) la siguiente línea
    `  - id: `, recortando al final las líneas en blanco y los
    comentarios-separador de nivel de lista (`  # ...`, 2 espacios) que
    en este archivo documentan la regla SIGUIENTE, no ésta -- los
    comentarios propios de la regla usan indentación de 4+ espacios."""
    marca = f"  - id: {rule_id}\n"
    apariciones = [i for i, l in enumerate(lineas) if l == marca]
    if len(apariciones) != 1:
        raise ValueError(
            f"{rule_id}: se esperaba una aparición única de {marca!r} "
            f"en {PROPUESTA}, hay {len(apariciones)}")
    inicio = apariciones[0]
    fin = len(lineas)
    for j in range(inicio + 1, len(lineas)):
        if lineas[j].startswith("  - id: "):
            fin = j
            break
    bloque = lineas[inicio:fin]
    while bloque and (bloque[-1].strip() == "" or bloque[-1].startswith("  #")):
        bloque.pop()
    return bloque


def _dividir_bloque(bloque: list[str], rule_id: str) -> tuple[str, str]:
    """Separa el bloque en (`entonces:` verbatim, cola verbatim desde
    `fuente:` -- lo que sigue a `falsable_si:` -- hasta el final). Los
    campos que van entre las dos secciones (`situacion`/`si`/`porque`/
    `tier`/`falsable_si`) los redacta este acto; no se copian de la
    propuesta."""
    i_entonces = next(
        (i for i, l in enumerate(bloque) if l.strip() == "entonces:"), None)
    i_falsable = next(
        (i for i, l in enumerate(bloque) if l.lstrip().startswith("falsable_si:")),
        None)
    if i_entonces is None or i_falsable is None:
        raise ValueError(
            f"{rule_id}: bloque de propuesta sin entonces:/falsable_si: "
            "reconocibles -- revisar a mano antes de automatizar")
    i_porque = next(
        (i for i in range(i_entonces, len(bloque))
         if bloque[i].lstrip().startswith("porque:")), None)
    if i_porque is None or i_porque <= i_entonces:
        raise ValueError(f"{rule_id}: no se halló porque: después de entonces:")
    entonces_verbatim = "".join(bloque[i_entonces:i_porque])
    cola_verbatim = "".join(bloque[i_falsable + 1:])
    return entonces_verbatim, cola_verbatim


def _verifica_entonces(rid: str, regla_propuesta: dict, resultados: dict) -> None:
    """`p` de la propuesta debe identificar exactamente al RESULT sellado
    que su propia cita declara -- la misma disciplina de «cambiar un `p`
    es otra firma» que PINES-3 (§7.c) ya impuso. Una conducta
    NO-ESTIMABLE (`p: null`) no se verifica contra ningún RESULT: tampoco
    se vuelve consumidor (mismo criterio que `_consumidores_conductas`
    de `tools/corrida0.py`, que salta `salida.p is None`)."""
    for salida in regla_propuesta["entonces"]:
        p = salida.get("p")
        conducta = salida["conducta"]
        if p is None:
            continue
        rid_result = salida.get("corrida0_resultado_id")
        fila = resultados.get(rid_result)
        if fila is None:
            raise ValueError(
                f"{rid}/{conducta}: {rid_result} no está en resultados.tsv")
        valor = float(fila["valor"])
        if valor != p:
            raise ValueError(
                f"{rid}/{conducta}: p de la propuesta ({p!r}) no identifica "
                f"al RESULT sellado ({valor!r})")
        if salida.get("corrida0_generacion") != "GEN2":
            raise ValueError(
                f"{rid}/{conducta}: corrida0_generacion != GEN2")
        if salida.get("rol_uso") != "proxy_descriptivo":
            raise ValueError(
                f"{rid}/{conducta}: rol_uso inesperado "
                f"{salida.get('rol_uso')!r}")


def _una_linea(texto: str) -> str:
    return " ".join(str(texto).split())


def _renderiza_regla_nueva(rule_id: str, entonces_verbatim: str,
                           cola_verbatim: str, redaccion: dict) -> str:
    campos = redaccion[rule_id]
    situacion = campos["situacion"]
    disparadores_estado = _una_linea(campos["disparadores_estado"])
    tier = campos["tier"]
    falsable_si = _una_linea(campos["falsable_si"])
    generador = campos["porque"]["generador"]
    mecanismo = _una_linea(campos["porque"]["mecanismo"])
    for etiqueta, valor in (("situacion", situacion),
                            ("disparadores_estado", disparadores_estado),
                            ("tier", tier), ("falsable_si", falsable_si),
                            ("mecanismo", mecanismo)):
        if '"' in valor:
            raise ValueError(
                f"{rule_id}.{etiqueta}: contiene comillas rectas, no se "
                "puede emitir como escalar YAML entre comillas dobles "
                "-- usar comillas angulares « » en la redacción")
    generador_yaml = "[" + ", ".join(generador) + "]"
    origen = _CITAS_ORIGEN_PROPUESTA[rule_id]
    encabezado = (
        "\n"
        "  # ══════════════════════════════════════════════════════════════════\n"
        f"  # ACTO {ACTO_V2} · 24/sep/2026 · regla nueva, copiada VERBATIM\n"
        "  # (texto, no re-serializada) de milpa/tramite-ola5-propuesta-v0.yaml\n"
        f"  # ({origen}): `entonces:`/`fuente`/el resto de campos medidos,\n"
        "  # carácter por carácter -- ningún `p` ni cita de RESULT se retoca.\n"
        f"  # Promoción al motor vivo autorizada por {_ENCABEZADO_PROMOCION}.\n"
        "  # `situacion`/`si.disparadores_estado`/`porque`/`tier`/\n"
        "  # `falsable_si` son PROPUESTO-POR-EJECUTOR\n"
        "  # (forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml); mesa\n"
        "  # los adopta o corrige al fusionar este PR (E.2).\n"
        "  # ══════════════════════════════════════════════════════════════════\n"
    )
    cuerpo = (
        f"  - id: {rule_id}\n"
        f"    situacion: {situacion}  # PROPUESTO-POR-EJECUTOR\n"
        "    si:\n"
        "      disparadores: {}\n"
        f"      disparadores_estado: \"{disparadores_estado}\"  # PROPUESTO-POR-EJECUTOR\n"
        f"{entonces_verbatim}"
        f"    porque: {{generador: {generador_yaml}, mecanismo: \"{mecanismo}\"}}  # PROPUESTO-POR-EJECUTOR\n"
        f"    tier: {tier}  # PROPUESTO-POR-EJECUTOR\n"
        f"    falsable_si: \"{falsable_si}\"  # PROPUESTO-POR-EJECUTOR\n"
        f"{cola_verbatim}"
    )
    return encabezado + cuerpo


def crear_desde_propuesta(apply_: bool = False) -> None:
    propuesta_lineas = PROPUESTA.read_text(encoding="utf-8").splitlines(keepends=True)
    reglas_propuesta = _propuesta_reglas()
    redaccion = _yaml_load(REDACCION)["reglas"]
    resultados = _resultados_por_id()

    old = TARGET.read_text(encoding="utf-8")
    ya_presentes = [rid for rid in IDS_CREAR_DESDE_PROPUESTA
                    if re.search(rf"^  - id: {re.escape(rid)}$", old, re.M)]
    if ya_presentes:
        raise ValueError(
            f"ya presentes en el consumidor vivo, no se re-crean: {ya_presentes}")

    bloques_nuevos = []
    for rid in IDS_CREAR_DESDE_PROPUESTA:
        if rid not in redaccion:
            raise ValueError(f"{rid}: sin redacción en {REDACCION}")
        if rid not in reglas_propuesta:
            raise ValueError(f"{rid}: no existe en {PROPUESTA}")
        _verifica_entonces(rid, reglas_propuesta[rid], resultados)
        bloque = _extraer_bloque_regla(propuesta_lineas, rid)
        entonces_verbatim, cola_verbatim = _dividir_bloque(bloque, rid)
        bloques_nuevos.append(_renderiza_regla_nueva(
            rid, entonces_verbatim, cola_verbatim, redaccion))

    nuevo = old.rstrip("\n") + "\n" + "".join(bloques_nuevos)

    # Autoverificación: el archivo resultante debe cargar con el mismo
    # cargador que usa el motor, y las tres reglas nuevas deben traer el
    # `p` y el `corrida0_resultado_id` idénticos a la propuesta -- no
    # solo el texto copiado, también lo que `cargar_reglas` interpreta de
    # él (atrapa un error de indentación silencioso en el corte de
    # `_dividir_bloque`).
    from milpa.src.emisor import cargar_reglas  # noqa: PLC0415
    with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".yaml", delete=False) as fh:
        fh.write(nuevo)
        ruta_tmp = Path(fh.name)
    try:
        reglas_cargadas = {r.id: r for r in cargar_reglas(ruta_tmp)}
        for rid in IDS_CREAR_DESDE_PROPUESTA:
            regla = reglas_cargadas.get(rid)
            if regla is None:
                raise ValueError(f"{rid}: no cargó en la simulación de --apply")
            for salida in regla.entonces:
                esperado = next(
                    e for e in reglas_propuesta[rid]["entonces"]
                    if e["conducta"] == salida.conducta)
                if salida.p != esperado.get("p"):
                    raise ValueError(
                        f"{rid}/{salida.conducta}: p cargado ({salida.p!r}) "
                        f"no idéntico al de la propuesta ({esperado.get('p')!r})")
                if salida.resultado_id != esperado.get("corrida0_resultado_id"):
                    raise ValueError(
                        f"{rid}/{salida.conducta}: corrida0_resultado_id "
                        "cargado no idéntico al de la propuesta")
    finally:
        ruta_tmp.unlink(missing_ok=True)

    diff = "".join(difflib.unified_diff(
        old.splitlines(keepends=True), nuevo.splitlines(keepends=True),
        fromfile="a/milpa/tramite.yaml", tofile="b/milpa/tramite.yaml"))
    print(diff)
    if apply_:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=TARGET.parent,
                prefix=".relevo-consumo-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(nuevo)
        try:
            os.replace(temp, TARGET)
        finally:
            temp.unlink(missing_ok=True)
        print("APLICADO: tres reglas nuevas; p y corrida0_resultado_id "
              "idénticos a la propuesta, campos pendientes redactados y "
              "rotulados PROPUESTO-POR-EJECUTOR")


# ── V3 · ACTO GEN2-RELEVO-MOTOR-34-1 · relevo por lote de conductas del motor ──
ACTO_V3 = "GEN2-RELEVO-MOTOR-34-1"
CORRIDAS_DIR = ROOT / "data/corrida0"
CORRIDAS_TSV = CORRIDAS_DIR / "corridas.tsv"
REPLAY_TSV = ROOT / "forense/replay-evidencia.tsv"
VIA_I, VIA_III = "i-CRUDO", "iii-DERIVADO-DE-GEN2"

# Cada relevo liga UNA conducta de una regla a UN RESULT sellado. La liga no
# se infiere por nombre: vía (iii) exige que la spec del derivado declare
# este mismo consumidor; vía (i) exige que la regla y el CALC citen el mismo
# payload del manifiesto (`sha256_payload`).
RELEVOS_V3 = (
    ("tramite.mordida.discrecional", "tramite_normal_encig2025",
     "CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001", "RESULT-ENCIGDER-A-Q", VIA_III),
    ("tramite.mordida.discrecional", "sin_solicitud_y_sin_entrega_encuci2020",
     "CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001", "RESULT-ENCUCIDER-A-Q", VIA_III),
    ("tramite.mordida.con_registro", "tramite_normal_encig2025_presencial_r2",
     "CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001", "RESULT-ENCIGDER-B-PRE-SD-Q", VIA_III),
    ("tramite.mordida.con_registro", "tramite_normal_encig2025_digital_r2",
     "CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001", "RESULT-ENCIGDER-B-DIG-SD-Q", VIA_III),
    ("tramite.gobierno_digital.util_sin_coercion", "rechaza_servicio_encig2025_luz",
     "CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001", "RESULT-ENCIGDER-C-Q", VIA_III),
    ("civico.denuncia.con_seguro", "denuncia",
     "CALC-ENVIPE-DENUNCIA-SEGURO-0001", "RESULT-ENVIPE-SEG-CON-P-DENUNCIA", VIA_I),
    ("civico.denuncia.con_seguro", "no_denuncia",
     "CALC-ENVIPE-DENUNCIA-SEGURO-0001", "RESULT-ENVIPE-SEG-CON-P-NO-DENUNCIA", VIA_I),
    ("civico.denuncia.sin_seguro", "denuncia",
     "CALC-ENVIPE-DENUNCIA-SEGURO-0001", "RESULT-ENVIPE-SEG-SIN-P-DENUNCIA", VIA_I),
    ("civico.denuncia.sin_seguro", "no_denuncia",
     "CALC-ENVIPE-DENUNCIA-SEGURO-0001", "RESULT-ENVIPE-SEG-SIN-P-NO-DENUNCIA", VIA_I),
)

_COMENTARIO_OBSOLETO_V3 = "Sin corrida0 propia, sin cita corrida0_*."
_COMENTARIO_NUEVO_V3 = (
    f"Relevado por clase iii (ACTO {ACTO_V3}): cita el complemento sellado "
    "de CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001.")


def _leer_tsv_simple(ruta: Path) -> list[dict]:
    import csv  # noqa: PLC0415
    csv.field_size_limit(sys.maxsize)
    lineas = [l for l in ruta.read_text(encoding="utf-8").splitlines()
              if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _ctx_corridas() -> dict:
    """`calc -> {estado, cuenta_gen2, resultado_replay}`: la vista publicada,
    completada para los CALC sellados en esta rama que el canal [deriva]
    todavía no publicó (se leen de su sello, su spec y su asiento de replay,
    las tres fuentes de las que la vista misma se deriva)."""
    ctx = {f["spec_id"]: {"estado": f["estado"], "cuenta_gen2": f["cuenta_gen2"],
                          "resultado_replay": f["resultado_replay"]}
           for f in _leer_tsv_simple(CORRIDAS_TSV) if f.get("origen") == "OFERTA"}
    asientos = {f["calc_id"]: f for f in _leer_tsv_simple(REPLAY_TSV)}
    for calc in {c for *_, c, _r, _v in RELEVOS_V3} - set(ctx):
        carpeta = CORRIDAS_DIR / calc
        sello = carpeta / "sello.json"
        if not sello.exists():
            continue
        spec = _yaml_load(carpeta / "spec.yaml")
        asiento = asientos.get(calc, {})
        ctx[calc] = {
            "estado": "SELLADA" if _sello_coincide(carpeta) else "SELLO-DISCORDANTE",
            "cuenta_gen2": str((spec.get("etiquetas") or {}).get("cuenta_gen2", "")),
            "resultado_replay": asiento.get("resultado_replay", "NO-VERIFICADO"),
        }
    return ctx


def _sello_coincide(carpeta: Path) -> bool:
    sello_json = carpeta / "sello.json"
    lado = (carpeta / "sello.sha256").read_text().split()
    if not lado or lado[0] != sha(sello_json):
        return False
    cubre = json.loads(sello_json.read_text())
    return all(sha(carpeta / nombre) == h for nombre, h in cubre.items())


def guardas_v3(relevo: tuple, ctx: dict, reglas: dict) -> float:
    """Las guardas de 4.1 (+D6: eje RESULTADO) sobre un relevo del motor.
    Devuelve el valor sellado del RESULT o levanta ValueError con la razón."""
    import pines_mesa  # noqa: PLC0415
    regla_id, conducta, calc, result, via = relevo
    consumidor = f"milpa/tramite.yaml:{regla_id}:{conducta}"
    carpeta = CORRIDAS_DIR / calc
    if not (carpeta / "sello.json").exists() or not _sello_coincide(carpeta):
        raise ValueError(f"{consumidor}: {calc} sin sello o sello discordante")
    estado = ctx.get(calc)
    if estado is None:
        raise ValueError(f"{consumidor}: {calc} no está en el registro")
    if not str(estado["estado"]).startswith("SELLADA"):
        raise ValueError(f"{consumidor}: {calc} estado={estado['estado']!r}")
    if estado["cuenta_gen2"] != "SI":
        raise ValueError(f"{consumidor}: {calc} cuenta_gen2={estado['cuenta_gen2']!r}")
    if estado["resultado_replay"] not in pines_mesa.veredictos_afirmativos_en_resultado():
        raise ValueError(f"{consumidor}: replay de {calc} = "
                         f"{estado['resultado_replay']!r}, no afirmativo en RESULTADO")
    spec = _yaml_load(carpeta / "spec.yaml")
    if via == VIA_I:
        if pines_mesa._ingiere(spec) or not pines_mesa._tiene_crudo(spec):
            raise ValueError(f"{consumidor}: vía (i) exige insumo crudo sin ingestión")
        regla = reglas[regla_id]
        pid = str(regla.get("payload_manifiesto_id", ""))
        ids_crudo = {str(i.get("id")) for i in spec.get("inputs") or []
                     if i.get("origen") == "manifiesto"}
        manifiesto = {e["id"]: e for e in _yaml_load(ROOT / "data/manifiesto.yaml")
                      if isinstance(e, dict) and "id" in e}
        if (not pid or pid not in ids_crudo
                or str(manifiesto.get(pid, {}).get("sha256")) != str(regla.get("sha256_payload"))):
            raise ValueError(f"{consumidor}: la regla y {calc} no citan el mismo payload")
    elif via == VIA_III:
        specs = {c: _yaml_load(CORRIDAS_DIR / c / "spec.yaml")
                 for c in pines_mesa._calcs_ingeridos(spec)[0]
                 if (CORRIDAS_DIR / c / "spec.yaml").exists()}
        codigo, razon = pines_mesa._valida_derivado(consumidor, calc, spec, ctx, specs)
        if codigo != pines_mesa.ACEPTADO:
            raise ValueError(f"{codigo}: {razon}")
        declarados = {(c["consumidor"], c["prefijo"] + "Q")
                      for c in spec["parametros"]["complementos"]}
        if (consumidor, result) not in declarados:
            raise ValueError(f"{consumidor}: {calc} no declara {result} para este consumidor")
    else:
        raise ValueError(f"{consumidor}: vía desconocida {via!r}")
    valor = json.loads((carpeta / "resultados.json").read_text())["resultados"].get(result)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
        raise ValueError(f"{consumidor}: {result}={valor!r} fuera de escala [0,1]")
    return float(valor)


def _ubica_conducta(lineas: list[str], regla_id: str, conducta: str) -> int:
    inicio = [i for i, l in enumerate(lineas) if l.rstrip("\n") == f"  - id: {regla_id}"]
    if len(inicio) != 1:
        raise ValueError(f"{regla_id}: se esperaba una regla única, hay {len(inicio)}")
    fin = next((j for j in range(inicio[0] + 1, len(lineas))
                if lineas[j].startswith("  - id: ")), len(lineas))
    patron = re.compile(rf"(\{{|- )conducta: {re.escape(conducta)}(,|\s*$)")
    hits = [j for j in range(inicio[0], fin) if patron.search(lineas[j])]
    if len(hits) != 1:
        raise ValueError(f"{regla_id}:{conducta}: se esperaba una conducta única, hay {len(hits)}")
    return hits[0]


def transform_v3(source: str, relevo: tuple, valor: float) -> str:
    regla_id, conducta, _calc, result, via = relevo
    lineas = source.splitlines(keepends=True)
    i = _ubica_conducta(lineas, regla_id, conducta)
    rendered = f"{valor:.6f}"
    cita = f"corrida0_resultado_id: {result}, corrida0_generacion: GEN2"
    linea = lineas[i]
    if linea.lstrip().startswith("- {"):
        codigo = linea.split("}  #", 1)[0]
        if "corrida0_" in codigo:
            if cita in codigo and f"p: {rendered}," in codigo:
                return source
            raise ValueError(f"{regla_id}:{conducta}: cita previa distinta; rechazo atómico")
        m = re.search(r"\bp: ([0-9.]+),", linea)
        if m is None:
            raise ValueError(f"{regla_id}:{conducta}: p literal no localizado")
        if via == VIA_III and m.group(1) != rendered:
            raise ValueError(f"{regla_id}:{conducta}: vía (iii) no cambia p "
                             f"({m.group(1)} != {rendered})")
        linea = linea[:m.start()] + f"p: {rendered}, {cita}," + linea[m.end():]
        linea = linea.replace(_COMENTARIO_OBSOLETO_V3, _COMENTARIO_NUEVO_V3)
        lineas[i] = linea
        return "".join(lineas)
    # forma bloque: `- conducta: X` y campos indentados debajo.
    fin = next(j for j in range(i + 1, len(lineas))
               if not lineas[j].startswith(" " * 8))
    bloque = range(i + 1, fin)
    if any("corrida0_" in lineas[j] for j in bloque):
        if any(f"corrida0_resultado_id: {result}" in lineas[j] for j in bloque):
            return source
        raise ValueError(f"{regla_id}:{conducta}: cita previa distinta; rechazo atómico")
    jp = [j for j in bloque if re.fullmatch(r" {8}p: [0-9.]+\n", lineas[j])]
    if len(jp) != 1:
        raise ValueError(f"{regla_id}:{conducta}: p de bloque no único")
    actual = lineas[jp[0]].split(":", 1)[1].strip()
    if via == VIA_III and actual != rendered:
        raise ValueError(f"{regla_id}:{conducta}: vía (iii) no cambia p ({actual} != {rendered})")
    lineas[jp[0]] = (f"        p: {rendered}\n"
                     f"        corrida0_resultado_id: {result}\n"
                     f"        corrida0_generacion: GEN2\n")
    return "".join(lineas)


def relevo_motor_v3(apply_: bool = False) -> None:
    reglas = {r["id"]: r for r in _yaml_load(TARGET)["reglas"]}
    ctx = _ctx_corridas()
    old = TARGET.read_text(encoding="utf-8")
    nuevo = old
    for relevo in RELEVOS_V3:
        nuevo = transform_v3(nuevo, relevo, guardas_v3(relevo, ctx, reglas))

    from milpa.src.emisor import cargar_reglas  # noqa: PLC0415
    with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".yaml", delete=False) as fh:
        fh.write(nuevo)
        ruta_tmp = Path(fh.name)
    try:
        cargadas = {r.id: r for r in cargar_reglas(ruta_tmp)}
    finally:
        ruta_tmp.unlink(missing_ok=True)
    for regla_id, conducta, calc, result, _via in RELEVOS_V3:
        salida = next(s for s in cargadas[regla_id].entonces if s.conducta == conducta)
        valor = json.loads((CORRIDAS_DIR / calc / "resultados.json").read_text())["resultados"][result]
        if salida.resultado_id != result or f"{salida.p:.6f}" != f"{valor:.6f}":
            raise ValueError(f"{regla_id}:{conducta}: no cargó con p=RESULT y su cita")

    diff = "".join(difflib.unified_diff(
        old.splitlines(keepends=True), nuevo.splitlines(keepends=True),
        fromfile="a/milpa/tramite.yaml", tofile="b/milpa/tramite.yaml"))
    print(diff or "SIN-DIFF: ya aplicado")
    if apply_ and nuevo != old:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=TARGET.parent,
                prefix=".relevo-consumo-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(nuevo)
        try:
            os.replace(temp, TARGET)
        finally:
            temp.unlink(missing_ok=True)
        print(f"APLICADO: {len(RELEVOS_V3)} conductas; p = RESULT al grano de seis "
              "decimales y cita GEN2; vía (iii) sin cambio de p")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence() -> str:
    sys.path.insert(0, str(ROOT / "tools"))
    import pines_mesa  # noqa: PLC0415

    pins = [p for p in pines_mesa.lee_pines() if p["llave_logica"] == KEY]
    if len(pins) != 1:
        raise ValueError("falta pin único de mesa para la llave exacta")
    pin = pins[0]
    if (pin["calc_gen2"], pin["result_gen2"], pin["via"]) != (
        CALC, RESULT, pines_mesa.VIA_DERIVADO
    ):
        raise ValueError("pin firmado cambió de identidad o vía")
    if not pin["firma"].strip() or not any(
        word in pin["nota"].lower() for word in ("replay", "contexto")
    ):
        raise ValueError("pin sin firma o sin declaración de replay/contexto")

    rows = json.loads(subprocess.run(
        [sys.executable, str(ROOT / "tools/relevo_usos.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout)
    matches = [r for r in rows if r["resultado_id"] == SLOT]
    if len(matches) != 1:
        raise ValueError("slot posicional cambió; revisar llave lógica")
    row = matches[0]
    if (row["consumidor"], row["veredicto"], row["calc_candidato"],
            row["result_gen2_candidato"], row["valor_legacy"]) != (
            CONSUMER, "RELEVADO-POR-PIN-DE-MESA", CALC, RESULT, OLD_P):
        raise ValueError("relevo no validó pin, identidad o valor legacy")
    if "paso las cuatro guardas" not in row["razon"]:
        raise ValueError("faltó verificación de las guardas del pin")

    folder = ROOT / "data/corrida0" / CALC
    seal_line = (folder / "sello.sha256").read_text().split()
    if seal_line != [sha(folder / "sello.json"), "sello.json"]:
        raise ValueError("sello de CALC no coincide")
    value = json.loads((folder / "resultados.json").read_text())["resultados"][RESULT]
    if not isinstance(value, (int, float)) or not 0 <= value <= 1:
        raise ValueError("RESULT fuera de escala proporción [0,1]")
    if str(row["valor_gen2"]) != str(value):
        raise ValueError("oferta y RESULT discrepan")
    rendered = f"{value:.6f}"
    if rendered != OLD_P:
        raise ValueError("el RESULT no coincide con el literal al grano de seis decimales")
    return rendered


def transform(source: str, rendered: str) -> str:
    lines = source.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines)
               if re.search(r"\bconducta: denuncia_por_otra_razon\b", line)]
    if len(matches) != 1:
        raise ValueError("conducta no es única")
    i = matches[0]
    line = lines[i]
    citation = f", corrida0_resultado_id: {RESULT}, corrida0_generacion: GEN2"
    if citation in line:
        if f"p: {rendered}" not in line or "PROPUESTA-NO-ADOPTADA-NC-0085" in line:
            raise ValueError("cita aplicada con valor o estado editorial inconsistente")
        return source
    if "corrida0_resultado_id:" in line or "corrida0_generacion:" in line:
        raise ValueError("cita parcial o distinta; rechazo atómico")
    if line.count("p: " + OLD_P) != 1:
        raise ValueError("literal previo no coincide")
    if line.count("}") < 1 or "rol_uso: complemento_dependiente" not in line:
        raise ValueError("estructura o rol de consumo cambió")
    before, marker, after = line.partition(", clase:")
    if not marker:
        raise ValueError("no se halló límite de campo p")
    if not before.endswith("p: " + OLD_P):
        raise ValueError("p no está en posición esperada")
    updated = before + citation + marker + after
    old_status = "PROPUESTA-NO-ADOPTADA-NC-0085: "
    if updated.count(old_status) != 1:
        raise ValueError("estado editorial previo cambió")
    lines[i] = updated.replace(old_status, "GEN2-RELEVADO-POR-PIN (antecedente NC-0085): ")
    return "".join(lines)


# ── V4 · ACTO GEN2-RELEVO-CONSUMIDORES-2 · procedencia y catálogo ─────────
# Esquema de cita B4 (opción a): la cita va en la propia entrada, junto al
# valor. Mismas guardas de 4.1 (+D6) que V3, vía (i): CALC sellado, cuenta
# GEN2, replay afirmativo en RESULTADO, insumo crudo sin ingestión.
ACTO_V4 = "GEN2-RELEVO-CONSUMIDORES-2"
PROCEDENCIA = ROOT / "milpa/procedencia.yaml"
CATALOGO = ROOT / "milpa/catalogo-momentos-v0_1.tsv"
CALC_SEGURO = "CALC-ENVIPE-DENUNCIA-SEGURO-0001"
CLASE_SEGURO = ("MEDIDO·p(tasa base ponderada, condicional a seguro; unidad "
                "delito, robo total de vehículo BPCOD=01)")

# (regla de asignados_probabilidad, RESULT por categoría en el orden de `valores`)
RELEVOS_PROCEDENCIA_V4 = (
    ("civico.denuncia.con_seguro",
     ("RESULT-ENVIPE-SEG-CON-P-DENUNCIA", "RESULT-ENVIPE-SEG-CON-P-NO-DENUNCIA")),
)
# (momento, RESULT, discrepancia_gen1) -- M08 bajo firma N (unidad DELITO).
RELEVOS_CATALOGO_V4 = (
    ("M08", "RESULT-ENVIPE-SEG-CON-P-DENUNCIA",
     "NO-REPRODUCE-GEN1: unidad DELITO (robo total de vehículo, FAC_DEL), "
     "no registro PERSONA; firma N"),
)
COLUMNAS_CATALOGO_V4 = ("valor_gen2", "corrida0_resultado_id",
                        "corrida0_generacion", "calc_gen2", "sello_gen2",
                        "discrepancia_gen1")


def guardas_v4(consumidor: str, calc: str, result: str, ctx: dict) -> float:
    """Guardas de 4.1 (+D6) vía (i), sin la liga regla↔payload de V3 (la
    entrada de procedencia y el catálogo no citan payload): la liga es la
    tabla de arriba, revisada por llave en los tests."""
    import pines_mesa  # noqa: PLC0415
    carpeta = CORRIDAS_DIR / calc
    if not (carpeta / "sello.json").exists() or not _sello_coincide(carpeta):
        raise ValueError(f"{consumidor}: {calc} sin sello o sello discordante")
    estado = ctx.get(calc)
    if estado is None or not str(estado["estado"]).startswith("SELLADA"):
        raise ValueError(f"{consumidor}: {calc} no SELLADA en el registro")
    if estado["cuenta_gen2"] != "SI":
        raise ValueError(f"{consumidor}: {calc} cuenta_gen2={estado['cuenta_gen2']!r}")
    if estado["resultado_replay"] not in pines_mesa.veredictos_afirmativos_en_resultado():
        raise ValueError(f"{consumidor}: replay de {calc} = "
                         f"{estado['resultado_replay']!r}, no afirmativo en RESULTADO")
    spec = _yaml_load(carpeta / "spec.yaml")
    if pines_mesa._ingiere(spec) or not pines_mesa._tiene_crudo(spec):
        raise ValueError(f"{consumidor}: vía (i) exige insumo crudo sin ingestión")
    valor = json.loads((carpeta / "resultados.json").read_text())["resultados"].get(result)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
        raise ValueError(f"{consumidor}: {result}={valor!r} fuera de escala [0,1]")
    return float(valor)


def transform_procedencia_v4(source: str, regla: str, valores: list[float],
                             result: str) -> str:
    """Reescribe `valores:` de UNA entrada de asignados_probabilidad y añade
    la cita B4 debajo. Rechazo atómico si la entrada no es única o ya trae
    una cita distinta."""
    lineas = source.splitlines(keepends=True)
    hits = [i for i, l in enumerate(lineas) if l.rstrip("\n") == f"  - regla: {regla}"]
    if len(hits) != 1:
        raise ValueError(f"{regla}: se esperaba una entrada única, hay {len(hits)}")
    i = hits[0]
    fin = next((j for j in range(i + 1, len(lineas))
                if not lineas[j].startswith("    ")), len(lineas))
    bloque = range(i + 1, fin)
    if any("corrida0_" in lineas[j] for j in bloque):
        if any(f"corrida0_resultado_id: {result}" in lineas[j] for j in bloque):
            return source
        raise ValueError(f"{regla}: cita previa distinta; rechazo atómico")
    jv = [j for j in bloque if lineas[j].startswith("    valores: [")]
    if len(jv) != 1:
        raise ValueError(f"{regla}: `valores:` no único")
    viejos = _yaml_load_texto(lineas[jv[0]])["valores"]
    if len(viejos) != len(valores):
        raise ValueError(f"{regla}: cardinalidad {len(viejos)} != {len(valores)}")
    lineas[jv[0]] = (
        f"    valores: [{', '.join(f'{v:.6f}' for v in valores)}]\n"
        f"    corrida0_resultado_id: {result}\n"
        f"    corrida0_generacion: GEN2\n"
        f"    clase_respaldo: \"{CLASE_SEGURO}\"\n"
        f"    relevo_gen2: \"ACTO {ACTO_V4}: valores = RESULT de {CALC_SEGURO} "
        f"(antes ASIGNADO {viejos}); la cita es la de la primera categoría\"\n")
    return "".join(lineas)


def _yaml_load_texto(texto: str):
    import yaml  # noqa: PLC0415
    return yaml.safe_load(texto)


def transform_catalogo_v4(source: str, momento: str, fila_relevo: dict) -> str:
    """Añade al final del TSV las seis columnas de relevo (si faltan) y llena
    las de UN momento. Ninguna columna sellada se toca."""
    import csv  # noqa: PLC0415
    import io  # noqa: PLC0415
    lector = csv.DictReader(io.StringIO(source), delimiter="\t")
    cols = list(lector.fieldnames)
    filas = list(lector)
    nuevas = [c for c in COLUMNAS_CATALOGO_V4 if c not in cols]
    if nuevas and len(nuevas) != len(COLUMNAS_CATALOGO_V4):
        raise ValueError("catálogo con columnas de relevo parciales; rechazo atómico")
    cols += nuevas
    hits = [f for f in filas if f["id_momento"] == momento]
    if len(hits) != 1:
        raise ValueError(f"{momento}: se esperaba un momento único, hay {len(hits)}")
    previo = {c: (hits[0].get(c) or "") for c in COLUMNAS_CATALOGO_V4}
    if any(previo.values()):
        if previo == fila_relevo:
            return source
        raise ValueError(f"{momento}: cita previa distinta; rechazo atómico")
    hits[0].update(fila_relevo)
    salida = io.StringIO()
    w = csv.DictWriter(salida, fieldnames=cols, delimiter="\t",
                       lineterminator="\n", restval="")
    w.writeheader()
    w.writerows(filas)
    return salida.getvalue()


def relevo_consumidores_v4(apply_: bool = False) -> None:
    ctx = _ctx_corridas()
    cambios = []
    old_p = PROCEDENCIA.read_text(encoding="utf-8")
    nuevo_p = old_p
    for regla, results in RELEVOS_PROCEDENCIA_V4:
        consumidor = f"milpa/procedencia.yaml:asignados_probabilidad:{regla}"
        valores = [guardas_v4(consumidor, CALC_SEGURO, r, ctx) for r in results]
        if abs(sum(valores) - 1) > 1e-6:
            raise ValueError(f"{consumidor}: suma {sum(valores)!r} != 1")
        nuevo_p = transform_procedencia_v4(nuevo_p, regla, valores, results[0])
    # la entrada relevada carga como YAML y conserva cardinalidad
    cargado = {e["regla"]: e for e in _yaml_load_texto(nuevo_p)["asignados_probabilidad"]}
    for regla, results in RELEVOS_PROCEDENCIA_V4:
        if cargado[regla].get("corrida0_resultado_id") != results[0]:
            raise ValueError(f"{regla}: no cargó con su cita")
    cambios.append((PROCEDENCIA, old_p, nuevo_p))

    old_c = CATALOGO.read_text(encoding="utf-8")
    nuevo_c = old_c
    for momento, result, discrepancia in RELEVOS_CATALOGO_V4:
        consumidor = f"milpa/catalogo-momentos-v0_1.tsv:{momento}"
        valor = guardas_v4(consumidor, CALC_SEGURO, result, ctx)
        nuevo_c = transform_catalogo_v4(nuevo_c, momento, {
            "valor_gen2": repr(valor), "corrida0_resultado_id": result,
            "corrida0_generacion": "GEN2", "calc_gen2": CALC_SEGURO,
            "sello_gen2": sha(CORRIDAS_DIR / CALC_SEGURO / "sello.json"),
            "discrepancia_gen1": discrepancia})
    cambios.append((CATALOGO, old_c, nuevo_c))

    for ruta, viejo, nuevo in cambios:
        rel = ruta.relative_to(ROOT)
        diff = "".join(difflib.unified_diff(
            viejo.splitlines(keepends=True), nuevo.splitlines(keepends=True),
            fromfile=f"a/{rel}", tofile=f"b/{rel}"))
        print(diff or f"SIN-DIFF: {rel} ya aplicado")
        if apply_ and nuevo != viejo:
            with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=ruta.parent,
                    prefix=".relevo-consumo-", delete=False) as handle:
                temp = Path(handle.name)
                handle.write(nuevo)
            try:
                os.replace(temp, ruta)
            finally:
                temp.unlink(missing_ok=True)
            print(f"APLICADO: {rel}")


# ── V5 · ACTO GEN2-RELEVO-CONSUMIDORES-2 (ADENDA-1, P5) · motor B1/B2 ─────
# Firmas FIRMAS-16, verbatim (forense/firmas-pendientes.tsv, rama de #1137):
#   a157-01 «SÍ: `emitir_binaria` devuelve el par GEN2 medido donde conducta y
#   disparador coinciden; los ocho ASIGNADO se retiran; donde no coinciden, se
#   conserva con rótulo.»
#   a157-02 «SÍ: las cuatro conductas NO-ADOPTAR-NC-0107 salen del consumo
#   vivo (rol histórico, sin sortear).»
REGLA_UTIL = "tramite.gobierno_digital.util_sin_coercion"
REGLA_DISC = "tramite.mordida.discrecional"
REGLA_REG = "tramite.mordida.con_registro"
REGLA_EVA = "tramite.evasion_norma"

# (regla, ASIGNADO, hermano medido): coinciden conducta y disparador -> retira.
B1_RETIRA = (
    (REGLA_UTIL, "adopta", "adopta_encig2025_luz"),
    (REGLA_UTIL, "rechaza_servicio", "rechaza_servicio_encig2025_luz"),
)
_NO_COINCIDE_MORDIDA = ("el hermano medido es SOLICITUD (ENCIG P8_3) o proxy "
                        "descriptivo del grupo P8_4, no PAGO")
_NO_COINCIDE_EVASION = ("el RESULT es la CONJUNTA P(no denunció ∧ norma inútil); "
                        "la regla escribe la CONDICIONAL")
# (regla, ASIGNADO, razón): no coinciden -> se conserva con rótulo.
B1_CONSERVA = (
    (REGLA_DISC, "paga_mordida", _NO_COINCIDE_MORDIDA),
    (REGLA_DISC, "tramite_normal", _NO_COINCIDE_MORDIDA),
    (REGLA_REG, "tramite_normal", _NO_COINCIDE_MORDIDA),
    (REGLA_REG, "paga_mordida", _NO_COINCIDE_MORDIDA),
    (REGLA_EVA, "evade_norma", _NO_COINCIDE_EVASION),
    (REGLA_EVA, "cumple_norma", _NO_COINCIDE_EVASION),
)
B2_HISTORICO = (
    (REGLA_REG, "paga_mordida_encig2025_presencial"),
    (REGLA_REG, "tramite_normal_encig2025_presencial"),
    (REGLA_REG, "paga_mordida_encig2025_digital"),
    (REGLA_REG, "tramite_normal_encig2025_digital"),
)
ROTULO_B1 = "ASIGNADO-CONSERVADO-B1"
# Líneas que una M sellada cita por TEXTO EXACTO (M-TRA-M-01/02 vía
# tools/emite_m.py:cita_p; tests/test_emite_m_calibracion.py::test_regresion_p2_pasa):
# su rótulo va en un comentario propio encima, nunca en la línea.
CITADAS_POR_M_SELLADA = frozenset({(REGLA_DISC, "paga_mordida")})


def _calc_de_result(result: str) -> str:
    hits = [c.name for c in sorted(CORRIDAS_DIR.iterdir())
            if (c / "resultados.json").exists()
            and result in json.loads((c / "resultados.json").read_text())
            .get("resultados", {})]
    if len(hits) != 1:
        raise ValueError(f"{result}: se esperaba un CALC único, hay {hits}")
    return hits[0]


def guardas_b1(regla: dict, hermano: str, ctx: dict) -> dict:
    """El hermano medido ya cita un RESULT GEN2: CALC sellado, cuenta GEN2,
    replay afirmativo en RESULTADO y `p` = RESULT al grano de seis decimales.
    Devuelve la salida cruda del hermano."""
    import pines_mesa  # noqa: PLC0415
    s = [e for e in regla["entonces"] if e.get("conducta") == hermano]
    if len(s) != 1:
        raise ValueError(f"{regla['id']}:{hermano}: hermano no único")
    s = s[0]
    result = s.get("corrida0_resultado_id")
    if not result or s.get("corrida0_generacion") != "GEN2":
        raise ValueError(f"{regla['id']}:{hermano}: el hermano no cita GEN2")
    calc = _calc_de_result(result)
    carpeta = CORRIDAS_DIR / calc
    if not _sello_coincide(carpeta):
        raise ValueError(f"{hermano}: {calc} sello discordante")
    spec_id = calc.split("--")[0]
    estado = ctx.get(spec_id) or ctx.get(calc)
    if (estado is None or not str(estado["estado"]).startswith("SELLADA")
            or estado["cuenta_gen2"] != "SI"
            or estado["resultado_replay"] not in pines_mesa.veredictos_afirmativos_en_resultado()):
        raise ValueError(f"{hermano}: {calc} no pasa las guardas de 4.1 ({estado})")
    valor = json.loads((carpeta / "resultados.json").read_text())["resultados"][result]
    if f"{float(s['p']):.6f}" != f"{float(valor):.6f}":
        raise ValueError(f"{hermano}: p={s['p']} != {result}={valor}")
    return s


def _linea_flujo(lineas: list[str], regla_id: str, conducta: str) -> int:
    i = _ubica_conducta(lineas, regla_id, conducta)
    if not lineas[i].lstrip().startswith("- {"):
        raise ValueError(f"{regla_id}:{conducta}: se esperaba forma flujo")
    return i


def _anade_campos(linea: str, campos: str) -> str:
    codigo, sep, comentario = linea.rstrip("\n").partition("}  #")
    if sep:
        return f"{codigo}, {campos}}}  #{comentario}\n"
    cuerpo = linea.rstrip("\n")
    if not cuerpo.endswith("}"):
        raise ValueError(f"línea sin cierre de flujo: {cuerpo[:60]!r}")
    return f"{cuerpo[:-1]}, {campos}}}\n"


def transform_motor_v5(source: str, ctx: dict) -> str:
    reglas = {r["id"]: r for r in _yaml_load_texto(source)["reglas"]}
    lineas = source.splitlines(keepends=True)
    for regla_id, asignado, hermano in B1_RETIRA:
        i = _linea_flujo(lineas, regla_id, asignado)
        if "corrida0_" in lineas[i]:
            if f"B1 (FIRMAS-16): par GEN2 de {hermano}" in lineas[i]:
                continue
            raise ValueError(f"{regla_id}:{asignado}: cita previa distinta; rechazo atómico")
        viejo = next(e for e in reglas[regla_id]["entonces"] if e["conducta"] == asignado)
        if viejo.get("clase") != "ASIGNADO":
            raise ValueError(f"{regla_id}:{asignado}: no es ASIGNADO")
        s = guardas_b1(reglas[regla_id], hermano, ctx)
        clase = json.dumps(s["clase"], ensure_ascii=False)
        lineas[i] = (
            f"      - {{conducta: {asignado}, p: {float(s['p']):.6f}, clase: {clase}, "
            f"corrida0_resultado_id: {s['corrida0_resultado_id']}, corrida0_generacion: GEN2}}"
            f"  # B1 (FIRMAS-16): par GEN2 de {hermano}; conducta y disparador coinciden "
            f"(el universo impone sin coerción ni riesgo fiscal, firma a1). Retirado el "
            f"ASIGNADO p={viejo['p']} (ACTO {ACTO_V4}).\n")
    for regla_id, asignado, razon in B1_CONSERVA:
        i = _linea_flujo(lineas, regla_id, asignado)
        previa = lineas[i - 1].lstrip()
        if ROTULO_B1 in lineas[i] or (previa.startswith("#") and ROTULO_B1 in previa):
            continue
        if "uso_motor:" in lineas[i].split("}  #", 1)[0]:
            raise ValueError(f"{regla_id}:{asignado}: ya trae uso_motor; rechazo atómico")
        rotulo = json.dumps(f"{ROTULO_B1} (FIRMAS-16): no coinciden conducta y "
                            f"disparador -- {razon}; estimando a re-especificar en CAJA",
                            ensure_ascii=False)
        if (regla_id, asignado) in CITADAS_POR_M_SELLADA:
            lineas.insert(i, f"      # {json.loads(rotulo)} -- rótulo fuera de la "
                             f"línea: M-TRA-M-01/02 la citan por texto exacto.\n")
            continue
        lineas[i] = _anade_campos(lineas[i], f"uso_motor: {rotulo}")
    for regla_id, conducta in B2_HISTORICO:
        i = _linea_flujo(lineas, regla_id, conducta)
        codigo = lineas[i].split("}  #", 1)[0]
        if "rol_uso: historico" in codigo:
            continue
        if "rol_uso:" in codigo or "NO-ADOPTAR-NC-0107" not in codigo:
            raise ValueError(f"{regla_id}:{conducta}: no es NO-ADOPTAR-NC-0107 sin rol")
        lineas[i] = _anade_campos(lineas[i], "rol_uso: historico")
    return "".join(lineas)


def relevo_motor_v5(apply_: bool = False) -> None:
    old = TARGET.read_text(encoding="utf-8")
    nuevo = transform_motor_v5(old, _ctx_corridas())
    from milpa.src import emisor  # noqa: PLC0415
    with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".yaml", delete=False) as fh:
        fh.write(nuevo)
        ruta_tmp = Path(fh.name)
    try:
        cargadas = {r.id: r for r in emisor.cargar_reglas(ruta_tmp)}
    finally:
        ruta_tmp.unlink(missing_ok=True)
    for regla_id, asignado, hermano in B1_RETIRA:
        a = emisor.emitir_binaria(cargadas[regla_id], asignado)
        h = emisor.emitir_binaria(cargadas[regla_id], hermano)
        if a.estado == "NO-EMITE" or a.valor_punto != h.valor_punto or a.resultado_id != h.resultado_id:
            raise ValueError(f"{regla_id}:{asignado}: no devuelve el par GEN2 de {hermano}")
    for regla_id, conducta in B2_HISTORICO:
        if emisor.emitir_binaria(cargadas[regla_id], conducta).estado != "NO-EMITE":
            raise ValueError(f"{regla_id}:{conducta}: sigue emitiendo")
    diff = "".join(difflib.unified_diff(
        old.splitlines(keepends=True), nuevo.splitlines(keepends=True),
        fromfile="a/milpa/tramite.yaml", tofile="b/milpa/tramite.yaml"))
    print(diff or "SIN-DIFF: ya aplicado")
    if apply_ and nuevo != old:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=TARGET.parent,
                prefix=".relevo-consumo-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(nuevo)
        try:
            os.replace(temp, TARGET)
        finally:
            temp.unlink(missing_ok=True)
        print(f"APLICADO: B1 retira {len(B1_RETIRA)}, conserva {len(B1_CONSERVA)} "
              f"con rótulo; B2 {len(B2_HISTORICO)} a rol histórico")


# ── V6 · ACTO GEN2-RELEVO-CONSUMIDORES-3 · FIRMAS-18 H1/H2 ───────────────
# Firmas verbatim (forense/firmas-pendientes.tsv, FP e760-01/02, FIRMADA 25/sep/2026):
#   H1 «Mesa declara HISTÓRICO-SIN-RELEVO las 8 entradas asignados_coeficiente de
#   milpa/procedencia.yaml; las 12 asignados_probabilidad siguen la regla de
#   FIRMAS-16 B1/B2; ejecuta RELEVO-CONSUMIDORES-3.»
#   H2 «Para M01–M07 y M23 rige la regla de M08: acotar a la unidad medida donde
#   el cotejo sea PARCIAL; HISTÓRICO-SIN-RELEVO donde sea NO-EQUIVALENTE;
#   ejecuta RELEVO-CONSUMIDORES-3.»
# H3 (marco) no escribe archivo: el contador lo lee por tipo_uso (tools/corrida0.py).
ACTO_V6 = "GEN2-RELEVO-CONSUMIDORES-3"
HISTORICO = "HISTÓRICO-SIN-RELEVO"
FIRMA_H1 = "H1 (FIRMAS-18, FP e760-01, 25/sep/2026)"
FIRMA_H2 = "H2 (FIRMAS-18, FP e760-02, 25/sep/2026)"
H1_COEFICIENTES = (
    ("G2", "sens_estatus"), ("G2", "aversion_riesgo"), ("G3", "aversion_riesgo"),
    ("G4", "horizonte_temporal"), ("G4", "sens_estatus"),
    ("G5", "familismo_obligacion"), ("G5", "radio_confianza"), ("G6", "deferencia"),
)
# B1 aplicado a procedencia: par GEN2 con conducta y disparador coincidentes
# (el mismo que FIRMAS-16 a157-01 ya reconoció en tramite.yaml).
# (regla, RESULT de la primera categoría -vía (i)-, RESULT del complemento -vía (iii)-)
H1_CITA = (
    ("tramite.gobierno_digital.util_sin_coercion",
     "RESULT-ENCIG-MOR-C-P-ADOPTA", "RESULT-ENCIGDER-C-Q"),
)
CLASE_UTIL = ("MEDIDO·p(tasa base ponderada, universo que impone sin coerción ni "
              "riesgo fiscal: pago digital de luz, ENCIG 2025; unidad persona)")
_SIN_HERMANO = "tramite.yaml no tiene regla hermana medida"
# B1 «donde no coinciden, se conserva con rótulo»: siguen contando como legacy.
H1_CONSERVA = (
    ("dinero.ahorro.informal_sin_puente", _SIN_HERMANO),
    ("dinero.ahorro.con_puente_y_respaldo", _SIN_HERMANO),
    ("dinero.planeacion.formal_estable",
     "el hermano GEN2 (ENFIH 2019, RESULT-ENFIH-A-P) es tasa base; la condicional "
     "de formalidad no es construible (disparadores_estado) -- no coincide el disparador"),
    ("dinero.credito.scoring_alternativo", _SIN_HERMANO),
    ("dinero.consumo.estatus_mediado_por_credito", _SIN_HERMANO),
    ("salud.atencion.leve_sin_imss", _SIN_HERMANO),
    ("salud.atencion.grave", _SIN_HERMANO),
    ("salud.prevencion.hombre_sin_permiso", _SIN_HERMANO),
    ("tramite.mordida.discrecional", _NO_COINCIDE_MORDIDA),
    ("tramite.mordida.con_registro", _NO_COINCIDE_MORDIDA),
    ("tramite.gobierno_digital.coercitivo",
     "sin conducta GEN2 medida en tramite.yaml (las dos son ASIGNADO)"),
)
ROTULO_H1 = "ASIGNADO-CONSERVADO-H1"
COLUMNA_ESTADO = "estado_relevo"
# H2, momento por momento (PROPUESTO-POR-EJECUTOR; fuente:
# forense/analisis/astra4-relevo/cotejo-documental-catalogo.md).
H2_HISTORICO = (
    ("M01", "NO-EQUIVALENTE-PAGO (ENCIG P8_3 registra solicitud, no pago)"),
    ("M02", "NO-EQUIVALENTE-PAGO (P8_3/P8_4 no identifica pago normal con registro)"),
    ("M06", "INSTRUMENTO SIN IDENTIDAD, leído como NO-EQUIVALENTE: ENIGH 2022 no "
            "coobserva puente, respaldo y adopción"),
    ("M07", "NO-EQUIVALENTE (proporción persona sin cruce de scoring, CAT y mora)"),
)
# (momento, RESULT vía (i), discrepancia_gen1)
H2_ACOTA = (
    ("M04", "RESULT-ENCIG-MOR-C-P-ADOPTA",
     "NO-REPRODUCE-GEN1: acotado a la unidad medida -- adopción de pago digital de luz, "
     "ENCIG 2025, persona en universo sin coerción ni riesgo fiscal (firma a1), no "
     "registro PERSONA ENIGH 2022; firma H2 (cotejo PARCIAL)"),
)


def _escribe(ruta: Path, viejo: str, nuevo: str, apply_: bool) -> None:
    rel = ruta.relative_to(ROOT)
    diff = "".join(difflib.unified_diff(
        viejo.splitlines(keepends=True), nuevo.splitlines(keepends=True),
        fromfile=f"a/{rel}", tofile=f"b/{rel}"))
    print(diff or f"SIN-DIFF: {rel} ya aplicado")
    if apply_ and nuevo != viejo:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=ruta.parent,
                prefix=".relevo-consumo-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(nuevo)
        try:
            os.replace(temp, ruta)
        finally:
            temp.unlink(missing_ok=True)
        print(f"APLICADO: {rel}")


def guarda_complemento_v6(consumidor: str, result: str, ctx: dict) -> float:
    """Vía (iii): el complemento ingiere un RESULT GEN2; se exige CALC sellado
    y coincidente, cuenta GEN2 y replay afirmativo en RESULTADO."""
    import pines_mesa  # noqa: PLC0415
    calc = _calc_de_result(result)
    carpeta = CORRIDAS_DIR / calc
    estado = ctx.get(calc) or ctx.get(calc.split("--")[0])
    if (not _sello_coincide(carpeta) or estado is None
            or not str(estado["estado"]).startswith("SELLADA")
            or estado["cuenta_gen2"] != "SI"
            or estado["resultado_replay"] not in pines_mesa.veredictos_afirmativos_en_resultado()):
        raise ValueError(f"{consumidor}: {calc} no pasa las guardas ({estado})")
    valor = json.loads((carpeta / "resultados.json").read_text())["resultados"][result]
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
        raise ValueError(f"{consumidor}: {result}={valor!r} fuera de escala [0,1]")
    return float(valor)


def _bloque_regla(lineas: list[str], regla: str) -> tuple[int, int]:
    hits = [i for i, l in enumerate(lineas) if l.rstrip("\n") == f"  - regla: {regla}"]
    if len(hits) != 1:
        raise ValueError(f"{regla}: se esperaba una entrada única, hay {len(hits)}")
    i = hits[0]
    fin = next((j for j in range(i + 1, len(lineas))
                if not lineas[j].startswith("    ")), len(lineas))
    return i, fin


def transform_procedencia_v6(source: str, ctx: dict) -> str:
    lineas = source.splitlines(keepends=True)
    # H1 · coeficientes: marca por fila dentro de su línea `detalle`.
    por_gen: dict[str, list[str]] = {}
    for gen, coef in H1_COEFICIENTES:
        por_gen.setdefault(gen, []).append(coef)
    for gen, coefs in por_gen.items():
        hits = [i for i, l in enumerate(lineas)
                if l.lstrip().startswith(f"- {{gen: {gen}, coefs: {{")]
        if len(hits) != 1:
            raise ValueError(f"{gen}: línea `detalle` no única ({len(hits)})")
        i = hits[0]
        codigo = lineas[i].split("}  #", 1)[0]
        detalle = _yaml_load_texto(lineas[i].split("#", 1)[0].strip()[2:])
        for coef in coefs:
            if coef not in detalle["coefs"]:
                raise ValueError(f"{gen}.{coef}: no está en `detalle`")
        marca = {c: f"{HISTORICO} · {FIRMA_H1}; valor conservado, no cuenta como deuda"
                 for c in sorted(coefs)}
        if "historico_sin_relevo:" in codigo:
            if detalle.get("historico_sin_relevo") == marca:
                continue
            raise ValueError(f"{gen}: marca previa distinta; rechazo atómico")
        campos = "historico_sin_relevo: {" + ", ".join(
            f"{c}: {json.dumps(v, ensure_ascii=False)}" for c, v in marca.items()) + "}"
        lineas[i] = _anade_campos(lineas[i], campos)
    # H1 · probabilidades con par GEN2 coincidente: cita.
    for regla, r_p, r_q in H1_CITA:
        consumidor = f"milpa/procedencia.yaml:asignados_probabilidad:{regla}"
        p = guardas_v4(consumidor, _calc_de_result(r_p), r_p, ctx)
        q = guarda_complemento_v6(consumidor, r_q, ctx)
        if abs(p + q - 1) > 1e-6:
            raise ValueError(f"{consumidor}: suma {p + q!r} != 1")
        i, fin = _bloque_regla(lineas, regla)
        bloque = range(i + 1, fin)
        if any("corrida0_" in lineas[j] for j in bloque):
            if any(f"corrida0_resultado_id: {r_p}" in lineas[j] for j in bloque):
                continue
            raise ValueError(f"{regla}: cita previa distinta; rechazo atómico")
        jv = [j for j in bloque if lineas[j].startswith("    valores: [")]
        if len(jv) != 1:
            raise ValueError(f"{regla}: `valores:` no único")
        viejos = _yaml_load_texto(lineas[jv[0]])["valores"]
        if len(viejos) != 2:
            raise ValueError(f"{regla}: cardinalidad {len(viejos)} != 2")
        lineas[jv[0]] = (
            f"    valores: [{p:.6f}, {q:.6f}]\n"
            f"    corrida0_resultado_id: {r_p}\n"
            f"    corrida0_generacion: GEN2\n"
            f"    clase_respaldo: \"{CLASE_UTIL}\"\n"
            f"    relevo_gen2: \"ACTO {ACTO_V6} · {FIRMA_H1}, regla B1: valores = {r_p} "
            f"y su complemento {r_q} (antes ASIGNADO {viejos}); la cita es la de la "
            f"primera categoría\"\n")
    # H1 · probabilidades sin par coincidente: se conservan con rótulo.
    for regla, razon in H1_CONSERVA:
        i, fin = _bloque_regla(lineas, regla)
        bloque = range(i + 1, fin)
        if any(lineas[j].startswith("    rotulo_relevo:") for j in bloque):
            if any(ROTULO_H1 in lineas[j] for j in bloque):
                continue
            raise ValueError(f"{regla}: rótulo previo distinto; rechazo atómico")
        if any("corrida0_" in lineas[j] for j in bloque):
            raise ValueError(f"{regla}: ya cita un RESULT; no se conserva")
        texto = (f"{ROTULO_H1} · {FIRMA_H1}, regla B1: no hay par GEN2 con conducta y "
                 f"disparador coincidentes -- {razon}; sigue legacy")
        lineas.insert(i + 1, f"    rotulo_relevo: {json.dumps(texto, ensure_ascii=False)}\n")
    return "".join(lineas)


def transform_catalogo_v6(source: str, ctx: dict) -> str:
    import csv  # noqa: PLC0415
    import io  # noqa: PLC0415
    lector = csv.DictReader(io.StringIO(source), delimiter="\t")
    cols = list(lector.fieldnames)
    filas = {f["id_momento"]: f for f in lector}
    if any(c not in cols for c in COLUMNAS_CATALOGO_V4):
        raise ValueError("catálogo sin las seis columnas de relevo (V4)")
    if COLUMNA_ESTADO not in cols:
        cols.append(COLUMNA_ESTADO)
    objetivo: dict[str, dict] = {}
    for m, razon in H2_HISTORICO:
        objetivo[m] = {COLUMNA_ESTADO: f"{HISTORICO} · {FIRMA_H2}: {razon}"}
    for m, result, discrepancia in H2_ACOTA:
        calc = _calc_de_result(result)
        valor = guardas_v4(f"milpa/catalogo-momentos-v0_1.tsv:{m}", calc, result, ctx)
        objetivo[m] = {"valor_gen2": repr(valor), "corrida0_resultado_id": result,
                       "corrida0_generacion": "GEN2", "calc_gen2": calc,
                       "sello_gen2": sha(CORRIDAS_DIR / calc / "sello.json"),
                       "discrepancia_gen1": discrepancia,
                       COLUMNA_ESTADO: f"ACOTADO-A-UNIDAD-MEDIDA · {FIRMA_H2}: cotejo PARCIAL"}
    for m, campos in objetivo.items():
        if m not in filas:
            raise ValueError(f"{m}: momento ausente")
        previo = {c: (filas[m].get(c) or "") for c in (*COLUMNAS_CATALOGO_V4, COLUMNA_ESTADO)}
        destino = {c: campos.get(c, "") for c in previo}
        if any(previo.values()) and previo != destino:
            raise ValueError(f"{m}: relevo previo distinto; rechazo atómico")
        filas[m].update(destino)
    salida = io.StringIO()
    w = csv.DictWriter(salida, fieldnames=cols, delimiter="\t",
                       lineterminator="\n", restval="")
    w.writeheader()
    w.writerows(filas.values())
    return salida.getvalue()


def relevo_consumidores_v6(apply_: bool = False) -> None:
    ctx = _ctx_corridas()
    viejo_p = PROCEDENCIA.read_text(encoding="utf-8")
    nuevo_p = transform_procedencia_v6(viejo_p, ctx)
    cargado = _yaml_load_texto(nuevo_p)
    marcados = {(d["gen"], c) for d in cargado["asignados_coeficiente"]["detalle"]
                for c in (d.get("historico_sin_relevo") or {})}
    if marcados != set(H1_COEFICIENTES):
        raise ValueError(f"H1: marcados {sorted(marcados)} != firma")
    viejo_c = CATALOGO.read_text(encoding="utf-8")
    nuevo_c = transform_catalogo_v6(viejo_c, ctx)
    _escribe(PROCEDENCIA, viejo_p, nuevo_p, apply_)
    _escribe(CATALOGO, viejo_c, nuevo_c, apply_)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--crear-desde-propuesta", action="store_true",
        help="modo V2: crea en milpa/tramite.yaml las reglas de "
             "IDS_CREAR_DESDE_PROPUESTA copiando verbatim los campos "
             "medidos de milpa/tramite-ola5-propuesta-v0.yaml y los "
             "campos redactados de forense/analisis/adopcion-4/"
             "redaccion-reglas-v1_0.yaml. Por defecto imprime el diff seco.")
    parser.add_argument(
        "--relevo-motor-34", action="store_true",
        help="modo V3 (ACTO GEN2-RELEVO-MOTOR-34-1): cita en milpa/tramite.yaml "
             "los RESULT sellados de RELEVOS_V3 tras las guardas de 4.1. Por "
             "defecto imprime el diff seco.")
    parser.add_argument(
        "--relevo-consumidores-2", action="store_true",
        help="modo V4 (ACTO GEN2-RELEVO-CONSUMIDORES-2): cita B4 en "
             "milpa/procedencia.yaml y columnas de relevo en el catálogo de "
             "momentos. Por defecto imprime el diff seco.")
    parser.add_argument(
        "--motor-b1-b2", action="store_true",
        help="modo V5 (ACTO GEN2-RELEVO-CONSUMIDORES-2, ADENDA-1): FIRMAS-16 "
             "B1 y B2 sobre milpa/tramite.yaml. Por defecto imprime el diff seco.")
    parser.add_argument(
        "--relevo-consumidores-3", action="store_true",
        help="modo V6 (ACTO GEN2-RELEVO-CONSUMIDORES-3): FIRMAS-18 H1 y H2 sobre "
             "milpa/procedencia.yaml y el catálogo de momentos. Por defecto "
             "imprime el diff seco.")
    args = parser.parse_args()
    if args.relevo_consumidores_3:
        relevo_consumidores_v6(apply_=args.apply)
        return
    if args.motor_b1_b2:
        relevo_motor_v5(apply_=args.apply)
        return
    if args.relevo_consumidores_2:
        relevo_consumidores_v4(apply_=args.apply)
        return
    if args.relevo_motor_34:
        relevo_motor_v3(apply_=args.apply)
        return
    if args.crear_desde_propuesta:
        crear_desde_propuesta(apply_=args.apply)
        return
    old = TARGET.read_text()
    if transform(old, OLD_P) == old:
        print("SIN-DIFF: ya aplicado")
        return
    if sha(TARGET) != EXPECTED_TARGET_SHA:
        raise ValueError("hash previo del consumidor cambió; revisar antes de aplicar")
    rendered = evidence()
    new = transform(old, rendered)
    if new == old:
        print("SIN-DIFF: ya aplicado")
        return
    diff = "".join(difflib.unified_diff(old.splitlines(keepends=True),
                                        new.splitlines(keepends=True),
                                        fromfile="a/milpa/tramite.yaml",
                                        tofile="b/milpa/tramite.yaml"))
    print(diff)
    if args.apply:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=TARGET.parent,
            prefix=".relevo-consumo-", delete=False,
        ) as handle:
            temp = Path(handle.name)
            handle.write(new)
        try:
            os.replace(temp, TARGET)
        finally:
            temp.unlink(missing_ok=True)
        print("APLICADO: una conducta, mismo p a seis decimales, cita GEN2")


if __name__ == "__main__":
    main()
