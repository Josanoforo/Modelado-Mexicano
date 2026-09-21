# Nota de cierre · ACTO GEN2-ENIGH2024-RESERVA-Y-DISENO-1

**ADR:** `ADR-260921-GEN2-ENIGH2024-RESERVA-Y-DISENO-1-b7ae-01` · **0-bis:** `b7ae01e` ·
**Encargo:** `forense/encargos/2026-09-21-GEN2-ENIGH2024-RESERVA-Y-DISENO-1.md`
(sello de cuerpo `e165564d6a03e743`) · **MODO:** ABIERTO · **COMPUERTA:** ninguna ·
**CONTADOR:** ninguno — `cuenta_gen2 = NO`, este acto no sella corrida.

## 0 · ARRANQUE (firma cruda)

```
ENTORNO · commit=fc13cdcc56bd · git_status=LIMPIO(0) · python=3.11.15
· numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE yaml=6.0.1 pyreadstat=AUSENTE
· CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
· red=000 · raices=data_raw:NO · corpus=NO(examinados=0)
```

Tres partes de A.2: variable `cloud_default` · sonda `http_code=000 http_connect=403`
· corpus **no montado, 0 archivos examinados** (A.13). `data/raw` ausente: **no es PARO**
y no se enlazó porque este acto **no abre microdato** — la latitud de §6 permite saltarlo
y se declara. Guard 0.a: `git rev-list --count HEAD..origin/main = 0` tras `git fetch --prune`
(el hook había reportado `detras=535` **sin fetch**; tras fetch, al día — premisa de
logística que cayó y se resolvió, D-19). 0.b: árbol limpio. 0.c: sin rama remota, sin
worktree y **cero PR abiertos** en el repo con el rótulo. 0.d: higiene reportada, no aplicada.

## 1 · El entorno que el encargo asignó, y el que había

El encargo asigna **NUBE `milpa-inegi`**, «se reconoce por la sonda de red, no por la
variable». La sonda salió **DENEGADA**, confirmada con **dos intentos** contra la URL real
del cuestionario 2024 (`curl: (56) CONNECT tunnel failed, response 403`).

A.5, literal: **NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS.** No se concluye nada sobre el
portal de INEGI: el veredicto es sobre esta sesión y su proxy, no sobre la fuente. Receta
manual de un minuto para quien tenga egreso: `curl -sS -o enigh2024_cuestionario.pdf
https://www.inegi.org.mx/contenidos/programas/enigh/nc/2024/doc/<nombre>.pdf`, verificando
el **cuerpo** y no solo el `200` — el hallazgo D3 del 21/sep ya documentó que INEGI devuelve
`200` con plantilla «Página no encontrada».

**Esto no fue PARO** (no es «entorno equivocado» de §7): el propio encargo previó la rama —
«Si la sonda sale DENEGADA: haz P0, P1 y P3 con lo que hay en el repo, deja P2 con NC y
dilo». Es lo que se hizo.

## 2 · Premisas del encargo, verificadas por su rótulo

| premisa | rótulo | veredicto |
|---|---|---|
| `enigh2012..2022_nc_csv` (seis olas); ENIGH 2024 con 0 entradas y fila `residual:ENIGH_2024_NC` prioridad 2 | `[EJECUTADO]`/`[LEÍDO]` | **SE SOSTIENE.** Fila 159 de la vista, `ids_manifiesto = SIN-ID-MANIFIESTO` |
| los sellados que leen ENIGH | `[EXISTE]` | **SE SOSTIENE y se completa**: los 7 nombrados existen; el censo por replay añade que ninguno más lee ENIGH (`CALC-R-FAM-M-05/06/07` citan el marco, no la ola) |
| **«que alguno trae el mismo estimando medido en ≥3 olas»** | `[SUPUESTO]` | **SE SOSTIENE — y era lo que P1 debía averiguar.** Uno solo: `remesas>0`, cinco olas. Ver §3 |
| `DISENO-duelo-prospectivo-ENVIPE2026-v1_0.md` archivado | `[LEÍDO]` | **NO SE SOSTIENE**: **NO-ENCONTRADO** en `forense/prereg-caja/` (universo: 56 archivos, `ls`). Se tomó la rama que el encargo previó: el texto de la firma **F7** (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-07`), leído verbatim. Premisa de **logística**, objetivo alcanzable → se replanteó y se declara (§2 de instrucciones, D-19) |
| interacción cruda 10.6 pp, encogida 1.9, piso 3.4 | `[LEÍDO]` | no re-verificada: **no se usa**, porque este duelo no tiene nivel de cruce (§4) |

**«Ya hecho», repetido por objeto con acceso propio** (§4 del encargo lo ordena):
`grep -rilE 'ENIGH[ _-]?2024'` sobre **3 466** archivos `.md`/`.tsv`/`.yaml`/`.py` → **35**
con coincidencia, ninguna una reserva ni un diseño; `decisiones.tsv` (185 filas) tenía
**una sola** clave `reserva:*`, `reserva:envipe2026`. Vocabulario A.4: **EXISTE-NO-SATISFACE**
para la reserva (la fila de cola existía y decía `REGLA ESPECIAL: ninguna`),
**NO-ENCONTRADO** para el diseño. La premisa de §4 se sostiene.

## 3 · P1 · El inventario, que es el corazón del acto

Universo declarado: las **16 filas** de `forense/replay-evidencia.tsv` (de 151) que citan
ENIGH, leídas contra el `spec.yaml` y el `resultados.json` de cada corrida.

**Pasa la regla de entrada (R sellado en ≥3 olas, universo idéntico): uno.**
Proporción de hogares con `remesas>0`; universo `concentradohogar` completo sin filtro;
ponderador `factor` de hogar; escala proporción.

| ola | P | IC95 | n | CALC |
|---|---|---|---|---|
| 2014 | 0.040784 | [0.036629, 0.045136] | 19 479 | `CALC-B-MARCO-ENIGH-0001` |
| 2016 | 0.047459 | [0.045098, 0.049759] | 70 311 | `-MARCO-` **y** `CALC-B-0001` |
| 2018 | 0.047285 | [0.045102, 0.049450] | 74 647 | `CALC-B-0001` |
| 2020 | 0.043775 | [0.041895, 0.045773] | 89 006 | `CALC-B-0001` |
| 2022 | 0.045694 | [0.043773, 0.047770] | 90 102 | `CALC-B-0001` **y** `CALC-ENIGH-0001` |

Los dos solapes coinciden (2016 dígito a dígito; 2022 con delta `0.0` exacto y
`REPLICA-RESULTADO`) — **validación de la serie que no costó una corrida nueva**.

**No pasan: tres**, todos sellados solo en 2022 — perfil estructural (unidad **persona**,
`poblacion.factor`), intensidad de remesas (monto, pesos corrientes de 2022 sin deflactor
declarado) y contexto de remesas (`est_socio` × `tam_loc`). Para cada uno el diseño nombra
el acto de caja que lo haría entrar: **correr el medidor ya sellado sobre olas ya abiertas**,
que no gasta reserva ni decisión de mesa.

**2014 sale de la ventana** por corte de serie (`...ENIGH-2014-NCV`; n de 19 479 a 70 311):
**VENCIDO EN ALCANCE (A.10)**, ni borrado ni refutado. Ventana del duelo: **2016–2022**,
cuatro puntos — suficiente para la regla de entrada, y el diseño dice qué **no** se puede
concluir con cuatro.

## 4 · El duelo es solo nacional, y eso es el entregable

ENIGH **no tiene ningún cruce con historia abierta**. El diseño declara el nivel cruce
**NO-CONSTRUIBLE** en vez de simularlo, que por la regla de salida de θ deja la fila **no
ocupada** — «nadie corrió el mecanismo», no una derrota de la interacción. El encargo §6
autorizó explícitamente esta clase de entregable, y el sucesor barato está nombrado en el
diseño §3. Ver `forense/hallazgos.md`, segunda entrada de este acto.

## 5 · Qué se escribió, y por qué el diseño NO lleva sidecar

Perímetro §9 respetado: fila de firma, filas de decisión, fila de cola (por su **fuente** y
regenerando la vista), el diseño en `forense/prereg-caja/`, semilla, nota, cascada. **Cero
escrituras en `milpa/`, en ningún CALC y en ninguna celda-D.**

El diseño **no lleva `.sha256`** a propósito: un hash en `prereg-caja/` se lee como
congelado, y §7(c) del encargo veda declarar algo congelado. Precedente en el mismo
directorio: `ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md`, propuesta sin sidecar. El documento
lo dice en su primera línea: **PROPUESTA, NO CONGELADA.**

## 6 · Auditoría (el acto produce un artefacto que afirma sobre México)

**Contadores movidos: cero**, dicho en una línea al inicio, como exige v2.4. El módulo
completo vive en §8 del diseño, donde afirma. Lo esencial: la incidencia de remesas es
**estructura económica transnacional antes que conducta** —depende del mercado laboral
estadounidense, del tipo de cambio, del costo de envío y de la política migratoria de otro
país, no de una disposición del hogar—, y el diseño **prohíbe por escrito** leer el
resultado del duelo como hallazgo sobre solidaridad familiar o reciprocidad. Se declara
además que ENIGH sub-capta ingreso alto y remesas informales; que la unidad es hogar y no se
cruza contra ENIF ni ENVIPE sin enlace; y que la serie histórica **no es ciega**
(contaminación declarada de `CALC-B-0001`, ADR-46) — lo ciego es 2024, que es precisamente
lo que este acto protege.

## 7 · Anti-PR#77

**No aplica:** este acto no descargó nada (la red salió denegada). `data/raw` sigue ausente
y ningún payload se creó en el worktree.
