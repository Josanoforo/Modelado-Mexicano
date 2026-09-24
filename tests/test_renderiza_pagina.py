#!/usr/bin/env python3
"""Guardia de tools/renderiza_pagina.py (ACTO GEN2-ASTRA5-U5-ADQUISICION-1).

Defecto que atrapa (real, 24/sep/2026): un 200 de gob.mx con la página «Challenge
Validation» se leyó como respuesta válida en bitácoras de agentes; y el reto de Cloudflare
en español («Un momento…») no lo detectaba ningún patrón de la sesión, que sólo buscaba
«Just a moment». Sin navegador ni red: todo sobre HTML sintético con las firmas medidas.

Uso: python3 tests/test_renderiza_pagina.py   (sale 0 si todo pasa)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import renderiza_pagina as r  # noqa: E402

fallos = 0


def check(nombre, ok, detalle=""):
    global fallos
    print(f"{'PASS' if ok else 'FAIL'} · {nombre}" + (f" · {detalle}" if detalle and not ok else ""))
    fallos += 0 if ok else 1


relleno = "<p>" + "x" * 400 + "</p>"
casos = {
    "gob.mx sin JavaScript": ("<html><head><title>Challenge Validation</title></head><body><script>cp_cl()</script>" + relleno, "RETO"),
    "Cloudflare en español": ("<html><head><title>Un momento…</title></head><body>" + relleno, "RETO"),
    "Cloudflare en inglés": ("<html><head><title>Just a moment...</title></head><body>" + relleno, "RETO"),
    "Akamai por IP": ("<html><head>\n<title>Access Denied</title>\n</head><body><h1>Access Denied</h1>" + relleno, "RETO"),
    "Incapsula (IMSS)": ("<html><head><title>IMSS</title></head><body><script src='/_Incapsula_Resource'></script>" + relleno, "RETO"),
    "certificado inválido": ("<html><head><title>Error de privacidad</title></head><body>" + relleno, "RETO"),
    "página real": ("<html><head><title>Resoluciones y sanciones | COFEPRIS | gob.mx</title></head><body>"
                    "<a href='/cms/uploads/attachment/file/1/a.pdf'>a</a><a href=\"https://datos.gob.mx/\">d</a>"
                    "<a href='#top'>x</a>" + relleno, "RENDERIZADO"),
    "respuesta vacía": ("<html></html>", "VACIO"),
    "sólo scripts (DOF)": ("<html><head><title></title><script>" + "var a=1;" * 80 + "</script></head><body></body></html>", "VACIO"),
    "error DNS del navegador": ("<html><head><title>directoriosancionados.apps.funcionpublica.gob.mx</title></head>"
                                "<body class=\"neterror\"><div id=\"main-frame-error\">No se puede acceder</div>"
                                "<div>ERR_NAME_NOT_RESOLVED</div>" + relleno, "ERROR-RED:ERR_NAME_NOT_RESOLVED"),
}
for nombre, (html, esperado) in casos.items():
    got = r.clasifica(html)
    check(f"clasifica · {nombre} -> {esperado}", got == esperado, got)

# mención de la palabra en el cuerpo de una página real no la vuelve reto
real = "<html><head><title>Nota</title></head><body>El sitio dijo: un momento, por favor." + relleno
check("clasifica · «un momento» en el cuerpo no es reto", r.clasifica(real) == "RENDERIZADO")

pag = casos["página real"][0]
enl = r.extrae_enlaces(pag, "https://www.gob.mx/cofepris/acciones-y-programas/resoluciones-y-sanciones")
check("extrae_enlaces · resuelve relativos y descarta anclas",
      enl == ["https://www.gob.mx/cms/uploads/attachment/file/1/a.pdf", "https://datos.gob.mx/"], str(enl))
check("extrae_enlaces · filtro por regex",
      r.extrae_enlaces(pag, "https://www.gob.mx/x", r"\.pdf$") == ["https://www.gob.mx/cms/uploads/attachment/file/1/a.pdf"])
check("titulo · desescapa y recorta", r.titulo("<title> A &amp; B \n </title>") == "A & B")
check("localiza_navegador · None si no hay candidatos", r.localiza_navegador(("/no/existe",)) is None)

antes = {"viejo.pdf": (10, 1.0), "tocado.csv": (5, 1.0)}
despues = {"viejo.pdf": (10, 1.0), "tocado.csv": (7, 2.0), "nuevo.xlsx": (358284, 3.0),
           "parcial.xlsx.crdownload": (100, 3.0), ".oculto": (1, 3.0)}
check("archivos_nuevos · detecta nuevos y cambiados, ignora .crdownload y ocultos",
      r.archivos_nuevos(antes, despues) == ["nuevo.xlsx", "tocado.csv"], str(r.archivos_nuevos(antes, despues)))
check("archivos_nuevos · sin cambios no hay nuevos", r.archivos_nuevos(antes, dict(antes)) == [])

print(f"{'VERDE' if not fallos else 'ROJO'} · {fallos} fallo(s)")
sys.exit(1 if fallos else 0)
