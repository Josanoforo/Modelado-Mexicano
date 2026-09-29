#!/usr/bin/env python3
"""Inventario de olas reservadas y vista de aperturas — ACTO GEN2-APERTURAS-PREREGISTRADAS-1.

Uso:
    python3 forense/prereg-aperturas/inventario_aperturas.py            # imprime (no escribe; D-23)
    python3 forense/prereg-aperturas/inventario_aperturas.py --escribe  # escribe la vista y los expedientes mínimos
    python3 forense/prereg-aperturas/inventario_aperturas.py --verifica # 0 si la vista casa con la derivación

Universo (A.15, por id y por contrato):
  (1) todo id del manifiesto que `tools/corpus_loader.motivo_reserva` reserva: campo `estado_reserva` que
      empieza por RESERVADA, o `RESERVA_FUERA_DEL_MANIFIESTO` (firmas R04/R05/R06 y régimen de la memoria);
      una sola definición de «reservado», la del cargador (D-15: ningún parámetro en dos sitios);
  (2) toda ola que un CALC sellado declara RESERVADA (E.6) y no-input en su `spec.yaml`
      (`contendientes_declarados()`); su fila la aporta el expediente que la sirve;
  (3) los expedientes completos `forense/prereg-aperturas/<X>/medidor_apertura_*.py` (su `CONTRATO`).
Estado vigente: el de la fuente, salvo lo que una firma o un código congelado ya cambió (`ESTADO_POR_FIRMA`,
cada fila con su cita). `cruces_vistos` se deriva: todo `CALC-*/spec.yaml` que nombra un id de la fila.
"""
from __future__ import annotations

import functools
import glob
import importlib.util
import os
import re
import sys
from collections import defaultdict

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VISTA = "data/corrida0/aperturas-pendientes-v1_0.tsv"
EXP = "forense/prereg-aperturas"
COLUMNAS = ("programa", "ola", "estado_vigente", "n_ids", "ids", "fuente_reserva", "contendientes", "familia",
            "cruces_vistos", "expediente", "que_la_abre", "firma_que_faltaria", "nota")

# CALC que declaran una ola RESERVADA pero cuya R ya se adjudicó por código congelado (cita = CALC adjudicador).
YA_ADJUDICADOS = {
    "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001": "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001/0002 (ejecucion.json)",
    "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001": "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001 (ejecucion.json)",
    "CALC-C2-COMPUESTO-IC-ENVIPE2025-0001": "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001 (23/sep): R sellada de las 38 celdas; C2 coincide 35/38 a 1e-6",
}

# (programa, ola) -> (estado_vigente, cita). Sólo lo que una firma o un código congelado cambió.
ESTADO_POR_FIRMA = {
    ("CAAS", "2015"): ("LEVANTADA-POR-ESCRITO", "R09 (a), ADENDA-1 de TRAMITE-FIRMAS-21; payloads siguen en reserva_respondentes: NC-260928-GEN2-TRAMITE-FIRMAS-21-8560-01"),
    ("ENG", "2009"): ("LEVANTADA-POR-ESCRITO", "R09 (a) (ENGPEE 2010 en la firma = cc1 eng_2009), ADENDA-1 de TRAMITE-FIRMAS-21; NC-260928-GEN2-TRAMITE-FIRMAS-21-8560-01"),
    ("MIGRACION", "2002"): ("LEVANTADA-POR-ESCRITO", "R09 (a) (MSM 2002 en la firma), ADENDA-1 de TRAMITE-FIRMAS-21; NC-260928-GEN2-TRAMITE-FIRMAS-21-8560-01"),
    ("ENCRIGE", "2016"): ("ABIERTA-COMO-VISTA", "R09 (a): «ENCRIGE 2016 queda como ola vista», ADENDA-1 de TRAMITE-FIRMAS-21"),
    ("ENVIPE", "2026"): ("RESERVA-PARCIAL", "abierto sólo lo que emitieron CALC-DUELO-ENVIPE2026-ADJUDICACION-0001 (22/sep) y -MARGINALES-ADJUDICACION-0001 (23/sep): «lo que no emita este CALC sigue RESERVADA»"),
    ("ENIF", "2024"): ("RESERVA-PARCIAL", "módulo 7 RESERVADA (R06, ADENDA-1 de TRAMITE-FIRMAS-21); de los 14 cruces RESERVADA del marcador: 9 con emisión C2 (desenlace informal_cualquiera, 68 celdas) en el expediente ENIF-2024 (la mitad ahorra_solo_informal ya tiene R en CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001) y 5 sin emisión sólo por mesa; lo demás abierto por CALC-C2-COMPUESTO-IC-ENIF2024-0001, CALC-DIN-* y CALC-ARBITRO-MARGINALES-ENIF2024-0001"),
    ("ENIGH", "2024"): ("RESERVA-PARCIAL", "memoria §1 «salvo seis columnas AMAI (C7)»; abierto además la columna remesas (CALC-ENIGH-DUELO-ADJUDICACION-0001, guardián tools/enigh_duelo_guardian.py)"),
    ("ENVIPE", "2025"): ("ABIERTA-POR-CODIGO-CONGELADO", "los 4 cruces que data/corrida0/marcador-segmento.tsv aún marca RESERVADA (38 celdas) tienen R sellada en CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001 (23/sep); el marcador está desfasado (pares_piloteados reconoce un par por programa: hallazgo); marginales por CALC-ARBITRO-MARGINALES-ENVIPE2025-0001; memoria §1: abierta"),
    ("ENUT", "2024"): ("RESERVA-PARCIAL", "1 cruce RESERVADA sin emisión en data/corrida0/marcador-segmento.tsv (NC-0328); ningún contendiente sellado"),
    ("ENCIG", "2025"): ("ABIERTA-POR-CODIGO-CONGELADO", "FP-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-01: cierre de la reserva por CALC-ENCIG-DUELO-2025-ADJUDICACION-0001/0002; «fuera del árbitro» (encargo) sin celda RESERVADA en el marcador"),
    ("ENDUTIH", "2025"): ("RESERVADA", "R05 RESERVADA (ADENDA-1 de TRAMITE-FIRMAS-21); hallazgo: tres CALC sellados ya consumen el payload (cruces_vistos)"),
    ("CSES", "MODULO5-2016-2021"): ("RESERVADA", "R04 RESERVADA (ADENDA-1 de TRAMITE-FIRMAS-21)"),
    ("ENCO", "TODAS"): ("RESERVADA", "memoria §1 «Reservas: … ENCO»: el programa entero; corpus_loader `(^|_)enco(_|$)`"),
}
FAMILIA_2027 = "NINGUNA"  # las 8 familias de familias-2027-estado-v1_0.tsv apuntan a olas 2027 (EJECUTADO en la nota)

_RE_DECLARA = re.compile(r"ola_reservada:|RESERVAD[AO][^\n]*no (es|son) input|RESERVADA para estos reactivos")


def _carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@functools.lru_cache(maxsize=1)
def _manifiesto():
    with open(os.path.join(RAIZ, "data", "manifiesto.yaml"), encoding="utf-8") as f:
        return yaml.load(f, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


@functools.lru_cache(maxsize=1)
def _loader():
    return _carga(os.path.join(RAIZ, "tools", "corpus_loader.py"), "corpus_loader_inv")


def _reservadas():
    cl = _loader()
    return [e for e in _manifiesto() if cl.motivo_reserva(e["id"], e)]


def reservados_del_manifiesto():
    return [e["id"] for e in _reservadas()]


def archivos_reservados_del_manifiesto():
    return [str(e["archivo"]) for e in _reservadas() if e.get("archivo")]


def programa_ola(i: str):
    if re.search(r"(^|_)enco(_|$)", i):
        return "ENCO", "TODAS"
    m = re.match(r"cc1_inegi_([a-z]+)_(\d{4})(t\d)?__", i)
    if m:
        return m.group(1).upper(), m.group(2) + (m.group(3).upper() if m.group(3) else "")
    m = re.match(r"oe1_([a-z]+)_(\d{4})_", i)
    if m:
        return m.group(1).upper(), m.group(2)
    if i.startswith("cses5_"):
        return "CSES", "MODULO5-2016-2021"
    m = re.match(r"enoe_(\d{4})_(\d)t_", i)
    if m:
        return "ENOE", f"{m.group(1)}T{m.group(2)}"
    m = re.match(r"([a-z]+?)_?(\d{4})(?:_|$)", i)
    if m:
        return m.group(1).upper(), m.group(2)
    return i.upper(), "?"


@functools.lru_cache(maxsize=1)
def _specs():
    out = {}
    for p in sorted(glob.glob(os.path.join(RAIZ, "data", "corrida0", "CALC-*", "spec.yaml"))):
        with open(p, encoding="utf-8") as f:
            out[os.path.basename(os.path.dirname(p))] = f.read()
    return out


def contendientes_declarados():
    """CALC sellados (con sello.json) cuyo spec.yaml declara, en sus primeras 200 líneas, una ola RESERVADA
    que no es input."""
    out = []
    for c, t in _specs().items():
        if not os.path.exists(os.path.join(RAIZ, "data", "corrida0", c, "sello.json")):
            continue
        if _RE_DECLARA.search("\n".join(t.splitlines()[:200])):
            out.append(c)
    return sorted(out)


@functools.lru_cache(maxsize=1)
def expedientes():
    out = {}
    for p in sorted(glob.glob(os.path.join(AQUI, "*", "medidor_apertura_*.py"))):
        M = _carga(p, "inv_" + os.path.basename(p)[:-3])
        C = M.CONTRATO
        out[(C["programa"], C["ola"])] = (C["x"], list(C["contendientes"]), [pid for pid, _n in C["payloads"]])
    return out


def _dir(prog, ola):
    return f"{EXP}/{prog}-{ola}"


def filas():
    g = defaultdict(list)
    fuente = {}
    cl = _loader()
    for e in _reservadas():
        k = programa_ola(e["id"])
        g[k].append(e["id"])
        fuente.setdefault(k, set()).add(cl.motivo_reserva(e["id"], e).split(":")[0].split("→")[0].strip())
    exps = expedientes()
    specs = _specs()
    out = []
    for k in sorted(set(g) | set(exps) | set(ESTADO_POR_FIRMA)):
        prog, ola = k
        x, cont, pay = exps.get(k, (None, [], []))
        ids = sorted(set(g.get(k, [])) | set(pay))
        pat = re.compile(r"\b(?:" + "|".join(map(re.escape, ids)) + r")\b") if ids else None
        vistos = sorted(c for c, t in specs.items() if pat and pat.search(t) and c not in cont)
        estado, cita = ESTADO_POR_FIRMA.get(k, (None, ""))
        if estado is None:
            estado = "RESERVADA" if k in g else "RESERVA-POR-ESTIMANDO"
        fr = ";".join(sorted(fuente.get(k, set()))) or "spec sellada del contendiente (E.6: «RESERVADA, no es input»)"
        nota = [cita] if cita else []
        if k not in g and x:
            nota.append("payload sin estado_reserva y no reservado por corpus_loader: la reserva la declara el contendiente (hallazgo)")
        if x:
            abre = f"CODIGO-CONGELADO del expediente {x} en caja (receta de un commit)"
            falta = f"FIRMA-DE-MESA que congele {_dir(prog, ola)} y autorice su apertura"
        elif estado == "LEVANTADA-POR-ESCRITO":
            abre, falta = "YA-LEVANTADA-POR-ESCRITO (falta mover los payloads fuera de reserva_respondentes, CAJA)", "NINGUNA"
        elif estado in ("ABIERTA-COMO-VISTA", "ABIERTA-POR-CODIGO-CONGELADO"):
            abre, falta = "YA-ABIERTA", "NINGUNA"
        else:
            abre = "SOLO-MESA-POR-ESCRITO (sin contendiente sellado que la espere)"
            falta = "FIRMA-DE-MESA por escrito (regla 6: ningún contendiente nuevo en esta etapa)"
        out.append({"programa": prog, "ola": ola, "estado_vigente": estado, "n_ids": str(len(ids)),
                    "ids": ";".join(ids), "fuente_reserva": fr, "contendientes": ";".join(cont) or "NINGUNO",
                    "familia": FAMILIA_2027, "cruces_vistos": ";".join(vistos) or "NINGUNO",
                    "expediente": _dir(prog, ola), "que_la_abre": abre, "firma_que_faltaria": falta,
                    "nota": " · ".join(nota)})
    return out


def _tsv(rows):
    # Cabecera de procedencia, no `# DERIVADO — NO EDITAR`: esa marca reserva el archivo al canal
    # [deriva] (tools/derivados_protegidos.py); esta vista viaja versionada, como el crosswalk de carriles.
    lin = [f"# {VISTA} · ACTO GEN2-APERTURAS-PREREGISTRADAS-1 · derivado por `python3 forense/prereg-aperturas/inventario_aperturas.py --escribe` (--verifica compara byte a byte). Nunca a mano.",
           "\t".join(COLUMNAS)]
    lin += ["\t".join(r[c].replace("\t", " ") for c in COLUMNAS) for r in rows]
    return "\n".join(lin) + "\n"


def _minimo(r):
    b = f"{r['programa']}-{r['ola']}"
    if r["que_la_abre"].startswith("SOLO-MESA"):
        linea = f"- **Sin prueba pre-registrada: solo mesa por escrito.** Qué la abre: {r['que_la_abre']}."
    else:
        linea = f"- Qué la abre: {r['que_la_abre']}."
    return (f"# Expediente mínimo de apertura · {r['programa']} {r['ola']}\n\n"
            f"Derivado por `forense/prereg-aperturas/inventario_aperturas.py --escribe` (ACTO GEN2-APERTURAS-PREREGISTRADAS-1).\n\n"
            f"- Estado vigente: `{r['estado_vigente']}` · fuente de la reserva: {r['fuente_reserva']} · ids ({r['n_ids']}): "
            f"fila `{b}` de `{VISTA}`.\n"
            f"- Contendientes sellados que la esperan como R: **{r['contendientes']}** · familia 2027: **{r['familia']}**.\n"
            f"- Cruces vistos (CALC sellados que consumen un id): {r['cruces_vistos']}.\n"
            f"{linea}\n"
            f"- Nota: {r['nota'] or '—'}\n")


def main(argv):
    rows = filas()
    if "--verifica" in argv:
        ruta = os.path.join(RAIZ, VISTA)
        casa = os.path.exists(ruta) and open(ruta, encoding="utf-8").read() == _tsv(rows)
        print(f"{VISTA}: {'CASA' if casa else 'NO-CASA'}")
        return 0 if casa else 1
    if "--escribe" not in argv:
        sys.stdout.write(_tsv(rows))
        return 0
    with open(os.path.join(RAIZ, VISTA), "w", encoding="utf-8") as f:
        f.write(_tsv(rows))
    for r in rows:
        d = os.path.join(RAIZ, r["expediente"])
        minimo = os.path.join(d, f"EXPEDIENTE-{os.path.basename(d)}.md")
        if r["contendientes"] == "NINGUNO":
            os.makedirs(d, exist_ok=True)
            with open(minimo, "w", encoding="utf-8") as f:
                f.write(_minimo(r))
        elif os.path.exists(minimo):
            os.remove(minimo)
    print(f"filas={len(rows)} ids={sum(int(r['n_ids']) for r in rows)} vista={VISTA}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
