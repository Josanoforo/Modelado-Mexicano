# ACTO GEN2-F5-DOC-CONTRATO-V1_1 · redacción del sucesor de transporte, cero llamadas

Fecha: 14 de septiembre de 2026. Entorno: NUBE, Opus.

Base: `22aa835b7572549a8450d5f3a6a8d83be37d14fc` (`origin/main` al arranque,
merge de PR #756). Compuerta verificada: `origin/main` HEAD es exactamente
el merge de PR #756 (`ACTO GEN2-F5-DOCUMENTAL-RUN`, el PARO). Encargo:
`forense/encargos/2026-09-14-GEN2-F5-DOC-CONTRATO-V1_1.md`.

## Entrega única

`forense/prereg-duelo-v2/F5-documental-v1_0/F5-documental-ejecucion-v1_1.md`
— sucesión fechada de v1.0 (v1.0 intacto). Contiene las cinco piezas que el
encargo exige, cada una con su evidencia cruda citada dentro del propio
contrato:

- **(a)** El auxiliar `claude-haiku-4-5` no toca la ruta de respuesta: el
  bloque `usage` de nivel superior de la sonda del PARO reconcilia
  exactamente (los cuatro campos, campo a campo) contra
  `modelUsage["claude-opus-5"]` y en ninguno contra Haiku; la forma de la
  llamada de Haiku (91 703 in / 22 out / 0 caché) es de compactación o
  telemetría interna, no de generación de respuesta. Se declara componente
  auxiliar **permitido**, con una regla de identidad verificable por
  mensaje (reconciliación de `usage` + tope de `outputTokens` para
  cualquier modelo adicional) que sustituye el criterio `modelos(sobre) ==
  {MODELO}` de v1.0.
- **(b)** Tabla línea por línea del comando `comando_mcp` sellado, con
  `--allowedTools mcp__f5docs__weighted_distribution` como la única línea
  nueva (la que cierra el hueco de permiso que produjo `TRANSPORTE-NO-
  VALIDADO` causa 1), y una corrección de atribución: `--tools` opera sobre
  el catálogo **incorporado** según su propio `--help`, no habilita
  herramientas MCP — v1.0 le atribuía ese papel por error.
- **(c)** Verificado en vivo contra el cliente `2.1.270` instalado en esta
  sesión (el mismo que corrió la sonda del PARO): `--max-turns` no aparece
  en `claude -p --help`, y una invocación real con ese flag no produce
  error ni efecto — se ignora en silencio. `num_turns=3` no violó un techo
  de 2 real: no hay techo de turnos en este cliente. Límite nuevo:
  `--max-budget-usd 2.00` (freno técnico real que el cliente sí documenta,
  con margen sobre el `total_cost_usd=1.3545` observado), y la contabilidad
  contra el techo de 96 deja de recortar hacia abajo un `num_turns` real
  que exceda el viejo `MAX_TURNS` (defecto de sub-conteo identificado en
  `cargo_solicitudes()`, línea 399-405 de `tools/f5_documental.py`).
- **(d)** Sonda re-especificada con cinco condiciones (marcador, identidad
  del modelo, ausencia de `permission_denials` para la MCP, costo bajo el
  nuevo freno, cargo real de turnos), evidencia que pega
  (`sonda-transporte-v1_1.json` con tres campos nuevos), costo de 1
  invocación cargada por `CARGO_RESERVA=4` ajustada al cierre. El embudo
  arrastra las 2/96 ya gastadas del ledger de v1.0 sin reiniciar: una
  sonda nueva con 3 turnos reales llevaría el total a 5/96 antes de la
  posición 1.
- **(e)** FP-373, 32 posiciones, techo 96, criterio `≥6/8` (cero
  sustituciones, mejora `≥4/8`) y exclusión FP-374/F6 — copiados sin tocar,
  declarados así explícitamente en el propio contrato.

El contrato cierra con la frase de sello: no reabre `TRIADA-0002`, no
autoriza `FP-374` ni `F6`, no cambia la escala del criterio.

## Lo que este acto NO hace

Ninguna solicitud al proveedor se gastó redactando este contrato (las
invocaciones de `claude -p` usadas para verificar el comportamiento de
`--max-turns` en vivo, en esta sesión, corrieron con `claude-haiku-4-5`
fuera del contrato F5 y fuera de su ledger — no cuentan contra el techo de
96 de FP-373, que sólo cuenta invocaciones bajo `comando_mcp`). El runner
`tools/f5_documental.py` no se editó: el acto sucesor
(`GEN2-F5-DOCUMENTAL-RUN` relanzado apuntando a v1.1) es quien lo ajusta.
La escala del criterio no se re-abrió.

## `--verify` (`NC-0178`) queda fuera de este contrato

El encargo de este acto lista cinco piezas, (a)-(e); ninguna es el paso
`--verify` / `sha256_manifiesto_fuentes` que `NC-0178` señala como reserva
abierta. Aunque la fila `NC-0177` (ver más abajo) anticipaba que "el mismo
sucesor" resolvería ambas, el texto verbatim de este encargo no lo pide —
se declara explícitamente fuera de perímetro en vez de absorberlo por
inercia. `NC-0178` sigue `ABIERTA`, sin tocar.

## `NC-0177` — de `SIN-ASIGNAR` a token

`NC-0177` (la NC sucesora del PARO) registraba sucesor `SIN-ASIGNAR hasta
que mesa lo lance`. Este acto es ese lanzamiento: se anota `NC-0177` con el
acto y el PR que produce v1.1, sin cerrarla — las 32 posiciones siguen
sin correr; eso lo hace el `RUN` relanzado, no este acto de redacción.
