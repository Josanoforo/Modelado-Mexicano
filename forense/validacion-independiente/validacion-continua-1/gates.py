"""Gates C1 por paquete para el universo de validación ciega continua (ACTO GEN2-VALIDACION-Y-2027-1, P1/P2).

Deriva, sin abrir microdato ni resultados sellados:
  - universo P1: RESULT de catalogo-del-mexicano-v1_3.tsv cuya llave no está en v1_2;
  - por CALC: spec humana (ruta y sha contra spec.yaml), firma de ACCESO-AUTORIZADO C1 en
    forense/firmas-pendientes.tsv, y fila en data/corrida0/validaciones-independientes.tsv;
  - `--verifica`: ids sin fila ciega en el libro y sin razón en gates-v1_3.tsv (criterio «hecho»: 0).

Uso: python3 forense/validacion-independiente/validacion-continua-1/gates.py [--escribe] [--verifica]
"""
import csv, hashlib, os, sys, yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "gates-v1_3.tsv")
CAB = ["paquete", "instrumento", "calc", "n_result", "spec_humana", "spec_humana_sha", "apto_tecnicamente",
       "contexto_nuevo_acreditado", "contrato_firmado", "acceso_autorizado", "estado", "razon", "firma_que_lo_abre"]
CONTEXTO = "SI-POR-RECETA: R32 opción A (FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02); se acredita por transcript al lanzar"
CONTRATO = "SI: CONTRATO-v3.md sha256 821a5ecb…94eb (R31, FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01)"


def _tsv(ruta):
    return list(csv.DictReader(open(ruta, encoding="utf-8"), delimiter="\t"))


def universo():
    v2 = {r["llave"] for r in _tsv("canon/catalogo-del-mexicano-v1_2.tsv")}
    return [r for r in _tsv("canon/catalogo-del-mexicano-v1_3.tsv") if r["llave"] not in v2]


def acceso_c1(instrumento):
    """Filas FIRMADA que conceden acceso C1 y nombran el instrumento (0 = gate en NO)."""
    hits = []
    for r in _tsv("forense/firmas-pendientes.tsv"):
        q = r["qué_se_firma"]
        if r["estado"].startswith("FIRMADA") and "Acceso C1" in q and instrumento in q:
            hits.append(r["id"])
    return hits


def filas():
    nuevas = universo()
    por_calc = {}
    for r in nuevas:
        por_calc.setdefault((r["instrumento"], r["calc"]), []).append(r["result_id"])
    out = []
    for (ins, calc), ids in sorted(por_calc.items()):
        d = f"data/corrida0/{calc}"
        y = yaml.safe_load(open(f"{d}/spec.yaml", encoding="utf-8"))
        sm = os.path.normpath(os.path.join(d, y["spec_md"]))
        casa = os.path.exists(sm) and hashlib.sha256(open(sm, "rb").read()).hexdigest() == y["spec_md_sha256"]
        acc = acceso_c1(ins)
        estado = "LANZABLE" if acc and casa else "NO-LANZADO (gate ACCESO)"
        out.append({
            "paquete": calc.replace("CALC-", "").lower(), "instrumento": ins, "calc": calc, "n_result": str(len(ids)),
            "spec_humana": sm, "spec_humana_sha": y["spec_md_sha256"],
            "apto_tecnicamente": ("PARCIAL: spec humana CASA; contenedor y allowlist por construir tras el acceso"
                                  if casa else "NO: spec humana no casa"),
            "contexto_nuevo_acreditado": CONTEXTO, "contrato_firmado": CONTRATO,
            "acceso_autorizado": ("SI: " + ",".join(acc)) if acc else
                                 "NO: 0 filas FIRMADA con «Acceso C1» que nombren " + ins + " en forense/firmas-pendientes.tsv",
            "estado": estado,
            "razon": "SIN-VALIDACION-CIEGA: gate ACCESO-AUTORIZADO sin firma; nada se abrió ni se comparó",
            "firma_que_lo_abre": f"«Autorizo el acceso C1 del paquete {calc} ({ins}): lectura por la reconstructora "
                                 f"sin historial de los inputs DATO de su spec.yaml, solo las columnas que nombre su spec "
                                 f"humana, con los cuatro gates y la receta de LANZAMIENTO-LOTE3. No adopta cifras.»",
        })
    return out


def verifica():
    libro = {r["resultado_id"] for r in _tsv("data/corrida0/validaciones-independientes.tsv")}
    razon = {r["calc"] for r in _tsv(SALIDA) if r["razon"]}
    faltan = [r["result_id"] for r in universo() if r["result_id"] not in libro and r["calc"] not in razon]
    print(f"universo={len(universo())} con_fila_ciega={sum(r['result_id'] in libro for r in universo())} "
          f"ids_sin_fila_ni_razon={len(faltan)}")
    return 1 if faltan else 0


if __name__ == "__main__":
    if "--escribe" in sys.argv:
        F = filas()
        with open(SALIDA, "w", encoding="utf-8", newline="") as f:
            f.write("\t".join(CAB) + "\n")
            for r in F:
                f.write("\t".join(r[k].replace("\t", " ") for k in CAB) + "\n")
        print(f"ESCRITO {SALIDA} filas={len(F)}")
    if "--verifica" in sys.argv:
        sys.exit(verifica())
    if len(sys.argv) == 1:
        for r in filas():
            print(r["calc"], r["n_result"], r["estado"])
