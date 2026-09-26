"""Auditoría estática acotada del lector y prohibición de valores no finitos."""
import ast
import math

IMPORTS = {"csv", "io", "json", "math", "hashlib", "zipfile", "collections", "numpy"}
COLS = {"LLAVEMOD", "FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V"} | {f"P5_6_{j}" for j in range(1,10)} | {f"P5_1_{j}" for j in range(1,7)}


def audita(codigo):
    fallos = []
    for n in ast.walk(ast.parse(codigo)):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            mods = [x.name.split(".")[0] for x in n.names] if isinstance(n, ast.Import) else [n.module.split(".")[0]]
            if set(mods)-IMPORTS:
                fallos.append("importación ajena")
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "r" and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
            # r es fila dentro de estima; r también resultado fuera: éste tiene su whitelist.
            if n.slice.value not in COLS | {"p", "replicas", "soporte", "familias"}:
                fallos.append("columna fuera del perímetro: "+n.slice.value)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {"eval", "exec", "open", "__import__"}:
            fallos.append("lectura o ejecución dinámica ajena")
    return fallos


def finitos(obj):
    if isinstance(obj, float):
        return math.isfinite(obj)
    if isinstance(obj, dict):
        return all(finitos(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(finitos(v) for v in obj)
    return True
