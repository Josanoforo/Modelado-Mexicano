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
relaciones.tsv fila por fila, en sitio, sin reordenar el archivo.

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
            entrada = por_id.get(idm)
            if entrada is None:
                estado, derivado = "ID_NO_EN_MANIFIESTO", actual
            else:
                estado = verificar_entrada(entrada, root, raices)
                estados_verificacion[estado] += 1
                derivado = "SI" if estado == "COINCIDE" else actual
            if derivado != actual:
                diffs.append({
                    "relacion_id": f["relacion_id"],
                    "necesidad_id": f["necesidad_id"],
                    "fuente_canonica_normalizada": f["fuente_canonica_normalizada"],
                    "actual": actual,
                    "derivado": derivado,
                    "razon": f"id_manifiesto={idm} estado={estado}",
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


def aplicar_diffs(relaciones_path: Path, diffs: list[dict]) -> None:
    """Reescribe solo el valor de capa2_manifiesto de las filas con diff --
    preserva orden y todas las demás columnas, nunca reordena el archivo."""
    derivado_por_id = {d["relacion_id"]: d["derivado"] for d in diffs}
    with relaciones_path.open(encoding="utf-8-sig", newline="") as handle:
        lector = csv.DictReader(handle, delimiter="\t")
        campos = lector.fieldnames
        filas = list(lector)
    for fila in filas:
        if fila["relacion_id"] in derivado_por_id:
            fila["capa2_manifiesto"] = derivado_por_id[fila["relacion_id"]]
    with relaciones_path.open("w", encoding="utf-8", newline="") as handle:
        escritor = csv.DictWriter(handle, fieldnames=campos, delimiter="\t", lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)


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
            aplicar_diffs(root / "data" / "curacion-registro" / "relaciones.tsv",
                           resultado["diffs_propuestos"])
            print(f"\n{len(resultado['diffs_propuestos'])} filas escritas en relaciones.tsv.")
        else:
            print("\n--escribe pasado, pero 0 diffs propuestos -- nada que escribir.")

    if estados["COINCIDE"] == 0 and resultado["filas_con_id_manifiesto"] >= 1:
        print("\ncero payloads verificables — ¿está data/raw montada?", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
