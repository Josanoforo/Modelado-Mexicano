# Cierre — demanda conciliada y ejecución NC-0165

Acto: `GEN2-DEMANDA-CONTRATOS-EJECUCION-NC0165`

Corte: 11 de septiembre de 2026

Entorno: CAJA Ubuntu/WSL2, corpus compartido; cero descargas, llamadas a
modelos, nuevas mediciones, adopciones o ejecuciones F5.

## Resultado para consumidores

La proyección conserva los 207 usos activos y ahora da a cada uno identidad,
propósito, `contrato_id`, estado, primer faltante, ejecutor y siguiente acción.
La oferta se enlaza por evidencia explícita y compatibilidad de fuente, ola,
estimando, unidad, población, transformación y propósito; se retiró la
heurística que buscaba una subcadena `RES-xxxx` en el nombre de un `RESULT`.

| consumidor/grupo | antes | después | evidencia | uso | pendiente/ejecutor |
|---|---|---|---|---|---|
| `RES-0028` | preparación genérica, sin oferta | propuesta `1 − RESULT-ENVIPE-DEN-P-C2-U4` enlazada a `NC-0085` | `RESULT-ENVIPE-DEN-P-C2-U4`, D11 y prueba del complemento | no emite; propuesta U4 | adopción / mesa |
| `RES-0039..0042` | preparación genérica | elección concreta de spec estrecha vs. definición nueva | propuesta `ENVIPE-DENUNCIA-SEGURO-v1_0` y `NC-0088` | no calculado | decisión científica / mesa |
| `RES-0063/0064` | preparación genérica | medición y adopción previas reconocidas | S7-L17, nota ENSANUT y regla vigente | la regla histórica contiene 0.777762/0.222238; consulta GEN2 no emite | alta `RESULT`/corrida0 / motor-gen2-registro |
| 14 `R` | confundidos con parámetros preadopción | árbitros empíricos disponibles por identidad exacta | `codificacion-R-v1_2.tsv` y `RESULT-R-*-PUNTO` | evaluación, nunca M | DIN conserva FP-371 sólo para EE/IC |
| 56 `L/M/AGREGADO` | preadopción genérica | salidas TRIADA/M disponibles para evaluación | `universo-triada-v1_4.tsv` y RESULT exactos | evaluación, no adopción | ninguno automático |
| tres horizontes | resultado visible sin destino suficientemente claro | guardia conservada | `NC-0126` y consulta real | `NO_COVERAGE`, sin fallback | fuente compatible / servicio GEN2-38 |
| `RES-0009/0011` | coincidencia textual parecía oferta de decisión | resultado discrepante queda no adoptable; D07/D08 no se vuelven a pedir | CALC-ENCIG-0001, `NC-0107`, `NC-0153` | no emite | acceso nacional evento×canal / titular y receptor |

## Recorrido real

Se ejerció la interfaz `tools/consulta_gen2.py` con cuatro identidades:

- `tramite.gobierno_digital.util_sin_coercion:adopta_encig2025_luz` →
  `EMITE`, `RESULT-ENCIG-MOR-C-P-ADOPTA`;
- `civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon` →
  `NO_COVERAGE`, porque la adopción de la propuesta no fue firmada;
- `dinero.ahorro.horizonte_corto:horizonte_corto` → `NO_COVERAGE`, con la
  guardia `NC-0126` y sin valor/fallback;
- `salud.vacunacion.disponible_ensanut2024:razon_no_vacunacion_logistica` →
  `NO_COVERAGE`: la medición está cargada en la regla, pero no declara RESULT.

Este último recorrido corrigió el rótulo intermedio: ENSANUT no vuelve a
`PREPARACION` ni requiere otra decisión científica, pero tampoco se presenta
como emisión GEN2 actual. Su único faltante es el registro de la medición ya
adoptada.

La selección de investigación al corte queda vacía por causas estructuradas:
las búsquedas públicas tienen revisión futura o están delegadas, y los accesos
requieren al titular. No se reabrió una espera ni se simuló una búsqueda.

## Conteo descriptivo, no suficiencia

La vista explica 207/207 elementos: 9 cubiertos, 70 salidas de evaluación
disponibles, 2 mediciones adoptadas sin cobertura contractual GEN2, 6 en
acceso, 1 en adopción, 3 bloqueados por datos/uso, 49 en decisión y 67 en
preparación. Entre las 51 NC que permanecen abiertas, 20 son técnicas o de
acceso y no se cuentan como contratos científicos incompletos.

`NC-0165` cierra porque su universo inicial ya tiene destino individual y las
obligaciones continúan bajo contratos/acciones/ejecutores específicos. El
cierre no afirma que el motor esté totalmente medido. `NC-0085`, `NC-0088`,
`NC-0107`, `NC-0126`, `NC-0153` y `FP-371` conservan su estado real.

## Verificación

- `python3 tests/test_adq_descubrimiento.py` → 9 grupos, 0 fallos;
- `python3 tests/test_motor_usos_complementos.py` → 16 pruebas, OK;
- regeneración de `data/adq-demanda-activa-v1_0.json` → 207/207 con contrato,
  identidad, estado, acción y ejecutor;
- `git diff --check` → limpio.

Contador científico: cero. La pieza concilia y consume evidencia existente; no
cuenta una medición compartida varias veces ni habilita una adopción nueva.
