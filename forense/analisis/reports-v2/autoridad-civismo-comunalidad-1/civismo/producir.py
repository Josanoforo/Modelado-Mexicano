"""Materializa el dictamen editorial explícito del reporte cívico.

No infiere un juicio desde el dictamen heredado ni desde un rango de líneas.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
ORIGINAL = "Psicología_Política_y_Comportamiento_Cívico_del_Mexicano_Contemporáneo__Una_Lectura_Anti-Esencialista_desde_Abajo__2026_.md"

# id numérico: juicio, razón concreta, soporte. Externo identifica una fuente
# primaria en fuentes.md; GEN2 identifica un RESULT consultable.
D = {
1:("MATIZA","La escala registra confianza declarada, no desempeño ni calibración causal.","ENCIG25; ENCUCI20"),
2:("MATIZA","La cifra negra incluye delitos denunciados sin carpeta; motivos declarados no identifican utilidad esperada.","ENVIPE25"),
3:("CONFIRMA","La gradación declarada corresponde al universo urbano de ENCIG; no es confianza nacional homogénea.","ENCIG25"),
4:("MATIZA","La comparación entre olas requiere la misma categoría y error de muestreo; no infiere una caída causal.","ENCIG25"),
5:("MATIZA","ENVIPE pregunta confianza en autoridad de seguridad con otra escala que ENCIG.","ENVIPE25"),
6:("CONFIRMA","El boletín oficial identifica año de ocurrencia, delitos estimados y denuncia.","ENVIPE25"),
7:("CONFIRMA","Son razones declaradas entre no denunciantes; no una función de utilidad estimada.","ENVIPE25"),
8:("MATIZA","El denominador de carpetas difiere del total de delitos; no combinar proporciones sin cadena de filtros.","ENVIPE25"),
9:("MATIZA","Estimación agregada de costos; no prueba el costo individual de denunciar.","ENVIPE25"),
10:("MATIZA","El 59.8% es estimación muestral INE; el cómputo presidencial marca 61.04%. Son productos con método/denominador distintos.","INE24-MUESTRA; INE24-COMPUTO"),
11:("SIN-CIFRA","No se observa percepción individual del peso del acto ni panel que una elecciones.","INE24-MUESTRA; INE25-JUDICIAL"),
12:("CONFIRMA","El estudio muestral INE separa sexo y edad; no implica una causa de la brecha.","INE24-MUESTRA"),
13:("MATIZA","El resultado geográfico oficial no acredita transversalidad por clase ni ausencia de clivajes.","INE24-COMPUTO"),
14:("SIN-CIFRA","Provisión, identidad y autoritarismo exigen constructos y estrategia de identificación conjunta.","ENCUCI20"),
15:("SIN-CIFRA","Serie de termómetros no verificada aquí con estimando y muestras constantes.","LITERATURA-HISTORICA"),
16:("SIN-CIFRA","Índice comparado publicado no equivale a una medición local replicada en este carril.","LITERATURA-HISTORICA"),
17:("SIN-CIFRA","Tesis sobre eje 4T y moderación depende de operacionalización; sin microdato comparable.","LITERATURA-HISTORICA"),
18:("ROMPE","Sólo la cláusula universal sin broker contradice investigación mexicana 2025 y FP-57.","LANGSTON25; FP-57"),
19:("SIN-CIFRA","Presupuesto, cobertura y condicionalidad son objetos distintos; no se reprodujo la fuente presupuestaria.","RESTRICCION-DOCUMENTAL"),
20:("MATIZA","Brecha entre beneficiarios y no beneficiarios es asociación con selección, no efecto del programa.","ENCUCI20"),
21:("MATIZA","Prevalencia urbana de corrupción documenta experiencia; el cálculo de cada pago no está identificado.","ENCIG23"),
22:("MATIZA","Percepción de frecuencia es distinta de victimización y no prueba una trampa social.","ENCIG25"),
23:("MATIZA","Tasas por habitantes y prevalencia entre usuarios de trámites tienen denominadores distintos.","ENCIG23; ENCIG25"),
24:("SIN-CIFRA","Un índice de percepción externo no mide experiencia personal de soborno.","TI24"),
25:("SIN-CIFRA","El conteo y su cobertura no fueron contrastados con base primaria; no atribuir motivo a los participantes.","ADQUISICION-PENDIENTE"),
26:("MATIZA","Institucionalidad comunitaria y linchamiento son organizaciones distintas; falta comparar comunidades y periodos.","RESTRICCION-DOCUMENTAL"),
27:("SIN-CIFRA","No hay denominador nacional ni muestra de todas las modalidades de protesta para jerarquizarlas.","INSTRUMENTO-INADECUADO"),
28:("SIN-CIFRA","Un registro acumulado con cortes móviles no mide directamente actividad ni composición de colectivos.","RESTRICCION-DOCUMENTAL"),
29:("SIN-CIFRA","Fragilidad es propiedad temporal/individual no identificable en dos cortes agregados.","LB24"),
30:("CONFIRMA","El informe Latinobarómetro registra la diferencia declarada entre cortes; no su causa.","LB24"),
31:("SIN-CIFRA","La victoria oficialista coincide con el cambio agregado, sin identificar efecto electoral.","LB24"),
32:("SIN-CIFRA","Ansiedad de estatus y conducta antisistema no se contrastaron conjuntamente.","INSTRUMENTO-INADECUADO"),
33:("SIN-CIFRA","Clasificación nacional dignidad/honor/face carece de medición mexicana representativa comparable.","MARCO-IMPORTADO"),
34:("SIN-CIFRA","Una elección no identifica efecto de provisión ni competitividad sobre participación.","INE24-COMPUTO"),
35:("SIN-CIFRA","Complejidad de boletas y percepción del resultado no se ligaron individualmente a abstención.","INE25-JUDICIAL"),
36:("ROMPE","Sólo la premisa causal de ausencia universal de broker es falsa; FP-57 la retiró.","LANGSTON25; FP-57"),
37:("SIN-CIFRA","El instrumento mide corrupción en trámites, no el contrafactual de funcionario sin registro.","ENCIG23"),
38:("MATIZA","La asociación entre seguro y denuncia depende de delito/selección; no identifica miedo.","RESULT-ENVIPE-SEG-CON-P-DENUNCIA; RESULT-ENVIPE-SEG-SIN-P-DENUNCIA"),
39:("SIN-CIFRA","No hay seguimiento de comunidades comparable que mida emergencia de autodefensa.","ADQUISICION-PENDIENTE"),
40:("SIN-CIFRA","Norma percibida, riesgo de sanción y evasión no se midieron conjuntamente.","INSTRUMENTO-INADECUADO"),
41:("CONFIRMA","Percepción de inseguridad es opinión de adultos, no delito observado.","ENVIPE25"),
42:("SIN-CIFRA","Rangos de casas encuestadoras no constituyen serie comparable sin diseño/campo.","NO-COMPARABILIDAD"),
"TRUST-002":("MATIZA","Confianza en conocidos y desconocidos exige reactivos/umbrales de una escala común.","ENCUCI20"),
}

# Cláusulas de filas compuestas. Mantienen la identidad de la fila matriz pero
# reciben su propio juicio para no convertir falta de dato en refutación.
EXTRA = [
    ("ASTRA5-U0-POL-010-JUD", "L18;L117", "12.86% en elección judicial 2025 como contraste de participación", "SIN-CIFRA", "Faltan cargo, acta y corte de la cifra judicial del v1; la búsqueda documental no la reconstruyó.", "INE25-JUDICIAL"),
    ("ASTRA5-U0-POL-018-AGENCIA", "L26;L153", "Aceptar bien y votar con autonomía", "SIN-CIFRA", "Secreto formal y posibilidad de voto autónomo no miden conducta efectiva ni percepción de secreto.", "BALLOT25; ENCUCI20"),
    ("ASTRA5-U0-POL-036-AGENCIA", "L262", "Transferencia vivida como derecho/gratitud y autonomía de voto", "SIN-CIFRA", "No se identifican juntos percepción de derecho, gratitud y voto individual.", "ENCUCI20; BALLOT25"),
    ("EXTRA-CIV-01", "L22;L129", "31 entidades ganadas implica ausencia de clivaje", "MATIZA", "Resultado estatal no prueba ausencia de división intrastatal o por clase.", "INE24-COMPUTO"),
    ("EXTRA-CIV-02", "L24;L145", "Polarización mexicana menor que estadounidense", "SIN-CIFRA", "Índices, poblaciones, años y objeto líder/partido no son comparables aquí.", "POLARIZACION"),
    ("EXTRA-CIV-03", "L85-L89", "Confianza mayor se debe a menor contacto extractivo", "SIN-CIFRA", "No se observó exposición y cambio de desempeño en la comparación invocada.", "ENCIG25"),
    ("EXTRA-CIV-04", "L103", "Motivos de no denuncia difieren por sexo", "SIN-CIFRA", "No se ejecutó contraste por sexo con incertidumbre de diseño.", "ENVIPE25"),
    ("EXTRA-CIV-05", "L117", "Boletas complejas y resultado percibido como decidido causan abstención", "SIN-CIFRA", "El agregado de votos no contiene percepciones previas de abstencionistas.", "INE25-JUDICIAL"),
    ("EXTRA-CIV-06", "L133", "Seguridad se evalúa mal aun entre quienes aprueban presidenta", "SIN-CIFRA", "No se cotejó microdato conjunto y fecha de campo de la casa encuestadora.", "NO-COMPARABILIDAD"),
    ("EXTRA-CIV-07", "L145", "México, EE. UU. y Perú tienen ratio líder/partido mayor que uno", "SIN-CIFRA", "Índice comparado histórico no recalculado con umbral común.", "POLARIZACION"),
    ("EXTRA-CIV-08", "L159", "Universalidad de pensión implica inexistencia de intermediación", "ROMPE", "Langston 2025 documenta intermediación de inscripción y comunicación, aunque no monitoreo individual.", "LANGSTON25; FP-57"),
    ("EXTRA-CIV-09", "L181", "Linchamientos crecen con criminalidad e impunidad", "SIN-CIFRA", "Faltan base primaria, cobertura y panel municipal para asociación temporal.", "ADQUISICION-PENDIENTE"),
    ("EXTRA-CIV-10", "L195", "8M y búsqueda son formas más vitales de acción cívica", "SIN-CIFRA", "No existe denominador común nacional de participación en todas las modalidades.", "INSTRUMENTO-INADECUADO"),
    ("EXTRA-CIV-11", "L208", "Informalidad equivale a evasión de subsistencia", "ROMPE", "Categoría laboral y evasión individual son variables distintas; equivalencia conceptual inválida.", "ENOE-DEFINICION"),
    ("EXTRA-CIV-12", "L214;L216", "Generación y religión determinan conducta cívica", "SIN-CIFRA", "No se midieron interacciones ni separaron edad, cohorte y periodo.", "INSTRUMENTO-INADECUADO"),
    ("EXTRA-CIV-13", "L224", "Policía comunitaria es distintivamente mexicana", "SIN-CIFRA", "Falta tipología internacional con definición comparable.", "COMPARACION-PENDIENTE"),
    ("EXTRA-CIV-14", "L236", "Colectivos son actores más legítimos y efectivos", "SIN-CIFRA", "Legitimidad y efectividad requieren actor evaluador y desenlace definidos.", "INSTRUMENTO-INADECUADO"),
]

def main() -> None:
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open() as f:
        rows = [r for r in csv.DictReader(f, delimiter="\t") if ORIGINAL in r["report"]]
    assert len(rows) == 43
    assert len(D) == len(rows)
    out = HERE / "afirmaciones.tsv"
    with out.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(("id_afirmacion","localizador_v1","afirmacion_original","juicio_v2","razon_especifica","evidencia","dictamen_mapa_historico"))
        for r in rows:
            key = "TRUST-002" if r["id_afirmacion"].endswith("TRUST-002") else int(r["id_afirmacion"].split("-")[-1])
            juicio, razon, evidencia = D[key]
            w.writerow((r["id_afirmacion"],r["localizador"],r["texto_vigente"],juicio,razon,evidencia,r["dictamen"]))
        for ident, loc, afirmacion, juicio, razon, evidencia in EXTRA:
            w.writerow((ident,loc,afirmacion,juicio,razon,evidencia,"DESDOBLE-EDITORIAL"))
    counts = Counter(x[0] for x in D.values()) + Counter(x[3] for x in EXTRA)
    report = f"corpus/reports-v2/{ORIGINAL}"
    summary = {
        "report": report,
        "registros": len(rows) + len(EXTRA),
        "mapa_filas": len(rows),
        "dictamenes": {k: counts[k] for k in ("CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA")},
        "cifras": ["RESULT-ENVIPE-SEG-CON-P-DENUNCIA", "RESULT-ENVIPE-SEG-SIN-P-DENUNCIA"],
        "generar": "python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/civismo/producir.py",
        "verificar": "python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/civismo/verificar.py",
    }
    (HERE / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(rows)} afirmaciones del mapa y {len(EXTRA)} desdobles; tabla={out}")

if __name__ == "__main__":
    main()
