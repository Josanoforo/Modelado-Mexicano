#!/usr/bin/env python3
"""Genera el deck de diez láminas (docs/deck/*.md + docs/deck.pptx) desde
una única fuente en este archivo (SLIDES). Una lámina = una idea; cifras
citadas, no fabricadas, con la misma fuente que el one-pager y el reto.

ACTO GEN2-FRONT-2 §1 P2. Requiere `python-pptx` para el .pptx
(`pip install --break-system-packages python-pptx`); si no está, el HTML
para Pages se escribe igual y el .pptx se omite con aviso.

Uso: python3 tools/genera_deck.py
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DECK_DIR = ROOT / "docs/deck"
PPTX_SALIDA = ROOT / "docs/deck.pptx"

SLIDES = [
    {
        "slug": "01-tesis",
        "titulo": "Tesis",
        "bullets": [
            "Lo que la gente dijo en la última encuesta oficial de México, por segmento, con intervalo — y la prueba pública de si un modelo la predice mejor que repetir la ola anterior.",
            "246 corridas selladas · 66 582 RESULT GEN2 sellados · 72 RESULT GEN2 adoptados activos (el piso que se publica).",
            "Los retadores evaluados no superaron los criterios de superioridad fijados en las comparaciones citadas. Esto no declara equivalencia ni se extiende a modelos nunca evaluados.",
        ],
    },
    {
        "slug": "02-seis-evaluaciones",
        "titulo": "Seis evaluaciones",
        "bullets": [
            "Piloto ahorro, localidad × edad (ENIF 2024) — `SIN-CANDIDATO-SUPERIOR`.",
            "Piloto evasión, escolaridad × dominio (ENVIPE 2025) — `SIN-CANDIDATO-SUPERIOR`.",
            "Piloto gobierno digital, edad × escolaridad (ENCIG 2025) — `FALSADOR-DÉBIL`: 3/15 celdas a favor del retador, ΔMAE 1.465 pp IC95 [0.439, 2.115] — el IC no despeja el umbral de 0.5 pp fijado antes de abrir el dato.",
            "Lote de interacción, 44 celdas puntuadas (ENIF 2024) — `PROPUESTA-CON-RESERVA`.",
            "Duelo de ola nueva (ENVIPE 2026) — `NADIE-VENCE` en ambos cruces.",
            "Duelo de candidatos (ENCIG 2025) — `FALSADOR-DÉBIL` agregado.",
        ],
    },
    {
        "slug": "03-corroboracion-externa",
        "titulo": "Corroboración externa (fuera de México)",
        "bullets": [
            "Corea, Korea Media Panel Survey de KISDI (Kim y Cho, arXiv:2608.28615, jul/2026): sobre seis indicadores comunes, persistir la ola previa erró 3.7 pp frente a 7.0–7.5 pp de los paneles sintéticos ya calibrados. La corrección no se trasladó entre olas.",
            "Tres países, seis baterías multirrespuesta (Doudkin, arXiv:2609.07305, sep/2026): recitar la tabla nacional (piso descriptivo) erró 4.85 pp frente a 6.08–12.14 pp de los modelos por celda.",
            "Ninguno de los dos estudios usa un instrumento mexicano ni nuestras unidades (delito, trámite, hogar): es corroboración del método — la persistencia como piso difícil de vencer — no evidencia sobre México.",
        ],
    },
    {
        "slug": "04-catalogo",
        "titulo": "Qué cubre el corpus y el catálogo",
        "bullets": [
            "31 reports temáticos de evidencia en el corpus — documentos, no dominios mutuamente excluyentes.",
            "Catálogo v1.0: 1 537 filas de estimando/segmento/ola en 5 áreas de consulta; la mayoría es piso histórico de contexto o propuesta sin adopción.",
            "72 filas adoptadas (`ADOPTADO-POR-FIRMA` + `CONSUMO-GEN2-ACTIVO`) en 4 de 5 áreas: dinero y crédito (27), trámites y Estado (22), tiempo/cuidado y vínculos (13), seguridad y norma (10). Ingreso y gasto está sellado como contexto, sin fila adoptada todavía.",
            "ENDIREH e INE/ENCUP siguen en medición; no se presentan como medición publicada.",
        ],
    },
    {
        "slug": "05-segmentacion-y-clase",
        "titulo": "Segmentación y clase",
        "bullets": [
            "No tratamos a los mexicanos como bloque homogéneo: toda cifra se segmenta por región, clase, edad, género, escolaridad, urbanización, religiosidad, migración y exposición global.",
            "El sesgo que más muerde es de clase dentro de la modernidad — sobre-muestreo del clasemediero urbano formal — y se declara al lado de cada cifra, no se esconde.",
            "El sistema indígena-comunal vivo es otro orden institucional: queda fuera por diseño. La huella indígena difusa sí se mapea.",
        ],
    },
    {
        "slug": "06-donde-ganan-los-otros",
        "titulo": "Dónde ganan los otros",
        "bullets": [
            "Informe de competencia propio (23/sep/2026, 33 actores revisados): nadie publica para México las tres propiedades juntas — validación prospectiva sellada, cobertura de intervalo medida y persistencia como piso de comparación.",
            "YouGov Parallax gana en alcance: responde cualquier pregunta nueva con un panel de 30M+ y entrega en 30 minutos. Le falta sellar predicciones antes de la ola; valida contra humanos en vivo, no ex ante.",
            "Gallup–Simile gana en capital y pedigrí (Serie B, US$200M): panel probabilístico y validador institucional. Le falta publicar resultados; es solo EE. UU. y no es prospectivo por olas.",
            "Matria AI (Celestial Dynamics) gana en granularidad geográfica (manzana/AGEB con INEGI/DENUE + NSE AMAI) y producto comercial vivo. Le falta toda validación conductual publicada.",
        ],
    },
    {
        "slug": "07-sellado-y-verificacion",
        "titulo": "Sellado y verificación",
        "bullets": [
            "Cada RESULT tiene su CALC: `spec.yaml`, `resultados.json`, `sello.json` con hash — verificable con `sha256sum` sin abrir microdato.",
            "344 sellos en el manifiesto externo, con testigo de tiempo: OpenTimestamps o TSA cuando hay egress; firma GPG del merge y tag de mesa cuando la sesión no tuvo salida a red — demuestra existencia-antes-de, no autoría.",
            "La validación independiente recalcula desde la spec humana, el cuestionario y el descriptor, sin leer el código que produjo la cifra, y commitea sus números antes de abrir los sellados.",
        ],
    },
    {
        "slug": "08-reto-publico",
        "titulo": "Reto público",
        "bullets": [
            "La tabla de piso publica 72 filas adoptadas — la línea que un retador tiene que vencer, derivada del catálogo por comando, no editada a mano.",
            "Regla: diferencia de error medio (ΔMAE) con IC por réplica, umbral fijado antes de abrir el dato. Vence si el IC despeja el umbral; propuesta con reserva si despeja 0 y no el umbral; nadie vence si incluye 0.",
            "Se entrega con spec pre-registrada por PR, antes de que exista el árbitro de la ola. Se invita por escrito a Toluna, ThinkNow, Matria/Celestial y YouGov; cualquier equipo puede participar por la misma vía.",
            "Sin promesas de adopción: el reto mide, mesa decide.",
        ],
    },
    {
        "slug": "09-que-viene",
        "titulo": "Qué viene",
        "bullets": [
            "ENDIREH (unidad ASTRA-5 U2) cerrado el 24/sep/2026; INE/ENCUP y el resto de la hoja ASTRA-5 (768 afirmaciones con adquisición identificada) siguen en medición.",
            "DOI vía Zenodo y activación de GitHub Pages: decisión de mesa, pendiente en este corte.",
            "Primeras entregas del reto público, conforme lleguen los PR con spec pre-registrada.",
        ],
    },
    {
        "slug": "10-contacto",
        "titulo": "Licencia, cita y contacto",
        "bullets": [
            "LICENSE: MIT para el código, CC BY-NC-SA 4.0 para corpus y documentación, con excepciones expresas para ciertos usos comerciales del corpus.",
            "Uso comercial fuera de esas excepciones: escribe a jonieqsa@gmail.com.",
            "Cita con CITATION.cff. DOI: pendiente (Zenodo, activación de mesa).",
            "one-pager · docs/verificar.md · docs/reto.md",
        ],
    },
]

FRONT_MATTER = "---\ntitle: \"{titulo}\"\n---\n"


def slugificar_link(slug: str) -> str:
    return slug + ".html"


def escribe_html_slides() -> None:
    DECK_DIR.mkdir(parents=True, exist_ok=True)
    n = len(SLIDES)
    indice_lineas = [
        "---\ntitle: Deck\n---\n",
        "# Deck: diez láminas\n",
        "[Portada]({{ '/' | relative_url }}) · [One-pager]({{ '/one-pager.html' | relative_url }})\n",
        "Una lámina, una idea. Cifras derivadas del mismo corte que el one-pager y el reto; comando en `tools/genera_deck.py` y en la nota de cierre del acto.\n",
    ]
    for i, slide in enumerate(SLIDES):
        indice_lineas.append(f"{i + 1}. [{slide['titulo']}]({{{{ '/deck/{slide['slug']}.html' | relative_url }}}})")
        lineas = [FRONT_MATTER.format(titulo=slide["titulo"])]
        lineas.append(f"# {i + 1}/{n} · {slide['titulo']}\n")
        lineas.append("[Deck]({{ '/deck.html' | relative_url }}) · [Portada]({{ '/' | relative_url }})\n")
        for b in slide["bullets"]:
            lineas.append(f"- {b}")
        lineas.append("")
        nav = []
        if i > 0:
            nav.append(f"[← anterior]({{{{ '/deck/{SLIDES[i - 1]['slug']}.html' | relative_url }}}})")
        if i < n - 1:
            nav.append(f"[siguiente →]({{{{ '/deck/{SLIDES[i + 1]['slug']}.html' | relative_url }}}})")
        if nav:
            lineas.append(" · ".join(nav))
        (DECK_DIR / f"{slide['slug']}.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (ROOT / "docs/deck.md").write_text("\n".join(indice_lineas) + "\n", encoding="utf-8")


def quita_markdown(texto: str) -> str:
    texto = re.sub(r"`([^`]+)`", r"\1", texto)
    texto = re.sub(r"\*\*([^*]+)\*\*", r"\1", texto)
    return texto


def escribe_pptx() -> bool:
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
    except ImportError:
        print("python-pptx no instalado: se omite docs/deck.pptx (HTML de Pages queda como vía principal)")
        return False

    prs = Presentation()
    layout_titulo = prs.slide_layouts[0]
    layout_contenido = prs.slide_layouts[1]

    portada = prs.slides.add_slide(layout_titulo)
    portada.shapes.title.text = "Benchmark del Mexicano"
    portada.placeholders[1].text = "Modelado Mexicano · Psicología del Mexicano Contemporáneo"

    for i, slide in enumerate(SLIDES):
        s = prs.slides.add_slide(layout_contenido)
        s.shapes.title.text = f"{i + 1}/{len(SLIDES)} · {slide['titulo']}"
        cuerpo = s.placeholders[1].text_frame
        cuerpo.word_wrap = True
        for j, b in enumerate(slide["bullets"]):
            p = cuerpo.paragraphs[0] if j == 0 else cuerpo.add_paragraph()
            p.text = quita_markdown(b)
            p.font.size = Pt(16)

    prs.save(str(PPTX_SALIDA))
    return True


def main() -> None:
    escribe_html_slides()
    print(f"escritas {len(SLIDES)} láminas en {DECK_DIR.relative_to(ROOT)}/ y docs/deck.md")
    if escribe_pptx():
        print(f"escrito: {PPTX_SALIDA.relative_to(ROOT)} ({PPTX_SALIDA.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
