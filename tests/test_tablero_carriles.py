#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_tablero_carriles.py -- guardia de `tools/tablero_carriles.py`
(ACTO GEN2-TABLERO-CARRILES-1, 28/sep/2026). Entra a CI como huérfano
(`tools/ci_guardias.py --ejecuta-huerfanos`), sin editar verify.yml ni check.py.

Defecto que atrapa (§2 del encargo): mesa decidía firmas, descargas y
prioridades por memoria y por transfers; el tablero sólo sirve si ningún
número se teclea. Falla si:
  (1) algún carril queda sin semáforo, o no son 31 tarjetas;
  (2) una línea del bloque derivado trae un número sin `⟨F…⟩` (derivado_de),
      o con una clave que no está en la cadena de procedencia;
  (3) [TABLERO-UNICO-1] los carriles no leen lo vigente: F2 no es el catálogo del puntero, F1/F3/F11 no son la
      versión más alta del árbol, `c6aa-01` (firma sobre el aparato) es stopper, o `43d6-01` (control positivo) no lo es;
  (4) la derivación no es determinista (dos corridas, dos resultados);
  (5) el crosswalk no casa con la derivación, no tiene 31 filas, o tiene una
      celda vacía (sin SIN-UNION);
  (6) la regla del semáforo no da lo declarado sobre casos sintéticos;
  (7) el lector de líneas del manifiesto difiere de yaml.safe_load.

No compara contra el md commiteado (eso lo hace `--verifica` y el canal): un PR
ajeno que mueve firmas-pendientes.tsv dejaría el md atrasado sin que este acto
tenga culpa, y el canal lo re-deriva en el push a main.

Corre sola:
    python3 tests/test_tablero_carriles.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tablero_carriles as TC  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_semaforo_sintetico():
    S = TC.semaforo
    afirma(S("GENETICA", 0.0, 1, 1, 1.0)[0] == "GRIS", "firewall GENETICA debe ser GRIS")
    afirma(S("GENOMICA", 0.0, 0, 1, 0.0)[0] == "GRIS", "firewall GENOMICA debe ser GRIS")
    afirma(S("X", TC.GRIS_NO_MEDIBLE_MIN + 0.01, 1, 1, 1.0)[0] == "GRIS", "NO-MEDIBLE mayoritario debe ser GRIS")
    afirma(S("X", TC.GRIS_NO_MEDIBLE_MIN, 1, 1, 1.0)[0] == "VERDE", "umbral GRIS es estricto (>)")
    afirma(S("X", 0.0, 0, 2, 1.0)[0] == "ROJO", "sin cifra en el núcleo debe ser ROJO")
    afirma(S("X", 0.0, 2, 2, TC.VERDE_REGLAS_MIN)[0] == "VERDE", "núcleo completo y reglas en el umbral debe ser VERDE")
    afirma(S("X", 0.0, 2, 2, TC.VERDE_REGLAS_MIN - 0.01)[0] == "AMARILLO", "reglas bajo el umbral debe ser AMARILLO")
    afirma(S("X", 0.0, 1, 2, 1.0)[0] == "AMARILLO", "núcleo incompleto con reglas debe ser AMARILLO")
    # NARANJA (firma FP-260928-GEN2-MEDICION-CARRILES-2-8fdf-01 punto 1)
    afirma(S("X", 0.0, 0, 1, 0.0, 1)[0] == "NARANJA", "núcleo sin cifra pero con piso pendiente registrado: NARANJA")
    afirma(S("X", 0.0, 1, 2, 0.0, 1)[0] == "NARANJA", "núcleo cubierto por cifra + piso pendiente: NARANJA")
    afirma(S("X", 0.0, 0, 2, 0.0, 1)[0] == "ROJO", "un núcleo sin cifra ni piso sigue ROJO")
    afirma(S("X", 0.0, 1, 3, 1.0, 1)[0] == "AMARILLO", "cifra parcial + piso parcial sin cubrir: AMARILLO")
    afirma(S("X", 0.0, 2, 2, TC.VERDE_REGLAS_MIN, 0)[0] == "VERDE", "NARANJA nunca desplaza a VERDE")
    afirma(S("GENETICA", 0.0, 0, 1, 0.0, 1)[0] == "GRIS", "firewall antes que NARANJA")
    afirma(TC.ORDEN_SEMAFORO.index("NARANJA") == TC.ORDEN_SEMAFORO.index("AMARILLO") + 1, "NARANJA entre AMARILLO y VERDE")
    afirma(TC.nucleo(TC.Counter({"A": 10, "B": 1})) == ["A"], "núcleo = dominio dominante")
    afirma(TC.nucleo(TC.Counter({"A": 5, "B": 5})) == ["A", "B"], "empate: los dos al núcleo")


def prueba_manifiesto():
    import yaml
    ids, reservas = TC.manifiesto()
    e = yaml.safe_load(open(os.path.join(ROOT, TC.FUENTES["F6"]), encoding="utf-8"))
    ids_y = {str(x["id"]) for x in e}
    res_y = sorted((str(x["id"]), str(x["estado_reserva"])) for x in e if x.get("estado_reserva"))
    afirma(ids == ids_y, f"lector de ids del manifiesto difiere de PyYAML ({len(ids)} vs {len(ids_y)})")
    afirma(sorted(reservas) == res_y, f"lector de estado_reserva difiere de PyYAML ({len(reservas)} vs {len(res_y)})")


def prueba_tablero():
    D1 = TC.derivar()
    D2 = TC.derivar()
    md1 = TC.genera(D1)
    md2 = TC.genera(D2)
    afirma(md1 == md2, "la derivación no es determinista")
    C = D1["carriles"]
    afirma(len(C) == 31, f"se esperaban 31 carriles (reports en corpus/reports/ del mapa); hay {len(C)}")
    afirma(all(c["semaforo"] in TC.ICONO for c in C), "un carril quedó sin semáforo válido")
    afirma(all(c["siguiente"]["sucesor"] for c in C), "un carril quedó sin siguiente acción")
    cuerpo = md1
    tarjetas = re.findall(r"(?m)^### (\S+) (CARRIL-\d{2}) ", cuerpo)
    afirma(len(tarjetas) == len(C), f"tarjetas {len(tarjetas)} != carriles {len(C)}")
    afirma(all(ic in TC.ICONO.values() for ic, _ in tarjetas), "una tarjeta sin icono de semáforo")
    for c in C:
        t = cuerpo.split(f" {c['carril']} · ", 1)[1].split("\n### ", 1)[0]
        afirma("**Semáforo " in t, f"{c['carril']}: sin línea de semáforo")
        afirma("**Afirmaciones " in t, f"{c['carril']}: sin línea de evidencia")
        afirma("**Stoppers" in t, f"{c['carril']}: sin línea de stoppers (ni «ninguno»)")
        afirma("**Siguiente acción**" in t, f"{c['carril']}: sin siguiente acción")
    # (2) todo número lleva derivado_de, salvo la tabla de procedencia (que ES la derivación)
    claves = set(TC.FUENTES) | {"S"}
    previo = cuerpo.split("## Cadena de procedencia", 1)[0]
    for ln in previo.splitlines():
        if not re.search(r"\d", ln) or re.fullmatch(r"\|[-:|]+\|", ln.strip()):
            continue
        tags = TC.TAG.findall(ln)
        afirma(bool(tags), f"número sin ⟨derivado_de⟩: {ln[:120]}")
        for t in tags:
            afirma(set(t.split()) <= claves, f"clave de procedencia desconocida {t}: {ln[:80]}")
    pie = cuerpo.split("## Cadena de procedencia", 1)[1]
    for k in claves:
        afirma(f"| {k} |" in pie, f"la cadena de procedencia no declara {k}")
    # (5) crosswalk
    cw = TC.crosswalk_texto(D1)
    real = open(os.path.join(ROOT, TC.CROSSWALK), encoding="utf-8").read()
    afirma(cw == real, "canon/crosswalk-carriles-v1_0.tsv no casa con la derivación (python3 tools/tablero_carriles.py --crosswalk)")
    filas = [ln.split("\t") for ln in cw.splitlines() if ln and not ln.startswith("#")]
    cab, datos = filas[0], filas[1:]
    afirma(len(datos) == 31, f"crosswalk con {len(datos)} filas")
    for f in datos:
        afirma(len(f) == len(cab), f"crosswalk: fila con {len(f)} celdas")
        afirma(all(x.strip() for x in f), f"crosswalk: celda vacía en {f[0]}")


def prueba_vigentes():
    """Criterio 3 de GEN2-TUBERIA-TABLERO-UNICO-1, sobre la salida de `tablero_carriles.py --json`."""
    import json
    import subprocess
    salida = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "tablero_carriles.py"), "--json"],
                            capture_output=True, text=True, cwd=ROOT)
    afirma(salida.returncode == 0, f"--json falló: {salida.stderr[-200:]}")
    D = json.loads(salida.stdout)
    proc = {k: v["archivo"] for k, v in D["procedencia"].items()}
    vig = json.load(open(os.path.join(ROOT, "docs/data/catalogo-vigente.json"), encoding="utf-8"))["catalogo"]
    afirma(proc["F2"] == f"canon/catalogo-del-mexicano-{vig}.tsv", f"F2 no es el catálogo del puntero ({vig}): {proc['F2']}")

    def alta(dirrel, patron):
        rx = re.compile(patron + r"-v(\d+)_(\d+)\.tsv$")
        vs = [(int(m.group(1)), int(m.group(2)), f) for f in os.listdir(os.path.join(ROOT, dirrel))
              for m in [rx.match(f)] if m]
        return dirrel + "/" + max(vs)[2]
    for k, d, p in (("F1", "canon", "mapa-dominios"), ("F3", "canon", "reglas-contrastadas"),
                    ("F11", "forense/analisis/familias-2027", "familias-2027-estado")):
        afirma(proc[k] == alta(d, p), f"{k} no es la versión más alta de su serie: {proc[k]} != {alta(d, p)}")
    stop = {}
    for c in D["carriles"]:
        for st in c["stoppers"].get("FIRMA", []):
            stop.setdefault(st["id"], set()).add(c["carril"])
    afirma("FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01" not in stop,
           "c6aa-01 (firma sobre el aparato) es stopper de " + str(sorted(stop.get("FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01", []))))
    afirma("FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01" not in json.dumps([c["siguiente"] for c in D["carriles"]]),
           "c6aa-01 es siguiente acción de un carril")
    ctl = stop.get("FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01", set())
    afirma({"CARRIL-03", "CARRIL-18"} <= ctl, f"control positivo 43d6-01: debe frenar CARRIL-03 y CARRIL-18; frena {sorted(ctl)}")


def main():
    prueba_semaforo_sintetico()
    prueba_tablero()
    prueba_manifiesto()
    prueba_vigentes()
    if FAILS:
        for f in FAILS:
            print("FAIL:", f)
        sys.exit(1)
    print("OK test_tablero_carriles: semáforo sintético, 31 tarjetas, derivado_de por línea, determinismo, crosswalk, manifiesto, versiones vigentes y firmas de aparato")


if __name__ == "__main__":
    main()
