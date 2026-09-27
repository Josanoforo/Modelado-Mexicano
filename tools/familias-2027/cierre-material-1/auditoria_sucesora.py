"""Control de I/O propuesto: código efectivo fijado y rutas exactas en ejecución.

No sustituye la firma de COMMIT-3 ni es sandbox para Python hostil. Se aplica
al código autenticado, cargado antes del contexto, en un proceso de una tarea.
"""
import ast
import contextlib
import hashlib
import os
from pathlib import Path
import sys


def audita(codigo, sha_esperado):
    if hashlib.sha256(codigo.encode()).hexdigest() != sha_esperado:
        raise ValueError("CODIGO-EFECTIVO-DISCORDANTE")
    tree = ast.parse(codigo)
    imports = {"csv", "io", "json", "math", "hashlib", "zipfile", "pathlib",
               "collections", "numpy"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = ([a.name.split('.')[0] for a in node.names]
                     if isinstance(node, ast.Import) else [node.module.split('.')[0]])
            if set(names) - imports:
                raise ValueError("IMPORTACION-AJENA")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"open", "eval", "exec", "__import__", "compile"}:
                raise ValueError("IO-DINAMICO-AJENO")
    # El hash protege todas las funciones y accesos, no solo nombres de imports.
    return {"sha256": sha_esperado, "funciones": [n.name for n in tree.body
            if isinstance(n, ast.FunctionDef)], "estado": "CODIGO-AUTENTICADO"}


class RutasExactas:
    """Rechaza open/Path/ZIP ajenos, escrituras fuera de tablas y enlaces.

    Se instala una vez por proceso; inactive fuera de la invocación material.
    El caller confiable acredita los inputs y pasa archivos concretos, no dirs.
    """
    def __init__(self, lecturas, escrituras=(), directorios=()):
        self.lecturas = {Path(p).resolve() for p in lecturas}
        self.escrituras = {Path(p).absolute() for p in escrituras}
        self.directorios = {Path(p).absolute() for p in directorios}
        self.activa = False
        sys.addaudithook(self._hook)

    def _salida(self, ruta):
        p = Path(os.fsdecode(ruta)).absolute()
        if any(a.is_symlink() for a in [p, *p.parents]):
            raise PermissionError("ENLACE-DE-SALIDA")
        if p != p.resolve():
            raise PermissionError("RUTA-DE-SALIDA-NO-CANONICA")
        return p

    def _hook(self, evento, args):
        if not self.activa:
            return
        if evento == "open":
            ruta, modo, flags = args
            if isinstance(ruta, int):
                raise PermissionError("DESCRIPTOR-NO-AUTORIZADO")
            escritura = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT |
                                      os.O_TRUNC | os.O_APPEND))
            if escritura:
                if self._salida(ruta) not in self.escrituras:
                    raise PermissionError("ESCRITURA-AJENA")
            elif Path(os.fsdecode(ruta)).resolve() not in self.lecturas | self.escrituras:
                raise PermissionError("LECTURA-AJENA")
        elif evento == "os.mkdir":
            if args[2] != -1 or self._salida(args[0]) not in self.directorios:
                raise PermissionError("DIRECTORIO-AJENO")
        elif evento in {"os.remove", "os.rename", "os.rmdir", "os.symlink",
                        "os.link", "os.chdir", "subprocess.Popen", "os.system"}:
            raise PermissionError("OPERACION-AJENA")

    @contextlib.contextmanager
    def aplica(self):
        self.activa = True
        try:
            yield
        finally:
            self.activa = False
