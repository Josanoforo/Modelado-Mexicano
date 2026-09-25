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
    args = parser.parse_args()
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
