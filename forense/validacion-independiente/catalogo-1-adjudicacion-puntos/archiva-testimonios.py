#!/usr/bin/env python3
"""Archiva salidas auxiliares redundantes preservando bytes y rutas originales.
No toca testimonios de lote1, raw, códigos o planes congelados.
"""
from pathlib import Path
import tarfile,io,json,hashlib
R=Path(__file__).resolve().parent
NAMES=["p2/contrastes-raw2011.tsv","p2/contrastes-raw2011-v2.tsv","p2/contrastes-raw2021-v3.tsv","p2/denuncia-factorial2011.tsv"]
archive=R/"c1-puntos-testimonios-auxiliares.tar"
manifest=R/"c1-puntos-testimonios-auxiliares.json"
if archive.exists():
    old=json.loads(manifest.read_text())
    with tarfile.open(archive) as t:
        for x in old["archivos"]:
            assert hashlib.sha256(t.extractfile(x["ruta_original"]).read()).hexdigest()==x["sha256"]
    # Un replay puede haber materializado nuevamente el mismo testimonio.
    for x in old["archivos"]:
        p=R/x["ruta_original"]
        if p.exists():
            assert hashlib.sha256(p.read_bytes()).hexdigest()==x["sha256"]
            p.unlink()
    print("ARCHIVO-COINCIDE; testimonios exactos preservados")
else:
    data={name:(R/name).read_bytes() for name in NAMES}
    with tarfile.open(archive,"w",format=tarfile.USTAR_FORMAT) as t:
        for name,body in sorted(data.items()):
            entry=tarfile.TarInfo(name);entry.size=len(body);entry.mode=0o644;entry.mtime=0;t.addfile(entry,io.BytesIO(body))
    with tarfile.open(archive) as t:
        assert all(t.extractfile(name).read()==body for name,body in data.items())
    manifest.write_text(json.dumps({"motivo":"Salidas auxiliares anteriores idénticas conservadas por ruta original dentro del tar; no se cambian bytes para cumplir T02", "raw":False,"archivos":[{"ruta_original":name,"sha256":hashlib.sha256(body).hexdigest(),"bytes":len(body)} for name,body in sorted(data.items())],"sha256_archive":hashlib.sha256(archive.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+"\n")
    for name in data:(R/name).unlink()
    print("ARCHIVADO; cada byte recuperable con hash")
