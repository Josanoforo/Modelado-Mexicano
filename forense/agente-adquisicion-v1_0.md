# Agente de adquisición · v1.0 — runbook de mesa

> ## ENMIENDA DE PRECEDENCIA — qué sección gobierna HOY
>
> Añadida por `ACTO GEN2-SONDA-ADQ-CABLEADO` (9/sep/2026, P1/P2,
> `forense/encargos/2026-09-09-GEN2-SONDA-ADQ-CABLEADO.md`), a partir del §4
> de `forense/notas/2026-09-09-REVISION-CABLEADO-SONDA-ADQUISICION-astra.md`
> («también hay documentación desfasada: el registro canónico aún encabeza
> cron de WSL, describe el vigilante anterior… el instalador y el código ya
> emplean otro mecanismo. Debe haber una enmienda visible que diga qué
> sección gobierna hoy»). Se enmienda por fecha, **no** reescribiendo el
> texto histórico: lo de abajo se conserva para poder auditar qué se decidió
> y cuándo.
>
> | Asunto | Qué gobierna HOY | Qué queda como histórico |
> |---|---|---|
> | **Disparador** | Windows Task Scheduler, tarea `\ModeladoMexicano\AdquiereCron`, instalada por `tools/windows/instala-tarea-adquisicion.ps1` (`ACTO ADQ-CRON-V2`, 7/sep/2026) | La «línea de crontab sugerida» del final de este archivo, y toda mención de `crontab -e` en la caja. El cron de WSL **está retirado**: no se instala, y si sigue instalado en alguna caja es hallazgo a reportar, no el mecanismo vigente. `adq_doctor.check_crontab_legado()` lo vigila por eso. |
> | **Selección de filas** | `.claude/commands/adquiere.md` §1, «CONTRATO ÚNICO DE ELEGIBILIDAD Y ORDEN», proyectado con `python3 tools/adq_doctor.py --selecciona` | La regla que el prompt de §1 traía por su cuenta («las 5 más antiguas con último intento ≥ 7 días»), que divergía del orden por prioridad de la skill. El prompt ahora **cita** el contrato en vez de repetirlo. |
> | **Vigilante** | `tests/check.py` T31 tras H1 (evidencia fusionada primaria, filtrado por fecha y `run_id`, `SIN-EVIDENCIA-NO-VERIFICABLE` para lecturas fallidas) y `tools/adq_doctor.py` que lo reusa | La lectura por rama `censo/<fecha>` como requisito, y el `COMPLETO` derivado de un cuerpo `[ADQ]` sin comprobar su fecha. |
> | **Horario** | `data/adq-config.yaml:calendario` es la autoridad única: lun-vie 07:30, `America/Mexico_City` / `Central Standard Time (Mexico)`. Instalador, runner, doctor y T31 lo consumen mediante `tools/adq_config.py`. | Las copias literales de 07:30 y la zona local en las secciones históricas inferiores. |
> | **Ejecutor** | `data/adq-config.yaml:ejecutor = codex`; `tools/adquiere_launcher.sh` resuelve la revisión antes de cargar el runner y `codex exec` corre no interactivo con `danger-full-access` en el clon dedicado. La corrida real del 11/sep demostró que `workspace-write` deja `.git` de sólo lectura e impide commit/push. | Claude y sus límites quedan como antecedente histórico. Sólo `ejecutor: claude` explícito activa compatibilidad; nunca hay fallback silencioso. El acceso pleno no autoriza compras, contacto, identidad inventada ni cambios fuera del encargo. |
>
> **Propagación ejecutada por GEN2-SONDA-CRON-PRODUCCION:** la advertencia
> anterior queda satisfecha sin cambiar la conducta (lun-vie 07:30). Los
> consumidores leen una sola autoridad. `ejecutor_timeout_segundos`,
> `ejecutor_kill_after_segundos` y `calendario.ventana_observacion_minutos`
> son tres límites distintos y se reportan por separado.

**P3** de `ACTO MAESTRA34-N7 · SKILLS-COLA-Y-ADQ`
(`forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md`, SHA de
redacción `e4af4ed`, merge `PR #455`).

Este archivo es para **mesa**, no para el ejecutor. Es la tercera
automatización del modelo `D-13`/`ADR-237`: la primera (`/tramite`,
`ADR-239`) hace el papeleo, la segunda (`/despacha`, `ACTO MAESTRA33-E2`)
ejecuta encargos de la cola, y esta **camina la cola de adquisición**
(`/adquiere`) sobre las filas más viejas sin intento reciente, en un
entorno que las dos anteriores no pueden usar: la caja Ubuntu/WSL de mesa,
por cron, sin `ANTHROPIC_API_KEY` — el mismo mecanismo sin API que
`runner_l_cli.py` (firma `MAESTRA33-E17`).

Firma de mesa que autoriza esta pieza (`DC-a`, verbatim, 1/sep/2026):

> «DC - a, DM2-a, MAESTRA34-E1- Escríbelo.» (mesa escribió el rótulo
> pelado; serie añadida por dirección para `T25`, `ADR-128`)

y antes, la razón medida (verbatim):

> «DC- pero eso solo puede correr en ubuntu, cloud claude code no tiene
> acceso a hacer esas revisiones y nos topamos con falla por eso migramos
> a ubuntu.»

**Nota de trazabilidad**: al redactar este runbook no se encontró en
`forense/` una nota separada de `N6` que documente "la vía de las tres
capas" con ese nombre exacto — `ACTO MAESTRA34-N6 · CURADOR-Y-SUITE` deja
escrito el mecanismo de alta en tres tablas de la **capa de relación**
(`tools/curador_registro/GUIA-CURADOR-REGISTRO.md`, sección «alta de
fuente nueva en tres tablas»), y `/adquiere` (`.claude/commands/adquiere.md`
§5/§6) ya escribe la **capa payload** (`data/manifiesto.yaml`) y la
**capa cola** (`data/curacion-registro/cola-adquisicion-registro.tsv`) en
su curso normal. §1 de abajo documenta la estructura de tres capas de
forma genérica a partir de esas dos fuentes, sin inventar un nombre ni un
archivo que no existe hoy en el árbol — esto no es una compuerta, es una
referencia de contexto declarada como tal.

---

## §1 · El prompt exacto

Cadencia sugerida: **lun-vie, 07:30 hora de mesa (GMT-6)** — ver §2 para
la línea de crontab sugerida, que mesa instala a mano.

Pega esto, tal cual, como prompt de la tarea recurrente (o pásalo por
`tools/adquiere_cron.sh`, que hace exactamente esto):

```text
Lee completa .claude/commands/adquiere.md y ejecuta ese procedimiento en
este clon, entorno CAJA (no NUBE): confirma
/home/pc0/mm-corpus/raw montado y red real a inegi.org.mx antes de
caminar una sola fila.
Lee también completa .claude/commands/sonda.md. Antes de cerrar por cero
descargas, ejecuta la selección de investigación que entrega el wrapper. Para
cada necesidad elegida busca realmente fuera del corpus, persiste progreso y
frontera por versión, y enlaza toda candidata pública al mandato GEN2-38. Si
ambas selecciones están vacías, cierra sin LLM; si hay investigación aunque
no haya descarga, no cierres como cola vacía.
La seleccion NO se re-decide aqui: el contrato unico de elegibilidad y
orden vive en .claude/commands/adquiere.md seccion 1, y se proyecta con
`python3 tools/adq_doctor.py --selecciona --maximo 5`. Pega su salida
-- IDs elegidos, excluidos y razon, incluso cuando los elegidos son
cero -- en el cierre de la caminata, ANTES de tocar ninguna fila. Una
caminata vacia con su lista emitida es informacion; una caminata vacia
sin lista es indistinguible de una seleccion equivocada.
La antiguedad se cuenta desde el intento efectivo de descarga, nunca
desde la fecha de descubrimiento de via que escribe /sonda. No actives
en bloque SIN-FETCH, OBTENIDO-PARCIAL ni negativos: una recomendacion
de /sonda sin autorizacion citada permanece propuesta.
Registra cada fila caminada por las tres capas: la capa payload
(data/manifiesto.yaml, via tests/manifiesto.py --registra), la capa cola
(data/curacion-registro/cola-adquisicion-registro.tsv, estado_A4A5) y la
capa de relacion cuando la fila lo amerite (relaciones.tsv /
evidencias.tsv / utilidad-modelo.tsv, via la GUIA-CURADOR-REGISTRO.md que
N6 dejo escrita) -- nunca edites data/cola-adquisicion-v1_0.tsv a mano,
es vista generada (tools/vista_cola_adquisicion.py la regenera).
Toda fila que cierre en NO-OBTENIDO-POR-ESTE-AGENTE o se reclasifique a
NO-ACCESIBLE va al PAQUETE-RECETAS-<fecha> del dia, un solo bloque.
Abre UN PR titulado [ADQ] <fecha> para firma de mesa y NO lo fusiones.
No invoques tools/adquiere_launcher.sh ni tools/adquiere_cron.sh: ya eres el
unico hijo de la corrida y volver a llamarlos seria recursion.
Si nada cambio (cero filas elegibles, o las 5 elegibles ya estaban
resueltas por otro proceso), cero commits -- una caminata vacia tambien
es informacion y no se fuerza un PR sin contenido.
```

Las **cuatro rutas del registro** que este prompt cita, columnas del
mecanismo que `/adquiere` ya gobierna (`.claude/commands/adquiere.md`):

1. `data/curacion-registro/cola-adquisicion-registro.tsv` — la fuente
   real de la cola (desde `ACTO MAESTRA33-A5`); `data/cola-adquisicion-v1_0.tsv`
   es su vista generada, nunca se edita a mano.
2. `data/manifiesto.yaml` — capa payload, un `sha256` por instrumento
   adquirido, gobernada por `tests/manifiesto.py`.
3. `data/curacion-registro/relaciones.tsv` (con `evidencias.tsv` y
   `utilidad-modelo.tsv` desde `ACTO MAESTRA34-N6`) — capa de relación,
   cuando la fila adquirida amerita una fila ahí.
4. El `PAQUETE-RECETAS-<fecha>.md` del día — el artefacto que
   `data/INFRAESTRUCTURA-v1_0.md` Dominio 1 declara para las filas que no
   se pudieron cerrar programáticamente.

Cuando una necesidad nueva queda detrás de un padre parcial u obtenido, el
alta canónica se hace con `python3 tools/adq_residual.py --help`. No es otra
cola: usa `tsv_crudo.upsert_fila`, conserva el padre y regenera la vista. El
selector y el recibo leen su metadata para separar residuales cubiertos,
accionables, pendientes de acceso, sin vía, en reintento o pendientes de
decisión; por eso `0 elegidos` ya no se interpreta como `0 necesidades`.

## §2 · Entorno

**UBUNTU/WSL de mesa, exclusivamente.** No corre en nube, sin excepción.

La razón es medida, no de preferencia (firma `DC-a` citada arriba,
verbatim): *"cloud claude code no tiene acceso a hacer esas revisiones y
nos topamos con falla por eso migramos a ubuntu."* Se buscó en
`canon/notas` y en `forense/` una entrada fechada 5/ago/2026 que
detallara la falla con más precisión que esa cita, y **no se encontró
ninguna** con esa fecha y ese contenido exactos — la razón que gobierna
esta pieza es la de la firma de mesa arriba, citada tal cual, no una
reconstrucción.

Lo que sí es medible y consistente con esa razón: `/adquiere` (§0 de su
propio archivo) exige `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `<sin
variable>` (CAJA, no NUBE) antes de tocar una sola fila, y `data/raw/`
solo existe enlazada al corpus compartido en esa caja
(`/home/pc0/mm-corpus/raw`) — una sesión de nube no tiene ese symlink ni
la sonda de red que confirma acceso real a `inegi.org.mx`.

`tools/adquiere_cron.sh` (§3 de abajo) hace las tres verificaciones de
entorno **antes** de invocar `claude -p`: clon al día (`git pull`),
corpus montado (`ls data/raw | head -1`, tercera parte de `A.2`), y
sonda de red cruda a `inegi.org.mx`.

### Herramientas de entorno de la caja (añadido 2/sep/2026, `ACTO MAESTRA35-A1`, firma de mesa e1)

**Extraer un `.rar`: `/mnt/c/Windows/System32/tar.exe`.** Windows 10 1803+
trae `bsdtar`/`libarchive` de serie en `System32`, y libarchive lee RAR3.
En esta caja **no hay ningún extractor nativo de Linux** (`unrar`, `unar`,
`7z`, `7za`, `7zz`, `p7zip`, `bsdtar`: los siete ausentes), y `sudo` no es
una salida — dentro del sandbox devuelve `The "no new privileges" flag is
set` y fuera `A terminal is required to authenticate`, así que **ningún
agente puede completar un `apt-get install`**; lo tiene que teclear el
operador. La vía de Windows es, por tanto, la única disponible sin operador:

```
cd <dir>; /mnt/c/Windows/System32/tar.exe -xvf archivo.rar
```

**Requisito: correrlo FUERA del sandbox.** Dentro falla con
`<3>WSL (10 - ) ERROR: UtilConnectUnix:526: socket failed 1` y `exit=1` — es
el socket del interop de WSL, **no** la herramienta. El síntoma se lee
igual que «no sirve» y ya costó dos actos (`MAESTRA34-L6`,
`MAESTRA35-L3`): ver `forense/hallazgos.md`, 2/sep/2026. Mismo cuidado con
`/mnt/c/Windows/System32/curl.exe`, presente por si la red de Linux falla.

**`rarfile` 4.5 y `py7zr` 1.1.3 están instalados**; `patoolib` y
`libarchive` no. `rarfile` sin binario de respaldo aborta con
`RarCannotExec: Cannot find working tool` — el hueco es el binario, no el
módulo.

**Control cruzado obligatorio al extraer**: comparar los tamaños que
`rarfile.infolist()` declara *antes* de extraer contra los del archivo
extraído, y correr `zipfile.testzip()` si el resultado es ZIP/XLSX. Un
extractor que devuelve `exit=0` no garantiza contenido íntegro.

## §3 · Falsador, a un mes

Se **retira** la pieza (runbook + cron) si en un mes:

- **ninguna corrida registra un payload** (cero altas nuevas en
  `data/manifiesto.yaml` atribuibles a esta pieza), **y**
- **ninguna corrida produce una receta que mesa efectivamente ejecute**
  (el `PAQUETE-RECETAS-<fecha>` se genera pero nadie lo camina).

Cualquiera de las dos condiciones sola no basta para el falsador — puede
haber un mes sin payload nuevo porque la cola entera está `NO-ACCESIBLE`
o `OBTENIDO`, y eso es información legítima, no fallo de la pieza. Es la
combinación de las dos —cero payload **y** cero receta ejecutada— la que
dice que el vehículo no está produciendo nada que mesa use, y dispara
revisión. Mismo criterio de caducidad que `D-10`..`D-13`
(`instrucciones-proyecto-v2_12.md`) y que los falsadores de
`forense/agente-tramite-v1_0.md` §3 y `forense/agente-despacho-v1_0.md`
§3.

El digesto de trámite (`tools/digesto_tramite.py`) lee `forense/agente-*.md`
para derivar la fecha de revisión de cada pieza — este archivo entra a
esa lectura automáticamente, sin cableado adicional.

**CONTADOR de este acto (P3): cero mediciones, declarado.** Es
infraestructura: instala el vehículo, no mide con él.

---

## Línea de crontab sugerida (NO instalada por este acto)

```cron
30 7 * * 1-5 cd /ruta/al/clon && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1
```

Lun-vie, 07:30, en la zona horaria local de la caja (GMT-6 si la caja
está en esa zona; si `cron` corre en UTC, ajustar a `30 13`). **Instalar
esta línea (`crontab -e` en la caja de mesa) es tarea de mesa** — este
acto la escribe y no la ejecuta, tal como el runbook de despacho dejó
escrito para su propia tarea recurrente en Claude Code.
