"""Circuito portable solo sintético; nunca acredita una sesión ciega."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import adaptador
import aislamiento

FIXTURES = Path(__file__).parent / "fixtures"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"tipo": "SINTETICO-PORTABLE-NO-CIEGO", "pasos": []}
    probe = aislamiento.probe_environment()
    report["entorno"] = probe
    report["sesion_nueva"] = {
        "estado": "NO-CORRIDO",
        "razon": "TUI create_thread hereda cwd; no acredita control FS/red. No se inicia sin lanzador aislado acreditado.",
    }
    with tempfile.TemporaryDirectory(prefix="astra6-sintetico-") as tmp:
        root = Path(tmp) / "entrada"
        allow = [{"path": name, "sha256": sha(FIXTURES / name)}
                 for name in ("entrada.csv", "reconstructor.py", "tolerancia.json")]
        manifest = aislamiento.materialize(FIXTURES, root, allow)
        report["pasos"].append({"paso": "materializar", "estado": "EJECUTADO", "manifest": manifest})
        original = output / "original.json"
        subprocess.run([sys.executable, str(root / "reconstructor.py"),
                        str(root / "entrada.csv"), str(original)], check=True,
                       env={"PATH": "/usr/bin:/bin"}, cwd=root)
        report["pasos"].append({"paso": "reconstruir", "estado": "EJECUTADO-PORTABLE-NO-CIEGO"})
        artifact = output / "congelado"
        seal = adaptador.freeze(artifact, original, [root / "reconstructor.py"],
                               root / "entrada.csv", root / "tolerancia.json")
        seal_hash = sha(seal)
        report["manifest_sha256"] = seal_hash
        report["pasos"].append({"paso": "congelar", "estado": "EJECUTADO", "sha256": seal_hash})
        adaptador.verify_freeze(artifact, seal_hash)
        report["pasos"].append({"paso": "verificar", "estado": "EJECUTADO"})
        # La referencia se produce/desvela después de congelar y verificar.
        reference = output / "referencia.json"
        reference.write_bytes((FIXTURES / "referencia.json").read_bytes())
        report["pasos"].append({"paso": "revelar", "estado": "EJECUTADO", "sha256": sha(reference)})
        report["comparacion"] = adaptador.compare(artifact, seal_hash, reference, sha(reference))
        if report["comparacion"]["resultados"][0]["estado"] != "COINCIDE":
            raise AssertionError("Referencia independiente no coincide")
        altered = json.loads(reference.read_text())
        altered["filas"][0]["punto"] = "0.76"
        alternate = output / "referencia-discrepante.json"
        alternate.write_text(json.dumps(altered, indent=2) + "\n")
        report["comparacion_discrepante"] = adaptador.compare(artifact, seal_hash, alternate, sha(alternate))
        if report["comparacion_discrepante"]["resultados"][0]["estado"] != "DISCREPA":
            raise AssertionError("Diferencia material no detectada")
        altered["filas"][0]["unidad"] = "porcentaje"
        alternate_units = output / "referencia-unidad-incompatible.json"
        alternate_units.write_text(json.dumps(altered, indent=2) + "\n")
        try:
            adaptador.compare(artifact, seal_hash, alternate_units, sha(alternate_units))
        except ValueError as exc:
            report["unidades_incompatibles"] = {"estado": "RECHAZADO", "error": str(exc)}
        else:
            raise AssertionError("Unidad incompatible aceptada")
        report["pasos"].append({"paso": "comparar", "estado": "EJECUTADO"})
        # Alteración material de números después del sello, sobre copia local propia.
        candidates = [p for p in artifact.rglob("*") if p.is_file() and p.name != Path(seal).name]
        target = next(p for p in candidates if "original" in p.name)
        saved = target.read_bytes()
        target.write_bytes(saved + b" ")
        try:
            adaptador.verify_freeze(artifact, seal_hash)
        except (ValueError, RuntimeError) as exc:
            report["tamper"] = {"estado": "RECHAZADO", "error": str(exc)}
        else:
            raise AssertionError("Artefacto alterado aceptado")
        finally:
            target.write_bytes(saved)
        report["pasos"].append({"paso": "tamper", "estado": report["tamper"]["estado"]})
    (output / "evidencia-sintetica.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(json.dumps({"tipo": result["tipo"], "pasos": result["pasos"], "tamper": result["tamper"]}))
