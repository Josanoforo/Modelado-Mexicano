#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_adq_contrato_fix.py -- ACTO GEN2-ADQ-CONTRATO-FIX
(`forense/encargos/2026-09-09-GEN2-ADQ-CONTRATO-FIX.md`, 9/sep/2026).

H1/H2/H3/H5 de la revisión adversarial del 9/sep sobre la implementación
de PR #660-666 (insumo externo ChatGPT/Astra -- ver
`forense/no-corrido.tsv` para el estado del registro de esa nota, que no
llegó adjunta a la sesión que redactó este archivo). Cada prueba nombra
el hallazgo (H1/H2/H3/H5) o el criterio de aceptación de la pieza (P1..P4)
que congela. Estas pruebas se escribieron y confirmaron ROJAS contra el
código sin reparar ANTES de tocar `tools/adq_doctor.py`,
`tools/adquiere_cron.sh` o `tests/check.py` (0-bis del encargo).

Corre sola:

    python3 tests/test_adq_contrato_fix.py
"""
import datetime
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tests"))
sys.path.insert(0, str(RAIZ / "tools"))
import check as C  # noqa: E402
from test_adq_cableado import _corre_bash, _doble_git, _seam_disponible  # noqa: E402

FALLOS = []


def afirma(cond, msg):
    if not cond:
        FALLOS.append(msg)


# ═══════════════════════════════════════════════════════════════
# P1 / H1 · _autorizada() exige token afirmativo e inequívoco
# ═══════════════════════════════════════════════════════════════

def prueba_h1_autorizada_fixtures_negativos_y_positivo():
    """P1 aceptación: fixtures negativos (ausencia, negación-espacio,
    negación-guion, cita ajena a otra fila) y positivo (autorización
    afirmativa de ESA fila)."""
    import adq_doctor as D
    afirma(D._autorizada("", "FILA_X") is False,
           "H1: ausencia de autorización debe ser False")
    afirma(D._autorizada("sin autorización de mesa todavía", "FILA_X") is False,
           "H1: prosa sin token no autoriza")
    afirma(D._autorizada("NO AUTORIZADA por mesa (pendiente de firma)", "FILA_X") is False,
           "H1: negación con ESPACIO debe ser False")
    afirma(D._autorizada("NO-AUTORIZADA por mesa (pendiente de firma)", "FILA_X") is False,
           "H1: negación con GUION debe ser False")
    afirma(D._autorizada("AUTORIZADA:mesa/2026-09-09/OTRA_FILA_DISTINTA", "FILA_X") is False,
           "H1: una cita ajena a otra fila no debe autorizar FILA_X")
    afirma(D._autorizada("AUTORIZADA:mesa/2026-09-09/FILA_X", "FILA_X") is True,
           "H1: autorización afirmativa e inequívoca de ESA fila debe autorizar")


def prueba_h1_no_autorizada_no_se_lee_como_autorizada_en_selector():
    """Reproduce H1 verbatim de la revisión: `"AUTORIZADA" in (nota or "")`
    acepta 'NO-AUTORIZADA' por subcadena. Congelado sobre selecciona_filas,
    no solo sobre la función aislada."""
    import adq_doctor as D
    filas = [
        ("NEG_GUION", "PENDIENTE", "1",
         "descubrimiento de vía 2026-09-09 por /sonda; "
         "SONDA-LATERAL-RECOMENDADA; NO-AUTORIZADA por mesa"),
        ("NEG_ESPACIO", "PENDIENTE", "1",
         "descubrimiento de vía 2026-09-09 por /sonda; "
         "SONDA-LATERAL-RECOMENDADA; NO AUTORIZADA por mesa"),
    ]
    r = D.selecciona_filas(filas, corte=datetime.date(2026, 9, 9), maximo=5)
    elegidos = {e["id"] for e in r["elegidos"]}
    afirma("NEG_GUION" not in elegidos,
           f"H1: 'NO-AUTORIZADA' no debe leerse como autorizada; elegidos={elegidos}")
    afirma("NEG_ESPACIO" not in elegidos,
           f"H1: 'NO AUTORIZADA' no debe leerse como autorizada; elegidos={elegidos}")


def prueba_h1_pedida_no_sustituye_autorizacion_en_sonda():
    """P1: «invocación nominal no sustituye autorización si el contrato
    exige ambas» -- el handoff de /sonda exige las cuatro cosas, nombrar
    la fila por ID no basta si la autorización sigue ausente."""
    import adq_doctor as D
    filas = [("SONDA_NOMBRADA_SIN_AUTORIZAR", "PENDIENTE", "1",
              "descubrimiento de vía 2026-09-09 por /sonda; "
              "SONDA-LATERAL-RECOMENDADA; sin autorización todavía")]
    r = D.selecciona_filas(filas, corte=datetime.date(2026, 9, 9), maximo=5,
                            nombradas=["SONDA_NOMBRADA_SIN_AUTORIZAR"])
    afirma("SONDA_NOMBRADA_SIN_AUTORIZAR" not in {e["id"] for e in r["elegidos"]},
           "H1/P1: la invocación nominal no sustituye la autorización "
           "cuando el contrato exige ambas")


# ═══════════════════════════════════════════════════════════════
# P2 / H2 · el ÚLTIMO intento efectivo, nunca uno inferido
# ═══════════════════════════════════════════════════════════════

def prueba_h2_toma_la_ultima_fecha_no_la_primera_en_el_texto():
    """Intentos en distinto orden textual: debe tomar el intento efectivo
    MÁS RECIENTE por valor, no el primero que aparece en el texto."""
    import adq_doctor as D
    nota = ("intento efectivo 2026-01-01: curl 35; luego "
            "intento efectivo 2026-08-20: curl 52")
    afirma(D.fecha_intento_efectivo(nota) == datetime.date(2026, 8, 20),
           f"H2: debe tomar el intento MÁS RECIENTE, dio "
           f"{D.fecha_intento_efectivo(nota)!r}")
    nota_invertida = ("intento efectivo 2026-08-20: curl 52; antes "
                       "intento efectivo 2026-01-01: curl 35")
    afirma(D.fecha_intento_efectivo(nota_invertida) == datetime.date(2026, 8, 20),
           "H2: el orden textual no debe importar")


def prueba_h2_descubrimiento_posterior_no_reinicia_plazo():
    import adq_doctor as D
    nota = ("intento efectivo 2026-01-01: curl 35; "
            "descubrimiento de vía 2026-09-08 por /sonda")
    afirma(D.fecha_intento_efectivo(nota) == datetime.date(2026, 1, 1),
           "H2: un descubrimiento posterior no debe contarse como intento")


def prueba_h2_fecha_en_enlace_no_entra_al_computo():
    import adq_doctor as D
    nota = ("espejo en https://ejemplo.org/archivo/2026-08-30/datos.zip, "
            "sin intento registrado")
    afirma(D.fecha_intento_efectivo(nota) is None,
           f"H2: una fecha dentro de un enlace no es un intento efectivo, "
           f"dio {D.fecha_intento_efectivo(nota)!r}")


def prueba_h2_cita_documental_no_cambia_elegibilidad():
    import adq_doctor as D
    nota_a = "cita: el documento fue publicado el 2026-01-01, sin intento registrado"
    nota_b = "cita: el documento fue publicado el 2026-08-30, sin intento registrado"
    afirma(D.fecha_intento_efectivo(nota_a) is None,
           f"H2: cita documental no debe leerse como intento, dio "
           f"{D.fecha_intento_efectivo(nota_a)!r}")
    afirma(D.fecha_intento_efectivo(nota_a) == D.fecha_intento_efectivo(nota_b),
           "H2: cambiar la fecha de una cita documental no debe cambiar el cómputo")


def prueba_h2_sin_fecha_da_none():
    import adq_doctor as D
    afirma(D.fecha_intento_efectivo("sin intento previo") is None,
           "H2: sin fecha -> None")
    afirma(D.fecha_intento_efectivo(None) is None, "H2: nota ausente -> None")


def prueba_h2_fecha_invalida_es_indeterminada_y_va_a_conciliacion():
    """Nota histórica indecidible -> FECHA-INDETERMINADA; jamás una fecha
    inferida, y no se camina automáticamente."""
    import adq_doctor as D
    nota = "intento efectivo 2026-13-40: fecha mal escrita en la nota histórica"
    afirma(D.fecha_intento_efectivo(nota) is D.FECHA_INDETERMINADA,
           f"H2: fecha de intento inválida debe ser el centinela "
           f"FECHA_INDETERMINADA, dio {D.fecha_intento_efectivo(nota)!r}")
    filas = [("NOTA_ROTA", "NO-OBTENIDO-POR-ESTE-AGENTE(1 intentos)", "1", nota)]
    r = D.selecciona_filas(filas, corte=datetime.date(2026, 9, 9), maximo=5)
    afirma("NOTA_ROTA" not in {e["id"] for e in r["elegidos"]},
           f"H2: FECHA-INDETERMINADA no se camina automáticamente; "
           f"elegidos={r['elegidos']!r}")
    excl = {e["id"]: e["razon"] for e in r["excluidos"]}
    afirma("NOTA_ROTA" in excl and "INDETERMINADA" in excl["NOTA_ROTA"],
           f"H2: la razón debe nombrar la indeterminación explícitamente: {excl}")


# ═══════════════════════════════════════════════════════════════
# P3 / H3 · la excepción nominal de verdad
# ═══════════════════════════════════════════════════════════════

def prueba_h3_pedida_no_salta_estado_sin_fetch_en_el_selector():
    import adq_doctor as D
    filas = [("SF_NOMBRADA", "SIN-FETCH", "1", "espejo localizado, no abierto")]
    r = D.selecciona_filas(filas, corte=datetime.date(2026, 9, 9), maximo=5,
                            nombradas=["SF_NOMBRADA"])
    afirma("SF_NOMBRADA" not in {e["id"] for e in r["elegidos"]},
           "H3: nombrar una fila SIN-FETCH no debe saltarla al selector sin "
           "transformación canónica previa")


def prueba_h3_obtenido_parcial_no_habilita_descarga_completa_por_defecto():
    import adq_doctor as D
    filas = [("PARCIAL_AUTORIZADA", "OBTENIDO-PARCIAL", "1",
              "cobertura 3 de 9 olas; AUTORIZADA:mesa/2026-09-09/PARCIAL_AUTORIZADA")]
    r = D.selecciona_filas(filas, corte=datetime.date(2026, 9, 9), maximo=5,
                            nombradas=["PARCIAL_AUTORIZADA"])
    afirma("PARCIAL_AUTORIZADA" not in {e["id"] for e in r["elegidos"]},
           "H3: OBTENIDO-PARCIAL no habilita descarga completa por defecto, "
           "ni con autorización ni con invocación nominal")


def prueba_h3_recorrido_sonda_autorizacion_transformacion_seleccion():
    """P3 aceptación literal: «el recorrido entero de una fila -- propuesta
    SONDA -> autorización asentada -> transformación canónica -> selección
    del objeto faltante -- probado como integración, no herramienta por
    herramienta»."""
    import adq_doctor as D

    with tempfile.TemporaryDirectory() as d:
        ruta = Path(d) / "cola-adquisicion-registro.tsv"
        campos = ["fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
                  "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
                  "ids_manifiesto", "origen", "nota"]
        cabecera = "\t".join(campos)
        fila_sonda = "\t".join([
            "999", "PILOTO_H3", "piloto_h3", "", "SIN-FETCH", "3", "", "", "sonda",
            "descubrimiento de vía 2026-09-09 por /sonda; espejo académico "
            "localizado; SONDA-LATERAL-RECOMENDADA",
        ])
        ruta.write_text(cabecera + "\n" + fila_sonda + "\n", encoding="utf-8")

        # sin autorización: la transformación canónica se rehúsa.
        ok, razon = D.transforma_sin_fetch_autorizada("PILOTO_H3", ruta=ruta)
        afirma(ok is False,
               f"H3: sin autorización no debe transformar; ok={ok} razon={razon!r}")

        # la invocación nominal tampoco se salta el estado en el selector.
        r = D.selecciona_filas(D.lee_cola(ruta), corte=datetime.date(2026, 9, 9),
                                maximo=5, nombradas=["PILOTO_H3"])
        afirma("PILOTO_H3" not in {e["id"] for e in r["elegidos"]},
               "H3: sin transformación canónica, la invocación nominal no "
               "selecciona la fila SIN-FETCH")

        # autorización asentada (mesa firma, cita verificable, esta fila).
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        lineas[1] = lineas[1] + "; AUTORIZADA:mesa/2026-09-09/PILOTO_H3"
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

        # transformación canónica: ahora sí procede.
        ok, razon = D.transforma_sin_fetch_autorizada("PILOTO_H3", ruta=ruta)
        afirma(ok is True,
               f"H3: con autorización afirmativa e inequívoca debe transformar; "
               f"razon={razon!r}")

        filas_transformadas = D.lee_cola(ruta)
        estado_final = next(f[1] for f in filas_transformadas if f[0] == "PILOTO_H3")
        afirma(estado_final == "PENDIENTE",
               f"H3: la fila debe quedar en su estado accionable PENDIENTE, "
               f"dio {estado_final!r}")

        # selección del objeto faltante: por el camino normal de PENDIENTE,
        # SIN invocación nominal -- no hay rama de excepción en el selector.
        r2 = D.selecciona_filas(filas_transformadas, corte=datetime.date(2026, 9, 9),
                                 maximo=5)
        afirma("PILOTO_H3" in {e["id"] for e in r2["elegidos"]},
               f"H3: tras la transformación canónica la fila debe seleccionarse "
               f"por el camino normal; elegidos={r2['elegidos']!r}")


# ═══════════════════════════════════════════════════════════════
# P4 / H5 · el vigilante distingue terminar de publicar
# ═══════════════════════════════════════════════════════════════

def prueba_h5_publicacion_fallida_no_acredita_via_funcion_pura():
    linea = ("[ADQ] 2026-09-09 07:33: invocado=si motivo=- exit=0 duracion=10s "
             "commits_nuevos=1 ramas_nuevas=1 archivos_modificados=1 sha=abc123 "
             "publicacion=FALLIDA(2) run_id=2026-09-09T073300-1\n")
    estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 9), set(), linea)
    afirma(estado != "COMPLETO",
           f"H5: agente 0/publicación fallida no debe acreditar el día, dio "
           f"{estado!r} ({detalle})")
    afirma(estado == "AGENTE-OK-PUBLICACION-FALLIDA",
           f"H5: el vigilante debe nombrar explícitamente la distinción "
           f"terminar/publicar, dio {estado!r} ({detalle})")
    afirma("FALLIDA(2)" in detalle, f"H5: el detalle debe citar publicacion=FALLIDA(2): {detalle!r}")


def prueba_h5_push_fallido_persistente_no_acredita():
    """DIVERGENCIA-DECLARADA: el push falla y la reconciliación también --
    sigue siendo publicación fallida, no un éxito parcial."""
    linea = ("[ADQ] 2026-09-09 07:40: invocado=si motivo=- exit=0 duracion=15s "
             "commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1 sha=def456 "
             "publicacion=FALLIDA(1) run_id=2026-09-09T074000-2\n")
    estado, _ = C.t_cron_estado(datetime.date(2026, 9, 9), set(), linea)
    afirma(estado == "AGENTE-OK-PUBLICACION-FALLIDA",
           f"H5: push fallido persistente no debe acreditar, dio {estado!r}")


def prueba_h5_push_recuperado_si_acredita():
    """Push inicial rechazado, reconciliado por merge y reintentado con
    éxito: PUBLICACION_FALLIDA queda en 0 y publicacion=OK -- el día SÍ
    se acredita."""
    linea = ("[ADQ] 2026-09-09 07:45: invocado=si motivo=- exit=0 duracion=20s "
             "commits_nuevos=2 ramas_nuevas=0 archivos_modificados=1 sha=aaa111 "
             "publicacion=OK run_id=2026-09-09T074500-3\n")
    estado, _ = C.t_cron_estado(datetime.date(2026, 9, 9), set(), linea)
    afirma(estado == "COMPLETO", f"H5: push recuperado sí debe acreditar, dio {estado!r}")


def prueba_h5_rama_remota_sin_pr_sigue_acreditando():
    """'push-sin-PR': la rama se empujó pero gh no creó (o no hay) PR --
    el recibo SÍ llegó al remoto, eso es publicación cumplida; el PR es
    trámite de mesa, no parte de esta señal."""
    linea = ("[ADQ] 2026-09-09 07:50: invocado=si motivo=- exit=0 duracion=12s "
             "commits_nuevos=1 ramas_nuevas=1 archivos_modificados=1 sha=bbb222 "
             "publicacion=OK run_id=2026-09-09T075000-4\n")
    estado, _ = C.t_cron_estado(datetime.date(2026, 9, 9), set(), linea)
    afirma(estado == "COMPLETO",
           f"H5: rama remota sin PR (push OK) debe seguir acreditando, dio {estado!r}")


def prueba_h5_huella_historica_sin_campo_conserva_tratamiento():
    """Huellas históricas sin el campo publicacion= conservan el
    tratamiento declarado -- no se reinterpretan por su ausencia."""
    linea = ("[ADQ] 2026-09-05 07:32: invocado=si motivo=- exit=0 duracion=90s "
             "commits_nuevos=0 ramas_nuevas=0 archivos_modificados=0\n")
    estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 5), set(), linea)
    afirma(estado == "COMPLETO",
           f"H5: huella histórica sin publicacion= debe seguir acreditando "
           f"igual que antes, dio {estado!r} ({detalle})")


def prueba_h5_pr_fusionado_rama_borrada_con_publicacion_ok():
    """Evidencia ya fusionada (rama censo/<fecha> retirada tras el merge)
    con publicacion=OK explícito: sigue acreditando por la vía primaria de
    H1 (evidencia fusionada), el nuevo campo no interfiere con eso."""
    linea = ("[ADQ] 2026-09-09 07:33: invocado=si motivo=- exit=0 duracion=5s "
             "commits_nuevos=0 ramas_nuevas=1 archivos_modificados=1 sha=ccc333 "
             "publicacion=OK run_id=2026-09-09T073007-999\n")
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 9), set(), None, evidencia_fusionada=linea)
    afirma(estado == "COMPLETO",
           f"H5: PR fusionado con rama borrada y publicacion=OK debe acreditar, "
           f"dio {estado!r} ({detalle})")


def prueba_h5_vigilante_distingue_terminar_de_publicar_runner_real():
    """P4 aceptación #7: 'agente 0/publicación fallida', con salida, recibo
    y señal juntos -- funciones REALES del runner (huella_adq vía el seam
    de solo-definición) y la función REAL del vigilante (t_cron_estado),
    no una reimplementación de ninguna de las dos."""
    if not _seam_disponible():
        FALLOS.append("H5: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    with tempfile.TemporaryDirectory() as d:
        bindir = Path(d) / "bin"
        bindir.mkdir()
        _doble_git(bindir, falla_en="push")
        trabajo = Path(d) / "repo"
        (trabajo / "forense" / "censo-raiz").mkdir(parents=True)
        # LOGFILE se re-deriva a la ruta relativa por defecto al cargar el
        # runner (LOGDIR/FECHA.log) aunque se pase distinta por entorno --
        # se crea el directorio para que `log()`/`tee` no revienten.
        (trabajo / "forense" / "adq-log").mkdir(parents=True)
        env = {"PATH": f"{bindir}:{os.environ['PATH']}",
               "LOGFILE": str(Path(d) / "log.txt")}
        rc, salida = _corre_bash(
            'FECHA=2026-09-09; CENSO_DIR="forense/censo-raiz"; LOGFILE="$LOGFILE"; '
            'RUN_ID="RUN-CONTRATO-FIX"; HEAD_ANTES=deadbeef; HEAD_USADO=deadbeef; '
            'RAMAS_ANTES=0; T0=$(date +%s); PUBLICACION_FALLIDA=0; '
            'huella_adq "si" "-" "0" || true; '
            'echo "PUBLICACION_FALLIDA=$PUBLICACION_FALLIDA"',
            entorno=env, cwd=str(trabajo))
        afirma("PUBLICACION_FALLIDA=1" in salida,
               f"H5: huella_adq con push fallido debe subir PUBLICACION_FALLIDA "
               f"(salida real del runner): {salida!r}")
        recibo = trabajo / "forense" / "censo-raiz" / "2026-09-09.txt"
        afirma(recibo.exists(), "H5: el recibo local debe existir aunque el push falle")
        texto_recibo = recibo.read_text(encoding="utf-8") if recibo.exists() else ""
        afirma("publicacion=FALLIDA(1)" in texto_recibo,
               f"H5: el recibo debe declarar publicacion=FALLIDA(1): {texto_recibo!r}")
        estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 9), set(), texto_recibo)
        afirma(estado == "AGENTE-OK-PUBLICACION-FALLIDA",
               f"H5: la señal REAL del vigilante sobre el recibo REAL del runner "
               f"debe nombrar la distinción terminar/publicar; dio {estado!r} "
               f"({detalle})")


def prueba_h5_censo_inicial_push_fallido_alimenta_contador():
    """P4: «revisa el camino de publicación inicial del censo (~527-550)
    para que sus fallos alimenten el contador». Antes de este acto, un
    push fallido de la sección 2.5 ([CENSO]) se logueaba como
    PARO-CENSO-PUSH sin tocar PUBLICACION_FALLIDA -- un censo que nunca
    llegó al remoto podía cerrar la corrida con publicacion=OK."""
    if not _seam_disponible():
        FALLOS.append("H5: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    fuente = (RAIZ / "tools" / "adquiere_cron.sh").read_text(encoding="utf-8")
    if "publica_censo_manual" not in fuente:
        FALLOS.append("H5: tools/adquiere_cron.sh debe extraer la publicación "
                       "inicial del censo a una función (publica_censo_manual) "
                       "para que su fallo sea ejercitable y alimente el contador")
        return
    with tempfile.TemporaryDirectory() as d:
        bindir = Path(d) / "bin"
        bindir.mkdir()
        _escribe_git_doble_con_diff(bindir, falla_en="push")
        trabajo = Path(d) / "repo"
        (trabajo / "forense" / "censo-raiz").mkdir(parents=True)
        (trabajo / "forense" / "adq-log").mkdir(parents=True)
        (trabajo / "tests").mkdir(parents=True)
        (trabajo / "tests" / "manifiesto.py").write_text(
            "import sys\n"
            "if '--escanea' in sys.argv:\n"
            "    print('Total en disco: 3 archivos')\n",
            encoding="utf-8")
        env = {"PATH": f"{bindir}:{os.environ['PATH']}", "LOGFILE": "/dev/null"}
        rc, salida = _corre_bash(
            'FECHA=2026-09-09; CENSO_DIR="forense/censo-raiz"; LOGFILE="$LOGFILE"; '
            'PUBLICACION_FALLIDA=0; '
            'publica_censo_manual || true; '
            'echo "PUBLICACION_FALLIDA=$PUBLICACION_FALLIDA"',
            entorno=env, cwd=str(trabajo))
        afirma("PUBLICACION_FALLIDA=1" in salida,
               f"H5/P4: un push fallido en la publicación inicial del censo debe "
               f"incrementar PUBLICACION_FALLIDA; salida: {salida!r}")
        afirma("PARO-CENSO-PUSH" in salida,
               f"H5/P4: el fallo debe seguir logueándose igual que antes: {salida!r}")


def _escribe_git_doble_con_diff(dirbin, falla_en="push"):
    """Como `_doble_git` de test_adq_cableado.py, pero además responde a
    `git diff --cached --quiet` como "sí hay diferencias" (exit 1) -- lo
    que `publica_censo_manual` necesita para llegar al commit/push. Ningún
    otro camino de esta suite ejercita `diff` sobre el doble compartido,
    así que se escribe aparte en vez de tocar ese helper."""
    import textwrap
    p = Path(dirbin) / "git"
    p.write_text(textwrap.dedent(f"""\
        #!/usr/bin/env bash
        sub="$1"
        for a in "$@"; do case "$a" in {falla_en}) sub="{falla_en}";; esac; done
        if [ "$sub" = "{falla_en}" ]; then
          echo "doble: '{falla_en}' falla a propósito" >&2
          exit 1
        fi
        case "$1" in
          rev-parse) echo 0000000000000000000000000000000000000000;;
          show-ref|ls-remote) exit 1;;
          diff) exit 1;;
          log) echo "0000000 doble";;
          status) : ;;
        esac
        exit 0
        """), encoding="utf-8")
    p.chmod(0o755)


# ═══════════════════════════════════════════════════════════════

PRUEBAS = [v for k, v in sorted(globals().items()) if k.startswith("prueba_")]


def main():
    for fn in PRUEBAS:
        try:
            fn()
        except Exception as e:  # una prueba que revienta es un fallo, no un abort
            FALLOS.append(f"{fn.__name__}: EXCEPCIÓN {type(e).__name__}: {e}")
    for f in FALLOS:
        print(f"FAIL {f}")
    print(f"\n{len(PRUEBAS)} pruebas, {len(FALLOS)} fallos")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
