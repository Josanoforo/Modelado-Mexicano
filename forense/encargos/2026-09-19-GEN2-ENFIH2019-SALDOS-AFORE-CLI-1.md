# GEN2-ENFIH2019-SALDOS-AFORE-CLI-1

## Mandato

Ejecuta en CAJA local, repositorio Josanoforo/Modelado-Mexicano. Mide cuánto saldo AFORE reportan los hogares, cómo se distribuye entre tenedores y cuánto puede afirmarse dadas las respuestas desconocidas. Entrega medición, CALC sellado, análisis sustantivo y PR. Pegar este encargo autoriza commit, push y apertura del PR; no merge, adopción ni cambios de gobierno.

Rama propia: `codex/gen2-enfih2019-saldos-afore-cli-1`. CALC propuesto: `CALC-ENFIH2019-SALDOS-AFORE-0001`, sujeto a comprobar unicidad y duplicados por contenido antes de congelar. Inicia worktree desde origin/main actualizado y reporta ruta absoluta, rama, HEAD y estado. Lee AGENTS.md y normas aplicables.

Base revisada: `8e455bd6a3870566d6776fef19834c4da16d2fa9`, 19/sep/2026. CALC-ENFIH-0001 ya está ejecutado y sellado: mide tenencia C_AFORE, sensibilidad H_PPAL y perfil por CAT_POS. Repetir esos resultados no constituye este encargo. C_AFORE es condición de tenencia; V_AFORE es el candidato de valor monetario cuya definición, tratamiento de desconocidos e imputación deben acreditarse en el diccionario antes de abrir respuestas.

## Aporte y límites

Separar cobertura de cuentas y distribución de saldos. Apoya la evaluación descriptiva de `dinero.planeacion.formal_estable`, pero no valida esa interpretación conductual ni sustituye sus proporciones selladas. Tener cuenta o saldo no identifica planeación, aportaciones voluntarias, flujo anual de ahorro ni estabilidad laboral. CAT_POS no es formalidad: no producir una tasa de formalidad con él.

La unidad primaria es hogar. No denominar estos resultados saldo individual de trabajadores ni promedios por cuenta. No construir serie temporal con una sola ola.

## Preparación y spec

1. Busca mediciones equivalentes en demanda, CALC, notas relevantes y ramas activas por V_AFORE, saldo, monto y distribución; no basta el nombre del CALC. Consulta solo lo pertinente de CALC-ENFIH-0001, su medidor/spec/resultados, `forense/prereg-caja/ENFIH-AFORE-spec-v1_0.md` y `forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md`. Declara exposición a sus cifras, no ceguera. Un duplicado completo se referencia; completa solo resultados materialmente faltantes.
2. Resuelve `enfih2019_bd_csv_zip` y `enfih2019_fd_xlsx` en el corpus local y verifica identidad/hash. Localiza cuestionario o documentación de construcción de variables ya disponibles cuando sean necesarios. No versionar datos ni rutas privadas.
3. Acredita C_AFORE y V_AFORE de TCONCENTRADORA.csv: unidad monetaria, fecha/periodo del stock, alcance dentro del hogar, códigos especiales, ceros, imputación y cualquier intervalo en vez de monto exacto. No interpretar un código de desconocido como dinero. Si V_AFORE contiene imputación oficial, identificarla y etiquetar el estimando; no afirmar que cada monto fue declarado directamente. No buscar otra fuente por comodidad.
4. Acredita FAC_HOG, EDIS y UPM_DIS y llave FOLIO+VIV_SEL+HOGAR. Conserva diseño como texto. Congela universo, tratamientos, cuantiles, estimadores, método de IC y RESULT, spec humana/YAML, código y pruebas sintéticas en COMMIT-1 antes de abrir respuestas. El primer resultado del procedimiento se reporta. COMMIT-2 publica ejecución/sello; defectos materiales posteriores siguen sucesión y preservan intentos.

Si la documentación no acredita que V_AFORE es un monto interpretable, no publiques promedios monetarios. Acota el bloqueo con documentos precisos; no conviertas categorías en montos medios inventados. Esta condición es una comprobación de unidad material, no motivo para una auditoría general.

## Tres piezas en una medición

### A. Cobertura y calidad que definen el denominador

Universo: hogares de TCONCENTRADORA con FAC_HOG válido y positivo, con exclusiones documentadas. Mide proporciones de tenedores, no tenedores y estado desconocido; la tenencia nacional sirve como control contra CALC-ENFIH-0001, no como novedad ni sustitución de su sello.

Entre tenedores, publica n y masa con saldo conocido cero, positivo, desconocido y cualquier categoría especial acreditada. Reporta coherencia C_AFORE/V_AFORE: no tenencia con saldo positivo, tenencia con saldo cero y faltantes. No corregir incoherencias silenciosamente. Fija antes del dato qué casos permiten estimación y cuáles quedan excluidos.

Entrega cobertura de monto válido con denominador todos los tenedores, incluyendo IC de diseño cuando sustentado. La selección de quienes conocen su saldo es una reserva material de cualquier distribución condicional.

### B. Nivel y distribución de saldos

Principal: entre hogares tenedores con monto válido, media, mediana y cuantiles ponderados p25, p75 y p90, con intervalos sustentados y n/masa. Congela convención de cuantiles y tratamiento de empates. Publica también distribución entre tenedores con saldo positivo, claramente separada. No filtrar extremos, winsorizar ni eliminar ceros válidos para mejorar la presentación.

Complemento: media de saldo por hogar en el universo con estado interpretable, incorporando cero para no tenedores únicamente si el instrumento lo respalda. Los tenedores con saldo desconocido siguen desconocidos. Si hay exclusiones monetarias, esa media describe el subconjunto cubierto; no rotularla media de todos los hogares.

No extrapolar un total nacional de stock a partir de casos completos con desconocidos sin una hipótesis adicional autorizada. No imputar montos, no ajustar a precios actuales y no anualizar un stock. Expresa moneda y fecha acreditadas junto a cada tabla.

### C. Concentración del saldo observado y contraste de hogar principal

Entre tenedores con monto válido y total positivo, estima la fracción del saldo ponderado acumulada por el 10% superior de hogares de esa población, ordenados por monto. Congela una regla reproducible de fracción de peso en el umbral y empates. Publica IC de diseño si sustentado, recalculando el umbral dentro de cada réplica. No etiquetarla concentración de todos los hogares ni concentración patrimonial total.

Sensibilidad única: repetir cobertura de monto, media y mediana restringiendo a H_PPAL==1 si su catálogo confirma el filtro. Contrastes principal–sensibilidad con covarianza compartida; no son grupos independientes. No abrir perfiles por CAT_POS, ingreso, entidades o una malla adicional en esta sesión.

La lectura final debe contestar cuánto aporta saber el saldo frente a solo saber tenencia, cómo cambia la lectura entre media y mediana, qué parte domina el extremo superior y cuánto limita el desconocimiento de montos. No convertir esas diferencias en evidencia de preferencias o causalidad.

## Incertidumbre y control material

Usa diseño documentado, no bootstrap iid de hogares. Para cuantiles/concentración congela un método de réplicas apropiado al diseño, semilla, número, tratamiento de estratos singleton, degeneraciones y réplicas sin denominador. Mantén el marco y estima dominios mediante indicadores. Publica réplicas válidas; fallos no son ceros. Si un IC no es defendible, reporta punto y precisión no disponible, sin bloquear estimandos distintos.

Verifica unicidad de hogar, denominadores, estados monetarios excluyentes y completos, cuantiles monótonos, concentración entre 0 y 1, invariancia de proporciones ante escalamiento común de pesos y de concentración ante escalamiento monetario. Comprueba una media y un cuantil con cálculo independiente y una varianza representativa si publicas IC. Pruebas sintéticas para códigos monetarios especiales, empates/umbral del decil y desconocidos versus cero. No refactorizar librerías compartidas ni gastar la sesión en tests heredados.

## Perímetro y entrega

Escritura: nuevo CALC y sucesores propios; `forense/prereg-caja/ENFIH2019-SALDOS-AFORE-*`; `forense/analisis/enfih2019-saldos-afore-cli-1/`; `tests/test_enfih2019_saldos_afore.py`; copia verbatim del encargo y cierre propios; asientos propios de replay y derivados generados solo por comandos existentes.

No modificar milpa, canon, NC/FP globales, decisiones, tablero, corrida0.py, tests/check.py o workflows. No abrir reservas ENIF2024/ENCIG2025/ENVIPE2025 ni pilotos ciegos. No tocar las sesiones ENUT ni ENIGH. Codex entrega mediciones y reservas propias; Claude hace recibo y enlace. Contador/adopción PENDIENTE-DE-MESA; ninguna firma inventada. Auditoría alrededor del 20% salvo riesgos que cambien números.

Publica con preflight, sellado, replay dirigido y registro por interfaz vigente. No aceptar cambios de replay ajeno mediante --lote. Si una compuerta ajena impide generar vistas, conserva el CALC y entrega PR con publicación pendiente y evidencia concreta, sin afirmar adopción, uso activo o registro exitoso. No arreglar gobierno para conseguir verde. Regenerar vistas compartidas sobre la base actual cuando corresponda; no resolverlas a mano. La segunda proyección debe ser estable.

Entrega tablas, RESULT→significado→universo, código/spec, hashes, ejecución/sello/replay, interpretación y reservas de cobertura. Incluye CONSUMIDO y NO-CORRIDO / RESERVAS, pruebas ejecutadas, URL de PR y SHA. Explica qué puede decidir mesa y qué falta para consumo. No fusionar.

## A.8 · Verificación de medición previa (salida añadida al ejecutar)

Comando: `python3 tools/ya_medido.py dinero.planeacion.formal_estable`

```text
=== ya_medido: dinero.planeacion.formal_estable ===
  resuelto por canon: dinero.planeacion.formal_estable -> R1.2 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): dinero.planeacion.formal_estable, R1.2

-- milpa/tramite.yaml --
  milpa/tramite.yaml:938  situacion=SELLADA tier=FUERTE p=0.538502  [TASA-EJECUTADA]
      id: dinero.planeacion.formal_estable

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:319  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.538502  [TASA-EJECUTADA]
      id: dinero.planeacion.formal_estable

-- data/corrida0 (RESULT + ejecución + sello) --
  data/corrida0/CALC-ENFIH-0001/resultados.json:13  resultado_id=RESULT-ENFIH-A-P ejecutado=SI sello=VALIDO  [TASA-EJECUTADA]
      RESULT-ENFIH-A-P=0.5385022873715912; ejecucion=data/corrida0/CALC-ENFIH-0001/ejecucion.json:28; sello=data/corrida0/CALC-ENFIH-0001/sello.json:4
  data/corrida0/CALC-ENFIH-0001/resultados.json:14  resultado_id=RESULT-ENFIH-A-P-COMPLEMENTO ejecutado=SI sello=VALIDO  [TASA-EJECUTADA]
      RESULT-ENFIH-A-P-COMPLEMENTO=0.46149771262840883; ejecucion=data/corrida0/CALC-ENFIH-0001/ejecucion.json:28; sello=data/corrida0/CALC-ENFIH-0001/sello.json:4

========================================
MEDIDA-EN: CALC-ENFIH-0001, tramite-ola5-propuesta-v0.yaml, tramite.yaml
```

El cuerpo anterior a este apéndice conserva verbatim el encargo recibido. La salida acredita que la tasa de tenencia ya estaba medida; este acto no la presenta como novedad y aporta únicamente cobertura y distribución de saldos.
