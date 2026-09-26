"""Verifica el lote ENCIG, sin escribir ni abrir ninguna ola futura."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
AREA = ROOT / "forense/analisis/familias-2027/astra6-encig"
CALCS = ("CALC-ENCIG-AUX-FAMILIAS-2027-0001",
         "CALC-FAMILIA-2027-ENCIG-PAGO-DIGITAL-0001",
         "CALC-FAMILIA-2027-ENCIG-SOLICITUD-MORDIDA-0001")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verifica():
    checks = []
    def check(name, passed):
        checks.append((name, bool(passed)))
    frozen = json.loads((AREA / "commit-1-hashes.json").read_text())
    enmienda = json.loads((AREA / "enmienda-verificacion.json").read_text())
    for p, item in enmienda["archivos"].items():
        if p not in ("tools/familias-2027/encig/cierre.py", "tools/familias-2027/encig/evaluar.py"):
            raise ValueError("ENMIENDA-FUERA-DE-CABLEADO")
        if frozen["archivos"][p] != item["anterior"]:
            raise ValueError("ENMIENDA-ORIGEN-DISCREPA")
        original = subprocess.check_output(["git", "show", enmienda["commit_1"] + ":" + p], cwd=ROOT)
        if hashlib.sha256(original).hexdigest() != item["anterior"]:
            raise ValueError("ENMIENDA-TESTIGO-DISCREPA")
        frozen["archivos"][p] = item["actual"]
    check("codigo-specs-congelados", all((ROOT / p).is_file() and sha(ROOT / p) == h
                                         for p, h in frozen["archivos"].items()))
    # No confiar en que un sello modificado coincida consigo mismo: hashes
    # de ejecución del COMMIT-2 se cotejan también con inventario aditivo.
    inv = json.loads((AREA / "inventario-sellos.json").read_text())
    check("inventario-sellos", all(sha(ROOT / p) == h for p, h in inv["archivos"].items()))
    check("orden-COMMIT-1-2", subprocess.run(["git", "merge-base", "--is-ancestor",
                                            inv["commit_1"], "HEAD"], cwd=ROOT).returncode == 0)
    for calc in CALCS:
        for command in ("preflight", "verify"):
            proc = subprocess.run([sys.executable, str(ROOT / "tools/corrida0.py"), command, calc],
                                  cwd=ROOT, text=True, capture_output=True)
            # preflight impide volver a ejecutar un CALC sellado. Ese único
            # bloqueo acredita inmutabilidad; verify contesta reproducción.
            immutable = (command == "preflight" and proc.stdout.strip().splitlines()[-1]
                         == "PRE-FLIGHT: BLOQUEADO calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO")
            check(command + ":" + calc, proc.returncode == 0 or immutable)
            if proc.returncode and not immutable:
                print(proc.stdout[-3000:] + proc.stderr[-1000:])
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/test_astra6_encig.py"],
                          cwd=ROOT, text=True, capture_output=True)
    print(proc.stdout[-1800:])
    check("guardias-fronteras-mutacion-conducto", proc.returncode == 0)
    pisos = json.loads((AREA / "pisos.json").read_text())
    raw = ROOT / "data/corrida0/CALC-ENCIG-0001/resultados.json"
    check("piso-historico-sellado", all(f["source_sha256"] == sha(raw)
          and f["sello_sha256"] == sha(raw.with_name("sello.json")) for f in pisos["familias"].values()))
    gold = json.loads((ROOT / "data/corrida0" / CALCS[0] / "tablas/replicas.json").read_text())
    historico = json.loads(raw.read_text())["resultados"]
    for name, floor in pisos["familias"].items():
        f = gold["familias"][name]
        check("oro-punto:" + name, f["p"] is not None and abs(f["p"] - historico[floor["result_id"]]) <= 1e-12)
        check("oro-vector:" + name, len(f["replicas"]) == 2000)
        calc = "CALC-FAMILIA-2027-ENCIG-" + name + "-0001"
        rs = json.loads((ROOT / "data/corrida0" / calc / "resultados.json").read_text())["resultados"]
        rid = "RESULT-FAMILIA-2027-ENCIG-" + name + "-P0"
        check("emision-sin-R-futura:" + name, set(rs) == {rid, rid + "-FUENTE", rid + "-ESTADO"}
              and rs[rid] == floor["p0"] and rs[rid + "-FUENTE"] == floor["result_id"])
    potencia = json.loads((AREA / "potencia.json").read_text())
    check("potencia-escenarios-MDE", len(potencia["escenarios"]) == 81 and len(potencia["mde"]) == 36)
    calendario = (AREA / "calendario.md").read_text()
    check("calendario-estado-y-fuente", "https://www.snieg.mx/" in calendario and "NO-CONFIRMADA" in calendario)
    check("atestacion-dependencia-declarada", inv["estado"] == "SELLADO-INTERNAMENTE"
          and inv["atestacion_externa_verificada"] == 0 and inv["dependencia"])
    for name, passed in checks:
        print(("OK " if passed else "FAIL ") + name)
    status = "VERDE" if all(p for _, p in checks) else "INCOMPLETO"
    print(json.dumps({"estado": status, "familias_emisiones_congeladas": 2, "olas_futuras": 1,
                      "atestacion_externa_verificada": 0, "calendario": "VENTANA-ESPERADA-2028-Q2",
                      "recibo_claude": "PENDIENTE"}, ensure_ascii=False))
    return 0 if status == "VERDE" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifica", action="store_true", required=True)
    parser.parse_args()
    raise SystemExit(verifica())
