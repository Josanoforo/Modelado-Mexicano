# ENIF 2024 · tenencia de ahorro formal∪informal — pre-registro congelado de `CALC-TIENE-AHORROS-0001`

### `prereg-caja-ENIF-TIENE-AHORROS` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENIF-TIENE-AHORROS-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENIF-TIENE-AHORROS`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro, en el esquema `D-15`, de una medición **ya corrida y sellada**: `tiene_ahorros_enif2024` / `no_tiene_ahorros_enif2024` (`dinero.ahorro.tiene_ahorros`, `milpa/tramite.yaml:641-642`), medida por `ACTO MAESTRA34-L5` P4 (`tools/medidor_ahorro_enif24.py`) y sellada por `ACTO MAESTRA35-N1` (firma c1, mesa, 2/sep/2026). Releva `CORR-0009` — `RES-0031` y `RES-0032`. |
> | **QUÉ NO ES** | No es `CALC-ENIF-0001` (releva `RES-0046`/`RES-0048`/`RES-0057..0060`, otra regla del mismo instrumento) ni `CALC-ENIF-0002` (releva `RES-0065`, ver §0.3 — **ya sellado, no re-tocado aquí**). No mide la serie 2005-06 (`tiene_ahorros`/`no_tiene_ahorros` histórico, `p=0.174804`): esa cifra se conserva íntegra como historia (firma c1) y **no forma serie** con esta (acervo vs. flujo, universos distintos — reserva heredada, no reabierta). No re-ejecuta el medidor. No toca `milpa/tramite.yaml`. |
> | **VERIFICAS ASÍ** | CAJA confirma que el payload resuelto por `enif_2024_enif_2024_bd_csv` (`sha256=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`) coincide, y que `tiene_ahorros_enif2024 + no_tiene_ahorros_enif2024 = 1.0` (`0.642080 + 0.357920 = 1.000000`, exacto). |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, entorno **NUBE**, sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

**Regla consumidora:** `dinero.ahorro.tiene_ahorros` (`milpa/tramite.yaml:631`), `situacion: SELLADA`, `tier: FUERTE`.

---

## 0 · A.8 — qué ya existe

### 0.1 · `ya_medido.py`, salida cruda

```
$ python3 tools/ya_medido.py dinero.ahorro.tiene_ahorros
  resuelto por canon: (id de motor, disparadores_estado=PENDIENTE-DE-MESA en canon §2.1-2.2)
  -- milpa/tramite.yaml -- :631-684  situacion=SELLADA tier=FUERTE
     tiene_ahorros_enif2024 p=0.642080  no_tiene_ahorros_enif2024 p=0.357920
     [TASA-EJECUTADA vía enmienda_enif2024, sellada ACTO MAESTRA35-N1]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- :803-853 (id dinero.ahorro.tiene_ahorros_enif2024)
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin CALC propio para ESTA pareja: 0 filas)
  -- forense/notas/*-L*-*.md -- 2026-09-02-MAESTRA34-L5-P4-spec.md
  ========================================
  MEDIDA-EN: tramite.yaml, tramite-ola5-propuesta-v0.yaml (sin CALC que la releve)
```

Mismo hueco de `CORR-0017`/`CORR-0007`: medida, sellada, cargada — sin
contrato `D-15` en el registro GEN2.

### 0.2 · Corrección de premisa del mapa-19

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (fila `CORR-0009`) cita
`RES-0031`/`RES-0032` como *"excluidos por nombre en la spec"* de
`CALC-ENIF-0001`. Verificado: **cierto que `CALC-ENIF-0001` no los cubre**
(su spec releva otra apertura de `dinero.ahorro.*`), pero **falso** que
estén sin medir en absoluto — tienen valor legacy sellado desde el
2/sep/2026 (arriba). El hueco real es capa 2, no ausencia de medición.

### 0.3 · `RES-0065` — corrección más fuerte: ya está sellado con `D-15` completo

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv` dice de `RES-0065`: *"cero
apariciones en cualquier spec o CALC"*. **Falso, verificado con comando:**

```
$ grep -rn "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P" data/corrida0/CALC-ENIF-0002/
data/corrida0/CALC-ENIF-0002/resultados.json:40:  "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P": 0.632782,
data/corrida0/CALC-ENIF-0002/spec.yaml:105:  - {id: RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P, ...}
$ ls data/corrida0/CALC-ENIF-0002/
ejecucion.json  medidor.py  resultados.json  sello.json  sello.sha256  spec.md  spec.yaml
```

`CALC-ENIF-0002` está **completo y sellado** (`sello.json`/`sello.sha256`
presentes — `ACTO GEN2-ENIF-POBLACION-Y-ADOPCION`, `ADR-459`), y
`milpa/tramite.yaml:1333` ya trae `corrida0_resultado_id:
RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P, corrida0_generacion: GEN2` en la
regla `dinero.ahorro.horizonte_no_trabajadores` que `RES-0065` cita. **No
hay nada que congelar aquí**: `RES-0065` ya tiene las dos capas de `D-15`
desde antes de este acto. El mapa estaba desactualizado
(`data/corrida0/demanda-resultados.tsv` es un snapshot legacy que no se
regenera al nacer un `CALC` nuevo — exactamente la advertencia que el
propio mapa trae: "no se re-genera y envejece", aplicada aquí a su fuente,
no solo a sí mismo). Este acto **no** escribe ningún `CALC` para
`RES-0065`: escribirlo sería un duplicado (`A.8`).

---

## 1 · Payload y medición original

| campo | valor |
|---|---|
| payload | `enif_2024_enif_2024_bd_csv`, `sha256=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` |
| script original | `tools/medidor_ahorro_enif24.py` (`ACTO MAESTRA34-L5` P4, spec `forense/notas/2026-09-02-MAESTRA34-L5-P4-spec.md`) |
| unidad | PERSONA elegida, 18 años y más |
| universo | `TMODULO.csv`, `EDAD_V` 18-98, las 13 502 personas sin pérdida |
| desenlace | `tiene_ahorros = 1` ⟺ alguna de `P5_1_1..P5_1_6` (informal) o `P5_6_1..P5_6_9` (formal) vale `'1'` — blanco por secuencia cuenta como no-ahorro por esa vía |
| ponderador | `FAC_PER` |
| diseño | `EST_DIS` × `UPM_DIS`, bootstrap de conglomerado, `n_boot=10000`, `seed=42` |
| numerador (con ahorro) | 8 699 |
| estratos | 190 |
| UPM | 2 164 |
| población expandida | 94 221 441 adultos |
| punto | `tiene_ahorros_enif2024 = 0.642080`, IC95 `[0.630602, 0.653440]` |
| complemento | `no_tiene_ahorros_enif2024 = 0.357920` — contado directamente |

---

## 2 · Reservas heredadas, no re-abiertas

`milpa/tramite.yaml:669-682`: la cifra 2005-06 (`p=0.174804`) y esta
(`p=0.642080`) **no forman serie** — acervo vs. flujo, y universo distinto
por razón 3.67× (panel retenido ENNViH n=6028 vs. muestra nacional 18+
expandida a 94M). Decisión escrita **antes** de ver el número (`spec §1.6`
citada). No se re-abre.

---

## 3 · `resultados` que releva esta spec

`RES-0031` (`dinero.ahorro.tiene_ahorros:tiene_ahorros_enif2024`),
`RES-0032` (`:no_tiene_ahorros_enif2024`). `RES-0065` **ya** relevado por
`CALC-ENIF-0002` (§0.3, no tocado). `CORR-0009` queda, tras este acto y la
corrección de §0.3, con **8 de 9** `RESULT` relevados (6 de
`CALC-ENIF-0001` + 2 de esta pieza; residuo declarado abajo).

## 4 · Lo que queda sin relevar — declaración A.15

| `RES` | por qué sigue sin `CALC` propio | dónde está |
|---|---|---|
| ninguno | — | `CORR-0009` queda **agotado**: los 9 `RESULT` tienen capa 1+2 tras este acto (6 previos + 2 de esta pieza + 1 ya sellado que el mapa citaba mal) |

## 5 · Qué NO hace este acto

No re-corre `tools/medidor_ahorro_enif24.py`. No toca `milpa/tramite.yaml`.
No escribe un `CALC` para `RES-0065` (ya existe, sellado, §0.3). No re-abre
la reserva de no-comparabilidad con 2005-06.

**El primer resultado que produjo este procedimiento —en `ACTO
MAESTRA34-L5`, no aquí— es el que se reporta.**
