"""Cierre por identidades desde dictamen P3; no lee objetivos ni adjudica adopción."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
RUN = OUT.parent


def rows(path):
    with path.open() as source:
        return list(csv.DictReader(source, delimiter='\t'))


def write(name, data, fields):
    with (OUT/name).open('w') as target:
        writer=csv.DictWriter(target,fieldnames=fields,delimiter='\t',lineterminator='\n')
        writer.writeheader()
        writer.writerows(data)


def main():
    table_path=RUN/'lote2-tabla-estimadores.tsv'
    table=rows(table_path)
    base=rows(OUT/'identidades-base.tsv')
    expected={(r['sucesor'],r['llave']) for r in base}
    observed=[(r['sucesor'],r['llave']) for r in table]
    assert len(observed)==len(set(observed))==425 and set(observed)==expected
    state_fields=['llave','paquete','sucesor','instrumento','ola','estado','estado_comparador','estado_punto','estado_ic','estado_publicabilidad','estado_spec','separacion_efectiva','commit_reconstruccion','reconstruccion_sha256','notas_dictamen','motivo','estado_validador','apartado_por_adenda','estado_ejecucion']
    write('cierre-identidades.tsv',[{k:r.get(k,'') for k in state_fields} for r in table],state_fields)
    findings=[]
    effects=[]
    uses=rows(OUT/'consumidores-linaje.tsv')
    apart=[r for r in table if r.get('apartado_por_adenda')=='True']
    no_corrido=[dict(llave=r['llave'],paquete_sucesor=r['sucesor'],estado='NO-CORRIDO-EN-COHORTE-EVALUABLE',razon='APARTADO-POR-ADENDA; defecto de identidad de ventana del empaquetado, no D-15',nc='NC-beee-09',sucesor_encargo='ASTRA6-C1-REEMPAQUETA-VENTANA-1',estado_validador_preservado=r.get('estado_validador',''),estado_ejecucion_preservado=r.get('estado_ejecucion',''),commit_preservado=r.get('commit_reconstruccion',''),sha256_preservado=r.get('reconstruccion_sha256',''),motivo=r.get('motivo','')) for r in apart]
    write('no-corrido-identidades-local.tsv',no_corrido,['llave','paquete_sucesor','estado','razon','nc','sucesor_encargo','estado_validador_preservado','estado_ejecucion_preservado','commit_preservado','sha256_preservado','motivo'])
    for row in table:
        if row['estado']=='NO-EVALUADO': continue
        finding=[]
        if row['estado_punto']=='DISCREPA': finding.append(('PUNTO','cifra; revisar incertidumbre, alcance y conclusión en adjudicación'))
        elif row['estado_punto']=='NO-RECALCULABLE-DESDE-SPEC':
            finding.append(('PUNTO-SPEC','cifra no reconstruible según contrato humano; propuesta D-15 sin completar códigos por inferencia'))
        if row['estado_ic']=='SIN-IC-DE-REFERENCIA':
            finding.append(('IC-SIN-REFERENCIA','incertidumbre: emisión independiente sin referencia comparativa'))
        elif row['estado_ic'] not in ['COINCIDE','NO-EVALUADO']:
            finding.append(('IC', 'incertidumbre; no permite confirmar IC del original'))
        elif 'sin referencia' in row.get('notas_dictamen',''):
            finding.append(('IC-SIN-REFERENCIA','incertidumbre: emisión independiente sin referencia comparativa'))
        if row['estado_spec'] not in ['SUFICIENTE-PARA-RECONSTRUCCION','NO-DICTAMINADA']:
            finding.append(('SPEC','completitud contractual según dictamen P3; incertidumbre si falta receta IC; clasificar defecto de entrega frente a D-15 de fuente original, sin adoptar reparación'))
        if row['estado_comparador']=='COMPARADOR-RECHAZADO':
            finding.append(('TRANSPORTE','estado técnico separado; usar dictamen preservado, no declarar éxito del adaptador'))
        for kind,effect in finding:
            findings.append(dict(llave=row['llave'],sucesor=row['sucesor'],hallazgo=kind,estado=row['estado'],punto=row['estado_punto'],ic=row['estado_ic'],spec=row['estado_spec'],motivo=row.get('motivo',''),efecto_propuesto=effect,fuente='lote2-tabla-estimadores.tsv',adopcion='NO-ADOPTADO'))
        for use in uses:
            if use['paquete']!=row['paquete']:continue
            # Id completo, para evitar unir un RESULT con su complemento.
            tokens=use['camino_linaje'].replace(' -> ',' ').replace(' | ',' ').split()
            if row['llave'] not in [use['resultado_id'],use['corrida0_resultado_id']] and row['llave'] not in tokens:continue
            effects.append(dict(llave=row['llave'],sucesor=row['sucesor'],consumidor=use['consumidor'],tipo_uso=use['tipo_uso'],estado_punto=row['estado_punto'],estado_ic=row['estado_ic'],estado_spec=row['estado_spec'],efecto_propuesto='; '.join(sorted({e for _,e in finding if _!='TRANSPORTE'})) or 'ningún efecto material demostrado en este dictamen',compatibilidad_semantica='NO-CERTIFICADA-POR-LINAJE',adopcion='NO-ADOPTADO'))
    write('hallazgos-efectos.tsv',findings,['llave','sucesor','hallazgo','estado','punto','ic','spec','motivo','efecto_propuesto','fuente','adopcion'])
    write('efectos-consumidores.tsv',effects,['llave','sucesor','consumidor','tipo_uso','estado_punto','estado_ic','estado_spec','efecto_propuesto','compatibilidad_semantica','adopcion'])
    groups=collections.defaultdict(list)
    for row in table:groups[(row['instrumento'],row['ola'])].append(row)
    grouped=[]
    for (instrument,wave),items in sorted(groups.items()):
        grouped.append(dict(instrumento=instrument,ola=wave,paquetes=len({r['sucesor'] for r in items}),identidades=len(items),evaluadas=sum(r['estado']!='NO-EVALUADO' for r in items),apartadas=sum(r.get('apartado_por_adenda')=='True' for r in items),pendientes_ejecutables=sum(r['estado']=='NO-EVALUADO' and r.get('apartado_por_adenda')!='True' for r in items),puntos_coinciden=sum(r['estado_punto']=='COINCIDE' for r in items),ic_coinciden=sum(r['estado_ic']=='COINCIDE' for r in items),estados=json.dumps(dict(collections.Counter(r['estado'] for r in items)),sort_keys=True)))
    write('cierre-olas.tsv',grouped,['instrumento','ola','paquetes','identidades','evaluadas','apartadas','pendientes_ejecutables','puntos_coinciden','ic_coinciden','estados'])
    source=json.loads((OUT/'cobertura-base.json').read_text())
    complete=[r for r in table if r['estado']!='NO-EVALUADO']
    separated=[r for r in complete if r['separacion_efectiva']=='True']
    summary=dict(tabla_sha256=hashlib.sha256(table_path.read_bytes()).hexdigest(),corte_base=source['corte'],seleccion_denominador=425,historico_denominador=source['historico_denominador'],overlay_denominador=source['overlay_denominador'],estados=dict(collections.Counter(r['estado'] for r in table)),punto=dict(collections.Counter(r['estado_punto'] for r in table)),ic=dict(collections.Counter(r['estado_ic'] for r in table)),spec=dict(collections.Counter(r['estado_spec'] for r in table)),comparador=dict(collections.Counter(r['estado_comparador'] for r in table)),identidades_con_dictamen=len(complete),identidades_con_dictamen_y_separacion=len(separated),puntos_coincidentes_con_separacion=sum(r['estado_punto']=='COINCIDE' for r in separated),ic_coincidentes_con_separacion=sum(r['estado_ic']=='COINCIDE' for r in separated),hallazgos_filas=len(findings),consumidores_filas=len(effects),catalogo_c1_cerrado=False,adopcion='NO-ADOPTADO',advertencia='Conteos sobre selección; no representan tasa del catálogo. NO-EVALUADO IC por ausencia de referencia no equivale a igualdad ni a fracaso del punto.')
    summary.update(apartadas_por_adenda=len(apart),ejecutables_segun_adenda=len(table)-len(apart),pendientes_ejecutables=sum(r['estado']=='NO-EVALUADO' and r.get('apartado_por_adenda')!='True' for r in table),diagnostico_apartadas=dict(collections.Counter(r.get('estado_validador','') for r in apart)),limitacion_red='NC-beee-08: contexto/archivos y transcript no acreditan bloqueo de red ni política egress; alcance observado, no aislamiento de red')
    summary['estados_ejecutables']=dict(collections.Counter(r['estado'] for r in table if r.get('apartado_por_adenda')!='True'))
    (OUT/'cierre-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    report=['# P4 · Efectos y cobertura del corte de resultados', '', 'EJECUTADO: regenerado desde `lote2-tabla-estimadores.tsv`, hash `'+summary['tabla_sha256']+'`. Los estados provienen de la unión P3 que selecciona el dictamen sucesor de revisión máxima; este lector no abre esperados ni recalcula ni cambia tolerancias.', '', 'EJECUTADO: '+str(len(complete))+' identidades con dictamen de '+str(len(table))+' seleccionadas; '+str(len(separated))+' con separación acreditada. Estados: '+json.dumps(summary['estados'],ensure_ascii=False,sort_keys=True)+'. Punto: '+json.dumps(summary['punto'],ensure_ascii=False,sort_keys=True)+'. IC: '+json.dumps(summary['ic'],ensure_ascii=False,sort_keys=True)+'.', '', 'EJECUTADO: denominadores separados, selección '+str(summary['seleccion_denominador'])+', histórico '+str(summary['historico_denominador'])+', overlay '+str(summary['overlay_denominador'])+'. `cierre-olas.tsv` agrupa instrumento/ola; `olas-fuentes.tsv` conserva dependencia por raw compartido. No se extrapola proporción de coincidencias al catálogo.', '', 'LEÍDO: el rechazo técnico de transporte se conserva como estado del comparador. Un dictamen separado puede evaluar el punto congelado sin acreditar éxito del adaptador. EDER: IC independientes sin referencia no acreditan coincidencia de incertidumbre. ENCODAT: una ausencia de receta humana IC sustentada por dictamen es hallazgo de la entrega; no demuestra por sí sola D-15 de la spec original; un alias o columna inesperada por sí solo no acredita insuficiencia de spec.', '', 'PROPUESTO-POR-EJECUTOR: `hallazgos-efectos.tsv` separa punto, IC, spec y transporte. Las consecuencias por consumidor en `efectos-consumidores.tsv` son propuestas: discrepancia IC afecta incertidumbre; su alcance y conclusión requieren adjudicación específica. La coincidencia de punto no remueve el hallazgo IC ni valida el mecanismo causal. No se adopta corrección, retiro ni parámetro.', '', 'LEÍDO: los enlaces consumidores provienen de la vista de usos al hash de preparación, por identidad completa. Su aptitud de linaje no certifica compatibilidad semántica. Ausencia de enlace observado no acredita ausencia de consumidores editoriales.', '', 'Pendiente: completar las entradas sin dictamen, adjudicar consecuencias materiales, recibo independiente y decisión de mesa. C1 no se declara cerrado.']
    report += ['', 'LEÍDO/EJECUTADO: adenda operativa sesión04 consumida: cohorte original '+str(len(table))+' = '+str(summary['ejecutables_segun_adenda'])+' ejecutables y '+str(len(apart))+' apartadas por NC-beee-09. Pendientes ejecutables: '+str(summary['pendientes_ejecutables'])+'. El defecto ENDIREH es identidad de ventana del empaquetado, no insuficiencia D-15. Se preservan primer intento, salida, hashes, commit y diagnóstico del validador en `no-corrido-identidades-local.tsv`; su NO-RECALCULABLE-DESDE-SPEC diagnóstico no se cuenta como dictamen adoptable del lote. Sucesor: ASTRA6-C1-REEMPAQUETA-VENTANA-1, con entrada/cohorte nuevas; las 767 de2021 no se absorben en04.', '', 'LEÍDO: NC-beee-08; evidencia de contexto/archivos y transcript no demuestra bloqueo de red ni política egress. No se afirma aislamiento de red. La limitación se preserva y una brecha material se adjudica al lanzamiento correspondiente, sin reconstruir ceguera retroactiva.']
    (OUT/'informe-efectos-corte.md').write_text('\n'.join(report)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
