# PAQUETE-RECETAS-8 — 2026-09-05

Producido por `ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION` sobre
las 3 fuentes candidatas de percepción cerradas en
`forense/notas/2026-09-05-MAESTRA38-N12-spec.md §2.1` (*Los mexicanos
vistos por sí mismos*, `ECOPRED`, *Cultura Constitucional*). A diferencia
de `PAQUETE-RECETAS-3`/`-5` (recetas reales verificadas) y como
`PAQUETE-RECETAS-6`/`-7` antes de este, este paquete trae **cero recetas
verificadas de ≤1 minuto** — se declara así en vez de fabricar una URL o un
paso sin haberlo ejecutado.

## Por qué cero, no una lista incompleta

Este acto corre en `ENTORNO: NUBE` (declarado en el encargo) y verificó,
antes de intentar cualquier receta, que la red de esta sesión bloquea
**ambos** hosts de referencia de las 3 fuentes — no solo uno, como en
`PAQUETE-RECETAS-6`/`-7`:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://losmexicanos.unam.mx/
000
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
...
"recentRelayFailures": [
  {"kind": "connect_rejected", "host": "www.inegi.org.mx:443",
   "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)"},
  {"kind": "connect_rejected", "host": "losmexicanos.unam.mx:443",
   "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)"}
]
$ WebFetch(https://www.inegi.org.mx/)      -> EGRESS_BLOCKED
$ WebFetch(https://losmexicanos.unam.mx/)  -> EGRESS_BLOCKED
```

Sin acceso de red verificable en esta sesión a ninguno de los dos hosts,
cualquier receta que este acto escribiera sería una secuencia de pasos sin
ejecutar — exactamente lo que A.4/A.13 prohíben (un veredicto de acceso sin
comando que lo haya examinado no es un veredicto). Este acto no fabrica
receta ejecutada: deja las 3 fichas de adquisición (`…N12-sonda.md §4`,
copiadas a `data/curacion-registro/cola-adquisicion-registro.tsv` por este
mismo acto, vía el writer canónico) como `PENDIENTE`, con una receta
**propuesta** (no verificada) cada una, para que un acto de CAJA (con red y
sin esta restricción de política) la corra y confirme.

## Tablero

| # | fuente_canonica en la cola | estado_A4A5 | qué falta |
|---:|---|---|---|
| 1 | `LOS_MEXICANOS_VISTOS_POR_SI_MISMOS_UNAM_IIJ_2015` | PENDIENTE | abrir `losmexicanos.unam.mx`, localizar índice de las 25 encuestas, nombrar cada una — sin verificar en esta sesión (red bloqueada) |
| 2 | `ECOPRED_2014_INEGI` | PENDIENTE | confirmar año exacto, ciudades cubiertas, y si el microdato es público sin registro (patrón `ENADIS`/`ENVIPE`) — sin verificar en esta sesión (red bloqueada) |
| 3 | `CULTURA_CONSTITUCIONAL_UNAM_IIJ` | PENDIENTE | confirmar título de publicación exacto, institución responsable, año(s) — ni la existencia del portal está confirmada, sin verificar en esta sesión (red bloqueada) |

## Contador

Recetas verificadas de ≤1 minuto: **0 de 3** — declarado, no encubierto.
Filas de cola nuevas: **3** (vía `tools/curador_registro/tsv_crudo.py::
upsert_fila`, clave `fuente_canonica`, sobre `data/curacion-registro/
cola-adquisicion-registro.tsv`; vista regenerada con `python3 tools/
vista_cola_adquisicion.py`, nunca escrita a mano). Este acto no descarga
nada, no abre microdato, no toca `data/manifiesto.yaml` (perímetro
explícito del encargo).
