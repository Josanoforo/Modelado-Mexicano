"""P3/P4 de ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · ensamblado y conteos, derivados.

· Lee los fragmentos `<PIEZA>-dictamenes.tsv` de este directorio (uno por pieza, escritos en el
  COMMIT-2 de cada pieza junto a su sello).
· Escribe `canon/reglas-contrastadas-v1_1.tsv` = v1.0 (no se edita) con las filas de regla que un
  fragmento dictamina: `dictamen`, `resultado_id`, `calc`, `punto`, `ic95_*`, `unidad`,
  `detalle_dictamen` (prefijo «PDR1:»). Toda otra fila queda byte a byte como en v1.0.
· Exige que cada `resultado_id` citado exista en el spec.yaml del `calc` citado y que el CALC tenga
  `sello.json` (o, si el CALC es de otro acto, que esté sellado en el árbol).
· Imprime los conteos de P4 y escribe `conteos-v1_0.json`.
Uso: python3 ensambla.py [--escribe]
"""
from __future__ import annotations

import csv
import glob
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).parent
V10, V11 = ROOT / "canon/reglas-contrastadas-v1_0.tsv", ROOT / "canon/reglas-contrastadas-v1_1.tsv"
DICT_REGLA = {"CONFIRMA", "MATIZA", "ROMPE", "INCOMPARABLE", "NO-CONSTRUIBLE"}
DICT_AFIRM = {"CONFIRMA", "MATIZA", "ROMPE", "PISO-DESCRIPTIVO", "NO-CONSTRUIBLE"}


def lee(p):
    with open(p, newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def ids_de_calc(calc: str) -> tuple[set[str], bool]:
    d = ROOT / "data/corrida0" / calc
    y = yaml.safe_load(open(d / "spec.yaml", encoding="utf-8")) if (d / "spec.yaml").exists() else {}
    return {r["id"] for r in (y or {}).get("resultados") or []}, (d / "sello.json").exists()


def main(escribe: bool) -> int:
    frag = []
    for f in sorted(glob.glob(str(AQUI / "*-dictamenes.tsv"))):
        for r in lee(f):
            r["_frag"] = Path(f).name
            frag.append(r)
    errores = []
    for r in frag:
        valido = DICT_REGLA if r["clase"] == "regla" else DICT_AFIRM
        if r["dictamen"] not in valido:
            errores.append(f"{r['id']}: dictamen fuera de vocabulario {r['dictamen']!r}")
        if r["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE", "PISO-DESCRIPTIVO"}:
            for rid, calc in zip(r["resultado_id"].split(";"), r["calc"].split(";") * 99):
                ids, sellado = ids_de_calc(calc.strip())
                if rid.strip() not in ids:
                    errores.append(f"{r['id']}: {rid} no está en {calc}/spec.yaml")
                if not sellado:
                    errores.append(f"{r['id']}: {calc} sin sello.json")
    reglas_frag = {r["id"]: r for r in frag if r["clase"] == "regla"}
    with open(V10, newline="", encoding="utf-8") as s:
        texto = s.read()
    v10 = lee(V10)
    campos = list(v10[0])
    salida, cambios = [], 0
    for r in v10:
        f = reglas_frag.get(r["regla_id"])
        if f and f["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE"}:
            r = dict(r)
            r.update(dictamen=f["dictamen"], resultado_id=f["resultado_id"], calc=f["calc"],
                     punto=f["punto"], ic95_inf=f["ic95_inf"], ic95_sup=f["ic95_sup"],
                     unidad=f["unidad"], detalle_dictamen="PDR1: " + f["detalle"])
            cambios += 1
        elif f:
            r = dict(r)
            r["detalle_dictamen"] = f"PDR1 {f['dictamen']}: {f['detalle']} · v1.0: {r['detalle_dictamen']}"
        salida.append(r)
    faltan = set(reglas_frag) - {r["regla_id"] for r in v10}
    errores += [f"{i}: regla no está en v1.0" for i in sorted(faltan)]
    antes = Counter(r["dictamen"] for r in v10)
    despues = Counter(r["dictamen"] for r in salida)
    afirm = [r for r in frag if r["clase"] == "afirmacion"]
    dom_con_piso = sorted({r["dominio"] for r in afirm if r["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE", "PISO-DESCRIPTIVO"}})
    conteos = {
        "fragmentos": sorted({r["_frag"] for r in frag}),
        "sin_cifra_v1_0": antes["SIN-CIFRA-GEN2"], "sin_cifra_v1_1": despues["SIN-CIFRA-GEN2"],
        "reglas_a_dictamen": cambios,
        "dictamen_reglas": dict(Counter(r["dictamen"] for r in reglas_frag.values())),
        "dictamen_afirmaciones": dict(Counter(r["dictamen"] for r in afirm)),
        "dominios_con_piso_propuesto": dom_con_piso, "n_dominios_con_piso_propuesto": len(dom_con_piso),
        "no_construible": sorted(r["id"] for r in frag if r["dictamen"] == "NO-CONSTRUIBLE"),
        "errores": errores,
    }
    print(json.dumps(conteos, ensure_ascii=False, indent=1))
    if escribe and not errores:
        # Escritura por línea física (la cabecera de v1.0 repite `tier_declarado`: DictWriter la
        # colapsaría). Cada fila es una línea de 32 campos; sólo se reescriben las celdas cambiadas.
        lineas = texto.split("\n")
        cab = lineas[0].split("\t")
        col = {c: cab.index(c) for c in ("regla_id", "dictamen", "resultado_id", "calc", "punto",
                                          "ic95_inf", "ic95_sup", "unidad", "detalle_dictamen")}
        por_id = {r["regla_id"]: r for r in salida}
        out = [lineas[0]]
        for ln in lineas[1:]:
            if not ln:
                out.append(ln)
                continue
            c = ln.split("\t")
            if c[col["regla_id"]] not in reglas_frag:
                out.append(ln)
                continue
            r = por_id[c[col["regla_id"]]]
            for k in col:
                c[col[k]] = r[k].replace("\t", " ").replace("\n", " ")
            out.append("\t".join(c))
        V11.write_text("\n".join(out), encoding="utf-8")
        (AQUI / "conteos-v1_0.json").write_text(json.dumps(conteos, ensure_ascii=False, indent=1) + "\n")
        print("escrito", V11.relative_to(ROOT))
    _ = texto
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main("--escribe" in sys.argv))
