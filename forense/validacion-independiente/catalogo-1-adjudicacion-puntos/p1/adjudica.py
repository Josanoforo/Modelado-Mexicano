#!/usr/bin/env python3
"""Deriva adjudicación documental por identidad; no lee microdatos ni altera sellos."""
import csv, json, hashlib
from collections import Counter
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote1/efectos-discrepancias.tsv'
# Juicios documentales fijados tras cotejo humano: véase evidencia.md.
RULES={
 'externos':('DEFECTO-PRODUCTOR','Negativo con cualquier casilla válida sin coincidencia','Negativo exige casillas válidas o vacías; desconocido conserva NA','C1-PUNTOS-E1','Corregir regla de ausencia en sucesor; no adoptar validador por proximidad'),
 'edad2011':('DEFECTO-PRODUCTOR','60+ incluye códigos EDAD 98/99 al aceptar hasta120','60+ limita60..97','C1-PUNTOS-E2','Excluir98/99 de cortes etarios; declarar universo global por separado'),
 'reciente':('DEFECTO-PRODUCTOR','Reciente condicionado adicionalmente a vida conocida','Reciente clasificado por sus respuestas y salto6.1=4','C1-PUNTOS-E3','Eliminar condición de vida conocida si ventana reciente clasificable; contrato sucesor explícito'),
 'instituciones':('AMBIGUEDAD-CONTRACTUAL-DIFERENCIA-ESTIMANDO','Cada institución entre solicitantes de alguna ayuda','Cada institución entre afectadas con respuesta conocida','C1-PUNTOS-E4','Fijar denominador por institución; ofrecer tasas distintas con nombres distintos'),
 'permisos':('DEFECTO-PRODUCTOR','CP7_1 sin filtro CP4_1','CP7_1 restringido CP4_1=1/2','C1-PUNTOS-E5','Aplicar filtro relación actual/anterior; conservar sello histórico'),
 'denuncia':('DEFECTO-PRODUCTOR','2.12 columnas1y5 y elegibilidad global ayuda','Columnas1..4 enlazadas a dos solicitudes institucionales','C1-PUNTOS-E6','Corregir selección y enlace de resultados de atención en sucesor'),
 'edad2021':('DEFECTO-PRODUCTOR','60+ incluye EDAD98/99','60+ excluye EDAD>=98','C1-PUNTOS-E7','Excluir98/99 en cortes; auditar elegibilidad global separadamente')}
def behavior_family(b):
 if b=='externo_denuncia_ultima_visita':return 'denuncia'
 if b.startswith('externo_'):return 'externos'
 if b.startswith('pareja_institucion_'):return 'instituciones'
 if b.startswith('permiso_'):return 'permisos'
 if b.startswith('pareja_') and b.endswith('desde_octubre_2010'):return 'reciente'
 return ''
def main():
 rows=[]
 for r in csv.DictReader(SOURCE.open(),delimiter='\t'):
  if r['componente']!='punto':continue
  age=r['eje']=='edad' and r['segmento']=='60+'
  family=('edad2021' if '2021' in r['paquete'] else 'edad2011') if age else behavior_family(r['conducta'])
  assert family in RULES, r
  state,pr,va,ref,proposal=RULES[family]
  concurrent=behavior_family(r['conducta']) if family=='edad2011' else ''
  limit='Defecto de regla probado; no se atribuye exhaustivamente el delta ni se valida toda la cifra independiente sin contrastes raw autorizados. Ranking, umbral y conclusión no comprobados.'
  if concurrent:limit+=' Concurre regla '+concurrent+'; grupo de edad no separa contribuciones.'
  rows.append(dict(identidad_original=r['llave'],paquete=r['paquete'],conducta=r['conducta'],eje=r['eje'],segmento=r['segmento'],familia=family,mecanismo_concurrente=concurrent,dictamen_documental=state,regla_productor=pr,regla_validador=va,evidencia_ref=ref,delta_nativo=r['delta_punto'],delta_pp=str(Decimal(r['delta_punto'])*100),efecto='cifra; alcance del denominador; conclusión pendiente de trazado P3',limite_atribucion=limit,propuesta='PROPUESTO-POR-EJECUTOR: '+proposal))
 assert len(rows)==685 and len({r['identidad_original'] for r in rows})==685
 rows.sort(key=lambda r:r['identidad_original'])
 with (OUT/'adjudicacion.tsv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 summary={'identidades':len(rows),'familias':dict(Counter(r['familia'] for r in rows)),'dictamenes':dict(Counter(r['dictamen_documental'] for r in rows)),'concurrencias':dict(Counter(r['mecanismo_concurrente'] for r in rows if r['mecanismo_concurrente'])),'sha256_entrada':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'max_delta_absoluto':str(max(abs(Decimal(r['delta_nativo'])) for r in rows))}
 (OUT/'c1-puntos-p1-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
