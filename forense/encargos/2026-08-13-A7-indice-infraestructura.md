- **SHA de redacción:** `2b13e88` (`origin/main` al momento en que se lanzó este encargo)
- **Entorno asignado:** NUBE — sin sonda de red (ADR-59(b)); no toca microdato ni red.
- **Estado:** CONSUMIDO — ejecutado por el acto de este mismo commit, PR #191 (`infra/indice-v1`, https://github.com/Josanoforo/Modelado-Mexicano/pull/191). Ver `data/INFRAESTRUCTURA-v1_0.md` y `forense/notas/2026-08-13-indice-infraestructura.md`.

---

Texto completo del encargo, tal como se lanzó (verbatim, incluye la Parte 1 dirigida a instrucciones-proyecto y la Parte 2, el ENCARGO NUBE que este acto ejecutó):

---

# A.7 · Regla nueva para instrucciones + ENCARGO de nube para construir el índice
### 13/ago/2026 · `origin/main = 2b13e88` · derivado por comando en esta sesión

---

# Parte 1 · El texto para las instrucciones — se pega después de A.6

## A.7 · Ningún encargo manda escribir en una tabla sin derivar antes qué tablas gobiernan ese dominio [NUEVO v2.7]

Un encargo que nombra la vía de escritura de memoria produce un registro a medias: el dato entra donde el redactor recordaba y no entra donde el resto de la maquinaria lo busca. **Es el defecto de ENASIC girado hacia adentro** — ahí el conocimiento existía en el repo y no llegaba a la receta; aquí la infraestructura existe en el repo y no llega al encargo.

**La regla, en tres frases.** Todo encargo que ordene escribir en una tabla, un manifiesto o un registro **declara primero qué tablas gobiernan ese dominio**, derivándolo de `data/INFRAESTRUCTURA-v1_0.md` y no de memoria. **Declara cuáles escribe y cuáles deliberadamente no**, con la razón de cada omisión. Si el índice no cubre el dominio, **ese hueco es el entregable**: se reporta y el encargo se detiene ahí, en vez de inventar una vía.

**Y la contraparte, para quien ejecuta.** Si el encargo nombra una vía que el índice no respalda, o omite una tabla que el índice dice que gobierna, **se para y se reporta** — igual que con cualquier otra premisa mal fundada. Ejecutar una vía incompleta cuesta más que no ejecutarla, porque deja un registro que parece completo.

**Qué defecto real atrapó, y qué le habría costado a un lector** (impuesto de v2.3, pagado). El 13/ago un encargo de registro de descargas —`ENCARGO-R-prima`, no lanzado— especificaba `data/manifiesto.yaml` + `universo-puertas` e **ignoraba `activos-descubiertos-durante-ronda.tsv` y `decisiones-adquisicion.tsv`**, que existen, tienen contrato de campos y tienen precedente de escritura (commit `0e07179`). Costo a un lector si hubiera corrido: un acto futuro que consulte la capa de activos no vería ISSP, concluiría que nunca se adquirió, y lo volvería a bajar. **Y hay una instancia posiblemente ya materializada**: los 11 payloads de WVS del 12/ago (`84f8e30`) entraron solo por el manifiesto, y ninguna de las 4 filas `ADESC-` existentes es de WVS.

**Falsador y caducidad.** Si en tres meses ningún encargo se detiene por esta regla y ningún índice desactualizado se detecta, **A.7 y el índice se retiran** y se anota. Si un encargo se detiene por ella y el hueco resulta falso —la tabla no gobernaba ese dominio— el índice estaba mal y se corrige el índice, no la regla.

**Lo que A.7 deliberadamente NO hace.** No añade un test: qué tabla gobierna qué dominio no es verificable desde la suite, y instrumentarlo sería vigilar lo que el test no puede ver. No exige mantener el índice al día por barrido periódico — se actualiza cuando un acto descubre que le falta algo, como cualquier tabla consolidada (regla de conducto, ADR-70(c)). No se audita a sí misma: no hay pregunta nueva en el módulo de auditoría.

---

# Parte 2 · ENCARGO · NUBE · construir `data/INFRAESTRUCTURA-v1_0.md`

### Base declarada: `origin/main = 2b13e88` · suite **VERDE 22 FAIL · 104 WARN** · cero ramas vivas — verificados por comando al escribir

> **PROCEDENCIA.** Verificado en esta sesión: **no existe ningún índice de infraestructura**. `data/` tiene dos artefactos `.md` —`UNIVERSO-MINIMO-FUENTE-v1_0.md` y `catalogo-fuentes-v2_0.md`— y ninguno describe la maquinaria interna. **`UNIVERSO-MINIMO-FUENTE-v1_0.md` es el precedente de forma**: seis niveles, cada uno con su URL y qué resuelve. Este acto construye su análogo hacia adentro.
>
> **Superficie derivada, para que dimensiones el acto:** ~25 TSV/YAML en `data/` · **19** TSV en `data/curacion-universo/` · `data/curacion-registro/` con sus propias tablas y `celdas-d/` · el motor en `tools/curador_registro/` · ~40 scripts en `tests/`.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

**ENTORNO ASIGNADO — y el que NO.** **NUBE.** Firma esperada `cloud_default` **sin sonda de red** — es la firma correcta de un acto de nube (ADR-59(b)), no un desajuste. Este acto **no toca microdato ni red**: dilo y salta el punto 4. NO caja local. NO en paralelo en otro entorno.

**PERÍMETRO.** SOLO: `data/INFRAESTRUCTURA-v1_0.md` (nuevo) · `forense/notas/2026-08-13-indice-infraestructura.md` · `forense/hallazgos.md` (append) · `forense/encargos/` (copia literal). **NO** modifica ninguna tabla, ningún script, ni `canon/`. **Este acto solo lee y documenta.** *Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.*

**CONCURRENCIA.** ACTO W, R″ y V2 pueden estar corriendo y **tocan tablas que este acto documenta**. Eso no es conflicto —tú no las escribes— pero **el índice debe declarar su fecha y que describe el estado de `2b13e88`**. Solapamiento único: `forense/hallazgos.md` (`merge=union`). **Merge local, main HACIA tu rama, nunca el botón ni el editor web.**

## PASO 1 · Premisas
```bash
git log -1 --format="%h %s"
ls data/*.md                                          # esperado: UNIVERSO-MINIMO-FUENTE y catalogo-fuentes; NO un índice
ls data/*.tsv data/*.yaml data/*.json | wc -l
ls data/curacion-universo/*.tsv | wc -l               # esperado 19
ls data/curacion-registro/ | wc -l
ls tools/curador_registro/*.py tests/*.py | wc -l
python3 tests/check.py --baseline                     # VERDE
```
**PARO si** ya existe un índice de infraestructura: entonces el defecto era no usarlo, no que faltara, y eso cambia el acto entero.

## PASO 2 · Agrupa por DOMINIO, no por directorio

El índice se organiza por **pregunta que un encargo se hace**, no por dónde vive el archivo. Un redactor no piensa "necesito escribir en `curacion-universo`"; piensa **"acabo de adquirir una fuente, ¿dónde se registra?"**.

Dominios mínimos —**deriva si hay más, no los inventes**:
1. **Adquirir una fuente / registrar un payload**
2. **Registrar una puerta o portal sondeado**
3. **Registrar un activo descubierto y su decisión de adquisición**
4. **Producir una estimación** (especificación, expediente, producción)
5. **Registrar una celda-D del piloto**
6. **Adjudicar un veredicto del Hito D**
7. **Sellar una decisión de gobierno** (ADR + cascada)
8. **Registrar un hallazgo o una nota de acto**

## PASO 3 · Por cada dominio, cinco campos — y ninguno se teclea de memoria

| campo | cómo se llena |
|---|---|
| **tablas que gobiernan** | ruta exacta, **verificada con `ls`** |
| **vía de escritura** | el script y su bandera (`tests/manifiesto.py --registra`), **o `A MANO, con precedente:` + el commit** que muestra cómo se hizo, **o `SIN VÍA`** si nada la escribe |
| **contrato de campos** | la cabecera real, **derivada con `head -1`**, no transcrita |
| **qué la lee** | quién consume esa tabla — `grep -rl` sobre `tools/` y `tests/`. **Si nadie la lee, dilo**: una tabla que solo se escribe es un hallazgo |
| **trampa conocida** | lo que ya mordió. Ej.: `manifiesto.yaml` **no tiene `merge=union`** y `--registra` lo reescribe entero → un escritor a la vez; la vía post-T0 **no regenera `snapshot-t0.json`** y hay que verificar que `snapshot_t0_sha256` no cambió |

**Regla de honestidad del índice, y es la que le da valor:** donde no exista vía, **se escribe `SIN VÍA` y no se inventa una**. `capa2_manifiesto` de `relaciones.tsv` es el caso testigo — `grep -rn "capa2" tools/ tests/` → **0**, con **105 filas en `NO_REFERENCIADO`** esperando. Un índice que disimule eso vale menos que no tenerlo.

## PASO 4 · La sección que hace al índice usable por quien redacta

Cierra con **"Si tu encargo hace X, escribe en Y"** — una tabla de dos columnas, en el vocabulario del redactor:

> *acabo de bajar un archivo* → manifiesto (vía) + activo descubierto (vía) + decisión de adquisición (vía) + fila de puerta (vía)
> *sondeé un portal* → fila de puerta
> *voy a estimar algo* → especificación congelada, expediente, dos commits
> *encontré un defecto* → `forense/hallazgos.md`
> …

**Esa tabla es el entregable real.** El resto es su respaldo. Un encargo mal escrito no falla por no conocer `curacion-universo`; falla por no saber que "bajé un archivo" toca cuatro tablas y no una.

## PASO 5 · Cierre
Siete líneas. `--baseline` cruda. **PR `infra/indice-v1`, NO FUSIONAR sin mesa.**

**Contadores de medición movidos: 0**, declarado. Este acto no mide nada sobre México — documenta la maquinaria para que los actos que sí miden no gasten su sesión orientándose ni escriban a medias.

**En el cierre, dos listas explícitas:** las tablas que encontraste **`SIN VÍA`**, y las que **nadie lee**. Las dos son colas de trabajo, no defectos de este acto.

**Lo que este acto NO hace.** No crea ninguna vía faltante — las nombra. No modifica ninguna tabla. No corrige el registro incompleto de WVS: eso es ACTO R″. No añade tests. No sella ADR — si mesa quiere canonizar A.7, es acto propio y de una línea.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-13-A7-indice-infraestructura.md" canon/gobernanza-v1_15.md` → 2: citado bajo ADR-76, ADR-77 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
