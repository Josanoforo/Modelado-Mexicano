#!/usr/bin/env python3
"""Prepara un worktree para resolver un conjunto cerrado de payloads.

La configuracion fisica sigue viviendo en ``data/raices.local.yaml`` y la
resolucion de cada objeto sigue siendo la canonica de ``tests/manifiesto.py``.
Este comando solo hace dos operaciones mecanicas que un worktree nuevo no
hereda por ser archivos gitignorados:

* copia una configuracion local ya autorizada;
* monta ``data/raw`` como enlace a la raiz ``data_raw`` declarada en ella.

Si un objeto ``data_raw`` falta en la raiz compartida, ``--recupera-desde``
permite copiar exclusivamente los ``--id`` pedidos desde otra raiz fisica.
La copia valida tamano y SHA antes de publicarse, se publica atomicamente sin
sobreescribir un destino existente y conserva el origen.

Sin ``--aplica`` solo previsualiza. Nunca recorre una raiz completa.

Ejemplo::

    python3 tools/prepara_corpus.py \
      --config-desde ../Modelado-Mexicano/data/raices.local.yaml \
      --id ensafi2023_bd_csv_zip --id ennvih1_2002_hogar_dta

    # Repetir con --aplica despues de revisar la previsualizacion.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tests"))
import manifiesto as M  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def carga_config(path: Path) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("la configuracion de raices no es un mapa YAML")
    clean = {str(k): str(v) for k, v in data.items() if v}
    if M.RAIZ_INTEGRADA not in clean:
        raise ValueError("la configuracion no declara data_raw")
    for name, value in clean.items():
        if not Path(value).is_absolute():
            raise ValueError(f"la raiz {name} no es absoluta")
    return clean


def ruta_relativa(entry: dict) -> Path:
    raw = entry.get("archivo")
    if not raw:
        raise ValueError("entrada sin archivo")
    rel = Path(str(raw))
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("archivo fuera de la raiz declarada")
    return rel


def identidad(path: Path, entry: dict) -> str:
    if not path.is_file():
        return "AUSENTE"
    expected_size = entry.get("tamano_bytes")
    if path.stat().st_size != expected_size:
        return "NO_COINCIDE"
    return "COINCIDE" if sha256(path) == entry.get("sha256") else "NO_COINCIDE"


def publica_copia_atomica(source: Path, destination: Path, entry: dict) -> str:
    """Copia sin sustituir: link(temp,dest) hace la publicacion atomica."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".corpus-tmp-", dir=destination.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as out, source.open("rb") as inp:
            shutil.copyfileobj(inp, out, length=1 << 20)
            out.flush()
            os.fsync(out.fileno())
        os.chmod(tmp, stat.S_IMODE(source.stat().st_mode))
        if identidad(tmp, entry) != "COINCIDE":
            raise RuntimeError("la copia temporal no conserva la identidad esperada")
        try:
            os.link(tmp, destination)
        except FileExistsError:
            return "DESTINO_IDENTICO" if identidad(destination, entry) == "COINCIDE" else "CONFLICTO_DESTINO"
        return "COPIADO"
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def instala_archivo_sin_sustituir(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = source.read_bytes()
    if destination.exists():
        return "LISTO" if destination.read_bytes() == content else "CONFLICTO"
    fd, tmp_name = tempfile.mkstemp(prefix=".raices-tmp-", dir=destination.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        try:
            os.link(tmp, destination)
        except FileExistsError:
            return "LISTO" if destination.read_bytes() == content else "CONFLICTO"
        return "INSTALADO"
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def instala_enlace_sin_sustituir(target: Path, link: Path) -> str:
    if link.is_symlink():
        return "LISTO" if link.resolve() == target.resolve() else "CONFLICTO"
    if link.exists():
        return "CONFLICTO"
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        # symlink() crea la entrada de directorio en una sola operacion y
        # falla con EEXIST; nunca reemplaza lo que aparezca concurrentemente.
        os.symlink(target, link, target_is_directory=True)
        return "MONTADO"
    except FileExistsError:
        return "LISTO" if link.is_symlink() and link.resolve() == target.resolve() else "CONFLICTO"


def plan(ids: list[str], config: dict[str, str], entries: list[dict],
         recovery: Path | None, root: Path) -> list[dict[str, str]]:
    by_id = {entry.get("id"): entry for entry in entries}
    result: list[dict[str, str]] = []
    for payload_id in dict.fromkeys(ids):
        entry = by_id.get(payload_id)
        if not entry or "sha256" not in entry:
            result.append({"id": payload_id, "raiz": "-", "origen": "-", "destino": "-", "estado": "ID_SIN_REFERENCIA"})
            continue
        root_name = entry.get("raiz", M.RAIZ_INTEGRADA)
        try:
            relative = ruta_relativa(entry)
        except ValueError:
            result.append({"id": payload_id, "raiz": root_name, "origen": "-", "destino": str(entry.get("archivo", "-")), "estado": "RUTA_INVALIDA"})
            continue
        root_value = config.get(root_name)
        destination = Path(root_value) / relative if root_value else None
        logical_destination = root / "data" / "raw" / relative if root_name == M.RAIZ_INTEGRADA else destination
        source = destination
        if not M.raiz_escaneable(root_name):
            state = "FUERA_DE_PERIMETRO"
        elif not root_value:
            state = "RAIZ_NO_CONFIGURADA"
        else:
            assert destination is not None
            current = identidad(destination, entry)
            if current == "COINCIDE":
                state = "DESTINO_IDENTICO"
            elif current == "NO_COINCIDE":
                state = "CONFLICTO_DESTINO"
            elif recovery is None or root_name != M.RAIZ_INTEGRADA:
                state = "AUSENTE_SIN_ORIGEN"
            else:
                source = recovery / relative
                source_state = identidad(source, entry)
                state = "RECUPERARIA" if source_state == "COINCIDE" else f"ORIGEN_{source_state}"
        result.append({"id": payload_id, "raiz": root_name,
                       "origen": str(source) if source else "-",
                       "destino": str(logical_destination) if logical_destination else "-",
                       "estado": state})
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config-desde", required=True, type=Path,
                    help="data/raices.local.yaml autorizado de esta maquina")
    ap.add_argument("--id", action="append", required=True,
                    help="id exacto del manifiesto; repetible")
    ap.add_argument("--recupera-desde", type=Path,
                    help="raiz data_raw alternativa; solo se usa si el destino compartido falta")
    ap.add_argument("--aplica", action="store_true",
                    help="instala configuracion/montaje y recupera faltantes validados")
    ap.add_argument("--root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    root = args.root.resolve()
    source_config = args.config_desde.resolve()
    try:
        config = carga_config(source_config)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR_CONFIG\t{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    _header, entries = M.leer_manifiesto(str(root / "data" / "manifiesto.yaml"))
    rows = plan(args.id, config, entries,
                args.recupera_desde.resolve() if args.recupera_desde else None,
                root)

    config_dest = root / "data" / "raices.local.yaml"
    raw_link = root / "data" / "raw"
    config_state = ("LISTO" if config_dest.exists() and config_dest.read_bytes() == source_config.read_bytes()
                    else "CONFLICTO" if config_dest.exists() else "INSTALARIA")
    target = Path(config[M.RAIZ_INTEGRADA])
    mount_state = ("LISTO" if raw_link.is_symlink() and raw_link.resolve() == target.resolve()
                   else "CONFLICTO" if raw_link.exists() or raw_link.is_symlink() else "MONTARIA")

    errors = {"ID_SIN_REFERENCIA", "RUTA_INVALIDA", "FUERA_DE_PERIMETRO", "RAIZ_NO_CONFIGURADA",
              "CONFLICTO_DESTINO", "AUSENTE_SIN_ORIGEN", "ORIGEN_AUSENTE", "ORIGEN_NO_COINCIDE"}
    if config_state == "CONFLICTO" or mount_state == "CONFLICTO" or any(r["estado"] in errors for r in rows):
        applicable = False
    else:
        applicable = True

    if args.aplica and applicable:
        config_state = instala_archivo_sin_sustituir(source_config, config_dest)
        mount_state = instala_enlace_sin_sustituir(target, raw_link)
        if config_state == "CONFLICTO" or mount_state == "CONFLICTO":
            applicable = False
        if applicable and args.recupera_desde:
            by_id = {entry.get("id"): entry for entry in entries}
            for row in rows:
                if row["estado"] != "RECUPERARIA":
                    continue
                entry = by_id[row["id"]]
                relative = ruta_relativa(entry)
                row["estado"] = publica_copia_atomica(
                    args.recupera_desde.resolve() / relative,
                    target / relative,
                    entry,
                )
                if row["estado"] == "CONFLICTO_DESTINO":
                    applicable = False
        if applicable:
            # La comprobacion final usa el resolvedor canonico, no una segunda
            # interpretacion de raices.
            for row in rows:
                resolved = __import__("payload_resolver").resolver_payload(row["id"], root=str(root))
                row["estado"] = resolved["estado"]
                if row["estado"] != "COINCIDE":
                    applicable = False

    print(f"modo\t{'APLICA' if args.aplica else 'PREVISUALIZA'}")
    print(f"config\t{config_state}")
    print(f"montaje_data_raw\t{mount_state}")
    print("id\traiz_logica\torigen\tdestino\testado")
    for row in rows:
        print(f"{row['id']}\t{row['raiz']}\t{row['origen']}\t{row['destino']}\t{row['estado']}")
    print(f"resumen\tids={len(rows)}\taplicable={'SI' if applicable else 'NO'}")
    return 0 if applicable else 1


if __name__ == "__main__":
    raise SystemExit(main())
