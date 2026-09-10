#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_digesto_candidatas.py` -- unidad de la sección K
(`tools/digesto_tramite.py::bloque_k`), localización de candidatas para
filas abiertas de `forense/no-corrido.tsv`/`forense/firmas-pendientes.tsv`.

P1 de `ACTO GEN2-OPERACION-1 · CICLO-CONCILIACION-PAGABLE`
(`forense/encargos/2026-09-09-GEN2-OPERACION-1-CICLO-CONCILIACION-PAGABLE.md`).
Lo llama `tests/check.py` (T42 · T-CANDIDATAS), mismo arnés que
`tests/test_digesto_nc.py`/`tests/test_digesto_mesa.py`: `corre()` devuelve
la lista de fallos (vacía = verde).

SIN corpus real, sin red: cada caso construye su propio árbol temporal
(directorios reales, sin `git init` -- `bloque_k` no necesita historial de
`git`, sólo lee archivos) y lo limpia con `shutil.rmtree`.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

_RUTA_TOOLS = str(RAIZ / "tools")
if _RUTA_TOOLS not in sys.path:
    sys.path.insert(0, _RUTA_TOOLS)

_spec = importlib.util.spec_from_file_location(
    "digesto_tramite_candidatas_bajo_prueba", RAIZ / "tools" / "digesto_tramite.py")
D = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = D
_spec.loader.exec_module(D)

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _afirma(cond, caso: str, msg: str) -> None:
    if not cond:
        _falla(caso, msg)


CABECERA_NC = ("id\tfecha\tacto\tpr\tpieza\tque_no_se_corrio\trazon\timpacto\t"
              "sucesor\testado\tcerrado_por\tfecha_cierre\n")
CABECERA_FP = "id\tcreado\testado\tqué_se_firma\tgatea\tfirmada_en\tejecutada_en\n"


def _fila_nc(id_, estado="ABIERTA", que="obligación pendiente de X", sucesor="Y"):
    return (f"{id_}\t2026-09-01\tACTO-T\tn/a\tP1\t{que}\trazón\timpacto\t"
            f"{sucesor}\t{estado}\t\t\n")


class _Arbol:
    """Un árbol temporal con `forense/no-corrido.tsv` +
    `forense/firmas-pendientes.tsv` mínimos y los directorios que K
    admite como fuente (`forense/notas/`, `forense/encargos/` + `cola/`,
    `canon/`)."""

    def __init__(self, con_gobernanza=True, con_notas=True, con_encargos=True):
        self.dir = Path(tempfile.mkdtemp(prefix="digesto-candidatas-test-"))
        (self.dir / "forense" / "digesto").mkdir(parents=True)
        if con_notas:
            (self.dir / "forense" / "notas").mkdir(parents=True)
        if con_encargos:
            (self.dir / "forense" / "encargos" / "cola").mkdir(parents=True)
        if con_gobernanza:
            (self.dir / "canon").mkdir(parents=True)
        (self.dir / "forense" / "firmas-pendientes.tsv").write_text(
            CABECERA_FP, encoding="utf-8")
        (self.dir / "forense" / "no-corrido.tsv").write_text(
            CABECERA_NC, encoding="utf-8")

    def cerrar(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def escribe_nc(self, filas_texto):
        (self.dir / "forense" / "no-corrido.tsv").write_text(
            CABECERA_NC + "".join(filas_texto), encoding="utf-8")

    def nota(self, nombre, texto):
        (self.dir / "forense" / "notas" / nombre).write_text(texto, encoding="utf-8")

    def encargo(self, nombre, texto, en_cola=False):
        sub = "cola" if en_cola else "."
        (self.dir / "forense" / "encargos" / sub / nombre).write_text(
            texto, encoding="utf-8")

    def gobernanza(self, texto):
        (self.dir / "canon" / "gobernanza-v1_15.md").write_text(texto, encoding="utf-8")

    def k(self):
        cuenta = D.Cuenta()
        out, resumen = D.bloque_k(str(self.dir), cuenta)
        return "\n".join(out), resumen


# ───────────────────────────────────────────────────────────────
# Casos de aceptación
# ───────────────────────────────────────────────────────────────

def t_cubre_conjunto_completo_de_un_corte():
    caso = "cubre_conjunto_completo"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0101"), _fila_nc("NC-0102"), _fila_nc("NC-0103")])
        texto, res = a.k()
        _afirma(res["examinadas"] == 3, caso,
                f"examinadas={res['examinadas']}, esperado 3 (todo el corte)")
        for rid in ("NC-0101", "NC-0102", "NC-0103"):
            _afirma(f"`{rid}`" in texto or f"_NC_0" in texto or rid.replace("-", "_0") in texto
                    or rid in texto.replace("_", "-"), caso,
                    f"{rid} no aparece citada en la salida")
    finally:
        a.cerrar()


def t_localiza_sucesora_sin_cerrar():
    caso = "localiza_sucesora_sin_cerrar"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0201", sucesor="ACTO-SUCESOR-1")])
        a.encargo("2026-09-09-acto-sucesor.md",
                  "Este encargo es el sucesor y objeto de NC-0201: cierra su hueco.\n")
        texto, res = a.k()
        _afirma(res["candidatos"] == 1, caso,
                f"candidatos={res['candidatos']}, esperado 1")
        _afirma("FUERTE" in texto, caso, "no marcó el cruce como evidencia FUERTE")
        _afirma("CANDIDATO" in texto or "candidato" in texto.lower(), caso,
                "no declara explícitamente que es candidato, no cierre")
        _afirma("CERRADA" not in texto, caso,
                "NO debe cerrar automáticamente la fila -- coincidencia textual "
                "es candidato, nunca cierre")
    finally:
        a.cerrar()


def t_ignora_pr_abierto():
    caso = "ignora_pr_abierto"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0301")])
        a.nota("2026-09-09-nota-pr.md", "Ver NC-0301 en el PR #999.\n")
        texto, res = a.k()
        _afirma(res["no_resolubles"] >= 1 or res["candidatos"] == 0, caso,
                "una cita desnuda de PR no debe contar como candidato resuelto")
        _afirma("NO-RESOLUBLE" in texto, caso,
                "no declaró NO-RESOLUBLE para la cita de PR")
    finally:
        a.cerrar()


def t_detecta_evidencia_nueva_con_tsv_sin_cambios():
    caso = "detecta_evidencia_nueva_tsv_sin_cambios"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0401")])
        texto1, res1 = a.k()
        _afirma(res1["sin_evidencia"] == 1, caso, "primera corrida debió ser sin-evidencia")
        a.nota("2026-09-09-evidencia-nueva.md",
              "Esta nota es el encargo objeto que resuelve NC-0401.\n")
        texto2, res2 = a.k()
        _afirma(res2["candidatos"] == 1, caso,
                "una fuente nueva (mismo TSV, sin cambios) debió producir un candidato")
    finally:
        a.cerrar()


def t_conserva_nc_0055_abierta_si_no_hay_evidencia_de_cierre():
    caso = "conserva_nc_0055_abierta"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0055", que="cuerpo curado pedido, no satisfecho")])
        texto, res = a.k()
        # Sin fuente que mencione NC-0055, la sección no debe fabricar un
        # candidato ni tocar el TSV -- sigue ABIERTA en el árbol de entrada,
        # y esta sección jamás la escribe.
        _afirma((a.dir / "forense" / "no-corrido.tsv").read_text(encoding="utf-8")
                .count("NC-0055") == 1, caso,
                "bloque_k no debe escribir en no-corrido.tsv bajo ninguna circunstancia")
        _afirma(res["examinadas"] == 1, caso, "debió examinar la fila NC-0055")
    finally:
        a.cerrar()


def t_ciclo_truncado_enumera_residuales_y_el_siguiente_no_los_omite():
    caso = "ciclo_truncado_enumera_residuales"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc(f"NC-{900+i:04d}") for i in range(5)])
        texto, res = a.k()
        _afirma(res["examinadas"] == 5, caso,
                f"examinadas={res['examinadas']}, esperado 5 -- un corte truncado "
                "no debe perder filas del universo declarado")
        # Segunda corrida sobre el MISMO árbol: debe seguir reportando las
        # mismas 5 (el "ciclo" es del trámite posterior, no de esta
        # sección -- pero la sección no debe omitir nada del universo
        # actual en ninguna corrida).
        texto2, res2 = a.k()
        _afirma(res2["examinadas"] == 5, caso,
                "la siguiente corrida sobre el mismo árbol omitió residuales")
    finally:
        a.cerrar()


def t_alcance_incompleto_si_falta_una_fuente():
    caso = "alcance_incompleto_fuente_faltante"
    a = _Arbol(con_gobernanza=False)
    try:
        a.escribe_nc([_fila_nc("NC-0501")])
        texto, res = a.k()
        _afirma(res["alcance_incompleto"], caso,
                "no declaró ALCANCE INCOMPLETO con una fuente faltante")
        _afirma("ALCANCE INCOMPLETO" in texto, caso,
                "no lo dice explícitamente en la salida (nunca en silencio)")
    finally:
        a.cerrar()


def t_excluye_repeticion_literal_de_la_obligacion():
    caso = "excluye_repeticion_literal"
    a = _Arbol()
    try:
        que = "obligación muy específica NC-0601 que se repite igual en todas partes"
        a.escribe_nc([_fila_nc("NC-0601", que=que)])
        # La nota trae el MISMO texto de la obligación -- no es evidencia
        # externa, es la fila citándose a sí misma.
        a.nota("2026-09-09-repite.md", f"NC-0601: {que}\n")
        texto, res = a.k()
        _afirma(res["candidatos"] == 0, caso,
                "la repetición literal de la propia obligación no debe contar "
                "como candidato externo")
    finally:
        a.cerrar()


def t_excluye_forense_digesto_como_prueba():
    caso = "excluye_forense_digesto"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0701")])
        (a.dir / "forense" / "digesto" / "DIGESTO-2026-09-08.md").write_text(
            "NC-0701 aparece aquí, pero este es el propio digesto.\n", encoding="utf-8")
        texto, res = a.k()
        _afirma(res["candidatos"] == 0 and res["sin_evidencia"] == 1, caso,
                "forense/digesto/ nunca debe contar como fuente de evidencia")
    finally:
        a.cerrar()


def t_nc_0040_se_presenta_sin_resolver():
    caso = "nc_0040_calibracion"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-0801")])
        texto, _res = a.k()
        _afirma("NC-0040" in texto, caso,
                "no presenta NC-0040 como calibración pendiente para mesa")
        _afirma("mesa decide" in texto.lower() or "mesa" in texto.lower(), caso,
                "no deja explícito que mesa resuelve, no esta sección")
    finally:
        a.cerrar()


# ───────────────────────────────────────────────────────────────
# H4 (revisión adversarial, ACTO GEN2-DERIVADORES-FIX) -- P0/P1:
# `_busca_candidatas_fila_k` usaba `texto.find(rid)` una sola vez por
# archivo. Si la PRIMERA aparición del id caía dentro de la exclusión (2)
# (la propia obligación citándose a sí misma), la función hacía `continue`
# al siguiente archivo sin examinar ninguna aparición posterior -- una
# segunda mención real, con sucesor firmado, en el MISMO archivo, quedaba
# invisible. Estos casos fallan contra el código viejo y deben pasar tras
# el fix (todas las apariciones, exclusiones por aparición, dedup,
# archivo ilegible declarado, enlace por línea sin repetir id).
# ───────────────────────────────────────────────────────────────

def t_h4_primera_mencion_excluida_segunda_valida():
    caso = "h4_primera_excluida_segunda_valida"
    fila = {"que_no_se_corrio": "obligación repetida NC-1001 en todas partes",
            "razon": "razón", "impacto": "impacto", "sucesor": "Y"}
    texto_propio = D._propio_texto_fila_k(fila)
    tmp = Path(tempfile.mkdtemp(prefix="h4-unit-"))
    try:
        ruta = tmp / "n.md"
        # Primera aparición: repite la obligación verbatim (exclusión 2) --
        # el mismo texto que `_propio_texto_fila_k` deriva de la fila.
        # Segunda aparición, más adelante en el MISMO archivo: mención
        # real con palabra clave fuerte (sucesor), sin relación con la
        # obligación propia.
        ruta.write_text(
            f"NC-1001: {texto_propio}\n" + ("relleno de por medio, sin el id.\n" * 5) +
            "El sucesor de NC-1001 es este mismo encargo, que lo cierra.\n",
            encoding="utf-8")
        universo = {"notas": ([str(ruta)], False)}
        fuertes, semanticas, _no_res, _ileg = D._busca_candidatas_fila_k(
            str(tmp), universo, "NC-1001", texto_propio, str(tmp / "digesto"), 220)
        _afirma(len(fuertes) + len(semanticas) == 1, caso,
                f"fuertes+semanticas={len(fuertes) + len(semanticas)}, esperado 1 -- "
                "la segunda aparición (válida) no debe quedar oculta por la "
                "exclusión de la primera")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_h4_varias_candidatas_en_un_archivo():
    caso = "h4_varias_candidatas_en_un_archivo"
    tmp = Path(tempfile.mkdtemp(prefix="h4-unit-"))
    try:
        ruta = tmp / "n.md"
        ruta.write_text(
            "El objeto de NC-1002 se toca aquí, encargo A.\n" +
            ("relleno\n" * 5) +
            "Y de nuevo, sucesor de NC-1002 en encargo B, más abajo.\n",
            encoding="utf-8")
        universo = {"notas": ([str(ruta)], False)}
        fuertes, semanticas, _no_res, _ileg = D._busca_candidatas_fila_k(
            str(tmp), universo, "NC-1002", "", str(tmp / "digesto"), 220)
        _afirma(len(fuertes) + len(semanticas) == 2, caso,
                f"hallados {len(fuertes) + len(semanticas)}, esperado 2 -- "
                "dos apariciones distintas del id en el mismo archivo deben "
                "producir dos candidatos, no recortarse a la primera")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_h4_id_prefijo_de_otro_no_colisiona():
    caso = "h4_id_prefijo_de_otro"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-100")])
        # Sólo aparece NC-1005 (NC-100 es *prefijo* de NC-1005, nunca debe
        # contar como aparición de NC-100 como token).
        a.nota("2026-09-10-prefijo.md",
              "El sucesor de NC-1005 es este encargo, objeto claro.\n")
        _, res = a.k()
        _afirma(res["candidatos"] == 0 and res["sin_evidencia"] == 1, caso,
                "NC-100 no debe casar como prefijo dentro de NC-1005")
    finally:
        a.cerrar()


def t_h4_fuente_ilegible_declara_alcance_incompleto():
    caso = "h4_fuente_ilegible"
    a = _Arbol()
    try:
        a.escribe_nc([_fila_nc("NC-1006")])
        # Un directorio con sufijo `.md` cae dentro del glob `*.md` pero
        # `open()` sobre él lanza `IsADirectoryError` (subclase de
        # `OSError`) sin importar privilegios -- a diferencia de
        # `chmod 0o000`, que root ignora, esto reproduce "archivo
        # ilegible" de forma portable.
        (a.dir / "forense" / "notas" / "2026-09-10-ilegible.md").mkdir()
        texto, res = a.k()
        _afirma(res["alcance_incompleto"], caso,
                "un archivo ilegible debe declarar ALCANCE INCOMPLETO, "
                "nunca desaparecer en silencio")
        _afirma("ilegible" in texto.lower() or "ALCANCE INCOMPLETO" in texto, caso,
                "no declara la causa del alcance incompleto")
    finally:
        a.cerrar()


def t_h4_sucesora_enlazada_sin_repetir_id():
    caso = "h4_sucesora_enlazada_sin_repetir_id"
    a = _Arbol()
    try:
        filas = [_fila_nc("NC-1007"), _fila_nc("NC-1008")]
        a.escribe_nc(filas)
        # NC-1007 es la fila 2 (línea 2, tras la cabecera) de no-corrido.tsv
        # en este árbol -- la nota cita esa línea explícitamente y JAMÁS
        # repite el texto "NC-1007".
        a.nota("2026-09-10-enlace-linea.md",
              "El objeto que cierra esta deuda queda descrito en "
              "`forense/no-corrido.tsv:2`, sin repetir aquí el identificador.\n")
        _, res = a.k()
        _afirma(res["candidatos"] >= 1, caso,
                "una cita explícita `archivo.tsv:N` que resuelve a la línea "
                "de NC-1007 debe producir candidato aunque el id no se "
                "repita como texto")
    finally:
        a.cerrar()


def t_h4_tope_lista_cero_agota_el_conjunto():
    caso = "h4_tope_lista_cero_agota_conjunto"
    a = _Arbol()
    try:
        filas = [_fila_nc(f"NC-{2000+i}") for i in range(8)]
        a.escribe_nc(filas)
        for i in range(8):
            a.nota(f"2026-09-10-pag-{i}.md",
                  f"El sucesor de NC-{2000+i} vive en este encargo, objeto {i}.\n")
        cuenta = D.Cuenta()
        out_topado, _ = D.bloque_k(str(a.dir), cuenta, tope_lista=3)
        texto_topado = "\n".join(out_topado)
        _afirma("omitidas por el" in texto_topado, caso,
                "con tope bajo debe declarar filas omitidas, no ocultarlas en silencio")
        out_todo, res_todo = D.bloque_k(str(a.dir), cuenta, tope_lista=0)
        texto_todo = "\n".join(out_todo)
        for i in range(8):
            _afirma(f"NC-{2000+i}" in texto_todo, caso,
                    f"tope_lista=0 debe agotar el conjunto -- NC-{2000+i} no aparece")
    finally:
        a.cerrar()


def corre():
    FALLOS.clear()
    for nombre, fn in list(globals().items()):
        if nombre.startswith("t_") and callable(fn):
            fn()
    return list(FALLOS)


if __name__ == "__main__":
    fallos = corre()
    if fallos:
        for f in fallos:
            print(f"FAIL: {f}")
        sys.exit(1)
    print("OK")
