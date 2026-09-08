"""Pruebas dirigidas de `tools/rutinas.py` -- los 6 casos de "Validación y
cierre" de `forense/encargos/2026-09-08-RUTINAS-2-COORDINACION-Y-REVISION.md`.

Sin red, sin PR, sin cálculo: funciones puras sobre fixtures fabricados.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import rutinas  # noqa: E402


HEAD1 = "a" * 40
HEAD2 = "b" * 40
MAIN1 = "c" * 40
MAIN2 = "d" * 40


# ───────────────────────────────────────────────────────────────
# Caso 1 · mismo PR/HEAD/main/cuerpo no duplica; HEAD o cuerpo cambian
# -> pendiente; main cambia -> resultado anterior no es revisión de la
# nueva combinación.
# ───────────────────────────────────────────────────────────────

def test_caso1_misma_identidad_no_duplica():
    body_sha = rutinas.body_sha256("cuerpo del PR")
    marca = rutinas.parsea_marca_revisa(
        rutinas.construye_marca_revisa(42, HEAD1, MAIN1, body_sha))
    actual = rutinas.IdentidadRevision(pr=42, head=HEAD1, main=MAIN1, body_sha256=body_sha)
    vigente, razon = rutinas.revision_esta_vigente(actual, marca)
    assert vigente is True
    assert "misma identidad" in razon


def test_caso1_head_cambia_pendiente():
    body_sha = rutinas.body_sha256("cuerpo del PR")
    marca = rutinas.parsea_marca_revisa(
        rutinas.construye_marca_revisa(42, HEAD1, MAIN1, body_sha))
    actual = rutinas.IdentidadRevision(pr=42, head=HEAD2, main=MAIN1, body_sha256=body_sha)
    vigente, razon = rutinas.revision_esta_vigente(actual, marca)
    assert vigente is False
    assert razon == "head cambio"


def test_caso1_cuerpo_cambia_pendiente():
    body_sha1 = rutinas.body_sha256("cuerpo v1")
    body_sha2 = rutinas.body_sha256("cuerpo v2, alcance distinto")
    marca = rutinas.parsea_marca_revisa(
        rutinas.construye_marca_revisa(42, HEAD1, MAIN1, body_sha1))
    actual = rutinas.IdentidadRevision(pr=42, head=HEAD1, main=MAIN1, body_sha256=body_sha2)
    vigente, razon = rutinas.revision_esta_vigente(actual, marca)
    assert vigente is False
    assert razon == "cuerpo cambio"


def test_caso1_main_cambia_no_es_revision_de_la_nueva_combinacion():
    body_sha = rutinas.body_sha256("cuerpo del PR")
    marca = rutinas.parsea_marca_revisa(
        rutinas.construye_marca_revisa(42, HEAD1, MAIN1, body_sha))
    actual = rutinas.IdentidadRevision(pr=42, head=HEAD1, main=MAIN2, body_sha256=body_sha)
    vigente, razon = rutinas.revision_esta_vigente(actual, marca)
    assert vigente is False
    assert razon == "main cambio"


def test_caso1_body_sha_normaliza_crlf_y_espacios():
    a = rutinas.body_sha256("texto\r\ncon crlf\r\n")
    b = rutinas.body_sha256("  texto\ncon crlf\n  ")
    assert a == b


def test_caso1_marca_sin_marca_previa_no_vigente():
    body_sha = rutinas.body_sha256("cuerpo")
    actual = rutinas.IdentidadRevision(pr=42, head=HEAD1, main=MAIN1, body_sha256=body_sha)
    vigente, razon = rutinas.revision_esta_vigente(actual, None)
    assert vigente is False
    assert razon == "sin marca previa"


# ───────────────────────────────────────────────────────────────
# Caso 2 · un PR administrativo más reciente no impide seleccionar otro
# elegible; PR fusionado durante revisión no genera post-hoc automático
# (esto último es de runbook, no de función pura -- se prueba la
# selección).
# ───────────────────────────────────────────────────────────────

def test_caso2_selecciona_pendiente_mas_antiguo_ignorando_administrativos():
    candidatos = [
        rutinas.CandidatoPR(1, "[TRAMITE] digesto 2026-09-08", False, "2026-09-08T00:00:00Z", False),
        rutinas.CandidatoPR(2, "Arregla motor X", False, "2026-09-05T00:00:00Z", False),
        rutinas.CandidatoPR(3, "Arregla motor Y", False, "2026-09-06T00:00:00Z", False),
    ]
    elegido = rutinas.elige_pendiente_mas_antiguo(candidatos)
    assert elegido is not None
    assert elegido.numero == 2  # el más antiguo de los NO administrativos


def test_caso2_borrador_excluido():
    candidatos = [
        rutinas.CandidatoPR(4, "Trabajo en progreso", True, "2026-09-01T00:00:00Z", False),
        rutinas.CandidatoPR(5, "Listo para revisar", False, "2026-09-05T00:00:00Z", False),
    ]
    elegido = rutinas.elige_pendiente_mas_antiguo(candidatos)
    assert elegido.numero == 5


def test_caso2_sin_candidato_nada_que_revisar():
    candidatos = [
        rutinas.CandidatoPR(6, "[REVISA] post-hoc #1", False, "2026-09-01T00:00:00Z", False),
        rutinas.CandidatoPR(7, "Ya revisado", False, "2026-09-01T00:00:00Z", True),
    ]
    assert rutinas.elige_pendiente_mas_antiguo(candidatos) is None


def test_caso2_ordena_por_antiguedad_del_pr_no_del_comentario():
    # El PR 8 es más viejo que el 9 aunque en un escenario real su último
    # comentario sea más reciente -- esta función no ve comentarios, solo
    # `creado_en`, que es exactamente la garantía que P1 pide.
    candidatos = [
        rutinas.CandidatoPR(8, "Motor: ajuste A", False, "2026-09-01T00:00:00Z", False),
        rutinas.CandidatoPR(9, "Motor: ajuste B", False, "2026-09-07T00:00:00Z", False),
    ]
    elegido = rutinas.elige_pendiente_mas_antiguo(candidatos)
    assert elegido.numero == 8


# ───────────────────────────────────────────────────────────────
# Caso 3 · rama de nota o trámite dentro de perímetro no cierra el
# candado; la misma rama con cambios ejecutables sí lo cierra. Acto
# manual activo y rama desconocida no se eximen.
# ───────────────────────────────────────────────────────────────

def test_caso3_tramite_dentro_de_perimetro_no_bloquea():
    v = rutinas.clasifica_rama_para_candado(
        "claude/tramite-2026-09-08", False,
        ["forense/digesto/DIGESTO-2026-09-08.md", "forense/rutinas.tsv"])
    assert v.exenta is True


def test_caso3_tramite_con_cambio_ejecutable_bloquea():
    v = rutinas.clasifica_rama_para_candado(
        "claude/tramite-2026-09-08", False,
        ["forense/digesto/DIGESTO-2026-09-08.md", "motor/calculo.py"])
    assert v.exenta is False
    assert "motor/calculo.py" in v.razon


def test_caso3_revisa_solo_nota_no_bloquea():
    v = rutinas.clasifica_rama_para_candado(
        "claude/revisa-post-hoc-3", False,
        ["forense/notas/2026-09-08-revisa-rotulo.md"])
    assert v.exenta is True


def test_caso3_revisa_con_cambio_fuera_de_notas_bloquea():
    v = rutinas.clasifica_rama_para_candado(
        "claude/revisa-post-hoc-3", False,
        ["forense/notas/2026-09-08-revisa-rotulo.md", "canon/gobernanza-v1_15.md"])
    assert v.exenta is False


def test_caso3_rama_desconocida_no_se_exime():
    v = rutinas.clasifica_rama_para_candado(
        "claude/lo-que-sea", False, ["forense/algo.md"])
    assert v.exenta is False
    assert "no eximida" in v.razon


def test_caso3_rama_ya_contenida_en_main_no_bloquea():
    v = rutinas.clasifica_rama_para_candado(
        "claude/lo-que-sea", True, ["motor/calculo.py"])
    assert v.exenta is True


def test_caso3_censo_no_se_exime_por_analogia():
    # [CENSO] no está en la tabla de exenciones -- ni por nombre de rama
    # ni por título se clasifica como tramite/revisa, así que cae al
    # "sin clasificación verificable".
    v = rutinas.clasifica_rama_para_candado(
        "claude/censo-2026-09-08", False, ["forense/censo-raiz/hoy.txt"],
        titulo_pr="[CENSO] barrido diario")
    assert v.exenta is False


# ───────────────────────────────────────────────────────────────
# Caso 4 · PR de trámite existente de ayer se reutiliza; PR fusionado
# abre un ciclo nuevo; dos candidatos no producen un tercero; un push
# rechazado no dispara force-push ni borra huellas (esto último es de
# runbook -- probado por ausencia de cualquier función de "force" en el
# módulo).
# ───────────────────────────────────────────────────────────────

def test_caso4_pr_existente_de_ayer_se_reutiliza():
    pr_ayer = rutinas.PRTramite(100, "claude/tramite-2026-09-07", "open", "[TRAMITE] digesto 2026-09-07")
    accion, pr = rutinas.decide_pr_tramite([pr_ayer])
    assert accion == "REUSA"
    assert pr.numero == 100
    assert pr.rama == "claude/tramite-2026-09-07"


def test_caso4_pr_fusionado_abre_ciclo_nuevo():
    pr_cerrado = rutinas.PRTramite(99, "claude/tramite-2026-09-06", "merged", "[TRAMITE] digesto 2026-09-06")
    accion, pr = rutinas.decide_pr_tramite([pr_cerrado])
    assert accion == "CREA"
    assert pr is None


def test_caso4_dos_candidatos_no_producen_un_tercero():
    p1 = rutinas.PRTramite(100, "claude/tramite-2026-09-07", "open", "[TRAMITE] digesto 2026-09-07")
    p2 = rutinas.PRTramite(101, "claude/tramite-2026-09-08-b", "open", "[TRAMITE] digesto 2026-09-08")
    accion, pr = rutinas.decide_pr_tramite([p1, p2])
    assert accion == "DUPLICADO"
    assert pr is None


def test_caso4_ninguno_abierto_crea():
    accion, pr = rutinas.decide_pr_tramite([])
    assert accion == "CREA"
    assert pr is None


def test_module_no_expone_force_push():
    # Guardrail negativo, mecánico: el helper compartido no ofrece ningún
    # atajo de "force" -- si alguien lo añade, esta prueba lo atrapa.
    fuente = open(os.path.join(os.path.dirname(__file__), "..", "tools", "rutinas.py"),
                  encoding="utf-8").read()
    assert "force" not in fuente.lower()


# ───────────────────────────────────────────────────────────────
# Caso 5 · comentario de Revisa presente en la fuente GitHub aparece como
# actividad; API ausente se declara como falta de verificación, no como
# cero revisiones.
# ───────────────────────────────────────────────────────────────

def test_caso5_marca_reconocida_como_actividad():
    body_sha = rutinas.body_sha256("cuerpo")
    comentario = rutinas.construye_marca_revisa(7, HEAD1, MAIN1, body_sha) + \
        "\n\nVEREDICTO: FUSIONABLE-CON-RESERVA"
    marca = rutinas.parsea_marca_revisa(comentario)
    assert marca is not None
    assert marca["pr"] == 7


def test_caso5_comentario_sin_marca_no_es_actividad_reconocida():
    # Un comentario real puede existir sin la marca (previo a este acto,
    # o de otra rutina); no se presume vigencia, pero tampoco se descarta
    # como "cero" -- eso lo decide el llamador con GITHUB-NO-VERIFICADO,
    # esta función solo dice que no hay marca que parsear.
    assert rutinas.parsea_marca_revisa("comentario cualquiera, sin marca") is None


# ───────────────────────────────────────────────────────────────
# Caso 6 · ejemplo histórico cuyo estado cambió después se conserva y no
# se trata como afirmación vigente; las referencias nuevas de observación
# son legibles y no rompen el esquema (probado indirectamente: el TSV de
# 4 columnas sigue siendo TSV de 4 columnas con las nuevas huellas).
# ───────────────────────────────────────────────────────────────

def test_caso6_traduccion_no_reescribe_verbos_no_mapeados():
    # Un verbo histórico que no está en la tabla de traducción se
    # conserva tal cual -- P4 dice "normalizar únicamente las nuevas
    # huellas, sin corregir filas antiguas".
    assert rutinas.traduce_resultado_rutina("tramite", "ALGO-VIEJO-NO-MAPEADO") == "ALGO-VIEJO-NO-MAPEADO"


def test_caso6_traduccion_tramite_abrio_a_hizo():
    assert rutinas.traduce_resultado_rutina("tramite", "ABRIO", detalle_pr="123") == "HIZO:123"


def test_caso6_traduccion_revisa_comento_a_hizo():
    assert rutinas.traduce_resultado_rutina("revisa", "COMENTO", detalle_pr="45") == "HIZO:45"


def test_caso6_traduccion_despacha_cola_vacia_a_nada_que_hacer():
    assert rutinas.traduce_resultado_rutina("despacha", "COLA-VACIA") == "NADA-QUE-HACER"


def test_caso6_candado_paro_promovio_conservan_significado():
    for verbo in ("CANDADO", "PARO", "PROMOVIO"):
        assert rutinas.traduce_resultado_rutina("despacha", verbo) == verbo


def test_caso6_rutinas_tsv_conserva_todas_las_filas_historicas():
    ruta = os.path.join(os.path.dirname(__file__), "..", "forense", "rutinas.tsv")
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l for l in fh if l.strip() and not l.startswith("#")]
    # cabecera + al menos las filas que ya existían antes de este acto
    # (3 filas de datos + 1 cabecera, medido 8/sep/2026 antes de este acto)
    assert len(lineas) >= 4, "no se perdieron filas históricas del TSV"
    cabecera = lineas[0].rstrip("\n").split("\t")
    assert len(cabecera) == 4, "el esquema sigue siendo de 4 columnas"


# ───────────────────────────────────────────────────────────────
# Arnés -- mismo patrón que `tests/test_digesto_nc.py`: `corre()` regresa
# la lista de fallos (vacía = verde). Único punto de conexión a
# `tests/check.py` (T40 · T-RUTINAS).
# ───────────────────────────────────────────────────────────────

def corre():
    fallos = []
    modulo = sys.modules[__name__]
    nombres = sorted(n for n in dir(modulo) if n.startswith("test_"))
    for nombre in nombres:
        fn = getattr(modulo, nombre)
        try:
            fn()
        except AssertionError as exc:
            fallos.append(f"{nombre}: {exc}")
        except Exception as exc:  # noqa: BLE001 -- se reporta, no se traga
            fallos.append(f"{nombre}: {type(exc).__name__}: {exc}")
    return fallos


if __name__ == "__main__":
    fallos = corre()
    if fallos:
        print(f"FAIL ({len(fallos)}):")
        for f in fallos:
            print(f"  - {f}")
        raise SystemExit(1)
    total = len([n for n in dir(sys.modules[__name__]) if n.startswith("test_")])
    print(f"OK -- {total} pruebas, 0 fallos")
