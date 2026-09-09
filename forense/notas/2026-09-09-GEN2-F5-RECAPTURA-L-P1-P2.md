# ACTO GEN2-F5-RECAPTURA-L — nota de cierre (P1+P2, y P3 tras autorización de mesa)

**Fecha:** 2026-09-09 · **Entorno:** CAJA (Ubuntu/WSL de mesa), Sonnet ·
**Redactado contra** `origin/main = ffeeca2cd1a9df65f513f1b286b35761c1fcf806`
(PR #667) · **ejecutado, tras merge a mitad de sesión, contra `origin/main =
cc1cfe2cf15f3abac8fcd64473531f7f99cb65d0`** (PR #668).

**Compuerta declarada por el encargo:** PR de `ACTO GEN2-RETIRO-CRON-LEGADO`
fusionado. **No se cumplía al arrancar** (verificado contra GitHub: sin PR, sin
rama, sin issue; crontab legado de WSL instalado y verificado en vivo con
`crontab -l`). Mesa, informada, autorizó P1+P2 ahora, P3 diferido
([[feedback-partial-gate-deviation]]). **Se cumplió a mitad de sesión** (`PR
#668`, merge `cc1cfe2`, ~15:16) — re-verificado empíricamente (`crontab -l` ya
no trae la línea). P3 sigue sin ejecutarse: la autorización de mesa cubría
P1+P2, no P3, y lanzar 224 invocaciones reales de captura sellada no es una
ampliación de alcance que esta sesión se conceda a sí misma.

---

## 1 · P1 — lo que se congeló (COMMIT-1)

`forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md` (sha256
`78a40f48495004802cc1b43d72d0edffb7d51a3c802085bce568f6f462eddbfb`, tras la
enmienda fechada que registra el cambio de estado de la compuerta):

- Pregunta primaria (transferencia, corte temporal por celda) y secundaria
  (uso documental) declaradas sin mezclarse.
- `L-spec-v1_3.json` generado — no existía — desde `marco-M-sorteado-v1_3.tsv`
  vía la plantilla mecánica ya sellada de `genera_l_spec_v1_1.py`, sin editarla.
- Corte temporal por celda: derivado de un escaneo real de los 37 documentos
  del corpus GEN2 adoptado (`corpus/reports/` + `corpus/forense/`) — 37
  agentes paralelos, uno por documento, lectura completa, extracción
  estructurada de toda cita de encuesta+ola — contra el calendario real de
  olas por encuesta (`data/manifiesto.yaml`). 0 a 6 documentos excluidos por
  celda, cada exclusión con la cita exacta que la motivó
  (`paquete-corpus-F5-v1_0/manifiesto.json`).
- Escala de adjudicación B-bis (GANA/PIERDE/EMPATE/INCONCLUSO) para
  `L_SOLO` vs `L_CORPUS` por desviación absoluta respecto a `R` — pregunta que
  no estaba sellada — construida reutilizando el aparato ya sellado de
  `procedimiento-scoring-v1_2.md` (unidades `z`, `delta=0.5`, `seed=42`,
  `nivel_ic=0.95`, `replicas=10000`), no inventado desde cero.
- Tres fuentes de incertidumbre declaradas por separado, con su límite.
- Contaminación declarada: los `R` ya existen en el repo y en memoria de
  dirección; el blindaje de P2 es físico, no de promesa.

**Enmienda a `runner_l_cli.py`** (sellado desde `MAESTRA33-E17`, con tres
amendments previas ya en el árbol — `MAESTRA34-N4`, `L-CORRIDAS-v1_2`, `P4/D3`;
ninguna citada por el encargo original). Hash antes: `b2c3965851423d07…`; hash
después: `2f1983eb687dd2f4…` (tabla completa, §8 de la spec). Tres cambios:

1. **Contexto real de `L+corpus`** — reemplaza el placeholder literal
   `"[contexto tierizado -- no construido en este acto]"` (que ninguna corrida
   anterior, v1.1 ni v1.2, había reemplazado nunca, porque ninguna llegó a
   `--correr`) por ensamblado real desde `paquete-corpus-F5-v1_0/`, con
   presupuesto de 600 000 caracteres y truncamiento declarado por invocación.
   **Hallazgo, no anticipado por el encargo: las 14 celdas truncan siempre**
   (31-37 documentos de ~35 KB promedio exceden el presupuesto en las 14) — el
   orden alfabético de inclusión queda fijado antes de capturar, declarado en
   cada registro (`contexto_corpus_metadata`), nunca en silencio.
2. **Orden de captura contrabalanceado**, semilla 42 (reutilizada de `FP-168`).
3. **Reintentos acotados y contados** — hasta 2 por captura; agotados, la
   captura se escribe con `estado_captura=RECHAZADO_TRAS_REINTENTOS` en vez de
   tumbar el lote completo con una excepción no capturada (defecto real del
   runner heredado: `ejecutar_corrida()` no tenía ningún manejo de error).

**Regresión, corrida en este acto:** `--dry-run` verde para `L-spec-v1_1.json`
(176 rutas, sin cambio de conteo), `L-spec-v1_2.json` (224, sin cambio) y
`L-spec-v1_3.json` (224, contexto real para las 112 invocaciones `L+corpus`,
0 sin paquete).

## 2 · P2 — el blindaje, evidencia por punto

Directorio aislado construido en `$TMPDIR/aislado-gen2-f5-v1_0/` (fuera de
todo clon — el sandbox de esta sesión solo permite escribir dentro del
worktree o en `$TMPDIR`; escribir fuera de ambos habría exigido desactivar el
sandbox sin necesidad, dado que `$TMPDIR` ya satisface "fuera de todo clon").
Contiene: `runner_l_cli.py` + sus dos dependencias por-ruta
(`carga_l_v1_1.py`, `pipeline-L-adv1-m2.py` — el encargo dice "el runner"
mencionando solo un archivo; en la práctica `runner_l_cli.py` no corre sin
estas dos, ya selladas en `PAQUETE-L-v1_2.md` §1, hash verificado igual aquí)
+ la spec sellada + `paquete-corpus-F5-v1_0/` + `corridas-L/` vacío (destino
de escritura, no dato preexistente).

**(1) `ls` del directorio aislado — sin repo, sin `data/raw`, sin
`corridas-R`.** Verificado: `git rev-parse --show-toplevel` falla (no hay
`.git` alcanzable); `ls data/raw/` falla (no existe); `find . -iname
corridas-R` vacío. Contenido raíz: `F5-duelo-contemporaneo-spec-v1_0.{md,sha256}`,
`L-spec-v1_3.{json,sha256}`, `carga_l_v1_1.py`, `pipeline-L-adv1-m2.py`,
`runner_l_cli.py`, `corridas-L/` (vacío), `paquete-corpus-F5-v1_0/`.

**(2) Firma A.2 (tres partes), corrida DESDE el directorio aislado:**
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `<unset>` (Ubuntu/caja, no nube,
consistente con la CABECERA); sonda de red `curl -s -o /dev/null -w
"%{http_code}"` a `https://api.anthropic.com/` → `404` (red real, no
bloqueada — distinto del `000` que un sandbox sin red devuelve); `ls
data/raw/` → no existe. Sin ruta al clon (verificado arriba).

**(3) Mecanismo de invocación — verificado por lectura de código y
`--dry-run`, no empíricamente por-captura (P3 no corrió):**
`construir_comando_cli()` no incluye `--add-dir` ni ninguna bandera de
herramientas de archivo (`--tools ""` las deshabilita); el prompt lo
construye `construir_prompt()` desde `SpecCelda` + el contexto ensamblado por
`cargar_contexto_corpus()`, nunca a mano; `sha256_prompt` se calcula y
registra por captura (`ejecutar_corrida()`, verificado en el código, no
ejercido aquí). **Pendiente de P3:** el hash real de cada uno de los 224
prompts, que solo existe una vez que la captura corre.

**(4) `claude --version` y `claude auth status`** (comandos de metadato, no
invocan modelo — corridos en esta caja, no en el directorio aislado, mismo
resultado):

```
claude --version  ->  2.1.267 (Claude Code)
claude auth status ->  {"loggedIn": true, "authMethod": "claude.ai",
                         "apiProvider": "firstParty", "subscriptionType": "max"}
```

Sesión de `claude.ai`, **sin** `ANTHROPIC_API_KEY` — exactamente la condición
que `PAQUETE-L-v1_1.md` §4-bis exige ("si muestra API key, PARO"). **Pendiente
de P3:** timestamp por captura.

**(5) Sesiones stateless, misma ventana** — verificado por construcción:
`ejecutar_corrida()` hace un `subprocess.run()` por invocación, `claude -p
--max-turns 1`, sin `--continue` ni reutilización de sesión; `orden_captura()`
intercala las 224 tuplas por semilla declarada, no agrupa por brazo — cuando
P3 corra, los dos brazos comparten la misma ventana de ejecución por diseño,
no por casualidad.

**Las cinco evidencias se produjeron.** Los aspectos que requieren una
captura real (el hash exacto de cada prompt, el timestamp de cada invocación)
quedan pendientes de P3 por construcción — no son un defecto del blindaje, son
la parte de la evidencia que solo existe una vez que hay captura.

## 3 · Hallazgo no anticipado por el encargo

Las 14 celdas de `marco-M-sorteado-v1_3.tsv` son, ID por ID, universo por
universo, las mismas 14 de `marco-M-sorteado-v1_2.tsv` — el único campo
transportado a `L-spec` que difiere es `conducta` en `TRA-M-02/03/07`
(`paga_mordida` → `paga_mordida_encig2025`). `PAQUETE-L-v1_2.md` (2/sep/2026)
ya había construido, para esas mismas 14 celdas, un paquete mecánico completo
que nunca llegó a `--correr` — su placeholder de contexto documental es
exactamente lo que este acto reemplazó.

## 4 · Suite

No se corrió `tests/check.py --baseline` en este acto — ninguno de los
cambios toca código de producción fuera de `forense/prereg-duelo-v2/`, y el
runner enmendado se regresionó directamente (§1). Se deja para el revisor del
PR confirmarlo si lo considera necesario.

## 5 · P3 — ejecutado, tras autorización explícita de mesa

Mesa, preguntada si lanzar P3 ahora que la compuerta se despejó, respondió
verbatim: *"Si está dentro del encargo ejecutalo si no no"* — P3 es
explícitamente la tercera pieza del encargo (COMMIT-2+), así que se ejecutó.

**Defecto medido en la primera invocación real, no supuesto.** Con el
contexto real de `L+corpus` (hasta 600 000 caracteres) ya construido (§1),
`subprocess.run(comando + [prompt], ...)` tiró `OSError: [Errno 7] Argument
list too long` — el argumento excede `MAX_ARG_STRLEN` de `execve` en Linux
(~128 KiB). Las 4 capturas `L-solo` (sin contexto) ya escritas no tocaban ese
límite y siguieron siendo válidas. **ENMIENDA F5-2**: `construir_comando_cli()`
ya no recibe ni devuelve el prompt; `ejecutar_corrida()` lo entrega por
`subprocess.run(..., input=prompt)` — verificado empíricamente con `claude -p`
(lee stdin cuando no recibe `[prompt]` posicional) antes de aplicar. Hash
`2f1983eb…` → `54c994b2…`. Regresión verde (v1.1: 176, v1.2: 224, v1.3: 224).
La corrida, reanudable, retomó exactamente donde se había quedado.

**Resultado: 224/224 capturas, embudo limpio.** `OK=224 · rechazadas=0 ·
reintentos=0`. Las 28 combinaciones (celda × variante) tienen sus 8 réplicas
cada una, sin faltantes. Duración total: 3 914 s (~65 min).

**Hallazgo declarado, no oculto: `modelo_real=None` en las 224 capturas.**
Limitación pre-existente y ya documentada (`FP-240`, medida primero sobre las
128 capturas de v1.2 con cliente `2.1.258`): el cliente en uso
(`claude --version` = `2.1.267 "Claude Code"`) sigue sin emitir la clave
`model` en `--output-format json`. `version_declarada` queda en el valor
precargado (`claude-opus-4-6`), nunca sustituido por falta de valor real.
Alias solicitado en cada invocación: `opus`.

`forense/prereg-duelo-v2/manifiesto-capturas-P3-v1_0.json`: hash individual
por archivo (`sha256_archivo`) ligado a `sha256_prompt`, bundle
`2ce0a78871f1afc17af52e2e63097a7d6112f0ff4963373ea84b1097643f89de`. Las 224
capturas viven en `forense/prereg-duelo-v2/corridas-L/` junto a las 424
históricas (648 total), con sufijo `__v1_3` que las distingue por nombre.

## Cascada

Cierre completo: `ADR-444` (`canon/gobernanza-v1_15.md`), `L0`
(`canon/estado-programa-v1_12.md`), rótulo `GEN2-F5-RECAPTURA-L` censado
(`canon/registro-rotulos.tsv`), reconciliados con
`tools/cierre_acto.py --aplica` (443→444 en los tres anclajes). `NC-0134`
CERRADA. El encargo, con su tabla NO-CORRIDO/RESERVAS (vacía — las tres
piezas se ejecutaron) y `Estado: CONSUMIDO`, vive en
`forense/encargos/2026-09-09-GEN2-F5-RECAPTURA-L.md` (0-bis, A.3).
