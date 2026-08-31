#!/usr/bin/env python3
"""ACTO MAESTRA32-E6 · ETIQUETA-v1_2 — COMMIT-2.

Dos reglas, aplicadas en el orden congelado por
`forense/notas/2026-08-30-etiqueta-v1_2-spec.md` (COMMIT-1):

  (a) Regla v1_1 — citada tal cual de
      `forense/notas/2026-08-27-etiqueta-regla.md` §2 (COMMIT-1 de
      `ACTO MAESTRA31-E7 · ETIQUETA`). Nunca se le aplicó a la capa FD
      (`data/inventario-fd-v1_0.tsv`); este acto es la primera vez.

  (b) Regla v1_2 — nueva, para los placeholders que la v1_1 deja sin
      resolver en cualquiera de las dos tablas: lee, con `yaml.safe_load`,
      los campos declarados de `data/manifiesto.yaml` para el `payload_id`
      (buscado por su campo `archivo`) y deriva `familia + año4` solo si
      alguno de esos campos trae, literal y adyacente (sin heurística de
      substring suelto), una familia canónica del corpus — lista cerrada
      tomada de los valores YA presentes en la columna `instrumento` de
      `data/inventario-reactivos-v1_1.tsv` — seguida de un año de 2 o 4
      dígitos. Si ningún campo declarado la trae, queda
      `(sin-instrumento-derivable)`; no se fuerza ninguna otra heurística
      (ni acrónimo inventado, ni vecino más parecido, ni conocimiento
      externo de qué encuesta es).

Entradas: `data/inventario-fd-v1_0.tsv`, `data/inventario-reactivos-v1_1.tsv`,
`data/manifiesto.yaml`. Salidas: `data/inventario-fd-v1_1.tsv`,
`data/inventario-reactivos-v1_2.tsv` (mismo esquema que sus predecesoras).

`tools/inventario_reactivos.py` NO se edita ni se importa — este script no
re-extrae nada, solo re-deriva la columna `instrumento` de dos tablas ya
producidas.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

FD_IN = REPO_ROOT / "data" / "inventario-fd-v1_0.tsv"
FD_OUT = REPO_ROOT / "data" / "inventario-fd-v1_1.tsv"
REACTIVOS_IN = REPO_ROOT / "data" / "inventario-reactivos-v1_1.tsv"
REACTIVOS_OUT = REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv"
MANIFIESTO = REPO_ROOT / "data" / "manifiesto.yaml"

PLACEHOLDER_RAIZ = "(raiz)"
PLACEHOLDER_SIN = "(sin-instrumento-derivable)"

# ---------------------------------------------------------------------------
# (a) Regla v1_1 — tabla citada tal cual de
# forense/notas/2026-08-27-etiqueta-regla.md §2. Orden de la tabla
# preservado (primera regex que hace match, gana).
# ---------------------------------------------------------------------------
REGLA_V1_1 = [
    ("encig", r"encig(\d{2,4})"),
    ("envipe", r"envipe(\d{4})"),
    ("enigh", r"enigh(\d{4})"),
    ("enif", r"enif_?(\d{4})"),
    ("enadid", r"enadid(\d{2})"),
    ("enestyc", r"enestyc_(\d{4})"),
    ("enut", r"enut(\d{4})"),
    ("encup", r"encup_?(\d{4})"),
    ("encoap", r"encoap_(\d{4})"),
    ("encuci", r"encuci(\d{4})"),
    ("cpv", r"cpv(\d{4})"),
    ("censo", r"censo(\d{4})"),
    ("enoen", r"enoen_(\d{4})"),
    ("enoe", r"enoe_(\d{4})"),
    ("iter", r"iter_nal_(\d{4})"),
]


def expand_year(y: str) -> str:
    if len(y) == 4:
        return y
    yy = int(y)
    return f"20{yy:02d}" if yy < 50 else f"19{yy:02d}"


def aplica_v1_1(payload_id: str) -> str | None:
    for familia, patron in REGLA_V1_1:
        m = re.search(patron, payload_id, re.IGNORECASE)
        if m:
            return f"{familia}{expand_year(m.group(1))}"
    return None


# ---------------------------------------------------------------------------
# (b) Regla v1_2
# ---------------------------------------------------------------------------
CAMPOS_MANIFIESTO = ["id", "usado_para", "nota", "url_origen"]  # orden de prioridad, declarado


def familias_canonicas(path_reactivos_v1_1: Path) -> list[str]:
    """Lista cerrada: stems de los valores YA presentes en `instrumento` de
    data/inventario-reactivos-v1_1.tsv (excluidos los dos placeholders)."""
    instrumentos: set[str] = set()
    with path_reactivos_v1_1.open(encoding="utf-8") as f:
        lineas = (l for l in f if not l.startswith("#"))
        for row in csv.DictReader(lineas, delimiter="\t"):
            v = row["instrumento"]
            if v not in (PLACEHOLDER_RAIZ, PLACEHOLDER_SIN):
                instrumentos.add(v)
    stems: set[str] = set()
    for v in instrumentos:
        m = re.match(r"^(.*?)_?(\d{2,4})$", v)
        stems.add(m.group(1).rstrip("_").lower() if m else v.lower())
    return sorted(stems, key=len, reverse=True)


def carga_manifiesto(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as f:
        entradas = yaml.safe_load(f)
    return {e["archivo"]: e for e in entradas if isinstance(e, dict) and e.get("archivo")}


def aplica_v1_2(payload_id: str, manifiesto: dict, familias: list[str]) -> tuple[str | None, str | None]:
    """Devuelve (instrumento derivado o None, campo del manifiesto que lo produjo o None)."""
    entrada = manifiesto.get(payload_id)
    if not entrada:
        return None, None
    for campo in CAMPOS_MANIFIESTO:
        texto = entrada.get(campo)
        if not isinstance(texto, str) or not texto:
            continue
        for familia in familias:
            patron = r"(?<![A-Za-z0-9_])" + re.escape(familia) + r"_?(\d{2,4})(?!\d)"
            m = re.search(patron, texto, re.IGNORECASE)
            if m:
                return f"{familia}{expand_year(m.group(1))}", campo
    return None, None


# ---------------------------------------------------------------------------
# I/O de tablas — misma convención que tools/inventario_reactivos.py:
# TSV plano sin comillas CSV, escritura manual por join de tabs.
# ---------------------------------------------------------------------------
def lee_filas(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(encoding="utf-8") as f:
        todas = f.readlines()
    no_comentario = [l for l in todas if not l.startswith("#")]
    reader = csv.DictReader(no_comentario, delimiter="\t")
    fields = reader.fieldnames
    filas = list(reader)
    return fields, filas


def escribe_filas(path: Path, cabecera_comentario: list[str], fields: list[str], filas: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        for linea in cabecera_comentario:
            handle.write(linea + "\n")
        handle.write("\t".join(fields) + "\n")
        for fila in filas:
            handle.write("\t".join(fila[c] for c in fields) + "\n")


def main() -> int:
    familias = familias_canonicas(REACTIVOS_IN)
    manifiesto = carga_manifiesto(MANIFIESTO)

    # ---------------- Capa FD: v1_0 -> v1_1 ----------------
    fd_fields, fd_filas = lee_filas(FD_IN)
    fd_via_v1_1 = 0
    fd_via_v1_2 = 0
    fd_sin_resolver = 0
    fd_payloads_v1_2 = {}
    for fila in fd_filas:
        if fila["instrumento"] != PLACEHOLDER_RAIZ:
            continue
        nuevo = aplica_v1_1(fila["payload_id"])
        if nuevo:
            fila["instrumento"] = nuevo
            fd_via_v1_1 += 1
            continue
        nuevo, campo = aplica_v1_2(fila["payload_id"], manifiesto, familias)
        if nuevo:
            fila["instrumento"] = nuevo
            fd_via_v1_2 += 1
            fd_payloads_v1_2[fila["payload_id"]] = (nuevo, campo)
            continue
        fila["instrumento"] = PLACEHOLDER_SIN
        fd_sin_resolver += 1

    cabecera_fd = [
        "# data/inventario-fd-v1_1.tsv -- ACTO MAESTRA32-E6 · ETIQUETA-v1_2, COMMIT-2",
        "# Sucesor de data/inventario-fd-v1_0.tsv (ADR-215). Primera vez que la capa FD recibe la regla v1_1"
        " (forense/notas/2026-08-27-etiqueta-regla.md, COMMIT-1 de MAESTRA31-E7) -- nunca se le habia aplicado.",
        "# Unico cambio: columna `instrumento` re-derivada para las filas que traian '(raiz)'. Regla v1_1 primero"
        " (regex sobre payload_id); lo que v1_1 no resuelve pasa por la regla v1_2 (forense/notas/2026-08-30-etiqueta-v1_2-spec.md,"
        " COMMIT-1 de MAESTRA32-E6) sobre campos declarados de data/manifiesto.yaml; lo que ninguna de las dos resuelve queda"
        " '(sin-instrumento-derivable)'. Cero re-extraccion: mismas filas, mismo sha256_12/archivo_miembro/variable_id/"
        "texto_reactivo/metodo/universo_declarado byte a byte. tools/ no se edito.",
    ]
    escribe_filas(FD_OUT, cabecera_fd, fd_fields, fd_filas)

    # ---------------- Reactivos: v1_1 -> v1_2 (39 payloads) ----------------
    reactivos_fields, reactivos_filas = lee_filas(REACTIVOS_IN)

    reactivos_resueltos = 0
    reactivos_sin_resolver = 0
    reactivos_payloads_resueltos = {}
    reactivos_payloads_sin = set()
    for fila in reactivos_filas:
        if fila["instrumento"] != PLACEHOLDER_SIN:
            continue
        nuevo, campo = aplica_v1_2(fila["payload_id"], manifiesto, familias)
        if nuevo:
            fila["instrumento"] = nuevo
            reactivos_resueltos += 1
            reactivos_payloads_resueltos[fila["payload_id"]] = (nuevo, campo)
        else:
            reactivos_sin_resolver += 1
            reactivos_payloads_sin.add(fila["payload_id"])

    n_payloads_39 = len(reactivos_payloads_resueltos) + len(reactivos_payloads_sin)
    pct = 100 * len(reactivos_payloads_resueltos) / n_payloads_39 if n_payloads_39 else 0.0
    falsador_disparado = pct < 50.0

    cabecera_reactivos = [
        "# data/inventario-reactivos-v1_2.tsv -- ACTO MAESTRA32-E6 · ETIQUETA-v1_2, COMMIT-2",
        "# Sucesor de data/inventario-reactivos-v1_1.tsv (ADR-216, sucesora a su vez de v1_0/ADR-213). Regla v1_2"
        " (forense/notas/2026-08-30-etiqueta-v1_2-spec.md, COMMIT-1) aplicada a las filas '(sin-instrumento-derivable)'"
        " (los 39 payloads que v1_1/ACTO MAESTRA31-E7 dejo honestamente sin resolver por regex de nombre):"
        f" {len(reactivos_payloads_resueltos)} de {n_payloads_39} payloads resueltos leyendo campos declarados"
        f" (id/usado_para/nota/url_origen) de data/manifiesto.yaml ({pct:.1f}%, bajo el 50% -- falsador de COMMIT-1(d)"
        " disparado, declarado en la nota de cierre, no se itera).",
        "# Cero re-extraccion: mismas 178246 filas, mismo payload_id/sha256_12/archivo_miembro/variable_id/texto_reactivo/"
        "metodo/universo_declarado byte a byte que v1_1. Columna `ola` sin tocar (NO_DETERMINADO, constante del extractor)."
        " tools/inventario_reactivos.py no se edito ni se importo.",
    ]
    escribe_filas(REACTIVOS_OUT, cabecera_reactivos, reactivos_fields, reactivos_filas)

    # ---------------- Control positivo ----------------
    def filas_no_placeholder(path: Path, placeholder_col_valores: set[str]) -> list[str]:
        fields, filas = lee_filas(path)
        return [
            "\t".join(fila[c] for c in fields)
            for fila in filas
            if fila["instrumento"] not in placeholder_col_valores
        ]

    fd_v0_no_raiz = filas_no_placeholder(FD_IN, {PLACEHOLDER_RAIZ})
    fd_v1_fields, fd_v1_filas_check = lee_filas(FD_OUT)
    fd_v1_lineas_por_payload_var = {
        (f["payload_id"], f["variable_id"], f["archivo_miembro"]): "\t".join(f[c] for c in fd_v1_fields)
        for f in fd_v1_filas_check
    }
    fd_control_diffs = 0
    for linea in fd_v0_no_raiz:
        partes = linea.split("\t")
        clave = (partes[0], partes[5], partes[4])  # payload_id, variable_id, archivo_miembro
        if fd_v1_lineas_por_payload_var.get(clave) != linea:
            fd_control_diffs += 1

    reactivos_v1_no_sin = filas_no_placeholder(REACTIVOS_IN, {PLACEHOLDER_SIN})
    reactivos_v2_fields, reactivos_v2_filas_check = lee_filas(REACTIVOS_OUT)
    reactivos_v2_lineas = {
        "\t".join(f[c] for c in reactivos_v2_fields) for f in reactivos_v2_filas_check
    }
    reactivos_control_diffs = sum(1 for linea in reactivos_v1_no_sin if linea not in reactivos_v2_lineas)

    resumen = {
        "familias_canonicas_v1_2": familias,
        "fd": {
            "raiz_antes": fd_via_v1_1 + fd_via_v1_2 + fd_sin_resolver,
            "resueltos_via_v1_1": fd_via_v1_1,
            "resueltos_via_v1_2": fd_via_v1_2,
            "payloads_via_v1_2": fd_payloads_v1_2,
            "sin_instrumento_derivable_despues": fd_sin_resolver,
            "control_positivo_filas_comparadas": len(fd_v0_no_raiz),
            "control_positivo_diferencias": fd_control_diffs,
        },
        "reactivos": {
            "payloads_39_resueltos": len(reactivos_payloads_resueltos),
            "payloads_39_totales": n_payloads_39,
            "porcentaje_resuelto": round(pct, 2),
            "falsador_menos_de_50pct_disparado": falsador_disparado,
            "filas_resueltas": reactivos_resueltos,
            "filas_sin_resolver_despues": reactivos_sin_resolver,
            "payloads_resueltos_detalle": reactivos_payloads_resueltos,
            "control_positivo_filas_comparadas": len(reactivos_v1_no_sin),
            "control_positivo_diferencias": reactivos_control_diffs,
        },
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
