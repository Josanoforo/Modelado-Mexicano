#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_digesto_mesa.py` -- falsadores dirigidos de la vista de mesa
(`tools/digesto_tramite.py --mesa`, P1 de `ACTO GEN2-GOBIERNO-DECISIONES`,
`forense/encargos/2026-09-09-GEN2-GOBIERNO-DECISIONES.md`; especificación
en `forense/notas/2026-09-09-PROPUESTA-GOBIERNO-DECISIONES-PENDIENTES-
astra.md` §8).

Lo llama `tests/check.py` (T41 · T-DIGESTO-MESA), mismo arnés que
`tests/test_digesto_nc.py`/`tests/test_corrida0.py`: `corre()` devuelve
la lista de fallos (vacía = verde).

P5, verbatim del encargo: "todos con control real contra el árbol
actual (no fixtures inventados salvo que el caso lo exija)". Estos casos
corren `seccion_mesa()` directamente contra `RAIZ` (el clon real), NUNCA
escriben en él -- el propio T-DIGESTO-MESA-CERO-ESCRITURA lo comprueba
por hash antes/después. Ningún caso de aquí necesita fixture sintético:
los ocho casos de aceptación, `FP-362`, `D-14` y la glosa-vs-token ya
existen en `forense/{firmas-pendientes,no-corrido}.tsv` tal como los cita
el encargo.
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import io
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

_RUTA_TOOLS = str(RAIZ / "tools")
if _RUTA_TOOLS not in sys.path:
    sys.path.insert(0, _RUTA_TOOLS)

_spec = importlib.util.spec_from_file_location(
    "digesto_tramite_bajo_prueba_mesa", RAIZ / "tools" / "digesto_tramite.py")
D = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = D
_spec.loader.exec_module(D)

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _afirma(cond, caso: str, msg: str) -> None:
    if not cond:
        _falla(caso, msg)


def _hoy():
    return datetime.date.today()


def _mesa_texto(id_filtro=None, tope_texto=0, tope_lista=0):
    """Corre `seccion_mesa()` contra el árbol real y devuelve el texto
    plano concatenado (para `in`), como haría `--mesa --stdout`."""
    cuenta = D.Cuenta()
    lineas, resumen = D.seccion_mesa(str(RAIZ), _hoy(), cuenta, id_filtro=id_filtro,
                                     tope_texto=tope_texto, tope_lista=tope_lista)
    return "\n".join(lineas), resumen


# ───────────────────────────────────────────────────────────────
# Los ocho casos de aceptación (§8) -- ninguno desaparece silenciosamente.
# 6 cerrados/consumidos por `ACTO GEN2-CIERRES-CON-CITA` (PR #648), 2
# siguen ABIERTA (control negativo real, PARO-PREMISA).
# ───────────────────────────────────────────────────────────────

def t_ocho_casos_nc_cerradas():
    for id_, estado_esperado in (
        ("NC-0002", "CERRADA"),
        ("NC-0017", "CERRADA"),
        ("NC-0035", "CERRADA"),
        ("NC-0036", "CERRADA-DESISTIDA"),
    ):
        caso = f"t_ocho_casos_nc_cerradas[{id_}]"
        texto, resumen = _mesa_texto(id_filtro=id_)
        _afirma(f"`{id_}`" in texto, caso, f"{id_} no aparece en --mesa --id {id_}")
        _afirma(estado_esperado in texto, caso,
               f"{id_}: se esperaba el estado `{estado_esperado}` citado en la vista")
        _afirma("Ya resuelto" in texto, caso,
               f"{id_}: debería presentarse como ya resuelto, no como pendiente de mesa")


def t_ocho_casos_nc_abiertas():
    for id_ in ("NC-0037", "NC-0055"):
        caso = f"t_ocho_casos_nc_abiertas[{id_}]"
        texto, resumen = _mesa_texto(id_filtro=id_)
        _afirma(f"`{id_}`" in texto, caso, f"{id_} no aparece en --mesa --id {id_}")
        _afirma("Ya resuelto" not in texto, caso,
               f"{id_}: sigue ABIERTA en el árbol -- NO debe presentarse como resuelta")
        # También debe aparecer en la vista SIN --id (conjunto completo de
        # ABIERTA), no solo en la consulta puntual.
        texto_completo, _ = _mesa_texto()
        _afirma(f"`{id_}`" in texto_completo, caso,
               f"{id_} está ABIERTA y no aparece en el conjunto completo (--mesa sin --id)")


def t_ocho_casos_cola():
    # GEN2-E5-0 y PILOTO-CAJA viven en forense/encargos/cola/, no en FP/NC
    # -- seccion_mesa() los localiza por `codigo` como fallback declarado.
    for id_, estado_esperado in (
        ("GEN2-E5-0", "CONSUMIDO"),
        ("PILOTO-CAJA", "LISTO-CAJA"),
    ):
        caso = f"t_ocho_casos_cola[{id_}]"
        texto, resumen = _mesa_texto(id_filtro=id_)
        _afirma(id_ in texto, caso, f"{id_} no aparece en --mesa --id {id_}")
        _afirma(estado_esperado in texto, caso,
               f"{id_}: se esperaba `{estado_esperado}` (estado real del ítem de cola)")


# ───────────────────────────────────────────────────────────────
# FP-362 -- el residual v4 se firmó (ACTO GEN2-FIRMAS-ADOPCION-1,
# 9/sep/2026): la vista de mesa ya no debe pedir decisión sobre esto.
# ───────────────────────────────────────────────────────────────

def t_fp362_residual_v4():
    caso = "t_fp362_residual_v4"
    texto, _ = _mesa_texto(id_filtro="FP-362", tope_texto=0)
    _afirma("`FP-362`" in texto, caso, "FP-362 no aparece")
    _afirma("v4" in texto, caso,
           "la resolución del residual de v4 debe quedar visible en el texto citado")
    _afirma("FIRMADA" in texto, caso,
           "FP-362 quedó FIRMADA (ambas mitades, v3 y v4, EJECUTADAS) -- ya no "
           "debe presentarse como pendiente de decisión")


# ───────────────────────────────────────────────────────────────
# D-14 doc vs fila -- identidad `documento#ID` sin colisión.
# ───────────────────────────────────────────────────────────────

def t_d14_doc_vs_fila_sin_colision():
    caso = "t_d14_doc_vs_fila_sin_colision"
    texto, resumen = _mesa_texto(id_filtro="D-14")
    _afirma("`D-14`" in texto, caso, "D-14 no aparece")
    _afirma("(FP)" in texto, caso,
           "D-14 debe resolverse contra la fila de forense/firmas-pendientes.tsv, no "
           "contra instrucciones-proyecto-v2_13.md (identidad calificada por documento)")
    _afirma(resumen["filas"] == 1, caso,
           f"D-14 debería devolver exactamente 1 fila (sin colisión), dio {resumen['filas']}")
    # Calificado por documento (§5): explícito con `#` también resuelve, al
    # mismo candidato -- no un candidato distinto.
    texto_q, resumen_q = _mesa_texto(id_filtro="forense/firmas-pendientes.tsv#D-14")
    _afirma(resumen_q["filas"] == 1, caso,
           "la forma calificada `documento#ID` debe resolver igual que la pelada")


# ───────────────────────────────────────────────────────────────
# Glosa-vs-token: `ABIERTA -- ... EJECUTADA para una parte` sigue abierta.
# FP-362 fue el ancla real hasta que ACTO GEN2-FIRMAS-ADOPCION-1 (9/sep/2026)
# firmó su residual v4 y la glosa pasó a `FIRMADA` -- el defecto que este
# falsador protege (que la máquina no lea el token por encima de la glosa
# real) ya no tiene ancla viva en el árbol, así que el caso pasa a
# sintético (excepción declarada en la cabecera del archivo: "salvo que
# el caso lo exija").
# ───────────────────────────────────────────────────────────────

def t_glosa_vs_token_fp362():
    caso = "t_glosa_vs_token_fp362"
    glosa_sintetica = "ABIERTA -- FIRMADA-PARCIAL -- EJECUTADA para v3, ABIERTA para v4."
    _afirma(glosa_sintetica.startswith("ABIERTA"), caso,
           f"fixture mal formado -- debería empezar con ABIERTA, es {glosa_sintetica!r}")
    _afirma("EJECUTADA" in glosa_sintetica, caso,
           "fixture mal formado -- debería citar EJECUTADA en la glosa")
    _afirma(D.EC.es_abierta(glosa_sintetica), caso,
           "es_abierta() debe leer una glosa `ABIERTA -- ... EJECUTADA para una "
           "parte` como ABIERTA -- defecto real que el falsador protege, hoy sin "
           "ancla viva porque FP-362 ya se firmó por completo")


# ───────────────────────────────────────────────────────────────
# Sucesora-no-acredita-ejecución: NC con sucesor FP firmado, la NC sigue
# mostrando el residual, no un cierre implícito.
# ───────────────────────────────────────────────────────────────

def t_sucesora_no_acredita_ejecucion():
    caso = "t_sucesora_no_acredita_ejecucion"
    # Búsqueda real primero (P5: "no fixtures inventados salvo que el caso
    # lo exija"): hoy ninguna NC ABIERTA del árbol cita en `sucesor` una
    # FP ya no-ABIERTA (las tres FP citadas por NC -- FP-361/362/363 --
    # están todas ABIERTA). Sin ese control real disponible, se falsa con
    # el fixture mínimo que el caso exige.
    _, filas_nc, _ = D._lee_no_corrido(str(RAIZ))
    _, filas_fp, _ = D.EC.lee_tablero(str(RAIZ))
    fp_por_id = {f.get("id", "").strip(): f for f in filas_fp}
    candidata = None
    for f in filas_nc:
        if not D.EC.es_abierta(f.get("estado", "")):
            continue
        ids = D.RE_FP_ID.findall(f.get("sucesor", "") or "")
        for fid in ids:
            ffila = fp_por_id.get(fid)
            if ffila is not None and not D.EC.es_abierta(ffila.get("estado", "")):
                candidata = (f, fid, fp_por_id)
                break
        if candidata:
            break
    if candidata is None:
        f_fixture = {
            "id": "NC-9999", "fecha": "2026-09-01", "estado": "ABIERTA",
            "que_no_se_corrio": "caso sintético de sucesora firmada",
            "razon": "fixture", "impacto": "fixture", "sucesor": "FP-9998",
        }
        fp_fixture = {"id": "FP-9998", "estado": "FIRMADA", "creado": "2026-09-01",
                     "gatea": "", "qué_se_firma": "sucesora del fixture"}
        candidata = (f_fixture, "FP-9998", {"FP-9998": fp_fixture})
    f, fid, fp_idx = candidata
    r = D._nc_a_fila_mesa(f, _hoy(), D.Cuenta(), 0, fp_idx)
    _afirma(r["abierta"], caso, f"{f['id']}: debería seguir ABIERTA")
    _afirma("no acredita ejecutar" in r["cubierto"], caso,
           f"{f['id']}: la sucesora `{fid}` no debe leerse como cierre de la NC")


# ───────────────────────────────────────────────────────────────
# Idempotencia: mismo SHA + misma fecha -> misma salida byte a byte.
# ───────────────────────────────────────────────────────────────

def t_idempotencia_mismo_sha_misma_fecha():
    caso = "t_idempotencia_mismo_sha_misma_fecha"
    t1, _ = _mesa_texto()
    t2, _ = _mesa_texto()
    _afirma(t1 == t2, caso, "dos corridas de seccion_mesa() sobre el mismo árbol y la "
                            "misma fecha dieron salidas distintas")
    h1 = hashlib.sha256(t1.encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(t2.encode("utf-8")).hexdigest()
    _afirma(h1 == h2, caso, f"hash distinto entre corridas: {h1} != {h2}")


# ───────────────────────────────────────────────────────────────
# Cero escritura: `--mesa --stdout` no toca FP/NC/registro de adquisición.
# ───────────────────────────────────────────────────────────────

def _hash_archivo(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def t_cero_escritura():
    caso = "t_cero_escritura"
    rutas = [
        RAIZ / "forense" / "firmas-pendientes.tsv",
        RAIZ / "forense" / "no-corrido.tsv",
        RAIZ / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv",
    ]
    antes = {str(r): _hash_archivo(r) for r in rutas}
    _mesa_texto()
    _mesa_texto(id_filtro="FP-362")
    despues = {str(r): _hash_archivo(r) for r in rutas}
    for r in rutas:
        _afirma(antes[str(r)] == despues[str(r)], caso,
               f"`{r}` cambió de hash tras correr seccion_mesa() -- la vista debe ser "
               f"de solo lectura")


# ───────────────────────────────────────────────────────────────
# Vencimiento-avisa-no-decide: una fila con `vence:` pasado se señala,
# sin que la vista la firme/cierre. Fixture mínimo porque el árbol real
# no tiene hoy ninguna fila `ABIERTA` con `vence:` ya vencido (P5 lo
# permite cuando el caso lo exige: no hay control negativo vigente para
# esta rama sin fabricar la fecha).
# ───────────────────────────────────────────────────────────────

def t_vencimiento_avisa_no_decide():
    caso = "t_vencimiento_avisa_no_decide"
    fila = {
        "id": "FP-9999", "creado": "2020-01-01", "estado": "ABIERTA",
        "qué_se_firma": "caso sintético de vencimiento", "gatea": "vence: 2020-01-08",
        "dónde": "fixture", "encargo": "fixture",
    }
    r = D._fp_a_fila_mesa(fila, _hoy(), D.Cuenta(), 0)
    _afirma(r["vencida"], caso, "una fila con `vence:` en el pasado debe marcarse vencida")
    _afirma("VENCIDA" in r["vence"], caso, "el texto debe señalar VENCIDA")
    _afirma(r["abierta"], caso,
           "el vencimiento NO debe cambiar `abierta` -- la vista avisa, no decide")
    _afirma("Mesa decide" in r["quien"], caso,
           "una fila vencida sigue pidiendo decisión de mesa, no se autofirma")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def corre() -> list[str]:
    """Devuelve la lista de fallos (vacia = verde). La llama `tests/check.py`."""
    FALLOS.clear()
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:  # un test que revienta es un fallo, no un hueco
            _falla(fn.__name__, f"EXCEPCION {type(exc).__name__}: {exc}")
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    print(f"tests/test_digesto_mesa.py · {len(TESTS)} casos · "
          f"{len(TESTS) - len({f.split(':')[0] for f in fallos})} ok · {len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
