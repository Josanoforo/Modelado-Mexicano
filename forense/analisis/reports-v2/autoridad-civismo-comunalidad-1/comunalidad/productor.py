"""Produce la matriz rural desde decisiones editoriales explícitas y mapa vigente."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent / "tabla-afirmaciones.tsv"
MAP = ROOT / "canon/mapa-dominios-v1_1.tsv"

# Clave: sufijo del id. Estado, razón concreta, fuente. No se hereda el dictamen del mapa.
D = {
1:("MATIZA","Modelo situado de autores ayuujk y zapotecos; interdependencia universal sin contraste","DIAZ"),
2:("SIN-CIFRA","ENUT pregunta servicio comunitario combinado; falta RESULT específico y no separa tequio","ENUT"),
3:("MATIZA","Cargo y servicio existen en casos, pero remuneración, rotación y acceso varían","CHANCE"),
4:("MATIZA","Portal IEEPCO vigente indica 418 municipios SNI; 417 es dato de otro periodo, no error demostrado del original","IEEPCO"),
5:("MATIZA","Sentencia acredita derecho y consulta, no aquí votos exactos o participación efectiva","TEPJF"),
6:("MATIZA","Asamblea formal no demuestra consenso, soberanía efectiva ni inclusión","IEEPCO"),
7:("MATIZA","Prácticas documentadas; seguro y protección universal requieren seguimiento de transferencias","DIAZ"),
8:("CONFIRMA","Catálogos y dictámenes describen reglas internas de elección; contenido varía por municipio","IEEPCO"),
9:("SIN-CIFRA","Dato RAN histórico sin verificación de serie y denominador actualizado en esta pieza","RAN"),
10:("MATIZA","Régimen agrario y participación institucional se relacionan pero no son identidad","RAN"),
11:("SIN-CIFRA","Conteo histórico de clubes y remesas sin fuente primaria localizada y periodo comparable","SIN-FUENTE"),
12:("MATIZA","La translocalidad es caso etnográfico, no efecto promedio de migrar","STEPHEN"),
13:("MATIZA","El norte contiene instituciones heterogéneas; no equivale a dispersión o rechazo general","SIN-FUENTE"),
14:("SIN-CIFRA","Mecanismo defensivo plausible sin comparación que identifique despojo frente a otras causas","TEPJF"),
15:("MATIZA","Comunalidad es elaboración intelectual situada; cronología del buen vivir requiere otra fuente","DIAZ"),
16:("CONFIRMA","Archivos de cuatro regiones sitúan jerarquía cívico-religiosa combinada sobre todo tras independencia","CHANCE"),
17:("CONFIRMA","Conflictos y exclusiones documentados invalidan armonía como supuesto","IEEPCO"),
18:("SIN-CIFRA","Aproximación EDUCA de ausencia de conflicto no equivale a incidencia observada","IEEPCO"),
19:("SIN-CIFRA","Recuento histórico de expulsiones no localizado en fuente primaria","SIN-FUENTE"),
20:("SIN-CIFRA","ENDIREH contiene ítem prenatal, sin RESULT aplicable ni identidad con medicina propia","SIN-RESULT"),
21:("MATIZA","Coexistencia en casos; prevalencia y equivalencia clínica no medidas aquí","SIN-RESULT"),
22:("SIN-CIFRA","Articulación respetuosa es pauta normativa, eficacia no identificada","SIN-RESULT"),
23:("SIN-CIFRA","Pobreza y erosión plausibles; no se estima efecto sobre redes","SIN-RESULT"),
24:("SIN-CIFRA","No hay evaluación causal de transferencia individual y tequio","SIN-RESULT"),
25:("MATIZA","Analogía heurística andina, no equivalencia de instituciones ni poblaciones","SIN-FUENTE"),
26:("SIN-CIFRA","Censo citado mezcla universos de autoadscripción y lengua; sin RESULT propio utilizable","INEGI"),
27:("SIN-CIFRA","Monolingüismo necesita universo y tabla censal precisos; no inferir motivo","INEGI"),
28:("SIN-CIFRA","Analfabetismo por hablante no atribuye déficit psicológico; cifra no revalidada","INEGI"),
29:("SIN-CIFRA","Serie CONEVAL histórica no sustituye cruce indígena-persona verificado","SIN-FUENTE"),
30:("MATIZA","Las tasas estatales históricas requieren cotejo CONEVAL; son estimandos de entidad, no de identidad indígena","SIN-FUENTE"),
31:("SIN-CIFRA","Evangelización y cargos requieren comunidad y periodo antes/después","SIN-RESULT"),
32:("SIN-CIFRA","Casos cooperativos históricos sin padrón y periodo primario verificados","SIN-FUENTE"),
33:("SIN-CIFRA","Seguro comunal exige desenlaces y contrafactual, no sólo reciprocidad observada","DIAZ"),
34:("SIN-CIFRA","Cifras Guatemala no reabiertas; comparación institucional no cuantificada aquí","SIN-FUENTE"),
35:("CONFIRMA","Corrección FP-293 preservada: objeción de validez de constructo, no efecto causal","DIAZ"),
36:("MATIZA","Cancian estudió Zinacantán; no establece gradiente económico de todos los cargos","CANCian"),
37:("MATIZA","Argumento de Warman sobre inversión pública requiere edición y página exactas","SIN-FUENTE"),
38:("SIN-CIFRA","Carga de cuidados ENUT no mide distribución de cada tequio por género","ENUT"),
39:("SIN-CIFRA","Desigualdad por remesas colectivas es mecanismo posible sin contraste identificado","SIN-RESULT"),
40:("SIN-CIFRA","Cobertura de pensión histórica mutable; no necesaria para tesis comunal","SIN-FUENTE"),
41:("SIN-CIFRA","ENASEM 2024 está reservado para esta pregunta; no abrir ni usar cifra","RESERVA"),
42:("SIN-CIFRA","Superficie Sembrando Vida histórica sin fuente y fecha comparables","SIN-FUENTE"),
43:("SIN-CIFRA","Impacto ocupacional de Oportunidades requiere evaluación y estimando exactos","SIN-FUENTE"),
44:("SIN-CIFRA","Intermediarios institucionales son mecanismo localizado sin tasa nacional","SIN-FUENTE"),
45:("SIN-CIFRA","Consulta de megaproyecto requiere expedientes específicos; no se adjudica en abstracto","SIN-FUENTE"),
46:("MATIZA","Correlación posterior a transferencia no basta para rediseño; medir trayectoria y rivales","SIN-RESULT"),
47:("SIN-CIFRA","Indicadores sanitarios propuestos sin operativo ni denominador","SIN-RESULT"),
48:("SIN-CIFRA","Diagnóstico mencionado sin localizador y contenido consultado","SIN-FUENTE"),
49:("SIN-CIFRA","Reforestación mayor que devastación no verificada; no publicar cifra","SIN-FUENTE"),
}

EXTRAS = [
    ("EXTRA-RURAL-001", "L116", "En 1995 hubo 412 municipios SNI en Oaxaca", "SIN-CIFRA", "Serie histórica requiere catálogo original comparable", "IEEPCO"),
    ("EXTRA-RURAL-002", "L120", "La ausencia de conflicto en 350 municipios implica conflicto agudo en los demás", "ROMPE", "Restar una aproximación no mide la intensidad del conflicto restante", "IEEPCO"),
    ("EXTRA-RURAL-003", "L122", "Cherán perdió más de veinte mil hectáreas de bosque", "SIN-CIFRA", "Magnitud sin localizador ambiental primario", "TEPJF"),
    ("EXTRA-RURAL-004", "L145", "La reforma de 1992 permite parcelar y enajenar toda tierra ejidal", "MATIZA", "Modalidades y procedimientos importan; ejido no equivale automáticamente a propiedad privada", "RAN"),
    ("EXTRA-RURAL-005", "L175", "Los pueblos del norte rechazan la autoridad centralizada", "SIN-CIFRA", "Generalización sin contraste entre pueblos, territorios y periodos; no queda refutada aquí", "SIN-FUENTE"),
    ("EXTRA-RURAL-006", "L229", "Frecuencias de lenguas describen población indígena", "MATIZA", "Lengua y autoadscripción tienen universos distintos", "INEGI"),
    ("EXTRA-RURAL-007", "L235", "México incorporó mientras Guatemala reprimió", "MATIZA", "Síntesis requiere periodos e instituciones comparables", "SIN-FUENTE"),
    ("EXTRA-RURAL-008", "L242", "Financiar módulos de medicina tradicional como política general", "MATIZA", "Propuesta sujeta a calidad, seguridad clínica y decisión local", "SIN-RESULT"),
    ("EXTRA-RURAL-009", "L245", "Convenio 169 exige consulta previa y de buena fe", "CONFIRMA", "Estándar jurídico; cumplimiento se evalúa por proyecto", "OIT"),
    ("EXTRA-RURAL-010", "L171", "Los yaquis conservaron una estructura de ocho pueblos de misión con fuerte autonomía", "MATIZA", "Institución histórica situada; autonomía y funcionamiento actuales requieren periodo y fuente propia", "SIN-FUENTE"),
    ("EXTRA-RURAL-011", "L209", "La lista de estados con alta pobreza prueba la situación de pobreza de personas indígenas residentes allí", "ROMPE", "Falacia ecológica: las tasas estatales no identifican situación de personas indígenas", "SIN-FUENTE"),
]

with MAP.open(newline="") as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if "Comunalidad" in r["report"]]
assert len(rows) == len(D) == 49
with OUT.open("w", newline="") as f:
    wr = csv.writer(f, delimiter="\t", lineterminator="\n")
    wr.writerow(["id", "localizador_v1", "afirmacion_v1", "dictamen_v2", "razon_editorial", "fuente_clave", "result_id", "reserva"])
    for r in rows:
        n = int(r["id_afirmacion"].rsplit("-", 1)[-1])
        status, reason, source = D[n]
        wr.writerow([r["id_afirmacion"], r["localizador"], r["texto_vigente"], status, reason, source, "", "NO-ABRIR" if n == 41 else "NO-APLICA"])
    for aid, loc, claim, status, reason, source in EXTRAS:
        wr.writerow([aid, loc, claim, status, reason, source, "", "NO-APLICA"])
print(f"{len(rows)} mapa + {len(EXTRAS)} añadidas, {OUT}")
