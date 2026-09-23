"""Header-only gate for preregistered ASTRA Seguro Popular endpoint.

Never reads outcome rows. A missing preregistered field is material,
not an invitation to pick a replacement variable after seeing the data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "ALL.tab": "79697720d54aa497156d49ad8f7ff86e10dc466abcbb4fc6866dfe41c3755788",
    "clustmatchlist.tab": "b995d5f4ef15722e2bb66f112a94c9ea44e9752ef79b97de84e28334745bcd9e",
}
REQUIRED = (
    "cluster", "id_pers", "age", "P01D1401", "P01D1601",
    "P11D0401", "P11D0501", "P10E0401_T2", "P10E0501_T2",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return next(csv.reader(stream, delimiter="\t"))


def missing_fields(columns: list[str]) -> list[str]:
    return [name for name in REQUIRED if name not in columns]


def diagnose(root: Path) -> dict:
    paths = {name: root / name for name in EXPECTED}
    hashes = {name: sha256(path) for name, path in paths.items()}
    all_columns = header(paths["ALL.tab"])
    pair_columns = header(paths["clustmatchlist.tab"])
    missing = missing_fields(all_columns)
    return {
        "calc_id": "CALC-ASTRA-THETA-SALUD-OFERTA-0001",
        "preregistro_commit": "c529cdf0",
        "adquisicion_commit": "37cfd059",
        "modo": "solo encabezado y hashes; cero filas de desenlace leidas",
        "hashes_validos": all(hashes[name] == expected for name, expected in EXPECTED.items()),
        "hashes_observados": hashes,
        "columnas_all": len(all_columns),
        "columnas_pares": len(pair_columns),
        "faltan_variables_preregistradas": missing,
        "estado": "NO-ESTIMABLE" if missing or any(hashes[n] != EXPECTED[n] for n in EXPECTED) else "LISTO-PARA-MEDIDOR",
        "causa": "La tabla de réplica omite reactivos de motivo y lugar de consulta requeridos por el desenlace; P10D04/P10D05 son otras preguntas del basal según codebook." if missing else "Ninguna guardia estructural falló.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        synthetic = list(REQUIRED)
        assert missing_fields(synthetic) == []
        synthetic.remove("P10E0501_T2")
        assert missing_fields(synthetic) == ["P10E0501_T2"]
    result = diagnose(args.root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
