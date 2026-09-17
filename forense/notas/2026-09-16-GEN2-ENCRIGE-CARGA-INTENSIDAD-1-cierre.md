# Cierre · GEN2-ENCRIGE-CARGA-INTENSIDAD-1

Fecha local: 16 de septiembre de 2026. Base efectiva `origin/main`:
`e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`. Rama:
`acto/gen2-encrige-carga-intensidad-1`.

## Producto y decisión que permite

Se produjo un análisis reproducible que separa alcance (`p=A/N`), incidencia
por empresa expuesta (`m=T/N`) e intensidad entre empresas afectadas
(`r=T/A`), mide la concentración de `N`, `A` y `T` por tamaño y descompone los
tres contrastes frente a Micro.

La lectura permite decidir qué dimensión descriptiva incorporar a TRA. Grande
tiene el mayor punto de prevalencia y una brecha de incidencia dominada por
intensidad condicional; Micro concentra 92.73% de empresas afectadas y 84.62%
del volumen de trámites/inspecciones con corrupción. Pequeña y Mediana ocultan
en incidencias casi iguales a Micro una cancelación entre menor prevalencia y
mayor intensidad condicional.

## Estado de ejecución

- **PREPARADO:** spec, código, prueba y encargo fijados en `18a8c46`, antes de
  la primera derivación real.
- **EJECUTADO:** cinco dominios, cuatro participaciones y tres contrastes;
  salida de producto en `forense/analisis/encrige-carga-intensidad-1/`.
- **SELLADO:** `CALC-ENCRIGE-CARGA-INTENSIDAD-0001`, corrida
  `CALC-ENCRIGE-CARGA-INTENSIDAD-0001--55259dbe975f`, sello `c94f098f…`.
- **INTEGRADO:** no; queda en PR para fusión exclusiva de Jonás.
- **ADOPTADO:** no; no se editó TRA, motor, decisiones ni consumidores.

## Verificación

`spec-check` pasó con 0 fallos. La prueba focal pasó 5/5: `A=0` deja `r` no
estimable, denominadores incompatibles se rechazan, una razón mayor que uno es
válida, `T<A` activa la guarda semántica y el caso real reproduce sin mutar al
padre. El CALC verificó sello, cinco inputs y 31 resultados con
`CONTEXTO=IDENTICO` y `RESULTADO=REPRODUCE`.

Las sumas de los cuatro tamaños reconstruyen exactamente los nacionales de
`N`, `A` y `T`. El residuo de `m=p*r` es cero al grano de salida y el máximo de
las descomposiciones es `2e-41`. No se ejecutó el medidor padre, no se abrió
microdato y no se descargó ninguna fuente.

## Reservas y cierre compartido diferido

No hay incertidumbre muestral utilizable en el CSV; no se declaran
significancia, causalidad, tendencia ni intervención óptima. `r` no distingue
oportunidades de interacción de riesgo por interacción. Para hacerlo falta el
total de todas las interacciones por empresa/tamaño, corruptas o no.

**CIERRE COMPARTIDO DIFERIDO.** Después de CAREO/TRÁMITE-4, la integración
serial necesaria se limita a:

1. decidir e incorporar la lectura descriptiva a TRA;
2. decidir el tratamiento de `cuenta_gen2`, sin contar este derivado como
   instrumento o validación independiente;
3. rederivar entonces los registros compartidos que correspondan.

No se escribieron `decisiones.tsv`, no-corrido, firmas, hallazgos, PARA,
gobernanza, estado, rótulos, tableros, contadores, colas ni registro global.
