# Encargo 22 · validación independiente de tres R ENVIPE

ENTORNO: CAJA
RAMA SUGERIDA: acto/gen2-validacion-r-envipe-22
MODELOS: cero llamadas nuevas.

## Resultado útil y autoridad

Resolver NC-0096 mediante una reconstrucción independiente de las tres referencias R de ENVIPE 2021/2023/2024: punto, numerador/denominador, incertidumbre y alcance del diseño. El control histórico ya reprodujo los puntos; falta la validación formal que la fila distingue expresamente de ese control. NC-0092, su dependencia de adopción en el duelo, ya está cerrada. No es otra firma que haya que solicitar.

Este encargo concreta la solicitud de Jonás de avanzar los trabajos independientes de nuevas firmas y revisar los candados. Al entregarlo al ejecutor autoriza implementación de validación, ejecución en corpus, commits, push y PR. No autoriza nuevas capturas, elegir una receta por cercanía a Gen1, reescribir R congelados ni firmar su uso en un consumidor nuevo.

## Fase 1 · delimitar el objeto y fijar el contraste

Leer `AGENTS.md`, `.claude/commands/acto.md`, el encargo y:

- NC-0096 y NC-0092 en `forense/no-corrido.tsv`;
- `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md`;
- `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv` y la decisión posterior que resolvió su firma;
- `data/corrida0/CALC-R-CIV-M-10/`, `CALC-R-CIV-M-12/`, `CALC-R-CIV-M-13/`: contratos e identidades;
- `forense/notas/2026-09-09-GEN2-R-SERIE-CSV-cierre.md`;
- contrato y evidencia de `tools/valida_envipe_independiente.py`, sólo para determinar qué se puede reutilizar sin compartir la aritmética decisiva.

Reportar worktree absoluto, rama, HEAD, estado y resolución de corpus. Corte #707: `cd92cb25acbb7b645a4b49ed180f042661d18e7e`. Comprobar que un PR posterior no haya resuelto precisamente NC-0096.

**#697 validó ocho olas distintas y cerró NC-0155; no cierra estos tres R.** No repetir aquellas ocho mediciones. El objetivo tampoco son CIV-M-01/02/04.

| Celda | Encuesta | Periodo de hechos | Payload |
|---|---|---|---|
| CIV-M-10 | ENVIPE 2021 | 2020 | `envipe2021_csv` |
| CIV-M-12 | ENVIPE 2023 | 2022 | `envipe2023_csv` |
| CIV-M-13 | ENVIPE 2024 | 2023 | `envipe2024_csv` |

Fijar y fechar el protocolo de validación antes de producir comparaciones nuevas: fuentes, definición, algoritmo independiente, tratamiento de diseño y tolerancias justificadas por precisión/unidad. Los resultados históricos son visibles; declarar esa exposición y no llamar ciego a este ejercicio ni presentarlo como una hipótesis original pre-registrada.

## Fase 2 · reconstruir la medición sin reutilizar la función decisiva

Resolver por identidad y hash los payloads; verificar cuestionario, diccionario y miembro exacto de cada ZIP. Escribir el cálculo desde la definición y documentación, sin importar/copiar la función del medidor, `tools/arbitra.py` o `tests/svystat.py:prop_ultimate_cluster` como motor de la validación. Se pueden reutilizar resolución de archivos, lectura genérica y utilidades no decisivas. Documentar qué se reutilizó.

Contrato primario U_R a verificar contra las fuentes: unidad DELITO, todos los tipos `BPCOD` 01–15, `BP1_23` válido 01–09, positivo 01/02/06 y negativo 03/04/05/07/08/09, 99/blanco excluidos; `FAC_DEL` válido como ponderador y `EST_DIS`/`UPM_DIS` como variables de diseño. No agregar el filtro `BP1_20=2` por copiar el estimando secundario de delitos personales. No sustituir por `FAC_DEL_AM` ni ponderación de personas. Mantener identificadores de diseño como cadenas opacas, sin normalizarlos por una conjetura numérica.

Entregar por ola el embudo, frecuencias de codificación, descartes, n, sumas ponderadas del numerador/denominador y punto. Preservar diferencia entre encuesta y año de hechos. Si la fuente contradice materialmente el contrato, documentar la discrepancia y su efecto por separado; no «reparar» los congelados ni decidir qué definición produce un número más deseable.

Antes de comparar con el productor, probar el algoritmo independiente con ejemplos pequeños de resultado calculable: pesos desiguales, exclusiones 99/blanco, varios delitos por persona, agrupación por estrato/UPM y un estrato con una sola UPM. No fijar como único oráculo los números del cálculo que se está validando.

## Fase 3 · incertidumbre: reproducción y suficiencia del diseño

Separar dos preguntas: (1) si el algoritmo declarado reproduce la varianza publicada; (2) si esa varianza está sustentada para el estimando y el diseño observado. Igualar un EE no acredita por sí solo la segunda.

Reconstruir el EE por una vía independiente documentada; contrastar intervalos y CV según la definición histórica, con diagnósticos de estratos/UPM y tamaños. Usar documentación metodológica primaria al fundamentar una alternativa. No traer el bootstrap Gen1 con semilla diferente como comparación equivalente del EE.

Las tres corridas declaran `IC-CON-ESTRATOS-DE-UPM-UNICA`. Examinar los estratos con UPM única: si son unidades de certeza acreditadas, si aparecen al restringir el dominio o si falta información de diseño. Cuando el dominio elimina otras UPM, comprobar si los datos disponibles permiten conservar las unidades del diseño completo con contribución cero al dominio. No imputar su existencia o sus identificadores sin evidencia.

Si la regla histórica da varianza cero a un estrato, reproducirla como contrato histórico cuando corresponda y distinguir su limitación. No calificar el IC como conservador o límite inferior garantizado por mera intuición. Si no se puede acreditar el diseño completo, señalar exactamente qué componente impide validar el uso inferencial; conservar el punto validado y la comparación numérica como resultados útiles.

Un desacuerdo material requiere localizar si procede de identidad, filtros, pesos, aritmética, dominio o información ausente. Terminar la demostración con datos diagnósticos agregados y, si corresponde, una propuesta sucesora reproducible que cambie sólo el componente identificado. No escoger la alternativa según su cercanía a R ni sustituir retrospectivamente el árbitro del duelo.

## Fase 4 · informe y cadena de cierre

Entregar una tabla por celda: identidad, n, numerador, denominador, punto, EE, IC/CV, diferencia contra productor, diagnóstico de diseño y veredicto de alcance. Distinguir `concordancia numérica`, `validación del punto` y `aptitud inferencial`; un hallazgo de insuficiencia no se resume como «todo validado».

Conservar código y evidencia de esta validación en un directorio nuevo; los insumos y outputs congelados de los tres CALC no se editan. Vincular la validación mediante el mecanismo vigente y el contrato de 17 cuando esté integrado. El trabajo matemático no espera a 17; no implementar en paralelo otro registro/resolver. Si falta únicamente integrar el enlace, entregar los artefactos completos y conciliarlo al actualizar la rama.

NC-0096 puede cerrarse por validación formal ejecutada con veredicto completo, no por contador o coincidencia del punto. Si una limitación deja sin cumplir parte de la obligación, mantener ese alcance explícito o su residual referenciado. «Validación ejecutada y detectó un defecto» no significa «resultado aprobado». No usar el cierre administrativo para elevar el estado de aptitud. Si nace una decisión metodológica nueva, entregar opciones con impacto y continuar todo lo independiente.

19 puede citar este resultado en diagnóstico actual, conservando qué R y qué evidencia existían en cada evaluación histórica. No reemitir el marcador, snapshots ni capturas. La validación tampoco convierte un dato usado como árbitro en evidencia retenida para entrenar o ajustar el competidor.

## Aceptación y concurrencia

Tres puntos reconstruidos, incertidumbre contrastada y límites de diseño examinados, código independiente de la función decisiva y evidencia reproducible; uso permitido/residual inequívoco. Ningún valor Gen1 entra como objetivo de optimización. Ningún congelado se modifica.

Usar corpus compartido en lectura y salidas propias; no escribir pruebas sobre el árbol científico real. No correr por inercia todas las series ni todos los bootstraps históricos. Archivar por el procedimiento vigente y actualizar sólo filas afectadas, sobre main reciente, preservando cambios ajenos. Entregar PR/HEAD, comando de reproducción y `obligación | evidencia | alcance | cierre/residual`. El merge queda con Jonás.


**Actualización al entregar:** #708 también está fusionado; main=`e7a471bf1499a096abbe58dc298f02243e885135`. Archiva el benchmark sin firmar sus cuatro decisiones; no cambia el alcance de este encargo.
