#!/usr/bin/env python3
"""Reglas deterministas compartidas por `/revisa`, `/despacha` y `/tramite`.

Nace de `ACTO RUTINAS-2 · COORDINACION-Y-REVISION-VIGENTE`
(`forense/encargos/2026-09-08-RUTINAS-2-COORDINACION-Y-REVISION.md`), para
que las tres rutinas no reimplementen cada una su propia versión de las
mismas cuatro decisiones:

- P1: identidad de una revisión (PR, HEAD, main, cuerpo) y su marca.
- P2: si una rama administrativa se exime del candado de `/despacha`.
- P4: cómo se traduce el desenlace de una rutina a la huella de
  `forense/rutinas.tsv`.

Es una librería pura: no hace `git`, no hace red, no escribe nada. Cada
función toma los datos ya derivados (listas de archivos, texto, sha) y
regresa una decisión. Las rutinas la importan; no la reimplementan.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

# ───────────────────────────────────────────────────────────────
# P1 · identidad y marca de una revisión
# ───────────────────────────────────────────────────────────────

# <!-- MM-REVISA:v2 pr=<n> head=<sha40> main=<sha40> body_sha256=<sha256> -->
MARCA_REVISA_RE = re.compile(
    r"<!--\s*MM-REVISA:v2\s+pr=(?P<pr>\d+)\s+head=(?P<head>[0-9a-f]{40})\s+"
    r"main=(?P<main>[0-9a-f]{40})\s+body_sha256=(?P<body_sha256>[0-9a-f]{64})\s*-->"
)


def body_sha256(texto: str) -> str:
    """Hash normalizado del cuerpo de un PR: recorta espacio en blanco de
    los extremos y normaliza fin de línea a `\\n` antes de hashear, para
    que un PR editado solo en su terminación de línea (CRLF/LF) no cuente
    como cambio de alcance."""
    normalizado = (texto or "").replace("\r\n", "\n").strip()
    return hashlib.sha256(normalizado.encode("utf-8")).hexdigest()


def construye_marca_revisa(pr: int, head: str, main: str, body_sha: str) -> str:
    """Construye el comentario-marca verbatim, con validación de forma."""
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError(f"head no es sha40: {head!r}")
    if not re.fullmatch(r"[0-9a-f]{40}", main):
        raise ValueError(f"main no es sha40: {main!r}")
    if not re.fullmatch(r"[0-9a-f]{64}", body_sha):
        raise ValueError(f"body_sha256 no es sha256: {body_sha!r}")
    return f"<!-- MM-REVISA:v2 pr={pr} head={head} main={main} body_sha256={body_sha} -->"


def parsea_marca_revisa(texto: str) -> Optional[dict]:
    """Extrae `pr, head, main, body_sha256` de un comentario que contenga
    la marca. `None` si el comentario no trae marca reconocible — un
    comentario sin marca NUNCA se trata como revisión vigente (P1:
    "si falta evidencia de versión, no presumir vigencia")."""
    m = MARCA_REVISA_RE.search(texto or "")
    if not m:
        return None
    d = m.groupdict()
    d["pr"] = int(d["pr"])
    return d


@dataclass(frozen=True)
class IdentidadRevision:
    pr: int
    head: str
    main: str
    body_sha256: str


def revision_esta_vigente(actual: IdentidadRevision,
                           marcada: Optional[dict]) -> tuple[bool, str]:
    """Compara la identidad actual (PR/HEAD/main/cuerpo re-derivados ahora)
    contra la última marca publicada. Regresa `(vigente, razon)`.

    - Sin marca previa -> no vigente, "sin marca previa" (primera revisión).
    - Marca de otro PR -> no vigente, "otro PR" (no debería pasar si se
      busca el comentario del PR correcto, pero se cubre igual).
    - HEAD o cuerpo distintos -> no vigente, "head cambio" / "cuerpo cambio":
      pendiente, la revisión anterior no se presenta como vigente.
    - Solo `main` distinto, HEAD y cuerpo iguales -> no vigente, "main
      cambio": el resultado anterior NO se presenta como revisión de la
      nueva combinación (aunque el código del PR no cambió).
    - Los tres iguales -> vigente: no duplicar comentario.
    """
    if marcada is None:
        return False, "sin marca previa"
    if int(marcada["pr"]) != actual.pr:
        return False, "otro PR"
    if marcada["head"] != actual.head:
        return False, "head cambio"
    if marcada["body_sha256"] != actual.body_sha256:
        return False, "cuerpo cambio"
    if marcada["main"] != actual.main:
        return False, "main cambio"
    return True, "misma identidad (pr, head, main, cuerpo)"


# ───────────────────────────────────────────────────────────────
# P2 · clasificación de ramas para el candado de /despacha
# ───────────────────────────────────────────────────────────────

# Rutas que un PR [TRAMITE] puede tocar sin que su rama bloquee un acto
# automático (P2/P3): digestos, huellas, y las modificaciones puntuales ya
# permitidas de firmas o `## CONSUMIDO` -- nunca el archivo de encargo
# completo, y nunca nada fuera de `forense/`.
_TRAMITE_PREFIJOS_EXENTOS = (
    "forense/digesto/",
    "forense/rutinas.tsv",
    "forense/no-corrido.tsv",
)
_TRAMITE_ARCHIVOS_EXENTOS_EXACTOS = (
    "forense/firmas-pendientes.tsv",
)
# Encargos: solo se permite tocarlos para apendar ## CONSUMIDO al final,
# lo cual esta función no puede verificar por sí sola (no ve el diff de
# líneas) -- por eso un archivo de `forense/encargos/` cuenta como
# "requiere revisión de línea" y no como exención automática de archivo
# completo (ver `clasifica_rama_tramite` para la variante que sí las
# acepta cuando el llamador ya verificó que el diff de esa ruta es
# solo-apéndice).
_ENCARGOS_PREFIJO = "forense/encargos/"

_REVISA_ARCHIVOS_EXENTOS_PREFIJOS = (
    "forense/notas/",
)


@dataclass(frozen=True)
class VeredictoRama:
    exenta: bool
    razon: str


def clasifica_rama_tramite(archivos_tocados: Iterable[str],
                            encargos_solo_apendice: bool = True) -> VeredictoRama:
    """P2/P3: una rama `[TRAMITE]`/`claude/tramite-*` se exime del candado
    de `/despacha` sólo si TODO su diff cae en el perímetro administrativo
    permitido: digestos, `rutinas.tsv`, `no-corrido.tsv`, las modificaciones
    puntuales de `firmas-pendientes.tsv`, o encargos tocados
    exclusivamente para apendar `## CONSUMIDO`/`## NO-CORRIDO` al final
    (`encargos_solo_apendice`, que el llamador certifica habiendo mirado
    el diff de línea -- esta función no lo puede derivar del nombre de
    archivo solo)."""
    archivos = list(archivos_tocados)
    if not archivos:
        return VeredictoRama(True, "diff vacío: no hay nada que bloquee")
    fuera = []
    for a in archivos:
        if a in _TRAMITE_ARCHIVOS_EXENTOS_EXACTOS:
            continue
        if any(a.startswith(p) for p in _TRAMITE_PREFIJOS_EXENTOS):
            continue
        if a.startswith(_ENCARGOS_PREFIJO):
            if encargos_solo_apendice:
                continue
            fuera.append(a)
            continue
        fuera.append(a)
    if fuera:
        return VeredictoRama(
            False,
            f"cambios fuera del perímetro administrativo de trámite: {sorted(fuera)}",
        )
    return VeredictoRama(True, "todo el diff cae en el perímetro administrativo de trámite")


def clasifica_rama_revisa(archivos_tocados: Iterable[str]) -> VeredictoRama:
    """P2: una rama `[REVISA]`/`claude/revisa-*` se exime del candado sólo
    si su diff completo es la nota de revisión post-hoc, nada ejecutable."""
    archivos = list(archivos_tocados)
    if not archivos:
        return VeredictoRama(True, "diff vacío: no hay nada que bloquee")
    fuera = [a for a in archivos
             if not any(a.startswith(p) for p in _REVISA_ARCHIVOS_EXENTOS_PREFIJOS)]
    if fuera:
        return VeredictoRama(
            False,
            f"cambios fuera de la nota de revisión permitida: {sorted(fuera)}",
        )
    return VeredictoRama(True, "solo nota de revisión (forense/notas/)")


def clasifica_rama_para_candado(nombre_rama: str,
                                 ya_contenida_en_main: bool,
                                 archivos_tocados: Iterable[str],
                                 titulo_pr: Optional[str] = None) -> VeredictoRama:
    """Punto de entrada único de P2 · tabla de clasificación.

    `ya_contenida_en_main` viene de
    `git merge-base --is-ancestor <rama> origin/main` (0 = contenida).
    `titulo_pr` es opcional -- puede no ser derivable sin `gh`; si no se
    tiene, la clasificación cae solo en el nombre de rama."""
    if ya_contenida_en_main:
        return VeredictoRama(True, "rama ya contenida en main")

    es_tramite = nombre_rama.startswith("claude/tramite-") or (
        titulo_pr is not None and titulo_pr.startswith("[TRAMITE]"))
    es_revisa = nombre_rama.startswith("claude/revisa-") or (
        titulo_pr is not None and titulo_pr.startswith("[REVISA]"))

    if es_tramite:
        return clasifica_rama_tramite(archivos_tocados)
    if es_revisa:
        return clasifica_rama_revisa(archivos_tocados)
    return VeredictoRama(
        False,
        "rama sin clasificación administrativa verificable: no eximida, "
        "candado con causa explícita",
    )


# ───────────────────────────────────────────────────────────────
# P3 · reutilización del PR administrativo de trámite
# ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class PRTramite:
    numero: int
    rama: str
    estado: str  # "open" | "closed" | "merged"
    titulo: str


def decide_pr_tramite(abiertos: Iterable[PRTramite]) -> tuple[str, Optional[PRTramite]]:
    """P3: dado el conjunto de PR `[TRAMITE]` (ya filtrado a los de esta
    rutina/repo), decide qué hacer.

    Regresa `(accion, pr)`:
    - `("REUSA", pr)` — exactamente un PR abierto: continuar su rama real.
    - `("CREA", None)` — ninguno abierto: crear `claude/tramite-<fecha>`.
    - `("DUPLICADO", None)` — más de uno abierto: declarar duplicidad, no
      crear otro ni cerrar los existentes.
    """
    vivos = [p for p in abiertos if p.estado == "open"]
    if len(vivos) == 1:
        return "REUSA", vivos[0]
    if len(vivos) == 0:
        return "CREA", None
    return "DUPLICADO", None


# ───────────────────────────────────────────────────────────────
# P4 · traducción de resultados a la huella de forense/rutinas.tsv
# ───────────────────────────────────────────────────────────────

# Traducción fijada por P4: los cierres de sesión reales de cada rutina se
# escriben en `rutinas.tsv` con este vocabulario normalizado. Los verbos
# de la izquierda son los que las rutinas ya usaban antes de este acto;
# no se reescriben filas históricas, solo se normalizan las nuevas.
_TRADUCCION_RESULTADO = {
    ("tramite", "ABRIO"): "HIZO",
    ("tramite", "ACTUALIZO"): "HIZO",
    ("revisa", "COMENTO"): "HIZO",
    ("revisa", "ACTUALIZO"): "HIZO",
    ("despacha", "COLA-VACIA"): "NADA-QUE-HACER",
}
# Estos conservan su significado sin traducción, en cualquier rutina.
_SIN_TRADUCCION = {"CANDADO", "PARO", "PROMOVIO", "NADA-QUE-HACER", "HIZO"}


def traduce_resultado_rutina(actor: str, resultado_crudo: str,
                              detalle_pr: Optional[str] = None) -> str:
    """P4: dado el actor (`tramite`/`revisa`/`despacha`) y el verbo crudo
    que produjo la sesión, regresa el token normalizado que va en la
    columna `resultado` de `forense/rutinas.tsv`.

    `HIZO:<PR>` cuando hay número de PR/URL disponible (`detalle_pr`);
    si no, el token normalizado solo, para que el llamador lo componga con
    su propio detalle."""
    base = resultado_crudo.split(":", 1)[0].strip().upper()
    if base in _SIN_TRADUCCION:
        token = base
    else:
        token = _TRADUCCION_RESULTADO.get((actor, base), base)
    if token == "HIZO" and detalle_pr:
        return f"HIZO:{detalle_pr}"
    return token


# ───────────────────────────────────────────────────────────────
# P1 · selección del PR elegible más antiguo con revisión pendiente
# ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CandidatoPR:
    numero: int
    titulo: str
    es_borrador: bool
    creado_en: str  # ISO8601 -- antigüedad del PR, no de su último comentario
    marca_vigente: bool  # True si ya hay revisión vigente para HEAD/main/cuerpo actuales


def filtra_elegibles(candidatos: Iterable[CandidatoPR]) -> list[CandidatoPR]:
    """P1 · filtro antes de la selección diaria: excluye borradores y PR
    `[TRAMITE]`/`[REVISA]` por título."""
    return [c for c in candidatos
            if not c.es_borrador
            and not c.titulo.startswith("[TRAMITE]")
            and not c.titulo.startswith("[REVISA]")]


def elige_pendiente_mas_antiguo(candidatos: Iterable[CandidatoPR]) -> Optional[CandidatoPR]:
    """P1 · del barrido diario, el PR elegible con revisión pendiente desde
    hace más tiempo, ordenando por antigüedad del PR (`creado_en`), nunca
    por la fecha de su último comentario. `None` si no hay candidato:
    termina `NADA-QUE-REVISAR`."""
    elegibles = [c for c in filtra_elegibles(candidatos) if not c.marca_vigente]
    if not elegibles:
        return None
    return min(elegibles, key=lambda c: c.creado_en)
