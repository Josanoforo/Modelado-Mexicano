# Pisos por segmento Latinobarómetro 2023, México — complemento COLA (satisfacción con la vida, con la
democracia y aprobación presidencial) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a): HUMOR/Latinobarómetro,
AUTORIDAD y POLÍTICA/Latinobarómetro). CALC: `CALC-LATINOBAROMETRO-COLA-2023-0001`. Congelada en el COMMIT-1,
**antes** de leer un solo valor de Latinobarómetro 2023 para estos tres reactivos (sólo el cuestionario del
propio zip del payload, ya extraído por texto — no se abrió el `.dta`).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `latinobarometro2023_bd_stata_zip` (manifiesto), sha256 `7689a62d…` COINCIDE (primeros
  8 hex del `sha256` del manifiesto). Miembro leído: `Latinobarometro_2023_Esp_Stata_v1_0.dta` (base en español,
  dentro del mismo zip; el zip también trae `..._Eng.pdf`, `..._Esp.pdf` como cuestionarios y las bases
  `..._Eng_Stata_v1_0.dta`). Se listó el zip con `zipfile` (Python) y se extrajo únicamente
  `Latinobarometro_2023_Esp.pdf` (cuestionario) por texto (`pdftotext -layout`); no se abrió ningún `.dta`.
- `[EJECUTADO]` Ola: sólo 2023 en corpus para este CALC (`OLA = "2023"`). El manifiesto también trae
  `latinobarometro2024_bd_stata` (2024) — **RESERVADA (E.6)**: el medidor no la nombra como input ni la abre;
  este pre-registro tampoco. Una sola ola abierta, sin IC de persistencia.
- `[EJECUTADO]` Este CALC es el **complemento** de `CALC-LATINOBAROMETRO-PISOS-2023-0001` (mismo payload, mismo
  miembro, mismo país, mismo instrumento 2023): ese CALC ya sirvió 21 conductas y quedó sellado bajo la spec
  `forense/prereg-caja/CONFIANZA-LATINOBAROMETRO-PISOS-spec-v1_0.md`. Este medidor reutiliza tres conductas
  nuevas de esa misma lista de 21 (satisfacción con la vida, con la democracia, aprobación presidencial) y repite
  una sola, ORO, `CONFIA-GOBIERNO` (columna `P13ST_E`, mucha/algo vs. poca/ninguna confianza en «Gobierno»):
  su TOTAL debe reproducir el ya sellado (E.5, «lo ya sellado se cita, no se re-mide»).
- `[LEÍDO]` El `.dta` no trae estrato ni UPM (274 columnas por metadatos citados en la spec sellada de PISOS,
  §0; este medidor pasa `estrato=None, upm=None` a `prepara_diseno`): bootstrap ponderado de entrevistas, etiqueta
  de diseño esperada `MAS-PONDERADO-SIN-ESTRATO` (`motor_pisos.py` línea ~155: `"CONGLOMERADOS"` si hay UPM, si
  no `"MAS-PONDERADO"`, más `"-ESTRATIFICADO"` si hay estrato o `"-SIN-ESTRATO"` si no).

## 1 · Unidad, universo, diseño

Unidad: **persona 18+** entrevistada en México (`idenpa = 484`; el lector `M.lee(..., pais=PAIS)` descarta los
demás países antes de devolver filas — `PAIS = ("idenpa", 484)`). Peso `wt` (`PESO = "wt"`, `UPM = None`).
Universo: `edad` ≥ 18 (columna `EDAD_COL = "edad"`, vía `M.edad(f, EDAD_COL)`; el universo se aplica en `mide()`
como `M.num(f["edad"]) >= 18`, y toda conducta fuera de universo sale NaN). Válido para el diseño: `wt` finito y
> 0 (no hay estrato/UPM que filtrar; `prepara_diseno` da a cada entrevista su propia UPM y un estrato único).

## 2 · Conductas (texto del cuestionario `Latinobarometro_2023_Esp.pdf`, dentro del payload)

Constantes del medidor: `CONDUCTAS = {...}`, regla `("bin", columna, [UNO], [CERO])`; `C4 = ([1, 2], [3, 4])`
(mucha/algo vs. poca/ninguna, reutilizado para la conducta ORO).

| conducta | columna | pregunta (texto del cuestionario) | UNO | CERO |
|---|---|---|---|---|
| SATISFECHO-CON-LA-VIDA | `P1ST` | «P1ST. En términos generales, ¿diría Ud. que está satisfecho con su vida? ¿Diría Ud. que está....?» — 1 Muy satisfecho · 2 Bastante satisfecho · 3 No muy satisfecho · 4 Para nada satisfecho | 1, 2 | 3, 4 |
| SATISFECHO-CON-LA-DEMOCRACIA | `P11STGBS_A` | «P11STGBS.A En general, ¿Diría Ud. que está muy satisfecho, más bien satisfecho, no muy satisfecho o nada satisfecho con el funcionamiento de la democracia en (PAÍS)?» — 1 Muy satisfecho · 2 Más bien satisfecho · 3 No muy satisfecho · 4 Nada satisfecho (8 NS, 0 NR fuera) | 1, 2 | 3, 4 |
| APRUEBA-GOBIERNO-DEL-PRESIDENTE | `P15STGBS` | «P15STGBS. ¿Ud. aprueba o no aprueba la gestión del gobierno que encabeza el presidente (nombre)?» — 1 Aprueba · 2 No aprueba (0 NS/NR fuera) | 1 | 2 |
| ORO-CONFIA-GOBIERNO | `P13ST_E` | «P13STGBS A-I. Por favor, mire esta tarjeta y dígame, para cada uno de los grupos, instituciones o personas de la lista ¿cuánta confianza tiene usted en ellas: mucha (1), algo (2), poca (3) o ninguna confianza (4) en...?» — ítem E «Gobierno»: 1 Mucha · 2 Algo · 3 Poca · 4 Ninguna (8 NS, 0 NR fuera) | 1, 2 | 3, 4 |

Todo código fuera de {1,2,3,4} (NS=8, NR=0, y para `P11STGBS_A` valores negativos observados en el sintético de
prueba, ajenos al catálogo) no cae en UNO ni CERO: recodificación binaria estándar del motor (`recodifica`),
fuera de la lista cerrada queda NaN. **ORO-CONFIA-GOBIERNO reproduce, para TOTAL/2023, el mismo resultado que
`CONFIA-GOBIERNO` en `CALC-LATINOBAROMETRO-PISOS-2023-0001`** (mismo payload, mismo miembro, mismo recorte de
país, misma regla `C4`); si no reproduce, es defecto a reportar, no a resolver aquí.

## 3 · Ejes (uno a la vez, heredados sin cambio de la spec sellada de PISOS)

TOTAL · SEXO (`sexo`: HOMBRE 1, MUJER 2) · EDAD (`edad`, cuatro tramos: 18-29, 30-44, 45-59, 60-MAS) ·
ESCOLARIDAD (`REEEDUC_1`: HASTA-BASICA 1-2-3, MEDIA 4-5, SUPERIOR 6-7) · TAMLOC (`tamciud`: MENOS-20MIL 1-2-3,
20MIL-100MIL 4-5-6, 100MIL-MAS 7-8) · CLASE-SUBJETIVA (`S2`, cuestionario «La gente algunas veces se describe a
sí misma como perteneciendo a una clase social...»: 1 Alta · 2 Media Alta · 3 Media · 4 Media Baja · 5 Baja →
ALTA-MEDIA-ALTA 1-2, MEDIA 3, MEDIA-BAJA 4, BAJA 5). `REEEDUC_1` y `tamciud` son variables de perfil/demográficas
del archivo, sin pregunta propia en el cuestionario visible (no se listan en el texto extraído); se citan por
columna, igual que en la spec sellada de PISOS (`CONFIANZA-LATINOBAROMETRO-PISOS-spec-v1_0.md` §3, misma
convención: "Estructura, ejes y lectura: los de aquel medidor, sin cambios" — docstring de este medidor).

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap ponderado de entrevistas (sin estrato ni UPM declarados: cada entrevista
es su propia UPM, un solo estrato — etiqueta `MAS-PONDERADO-SIN-ESTRATO`), semilla y réplicas del contrato
(`contrato["seed"]["valor"]`, `contrato["parametros"]["bootstrap_replicas"]`; en la spec sellada de PISOS:
`PCG64(20260926)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato conservador — una réplica
degenerada da EE/IC vacíos). Receta y motor por sha256, cargados desde bytes de repo (`_guardia_inputs` exige
`INPUTS_REPO = {"receta_pisos_salud", "motor_pisos_confianza"}` con bytes no vacíos, más el payload con
`ruta_absoluta`): `tools/dominios/salud/pisos_diseno.py` (receta) + `tools/dominios/confianza/motor_pisos.py`
(motor), los mismos de la spec sellada de PISOS. Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20260928)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-LATINOBAROMETRO-COLA-2023-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py`, función `test_lb_cola_mas_ponderado`: construye un frame
sintético (sin microdato) con las columnas de `columnas()`, corre `m.mide(f, R, M, REPS, 7)`, exige
`out[f"{m.P}-G-DISENO"] == "MAS-PONDERADO-SIN-ESTRATO"` y cierra con `_cierra()` — que valida contra
`corrida0._valida_outputs` con el `esquema_resultados()` de este CALC y exige que todo valor flotante sea finito
(sin NaN/inf). No prueba la reproducción exacta del TOTAL de `ORO-CONFIA-GOBIERNO` contra el CALC de PISOS ya
sellado (eso se verifica al correr `corrida0 run` sobre el dato real, no en el sintético). Ninguna ejecución
diagnóstica sobre el dato: la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas de 18+ entrevistadas en México; ninguna se promedia con otra
unidad ni con otro instrumento (cada pregunta en su propia escala: satisfacción 1-4, aprobación 1-2, confianza
1-4). **Estructura ≠ cultura:** la satisfacción con la vida, la democracia o la aprobación presidencial
covarían con escolaridad, tamaño de localidad y clase subjetiva de forma esperable por acceso a bienestar y
evaluación de desempeño de gobierno, no por «carácter nacional»; un gradiente por clase subjetiva es primero
condición material y expectativa, no rasgo. **Evidencia:** (a) datos primarios en México (encuesta de personas,
mismo instrumento que ya sirvió 21 conductas en el CALC de PISOS) — nada aquí es (b) diáspora ni (c) marco
importado. **Firewall genético:** ninguna segmentación por ascendencia, color de piel o etnia en este CALC.
**Temporalidad:** todo es RETROSPECTIVO (ola 2023, cerrada); ninguna cifra es PROSPECTIVA; 2024 queda RESERVADA
y no se cita ni se compara. **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
