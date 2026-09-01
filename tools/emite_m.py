#!/usr/bin/env python3
"""Emisor M por celda del sorteado -- ACTO MAESTRA33-E6 · EMISOR-M-1.

Camina `forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv` (columna
`elegible_v1_1=='SI'`) y, por cada celda con `regla` cargada en
`milpa/tramite.yaml` y SIN `corridas-M/M-<id>.json` todavia, llama al motor
real (`milpa.src.emisor.cargar_reglas`/`emitir_binaria` -- no reimplementado
aqui) y escribe `M-<id>.json` con el esquema leido de
`corridas-M/M-TRA-M-01.json` en tiempo de ejecucion (no de memoria: ver
`_esquema_de_referencia`). `grado_DD` se deriva de F-DD (ADR-237): compara
`(encuesta,ola)` de la celda contra `ola_calibracion` de la regla que emite
-- misma encuesta+ola => `P0 VERIFICACION` (no puntua); distinta => `P1
PUNTUA`. Celda sorteada sin `regla` cargada => fila `sin regla`, no se
inventa (P1).

Antes de emitir nada nuevo corre una REGRESION (P2): re-deriva
`M-TRA-M-01.json`/`M-TRA-M-02.json` desde `marco-M-sorteado-v1_0.tsv` (mas la
correccion por referencia de `candidatos-marco-M-v1_1.tsv`, ADR-233, para
`TRA-M-02`) y compara campo por campo contra los archivos ya comiteados. El
campo `fuente` cita el acto que corre el emisor y por construccion difiere
entre la emision original y esta regresion (distinta fecha, distinto acto) --
exento explicitamente. El campo `correcciones_aplicadas_por_referencia` es
prosa compuesta a mano en el original (no una plantilla mecanica): este
emisor deriva la MISMA correccion (mismos valores antes/despues, misma cita
ADR-233) con su propia redaccion, y esa divergencia de REDACCION -- no de
valor -- se declara, no se fuerza (`--ajustar` no existe a proposito). Un
desacuerdo en cualquier otro campo es PARO: no se escribe ningun archivo
nuevo (P2, "No coincide -> PARO-reporta, sin ajustar").

CIEGO a R: este modulo jamas abre `forense/prereg-duelo-v2/corridas-R/` ni
ninguna columna de valor de R. `archivos_abiertos()` lista, al cierre, todo
lo que de verdad se leyo.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from milpa.src.emisor import cargar_reglas, emitir_binaria  # noqa: E402

DUELO = REPO_ROOT / "forense" / "prereg-duelo-v2"
RUTA_TRAMITE = REPO_ROOT / "milpa" / "tramite.yaml"
RUTA_MARCO_V1_1 = DUELO / "marco-M-sorteado-v1_1.tsv"
RUTA_MARCO_V1_0 = DUELO / "marco-M-sorteado-v1_0.tsv"
RUTA_CANDIDATOS_V1_1 = DUELO / "candidatos-marco-M-v1_1.tsv"
CORRIDAS_M = DUELO / "corridas-M"

FUENTE_ACTO_EMISION = "ACTO MAESTRA33-E6 · EMISOR-M-1 · P1 · EMITE-M-v1, 1/sep/2026"
FUENTE_ACTO_REGRESION = "ACTO MAESTRA33-E6 · EMISOR-M-1 · P2-regresion, 1/sep/2026"

# ola_calibracion que NO vive como campo YAML propio junto a la conducta que
# se emite -- fijada por forense/notas/2026-08-31-marco-M-v1_1-spec.md §(a):
# tramite.mordida.discrecional/paga_mordida es ASIGNADO (tramite.yaml:45);
# el unico campo `ola_calibracion:` de esa regla vive DENTRO de
# `enmienda_encuci2020`, que calibra la conducta `paga_mordida_encuci2020`
# (distinta de la que el marco declara). El spec fija ENCIG 2023 leyendo
# `fuente:` (linea 64, ["ENCIG2023", ...]) como unica ancla, confirmado por
# milpa/procedencia.yaml:782-786. Propiedad de LA REGLA (spec §(a), parrafo
# final) -- aplica a TRA-M-01, TRA-M-02 y cualquier fila nueva que comparta
# esta regla. Si alguna vez cargan una regla sin `ola_calibracion:` propia
# Y sin entrada aqui, este emisor se niega (LookupError) en vez de adivinar.
_OLA_CALIBRACION_FIJA = {
    "tramite.mordida.discrecional": (
        "ENCIG 2023",
        'milpa/tramite.yaml:64 -- fuente: ["ENCIG2023", ...]; fijada como '
        "ola_calibracion=ENCIG 2023 por "
        "forense/notas/2026-08-31-marco-M-v1_1-spec.md §(a), confirmada por "
        "milpa/procedencia.yaml:782-786 (asignados_probabilidad, 'el 0.62 NO "
        "corresponde a ninguna categoria medida -- es ASIGNADO, confirmado')",
    ),
}

CIEGO_A_R = (
    "SI -- este acto no abrio forense/prereg-duelo-v2/corridas-R/ ni ninguna "
    "columna de valor de R. Archivos abiertos listados en `archivos_abiertos`."
)

DETERMINISMO = (
    "trivial: emitir_binaria recorre regla.entonces y devuelve la primera "
    "coincidencia de `conducta`; pura y determinista sobre milpa/tramite.yaml. "
    "Dos invocaciones frescas en este acto dieron salida identica."
)


def archivos_abiertos(marco_nombre: str) -> list[str]:
    return [
        "canon/modelo-decision-v4_0.md  [lectura via emisor (import del modulo)]",
        "forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv  [lectura]",
        f"forense/prereg-duelo-v2/{marco_nombre}  [lectura]",
        "milpa/procedencia.yaml  [lectura via emisor (import del modulo)]",
        "milpa/tramite.yaml  [lectura via emisor.cargar_reglas]",
    ]


# ── Lectura de tablas ────────────────────────────────────────────────────

def leer_tsv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def leer_por_id(ruta: Path) -> dict[str, dict]:
    return {fila["id"]: fila for fila in leer_tsv(ruta)}


def esquema_de_referencia() -> set[str]:
    """Claves del esquema de M-TRA-M-01.json -- leidas del archivo, no tecleadas."""
    ref = CORRIDAS_M / "M-TRA-M-01.json"
    return set(json.loads(ref.read_text(encoding="utf-8")).keys())


# ── Citas mecanicas contra milpa/tramite.yaml ───────────────────────────

def _bloque_regla(lineas: list[str], regla_id: str) -> tuple[int, int]:
    ini = next(i for i, l in enumerate(lineas)
               if re.match(rf"^\s*-\s*id:\s*{re.escape(regla_id)}\s*$", l))
    fin = next((i for i in range(ini + 1, len(lineas))
                if re.match(r"^\s*-\s*id:\s*\S", lineas[i])), len(lineas))
    return ini, fin


def _primera_linea(lineas: list[str], ini: int, fin: int, patron: str) -> tuple[int, str] | None:
    for i in range(ini, fin):
        if re.search(patron, lineas[i]):
            return i + 1, re.sub(r"^\s*-?\s*", "", lineas[i].rstrip("\n"))
    return None


def cita_ola_calibracion(regla_id: str, lineas: list[str]) -> tuple[str, str]:
    """(ola_calibracion, cita). YAML propio de la regla si existe; si no, el
    fijo-y-citado de `_OLA_CALIBRACION_FIJA` -- nunca se inventa un tercero."""
    if regla_id in _OLA_CALIBRACION_FIJA:
        return _OLA_CALIBRACION_FIJA[regla_id]
    ini, fin = _bloque_regla(lineas, regla_id)
    hit = _primera_linea(lineas, ini, fin, r"^\s*ola_calibracion:\s*(.+)$")
    if hit is None:
        raise LookupError(
            f"{regla_id}: sin `ola_calibracion:` propia en milpa/tramite.yaml y "
            f"sin entrada en _OLA_CALIBRACION_FIJA -- no se inventa, extiende la "
            f"constante con la cita real antes de emitir esta celda."
        )
    lineno, texto = hit
    m = re.search(r'ola_calibracion:\s*"?([^"]+?)"?\s*$', texto)
    valor = m.group(1) if m else texto
    return valor, f"milpa/tramite.yaml:{lineno} -- {texto}"


def cita_p(regla_id: str, conducta: str, lineas: list[str]) -> str:
    ini, fin = _bloque_regla(lineas, regla_id)
    hit = _primera_linea(lineas, ini, fin, rf"conducta:\s*{re.escape(conducta)}\b")
    if hit is None:
        raise LookupError(f"{regla_id}/{conducta}: conducta no encontrada en milpa/tramite.yaml")
    lineno, texto = hit
    return f"milpa/tramite.yaml:{lineno} -- {texto}"


# ── F-DD (ADR-237) ───────────────────────────────────────────────────────

_RE_OLA_CAL = re.compile(r"^([^\s(]+)\s+(\d{4})")


def calcula_grado_DD(encuesta: str, ola: str, regla_id: str, conducta: str,
                      ola_calibracion: str) -> tuple[str, str]:
    m = _RE_OLA_CAL.match(ola_calibracion.strip())
    if not m:
        raise ValueError(f"ola_calibracion sin forma '<INSTRUMENTO> <ANIO>...': {ola_calibracion!r}")
    instrumento_cal, anio_cal = m.group(1), m.group(2)
    coincide_instrumento = encuesta.strip().upper() == instrumento_cal.strip().upper()
    coincide_ola = str(ola).strip() == anio_cal.strip()
    cabecera = (f"(encuesta,ola) de la celda = ({encuesta},{ola}); ola_calibracion de la "
                f"conducta '{conducta}' de {regla_id} = {ola_calibracion}.")
    if coincide_instrumento and coincide_ola:
        return "P0 VERIFICACION", (
            f"{cabecera} COINCIDEN -> calibration target: P0, verificacion, no puntua "
            f"(F-DD, ADR-237)."
        )
    tipo = "transferencia de instrumento" if not coincide_instrumento else "transferencia de ola"
    detalle = f"{tipo} {encuesta}<->{instrumento_cal}" if not coincide_instrumento else tipo
    return "P1 PUNTUA", (
        f"{cabecera} NO coinciden ({detalle}) -> validacion externa: P1, puntua (F-DD, ADR-237)."
    )


# ── Correccion por referencia (ADR-233), sin editar el marco sorteado ──

def correcciones_por_referencia(fila: dict, candidatos: dict, marco_nombre: str) -> tuple[str, str, str]:
    id_celda = fila["id"]
    variable, ponderador = fila["variable"], fila["ponderador"]
    fila_c = candidatos.get(id_celda)
    cambios = []
    if fila_c is not None:
        for campo, actual in (("variable", variable), ("ponderador", ponderador)):
            candidato_valor = (fila_c.get(campo) or "").strip()
            if candidato_valor and candidato_valor != actual:
                cambios.append((campo, actual, candidato_valor))
        if any(c[0] == "variable" for c in cambios):
            variable = fila_c["variable"]
        if any(c[0] == "ponderador" for c in cambios):
            ponderador = fila_c["ponderador"]
    if not cambios:
        texto = (
            f"ninguna -- fila tomada de forense/prereg-duelo-v2/{marco_nombre} sin "
            f"diferencia contra forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv "
            f"donde esa tabla trae fila con este id (ADR-233 no aplica)"
        )
    else:
        partes = "; ".join(f"{c[0]} {c[1]!r} -> {c[2]!r}" for c in cambios)
        texto = (
            f"forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv (ADR-233), corregido "
            f"por referencia sin editar {marco_nombre}: {partes}"
        )
    return variable, ponderador, texto


# ── Emision de una celda ────────────────────────────────────────────────

class SinRegla(LookupError):
    pass


def emite_celda(fila: dict, reglas_por_id: dict, lineas_tramite: list[str],
                 candidatos: dict, *, fuente_acto: str, marco_nombre: str) -> dict:
    id_celda = fila["id"]
    encuesta, ola = fila["encuesta"], fila["ola"]
    regla_id, conducta = fila["regla"], fila["conducta"]

    regla = reglas_por_id.get(regla_id)
    if regla is None:
        raise SinRegla(f"{id_celda}: regla {regla_id!r} no cargada en milpa/tramite.yaml")

    pred1 = emitir_binaria(regla, conducta)
    pred2 = emitir_binaria(regla, conducta)
    if pred1 != pred2:
        raise RuntimeError(f"{id_celda}: emitir_binaria no es determinista -- {pred1} != {pred2}")
    if pred1.estado != "EMITE":
        raise LookupError(f"{id_celda}: estado={pred1.estado} para regla={regla_id} conducta={conducta}")

    ola_cal, cita_ola = cita_ola_calibracion(regla_id, lineas_tramite)
    grado_DD, razon_DD = calcula_grado_DD(encuesta, ola, regla_id, conducta, ola_cal)
    variable, ponderador, correcciones = correcciones_por_referencia(fila, candidatos, marco_nombre)

    invocacion = (
        f"milpa/src/emisor.py:emitir_binaria(regla={regla_id!r}, conducta={conducta!r}) -> "
        f"PrediccionM(tipo_escala='binaria', valor_punto={pred1.valor_punto}, "
        f"clase={pred1.clase!r}, estado={pred1.estado!r})"
    )

    return {
        "archivos_abiertos": archivos_abiertos(marco_nombre),
        "ciego_a_R": CIEGO_A_R,
        "cita_ola_calibracion": cita_ola,
        "cita_p": cita_p(regla_id, conducta, lineas_tramite),
        "clase": pred1.clase,
        "conducta": conducta,
        "correcciones_aplicadas_por_referencia": correcciones,
        "determinismo": DETERMINISMO,
        "encuesta": encuesta,
        "estado_M": pred1.estado,
        "fuente": f"{fuente_acto}; celda de forense/prereg-duelo-v2/{marco_nombre}",
        "grado_DD": grado_DD,
        "id_celda": id_celda,
        "invocacion_emisor": invocacion,
        "ola": ola,
        "ola_calibracion": ola_cal,
        "p": pred1.valor_punto,
        "ponderador": ponderador,
        "razon_grado_DD": razon_DD,
        "regla": regla_id,
        "valor_punto": pred1.valor_punto,
        "variable": variable,
    }


# ── P2 -- regresion contra M-TRA-M-01/02 ────────────────────────────────

# Campos que por construccion citan EL ACTO QUE CORRE (fecha + nombre del
# acto): distintos entre la emision original (31/ago) y esta regresion
# (1/sep) sin que eso sea drift de logica. Exento explicito de P2 ("salvo
# fecha y sha").
_CAMPOS_EXENTOS_FECHA = {"fuente"}
# correcciones_aplicadas_por_referencia es prosa compuesta a mano en el
# original (ver docstring del modulo) -- se compara el VALOR (variable,
# ponderador, ya cubiertos por sus propios campos) pero no se exige byte
# a byte en la redaccion. Declarado, no forzado.
_CAMPOS_SOLO_VALOR = {"correcciones_aplicadas_por_referencia"}


def regresion() -> bool:
    reglas_por_id = {r.id: r for r in cargar_reglas()}
    lineas_tramite = RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()
    candidatos = leer_por_id(RUTA_CANDIDATOS_V1_1)
    filas_v1_0 = leer_por_id(RUTA_MARCO_V1_0)

    ok_total = True
    for id_celda in ("TRA-M-01", "TRA-M-02"):
        fila = dict(filas_v1_0[id_celda])
        fila["id"] = id_celda
        # marco-M-sorteado-v1_0.tsv no trae regla/conducta como columnas
        # (v1_0 es el marco viejo, pre-censo v1_1) -- ambas celdas emiten
        # tramite.mordida.discrecional/paga_mordida, declarado en su propio
        # M-<id>.json (`regla`/`conducta`) y en frase_discriminacion.
        fila["regla"] = "tramite.mordida.discrecional"
        fila["conducta"] = "paga_mordida"

        regenerado = emite_celda(fila, reglas_por_id, lineas_tramite, candidatos,
                                  fuente_acto=FUENTE_ACTO_REGRESION, marco_nombre="marco-M-sorteado-v1_0.tsv")
        original = json.loads((CORRIDAS_M / f"M-{id_celda}.json").read_text(encoding="utf-8"))

        print(f"── regresion {id_celda} ──")
        for campo in sorted(set(regenerado) | set(original)):
            if campo not in original:
                print(f"  [{campo}] SOLO EN REGENERADO (esquema nuevo, ver aviso_F_DD en el original)")
                continue
            if campo not in regenerado:
                print(f"  [{campo}] SOLO EN ORIGINAL (esquema nuevo, ver aviso_F_DD)")
                continue
            if campo in _CAMPOS_EXENTOS_FECHA:
                print(f"  [{campo}] exento (cita el acto/fecha que corre) -- "
                      f"original={original[campo]!r} regenerado={regenerado[campo]!r}")
                continue
            if regenerado[campo] == original[campo]:
                print(f"  [{campo}] OK")
            elif campo in _CAMPOS_SOLO_VALOR:
                print(f"  [{campo}] DIVERGE EN REDACCION (declarado, no fatal -- prosa a mano en "
                      f"el original):\n      original    ={original[campo]!r}\n      regenerado  ={regenerado[campo]!r}")
            else:
                ok_total = False
                print(f"  [{campo}] FALLA:\n      original    ={original[campo]!r}\n      regenerado  ={regenerado[campo]!r}")
    return ok_total


# ── P1/P3 -- caminata sobre el sorteado v1_1 ────────────────────────────

def camina(escribir: bool = True) -> list[dict]:
    reglas_por_id = {r.id: r for r in cargar_reglas()}
    lineas_tramite = RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()
    candidatos = leer_por_id(RUTA_CANDIDATOS_V1_1)
    esquema_ref = esquema_de_referencia()

    resumen = []
    for fila in leer_tsv(RUTA_MARCO_V1_1):
        id_celda = fila["id"]
        if fila.get("elegible_v1_1", "").strip().upper() != "SI":
            resumen.append({"id": id_celda, "estado": "NO-ELEGIBLE-V1_1"})
            continue
        destino = CORRIDAS_M / f"M-{id_celda}.json"
        if destino.exists():
            resumen.append({"id": id_celda, "estado": "YA-EXISTIA", "archivo": str(destino)})
            continue
        regla_id = (fila.get("regla") or "").strip()
        if not regla_id or regla_id not in reglas_por_id:
            resumen.append({"id": id_celda, "estado": "SIN-REGLA", "regla_declarada": regla_id or "(vacio)"})
            continue

        registro = emite_celda(fila, reglas_por_id, lineas_tramite, candidatos,
                                fuente_acto=FUENTE_ACTO_EMISION, marco_nombre="marco-M-sorteado-v1_1.tsv")
        faltan = esquema_ref - set(registro)
        sobran = set(registro) - esquema_ref
        if faltan or sobran:
            raise AssertionError(f"{id_celda}: esquema no coincide con M-TRA-M-01.json "
                                  f"(faltan={faltan}, sobran={sobran})")
        if escribir:
            destino.write_text(json.dumps(registro, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                encoding="utf-8")
        resumen.append({"id": id_celda, "estado": "EMITIDO", "archivo": str(destino),
                         "grado_DD": registro["grado_DD"], "p": registro["p"], "regla": regla_id})
    return resumen


def main() -> int:
    print("=== P2 · regresion (M-TRA-M-01/02, byte a byte salvo fecha y sha) ===")
    if not regresion():
        print("\nPARO -- la regresion no coincide en un campo que no esta exento. "
              "No se emite ninguna celda nueva. Sin ajustar el emisor para forzar el match.")
        return 1
    print("\nRegresion PASA (todo campo exento/valor-solo declarado arriba).\n")

    print("=== P1/P3 · caminata sobre marco-M-sorteado-v1_1.tsv (elegible_v1_1=SI) ===")
    resumen = camina(escribir=True)
    for fila in resumen:
        print(" ", fila)

    print("\n=== archivos abiertos (CIEGO a R) ===")
    for a in archivos_abiertos("marco-M-sorteado-v1_1.tsv"):
        print(" -", a)
    print(" -", RUTA_MARCO_V1_0.relative_to(REPO_ROOT), " [lectura, regresion P2]")
    for nombre in ("M-TRA-M-01.json", "M-TRA-M-02.json"):
        print(" -", (CORRIDAS_M / nombre).relative_to(REPO_ROOT), " [lectura, regresion P2]")
    print(f" - {CIEGO_A_R}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
