# PAQUETE-RECETAS-6 — 2026-09-04

Producido por `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3` (`FP-298`) sobre las 2
filas `CON-CANDIDATA` de `forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md`
§3 (#3 `dinero.credito.scoring_alternativo`, #4 `dinero.credito.
baja_friccion_usura_dano_downstream`/`N34`). A diferencia de `PAQUETE-RECETAS-3`
(seis `BAJAR` con receta directa) y de las cuatro reales de `PAQUETE-RECETAS-5`, este
paquete trae **cero recetas verificadas de ≤1 minuto** — se declara así en vez de
fabricar una URL sin verificar.

## Por qué cero, no una lista incompleta

`N5` §2.3/§2.4 ya declaraba las dos fichas como «pendiente identificar la URL
exacta» / «ambas pendientes de adquisición» — ninguna de las dos traía, en su propio
texto, una URL de descarga concreta (a diferencia de las filas de `PAQUETE-RECETAS-5`,
que sí las traían y solo faltaba consolidarlas). Este acto corre en `ENTORNO: NUBE`
(declarado en el encargo) y verificó, antes de intentar cualquier receta, que la red
de este entorno bloquea el host de referencia del programa:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
...
"recentRelayFailures": [{"kind": "connect_rejected",
  "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
  "host": "www.inegi.org.mx:443"}]
```

Sin acceso de red verificable en esta sesión, cualquier URL que este acto escribiera
para `cnbv.gob.mx` o `condusef.gob.mx` sería inventada, no verificada — exactamente
lo que A.4/A.13 prohíben (un veredicto de acceso sin comando que lo haya examinado no
es un veredicto). Este acto no fabrica receta: deja la ficha de adquisición (ya
escrita por `N5`, copiada a `data/curacion-registro/cola-adquisicion-registro.tsv`
por este mismo acto, vía el writer canónico) como `PENDIENTE-DE-MESA`, para que un
acto de caja (con red y sin esta restricción de política) identifique la URL y
corra la sonda de alcanzabilidad antes de escribir una receta.

## Tablero

| # (=regla de N5) | fuente_canonica en la cola | estado_A4A5 | qué falta |
|---:|---|---|---|
| 3 | `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | PENDIENTE-DE-MESA | URL exacta del boletín vigente de IMOR de consumo (CNBV) — sin verificar en esta sesión (red bloqueada) |
| 4 | `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` | PENDIENTE-DE-MESA | (i) lectura completa del FD de ENCRIGE 2020 ya en corpus (no es descarga, es lectura); (ii) URL de informes de quejas CONDUSEF/Buró de Entidades Financieras — sin verificar en esta sesión |

## Contador

Recetas verificadas de ≤1 minuto: **0 de 2** — declarado, no encubierto. Filas de
cola nuevas: **2** (vía `tools/curador_registro/tsv_crudo.py::upsert_fila`, clave
`fuente_canonica`, sobre `data/curacion-registro/cola-adquisicion-registro.tsv`;
vista regenerada con `python3 tools/vista_cola_adquisicion.py`, nunca escrita a
mano). Este acto no descarga nada, no abre microdato, no toca `data/manifiesto.yaml`
(perímetro explícito del encargo).
