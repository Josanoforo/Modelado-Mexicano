# ENCARGO · ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1 · Que las reglas de lectura se cumplan solas (hook que bloquea, no consejo), que Codex y Astra las tengan igual que Claude (`AGENTS.md` espejo), que exista una memoria operativa corta importada en cada arranque y regenerada por trámite para no redescubrir la rueda, que se mida el cumplimiento, y que entren los restos de RENDIMIENTO-1

> ENTORNO: **NUBE** — `.claude/`, `CLAUDE.md`, `AGENTS.md`, `canon/`, `tools/`, CI. Hook imprime ENTORNO-DERIVADO; si dice CAJA, solo corre P6.

CABECERA · SHA de redacción `34949751` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`; el orden y la agrupación los decide la sesión) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; contadores propios: intentos bloqueados por el hook (nuevo registro), líneas de contexto que un arranque carga (antes/después), tiempos de suite y de instalación (antes/después). Gate D-14 por pieza en la nota.

## 1 · OBJETIVO
- **P1 · Hook que hace cumplir** (`.claude/settings.json`, `PreToolUse` sobre `Bash` y `Read`): bloquea con mensaje y salida 2 (a) `cat`/`less`/`Read` sin rango sobre archivos > 200 líneas (medido en el momento con `wc -l`), (b) cualquier lectura completa de los derivados listados en `CLAUDE.md` (`data/corrida0/*.tsv`, `CALC-*/resultados.json`, `manifiesto.yaml`, `milpa/estimadores-*`), (c) `git log -p` sin ruta, (d) `pytest` sin `-q`. El mensaje dice qué usar en su lugar (`head -n`, `sed -n`, `Read` con `offset/limit`, `consulta.py`, `jq`/`yq`). Permite todo lo demás. `--permitir-lectura-completa` como bandera de escape declarada, que **registra** el uso. Cada bloqueo y cada escape escriben una fila en `forense/analisis/cableado/bloqueos.tsv` (fecha, sesión si el hook la conoce, comando recortado, motivo); ese TSV es el contador de cumplimiento (derivado, no se edita).
- **P2 · `AGENTS.md` espejo.** Sección «Reglas de lectura y herramientas» idéntica a la de `CLAUDE.md` (una fuente: el texto vive en `canon/REGLAS-DE-LECTURA.md` y los dos archivos lo incluyen o lo copian con un test de igualdad), más las cinco reglas de Astra del 23/sep y la cláusula de autonomía citadas por sha. Codex no ejecuta hooks de Claude: para él, `tools/ci_guardias.py` gana una guardia que revisa el diff del PR y **marca WARN** si el historial de la rama muestra `cat` de derivados en scripts o notas (no bloquea; mide).
- **P3 · Memoria operativa** (`canon/MEMORIA-OPERATIVA.md`, ≤ 80 líneas, **texto inicial en §11 de este encargo, de dirección**): régimen vigente, herramientas y para qué sirve cada una, decisiones activas por objeto con su id de firma, «ya se intentó y no» con la razón, y un índice de dónde está cada cosa. `CLAUDE.md` la importa con `@canon/MEMORIA-OPERATIVA.md`; `AGENTS.md` la cita como lectura obligatoria de arranque; el hook de `SessionStart` imprime sus primeras 15 líneas + `corrida0.py status` recortado, para que ninguna sesión gaste sus primeros 5 000 tokens explorando. **Regeneración:** `/tramite` gana un paso T-MEM que actualiza la sección «Decisiones activas» desde `firmas-pendientes.tsv` (FIRMADA del último corte) y «Herramientas» desde `tools/` con docstring, sin tocar las secciones escritas a mano (bloque derivado marcado, como el tablero). Test: la memoria no supera 80 líneas y el bloque derivado coincide con el TSV.
- **P4 · Subagentes por pieza.** Regla en `CLAUDE.md`/`REGLAS-DE-LECTURA`: en un lote de ≥ 3 piezas, cada pieza corre en un subagente con perímetro propio y devuelve solo su tabla y su diff-stat; el hilo principal ensambla. Con ejemplo de invocación. Es la palanca más grande para actos como COLA-COMPLETA-1 y C3 de Astra.
- **P5 · Restos de RENDIMIENTO-1 (`…ae2a-01..04`):** `pytest -n auto` por `tools/ci_guardias.py` (no por `check.py`); `pyproject.toml` mínimo + `uv.lock`; tiempos de CI antes/después leídos de los logs del PR y pegados; la caché Parquet sigue diferida a caja (P6).
- **P6 · Caché Parquet (CAJA, si la sesión es de caja; si no, `DIFERIDO-A` con receta):** `tools/cache_parquet.py <id>`, fuera del manifiesto, transparente para los medidores (mismo `resultados.json` con y sin caché, test sobre un CALC sellado).
- **P7 · Prueba de arranque real.** Abrir una sesión nueva sobre la rama y pegar en la nota: qué cargó el arranque (líneas), qué bloqueó el hook en tres intentos deliberados (`cat data/corrida0/resultados.tsv`, `Read manifiesto.yaml`, `git log -p`), y cuánto tardó `check.py --rapido`.
«Hecho» sobre el commit final con origin/main fusionado: hook activo con los tres bloqueos demostrados y `bloqueos.tsv` con esas filas · `AGENTS.md` con la sección espejo y test de igualdad VERDE · `canon/MEMORIA-OPERATIVA.md` ≤ 80 líneas, importada por `CLAUDE.md`, impresa al arranque, con T-MEM en `/tramite` y test · regla de subagentes con ejemplo · `pyproject.toml` + `uv.lock` + `-n auto` en `ci_guardias` con tiempos pegados · P6 hecho o diferido con receta · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
**Mesa, 26/sep (chat):** «revisa qué otras eficiencias de tokens podemos usar y asegura que está cableado, que las sesiones lo van a usar y que no se redescubra la rueda en cada sesión». **Cláusula de autonomía v1.0** (aplica a Codex y Astra: se cita en `AGENTS.md`). **D-14** (cada pieza declara defecto real, efecto y costo) y **D-23** (una herramienta de verificación no muta el clon: el hook solo lee `wc -l` y escribe su registro).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`34949751`): `CLAUDE.md` 27 líneas con reglas de lectura + `@instrucciones-proyecto-v2_16.md` (112 líneas cargadas por sesión: se quedan, son la norma); `.claude/settings.json` solo `SessionStart` → `tools/entorno.py --arranque`; sin `PreToolUse`; `AGENTS.md` 284 líneas, 0 menciones a `consulta.py`/`head`/`wc`; `tools/consulta.py` 148 líneas, 6 subcomandos; `docs/sesiones.md` 56 líneas citado en `/acto` l.90; CI con `uv` (12.9 s → 1.3 s); sin `uv.lock`, sin `pyproject.toml`, sin `-n auto`. NO-CORRIDO de RENDIMIENTO-1: `ae2a-01..04`. No existe memoria operativa ni registro de cumplimiento. `[SUPUESTO]` que la versión de Claude Code de mesa soporta `PreToolUse` con `matcher: "Bash"` y salida 2 para bloquear (documentado); si `Read` no es interceptable por hook, se bloquea vía `Bash` y se dice.
ADJUNTOS: ninguno (el texto de la memoria va en §11).

## 4 · YA HECHO / YA DECIDIDO
`ls canon | grep -c MEMORIA-OPERATIVA` → 0. `grep -c PreToolUse .claude/settings.json` → 0. `ls pyproject.toml uv.lock` → no. RENDIMIENTO-1 (#1156) hizo P1/P2/P3 de su encargo; este acto no los repite.

## 5 · PIEZAS
Las agrupa la sesión; sugerencia: P3 (memoria) y P1 (hook) primero porque son los que cambian el arranque de todas las demás; P2; P4; P5; P7 al final; P6 solo en caja.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 + AMPLITUD
1–7 verbatim. Forma del hook (script Python o shell), umbrales (200 líneas, 50 MB), formato de la memoria: tuyos, declarados. Si un hook rompe un flujo legítimo (p. ej. `/acto` necesita leer un encargo de 300 líneas), se añade excepción por ruta declarada, no se apaga el hook. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) tocar sellos, vistas, `registro`; apagar `tools/entorno.py --arranque` · c) mover contadores · d) no aplica · e) — (P6 solo en caja).

## 8 · COMPUERTAS
«El hook bloquea; no edita ni borra nada; su registro es derivado» protege: **borrar** (D-23). «Memoria: secciones a mano intactas por T-MEM; bloque derivado marcado» protege: **congelar** (una memoria editada por máquina sin marcar es un tablero de rama). «`AGENTS.md` = `CLAUDE.md` por test de igualdad» protege: **congelar** (una sola fuente de reglas).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.claude/settings.json`, `.claude/hooks/` (nuevo), `tools/hook_lectura.py` (nuevo), `CLAUDE.md`, `AGENTS.md`, `canon/REGLAS-DE-LECTURA.md` (nuevo), `canon/MEMORIA-OPERATIVA.md` (nuevo), `.claude/commands/tramite.md` (T-MEM), `.claude/commands/acto.md` (una línea en ARRANQUE citando la memoria), `tools/ci_guardias.py` (guardia WARN y `-n auto`), `pyproject.toml`, `uv.lock`, `requirements-dev.txt`, `forense/analisis/cableado/`, `tools/cache_parquet.py` (P6), `.gitignore`, tests, nota, L0, cascada. Ajeno: `verify.yml` fuera de la instalación (uv ya está), `corrida0.py`, medidores, vistas, manifiesto. En vuelo: CIERRE-SEMANAL-1 y PRODUCTO-CONSULTA-1 (nube; no tocan `.claude/` ni `AGENTS.md`), COLA-COMPLETA-1 / ENSU / COLA-LOTE-1 (caja), MISION-ASTRA-6 (lee `AGENTS.md`: cuando este fusione, sus recibos lo citan).

## 10 · LO QUE NO HACE · SUCESORES
No cambia las reglas de contenido; no reescribe las instrucciones (v2.17 es de dirección con mesa). Sucesores: `-2` si `Read` no es interceptable o si la memoria necesita otra sección derivada; RENDIMIENTO-2 queda absorbido aquí.

## 11 · MEMORIA OPERATIVA v1.0 — texto de dirección (se copia a `canon/MEMORIA-OPERATIVA.md`; ≤ 80 líneas; las secciones marcadas ⟲ las regenera T-MEM)
```
# MEMORIA OPERATIVA · Modelado Mexicano · se lee al arrancar, antes de explorar
Última mano de dirección: 26/sep/2026 · derivada: ⟲ por /tramite

## 1 · Régimen vigente (no lo re-diagnostiques)
- Instrucciones v2.16 (+ cláusula de autonomía v1.0: resuelve, interpreta, redacta rotulado, PARA solo por D-19 estricta). Plantilla de encargo v2.1 (v2.2 en trámite).
- Canal de publicación: el job de derivados corre en cada push a main y abre un PR [deriva] que se auto-fusiona; también se dispara a mano (Actions → Run workflow). status lee las vistas: si no hay [deriva] reciente, main va atrasado y se dice.
- Auto-merge solo: [deriva], claude/encola-*, acto/gen2-tramite-*. Todo lo que sella corridas o escribe en milpa/ lo fusiona mesa. Ramas codex/*: recibo de Claude obligatorio (R(a)).
- Recibo: forense/analisis/<unidad>/recibo-para-claude.md, EJECUTADO/LEÍDO por frase.
- Reservas: ola más reciente de todo programa con historia; ENVIPE 2026; ENCO; ENIGH 2024 salvo seis columnas AMAI (C7). ENCIG 2025 y ENVIPE 2025: abiertas.
- Etapa de retadores: cerrada (seis evaluaciones; el piso no pierde). Regla 6: sin retadores, pilotos ni duelos sobre olas vistas. Frente prospectivo = familias 2027.

## 2 · Herramientas (úsalas antes de abrir un archivo)
- tools/consulta.py result|corrida|celda|payload|fp|nc <id> → una línea. tools/vista.py → vistas por referencia (valor_de). tools/benchmark.py → consulta de producto (cuando fusione).
- corrida0.py status (contadores) · demanda (cola) · verify <CALC> · registro --escribe (solo el job).
- tools/entorno.py --arranque (firma de entorno). docs/sesiones.md (clon parcial). tools/escribe_relevo_consumo.py (único que escribe milpa/). tools/marcador_segmento.py --escribe (solo el job).
- Mapa de dominios: canon/mapa-dominios-v1_1.tsv; cola de medición: forense/analisis/dominios/cola-medicion-v1_0.tsv; corpus: forense/analisis/corpus-completo/tabla-final-v1_0.tsv (131 programas).

## 3 · Ya se intentó y no (no lo vuelvas a proponer)
- Git LFS (cuota); sacar la vista del canal (E.7); deploy key para empujar directo (el canal abre PR); bypass de GitHub Actions en rulesets (no existe).
- Pin i-CRUDO al catálogo de momentos: rompe T-REPRO(c); el catálogo lleva valor GEN2 + cita + discrepancia_gen1 (#1115).
- Contar adopciones desde milpa/tramite.yaml a mano: status lee usos.tsv, que solo publica el canal.
- Reglas del motor "existentes" para los diez RESULT de Banxico/CTX/MOTRAL: no existían; se crearon por el escritor (ADOPCION-4).
- Buscar "¿lanzado?" por rama: la plataforma nombra ramas claude/new-session-*; búscalo por archivo en forense/encargos/ y por CONSUMIDO.
- Marcar PROSPECTIVA por el champion vigente: la marca vive en la evaluación original; un sucesor re-medido es RETROSPECTIVA-MECÁNICA y no la borra.

## 4 · Decisiones activas por objeto ⟲ (FIRMADA del último corte, id → una línea)
[T-MEM: firmas-pendientes.tsv estado=FIRMADA, últimos 14 días, id · objeto · EJECUTA]

## 5 · Dónde está cada cosa
- Encargos y adendas: forense/encargos/ (CONSUMIDO al pie). Notas de cierre: forense/notas/. ADR: canon/L0/. Firmas: forense/firmas-pendientes.tsv. Deuda: forense/no-corrido.tsv (razón A.14).
- Producto: canon/catalogo-del-mexicano-v1_N, canon/informe-programa-v1_N, canon/tabla-de-piso-v1_N, docs/ (Pages). Tablero: canon/TABLERO-PROGRAMA.md (solo el bloque derivado; árbol == origin/main True o inválido).
- Sellos: data/corrida0/CALC-*/sello.json; manifiesto de sellos: forense/sellos/. Corpus: data/manifiesto.yaml (por id; nunca cat).
```

## NO-CORRIDO / RESERVAS

- **qué:** P2 · «las cinco reglas de Astra del 23/sep» · **por qué:** `NO-VERIFICABLE-AQUÍ` — el texto no aparece en `forense/`, `canon/` ni `AGENTS.md`, y el clon superficial no deja ver el historial; se citó R(a) firmada en su lugar · **impacto:** `AGENTS.md` no trae las cinco reglas por nombre · **sucesor:** GEN2-TUBERIA-CABLEADO-SESIONES-2 (`NC-260926-GEN2-TUBERIA-CABLEADO-SESIONES-1-0038-01`).
- **qué:** P6 · caché Parquet · **por qué:** `DIFERIDO-A:caja` — la sesión es NUBE; la receta está en la NC · **impacto:** sin caché de microdato en caja · **sucesor:** GEN2-TUBERIA-CABLEADO-SESIONES-2 (`…-0038-02`).
- **qué:** P5 · tiempos de CI leídos de los logs del PR · **por qué:** `NO-VERIFICABLE-AQUÍ` — se pegaron los tiempos medidos en esta nube (9 min 38 s → 6 min 29 s) · **impacto:** el ahorro en el runner no está medido · **sucesor:** GEN2-TUBERIA-CABLEADO-SESIONES-2 (`…-0038-03`).
- **qué:** P7 · abrir una sesión nueva sobre la rama · **por qué:** `NO-VERIFICABLE-AQUÍ` — la prueba se hizo en vivo en esta sesión (3 bloqueos) y en un *resume* · **impacto:** falta el recibo de una sesión fresca · **sucesor:** GEN2-TUBERIA-CABLEADO-SESIONES-2 (`…-0038-04`).

## CONSUMIDO

Ejecutado por PR #1165 (rama `claude/new-session-ibivey`), ADR-260926-GEN2-TUBERIA-CABLEADO-SESIONES-1-0038-01, nota `forense/notas/2026-09-26-GEN2-TUBERIA-CABLEADO-SESIONES-1-cierre.md`.
