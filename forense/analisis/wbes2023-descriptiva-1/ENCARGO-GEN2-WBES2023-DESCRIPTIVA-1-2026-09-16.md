# ENCARGO · GEN2-WBES2023-DESCRIPTIVA-1

**Entorno:** Codex CLI en CAJA. Claude Cloud sólo si dispone legítimamente del corpus y entorno; no duplicar ejecuciones.  
**Resultado:** una medición descriptiva ponderada, reproducible, de solicitudes/expectativas de pagos informales en establecimientos de México en WBES 2023, con universo, denominador y límites explícitos. Se destina a la sección descriptiva TRA admitida por F-19.

## 1. Premisa y decisión que habilita

F-19 ya excluyó R02-WBES del duelo de transferencia persona→establecimiento y admitió su uso descriptivo junto con ENCRIGE. ENCRIGE tiene producto fusionado (#826); WBES tiene microdato y documentación registrados. El nuevo resultado permitirá describir otro universo empresarial y valorar qué información aporta al informe TRA. **No validará el motor ni se mezclará numéricamente con ENCIG/ENCRIGE.**

Evidencia en el corte revisado:

- `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`, fila `R02-TRA-WBES-SOBORNO` (línea 3).
- `forense/no-corrido.tsv`, `NC-0233`, firma F-19 y uso descriptivo (buscar por ID, no por número de línea móvil).
- `data/manifiesto.yaml`: `wbes_mexico_2023_ddi_xml`, `wbes_mexico_2023_ddi_pdf`, `wbes_mexico_2023_microdato_dta_zip`, `wbes_mexico_2023_documentacion_zip`.
- Para separar los universos del informe, sólo leer la conclusión ya pública de `forense/analisis/encrige-descriptiva-1/lectura-TRA.md`; no repetir su extracción.

SHA observados, a contrastar con la versión vigente y los bytes efectivamente usados:

| Objeto | SHA-256 |
|---|---|
| DDI XML | `1d5cded32bef39cc2f129ef63c122d59e4e37b1257b36fc98bc0cc8daccad54c` |
| DDI PDF | `069fe4981e1e5d3b2d765009462fc51d24892d6593724f46a8985561b69ae603` |
| Microdato 2023 ZIP | `bc09225244f1e1274d9c9e58221acf8884512a1ab600551f98fbc0466f479f3f` |
| Documentación 2023 ZIP | `2b3b0db77f12b841814a37265db279cfcb1778c4377876b77e0a4b725a76c0f7` |

No adquirir otra vez esos objetos. No abrir panel 2010–2023, olas 2006/2010 ni WBES 2026: no hacen falta para este resultado.

## 2. Definición antes del cálculo

Lee primero cuestionario, DDI y metodología: extracción estructural de variables, categorías, filtros, pesos, cobertura y diseño. Los DDI pueden contener frecuencias; no imprimir sus estadísticas antes de fijar la especificación. Si alguna cifra ya fue vista, declararlo: sigue siendo una descripción válida, sin pretensión ciega.

Fija en la spec, con localizadores documentales:

- Unidad establecimiento, cobertura sectorial/geográfica, límites por tamaño y periodo de referencia real de cada pregunta; el año del levantamiento no define automáticamente el periodo recordado.
- Desenlace primario: proporción ponderada de establecimientos elegibles que reportan al menos una solicitud o expectativa de regalo/pago informal en la batería de interacciones utilizada por el indicador oficial de incidencia de soborno. Acreditar cuáles interacciones componen esa batería, variable por variable; no presumir nombres de códigos ni un número de trámites.
- Distinguir solicitud/expectativa de pago efectivamente realizado. El título del resultado debe decir lo que los reactivos realmente observan.
- Denominador: establecimientos con al menos una interacción elegible, conforme a la definición oficial acreditada. No usar todos los entrevistados ni interpretar ausencia de interacción como ausencia de corrupción.
- Códigos especiales, rechazos, no sabe y saltos; documentar la regla oficial de casos parcialmente observados si existe. Si no está documentada, el primario propio será: evento positivo si hay al menos un sí válido; negativo si todas las interacciones aplicables están observadas y son no; desconocido si no hay sí y falta respuesta de alguna interacción aplicable; sin interacción queda fuera. Etiquetarlo como estimando descriptivo propio, no réplica exacta del indicador oficial.
- Para el primario propio, emitir aparte masa ponderada desconocida y límites lógicos de identificación por faltantes entre expuestos: `sí/(sí+no+desconocido)` y `(sí+desconocido)/(sí+no+desconocido)`. No llamarlos IC ni sustituir por ellos la varianza de diseño. No completar desconocidos al valor que más acerque al dato publicado.
- Ponderador principal: el recomendado en la documentación para estimaciones transversales 2023; si hay varias alternativas, fijar la recomendada antes de los resultados y dar la razón. Sin recomendación inequívoca, entregar escenarios de pesos nombrados y sin ganador elegido por cifra; nunca promediarlos.
- Total nacional cubierto y desagregación por **tamaño oficial de WBES**, si la variable está acreditada. No importar los cortes de ENCRIGE ni seleccionar subgrupos según resultados. No extender a estados, sector×tamaño o regresiones.

Si no se acredita el agregado oficial, eso no impide calcular las tasas separadas de las interacciones inequívocamente documentadas, declaradas en la spec antes del dato. No improvisar un compuesto entre reactivos incompatibles. Si ninguna variable acredita pago informal, cerrar la premisa con evidencia puntual y la pieza faltante; no abrir todos los desenlaces del instrumento.

## 3. Ejecución completa

1. Buscar si un sucesor ya produjo exactamente el resultado; reutilizarlo si existe. Crear un CALC nuevo con nombre único, sugerido `CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001`, spec humana/mecánica, medidor y fixtures. No copiar un CALC sellado para editar su identidad.
2. **COMMIT 1:** spec y código probado con datos sintéticos, antes de abrir respondentes. Resolver sólo los cuatro objetos autorizados de 2023 por las raíces existentes.
3. **COMMIT 2:** ejecutar y sellar con el runner vigente. Calcular razón de totales ponderados, no media de porcentajes por trámite ni promedio simple de subgrupos. Publicar n real, suma de pesos, numerador, denominador, masa excluida/desconocida y resultado por dominio. No publicar registros individuales.
4. Usar varianza de diseño únicamente si se acreditan variables/procedimiento adecuados a WBES: estratos, UPM cuando aplique, pesos y tratamiento de estratos singulares. Reutilizar una implementación adecuada existente. Sin diseño operativo, publicar punto y `IC-DE-DISEÑO-NO-ESTIMABLE-CON-INSUMOS-DISPONIBLES`; no fabricar un IC binomial o bootstrap iid rotulado como diseño. Los límites por faltantes se mantienen separados de la incertidumbre muestral.
5. Verificar sólo este CALC; no escribir vistas globales. Comparar con la publicación oficial sólo **después** de congelar la definición y medir, si está ya disponible en la documentación autorizada. Una discrepancia conduce a revisar universo/códigos/pesos, nunca a ajustar la definición para reproducir una cifra.
6. Entregar lectura de hasta dos páginas: qué se estimó, magnitud observada, diferencia entre establecimientos expuestos y universo total, qué comparaciones de tamaño admite la precisión y qué no permite concluir. Tabla semántica WBES↔ENCRIGE: unidad, universo, interacción, evento, periodo y escala; sin resta/razón entre instrumentos ni ranking conjunto.

## 4. Pruebas y aceptación

Pruebas mínimas ligadas a riesgos materiales: ningún trámite no equivale a cero; uno positivo con otro faltante; todos negativos observados; negativo y otro aplicable faltante; pesos desiguales; denominador vacío; códigos especiales; si hay batería, evitar duplicar establecimientos. Probar conversión proporción/porcentaje. Reutilizar pruebas existentes cuando cubran el riesgo. Una corrida real y verify dirigido bastan.

Cierre pleno: CALC reproducible, tabla agregada con denominadores y reservas, y texto usable para TRA. Un punto ponderado sin IC oficial puede ser un producto descriptivo completo si la ausencia está tipada. Si falta el payload en el entorno elegido pero existe en CAJA, devolver comando de montaje/ejecución y continuar allí, sin reabrir adquisición ni declarar el estudio imposible.

## 5. Perímetro propio

- CALC nuevo `data/corrida0/CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001/`, o nombre sucesor justificado.
- `forense/analisis/wbes2023-descriptiva-1/`: tabla, lectura y correspondencia semántica.
- `tests/test_wbes2023_descriptiva.py`, sólo pruebas necesarias.
- Archivo de este encargo y nota de cierre propios, con rótulo y fecha únicos.

No editar `tools/corrida0.py` (lo trabaja L8), manifiesto, `milpa/`, CALC ajenos, panel F6 ni el informe canónico compartido. El texto descriptivo queda listo para insertar después del trámite. Sin adopciones ni modificación del contador.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ 4fff914f286021574ac0897273ee0e6971b38f04`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. Las sesiones existentes conservan ENCIG2023-AGREGADO-CONDICIONAL-1 y ENVIPE-RES0028-DERIVADO-U4-1. No intervenir sus archivos ni rehacer sus resultados. F6 mantiene su preparación y sus reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. La excepción puntual para manifiesto, si existe, se indica en el perímetro específico.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-WBES2023-DESCRIPTIVA-1 en CAJA. Autorizo la medición descriptiva WBES 2023 delimitada, spec y código comprometidos antes de abrir respondentes, CALC sucesor, pruebas, commits, push y PR; fusión conmigo. Aplica la excepción temporal de cascada. No hagas transferencia persona→establecimiento, adopciones, llamadas experimentales ni lecturas de las reservas ENIF/F6/WBES2026. Si la rama anterior de esta sesión ya se fusionó, conserva su trabajo y usa una rama sucesora desde origin/main. Entrega medición, denominadores, incertidumbre tipada y lectura TRA, no sólo una propuesta.
