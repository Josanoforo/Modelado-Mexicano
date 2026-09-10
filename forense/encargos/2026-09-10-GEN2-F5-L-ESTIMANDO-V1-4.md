# ENCARGO · GEN2-F5-L-ESTIMANDO-V1-4

**SHA de redacción:** `e81aa27` (`origin/main` posterior al merge de PR #683).

**Entorno asignado:** NUBE/Ubuntu, repo-only; cero llamadas a Claude.

**Estado:** VIVO hasta que se abra el PR de este acto.

## ARRANQUE

Worktree limpio creado desde `origin/main` en
`/home/pc0/mm-gen2-f5-l-estimando-v1-4`, rama
`acto/gen2-f5-l-estimando-v1-4`, HEAD `e81aa27`.

## VERIFICACIÓN DE EXISTENCIA (A.8)

1. **Estructura:** existen `L-spec-v1_3.json`,
   `marco-M-sorteado-v1_3.tsv`, `codificacion-R-v1_2.tsv`, los 14 árbitros R
   activos, `paquete-corpus-F5-v1_0` y `NC-0146` abierta.
2. **Contenido:** v1.3 contiene ocho universos `NO ESTIMADO EN ESTE ACTO` y
   tres TRA con `paga_mordida_encig2025`; los R activos definen universos y
   eventos distintos y explícitos.
3. **Cobertura retroactiva:** las capturas y `CALC-TRIADA-0001` históricos se
   conservan; este acto crea solo contrato prospectivo y diagnóstico.

Texto recibido de mesa el 10/sep/2026, archivado íntegro:

> # ENCARGO · GEN2-F5-L-ESTIMANDO-V1-4
>
> ## OBJETIVO
>
> Construir y sellar un contrato sucesor de preguntas para el corredor L que corrija la desalineación semántica descubierta después de `CALC-TRIADA-0001`.
>
> Este acto NO corre L, NO llama Claude, NO calcula errores contra R y NO adjudica TRIADA.
>
> Su producto debe dejar lista una recaptura prospectiva y mínima.
>
> Partir de `main` posterior al merge de PR #683.
>
> ---
>
> ## HALLAZGO MATERIAL DE PARTIDA
>
> `CALC-TRIADA-0001` dejó:
>
> * `UR = 14/14`;
> * `L_SOLO`: 6/14 celdas con punto;
> * `L_CORPUS`: 3/14 celdas con punto;
> * `M`: 14/14;
> * `U3 = 3/14`.
>
> Las ocho celdas sin punto L_SOLO son:
>
> * CIV-M-01
> * CIV-M-02
> * CIV-M-04
> * CIV-M-10
> * CIV-M-12
> * CIV-M-13
> * DIN-M-01
> * FAM-M-01
>
> Esas mismas ocho aparecen en `L-spec-v1_3.json` con:
>
> `universo = "NO ESTIMADO EN ESTE ACTO ... censo de existencia..."`
>
> Además, las tres TRA:
>
> * TRA-M-02
> * TRA-M-03
> * TRA-M-07
>
> usan como `conducta` el alias de consumidor:
>
> `paga_mordida_encig2025`
>
> aunque las celdas corresponden a ENCUCI 2020 y ENCIG 2013/2021.
>
> Capturas reales de L muestran que esa incoherencia fue utilizada explícitamente como razón de abstención.
>
> Por tanto, la hipótesis operativa de este acto es:
>
> > La cobertura insuficiente de L está parcialmente causada por una desalineación entre la pregunta entregada a L y el estimando primario que R realmente arbitra.
>
> Este acto prueba y corrige esa identidad semántica. No presupone que corregirla vaya a producir una cifra.
>
> ---
>
> # P1 · CENSO DE IDENTIDAD SEMÁNTICA 14/14
>
> Construye una tabla para las 14 celdas:
>
> | id | pregunta v1.3 | estimando primario R | universo R | evento binario R | alineación | defecto | recaptura necesaria |
> | -- | ------------- | -------------------- | ---------- | ---------------- | ---------- | ------- | ------------------- |
>
> Clasifica `alineación` únicamente como:
>
> * `ALINEADA`
> * `DESALINEADA-MATERIAL`
> * `DUDOSA-REQUIERE-MESA`
>
> Una desalineación es MATERIAL si puede hacer que L responda sobre un objeto distinto, no sepa qué denominador usar o interprete que no debe estimar.
>
> No uses como criterio si L acertó o se equivocó contra R.
>
> ## FUENTES
>
> Puedes leer:
>
> * `L-spec-v1_3.json`;
> * `marco-M-sorteado-v1_3.tsv`;
> * specs activas de `CALC-R-*`;
> * `codificacion-R-v1_2.tsv`;
> * fichas/diccionarios ya citados por esas specs;
> * textos crudos de `corridas-L/*__v1_3.json` únicamente para documentar razones de abstención.
>
> ### PROHIBIDO PARA REDACTAR EL NUEVO TARGET
>
> No copies ni uses:
>
> * punto R;
> * EE/IC de R;
> * punto M;
> * errores TRIADA;
> * ranking;
> * valores observados del desenlace;
> * conteos `sí/no` que permitan reconstruir aproximadamente el punto;
> * ninguna cifra de `resultados.json` como información del prompt.
>
> Si una spec activa contiene esas cifras mezcladas con descripción estructural, extrae únicamente la definición del estimando.
>
> ---
>
> # P2 · TARGET CARD LIMPIA PARA 14/14
>
> Crea una fuente sucesora explícita, por ejemplo:
>
> `forense/prereg-duelo-v2/L-estimandos-v1_4.tsv`
>
> con una fila por celda y al menos:
>
> * `id`
> * `encuesta`
> * `ola`
> * `unidad_observacion`
> * `universo_L`
> * `evento_L`
> * `escala`
> * `fuente_definicion`
> * `cambio_vs_v1_3`
> * `requiere_recaptura`
>
> La regla fundamental es:
>
> > L debe recibir la definición humana del MISMO estimando primario que R evalúa, pero nunca su respuesta.
>
> ### CIV-M-*
>
> No uses el alias ambiguo `denuncia_con_miedo_o_desconfianza`.
>
> La target card debe representar exactamente la construcción primaria de BP1_23 que el R activo arbitra: mismo universo, misma unidad y misma partición conceptual entre miedo/extorsión/desconfianza y las demás razones válidas de no denuncia.
>
> Tradúcela a lenguaje humano. No expongas el punto observado.
>
> ### DIN-M-01
>
> Sustituye el placeholder por el universo y evento real de `cr27 / TIENE AHORROS`, conforme al R activo.
>
> No copies los conteos observados de respuestas.
>
> ### FAM-M-01
>
> Sustituye el placeholder por el universo y significado real de `p9_9_4`, conforme al diccionario/R activo.
>
> Usa la redacción o significado del reactivo, no únicamente el alias interno del motor.
>
> ### FAM-M-05/06/07
>
> Preserva su significado actual si P1 confirma que ya está alineado.
>
> No cambies una pregunta que ya representa correctamente el estimando solo para uniformar estilo.
>
> ### TRA-M-02/03/07
>
> NO uses `paga_mordida_encig2025` como texto de la conducta.
>
> Ese nombre pertenece al consumidor/modelo, no es la definición del estimando de estas tres celdas.
>
> Redacta cada target a partir de su reactivo real:
>
> * TRA-M-02: construcción real `AP5_17 | AP5_18` de ENCUCI 2020;
> * TRA-M-03: reactivo real `P8_3` de ENCIG 2013;
> * TRA-M-07: reactivo real `P8_3_1` de ENCIG 2021.
>
> Conserva las diferencias semánticas reales entre ENCUCI y ENCIG. No colapses “solicitud”, “entrega/pago”, “experiencia de corrupción” o cualquier otro concepto si los instrumentos no son iguales.
>
> ---
>
> # P3 · L-SPEC v1.4
>
> Genera:
>
> `forense/prereg-duelo-v2/L-spec-v1_4.json`
>
> como SUCESORA.
>
> NO editar:
>
> * `L-spec-v1_3.json`;
> * `F5-contrato-triada-spec-v1_1.md`;
> * capturas v1.3;
> * `CALC-TRIADA-0001`;
> * ningún resultado histórico.
>
> La nueva pregunta debe seguir la misma plantilla básica del corredor L y conservar la regla de honestidad epistémica:
>
> * pedir mejor estimación puntual;
> * permitir abstención si realmente no hay base;
> * NO obligar a inventar una cifra.
>
> No queremos “arreglar” cobertura forzando respuestas. Queremos arreglar el objeto que se le pide estimar.
>
> ---
>
> # P4 · GUARDIAS DEL DEFECTO OBSERVADO
>
> Añade una validación pequeña y barata porque este defecto sí cambió materialmente la medición.
>
> Como mínimo, `L-spec-v1_4` debe fallar validación si:
>
> 1. alguna celda contiene `NO ESTIMADO EN ESTE ACTO` como universo;
> 2. una TRA usa `paga_mordida_encig2025` como definición entregada a L;
> 3. falta universo o evento explícito;
> 4. no existen exactamente 14 ids;
> 5. los ids difieren del marco congelado 14/14.
>
> No conviertas esto en framework de gobernanza.
>
> ---
>
> # P5 · CONJUNTO DE RECAPTURA
>
> Deriva mecánicamente `requiere_recaptura`.
>
> Regla:
>
> * si la semántica entregada a L cambia materialmente respecto de v1.3 → recapturar AMBOS brazos de esa celda;
> * si no cambia materialmente → reutilizar las capturas v1.3 en el futuro sucesor.
>
> Recapturar ambos brazos evita comparar dentro de una misma celda:
>
> * `L_SOLO` con prompt viejo
>   contra
> * `L_CORPUS` con prompt nuevo.
>
> Reporta:
>
> * número de celdas a recapturar;
> * número futuro de invocaciones = `celdas × 2 × k=8`.
>
> **NO ejecutes esas invocaciones en este acto.**
>
> No invoques `claude -p`.
>
> ---
>
> # P6 · CORPUS, SOLO DIAGNÓSTICO MÍNIMO
>
> Para las celdas marcadas para recaptura, verifica mecánicamente que el ensamblado de `L+corpus` actual puede construirse con `paquete-corpus-F5-v1_0`.
>
> Reporta por celda:
>
> * documentos disponibles;
> * documentos efectivamente incluidos antes del límite;
> * chars incluidos;
> * truncado sí/no;
> * existencia de al menos una mención del nombre de encuesta;
> * existencia de mención conjunta de encuesta + ola;
> * existencia de evidencia directamente relacionada con el evento objetivo: `SI / NO / DUDOSA`.
>
> Esta última clasificación es EXPLORATORIA.
>
> No reconstruyas el paquete, no cambies el límite de 600k y no implementes retrieval nuevo en este acto.
>
> La finalidad es decidir después si la próxima recaptura puede usar el mismo corpus o necesita una spec sucesora de acceso documental.
>
> ---
>
> # P7 · DECISIÓN OPERATIVA
>
> El cierre debe producir una de estas tres recomendaciones:
>
> ### A · `LISTO-PARA-RECAPTURA-v1_4`
>
> Si el principal defecto era semántico y el corpus actual sigue siendo un tratamiento válido para la pregunta del experimento.
>
> ### B · `REQUIERE-CORPUS-SUCESOR-ANTES-DE-RECAPTURA`
>
> Si corregir la pregunta pero mantener el ensamblado actual haría que `L+corpus` siga recibiendo un tratamiento materialmente defectuoso, por ejemplo porque el corpus prometido existe pero el runner sistemáticamente no entrega información pertinente por su construcción.
>
> ### C · `DECISION-DE-MESA-PENDIENTE`
>
> Solo si existe una elección epistemológica real que no pueda resolverse mecánicamente.
>
> No uses C para ambigüedades menores.
>
> ---
>
> # P8 · NC-0146
>
> NO cierres `NC-0146`.
>
> Actualízala únicamente si P1 demuestra la causa material.
>
> Debe quedar claro que:
>
> * el `CALC-TRIADA-0001` histórico permanece válido bajo su spec sellada;
> * no se reescribe su resultado `SIN-GANADOR-UNICO`;
> * este acto explica por qué aquella cobertura no basta para adjudicar la pregunta central;
> * el sucesor es la recaptura bajo contrato semántico limpio o, si P7=B, primero el corpus sucesor.
>
> No crear otra NC salvo que aparezca un bloqueo material distinto y realmente independiente.
>
> `NC-0147` queda fuera de perímetro: no calculamos ninguna nueva banda ni adjudicación en este acto.
>
> ---
>
> # PERÍMETRO
>
> Permitido:
>
> * nueva target card v1.4;
> * nueva `L-spec-v1_4.json`;
> * generador/validador sucesor mínimo;
> * diagnóstico de corpus;
> * nota de cierre;
> * actualización acotada de `NC-0146`;
> * encargo archivado;
> * cascada mínima exigida por las reglas actuales del repo.
>
> Prohibido:
>
> * modificar v1.3;
> * modificar capturas históricas;
> * modificar extractor v1.3;
> * modificar R o M;
> * modificar `milpa/`;
> * recalcular TRIADA;
> * recapturar L;
> * tocar `NC-0147` o `NC-0148`;
> * reparar infraestructura incidental.
>
> ---
>
> # VERIFICACIÓN
>
> Ejecuta:
>
> * validación de 14/14 targets;
> * diff semántico v1.3 → v1.4;
> * dry-run del mecanismo que una futura recaptura utilizará, SIN modelo;
> * tests existentes relevantes;
> * `tests/check.py --baseline`, aislando/restaurando el efecto lateral conocido de `NC-0141`.
>
> No necesitas dejar verde ningún fallo heredado no relacionado.
>
> ---
>
> # ENTREGA
>
> Abre UN PR contra `main`.
>
> NO fusiones.
>
> El cuerpo del PR debe comenzar con:
>
> 1. `VEREDICTO DE CAUSA DE COBERTURA`;
> 2. tabla 14/14 de alineación;
> 3. celdas que requieren recaptura;
> 4. número de futuras invocaciones;
> 5. veredicto P7 A/B/C;
> 6. qué cambió en `L-spec-v1_4`;
> 7. qué NO se ejecutó;
> 8. estado de `NC-0146`;
> 9. tests.
>
> Al terminar devuelve el número de PR y detente.
