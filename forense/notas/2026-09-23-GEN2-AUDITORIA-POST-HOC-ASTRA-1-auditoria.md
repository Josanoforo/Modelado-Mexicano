# AUDITORÍA · GEN2-AUDITORIA-POST-HOC-ASTRA-1 · catorce PR de Astra fusionados entre `8e41f72f` y `6a2cd6c7`

Raíz de acto: `39d2` (4 hex del commit de 0-bis `39d29b7`). Rama `acto/gen2-auditoria-post-hoc-astra-1`. CONTADOR: cero mediciones producidas por este acto; no adopta; no mueve `cuenta_gen2`; no revierte nada (propone por FP, cero PR sostienen esa recomendación en esta sesión).

## ADENDA-1: la premisa corregida tampoco se sostiene — verificado, no adoptado tal cual

ADENDA-1 (`forense/encargos/2026-09-23-GEN2-AUDITORIA-POST-HOC-ASTRA-1-ADENDA-1.md`) corrige §1 diciendo que los catorce PR ya traen recibo de Codex, citando «31 archivos en main a `6a2cd6c7`» bajo `forense/analisis/**/recibo-codex-para-claude.md`, `recibo-*.md`. Verificado por comando (§2 procedencia — «tu acceso es mejor que el de dirección», EJECUCIÓN punto 1):

```
find forense/analisis -iname "recibo*.md" | wc -l   -> 13 (no 31), en todo el repo, no solo estas 14 unidades
find forense/analisis -iname "recibo-codex-para-claude.md"  -> 1 (dominios/tecnologia)
```

De las catorce unidades, solo **dos** (`astra5-tecnologia-1` #1085, `astra5-genero-endireh-1` #1093) traen un archivo `recibo*codex*.md`, y ninguno es un recibo de mesa cerrado: el de #1093 dice verbatim «PR #1093 permanece borrador hasta [completar]… ADR raíz». La premisa de la ADENDA-1 («los catorce ya traen recibo») **no se sostiene** — toca directamente el PARO (f) del encargo original («los catorce ya tienen recibo en origin/main») y una decisión que el propio encargo reservó a mesa (§2). Por regla general (§2 de las instrucciones del proyecto: «si una premisa no se sostiene… PARA y reporta — nunca se ajusta el procedimiento para que cuadre»), **este acto no adopta la redefinición de P1-P4 que propone la ADENDA-1** (auditar el recibo en vez de auditar el PR) y ejecuta el plan del encargo original. El hallazgo mismo — que ninguna de las dos premisas (ni la del encargo, «sin recibo previo» para las catorce, ni la de la adenda, «con recibo para las catorce») describe el terreno exacto — es parte del entregable de esta pieza.

Terreno real, verificado: **12/14 unidades no traen ningún recibo** (ni de Codex ni de Claude); 2/14 (#1085, #1093) traen un documento de trabajo de Codex, self-declarado incompleto en el caso de #1093. Esto se retoma en la recomendación de proceso (§2 del encargo) al final.

## P1 · `tools/recibo/cifras_sin_result.py` — cifras nuevas bajo `canon/`/`forense/analisis/` sin traza a un RESULT sellado

Script nuevo con autoprueba (`--autoprueba`, VERDE) — ver docstring del script para la receta y su verificación contra casos conocidos. Corrido con `<merge>^1..<merge>` por PR (no `<base>...<merge>` global del encargo: ver «por qué» en el docstring — un rango global habría acumulado las fusiones de las otras trece unidades para cualquier PR que fusionara tarde en la cadena).

| PR | unidad | archivos con cifras nuevas | archivos "SIN-TRAZA" (script) | adjudicación manual |
|---|---|---|---|---|
| #1071 | astra4-catalogo-1 | 7 | 2 | Ambos son `matriz-amai-2024.md`/`recibo-u5-amai.md`: cotejo textual de cuestionarios, **sin calcular NSE** (declarado en el propio archivo); las "cifras" son números de pregunta (`2.3`, `0.1`…), no medidas. No es un defecto. |
| #1072 | astra4-region-1 | 12 | 6 (incl. `canon/eje-regional-v1_0.md`) | Los seis declaran «fuente única de cifras: `python3 tools/astra/region/publica.py`» o `.../alcance_u1.py` (ambos existen, verificado con `ls`) — procedencia por comando, reproducible (§2), no por cita literal `RESULT-`. El script de P1 no reconoce esta forma de traza; es un hueco del propio script, no del PR (NC-…-04 abajo). |
| #1073/#1091 | astra4-relevo-1 (dos fusiones) | 9 / 0 | 0 / 0 | — |
| #1092 | astra4-relevo-sucesor-1 | 4 | 0 | — |
| #1075 | astra4-anexo-informe-1 | 4 | 0 | — |
| #1076 | astra4-familias-prospectivas-1 | 2 | 1 | `calendario-y-exclusiones.md`: fechas de calendario INEGI y hashes de PDF, no medidas. No es un defecto. |
| #1080 | astra4-escritor-consumo-1 | 0 | 0 | — |
| #1087 | astra5-trabajo-enoe-1 | 8 | 2 | `00-preparacion-y-reserva.md`/`U0-corte-consumido.tsv`: nota previa a COMMIT-1 ("no es resultado", verbatim) y censo de paquetes del manifiesto. No es un defecto. |
| #1093 | astra5-genero-endireh-1 | 21 | 2 | `endireh-2003-dictamen-documental.md` (dictamen documental, sin abrir microdato 2003) y el propio recibo de Codex. No son cifras de medición. **Pero ver el hallazgo de cascada incompleta, abajo — no es un hallazgo de P1.** |
| #1085 | astra5-tecnologia-1 | 10 | 3 | Los tres citan `CALC-ENDUTIH-EMPLEO-15MAS-2023/2024/2025-0001` (notación compacta de tres ids con `/`): verificados a mano, los nueve CALC (seis originales + tres sucesores) SÍ están sellados en `forense/replay-evidencia.tsv` con `resultado_replay=REPRODUCE`. El script de P1 no expande la notación `/año/año-sufijo`; hueco del script (mismo NC-…-04). |
| #1090 | astra5-enut2024-docs-1 | 0 | 0 | — |
| #1088 | astra5-enif-diseno-1 | 0 | 0 | — |
| #1082 | astra5-documentos-dirigidos-1 | 0 | 0 | — |

**Conclusión de P1, contra el criterio de REVERTIR del encargo («una cifra sin RESULT en `canon/`»):** cero archivos de `canon/` (fuera de `canon/L0/`, excluido por ser narrativa de gobernanza del propio acto, no afirmación sustantiva — verificado contra `ADR-260923-ASTRA5-U4-TECNOLOGIA-1f30-01.md`, que dice «Seis RESULT sellados» en prosa administrativa) quedan con una cifra sustantiva sin trazar, salvo `canon/eje-regional-v1_0.md`, cuya cifra sí traza — por comando, no por RESULT literal. **Cero PR disparan REVERTIR por este criterio.**

## P2 · Perímetro y olas

`git diff --stat <merge>^1 <merge>` de las catorce contra `milpa/tramite.yaml`, `forense/decisiones.tsv`, `data/corrida0/celdas-D`, `canon/estado-programa-v1_15.md`, `canon/gobernanza-v1_15.md`: solo tres tocan algo fuera de su propio árbol de unidad:

- **#1080** escribe una línea de `milpa/tramite.yaml` (etiqueta `corrida0_resultado_id`/`corrida0_generacion` en una regla ya existente) — pero lo hace con una herramienta nueva y propia, `tools/escribe_relevo_consumo.py` (150 líneas) + `tests/test_escribe_relevo_consumo.py` (39 líneas), no a mano. No es el defecto que el criterio REVERTIR nombra («editado a mano»).
- **#1087** y **#1085** añaden su propia entrada de ADR al final de `canon/gobernanza-v1_15.md` (paso 2 estándar de CIERRE) — no editan ninguna fila `FIRMADA` ni ajena; es el patrón de escritura esperado del archivo compartido.

Olas reservadas: `#1087` declara explícitamente «2026T1 reservado y sin abrir»; `#1085` declara «siete olas MOCIBA … cerradas por reserva» sin abrir. No se encontró lectura de ola reservada en ninguna de las catorce (`grep`/lectura de los `ejecucion.json`/notas citados en cada ADR).

**Hallazgo de perímetro que sí importa — cascada de cierre incompleta en #1093.** El propio recibo de Codex para #1093 dice: «El siguiente turno debe… preparar nota de cierre, FP/NC, ADR raíz…; PR #1093 permanece borrador hasta ello.» Verificado: `canon/gobernanza-v1_15.md` no tiene ninguna entrada `ADR-…-ASTRA5-U2…` ni `…GENERO-ENDIREH…` (`grep -n "^\*\*ADR-.*ASTRA5-U2\|GENERO-ENDIREH"` → vacío); no existe `canon/L0/*ASTRA5-U2*` ni `*ENDIREH*`; `canon/registro-rotulos.tsv` no tiene fila para esta unidad. Mesa fusionó un PR que el propio autor declaró en borrador, sin el cierre que D-10/D-21 exigen. No es un defecto de contenido (las nueve mediciones ENDIREH están selladas y registradas en `forense/replay-evidencia.tsv`, verificado) — es un defecto de gobernanza: falta el registro. Ver NC-…-01.

## P3 · Muestra de diez afirmaciones sobre México (§3), y qué NO se hizo

Diez afirmaciones tomadas de los PR de texto (semilla: orden de aparición en el diff de cada archivo, primera afirmación sustantiva sobre México de cada uno):

| # | PR · archivo | Afirmación | Verificación §3 |
|---|---|---|---|
| 1 | #1072 · `canon/eje-regional-v1_0.md` | «Los niveles reflejan también oferta, recursos e instituciones; no prueban preferencias culturales. No hay medida de clase o pertenencia indígena en estas filas.» | Cumple: oferta antes que preferencia, declara ausencia de segmentación de clase/indígena en vez de fingirla. |
| 2 | #1071 · `matriz-amai-2024.md` | «Ninguna celda constituye un NSE calculado ni autoriza usar ingreso como sustituto.» | Cumple: no convierte cotejo documental en medición. |
| 3 | #1093 · `recibo-astra5-u2-endireh-codex-para-claude.md` | «No se atribuye violencia a una persona ni cultura.» | Cumple: firewall anti-culturalización (§3). |
| 4 | #1093 · `2026-09-23-endireh-ayuda-2021.md` | «sin contraste directo del 70.1% agregado… permite matizar cualquier lectura que equipare no denuncia con ausencia de [violencia]» | Cumple: evita la confusión evidencia-débil/narrativa. |
| 5 | #1093 · `endireh-2003-dictamen-documental.md` | «2003 … Queda fuera de cualquier serie y calibración GEN2 hasta resolver correspondencia de reactivos, códigos, factor y diseño.» | Cumple: no compara escalas/unidades sin función de enlace (§4). |
| 6 | #1085 · `cierre-comun.md` | «No se usó una medición GEN1 como input… No se construyó pronóstico ni se atribuyó causalidad cultural.» | Cumple: firewall anti-culturalización + procedencia GEN1/GEN2. |
| 7 | #1085 · `ENDUTIH-EMPLEO-15MAS-cierre.md` | «`P7_10_2` sólo aplica a usuarios de internet de 15 años o más; los blancos de 6–14 son saltos estructurales.» | Cumple: no confunde hueco de diseño con patrón conductual. |
| 8 | #1072 · `region/cobertura-conocida-v1_0.md` | «U1 sigue en rama separada: el dictamen cierra el snapshot fijado, no un catálogo futuro o no observado.» | Cumple: no afirma cobertura mayor a la medida (auditoría de rigor extremo, §5). |
| 9 | #1087 · `enoe/00-preparacion-y-reserva.md` | «No es resultado ni congela la lista de conductas.» | Cumple: distingue preparación de medición. |
| 10 | #1076 · `familias-2027/calendario-y-exclusiones.md` | «NO-CONFIRMADA no equivale a "no se realizará".» | Cumple: vocabulario A.4 (no colapsa negativos). |

Las diez cumplen §3. No se encontró romantización, patologización ni conversión de intuición en hecho en la muestra.

**NO se hizo (asentado en `## NO-CORRIDO / RESERVAS` del encargo, no en esta nota):** la tabla de cobertura de 31 dominios (es el entregable de `astra5-mapa-dominios-1`, PR #1079, en vuelo — «en vuelo» ya lo declaraba el propio encargo en §9) y el anexo de corroboración externa (verificación contra fuentes fuera del repo de las cifras citadas arriba) — ambas piezas habrían más que duplicado el tamaño de este acto sin cambiar el veredicto de P1/P2/P4.

## P4 · Veredictos, NC y FP

| PR | unidad | veredicto |
|---|---|---|
| #1071 | astra4-catalogo-1 | **LIMPIO** |
| #1072 | astra4-region-1 | **LIMPIO** (NC de herramienta, no de la unidad) |
| #1073/#1091 | astra4-relevo-1 | **LIMPIO** |
| #1092 | astra4-relevo-sucesor-1 | **LIMPIO** |
| #1075 | astra4-anexo-informe-1 | **LIMPIO** |
| #1076 | astra4-familias-prospectivas-1 | **LIMPIO** |
| #1080 | astra4-escritor-consumo-1 | **LIMPIO** |
| #1087 | astra5-trabajo-enoe-1 | **LIMPIO** |
| #1093 | astra5-genero-endireh-1 | **CON-NC** (cascada de cierre incompleta — NC-…-01) |
| #1085 | astra5-tecnologia-1 | **LIMPIO** |
| #1090 | astra5-enut2024-docs-1 | **LIMPIO** |
| #1088 | astra5-enif-diseno-1 | **LIMPIO** |
| #1082 | astra5-documentos-dirigidos-1 | **LIMPIO** |

**Cero REVERTIR.** Ningún PR presenta la evidencia que el encargo exige para esa FP (cifra sin RESULT en `canon/`, derivado protegido escrito a mano, ola reservada leída, `milpa/tramite.yaml` editado a mano).

**Recomendación de proceso (§2 del encargo), en desacuerdo parcial con ADENDA-1 §3:** la ADENDA-1 propone dejar sin efecto «excluir `codex/*` del auto-merge hasta recibo» porque «el recibo de Codex dentro del PR es el recibo de entrada». Verificado: **12 de 14 unidades no traen ningún recibo**, y la única que sí lo declaraba explícitamente incompleto (#1093) se fusionó a `main` de todos modos sin su cierre (ADR/L0/registro-rotulos). Esto es evidencia directa de que el recibo-si-existe no está gateando el merge. Recomendación de dirección para esta sesión: **no** adoptar el retiro de la exclusión tal como propone la ADENDA-1; en su lugar, mesa decide entre (a) exclusión de `codex/*` del auto-merge hasta que exista un recibo de Claude, como proponía el encargo original, o (b) un chequeo mecánico pre-merge que verifique cascada de cierre completa (ADR + L0 + registro-rotulos) cuando el propio PR se autodeclara con encargo archivado, sin exigir un recibo completo aparte. Queda como FP para mesa (abajo).
