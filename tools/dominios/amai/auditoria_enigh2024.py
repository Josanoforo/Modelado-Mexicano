"""Auditoría estática de `enigh2024.py` antes de abrir ENIGH 2024 (firma C7).

Lee el FUENTE (no ejecuta nada, no toca microdato) y verifica:
A1 imports: sólo la lista de abajo; ningún otro lector del repo.
A2 del medidor congelado sólo se usan `distribucion` y `validacion`.
A3 `read_csv` y `.open(` de zip aparecen sólo dentro de `lee_acotado`,
   y `read_csv` lleva `usecols`.
A4 `lee_acotado` sólo se llama con `COLUMNAS[<tabla>]`.
A5 toda clave de subíndice con cadena literal (`d["x"]`) está en la lista
   blanca o en los nombres derivados de los seis componentes.
A6 `groupby` aparece sólo dentro de `agrega`.

Uso: python3 -m tools.dominios.amai.auditoria_enigh2024 [ruta]  -> AUDITORIA-VERDE | ROJA
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

RUTA = Path(__file__).with_name("enigh2024.py")
IMPORTS = {"__future__", "hashlib", "io", "json", "re", "zipfile", "pathlib",
           "numpy", "pandas", "tools.dominios.amai"}
DE_MEDIDOR = {"distribucion", "validacion", "__file__"}
DERIVADOS = {"llave", "educa_jefe", "banos", "autos", "internet", "ocupados",
             "dormitorios", "factor", "EST_DIS", "UPM_DIS", "puntaje", "nivel", "grupo",
             "niveles", "grupos", "masa_puntaje_cero", "n_hogares_con_nse",
             "n_hogares_sin_nse", "estado", "desvio_max_grupo_pp", "desvio_max_nivel_pp",
             "parametros", "columnas_leidas", "input_id", "ruta_absoluta",
             "viviendas", "hogares", "concentrado", "n_min", "sum", "size", "calc_id"}


def _funcion_de(arbol: ast.AST) -> dict[ast.AST, str]:
    dueno = {}
    for f in ast.walk(arbol):
        if isinstance(f, ast.FunctionDef):
            for n in ast.walk(f):
                dueno[n] = f.name
    return dueno


def audita(fuente: str) -> list[str]:
    arbol = ast.parse(fuente)
    dueno = _funcion_de(arbol)
    fallas = []
    blanca = set()
    for n in ast.walk(arbol):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "COLUMNAS"
                                             for t in n.targets):
            for v in n.value.values:
                blanca |= {e.value for e in v.elts}
    permitidas = blanca | DERIVADOS
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] not in {i.split(".")[0] for i in IMPORTS} or \
                        a.name.startswith("tools"):
                    fallas.append(f"A1 import no autorizado: {a.name}")
        if isinstance(n, ast.ImportFrom):
            if n.module not in IMPORTS:
                fallas.append(f"A1 import no autorizado: from {n.module}")
            if n.module == "tools.dominios.amai":
                for a in n.names:
                    if a.name not in {"medidor", "regla"}:
                        fallas.append(f"A1 módulo AMAI no autorizado: {a.name}")
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "M":
            if n.attr not in DE_MEDIDOR:
                fallas.append(f"A2 uso del medidor no autorizado: M.{n.attr}")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "read_csv":
                if dueno.get(n) != "lee_acotado":
                    fallas.append("A3 read_csv fuera de lee_acotado")
                if not any(k.arg == "usecols" for k in n.keywords):
                    fallas.append("A3 read_csv sin usecols")
            if n.func.attr == "open" and dueno.get(n) != "lee_acotado":
                fallas.append("A3 .open( fuera de lee_acotado")
            if n.func.attr == "groupby" and dueno.get(n) != "agrega":
                fallas.append("A6 groupby fuera de agrega")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "lee_acotado":
            arg = n.args[2] if len(n.args) > 2 else None
            if not (isinstance(arg, ast.Subscript) and isinstance(arg.value, ast.Name)
                    and arg.value.id == "COLUMNAS"):
                fallas.append("A4 lee_acotado con columnas que no son COLUMNAS[...]")
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) \
                and isinstance(n.slice.value, str) and not (
                    isinstance(n.value, ast.Name) and n.value.id in {"MIEMBROS", "COLUMNAS",
                                                                      "masa", "out", "inputs",
                                                                      "contrato", "dist", "val"}):
            if n.slice.value not in permitidas:
                fallas.append(f"A5 columna no autorizada: {n.slice.value!r}")
    return fallas


def main(argv: list[str]) -> int:
    ruta = Path(argv[0]) if argv else RUTA
    fallas = audita(ruta.read_text(encoding="utf-8"))
    for f in fallas:
        print(f)
    print("AUDITORIA-VERDE" if not fallas else f"AUDITORIA-ROJA ({len(fallas)})")
    return 0 if not fallas else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
