# P1 · ¿Sirve ENIGH como semilla IPF? · seis ejes, llave persona

### 31/jul/2026 · derivada contra `enigh2022_nc_csv.zip` (sha256 `3b2b0bc9…9e06`, verificado abajo) · rama `sesion/p1-enigh-semilla`, base `5f59902` (`origin/main`)

> | | |
> |---|---|
> | **QUÉ ES** | Responde al ENCARGO P1: para los 6 ejes de segmentación, ¿la ENIGH más reciente en disco trae los descriptores en el mismo registro-persona (o unible a él), lo suficiente para sembrar un IPF? |
> | **QUÉ NO ES** | No corre IPF. No estima cobertura de perfiles. No abre `conjunto_de_datos/` (filas de microdato) de ningún módulo — mismo firewall que INV-SEG (ADR-46): solo `diccionario_de_datos/`, `catalogos/` y `metadatos/`. |
> | **PROCEDENCIA** | Tipo (1): los nombres de campo, catálogos y llaves de abajo se leyeron en esta sesión, directo del ZIP en disco. Tipo (3) re-verificado, no asumido: la tabla A de INV-SEG (`forense/notas/2026-07-31-inventario-segmentacion.md`) y el estado del manifiesto. |
> | **QUÉ NO SE HIZO** | No se ejecutó P1-bis (abrir descriptores de ENOE) — el veredicto de este archivo no lo requiere; ver §4. |

---

## 0 · Verificación de premisas del encargo

| # | Premisa | Verificado contra | Veredicto |
|---|---|---|---|
| 1 | INV-SEG tabla A da a ENIGH cubriendo los 6 ejes en régimen laxo | `forense/notas/2026-07-31-inventario-segmentacion.md` líneas 39-118 (Tabla A, secciones 1-6) | **SE SOSTIENE** — ENIGH aparece con veredicto Sí/Parcial (nunca "No") en los 6 bloques; ver cita por eje en §2 |
| 2 | ENIGH está en disco con hash verificado en el manifiesto | `python3 tests/manifiesto.py --verifica --id enigh2022_nc_csv` | **SE SOSTIENE, con matiz** — ver abajo |
| 3 | La revisión que motiva esto está (o estará) en la raíz como `revision-programa-2026-07-31.md` | `git ls-tree -r origin/main --name-only \| grep -i revision-programa` (vacío) | **NO SE SOSTIENE en `main`** — el PR del Paso 1 no ha fusionado. Se trabaja con el encargo de chat como fuente, como instruye la premisa misma si esto ocurre. |

**Matiz de la premisa 2.** El primer `--verifica` en este worktree (`mm-inv-seg-p3`, checkout nuevo, sin correr antes) reportó **AUSENTE**: este worktree no traía `data/raw` (symlink) ni `data/raices.local.yaml` (ambos gitignorados, por-máquina/por-worktree, y no se propagan solos a un checkout nuevo — otros worktrees del mismo repo, ej. `mm-inv-seg`, sí los tenían). No es corrupción: el payload existe en `/home/pc0/mm-corpus/raw/enigh2022_nc_csv.zip`, comprobado por `sha256sum` directo, coincidiendo byte a byte con el `sha256` del manifiesto. Se replicó el mismo wiring que usan los demás worktrees (symlink `data/raw -> /home/pc0/mm-corpus/raw` + copia de `data/raices.local.yaml`, ambos gitignorados, cero cambios versionados) y `--verifica` pasó a **COINCIDE**:

```
$ python3 tests/manifiesto.py --verifica --id enigh2022_nc_csv
enigh2022_nc_csv [data_raw]: COINCIDE -- sha256 y tamaño (90030937 bytes) verificados contra data/manifiesto.yaml
```

Si esto se hubiera reportado como "ENIGH no está íntegra" sin la re-verificación, habría sido un falso negativo del wiring del worktree, no un hallazgo real sobre el dato. Se deja documentado porque el encargo pide precisamente distinguir "no lo encontré" de "no existe" — aquí era "no lo encontré en este worktree", con hash confirmado en cuanto se buscó en el lugar correcto.

**Edición.** `enigh2022_nc_csv` es ENIGH 2022, modalidad nueva serie (`_ns`, confirmado por los nombres de archivo dentro del ZIP: `conjunto_de_datos_poblacion_enigh2022_ns/…`; el segmento `nc` del id y de la URL de origen es el código de programa de INEGI, no la modalidad de la encuesta). Es la más reciente en disco: `data/manifiesto.yaml:421-422` documenta que ENIGH 2024 solo tiene un placeholder de plantilla (JSON-LD sin distribución real), no publicada aún — mismo hallazgo que ya tenía INV-SEG.

---

## 1 · Estructura de llaves del paquete (verificado, no de memoria)

Se leyeron los primeros campos de `diccionario_de_datos/` de los cuatro módulos relevantes, directo del ZIP:

| módulo | campos 1-3 (orden del diccionario) | nivel |
|---|---|---|
| `poblacion` | `folioviv`, `foliohog`, `numren` | **PERSONA** (numren = número de renglón/persona dentro del hogar) |
| `trabajos` | `folioviv`, `foliohog`, `numren` (+ `id_trabajo`: 1=principal, 2=secundario) | **PERSONA**, con hasta 2 filas por persona (multi-trabajo); sin fila para quien no trabajó |
| `hogares` | `folioviv`, `foliohog` | **HOGAR** (sin `numren`) |
| `concentradohogar` | `folioviv`, `foliohog` | **HOGAR** (sin `numren`) |

`poblacion` trae `folioviv`+`foliohog` además de `numren`, así que cualquier variable de `hogares`/`concentradohogar` se une a **cada persona de ese hogar** por `folioviv`+`foliohog` de forma determinista y sin ambigüedad — no es "sin llave utilizable", es un join hogar→persona limpio. La diferencia real es otra: el valor queda **constante entre las personas del mismo hogar** (sin varianza intra-hogar en esa variable). Esa distinción es la que separa EN CONJUNTA de EN CONJUNTA VÍA HOGAR abajo — ninguna de las dos es FUERA DE CONJUNTA.

---

## 2 · Tabla eje × variable × tabla/módulo × llave × veredicto

| eje | variable(s) exacta(s) | valores | tabla/módulo | llave de unión a persona | veredicto |
|---|---|---|---|---|---|
| **1. Formalidad laboral** | `segsoc` (Sí/No, derechohabiencia) | 1 Sí / 2 No | `poblacion` | **PERSONA** directa (`folioviv`+`foliohog`+`numren`) | **EN CONJUNTA** |
| | `contrato`, `tipocontr`, `pres_1..20` (incl. `pres_8`=SAR/AFORE), `medtrab_1..7` | binarias/catálogo por prestación | `trabajos` | **PERSONA** vía `folioviv`+`foliohog`+`numren` (+`id_trabajo`, condicionado a haber trabajado — sin fila para quien no) | **EN CONJUNTA** (con nulos esperados en no-trabajadores, inherente al eje) |
| **2. Edad** | `edad` | entero, años | `poblacion` | **PERSONA** directa | **EN CONJUNTA** |
| | *(`edad_jefe` en `concentradohogar` es redundante: el diccionario la define como "igual a la variable `edad` donde `parentesco`=101 de la tabla `poblacion`" — no aporta nada que `poblacion.edad` no tenga ya a nivel persona)* | | | | — |
| **3. Urbanización / tamaño de localidad** | `tam_loc` | 1 100k+ / 2 15k-99,999 / 3 2,500-14,999 / 4 <2,500 (catálogo `tam_loc.csv`) | `concentradohogar` (copiada de `viviendas`) | **HOGAR** (`folioviv`+`foliohog`), heredable a persona vía `poblacion` | **EN CONJUNTA VÍA HOGAR** |
| **4. Ingreso** | `ing_cor` (continuo) + `est_socio` (índice NSE, catálogo `est_socio.csv`: 1 Bajo / 2 Medio bajo / 3 Medio alto / 4 Alto) | monto trimestral / 4 categorías | `concentradohogar` | **HOGAR**, heredable a persona | **EN CONJUNTA VÍA HOGAR** |
| **5. Acceso digital** | `celular` (SERV_2), `conex_inte` (SERV_4) | 1 Sí / 2 No, binario, tenencia | `hogares` | **HOGAR** (`folioviv`+`foliohog`), heredable a persona | **EN CONJUNTA VÍA HOGAR** — más débil que los demás: tenencia binaria del hogar, sin distinguir celular básico de smartphone, sin uso individual ni banca en línea (mismo límite que ya señaló INV-SEG) |
| **6. Condición migratoria** | `residencia` (32 entidades + "Estados Unidos de América" + "Otro país", catálogo `residencia.csv`) | 34 categorías | `poblacion` | **PERSONA** directa | **EN CONJUNTA** — con el límite ya señalado por INV-SEG, re-verificado aquí: ni el diccionario ni `metadatos_enigh_2022_ns.txt` traen el texto literal de la pregunta (`grep` de "residenc" sobre el metadatos: sin resultado) — no se puede confirmar la referencia temporal exacta (¿residencia hace 5 años? ¿al nacer?) sin el cuestionario, que **no viene incluido en este ZIP** (0 PDFs dentro del paquete) |
| | `remesas` (Σ de `ingresos.ing_tri` cuando clave ∈ {P041}) | monto trimestral | `concentradohogar` | **HOGAR**, heredable a persona | **EN CONJUNTA VÍA HOGAR** (complementaria, no necesaria para que el eje pase) |

---

## 3 · Veredicto global: **CONJUNTA COMPLETA**

Los 6 ejes llegan a EN CONJUNTA o EN CONJUNTA VÍA HOGAR. Ninguno cae en FUERA DE CONJUNTA — no hay ningún eje cuyo único descriptor viva en un módulo sin llave de unión a `poblacion`. La ruta IPF vive: se puede construir un microdato semilla a nivel persona (base `poblacion`, `folioviv`+`foliohog`+`numren`) con los 6 atributos en el mismo registro, uniendo `trabajos` por persona y `hogares`/`concentradohogar` por hogar.

**Caveat para quien redacte P2 (no es defecto de conjunta, es granularidad):** 3 de 6 ejes (urbanización, ingreso, acceso digital) y el componente `remesas` del eje 6 son atributos de **hogar**, no de persona — todas las personas del mismo hogar comparten el mismo valor en esas columnas tras el join. Si P2 va a construir celdas de atributos que requieran varianza intra-hogar en tamaño de localidad, ingreso o acceso digital (ej. "dos hermanos del mismo hogar en celdas distintas por ingreso"), esa varianza **no existe en ENIGH** — es indistinguible de una persona a otra del mismo hogar por diseño del instrumento, no por un hueco de esta sesión. Edad, formalidad laboral y residencia (ejes 1/2/6) sí varían persona a persona.

Por ser CONJUNTA COMPLETA, **no aplica** la sección de "qué prometería ENOE para los ejes caídos" (encargo, condicional a PARCIAL/NO) — no hay ejes caídos. No se abrió ningún descriptor de ENOE en esta sesión más allá de leer la fila ya existente de la Tabla A de INV-SEG (contaminación previa de esa sesión, no de esta).

---

## 4 · Límite declarado

- Firewall respetado: solo `diccionario_de_datos/`, `catalogos/` y `metadatos/` de `poblacion`, `trabajos`, `hogares`, `concentradohogar`; ningún `conjunto_de_datos/*.csv` (fila real) abierto.
- No se estima cobertura de perfiles ni se corre IPF — eso es explícitamente fuera del alcance de este archivo.
- El wiring de `data/raw`/`data/raices.local.yaml` en este worktree (`mm-inv-seg-p3`) se dejó igual que en los demás worktrees del repo (symlink + copia de config gitignorada) para que `--verifica` diera una lectura real; ningún archivo versionado cambió por esto.
- `revision-programa-2026-07-31.md` no está en `origin/main` al momento de esta sesión (commit `5f59902`); se trabajó con el encargo de chat como fuente de la premisa, tal como esta misma indica hacer si el PR del Paso 1 no ha fusionado. Se vio un archivo con ese nombre en `/mnt/c/Users/PC0/Downloads/` (fuera del repo) — no se leyó ni se usó como fuente: no es el estado del repo, es un artefacto local fuera de alcance de esta verificación.
