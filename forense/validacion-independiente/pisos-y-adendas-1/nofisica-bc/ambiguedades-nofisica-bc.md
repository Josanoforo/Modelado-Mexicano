# Ambigüedades · recalculo NOFISICA-BC

**Verificación del ZIP.** `sha256sum bd_endireh_2021_csv.zip` =
`e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`, idéntico
al declarado por la spec (§1) y por el encargo. Verificado antes de leer el
microdato.

Recalculado desde `forense/prereg-caja/ENDIREH-PISOS-2021-NOFISICA-BC-spec-v2_0.md`
únicamente. No se leyó `data/corrida0/CALC-ENDIREH-*` ni ningún otro artefacto
fuera del perímetro permitido.

## N del marco

`RESULT-ENDIREH2021-NF-BC-N-ELEGIBLES` obtenido por spec: **105278** filas de
`TB_SEC_XIV.csv` (sobre 110127 filas totales), tras aplicar en orden:
`T_INSTRUM` (texto crudo) ∈ {A1,A2,B1,B2,C1} → enlace a `TSDem.csv` con
`EDAD` entero en [15,120] → `FAC_MUJ` real/finito/>0 → `EST_DIS`/`UPM_DIS` no
vacíos. Marco de conglomerados: 17725 pares (estrato, UPM), 617 estratos.

## Alcance de este recálculo

El protocolo (§1) solo pide `ayuda_bc`×escolaridad (`#495-498`) y
`denuncia_bc`×escolaridad (`#544-547`); ninguno de los diez desenlaces de
grupo (`emocional_control__vida_relacion`, …, `no_fisica_alguna
__desde_octubre_2020`) ni `institucion_bc_*`/`razon_bc_*` es requerido. Como
`ayuda_bc`/`denuncia_bc` dependen exclusivamente de la "violencia" (clasificador
sobre los 38 actos de 14.1, párrafo "Ayuda y denuncia B/C" de §3) y no de los
desenlaces de grupo, el código **no** implementa el clasificador de ventana
`vida_relacion`/`desde_octubre_2020` de esos diez desenlaces de grupo (no hace
falta para las 8 llaves pedidas); sí implementa el enumerador de índices
completo (613 slots) para verificar la identidad de las llaves requeridas.

## Puntos donde la spec admitía más de una lectura literal

1. **Omisión de los seis actos `AB` para `C1` (§3).** La spec dice "C1 no los
   pregunta: para C1 se omiten de toda lista", tanto para los grupos como
   para el párrafo de "Ayuda y denuncia B/C" ("para C1 sin los seis AB").
   Implementé la omisión construyendo la lista de actos a evaluar (1–38)
   **excluyendo** los seis actos `{23,24,35,36,37,38}` cuando `T_INSTRUM ==
   'C1'`, antes de aplicar el clasificador — en vez de incluir esas columnas
   con su valor crudo (probablemente en blanco) en la lista. La diferencia
   es observable: si se incluyeran como valores en blanco, una fila `C1` con
   los 32 actos restantes en `4` y los 6 `AB` en blanco NO cumpliría "todos
   son 4" (por los blancos) y saldría desconocida en vez de 0. Elegí la
   omisión explícita porque es literalmente lo que dice la spec ("se omiten
   de toda lista").
2. **`EST_DIS`/`UPM_DIS` vacío = únicamente `''`.** Mismo criterio que en la
   spec DISCRIMINACION (ver su `ambiguedades.md`): comparación literal contra
   cadena vacía, sin recorte. No se observó ninguna fila con espacios en
   blanco en esos campos.
3. **Conversión de `EDAD` a entero:** `int(texto)` de Python (tolera
   espacios y ceros a la izquierda). Igual que en DISCRIMINACION.
4. **Semilla de `ayuda_bc`/`denuncia_bc`.** La spec (§5.5) da tres reglas de
   semilla distintas: normal (`desenlace+eje+categoria`), la de los
   desenlaces de grupo (`<grupo>__<ventana>` en vez de un solo nombre) y la
   de `institucion_bc_*`/`razon_bc_*` (solo el nombre del desenlace, porque
   esos solo tienen celda nacional). `ayuda_bc` y `denuncia_bc` no son
   ninguno de esos dos casos especiales — no son "desenlaces de grupo" (esos
   llevan el patrón `<grupo>__<ventana>`) ni tienen "solo celda nacional"
   (§4 los define sobre los seis ejes completos). Se les aplicó la regla
   normal: `texto_semilla = 'ayuda_bc' + eje + categoria` (p. ej.
   `'ayuda_bcescolaridadninguno'`).
5. **Enlace `ID_PER → (EDAD, NIV)` de `TSDem.csv` con posible repetición.**
   Verifiqué directamente sobre el ZIP que `ID_PER` es único en las cuatro
   tablas usadas por las tres specs (`TSDem`, `TB_SEC_VIII`, `TB_SEC_XIV`,
   `TB_SEC_XIV_2`: 110127/432746 valores no vacíos, todos distintos), así
   que la regla "si se repitiera, vale la última fila leída" no tuvo ningún
   caso real que ejercer en este recálculo.
6. **Salida numérica cuando `SUPRIMIDA`.** No se ejerció: las 8 celdas
   requeridas salieron `PUBLICABLE`.

## Verificación de identidad índice → llave

Enumerador general de los 613 slots (5 grupos × 2 ventanas × 49 celdas, más
`ayuda_bc`×49, `denuncia_bc`×49, `institucion_bc_01..10`, `razon_bc_01..15`,
en el orden de §6). Para las 8 llaves requeridas: `#495..#498` =
`ayuda_bc`×escolaridad×{ninguno,basica,media_superior,superior}; `#544..#547`
= `denuncia_bc`×escolaridad×{las cuatro}. **Coincide exactamente** con lo que
declara `protocolo-recalculo-v1_0.md` §1. Ninguna discrepancia.

## Consulta a FD / cuestionarios

No hizo falta abrir el FD ni los cuestionarios: la tabla `NIV → escolaridad`
y los textos de los reactivos ya están verbatim en la spec. Los nombres de
columna (`T_INSTRUM`, `P14_1_*`, `P14_3_*`, `P14_7_1`, `P14_7_2`, `EST_DIS`,
`UPM_DIS`, `FAC_MUJ`) se confirmaron contra el encabezado real de
`TB_SEC_XIV.csv`/`TSDem.csv` dentro del ZIP.

Ninguna otra ambigüedad.
