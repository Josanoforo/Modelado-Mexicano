"""Lector DBF mínimo (dBase III) que solo extrae las columnas pedidas."""
import struct

import numpy as np


def leer_encabezado(ruta):
    with open(ruta, "rb") as f:
        cab = f.read(32)
        n_reg, long_cab, long_reg = struct.unpack("<IHH", cab[4:12])
        campos = []
        pos = 1  # byte 0 del registro es la marca de borrado
        while True:
            d = f.read(32)
            if d[0] == 0x0D:
                break
            nombre = d[:11].split(b"\x00")[0].decode("ascii")
            tipo = chr(d[11])
            largo, dec = d[16], d[17]
            campos.append({"nombre": nombre, "tipo": tipo, "largo": largo, "dec": dec, "pos": pos})
            pos += largo
    return {"n_registros": n_reg, "long_cabecera": long_cab, "long_registro": long_reg, "campos": campos}


def leer_columnas(ruta, columnas, codificacion="latin-1"):
    """Devuelve (dict columna -> lista de str crudas sin recortar, array bool de borrados)."""
    enc = leer_encabezado(ruta)
    por_nombre = {c["nombre"]: c for c in enc["campos"]}
    faltan = [c for c in columnas if c not in por_nombre]
    if faltan:
        raise KeyError(f"columnas ausentes en {ruta}: {faltan}")
    n, L = enc["n_registros"], enc["long_registro"]
    with open(ruta, "rb") as f:
        f.seek(enc["long_cabecera"])
        buf = f.read(n * L)
    if len(buf) != n * L:
        raise ValueError("archivo DBF truncado")
    mat = np.frombuffer(buf, dtype=np.uint8).reshape(n, L)
    borrados = mat[:, 0] == ord("*")
    salida = {}
    for c in columnas:
        d = por_nombre[c]
        bloque = mat[:, d["pos"]:d["pos"] + d["largo"]].tobytes()
        w = d["largo"]
        salida[c] = [bloque[i * w:(i + 1) * w].decode(codificacion) for i in range(n)]
    return salida, borrados
