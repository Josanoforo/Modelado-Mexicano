"""H5 (hoja NC-DECISIONES-1, fila H5, firma de mesa 28/sep, ejecutado por
`ACTO GEN2-TUBERIA-Y-CURACION-1`): `docs/index.md` lleva los mismos
marcadores `deriva[...]` que `README.md` (`tools/readme_derivado.py::DOCUMENTOS`
ya recomputa las dos), pero el job `derivados` de `.github/workflows/verify.yml`
solo committeaba `README.md` -- el recómputo de `docs/index.md` se descartaba
en cada corrida sin que nadie lo notara (defecto real, no hipotético: medido
27/sep, NC-260926-GEN2-FRONT-3-PORTADA-1-8914-01).

Guarda estática sobre el YAML (no ejecuta el job): la línea `git add` del
paso que commitea los derivados debe citar `docs/index.md` junto con
`README.md`. Un test que corriera el job completo sería más caro que el
defecto que atrapa (D-14); esta línea es exactamente lo que se rompió.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERIFY = (ROOT / ".github/workflows/verify.yml").read_text(encoding="utf-8")

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_git_add_derivados_incluye_index():
    lineas = [l for l in VERIFY.splitlines() if l.lstrip().startswith("git add --")
              and "data/corrida0/corridas.tsv" in l]
    afirma(len(lineas) == 1,
           f"se esperaba exactamente una línea `git add` del job derivados con "
           f"data/corrida0/corridas.tsv, se encontraron {len(lineas)}")
    if len(lineas) == 1:
        campos = lineas[0].split()
        afirma("README.md" in campos, "la línea debe seguir citando README.md")
        afirma("docs/index.md" in campos,
               "docs/index.md debe entrar al mismo `git add` que README.md "
               "(H5): " + lineas[0])


def prueba_readme_derivado_ya_recomputa_index():
    # Guarda cruzada: si algún día DOCUMENTOS deja de incluir docs/index.md,
    # el `git add` de arriba quedaría commiteando un archivo que el propio
    # escritor ya no toca -- silencioso de otro modo.
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import readme_derivado as RD
    rutas = {p.name for p in RD.DOCUMENTOS}
    afirma("index.md" in rutas, f"tools/readme_derivado.py::DOCUMENTOS debe incluir docs/index.md: {rutas}")


def main():
    prueba_git_add_derivados_incluye_index()
    prueba_readme_derivado_ya_recomputa_index()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print(f"OK -- {Path(__file__).name}: 2 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
