# Astra 3 / U3 — cotejo de universo y preparación

## EJECUTADO / LEÍDO

- Worktree `/home/pc0/mm-astra3-enif-formalidad-error-1`, rama
  `codex/astra3-enif-formalidad-error-1`, base `638c6f2fd434f8367d324989790e840eaeefc10c`
  de `origin/main`; `git fetch origin` ejecutado al abrir.
- Leídos íntegros `input-verbatim.md` y la misión conservada en
  `mision-verbatim.md.gz` (`gzip -dc` reproduce los bytes exactos; SHA256 de fuente
  `0402e96a5a9680557fcc9d80132c2b32bf589f24d696add350f99a036d257f7d`
  y `c31917eb549d20b98f15780bc7171cd1f3f2dccca9c10e5ce47e64337d4a7bdc`).
- Metadato 2021: las seis identidades son tres desenlaces por dos categorías
  de seguridad social, unidad `PERSONA ELEGIDA 18+`; el spec 2021 dice
  explícitamente «sin filtro de edad». El spec del árbitro 2024 también
  declara persona 18+ y lista P/LO/HI para cuatro de las seis identidades.
  Búsqueda por esquemas no encontró RESULT GEN2 sellado de
  `horizonte_corto × formalidad` en 2024.
- La mesa eligió **B: mantener persona 18–70**. Eso exige nuevos resultados
  2021 y 2024 para los seis pares. Ningún promedio de 18+ puede recortarse
  después a 18–70. El CALC de crédito `...ENIF2021-RECORTE1870-0001` usa
  desenlaces de crédito distintos.
- NC-0414 y NC-0431 permanecen ABIERTAS en la base. El error 18–70 no cierra
  por sí mismo el error pendiente de las seis celdas originales 18+.
- Preparados un medidor de enlace por identidad y hash, tabla histórica de
  seis identidades y fixture sintético. `python3 -m unittest
  tests.test_astra3_formalidad_error -v`: 2 pruebas OK. No se han abierto
  valores de resultados de ninguna ola.

## REPORTADO

No hay cifras, diferencias, IC ni clases de persistencia reales. No se creó
CALC sellado, no se hizo freeze, no se cerró NC ni se solicitó adopción.

## NO-CORRIDO / RESERVAS

Nuevos pisos ENIF2021 y R ENIF2024 de persona 18–70, freeze, CAJA, corrida,
verify, replay y recibo: pendientes de autorización expresa del perímetro
ampliado. La misión original nombra como insumos solo el piso sellado y
ENIF2024; el documento de error advierte que B requiere nuevos insumos y
encargo ampliado. La tabla de seis identidades 18+ es referencia, no entrada
de cálculo bajo B.

## CONSUMIDO

PR borrador #1040 (`codex/astra3-enif-formalidad-error-1`). La mesa consumirá
este diagnóstico para decidir un encargo ampliado y, separadamente, el cierre
de las deudas originales.
