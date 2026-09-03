#!/usr/bin/env python3
"""Deriva capa2_manifiesto por fila de relaciones.tsv desde el manifiesto real.

Especificación completa (regla derivada del corpus, qué pasa con las 68
SI_O_REFERENCIADO): forense/notas/2026-08-13-v2-via-capa2.md.

Regla, probada sin excepción sobre las 197 filas actuales: una fila es `SI`
cuando su `id_manifiesto` resuelve a una entrada real de `data/manifiesto.yaml`
con payload íntegro (sha256/tamaño verificados contra disco) -- el mismo
límite que ya separa las 24 `SI` de hoy de las otras 173. Esta vía NO
promueve `SI_O_REFERENCIADO`/`NO_REFERENCIADO` a `SI` por coincidencia de
nombre de fuente (prohibido por la jerarquía de evidencia de MAP-B/PR#189)
-- solo reporta, como diagnóstico auxiliar para revisión humana, qué filas
sin `id_manifiesto` propio tienen una fuente con alguna presencia conocida
en el manifiesto vía `data/inventarios/alias-fuentes.yaml`.

Modo lectura por defecto. --escribe aplica los diffs propuestos a
relaciones.tsv fila por fila, en sitio, sin reordenar el archivo -- y, en las
filas que promueve a `SI` con `estado == "COINCIDE"`, escribe también
`capa3_disco_real = EXISTE;COINCIDE;INTEGRO`, que es lo que esa verificación
literalmente afirma. Sin eso, cada promoción rompía la biyección
capa2<->capa3 y dejaba una reconciliación manual detrás (medido en ENLACE-2,
PR #236: 8 promociones, 8 desacuerdos). Ver aplicar_diffs().

Sale con código 1 (sin escribir nada) si el desglose de estados de
verificación da COINCIDE=0 habiendo >=1 fila con id_manifiesto -- señal de
que data/raw no está montada, no de que ya no queda nada por promover.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

try:
    from .baseline import NO_DETERMINADO, leer_tsv
except ImportError:  # ejecución directa
    from baseline import NO_DETERMINADO, leer_tsv

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML no disponible.", file=sys.stderr)
    raise


def cargar_manifiesto(manifiesto_path: Path) -> list[dict]:
    if not manifiesto_path.exists():
        return []
    texto = manifiesto_path.read_text(encoding="utf-8")
    lineas = texto.split("\n")
    i = 0
    while i < len(lineas) and (lineas[i].startswith("#") or not lineas[i].strip()):
        i += 1
    cuerpo = "\n".join(lineas[i:])
    return yaml.safe_load(cuerpo) or []


def cargar_raices(root: Path) -> dict[str, str]:
    ruta = root / "data" / "raices.local.yaml"
    if not ruta.exists():
        return {}
    datos = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    return {k: v for k, v in datos.items() if k != "data_raw"}


def cargar_alias(alias_path: Path) -> dict[str, set[str]]:
    """fuente_canonica_normalizada (tal cual aparece en relaciones.tsv, en
    mayúsculas) -> conjunto de formas conocidas (canónico + alias), en
    minúsculas -- para el diagnóstico auxiliar, nunca para escribir."""
    if not alias_path.exists():
        return {}
    datos = yaml.safe_load(alias_path.read_text(encoding="utf-8")) or []
    resultado: dict[str, set[str]] = {}
    for entrada in datos:
        canon = (entrada.get("canonico") or "").strip()
        if not canon:
            continue
        formas = {canon.lower()}
        for a in entrada.get("alias") or []:
            if a and a.strip():
                formas.add(a.strip().lower())
        resultado[canon.upper()] = formas
    return resultado


def _sin_acentos(s: str) -> str:
    """Minúsculas sin diacríticos -- 'latinobarómetro' -> 'latinobarometro'."""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def _con_frontera_de_letra(forma: str, texto: str) -> bool:
    """True si `forma` aparece en `texto` sin quedar embebida dentro de una
    palabra más larga: el carácter inmediato anterior/posterior, si existe, no
    puede ser otra letra a-z (dígitos/guion_bajo/espacio/puntuación sí cuentan
    como frontera válida -- necesario para casar 'latinobarometro' contra
    'latinobarometro2024_bd_stata', donde el año sigue sin separador). Ambos
    argumentos ya en minúsculas y sin acentos (ver `_sin_acentos`)."""
    if not forma:
        return False
    patron = re.compile(r"(?<![a-z])" + re.escape(forma) + r"(?![a-z])")
    return patron.search(texto) is not None


def sha256_de(path: Path, buf_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(buf_size), b""):
            h.update(chunk)
    return h.hexdigest()


def verificar_entrada(entrada: dict, root: Path, raices: dict[str, str]) -> str:
    """COINCIDE | NO_COINCIDE | AUSENTE | SIN_PAYLOAD | RAIZ_NO_CONFIGURADA."""
    archivo = entrada.get("archivo")
    if not archivo:
        return "SIN_PAYLOAD"
    raiz_nombre = entrada.get("raiz")
    if raiz_nombre:
        base = raices.get(raiz_nombre)
        if base is None:
            return "RAIZ_NO_CONFIGURADA"
        ruta = Path(base) / archivo
    else:
        ruta = root / "data" / "raw" / archivo
    if not ruta.exists():
        return "AUSENTE"
    sha_esperado = entrada.get("sha256")
    tam_esperado = entrada.get("tamano_bytes")
    if sha256_de(ruta) != sha_esperado or ruta.stat().st_size != tam_esperado:
        return "NO_COINCIDE"
    return "COINCIDE"


ESTADOS_VERIFICACION = ("COINCIDE", "NO_COINCIDE", "AUSENTE", "SIN_PAYLOAD", "RAIZ_NO_CONFIGURADA")

# El valor de capa3_disco_real que acompaña a capa2_manifiesto=SI en
# relaciones.tsv, sin excepción. No se inventa aquí: se lee del archivo (las
# 51 filas SI de hoy lo llevan) y afirma exactamente lo que verifica
# verificar_entrada() == "COINCIDE" -- existe en disco, sha256 y tamaño
# coinciden. Ver aplicar_diffs() para por qué la vía lo escribe.
CAPA3_INTEGRO = "EXISTE;COINCIDE;INTEGRO"


def derivar(root: Path) -> dict:
    relaciones_path = root / "data" / "curacion-registro" / "relaciones.tsv"
    manifiesto_path = root / "data" / "manifiesto.yaml"
    alias_path = root / "data" / "inventarios" / "alias-fuentes.yaml"

    filas = leer_tsv(relaciones_path)
    manifiesto = cargar_manifiesto(manifiesto_path)
    por_id = {e["id"]: e for e in manifiesto if e.get("id")}
    raices = cargar_raices(root)
    alias = cargar_alias(alias_path)
    texto_manifiesto = " | ".join(
        f"{e.get('usado_para', '')} {e.get('archivo', '')}".lower() for e in manifiesto
    )
    texto_manifiesto_norm = _sin_acentos(texto_manifiesto)

    diffs: list[dict] = []
    diagnostico: list[dict] = []
    estados_verificacion: dict[str, int] = dict.fromkeys(ESTADOS_VERIFICACION, 0)
    filas_con_id_manifiesto = 0
    for f in filas:
        actual = f.get("capa2_manifiesto", "")
        idm = f.get("id_manifiesto", NO_DETERMINADO)
        if idm != NO_DETERMINADO:
            filas_con_id_manifiesto += 1
            # FP-246 (ACTO MAESTRA37-N2, 3/sep/2026): `id_manifiesto` puede
            # traer una LISTA de ids separada por `;` (6 filas hoy, 29
            # payloads -- INE, IEC_COAHUILA, IEEM_EDOMEX, IEEBC_BC,
            # IEEZ_ZACATECAS, IEECH_CHIHUAHUA). Antes, `por_id.get(idm)` con
            # `idm` la cadena completa `;`-unida nunca resolvía -- esas 6
            # filas caían siempre en ID_NO_EN_MANIFIESTO sin que ninguno de
            # sus ids individuales se examinara. Ahora cada id se resuelve
            # por separado y la fila se enumera id por id (A.1, no se
            # colapsa a un solo estado) -- `estados_por_id` en el diff.
            ids = [pedazo for pedazo in idm.split(";") if pedazo]
            estados_por_id: dict[str, str] = {}
            for id_unico in ids:
                entrada = por_id.get(id_unico)
                if entrada is None:
                    estados_por_id[id_unico] = "ID_NO_EN_MANIFIESTO"
                else:
                    estado_id = verificar_entrada(entrada, root, raices)
                    estados_por_id[id_unico] = estado_id
                    # El contador agregado (`estados_verificacion`) solo
                    # cuenta estados de ids que SÍ están en el manifiesto --
                    # mismo criterio que la rama de un solo id de antes.
                    estados_verificacion[estado_id] += 1
            if len(ids) == 1:
                estado = estados_por_id[ids[0]]
            else:
                estado = ("COINCIDE" if all(v == "COINCIDE" for v in estados_por_id.values())
                           else "LISTA_" + "|".join(f"{k}={v}" for k, v in estados_por_id.items()))
            # La fila solo se promueve a SI cuando TODOS los ids de la
            # lista coinciden -- una lista con un solo id ausente no basta
            # para afirmar capa2_manifiesto=SI de toda la fila.
            derivado = "SI" if all(v == "COINCIDE" for v in estados_por_id.values()) else actual
            if derivado != actual:
                diffs.append({
                    "relacion_id": f["relacion_id"],
                    "necesidad_id": f["necesidad_id"],
                    "fuente_canonica_normalizada": f["fuente_canonica_normalizada"],
                    "actual": actual,
                    "derivado": derivado,
                    "estado": estado,
                    "capa3_actual": f.get("capa3_disco_real", ""),
                    "razon": (f"id_manifiesto={idm} estado={estado}" if len(ids) == 1
                              else "id_manifiesto (lista de %d ids)=%s; por id: %s" % (
                                  len(ids), idm,
                                  ", ".join(f"{k}={v}" for k, v in estados_por_id.items()))),
                })
        else:
            fc = f["fuente_canonica_normalizada"]
            formas = alias.get(fc.upper(), {fc.lower()})
            formas_norm = {_sin_acentos(forma) for forma in formas if forma}
            if any(_con_frontera_de_letra(forma, texto_manifiesto_norm) for forma in formas_norm):
                diagnostico.append({
                    "relacion_id": f["relacion_id"],
                    "necesidad_id": f["necesidad_id"],
                    "fuente_canonica_normalizada": fc,
                    "capa2_actual": actual,
                })

    return {
        "total_filas": len(filas),
        "diffs_propuestos": diffs,
        "diagnostico_candidatas_sin_id": diagnostico,
        "estados_verificacion": estados_verificacion,
        "filas_con_id_manifiesto": filas_con_id_manifiesto,
    }


def aplicar_diffs(relaciones_path: Path, diffs: list[dict]) -> int:
    """Reescribe capa2_manifiesto de las filas con diff y, cuando la promoción
    es a `SI` con `estado == "COINCIDE"`, también capa3_disco_real --
    preserva orden y todas las demás columnas, nunca reordena el archivo.
    Devuelve cuántas celdas de capa3 escribió.

    Por qué capa3 va aquí y no en un acto aparte (ADR de B2, 14/ago/2026):
    `capa2_manifiesto` y `capa3_disco_real` son biyectivos en `relaciones.tsv`
    sin una sola excepción, y esta función era la única forma de romperlo --
    escribía capa2 y dejaba capa3 atrás, así que cada promoción producía una
    fila `SI`|`SI_O_PARCIAL` que alguien tenía que reconciliar a mano después.
    Ocurrió, medido, en ENLACE-2 (PR #236): 8 filas promovidas, 8 desacuerdos
    creados en el mismo comando. El precedente de que eso cuesta un acto
    propio es CAPA3-RECONCILIA (PR #202, 19 desacuerdos -> 0).

    `CAPA3_INTEGRO` no se inventa: es el valor que ya llevan las filas `SI` del
    archivo, y `verificar_entrada() == "COINCIDE"` es literalmente lo que ese
    valor afirma (existe en disco, sha256 y tamaño coinciden). Fuera de esa
    condición no se escribe capa3 -- una promoción que no venga de COINCIDE no
    existe hoy (`derivado = "SI" if estado == "COINCIDE"`), y si algún día
    existiera, esta función debe dejarla en paz en vez de adivinar."""
    por_id = {d["relacion_id"]: d for d in diffs}
    with relaciones_path.open(encoding="utf-8-sig", newline="") as handle:
        lector = csv.DictReader(handle, delimiter="\t")
        campos = lector.fieldnames
        filas = list(lector)
    capa3_escritas = 0
    for fila in filas:
        d = por_id.get(fila["relacion_id"])
        if d is None:
            continue
        fila["capa2_manifiesto"] = d["derivado"]
        if (d["derivado"] == "SI" and d.get("estado") == "COINCIDE"
                and "capa3_disco_real" in fila
                and fila["capa3_disco_real"] != CAPA3_INTEGRO):
            fila["capa3_disco_real"] = CAPA3_INTEGRO
            capa3_escritas += 1
    with relaciones_path.open("w", encoding="utf-8", newline="") as handle:
        escritor = csv.DictWriter(handle, fieldnames=campos, delimiter="\t", lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)
    return capa3_escritas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("."),
                         help="Raíz del repo (por defecto, el directorio actual).")
    parser.add_argument("--escribe", action="store_true",
                         help="Aplica los diffs propuestos a relaciones.tsv en sitio. "
                              "Sin esta bandera, solo reporta (modo por defecto).")
    args = parser.parse_args()
    root = args.root.resolve()

    resultado = derivar(root)
    estados = resultado["estados_verificacion"]

    print(f"Filas en relaciones.tsv: {resultado['total_filas']}")
    print("Estados de verificación (verificar_entrada(), antes de diffs): "
          + " ".join(f"{e}={estados[e]}" for e in ESTADOS_VERIFICACION))
    print(f"Diffs propuestos (capa2_manifiesto): {len(resultado['diffs_propuestos'])}")
    for d in resultado["diffs_propuestos"]:
        print(f"  {d['relacion_id']} [{d['necesidad_id']}/{d['fuente_canonica_normalizada']}]: "
              f"{d['actual']} -> {d['derivado']} ({d['razon']})")

    diag = resultado["diagnostico_candidatas_sin_id"]
    print(f"\nDiagnóstico auxiliar -- filas SIN id_manifiesto cuya fuente ya tiene alguna "
          f"presencia conocida en el manifiesto (NO se promueven; candidatas a revisión "
          f"humana): {len(diag)}")
    for d in diag[:50]:
        print(f"  {d['relacion_id']} [{d['necesidad_id']}/{d['fuente_canonica_normalizada']}] "
              f"capa2_actual={d['capa2_actual']}")
    if len(diag) > 50:
        print(f"  … y {len(diag) - 50} más (no se trunca la cuenta, solo el listado impreso).")

    if args.escribe:
        if resultado["diffs_propuestos"]:
            capa3 = aplicar_diffs(root / "data" / "curacion-registro" / "relaciones.tsv",
                                   resultado["diffs_propuestos"])
            print(f"\n{len(resultado['diffs_propuestos'])} filas escritas en relaciones.tsv "
                  f"(capa2_manifiesto), de las cuales {capa3} llevaron también "
                  f"capa3_disco_real -> {CAPA3_INTEGRO}.")
        else:
            print("\n--escribe pasado, pero 0 diffs propuestos -- nada que escribir.")

    if estados["COINCIDE"] == 0 and resultado["filas_con_id_manifiesto"] >= 1:
        print("\ncero payloads verificables — ¿está data/raw montada?", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
