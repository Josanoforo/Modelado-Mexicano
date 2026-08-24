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
import re
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA_TRAMITE = RAIZ / "milpa" / "tramite.yaml"
RUTA_PROCEDENCIA = RAIZ / "milpa" / "procedencia.yaml"
RUTA_MODELO = RAIZ / "canon" / "modelo-decision-v4_0.md"
RUTA_MARCO = RAIZ / "forense" / "marco-candidatas-piloto-v1_0.tsv"

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


@dataclass(frozen=True)
class Regla:
    id: str
    situacion: str
    disparadores: tuple[tuple[str, object], ...]   # nivel 1 — globales (ADR-26)
    palancas: tuple[tuple[str, object], ...]       # nivel 2 — booleanos de dominio
    palancas_origen: tuple[str, ...]               # de qué sub-dict vinieron (contexto_*)
    entonces: tuple[Salida, ...]
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
        entonces = tuple(
            Salida(e["conducta"], e.get("p"), e.get("clase"))
            for e in r.get("entonces", [])
        )
        porque = r.get("porque", {}) or {}
        reglas.append(Regla(
            id=r["id"], situacion=r.get("situacion", ""),
            disparadores=disparadores, palancas=tuple(palancas),
            palancas_origen=tuple(origen), entonces=entonces,
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


def emitir_binaria(regla: Regla, conducta: str) -> PrediccionM:
    for s in regla.entonces:
        if s.conducta == conducta:
            return PrediccionM("binaria", valor_punto=s.p, valor_categoria=conducta,
                               clase=s.clase, regla_id=regla.id)
    return PrediccionM("binaria", estado="NO-EMITE", regla_id=regla.id,
                       valor_categoria=conducta)


# ── Crosswalk pregunta↔máquina, pasada 1 ───────────────────────────────────

def construir_crosswalk(salida: Path) -> int:
    """Pasada 1 sobre el marco (60 candidatas, lado árbitro): para cada
    `variable`, ¿aparece en alguna fuente-máquina? Universo declarado por fila.
    Vocabulario conservador: `CANDIDATO-EMITE` (con archivo:línea) exige aún
    enlace de escala/universo declarado antes de emitir; lo demás `NO-EMITE`.
    El conteo NO-EMITE es dato para la saturación del marco (FP-82)."""
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
            hits = [f"{arch}:{i+1}" for arch, lin in fuentes.items()
                    for i, l in enumerate(lin) if var and var in l]
            emis = "CANDIDATO-EMITE" if hits else "NO-EMITE"
            w.writerow([fila.get("id", ""), fila.get("encuesta", ""), var, emis,
                        ";".join(hits[:3]), "procedencia.yaml+tramite.yaml, término=variable"])
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
