# P01 · ENCIG 2023: fijar estimando y consumidor antes de enlazar

**Compuerta:** `DECISION-REQUERIDA`.  
**Prioridad:** 1 entre los paquetes propuestos: el dato ya está medido y sellado; falta una decisión pequeña pero material.  
**No es:** adopción automática ni reapertura de MEDICION-DEMANDA-3.

## 1. Resultado y consumidor

Entregar una correspondencia explícita y científicamente coherente entre la medición ENCIG 2023 por canal y los consumidores de `tramite.mordida.*`:

- `RES-0007` → `milpa/tramite.yaml:tramite.mordida.con_registro:tramite_normal`.
- `RES-0008` → `milpa/tramite.yaml:tramite.mordida.con_registro:paga_mordida`.

El mismo acto debe declarar que `RES-0001/0002` (`tramite.mordida.discrecional`) **no están cubiertos** por esta familia B. La propia spec v1.1 lo dice; compartir `CORR-0001` no vuelve equivalentes dos reglas.

## 2. Slots, fuentes y dato existente

| slot | dato/fuente acreditada | límite |
|---|---|---|
| `RES-0007/0008` | `CALC-ENCIG-2023-0001-v1_1`, `RESULT-ENCIG23-MOR-B-P-PRE-SD=0.130796...`, `...P-NORMAL-PRE-SD=0.869203...`, `...P-DIG-SD=0.023407...`, `...P-NORMAL-DIG-SD=0.976592...`; payload `encig23_base_datos_csv` | los RESULT son por canal; los consumidores actuales no declaran canal |
| `RES-0001/0002` | prior legacy `0.62/0.38` | la spec declara que no mide familia A; no hay RESULT candidato |

F-8 ordena leer la medición `CON-RESERVA`: la cobertura efectiva del universo observado por 8.3 es ~0.19, no la cobertura mecánica de join 1.0.

## 3. Cambio mínimo

Mesa elige una de estas salidas:

- **A · partir el consumidor por canal:** crear consumidores presencial/digital explícitos y enlazar cada uno con su par p/complemento exacto.
- **B · conservar consumidor único:** escribir una spec sucesora que produzca un único RESULT agregado con pesos y universo declarados; luego enlazar p y complemento.
- **C · conservar el prior actual:** declarar que el dato por canal es descriptivo y no releva estos slots.

**Recomendación:** B si el modelo necesita mantener un único consumidor; A si puede representar heterogeneidad por canal. No enlazar sólo el brazo presencial o digital al consumidor sin canal: escogerlo después de ver el resultado cambia el estimando.

## 4. Perímetro y compatibilidad

Acto futuro, serializado: `milpa/tramite.yaml` sólo para los consumidores decididos; spec/CALC sucesor sólo bajo opción B; prueba focal del resolvedor de usos; nota propia. NUBE para decisión/especificación; CAJA sólo si B requiere computar el agregado. No toca MEDICION-DEMANDA-3, piloto de celda-D, F6, theta ni marcador.

## 5. Terminado y secuencia

1. Firma una opción y el universo/canal.
2. Si B, congela spec antes de calcular; si A/C, no re-mide.
3. Declara enlaces `slot → RESULT` exactos o la reserva explícita `SIN-RELEVO`.
4. Ejecuta `relevo_usos.py --json`; `RES-0007/0008` dejan de estar `SIN-CANDIDATO` sólo si hay enlace inequívoco. `RES-0001/0002` permanecen separados salvo una medición propia.
5. Comprueba p+q sobre el mismo denominador y conserva el rótulo `CON-RESERVA`.

No requiere llamadas experimentales ni adquisición.
