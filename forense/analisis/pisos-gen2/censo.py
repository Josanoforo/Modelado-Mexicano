#!/usr/bin/env python3
"""Censo de origen de los pisos que consume el programa (ACTO GEN2-PISOS-GEN2-2, P1).

Generaliza el censo de ACTO GEN2-ENCIG-PISOS-GEN2-1 (#1116,
`forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv`, hecho a mano
sobre 5 celdas-D) a todo el árbol:

  A · las 21 celdas-D de `data/curacion-registro/celdas-d/` -- las 5 con
      `champion_actual: C2` una fila por sub-celda de `adjudicacion_por_celda`
      (es lo que el marcador consume, `tools/marcador_segmento.py::_celdas_d_c2`);
      las otras 16 una fila por celda, con el candidato que su
      `champion_actual` nombra (o el C2 si no hay champion);
  B · los 57 pisos del árbitro de marginales
      (`forense/prereg-caja/ARBITRO-MARGINALES-metadatos-v1_0.tsv`, columna
      `calc_piso`), que el marcador consume como piso de las filas MARGINAL.

Método: se sigue la cadena del PUNTO, no la de todos los inputs. Un CALC lee
muchos inputs que no alimentan su punto (oro, controles, sellos): recorrerlos
todos marcaría LEGACY a un piso cuyo número sale de microdato (p. ej. el -0002
de ENCIG lee el -0001 como oro). Por eso cada CALC emisor lleva en `PUNTO`
la lista declarada de lo que alimenta su punto, con la línea del medidor que
lo prueba. Un CALC sin entrada en `PUNTO` sale `SIN-CLASE` -- el censo no
infiere. Terminales:

  * input `origen: manifiesto`                      -> MANIFIESTO
  * input `origen: repo` bajo `milpa/`              -> LEGACY
  * `parametros.<k>` con números tecleados de milpa -> LEGACY
  * `data/curacion-registro/expedientes-produccion` / `milpa/procedencia` -> LEGACY (producción GEN1)
  * input `origen: repo` bajo `data/corrida0/CALC-X/resultados.json` -> se recursa en X

Clase: NUEVO si toda terminal del punto es MANIFIESTO; HEREDADO-DE-LEGACY si
alguna es LEGACY; HEREDADO-DE-GEN2 si llega a manifiesto pero atraviesa un CALC
sin `sello.json` (GEN2 no sellado). Con `--ref <git-ref>` lee el árbol de ese
ref (tabla «antes»).

Uso:  python3 forense/analisis/pisos-gen2/censo.py [--ref REF] [--tsv SALIDA]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[3]
CELDAS_D = "data/curacion-registro/celdas-d"
META_ARBITRO = "forense/prereg-caja/ARBITRO-MARGINALES-metadatos-v1_0.tsv"

# CALC -> (lo que alimenta el punto, prueba). Cada elemento es un input id del
# spec.yaml, `parametros:<clave>` o `ref:<ruta>` (referencia citada por la
# celda-D sin CALC). Leído en el medidor de cada CALC; la prueba es la línea.
PUNTO: dict[str, tuple[list[str], str]] = {
    # --- celdas-D con champion C2 -------------------------------------------
    "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001": (
        ["parametros:marginales_sellados_D9"],
        "medidor.py:373,391-408 compone C2-P de parametros.marginales_sellados_D9 "
        "(E1-E4, L1-L2 de milpa/tramite-ola5-propuesta-v0.yaml; NAC de milpa/tramite.yaml)"),
    "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001": (
        ["parametros:marginales_sellados"],
        "medidor.py:223,281-291 compone C2-P de parametros.marginales_sellados "
        "(milpa/tramite-ola5-propuesta-v0.yaml:1715-1731; NAC de milpa/tramite.yaml:497)"),
    "CALC-GOB-DIGITAL-EXE-EMISIONES-0002": (
        ["encig25_base_datos_csv"],
        "piloto 3: compone C2 de marginales medidos de encig25_base_datos_csv; "
        "c2_compuesto_resultados es sólo control (censo #1116, fila de mesa NUEVO)"),
    "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001": (
        ["emisiones_edadxsexo_resultados", "emisiones_escolaridadxsexo_resultados"],
        "medidor.py:637-639 copia el -C2-P de las emisiones"),
    "CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001": (
        ["c2_compuesto_resultados"], "C2 copiado de CALC-C2-COMPUESTO-RESERVADAS-0001"),
    "CALC-ENCIG-DUELO-2025-ESCOLARIDADXSEXO-EMISIONES-0001": (
        ["c2_compuesto_resultados"], "C2 copiado de CALC-C2-COMPUESTO-RESERVADAS-0001"),
    "CALC-C2-COMPUESTO-RESERVADAS-0001": (
        ["*milpa"], "compone C2 de marginales de milpa/ (censo #1116)"),
    "CALC-ENCIG-DUELO-2025-ADJUDICACION-0002": (
        ["piso_c2_resultados"],
        "C2 leído por id de CALC-ENCIG2025-PISOS-GOBDIGITAL-0001 (spec §2 del -0002)"),
    "CALC-ENCIG2025-PISOS-GOBDIGITAL-0001": (
        ["encig25_base_datos_csv"],
        "medidor.py:303 G-ORIGEN: marginales medidos de encig25_base_datos_csv; "
        "marginales_2025/adjudicacion_0001 son control"),
    # --- sucesores de este acto (P2/P3) --------------------------------------
    "CALC-ENIF2024-PISOS-AHORRO-LXE-0001": (
        ["enif2024_csv"], "piso GEN2-PISOS-GEN2-2: marginales re-medidos de ENIF 2024"),
    "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002": (
        ["piso_c2_resultados"], "C2 leído por id del piso ENIF 2024 (spec §2 del -0002)"),
    "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001": (
        ["envipe2025_csv"], "piso GEN2-PISOS-GEN2-2: marginales re-medidos de ENVIPE 2025"),
    "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002": (
        ["piso_c2_resultados"], "C2 leído por id del piso ENVIPE 2025 (spec §2 del -0002)"),
    # --- celdas-D sin champion C2 --------------------------------------------
    "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001": (
        ["marginales_2025_resultados"],
        "medidor.py:170-173,377-383 C2-P de marginales 2025 SELLADOS de "
        "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001"),
    "CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002": (
        ["EMISIONES-0001"],
        "medidor.py:221-224: PERSISTENCIA se lee de las emisiones selladas "
        "(input EMISIONES-0001); enif2024_csv es R"),
    "CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001": (
        ["PISO-2021"], "medidor.py:60: PERSISTENCIA = p_2021(celda) del input PISO-2021"),
    "CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001": (
        ["enif2021_csv"],
        "p_2021 medido de enif2021_csv; los demás inputs son medidor importado por "
        "sha y metadatos de rejilla/comparabilidad (sin números)"),
    # --- pisos del árbitro de marginales -------------------------------------
    "CALC-PISOS-ENIF2021-EJES-0003": (["enif2021_csv"], "piso t-1 medido de ENIF 2021"),
    "CALC-PISOS-ENVIPE2024-EJES-0002": (["envipe2024_csv"], "piso t-1 medido de ENVIPE 2024"),
    "CALC-PISOS-ENCIG2023-EJES-0002": (["encig23_base_datos_csv"], "piso t-1 medido de ENCIG 2023"),
    "CALC-PISOS-ENIF2021-FORMALIDAD-0001": (
        ["enif2021_csv"],
        "medidor.py:36-50: ARBITRO-OLA5-YAML (milpa/) sólo aporta la REJILLA "
        "(nombres de las dos categorías del eje, con guardia que falla si no son "
        "dos); el número sale de enif2021_csv -- ningún número de milpa/"),
    "CALC-ARBITRO-MARGINALES-ENIF2024-0001": (["enif_2024_enif_2024_bd_csv"], "R medido de ENIF 2024"),
    "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001": (["envipe2025_csv"], "R medido de ENVIPE 2025"),
    "CALC-ARBITRO-MARGINALES-ENCIG2025-0001": (["encig25_base_datos_csv"], "R medido de ENCIG 2025"),
}

LEGACY_REF = ("milpa/", "data/curacion-registro/expedientes-produccion",
              "data/curacion-registro/especificaciones-produccion",
              "data/curacion-registro/produccion-modelo")


class Arbol:
    def __init__(self, ref: str | None):
        self.ref = ref

    def lee(self, ruta: str) -> str | None:
        if self.ref is None:
            p = RAIZ / ruta
            return p.read_text(encoding="utf-8") if p.exists() else None
        r = subprocess.run(["git", "-C", str(RAIZ), "show", f"{self.ref}:{ruta}"],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    def existe(self, ruta: str) -> bool:
        if self.ref is None:
            return (RAIZ / ruta).exists()
        return subprocess.run(["git", "-C", str(RAIZ), "cat-file", "-e", f"{self.ref}:{ruta}"],
                              capture_output=True).returncode == 0

    def lista(self, carpeta: str) -> list[str]:
        if self.ref is None:
            return sorted(p.name for p in (RAIZ / carpeta).glob("*.yaml"))
        r = subprocess.run(["git", "-C", str(RAIZ), "ls-tree", "--name-only", f"{self.ref}:{carpeta}"],
                           capture_output=True, text=True, check=True)
        return sorted(n for n in r.stdout.split() if n.endswith(".yaml"))


def cadena(arbol: Arbol, calc: str, vistos: frozenset = frozenset()) -> tuple[set, list[str]]:
    """Devuelve (terminales, pasos) de la cadena del punto de `calc`."""
    if calc in vistos:
        return {"CICLO"}, [f"{calc}: ciclo"]
    if calc not in PUNTO:
        return {"SIN-CLASE"}, [f"{calc}: sin entrada en PUNTO (no se infiere)"]
    spec_txt = arbol.lee(f"data/corrida0/{calc}/spec.yaml")
    if spec_txt is None:
        return {"SIN-CLASE"}, [f"{calc}: spec.yaml ausente en el árbol"]
    spec = yaml.safe_load(spec_txt)
    ins = {i["id"]: i for i in spec.get("inputs", [])}
    params = spec.get("parametros") or {}
    fuentes, prueba = PUNTO[calc]
    terms: set = set()
    pasos = [f"{calc} [{prueba}]"]
    if not arbol.existe(f"data/corrida0/{calc}/sello.json"):
        terms.add("SIN-SELLO")
        pasos.append(f"{calc}: sin sello.json")
    for f in fuentes:
        if f == "*milpa":
            terms.add("LEGACY"); pasos.append(f"{calc}: milpa/")
        elif f.startswith("parametros:"):
            k = f.split(":", 1)[1]
            if k not in params:
                terms.add("SIN-CLASE"); pasos.append(f"{calc}: parametros.{k} ausente")
            else:
                terms.add("LEGACY"); pasos.append(f"{calc}: parametros.{k} (números tecleados de milpa/)")
        else:
            i = ins.get(f)
            if i is None:
                terms.add("SIN-CLASE"); pasos.append(f"{calc}: input {f} ausente del spec")
                continue
            if i.get("origen") == "manifiesto":
                terms.add("MANIFIESTO"); pasos.append(f"{calc}: {f} (manifiesto)")
                continue
            ruta = i.get("ruta", "")
            if ruta.startswith(LEGACY_REF):
                terms.add("LEGACY"); pasos.append(f"{calc}: {f} -> {ruta}")
            elif ruta.startswith("data/corrida0/CALC-"):
                sub = ruta.split("/")[2]
                t, p = cadena(arbol, sub, vistos | {calc})
                terms |= t; pasos.append(f"{calc}: {f} -> {sub}"); pasos += p
            else:
                terms.add("SIN-CLASE"); pasos.append(f"{calc}: {f} -> {ruta} (terminal no tipificada)")
    return terms, pasos


def clase(terms: set) -> str:
    if terms & {"SIN-CLASE", "CICLO"}:
        return "SIN-CLASE"
    if "LEGACY" in terms:
        return "HEREDADO-DE-LEGACY"
    if "SIN-SELLO" in terms:
        return "HEREDADO-DE-GEN2"
    return "NUEVO" if terms == {"MANIFIESTO"} else "SIN-CLASE"


def _calc_de_refs(refs: list[str]) -> str | None:
    """Primer CALC citado por el candidato: el que emite su punto (los
    siguientes son la adjudicación que lo consume)."""
    calcs = [r for r in refs or [] if str(r).startswith("CALC-")]
    return calcs[0] if calcs else None


def filas(arbol: Arbol) -> list[dict]:
    out = []
    for nombre in arbol.lista(CELDAS_D):
        d = yaml.safe_load(arbol.lee(f"{CELDAS_D}/{nombre}"))
        cd = d.get("celda_d", d)
        celda = nombre[:-5]
        champ = cd.get("champion_actual")
        adj = cd.get("adjudicacion_por_celda") or {}
        if champ == "C2" and adj:
            for sub, a in adj.items():
                if a.get("id_candidato") != "C2":
                    continue
                t, p = cadena(arbol, a["calc"])
                out.append(dict(universo="CELDA-D", consumido_por_marcador="SI", celda=celda,
                                sub_celda=sub, candidato="C2", calc=a["calc"],
                                resultado=a.get("resultado_puntual", ""), clase=clase(t),
                                cadena=" | ".join(p)))
            continue
        cands = cd.get("candidatos") or []
        objetivo = champ if champ not in (None, "NINGUNO") else "C2"
        cand = next((c for c in cands if c.get("id_candidato") == objetivo
                     or (objetivo.startswith("BASELINE") and c.get("rol") == "BASELINE")), None)
        refs = (cand or {}).get("production_spec_refs") or []
        calc = _calc_de_refs(refs)
        if calc:
            t, p = cadena(arbol, calc)
        else:
            leg = [r for r in refs if any(str(r).startswith(x) for x in LEGACY_REF)]
            t = {"LEGACY"} if leg else {"SIN-CLASE"}
            p = [f"sin CALC; refs: {'; '.join(map(str, refs))}"]
        out.append(dict(universo="CELDA-D", consumido_por_marcador="NO", celda=celda,
                        sub_celda="(celda)", candidato=f"{objetivo} (champion_actual={champ})",
                        calc=calc or "", resultado="", clase=clase(t), cadena=" | ".join(p)))
    meta = arbol.lee(META_ARBITRO).splitlines()
    cab = meta[0].split("\t")
    for linea in meta[1:]:
        r = dict(zip(cab, linea.split("\t")))
        t, p = cadena(arbol, r["calc_piso"])
        out.append(dict(universo="ARBITRO-MARGINALES", consumido_por_marcador="SI",
                        celda=r["marcador_celda_id"], sub_celda=f"{r['axis']}={r['category']}",
                        candidato="PISO-t-1", calc=r["calc_piso"], resultado=r["cell_id_piso"],
                        clase=clase(t), cadena=" | ".join(p)))
    return out


COLS = ["universo", "consumido_por_marcador", "celda", "sub_celda", "candidato", "calc",
        "resultado", "clase", "cadena"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref")
    ap.add_argument("--tsv")
    a = ap.parse_args()
    fs = filas(Arbol(a.ref))
    texto = "\t".join(COLS) + "\n" + "".join(
        "\t".join(str(f[c]).replace("\t", " ") for c in COLS) + "\n" for f in fs)
    if a.tsv:
        Path(a.tsv).write_text(texto, encoding="utf-8")
    from collections import Counter
    cuenta = Counter((f["universo"], f["consumido_por_marcador"], f["clase"]) for f in fs)
    for k in sorted(cuenta):
        print(*k, cuenta[k], sep="\t")
    print("filas", len(fs), "sin_clase", sum(f["clase"] == "SIN-CLASE" for f in fs), sep="\t")
    return 0


if __name__ == "__main__":
    sys.exit(main())
