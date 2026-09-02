# Agente de adquisición · v1.0 — runbook de mesa

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
Corre /adquiere sobre las 5 filas mas antiguas de
data/curacion-registro/cola-adquisicion-registro.tsv cuyo ultimo intento
tenga >= 7 dias (o sin intento previo), en este clon, entorno CAJA (no
NUBE): confirma /home/pc0/mm-corpus/raw montado y red real a
inegi.org.mx antes de caminar una sola fila.
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
