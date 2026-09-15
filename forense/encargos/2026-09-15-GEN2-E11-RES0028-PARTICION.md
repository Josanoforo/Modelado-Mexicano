# E11 · GEN2 · RES-0028: partición/universo y propuesta de uso del derivado-declarado

ENTORNO: NUBE — Opus
RAMA: `claude/adoring-euler-jxeoud`
OBJETO: ficha sucesora de `RES-0028` (`milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon`), exigida por la propia fila de `NC-0085` (`forense/no-corrido.tsv:86`).
PRODUCTO: documento de propuesta para firma de mesa — partición/universo reconstruidos, uso concreto materializado del derivado `1 − RESULT-ENVIPE-DEN-P-C2-U4`, sin adoptar nada.

## Contrato autónomo de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Base `origin/main = ce16af3b71433dc5a27221529297f0b5b597ece6`, árbol limpio, sin adelanto pendiente.

`D11` (`ACTO MESA-CONCILIACION-E01`/#685, `forense/notas/BENCHMARK-D11-COMPLEMENTOS-Y-USO-EN-MOTOR.md`) autorizó **desarrollar** la propuesta de uso de `RES-0028`; no autoriza adoptarla. `NC-0085` sigue `ABIERTA` y su reserva exacta es: *"adopcion requiere firma posterior"*. Este acto entrega la propuesta que mesa firma o rechaza; no toca `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `milpa/src/emisor.py`, ni ningún consumidor del motor. Cero motor, cero milpa.

Si en cualquier fase resulta necesario abrir un byte de microdato ENVIPE que la reconstrucción de abajo no cubra (por ejemplo, para verificar una celda no citada en `F3`), PARA de inmediato y repórtalo como hallazgo — no lo abras. Ese hallazgo re-rutea a CAJA (el único entorno con corpus montado) y es entregable de este acto igual que la propuesta misma.

Perímetro: propuesta, `NC-0085`, registro administrativo (`forense/no-corrido.tsv`, nota de cierre). No colisiona con `FICHAS` ni con `TRAMITE`: ambos solo comparten el append ordinario de no-corrido al cierre, sobre filas distintas.

## Base ya disponible — no se remide nada

La reconstrucción de partición/universo que este acto debe producir **ya existe**, hecha por `ACTO GEN2-MOTOR-USOS-Y-COMPLEMENTOS` (10/sep/2026):

- `forense/notas/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS-cierre.md` §F3 — ficha exacta de `RES-0028`: padre (`RESULT-ENVIPE-DEN-P-C2-U4=0.29431298745731216`), unidad/universo (persona 18+, `BP1_23∈{01..08}`, `FAC_ELE`, `n=13023`), evento padre vs. residual, incluidos/excluidos (`09 Otra` = 2200 delitos, `99 NS/NR` = 111, sobre `U1=20225`/`U3=22536`), fórmula (`q=1−p`, `Cov(p,q)=−Var(p)`), punto (`q=0.7056870125426878`, publicado `0.705687`), IC95 por transformación (`[0.6942008049952509, 0.7169802491746927]`).
- `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` §3.2 y §6.2 — universos `U1..U4` pre-declarados y el veredicto `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U1`: el complemento suma 1 con el primario **solo bajo `U1`**, no bajo el universo completo (`U3`); ahí, la misma codificación da `0.242676`, no `0.267243` (cita ya asentada en la fila de `NC-0085`).
- `forense/notas/BENCHMARK-D11-COMPLEMENTOS-Y-USO-EN-MOTOR.md` — contrato matemático del complemento (§3) y qué debe hacer el motor si algún día se adopta (§4), más la definición literal del encargo E11 en su propio §6.

No reabras microdato para reproducir estas cifras: ya están selladas con `payload_sha256` en `data/corrida0/demanda-resultados.tsv:30` y verificadas por la corrida `CALC-ENVIPE-0001`. El trabajo de este acto es **redactar la ficha sucesora que cite esa base y materialice el uso concreto**, no volver a medir.

## Fase 1 · Ficha sucesora — partición/universo, citando lo ya reconstruido

Redacta `forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION.md` con, como mínimo:

1. Tabla de partición: qué incluye `C2` (`01,02,06,08`), qué incluye el residual (`03,04,05,07`), qué queda fuera de ambos (`09`, `99`, blanco) y su peso exacto en `U3` (`P-OTRA-U3=0.087445`, `P-NSNR-U3=0.004484`), citando §F3 y la spec verbatim en vez de recalcular.
2. El veredicto de exhaustividad reproducido literal: bajo `U1` suman 1 por construcción del recorte, no porque el instrumento sea exhaustivo; bajo `U3` la cifra cambia a `0.242676`. Deja explícito que `0.705687` **no es una cantidad medida independiente**: es `1 −` el primario sobre un denominador que excluye categorías reales.
3. Nombre descriptivo preciso del residual (exigido por `BENCHMARK-D11` §6: *"si no coincide con una categoría literal, proponer el nombre descriptivo preciso"*): no es "otra razón" en el sentido del código `09`; es el resto de las ocho razones sustantivas de `U1` excluyendo `{01,02,06,08}`. Propón el rótulo exacto que el registro usaría si adopta.

## Fase 2 · Uso concreto propuesto — sin adoptar

Materializa, como propuesta y no como cambio ejecutado:

1. La recomendación exacta que `NC-0085` ya registra como pendiente: dar a `RES-0028` su propio `corrida0_resultado_id` en el registro (hoy comparte fila de derivado con el padre en `demanda-resultados.tsv:30`, columna `corrida0_resultado_id=NO-DECLARADO-EN-EL-REGISTRO`). Redacta la entrada propuesta completa (id, fórmula, universo, cita al padre) como iría si mesa firma — no la escribas todavía en el TSV real.
2. El dominio de aplicación del derivado si se adopta: bajo qué contexto (persona 18+, delito no denunciado, `U1`) sería válido usarlo en el motor, y qué NO cubre (no es tasa sobre `U3`, no es "otra razón" en sentido de `09`, no se propaga a otra ola — cita §7.1 de la spec).
3. Una recomendación explícita a mesa: adoptar el residual acotado sobre `U1` con su rótulo propio, o pedir un estimando sucesor sobre `U3` si mesa prefiere "otras razones" sobre la población completa (la disyuntiva que el propio `BENCHMARK-D11` deja abierta en su recomendación final).

No edites `milpa/tramite.yaml` ni ningún consumidor. No emitas un `RESULT` nuevo. No corras `corrida0`.

## Fase 3 · Registro y cierre

1. Actualiza la fila `NC-0085` en `forense/no-corrido.tsv` (columna de siguiente-acción) para enlazar la ficha sucesora recién escrita, en vez de seguir apuntando genéricamente a "E11: reconstruir…" — sustitúyelo por la ruta del documento producido en Fase 1/2, conservando el estado `ABIERTA` (la firma sigue pendiente de mesa).
2. Redacta nota de cierre breve del acto (puede vivir en el mismo documento de Fase 1, sección final) declarando: qué se propuso, qué no se adoptó, y que `NC-0085` permanece abierta hasta firma posterior.
3. Commits, push a `claude/adoring-euler-jxeoud`, PR propio. No fusionar.

Aceptación: ficha sucesora con partición completa y uso concreto propuesto, fila de `NC-0085` enlazada al documento, cero cambios a `milpa/`, cero `RESULT` nuevo, cero apertura de microdato salvo hallazgo declarado y reportado como PARO.

## Prompt de lanzamiento

> Ejecuta el encargo E11 sobre `RES-0028`/`NC-0085`. La reconstrucción de partición/universo ya existe en `forense/notas/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS-cierre.md` §F3 y en la spec `ENVIPE-DENUNCIA-spec-v1_0.md`; no vuelvas a medir. Redacta la ficha sucesora que cite esa base, proponga el uso concreto del derivado (incluyendo la entrada de registro que `RES-0028` tendría con `corrida0_resultado_id` propio, sin escribirla en el TSV real) y una recomendación a mesa. Enlaza la fila de `NC-0085` al documento nuevo, sin cambiar su estado `ABIERTA`. Cero motor, cero milpa, cero microdato nuevo — si hace falta abrir alguno, PARA y repórtalo como hallazgo. Commit, push, PR propio; el merge queda con mesa.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Adopción de `RES-0028` (escribir `corrida0_resultado_id` real en `data/corrida0/demanda-resultados.tsv`, cambiar consumidor en `milpa/tramite.yaml`) | `DECISIÓN-DE-MESA-PENDIENTE` — `D11` autoriza desarrollar la propuesta, no adoptarla; la firma de adopción de `NC-0085` sigue pendiente | `RES-0028` sigue sin `corrida0_resultado_id` propio; el motor sigue citando el alias actual (`denuncia_por_otra_razon`) | Firma de mesa sobre `forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md` §2.3; si adopta, un acto posterior ejecuta §2.1 |
| Estimando sucesor sobre `U3` («otras razones» de la población completa, incluyendo `09` y `99`) | `DECISIÓN-DE-MESA-PENDIENTE` — camino 2 de §2.3 de la ficha sucesora, objeto nuevo fuera del perímetro de este acto | Ninguno mientras mesa no elige entre los dos caminos | Acto nuevo, sólo si mesa prefiere ese camino sobre adoptar el residual acotado |

## CONSUMIDO

`PR #773` (rama `claude/adoring-euler-jxeoud`). Ejecutado íntegro: ficha sucesora (`forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md`), fila `NC-0085` enlazada al documento (estado sin cambio, `ABIERTA`), `ADR-509` (`canon/gobernanza-v1_15.md`, renumerado de `ADR-508` al fusionar `main`: `ACTO GEN2-CAJA-RESIDUAL-1`/`PR #772` fusionó primero), L0 y contadores reconciliados (`canon/estado-programa-v1_13.md`), rótulo `GEN2-E11` censado (`canon/registro-rotulos.tsv`). Cero cambios a `milpa/`, cero `RESULT` nuevo, cero microdato abierto. `python3 tests/check.py --baseline` en VERDE. **NO FUSIONAR** — el merge queda con mesa.
