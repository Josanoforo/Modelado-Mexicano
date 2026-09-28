#!/usr/bin/env python3
"""Produce la tabla de afirmaciones de humor desde juicios editoriales explícitos."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "canon/mapa-dominios-v1_1.tsv"
OUT = Path(__file__).with_name("tabla-afirmaciones.tsv")
REPORT = "corpus/reports/Humor_in_Mexican_Psychological_Life__2023-2026_Update.md"

# Cada entrada conserva una decisión de contenido, no deduce el juicio del mapa.
# Las referencias F están desarrolladas en fuentes.md.
DECISIONS = {
"001": ("CONFIRMA", "Nivel WHR 2025 publicado; mide evaluación vital, no humor.", "F3"),
"002": ("CONFIRMA", "Nivel WHR 2024 publicado para otra ventana trianual.", "F3"),
"003": ("MATIZA", "Dos niveles publicados; ventanas superpuestas, sin prueba de cambio ni de humor.", "F3"),
"004": ("MATIZA", "Satisfacción regional de vida; no se transporta a México ni a humor.", "F5"),
"005": ("MATIZA", "Reactivo mexicano de vida ajeno al humor; cifra externa pendiente de cotejo puntual.", "F5"),
"006": ("MATIZA", "Satisfacción democrática es otro reactivo; comparación temporal no estima humor.", "F5"),
"007": ("MATIZA", "Identidades de redes de DataReportal no equivalen a personas únicas ni a humor.", "F4"),
"008": ("MATIZA", "EHV: 550+830=1380, no 1380+550; propiedades de muestra no prevalencia.", "F1"),
"009": ("MATIZA", "ESSH exploratoria con 185; sus coeficientes no pertenecen a escala final.", "F2"),
"010": ("CONFIRMA", "ESSH final de nueve reactivos en muestra AFC de 302; solo validez de muestra.", "F2"),
"011": ("MATIZA", "Invarianza estricta no acreditada sin reservas; tablas ambiguas.", "F1,F2"),
"012": ("SIN-CIFRA", "Validación HSQ histórica precisa artículo primario para sus coeficientes.", "mapa"),
"013": ("SIN-CIFRA", "Ausencia universal de validación nueva no se demuestra sin búsqueda reproducible.", "mapa"),
"014": ("SIN-CIFRA", "Ausencia de reaplicación clínica no demuestra falta universal de estudios.", "mapa"),
"015": ("MATIZA", "Batería de afrontamiento no identifica efecto específico ni causal del humor.", "mapa"),
"016": ("MATIZA", "Asociación en parejas reclutadas no predice causalmente relaciones mexicanas.", "mapa"),
"017": ("SIN-CIFRA", "WHR no mide uso de humor ni identifica mecanismo familiar; la hipótesis requiere datos pareados.", "F3,F7"),
"018": ("SIN-CIFRA", "Porcentajes de plataformas requieren fuente, periodo y denominadores propios.", "mapa"),
"019": ("SIN-CIFRA", "Horas de TikTok carecen de métrica primaria y base mexicana identificadas.", "mapa"),
"020": ("MATIZA", "Redes son un canal posible; identidades digitales no prueban difusión ni eficacia del humor.", "F4"),
"021": ("MATIZA", "Análisis de diez memes de Chilpancingo: interpretación local, no frecuencia.", "F6"),
"022": ("SIN-CIFRA", "Ejemplos de eventos no cuantifican respuesta nacional ni catarsis.", "mapa"),
"023": ("SIN-CIFRA", "Conteo de hashtag y desplazamiento por IA sin captura ni prueba causal.", "mapa"),
"024": ("SIN-CIFRA", "Incidente y ejemplos de artistas no establecen tendencia ni prevalencia.", "mapa"),
"025": ("SIN-CIFRA", "Testimonios de caricaturistas no estiman censura sectorial.", "mapa"),
"026": ("SIN-CIFRA", "Vacío de estudios laborales exige búsqueda reproducible.", "mapa"),
"027": ("SIN-CIFRA", "Atenciones de salud mental no tienen vínculo observado con humor.", "mapa"),
"028": ("SIN-CIFRA", "Carga modelada GBD no mide humor ni mecanismo paliativo.", "mapa"),
"029": ("SIN-CIFRA", "Autopercepción AXA/Ipsos tiene universo distinto y no mide humor.", "mapa"),
"030": ("SIN-CIFRA", "Coexistencia de indicadores de salud no identifica paliación o negación por humor; falta medición conjunta.", "mapa"),
"032": ("SIN-CIFRA", "Tesis de albur pendiente de lectura primaria; no prevalencia nacional.", "mapa"),
"033": ("SIN-CIFRA", "Ponencia individual no prueba eficacia ni prevalencia de comedia feminista.", "mapa"),
"034": ("MATIZA", "Recomendaciones editoriales se revisan según alcance de cada fuente.", "F1-F7"),
"035": ("MATIZA", "WHR 2026 mantiene México top 20, pero rango no debe disparar regla sobre humor.", "F7"),
}

with SOURCE.open(newline="") as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if r["report"] == REPORT]
assert len(rows) == len(DECISIONS) == 34
assert {r["id_afirmacion"][-3:] for r in rows} == set(DECISIONS)
with OUT.open("w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["id", "id_mapa", "afirmacion_original", "localizador_v1", "dictamen", "razon", "evidencia", "result_propio", "razon_sin_result"])
    for r in rows:
        suffix = r["id_afirmacion"][-3:]
        verdict, reason, evidence = DECISIONS[suffix]
        w.writerow([r["id_afirmacion"], r["id_afirmacion"], r["texto_vigente"], r["localizador"], verdict, reason, evidence, "NINGUNO", "No hay RESULT propio de humor aplicable; fuente externa o afirmación no instrumentada."])
    w.writerow(["RES-HUM-031", "", "Latinobarómetro: apoyo a la democracia en México, 49% en 2024 frente a 35% en 2023, ligado en el original al humor político.", "L49", "MATIZA", "Apoyo democrático es un reactivo político distinto del humor; los puntos requieren cotejo con sus olas y no identifican un efecto de sátira.", "F5", "NINGUNO", "Sin RESULT propio de apoyo o humor en este report."])
print(f"{len(rows)} filas de mapa + 1 residual -> {OUT}")
