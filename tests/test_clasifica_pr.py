#!/usr/bin/env python3
"""`tools/clasifica_pr.py`, probado con diffs sintéticos.

ACTO `GEN2-TUBERIA-ENRUTAMIENTO-PR-1`, P3.

Un caso por clase; uno que dispara DOS señales y sale con la de mayor
precedencia listando AMBAS; uno sin archivos; y uno que adopta VARIOS CALC
y los cuenta bien. Más el punto de entrada corrido de verdad sobre un diff
real -- un medidor cuyas pruebas sólo ejercitan guardias y constantes no es
un COMMIT-1 (D-22).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import clasifica_pr as C  # noqa: E402

FALLOS: list[str] = []


def ok(cond: bool, msg: str) -> None:
    if cond:
        print(f"  ok   {msg}")
    else:
        print(f"  FAIL {msg}")
        FALLOS.append(msg)


def ns(*pares: tuple[str, str]) -> list[str]:
    """Construye un `--name-status` sintético y lo pasa por el parser real."""
    texto = "\n".join(f"{e}\t{r}" for e, r in pares)
    return [r for _, r in C.rutas_de_name_status(texto)]


def caso_por_clase() -> None:
    print("1 · un caso por clase")

    r = C.clasifica(ns(("A", "data/corrida0/CALC-0042/sello.json")))
    ok(r["clase"] == "ADOPTA", f"sello.json -> ADOPTA (dio {r['clase']})")
    ok("adopta 1 corrida sellada" in r["enrutamiento"], "ADOPTA cuenta 1 y singulariza")
    ok("CALC-0042" in r["enrutamiento"], "ADOPTA nombra el CALC")

    r = C.clasifica(ns(("M", "data/corrida0/decisiones.tsv")))
    ok(r["clase"] == "FIRMA", f"decisiones.tsv -> FIRMA (dio {r['clase']})")
    ok("firma verbatim" in r["enrutamiento"], "FIRMA pide citar la firma verbatim")

    r = C.clasifica(ns(("M", "milpa/algo.md")))
    ok(r["clase"] == "FIRMA", f"milpa/ -> FIRMA (dio {r['clase']})")

    r = C.clasifica(ns(("M", "tests/check.py")))
    ok(r["clase"] == "APARATO", f"tests/check.py -> APARATO (dio {r['clase']})")
    ok("la suite en verde" in r["enrutamiento"], "APARATO manda a la suite")

    r = C.clasifica(ns(("M", "forense/notas/una-nota.md"), ("A", "README.md")))
    ok(r["clase"] == "REVISIÓN", f"nota+README -> REVISIÓN (dio {r['clase']})")
    ok(r["señales"] == [], "REVISIÓN no dispara ninguna señal")


def caso_dos_señales() -> None:
    print("2 · dos señales a la vez: gana la precedencia, se listan ambas")
    r = C.clasifica(ns(
        ("A", "data/corrida0/CALC-0007/sello.json"),
        ("M", ".github/workflows/verify.yml"),
    ))
    ok(r["clase"] == "ADOPTA", f"ADOPTA > APARATO (dio {r['clase']})")
    ok(r["señales"] == ["ADOPTA", "APARATO"],
       f"ambas señales, en orden de precedencia (dio {r['señales']})")

    # Las cuatro a la vez, para que la precedencia completa quede probada.
    r = C.clasifica(ns(
        ("A", "data/corrida0/CALC-0001/sello.json"),
        ("M", "milpa/x.md"),
        ("M", "tools/corrida0.py"),
        ("M", "otro/archivo.txt"),
    ))
    ok(r["señales"] == ["ADOPTA", "FIRMA", "APARATO"],
       f"precedencia completa (dio {r['señales']})")
    ok(r["clase"] == "ADOPTA", "la principal sigue siendo ADOPTA")

    # FIRMA gana a APARATO cuando no hay sello.
    r = C.clasifica(ns(("M", "data/corrida0/CALC-0001/spec.yaml"),
                       ("M", ".gitattributes")))
    ok(r["clase"] == "FIRMA", f"FIRMA > APARATO (dio {r['clase']})")


def caso_vacio() -> None:
    print("3 · diff sin archivos")
    r = C.clasifica([])
    ok(r["clase"] == "REVISIÓN", f"sin archivos -> REVISIÓN (dio {r['clase']})")
    ok(r["n_archivos"] == 0, "cuenta 0 archivos")
    ok(r["calc_adoptados"] == [], "cero CALC")
    ok("Ninguna señal disparada" in C.markdown(r), "el markdown lo dice sin fallar")


def caso_varios_calc() -> None:
    print("4 · adopta varios CALC y los cuenta bien")
    r = C.clasifica(ns(
        ("A", "data/corrida0/CALC-0001/sello.json"),
        ("A", "data/corrida0/CALC-0002/sello.json"),
        ("A", "data/corrida0/CALC-0003/sello.json"),
        # Ruido que NO debe contar como CALC adoptado:
        ("A", "data/corrida0/CALC-0003/ejecucion.json"),
        ("M", "data/corrida0/CALC-0004/spec.yaml"),
    ))
    ok(r["clase"] == "ADOPTA", f"-> ADOPTA (dio {r['clase']})")
    ok(r["calc_adoptados"] == ["CALC-0001", "CALC-0002", "CALC-0003"],
       f"tres CALC, sin contar el spec.yaml ni el ejecucion.json "
       f"(dio {r['calc_adoptados']})")
    ok("adopta 3 corridas selladas" in r["enrutamiento"],
       f"la línea dice 3 y pluraliza (dio: {r['enrutamiento']})")
    ok("FIRMA" in r["señales"], "el spec.yaml sí dispara FIRMA como señal secundaria")


def caso_renombre_y_borrado() -> None:
    print("5 · renombre y borrado")
    rutas = C.rutas_de_name_status(
        "R100\tdata/viejo/sello.json\tdata/corrida0/CALC-0009/sello.json"
    )
    ok(rutas == [("R", "data/corrida0/CALC-0009/sello.json")],
       f"un renombre se lee por su ruta NUEVA (dio {rutas})")
    r = C.clasifica(ns(("D", "data/corrida0/CALC-0010/sello.json")))
    ok(r["clase"] == "ADOPTA",
       "borrar un sello también dispara: no es menos grave que añadirlo")


def caso_punto_de_entrada() -> None:
    """D-22: el punto de entrada corre de verdad, no sólo las funciones."""
    print("6 · punto de entrada, corrido (D-22)")
    with tempfile.TemporaryDirectory() as td:
        diff = Path(td) / "d.txt"
        diff.write_text("A\tdata/corrida0/CALC-0123/sello.json\n"
                        "M\t.github/workflows/verify.yml\n", encoding="utf-8")
        resumen = Path(td) / "resumen.md"
        p = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "clasifica_pr.py"),
             "--diff", str(diff), "--resumen", str(resumen)],
            capture_output=True, text=True,
        )
        ok(p.returncode == 0, f"sale 0 pese a clasificar ADOPTA (rc={p.returncode})")
        ok("`ADOPTA`" in p.stdout, "imprime la clase")
        ok(resumen.exists() and "CALC-0123" in resumen.read_text(encoding="utf-8"),
           "escribe el resumen al archivo de --resumen")

        # Sólo falla si no puede LEER el diff.
        p2 = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "clasifica_pr.py"),
             "--diff", str(Path(td) / "no-existe.txt")],
            capture_output=True, text=True,
        )
        ok(p2.returncode == 2, f"diff ilegible -> rc 2 (dio {p2.returncode})")
        ok("NO-PUDE-LEER-EL-DIFF" in p2.stderr, "y lo dice con su token")

    # Y sobre el árbol REAL, por git, contra la base de este repo.
    p3 = subprocess.run(
        [sys.executable, str(RAIZ / "tools" / "clasifica_pr.py"),
         "--base", "HEAD", "--cabeza", "HEAD"],
        capture_output=True, text=True,
    )
    ok(p3.returncode == 0, f"corre contra git sobre el árbol real (rc={p3.returncode})")


def caso_tabla_coherente() -> None:
    print("7 · la tabla de señales, coherente (D-15)")
    for señal, cfg in C.SEÑALES.items():
        ok(señal in C.PRECEDENCIA, f"`{señal}` está en PRECEDENCIA")
        for patron, porque in cfg["rutas"]:
            ok(bool(porque.strip()), f"`{patron}` trae su línea de por qué")
    ok(C.PRECEDENCIA[-1] == "REVISIÓN", "REVISIÓN es el resto, al final")


def caso_la_clase_nunca_adjudica() -> None:
    """El PARO del encargo, blindado: «que la clase haga fallar el CI».

    Desde que el job `enrutamiento-pr` entró a `needs` de `check` (la guarda
    de `tests/test_check_parallel.py` deriva el conjunto del workflow: TODO
    job menos el gate es requerido), lo único que separa a la clase de
    adjudicar es que el punto de entrada salga 0 SIEMPRE. Eso deja de ser
    una propiedad leída del código y pasa a ser una que se prueba: una de
    las cuatro clases saliendo distinto de 0 bloquearía un PR por lo que
    toca, que es exactamente lo que el encargo prohíbe.
    """
    print("8 · la clase nunca adjudica (D-16): rc 0 en las CUATRO clases")
    casos = {
        "ADOPTA": "A\tdata/corrida0/CALC-0001/sello.json\n",
        "FIRMA": "M\tmilpa/x.md\n",
        "APARATO": "M\ttests/check.py\n",
        "REVISIÓN": "M\tREADME.md\n",
    }
    with tempfile.TemporaryDirectory() as td:
        for esperada, cuerpo in casos.items():
            d = Path(td) / f"{esperada}.txt"
            d.write_text(cuerpo, encoding="utf-8")
            p = subprocess.run(
                [sys.executable, str(RAIZ / "tools" / "clasifica_pr.py"), "--diff", str(d)],
                capture_output=True, text=True,
            )
            ok(p.returncode == 0, f"clase {esperada} -> rc 0 (dio {p.returncode})")
            ok(f"`{esperada}`" in p.stdout, f"y la reporta como {esperada}")


def main() -> int:
    for f in (caso_por_clase, caso_dos_señales, caso_vacio, caso_varios_calc,
              caso_renombre_y_borrado, caso_punto_de_entrada, caso_tabla_coherente,
              caso_la_clase_nunca_adjudica):
        f()
    print()
    if FALLOS:
        print(f"FAIL · {len(FALLOS)} caso(s): " + " · ".join(FALLOS))
        return 1
    print("OK · todos los casos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
