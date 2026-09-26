---
title: Reto público
---

# Reto público: vence al piso · v1.1

[Portada]({{ '/' | relative_url }}) · [Corpus y catálogo]({{ '/catalogo.html' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }}) · [Consultar]({{ '/consultar.html' | relative_url }}) · [Contrato de consulta]({{ '/consulta.html' | relative_url }})

> v1.1 (26/sep/2026, acto `GEN2-PRODUCTO-CONSULTA-1`, PROPUESTO-POR-EJECUTOR sobre el plan de visibilización §3.6 aprobado en bloque): añade el formato de entrega para una familia 2027 — la predicción se entrega **en el mismo formato que devuelve la consulta**, sellada antes de que exista el árbitro, con recibo y comparación primaria fijados aquí. Lo demás de v1.0 no cambia.

Este programa no mide para convencer: mide para que cualquiera pueda intentar vencerlo. La [tabla de piso](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_0.tsv) publica **72 filas** <!-- deriva: python3 tools/genera_tabla_piso.py | rg '^filas_adoptadas=' --> — el conjunto **adoptado**, no el catálogo completo (1 537 filas, la mayoría contexto histórico sin adopción). Adoptado significa `ADOPTADO-POR-FIRMA` o `CONSUMO-GEN2-ACTIVO`: piso u orden de mesa firmada, no propuesta, no piso histórico de contexto, no pendiente de dictamen. La tabla se deriva con `python3 tools/genera_tabla_piso.py`; no se edita a mano.

## Qué cubre hoy

| Área de consulta | Filas adoptadas |
|---|---:|
| Dinero y crédito | 27 <!-- deriva: python3 -c "import csv;print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_0.tsv'),delimiter='\t') if r['area_consulta']=='Dinero y crédito'))" --> |
| Trámites y Estado | 22 <!-- deriva: python3 -c "import csv;print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_0.tsv'),delimiter='\t') if r['area_consulta']=='Trámites y Estado'))" --> |
| Tiempo, cuidado y vínculos | 13 <!-- deriva: python3 -c "import csv;print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_0.tsv'),delimiter='\t') if r['area_consulta']=='Tiempo, cuidado y vínculos'))" --> |
| Seguridad y norma | 10 <!-- deriva: python3 -c "import csv;print(sum(1 for r in csv.DictReader(open('canon/tabla-de-piso-v1_0.tsv'),delimiter='\t') if r['area_consulta']=='Seguridad y norma'))" --> |
| Ingreso y gasto | 0 — sellado como contexto, sin fila adoptada en este corte |

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

1. Elige una fila (o un lote de hasta cuatro) de la [tabla de piso](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/canon/tabla-de-piso-v1_0.tsv) por su `llave`.
2. Abre un PR con: la spec humana congelada (universo, unidad, umbral, regla de decisión) **antes** de que exista el árbitro `R` de la ola que evalúas — si ya existe `R`, tu emisión es retrospectiva y se rotula así, no prospectiva; tu identidad (nombre, afiliación si aplica) y cómo contactarte.
3. Recibirás un recibo (comentario en el PR) confirmando que la spec quedó sellada y en qué ola se evaluará. El PR no se fusiona hasta que exista `R` y se calcule la comparación primaria (regla 2).
4. El resultado — venza, quede con reserva, o nadie venza — se publica en esta misma tabla y en el catálogo, con la cita de tu CALC y tu sello.

**Sin promesas de adopción.** El reto mide; mesa decide si un candidato que vence sustituye al piso adoptado. Vencer la comparación primaria es condición necesaria, no suficiente, para que mesa adopte.

## v1.1 · Entregar predicciones para una familia 2027

**Familia 2027.** Un conjunto de celdas `conducta × instrumento × segmento` cuya ola 2027 todavía no publica INEGI: no existe el árbitro `R` y, por E.6, toda ola nueva nace reservada al entrar al corpus. El piso a vencer es la fila del catálogo vigente que devuelve la [consulta]({{ '/consultar.html' | relative_url }}) para esa conducta y segmento (la ola anterior por eje, o los marginales públicos de la misma ola en cruces). Si la consulta dice `NO CONTESTA` para una celda, esa celda no tiene piso y no entra a la comparación primaria: se reporta aparte.

**Formato — el contrato de consulta como formato de salida.** Un archivo `prediccion.json` con la misma envoltura que `python3 tools/benchmark.py consulta --json` ([contrato §3]({{ '/consulta.html' | relative_url }})), una respuesta por celda:

| campo | valor en la entrega |
|---|---|
| `llave` | la llave del piso que enfrentas (de la consulta) |
| `conducta`, `instrumento`, `eje`, `segmento`, `unidad` | idénticos a los del piso — misma unidad y mismo universo, o la celda no se compara |
| `ola` | `"2027"` (o la ola futura que declares) |
| `punto`, `ic95`, `tipo_ic` | tu predicción; `ic95` obligatorio si quieres que se reporte cobertura |
| `temporalidad` | `"PROSPECTIVA"` — sólo lo es si el sello precede a la publicación de la ola |
| `origen_piso` | `"RETADOR:<tu-id>"` |
| `result`, `calc`, `sha256_*` | vacíos: los asigna el programa al sellar tu CALC |

**Sello previo.** Abre un PR que añade `prediccion.json` y tu spec humana (universo, unidad, umbral, regla de decisión). El sello es el `sha256` de `prediccion.json` en el commit del PR, más, si quieres un testigo fuera de GitHub, el [sello externo]({{ '/sello-externo.html' | relative_url }}). Un archivo cuyo commit es posterior a la publicación de la ola se rotula `RETROSPECTIVA` y se reporta en otra columna (§4 de las instrucciones: ninguna frase mezcla las dos).

**Recibo.** Un comentario en tu PR con: `sha256` de `prediccion.json`, commit, fecha, número de celdas recibidas, cuántas casan con un piso de la consulta y cuántas no (con su razón `NO CONTESTA`), y la ola contra la que se evaluará. El recibo no juzga la predicción.

**Comparación primaria — fijada antes de abrir el dato.** Cuando INEGI publique la ola y el programa derive `R` con su código congelado, se calcula la regla 2 de arriba: `ΔMAE` entre el piso y tu predicción sobre las celdas puntuadas, con IC por réplica; vence / propuesta con reserva / nadie vence según el IC contra el umbral que declaraste. La cobertura (`R` dentro de tu IC) se reporta aparte, con intervalo binomial, por celda y por conglomerado. El conteo de celdas ganadas es descriptivo.

**Qué no cambia.** La consulta devuelve pisos, no retadores (regla 6): tu predicción no aparece en la consulta hasta que mesa la adopte.

## A quién se invita

Por escrito, sin publicar en redes (eso es decisión de mesa): **Toluna, ThinkNow, Matria/Celestial, YouGov**. Cualquier otro equipo — académico, comercial o independiente — puede participar por la misma vía del PR; no hace falta invitación para presentarse.

## Verificar antes de intentarlo

Antes de construir un retador, verifica que entiendes el piso que vas a enfrentar: [«Verifica en 5 minutos»]({{ '/verificar.html' | relative_url }}) explica cómo comprobar la identidad de un `CALC` sin abrir microdato, y [Corpus y catálogo]({{ '/catalogo.html' | relative_url }}) explica cómo leer `universo_denominador` y `unidad_escala` antes de comparar filas.

## Contacto

Para preguntas sobre el reto antes de abrir un PR: [Licencia y contacto]({{ '/contacto.html' | relative_url }}). El protocolo de cambio general está en [CONTRIBUTING.md](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/CONTRIBUTING.md).
