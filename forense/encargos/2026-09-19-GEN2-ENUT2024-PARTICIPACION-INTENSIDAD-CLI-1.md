# GEN2-ENUT2024-PARTICIPACION-INTENSIDAD-CLI-1

## Mandato

Ejecuta en CAJA local, repositorio Josanoforo/Modelado-Mexicano. Produce una medición completa de participación e intensidad del cuidado por sexo y edad, con incertidumbre de diseño, CALC sellado y PR. Este encargo autoriza commit, push y apertura de PR; no merge ni adopción. Codex mide; Claude recibe, gobierna e integra el motor; mesa decide adopción.

Rama propia: `codex/gen2-enut2024-participacion-intensidad-cli-1`. CALC propuesto: `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001`; comprueba unicidad y equivalencia de contenido antes de congelar. Un worktree por sesión, desde origin/main actualizado; informa ruta absoluta, rama, HEAD y estado. Lee AGENTS.md e instrucciones aplicables.

Base revisada: `8e455bd6a3870566d6776fef19834c4da16d2fa9`, 19/sep/2026. En esa base CALC-ENUT-0001 YA tiene ejecución y sello: su texto histórico de medidor ausente está desactualizado. Su resultado principal es una participación de horas de mujeres de 40+ con ponderación de hogar; sus secundarios incluyen variante SIN_CP y participación poblacional. No repetir esa corrida ni sobrescribirla.

## Pregunta y aporte

¿Las diferencias de carga de cuidado por sexo y edad se explican descriptivamente por cuántas personas participan, por cuánto tiempo dedican quienes participan, o por ambas cosas? Entrega las tres cantidades compatibles: P(h>0), E(h) y E(h | h>0), más contrastes mujeres–hombres dentro de tramos de edad.

Es ampliación descriptiva de la familia `familia.cuidado.recae_mujeres_40mas`; NO relevo automático del RESULT anterior. Unidad persona y FAC_PER no son intercambiables con el estimando de hogar de CALC-ENUT-0001. La identidad E(h)=P(h>0)×E(h|h>0) es contable, no causal. No estimar efectos del género ni preferencias familiares.

## Reconocimiento dirigido y congelamiento

1. Consulta demanda vigente y busca equivalentes por contenido en main y ramas activas: participación, horas, cuidado, sexo, edad. Lee CALC-ENUT-0001/spec.*, resultados y medidor; `tools/medidor_cuidado_enut.py`, `forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md` y el bloque pertinente de milpa/tramite.yaml, solo lectura. Ya existen descriptores GEN1 por sexo/edad: declara exposición previa, reutiliza sus cortes documentados si son compatibles y distingue reestimación GEN2 de novedad. Si ya existe exactamente el resultado pedido, referéncialo y completa únicamente lo faltante.
2. Localiza `enut2024_bd_csv` y `enut2024_fd_xlsx` mediante manifiesto/configuración vigente del corpus. Verifica identidad y hash. Una ruta sin configurar no significa payload ausente. Usa corpus compartido sin versionar microdatos ni rutas privadas.
3. Acredita en documentación universo de edad, periodo de horas, llave persona, SEXO, EDAD, FAC_PER, EST_DIS y UPM_DIS. Conserva identificadores de diseño como texto. No inventes la llave ni el universo por el nombre del archivo.
4. Congela spec humana y YAML, RESULT previstos, medidor y pruebas sintéticas en COMMIT-1 antes de abrir respuestas. Declara resultados históricos conocidos; no reclamar ceguera. Fija faltantes, códigos especiales, cortes, contrastes y método de IC. El primer resultado del procedimiento es el reportado. COMMIT-2 entrega ejecución, resultados y sello. Una corrección material posterior conserva el intento y sigue la sucesión vigente.

## Medición integrada

Define h para la misma familia de cuidado del precedente, a partir de TVAR_CREA y documentación: CUID_ESP_INT_HOG_CON_CP, CUID_INT_0A5_CON_CP, CUID_INT_6A14_CON_CP y CUID_INT_60MAS_CON_CP. Verifica unidades y semántica antes de congelar. El precedente excluye CUID_INT_15A59 del agregado CON_CP por no tener variante equivalente: conserva esa delimitación explícita, no lo vendas como todo el cuidado.

La suma con cuidados pasivos puede incluir simultaneidad: se reporta como agregado de horas declaradas de esas actividades; no como tiempo exclusivo del reloj ni jornada libre. No capar en 168 horas ni borrar extremos sin regla documental. Publica incidencia de valores incompatibles con la documentación y su tratamiento previamente fijado.

Calcula, con FAC_PER y sobre un universo válido común:

- Nacional, por sexo y por los tramos de edad del precedente: participación h>0, media de h incluyendo ceros válidos, media entre participantes, n y masa ponderada de cada denominador.
- Cruce sexo×tramo de edad con las tres medidas. Sin extender a ocupación, entidades o una malla de seis ejes.
- Contrastes mujeres–hombres de cada medida en cada tramo y en el total, con covarianza de diseño. No deducir la significación restando extremos de IC separados.
- Como sensibilidad preespecificada, repetir las tres medidas usando las variantes SIN_CP documentadas y homologables de las mismas actividades, con sus diferencias pareadas frente a CON_CP. No llamar cuidado activo a SIN_CP si el diccionario no acredita esa interpretación. Si no hay equivalencia documental de una actividad, limitar y etiquetar la sensibilidad; el principal sigue.

No reemplazar faltantes por cero. Distinguir ceros genuinos, no aplicabilidad y no respuesta según catálogo. Informar cobertura válida por grupo. Si se requiere un join, acreditar cardinalidad y ausencia de expansión; nunca escoger un FAC_PER arbitrario por hogar. No usar FAC_HOG para estos estimandos de persona.

Publica tablas largas legibles y RESULT estructurados compatibles con el contrato vigente. Incluye todos los grupos congelados; un denominador vacío da estado no estimable, no cero.

## Incertidumbre y verificación suficiente

Usa el diseño documentado y estimación de dominios conservando el marco de UPM/estratos. Un único plan de réplicas compartido puede cubrir medias, razones y contrastes; congela algoritmo, semilla, cantidad y tratamiento de estratos de UPM única. No bootstrap iid de personas. Si el diseño no permite un IC, conserva el punto y declara precisión no disponible para ese resultado.

Comprueba la identidad contable con pesos y cobertura idénticos, reconciliación de denominadores, medias nacionales contra agregación de grupos exhaustivos, diferencias calculadas con el mismo plan y una estimación/varianza representativa por una vía independiente. Pruebas sintéticas dirigidas a ceros versus faltantes, cambio hogar/persona y participantes ausentes. No suite general por inercia ni nueva infraestructura estadística global.

La nota sustantiva debe responder dónde aparecen las brechas y si predominan diferencias de participación o intensidad, con sus límites. Esa lectura es descriptiva; no hace falta una descomposición causal ni adjudicar mecanismos.

## Perímetro, publicación y cierre

Escritura: nuevo CALC y sucesores propios; `forense/prereg-caja/ENUT2024-PARTICIPACION-INTENSIDAD-*`; `forense/analisis/enut2024-participacion-intensidad-cli-1/`; `tests/test_enut2024_participacion_intensidad.py`; copia verbatim de este encargo y nota de cierre propias; asientos propios de replay; vistas derivadas exclusivamente por comandos existentes.

No modificar milpa, canon, NC/FP globales, decisiones, tablero, herramientas de corrida0, tests/check.py o workflows. No abrir pilotos ciegos ni reservas ENIF2024/ENCIG2025/ENVIPE2025. No tocar el encargo ENIGH estructural ni la sesión ENFIH saldo. Auditoría aproximadamente 20%, salvo riesgo material.

Ejecuta preflight, medición, sellado, replay dirigido y registro conforme a la interfaz vigente de la casa. No usar --lote para aceptar replay ajeno. Si el generador bloquea por transiciones ajenas, preserva resultados y entrega el PR con publicación pendiente y evidencia mínima del bloqueo, sin declarar consumos activos ni registro exitoso y sin reparar infraestructura fuera del perímetro. No cambiar decisiones ni evidencia de otras corridas. Las vistas compartidas se regeneran, nunca se mezclan a mano; una segunda proyección debe ser estable.

Contador y adopción quedan PENDIENTE-DE-MESA; no inventar firmas. Entrega PR con tablas, estimandos/universos, RESULT, hashes, ejecución/sello/replay, interpretación, validaciones y secciones CONSUMIDO y NO-CORRIDO / RESERVAS. Separa cualquier fallo heredado de defectos introducidos. Cierra con URL y SHA, qué permite decidir y qué falta para usarlo; no fusionar.
