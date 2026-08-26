# Cierre — `E2-PREP-L-RUN`, 26/ago/2026

**Acto:** `E2-PREP-L-RUN` (NUBE, `cloud_default`, repo-only). Encargo: `forense/encargos/2026-08-26-E2-PREP-L-RUN.md`. SHA de redacción: `186f090`. CONTADOR: cero, declarado — este acto produce el instrumento del primer marcador, no el marcador.

## 1 · Arranque

- **Repo:** clon existente en `/home/user/Modelado-Mexicano`; no se clonó ninguno nuevo. `git log -1 --format="%h %s"` → `186f090 Merge pull request #369 from Josanoforo/claude/cierra-4-firmas-8b6f2r`. `git status` → limpio, rama `claude/lanzamiento-l-v1-prep-st1rkm`.
- **SHA:** coincide exactamente con el declarado por el encargo (`186f090`). Sin diferencia que refrescar ni cifra que re-derivar por movimiento de `main`.
- **`data/raw/`:** ausente, no creada ni enlazada — este acto no toca microdato ni red, no lo requiere.
- **Entorno:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con lo esperado, NUBE). Sonda cruda: `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (fallo de conexión, consistente con `cloud_default` sin red saliente). Este comando examinó **0 archivos** — es sonda de red, no de árbol; el negativo se declara con ese conteo (A.13), no se infiere de ausencia de payloads.
- **Espejo:** no consultado. Toda cifra de este acto sale del clon citado en (Repo), comandos a la vista abajo.

## 2 · Compuerta Cero — re-verificación de los 6 pins `F1`

Salida cruda de `sha256sum`, una invocación por archivo, ejecutada desde `forense/prereg-duelo-v2/`:

```
a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d  pipeline-L-adv1-m2.py
14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1  corredor-B-tasa-base.py
7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d  corredor-E-combinacion-LM.py
beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb  scoring-adv1-m3.py
140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11  sorteo-resultados-v1_0.md
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2  marco-congelado-piloto-v1_0.tsv
```

Los seis valores **COINCIDEN** exactamente con la tabla `F1` de `prereg-corrida-v1_0.md:99-108` y con los prefijos precargados en el encargo. `marco-congelado-piloto-v1_0.tsv` coincide además con `CONGELADO-v1_0.sha256`. Sin discordancia — `A.7` no aplica.

## 3 · Entregable

`forense/prereg-duelo-v2/lanzamiento-L-v1_0.md` — el paquete autocontenido para correr `L`: compuerta de hashes lista para pegar, invariantes citados con archivo:línea (15 celdas del sorteo, 2 variantes, `k=8`, `temperatura=1.0`, `modelo_id`/`version_declarada`, `comparacion_principal_id=L-solo` con `FP-162` FIRMADA, cero descartes, agregado §5, plantillas intactas), aclaración de ceguera (F0.2/RANURA 2), implementación de `llamar_modelo` lista para pegar (sin tocar `pipeline-L-adv1-m2.py`), dónde corre `L-RUN` (fuera de NUBE, único destino de red `api.anthropic.com`, firma A.2 de tres partes para el ejecutor), formato de capturas (240 JSON en `corridas-L/`), orden sagrado y muralla (L nunca abre microdato ni corre B/E/scoring), mapa de qué sigue, y checklist de mesa.

**Modelo sellado en este lanzamiento:** `claude-opus-4-6` — la RANURA DE MESA del encargo quedó tal cual (no fue editada), así que el lanzamiento fija ese `modelo_id` conforme a `F2(a)` del prereg.

## 4 · Qué no hizo este acto

No corrió ninguna llamada al modelo. No editó `pipeline-L-adv1-m2.py`, el prereg, el sorteo, el marco congelado ni las plantillas. No abrió microdato. No creó `forense/prereg-duelo-v2/corridas-L/` (la crea `L-RUN` al ejecutar). No añadió fila de tablero nueva.

## 5 · ADR y recifrado

Máximo `ADR` re-derivado por conteo entero, `re.findall(r'ADR-(\d+)')` sobre `canon/gobernanza-v1_15.md` → **199**, sin huecos (no `sort -t- -k2 -n`, que parte en el primer guion y da un máximo falso). Este acto candidatea **`ADR-200`**. Sin `PR` abierto en vuelo conocido al momento de escribir esta nota que compita por el mismo número; si al fusionar otro acto ya tomó `ADR-200`, este se renumera al fusionar segundo, conservando íntegro lo ajeno — misma regla aplicada en `ADR-198`/`ADR-199`.

## 6 · Suite

`python3 tests/check.py --baseline` (nunca `--freeze`): **19 FAIL · 129 WARN, LÍNEA BASE VERDE** — sin regresión frente a `tests/baseline.json`. Fricción encontrada y resuelta antes del verde: (a) `T15` exigía que las cabeceras de `gobernanza`/`estado` citaran `200 ADR`, no `199` — corregido en ambos archivos; (b) `T22`/`T25` marcaban los tres archivos nuevos de este acto (citan `RANURA`/`RANURA DE MESA` y el rótulo pelado `E2`, el nombre propio del acto) como marcadores sin dueño — extensión mínima de `_T22_ARCHIVOS_CONOCIDOS`/`_T25_ARCHIVOS_CONOCIDOS` en `tests/check.py`, mismo precedente que `ADR-147(c)`/`ADR-164`/`ADR-197` (RANURA 1/RANURA 2 ya resueltas por `FP-162`/`ADR-197`; `E2` es el nombre del acto, no un espacio nuevo de la escala). `tests/check.py` no estaba en el perímetro declarado del encargo — desviación mecánica mínima, declarada aquí, no oculta.

## 7 · Escrituras

`forense/prereg-duelo-v2/lanzamiento-L-v1_0.md` (nuevo) · esta nota · `forense/encargos/2026-08-26-E2-PREP-L-RUN.md` (A.3, `CONSUMIDO`) · `canon/gobernanza-v1_15.md` (`ADR-200`) · `canon/estado-programa-v1_10.md` (`§L0` recifrado `199→200`) · `tests/check.py` (censo `_T22_ARCHIVOS_CONOCIDOS`/`_T25_ARCHIVOS_CONOCIDOS`, desviación mecánica mínima fuera del perímetro nominal, declarada en esta nota).
