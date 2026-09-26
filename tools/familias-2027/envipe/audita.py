"""Guardia estática del medidor: sin imports/cargadores de productores vivos."""
import ast
from pathlib import Path

IMPORTS = {'csv', 'hashlib', 'io', 'zipfile', 'pathlib', 'numpy'}


def auditar(texto):
    tree = ast.parse(texto)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [x.name.split('.')[0] for x in node.names] if isinstance(node, ast.Import) else [node.module]
            if not set(names) <= IMPORTS:
                raise ValueError('import fuera de lista blanca')
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {'eval','exec','open','__import__'}:
                raise ValueError('cargador dinámico/fuera de guardia')
            if isinstance(node.func, ast.Attribute) and node.func.attr in {'read_csv','read_excel','extract','extractall','read_text'}:
                raise ValueError('lectura fuera de guardia')
    # Comprobaciones sobre estructura de la selección, no sólo texto de comentarios.
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    if not any(isinstance(n.func, ast.Attribute) and n.func.attr == 'open'
               and isinstance(n.func.value, ast.Name) and n.func.value.id == 'z'
               and len(n.args) == 1 and isinstance(n.args[0], ast.Name)
               and n.args[0].id == 'member' for n in calls):
        raise ValueError('miembro ZIP congelado no localizado')
    return True


if __name__ == '__main__':
    auditar(Path(__file__).with_name('medidor.py').read_text())
    print('AUDITORIA-CODIGO: PASS; lector cerrado; sin productor histórico importado')
