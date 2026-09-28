# Nota de cierre · ACTO GEN2-TABLERO-CARRILES-1 · 28/sep/2026

Contador: **cero mediciones, cero adopciones, ningún contador movido.** El acto construye una vista; todo número del tablero lleva `⟨F…⟩` y sale de `python3 tools/tablero_carriles.py --json`.

- Encargo: `forense/encargos/2026-09-28-GEN2-TABLERO-CARRILES-1.md` (sello de cuerpo `11d9409e…`, 0-bis `e2ebf6cb`).
- ADR: `ADR-260928-GEN2-TABLERO-CARRILES-1-e2eb-01` · L0: `canon/L0/ADR-260928-GEN2-TABLERO-CARRILES-1-e2eb-01.md`.
- Entorno: NUBE (`cloud_default`; `data_raw:NO`, corpus examinados=0). Cero microdato, cero red.
- Base: `98f80cc7` = SHA de redacción = `origin/main` al arrancar (0 detrás).
- Modelo sugerido Opus; modo AUTÓNOMO-AMPLIO.

## 1 · Qué quedó

| pieza | artefacto | comando |
|---|---|---|
| P1 | `canon/crosswalk-carriles-v1_0.tsv` (31 filas, 12 columnas, 0 celdas vacías; regla de unión en su cabecera `#`), registrado en `data/INFRAESTRUCTURA-v1_0.md` | `python3 tools/tablero_carriles.py --crosswalk` |
| P2 | `forense/tablero/TABLERO-CARRILES.md` y `docs/tablero-carriles.html` (31 tarjetas: semáforo, evidencia, stoppers con sucesor, siguiente acción) | `python3 tools/tablero_carriles.py --actualiza` |
| P3 | sección «Adquisición — global» + línea «Adquisición del carril» y stoppers ADQUISICION por tarjeta | ídem |
| P4 | sección «Frente 2027», línea por tarjeta, «Cadena de procedencia» (archivo · blob git · lector · filas); una línea en el job derivados; enlaces en `README.md` y `docs/index.md`; test huérfano `tests/test_tablero_carriles.py` | `python3 tests/test_tablero_carriles.py` |

Verificación (EJECUTADO en esta sesión, sobre el commit final):

```
$ python3 tools/tablero_carriles.py --verifica
canon/crosswalk-carriles-v1_0.tsv: CASA
forense/tablero/TABLERO-CARRILES.md: CASA
docs/tablero-carriles.html: CASA
$ python3 tests/test_tablero_carriles.py
OK test_tablero_carriles: semáforo sintético, 31 tarjetas, derivado_de por línea, HTML ⊆ md, determinismo, crosswalk, manifiesto
```

El test ya atrapó un defecto real antes del primer commit: la línea «Stoppers (n)» y dos rótulos (`A4/A5`, `2027`) salían sin `⟨F…⟩`; se corrigió en el script, no en el test.

Lectura del estado (derivada; `python3 tools/tablero_carriles.py --json | jq '[.carriles[].semaforo] | group_by(.) | map({(.[0]): length}) | add'`): ROJO 7 · AMARILLO 21 · VERDE 0 · GRIS 3. Afirmaciones con adquisición clasificadas (`jq '[.carriles[].adquisicion] | map(to_entries) | flatten | group_by(.key) | map({(.[0].key): (map(.value)|add)}) | add'`): SIN-UNION 494 · PROGRAMA-OBTENIDO-EN-COLA 56 · EN-MANIFIESTO 52 · COLA-PENDIENTE 23. La «Lectura de dirección» del md (opinión, fechada) resume qué significa.

## 2 · Premisas: verificadas y caídas (todas de logística; el objetivo siguió alcanzable)

- [EJECUTADO §3] columnas del mapa, catálogo, reglas, cola, familias, demanda, INDICE: **se sostienen**, con tres precisiones:
  - «afirmaciones por `clase`» (medible en corpus / con adquisición / no medible / no construible) es la columna **`dictamen`** del mapa v1.1; `clase` trae 64 valores de otra naturaleza (CIFRA-PUBLICADA, HIPOTESIS…). El tablero usa `dictamen`.
  - `canon/reglas-contrastadas-v1_0.tsv::origen` **no** nombra el report (valores TABLA-C3-1 / REPORT-V1 / REPORT-V2); el report sale del basename de `fuentes` (v1 y v2 son homónimos).
  - el manifiesto no tiene campo `reserva`: es **`estado_reserva`** (222 entradas).
- [LEÍDO §3] `cifra_v1_5.py` vive en `forense/analisis/informe-v1_5/`, no en `tools/`. No se reutilizó: su tabla es por dominio del mapa, y el carril necesitaba la unión por núcleo; el cómputo equivalente vive en `derivar()`.
- 1 396 afirmaciones del mapa → 37 `report`; los 31 carriles son los de `corpus/reports/` (1 205 afirmaciones); los 6 de `corpus/forense/` quedan fuera por diseño del encargo («los 31 reports»).
- Ya hecho / ya decidido, por objeto: `git ls-tree -r --name-only origin/main forense/encargos | grep -c 'TABLERO-CARRILES\|TABLERO-REPORTS\|CONTROL-CENTRAL'` → 0 (universo: 1 199 archivos de `forense/encargos` en `origin/main`). Sin homónimo nuevo.

## 3 · Decisiones de latitud (tuyas según §6; declaradas)

- **Núcleo del carril** = dominios con peso ≥ 0.20, más siempre el dominante. Sin núcleo, un report con 4 afirmaciones de GENERO entre 57 quedaba «sin cifra» en un dominio que no es suyo.
- **Instrumentos del núcleo** casan firmas, reservas, NC, CALC, actos en vuelo y validación ciega; en la primera pasada, un ENDIREH citado una vez hacía de una firma de ENDIREH la siguiente acción del carril rural-indígena. Dentro de cada categoría, orden por relevancia (afirmaciones que citan lo casado).
- **GRIS** incluye, además del firewall, NO-MEDIBLE-POR-DISEÑO > 50 % («lo que el mapa marque»): sólo Sanción Social (64 %) cae ahí.
- **NC-PARO** entra en la precedencia entre ADQUISICION y CALC (el encargo lista firma > reserva > adquisición > CALC > editorial y pide mostrar NC PARO sin ubicarlas); actos en vuelo se muestran pero no generan acción.
- **Vocabulario de instrumentos** = tabla-final ∪ catálogo ∪ `programa_id` ∪ EXTRA (tokens de la cola citados por los reports y fuera de las tres: CONDUSEF, CSES, ECCO, ENAFI, ENCOVID, ENCUP, ENEM, ENNVIH, IECM, MCPS, OECD, PISA, SESNSP, SHF, TEPJF) − instituciones. EXTRA queda fijo para que el crosswalk dependa sólo de tablas versionadas; el tablero audita en vivo si la cola trae tokens citados fuera del vocabulario (hoy: ninguno).
- **Sin guardián de origin/main.** La salida es función del contenido (blob git de cada fuente en el pie), no de HEAD ni de la fecha; por eso `--actualiza` en una rama y en el canal dan lo mismo sobre el mismo árbol, y el criterio «`git diff` vacío» se sostiene.
- **El test no compara contra el md commiteado** (lo hace `--verifica`): un PR ajeno que mueva `firmas-pendientes.tsv` dejaría el md atrasado sin culpa propia; el canal lo re-deriva.
- **HTML** = el md renderizado desde «Lectura de dirección» (encabezado propio para Pages); el test exige que todo número del HTML esté en el md.

## 4 · Defectos adyacentes arreglados (D-21, ≤ 10 líneas cada uno)

- `tools/tablero_programa.py::DERIVADOS_DEL_CANAL` (+1 línea): el job derivados hace `git reset` tras cada trozo y deja en el árbol lo regenerado; sin la excepción, el guardián de `tablero_programa.py --actualiza` se negaría desde el segundo trozo por «árbol sucio». `python3 tests/test_tablero_programa.py` → 18 pruebas, 0 fallos.
- `tests/check.py::_T25_ARCHIVOS_CONOCIDOS` (+6 líneas): el tablero cita verbatim textos de firmas y NC; su primer rótulo pelado (`E1`) es letra de la hoja NC-DECISIONES-1. Censado por archivo porque el contenido cambia con cada `[deriva]`.
- `.github/workflows/verify.yml` (+1 línea, la que el encargo pide): corre `--actualiza` tras `tablero_programa.py` y añade los dos archivos al árbol del trozo; si falla, avisa y no tumba la vista. Coordinación con TUBERIA-3: una sola línea, sin tocar las vecinas.

## 5 · Hallazgos (una línea en `forense/hallazgos.md` cada uno)

- La reserva de ENIGH 2024 que declara `canon/MEMORIA-OPERATIVA.md` §1 no tiene token ni en `data/manifiesto.yaml::estado_reserva` ni en `tabla-final::olas_reservadas_al_entrar`: ningún lector por campo la ve (A.16).
- `tools/hook_lectura.py` cuenta «líneas» de un PNG y bloquea `Read` de una imagen sin rango; con `offset/limit` pasa.

## NO-CORRIDO / RESERVAS

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| «el canal lo publica (un `[deriva]` con el tablero nuevo, run_id en la nota)» | `DIFERIDO-A: primer run del job derivados tras el merge de mesa` — el job corre en el push a `main`; antes del merge no hay run que citar | el tablero existe en la rama y regenera idéntico, pero ningún `[deriva]` lo ha publicado todavía | `GEN2-TABLERO-CARRILES-2` o el `/tramite` siguiente asienta el run_id (NC-260928-GEN2-TABLERO-CARRILES-1-e2eb-01) |
