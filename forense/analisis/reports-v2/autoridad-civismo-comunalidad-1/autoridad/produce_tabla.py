#!/usr/bin/env python3
"""Materializa el dictamen editorial explícito de Autoridad desde el mapa vigente."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
MAP = ROOT / 'canon/mapa-dominios-v1_1.tsv'
SOURCE = 'corpus/reports/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md'

# Dictamen y fundamento por identidad. Nunca se deducen del dictamen heredado.
DECISIONS = {
 '001': ('MATIZA','INEGI-ENCUCI','Acuerdo con enunciado; no deseo de caudillo ni conducta.'),
 '002': ('MATIZA','INEGI-ENCUCI','Acuerdo con participación; no participación efectiva.'),
 '003': ('MATIZA','INEGI-ENCUCI','Referentes y escalas requieren su propio denominador; no relación exclusiva.'),
 '004': ('SIN-CIFRA','WVS-Q','Reactivo infantil sin RESULT compatible; no mide obediencia adulta.'),
 '005': ('MATIZA','HOF','Índice publicado de muestra empresarial; inferencia nacional individual inválida.'),
 '006': ('MATIZA','GLOBE','Prácticas y valores son escalas declaradas de gerentes; no conducta observada.'),
 '007': ('SIN-CIFRA','—','No hay medida simultánea de cortesía y motivación interna; instrumento inadecuado.'),
 '008': ('SIN-CIFRA','WVS-Q','Comparación de países sin tabla armonizada de reactivo y universo.'),
 '009': ('SIN-CIFRA','—','Jefe y compadre exigen comparación en el mismo ámbito laboral; OCDE no es ese contraste.'),
 '010': ('MATIZA','INEGI-ENCUCI','Marginales no establecen coexistencia individual; requiere cruce en la misma persona.'),
 '011': ('SIN-CIFRA','—','Máxima histórica no identifica conducta contemporánea; instrumento inadecuado.'),
 '012': ('SIN-CIFRA','—','No hay tasa nacional de palancas ni contrafactual; adquisición pendiente.'),
 '013': ('ROMPE','OCDE24','Confianza institucional y personal coexisten; exclusividad es falsa.'),
 '014': ('MATIZA','GLOBE','Preferencia gerencial no identifica tipo de jefe eficaz ni población completa.'),
 '015': ('SIN-CIFRA','—','Semántica de sí/quizás sin corpus contextual; no medible aquí.'),
 '016': ('SIN-CIFRA','—','Razón de movilidad carece de fuente primaria y definición homogénea.'),
 '017': ('SIN-CIFRA','—','Gradiente de ingreso requiere fuente, ajuste y universo; causalidad no identificada.'),
 '019': ('SIN-CIFRA','—','Trabajo de Berkeley no verificado para población México; transporte no acreditado.'),
 '020': ('SIN-CIFRA','—','Equivalencia región-país y tres perfiles regionales carecen de métrica comparativa.'),
 '021': ('MATIZA','INEGI-CENSO','Afiliación censal no mide obediencia a autoridad religiosa; denominadores históricos incompatibles.'),
 '022': ('SIN-CIFRA','—','Empresa familiar, gobernanza y sucesión mezclan marcos muestrales sin fuente primaria.'),
 '023': ('CONFIRMA','OCDE24','La nota primaria sí publica 27% para empleados públicos que rechazarían soborno para acelerar servicio; escenario distinto de favores políticos.'),
 '024': ('SIN-CIFRA','—','Aprobación, clientelismo y debilitamiento institucional son estimandos distintos.'),
 '025': ('SIN-CIFRA','—','Absorción de redes y criterio de recompensa requieren evidencia organizacional identificada.'),
 '026': ('MATIZA','OCDE24','No hay baja confianza uniforme; la medida cambia por referente y cobertura urbana.'),
 '027': ('SIN-CIFRA','—','No se identifican motivaciones por cumplimiento observable; instrumento inadecuado.'),
 '028': ('SIN-CIFRA','—','Trabajo remoto sin contrafactual ni cohorte mexicana comparable.'),
 '029': ('MATIZA','HOF','Se preserva corrección FP-293: covariación sin multiplicador causal medido.'),
 '030': ('SIN-CIFRA','INEGI-ENCUCI','Valores publicados requieren RESULT del reactivo y denominador.'),
 '031': ('SIN-CIFRA','INEGI-ENCUCI','Autoritarismo declarado no equivale a conducta política; falta RESULT.'),
}
EXTRA = [
 ('AUTOR-003a','Confianza en servidores públicos de ENCUCI','SIN-CIFRA','Requiere RESULT propio de referente, escala y denominador válido.'),
 ('AUTOR-003b','Confianza en conocidos personalmente de ENCUCI','SIN-CIFRA','Requiere RESULT propio; no implica confianza exclusivamente personal.'),
 ('AUTOR-010a','Acuerdo con gobierno encabezado por líder fuerte','MATIZA','Preferencia declarada de frase, no autoritarismo ni conducta.'),
 ('AUTOR-010b','Acuerdo con participación de todos','MATIZA','Preferencia declarada de frase, no participación efectiva.'),
 ('AUTOR-010c','Los mismos encuestados apoyan ambas opciones','SIN-CIFRA','Falta cruce individual AP4_9_1 por AP4_9_4.'),
 ('AUTOR-021a','Cambio de afiliación católica entre censos','MATIZA','Requiere denominadores comparables; no mide poder de clero.'),
 ('AUTOR-021b','Proporción protestante y sin religión en censo','SIN-CIFRA','Falta RESULT propio de categorías, universo y periodo.'),
 ('AUTOR-029a','PDI y aversión a incertidumbre covarían en perfil','MATIZA','FP-293 conserva co-variación descriptiva.'),
 ('AUTOR-029b','Ambas puntuaciones producen efecto multiplicador','SIN-CIFRA','FP-293 retiró mecanismo causal no medido.'),
 ('L26','Conflicto evitado sistemáticamente en toda organización','SIN-CIFRA','No hay muestra de actos comunicativos; heterogeneidad de organizaciones.'),
 ('L28','La fuerza laboral joven es mayoría y causa cambio gerencial','SIN-CIFRA','El porcentaje citado no tiene fuente verificable; edad y cohorte se confunden.'),
 ('L29','Norte, centro y sur son tres culturas de autoridad','SIN-CIFRA','Categorías geográficas no son clases psicológicas ni muestras regionales.'),
 ('L31','Gobernanza de empresas familiares: porcentajes universales','SIN-CIFRA','Marco muestral, definición y fuente no verificables.'),
 ('L33','Corrupción como lubricante racional','SIN-CIFRA','Sin comparación de costos, riesgos ni alternativas; no es efecto estimado.'),
 ('L34','Morena heredó redes clientelares y premia lealtad','SIN-CIFRA','Necesita unidad, periodo y evidencia de selección/contrato; no inferible de aprobación.'),
 ('§2','Autoridad técnica subordinada habitualmente a la personal','SIN-CIFRA','No hay contraste de decisiones donde cambie credencial y relación por separado.'),
 ('§4','Respeto familiar internalizado y laboral estratégico','SIN-CIFRA','Misma conducta puede surgir de normas, incentivos o temor; falta diseño discriminante.'),
 ('§4','Desconfianza produce evasión y no confrontación','SIN-CIFRA','Frecuencias de confianza no identifican respuesta conductual.'),
 ('§5','Aztecas, colonia e Iglesia causan jerarquía actual','SIN-CIFRA','Genealogía histórica sin identificación de transmisión y contrafactual.'),
 ('§5','PRI reprodujo jerarquía psicológica nacional','SIN-CIFRA','Historia institucional no estima actitudes individuales posteriores.'),
 ('§5','Familia entrena deferencia transferible al empleo','SIN-CIFRA','Transferencia intercontextual sin seguimiento de personas.'),
 ('§6','Ramos ofrece arquetipos de clase útiles hoy','SIN-CIFRA','Tipología literaria sin validación predictiva contemporánea; utilidad no contrastada.'),
 ('§6','Gen Z pide justificar autoridad más que generaciones previas','SIN-CIFRA','Sin panel o contraste de cohorte, edad y periodo.'),
 ('§7','PDI comparado prueba que México supera a Japón o España','MATIZA','Puntuaciones de origen corporativo no identifican jerarquía conductual actual.'),
 ('§8','Liderazgo paternalista-participativo eleva desempeño','SIN-CIFRA','Sin ensayo o cuasiexperimento mexicano con desenlace laboral.'),
 ('§8','Nunca criticar públicamente y usar feedback indirecto','SIN-CIFRA','Consejo local plausible, no efecto universal; probar seguridad y resultados.'),
 ('§8','Contratos verbales superan escritos por confianza','SIN-CIFRA','Sin datos de cumplimiento/daño y contexto contractual.'),
 ('§9','Protestas demuestran ausencia de sumisión nacional','MATIZA','Existencia de protesta refuta universalidad, no estima disposición media.'),
 ('§10','Redes personales debilitan instituciones en ciclo','SIN-CIFRA','Se conserva FP-293: ciclo causal no demostrado longitudinalmente.'),
]

def rows():
    with MAP.open(newline='') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            if row['report'] != SOURCE: continue
            suffix = row['id_afirmacion'].rsplit('-',1)[-1]
            if suffix not in DECISIONS: raise SystemExit(f'Sin decisión: {row["id_afirmacion"]}')
            status, evidence, reason = DECISIONS[suffix]
            yield [row['id_afirmacion'],row['localizador'],row['texto_vigente'],status,reason,evidence,'Externa; sin RESULT propio','Población/escala indicadas en fuente; sin extrapolación individual']
    for i,(loc,claim,status,reason) in enumerate(EXTRA,1):
        yield [f'AUT-V2-EXTRA-{i:03}',loc,claim,status,reason,'Original v1 y contraste editorial','Sin RESULT propio','Alcance limitado a tesis original']

if __name__ == '__main__':
    out=HERE/'afirmaciones.tsv'
    with out.open('w', newline='') as f:
        wr=csv.writer(f,delimiter='\t',lineterminator='\n')
        wr.writerow(['id','localizador_v1','afirmacion','dictamen','razon','evidencia','estado_result','alcance'])
        wr.writerows(rows())
    data=list(rows())
    mapped=sum(row[0].startswith('ASTRA5-') for row in data)
    count=Counter(row[3] for row in data)
    summary={
      'report':'corpus/reports-v2/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md',
      'registros':len(data),'mapa_filas':mapped,
      'dictamenes':{k:count.get(k,0) for k in ('CONFIRMA','MATIZA','ROMPE','SIN-CIFRA')},
      'cifras':{'propias_result':0,'externas_en_prosa':'OCDE24 27% soborno: adultos urbanos de México, ola 2023, percepción 6–10 en escala 0–10'},
      'generar':'python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/autoridad/produce_tabla.py',
      'verificar':'python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/autoridad/verifica.py',
    }
    (HERE/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(out)
