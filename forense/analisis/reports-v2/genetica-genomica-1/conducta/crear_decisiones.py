"""Build editorial decisions from the immutable GENBEH map plus explicit additions."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MAP = ROOT / 'canon/mapa-dominios-v1_1.tsv'
OUT = Path(__file__).with_name('decisiones.json')

# Judgment is explicit; no RESULT exists for this genetic domain.
judgments = {
  1: ('CONFIRMA', 'Revisión bibliográfica de composición de estudios, no desempeño mexicano.', 'Duncan 2019'),
  2: ('MATIZA', 'Porcentaje histórico sujeto al criterio de agrupación; no es prevalencia de población ni rendimiento PRS.', 'Duncan 2019'),
  3: ('MATIZA', 'Número de loci del artículo; se evita trasladar conteo a fenotipo mexicano.', 'Karlsson Linner 2019'),
  4: ('MATIZA', 'Loci de análisis combinado de rasgos distintos; no se suman como loci de una conducta única.', 'Karlsson Linner 2019'),
  5: ('MATIZA', 'R2 incremental en validación de hermanos, no probabilidad de acertar persona.', 'Karlsson Linner 2019'),
  6: ('MATIZA', 'Asociación de instrumento y consumo autorreportado en europeos; no efecto causal genotípico individual.', 'Holmes 2014'),
  7: ('CONFIRMA', 'OR de binge drinking de portadores frente a no portadores en la muestra europea.', 'Holmes 2014'),
  8: ('CONFIRMA', 'OR de abstención de portadores frente a no portadores en la muestra europea.', 'Holmes 2014'),
  9: ('MATIZA', 'Vía bioquímica plausible; R2 instrumental y aversión no equivalen a causalidad conductual completa.', 'Holmes 2014'),
 10: ('ROMPE', 'Agnosticismo normativo de uso no demuestra imposibilidad de efectos poblacionales ni dominio estructural universal.', 'Holmes 2014'),
 11: ('SIN-CIFRA', 'Cifra de estudio caso-control no cotejada en fuente primaria en esta revisión; asociación local no transportable.', 'Bierut 2012'),
 12: ('MATIZA', 'Ausencia en muestras antiguas no significa ausencia universal ni desacredita por sí sola todo mito.', 'Estudio ALDH2 1994'),
 13: ('MATIZA', 'Pequeño experimento Mission Indian no representa a pueblos mexicanos ni identifica prevalencia.', 'Garcia-Andrade 1997'),
 14: ('SIN-CIFRA', 'Asociación de expectativa en muestra específica sin lectura primaria aquí; no se afirma efecto causal.', 'Gonzalez y Skewes 2018'),
 15: ('SIN-CIFRA', 'Frecuencias v1 combinan muestras y denominadores no homologados; retirar intervalo nacional.', 'Lisker 1995; Konishi 2003'),
 16: ('SIN-CIFRA', 'Frecuencia huichol sin fuente primaria y denominador comprobados; no usar como punto nacional.', 'Fuente histórica por verificar'),
 17: ('MATIZA', 'Interacción de cohorte no es gen de violencia ni replica universal.', 'Caspi 2002'),
 18: ('MATIZA', 'Metaanálisis de interacción con heterogeneidad y sesgo potencial; p no es tamaño clínico.', 'Byrd y Manuck 2014'),
 19: ('SIN-CIFRA', 'Narrativa mediática y frecuencia maorí no cotejadas en original; se conserva advertencia sin cifra.', 'Lea y Chambers 2007'),
 20: ('SIN-CIFRA', 'Alegación judicial exacta no cotejada en expediente primario; no reproducir multiplicador.', 'Expediente judicial por verificar'),
 21: ('MATIZA', 'SNP-heredabilidad de fenotipo en muestra GWAS, no R2 del score ni herencia individual.', 'Karlsson Linner 2019'),
 22: ('SIN-CIFRA', 'Rango de correlaciones entre rasgos sin tabla primaria cotejada; se conserva poligenicidad cualitativa.', 'Karlsson Linner 2019'),
 23: ('MATIZA', 'Metaanálisis de cesación en subgrupos, distinto de utilidad clínica mexicana.', 'Buchwald 2022'),
 24: ('SIN-CIFRA', 'OR adolescente no cotejado en texto primario; no trasladarlo a pacientes mexicanos.', 'Chenoweth 2013'),
 25: ('MATIZA', 'Ensayo usa NMR fenotípico; no prueba regla por genotipo ni necesidad de bupropión.', 'Lerman 2015'),
 26: ('ROMPE', 'Hay estudio mexicano de CYP2A6 con 88 fumadores jóvenes; sigue sin prevalencia representativa.', 'Borrego-Soto 2020'),
 27: ('MATIZA', '30 y 51 por ciento corresponden a edades y tarea específicas; 25 por ciento infantil no cotejado.', 'Anokhin 2011'),
 28: ('CONFIRMA', 'GWAS europeo 23andMe reporta 11 loci y SNP-h2 9.85 ±0.57%; no replica señal previa.', 'Sanchez-Roige 2025'),
 29: ('ROMPE', 'Correlación genética con educación no demuestra que señal esté confundida por entorno.', 'Sanchez-Roige 2018; 2025'),
 30: ('MATIZA', 'Cambio cognitivo pre/post cosecha en India no mide descuento temporal mexicano.', 'Mani 2013'),
 31: ('ROMPE', 'No hay comparación identificada de magnitudes sobre mismo desenlace que ordene estructura y genética.', 'Anokhin 2011; Sanchez-Roige 2025'),
 32: ('MATIZA', 'Preservar distinción ya hecha por v1: percepción fuerte, ingesta inconsistente; p exacta sin fuente cotejada.', 'TAS2R38 literatura primaria'),
 33: ('SIN-CIFRA', 'Identidad del ensayo de intervención citado ambiguamente; efecto retirado hasta cotejo.', 'Calancie 2018 por cotejar'),
 34: ('ROMPE', 'No se identificó contraste mexicano que demuestre dominio de cocina/precio sobre genotipo.', 'Sin comparación identificada'),
 35: ('MATIZA', 'Estructura genómica mexicana heterogénea, no orden de temperamento entre grupos.', 'Moreno-Estrada 2014'),
 36: ('MATIZA', 'Gen candidato local solo hipótesis; requiere replicación, control de estructura y pruebas múltiples.', 'Estudio DRD2/ANKK1 PMID 28152448'),
 37: ('MATIZA', 'No hay evidencia que sostenga esencialismo nacional; ausencia de soporte no prueba mecanismo alterno.', 'Síntesis de estudios anteriores'),
 38: ('MATIZA', 'Reglas clínicas y públicas requieren validación de utilidad; firewall es decisión del proyecto.', 'Lerman 2015; mandato C3'),
}
urls = {
 'Duncan 2019':'https://pubmed.ncbi.nlm.nih.gov/31346163/',
 'Karlsson Linner 2019':'https://www.nature.com/articles/s41588-018-0309-3',
 'Holmes 2014':'https://www.bmj.com/content/349/bmj.g4164',
 'Borrego-Soto 2020':'https://pubmed.ncbi.nlm.nih.gov/31959879/',
 'Lerman 2015':'https://pubmed.ncbi.nlm.nih.gov/25588294/',
 'Anokhin 2011':'https://pubmed.ncbi.nlm.nih.gov/20700643/',
 'Sanchez-Roige 2025':'https://www.nature.com/articles/s41380-025-03356-8',
 'Moreno-Estrada 2014':'https://pubmed.ncbi.nlm.nih.gov/24926019/',
 'Byrd y Manuck 2014':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3858396/',
 'Caspi 2002':'https://pubmed.ncbi.nlm.nih.gov/12161658/',
}
sin_cifra_categoria = {
 11:'adquisición pendiente', 14:'adquisición pendiente',
 15:'no comparabilidad', 16:'adquisición pendiente',
 19:'adquisición pendiente', 20:'adquisición pendiente',
 22:'adquisición pendiente', 24:'adquisición pendiente',
 33:'adquisición pendiente',
}
rows=[]
with MAP.open() as f:
    for m in csv.DictReader(f, delimiter='\t'):
        ident=m['id_afirmacion']
        if 'GENBEH' not in ident: continue
        n=int(ident[-3:]); d, why, source=judgments[n]
        rows.append(dict(id=f'COND-{n:03}', mapa_id=ident, dictamen=d,
                         razon=why, razon_sin_cifra=(f'{sin_cifra_categoria[n]}: {why}' if d=='SIN-CIFRA' else ''),
                         fuente=source, fuente_url=urls.get(source,''),
                         lectura_fuente=(('LEIDO-TEXTO-HTML' if source in {'Holmes 2014','Karlsson Linner 2019','Sanchez-Roige 2025'} else 'LEIDO-RESUMEN-PRIMARIO') if source in urls else 'REFERENCIA-V1-NO-COTEJADA'),
                         resultado='', trace=m['localizador']))
extras=[
 ('039','L3','ROMPE','Tesis general de dominio estructural carece de magnitudes causales comparables en el mismo desenlace.','Sin comparación identificada'),
 ('040','L9','MATIZA','Llamar causal al contraste genotipo-consumo confunde asociación del instrumento con efecto MR de alcohol sobre enfermedad.','Holmes 2014'),
 ('041','L17','ROMPE','Baja R2 limita predicción observada, pero no demuestra inutilidad absoluta de cualquier modelo futuro.','Karlsson Linner 2019'),
 ('042','L206','ROMPE','Utilidad clínica directa del NMR/CYP2A6 en México no está demostrada por ensayo extranjero.','Lerman 2015'),
 ('043','L224','MATIZA','Prohibición de segmentar por ascendencia es regla del proyecto, no resultado experimental.','Mandato C3'),
]
for n, loc, d, why, source in extras:
    rows.append(dict(id=f'COND-{n}',mapa_id='',dictamen=d,razon=why,
                     razon_sin_cifra='',fuente=source,fuente_url=urls.get(source,''),
                     lectura_fuente=(('LEIDO-TEXTO-HTML' if source in {'Holmes 2014','Karlsson Linner 2019','Sanchez-Roige 2025'} else 'LEIDO-RESUMEN-PRIMARIO') if source in urls else 'REFERENCIA-V1-NO-COTEJADA'),
                     resultado='',trace=loc))
assert len(rows)==43
OUT.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
