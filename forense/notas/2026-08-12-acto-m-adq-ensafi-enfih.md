# ACTO M-ADQ · Adquisición documental ENSAFI 2023 + ENFIH 2019 hasta el universo mínimo (ADR-69/70)

`ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO`, 12/ago/2026 (`forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`), §3. Worktree `/home/pc0/mm-m-adq-ensafi-enfih`, rama `acto-m-adq/ensafi-enfih`. Adquisición **documental**, no de microdato: ENFIH ya tiene descriptor (838 variables, 16 hojas) pero está por debajo del universo mínimo de ADR-69 (llegar a ficha RNM y cuestionario); ENSAFI está por debajo de ENFIH. Este acto no abre nada a nivel variable — eso es M-APERTURA (§6), gateado sobre el cierre de éste.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/mm-m-adq-ensafi-enfih`. `git log -1`: `31c4ec3 forense/encargos: archiva ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO (A.3)`. `git status`: árbol limpio salvo `data/raw` (symlink esperado, gitignorado).
2. **SHA.** `origin/main = 11083af` (merge de PR #184, E4c Paso 3 corrida real R5.1-D2 — sin relación con este acto). `git rev-list --left-right --count origin/main...HEAD` → `0  1`: la rama es exactamente `origin/main` + el commit A.3 de este acto, sin deriva que re-derivar.
3. **data/raw.** Ya enlazado al abrir la sesión: `data/raw -> /home/pc0/mm-corpus/raw` (`readlink -f` confirma la ruta real). Este acto NO descarga microdato — no aplica la verificación PR#77 de corpus compartido.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → `sin_variable`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`, verificado en esta sesión. Firma de caja (`sin_variable` + sonda 200) — este acto acepta nube o caja; se declara **caja**, libre en esta sesión (P·Lote-1 ya reclamó `mm-p-lote1-adquisicion` en caja, pero ambos actos corren en paralelo por diseño del documento, perímetros disjuntos salvo el puntero de puertas).
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de comandos corridos en esta sesión (`curl`, `git`, `grep`, `python3`), con el comando a la vista donde importa.
5-bis. **CONCURRENCIA (regla de mesa para este acto, no del bloque ARRANQUE estándar).** `data/manifiesto.yaml` (reescritura completa vía `yaml.dump`) y `data/universo-puertas-2026-08-12.tsv` (puntero de puertas/activos documentales) son de un solo escritor a la vez entre este acto y P·Lote-1, que corre en paralelo. Este acto llega hasta clasificar cada pieza y **propone** las filas del conducto sin escribirlas — mesa secuencia la escritura real. Declarado explícitamente al cierre del Commit 2 (§2.3).

**Regla A.3 aplicada primero.** El texto completo del encargo (los ocho §, §0-§8) se archivó como *primer commit* de la sesión, antes de este acto (`31c4ec3`, ya en `HEAD` al abrir esta sesión).

**Verificado por comando, no de memoria (Commit 1(b)):**

```
$ awk -F'\t' '$3=="ENFIH" || $3=="ENSAFI"' data/curacion-registro/relaciones.tsv \
  | awk -F'\t' '{print $3" capa3="$11}' | sort -u
ENFIH capa3=EXISTE;COINCIDE;INTEGRO
ENSAFI capa3=EXISTE;COINCIDE;INTEGRO

$ ls data/raw/ensafi2023/
ensafi_2023_bd_csv.zip
$ ls data/raw/enfih2019/
enfih_2019_base_de_datos_csv.zip  enfih_2019_fd.xlsx

$ grep -n "^- id:.*ensafi\|^- id:.*enfih" data/manifiesto.yaml
3928:- id: ensafi2023_bd_csv_zip
3994:- id: enfih2019_bd_csv_zip
4014:- id: enfih2019_fd_xlsx

$ grep -in "ensafi\|enfih" data/universo-puertas-2026-08-12.tsv data/universo-puertas-2026-08-08.tsv
(sin resultados para ninguna fila real — el único hit es "ENFIH" citado de pasada dentro de la fila NO-ENCONTRADO
de ITAM_panel_household_finance, no una fila propia de ENSAFI/ENFIH)
```

Confirma el terreno que el encargo supone, con una corrección de detalle: **el nivel 1 ("el payload y su descriptor") NO está parejo entre las dos fuentes.** ENFIH tiene ambos (ZIP + `enfih_2019_fd.xlsx`, 16 hojas). ENSAFI **solo tiene el ZIP** — no hay ningún `*_fd.xlsx` ni equivalente en `data/raw/ensafi2023/`, y el propio `manifiesto.yaml` (entrada `ensafi2023_bd_csv_zip`, escrita 2026-08-04/05) ya documenta que ese hueco se investigó una vez, con un único patrón de URL (`.../ensafi/2023/microdatos/...`, soft-404 de 2263 B) y sin llegar a la RNM — exactamente el defecto que ADR-69 nombra (universo declarado incompleto, no falta de rigor dentro de él). Este acto retoma esa pieza.

## 1 · Commit 1 — Pre-registro

### 1.1 · Qué exige el universo mínimo (a) — leído de `data/UNIVERSO-MINIMO-FUENTE-v1_0.md`, no parafraseado

Seis niveles, costo creciente (archivo íntegro leído en esta sesión antes de escribir esta nota): **(1)** payload+descriptor en `data/raw`. **(2)** PDF "Conociendo la base de datos" de la edición, si existe. **(3)** ficha RNM (`/rnm/index.php/catalog/{id}`) — muestreo, recolección de datos (periodo de ejecución/levantamiento/referencia con fecha inicio/fin), factores de expansión por tabla con nombre exacto de columna, tasa de respuesta, cuestionarios por sección, política de acceso; exportable en `/rnm/index.php/metadata/export/{id}/json` y `/ddi`; el buscador interno del catálogo está roto (devuelve el catálogo completo sin filtrar) — el `{id}` se obtiene por navegación directa o enlace ya conocido, nunca por ese buscador. **(4)** indicadores de calidad publicados (CV/EE/IC), típicamente en `/rnm/index.php/catalog/{id}/download/{n}` — verificar `Content-Type`/`Content-Disposition` antes de registrar, un enlace catalogado no garantiza el documento correcto. **(5)** documentos de biblioteca que la ficha cite (Diseño muestral, Informe operativo, Diseño conceptual) en `https://www.inegi.org.mx/app/biblioteca/ficha.html?upc={id}`. **(6)** DOF, solo si la cifra buscada es un umbral/índice/regla de programa, no dato de encuesta.

La regla de cierre: un `NO-ENCONTRADO` sobre un campo material declara qué niveles se recorrieron y cuáles no, con mecanismo y fecha. Un nivel no recorrido es un pendiente, no un hallazgo negativo.

### 1.2 · ENSAFI 2023

**(b) Ya en el conducto:** payload (`ensafi2023_bd_csv_zip`, ZIP, en `data/raw` y `manifiesto.yaml`) — nivel 1 **parcial**, sin descriptor propio. Cero filas en `universo-puertas-*.tsv`. Ninguna nota previa del repo abrió una ficha RNM para esta fuente (verificado: `grep -rin "rnm.*ensafi\|ensafi.*rnm" forense/ data/ canon/` no trae ninguna apertura, solo una URL de metadatos citada sin abrir en `data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:111` y una fila `NO_INSPECCIONADO` en `data/curacion-universo/universo-declarado-t0.tsv:32889`).

**(c) Qué falta, pieza por pieza:** (i) descriptor/FD (resto del nivel 1); (ii) PDF "Conociendo la base de datos" (nivel 2); (iii) la ficha RNM misma (nivel 3, identidad sin confirmar en sesión); (iv) factores de expansión con nombre exacto de columna; (v) tasa de respuesta; (vi) cuestionario por sección; (vii) política de acceso; (viii) indicadores de calidad (nivel 4); (ix) documentos de biblioteca — Diseño muestral, Informe operativo, Diseño conceptual (nivel 5); (x) DOF (nivel 6, aplicabilidad por confirmar).

**(d) Dónde se buscará:** (iii)-(vii) en la ficha candidata `https://www.inegi.org.mx/rnm/index.php/catalog/992` — **SIN-FETCH hasta abrir (A.6)**: el id 992 viene de `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:111`, nunca abierto en este repo, se trata como candidata no confirmada hasta sondearla en esta sesión. (i)/(ii) en el portal del programa (`inegi.org.mx/programas/ensafi/2023/` y variantes `contenidos/programas/ensafi/2023/...`) y, si la ficha existe, en su pestaña de diccionario de datos. (viii) en los enlaces `/download/{n}` que la ficha declare. (ix) en la pestaña "Materiales de Referencia" de la ficha y en las citas `biblioteca/ficha.html?upc=...` que su prosa incluya. (x) no aplica salvo que alguna pieza resulte ser un umbral/índice — se declara explícitamente si no.

**(e) Criterio A.4 por pieza:** **EXISTE-SATISFACE** = documento localizado y abierto byte a byte en esta sesión, con `Content-Type`/portada confirmando que es el documento correcto (fuente+año+tipo), no solo el enlace catalogado. **EXISTE-NO-SATISFACE** = localizado pero incompleto o de identidad distinta a la buscada, declarando qué falta. **NO-ENCONTRADO** = los niveles pertinentes recorridos sin hallar la pieza, con términos y portales declarados. **NO-ACCESIBLE** = localizado pero detrás de pago o afiliación institucional (registro gratuito no cuenta como NO-ACCESIBLE).

### 1.3 · ENFIH 2019

**(b) Ya en el conducto:** payload + descriptor completos (`enfih2019_bd_csv_zip` + `enfih2019_fd_xlsx`, 16 hojas, en `data/raw` y `manifiesto.yaml`) — nivel 1 **satisfecho**. Cero filas en `universo-puertas-*.tsv`. Ninguna nota previa del repo abrió una ficha RNM para esta fuente (mismo grep que ENSAFI, sin resultados de apertura); URL de metadatos citada sin abrir en `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:123` y fila `NO_INSPECCIONADO` en `universo-declarado-t0.tsv:15084`.

**(c) Qué falta, pieza por pieza:** (i) PDF "Conociendo la base de datos" (nivel 2); (ii) la ficha RNM misma (nivel 3); (iii) factores de expansión con nombre exacto de columna; (iv) tasa de respuesta; (v) cuestionario por sección; (vi) política de acceso; (vii) indicadores de calidad (nivel 4); (viii) documentos de biblioteca (nivel 5); (ix) DOF (nivel 6, aplicabilidad por confirmar).

**(d) Dónde se buscará:** (ii)-(vi) en la ficha candidata `https://www.inegi.org.mx/rnm/index.php/catalog/709` — **SIN-FETCH hasta abrir (A.6)**, id de `inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md:123`, nunca abierto en este repo. (i) en el portal del programa (`inegi.org.mx/programas/enfih/2019/`, ya conocido como SPA por precedente de este repo para rutas `/programas/`) y su árbol `contenidos/programas/enfih/2019/...`. (vii) en los `/download/{n}` de la ficha. (viii) en "Materiales de Referencia" de la ficha, con fallback a `https://www.banxico.org.mx/enfih/` (espejo declarado en el inventario, INEGI+Banxico co-ejecutan esta encuesta) si el catálogo INEGI no da enlace directo. (ix) no aplica salvo hallazgo contrario, se declara.

**(e) Criterio A.4 por pieza:** idéntico a 1.2(e).

---

El primer resultado que produzca este procedimiento es el que se reporta.
