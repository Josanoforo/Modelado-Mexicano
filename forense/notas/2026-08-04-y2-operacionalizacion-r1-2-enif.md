# Operacionalización pre-registrada · `R1.2` · ENIF 2024 · Encargo Y, commit 1

*(Escrita antes de correr ninguna estadística de resultado. `enif2024_csv.zip` empaqueta diccionario y microdato juntos (4 tablas: `tvivienda`, `thogar`, `tsdem`, `tmodulo`, cada una con su propio subdirectorio `diccionario_de_datos/`) — hubo que abrirlo para ver la estructura, igual que en W. Se declara, no se disimula.)*

**Umbral de la ficha (línea 44):** "**<15%** de formales estables con ingreso suficiente hacen aportación voluntaria a afore **o** contratan seguro privado."

**Premisa a verificar primero (línea 47, fila `A`): "umbral cruzado con dato CONSAR/ENIF".** CONSAR no está en disco (`grep -i consar` sobre `data/manifiesto.yaml`: una sola mención, dentro del campo `usado_para` de `enif2018_csv`, como fuente candidata citada, no como entrada de fuente propia, descargada o pendiente; `grep -i consar` sobre `data/catalogo-fuentes-v1_0.md`: cero coincidencias). **Verificado: el Umbral es evaluable con ENIF sola**, sin CONSAR — numerador y denominador completos viven en la tabla `tmodulo` de ENIF 2024. No hay PARO por esta vía.

**ENIF 2024 es transversal** (`metadatos_enif2024.txt`: levantamiento único 2024-06-24 a 2024-08-16, periodicidad trienal declarada).

## Unidad de análisis

Personas de `tmodulo.csv` (individuo, ligado a `tsdem` por `llavehog`/`llaveviv`/`n_ren`), sin restricción de edad adicional a la que ya impone el instrumento (18+, informante elegido).

## Construcción del denominador — "formales estables con ingreso suficiente"

- **Formal:** `p3_13 ∈ {1,2,3,4}` (derechohabiencia por su trabajo: IMSS, ISSSTE, ISSSTE estatal, o PEMEX/Defensa/Marina) — proxy estándar de formalidad usado en la literatura laboral mexicana (afiliación a seguridad social vía patrón). Se excluye `p3_13=5` (seguro privado de gastos médicos vía trabajo — no es la seguridad social contributiva que define "formal" en este contexto) y `p3_13=7` (carece de derecho — informal).
- **Ingreso estable:** `p3_12=1` ("¿Este ingreso es...? Fijo") — variable declarada explícitamente en el cuestionario para este propósito, no un proxy.
- **Ingreso suficiente:** la ficha no define un umbral numérico. Se declara aquí, **antes de correr nada**, un ancla externa y verificable: ingreso mensual normalizado (`p3_11a` según periodicidad de `p3_11b`) **≥ 1 salario mínimo general vigente 2024** ($248.93 MXN/día × 30.4 ≈ $7,567 MXN/mes; Resolución CONASAMI, DOF 12/dic/2023, vigente desde 1/ene/2024). Es una decisión operacional de este commit, no un dato de la ficha — declarada como tal, no oculta como si viniera del instrumento.

## Construcción del numerador — "aportación voluntaria a afore O seguro privado"

- **Afore:** `p9_3=1` ("¿realiza aportaciones voluntarias a su Afore?"). `p9_3` solo se pregunta si `p9_1=1` (tiene cuenta Afore) — filtro anidado del propio cuestionario (pág. 25, "PASE A 9.3" solo desde 9.1=Sí). Para `p9_1=2` (no tiene Afore), se define `aporta_voluntaria_afore=0` por construcción (no puede aportar voluntariamente a una cuenta que no tiene) — declarado, no inferido después de ver la distribución.
- **Seguro privado:** `p8_5_1=1` (vida) **∨** `p8_5_2=1` (gastos médicos mayores). Se excluyen deliberadamente `p8_5_3` (auto) y otras categorías de `p8_5_x` no listadas: protección de activo de corto plazo, no instrumento de planeación de horizonte largo comparable a afore/seguro de vida — misma familia conceptual que la regla evalúa (afore, seguro, hipoteca).
- **Numerador = 1 si `aporta_voluntaria_afore=1` O `seguro_privado=1`.**

## Control de "acceso efectivo" (fila `B` de la escala propia, línea 47)

La ficha distingue fila `A` (umbral cruzado, con control) de fila `B` ("tasas bajas **sin** control de acceso efectivo — ¿no planea o no puede?"). ENIF tiene las variables de motivo exactas para este control, verificadas en el diccionario de `tmodulo` antes de correr: `p9_4` ("¿Cuál es la razón principal por la que no hace aportaciones voluntarias?", 7 categorías) y `p8_3` ("¿Cuál es la razón principal por la que no dispone de algún seguro?", 8 categorías). Regla de clasificación **declarada ahora, antes de ver las categorías con sus frecuencias**: cualquier motivo que declare falta de ingreso disponible, no ofrecimiento/no disponibilidad del producto, o desconocimiento de cómo hacerlo se clasifica como **acceso efectivo ausente**; motivos que declaren preferencia, desconfianza o "no lo necesita/no le interesa" se clasifican como **decisión**. Si el motivo dominante entre quienes no cumplen el numerador es de acceso, la fila es `B` aunque el porcentaje numérico cruce el 15%; si es de decisión, la fila es `A`.

## Diseño muestral

Ponderador `fac_per` (tabla `tmodulo`); estrato `est_dis`; UPM `upm_dis` (mismos nombres en las 4 tablas).

## Consecuencia si cruza (línea 45, ya en la ficha, no una decisión de este commit)

Si `A`: "la regla no se rompe entera: se parte. Sobrevive 'permite' `[FUERTE]`; cae 'produce', que es la que el motor usa para enrutar perfiles 1 y 4" (id del motor: `dinero.planeacion.formal_estable`, `modelo-decision-v4_0.md:342`). El veredicto de este commit reporta esa partición explícitamente si aplica — no "refutada" a secas.

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta.** No se recalculará el proxy de formalidad, el umbral de ingreso suficiente, ni la composición del numerador después de ver el porcentaje.
