# EXPEDIENTE C2 · familias 2027 · v1.0

Acto `GEN2-ASTRA-CONTINUIDAD-C2-1` · 28/sep/2026 · NUBE · base `origin/main` e584ee5f · 0-bis `ba6ccd23` · ADR-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01.

**Contadores movidos: cero mediciones.** No abre olas, no adopta, no toca emisiones ni specs (`git diff --stat origin/main -- forense/prereg-caja forense/prereg-duelo-v2 data/corrida0` = vacío, EJECUTADO).

## 1 · Tablero por familia × ola (P1)

Fuente única: `familias-2027-estado-v1_0.tsv` (15 columnas: rutas, sha256, commits, emisiones, potencia, OTS, gate, firma y estado). Todas las filas se leyeron del objeto (spec, yaml, sello, hoja-firma), no de notas. EJECUTADO: el `sha256sum -c` sobre las 16 rutas de spec y yaml da OK 16/16.

| familia | ola | spec humana (sha12) | COMMIT-1 | COMMIT-2 | gate faltante | firma que lo abre | estado |
|---|---|---|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | enif_2027 | `b69a0546fc31` | md:a6504860 2026-09-26 (sidecar CASA); yaml:a6504860 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06)+FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14;control ENIF)+ACCESO-AUTORIZADO+DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14; FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01 | BLOQUEADA(FIRMA-DE-MESA control ENIF antes de COMMIT-3) |
| ENIF-HORIZONTE-AHORRO | enif_2027 | `f2e556562ac0` | md:a6504860 2026-09-26 (sidecar CASA); yaml:a6504860 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06)+FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14;control ENIF)+ACCESO-AUTORIZADO+DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14; FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01 | BLOQUEADA(FIRMA-DE-MESA control ENIF antes de COMMIT-3) |
| ENCIG-PAGO-DIGITAL | encig_2027 | `b6a13eb08e7d` | md:0dbe658d 2026-09-26 (sidecar CASA); yaml:0dbe658d 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-dato del residuo)+DATO-2027-AUSENTE | FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01 (FIRMADA: suspender); FP-260926-GEN2-ASTRA6-C2-CIERRE-MATERIAL-1-ad01-01 (FIRMADA B1); abre: enmienda sucesora aún sin firma | SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01) |
| ENCIG-SOLICITUD-MORDIDA | encig_2027 | `4d002205e709` | md:0dbe658d 2026-09-26 (sidecar CASA); yaml:0dbe658d 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14;identidad ENCIG)+FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06)+DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 | BLOQUEADA(FIRMA-DE-MESA identidad técnica ENCIG) |
| ENVIPE-DENUNCIA-U4 | envipe_2027 | `2f0af51c8949` | md:f59b1b90 2026-09-26 (sidecar CASA); yaml:f59b1b90 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15;singleton contribuyente)+FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06)+DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 | BLOQUEADA(FIRMA-DE-MESA unidad de remuestreo; activación condicional) |
| ENVIPE-EVASION-NORMA | envipe_2027 | `72c48af39007` | md:f59b1b90 2026-09-26 (sidecar CASA); yaml:f59b1b90 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15;singleton contribuyente)+FIRMA-DE-MESA(FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06)+DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15; FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 | BLOQUEADA(FIRMA-DE-MESA unidad de remuestreo; activación condicional) |
| ENOE-INFORMALIDAD | 2027T4 | `c8c218562cca` | md:cc1b846d 2026-09-26 (sin sidecar); yaml:cc1b846d 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01)+FIRMA-DE-MESA(FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01)+DATO-2027-AUSENTE | FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01; FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 | NO-LANZAR-TODAVIA |
| ENSU-CAMPECHE-INSEGURIDAD | 2027T4 | `b97f54ee690f` | md:cc1b846d 2026-09-26 (sin sidecar); yaml:cc1b846d 2026-09-26 | NO-HAY (ola 2027 no publicada; ningún COMMIT de R/resultados 2027) | CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA(FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01)+DATO-2027-AUSENTE | FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 | NO-LANZAR-TODAVIA |

Abreviaturas de firma: NC-DECISIONES-B4 = `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06` · NC-DECISIONES-E3 = `…-f2e5-14` · NC-DECISIONES-E4 = `…-f2e5-15` · frontera = `FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01` · ENOE = `FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01` · permisos parciales (C1) = `FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01`.

Hallazgos de P1 (LEÍDO):
- Atestación externa: **no** en las 8 filas. Examiné el repo sin `data/raw` y encontré 0 archivos `*.ots`. El manifiesto de sellos no es un OTS.
- COMMIT-2: **NO-HAY** en las 8 filas, porque todavía no hay dato 2027. COMMIT-1 es del 26/09 en las seis familias Astra y de `cc1b846d` en ENOE y ENSU.
- De los `CALC-FAMILIA-2027-*`, seis son emisiones prospectivas selladas sin R. Los dos `ENIF-ORO-*` son auxiliares históricos sobre olas vistas, y `ORO-0001` no tiene `ejecucion.json` ni sello.
- Las emisiones de ENVIPE dicen «sellada en disco, no registrada» (E.7): va a NC `…ba6c-02`.
- ENIF y ENVIPE no tienen `.yaml` en `prereg-caja`, así que el tablero cita el `spec.yaml` del CALC. Los sidecars `.md.sha256` de v1_3 casan.
- Premisa caída (§3 del encargo): «`71cf-01` ya firmada». En `firmas-pendientes.tsv` sigue **ABIERTA**. Existe su recibo técnico, pero no la firma, así que va en la hoja como pendiente.

## 2 · ENOE-INFORMALIDAD 2027T4 (P2) — NO-LANZAR-TODAVIA

Detalle en `p2-enoe-v1_0.md`. EJECUTADO: `python3 forense/analisis/familias-2027/reproduce_singleton_enoe.py`. Salida:
```
grupo 1: singleton=39 (lista) · estratos=1210
grupo 2: singleton=39 (lista) · estratos=1210
union=39 interseccion=39 suma_sin_deduplicar=78
singleton_union declarado=39 -> COINCIDE
VEREDICTO: REPRODUCE
```
El conteo sale del artefacto `diagnostico/enoe-auditoria.json`, cuyo sha casa, y no del diseño muestral, que no está en esta sesión. La receta para caja está en p2 §1 y va a NC `…ba6c-01`.

Por qué no se lanza: en esos 39 estratos el factor m/(m−1) no está definido, así que el error estándar por sexo queda nulo, y la regla exige que los dos grupos tengan error estándar válido. **No es un veto a toda cifra ENOE**: los pisos sellados siguen en pie.

La propuesta de consulta a INEGI (BORRADOR · NO ENVIADO · no equivale a autorización) está en p2.

## 3 · Frontera y cierre material (P3)

Detalle en `p3-frontera-cierre-v1_0.md`. EJECUTADO:
- `enoe-hashes.sha256` 7/7 OK · `ensu-hashes.sha256` 7/7 OK · `frontera-inventario.json` 32/32 · `paquete-control-hashes.json` 18/18.
- Oros ENOE 2024T4 y ENSU 2025T4: `retador: null`. Tienen rótulo RETROSPECTIVA (descripción y calibración), así que no violan la regla 6.
- Cierre material: ENCIG-PAGO-DIGITAL está SUSPENDIDA/NO-ESTIMABLE; ENIF ×2, ENCIG-MORDIDA y ENVIPE ×2 están CONDICIONAL.
- «Ambos grupos y escenarios completos obligatorios» se sostiene en `potencia/calcula.py:17-50`, pero no está escrito en la spec del paquete.
- Cruces que #1242/#1248 proponen declarar consumidos: hay 8 cruces vistos con archivo y línea en p3. Por E.6 se declara consumido el cruce, no la ola. La firma propuesta `b544-02` enumera olas y va con reparo a la hoja.
- Tensión: ENSU dic/2025 aparece como ola reservada en el incidente de #1242 y como oro abierto en frontera-1. Va a la hoja (`…ba6c-01`).

## 4 · NC y FP de C2 (P4)

Dictamen por objeto en `dictamen-nc-c2-v1_0.tsv`: de 21 NC abiertas, **2 CERRADA**, **6 DECISIÓN** y **13 SIGUE-ABIERTA**. Las dos cerradas se cerraron en `no-corrido.tsv` con su cita:
- `7045-04`: recibo `53853397` en main.
- `996b-01`: `500c0953` vía #1170.

FP de C2 abiertas: 71cf-01, 310e-01, NC-DECISIONES-B4, NC-DECISIONES-E3, NC-DECISIONES-E4, más la FP nueva de este acto. Este acto **no asienta** NC-DECISIONES-B4, NC-DECISIONES-E3 ni NC-DECISIONES-E4: solo las lleva.

## 5 · Hoja para mesa

`hoja-c2-para-mesa-v1_0.md`, con texto de firma listo por renglón. Pregunta nueva: `FP-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01`, con tres partes:
- (a) si MOCIBA y ENSANUT entran al tablero;
- (b) si ENSU dic/2025 está abierta o reservada;
- (c) «consumido» por cruce enumerado.

## 6 · Módulo de auditoría v2.16

- Todas las cifras futuras de este expediente son **PROSPECTIVA** por construcción, porque las emisiones se sellaron antes de R. Los oros son RETROSPECTIVA. Ninguna frase mezcla las dos.
- Unidad por familia: ENIF, persona 18+; ENCIG-PAGO-DIGITAL, **trámite**; ENCIG-MORDIDA, persona; ENVIPE-U4, persona víctima; ENVIPE-EVASIÓN, **delito**; ENOE, persona ocupada; ENSU, persona. No se promedian entre sí.
- Riesgo de lectura simplista: «mordida» o «evasión» leídos como rasgo cultural. Son tasas condicionadas a oferta institucional y a victimización (§3), y la clase media urbana está sobre-representada en los trámites digitales.
- Ninguna afirmación sobre el estado del corpus está escrita a mano: todas se derivan por comando o se citan con archivo.
