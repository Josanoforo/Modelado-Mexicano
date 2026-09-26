# Pisos por segmento MMSI 2016 (escolaridad superior, ocupación directiva y movilidad percibida por tono de piel y origen autoadscrito) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
MOVILIDAD/MMSI). CALC: `CALC-MMSI-PISOS-2016-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de
MMSI (sólo FD `mmsi2016_fd.xlsx`, cuestionario, manual del entrevistador y la cabecera del CSV).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `mmsi2016_bd_csv_zip`, sha256 `c37656bf…` COINCIDE; miembro único `MMSI_2016.csv`.
- `[EJECUTADO]` Una sola ola del módulo en corpus (E.6: se abre y se declara; sin IC de persistencia).
- `[LEÍDO]` Escala cromática: pregunta 10.2, tarjeta del manual del entrevistador (p. 81 impresa, «Tarjeta escala
  cromática»): once tonos A…K, **A el más oscuro, K el más claro** (verificado sobre la imagen de la tarjeta;
  el orden no está en texto). Autorreportado por el informante.
- `[LEÍDO]` El módulo no trae índice ni quintil socioeconómico de origen ni de destino ya construido (sólo
  insumos): la movilidad de quintil que cita MER-033 no se construye aquí (NC propia).

## 1 · Unidad, universo, diseño

Unidad: **persona informante de 25 a 64 años** (`P1_2`). Peso `Factor_Per`; bootstrap de UPM `upm_ENH` dentro de
estrato `est_dis_ENH`. Válido: peso > 0, estrato y UPM no vacíos.

## 2 · Conductas (FD `mmsi2016_fd.xlsx`, hoja «MMSI 2016»)

| conducta | variable y texto | UNO | CERO |
|---|---|---|---|
| EDUCACION-SUPERIOR | `NivEsc_Inf` «Nivel de escolaridad del informante» (derivada de INEGI a partir de 8.3 «¿Cuál es el último año o grado que aprobó en la escuela?»): 1 Sin escolaridad … 6 Preparatoria o Bachillerato · 7 Licenciatura o Superior | 7 | 1–6 |
| EDUCACION-SUPERIOR-MUJER / -HOMBRE | la anterior sólo en `P1_1` = 2 / = 1 («(NOMBRE) es…») | 7 | 1–6 |
| OCUPACION-DIRECTIVA | `DivOcu_Act` «División principal de ocupación del informante» (SINCO 2011 agrupado; 6.5 «¿Cuál es (era) el nombre del oficio, puesto o cargo…?»): 01 Funcionarios, directores y jefes … 09 | 01 | 02–09 |
| PERCIBE-MEJORA-SOCIOECONOMICA | `Per_SitEco` «Percepción de mejora en nivel socioeconómico»: 1 Mejor · 2 Igual · 3 Peor | 1 | 2, 3 |

`NivEsc_Inf` 9 y blanco, `DivOcu_Act` 99 y blanco: fuera.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (`P1_1`) · EDAD (25–34, 35–44, 45–54, 55–64) · TONO (`P10_2` «10.2 A partir de la siguiente escala de
color (MOSTRAR ESCALA CROMÁTICA), ¿cuál considera que es el color de piel de su cara?», 01–11 = A…K, once
categorías) · TONO-TRAMO (A–E, F–G, H–K; tramos fijados aquí, antes de ver la distribución) ·
ORIGEN-AUTOADSCRITO (`P10_3` «En nuestro país viven personas de múltiples orígenes raciales, ¿se considera usted
una persona…»: 1 Negra o mulata · 2 Indígena · 3 Mestiza · 4 Blanca · 5 Otra raza; 9 No sabe fuera) ·
LENGUA-INDIGENA (`P10_1` 1/2) · TAMLOC (`tam_loc_ENH` 1–4).

## 4 · Estimación

Razón ponderada con bootstrap de UPM dentro de estrato, `PCG64(20260927)`, 2 000 réplicas, bloques de 50,
percentiles 2.5/97.5, contrato conservador. Receta y motor por sha256 (los de ENDISEG, misma spec §4). Un eje a la
vez; nunca cruces (EDUCACION-SUPERIOR-MUJER es una conducta de subpoblación, no un cruce de ejes).

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py` (rama sin soporte: ocupación toda «no especificada»).
La primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Firewall genético (§3):** tono de piel y origen autoadscrito entran **sólo como marcador de trato y posición
social**; las conductas son resultados de estratificación (escolaridad alcanzada, ocupación, percepción de
movilidad), no decisiones atribuidas a un grupo, y ninguna lectura va de ascendencia a conducta.
INTERPRETACIÓN-DECLARADA por la sesión con la opción recomendada (encargo §6.4) y rotulada para ratificación en la
hoja de firmas (VETAR es una opción). **Estructura ≠ cultura:** un gradiente por tono es primero discriminación,
origen socioeconómico y región; sin índice de origen no se separan. **Asociación, no identificación.**
**Evidencia:** (a) datos primarios en México. **Temporalidad:** RETROSPECTIVO. **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
