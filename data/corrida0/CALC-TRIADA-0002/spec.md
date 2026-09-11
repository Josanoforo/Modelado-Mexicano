# CALC-TRIADA-0002 · F5 completa

**Acto:** `GEN2-F5-COMPLETA`, 10/sep/2026. **Generación:** GEN2.
**Cuenta GEN2:** `SI`, por el objeto explícito del encargo archivado: «para
CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita explícitos».
Contar no adopta ningún brazo ni modifica el motor.

## Objeto

Ejecutar y sellar el cálculo prospectivo de
`F5-completa-spec-v1_0.md`, congelado junto con el plan y el medidor fuente en
el commit `7d97681`, anterior a toda respuesta. Compara `L_SOLO`, `L_CORPUS`
y el snapshot M contra los 14 árbitros R. La pregunta primaria es uso
documental/operacional; transferencia permanece secundaria.

Las 224 posiciones son nuevas y pertenecen al mismo tratamiento, pregunta,
cliente y alias. Todas terminaron `OK`; una reanudación posterior al límite de
cuota preservó los sobres fallidos como antecedentes. Los 194 sobres iniciales
y los 30 reanudados acreditan el mismo competidor canónico
`claude-opus-5` mediante `modelUsage`; el campo superior `model` no está
presente en el formato actual del cliente.

## Método

El medidor invoca por ruta el cálculo ya congelado en
`tools/calcula_f5_completa.py`. Este extrae sólo la última línea no vacía:
`ESTIMACION_PUNTUAL=N%`, `ABSTENCION`, malformada o error técnico, sin
rellenar faltantes. El punto por celda y brazo es la mediana de réplicas
numéricas. U3 es la intersección con punto de L_SOLO, L_CORPUS, M y R.

Sobre el mismo U3 calcula MAE en pp y tres diferencias de MAE mediante
bootstrap pareado por celda, 10,000 réplicas, semilla 42 e IC percentil 95%.
La banda práctica es 0.5 pp y la tolerancia numérica separada es 1e-9 pp. Un
ganador global debe ganar ambas comparaciones y no tener menor cobertura;
de otro modo el resultado es `SIN-GANADOR-UNICO`. Las pruebas prospectivas
cubren borde exacto, residuo binario, diferencia material y simetría.

## Insumos y límite de identidad

`spec.yaml` fija por hash la spec científica, el plan de 224 identidades, el
calculador, el snapshot M y el universo que resuelve los 14 R. Las capturas y
los catorce `resultados.json` R son colecciones repo-locales: su identidad
colectiva queda fijada por el commit de ejecución, igual que el precedente
`CALC-SMOKE-0002` para directorios de corridas. El medidor verifica 224 filas,
identidad contra el plan y estados/exclusiones antes de emitir resultados.

No abre microdato, no llama a modelos, no modifica capturas históricas, no
generaliza fuera del marco y no habilita F6 ni adopción al motor.

## Salidas

Se declaran antes de ejecutar: controles de 224 posiciones y estados;
U3 y coberturas; tres MAE; para cada pareada, punto, IC95 y veredicto; y el
veredicto global. Los textos comparan exacto y los flotantes con tolerancia
absoluta 1e-9.
