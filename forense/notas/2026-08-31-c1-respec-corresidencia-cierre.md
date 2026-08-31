# MAESTRA33-C1 · RE-SPEC-CORRESIDENCIA — COMMIT-2 (resultado)

Continúa `forense/notas/2026-08-31-c1-respec-corresidencia-spec.md` (COMMIT-1, commit `5086ab1`). No se edita ninguna letra de esa spec ni de la entrada `DEVUELTA` en `milpa/tramite-ola5-propuesta-v0.yaml:80-126`.

## Resultado

```
=== familia.corresidencia.adulto_familiar_actual ===
  estado: MEDIDO
  sha256_payload: bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3
  n_persona_csv_total_todas_edades: 94101
  n_persona_universo_eder_20_54: 23831
  n_universo_viviendas_tipo_adqui_no_blanco: 14690
  n_ego_jefe_o_conyuge_eder: 16687
  n_antes_de_peso: 16687
  n_con_ponderador: 9397
  n = 9397
  p = 0.057531
  IC95 = [0.051297, 0.063913]
```

Script: `tools/tasas_base_corresidencia_actual.py` (nuevo). Comando: `python3 tools/tasas_base_corresidencia_actual.py`.

**p = 0.057531 · IC95% [0.051297, 0.063913] · n = 9,397 (no ponderado).**

## Verificación contra la spec congelada, antes de aceptar el resultado

Los tres puntos de control que COMMIT-1 declaró por adelantado (§2-§3, antes de abrir el desenlace) reproducen **exactos** en esta corrida:

| control declarado en COMMIT-1 | valor congelado | valor de esta corrida |
|---|---|---|
| personas EDER elegibles (20-54, historiavida) | 23,831 | 23,831 ✓ |
| egos con `parentesco` propio ∈ {Jefe,Cónyuge} | 16,687 | 16,687 ✓ |
| universo final (+ vivienda no-blanco + factor) | 9,397 | 9,397 ✓ |

Los tres coinciden dígito por dígito con lo que `2026-08-31-c1-respec-corresidencia-spec.md` §2-§3 declaró **antes de que este script tocara `parentesco` para calcular ningún desenlace**. Sirve como control positivo de que el código de COMMIT-2 implementa el universo que COMMIT-1 congeló, y no uno distinto.

## Dos defectos de implementación encontrados y corregidos ANTES de reportar ningún `p` (declarado, no oculto)

Ninguno de los dos cambia la spec — los dos son el código de COMMIT-2 fallando en implementar correctamente lo que COMMIT-1 ya había congelado. Se documentan porque el control de la tabla de arriba es exactamente lo que los atrapó.

**Intento 1** (antes de cualquier corrección): el script leía `persona.csv` completo (94,101 filas, todas las edades del hogar) sin restringirlo al universo respondiente EDER. Salida: `n_ego_jefe_o_conyuge_eder: 40957` — no coincide con el `16,687` que COMMIT-1 ya había declarado. Se descartó sin usar su `p` (`0.047527`, nunca verificado contra la spec, no es el resultado de este procedimiento — es el resultado de un procedimiento distinto y equivocado).

**Intento 2** (primera corrección, incompleta): se restringió `persona.csv` al universo EDER (join contra `historiavida.csv` por `folioviv+foliohog+id_pobla`) **antes** de calcular qué hogares tienen un integrante con código `6`/`7`. Defecto: un ascendiente (código `6`, madre o padre del jefe) de un ego de 20-54 años muy plausiblemente tiene 55+ años y por eso nunca tiene fila propia en `historiavida.csv` — restringir la tabla de composición del hogar al universo EDER subcontaba "ascendiente presente" para cualquier hogar donde el ascendiente mismo no calificara para EDER. No se llegó a ejecutar esta variante hasta el final (se detectó en revisión de código antes de correr).

**Intento 3** (el reportado arriba): la tabla de composición del hogar (¿hay código 6/7 en el `folioviv+foliohog`?) se calcula sobre el roster **completo** de `persona.csv` (94,101 filas); solo la selección de `ego` (quién es el entrevistado cuyo desenlace se mide) se restringe al universo EDER. Los tres controles de la tabla de arriba coinciden exactos con COMMIT-1 — es la primera corrida que implementa la spec tal como se congeló, y es la que se reporta.

## Lo que este número es, y lo que no es (A-bis regla 3 y 4 — escala y universo)

`p=0.057531` (corresidencia ACTUAL, hoy) y `p=0.996086` (corresidencia alguna vez en la vida, entrada `DEVUELTA` intacta) están en la misma escala nominal (proporción ponderada, [0,1]) pero **no son la misma pregunta y no se leen como "el número correcto reemplaza al techo saturado"**. Difieren en tres ejes a la vez, cada uno declarado:

1. **Ventana**: punto-en-el-tiempo (hoy) vs. incidencia acumulada de por vida (alguna vez) — un techo casi saturado en la ventana de "alguna vez" y una prevalencia baja en la ventana "hoy" son exactamente lo que predeciría cualquier lectura de ciclo de vida (casi todos vivieron con un padre en la niñez; pocos adultos de 20-54 años que ya son jefe/cónyuge de su propio hogar están hoy coresidiendo con un ascendiente o suegro). No es una discordancia que exija adjudicación — es la relación esperada entre una tasa de incidencia acumulada y una prevalencia puntual.
2. **Universo**: la corrida heredada cubre a **todos** los respondientes EDER elegibles (16,687→14,887 tras filtro de vivienda, ronda completa); esta corrida cubre **solo** Jefe/Cónyuge (16,687→9,397), 70.0% de los mismos respondientes — restricción estructural forzada por cómo `persona.csv` codifica `parentesco` (spec §2). Un estimando restringido a esa subpoblación no se compara contra uno que no lo está (A-bis regla 4) sin declarar la diferencia de universo — declarada aquí.
3. **Componente de parentesco**: la corrida heredada incluye `hnos_cor` (hermanos) en su cómputo pese a llamarse "ascendiente o suegro" (spec §1); esta corrida no puede replicar ese componente (el catálogo de `parentesco` actual no aísla hermano de "Otro") y por tanto mide estrictamente ascendiente∪suegro, sin hermanos — más ceñida al nombre de la regla que la medición que hereda, no menos.

No se propone aquí ninguna fila de escala ni adjudicación — el `ENCARGO` no lo pide (`situacion: PENDIENTE-DE-MESA`, ver abajo) y decidir la fila es explícitamente trabajo de mesa, no de este acto.

## Reserva metodológica heredada de COMMIT-1, no resuelta aquí

`factor` (vivienda.csv) se usó como ponderador, tal como el `ENCARGO` instruye heredar. El script R oficial de INEGI sugiere `factor_per` (`antecedentes.csv`) para esta población (20-54, EDER). No se recalculó con `factor_per` — sería exceder "lo único que cambia es la ventana". Reserva declarada en COMMIT-1 §3, repetida aquí para que viaje con el resultado.

## Entrada nueva en la propuesta

Se añade a `milpa/tramite-ola5-propuesta-v0.yaml`, **después** de la entrada `DEVUELTA-POR-MESA` (que queda con cuerpo intacto, cero líneas tocadas):

```yaml
  - id: familia.corresidencia.adulto_familiar_actual
    situacion: PENDIENTE-DE-MESA
    si:
      disparadores: PENDIENTE-DE-MESA
    entonces:
      - {conducta: coreside_con_ascendiente_o_suegro_actual, p: 0.057531, clase: "MEDIDO·p(tasa base ponderada)"}
      - {conducta: no_coreside_con_ascendiente_o_suegro_actual, p: 0.942469, clase: "MEDIDO·p(tasa base ponderada)"}
    porque: {generador: [G5], mecanismo: PENDIENTE-DE-MESA}
    tier: PENDIENTE-DE-MESA
    falsable_si: PENDIENTE-DE-MESA
    fuente: ["EDER2017", "ACTO MAESTRA33-C1", "persona.csv[parentesco] (roster ENH actual, no historiavida)"]
    ola_calibracion: "EDER 2017 (unica ola)"
    ic95: [0.051297, 0.063913]
    n: 9397
    ponderador: factor
    universo: "vivienda.tipo_adqui no blanco (mismo filtro heredado) + persona.csv con fila en historiavida.csv (20-54 anios, universo respondiente EDER) + parentesco propio in {1=Jefe, 2=Conyuge} (70.0% de los respondientes elegibles -- unica traduccion sin ambiguedad del catalogo, que codifica parentesco relativo al jefe de hogar, no al entrevistado; ver forense/notas/2026-08-31-c1-respec-corresidencia-spec.md S2). Desenlace = existe otro integrante del mismo folioviv+foliohog con parentesco=6 (ascendiente) o =7 (suegro), traducido segun si ego=Jefe (lectura directa) o ego=Conyuge (invertida). NO incluye hermanos (hnos_cor de la corrida heredada no tiene analogo limpio en el roster actual)."
    hallazgo: "Ventana ACTUAL (hoy) de la re-especificacion que FP-200=(b) pidio sobre familia.corresidencia.adulto_familiar (DEVUELTA arriba, cuerpo intacto, p=0.996086 'alguna vez en la vida'). p=5.75%% vs 99.6%% no es una discordancia que adjudicar -- es la relacion esperada entre incidencia acumulada de vida y prevalencia puntual, mas la restriccion de universo a Jefe/Conyuge (70%% de los mismos respondientes) que el catalogo de persona.csv fuerza. Reserva declarada, no resuelta: ponderador correcto segun script R oficial de INEGI para esta poblacion es factor_per (antecedentes.csv), no factor (vivienda.csv); se hereda factor por instruccion explicita del encargo."
```

## Cascada (este mismo commit)

- `forense/firmas-pendientes.tsv`: `FP-204` → `CERRADA` (ejecutada, con este acto citado) + fila de recibo nueva.
- `forense/hallazgos.md`: una línea.
- `## CONSUMIDO` en el encargo archivado, con el PR (paso final de este acto, tras verificar `tests/check.py --baseline`).
- ADR, recifrado de `canon/gobernanza-v1_15.md`/`estado-programa-v1_10.md`, `registro-rotulos.tsv`: commit de cascada separado, per D-10 (el número de ADR se deriva por comando **al cerrar**, no aquí).

## Contador

`CONTADOR` del encargo: **1 p medida nueva, en propuesta** — no carga a `milpa/tramite.yaml` (sellar es de mesa; el congelamiento sigue vigente, tal como el encargo instruye). Ningún contador de reglas selladas del motor se mueve por este acto.
