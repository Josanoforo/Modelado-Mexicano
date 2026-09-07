# ENCARGO FINAL · AUTOMATIZA-2 · CABLEADO POST-E3

*(archivado verbatim, A.3, por `ACTO AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`)*

## Autoridad

Este encargo incorpora y consolida:

1. `PLAN AUTOMATIZA-2 · CABLEADO POST-E3`;
2. `DICTAMEN · PLAN AUTOMATIZA-2 · CABLEADO POST-E3`, dirección Fable, 7/sep/2026.

Cuando exista una diferencia entre ambos, las precisiones del dictamen gobiernan.

Estado observado por dirección al emitir el dictamen:

* `origin/main = 0a19d39` (#579);
* ADR máx observado: 372;
* FP máx observado: 329;
* en vuelo: `acto/automatiza-2-e4-pdn-compara`;
* fusionados desde la revisión anterior: #578 LOTE-CRUCE y #579 AUTOMATIZA-2-E5 SCORE-RENDER.

Estos números son contexto histórico, NO parámetros de ejecución.
Cada acto debe re-derivar el estado vigente desde `origin/main`.

## OBJETIVO

Ejecutar secuencialmente tres piezas mecánicas pequeñas:

1. `AUTOMATIZA-2-A · BLINDA-HEAD-PR`
2. `AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`
3. `AUTOMATIZA-2-C · SELLA-SIDECAR`

Una cuarta idea:
`RENUMERA-DIAGNÓSTICO`
queda expresamente DESCARTADA:

* sin código;
* sin test;
* sin ADR;
* sin nota de backlog.

No buscar un `AUTOMATIZA-3` después de terminar esta tanda.
Después de C aplica regla de parada: el siguiente trabajo mecánico se automatiza sólo si aparece y se mide en uso.

## CONDICIÓN DE LANZAMIENTO

### A no empieza todavía si E4 sigue sin PR

Antes de iniciar `AUTOMATIZA-2-A`, comprobar que:
`acto/automatiza-2-e4-pdn-compara`
ya abrió su PR.

Razón:
E4 debe terminar usando la cascada vigente de `/acto`; no se cambia el guion operativo debajo de un acto ya en vuelo.

No hace falta esperar a que E4 sea fusionado salvo que otra compuerta vigente lo exija. La condición específica de este encargo es:
E4 debe haber abierto su PR antes de arrancar A.

Si no lo ha abierto:
`PARO-REPORTADO`
sin commits sustantivos de A.

## REGLAS COMUNES

Los tres actos son de entorno NUBE.
Modelo sugerido: Sonnet.
Secuencia estricta:

```text
A
↓
mesa fusiona A
↓
B desde main fresco
↓
mesa fusiona B
↓
C desde main fresco
```

No apilar PRs.
No ejecutar B sobre una rama basada en A todavía abierto.
No ejecutar C sobre B todavía abierto.
Mesa fusiona. El ejecutor nunca fusiona.

## ARRANQUE DE CADA ACTO

Usar `/acto`.
En el 0-bis:

1. `git fetch origin main`;
2. obtener SHA vigente de `origin/main`;
3. partir de worktree/rama fresca desde ese SHA;
4. ejecutar el preflight vigente de `tools/cierre_acto.py`;
5. derivar ADR, FP y rótulo desde el árbol actual;
6. archivar en A.3 el plan íntegro y este dictamen;
7. no heredar ADR 372, FP 329 ni ningún número de este documento.

Las compuertas se verifican por producto, no por nombre de commit.
No usar:

```bash
git log | grep ...
```

como prueba suficiente de que una pieza previa existe.

## PERÍMETRO GENERAL

No tocar:

* corpus;
* `data/raw`;
* `descargas_mx`;
* raíces físicas;
* manifiesto;
* adquisición;
* relaciones;
* motor;
* baseline mediante `--freeze`;
* CI;
* GitHub Actions;
* reglas de protección de rama.

La carpeta browser `Downloads` permanece fuera del proyecto y no se inspecciona.
No hacer auditoría general.
No corregir incidentalmente defectos cosméticos ajenos.
Cerrar cada acto con:

```bash
python3 tests/check.py --baseline
```

sin regresión nueva contra línea base.

## ACTO A · AUTOMATIZA-2-A · BLINDA-HEAD-PR

### Defecto real

PR #572 fue fusionado contra un HEAD anterior al último commit de cierre.
El `## CONSUMIDO` quedó fuera y hubo que incorporarlo posteriormente mediante #576.

Además, `/despacha` realiza dos pushes:

1. trabajo del acto;
2. commit posterior con estado/bitácora/`## CONSUMIDO`.

No existe hoy un guard final que pruebe que el remoto terminó exactamente en el HEAD local.

### Objetivo

Antes de declarar cualquier PR listo para mesa:

```text
HEAD local == HEAD de origin/<rama>
```

verificado contra el remoto vivo.

### Implementación

Crear:

```text
tools/verifica_head_remoto.py
```

Invocación

```bash
python3 tools/verifica_head_remoto.py
```

Opcional:

```bash
python3 tools/verifica_head_remoto.py \
  --remote origin \
  --branch <rama>
```

Si no se pasa rama:

```bash
git branch --show-current
```

### Evidencia

Usar:

```bash
git rev-parse HEAD
git ls-remote --heads <remote> refs/heads/<rama>
```

No usar como sustituto:

```text
refs/remotes/origin/<rama>
```

porque puede estar stale.

### Estados y exit codes

#### 0 · Sincronizado

Exit `0`:

```text
PR_HEAD_SINCRONIZADO
rama=<rama>
local=<sha>
remote=<sha>
refs_examinadas=<n>
```

#### 2 · Desactualizado

Si la rama existe pero el SHA remoto difiere del local:
Exit `2`:

```text
PR_HEAD_DESACTUALIZADO
rama=<rama>
local=<sha>
remote=<sha>
refs_examinadas=<n>
NO FUSIONAR
```

#### 3 · Rama ausente

Si `ls-remote` funciona correctamente pero no devuelve la rama solicitada:
Exit `3`:

```text
RAMA_AUSENTE_EN_ORIGIN
rama=<rama>
local=<sha>
refs_examinadas=0
NO FUSIONAR
```

#### 4 · Remoto no verificable

Si `git ls-remote` falla:
Exit `4`:

```text
HEAD_REMOTO_NO_VERIFICABLE
rama=<rama>
local=<sha>
refs_examinadas=<n-si-se-pudo-derivar>
NO FUSIONAR
```

Preservar stderr/salida diagnóstica suficiente para declarar qué se examinó.
Una rama ausente y un fallo de red/remoto son hallazgos distintos. No colapsarlos.

### Restricciones del helper

`tools/verifica_head_remoto.py` es sólo lectura.
Nunca:

* push;
* fetch;
* commit;
* merge;
* abre PR;
* llama GitHub API;
* cambia archivos.

No integrarlo en `tools/cierre_acto.py`.
`cierre_acto.py` es preflight/cierre de cascada, no guard de entrega.

### Integración en `/despacha`

Conservar su secuencia actual.
Después del último commit/push susceptible de alterar HEAD:

```bash
python3 tools/verifica_head_remoto.py
```

Si devuelve `PR_HEAD_DESACTUALIZADO`:

1. realizar UN:

```bash
git push origin <rama>
```

2. repetir UNA vez:

```bash
python3 tools/verifica_head_remoto.py
```

Si continúa:

* desactualizado;
* rama ausente;
* remoto no verificable;

terminar:

```text
NO FUSIONAR
```

No loop.
No abrir segundo PR.

### Integración en `/acto`

Para ejecución directa de `/acto`:

1. cerrar trabajo;
2. cascada;
3. commit;
4. push;
5. abrir único PR;
6. obtener número real;
7. escribir `## CONSUMIDO`;
8. commit;
9. push final;
10. baseline final si el árbol cambió;
11. `python3 tools/verifica_head_remoto.py`;
12. sólo entonces declarar el PR listo para mesa.

Cuando `/acto` corre bajo `/despacha`, `/despacha` conserva la propiedad del push/PR/guard.
No duplicar esos pasos.

### Verificación dirigida

No test permanente dependiente de red.
Demostrar el comportamiento con repositorio temporal bare si resulta barato.
Como mínimo deben quedar demostrados tres estados:

1. local == remoto → exit 0;
2. commit local sin push → exit 2;
3. push → exit 0.

También comprobar semánticamente:

* rama ausente → exit 3;
* fallo real de `ls-remote` → exit 4.

No crear un aparato de mocks si cuesta más que el defecto que protege.

### Aceptación del propio A

El propio PR de A debe terminar ejecutando:

```bash
python3 tools/verifica_head_remoto.py
```

y mostrar:

```text
PR_HEAD_SINCRONIZADO
local=<sha-final>
remote=<mismo-sha>
```

CONTADOR:

```text
clases observadas de merge con HEAD anterior protegidas: 0 → 1
```

Abrir un PR.
NO fusionar.

### COMPUERTA A → B

Esperar fusión de mesa.
Después:

```bash
git fetch origin main
```

Verificar por producto:

```bash
git show origin/main:tools/verifica_head_remoto.py
```

y comprobar que las instrucciones vigentes de:

```text
.claude/commands/acto.md
.claude/commands/despacha.md
```

incluyen el guard final.
No usar sólo historial de commits.
Si falta el producto:
cero commits de B.

## ACTO B · AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR

### Defecto real

`tools/cierre_acto.py` reconcilia actualmente:

1. cabecera de gobernanza;
2. L0.

Existe una tercera cita viva del mismo número en:

```text
canon/estado-programa-v1_12.md
```

fila:

```text
| **`gobernanza`** | `gobernanza-v1.15.md` | N ADR, protocolo de cambio |
```

Esta cifra ya requirió recifrado manual repetido.

### Objetivo

Después de que el humano cree el ADR y la anotación semántica L0:

```bash
python3 tools/cierre_acto.py --aplica
```

debe reconciliar mecánicamente:

1. cabecera de gobernanza;
2. L0;
3. fila `gobernanza` de la tabla de estado.

### Ancla exacta de la tabla

Usar el patrón correspondiente a:

```python
(\| \*\*`gobernanza`\*\* \| `gobernanza-v1.15.md` \| )(\d+)( ADR, protocolo de cambio \|)
```

Puntos críticos:

* la celda contiene literalmente `gobernanza-v1.15.md`;
* usar `v1.15`, con punto;
* NO usar el filename físico `gobernanza-v1_15.md` como texto del ancla;
* no anclar por número de línea.

Usar `re.subn(..., count=1)` o mecanismo equivalente que permita probar cardinalidad exacta.

### `estado-programa` se procesa una sola vez

Leer:

```text
canon/estado-programa-v1_12.md
```

una vez.
Sobre un mismo buffer en memoria:

1. aplicar sustitución L0;
2. aplicar sustitución de tabla.

El archivo se escribe una sola vez.
No hacer dos ciclos independientes de read/write.

### Atomicidad

Antes de escribir:

* cabecera gobernanza: exactamente 1 ancla;
* L0: exactamente 1 ancla;
* tabla: exactamente 1 ancla.

Preparar todos los contenidos.
Validar `1/1/1`.
Después confirmar.

Conservar la semántica heredada de E3:
si un `os.replace()` posterior falla después de que uno anterior ya confirmó, reportar el estado real.
Nunca afirmar:

```text
0 archivos escritos
```

cuando ya se escribió uno.

### Fase A

El dry-run debe informar:

```text
ADR reales: N
Cabecera declara: X
L0 declara: Y
Tabla estado declara: Z
```

y enumerar divergencias.

### Fase B

Salida exitosa cuando había divergencia:

```text
APLICADO: gobernanza X→N · L0 Y→N · tabla estado Z→N
```

Si ya coincide todo:

```text
sin cambios
```

### Tests

Modificar únicamente:

```text
tests/test_cierre_acto.py
```

Extender el fixture actual.
Cubrir:

1. dry-run detecta las tres cifras;
2. `--aplica` corrige las tres;
3. sólo cambian los dígitos autorizados;
4. se preserva la anotación semántica de L0;
5. ancla de tabla duplicada/rota aborta antes de escribir;
6. ancla L0 rota sigue abortando;
7. segunda corrida es idempotente;
8. conservar el caso actual de fallo del segundo `os.replace()` y reporte veraz.

No crear otra batería de tests.

### `/acto`

Actualizar únicamente la descripción para hablar de tres contadores:

* cabecera;
* L0;
* tabla de estado.

No ampliar autoridad de `cierre_acto.py`.
Siguen siendo humanas:

* redacción del ADR;
* anotación semántica L0;
* decisión de rótulos;
* firmas;
* decisiones.

### Verificación

```bash
python3 tests/test_cierre_acto.py
python3 tools/cierre_acto.py
python3 tests/check.py --baseline
```

Y al final:

```bash
python3 tools/verifica_head_remoto.py
```

### Aceptación

En el cierre real de B:

* el humano no recifra manualmente las tres cifras;
* `--aplica` hace la reconciliación;
* segunda corrida devuelve `sin cambios`.

CONTADOR:

```text
recifrados ADR mecánicos manuales por acto: 1 → 0
```

Abrir PR.
NO fusionar.

### COMPUERTA B → C

Esperar fusión de mesa.
Después:

```bash
git fetch origin main
```

Verificar el producto, no el nombre:

```bash
python3 tools/cierre_acto.py
```

El dry-run debe reportar:

* cabecera;
* L0;
* tabla.

Si no lo hace:
cero commits de C.

## ACTO C · AUTOMATIZA-2-C · SELLA-SIDECAR

### Defecto real

Las specs congeladas usan sidecar hermano:

```text
<sha256>  <basename>
```

Ejemplo de convención:

```text
S7-L17-spec-v1_1.md
S7-L17-spec-v1_1.sha256
```

No:

```text
S7-L17-spec-v1_1.md.sha256
```

El sidecar sustituye sólo la última extensión.

### Objetivo

Crear:

```text
tools/sella_sha256.py
```

para sellar o verificar únicamente archivos pasados de forma explícita.

### Derivación del sidecar

Para:

```text
ruta/S7-L17-spec-v1_1.md
```

producir:

```text
ruta/S7-L17-spec-v1_1.sha256
```

Equivalente conceptual:

```python
path.with_suffix(".sha256")
```

No concatenar `.sha256` al filename completo.

### Sellado

```bash
python3 tools/sella_sha256.py ruta/spec.md
```

Escribe exactamente:

```text
<64-hex-minúsculas><dos espacios><basename>\n
```

Hash calculado sobre los bytes exactos del archivo.
Escritura atómica simple:

* temporal en mismo directorio;
* `os.replace()`.

### Verificación

```bash
python3 tools/sella_sha256.py --verifica ruta/spec.md
```

Nunca escribe.
Debe distinguir al menos tres resultados.

#### Exit 0 · válido

```text
SELLO_COINCIDE
```

#### Exit propio · sidecar ausente

Por ejemplo exit `2`:

```text
SIDECAR_AUSENTE
```

No llamarlo hash discordante.

#### Exit propio · sidecar presente pero incorrecto

Por ejemplo exit `3`:

```text
SELLO_NO_COINCIDE
```

Incluye:

* hash esperado;
* hash real;

o diagnóstico de formato/basename si ése es el defecto.

No es necesario crear una taxonomía de diez exits. El requisito es distinguir ausencia de discordancia.

### Rechazos de entrada

Rechazar:

1. fuente cuyo nombre termina en `.sha256`;
2. directorio.

Dar error claro y exit distinto de cero.
No tratar un directorio como lote implícito.

### Prohibiciones

NO:

* glob;
* descubrir archivos;
* caminar directorios;
* sellar recursivamente;
* sellar todo `forense/prereg-caja`;
* timestamps;
* YAML;
* registry de hashes;
* firmas;
* Git;
* decidir autorización semántica de una modificación.

No integrarlo globalmente a `/acto`.
Un cambio accidental en una spec no debe volverse aceptado automáticamente sólo porque el cierre reselló el archivo.

### Verificación dirigida real

Primero:

```bash
python3 tools/sella_sha256.py --verifica \
  forense/prereg-caja/S7-L17-spec-v1_1.md
```

Debe aceptar el sidecar vigente sin modificarlo.
Elegir un segundo sidecar real como control.
No veinte.

Después, fixture temporal:

1. crear `ejemplo.md`;
2. sellar;
3. verificar → éxito;
4. guardar contenido del sidecar;
5. modificar un byte de `ejemplo.md`;
6. verificar → discordancia;
7. comprobar que `--verifica` no cambió el sidecar;
8. comprobar sidecar ausente;
9. comprobar rechazo de directorio;
10. comprobar rechazo de `.sha256`.

No crear test permanente salvo que durante la implementación aparezca un defecto real que justifique conservarlo.

### Cierre

```bash
python3 tests/check.py --baseline
python3 tools/verifica_head_remoto.py
```

CONTADOR:

```text
transcripciones manuales necesarias para construir un sidecar: 1 → 0
```

Abrir PR.
NO fusionar.

## RENUMERA-DIAGNÓSTICO · DESCARTADO

No ejecutar.
No codificar.
No documentar adicionalmente.
No crear ADR.
No crear backlog.

Razón:
`tools/estado_comun.py` + `tools/cierre_acto.py` ya cubren la parte mecánica útil:

* ADR máximo;
* FP máximo;
* ramas remotas;
* candidato ADR;
* detección mecánica básica.

Lo restante necesita juicio editorial/semántico:

* texto propio vs texto heredado;
* cuerpos verbatim;
* mappings encadenados;
* derivados regenerables;
* conflictos de prosa.

No convertir eso en automatización preventiva.
Reabrir sólo si un defecto futuro revela un subpaso concreto, repetido, determinista y barato de automatizar.

## TRABAJO QUE SIGUE EN PARALELO PERO NO PERTENECE A ESTE PAQUETE

No absorber en A/B/C:

* TRÁMITE-5;
* N18;
* FP-328;
* ponderador ENNViH `fac_3b_px`;
* tablero/relaciones relacionados;
* `forense/benchmark/`;
* specs sustantivas correspondientes.

Tampoco convertir el estado de cron en AUTOMATIZA:
si falta `censo/2026-09-07` según su playbook, aplicar el playbook vigente. No abrir acto nuevo por ello.

Después de C, la prioridad estratégica vuelve a trabajo sustantivo.
Dirección ya identifica:

```text
M-POR-CELDA
```

como trabajo de modelo relevante: el emisor del duelo todavía no consume las 21 reglas medidas.
Eso va antes de buscar un `AUTOMATIZA-3`.

## REPORTE FINAL DEL PAQUETE

Después de C, reportar a mesa:

1. qué se automatizó;
2. defecto/repetición concreta que justificó cada pieza;
3. medición antes → después;
4. qué sigue explícitamente humano;
5. resultado final de `python3 tests/check.py --baseline`;
6. SHA local y SHA remoto final de cada PR;
7. pieza descartada y por qué.

No reportar volumen de trabajo como resultado.
No abrir auditoría retrospectiva.
No buscar nuevas automatizaciones para "aprovechar" la sesión.
La tanda termina con C.

---

# DICTAMEN · PLAN AUTOMATIZA-2 · CABLEADO POST-E3

**GAP DE ARCHIVO, declarado explícitamente en vez de fabricado o silenciado.**

`PAQUETE DE LANZAMIENTO · AUTOMATIZA-2 · A → B → C` (abajo) identifica este
dictamen como dirección Fable, 7/sep/2026, `sha256`
`b6b754903372b609f90ebb93197f1a6b29b6c265d95d015320d3d2d098a84f7a`, y pide
archivarlo verbatim junto al encargo final y al propio paquete.

Su texto **no llegó a esta sesión**: no vino pegado en el mensaje que
invocó `/acto`, no hay archivo adjunto que lo traiga, y una búsqueda sobre
el árbol completo (`grep` del `sha256` citado, `grep -li dictamen` sobre
todo `*.md`, `git log --all` por rótulo) no encontró ningún rastro previo
—tampoco lo trajo ningún acto anterior de esta serie (`AUTOMATIZA-2-E4`,
`AUTOMATIZA-2-E5`).

El `ENCARGO FINAL` de arriba declara en su primera línea que "incorpora y
consolida" tanto el plan como este dictamen — es decir, la sustancia
ejecutable de `AUTOMATIZA-2-A/B/C` ya vive, consolidada, en el encargo
final archivado arriba. La ausencia del texto propio del dictamen es una
deuda de *provenance* (un tercer documento fuente sin copia local), no una
falta de especificación: no bloquea la ejecución de `A`, y se declara así
en el ADR de cierre de este acto en vez de PARAR o de fabricar un texto
que no se puede verificar contra el `sha256` citado.

Si dirección/mesa considera necesario cerrar este gap, el texto verbatim
del dictamen puede pegarse en un PR posterior que lo añada a este mismo
archivo, verificando su `sha256` al pegarlo.

---

# PAQUETE DE LANZAMIENTO · AUTOMATIZA-2 · A → B → C (nube) · 7/sep/2026
### dirección (Fable) · contra `origin/main = e1c3c84` (#580 — **E4 fusionado**) · ramas vivas: ninguna · PR abiertos: 0 · ADR/FP: derivar en el 0-bis con `tools/cierre_acto.py` · MODELO SUGERIDO: Sonnet «ultracode» (puede subir, nunca bajar)

## 0 · Qué es este documento y qué no
El **encargo** es el texto `ENCARGO FINAL · AUTOMATIZA-2 · CABLEADO POST-E3` (adjunto de mesa, gobierna) más el `DICTAMEN · PLAN AUTOMATIZA-2 · CABLEADO POST-E3` (dirección, sha256 `b6b754903372b609f90ebb93197f1a6b29b6c265d95d015320d3d2d098a84f7a`); donde difieran, las precisiones del dictamen mandan, como el propio encargo dice. Este documento **no los repite**: añade la cabecera de la casa, la condición verificada, la concurrencia real de hoy y la instrucción de archivo. Se archiva junto a los otros dos.

## 1 · Condición de lanzamiento — cumplida y verificada por producto
- `acto/automatiza-2-e4-pdn-compara` → **fusionado como #580** (`git log -1 origin/main` = `e1c3c84 Merge pull request #580`); `git ls-remote --heads origin` → sólo `main`; GitHub API `pulls?state=open` → 0. A puede arrancar ya.
- E4 cerró con la cascada vigente; A cambia el guion de entrega **después**, como quería el encargo.

## 2 · Cabecera de la casa (A, B y C)
- Cada acto invoca `/acto`: ARRANQUE (nube: `ls data/raw/` ausente → «no aplica», declarado); guard de rama (`git ls-remote --heads origin | grep -i automatiza-2-<a|b|c>` → coincidencia = PARA); 0-bis A.3 con **tres archivos verbatim** en `forense/encargos/2026-09-0X-AUTOMATIZA-2-<A|B|C>.md`: el encargo final, el dictamen y este paquete (con el sha256 del dictamen verificado al pegar); push del 0-bis al primer minuto.
- Rótulos ADR/FP derivados en el 0-bis con `tools/cierre_acto.py` (dry-run pegado); no se hereda 372/329 ni ningún número del encargo.
- Cascada D-10 con `cierre_acto.py --aplica` tras escribir la sustancia; `python3 tests/check.py --baseline` VERDE o PARO-reporta; `## CONSUMIDO`; y desde A en adelante, `python3 tools/verifica_head_remoto.py` como último paso antes de declarar el PR listo (A lo aplica sobre sí mismo).
- El ejecutor propaga; si el terreno no cuadra con el encargo (línea, ancla, formato de sidecar), PARA con archivo y línea — precedente ADR-358. *Si te encuentras escribiendo fuera de la lista de tu acto, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.*
- Perímetros por acto (del encargo, resumidos para el guard): **A** `tools/verifica_head_remoto.py` (nuevo) · `.claude/commands/acto.md` (cierre, dos fases) · `.claude/commands/despacha.md` (guard final) · notas · A.3 · cascada. **B** `tools/cierre_acto.py` (tercera ancla) · `tests/test_cierre_acto.py` (extensión) · `.claude/commands/acto.md` (una frase: tres contadores) · notas · A.3 · cascada. **C** `tools/sella_sha256.py` (nuevo) · runbook de sellado sólo si existe uno único y obvio · notas · A.3 · cascada. Ninguno toca corpus, manifiesto, cola, relaciones, motor, `baseline --freeze`, CI ni `Downloads`.

## 3 · Concurrencia — lo que corre al lado y no se cruza
**Nube, en paralelo con A/B/C (ya escritos, se lanzan cuando mesa quiera):**
- `MAESTRA38-TRAMITE-5` — FP-327 (obsoleta: #573 ya trajo el v1.5), FP-328 (a)(b), benchmark v1.2 al repo en `forense/benchmark/`, filas D1/D4. Toca tablero TSV, relaciones (4 filas + 1 fuente), `forense/benchmark/`, INFRAESTRUCTURA.
- `MAESTRA38-N18` — S6 v1.1 (y S7 v1.2 si aplica) rama A con ponderador **`fac_3b_px`** adjudicado. Toca `forense/prereg-caja/`.
- Intersección con A/B/C: sólo la cascada y `_T25_ARCHIVOS_CONOCIDOS` (append; quien fusiona segundo conserva ambas entradas). **C no debe resellar** las specs que N18 cree: N18 escribe sus propios sidecars a mano (o con `sella_sha256.py` si C ya fusionó — se dice cuál).
**Caja: nada de este paquete.** Está libre. Lo siguiente en caja es `MAESTRA38-L16-BIS · RAMA A ENNViH` (Opus), gateado a N18 sellado; se redacta completo cuando N18 fusione, con S6 v1.1 y su sha como COMMIT-1. Hasta entonces la caja sólo tiene el cron: `censo/2026-09-07` no existe todavía (03:02 UTC = 21:02 CST del domingo; primera prueba del programador 07:35 CST) — si a las 07:40 no está, playbook §5 de `forense/cron/REGISTRO-CRON-v1_0.md`, sin acto nuevo.

## 4 · Orden de mesa
1. Lanzar **A** ahora (nube). Al fusionar A, lanzar **B**; al fusionar B, lanzar **C**. Nunca apilar.
2. En paralelo, cuando quieras: TRÁMITE-5 y N18 (nube). Al fusionar N18: L16-BIS (caja).
3. Después de C: reporte final del paquete (los siete puntos del encargo) y **parada**. Lo siguiente es dirección, no aparato: `M-POR-CELDA`.

**Contadores movidos por este documento: cero.** Declarado.

## CONSUMIDO

Ejecutado: **ACTO AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR**, únicamente — `C` queda para lanzarse por separado, desde `main` fresco, después de que mesa fusione este PR (regla de la casa de esta misma tanda: no apilar).

**PR:** [`#584`](https://github.com/Josanoforo/Modelado-Mexicano/pull/584), rama `claude/automatiza-2-cableado-post-e3-mb1anf`, contra `main`. **NO fusionado por el ejecutor** — mesa fusiona.

**Condición de lanzamiento**, verificada por producto al arrancar: `A` ya fusionada (`origin/main = 3a04d5359566c073e8bd49cd3c32db8b7ef58f48`, `Merge pull request #582`), `git show origin/main:tools/verifica_head_remoto.py` existe, y `.claude/commands/acto.md`/`.claude/commands/despacha.md` en `origin/main` ya traen el guard final de HEAD.

**Gap de archivo declarado (heredado de A).** El `DICTAMEN · PLAN AUTOMATIZA-2 · CABLEADO POST-E3` (sha256 `b6b754903372b609f90ebb93197f1a6b29b6c265d95d015320d3d2d098a84f7a`) sigue sin llegar a ninguna sesión de esta tanda — re-verificado contra el árbol fresco tras la fusión de `A`, sin rastro nuevo.

**Qué se hizo.** `tools/cierre_acto.py` gana `TABLA_ADR_RE` (ancla la fila `gobernanza` de la tabla de nombres estables de `canon/estado-programa-v1_12.md` §0, sobre el nombre cosmético con punto, nunca el filename físico ni por número de línea). `canon/estado-programa-v1_12.md` se lee y se escribe una sola vez: `L0` y la fila de tabla se reconcilian en secuencia sobre el mismo buffer, cada paso validado contra su buffer inmediato anterior. Atomicidad ampliada a `1/1/1` anclas antes de escribir; preserva la semántica de `E3` sobre el fallo del segundo `os.replace()`. `tests/test_cierre_acto.py`: 7 pruebas (dos nuevas/reescritas para la tercera ancla, incluido el caso distinto de tabla rota vs. `L0` rota). `.claude/commands/acto.md` §4 paso 3: una frase, "los TRES contadores".

**Aceptación real, demostrada en el propio cierre de este acto.** Al redactar `ADR-376` y su anotación `L0` (humano), corrí `python3 tools/cierre_acto.py --aplica`: `APLICADO: gobernanza 375->376 · L0 375->376 · tabla estado 375->376` — las tres cifras en un solo paso, sin recifrar ninguna a mano. Segunda corrida: `sin cambios -- cabecera, L0 y tabla estado ya declaran 376, igual al real` (idempotente).

**Commits:** 0-bis (`d43707b`, este archivo verbatim) · COMMIT 1 (`c153918`, `tools/cierre_acto.py` + test) · COMMIT 2 (`db19e21`, `.claude/commands/acto.md`) · cascada (`448dbbe`, `ADR-376`/`L0`/`T25`) · este commit (`## CONSUMIDO`).

**`python3 tests/check.py --baseline`**: LÍNEA BASE VERDE, sin regresión nueva.

**Perímetro cumplido tal como el encargo lo declaró.** Tocó `tools/cierre_acto.py` (tercera ancla) · `tests/test_cierre_acto.py` (extensión) · `.claude/commands/acto.md` (una frase) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_12.md` · `tests/check.py` (sólo `_T25_ARCHIVOS_CONOCIDOS`) · A.3 (este archivo) · cascada. **No tocó** corpus, `data/raw`, `descargas_mx`, raíces físicas, manifiesto, adquisición, relaciones, motor, `baseline --freeze`, CI, GitHub Actions, reglas de protección de rama, `Downloads`.

**CONTADOR final:** recifrados ADR mecánicos manuales por acto, `1 → 0`.
