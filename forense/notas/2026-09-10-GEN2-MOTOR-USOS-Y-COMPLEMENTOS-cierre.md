# ACTO GEN2-MOTOR-USOS-Y-COMPLEMENTOS · cierre técnico

Fecha real: 10 de septiembre de 2026. Base de arranque: `origin/main`
`44134745ce7f19af18a87b153a99de3d506063b0`. Autoridad: encargo archivado
en `forense/encargos/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS.md` y decisiones
D03/D06/D07/D08/D09/D10/D11 asentadas por mesa en
`ACTO MESA-CONCILIACION-E01`/#685.

## P0 · mapa de uso y rutas exactas

| objeto | activador → dominio | evento / parámetro | consumidor real | cambio |
|---|---|---|---|---|
| RES-0005/0006, ENCUCI | `servidor_tiene_discrecion` → persona 15+ con contacto en 12 meses y respuesta válida AP5_17/AP5_18 | solicitud `S=AP5_17`, entrega `E=AP5_18`, unión `S∪E`, complemento `S=0∧E=0` | `milpa/tramite.yaml:tramite.mordida.discrecional`; `milpa/src/emisor.py:emitir_transicion` | separa los tres eventos y rechaza aplicar las tasas sin contacto |
| tasas ENCIG por canal | trámite de alguien que ya declaró corrupción → `P8_4` observado y canal `P7_3` | solicitud observada, no pago ni tasa general | `milpa/tramite.yaml:tramite.mordida.con_registro`; `milpa/src/emisor.py:emitir_binaria_en_contexto` | sólo r2 sin deduplicar queda utilizable, dentro del grupo observado; las dos discrepantes quedan `NO-ADOPTAR-NC-0107` |
| proxy fintech | persona con tenencia fintech → canal del último crédito/cuenta | distribución descriptiva del último producto, no canal del producto fintech | `milpa/procedencia.yaml:asignados_probabilidad:dinero.credito.scoring_alternativo.proxy_canal_enif2024` | se conserva como proxy descriptivo que no calibra aprobación/rechazo |
| RES-0059/0060, ENIF | persona sin cuenta, partida por conocimiento IPAB | código P5_20=03: “desconfianza o mal servicio” | `milpa/tramite.yaml:dinero.ahorro.seguro_deposito_enif2024`; emisor y alias legacy | corrige rótulo; cálculo/RESULT y adopción del dominio siguen coordinados con lote 03 |
| RES-0035/0036, ENIGH | hogar ENIGH 2022 | `remesas>0` y su complemento | `milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado`; `tools/corrida0.py:_instrumento` | procedencia por conducta = ENIGH2022; las otras cinco olas siguen como serie, nunca promedio |
| RES-0028, ENVIPE | víctima 18+, delito no denunciado, `BP1_23∈01..08`, colapso a persona | resto `{03,04,05,07}` de ese recorte, no código literal 09 “Otra” | `milpa/tramite.yaml:civico.denuncia.miedo_desconfianza`; emisor | complemento dependiente del padre; propuesta de uso, adopción final pendiente NC-0085 |

Tasas del perímetro sin consumidor nuevo: las transiciones ENCUCI de solicitud y
entrega ya tenían RESULT sellado, pero sólo la unión tenía salida legacy. Ahora
`emitir_transicion` las expone sin agregarlas al inventario de demandas legacy.
Consumidor sin respaldo: la tasa general ENCIG no es identificable en P8_4; se
inscribe como demanda `NC-0153` y se remite al lote 06. No se registra como
adquisición.

## F1 · decisiones inequívocas propagadas

- ENIF usa el rótulo canónico `desconfianza_o_mal_servicio_*`; los dos nombres
  antiguos son alias del mismo objeto y no crean resultados nuevos.
- ENCIG r2 exige `p8_4_observado=true` y el canal correspondiente. Las variantes
  deduplicadas discrepantes siguen en el archivo por historia, pero el campo
  `uso_motor` prohíbe adoptarlas. No se buscó un desempate que reprodujera la
  cifra vieja.
- El proxy fintech se etiqueta literalmente como canal del último producto
  entre tenedores de fintech. Las cifras 2024 son descriptivas y no modifican
  `dinero.credito.scoring_alternativo`.
- RES-0035 y su complemento quedan atribuidos a ENIGH 2022 por conducta. La
  derivación de `demanda` baja las dos ambigüedades correspondientes; 2012–2020
  permanecen como observaciones separadas de `serie_olas`.

## F2 · ENCUCI, resultado y comparación del flujo

El punto de activación es un contacto con funcionario; por ello el motor usa
probabilidades entre contactos con respuesta válida, no carga poblacional. Si
otro flujo requiere carga, la salida ya sellada es
`RESULT-ENCUCI-A-P-CUALQUIERA-POBLACION=0.07995806060682063` y debe modelar la
exposición explícitamente.

| estado | antes | después |
|---|---:|---:|
| salida legacy rotulada “paga_mordida_encuci2020” | 0.125822, descrita falsamente como solicitud | alias de la unión `S∪E=0.126006` |
| solicitud `P(S|contacto,válida)` | sin salida de motor | 0.106319 |
| entrega `P(E|contacto,válida)` | sin salida de motor | 0.073640 |
| ninguna `P(S=0,E=0|contacto,válida)` | 0.874178 como salida independiente | `1−0.126006=0.873994`, mismo padre |

La unión no se obtiene multiplicando marginales. La lógica conserva `(0,0)`,
`(1,0)`, `(0,1)` y `(1,1)`. Un 1 resuelve la unión aunque el otro componente
falte; `(0,NA)`, `(NA,0)` y `(NA,NA)` quedan indeterminados. Los 24 contactos
con algún 9/blanco no se convierten en No: `N_contacto=13435`, `U_A=13411`.
Esto resuelve NC-0137 sin medir la variante post-hoc que codificaba 9 como 0.

## F3 · ficha exacta de RES-0028

| campo | definición |
|---|---|
| padre | `RESULT-ENVIPE-DEN-P-C2-U4=0.29431298745731216` |
| unidad / universo | persona de 18+ con al menos un delito no denunciado de `BPCOD 05..15`, `BP1_23∈{01..08}`, `FAC_ELE` válido; `n=13023` |
| evento padre | algún delito de U1 con razón principal `{01,02,06,08}` |
| evento residual | ningún delito de U1 en el padre; resto `{03,04,05,07}` del recorte. No es la categoría `09 Otra` |
| incluidos / excluidos | incluye en el denominador `01..08`; excluye `09 Otra` (2,200 delitos), `99 NS/NR` (111) y blancos; U1 tiene 20,225 delitos, U3 22,536 |
| fórmula | `q=1−p`; en cada réplica `q[b]=1−p[b]`; `Cov(p,q)=−Var(p)` |
| punto materializado | `q=0.7056870125426878`, publicado a seis decimales como `0.705687` |
| incertidumbre | IC95 del padre `[0.2830197508253073, 0.3057991950047491]`; por transformación, IC95(q) `[0.6942008049952509, 0.7169802491746927]` |
| consumidor | `civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon`, sólo bajo el dominio U1/U4 declarado |
| reserva | `NC-0085` sigue ABIERTA: mesa aún debe firmar si adopta este residual acotado o pide un estimando sucesor sobre U3 |

La categoría literal `09 Otra` pesa `0.08744473726442899` en U3 y NS/NR
`0.004484044074885197`; por eso “otra razón” no puede significar a la vez el
residual de U1 y el código 09. Dos consumidores/alias del residual comparten el
mismo padre y nunca cuentan como dos confirmaciones.

## F4 · pruebas, cierres y residuales

Se añadieron pruebas dirigidas en `tests/test_motor_usos_complementos.py` y se
preservó la regresión de calibración por conducta de `tools/emite_m.py`.
`tools/corrida0.py demanda` re-deriva las vistas y reduce de 11 a 9 las
ambigüedades, exactamente las dos ENIGH del perímetro.

Cerradas por consumidor corregido: NC-0105, NC-0127 y NC-0137/0138/0139.
Permanecen abiertas: NC-0107 (variantes deduplicadas discrepantes), NC-0111 y
NC-0153 (tasa general ENCIG), NC-0121 (serie fintech 2018/2021), NC-0122
(canal del producto fintech exacto) y NC-0085 (firma de RES-0028).

Rutas sustantivas editadas: `milpa/tramite.yaml`, `milpa/procedencia.yaml`,
`milpa/src/emisor.py`, `tools/corrida0.py`, las dos vistas derivadas
`data/corrida0/demanda-{resultados,corridas}.tsv` y la prueba dirigida. Rutas
administrativas: encargo, esta nota y `forense/no-corrido.tsv`. No se editaron
snapshots M/R de la tríada ni sellos de CALC.
