# Diseño 18–70 para U3 — borrador sin medición

Decisión de mesa, 22/sep/2026: **B, mantener persona elegida 18–70**.
Alcance de esta tanda: **solo diseño**. Este documento no es freeze ni
autorización para abrir microdatos. La misión íntegra y el encargo correctivo
están conservados verbatim en esta carpeta.

## 1. Producto y relación con las deudas

Tres corridas nuevas, con IDs definitivos sujetos a comprobación de unicidad
contra `origin/main` al ejecutar:

1. `CALC-PISOS-ENIF2021-FORMALIDAD-1870-0001`: seis P e IC95 del piso,
   persona elegida 18–70.
2. `CALC-R-ENIF2024-FORMALIDAD-1870-0001`: seis P e IC95 de la ola objetivo,
   mismo universo y definiciones armonizadas.
3. `CALC-PISO-PERSISTENCIA-ERROR-FORMALIDAD-1870-0001`: seis diferencias e IC
   por enlace de identidad exacta entre los dos RESULT anteriores.

La tercera corrida es RETROSPECTIVA-MECÁNICA. Los R de 2024 ya se han visto
en otros trabajos; no habrá selección de variante por resultado. Las seis
celdas originales selladas son 18+; este nuevo producto 18–70 no cierra
automáticamente NC-0414 ni NC-0431, que piden error de aquellas celdas.

## 2. Definición común de las seis celdas

Unidad: persona elegida. Edad inclusiva 18–70 antes de construir desenlace,
eje y réplicas. Cada denominador contiene solo personas con factor positivo,
estrato/UPM válidos, categoría de formalidad válida y el desenlace respectivo
definido. No se impone denominador común entre los tres desenlaces.

| Desenlace | 2021 | 2024 | Regla |
|---|---|---|---|
| `ahorra_solo_informal` (D9) | `P5_1_1..6`, `P5_4_1..9`, `P5_7_1..9` | `P5_1_1..6`, `P5_4_1..9`, `P5_6_1..9` | Informal sí y ahorro formal no, con la lógica de valores indefinidos del medidor sellado del piso 2021. |
| `informal_cualquiera` | `P5_1_1..6` | `P5_1_1..6` | Al menos una respuesta afirmativa válida, con la lógica de indefinidos del mismo medidor. |
| `horizonte_corto` | `P4_10` | `P4_10` | Código `1` entre válidos `1..5`; `8`, `9` y blanco indefinidos. Es el corte de las seis celdas originales, aunque otra familia ENIF use `1..2`. |

Dos categorías por desenlace: 2021 `P3_10` en `1..5` = con seguridad social,
`6` = sin; 2024 `P3_13` en `1..6` = con, `7` = sin. Los demás códigos quedan
fuera de este eje, con conteos diagnósticos. El cuestionario/FD comparados
en `PISOS-ENIF2021-formalidad-spec-v1_0.md` §§1–2 documentan el texto,
los saltos de flujo y la armonización. La edad es `EDAD` en 2021 y `EDAD_V`
en 2024, como declaran los medidores sellados respectivos.

## 3. Estimación de cada ola

Leer solo el miembro `conjunto_de_datos_tmodulo_enif_2021.csv` del payload
`enif_2021_enif_2021_bd_csv` y solo `TMODULO.csv` de
`enif_2024_enif_2024_bd_csv`. Verificar hashes y presencia antes del freeze;
abrir valores únicamente después. CAJA para ambas olas. Reusar por ruta/hash
las funciones de definición y bootstrap de `CALC-PISOS-ENIF2021-EJES-0003`;
no cargar módulos que lean otras olas al importarse. `FAC_ELE` (2021) y
`FAC_PER` (2024); UPM con reemplazo dentro de `EST_DIS`, 10 000 réplicas
compartidas, `numpy.PCG64(42)`, IC95 percentil 2.5/97.5. Este es el método
de los contratos 2021/2024 existentes. Fijar en cada spec la versión y hash
del código importado, miembros y hashes del manifiesto, semilla, tolerancia,
esquema de P/LO/HI/N/DEN-W/B-VALIDAS y diagnósticos de exclusión.

Antes del freeze, verificar el texto `P4_10` y la edad en ambos FD y
cuestionarios disponibles en el manifiesto. Una pregunta ausente o una
categoría incompatible vuelve la celda NO-CONSTRUIBLE; no se sustituye
silenciosamente por otro estimando. No leer sección de crédito 2024 ni otros
cruces. Tras freeze, el primer resultado del procedimiento es el reportado.

## 4. Error y entregables posteriores

Tabla nueva de identidad con seis filas, dos IDs de RESULT distintos por fila,
universo `PERSONA ELEGIDA 18-70` y hash. El medidor preparado aquí verifica
los tres hashes, falla por llaves duplicadas, despareadas o universos distintos
y enlaza por `input_id`, nunca por posición. Para P/IC íntegros aplica
`d_pp = 100(R − piso)` y `IC95(d) = d_pp ± 100 × 1.959964 ×
sqrt(se_R² + se_piso²)`, con `se = (HI − LO)/(2 × 1.959964)`.
La independencia entre olas y la simetría normal aproximada son supuestos;
ese IC no es bootstrap directo de la diferencia. `PERSISTE` si el IC incluye
cero; `CAMBIA` en otro caso. `PERSISTE` no prueba equivalencia. Falta de P,
IC o identidad compatible: `NO-COMPARABLE`, causa y diferencia nula.

Cuando se autorice la ejecución ampliada: prerregistro humano y sidecar de
cada ola y del error, `spec.yaml` y código completos; commit de freeze antes
de valores; preflight, run, verify REPRODUCE, replay, asiento propio, nota,
recibo, commit/push/PR. Etiquetas GEN2, cuenta_gen2 SI, adopta NO y origen
numérico verdadero según cada corrida. Mantener NC-0414/0431 abiertas salvo
que la mesa autorice medir también las seis celdas 18+ originales.
