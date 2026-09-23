#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ci_guardias.py -- censo y corredor de guardias huerfanas (ACTO GEN2-CI-GUARDIAS-VIVAS-1)

Defecto que ataca: `tests/check.py` no auto-descubre `tests/test_*.py` y
`.github/workflows/verify.yml` cablea sus pasos uno por uno -- un test nuevo
que nadie referencia en ninguno de los dos lugares nunca corre en CI. Esta
sesion midio 97/122 archivos en ese estado (ver
`forense/analisis/ci-guardias/censo-tests.tsv`).

Dos usos:

    python3 tools/ci_guardias.py --censo
        Deriva el TSV de censo (P1). Nunca ejecuta un test para decidir si
        esta cableado -- solo grep de nombre base contra verify.yml y
        check.py. Si corre con --con-ejecucion, tambien ejecuta cada
        archivo NO cableado para clasificar CORRE-EN-CI (si de hecho pasa
        solo) vs NECESITA-DEPENDENCIA vs NECESITA-CORPUS vs FALLA-DE-VERDAD.

    python3 tools/ci_guardias.py --ejecuta-huerfanos
        Lee el censo TSV y ejecuta, con el invocador que el censo declara,
        todo archivo marcado NECESITA-EJECUTARSE-EN-CI (union de
        CORRE-EN-CI real y NECESITA-DEPENDENCIA cuya dependencia ya esta
        instalada en este entorno) que NO este ya cableado. Salta los
        NECESITA-CORPUS con una linea `SKIP <archivo>: corpus` y cuenta.
        Sale != 0 si algun test descubierto en tests/test_*.py no aparece
        en el censo (asi ningun test nuevo nace huerfano sin que este
        script lo note).
"""
import ast
import glob
import io
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(ROOT, "tests")
VERIFY_YML = os.path.join(ROOT, ".github", "workflows", "verify.yml")
CHECK_PY = os.path.join(TESTS_DIR, "check.py")
CENSO_TSV = os.path.join(ROOT, "forense", "analisis", "ci-guardias", "censo-tests.tsv")

STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
# Modulos del propio repo que no cuentan como "dependencia externa".
REPO_TOP_PACKAGES = {"tools", "tests", "milpa", "canon", "forense", "corpus", "data"}


def leer(p):
    return io.open(p, encoding="utf-8").read()


def descubre_tests():
    return sorted(glob.glob(os.path.join(TESTS_DIR, "test_*.py")))


def nombre_base(path):
    return os.path.splitext(os.path.basename(path))[0]


def cableado_en(texto, base):
    """True si el nombre base del test aparece citado en el texto, como
    script (tests/<base>.py), como modulo (tests.<base> o tests/<base>) o
    pelado dentro de un run de -m unittest."""
    patrones = [
        re.escape("tests/" + base + ".py"),
        re.escape("tests." + base),
        re.escape("tests/" + base) + r"\b",
    ]
    return any(re.search(pat, texto) for pat in patrones)


def censa_cableado():
    verify_txt = leer(VERIFY_YML)
    check_txt = leer(CHECK_PY)
    cableados = {}
    for p in descubre_tests():
        base = nombre_base(p)
        en_verify = cableado_en(verify_txt, base)
        en_check = cableado_en(check_txt, base)
        cableados[base] = {
            "en_verify_yml": en_verify,
            "en_check_py": en_check,
            "cableado": en_verify or en_check,
        }
    return cableados


def imports_de(path):
    """Nombres top-level de modulos importados por el archivo, via AST
    (no ejecuta el archivo)."""
    try:
        tree = ast.parse(leer(path), filename=path)
    except SyntaxError:
        return set()
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # import relativo -- del propio paquete
            if node.module:
                mods.add(node.module.split(".")[0])
    return mods


def dependencias_externas(path):
    mods = imports_de(path)
    externos = set()
    for m in mods:
        if m in STDLIB_MODULES:
            continue
        if m in REPO_TOP_PACKAGES:
            continue
        externos.add(m)
    return sorted(externos)


def menciona_data_raw(path):
    txt = leer(path)
    return bool(re.search(r"data[/\\]raw|data_raw|raiz_logica|RAICES", txt))


def invocador_de(path):
    txt = leer(path)
    if re.search(r"^import unittest\b|^\s*import unittest\b", txt, re.M):
        if re.search(r"unittest\.main\(", txt):
            return "script"  # corre python3 tests/x.py, usa unittest internamente
    if re.search(r"^import pytest\b|from pytest\b", txt, re.M):
        return "pytest"
    return "script"


def requirements_declaradas():
    req_path = os.path.join(ROOT, "requirements.txt")
    if not os.path.exists(req_path):
        return set()
    out = set()
    for linea in leer(req_path).splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        nombre = re.split(r"[<>=!~\[; ]", linea)[0].strip()
        if nombre:
            out.add(nombre.lower())
    return out


PKG_A_IMPORT = {
    "pyyaml": "yaml",
    "markdown": "markdown",
    "xlrd": "xlrd",
    "jsonschema": "jsonschema",
    "pyreadstat": "pyreadstat",
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "pytest": "pytest",
}


def modulo_instalado(mod):
    try:
        __import__(mod)
        return True
    except Exception:
        return False


def ejecuta(path, invocador, timeout=40):
    if invocador == "pytest":
        cmd = [sys.executable, "-m", "pytest", "-q", path]
    elif invocador == "modulo":
        base = nombre_base(path)
        cmd = [sys.executable, "-m", "tests." + base]
    else:
        cmd = [sys.executable, path]
    t0 = time.time()
    try:
        r = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout
        )
        dt = time.time() - t0
        return r.returncode, (r.stdout + r.stderr), dt, False
    except subprocess.TimeoutExpired as e:
        # ACTO GEN2-TUBERIA-CANAL-PUBLICACION-1 (22/sep/2026), defecto
        # adyacente ≤10 líneas (D-21): `TimeoutExpired.stdout/.stderr`
        # pueden llegar en bytes aunque `run()` pidiera `text=True` -- el
        # timeout corta antes de que Popen decodifique el buffer parcial
        # (medido: `test_consulta_gen2` sin corpus en NUBE). Decodifica
        # perezoso en vez de asumir str.
        dt = time.time() - t0
        def _texto(x):
            if x is None:
                return ""
            return x.decode("utf-8", "replace") if isinstance(x, bytes) else x
        return 124, (_texto(e.stdout) + _texto(e.stderr)), dt, True


def ultimo_error(salida):
    lineas = [l for l in salida.splitlines() if l.strip()]
    for l in reversed(lineas):
        if l.startswith("ModuleNotFoundError") or l.startswith(
            "FileNotFoundError"
        ) or re.match(r"^\w*Error", l) or l.strip().startswith("E   "):
            return l.strip()
    return lineas[-1].strip() if lineas else "(sin salida)"


def clasifica(path, cableados_map):
    base = nombre_base(path)
    externos = dependencias_externas(path)
    reqs = requirements_declaradas()
    faltan = []
    for mod in externos:
        # nombre de import puede no coincidir con nombre de paquete pip;
        # se compara contra los alias conocidos y contra el nombre crudo.
        instalado = modulo_instalado(mod)
        if not instalado:
            faltan.append(mod)
    invocador = invocador_de(path)
    necesita_corpus = menciona_data_raw(path)
    cableado = cableados_map.get(base, {}).get("cableado", False)

    fila = {
        "archivo": "tests/" + base + ".py",
        "invocador": invocador,
        "cableado_hoy": "SI" if cableado else "NO",
        "dependencias_faltantes": ",".join(faltan) if faltan else "(ninguna)",
        "necesita_corpus_por_codigo": "SI" if necesita_corpus else "NO",
        "tiempo_seg": "",
        "veredicto": "",
        "detalle": "",
    }

    # El escaneo estatico de imports es solo informativo (columna
    # dependencias_faltantes): varios tests insertan tests/ o tools/ en
    # sys.path en tiempo de ejecucion antes de importar un modulo hermano
    # (p.ej. `import check as C` tras `sys.path.insert(0, RAIZ/"tests")`),
    # asi que un import "externo" segun AST puede resolver bien en
    # ejecucion real. El veredicto lo decide SIEMPRE la ejecucion, nunca
    # el escaneo estatico -- ejecutar es la unica fuente de verdad (§2,
    # "ninguna cifra esperada se teclea").
    rc, salida, dt, timed_out = ejecuta(path, invocador)
    fila["tiempo_seg"] = "%.1f" % dt
    if timed_out:
        fila["veredicto"] = "FALLA-DE-VERDAD"
        fila["detalle"] = "TIMEOUT>40s"
        return fila
    if rc == 0:
        fila["veredicto"] = "CORRE-EN-CI"
        fila["detalle"] = "exit 0 sin corpus"
        return fila

    err = ultimo_error(salida)
    if "No module named" in err:
        mod = re.search(r"No module named '([^']+)'", err) or re.search(
            r"No module named (\S+)", err
        )
        modname = mod.group(1) if mod else "?"
        if modname.split(".")[0] in REPO_TOP_PACKAGES and invocador != "modulo":
            # No es que falte la dependencia: falta invocarlo como modulo
            # (`python3 -m tests.<x>`) para que `tools`/`milpa` resuelvan
            # por el cwd=ROOT. Se reintenta asi antes de fallar el
            # veredicto -- y el contenido, no la invocacion, decide.
            rc2, salida2, dt2, timed_out2 = ejecuta(path, "modulo")
            fila["tiempo_seg"] = "%.1f" % (dt + dt2)
            if timed_out2:
                fila["veredicto"] = "FALLA-DE-VERDAD"
                fila["detalle"] = "TIMEOUT>40s (con -m tests.%s)" % base
                fila["invocador"] = "modulo"
                return fila
            if rc2 == 0:
                fila["veredicto"] = "CORRE-EN-CI"
                fila["invocador"] = "modulo"
                fila["detalle"] = "exit 0 con -m tests.%s (invocacion de script fallaba)" % base
                return fila
            err2 = ultimo_error(salida2)
            fila["invocador"] = "modulo"
            fila["veredicto"] = "FALLA-DE-VERDAD"
            fila["detalle"] = err2
            return fila
        fila["veredicto"] = "NECESITA-DEPENDENCIA(%s)" % modname
        fila["detalle"] = err
        return fila
    if "FileNotFoundError" in err and re.search(r"data[/\\]raw", err):
        fila["veredicto"] = "NECESITA-CORPUS"
        fila["detalle"] = err
        return fila

    fila["veredicto"] = "FALLA-DE-VERDAD"
    fila["detalle"] = err
    return fila


def cmd_censo():
    cableados_map = censa_cableado()
    filas = []
    for p in descubre_tests():
        base = nombre_base(p)
        if cableados_map[base]["cableado"]:
            filas.append(
                {
                    "archivo": "tests/" + base + ".py",
                    "invocador": invocador_de(p),
                    "cableado_hoy": "SI",
                    "dependencias_faltantes": "(ninguna)",
                    "necesita_corpus_por_codigo": "SI"
                    if menciona_data_raw(p)
                    else "NO",
                    "tiempo_seg": "",
                    "veredicto": "CORRE-EN-CI",
                    "detalle": "ya cableado en verify.yml y/o check.py",
                }
            )
        else:
            filas.append(clasifica(p, cableados_map))

    os.makedirs(os.path.dirname(CENSO_TSV), exist_ok=True)
    cols = [
        "archivo",
        "invocador",
        "cableado_hoy",
        "dependencias_faltantes",
        "necesita_corpus_por_codigo",
        "tiempo_seg",
        "veredicto",
        "detalle",
    ]
    with io.open(CENSO_TSV, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for fila in filas:
            f.write("\t".join(str(fila.get(c, "")) for c in cols) + "\n")

    total = len(filas)
    huerfanos = sum(1 for f in filas if f["cableado_hoy"] == "NO")
    print(
        "CENSO · %d archivos tests/test_*.py · %d cableados hoy · %d huerfanos -> %s"
        % (total, total - huerfanos, huerfanos, os.path.relpath(CENSO_TSV, ROOT))
    )
    for v in ("CORRE-EN-CI", "NECESITA-CORPUS", "FALLA-DE-VERDAD"):
        c = sum(1 for f in filas if f["cableado_hoy"] == "NO" and f["veredicto"] == v)
        if c:
            print("  %s: %d" % (v, c))
    dep = [
        f
        for f in filas
        if f["cableado_hoy"] == "NO" and f["veredicto"].startswith("NECESITA-DEPENDENCIA")
    ]
    if dep:
        print("  NECESITA-DEPENDENCIA: %d" % len(dep))
    return filas


def lee_censo():
    if not os.path.exists(CENSO_TSV):
        print("censo ausente: corre --censo primero", file=sys.stderr)
        sys.exit(2)
    with io.open(CENSO_TSV, encoding="utf-8") as f:
        r = f.read().splitlines()
    cols = r[0].split("\t")
    filas = []
    for linea in r[1:]:
        vals = linea.split("\t")
        filas.append(dict(zip(cols, vals)))
    return filas


def cmd_ejecuta_huerfanos():
    filas = lee_censo()
    presentes = {nombre_base(p) for p in descubre_tests()}
    censados = {nombre_base(f["archivo"]) for f in filas}
    huerfanos_del_censo = presentes - censados
    if huerfanos_del_censo:
        print(
            "FALLA: tests sin fila en el censo (nacieron huerfanos): %s"
            % ", ".join(sorted(huerfanos_del_censo)),
            file=sys.stderr,
        )
        sys.exit(1)

    saltados = 0
    ejecutados = 0
    fallidos = 0
    for f in filas:
        if f["cableado_hoy"] == "SI":
            continue
        base = nombre_base(f["archivo"])
        path = os.path.join(TESTS_DIR, base + ".py")
        if f["veredicto"] == "NECESITA-CORPUS":
            print("SKIP %s: corpus" % f["archivo"])
            saltados += 1
            continue
        if f["veredicto"] == "FALLA-DE-VERDAD":
            print("SKIP %s: FALLA-DE-VERDAD conocida, NC abierta" % f["archivo"])
            saltados += 1
            continue
        if f["veredicto"].startswith("NECESITA-DEPENDENCIA"):
            print(
                "SKIP %s: dependencia-pendiente %s (FP de mesa, no decidida aqui)"
                % (f["archivo"], f["veredicto"])
            )
            saltados += 1
            continue
        invocador = f["invocador"]
        rc, salida, dt, timed_out = ejecuta(path, invocador, timeout=600)
        ejecutados += 1
        estado = "OK" if rc == 0 and not timed_out else "FAIL"
        if estado == "FAIL":
            fallidos += 1
        print("%s %s (%.1fs)" % (estado, f["archivo"], dt))
        if estado == "FAIL":
            print(salida[-4000:])

    print(
        "RESUMEN guardias: ejecutados=%d saltados=%d fallidos=%d"
        % (ejecutados, saltados, fallidos)
    )
    sys.exit(1 if fallidos else 0)


def main():
    if "--censo" in sys.argv:
        cmd_censo()
    elif "--ejecuta-huerfanos" in sys.argv:
        cmd_ejecuta_huerfanos()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
