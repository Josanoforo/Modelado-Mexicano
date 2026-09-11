# F5-A · cobertura documental dirigida · propuesta v1.0

Estado: **PROPUESTA PARA MESA; NO AUTORIZA LLAMADAS**. Producto distinto de
transferencia. Reutiliza el diseño de #698 sin convertir el panel conocido en
confirmación.

## Pregunta y unidad

Pregunta: ¿un paquete con la fuente específica del mismo estimando convierte
las abstenciones de `DIN-M-01` y `TRA-M-07` en puntos trazables, sin sustituir
encuesta, población, evento, códigos o unidad?

Unidad de análisis: celda × brazo. Las ocho respuestas de una celda/brazo
miden variación de la captura; no son ocho familias ni ocho encuestas.

## Diseño y coste

- Celdas: 2 (`DIN-M-01`, `TRA-M-07`).
- Brazos contemporáneos: 2 (`CONTEXTUAL-v2`, `FUENTE-DIRIGIDA-v1`).
- Réplicas: 8 por celda/brazo.
- Total: **2 × 2 × 8 = 32 llamadas**. M no compite y R sólo identifica el
  estimando; no se recalcula para escoger documentos.
- Máximo dos reintentos sólo para error técnico. Una respuesta válida o una
  abstención válida no se repite.

El modelo real, cliente, prompt, ventana y orden se congelan. Cambiar el
modelo rompe identidad; Codex no lo sustituye.

## Fuentes requeridas

Antes de la primera captura se fijan ruta, hash, procedencia y licencia de:

- DIN: documento/microdato autorizado que contiene `cr27` de ENNViH/MxFLS
  ola 1, población/libro 3B, códigos, ponderador y referencia temporal;
- TRA: documento/tabulación autorizada de ENCIG 2021 para `P8_3_1`, personas
  18+, respuesta válida, ponderador y referencia temporal.

El brazo contextual conserva el paquete comparable de #698; el dirigido añade
sólo la fuente específica. Una tabla derivada del propio R o una transcripción
del valor R no cuenta como fuente nueva independiente. Si el dato objetivo
está explícito, el éxito prueba recuperación/verificación documental, no
predicción ni generalización.

## Identidad, contaminación y faltantes

Cada posición declara hash de prompt y respuesta. Fuentes y respuestas se
resuelven una vez. R, resultados derivados de R y cualquier antecesor
materializado del objetivo están fuera de ambos paquetes. Renombrar/copiar no
borra origen. Fuente o procedencia indeterminada detiene la celda.

Una salida sin punto es `ABSTENCION`, `MALFORMADA` o `ERROR_TECNICO`; nunca
cero. El reporte conserva 32 posiciones y su causa.

## Éxito y parada

Éxito exige **en cada celda**:

- al menos 6/8 puntos del brazo dirigido trazables al documento correcto;
- cero sustituciones semánticas;
- mejora de cobertura de al menos 4/8 respecto al control contemporáneo.

Se termina después de 32 posiciones, o antes si cambia identidad de
modelo/cliente, aparece contaminación con R o hay dos fallos sistémicos
consecutivos de autenticación/cuota. Si una celda no alcanza el umbral, se
vuelve a adquisición/definición; no se amplía `k` para obtener una cifra.

Un éxito habilita diseñar celdas nuevas. No reabre `TRIADA-0002`, no cierra
por sí solo `NC-0152` y no autoriza F6.
