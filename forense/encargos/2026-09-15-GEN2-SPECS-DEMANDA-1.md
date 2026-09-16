ENCARGO · ACTO GEN2-SPECS-DEMANDA-1
Recorre las 19 CORR sin candidato del registro GEN2: congela la spec ejecutable de las que se puedan, clasifica A.4 las que no

CABECERA · redactado contra `f5a5227` (merge de #771 — base verificada en el ARRANQUE, 0 commits detrás de `origin/main`) · ENTORNO: **NUBE** — sin `data/raw`, corpus NO montado; el acto abre SOLO codebook y metadato (E.5), microdato JAMÁS · COMPUERTA: ninguna · MODELO: Opus (juicio de medición: qué es construible y qué no) · Estado: VIVO · candidatos FP/ADR: deriva al cierre.
LANZAMIENTO, verbatim (mesa, 15/sep/2026): el texto de PIEZAS de abajo es el mensaje de lanzamiento tal como llegó; este archivo lo fija por A.3 porque llegó pegado en el mensaje que invocó `/acto`, no como archivo del repo.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `f5a5227` — el encargo llegó sin el bloque y A.8 manda pararse o contestarlo con comando, no suponerlo):

(1) ¿Existe ya la estructura? SÍ. `data/corrida0/demanda-corridas.tsv` y `demanda-resultados.tsv` (cabecera `# DERIVADO — NO EDITAR`, derivados por `tools/corrida0.py demanda`) gobiernan el dominio «demanda GEN2 por corrida»; `data/manifiesto.yaml` gobierna «qué payload tenemos»; `data/inventario-reactivos-v1_2.tsv`, `data/inventario-reactivos-descargas-mx-v1_2.tsv` y `data/inventario-reactivos-ext-v1_0.tsv` son los inventarios canónicos vigentes que A.15 exige citar; `forense/prereg-caja/` guarda las specs humanas selladas y `data/corrida0/CALC-*/spec.yaml` los contratos ejecutables. Ningún hueco de índice que reportar.

(2) ¿Existe ya el contenido? Parcialmente — y eso es entregable, no interrupción:
```
$ awk -F'\t' 'NR>2 && $4 ~ /SIN-CANDIDATO/' data/corrida0/demanda-corridas.tsv | wc -l
19
```
(la premisa del encargo se confirma: 19 de 82 corridas sin candidato). Y:
```
$ for n in 0001 … 0019; do grep -rl "CORR-$n" data/corrida0/*/spec.yaml forense/prereg-caja/; done
CORR-0002 → data/corrida0/CALC-ENCIG-0001/spec.yaml + forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md   [EXISTE-SATISFACE]
CORR-0003 → data/corrida0/CALC-ENCUCI-0001/spec.yaml + forense/prereg-caja/ENCUCI-MORDIDA-PROTESTA-spec-v1_0.md   [EXISTE-SATISFACE]
CORR-0007 → forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md (+ CORRECCIÓN 15/sep)   [EXISTE-NO-SATISFACE: cubre 2 de 8 RESULT]
CORR-0009 → data/corrida0/CALC-ENIF-0001/spec.yaml + forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md   [EXISTE-NO-SATISFACE: no releva RES-0031/0032/0065]
CORR-0013 → citado en data/corrida0/CALC-EDER-0001/spec.yaml con «NO se releva aquí»   [NO-ENCONTRADO como cobertura]
CORR-0017 → citado en ENIF-AHORRO-spec-v1_0.md solo para corregir un rótulo del encargo   [NO-ENCONTRADO como cobertura]
CORR-0001, 0004, 0005, 0006, 0008, 0010, 0011, 0012, 0014, 0015, 0016, 0018, 0019 → 0 aciertos   [NO-ENCONTRADO]
```
El encargo pide «recorrer las 19»: dos de ellas (`CORR-0002`, `CORR-0003`) ya están relevadas por una spec congelada y no se re-especifican — se asientan como ya cubiertas, que es lo que A.8 existe para no volver a pagar.

(3) ¿La estructura es posterior al trabajo? SÍ, y la brecha se declara: `demanda-corridas.tsv` nació el 7/sep/2026 (`tools/corrida0.py demanda`, GEN2); las conductas que puebla son de GEN1 (jul–sep/2026) y sus `script_legacy`/`spec_legacy` están vacíos **por construcción** — `SIN-CANDIDATO-EN-EL-REGISTRO` describe el registro legado, no el mundo. Que una corrida no tenga candidato ahí no implica que no exista una spec GEN2 posterior que la releve: la lista de (2) es exactamente ese cruce, y por eso se hace con comando y no de memoria.


(2-bis) ¿Las reglas que este acto PRE-REGISTRA ya se midieron? `tools/ya_medido.py`, una invocación por regla (ADR-340, exigido por `T-YAMEDIDO` a todo acto que clasifique, pre-registre, cargue o selle una regla del motor). Salida verbatim de la última línea de cada una:

```
$ python3 tools/ya_medido.py familia.seguro.volatilidad_ausencia_estado
  MEDIDA-EN: CALC-B-0001, tramite-ola5-propuesta-v0.yaml, tramite.yaml
  (CALC en data/corrida0) data/corrida0/CALC-B-0001/resultados.json:41  resultado_id=RESULT-B-ENIGH-2022-P ejecutado=SI sello=VALIDO  [TASA-EJECUTADA]
$ python3 tools/ya_medido.py dinero.planeacion.formal_estable
  MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
$ python3 tools/ya_medido.py familia.union.libre
  MEDIDA-EN: tramite.yaml
$ python3 tools/ya_medido.py familia.cuidado.recae_mujeres_40mas
  MEDIDA-EN: tramite.yaml
```

Y las **dos** reglas que la tanda 2 pre-registra, mismo trámite:

```
$ python3 tools/ya_medido.py salud.vacunacion.disponible_ensanut2024
  MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
$ python3 tools/ya_medido.py civico.participacion.concurrencia_presidencial_conversion
  milpa/tramite.yaml:1122  situacion=SELLADA tier=MEDIA veredicto_heredado=ACOTADA p=0.345267
  NUNCA-MEDIDA
```

Las cuatro están MEDIDAS en `milpa/` (GEN1) y **ninguna tiene `CALC` propio** — salvo `familia.seguro.volatilidad_ausencia_estado`, cuyo único `CALC` (`CALC-B-0001`) declara `reglas_bajo_prueba: NINGUNA` bajo la firma `T9` y por tanto **no la releva**. Eso es exactamente lo que este acto congela: no falta el número, falta la cadena (`E.2`). Ninguna de las cuatro cambia de cifra por este acto.

Y el `NUNCA-MEDIDA` de la segunda **no es un fallo de la herramienta: es el hallazgo**. `ya_medido.py` encuentra la regla en el motor con su `p`, y aun así la declara nunca medida porque su entrada YAML **no trae `sha256_payload` ni `medido_en`** — sin procedencia, `clase: MEDIDO·Δ` es una etiqueta, no una cadena. Es exactamente por eso que `CORR-0016` sale con `payload_ids = NO-DECLARADO-EN-EL-REGISTRO`, y exactamente lo que `CALC-L8-CONVERSION-0001` repara: declara el insumo (`IN-L8-JSON`) con su `sha256` y su ruta. Ninguna de las seis reglas cambia de cifra por este acto.

PIEZAS (texto de mesa, verbatim)

> 1 · NUBE — ACTO GEN2-SPECS-DEMANDA-1 (Opus, integral, multi-día)
>
> Recorrer las 19 CORR sin candidato, en tandas por instrumento. Por cada una: A.8/A.15 contra los inventarios canónicos vigentes (¿el payload está en corpus? ¿los reactivos existen — verificados por archivo, secciones del codebook leídas del índice, no del nombre?), y entonces redactar y CONGELAR la spec ejecutable (md humana + spec.yaml, D-15, abriendo SOLO codebook y metadato — E.5 lo permite en nube, microdato jamás). Las que no se puedan: clasificación A.4 con bloqueador nombrado — payload faltante → cola/sobre, decisión → propuesta armada para tu firma (CORR-0001/ENCIG-2023 cae aquí: el acto te trae la decisión "adquirir vs. celda sin fuente" preparada, no pendiente). Entregable: N specs congeladas en COMMIT-1 + el mapa completo de las 19. Cada spec congelada es munición directa del encargo 2.

PERÍMETRO: `forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-1.md` (este archivo) · `forense/prereg-caja/` (specs humanas nuevas) · `data/corrida0/CALC-*/spec.yaml` (contratos ejecutables nuevos) · `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (el mapa de las 19) · `forense/notas/` (nota de cierre) · `forense/no-corrido.tsv` · `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv` (cascada). NO toca: `milpa/` (ningún consumidor cambia de cifra) · `data/manifiesto.yaml` · ningún CALC sellado · ningún microdato.

CONTADOR: **cero mediciones** — se dice en esta línea y no se disfraza (regla de señal v2.3). Un acto de specs congeladas produce contratos, no números: los números los produce la corrida en CAJA que consuma estos contratos.

LO QUE NO HACE: no corre ningún `CALC` · no abre un solo byte de microdato · no adopta ninguna cifra a ningún consumidor · no edita specs selladas (las sucede, si hiciera falta) · no decide por mesa ninguna de las adjudicaciones que arma.

CIERRE: cascada completa + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` con el PR.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «redactar y CONGELAR la spec ejecutable (**md humana + `spec.yaml`**, `D-15`)» — el `medidor.py` de las seis corridas congeladas (`NC-0192`) | `DIFERIDO-A:ACTO GEN2-MEDICION-DEMANDA-1`. El encargo enumera las **dos** capas de `D-15` y el acto de CAJA declara en su propio perímetro que congela el medidor cuando una spec llegue sin él. Se declara como **se hizo distinto**, no como omisión: el precedente de la casa (`CALC-ENCIG-0001`, `CALC-B-0001`) sí lo escribe en `COMMIT-1`, pero en actos que además lo corrían. Éste no puede correrlo (NUBE, sin corpus, `numpy`/`pandas` AUSENTES) y un medidor no probado contra ningún payload sería peor insumo que ninguno | `preflight` reporta `BLOQUEADO:script_ausente` en las seis — único bloqueo en cinco; `CALC-ENSANUT-0001` trae además `RAIZ_NO_CONFIGURADA=descargas_mx`, que es del **entorno** y no de la spec. Las seis corridas no pueden correr y `N_corridas_selladas` no se mueve de 63 | `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, en vuelo) |
| «Recorrer las 19 `CORR` … y entonces redactar y CONGELAR la spec ejecutable» — **6 de 19** congeladas tras dos tandas (`NC-0193`) | `DIFERIDO-A:tanda 3`. **Dos** más son construibles y no están bloqueadas por nada material: los residuos de `CORR-0009` (`RES-0031`/`0032`/`0065`) y de `CORR-0007` (`RES-0025`/`0026`), que comparten payload con specs ya selladas y sólo añaden desenlaces. Es presupuesto de sesión. De `CORR-0007`, además, `RES-0039`…`0042` tienen propuesta **no firmada** (`NC-0088`): eso es decisión, no spec | Dos contratos menos para el acto de CAJA. Las **9** restantes sí tienen bloqueador nombrado en el mapa y no son deuda de este acto | tanda 3 de `ACTO GEN2-SPECS-DEMANDA-1` (nube) |
| Hallazgo `A.15` sobre `CORR-0013` **no corregido** (`NC-0194`) | `FUERA-DE-PERÍMETRO`. `milpa/` no se toca en este acto y el derivado no se edita a mano | Un `verify` resolvería el ZIP de EDER (`bcc7eb90…`) como INPUT de una cifra calculada sobre ENADID 2023, **y el hash coincidiría**: la cadena `E.2` sería falsa sin que nada la contradiga. ENADID está en el manifiesto y no aparece en ninguna corrida | MESA (si la celda ENADID se sucede) + el acto que toque `milpa/` |
| Hallazgo `A.8` sobre `CORR-0010` **no corregido** (`NC-0195`) | `FUERA-DE-PERÍMETRO` | `CORR-0010` queda `BLOQUEADA` por identidad cuando su payload está en disco y verificado por hash (`00e4b0b4…f039` = `enif_2024_enif_2024_bd_csv`). **No va a cola de adquisición** | el acto que toque `milpa/`; la tanda 2 congela la spec en cuanto la identidad esté escrita |
| Hallazgo `A.15` sobre `CORR-0014` **no corregido** (`NC-0196`) | `FUERA-DE-PERÍMETRO` | El texto de `milpa/` sigue diciendo que el ponderador `FAC_HOG` está en `tvar_crea.csv`, donde no está. No bloquea la corrida (la spec fija `tsdem.csv` y añade la guarda); bloquea la lectura | el acto que toque `milpa/` |
| «decisión → propuesta armada para tu firma» — las tres quedan **armadas y sin firmar** (`NC-0197`) | `DECISIÓN-DE-MESA-PENDIENTE`. Armarlas es lo que el encargo pide; firmarlas no es del ejecutor | **6 de las 10 `CORR` bloqueadas** esperan una de estas tres firmas, no trabajo. Premisa de **D1** corregida en este acto: el encargo la planteaba como «adquirir vs. celda sin fuente» y el payload ENCIG 2023 está en el manifiesto desde el 29/jul/2026 en cinco formatos — la frase «ENCIG2023, sin payload» de `ENCIG-MORDIDA-spec-v1_0.md:142` es falsa en la letra desde entonces y **no se edita** (`E.3`) | MESA |
| Firma de contador con OBJETO para las seis specs (`NC-0198`) | `DECISIÓN-DE-MESA-PENDIENTE`. El lanzamiento autoriza **congelar** y no declara OBJETO sobre el contador; `FP-367`/`FP-368` piden autoridad + fecha + OBJETO y no se satisface | Las seis llevan `cuenta_gen2 = PENDIENTE-DE-MESA`: cuando CAJA las selle **no incrementan el contador GEN2** salvo que la firma llegue. `ACTO GEN2-MEDICION-DEMANDA-1` sí trae firma con OBJETO y prevé declararla en `data/corrida0/decisiones.tsv` sin editar el `COMMIT-1` — esa es la vía; esta fila existe para que no se pierda si no se recorre | MESA o `ACTO GEN2-MEDICION-DEMANDA-1` (vía `decisiones.tsv`) |

## CONSUMIDO

PR [#775](https://github.com/Josanoforo/Modelado-Mexicano/pull/775), abierto contra `main` el 15/sep/2026 y **no fusionado por el ejecutor** (el merge es de mesa). Cascada de cierre completa en `d944f0d`: **ADR-510** en `canon/gobernanza-v1_15.md`, anotación L0 en `canon/estado-programa-v1_13.md`, los tres contadores mecánicos reconciliados por `tools/cierre_acto.py --aplica` (`gobernanza 509→510 · tabla estado 509→510`), rótulo `GEN2-SPECS-DEMANDA-1` censado en `canon/registro-rotulos.tsv`, `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` registrado en `data/INFRAESTRUCTURA-v1_0.md`, y `NC-0192`…`NC-0198` en `forense/no-corrido.tsv`. `python3 tests/check.py --baseline` **VERDE** antes y después del merge de `origin/main` (`3 FAIL · 3655 WARN`, nada nuevo frente a `tests/baseline.json`).

**Tanda 2** — PR [#776](https://github.com/Josanoforo/Modelado-Mexicano/pull/776), abierto contra `main` el 15/sep/2026 y **no fusionado por el ejecutor**. Mesa fusionó el PR #775 (`da9b47a`) mientras la tanda 2 corría: un PR fusionado está terminado y no puede seguir el trabajo posterior, así que la tanda 2 va en un PR **nuevo** sobre la misma rama, rebasada por **merge** —no por rebase— a propósito: `origin/claude/amazing-noether-l1iegk` es de donde el `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA) consume las specs tanda tras tanda, y un force-push le movería el suelo. **Sin ADR nuevo:** la tanda 2 es continuación del mismo acto, así que extiende el texto de `ADR-510` en vez de abrir un `ADR-511` que contaría el acto dos veces; los tres contadores mecánicos siguen en 510. Congela `CORR-0017` (`CALC-ENSANUT-0001`) y `CORR-0016` (`CALC-L8-CONVERSION-0001`), y deja el registro entero al día en **6 de 19**.

**Este encargo NO queda agotado.** Es multi-día por diseño del lanzamiento: la **tanda 1** congeló cuatro specs (`CORR-0011`, `CORR-0012`, `CORR-0013`, `CORR-0014`) y entregó el mapa completo de las 19; la **tanda 2** congeló dos más (`CORR-0017` y `CORR-0016`); la **tanda 3** (`NC-0193`) tiene dos más construibles y sin bloqueo material — los residuos de `CORR-0009` y de `CORR-0007`.

## ENMIENDA FECHADA — 15/sep/2026, por FIRMA DE MESA

Se añade al pie por adición. **No edita una sola línea del texto anterior** (`E.3`): lo que arriba dice «Este encargo NO queda agotado» queda archivado como lo que la mesa leyó al firmar, y es esta enmienda —posterior y fechada— la que rige.

**FIRMA DE MESA, mesa, 15 de septiembre de 2026 — verbatim:**

> FIRMA DE MESA, mesa, 15 de septiembre de 2026 — OBJETO: ACTO GEN2-SPECS-DEMANDA-1 queda AGOTADO-CON-REMANENTE-BLOQUEADO; no se abre tanda 3.

**Qué cambia de estado.** El encargo pasa de `NO AGOTADO (multi-día)` a **`AGOTADO-CON-REMANENTE-BLOQUEADO`**. No se abre **tanda 3** y este acto no vuelve a la nube.

**Cuál es el remanente, exactamente.** Las **tres `BLOQUEADAS` que dependen de la hoja de firmas 2**, todas ya rastreadas en el tablero — esta enmienda **no abre filas nuevas** en `forense/no-corrido.tsv`:

| remanente | fila del tablero | estado verificado al firmar |
|---|---|---|
| `CORR-0004` (`tramite.gobierno_digital.coercitivo:adopta`) — precedencia del MEDIDO / prior | `NC-0206` | `CERRADA` por `ACTO GEN2-FIRMAS-MESA-2`, 15/sep/2026; la salida la firma mesa |
| la spec ENADID para `familia.union.libre` (hallazgo `A.15` sobre `CORR-0013`) | `NC-0194` | `ABIERTA`; sucesor ya escrito: MESA (decide si la celda ENADID se sucede) + el acto que toque `milpa/` |
| las cuatro celdas sin `B` del marco (`DIN-M-01`, `FAM-M-01`, `TRA-M-02`, `TRA-M-03`) | `NC-0179` | `CERRADA` por `ACTO GEN2-FIRMAS-MESA-2`, 15/sep/2026; el crosswalk entre instrumentos es decisión de mesa |

**Quién las escribe.** Al firmarse la hoja 2, las specs de ese remanente las escribe **MANTENIMIENTO-Y-ARCHIVO-2 como pieza** —ya tiene permiso sobre `milpa/` donde una firma lo autorice—, no un tercer acto de nube. Su corrida va a una **MEDICION-DEMANDA-3 corta**.

**Por qué no hay tanda 3 que reclamar.** `NC-0193` —la fila que reservaba «dos más construibles» para una tanda 3— ya está **`CERRADA`** por `ACTO GEN2-MEDICION-DEMANDA-2` (PR [#789](https://github.com/Josanoforo/Modelado-Mexicano/pull/789)), 15/sep/2026, **por producto**: los residuos de `CORR-0009` y de `CORR-0007` tuvieron spec congelada en el PR [#781](https://github.com/Josanoforo/Modelado-Mexicano/pull/781) y quedaron SELLADOS vía sus sucesoras `v1_1`. Esa fila lo dice con todas sus letras: «la tanda 3 de `GEN2-SPECS-DEMANDA-1` ya no tiene objeto». La firma de mesa y el tablero coinciden; esta enmienda sólo lo asienta.

**CONTADOR:** cero mediciones. Una enmienda de asiento no produce números, no congela specs, no corre ningún `CALC` y no adopta ninguna cifra a ningún consumidor. Ningún `milpa/`, ningún `CALC` sellado y ningún microdato se tocan.

**Cierre (A.14):** cascada mínima —este archivo y nada más— y **rama fusionada o borrada al cerrar**.
