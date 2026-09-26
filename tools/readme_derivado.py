#!/usr/bin/env python3
"""Deriva las cifras de la portada (README.md, docs/index.md) y sus badges por comando.

ACTO GEN2-FRONT-3-PORTADA-1 (P2). Sucede a la versión de FRONT-1 que solo
refrescaba la tabla de `corrida0.py status`: esa tabla vive ahora en
`docs/estado.md` como claves y comandos, sin valores que puedan envejecer.

Cada cifra visible de README.md va escrita como

    **<valor>** <!-- deriva[<clave>]: <comando> -->

El comentario es invisible en el render. `<clave>` debe estar en FUENTES y
`<comando>` debe ser, verbatim, el comando que FUENTES declara para esa clave:
nunca se ejecuta un comando tomado del Markdown (el comando visible es para el
lector; el cálculo es el de FUENTES, que hace lo mismo sin shell).

Las cifras que mueve `corrida0.py status` van en la línea de cifras, dentro del
bloque TABLERO-DERIVADO, que es lo único que `derivados_protegidos.py
--solo-derivados` acepta cambiar en un PR `[deriva]` del job guardias.

Los badges (`docs/data/badges/*.json`, formato `endpoint` de shields.io) solo
llevan cifras que el job guardias no mueve (evaluaciones, instrumentos,
celdas, reports): el job no añade esa carpeta a su commit, así que un badge de
`status` quedaría viejo en silencio.

Uso:
  python3 tools/readme_derivado.py              # 1 si README o badges tienen desfase
  python3 tools/readme_derivado.py --escribe    # reescribe valores y badges
  python3 tools/readme_derivado.py --clave K    # imprime el valor de una clave
  python3 tools/readme_derivado.py --vista-previa   # docs/assets/social-preview.png (1280x640)

La vista previa social (Settings -> Social preview) se genera sin red con
el `headless_shell` de Chromium (Playwright lo trae en /opt/pw-browsers; o
`CHROMIUM=<ruta>`; el `chrome` completo recorta ~90 px de alto):
título, tagline del README y las tres cifras de la prueba, sin logos ajenos.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"
# Documentos con marcas deriva[...]: la portada y la landing (P4: mismas cifras).
DOCUMENTOS = [README, RAIZ / "docs" / "index.md"]
BADGES = RAIZ / "docs" / "data" / "badges"
CENSO = "forense/analisis/informe-v1_3/censo_evaluaciones.py"
COBERTURA = "forense/analisis/dominios/cobertura-v1_1.tsv"

MARCA = re.compile(r"\*\*([^*\n]+)\*\* <!-- deriva\[([A-Za-z_]+)\]: (.+?) -->")

_PALABRAS = ["cero", "una", "dos", "tres", "cuatro", "cinco", "seis", "siete",
             "ocho", "nueve", "diez"]


def _miles(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def _palabra(n: int) -> str:
    return _PALABRAS[n] if 0 <= n < len(_PALABRAS) else _miles(n)


_CACHE: dict[str, str] = {}


def _status(clave: str) -> int:
    if "status" not in _CACHE:
        _CACHE["status"] = subprocess.check_output(
            [sys.executable, "tools/corrida0.py", "status"], cwd=RAIZ, text=True)
    m = re.search(rf"(?m)^{re.escape(clave)}=(\d+)$", _CACHE["status"])
    if not m:
        raise SystemExit(f"{clave} no aparece en corrida0.py status")
    return int(m.group(1))


def _censo(clave: str) -> int:
    return int(subprocess.check_output(
        [sys.executable, CENSO, "--clave", clave], cwd=RAIZ, text=True).strip())


def _reports() -> set[str]:
    return {p.name for p in (RAIZ / "corpus" / "reports").glob("*.md")}


def _reports_medibles() -> int:
    """Reports de corpus/reports con al menos una afirmación MEDIBLE-EN-CORPUS
    en la tabla de cobertura del mapa de dominios v1.1 (medible, no medida)."""
    with open(RAIZ / COBERTURA, encoding="utf-8") as f:
        filas = csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t")
        reps = _reports()
        return sum(1 for r in filas if r["report"] in reps and int(r["medible_en_corpus"]) > 0)


def _doi() -> str:
    m = re.search(r"(?m)^doi:\s*\"?([^\"\n]+)", (RAIZ / "CITATION.cff").read_text(encoding="utf-8"))
    return m.group(1).strip() if m else "pendiente"


def _st(k):
    return (f"python3 tools/corrida0.py status | rg '^{k}='", lambda: _miles(_status(k)))


def _ce(k, palabra=False):
    return (f"python3 {CENSO} --clave {k}",
            lambda: _palabra(_censo(k)) if palabra else _miles(_censo(k)))


# clave -> (comando visible, función que da el texto impreso)
FUENTES = {
    "N_corridas_selladas": _st("N_corridas_selladas"),
    "celdas_validadas_prospectiva": _st("celdas_validadas_prospectiva"),
    "reports_medibles": ("python3 tools/readme_derivado.py --clave reports_medibles",
                         lambda: _miles(_reports_medibles())),
    "reports_total": ("rg --files corpus/reports -g '*.md' | wc -l", lambda: _miles(len(_reports()))),
    "n_evaluaciones": _ce("n_evaluaciones", palabra=True),
    "n_instrumentos": _ce("n_instrumentos", palabra=True),
    "n_celdas_total": _ce("n_celdas_total"),
    "doi": ("rg '^doi:' CITATION.cff", _doi),
}

# Badges: solo claves que el job guardias no mueve (ver docstring).
BADGE_CLAVES = {
    "evaluaciones": ("evaluaciones prospectivas", "n_evaluaciones"),
    "instrumentos": ("instrumentos oficiales", "n_instrumentos"),
    "celdas": ("celdas evaluadas", "n_celdas_total"),
    "reports": ("reports de evidencia", "reports_total"),
}
COLOR = "2b6cb0"


def valor(clave: str) -> str:
    if clave not in _CACHE:
        _CACHE[clave] = FUENTES[clave][1]()
    return _CACHE[clave]


def _numero(clave: str) -> str:
    """Badges en dígitos aunque el README use la palabra."""
    if clave == "reports_total":
        return str(len(_reports()))
    return str(_censo(clave))


def badges() -> dict[str, dict]:
    return {nombre: {"schemaVersion": 1, "label": etiqueta, "message": _numero(clave), "color": COLOR}
            for nombre, (etiqueta, clave) in BADGE_CLAVES.items()}


def deriva_readme(texto: str) -> tuple[str, list[str]]:
    cambios: list[str] = []

    def sustituye(m: re.Match) -> str:
        impreso, clave, comando = m.group(1), m.group(2), m.group(3)
        if clave not in FUENTES:
            raise SystemExit(f"README cita deriva[{clave}], que no está en FUENTES")
        if comando != FUENTES[clave][0]:
            raise SystemExit(f"README deriva[{clave}] declara {comando!r}; FUENTES dice {FUENTES[clave][0]!r}")
        nuevo = valor(clave)
        if impreso != nuevo:
            cambios.append(f"{clave}: {impreso} -> {nuevo}")
        return f"**{nuevo}** <!-- deriva[{clave}]: {comando} -->"

    return MARCA.sub(sustituye, texto), cambios


VISTA_PREVIA = RAIZ / "docs" / "assets" / "social-preview.png"


def _tagline() -> str:
    m = re.search(r"(?m)^\*\*(Lo que la gente dijo[^*]+)\*\*$", README.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit("README sin tagline en negritas")
    return m.group(1)


def vista_previa() -> pathlib.Path:
    import glob
    import html
    import os
    import tempfile
    chrome = os.environ.get("CHROMIUM") or next(iter(sorted(glob.glob(
        "/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell"))), None)
    if not chrome:
        raise SystemExit("sin Chromium: exporta CHROMIUM=<ruta al binario>")
    cifras = [(_numero("n_evaluaciones"), "evaluaciones prospectivas"),
              (_numero("n_instrumentos"), "instrumentos oficiales"),
              (_numero("n_celdas_total"), "celdas de población")]
    bloques = "".join(f'<div class="c"><b>{html.escape(n)}</b><span>{html.escape(t)}</span></div>'
                      for n, t in cifras)
    pagina = f"""<!doctype html><meta charset="utf-8"><style>
html,body{{margin:0;width:1280px;height:640px;background:#0f1b2d;color:#f4f1ea;
font-family:"DejaVu Serif",Georgia,serif}}
.w{{box-sizing:border-box;width:1280px;height:640px;padding:72px 88px;display:flex;
flex-direction:column;justify-content:space-between;border-left:18px solid #c8553d}}
h1{{font-size:76px;margin:0;letter-spacing:-1px}}
p{{font-size:30px;line-height:1.35;margin:18px 0 0;color:#d9d4c7;max-width:1060px}}
.f{{display:flex;gap:72px}} .c b{{display:block;font-size:84px;color:#f2b134;font-family:"DejaVu Sans",sans-serif}}
.c span{{font-size:24px;color:#d9d4c7;font-family:"DejaVu Sans",sans-serif}}
.u{{font-size:22px;color:#9fb0c4;font-family:"DejaVu Sans Mono",monospace}}
</style><div class="w"><div><h1>Benchmark del Mexicano</h1><p>{html.escape(_tagline())}</p></div>
<div class="f">{bloques}</div><div class="u">github.com/Josanoforo/Modelado-Mexicano</div></div>"""
    VISTA_PREVIA.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        fuente = pathlib.Path(tmp) / "vista.html"
        fuente.write_text(pagina, encoding="utf-8")
        subprocess.run([chrome, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--user-data-dir={tmp}/perfil", "--window-size=1280,640",
                        f"--screenshot={VISTA_PREVIA}", fuente.as_uri()],
                       check=True, capture_output=True, timeout=120)
    return VISTA_PREVIA


def main(argv: list[str]) -> int:
    if "--vista-previa" in argv:
        print(vista_previa().relative_to(RAIZ))
        return 0
    if "--clave" in argv:
        print(valor(argv[argv.index("--clave") + 1]))
        return 0
    cambios: list[str] = []
    reescritos = {}
    for doc in DOCUMENTOS:
        texto = doc.read_text(encoding="utf-8")
        nuevo, c = deriva_readme(texto)
        cambios += [f"{doc.relative_to(RAIZ)} {x}" for x in c]
        if nuevo != texto:
            reescritos[doc] = nuevo
    esperados = badges()
    for nombre, cuerpo in esperados.items():
        ruta = BADGES / f"{nombre}.json"
        actual = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None
        if actual != cuerpo:
            cambios.append(f"badge {nombre}: {actual and actual.get('message')} -> {cuerpo['message']}")
    for c in cambios:
        print(c)
    if "--escribe" in argv:
        for doc, nuevo in reescritos.items():
            doc.write_text(nuevo, encoding="utf-8")
        BADGES.mkdir(parents=True, exist_ok=True)
        for nombre, cuerpo in esperados.items():
            (BADGES / f"{nombre}.json").write_text(
                json.dumps(cuerpo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0
    return 1 if cambios else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
