# Nota de cierre · ACTO GEN2-TUBERIA-METRICA-RECTORA-1

## Dónde se imprime `celdas_validadas` · comando

| Dónde | Comando |
|---|---|
| Módulo fuente (única definición) | `python3 tools/celdas_validadas.py --json` |
| Línea de una sola fila | `python3 tools/celdas_validadas.py --linea` |
| `corrida0 status` | `python3 tools/corrida0.py status \| grep "^celdas_validadas"` |
| `digesto --mesa` (primera línea) | `python3 tools/digesto_tramite.py --mesa --stdout \| head -1` |
| Tablero del programa | `python3 tools/tablero_programa.py --json` (importa el módulo) |
| Cabecera de era del estado | `canon/estado-programa-v1_15.md` (línea nueva, sin comando: cita el SHA de este cierre) |
| Δ en el cierre de cualquier acto | `python3 tools/cierre_acto.py --encargo <ruta>` (sección `CELDAS_VALIDADAS`) |

## Compuerta (§8)

`python3 -c "import sys; sys.path.insert(0,'tools'); import json, tablero_programa as T; print(json.dumps(T._celdas_validadas(), sort_keys=True))"` antes de mover (P0, guardado como línea base) y después de moverla (P1): JSON idéntico, mismo SHA. **PASA.**

## `grep -rn "def _celdas_validadas" tools/`

Una sola aparición, en `tools/celdas_validadas.py`.

## Premisas verificadas

Las cinco premisas `EJECUTADO` del encargo se re-verificaron de pasada y se sostuvieron: la función vivía sólo en `tablero_programa.py`; devuelve `total_celdas_validadas=92` con el desglose 35+57, prospectividad PROSPECTIVA 20/RETROSPECTIVA 59/IDENTICO 89/SIN-EMISION 30/EMITIDA-SIN-R 16; `adoptadas` no está entre sus claves; `canon/estado-programa-v1_15.md` cita `92` a mano en seis sitios (no tocados); el conteo de ramas vivas se re-derivó al abrir (ver `## NO-CORRIDO / RESERVAS` del encargo archivado).

## `adoptadas`

No entra a este acto (§2/§6 del encargo): sin definición ni fuente sellada. Queda como propuesta para mesa; sucesor `SIN-ASIGNAR`.

## Concurrencia con sucesores de `#980`

Al cerrar, ningún sucesor de P-C (retiro del canal WARN) ni de P-D (derivados fuera de PR) de `#980` estaba fusionado ni en vuelo sobre los archivos de este perímetro — verificado contra `origin/main` en el 0-bis y de nuevo antes de empujar. No aplicó la rama de "fusiona `main` hacia la rama y re-aplica".
