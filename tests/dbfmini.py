#!/usr/bin/env python3
"""Lector minimo de DBF (dBase III/IV), Python puro -- sin dbfread/pandas
en este entorno. Solo lee: encabezado, descriptores de campo tipo C/N/F,
y registros como texto de ancho fijo (decodificado latin-1, con strip).

Suficiente para leer las tablas ENCUCI_2020_*.dbf (sesion CAL-CONF Fase B,
segunda ola, 03/ago/2026) -- no pretende ser un lector DBF completo.
"""
import struct


def read_dbf(path, wanted_fields=None):
    """Generador de dicts {campo: valor_str} para cada registro activo.

    wanted_fields: si se da, solo se decodifican esos campos (mas rapido).
    """
    with open(path, "rb") as f:
        header = f.read(32)
        num_records = struct.unpack("<I", header[4:8])[0]
        header_size = struct.unpack("<H", header[8:10])[0]
        record_size = struct.unpack("<H", header[10:12])[0]

        fields = []
        while True:
            desc = f.read(32)
            if desc[0:1] == b"\x0d":
                break
            name = desc[0:11].split(b"\x00")[0].decode("latin-1")
            ftype = desc[11:12].decode("latin-1")
            flen = desc[16]
            fields.append((name, ftype, flen))

        if wanted_fields is not None:
            wanted_set = set(wanted_fields)
        else:
            wanted_set = None

        f.seek(header_size)
        for _ in range(num_records):
            rec = f.read(record_size)
            if len(rec) < record_size:
                break
            if rec[0:1] == b"\x2a":
                continue  # registro borrado
            out = {}
            pos = 1
            for name, ftype, flen in fields:
                raw = rec[pos:pos + flen]
                pos += flen
                if wanted_set is not None and name not in wanted_set:
                    continue
                out[name] = raw.decode("latin-1").strip()
            yield out


def field_names(path):
    with open(path, "rb") as f:
        header = f.read(32)
        header_size = struct.unpack("<H", header[8:10])[0]
        fields = []
        while True:
            desc = f.read(32)
            if desc[0:1] == b"\x0d":
                break
            name = desc[0:11].split(b"\x00")[0].decode("latin-1")
            ftype = desc[11:12].decode("latin-1")
            flen = desc[16]
            fields.append((name, ftype, flen))
        return fields
