"""Emisor del corredor `M` — ACTO EMISOR-M-1 · 20/ago/2026.

Qué es: el componente que convierte lo que el modelo AFIRMA en su capa máquina
en (a) predicciones calificables por el marcador del duelo (ADV1-M3, forma
`PrediccionCorredor` de `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py`)
y (b) corridas contrafactuales para el gate `R3.4` (ADR-37 / milpa-spec §10.1).

Firmas de mesa que lo autorizan (20/ago/2026, capturadas por widget, verbatim):
  Q1     → "benchmark web"  (corrido y archivado:
           BENCHMARK-INTERVALO-CORREDOR-M-2026-08-20.md — síntesis: punto +
           clase-como-confianza + intervalo solo con EE real + CAL-ASIGNADO)
  Q2     → "Las reglas en prosa nos mete en problemas encuentra otra solución"
           (resuelto: este módulo NO compila prosa — ver abajo)
  Q1-bis → "Sí — sella y lanza EMISOR-M-1"

ARQUITECTURA SIN PROSA (delta v1.1 del diseño). Este módulo consume SOLO tres
fuentes-máquina existentes y jamás lee prosa como regla:
  1. `milpa/tramite.yaml`        — reglas con `p`, dos niveles ya separados.
  2. `milpa/procedencia.yaml`    — coeficientes/condicionales con clase y la
                                   capa de generadores (`detalle: {gen, coefs}`).
  3. `canon/modelo-decision-v4_0.md` §7 — el Registro congelado de IDs,
                                   PARSEADO, nunca re-transcrito. El parser no
                                   puede inflar un tier: lo copia, y
                                   `tests/test_emisor_fidelidad.py` compara cada
                                   fila parseada contra el archivo.
Lo que el modelo solo afirma en prosa es `NO-EMITE` por construcción; la
promoción prosa→máquina es el mecanismo ordinario del canon por acto con firma
(precedente: modelo §0, numerador 9→12), nunca tarea de este módulo.

ADR-68(a) / APERTURA v1.2:42 — este módulo no edita `tools/curador_registro/`
ni regla alguna: es un consumidor nuevo. No importa `milpa.src.motor` ni toca
los seis `tests/test_motor_*.py`.

Salidas del bucle, las tres explícitas (gobernanza:275): `EMITE` ·
`NO_COVERAGE` (salida de primera clase, nunca silencio) · `CONFLICTO`
(se reporta con ambos ids, no se promedia).
"""
from __future__ import annotations

import csv
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA_TRAMITE = RAIZ / "milpa" / "tramite.yaml"
RUTA_PROCEDENCIA = RAIZ / "milpa" / "procedencia.yaml"
RUTA_MODELO = RAIZ / "canon" / "modelo-decision-v4_0.md"
RUTA_MARCO = RAIZ / "forense" / "marco-candidatas-piloto-v1_0.tsv"
RUTA_USOS_CORRIDA0 = RAIZ / "data" / "corrida0" / "usos.tsv"
RUTA_RESULTADOS_CORRIDA0 = RAIZ / "data" / "corrida0" / "resultados.tsv"

MODO_HISTORICO = "HISTORICO"
MODO_GEN2 = "GEN2"
# `milpa/tramite.yaml` materializa proporciones a seis decimales. Este umbral
# sólo acredita esa representación; la aptitud del RESULT la decide linaje.py.
TOLERANCIA_MATERIALIZACION_P = 5e-7

# Umbrales del gate — ASIGNADOS, no medidos (milpa-spec §10.1 / ADR-37,
# gobernanza:267+: "los criterios de B y C (≥70%, <30%) son ASIGNADOS...
# no salen de ningún dato"). Se citan, no se eligen aquí.
UMBRAL_A_RAZON = 0.10      # A: adopción CoDi < 10% del comparador
UMBRAL_B_COLAPSO = 0.70    # B: la brecha colapsa ≥70% al apagar riesgo
UMBRAL_C_REDUCCION = 0.30  # C: la brecha se reduce <30% al apagar el canal


# ── Reglas máquina (fuente 1) ──────────────────────────────────────────────

@dataclass(frozen=True)
class Salida:
    conducta: str
    p: float | None
    clase: str | None
    aliases: tuple[str, ...] = ()
    evento: str | None = None
    dominio_elegible: tuple[tuple[str, object], ...] = ()
    complemento_de: str | None = None
    resultado_id: str | None = None
    resultado_generacion: str | None = None
    uso_motor: str | None = None
    rol_uso: str | None = None


@dataclass(frozen=True)
class Regla:
    id: str
    situacion: str
    disparadores: tuple[tuple[str, object], ...]   # nivel 1 — globales (ADR-26)
    palancas: tuple[tuple[str, object], ...]       # nivel 2 — booleanos de dominio
    palancas_origen: tuple[str, ...]               # de qué sub-dict vinieron (contexto_*)
    entonces: tuple[Salida, ...]
    transiciones: tuple[Salida, ...]
    tier: str
    generadores: tuple[str, ...]
    fuente: tuple[str, ...]

    def condiciones(self) -> dict:
        return dict(self.disparadores) | dict(self.palancas)


def cargar_reglas(ruta: Path = RUTA_TRAMITE) -> tuple[Regla, ...]:
    """Carga un YAML de dominio con el esquema de `tramite.yaml`.

    El split de niveles es el del propio esquema (verificado en sesión):
    `si.disparadores` = nivel 1; cualquier `si.contexto_*` = nivel 2.
    No se inventa ningún campo: regla sin `p` entra con `p=None` (CUALITATIVA).
    """
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    reglas = []
    for r in doc.get("reglas", []):
        si = r.get("si", {}) or {}
        disparadores = tuple(sorted((si.get("disparadores") or {}).items()))
        palancas: list[tuple[str, object]] = []
        origen = []
        for k in sorted(si):
            if k.startswith("contexto_"):
                origen.append(k)
                palancas.extend(sorted((si[k] or {}).items()))
        entonces = tuple(Salida(
            conducta=e["conducta"], p=e.get("p"), clase=e.get("clase"),
            aliases=tuple(e.get("aliases", []) or []),
            evento=e.get("evento"),
            dominio_elegible=tuple(sorted(
                (e.get("dominio_elegible") or {}).items())),
            complemento_de=e.get("complemento_de"),
            resultado_id=e.get("corrida0_resultado_id"),
            resultado_generacion=e.get("corrida0_generacion"),
            uso_motor=e.get("uso_motor"),
            rol_uso=e.get("rol_uso"),
        ) for e in r.get("entonces", []))
        transiciones = tuple(Salida(
            conducta=e["conducta"], p=e.get("p"), clase=e.get("clase"),
            aliases=tuple(e.get("aliases", []) or []),
            evento=e.get("evento"),
            dominio_elegible=tuple(sorted(
                (e.get("dominio_elegible") or {}).items())),
            complemento_de=e.get("complemento_de"),
            resultado_id=e.get("corrida0_resultado_id"),
            resultado_generacion=e.get("corrida0_generacion"),
            uso_motor=e.get("uso_motor"),
            rol_uso=e.get("rol_uso"),
        ) for e in r.get("transiciones", []))
        porque = r.get("porque", {}) or {}
        reglas.append(Regla(
            id=r["id"], situacion=r.get("situacion", ""),
            disparadores=disparadores, palancas=tuple(palancas),
            palancas_origen=tuple(origen), entonces=entonces,
            transiciones=transiciones,
            tier=r.get("tier", ""),
            generadores=tuple(porque.get("generador", []) or []),
            fuente=tuple(r.get("fuente", []) or []),
        ))
    return tuple(reglas)


# ── Bucle de evaluación de dos niveles (ADR-26) ────────────────────────────

@dataclass(frozen=True)
class ResultadoEval:
    estado: str                       # "EMITE" | "NO_COVERAGE" | "CONFLICTO"
    reglas: tuple[Regla, ...]
    contexto: tuple[tuple[str, object], ...]
    detalle: str = ""

    def p_de(self, conducta: str) -> float:
        if self.estado != "EMITE":
            raise LookupError(f"{self.estado}: {self.detalle}")
        (regla,) = self.reglas
        for s in regla.entonces:
            if s.conducta == conducta:
                if s.p is None:
                    raise LookupError(f"regla {regla.id} es CUALITATIVA para {conducta}")
                return s.p
        raise LookupError(f"regla {regla.id} no emite conducta {conducta!r}")


def evaluar(reglas: tuple[Regla, ...], situacion: str,
            globales: dict, palancas: dict) -> ResultadoEval:
    """Match determinista: una regla aplica si su `situacion` coincide y CADA
    condición que declara (nivel 1 y nivel 2) está presente e igual en el
    contexto provisto. Cero reglas → NO_COVERAGE con el contexto a la vista.
    Más de una con salidas distintas → CONFLICTO con ambos ids, sin promediar.
    """
    contexto = dict(globales) | dict(palancas)
    aplican = []
    for r in reglas:
        if r.situacion != situacion:
            continue
        cond = r.condiciones()
        if all(k in contexto and contexto[k] == v for k, v in cond.items()):
            aplican.append(r)
    ctx = tuple(sorted(contexto.items()))
    if not aplican:
        return ResultadoEval("NO_COVERAGE", (), ctx,
                             f"ninguna regla cubre situacion={situacion!r} con {dict(ctx)!r}")
    if len(aplican) > 1:
        mapas = {tuple((s.conducta, s.p) for s in r.entonces) for r in aplican}
        if len(mapas) > 1:
            ids = ", ".join(r.id for r in aplican)
            return ResultadoEval("CONFLICTO", tuple(aplican), ctx,
                                 f"reglas con salidas incompatibles: {ids}")
    return ResultadoEval("EMITE", (aplican[0],), ctx)


# ── Registro congelado de IDs (fuente 3) — parser, no transcripción ────────

@dataclass(frozen=True)
class FilaRegistro:
    id: str
    linea_motor: str
    enunciado: str
    tier: str
    resto: str
    cruda: str


# La celda de tier admite anotación tras el rótulo (caso real: R4.3,
# "`[FUERTE / MEDIA]` — compuesta"). El parser copia la celda entera.
_FILA = re.compile(r"^\|\s*`(R\d+\.\d+)`\s*\|\s*(L\d+)\s*\|(.*?)\|\s*(`?\[[^\]]+\]`?[^|]*)\|(.*)\|\s*$")


def parsear_registro_7(ruta: Path = RUTA_MODELO) -> dict[str, FilaRegistro]:
    """Extrae el Registro congelado de `modelo §7` (tabla de 49 filas,
    formato `| R#.# | L### | enunciado | [TIER] | ... |`). Solo dentro de la
    sección `## 7` — la tabla de traducción de §1.6 usa otro formato y queda
    fuera. Cada fila guarda su texto crudo para el test de fidelidad."""
    texto = ruta.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    ini = next(i for i, l in enumerate(lineas) if l.startswith("## 7 "))
    fin = next((i for i in range(ini + 1, len(lineas))
                if lineas[i].startswith("## ")), len(lineas))
    filas: dict[str, FilaRegistro] = {}
    for l in lineas[ini:fin]:
        m = _FILA.match(l)
        if m:
            rid = m.group(1)
            filas[rid] = FilaRegistro(rid, m.group(2), m.group(3).strip(),
                                      m.group(4).strip("`"), m.group(5).strip(), l)
    return filas


# ── Capa de generadores (fuente 2): switch puro para la condición C ────────

def apagar_generador(detalle: list[dict], gen: str) -> tuple[dict, ...]:
    """Apaga un generador en la combinación `detalle` de procedencia.yaml
    (poner a cero sus coeficientes numéricos). Función PURA: no muta la
    entrada; los coeficientes declarados SIN MAGNITUD (str) se conservan tal
    cual — cero también es una magnitud, y no la tienen."""
    salida = []
    for combo in detalle:
        c = dict(combo)
        if c.get("gen") == gen:
            c = dict(c)
            c["coefs"] = {k: (0.0 if isinstance(v, (int, float)) else v)
                          for k, v in dict(c.get("coefs", {})).items()}
            c["apagado"] = True
        salida.append(c)
    return tuple(salida)


# ── Gate R3.4 — tres condiciones (ADR-37 / milpa-spec §10.1) ───────────────

SIT_GOB = "le_ofrecen_servicio_gobierno_digital"
CTX_A = {"coercitivo": True, "riesgo_fiscal_percibido": True}
CTX_B = {"coercitivo": False, "riesgo_fiscal_percibido": False}  # regla espejo


@dataclass(frozen=True)
class GateR34:
    adopcion_codi_A: float | None
    adopcion_pareja_util: float | None       # CoDi/SPEI útil-sin-coerción (la pareja de la regla)
    adopcion_retail: float | None            # comparador de A per spec §10.1 — hoy NO-EMITE
    razon_A_pareja: float | None
    colapso_B: float | None
    reduccion_C: float | None
    pasa_B: bool | None
    pasa_C: bool | None
    huecos: tuple[str, ...]
    notas: tuple[str, ...]
    veredicto: str
    # Estampa de base empírica (advertencia de mesa, 20/ago/2026): un cálculo
    # correcto sobre insumos sin base medida no debe poder confundirse con uno
    # medido. Instrucciones A-bis(3)/A.10 aplicadas al resultado computado.
    insumos_clase: tuple[tuple[str, int], ...] = ()
    estampa: str = ""


def gate_r3_4(reglas: tuple[Regla, ...] | None = None) -> GateR34:
    """Corre las tres condiciones sobre la capa máquina. NO adjudica el gate:
    computa lo computable y NOMBRA los huecos (diseño §5: 'corriendo, o con el
    impedimento nombrado'). Umbrales citados arriba, rotulados ASIGNADO."""
    reglas = reglas if reglas is not None else cargar_reglas()
    huecos: list[str] = []
    notas: list[str] = []

    rA = evaluar(reglas, SIT_GOB, {"cobertura_formal": False}, CTX_A)
    rB = evaluar(reglas, SIT_GOB, {}, CTX_B)
    for nombre, r in (("A(coercitivo+riesgo)", rA), ("B(espejo útil)", rB)):
        if r.estado != "EMITE":
            huecos.append(f"{r.estado} en corrida {nombre}: {r.detalle}")
    if huecos:
        return GateR34(None, None, None, None, None, None, None, None,
                       tuple(huecos), tuple(notas),
                       "NO-ADJUDICADO — el gate no puede pasar por pérdida de cobertura")

    codi_A = rA.p_de("adopta")
    util = rB.p_de("adopta")

    # A per spec §10.1: comparador = "canal retail-efectivo tipo OXXO Pay".
    # Universo buscado (A.4): milpa/tramite.yaml + milpa/procedencia.yaml,
    # términos retail/oxxo/canal, 20/ago/2026 → NO-ENCONTRADO como cantidad.
    retail = None
    huecos.append(
        "H1 · adopción por canal retail-efectivo (comparador de A, spec §10.1): "
        "NO-EMITE — la capa máquina no la afirma; candidata a UN acto de "
        "promoción prosa→máquina por el mecanismo ordinario del canon.")
    huecos.append(
        "H2 · discrepancia de comparador: spec §10.1 dice 'OXXO Pay' (retail); "
        "el Registro §7 enuncia R3.4 como 'CoDi rechazado vs. útil (SPEI) "
        "adoptado'. Cuál comparador rige la condición A es firma de mesa.")
    razon_pareja = codi_A / util
    notas.append(
        f"Diagnóstico bajo lectura pareja-SPEI (no adjudica A): "
        f"{codi_A:.2f}/{util:.2f} = {razon_pareja:.3f} — "
        f"{'<' if razon_pareja < UMBRAL_A_RAZON else '≥'} {UMBRAL_A_RAZON:.2f}.")

    # B: apagar riesgo, canal constante — la brecha de la PAREJA colapsa.
    brecha_A = util - codi_A
    codi_B = rB.p_de("adopta")           # riesgo apagado → la espejo emite
    brecha_B = util - codi_B
    colapso = (brecha_A - brecha_B) / brecha_A if brecha_A else None
    pasa_B = colapso is not None and colapso >= UMBRAL_B_COLAPSO

    # C: apagar el canal de confianza personal (G1a) con riesgo encendido.
    # Implementación firmada (delta v1.1): switch de generador en la capa de
    # procedencia — no una regla nueva. En la capa de reglas del dominio §3.3
    # las p no cargan G1a, así que la brecha no se mueve; se DECLARA la
    # trivialidad en vez de esconderla.
    proc = yaml.safe_load(RUTA_PROCEDENCIA.read_text(encoding="utf-8"))
    detalle = _busca_detalle(proc)
    if detalle is None:
        huecos.append("H3 · capa de generadores (`detalle: {gen, coefs}`) no "
                      "localizada en procedencia.yaml — el switch C no corre.")
        reduccion = None
        pasa_C = None
    else:
        apagado = apagar_generador(detalle, "G1")
        assert any(c.get("apagado") for c in apagado)
        rC = evaluar(reglas, SIT_GOB, {"cobertura_formal": False}, CTX_A)
        brecha_C = util - rC.p_de("adopta")
        reduccion = (brecha_A - brecha_C) / brecha_A if brecha_A else None
        pasa_C = reduccion is not None and reduccion < UMBRAL_C_REDUCCION
        notas.append(
            "C es trivial en la capa de reglas (las p del dominio §3.3 no "
            "cargan G1a): reducción 0% por construcción. Un C no-trivial "
            "exige el enlace índice→adopción (h_r) — OLA futura, declarado.")

    # Estampa: las clases se DERIVAN de las salidas consumidas, no se teclean.
    clases: dict[str, int] = {}
    for res in (rA, rB):
        (regla,) = res.reglas
        for s in regla.entonces:
            if s.conducta == "adopta" and s.p is not None:
                clases[s.clase or "SIN-CLASE"] = clases.get(s.clase or "SIN-CLASE", 0) + 1
    n_medido = sum(v for k, v in clases.items() if k.startswith("MEDIDO"))
    estampa = (
        f"insumos del cálculo: {sum(clases.values())} probabilidades consumidas, "
        f"clases {clases}; base medida: {n_medido} de {sum(clases.values())} — "
        "B y C son propiedades estructurales del par ASIGNADO, no hallazgos "
        "empíricos (advertencia de mesa, 20/ago/2026); universo: tramite.yaml + "
        "procedencia.yaml + modelo §7")

    veredicto = ("NO-ADJUDICADO — B y C computados; A espera el comparador "
                 "(huecos H1/H2 a mesa)")
    return GateR34(codi_A, util, retail, razon_pareja, colapso, reduccion,
                   pasa_B, pasa_C, tuple(huecos), tuple(notas), veredicto,
                   tuple(sorted(clases.items())), estampa)


def _busca_detalle(nodo) -> list | None:
    """Localiza la lista `detalle: [{gen, coefs}, ...]` donde viva (fuente 2)."""
    if isinstance(nodo, dict):
        d = nodo.get("detalle")
        if (isinstance(d, list) and d and isinstance(d[0], dict) and "gen" in d[0]):
            return d
        for v in nodo.values():
            r = _busca_detalle(v)
            if r is not None:
                return r
    elif isinstance(nodo, list):
        for v in nodo:
            r = _busca_detalle(v)
            if r is not None:
                return r
    return None


# ── Vocabulario M-2 — dos variables dependientes, disparadores por
#    componente (ACTO EMISOR-M-2 · 24/ago/2026) ─────────────────────────────
# Firma de mesa que autoriza (24/ago, verbatim): "entiendo la reformulación
# pero lo que inicialmente queremos medir es adopción vs cohersión, aun
# cuando tenemos casos base si es importante asegurar que estamos teniendo
# esto en consideración, el motor debe poder considerar estas dos variables
# para predecir el comportamiento."
#
# Hoy el motor funde en una sola conducta ("adopta"/"rechaza_servicio") dos
# que mesa separa: cumplir bajo mandato con sanción, y adoptar por elección.
# Este bloque declara el vocabulario; no adjudica ninguna celda ni abre red.
# Fuente operativa: COERCION-Y-ADOPCION-rediseno-2026-08-20.md §4, §6 (no
# commiteado — ver forense/coercion-adopcion-espec-operativa-v0_1.md, T4).

VARIABLES_DEPENDIENTES_M2 = {"cumplimiento", "adopcion"}

# Dominios celda-D (tests/test_celdas_d.py: DOMINIOS) donde el encargo exige
# DV declarada. "tecnología/pagos/registros" del encargo mapea al único
# dominio del enum que los cubre: TEC.
DOMINIOS_EXIGEN_DV_M2 = {"TEC"}

DISPARADORES_COMPONENTE_M2 = {
    "riesgo_fiscal_percibido": bool,                       # existe, Nota 3 de R3.4
    "friccion_uso": bool,
    "utilidad_marginal_sobre_sustituto": bool,
    "lado_obligado": {"ninguno", "oferta", "usuario"},
    "sancion": {"ninguna", "suspension", "bloqueo"},
    "dato_sensible": {"no", "identificador", "biometrico"},
}


def valida_dv_celda_m2(celda: dict, filename: str = "<celda>") -> tuple[str, ...]:
    """Válida el vocabulario M-2 de una celda-D (o de cualquier mapeo con
    forma celda_d). NO adjudica nada: solo exige que las celdas del dominio
    que el encargo cubre declaren cuál de las dos variables dependientes
    miden, y que los disparadores por componente que declaren, si los
    declaran, estén bien formados. Devuelve la tupla de errores (vacía si
    pasa). El emisor se niega ante una celda sin DV declarada —
    ACTO EMISOR-M-2, 24/ago/2026."""
    errs: list[str] = []
    dominio = celda.get("dominio")
    dv = celda.get("variable_dependiente")

    if dominio in DOMINIOS_EXIGEN_DV_M2:
        if dv is None:
            errs.append(
                f"{filename}: falta 'variable_dependiente' (ACTO EMISOR-M-2, "
                f"24/ago/2026 — toda celda-D de dominio {dominio!r} declara si "
                f"mide cumplimiento o adopción; el emisor se niega sin DV declarada)"
            )
        elif dv not in VARIABLES_DEPENDIENTES_M2:
            errs.append(
                f"{filename}: variable_dependiente inválida: {dv!r} "
                f"(ACTO EMISOR-M-2: {sorted(VARIABLES_DEPENDIENTES_M2)})"
            )
    elif dv is not None and dv not in VARIABLES_DEPENDIENTES_M2:
        errs.append(f"{filename}: variable_dependiente inválida: {dv!r}")

    disparadores = celda.get("disparadores_m2") or {}
    for clave, valor in disparadores.items():
        regla = DISPARADORES_COMPONENTE_M2.get(clave)
        if regla is None:
            errs.append(f"{filename}: disparador_m2 desconocido: {clave!r}")
        elif regla is bool:
            if not isinstance(valor, bool):
                errs.append(f"{filename}: disparador_m2 {clave!r} debe ser booleano, no {valor!r}")
        elif valor not in regla:
            errs.append(f"{filename}: disparador_m2 {clave!r} inválido: {valor!r} ({sorted(regla)})")

    return tuple(errs)


def estampa_base_extendida_m2(reglas: tuple[Regla, ...] | None = None) -> str:
    """T2: por disparador M-2, ¿tiene base medida hoy? Deriva de las clases
    (`clase:`) realmente consumidas por las reglas del dominio tramite —
    no se teclea. La respuesta esperable es 'casi ninguno': se reporta tal
    cual, sin maquillar (v0.3.0 de tramite.yaml: las 10 probabilidades del
    dominio son clase ASIGNADO, ninguna MEDIDO)."""
    reglas = reglas if reglas is not None else cargar_reglas()
    lineas = []
    for disparador in sorted(DISPARADORES_COMPONENTE_M2):
        clases: set[str] = set()
        for r in reglas:
            if disparador in dict(r.condiciones()):
                for s in r.entonces:
                    if s.clase:
                        clases.add(s.clase)
        if not clases:
            estado = "SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla"
        elif any(c.startswith("MEDIDO") for c in clases):
            n_medido = sum(1 for c in clases if c.startswith("MEDIDO"))
            estado = f"BASE MEDIDA parcial: {n_medido}/{len(clases)} clases MEDIDO ({sorted(clases)})"
        else:
            estado = f"SIN BASE MEDIDA — clases consumidas: {sorted(clases)} (ninguna MEDIDO)"
        lineas.append(f"  {disparador}: {estado}")
    return "estampa de base extendida EMISOR-M-2 (T2, casi ninguno tiene base medida):\n" + "\n".join(lineas)


# ── Emisión al marcador (forma PrediccionCorredor, campos núcleo idénticos) ─

@dataclass(frozen=True)
class PrediccionM:
    tipo_escala: str                       # "continua" | "binaria" | "ordinal"
    valor_punto: float | None = None
    valor_categoria: str | None = None
    intervalo_lo: float | None = None      # solo donde hay EE real (Q1-bis)
    intervalo_hi: float | None = None
    confianza_declarada: float | None = None  # numérica: NO se usa para clase
    clase: str | None = None               # clase-como-confianza (IPCC: no probabilística)
    regla_id: str | None = None
    estado: str = "EMITE"
    derivado_de: str | None = None
    resultado_id: str | None = None
    resultado_generacion: str | None = None
    dominio_elegible: tuple[tuple[str, object], ...] = ()
    rol_uso: str | None = None
    uso_motor: str | None = None
    modo_emision: str = MODO_HISTORICO
    proposito: str | None = None
    uso_solicitado: str | None = None
    origen_numerico: str | None = None
    aptitud_uso: str | None = None
    camino_linaje: str | None = None
    dependencias_estructurales: tuple[str, ...] = ()
    detalle: str = ""


@dataclass(frozen=True)
class EvidenciaResultado:
    """Fila vigente de ``resultados.tsv`` que acredita un número."""

    resultado_id: str
    valor: float | None
    tipo: str
    unidad: str
    estado: str
    generacion: str
    origen_numerico: str
    validacion_independiente: str
    rol_evaluacion: str
    camino_linaje: str
    fuente_replay: str
    depende_de: str


@dataclass(frozen=True)
class UsoRegistrado:
    """Enlace activo consumidor→RESULT derivado por el registro de 17."""

    consumidor: str
    resultado_id: str
    corrida0_resultado_id: str
    generacion_leida: str
    corrida0_generacion: str
    tipo_uso: str
    uso_solicitado: str
    origen_numerico: str
    aptitud_uso: str
    motivo_aptitud: str
    activo: str
    camino_linaje: str


@dataclass(frozen=True)
class IndiceLinajeEmision:
    resultados: Mapping[str, EvidenciaResultado]
    usos: Mapping[str, UsoRegistrado]


def _leer_vista_derivada(ruta: Path) -> list[dict[str, str]]:
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    if lineas and lineas[0].startswith("# DERIVADO"):
        lineas = lineas[1:]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _valor_numerico(valor: str) -> float | None:
    if str(valor).strip() in {"", "None", "null", "PENDIENTE", "NO-COMPARABLE"}:
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    return numero if math.isfinite(numero) else None


def cargar_indice_linaje_emision(
        ruta_usos: Path = RUTA_USOS_CORRIDA0,
        ruta_resultados: Path = RUTA_RESULTADOS_CORRIDA0,
) -> IndiceLinajeEmision:
    """Consume las vistas de 17; no vuelve a resolver rutas ni procedencia."""
    por_id: dict[str, list[dict[str, str]]] = {}
    for fila in _leer_vista_derivada(ruta_resultados):
        por_id.setdefault(fila["resultado_id"], []).append(fila)

    resultados: dict[str, EvidenciaResultado] = {}
    for resultado_id, filas in por_id.items():
        vigentes = [f for f in filas
                    if not str(f.get("estado", "")).startswith("SUPERADO")]
        if len(vigentes) != 1:
            raise ValueError(
                f"{resultado_id}: se esperaba una fila vigente; hay {len(vigentes)}")
        f = vigentes[0]
        resultados[resultado_id] = EvidenciaResultado(
            resultado_id=resultado_id,
            valor=_valor_numerico(f.get("valor", "")),
            tipo=f.get("tipo", ""),
            unidad=f.get("unidad", ""),
            estado=f.get("estado", ""),
            generacion=f.get("generacion", ""),
            origen_numerico=f.get("origen_numerico", ""),
            validacion_independiente=f.get("validacion_independiente", ""),
            rol_evaluacion=f.get("rol_evaluacion", ""),
            camino_linaje=f.get("camino_linaje", ""),
            fuente_replay=f.get("fuente_replay", ""),
            depende_de=f.get("depende_de", ""),
        )

    usos: dict[str, UsoRegistrado] = {}
    for f in _leer_vista_derivada(ruta_usos):
        if f.get("activo") != "SI":
            continue
        consumidor = f["consumidor"]
        if consumidor in usos:
            raise ValueError(f"consumidor activo duplicado: {consumidor}")
        usos[consumidor] = UsoRegistrado(
            consumidor=consumidor,
            resultado_id=f.get("resultado_id", ""),
            corrida0_resultado_id=f.get("corrida0_resultado_id", ""),
            generacion_leida=f.get("generacion_leida", ""),
            corrida0_generacion=f.get("corrida0_generacion", ""),
            tipo_uso=f.get("tipo_uso", ""),
            uso_solicitado=f.get("uso_solicitado", ""),
            origen_numerico=f.get("origen_numerico", ""),
            aptitud_uso=f.get("aptitud_uso", ""),
            motivo_aptitud=f.get("motivo_aptitud", ""),
            activo=f.get("activo", ""),
            camino_linaje=f.get("camino_linaje", ""),
        )
    return IndiceLinajeEmision(resultados=resultados, usos=usos)


def _salida(regla: Regla, conducta: str) -> Salida | None:
    coincidencias = [s for s in regla.entonces
                     if conducta == s.conducta or conducta in s.aliases]
    if len(coincidencias) > 1:
        raise ValueError(
            f"alias ambiguo {conducta!r} en regla {regla.id}: "
            f"{[s.conducta for s in coincidencias]!r}")
    return coincidencias[0] if coincidencias else None


def _dependencias_estructurales(regla: Regla) -> tuple[str, ...]:
    """Componentes que un RESULT numérico no acredita por sí solo."""
    partes = [f"regla:{regla.id}:disparadores"]
    if regla.palancas:
        partes.append(f"regla:{regla.id}:palancas")
    if regla.generadores:
        partes.append("generadores:" + ",".join(regla.generadores))
    if regla.tier:
        partes.append(f"tier:{regla.tier}")
    return tuple(partes)


def emitir_binaria(regla: Regla, conducta: str) -> PrediccionM:
    """Emite una salida y conserva alias; un complemento se deriva del padre.

    La API historica sigue disponible para replays. Los consumidores nuevos
    que conocen el contexto deben usar :func:`emitir_binaria_en_contexto`.
    """
    s = _salida(regla, conducta)
    if s is not None:
        punto = s.p
        if s.complemento_de:
            padre = _salida(regla, s.complemento_de)
            if padre is None or padre.p is None:
                return PrediccionM(
                    "binaria", estado="NO-EMITE", regla_id=regla.id,
                    valor_categoria=s.conducta,
                    detalle=f"complemento sin padre {s.complemento_de!r}")
            punto = 1.0 - padre.p
            if s.p is not None and abs(s.p - punto) > 5e-7:
                return PrediccionM(
                    "binaria", estado="CONFLICTO", regla_id=regla.id,
                    valor_categoria=s.conducta, derivado_de=padre.conducta,
                    detalle=(f"p materializada {s.p} no coincide con "
                             f"1-p({padre.conducta})={punto}"))
        return PrediccionM(
            "binaria", valor_punto=punto, valor_categoria=s.conducta,
            clase=s.clase, regla_id=regla.id, derivado_de=s.complemento_de,
            resultado_id=(padre.resultado_id if s.complemento_de else
                          s.resultado_id),
            resultado_generacion=(padre.resultado_generacion
                                  if s.complemento_de else
                                  s.resultado_generacion),
            dominio_elegible=s.dominio_elegible, rol_uso=s.rol_uso,
            uso_motor=s.uso_motor)
    return PrediccionM("binaria", estado="NO-EMITE", regla_id=regla.id,
                       valor_categoria=conducta)


def emitir_binaria_en_contexto(regla: Regla, conducta: str,
                               contexto: dict, *,
                               uso_solicitado: str | None = None) -> PrediccionM:
    """Impide aplicar una tasa fuera de su dominio o propósito declarado.

    ``uso_solicitado=None`` conserva la API histórica. Un consumidor nuevo
    puede declarar su propósito; los proxies descriptivos fallan cerrados si
    se les pide una probabilidad empírica u otro uso no acreditado.
    """
    s = _salida(regla, conducta)
    if s is None:
        return emitir_binaria(regla, conducta)
    faltan = {k: v for k, v in s.dominio_elegible
             if k not in contexto or contexto[k] != v}
    if faltan:
        return PrediccionM(
            "binaria", estado="NO_COVERAGE", regla_id=regla.id,
            valor_categoria=s.conducta, dominio_elegible=s.dominio_elegible,
            resultado_id=s.resultado_id,
            resultado_generacion=s.resultado_generacion,
            rol_uso=s.rol_uso, uso_motor=s.uso_motor,
            detalle=f"fuera del dominio elegible: requiere {faltan!r}")
    permitidos_proxy = {"baseline", "consulta_descriptiva", "escenario"}
    if (s.rol_uso in {"proxy_descriptivo", "complemento_proxy_descriptivo"}
            and uso_solicitado is not None
            and uso_solicitado not in permitidos_proxy):
        return PrediccionM(
            "binaria", estado="NO_COVERAGE", regla_id=regla.id,
            valor_categoria=s.conducta, dominio_elegible=s.dominio_elegible,
            resultado_id=s.resultado_id,
            resultado_generacion=s.resultado_generacion,
            rol_uso=s.rol_uso, uso_motor=s.uso_motor,
            detalle=(f"uso {uso_solicitado!r} no permitido para "
                     f"rol_uso={s.rol_uso!r}; permitidos="
                     f"{sorted(permitidos_proxy)!r}"))
    return emitir_binaria(regla, conducta)


def _sin_cobertura_contrato(base: PrediccionM, detalle: str, *, modo: str,
                            proposito: str, uso: str,
                            dependencias: tuple[str, ...],
                            resultado_id: str | None = None,
                            origen: str | None = None,
                            aptitud: str | None = None,
                            camino: str | None = None) -> PrediccionM:
    previo = f"{base.detalle}; " if base.detalle else ""
    return replace(
        base, estado="NO_COVERAGE", valor_punto=None,
        resultado_id=resultado_id or base.resultado_id,
        modo_emision=modo, proposito=proposito, uso_solicitado=uso,
        origen_numerico=origen, aptitud_uso=aptitud,
        camino_linaje=camino,
        dependencias_estructurales=dependencias,
        detalle=previo + detalle,
    )


def emitir_binaria_contrato(
        regla: Regla,
        conducta: str,
        contexto: dict,
        *,
        modo: str,
        proposito: str,
        uso_solicitado: str | None = None,
        indice: IndiceLinajeEmision | None = None,
        resultado_id_seleccionado: str | None = None,
        valor_seleccionado: float | None = None,
        rol_seleccionado: str = "OPERATIVO",
        detalle_seleccion: str = "",
) -> PrediccionM:
    """Emite por la ruta histórica o por un contrato GEN2 que falla cerrado.

    La ruta ``HISTORICO`` conserva el valor materializado en YAML. La ruta
    ``GEN2`` exige la fila activa del consumidor, un RESULT sellado, origen
    ``NUEVO`` apto según :mod:`milpa.src.linaje` e identidad numérica. Para
    transferencia el selector puede entregar otro RESULT; el valor se vuelve
    a leer del registro y nunca del árbitro ni del ``p`` histórico.
    """
    modo_norm = str(modo or "").upper()
    proposito_norm = str(proposito or "").strip().lower()
    usos_por_defecto = {
        (MODO_HISTORICO, "baseline"): "BASELINE",
        (MODO_HISTORICO, "consulta"): "DESCRIPTIVO",
        (MODO_GEN2, "consulta"): "MEDICION-GEN2",
        (MODO_GEN2, "transferencia"): "MEDICION-GEN2",
    }
    uso = str(uso_solicitado or usos_por_defecto.get(
        (modo_norm, proposito_norm), "")).upper().replace("_", "-")
    dependencias = _dependencias_estructurales(regla)
    uso_contexto = {
        "BASELINE": "baseline",
        "DESCRIPTIVO": "consulta_descriptiva",
        "CALIBRACION": "escenario",
    }.get(uso, "probabilidad_evento")
    base = emitir_binaria_en_contexto(
        regla, conducta, contexto, uso_solicitado=uso_contexto)

    if modo_norm == MODO_HISTORICO:
        salida = _salida(regla, conducta)
        extra = ()
        if salida is not None and salida.resultado_id is None:
            clase = str(salida.clase or "SIN-CLASE").split("·", 1)[0]
            extra = (f"numero:{clase}-SIN-RESULT",)
        return replace(
            base, modo_emision=MODO_HISTORICO,
            proposito=proposito_norm, uso_solicitado=uso,
            dependencias_estructurales=dependencias + extra,
        )

    if modo_norm != MODO_GEN2:
        return _sin_cobertura_contrato(
            base, f"modo de emisión desconocido: {modo!r}", modo=modo_norm,
            proposito=proposito_norm, uso=uso, dependencias=dependencias)
    if proposito_norm not in {"consulta", "transferencia"}:
        return _sin_cobertura_contrato(
            base, ("GEN2 exige propósito explícito 'consulta' o "
                   "'transferencia'; baseline pertenece a HISTORICO"),
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias)
    if base.estado != "EMITE":
        return _sin_cobertura_contrato(
            base, "el dominio o propósito de la salida no está cubierto",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias)
    if rol_seleccionado.upper() in {"ARBITRO", "ORIGEN-ARBITRO"}:
        return _sin_cobertura_contrato(
            base, "un valor usado como árbitro no puede alimentar GEN2",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias,
            resultado_id=resultado_id_seleccionado)

    salida = _salida(regla, conducta)
    if salida is None:
        return _sin_cobertura_contrato(
            base, "conducta sin salida máquina", modo=modo_norm,
            proposito=proposito_norm, uso=uso, dependencias=dependencias)
    marca_adopcion = str(salida.uso_motor or "").upper()
    if ("PROPUESTA-NO-ADOPTADA" in marca_adopcion
            or "NO-ADOPTAR" in marca_adopcion):
        return _sin_cobertura_contrato(
            base, "la salida está documentada pero su adopción no fue firmada",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=salida.resultado_id)
    fuente_salida = salida
    if salida.complemento_de:
        padre = _salida(regla, salida.complemento_de)
        if padre is None:
            return _sin_cobertura_contrato(
                base, f"complemento sin padre {salida.complemento_de!r}",
                modo=modo_norm, proposito=proposito_norm, uso=uso,
                dependencias=dependencias)
        fuente_salida = padre

    transferencia = resultado_id_seleccionado is not None
    resultado_id = resultado_id_seleccionado or fuente_salida.resultado_id
    if not resultado_id:
        return _sin_cobertura_contrato(
            base, "la salida numérica no declara RESULT; no se usa el p viejo",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias)
    indice = indice or cargar_indice_linaje_emision()

    consumidor = f"milpa/tramite.yaml:{regla.id}:{salida.conducta}"
    uso_activo = indice.usos.get(consumidor)
    if uso_activo is None:
        return _sin_cobertura_contrato(
            base, f"consumidor no activo en usos.tsv: {consumidor}",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=resultado_id)

    if not transferencia:
        consumidor_fuente = (
            f"milpa/tramite.yaml:{regla.id}:{fuente_salida.conducta}")
        uso_fuente = indice.usos.get(consumidor_fuente)
        if uso_fuente is None:
            return _sin_cobertura_contrato(
                base, f"padre numérico no activo: {consumidor_fuente}",
                modo=modo_norm, proposito=proposito_norm, uso=uso,
                dependencias=dependencias, resultado_id=resultado_id)
        if (uso_fuente.corrida0_resultado_id != resultado_id
                or uso_fuente.corrida0_generacion != "GEN2"
                or fuente_salida.resultado_generacion != "GEN2"):
            return _sin_cobertura_contrato(
                base, ("identidad/generación declarada no coincide: "
                       f"YAML={fuente_salida.resultado_id}/"
                       f"{fuente_salida.resultado_generacion}, "
                       f"registro={uso_fuente.corrida0_resultado_id}/"
                       f"{uso_fuente.corrida0_generacion}"),
                modo=modo_norm, proposito=proposito_norm, uso=uso,
                dependencias=dependencias, resultado_id=resultado_id,
                camino=uso_fuente.camino_linaje)

    evidencia = indice.resultados.get(resultado_id)
    if evidencia is None:
        return _sin_cobertura_contrato(
            base, f"RESULT inexistente en resultados.tsv: {resultado_id}",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=resultado_id)
    camino = f"{consumidor} -> {resultado_id} -> {evidencia.camino_linaje}"
    if not evidencia.estado.startswith("SELLADA"):
        return _sin_cobertura_contrato(
            base, f"RESULT no sellado: estado={evidencia.estado}",
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=resultado_id,
            origen=evidencia.origen_numerico, camino=camino)
    if evidencia.generacion != "GEN2" or evidencia.valor is None:
        return _sin_cobertura_contrato(
            base, (f"RESULT sin número GEN2: generación={evidencia.generacion}, "
                   f"valor={evidencia.valor!r}"),
            modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=resultado_id,
            origen=evidencia.origen_numerico, camino=camino)

    # Contrato compartido con registro/T35; esta capa agrega dominio e
    # identidad de estimando, que linaje.py deliberadamente no decide.
    from milpa.src.linaje import APTA_LINAJE, aptitud_para_uso
    aptitud, motivo = aptitud_para_uso(
        evidencia.origen_numerico, uso,
        evidencia.validacion_independiente, evidencia.rol_evaluacion)
    if aptitud != APTA_LINAJE:
        return _sin_cobertura_contrato(
            base, motivo, modo=modo_norm, proposito=proposito_norm, uso=uso,
            dependencias=dependencias, resultado_id=resultado_id,
            origen=evidencia.origen_numerico, aptitud=aptitud, camino=camino)

    valor_resultado = evidencia.valor
    if transferencia:
        if valor_seleccionado is None or not math.isclose(
                valor_seleccionado, valor_resultado, rel_tol=0.0, abs_tol=1e-12):
            return _sin_cobertura_contrato(
                base, ("el valor elegido por el selector no coincide con "
                       f"{resultado_id}: {valor_seleccionado!r} != "
                       f"{valor_resultado!r}"),
                modo=modo_norm, proposito=proposito_norm, uso=uso,
                dependencias=dependencias, resultado_id=resultado_id,
                origen=evidencia.origen_numerico, aptitud=aptitud,
                camino=camino)
        valor_emitido = valor_resultado
    else:
        valor_emitido = (1.0 - valor_resultado
                         if salida.complemento_de else valor_resultado)
        if (base.valor_punto is None or
                abs(base.valor_punto - valor_emitido) >
                TOLERANCIA_MATERIALIZACION_P):
            return _sin_cobertura_contrato(
                base, ("p materializado no identifica al RESULT: "
                       f"{base.valor_punto!r} vs {valor_emitido!r}, tolerancia="
                       f"{TOLERANCIA_MATERIALIZACION_P}"),
                modo=modo_norm, proposito=proposito_norm, uso=uso,
                dependencias=dependencias, resultado_id=resultado_id,
                origen=evidencia.origen_numerico, aptitud=aptitud,
                camino=camino)

    detalle = f"{resultado_id}: {motivo}"
    if detalle_seleccion:
        detalle += f"; selección={detalle_seleccion}"
    return replace(
        base, valor_punto=valor_emitido, resultado_id=resultado_id,
        resultado_generacion=evidencia.generacion,
        modo_emision=MODO_GEN2, proposito=proposito_norm,
        uso_solicitado=uso, origen_numerico=evidencia.origen_numerico,
        aptitud_uso=aptitud, camino_linaje=camino,
        dependencias_estructurales=dependencias, detalle=detalle,
    )


def emitir_transicion(regla: Regla, evento: str, contexto: dict) -> PrediccionM:
    """Emite una transición medida sin mezclarla con la salida legacy."""
    coincidencias = [s for s in regla.transiciones if s.evento == evento]
    if len(coincidencias) != 1:
        return PrediccionM(
            "binaria", estado="NO-EMITE", regla_id=regla.id,
            valor_categoria=evento,
            detalle=f"se esperaban 1 transicion para {evento!r}; hay {len(coincidencias)}")
    s = coincidencias[0]
    faltan = {k: v for k, v in s.dominio_elegible
             if k not in contexto or contexto[k] != v}
    if faltan:
        return PrediccionM(
            "binaria", estado="NO_COVERAGE", regla_id=regla.id,
            valor_categoria=s.conducta, dominio_elegible=s.dominio_elegible,
            resultado_id=s.resultado_id,
            resultado_generacion=s.resultado_generacion,
            rol_uso=s.rol_uso, uso_motor=s.uso_motor,
            detalle=f"fuera del dominio elegible: requiere {faltan!r}")
    return PrediccionM(
        "binaria", valor_punto=s.p, valor_categoria=s.conducta,
        clase=s.clase, regla_id=regla.id,
        resultado_id=s.resultado_id,
        resultado_generacion=s.resultado_generacion,
        dominio_elegible=s.dominio_elegible, rol_uso=s.rol_uso,
        uso_motor=s.uso_motor)


def estado_encuci_solicitud_entrega(solicitud: int | None,
                                    entrega: int | None) -> dict:
    """Lógica de AP5_17/AP5_18 sin imponer E⊆S ni convertir faltantes en No."""
    validos = {0, 1, None}
    if solicitud not in validos or entrega not in validos:
        raise ValueError("solicitud y entrega deben ser 0, 1 o None")
    union = 1 if 1 in (solicitud, entrega) else (
        0 if solicitud == 0 and entrega == 0 else None)
    return {"solicitud": solicitud, "entrega": entrega, "union": union}


def complementar_replicas(punto: float,
                           replicas: tuple[float, ...] = ()) -> tuple[float, tuple[float, ...]]:
    """D11: q=1-p y q[b]=1-p[b], nunca un segundo sorteo independiente."""
    valores = (punto,) + replicas
    if any(v < 0.0 or v > 1.0 for v in valores):
        raise ValueError("una proporcion y sus replicas deben estar en [0,1]")
    return 1.0 - punto, tuple(1.0 - v for v in replicas)


# ── Crosswalk pregunta↔máquina, pasada 1 ───────────────────────────────────

def _token_encuesta(encuesta: str) -> str:
    """Acrónimo de encuesta: primer token antes de espacio/paréntesis/slash
    (p.ej. "ENCIG 2023" -> "ENCIG"; "ENAFIN (Encuesta ...)" -> "ENAFIN")."""
    m = re.match(r"[^\s(/]+", encuesta.strip())
    return m.group(0) if m else encuesta.strip()


def _tiene_token(linea: str, token: str) -> bool:
    """Coincidencia por token exacto (no subcadena): ni prefijo ni sufijo
    alfanumérico pegado al token buscado."""
    return re.search(r"(?<![\w])" + re.escape(token) + r"(?![\w])", linea) is not None


def construir_crosswalk(salida: Path) -> int:
    """Pasada 1 sobre el marco (60 candidatas, lado árbitro): para cada
    `variable`, ¿aparece en alguna fuente-máquina en la misma línea que su
    `encuesta`? Universo declarado por fila. Vocabulario conservador:
    `CANDIDATO-EMITE` (con archivo:línea) exige aún enlace de escala/universo
    declarado antes de emitir; lo demás `NO-EMITE`. El emparejamiento exige
    coincidencia de encuesta además de la variable, y variable por token
    exacto (no subcadena) -- corrige los falsos positivos de subcadena
    documentados en DERIVACION-M-v1_0.md (AP7_1/P7_12_7 vs P7_1,
    AP5_3_XX vs P5_3, "(P2 §2.d)" vs P2). El conteo NO-EMITE es dato para
    la saturación del marco (FP-82)."""
    fuentes = {"milpa/procedencia.yaml": RUTA_PROCEDENCIA.read_text(encoding="utf-8").splitlines(),
               "milpa/tramite.yaml": RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()}
    n = 0
    with RUTA_MARCO.open(encoding="utf-8") as fh, salida.open("w", encoding="utf-8", newline="") as out:
        lector = csv.DictReader(fh, delimiter="\t")
        w = csv.writer(out, delimiter="\t", lineterminator="\n")  # LF: regeneración byte-estable (A.7, revisión 21/ago)
        w.writerow(["candidata_id", "encuesta", "variable", "emisibilidad_p1",
                    "evidencia", "universo_buscado"])
        for fila in lector:
            var = (fila.get("variable") or "").strip()
            enc = _token_encuesta(fila.get("encuesta") or "")
            hits = [f"{arch}:{i+1}" for arch, lin in fuentes.items()
                    for i, l in enumerate(lin)
                    if var and enc and _tiene_token(l, var) and _tiene_token(l, enc)]
            emis = "CANDIDATO-EMITE" if hits else "NO-EMITE"
            w.writerow([fila.get("id", ""), fila.get("encuesta", ""), var, emis,
                        ";".join(hits[:3]), "procedencia.yaml+tramite.yaml, término=variable, "
                        "encuesta=coincidencia-de-línea"])
            n += 1
    return n


if __name__ == "__main__":  # pragma: no cover
    g = gate_r3_4()
    print(f"gate R3.4 · veredicto: {g.veredicto}")
    print(f"  codi(A)={g.adopcion_codi_A}  útil(pareja)={g.adopcion_pareja_util}  "
          f"razón_pareja={g.razon_A_pareja}")
    print(f"  B: colapso={g.colapso_B} pasa={g.pasa_B} · C: reducción={g.reduccion_C} pasa={g.pasa_C}")
    for h in g.huecos:
        print(f"  HUECO · {h}")
    for nnota in g.notas:
        print(f"  NOTA  · {nnota}")
    print(f"  ESTAMPA · {g.estampa}")
