#!/usr/bin/env python3
"""Produce tabla TIME desde juicios editoriales explícitos y mapa vigente; no decide por regex."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MAP = ROOT / 'canon/mapa-dominios-v1_1.tsv'
OUT = Path(__file__).with_name('afirmaciones.tsv')
PREFIX = 'corpus/reports/El_Mexicano_y_el_Tiempo__'

# id: dictamen editorial, razón concreta, ancla (RESULT o publicación primaria)
J = {
 'ENOE-001': ('MATIZA','La tasa describe ocupados; no identifica cultura ni causa de planear.','RESULT-ENOE-PISOS-TABLA:empleo_informal/nacional/NAC'),
 'TIME-001': ('SIN-CIFRA','El tabulado externo de ola reservada se excluye; los RESULT de ahorro disponibles no miden metas ni estabilidad individual del ingreso.','restriccion-documental-ENIF2024'),
 'TIME-002': ('SIN-CIFRA','El tabulado externo de ola reservada se excluye; este producto no tiene RESULT autorizado de carga doméstica.','restriccion-documental-ENUT2024'),
 'TIME-003': ('SIN-CIFRA','ENIGH2024 reservada; la cifra territorial no es necesaria para inferir tiempo.','reserva-ENIGH2024'),
 'TIME-004': ('SIN-CIFRA','ENIGH2024 reservada; sin apertura ni sustitución.','reserva-ENIGH2024'),
 'TIME-005': ('SIN-CIFRA','ENIGH2024 reservada; sin apertura ni sustitución.','reserva-ENIGH2024'),
 'TIME-006': ('MATIZA','Colchón corto (<1 mes; P4_10 en {1,2}) es más frecuente SIN seguridad social que CON ella: menor resiliencia descriptiva SIN. Grupos seleccionados; no prueba efecto de formalizar, horizonte de metas ni puntualidad.','RESULT-ENIF-AHO-A-P-CORTO-CON-P;RESULT-ENIF-AHO-A-P-CORTO-SIN-P'),
 'TIME-007': ('SIN-CIFRA','Instrumento inadecuado para preferencia causal nacional frente a estabilidad individual.','ENIF2024/P4_10'),
 'TIME-008': ('MATIZA','La cifra del v1 tiene periodo y definición distintos del registro adoptado; se usa el estimando 2024T3 con denominador explícito.','RESULT-ENOE-PISOS-TABLA:empleo_informal/nacional/NAC'),
 'TIME-009': ('SIN-CIFRA','TIL urbana de otra ola no es comparable con informalidad nacional ni mide planeación.','ENOE-boletín-histórico'),
 'TIME-010': ('ROMPE','Llamar irracional a planear a todo un grupo desde una tasa agregada es inferencia inválida.','RESULT-ENOE-PISOS-TABLA:empleo_informal/nacional/NAC'),
 'TIME-011': ('SIN-CIFRA','Sondeo de profesionistas sin informe primario y diseño verificados; tasas retiradas.','fuente-no-verificada'),
 'TIME-012': ('SIN-CIFRA','No hay medición emparejada de puntualidad social/laboral en mismas personas.','instrumento-inadecuado'),
 'TIME-013': ('MATIZA','Uso lexicográfico plausible; compromiso y asistencia no se desprenden del significado.','Diccionario-del-español-de-México'),
 'TIME-014': ('ROMPE','Ausencia de vehículos confiables no está identificada como causa principal de falta de previsión.','RESULT-ENIF-AHO-B-P-FORMAL-P'),
 'TIME-015': ('SIN-CIFRA','Marco de escasez importado; mecanismo psicológico no medido conjuntamente en México.','Mullainathan-Shafir-2013'),
 'TIME-016': ('SIN-CIFRA','La presentación de la última ola reservada se excluye; no hay medición de duración de planes en este producto.','restriccion-documental-ENSU2025'),
 'TIME-017': ('SIN-CIFRA','Informe de desplazamiento primario no cotejado completo; retirar magnitud.','fuente-pendiente'),
 'TIME-018': ('MATIZA','Evitación podría medirse; racionalidad e horizonte futuro no se identifican desde percepción.','ENVIPE2021-AP4_4/AP4_10'),
 'TIME-019': ('SIN-CIFRA','La publicación de ola reservada se excluye; no se infiere disponibilidad individual ni planeación.','restriccion-documental-ENUT2024'),
 'TIME-020': ('SIN-CIFRA','La publicación de ola reservada se excluye; sus agregados no son evidencia de este producto.','restriccion-documental-ENUT2024'),
 'TIME-021': ('MATIZA','Hall/Hofstede son marcos importados, no medición individual nacional.','Hall1959/Hofstede'),
 'TIME-022': ('SIN-CIFRA','Puntaje nacional histórico sin muestra actual representativa; se retira.','Hofstede'),
 'TIME-023': ('MATIZA','Ensayo bancario aleatorizado identifica efecto de mensaje en clientes, no descuento temporal nacional.','DOI:10.1093/pnasnexus/pgad058'),
 'TIME-024': ('SIN-CIFRA','Estudio fronterizo no cotejado en texto completo; sin extrapolación.','literatura-pendiente'),
 'TIME-025': ('SIN-CIFRA','Estudio de estímulos alimentarios no cotejado en texto completo; sin extrapolación.','literatura-pendiente'),
 'TIME-026': ('MATIZA','El descuento temporal aparece fuera de México, pero universalidad estricta excede evidencia aquí leída.','marco-importado'),
 'TIME-027': ('ROMPE','Edad/cohorte poblacional no prueba inmediatez digital ni preferencia temporal.','CPV2020-no-mide-preferencia'),
 'TIME-028': ('SIN-CIFRA','Tasas comerciales de pagos juveniles sin metodología primaria cotejada; retiradas.','fuente-no-verificada'),
 'TIME-029': ('SIN-CIFRA','Simpatía como motivo del sí voy requiere medir motivo y asistencia en misma persona.','instrumento-inadecuado'),
 'TIME-030': ('MATIZA','Confianza regional Latinobarómetro no equivale a confianza mexicana ni predice planeación.','Latinobarómetro2024'),
 'TIME-031': ('CONFIRMA','La policronía histórica no aporta medición nacional contemporánea representativa.','Hall1959-1983'),
 'TIME-032': ('SIN-CIFRA','Cobertura de emergencia no se traslada a duración de meta; cifra exacta no consultada en RESULT de esta pieza.','ENIF2024-P4_10'),
 'TIME-034': ('SIN-CIFRA','Minutos de holgura social inventados sin registro de hora pactada y llegada.','instrumento-inadecuado'),
 'TIME-035': ('SIN-CIFRA','Compromiso formal y sanción no están emparejados con cumplimiento real.','instrumento-inadecuado'),
 'TIME-036': ('SIN-CIFRA','RSVP social y costo de faltar no medidos conjuntamente.','instrumento-inadecuado'),
 'TIME-037': ('SIN-CIFRA','Asistencia a cita y recordatorio/costo no medidos conjuntamente en este corpus.','instrumento-inadecuado'),
 'TIME-038': ('MATIZA','ENVIPE permite evitar salir de noche; no mide contracción del horizonte temporal.','ENVIPE2021-AP4_4/AP4_10'),
}

EXTRA = [
 ('T-EXTRA-01','L17','La cuenta de retiro y aportación voluntaria prueban falta de previsión','SIN-CIFRA','La publicación externa de ola reservada se excluye; tenencia no demuestra motivación ni previsión.','restriccion-documental-ENIF2024'),
 ('T-EXTRA-02','L141','Inmediatez de Gen Z por pagos y TikTok','SIN-CIFRA','Edad y uso de medios no miden descuento temporal; cifras comerciales no verificadas.','instrumento-inadecuado'),
 ('T-EXTRA-03','L175-L188','Formalidad/exportación demuestra que las mismas personas planean','ROMPE','Comparación entre sectores seleccionados no sigue a las mismas personas.','selección-sin-panel'),
 ('T-EXTRA-04','L181','Falta a citas médicas causada por barreras materiales','SIN-CIFRA','El estudio acotado no identifica causalidad ni tasa nacional actual.','instrumento-inadecuado'),
 ('T-EXTRA-05','L15;L111','Sanción formal causa puntualidad social/laboral diferencial','SIN-CIFRA','No hay comparación emparejada ni cambio de sanción exógeno.','instrumento-inadecuado'),
 ('T-EXTRA-06','L113','Improvisación de bomberazo causada por escasez','SIN-CIFRA','No hay medición representativa de improvisación y escasez en la misma tarea.','instrumento-inadecuado'),
 ('T-EXTRA-07','L139','Confianza interpersonal urbana implica racionalidad de no planear','ROMPE','Confianza en personas no equivale a garantía institucional ni prueba óptimo individual.','ENCOAP2023-distinto-reactivo'),
]

# La columna de cita v1 conserva el localizador, pero no retranscribe
# extractos de publicaciones reservadas en el producto corregido.
REDACTED_V1 = {
 'TIME-001': 'El v1 sostiene que la estabilidad del ingreso determina el horizonte de planeación y usa la existencia de metas económicas de largo plazo como apoyo; extracto reservado omitido.',
 'TIME-002': 'El v1 atribuye a mujeres más trabajo no remunerado que a hombres, acentúa la brecha en localidades pequeñas e infiere menos tiempo para planear o comprometerse; extracto reservado omitido.',
 'TIME-003': 'El v1 usa la pobreza multidimensional de Chiapas como contexto territorial de la planeación; extracto reservado omitido.',
 'TIME-004': 'El v1 usa la pobreza multidimensional de Guerrero como contexto territorial de la planeación; extracto reservado omitido.',
 'TIME-005': 'El v1 usa la pobreza multidimensional de Oaxaca como contexto territorial de la planeación; extracto reservado omitido.',
 'TIME-006': 'El v1 afirma que trabajadores formales ahorran para el retiro y contratan seguros e hipotecas, y de ello infiere planeación a largo plazo causada por estabilidad; extracto reservado omitido.',
 'TIME-016': 'Afirmación v1 sobre percepción de inseguridad (texto histórico en v1; extracto reservado omitido)',
 'TIME-019': 'Afirmación v1 sobre carga de cuidados (texto histórico en v1; extracto reservado omitido)',
 'TIME-020': 'Afirmación v1 sobre uso del tiempo (texto histórico en v1; extracto reservado omitido)',
 'TIME-032': 'Afirmación v1 sobre emergencia financiera (texto histórico en v1; extracto reservado omitido)',
}

rows=[]
with MAP.open(newline='') as f:
 for m in csv.DictReader(f,delimiter='\t'):
  if PREFIX not in m['report'] and m['id_afirmacion']!='ASTRA5-U0-ENOE-001': continue
  key=m['id_afirmacion'].removeprefix('ASTRA5-U0-')
  if key not in J: raise SystemExit(f'Falta decisión explícita: {key}')
  verdict,reason,source=J[key]
  rows.append([m['id_afirmacion'],m['localizador'],REDACTED_V1.get(key,m['texto_vigente']),m['dictamen'],verdict,reason,source])
for id_,loc,claim,verdict,reason,source in EXTRA:
 rows.append([id_,loc,claim,'AUSENTE-DEL-MAPA',verdict,reason,source])
if set(J)!={x[0].removeprefix('ASTRA5-U0-') for x in rows if x[0].startswith('ASTRA5-')}:
 raise SystemExit('Decisiones huérfanas o filas duplicadas')
with OUT.open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['id','localizador_v1','afirmacion_v1','dictamen_mapa','dictamen_v2','razon_editorial','ancla']);w.writerows(rows)
print(f'{OUT}: {len(rows)} afirmaciones; mapa={len(rows)-len(EXTRA)}, extras={len(EXTRA)}')

# Traza de las únicas cifras propias consumidas en el texto. Se consultan los
# objetos sellados y la decisión de catálogo; ninguna cifra se teclea aquí.
USED = (
 'RESULT-ENIF-AHO-B-P-FORMAL-P',
 'RESULT-ENIF-AHO-B-P-INFORMAL-P',
 'RESULT-ENIF-AHO-A-P-CORTO-CON-P',
 'RESULT-ENIF-AHO-A-P-CORTO-SIN-P',
)
calc = ROOT/'data/corrida0/CALC-ENIF-0001/resultados.json'
raw = calc.read_bytes()
data = json.loads(raw)['resultados']
sha = hashlib.sha256(raw).hexdigest()
sello = json.loads((calc.parent/'sello.json').read_text())
assert sello['resultados.json'] == sha
catalog={}
with (ROOT/'canon/catalogo-del-mexicano-v1_3.tsv').open(newline='') as f:
 for x in csv.DictReader(f,delimiter='\t'):
  if x['result_id'] in USED: catalog[x['result_id']] = x
assert set(catalog)==set(USED)
trace=Path(__file__).with_name('trazas-result.tsv')
with trace.open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n')
 w.writerow(['result_id','calc','fila_json','sha256_resultados_json','valor_p','unidad','poblacion','ola','denominador','n_denominador','metodo_ic','estado_adopcion','firma_fp'])
 for rid in USED:
  stem=rid[:-2]
  c=catalog[rid]
  assert c['calc']=='CALC-ENIF-0001' and c['estado_adopcion']=='ADOPTADO'
  w.writerow([rid,'CALC-ENIF-0001',f'/resultados/{rid}',sha,data[rid],
              'proporción ponderada (p)','persona elegida ENIF 18+','ENIF 2024',
              data[stem+'-DENOMINADOR'],data[stem+'-N-DENOMINADOR'],
              data[stem+'-METODO-IC'],c['estado_adopcion'],c['firma_fp']])
print(f'{trace}: {len(USED)} RESULT con fila/hash/denominador/adopción')
