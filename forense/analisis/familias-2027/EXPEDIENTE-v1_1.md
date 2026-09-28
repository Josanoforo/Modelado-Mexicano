# EXPEDIENTE C2 · familias 2027 · v1.1

Acto `GEN2-ASTRA6-C2-EJECUCION-1` · 28/sep/2026 · CAJA · 0-bis `e897d3df` · `ADR-260928-GEN2-ASTRA6-C2-EJECUCION-1-e897-01`. Sucede a `EXPEDIENTE-v1_0.md` sin editarlo.

**Contadores movidos.**
- Cero cifras para el canon desde las familias: sus emisiones son predicciones selladas, no RESULT adoptables, y `celdas_validadas` queda en 219 → 219.
- Un CALC GEN2 descriptivo nuevo: `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001`, RETROSPECTIVA, `adopta: NO`. Está «sellada en disco, no registrada» hasta que el canal de derivados la publique tras el merge (E.7). Su replay está asentado: REPRODUCE/IDENTICO.

## 1 · Tablero (fuente única: `familias-2027-estado-v1_1.tsv`, 17 columnas)

| familia | ola | estado v1.1 | gate que queda | qué lo movió |
|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE · reserva heredada: ACCESO-AUTORIZADO (`…9c9e-01`, ABIERTA) | B4-(i) = E3-(1): envoltura de control para el COMMIT-3; oferta al lado |
| ENIF-HORIZONTE-AHORRO | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | ídem | ídem |
| ENCIG-PAGO-DIGITAL | encig_2027 | SUSPENDIDA (`…fde0-01`) | gate vigente + enmienda pre-dato sin firma | sin cambio: no se reactiva |
| ENCIG-SOLICITUD-MORDIDA | encig_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | B4-(ii) = E3-(1): identidad reconocida |
| ENVIPE-DENUNCIA-U4 | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | B4-(iii) = E4-(1): singleton = marco completo |
| ENVIPE-EVASION-NORMA | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | ídem |
| ENOE-INFORMALIDAD | 2027T4 | NO-LANZAR-TODAVIA | contrato de inferencia de los 39 singletons + `…310e-01` + `…71cf-01` | sin cambio: contrato no firmado |
| ENSU-CAMPECHE-INSEGURIDAD | 2027T4 | NO-LANZAR-TODAVIA | contrato nuevo (potencia insuficiente, banda de 5 pp) + `…71cf-01` | sin cambio: contrato no firmado |

Ningún gate queda vacío. EJECUTADO: lector csv sobre el TSV, 8 filas y 17 columnas, `all(celdas)`.

A.17: se re-verificaron el 28/sep en `forense/firmas-pendientes.tsv` los bloqueadores heredados. `…9c9e-01`, `…71cf-01` y `…310e-01` siguen ABIERTA; `…fde0-01` sigue FIRMADA (suspender).

## 2 · Qué hizo este acto y qué ya estaba hecho

- **P1, las tres firmas.** Se ejecutaron como enmiendas de forma en `astra6-enif/enmienda-firmas-c2-v1_0 · astra6-{encig,envipe}/enmienda-firmas-c2-{encig,envipe}-v1_0.md` y `.yaml`, sin editar `prereg-*`, `spec.yaml`, emisiones ni sellos. `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06`, `-14` y `-15` pasan a FIRMADA con este PR. Se cierran las NC `96f9-01`, `ad01-01` y `ad01-03`.
- **P2/P3 = YA-HECHO. Premisa caída del encargo, decisión de mesa 28/sep: «YA-HECHO: verificar».** Las cinco familias tenían COMMIT-1 (specs v1_3 con sidecar, 26/09) y emisiones selladas (26/09). Lo que bloqueaban las firmas era el **COMMIT-3**. Verificación del 28/sep:
  - `sello.json` SELLO_COINCIDE en 5 de 5.
  - Guardias y pruebas de mutación: ENIF 32 passed · ENVIPE 23 passed · ENCIG 50 passed (`tests/test_astra6_encig.py`) · cierre material 23 passed.
  - `corrida0 preflight` sobre esos CALC sale BLOQUEADO por `CALC-INMUTABLE-YA-SELLADO`. Es correcto: el preflight es la compuerta *antes* de `run`. Los dos de ENVIPE, además, no siguen el esquema de `corrida0` (se emitieron con `cierre.py`; NC `…ba6c-02` sigue abierta).
- **Potencia.** No cambia: `astra6-enif/potencia.tsv`, `astra6-encig/potencia.json` y `astra6-envipe/potencia.json`, citadas por fila en el TSV.
- **Ninguna ola reservada abierta.** Los únicos bytes de casos que leyó el acto son 16 columnas de la sección 5 (cuentas) de ENIF 2024, `TMODULO.csv` de `enif_2024_enif_2024_bd_csv`. Esa sección ya estaba abierta: `CALC-ENIF-0001` leyó `P5_4_*`, `P5_6_*` y `P5_20`, y la reserva de ola se consumió con el lote de 14 cruces (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01`). La reserva sin decidir de ENIF 2024 es el **módulo 7 (pagos)** (HOJA-FIRMAS-21 R06; NC `…4b11-04`) y no se tocó.

## 3 · Oferta al lado del marginal de ahorro (E4 → ENIF, por mesa)

`CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001` es sucesor 2024 de `DIN-OFERTA-EXCLUSION-ENIF` v1.0, con la regla de clases verbatim. Primer resultado (RETROSPECTIVA · ENIF 2024 · U_B 18+ · NACIONAL · IC95 bootstrap de UPM en estrato, 2 000 réplicas):

| estimando | punto | IC95 |
|---|---|---|
| adultos sin cuenta (SIN-CUENTA-UB) | 0.3446 | [0.3327, 0.3568] |
| entre ellos: razón de OFERTA | 0.1037 | [0.0917, 0.1162] |
| entre ellos: razón de PREFERENCIA | 0.5374 | [0.5171, 0.5570] |
| entre ellos: OTRO/NS | 0.3589 | [0.3389, 0.3787] |
| · de ello, ingreso insuficiente | 0.2082 | [0.1911, 0.2255] |
| · de ello, desconocimiento | 0.0630 | [0.0547, 0.0721] |
| · de ello, desconfianza o mal servicio | 0.0385 | [0.0318, 0.0455] |

Denominadores: 13 502 personas en U_B y 4 346 no usuarias (2 970 nunca tuvieron cuenta, 1 376 son ex usuarias). La cobertura de la razón es 1.0. Hay 7 estratos de UPM única, que quedan fijos y declarados en `METODO-IC`.

**Lectura permitida:** entre los adultos sin cuenta, uno de cada diez da como razón principal una barrera de oferta: distancia, costo, requisitos, saldo mínimo o intereses. **Lectura no permitida:** que más de la mitad «prefiera» no tener cuenta. «No la necesita» y «prefiere tanda» pueden ser adaptación a ingresos bajos o variables. Y la razón se pregunta sólo a quien no tiene cuenta: no descompone a quien la tiene y no ahorró en ella, que también es F = 0 en el marginal de ahorro formal.

## 4 · Módulo de auditoría v2.16

- PROSPECTIVA = las emisiones 2027 del 26/09. RETROSPECTIVA = la oferta 2024 y los oros. Ninguna frase de este expediente las mezcla.
- Unidades: persona (ENIF, ENCIG-MORDIDA, ENVIPE-U4), trámite (ENCIG-PAGO), **delito** (ENVIPE-EVASIÓN). No se promedian.
- Oferta antes que preferencia: el marginal de ahorro formal ya tiene su medida al lado (§3). ENCIG-PAGO-DIGITAL, que sería el otro marginal de mercado (canal), está suspendida, y su medida de oferta queda para su reactivación.
- Riesgo de lectura simplista: «mordida», «evasión», «no denuncia» o «no quiere banco» leídos como rasgos culturales. Todas son tasas condicionadas a la oferta institucional, a la victimización y al ingreso. Las cifras nacionales sobrerrepresentan lo urbano formal en ENCIG (localidades de 100 mil y más) y no describen el orden indígena-comunal.

## 5 · Hoja para mesa

`hoja-c2-para-mesa-v1_1.md`: lo que queda de C2 en lenguaje de decisión.
