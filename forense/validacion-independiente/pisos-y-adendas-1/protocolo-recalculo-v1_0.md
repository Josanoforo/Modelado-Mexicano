# Protocolo de recalculación · P4 de GEN2-PISOS-Y-ADENDAS-1 · v1.0

28/sep/2026. Se commitea **con las tres adendas y antes** de recalcular; los números de la recalculación se commitean **antes** de abrir los `RESULT` sellados (E.2). Rótulo de toda cifra que salga de aquí: **RETROSPECTIVA-MECÁNICA** (ola ya vista, ENDIREH 2021; validación de origen móvil sin selección de variante). Unidad: persona (mujer).

## 1 · Qué se recalcula

Criterio del encargo (P4): «un lector con solo la adenda, el cuestionario y el descriptor debe poder recalcular». Se prueba sobre **las llaves que la validación ciega marcó `NO-RECALCULABLE-DESDE-SPEC` por la falta que cada adenda corrige** (`forense/validacion-independiente/catalogo-1-ejecucion-lote1/reconstrucciones/<paquete>/<paquete>--reconstruccion.tsv`, columna `motivo`), identificadas por (desenlace, eje, categoría) desde `estimandos.tsv` del paquete ciego:

| CALC sellado | adenda | llaves (32) |
|---|---|---|
| `CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001` | `forense/prereg-caja/ENDIREH-PISOS-2021-DISCRIMINACION-spec-v2_0.md` | 23: `#5 #6 #7 #8` (prueba_ingreso × escolaridad ninguno/basica/media_superior/superior) · `#56 #57 #58` (prueba_continuidad × basica/media_superior/superior) · `#105 #106 #107 #108` (prueba_alguna × las cuatro) · `#156 #157 #158` (despido_embarazo × basica/media_superior/superior) · `#206 #207 #208` (no_renovacion_embarazo × ídem) · `#256 #257 #258` (reduccion_embarazo × ídem) · `#306 #307 #308` (perjuicio_embarazo_alguno × ídem) |
| `CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001` | `forense/prereg-caja/ENDIREH-PISOS-2021-NOFISICA-BC-spec-v2_0.md` | 8: `#495 #496 #497 #498` (ayuda_bc × escolaridad las cuatro) · `#544 #545 #546 #547` (denuncia_bc × las cuatro) |
| `CALC-ENDIREH-PISOS-2021-AYUDA-0001` | `forense/prereg-caja/ENDIREH-PISOS-2021-AYUDA-spec-v2_0.md` | 1: `#115` (razon_14 × nacional) |

## 2 · Quién y con qué

Una sesión de recalculación **aparte del hilo que leyó los medidores**: un subagente de este acto, con contexto nuevo, al que se le entregan **sólo** la adenda, el FD y el cuestionario (PDF del corpus, por id del manifiesto) y el ZIP de microdato `endireh2021_bd_csv_zip`. Tiene prohibido leer `data/corrida0/CALC-ENDIREH-*` (spec, medidor, resultados), la spec v1, `forense/validacion-independiente/catalogo-1*` y cualquier nota que cite cifras de ENDIREH 2021. Escribe su propio código. El hilo principal sí leyó los medidores para escribir las adendas (permitido por el encargo) y lo declara; por eso no es él quien recalcula. Salida por CALC en `forense/validacion-independiente/pisos-y-adendas-1/<calc>/`: `recalculo.py` (código propio), `recalculo.tsv` (`llave, desenlace, eje, categoria, estado, n, upm, punto, ic95_inf, ic95_sup, se`) y `ambiguedades.md` (dónde la adenda no bastó y qué decidió, si algo).

## 3 · Tolerancia y dictamen (fijados aquí, antes de recalcular)

Por llave, contra la celda de mismo índice del `RESULT` sellado:
- **(a) estado** (`PUBLICABLE`/`SUPRIMIDA`) y **n** idénticos;
- **(b) punto**: `|Δ| ≤ 1.0e-10` — la tolerancia `flotante abs 1.0e-10` que el `spec.yaml` sellado de cada CALC ya declara (el punto es determinista);
- **(c) IC**: extremos a `≤ 1.0 pp` y razón de semianchos en `[0.80, 1.25]` — la tolerancia de IC de `forense/notas/2026-09-21-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-cierre.md:32`, porque una reimplementación del bootstrap puede diferir en orden de sorteo sin que la spec sea insuficiente. Se reporta aparte, sin adjudicar, si el IC coincide además a `1.0e-10`.

Dictamen por adenda, vocabulario cerrado: **PASA** si todas sus llaves cumplen (a), (b) y (c); **NO-PASA** si alguna falla, con la llave y el criterio. `NO-PASA` es un hallazgo sobre la adenda (la spec humana sigue sin bastar), no sobre el `RESULT` sellado, que no se toca en ningún caso. Si la recalculación no puede correr (entorno), el dictamen es `NO-EVALUADA`, no `NO-PASA`.

## 4 · Orden de commits

(1) adendas + sidecars + este protocolo → (2) `recalculo.*` con los números → (3) apertura de los tres `resultados.json` sellados, comparación por llave (`comparacion.tsv`) y dictamen. El diff de (2) a (3) es el sello del orden.
