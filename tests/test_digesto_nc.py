#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_digesto_nc.py` -- unidad del digesto INCREMENTAL de
`forense/no-corrido.tsv` (sección H de `tools/digesto_tramite.py`).

P4 de `ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE`
(`forense/encargos/2026-09-08-digesto-incremental-reservas.md`). Lo llama
`tests/check.py` (T39 · T-DIGESTO-NC), mismo arnés que
`tests/test_corrida0.py`/`tests/test_corredores_gen2.py`: `corre()`
devuelve la lista de fallos (vacía = verde).

SIN CORPUS, sin red, sin reloj real: cada caso construye su propio
repositorio Git temporal (`git init` + commits reales), para poder
recuperar TSV anteriores por SHA -- el propio mecanismo que P1 exige --
sin depender de GitHub ni de la caja. Se limpia siempre con
`shutil.rmtree`, y ningún caso escribe dentro del repo real.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# `tools/digesto_tramite.py` hace `import estado_comun as EC` (absoluto, no
# relativo): necesita `tools/` en `sys.path`, mismo patrón que
# `tests/check.py` usa para el resto de módulos de `tools/`.
_RUTA_TOOLS = str(RAIZ / "tools")
if _RUTA_TOOLS not in sys.path:
    sys.path.insert(0, _RUTA_TOOLS)

_spec = importlib.util.spec_from_file_location(
    "digesto_tramite_bajo_prueba", RAIZ / "tools" / "digesto_tramite.py")
D = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = D
_spec.loader.exec_module(D)

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _afirma(cond, caso: str, msg: str) -> None:
    if not cond:
        _falla(caso, msg)


CABECERA_NC = ("id\tacto\tpieza\tque_no_se_corrio\trazon\timpacto\tsucesor\t"
              "estado\n")
CABECERA_TABLERO = ("id\tcreado\testado\tqué_se_firma\tgatea\tfirmada_en\t"
                    "ejecutada_en\n")


def _fila_nc(id_, estado="ABIERTA", sucesor="S", pieza="P1", impacto="I"):
    return f"{id_}\tA1\t{pieza}\tno se corrio\trazon\t{impacto}\t{sucesor}\t{estado}\n"


def _git(repo, *args, chk=True):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if chk and p.returncode != 0:
        raise RuntimeError(f"git {args} fallo: {p.stdout}{p.stderr}")
    return p


class _Repo:
    """Un repo Git temporal con `forense/no-corrido.tsv` +
    `forense/firmas-pendientes.tsv` mínimos, más helpers para escribir el
    TSV, commitear, y publicar un digesto DE VERDAD (llamando a
    `D.construye`) para que el siguiente caso lo encuentre por su propio
    mecanismo de localización (`_localiza_ultimo_digesto`)."""

    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="digesto-nc-test-"))
        _git(self.dir, "init", "-q")
        _git(self.dir, "config", "user.email", "t@t.com")
        _git(self.dir, "config", "user.name", "t")
        (self.dir / "forense" / "digesto").mkdir(parents=True)
        (self.dir / "forense" / "encargos").mkdir(parents=True)
        (self.dir / "forense" / "firmas-pendientes.tsv").write_text(
            CABECERA_TABLERO, encoding="utf-8")

    def cerrar(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def escribe_nc(self, filas_texto):
        (self.dir / "forense" / "no-corrido.tsv").write_text(
            CABECERA_NC + "".join(filas_texto), encoding="utf-8")

    def commit(self, msg="corte"):
        _git(self.dir, "add", "-A")
        _git(self.dir, "commit", "-q", "-m", msg)

    def sha_head(self):
        return _git(self.dir, "rev-parse", "HEAD").stdout.strip()

    def publica(self, fecha):
        """Genera y COMMITEA un digesto real vía `D.construye`, como lo
        haría `main()` en modo publicación -- para que el siguiente caso
        lo localice tal como lo haría el generador real."""
        import datetime as _dt
        anio, mes, dia = (int(x) for x in fecha.split("-"))
        f = _dt.date(anio, mes, dia)
        texto, res = D.construye(str(self.dir), f, True, 220, 25, None)
        assert not res.get("h_error"), res.get("h_error")
        salida = self.dir / "forense" / "digesto" / f"DIGESTO-{fecha}.md"
        salida.write_text(texto, encoding="utf-8")
        self.commit(f"digesto {fecha}")
        return texto

    def h(self, fecha="2026-09-08", base_nc_ref=None):
        import datetime as _dt
        anio, mes, dia = (int(x) for x in fecha.split("-"))
        f = _dt.date(anio, mes, dia)
        out, resumen = D.seccion_h(str(self.dir), f, base_nc_ref=base_nc_ref)
        return "\n".join(out), resumen


# ───────────────────────────────────────────────────────────────
# Casos de aceptación (P4)
# ───────────────────────────────────────────────────────────────

def t_primera_emision():
    caso = "primera_emision"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        texto, res = r.h("2026-09-01")
        _afirma("SIN-BASE-COMPARABLE" in texto, caso, "no declaró SIN-BASE-COMPARABLE")
        _afirma("NUEVA" not in texto.split("SIN-BASE-COMPARABLE")[1].split("H-REF")[0]
                if "H-REF" in texto else True, caso,
                "no debe listar filas como NUEVA en la primera emisión")
        _afirma(res["no_corrido_abiertas"] == 1, caso,
                f"no_corrido_abiertas={res['no_corrido_abiertas']}, esperado 1")
        _afirma(res["h_error"] is None, caso, "h_error inesperado en primera emisión")
        _afirma("<!-- H-REF sha_arbol=" in texto, caso,
                "no dejó la marca H-REF para la siguiente emisión")
    finally:
        r.cerrar()


def t_cortes_iguales_sin_cambios():
    caso = "cortes_iguales"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        r.publica("2026-09-01")
        texto, res = r.h("2026-09-02")
        _afirma("SIN-CAMBIOS" in texto, caso, "no declaró SIN-CAMBIOS")
        _afirma("BASE-COMPARABLE" in texto, caso, "no declaró comparabilidad")
        _afirma(res["no_corrido_abiertas"] == 1, caso, "total de abiertas no preservado")
    finally:
        r.cerrar()


def t_alta_cierre_reapertura_modificacion():
    caso = "alta_cierre_reapertura_modificacion"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002"), _fila_nc("NC-0003")])
        r.commit("init")
        r.publica("2026-09-01")
        # NC-0001: cierre (ABIERTA->CERRADA). NC-0002: cambio de sucesor
        # (modificada, mismo estado). NC-0003: sin cambios. NC-0004: alta.
        r.escribe_nc([_fila_nc("NC-0001", estado="CERRADA"),
                      _fila_nc("NC-0002", sucesor="S2"),
                      _fila_nc("NC-0003"),
                      _fila_nc("NC-0004")])
        r.commit("dia2")
        texto, res = r.h("2026-09-02")
        _afirma("BASE-COMPARABLE" in texto, caso, "no comparable")
        _afirma("`NC-0001`" in texto and "CAMBIO-DE-ESTADO" in texto, caso,
                "no detectó el cierre de NC-0001")
        _afirma("`NC-0002`" in texto and "MODIFICADA" in texto, caso,
                "no detectó la modificación de sucesor de NC-0002")
        _afirma("`NC-0003`" not in texto.split("| `id` |")[1] if "| `id` |" in texto
                else True, caso, "NC-0003 sin cambios no debe aparecer en la tabla")
        _afirma("`NC-0004`" in texto and "NUEVA" in texto, caso, "no detectó el alta NC-0004")
        _afirma("**3** ID(s) afectado(s)" in texto, caso,
                "el total de afectados no cuenta 3 (0001, 0002, 0004)")
        # reapertura: un tercer corte que reabre NC-0001
        r.publica("2026-09-02")
        r.escribe_nc([_fila_nc("NC-0001", estado="ABIERTA"),
                      _fila_nc("NC-0002", sucesor="S2"),
                      _fila_nc("NC-0003"),
                      _fila_nc("NC-0004")])
        r.commit("dia3-reapertura")
        texto3, _ = r.h("2026-09-03")
        _afirma("`NC-0001`" in texto3 and "CAMBIO-DE-ESTADO" in texto3, caso,
                "no detectó la reapertura de NC-0001")
    finally:
        r.cerrar()


def t_reordenamiento_sin_cambios_falsos():
    caso = "reordenamiento"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002")])
        r.commit("init")
        r.publica("2026-09-01")
        r.escribe_nc([_fila_nc("NC-0002"), _fila_nc("NC-0001")])  # mismo contenido, otro orden
        r.commit("dia2-reordenado")
        texto, _ = r.h("2026-09-02")
        _afirma("SIN-CAMBIOS" in texto, caso,
                "un reordenamiento sin cambio de contenido debe ser SIN-CAMBIOS")
    finally:
        r.cerrar()


def t_ausencia_nunca_cierre():
    caso = "ausencia"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002")])
        r.commit("init")
        r.publica("2026-09-01")
        r.escribe_nc([_fila_nc("NC-0001")])  # NC-0002 desaparece del corte
        r.commit("dia2-elimina")
        texto, _ = r.h("2026-09-02")
        _afirma("AUSENTE-EN-CORTE-ACTUAL" in texto, caso, "no declaró la ausencia")
        _afirma("`NC-0002` | AUSENTE-EN-CORTE-ACTUAL" in texto, caso,
                "la fila de NC-0002 no está marcada AUSENTE-EN-CORTE-ACTUAL")
        _afirma("CERRADA" not in texto.split("AUSENTE-EN-CORTE-ACTUAL")[0][-40:], caso,
                "una ausencia nunca se llama cierre por inferencia")
    finally:
        r.cerrar()


def t_referencia_valida_e_invalida():
    caso = "referencia_explicita"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        sha_valido = r.sha_head()
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002")])
        r.commit("dia2")
        texto_ok, res_ok = r.h("2026-09-02", base_nc_ref=sha_valido)
        _afirma(res_ok["h_error"] is None, caso, "ref válida marcada como error")
        _afirma("NUEVA" in texto_ok and "`NC-0002`" in texto_ok, caso,
                "con ref explícita válida no detectó el alta")

        texto_bad, res_bad = r.h("2026-09-02", base_nc_ref="deadbeefdeadbeef")
        _afirma(res_bad["h_error"] is not None, caso,
                "una ref explícita inválida debe marcar h_error, nunca sustituirse")
        _afirma("ERROR" in texto_bad, caso, "el texto no declara el ERROR de ref inválida")
    finally:
        r.cerrar()


def t_sha_no_recuperable_shallow():
    caso = "sha_antiguo_no_recuperable"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        texto, res = r.h("2026-09-01", base_nc_ref="0000000000000000000000000000000000000f")
        _afirma(res["h_error"] is not None, caso, "un SHA inexistente debe ser error, no éxito")
    finally:
        r.cerrar()


def t_dos_publicaciones_mismo_dia():
    caso = "dos_publicaciones_mismo_dia"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        r.publica("2026-09-08")
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002")])
        r.commit("cambio-mismo-dia")
        texto2, _ = r.h("2026-09-08")
        _afirma("NUEVA" in texto2 and "`NC-0002`" in texto2, caso,
                "la segunda emisión del mismo día no detectó el alta contra la primera")
    finally:
        r.cerrar()


def t_salto_de_dias():
    caso = "salto_de_dias"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        r.publica("2026-09-01")
        r.escribe_nc([_fila_nc("NC-0001", estado="CERRADA")])
        r.commit("varios-dias-despues")
        texto, _ = r.h("2026-09-06")  # 5 días sin ejecución del digesto
        _afirma("CAMBIO-DE-ESTADO" in texto, caso,
                "un salto de varios días debe seguir comparando contra el último publicado")
    finally:
        r.cerrar()


def t_reintento_antes_de_publicar_no_autoconsume():
    caso = "reintento_no_autoconsume"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        r.publica("2026-09-01")
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002")])
        r.commit("dia2")
        texto_a, _ = r.h("2026-09-02")
        texto_b, _ = r.h("2026-09-02")  # reintento, nada se comiteo entre medias
        _afirma(texto_a == texto_b, caso,
                "dos corridas sobre el mismo corte y la misma base deben ser byte-idénticas")
    finally:
        r.cerrar()


def t_stdout_no_escribe():
    caso = "stdout_no_escribe"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        antes = set((r.dir / "forense" / "digesto").iterdir())
        rc = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "digesto_tramite.py"),
             "--raiz", str(r.dir), "--stdout", "--sin-suite", "--fecha", "2026-09-01"],
            capture_output=True, text=True)
        despues = set((r.dir / "forense" / "digesto").iterdir())
        _afirma(rc.returncode == 0, caso, f"--stdout no debió fallar: {rc.stderr}")
        _afirma(antes == despues, caso, "--stdout escribió un archivo en forense/digesto/")
    finally:
        r.cerrar()


def t_tsv_invalido_error():
    caso = "tsv_duplicado_invalido"
    r = _Repo()
    try:
        (r.dir / "forense" / "no-corrido.tsv").write_text(
            CABECERA_NC + _fila_nc("NC-0001") + _fila_nc("NC-0001"), encoding="utf-8")
        r.commit("dup")
        texto, res = r.h("2026-09-01")
        _afirma(res["h_error"] is not None, caso, "un `id` duplicado debe ser error explícito")
        _afirma("ERROR" in texto, caso, "el texto no declara el ERROR")
    finally:
        r.cerrar()


def t_neutralizacion_preservada():
    """En la primera emisión (`SIN-BASE-COMPARABLE`) H no imprime ninguna
    fila individual -- solo cuenta -- así que un rótulo pelado en `sucesor`
    no llega a esta salida por esa vía. Caso base: `verifica()` sigue
    corriendo sobre la salida COMPLETA del digesto sin romperse."""
    caso = "neutralizacion_preservada"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001", sucesor="E3")])  # rótulo pelado en `sucesor`
        r.commit("init")
        texto, _ = r.h("2026-09-01")
        problemas = D.verifica(texto)
        _afirma(not problemas, caso, f"H dejó pasar un marcador sin neutralizar: {problemas}")
    finally:
        r.cerrar()


def t_neutralizacion_preservada_en_diff():
    """ACTO GEN2-T11 · RUTINAS-FIX, 8/sep/2026. A diferencia de la primera
    emisión (caso anterior), la rama `BASE-COMPARABLE` SÍ imprime `estado`/
    `sucesor` fila por fila en la tabla de afectados (`NUEVA`, `CAMBIO-DE-
    ESTADO`, `MODIFICADA`) -- y esas dos columnas pueden traer un rótulo
    `M`/`E` pelado (filas retrofit de ADR-393, o cualquier `sucesor` que
    cite un acto por su forma corta). Sin `neutraliza()` en ese camino,
    T25 para sobre el digesto igual que paraba antes del arreglo de la
    sección I. Ejercita las tres formas (alta, cambio de estado,
    modificación) con el mismo rótulo pelado `E7`."""
    caso = "neutralizacion_preservada_en_diff"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001"), _fila_nc("NC-0002", sucesor="S")])
        r.commit("init")
        r.publica("2026-09-01")
        # NC-0001: cierre con sucesor pelado. NC-0002: sucesor se modifica a
        # pelado. NC-0003: alta con sucesor pelado.
        r.escribe_nc([_fila_nc("NC-0001", estado="CERRADA", sucesor="E7"),
                      _fila_nc("NC-0002", sucesor="E7"),
                      _fila_nc("NC-0003", sucesor="E7")])
        r.commit("dia2")
        texto, res = r.h("2026-09-02")
        _afirma("BASE-COMPARABLE" in texto, caso, "no comparable")
        tabla = texto.split("| `id` |")[1] if "| `id` |" in texto else ""
        _afirma("_E7" in tabla, caso, "el rótulo pelado 'E7' del diff no salió neutralizado")
        _afirma("| E7 |" not in tabla and "E7 |" not in tabla.replace("_E7", ""), caso,
                "el rótulo 'E7' sobrevivió sin neutralizar en la tabla de afectados")
        problemas = D.verifica(texto)
        _afirma(not problemas, caso,
                f"H (rama BASE-COMPARABLE) dejó pasar un marcador sin neutralizar: {problemas}")
    finally:
        r.cerrar()


def t_esquema_cambiado_declarado():
    caso = "esquema_cambiado"
    r = _Repo()
    try:
        r.escribe_nc([_fila_nc("NC-0001")])
        r.commit("init")
        r.publica("2026-09-01")
        # Corte 2: agrega una columna nueva.
        (r.dir / "forense" / "no-corrido.tsv").write_text(
            "id\tacto\tpieza\tque_no_se_corrio\trazon\timpacto\tsucesor\testado\tcolumna_nueva\n"
            "NC-0001\tA1\tP1\tno se corrio\trazon\tI\tS\tABIERTA\tx\n", encoding="utf-8")
        r.commit("dia2-esquema")
        texto, res = r.h("2026-09-02")
        _afirma(res["h_error"] is None, caso, "una columna añadida no debe abortar el diff")
        _afirma("columna_nueva" in texto, caso, "no declaró la columna añadida")
    finally:
        r.cerrar()


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def corre() -> list[str]:
    """Devuelve la lista de fallos (vacía = verde). La llama `tests/check.py`."""
    FALLOS.clear()
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:  # un test que revienta es un fallo, no un hueco
            _falla(fn.__name__, f"EXCEPCION {type(exc).__name__}: {exc}")
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    print(f"tests/test_digesto_nc.py · {len(TESTS)} casos · "
          f"{len(TESTS) - len({f.split(':')[0] for f in fallos})} ok · {len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
