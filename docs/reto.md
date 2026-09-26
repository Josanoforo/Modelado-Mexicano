---
title: Reto público
---

# Reto público: vence al piso

[Portada]({{ '/' | relative_url }}) · [Corpus y catálogo]({{ '/catalogo.html' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})

Este programa no mide para convencer: mide para que cualquiera pueda intentar vencerlo. La [tabla de piso v1.1](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_1.tsv) publica 43188 <!-- deriva: python3 tools/genera_tabla_piso_v1_1.py | rg '^filas_adoptadas=' --> filas — solo lo **adoptado**: cada fila es un estimador del [catálogo del mexicano v1.2](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/catalogo-del-mexicano-v1_2.md) con firma de mesa citada por id (`firma_fp`), `ADOPTADO` o `ADOPTADO-CON-RESERVA-DE-ANCHO`; ninguna es propuesta, contexto histórico ni piso heredado de legacy. La tabla se deriva con `python3 tools/genera_tabla_piso_v1_1.py --escribe`; no se edita a mano. La [v1.0](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_0.tsv) queda como histórico.

## Qué cubre hoy

| Área de consulta | Filas adoptadas |
|---|---:|
| Trabajo | 26273 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Trabajo'))" --> |
| Violencia contra las mujeres | 6887 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Violencia contra las mujeres'))" --> |
| Ingreso y gasto | 4470 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Ingreso y gasto'))" --> |
| Tecnología | 1827 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Tecnología'))" --> |
| Salud y bienestar | 980 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Salud y bienestar'))" --> |
| Confianza, religión y vínculos | 974 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Confianza, religión y vínculos'))" --> |
| Tiempo, cuidado y vínculos | 835 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Tiempo, cuidado y vínculos'))" --> |
| Trámites y Estado | 826 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Trámites y Estado'))" --> |
| Dinero y crédito | 100 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Dinero y crédito'))" --> |
| Seguridad y norma | 16 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['area_consulta']=='Seguridad y norma'))" --> |

El eje de clase NSE AMAI (con reserva de instrumento) está en 82 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['eje_nse_o_region']=='NSE'))" --> filas y el eje regional (entidad) en 23010 <!-- deriva: python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_1.tsv'),delimiter='\t') if r['eje_nse_o_region']=='REGION'))" -->; la columna `eje_nse_o_region` las marca. Casi todo el volumen es ENOE: una fila por celda de trimestre, eje y segmento. Todas las filas son RETROSPECTIVAS.

Cada fila trae su instrumento y ola, su universo/denominador, su unidad y escala, el punto y el IC (cuando está identificado), y las citas `RESULT`/`CALC`/hash para verificar la identidad del piso antes de intentar vencerlo. Una fila con IC vacío es IC no identificado, no cero: la comparación primaria de esa fila usa el error, no la cobertura.

## Las reglas — vocabulario B-bis, fijado antes de abrir el dato

1. **Pre-registro.** El retador congela su procedimiento (COMMIT-1) antes de abrir el árbitro `R` de la ola contra la que se evalúa: universo, unidad, umbral y regla de decisión quedan fijos por spec humana (`forense/prereg-caja/*-spec-v*.md`) y `spec.yaml` ejecutable, **antes** de ver el dato. Un umbral fijado después de ver la simulación de potencia o el resultado no cuenta.
2. **Comparación primaria.** Diferencia de error medio (`ΔMAE`) entre el piso adoptado y el retador sobre las celdas puntuadas de la fila o lote, con IC por réplica:
   - **Vence** si el IC despeja el umbral fijado.
   - **Propuesta con reserva** si el IC despeja 0 mas no el umbral.
   - **Nadie vence** si el IC incluye 0.
   El conteo de celdas ganadas es secundario y descriptivo, nunca la comparación primaria. Ejemplo ya corrido en este programa: piloto de gobierno digital, 3 de 15 celdas a favor del retador, `ΔMAE = 1.465 pp, IC95 [0.439, 2.115]` — el IC no despeja el umbral de 0.5 pp declarado antes de abrir el dato, así que el veredicto pre-registrado fue `FALSADOR-DÉBIL`, no una victoria. <!-- fuente: forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md l.52 -->
3. **Un piso no vencido se adopta.** Salvo veto de mesa, el piso sigue siendo el estimador adjudicado de su celda hasta que un retador pre-registrado despeje el umbral con su IC. Un retador que empata (nadie vence) es evidencia de que el piso no está identificado, no de que el retador ganó.
4. **Unidades.** Ninguna cifra de unidad delito o trámite se compara ni se promedia con una de unidad persona u hogar. Cada fila declara su unidad; la comparación exige la misma unidad y el mismo universo/denominador, o se recalcula al mismo universo primero.
5. **Cobertura ≠ punto dentro del IC.** Si el reto reporta cobertura, es «`R` dentro del IC del candidato», reportada con intervalo binomial, por celda y por conglomerado; el punto del candidato dentro del IC de `R` es otra medida y no se presenta como la misma cosa.

## Qué entregar y cómo se recibe

1. Elige una fila (o un lote de hasta cuatro) de la [tabla de piso](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_1.tsv) por su `llave`.
2. Abre un PR con: la spec humana congelada (universo, unidad, umbral, regla de decisión) **antes** de que exista el árbitro `R` de la ola que evalúas — si ya existe `R`, tu emisión es retrospectiva y se rotula así, no prospectiva; tu identidad (nombre, afiliación si aplica) y cómo contactarte.
3. Recibirás un recibo (comentario en el PR) confirmando que la spec quedó sellada y en qué ola se evaluará. El PR no se fusiona hasta que exista `R` y se calcule la comparación primaria (regla 2).
4. El resultado — venza, quede con reserva, o nadie venza — se publica en esta misma tabla y en el catálogo, con la cita de tu CALC y tu sello.

**Sin promesas de adopción.** El reto mide; mesa decide si un candidato que vence sustituye al piso adoptado. Vencer la comparación primaria es condición necesaria, no suficiente, para que mesa adopte.

## A quién se invita

Por escrito, sin publicar en redes (eso es decisión de mesa): **Toluna, ThinkNow, Matria/Celestial, YouGov**. Cualquier otro equipo — académico, comercial o independiente — puede participar por la misma vía del PR; no hace falta invitación para presentarse.

## Verificar antes de intentarlo

Antes de construir un retador, verifica que entiendes el piso que vas a enfrentar: [«Verifica en 5 minutos»]({{ '/verificar.html' | relative_url }}) explica cómo comprobar la identidad de un `CALC` sin abrir microdato, y [Corpus y catálogo]({{ '/catalogo.html' | relative_url }}) explica cómo leer `universo_denominador` y `unidad_escala` antes de comparar filas.

## Contacto

Para preguntas sobre el reto antes de abrir un PR: [Licencia y contacto]({{ '/contacto.html' | relative_url }}). El protocolo de cambio general está en [CONTRIBUTING.md](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/CONTRIBUTING.md).
