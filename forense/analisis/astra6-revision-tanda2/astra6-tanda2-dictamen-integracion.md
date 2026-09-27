# Revisión ASTRA6 · cierre de dependencias de la segunda tanda

ARCHIVO: forense/analisis/astra6-revision-tanda2/astra6-tanda2-dictamen-integracion.md
NOMBRE ESTABLE: Dictamen ASTRA6 segunda tanda
CONTADOR: cero; revisión documental, sin mediciones ni adopciones.

Corte consolidado: `57a3f2a4f55178d02d8b0e3c165502014ca48efa`.
Consulta GitHub: 27/sep/2026 03:35:20 UTC (26/sep 21:35:20 CDMX).
Encargo: actualizar el estado de dependencias del documento de mesa
`07-REVISION-PR-Y-DECISION.md` y entregar este dictamen en PR, por solicitud expresa.
Perímetro: esta carpeta. Dictamen PROPUESTO-POR-EJECUTOR.

## Dictamen

La tanda está integrada: las seis PR están fusionadas y sus siete controles
remotos terminaron SUCCESS sobre los HEAD finales registrados en astra6-tanda2-estado-pr.json.
Esto cierra la espera de ramas. El cierre sustantivo conserva recibos, firmas
y decisiones pendientes; CI y fusión no los sustituyen.

| Entrega | PR | Resultado integrado | Pendiente para su uso |
|---|---|---|---|
| C1 ejecución | [1184](https://github.com/Josanoforo/Modelado-Mexicano/pull/1184) | Nueve paquetes, 3371 identidades: 3 COINCIDE, 2569 DISCREPA, 799 NO-RECALCULABLE-DESDE-SPEC | Dictamen de discrepancias y continuidad C1; revisión Claude FUSIONABLE-CON-RESERVA, replay contra microdatos NO-VERIFICADO por ese revisor |
| C1 preparación | [1185](https://github.com/Josanoforo/Modelado-Mexicano/pull/1185) | 59 sucesores: 11 paquetes/425 estimadores preparados, 48/32347 con impedimentos | Recibo; reconocimiento de hashes sucesores antes de revelación; firmas de acceso/tolerancias donde corresponda |
| C2 cierre material | [1182](https://github.com/Josanoforo/Modelado-Mexicano/pull/1182) | Inventario portable, cobertura de lector efectivo y cotejo de enmienda/drivers; conflictos y CI corregidos | Recibo sobre HEAD final y firmas independientes de propuestas; atestación externa no verificada |
| Consumo/familia | [1179](https://github.com/Josanoforo/Modelado-Mexicano/pull/1179) | Cláusulas explícitas; cinco ROMPE sin evidencia contraria pasan a SIN-CIFRA; Zeiders separado | Nuevo recibo técnico y cotejo de fuentes; #1178 no acepta este sucesor |
| Género/violencia/salud | [1180](https://github.com/Josanoforo/Modelado-Mexicano/pull/1180) | Tres reports v2 con constructos, denominadores y límites explícitos | Recibo independiente y revisión humana de tesis |
| Trabajo/movilidad/clase | [1181](https://github.com/Josanoforo/Modelado-Mexicano/pull/1181) | Tres reports; corrección final de MOV-034a y MOV-EX02; movilidad queda sin ROMPE | Recibo sobre HEAD final; adjudicación de exposición a ENIGH2024_RR.pdf; aclaración de condicionamiento CEEY |

Las 2569 discrepancias C1 no son 2569 puntos numéricos distintos: el informe
separa 685 puntos distintos, 1873 coincidencias de punto con IC distinto y
11 discrepancias de publicabilidad. Las 799 identidades restantes no se pudieron
recalcular desde la spec. No se extrapola este diagnóstico al catálogo completo.
Fuentes locales: [resumen C1](../../validacion-independiente/catalogo-1-ejecucion-lote1/resumen-lote1.json)
y [informe C1](../../validacion-independiente/catalogo-1-ejecucion-lote1/informe-lote1.md).

Se cotejaron 11 archivos Markdown en corpus/reports-v2: cinco previos y seis
nuevos. Frente a la meta editorial de 31, restan 20 por redactar. Este conteo
no acredita once reports validados. El recibo SOCIAL N=2 seguía pendiente en
el documento 07; este pase no obtuvo evidencia de su cierre.

## Decisión que permite y siguiente trabajo

La mesa puede dejar de esperar integración y orientar la siguiente tanda a:
recibos de productos/C2 sobre identidades finales; diagnóstico y resolución
de discrepancias C1; ejecución de los paquetes preparados después de resolver
los requisitos de firma y del comparador; tratamiento de los 48 impedimentos.
Son recomendaciones del ejecutor, no nuevos encargos autorizados.

Pago digital conserva SUSPENDIDO/NO-ESTIMABLE. COMMIT-3 sigue cerrado. Las seis
familias congeladas no acreditan atestación externa ni autorización de apertura.
La exposición de trabajo/movilidad queda documentada: retirar contenido no
restablece ceguera ni autoriza retroactivamente su lectura.

El comentario NO-FUSIONAR de Claude en #1182 revisó `7f0c4370`; el HEAD final
fusionado es `70e7ea19`. No se trasladan automáticamente sus bloqueos mecánicos
anteriores al HEAD final, ni se infiere un recibo nuevo de su fusión. #1184 sí
tiene comentario FUSIONABLE-CON-RESERVA sobre su mismo HEAD final `3effe094`.
No se localizaron comentarios/reviews acreditando los recibos restantes en las
seis PR consultadas; esta búsqueda no descarta expedientes en otro circuito.

## Alcance de la verificación

EJECUTADO: consultas GitHub de estado, merge, HEAD, controles y comentarios de
las seis PR; conteo de archivos de reports y sumas del resumen C1 consolidado.
LEÍDO: descripciones finales de entregas y resumen C1. Las pruebas de productores,
mutaciones, clon limpio y replays son antecedentes declarados por sus autores
y CI; este pase no los ejecutó de nuevo. No es un recibo formal de Claude ni
una auditoría de metodología o código completa.

## NO-CORRIDO / RESERVAS

| Qué | Razón | Impacto | Sucesor |
|---|---|---|---|
| Replays CAJA y recálculo de microdatos | DIFERIDO-A: circuito técnico C1/C2 | Este dictamen verifica entregas, no valida cifras por réplica propia | Recibos técnicos y continuidad C1 |
| Recibos independientes sobre productos y C2 finales | DIFERIDO-A: GEN2-RECIBO-ASTRA-PRODUCTO-N por circuito de mesa | Integración no acredita aceptación sustantiva | Paquetes recibo-para-claude de cada entrega |
| Adjudicación de exposición y propuestas de firmas | DECISIÓN-DE-MESA-PENDIENTE | No se concede permiso retroactivo ni apertura | Mesa sobre expedientes integrados |
| Atestación externa / COMMIT-3 | DIFERIDO-A: autorización explícita futura | Ningún envío ni sello temporal externo acreditado | Circuito autorizado por mesa |
