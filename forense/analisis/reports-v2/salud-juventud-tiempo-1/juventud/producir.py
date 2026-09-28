#!/usr/bin/env python3
"""Produce la tabla de afirmaciones desde juicios editoriales explícitos."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'forense/analisis/dominios/lotes/juventud-filas-v1_0.tsv'
OUT = HERE / 'tabla.tsv'

# Dictamen, razón y condición de revisión. Una clave equivale a una fila del mapa,
# nunca a una decisión inferida de palabras o de posición en el original.
JUICIOS = {
1: ('SIN-CIFRA','EDER 2025 reservada; salir antes de 18 no identifica independencia económica ni efecto causal de cohorte.','Abrir solo con permiso; estimar historias a igual edad y entorno.'),
2: ('SIN-CIFRA','EDER 2025 reservada; primera unión no es salida del hogar.','Contrastar transiciones con universo y edad comunes.'),
3: ('SIN-CIFRA','No se localizó tabulado OCDE primario con denominador y año.','Localizar tabla de convivencia parental 20–30.'),
4: ('SIN-CIFRA','ENADID 2023 reservada; la tasa trienal no debe fecharse como flujo anual.','Permiso y comparación de tasas con referencia temporal correcta.'),
5: ('SIN-CIFRA','ENADID 2023 reservada; TGF sintética de periodo no mide hijos finales de una cohorte.','Permiso y estimandos comparables.'),
6: ('SIN-CIFRA','Extremos históricos de unión y matrimonio sin universo homogéneo verificado; ENADID 2023 reservada.','Serie de estado conyugal por edad y fuente.'),
7: ('MATIZA','ENDUTIH mide uso individual; grupo de edad, horas y dispositivo son componentes distintos; el RESULT de población 6+ no verifica 18–24.','Tabular 18–24, horas y dispositivo con mismo universo.'),
8: ('MATIZA','RESULT-ENDUTIH-PISOS-2024-TABLA#46 y cortes TLOC apoyan brecha 6+; no la magnitud joven ni mecanismo de habilidad.','Corte 18–24 por localidad y diseño.'),
9: ('MATIZA','Artículo primario ENSANUT 2022 sostiene diferencias de intento, pero no ideación mayor en adolescentes; vida y año son ventanas distintas.','Comparar misma ventana y edad con incertidumbre.'),
10: ('SIN-CIFRA','ENCODAT 2025 sin comprobación de reserva y publicación primaria completa en esta pieza.','Acreditar permiso y tabla de edad/sexo.'),
11: ('SIN-CIFRA','Tasa por sexo requiere defunciones y población comparables; conteo EDR no es tasa.','Tasas por sexo, residencia y año.'),
12: ('SIN-CIFRA','Cita Oxfam no cotejada contra método; no empleo no equivale a cuidados y porcentajes compuestos tienen denominadores distintos.','Documento primario y ENOE con actividad, estudio y cuidado.'),
13: ('SIN-CIFRA','Cuenta satélite externa no verificada aquí; valor agregado no es prevalencia juvenil.','Tabulado de cuenta satélite y año.'),
14: ('SIN-CIFRA','NEET OCDE exige definición, edad y año.','Tabla primaria comparable.'),
15: ('ROMPE','La ausencia de descenso agregado no identifica efecto causal del programa; faltan contrafactual, exposición y rezagos.','Evaluación de impacto con comparador.'),
16: ('SIN-CIFRA','Censo puede medir afiliación, pero no cohorte persistente ni sexo motor del cambio desde un corte.','Series con misma pregunta y composición.'),
17: ('SIN-CIFRA','Superlativo de asistencia sin conteo comparable ni método.','Registro de asistentes comparable.'),
18: ('MATIZA','Cambio legal es observable; acceso efectivo y efecto actitudinal requieren otros indicadores.','Serie legal, oferta y uso por entidad.'),
19: ('SIN-CIFRA','ENDISEG 2021 es fuente pública, pero identificación por edad en corte no prueba cambio generacional; reserva por alcance pendiente de cotejo.','Permiso y repetición de idéntica pregunta.'),
20: ('MATIZA','Muestra comercial de usuarios de app no transporta a población joven; sesgo de selección explícito.','Marco muestral probabilístico.'),
21: ('ROMPE','Encuesta estadounidense de jerarquía política no acredita conducta laboral mexicana ni exigencia de justificación.','Escala mexicana de autoridad laboral con comparación etaria.'),
22: ('MATIZA','Deloitte multinacional describe su muestra; aspiración directiva y movilidad laboral no miden rechazo a jerarquía.','Microdatos mexicanos con definición de marco y empleo.'),
23: ('SIN-CIFRA','Choque con mando vertical y deferencia residual es mecanismo sin medición mexicana.','Encuesta o experimento en organizaciones.'),
24: ('ROMPE','Participación de jóvenes entre votos de coalición no es apoyo de la coalición entre jóvenes ni decisividad.','Encuesta validada y contrafactual electoral.'),
25: ('SIN-CIFRA','Emisor y simulacros sin identificación; muestras universitarias no representan electorado juvenil.','Identificar levantador, diseño y denominador.'),
26: ('SIN-CIFRA','Punto anterior y comparabilidad temporal no acreditados; México total no es juventud.','Dos olas comparables de Latinobarómetro con edad.'),
27: ('SIN-CIFRA','Referencia Guerrero 2024 incompleta; no hay estimando nacional.','Cita completa y lectura de métodos.'),
28: ('MATIZA','El mapa menciona piso ENOE agregado, pero el alias RESULT-ENOE-PISOS-TABLA no resuelve por consulta; no se consume como RESULT. Ocupados total no contrasta edad 20–30; informalidad no es NEET.','Corte de ocupados 20–30 con IC de diseño y RESULT individual resoluble.'),
29: ('SIN-CIFRA','Tipología cuatro íes sin escala mexicana validada; juicio de transporte, no rasgo nacional medido.','Validación psicométrica y muestra mexicana.'),
30: ('ROMPE','Declarar predominio de periodo o de cohorte sin identificación APC viola edad=periodo−cohorte.','Panel/repetidas y restricciones identificadoras explícitas.'),
31: ('MATIZA','Los universales de los clichés son débiles; no queda demostrada la atribución común a desigualdad y cuidados.','Medidas directas de competencia, empleo, cuidados y autoridad.'),
32: ('SIN-CIFRA','"Casi toda" literatura requiere censo de estudios y universos; no se cuenta aquí.','Censo reproducible de fuentes y muestras.'),
}
EXTRAS = [
('JUV-EXTRA-01','L9,L29,L215','Vivienda, salario e informalidad explican principalmente la emancipación y fecundidad','ROMPE','Correlaciones descriptivas no identifican fracción causal ni descartan preferencia.','Panel/transición y variación exógena o control de selección.'),
('JUV-EXTRA-02','L126,L262','Jóvenes Construyendo el Futuro no redujo NEET','ROMPE','Serie agregada no estima efecto del programa.','Comparador de elegibilidad y exposición.'),
('JUV-EXTRA-03','L236','Escolaridad es motor del cambio actitudinal','SIN-CIFRA','Escolaridad, edad, selección y periodo no están descompuestos.','Medir actitudes y educación con diseño longitudinal.'),
('JUV-EXTRA-04','L259','Reducción de fecundidad está asociada a educación sexual','SIN-CIFRA','No hay contraste de exposición a educación sexual.','Evaluación con acceso, cohorte y contexto.'),
('JUV-EXTRA-05','L195','No participar equivale a desafección institucional','ROMPE','Abstención puede tener muchas causas; atribución individual no identificada.','Encuesta de no votantes con motivos.'),
]

# Las celdas del mapa contienen literales de olas reservadas. Conservar la
# identidad y el estimando sin republicar sus valores en la tabla editorial.
REDACTAR = {
    1: 'Salida del hogar de origen antes de la adultez por cohorte EDER 2025; contraste entre cohortes.',
    2: 'Primera unión antes de la adultez por cohorte EDER 2025.',
    4: 'Cambio de la fecundidad adolescente entre ENADID 2018 y ENADID 2023.',
    5: 'Cambio de la tasa global de fecundidad entre ENADID 2018 y ENADID 2023.',
    6: 'Cambio de unión libre y matrimonio entre periodos citados en el original.',
    10: 'Malestar psicológico y conducta suicida adolescente por edad y sexo, ENCODAT 2025.',
    16: 'Cambio de afiliación religiosa entre censos y diferencias por edad y sexo.',
    19: 'Autoidentificación LGBTI+ por edad, ENDISEG 2021.',
    26: 'Cambio de apoyo declarado a la democracia entre olas de Latinobarómetro.',
}

def main():
    with SOURCE.open(newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    assert len(rows) == len(JUICIOS) == 32
    with OUT.open('w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['id','localizador','afirmacion_v1','dictamen_v2','razon_especifica','evidencia_o_limite','falsador_o_siguiente_prueba'])
        for i, row in enumerate(rows, 1):
            decision, reason, test = JUICIOS[i]
            evidence = {'MATIZA':'fuente primaria o RESULT de componente acotado','ROMPE':'inferencia del original inválida','SIN-CIFRA':'adquisición, ejecución, comparabilidad o reserva indicada en razón'}[decision]
            if i == 28:
                evidence = 'alias agregado no resoluble; sin cifra propia juvenil'
            claim = REDACTAR.get(i, row['texto_vigente'])
            w.writerow([row['id_afirmacion'],row['localizador'],claim,decision,reason,evidence,test])
        for extra in EXTRAS:
            ident, locator, claim, decision, reason, test = extra
            w.writerow([ident,locator,claim,decision,reason,'lectura íntegra del original; fuera del mapa',test])
    print(f'{len(rows)} filas del mapa + {len(EXTRAS)} adicionales → {OUT}')

if __name__ == '__main__':
    main()
