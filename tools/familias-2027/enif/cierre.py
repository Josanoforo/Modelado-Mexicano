"""Verificación propia del lote y vistas locales desde RESULT sellados."""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml
from auditoria import audita, finitos

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "data/corrida0"
ANALISIS = ROOT / "forense/analisis/familias-2027/astra6-enif"
ORO = ("CALC-FAMILIA-2027-ENIF-ORO-0002" if
       (BASE/"CALC-FAMILIA-2027-ENIF-ORO-0002/sello.json").is_file()
       else "CALC-FAMILIA-2027-ENIF-ORO-0001")
FAMILIAS = ("AHORRO-FORMAL", "HORIZONTE-AHORRO")
CALCS = [ORO] + ["CALC-FAMILIA-2027-ENIF-"+f+"-EMISIONES-0001" for f in FAMILIAS]


def resultados(cid):
    o = json.loads((BASE/cid/"resultados.json").read_text())
    return o.get("resultados", o)


def tabla_json(cid, valor):
    if not valor.startswith("REF:"):
        return json.loads(valor)
    rel, _, sha = valor[4:].partition("#sha256:")
    esperado = BASE/cid/"tablas"
    p = ROOT/rel
    if p.is_symlink() or p.resolve().parent != esperado.resolve():
        raise ValueError("REF fuera de tablas propias")
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError("REF hash discordante")
    return json.loads(raw)


def deriva():
    oro = resultados(ORO)
    potencia = tabla_json(ORO, oro["RESULT-FAMILIA-ENIF-ORO-POTENCIA"])
    with (ANALISIS/"potencia.tsv").open("w") as f:
        cols = ["familia", "escala_se", "sd_deriva", "delta", "compatible", "indeterminado", "desvio", "ambas_informativas"]
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t"); w.writeheader()
        for s in potencia["escenarios"]:
            for j, familia in enumerate(FAMILIAS):
                p = s["familias"][j]
                w.writerow(dict(familia=familia, escala_se=s["escala_se"], sd_deriva=s["sd_deriva"], delta=s["delta"], compatible=p["COMPATIBLE-CON-TOLERANCIA"], indeterminado=p["INDETERMINADO"], desvio=p["DESVÍO-MATERIAL"], ambas_informativas=s["ambas_informativas"]))
    detalle = {"mde80": dict(zip(FAMILIAS, potencia["mde80"])), "correlacion_muestral": potencia["correlacion_muestral"], "supuesto": potencia["supuesto"], "auditoria": json.loads(oro["RESULT-FAMILIA-ENIF-ORO-AUDITORIA"]), "estimandos": 2, "olas_futuras": 1, "retadores": 0, "R_futura": None}
    (ANALISIS/"potencia-resumen.json").write_text(json.dumps(detalle, indent=2, ensure_ascii=False)+"\n")
    filas = []
    for fam, g in zip(FAMILIAS, ("FORMAL", "AMBAS")):
        emitted = resultados("CALC-FAMILIA-2027-ENIF-"+fam+"-EMISIONES-0001")
        p0 = emitted["RESULT-FAMILIA-ENIF-"+fam+"-PISO-P"]
        p = oro["RESULT-FAMILIA-ENIF-ORO-"+g+"-P"]
        filas.append({"familia": fam, "piso": p0, "oro": p, "delta": p-p0, "tolerancia": 1e-6, "coincide": abs(p-p0)<=1e-6, "alcance": "reproducción histórica del estimando; no acierto futuro"})
    (ANALISIS/"oro-comparacion.json").write_text(json.dumps(filas, indent=2, ensure_ascii=False)+"\n")


def verifica():
    fallos = []
    for cid in CALCS:
        d = BASE/cid
        s = yaml.safe_load((d/"spec.yaml").read_text())
        for p, expected in ((d/s["spec_md"], s["spec_md_sha256"]), (ROOT/s["script"], s["script_sha256_congelado"])):
            if hashlib.sha256(p.read_bytes()).hexdigest() != expected:
                fallos.append(f"hash discordante: {p}")
        cmd = [sys.executable, str(ROOT/"tools/corrida0.py"), "verify", cid]
        r = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        print(f"verify {cid}: exit={r.returncode}; " + r.stdout.strip().split("\n")[-1])
        if r.returncode or "CONTEXTO=IDENTICO · RESULTADO=REPRODUCE" not in r.stdout:
            fallos.append("no reproduce: "+cid+" "+r.stderr[-300:])
        try:
            o = resultados(cid)
            if not finitos(o):
                fallos.append("no finito en resultados: "+cid)
            for key in ("RESULT-FAMILIA-ENIF-ORO-REPLICAS", "RESULT-FAMILIA-ENIF-ORO-POTENCIA"):
                if key in o and not finitos(tabla_json(cid, o[key])):
                    fallos.append("no finito en JSON material: "+key)
        except OSError as e:
            fallos.append(str(e))
    for fam in FAMILIAS:
        p = ROOT/("forense/prereg-caja/FAMILIA-2027-ENIF-"+fam+"-spec-v1_3.md")
        side = Path(str(p)+".sha256")
        if not side.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != side.read_text().split()[0]:
            fallos.append("spec humana/hash discordante: "+fam)
    fallos += audita((ROOT/"tools/familias-2027/enif/lector.py").read_text())
    if ORO.endswith("0001") and (BASE/ORO/"medidor.py").read_bytes() != (ROOT/"tools/familias-2027/enif/lector.py").read_bytes():
        fallos.append("lector congelado difiere de medidor material")
    for name in ("contrato-futuro.yaml", "contrato-futuro-serializacion-v2.yaml"):
        contrato = yaml.safe_load((ROOT/"tools/familias-2027/enif"/name).read_text())
        material = ROOT/contrato["script_material"]
        if hashlib.sha256(material.read_bytes()).hexdigest() != contrato["script_sha256_congelado"]:
            fallos.append("hash futuro discordante: "+name)
        if contrato["calc_id"] is not None or contrato["R_futura"] is not None:
            fallos.append("contrato contiene ejecución futura: "+name)
    inventario = json.loads((ANALISIS/"inventario-sellos.json").read_text())
    for archivo in inventario["archivos"]:
        p = ROOT/archivo["archivo"]
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != archivo["sha256"]:
            fallos.append("inventario discordante: "+str(p))
    if inventario["atestaciones_externas_verificadas"] != 0 or inventario["comprobante_ots"] is not None:
        fallos.append("atestación no corresponde al estado acreditado del lote")
    tests = subprocess.run([sys.executable,"-m","pytest","-q",str(ROOT/"tools/familias-2027/enif/tests")], cwd=ROOT, text=True, capture_output=True)
    print(tests.stdout.strip().split("\n")[-1])
    if tests.returncode:
        fallos.append("guardias/fronteras fallan")
    try:
        oro = resultados(ORO)
        if oro["RESULT-FAMILIA-ENIF-ORO-SOPORTE"] != "SI":
            fallos.append("oro sin soporte")
        for fam, g in zip(FAMILIAS, ("FORMAL", "AMBAS")):
            emitted = resultados("CALC-FAMILIA-2027-ENIF-"+fam+"-EMISIONES-0001")
            if abs(emitted["RESULT-FAMILIA-ENIF-"+fam+"-PISO-P"]-oro["RESULT-FAMILIA-ENIF-ORO-"+g+"-P"]) > 1e-6:
                fallos.append("oro discrepante: "+fam)
        reps = tabla_json(ORO, oro["RESULT-FAMILIA-ENIF-ORO-REPLICAS"])
        if len(reps) != 2000 or any(len(x)!=4 for x in reps):
            fallos.append("réplicas conjuntas incompletas")
        potencia = tabla_json(ORO, oro["RESULT-FAMILIA-ENIF-ORO-POTENCIA"])
        if len(potencia["escenarios"]) != 54 or len(potencia["mde80"]) != 2:
            fallos.append("escenarios incompletos")
        for cid in CALCS[1:]:
            if len(resultados(cid)) != 1:
                fallos.append("emisión contiene algo distinto de piso único")
        for f in ("calendario.md", "hoja-firma.md", "potencia.tsv", "potencia-resumen.json", "oro-comparacion.json"):
            if not (ANALISIS/f).is_file():
                fallos.append("evidencia ausente: "+f)
    except (OSError, KeyError, ValueError) as e:
        fallos.append(str(e))
    for fallo in fallos:
        print("FAIL: "+fallo)
    print("CIERRE: " + ("VERDE; 2 familias, 1 ola futura, 0 R futura; atestación externa pendiente" if not fallos else "INCOMPLETO"))
    return bool(fallos)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--verifica", action="store_true"); p.add_argument("--deriva", action="store_true"); a = p.parse_args()
    if a.deriva:
        deriva()
    if a.verifica:
        raise SystemExit(verifica())
