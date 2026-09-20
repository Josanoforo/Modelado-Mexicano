"""Instrumenta main() sin sustituir su inventario. Salida JSON fuera del repo.

Uso: python3 medir-suite.py CHECKOUT /tmp/medicion.json [--parallel]
Los JSON guardan diagnósticos completos para comparar multiconjuntos y orden.
"""
import ast
import sys
import time
import json
import resource
from pathlib import Path

def main():
    root = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2])
    parallel = '--parallel' in sys.argv
    sys.path.insert(0, str(root / 'tests'))
    sys.argv = [str(root / 'tests/check.py'), '--baseline'] + (['--parallel'] if parallel else [])
    import check
    times = {}
    tree = ast.parse((root / 'tests/check.py').read_text())
    main_fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    inventory = next(n.value for n in main_fn.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'tests' for t in n.targets))
    # Instrumentación de la lista explícita existente; no descubre nuevas pruebas.
    names = [item.elts[1].id for item in inventory.elts] + ['t16_suite_self_check']
    for name in names:
        fn = getattr(check, name)
        if callable(fn):
            def wrapped(*args, _name=name, _fn=fn, **kwargs):
                start = time.perf_counter()
                try:
                    return _fn(*args, **kwargs)
                finally:
                    elapsed = time.perf_counter() - start
                    times.setdefault(_name, elapsed)
                    print(f'TIMING {_name} {elapsed:.3f}s', flush=True)
            setattr(check, name, wrapped)
    start = time.perf_counter()
    code = check.main()
    usage = [resource.getrusage(who) for who in (resource.RUSAGE_SELF, resource.RUSAGE_CHILDREN)]
    output.write_text(json.dumps({'total': time.perf_counter()-start, 'code': code,
                                  'cpu': sum(u.ru_utime+u.ru_stime for u in usage),
                                  'times': times, 'fails': check.FAILS,
                                  'warns': check.WARNS, 'senal': check.SENAL}, indent=2))
    return code

if __name__ == '__main__':
    sys.exit(main())
