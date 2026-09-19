#!/usr/bin/env python3
"""C2 compuesto sobre los cruces RESERVADA del marcador de segmento.

ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 (19/sep/2026).

Dos piezas, una sola fuente de verdad:

  P1 `dictamen()`  -- par por par, ¿los dos ejes marginales y el nacional
                      comparten desenlace, universo, unidad, ola y
                      ponderador? EMITIBLE / NO-EMITIBLE(causa), con cita
                      de línea del yaml del árbitro para cada campo leído.
  P2 `emisiones()` -- para cada celda de cada par EMITIBLE, el punto C2
                      log-aditivo. La FORMA no se reinventa: se importa
                      `tests/test_celda_d_c2.py::piso_log_aditivo`, que es
                      la función de referencia que los dos CALC ya
                      sellados citan (`CALC-DIN-AHORRO-SOLO-INFORMAL-
                      EMISIONES-0001/spec.yaml:187`, `CALC-TRA-EVADE-
                      NORMA-SXD-EMISIONES-0001/medidor.py:149`).

Este módulo NO abre microdato: su única entrada de números es
`milpa/tramite-ola5-propuesta-v0.yaml` (marginales sellados del árbitro)
más los cuatro nacionales congelados abajo, que salen de `milpa/
tramite.yaml`. No deriva R de ningún cruce, no adopta y no propaga IC.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
PROPUESTA = RAIZ / "milpa" / "tramite-ola5-propuesta-v0.yaml"
TRAMITE = RAIZ / "milpa" / "tramite.yaml"
MARCADOR = RAIZ / "data" / "corrida0" / "marcador-segmento.tsv"

sys.path.insert(0, str(RAIZ / "tests"))
from test_celda_d_c2 import piso_log_aditivo  # noqa: E402  (forma sellada)


# ── nacionales ────────────────────────────────────────────────────────────
# El nacional NO se deriva aquí: se cita. Cada entrada es la tasa base de
# la MISMA regla, la MISMA ola, el MISMO universo y el MISMO ponderador que
# los marginales por eje, tal como los dos CALC ya sellados lo hicieron
# (`marginales_sellados_D9.NAC`). `clase` se conserva verbatim porque
# distingue MEDIDO de DERIVADO, y esa distinción viaja a la emisión.
NACIONALES = {
    "ahorra_solo_informal": {
        "p": 0.357153,
        "ic95": None,
        "n": 13502,
        "clase": "DERIVADO de A, B y A∪B de MAESTRA34-L5 P4 -- sin IC propio; no es MEDIDO",
        "fuente": "milpa/tramite.yaml:1312 y milpa/tramite-ola5-propuesta-v0.yaml:1127",
    },
    "informal_cualquiera": {
        "p": 0.561920,
        "ic95": [0.549922, 0.573502],
        "n": 13502,
        "clase": "MEDIDO·p(tasa base ponderada, sensibilidad B_solo_informal)",
        "fuente": "milpa/tramite.yaml:1317 y milpa/tramite-ola5-propuesta-v0.yaml:1131",
    },
    "adopta_encig2025_luz": {
        "p": 0.673393,
        "ic95": [0.663165, 0.683910],
        "n": 20203,
        "clase": "MEDIDO·p(tasa base ponderada, universo N_TRA=01)",
        "fuente": "milpa/tramite.yaml:400 (p) y milpa/tramite.yaml:427-432 (ic95/n/ponderador/universo)",
    },
    "evade_norma_envipe2025": {
        "p": 0.562774,
        "ic95": [0.551982, 0.573448],
        "n": 40280,
        "clase": "MEDIDO·p(tasa base ponderada, unidad delito)",
        "fuente": "milpa/tramite.yaml:497 (p) y milpa/tramite.yaml:519-524 (ic95/n/ponderador/universo)",
    },
}

# Desenlace por bloque de ejes. La clave es (id de regla, nombre del bloque
# `desenlaces:`, o "" cuando la regla trae `ejes:` plano). El nombre sale
# del propio yaml (`desenlaces.<b>.nombre`) donde existe; donde la regla es
# plana, de la regla madre que su `fuente_regla` cita.
DESENLACE_DE_BLOQUE = {
    ("dinero.ahorro.via_informal_ejes_enif2024", "principal"): "ahorra_solo_informal",
    ("dinero.ahorro.via_informal_ejes_enif2024", "secundario"): "informal_cualquiera",
    ("tramite.gobierno_digital.util_sin_coercion_ejes_encig2025", ""): "adopta_encig2025_luz",
    ("tramite.evasion_norma_ejes_envipe2025", ""): "evade_norma_envipe2025",
    # ENUT no tiene desenlace binario común: `reparto_hogar` es un
    # ESTIMADOR DE RAZÓN sobre hogares y `sexo_edad` una MEDIA de horas
    # sobre personas. Se deja fuera a propósito -- el dictamen lo declara.
    ("familia.cuidado.reparto_mujeres40_ejes_enut2024", ""): None,
}

# Reservas de validez que NO bloquean la emisión (la firma de mesa pone
# cuatro condiciones: desenlace, universo, unidad y ola) pero que la
# emisión lleva encima, campo por campo.
RESERVAS_DE_EJE = {
    ("dinero.ahorro.via_informal_ejes_enif2024", "principal", "cuenta_formal"):
        "ANIDAMIENTO-POR-CUESTIONARIO: P5_4_* gatea a P5_6_*, así que en la "
        "celda `sin cuenta` el desenlace principal se reduce a "
        "informal_cualquiera por construcción (propuesta:1489-1492). El eje "
        "es NO-FALSABLE contra este desenlace; la composición es aritmética "
        "y se emite, rotulada.",
}


def _lineas(ruta: Path) -> list[str]:
    return ruta.read_text(encoding="utf-8").splitlines()


def _linea_de(lineas: list[str], patron: str, desde: int = 0) -> int | None:
    """1-indexada, primera coincidencia a partir de `desde` (0-indexado)."""
    rx = re.compile(patron)
    for i in range(desde, len(lineas)):
        if rx.search(lineas[i]):
            return i + 1
    return None


def _reglas_ejes() -> tuple[dict, list[str]]:
    d = yaml.safe_load(PROPUESTA.read_text(encoding="utf-8"))
    reglas = {r["id"]: r for r in d["reglas_propuestas"] if "_ejes_" in r.get("id", "")}
    return reglas, _lineas(PROPUESTA)


def _bloques_de_ejes(regla: dict) -> dict[str, list[dict]]:
    """{nombre_de_bloque: [eje, ...]}. `""` para la regla de `ejes:` plano."""
    if "desenlaces" in regla:
        return {b: v.get("ejes") or [] for b, v in regla["desenlaces"].items()}
    return {"": regla.get("ejes") or []}


def _parte_el_par(par: str, nombres) -> tuple[str, str]:
    """`escolaridad_proxyxsexo` -> (`escolaridad_proxy`, `sexo`).

    El marcador serializa el par como `f"{a}x{b}"` y hay ejes con `x`
    adentro (`escolaridad_proxy`), así que partir por la PRIMERA `x` da
    (`escolaridad_pro`, `yxsexo`) y pierde el par entero. Se parte contra
    los nombres de eje que la regla declara, no contra el separador.
    """
    nombres = set(nombres)
    cand = [(par[:i], par[i + 1:]) for i, c in enumerate(par) if c == "x"]
    exactos = [(a, b) for a, b in cand if a in nombres and b in nombres]
    if len(exactos) == 1:
        return exactos[0]
    if len(exactos) > 1:
        raise ValueError(f"par ambiguo contra los ejes de la regla: {par} -> {exactos}")
    # ningún corte casa: se devuelve el primero para que el dictamen lo
    # declare DESENLACE-NO-COMPARTIDO con el nombre crudo a la vista.
    return cand[0] if cand else (par, "")


def pares_reservados() -> list[dict]:
    """Las filas `RESERVADA` del marcador, tal cual las dejó #873."""
    filas = []
    with MARCADOR.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    for f in csv.DictReader(lineas, delimiter="\t"):
        if f["estado"] == "RESERVADA":
            filas.append(f)
    return filas


def _contexto(regla: dict, bloque: str, lineas: list[str], l0: int) -> dict:
    """Universo / unidad / ola / ponderador que gobiernan un bloque de ejes.

    Los cuatro son de la REGLA (el árbitro no los redeclara por eje); lo
    que sí vive por eje es `cobertura` y `universo_restringido`, que es
    justo lo que A-bis 4 mira.
    """
    pond = regla.get("ponderador")
    return {
        "universo": regla.get("universo", ""),
        "unidad_dato": _unidad(regla),
        "ola": _ola(regla),
        "ponderador": pond if isinstance(pond, str) else json.dumps(pond, ensure_ascii=False),
        "linea_regla": l0,
    }


def _unidad(regla: dict) -> str:
    """La unidad del ÁRBITRO, leída de `payload:` -- no la del marcador.

    El marcador escribe `unidad_dato` por regla vía `_unidad_dato()`; para
    ENCIG esa columna dice `persona` mientras el árbitro dice TRÁMITE. La
    emisión hereda la del árbitro, que es la que el encargo nombra.
    """
    p = (regla.get("payload") or "")
    m = re.search(r"unidad\s*=\s*([^·]+)", p)
    return m.group(1).strip() if m else "NO-DECLARADA-EN-PAYLOAD"


def _ola(regla: dict) -> str:
    p = (regla.get("payload") or "")
    m = re.match(r"\s*([A-ZÁÉÍÓÚÑ]+\s+\d{4})", p)
    return m.group(1) if m else "NO-DERIVABLE-DEL-PAYLOAD"


def dictamen() -> list[dict]:
    """P1. Una fila por (par RESERVADA × bloque de desenlace)."""
    reglas, lineas = _reglas_ejes()
    salida = []
    for fila in pares_reservados():
        rid = fila["regla_o_eje_origen"]
        regla = reglas[rid]
        nombres_regla = {e["eje"] for es in _bloques_de_ejes(regla).values() for e in es}
        a, b = _parte_el_par(fila["eje_o_par"], nombres_regla)
        l_regla = _linea_de(lineas, rf"^\s*- id: {re.escape(rid)}\s*$")
        bloques = _bloques_de_ejes(regla)
        for bloque, ejes in bloques.items():
            por_nombre = {e["eje"]: e for e in ejes}
            desenlace = DESENLACE_DE_BLOQUE.get((rid, bloque), "SIN-MAPEO")
            ctx = _contexto(regla, bloque, lineas, l_regla)
            causas, reservas = [], []

            faltan = [x for x in (a, b) if x not in por_nombre]
            if faltan:
                causas.append(
                    f"DESENLACE-NO-COMPARTIDO: el eje `{'`, `'.join(faltan)}` no existe "
                    f"bajo el desenlace `{bloque or 'único'}` de {rid}")
            if desenlace is None:
                causas.append(
                    "SIN-DESENLACE-BINARIO-COMUN: los dos ejes de esta regla no miden "
                    "el mismo evento (uno es estimador de RAZÓN sobre hogares, el otro "
                    "una MEDIA de horas sobre personas); no hay nacional que restar y "
                    "el logit no está definido fuera de [0,1]")
            elif desenlace == "SIN-MAPEO":
                causas.append(f"SIN-MAPEO-DE-DESENLACE para ({rid}, {bloque})")

            nac = NACIONALES.get(desenlace) if isinstance(desenlace, str) else None

            for nombre in (a, b):
                e = por_nombre.get(nombre)
                if e is None:
                    continue
                if e.get("universo_restringido"):
                    causas.append(
                        f"A-BIS-4 UNIVERSO-RESTRINGIDO: el eje `{nombre}` cubre "
                        f"{e.get('cobertura')} del universo de la regla y el árbitro lo "
                        f"marca `universo_restringido: true`; no reconcilia contra el "
                        f"marginal poblacional ni contra el nacional")
                for c in e.get("celdas") or []:
                    p = c.get("p")
                    if p is None:
                        causas.append(f"MARGINAL-SIN-PUNTO: `{nombre}` / `{c.get('celda')}`")
                    elif not (0.0 < p < 1.0):
                        causas.append(
                            f"MARGINAL-DEGENERADO: `{nombre}` / `{c.get('celda')}` p={p} "
                            f"(el logit diverge; no se recorta ni se sustituye)")
                r = RESERVAS_DE_EJE.get((rid, bloque, nombre))
                if r:
                    reservas.append(f"{nombre}: {r}")

            if nac is None and not causas:
                causas.append(f"NACIONAL-NO-SELLADO para el desenlace `{desenlace}`")
            elif nac is not None and not (0.0 < nac["p"] < 1.0):
                causas.append(f"NACIONAL-DEGENERADO p={nac['p']}")

            n_celdas = (len(por_nombre[a]["celdas"]) * len(por_nombre[b]["celdas"])
                        if not faltan else 0)
            salida.append({
                "celda_id_marcador": fila["celda_id"],
                "regla": rid,
                "bloque_desenlace": bloque or "unico",
                "desenlace_id": desenlace if isinstance(desenlace, str) else "NINGUNO",
                "par": f"{a}x{b}",
                "veredicto": "NO-EMITIBLE" if causas else "EMITIBLE",
                "causa": " | ".join(causas),
                "reserva": " | ".join(reservas),
                "n_celdas": n_celdas,
                "unidad_dato_arbitro": ctx["unidad_dato"],
                "unidad_dato_marcador": fila["unidad_dato"],
                "ola": ctx["ola"],
                "ponderador": ctx["ponderador"],
                "universo": ctx["universo"],
                "nacional_p": "" if nac is None else nac["p"],
                "nacional_clase": "" if nac is None else nac["clase"],
                "nacional_fuente": "" if nac is None else nac["fuente"],
                "linea_regla_yaml": f"milpa/tramite-ola5-propuesta-v0.yaml:{ctx['linea_regla']}",
            })
    return salida


def _rango_diagnostico(ca: dict, cb: dict, nac: dict) -> tuple | None:
    """NO es un IC. Es el recorrido del punto C2 cuando cada marginal se
    mueve a los extremos de SU IC95, uno a uno y sin covarianza -- ocho
    esquinas cuando los tres tienen IC, menos cuando alguno no lo tiene.
    Se reporta rotulado como diagnóstico, nunca como incertidumbre."""
    def bordes(m):
        ic = m.get("ic95")
        return [m["p"]] if not ic else [ic[0], ic[1]]
    vals = []
    for pa in bordes(ca):
        for pb in bordes(cb):
            for pn in bordes(nac):
                if not all(0.0 < x < 1.0 for x in (pa, pb, pn)):
                    return None
                vals.append(piso_log_aditivo(
                    {"desenlace_id": "d", "p": pa},
                    {"desenlace_id": "d", "p": pb},
                    {"desenlace_id": "d", "p": pn})["p"])
    return (min(vals), max(vals))


def emisiones() -> list[dict]:
    """P2. Una fila por celda de cada par EMITIBLE del dictamen."""
    reglas, _ = _reglas_ejes()
    filas = []
    for d in dictamen():
        if d["veredicto"] != "EMITIBLE":
            continue
        regla = reglas[d["regla"]]
        bloque = "" if d["bloque_desenlace"] == "unico" else d["bloque_desenlace"]
        ejes = {e["eje"]: e for e in _bloques_de_ejes(regla)[bloque]}
        a, b = _parte_el_par(d["par"], ejes)
        nac = NACIONALES[d["desenlace_id"]]
        for ca in ejes[a]["celdas"]:
            for cb in ejes[b]["celdas"]:
                punto = piso_log_aditivo(
                    {"desenlace_id": d["desenlace_id"], "p": ca["p"]},
                    {"desenlace_id": d["desenlace_id"], "p": cb["p"]},
                    {"desenlace_id": d["desenlace_id"], "p": nac["p"]})["p"]
                rango = _rango_diagnostico(ca, cb, nac)
                filas.append({
                    "resultado_id": _result_id(d, ca, cb),
                    "celda_id_marcador": d["celda_id_marcador"],
                    "regla": d["regla"],
                    "desenlace_id": d["desenlace_id"],
                    "par": d["par"],
                    "celda_a": ca["celda"], "celda_b": cb["celda"],
                    "p_a": ca["p"], "p_b": cb["p"], "p_nacional": nac["p"],
                    "n_a": ca.get("n"), "n_b": cb.get("n"), "n_nacional": nac["n"],
                    "p_c2": punto,
                    "escala": "proporcion",
                    "unidad_dato": d["unidad_dato_arbitro"],
                    "universo": d["universo"],
                    "ola": d["ola"],
                    "ponderador": d["ponderador"],
                    "supuesto": "sin-interaccion",
                    "tipo_incertidumbre": "NO-PROPAGADA-COVARIANZA-NO-SELLADA",
                    "ic95_inf": "", "ic95_sup": "",
                    "diagnostico_rango_inf": "" if rango is None else rango[0],
                    "diagnostico_rango_sup": "" if rango is None else rango[1],
                    "diagnostico_rango_es_ic": "NO",
                    "estado": "EMITIDA-SIN-EVALUAR",
                    "reserva": d["reserva"],
                    "cotas_frechet_n": _frechet(ca.get("n"), cb.get("n"), nac["n"]),
                })
    return filas


def _frechet(na, nb, N) -> str:
    """Lo único que los márgenes acreditan sobre la intersección (H4).
    No entra al punto: viaja como contexto de soporte."""
    if na is None or nb is None or not N:
        return "NO-DERIVABLE"
    return f"[{max(0, na + nb - N)}, {min(na, nb)}]"


_SLUG = re.compile(r"[^A-Z0-9]+")


def _slug(s: str) -> str:
    return _SLUG.sub("-", str(s).upper()).strip("-")


def _result_id(d: dict, ca: dict, cb: dict) -> str:
    return (f"RESULT-C2COMP-{_slug(d['desenlace_id'])}-{_slug(d['par'])}"
            f"-{_slug(ca['celda'])}-X-{_slug(cb['celda'])}")



def _escribe_tsv(ruta: Path, filas: list[dict], cabecera_comentario: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    campos = list(filas[0].keys())
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        fh.write(cabecera_comentario.rstrip("\n") + "\n")
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)


def main(argv: list[str]) -> int:
    modo = argv[1] if len(argv) > 1 else "dictamen"
    if modo == "dictamen":
        filas = dictamen()
        _escribe_tsv(
            RAIZ / "data" / "corrida0" / "c2-compuesto-dictamen-v1_0.tsv", filas,
            "# DERIVADO — NO EDITAR (tools/c2_compuesto.py dictamen, "
            "ACTO GEN2-C2-COMPUESTO-RESERVADAS-1)")
        em = sum(1 for f in filas if f["veredicto"] == "EMITIBLE")
        print(f"DICTAMEN · filas={len(filas)} EMITIBLE={em} "
              f"NO-EMITIBLE={len(filas) - em} "
              f"pares_reservados_examinados={len(pares_reservados())} "
              f"celdas_emitibles={sum(f['n_celdas'] for f in filas if f['veredicto'] == 'EMITIBLE')}")
    elif modo == "emisiones":
        filas = emisiones()
        _escribe_tsv(
            RAIZ / "data" / "corrida0" / "c2-compuesto-emisiones-v1_0.tsv", filas,
            "# DERIVADO — NO EDITAR (tools/c2_compuesto.py emisiones, "
            "ACTO GEN2-C2-COMPUESTO-RESERVADAS-1) · EMITIDA-SIN-EVALUAR: "
            "excluida de la estimación adoptada del motor")
        print(f"EMISIONES · celdas={len(filas)} "
              f"tipo_incertidumbre=NO-PROPAGADA-COVARIANZA-NO-SELLADA (0 IC)")
    else:
        print(f"modo desconocido: {modo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
