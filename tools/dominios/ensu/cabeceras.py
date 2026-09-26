"""Inventario de cabeceras ENSU por trimestre (sólo nombres de columna del
cuestionario de la persona seleccionada, CB; nunca valores). ACTO
GEN2-SEGURIDAD-ENSU-SERIE-1, P1. Excluye el año reservado (2026)."""
from __future__ import annotations
import io, re, struct, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "data/raw"
PAYLOADS = {
    2013: "corpus-completo/inegi/ensu/2013/ensu_bd_2013_dbf.zip",
    2014: "corpus-completo/inegi/ensu/2014/ensu_bd_2014_dbf.zip",
    2015: "corpus-completo/inegi/ensu/2015/ensu_bd_2015_dbf.zip",
    2016: "corpus-completo/inegi/ensu/2016/ensu_bd_2016_dbf.zip",
    2017: "corpus-completo/inegi/ensu/2017/ensu_bd_2017_dbf.zip",
    2018: "corpus-completo/inegi/ensu/2018/ensu_bd_2018_dbf.zip",
    2019: "corpus-completo/inegi/ensu/2019/ensu_bd_2019_dbf.zip",
    2020: "corpus-completo/inegi/ensu/2020/ensu_bd_2020_dbf.zip",
    2021: "corpus-completo/inegi/ensu/2021/ensu_bd_2021_csv.zip",
    2022: "corpus-completo/inegi/ensu/2022/ensu_bd_2022_csv.zip",
    2023: "corpus-completo/inegi/ensu/2023/ensu_bd_2023_csv.zip",
    2024: "ENSU/2024/ensu_bd_2024_csv.zip",
    2025: "ensu2025/ensu_bd_2025_csv.zip",
}
MES = {"mar": 1, "jun": 2, "sep": 3, "dic": 4, "03": 1, "06": 2, "09": 3, "12": 4}


def miembros(zbytes, ruta=""):
    """Recorre zips anidados; produce (ruta, bytes) de cada DBF/CSV."""
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for i in z.infolist():
        if i.is_dir():
            continue
        n = i.filename.lower()
        b = z.read(i)
        if n.endswith(".zip"):
            yield from miembros(b, ruta + i.filename + "!")
        elif n.endswith((".dbf", ".csv")):
            yield ruta + i.filename, b


def trimestre(ruta):
    n = ruta.lower()
    for k, t in (("marzo", 1), ("junio", 2), ("septiembre", 3), ("diciembre", 4),
                 ("_mar", 1), ("_jun", 2), ("_sep", 3), ("_dic", 4)):
        if k in n:
            return t
    m = re.search(r"_(03|06|09|12)(\d\d)\.(dbf|csv)$", n)
    return MES[m.group(1)] if m else None


def columnas(nombre, b):
    if nombre.lower().endswith(".dbf"):
        hl = struct.unpack("<H", b[8:10])[0]
        cols, p = [], 32
        while p < hl - 1 and b[p] != 0x0D:
            cols.append(b[p:p + 11].split(b"\0")[0].decode("latin-1").strip())
            p += 32
        return cols
    primera = b.split(b"\n", 1)[0].decode("utf-8-sig", "replace").strip("\r")
    return [c.strip().strip('"') for c in primera.split(",")]


def es_cb(ruta):
    n = ruta.lower().rsplit("/", 1)[-1]
    return "_cb_" in n or n.startswith("ensu_cb") or "cb_" in n


def inventario():
    out = {}
    for anio, rel in PAYLOADS.items():
        for ruta, b in miembros((RAW / rel).read_bytes()):
            if not es_cb(ruta):
                continue
            t = trimestre(ruta)
            out[(anio, t, ruta)] = columnas(ruta, b)
    return out


if __name__ == "__main__":
    for (a, t, r), c in sorted(inventario().items(), key=lambda x: (x[0][0], x[0][1] or 0)):
        print(f"{a}T{t}\t{r}\t{len(c)}\t{' '.join(c)}")
