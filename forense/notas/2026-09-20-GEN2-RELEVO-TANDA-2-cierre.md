# ACTO GEN2-RELEVO-TANDA-2 · nota de cierre

**20 de septiembre de 2026 · `ADR-559` · rama `claude/eager-goodall-2lh66n` · NUBE `cloud_default`, Opus 5**

Encargo archivado verbatim por 0-bis A.3 en
`forense/encargos/2026-09-20-GEN2-RELEVO-TANDA-2.md` (llegó pegado en el
mensaje de lanzamiento).

## ARRANQUE (crudo)

```
$ git fetch --prune && git rev-list --count HEAD..origin/main
0
$ git status --porcelain
(vacío)
$ git log -1 --format="%h %s"
8a842af Merge pull request #908 from Josanoforo/acto/gen2-pisos-enut2019-ejes-1
$ python3 tools/entorno.py --sonda-red
ENTORNO · commit=8a842afccacd · git_status=LIMPIO(0) · python=3.11.15 ·
numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE yaml=6.0.1 pyreadstat=AUSENTE ·
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default CHECK_SELFCHECK_CHILD=sin_variable
MODELADO_RAICES=sin_variable PYTHONHASHSEED=sin_variable TZ=sin_variable ·
red=000 · raices=data_raw:NO · corpus=NO(examinados=0)
$ python3 tools/limpia_arbol.py --reporta
A · worktrees vivos: 1   B · ramas locales fusionadas y vivas: 1
C · base: HEAD esta 0 commits detras de origin/main (al_dia=SI)
D · ramas remotas sin PR abierto: NO-VERIFICABLE-SIN-GH
```

SHA de redacción declarado `8a842afc`, re-derivado al abrir: **coincide**
(`8a842afccacd0abf31c3b7eb3ebcd8eaf668d6b5`). Este acto no abre microdato ni
toca red: `corpus=NO(examinados=0)` es la declaración A.13, no un negativo
sobre el dato.

**Duplicado (0.c), los tres sitios:** `git ls-remote --heads origin | grep -i
relevo` → 0 · `git worktree list` → 1 (éste) · PR abiertos `#910`, `#911`,
`#912`, ninguno con el rótulo.

## COMPUERTA — `#905` (`GEN2-RELEVO-TANDA-1`) en main: CUMPLIDA

Verificada **por producto** (`ADR-277`: el `grep` sobre el log es indicio, no
prueba):

```
$ git log --oneline origin/main | grep -i "RELEVO-TANDA-1"
613d50b Merge pull request #905 from Josanoforo/claude/intelligent-albattani-v7kf2s
2102e2a ## CONSUMIDO: ACTO GEN2-RELEVO-TANDA-1 ejecutado por PR #905
$ git cat-file -e origin/main:forense/encargos/2026-09-20-GEN2-RELEVO-TANDA-1.md && echo EXISTE
EXISTE
$ git cat-file -e origin/main:forense/analisis/relevo-tanda-1/P2-mismo-estimando.tsv && echo EXISTE-P2
EXISTE-P2
```

## P1 · re-verificación slot por slot (12 filas)

| slot | conducta | `p` vigente | RESULT candidato | valor | CALC | estado | sello | replay | grano 1e-6 | P2 `dimensiones_rotas` |
|---|---|---|---|---|---|---|---|---|---|---|
| RES-0025 | `evade_norma_envipe2025` | 0.562774 | `RESULT-EVASIONNORMA-A-P-EVADE` | 0.5627744787844097 | `CALC-EVASION-NORMA-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0026 | `cumple_norma_envipe2025` | 0.437226 | `RESULT-EVASIONNORMA-A-P-CUMPLE` | 0.43722552121559033 | `CALC-EVASION-NORMA-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0028 | `denuncia_por_otra_razon` | 0.705687 | `RESULT-ENVIPE-RES0028-Q-C2-U4` | 0.7056870125426878 | `CALC-ENVIPE-RES0028-U4-DERIVADO-0001` | SELLADA | COINCIDE | REPRODUCE | SÍ | *(re-leído aquí: CASA 5/5)* |
| RES-0031 | `tiene_ahorros_enif2024` | 0.642080 | `RESULT-TIENEAHORROS-A-P-TIENE` | 0.6420795665818781 | `CALC-TIENE-AHORROS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0032 | `no_tiene_ahorros_enif2024` | 0.357920 | `RESULT-TIENEAHORROS-A-P-NO-TIENE` | 0.35792043341812185 | `CALC-TIENE-AHORROS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0033 | `recibe_dinero_familiares_para_vejez` | 0.457707 | `RESULT-DFVEJEZ-A-P-RECIBE` | 0.4577065669362348 | `CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0034 | `no_recibe_dinero_familiares_para_vejez` | 0.542293 | `RESULT-DFVEJEZ-A-P-NO-RECIBE` | 0.5422934330637652 | `CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0053 | `ahorra_solo_informal` | 0.357153 | `RESULT-HVD-A-SOLO-INFORMAL` | 0.3571525665818782 | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0054 | `ahorra_ambas_vias` | 0.204767 | `RESULT-HVD-A-AMBAS-VIAS` | 0.20476743341812176 | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0055 | `ahorra_solo_formal` | 0.080160 | `RESULT-HVD-A-SOLO-FORMAL` | 0.08015956658187823 | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0056 | `no_ahorra` | 0.357920 | `RESULT-HVD-A-NO-AHORRA` | 0.35792043341812185 | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |
| RES-0066 | `horizonte_no_corto` | 0.367218 | `RESULT-HVD-A-HORIZONTE-NO-CORTO-NO-TRABAJA` | 0.36721800000000004 | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` | SELLADA | COINCIDE | REPRODUCE | SÍ | NINGUNA |

Deltas: de `5.55e-17` a `4.79e-07` — el ruido del sexto decimal con que
`milpa/` materializa. **Cero materiales.**

### RES-0028 · la lectura de cinco dimensiones, hecha aquí

`TANDA-1` la hizo contra `RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1` (unidad
**delito**) y encontró `evento;universo;unidad;denominador` rotas. Contra
`data/corrida0/CALC-ENVIPE-RES0028-U4-DERIVADO-0001/spec.yaml`, **las cinco
CASAN**:

| dimensión | legacy (`milpa/tramite.yaml:637`) | spec del candidato U4 | veredicto |
|---|---|---|---|
| **evento** | «ningún delito elegible de la persona pertenece al grupo padre {01,02,06,08}» | `transformacion`: «q=1 sólo cuando ningún delito elegible de la persona pertenece a C2={01,02,06,08}» | CASA |
| **universo** | `dominio_elegible {victima_18_mas, delito_no_denunciado, bp1_23_en_01_08}` | `universo`: «persona de 18 años o más con al menos un delito personal no denunciado elegible en U1 (BPCOD 05..15, BP1_20=2, BP1_23 en 01..08)» | CASA |
| **unidad** | `clase: "DERIVADO·q=1-p(C2,U4), mismo recorte e incertidumbre"` | «U4, unidad persona», `ponderador: FAC_ELE heredado del padre` | CASA |
| **ola** | ENVIPE 2025 (la regla se calibró sobre el padre) | padre `CALC-ENVIPE-0001`, `envipe2025_csv`, levantamiento marzo-abril 2025 | CASA |
| **denominador** | «mismo recorte e incertidumbre» que el padre | `n = 13 023` personas, masa `FAC_ELE = 14 982 594.0`, idénticos a los del padre; `SUMA-P-Q-C2-U4 = 1.0` | CASA |

**Control independiente que no depende de leer texto:** la conducta padre de
la misma regla, `denuncia_con_miedo_o_desconfianza`, **ya está adoptada** a
`RESULT-ENVIPE-DEN-P-C2-U4` (persona/U4, `p = 0.294313`). Aparear su
complemento con un `RESULT` sobre delitos dejaría padre e hijo en dos
unidades distintas dentro del mismo bloque `entonces`. `0.294313 + 0.705687 = 1.0`.

**`FP-391` tiene razón por texto.**

### RES-0055 · qué le falta, y si eso impide anotar procedencia

Le faltan **`se_mueve_si` e IC legacy propio**: los cuatro renglones de la
partición declaran «sin IC propio; no es MEDIDO», y el IC vive en los dos
`MEDIDO` padres del mismo bloque (`formal_cualquiera`, `informal_cualquiera`).
**No impide anotar procedencia** — eso bloquea el *test* de bin 2, que compara
un delta contra un criterio de movimiento y un intervalo, no la *anotación*,
que no consume ninguno de los dos. Precedente vivo en su mismo bloque:
`formal_cualquiera` e `informal_cualquiera` llevan procedencia sin
`se_mueve_si`. **Se adopta.**

## P2 · la procedencia escrita — y el slot que no se pudo escribir

Escritos **once**: `corrida0_resultado_id` + `corrida0_generacion: GEN2`.
Verificado línea por línea que, quitados los dos campos nuevos, el cuerpo del
mapping es **idéntico** al original: ni un `p`, ni un `tier`, ni un `clase`,
ni un nombre, ni un `complemento_de` cambian.

**`RES-0028` NO se escribió.** Escrita la línea, `corrida0 status` **PARA**:

```
PARO · USO-NO-APTO:
  milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon
  -> RESULT-ENVIPE-RES0028-Q-C2-U4 · uso=MEDICION-GEN2 · origen=INDETERMINADO
  · impacto=civico.denuncia.miedo_desconfianza · el origen numérico no está acreditado
```

`milpa/src/linaje.py::aptitud_para_uso` devuelve `NO-APTA` para todo
`origen == INDETERMINADO`, y `tools/corrida0.py:4004` lo convierte en
`ParoRegistro`. El origen es `INDETERMINADO` porque el CALC derivado declara
cuatro `inputs` y dos —`IN-ENVIPE-0001-SELLO` (`sello.json`) e
`IN-ENVIPE-0001-SELLO-SHA256`— quedan `FUNCION-INDETERMINADA`, que
`combina_origenes` propaga sobre toda la mezcla:

```
CALC-ENVIPE-0001                      origen_numerico=NUEVO
CALC-ENVIPE-RES0028-U4-DERIVADO-0001  origen_numerico=INDETERMINADO
  funciones: DATO=1,INDETERMINADA=2,METADATO=1
```

**El padre es `NUEVO`; el hijo es `INDETERMINADO` sólo por citar los dos
ficheros de sello de su padre.** La corrección vive en la lista `inputs` de
una `spec.yaml` **SELLADA**, y el perímetro dice «No toca ningún CALC ni
spec». La línea de `milpa/tramite.yaml:637` quedó **byte a byte como
estaba**. `NC-0384`, con sucesor. Se aplicó la regla del encargo: «un slot que
no pase, no se adopta; no tumba el lote».

`milpa/procedencia.yaml` **no se tocó**: el mecanismo no lo exige.

## P3 · derivados por comando · antes → después

`python3 tools/relevo_usos.py --escribe` · `python3 tools/corrida0.py registro
--escribe` · `python3 tools/corrida0.py status`. Worktree
`/home/user/Modelado-Mexicano`, rama `claude/eager-goodall-2lh66n`.

| contador | antes | después |
|---|---|---|
| `dependencias_numericas_legacy_activas` | **182** | **173** (−9, ver nota) |
| `N_resultados_gen2_adoptados_activos` | **46** | **57** (+11) |
| `relevo-usos` `YA-ADOPTADO` | 24 | **35** |
| `relevo-usos` `CANDIDATO-GEN2` | 12 | **1** (`RES-0028`) |
| `N_resultados_gen2_pendientes_adopcion` | 12 | 12 *(no se mueve — ver abajo)* |
| `N_corridas_selladas` | 102 | 102 |
| `diferencias_materiales` | 0 | 0 |

**Once de los doce quedaron `YA-ADOPTADO`.**

`N_resultados_gen2_pendientes_adopcion` **no se mueve y es correcto**:
`tools/corrida0.py:4330` lo deriva de los `RESULT` citados en
`milpa/tramite-ola5-propuesta-v0.yaml`, y ninguno de los once adoptados
aparece ahí (`grep -c` → 0 en los tres verificados). Es otra población, no la
cola de estos slots.

**El neto del contador es `−9`, no `−11`, y la diferencia está medida, no supuesta.** La base se re-derivó en un worktree limpio de `origin/main` (`registro --escribe`, exit 0): **228** filas de uso, **182** legacy. Esta rama: **230** filas, **173** legacy. Descompuesto por consumidor: salen **exactamente los once** adoptados (`LEGACY-GEN1` → `GEN2`) y **entran dos** slots de demanda que antes no tenían fila de uso — `RES-0175` (`celda_D`, `TRA.evade_norma.envipe2025.escolaridad_x_dominio`) y `RES-0198` (`momento` nº 23 del catálogo, sobre `dinero.ahorro.via_informal`) —, los dos atados a reglas que este acto adoptó y los dos entrando como `LEGACY-GEN1` con `corrida0_resultado_id` vacío. Los archivos fuente son **idénticos** en las dos ramas y este acto no los toca; `_consumidores_celdas_d`/`_consumidores_momentos` (`tools/corrida0.py:587-643`) los enumeran de disco sin condición, así que la aparición se decide más abajo. **No se afirma el mecanismo porque no se probó**, y `corrida0.py` no está en el perímetro: `NC-0387`. Si la aparición fuera un defecto de la vista el valor honesto sería `171`; si es correcta, la adopción **suma** dos dependencias legacy nuevas y `173` es el estado real. `adoptados_activos` sí se mueve limpio: **46 → 57**, `+11` exacto.

## P4 · la vista y el candidato equivocado — la conjetura del encargo es falsa

El encargo preguntaba «¿el CALC derivado no declara pin al slot?». **Sí lo
declara.** `CALC-ENVIPE-RES0028-U4-DERIVADO-0001/spec.yaml:102`, en
`resultados[].unidad`: «q=1-p(C2,U4); persona, FAC_ELE, escala [0,1];
**candidato para RES-0028**».

Lo que falla es el reconocedor. El canal `C2-RESULTADO` usa `RE_ENLACE`
(`tools/relevo_usos.py:150-152`):

```python
RE_ENLACE = re.compile(
    r"(?:releva|ADOPTABLE|candidato a|candidata a|candidato de|candidata de)"
    r"\s+(RES-\d{4})")
```

**«candidato para» no está en la lista.** El padre
`CALC-ENVIPE-0001/spec.yaml:210` escribe «el **candidato a** RES-0028» sobre
`RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1` (unidad **delito**, `FAC_DEL`,
`0.7327566`) y sí casa: por eso la vista propone ése. El CALC derivado tampoco
declara bloque `parametros.adopcion*` (canal `C1`), que habría enlazado por la
vía fuerte.

Es una línea en la spec de un CALC **sellado**: no se edita. El arreglo
alternativo —ampliar `RE_ENLACE`— tampoco se ejecuta: `tools/relevo_usos.py`
está en el perímetro sólo como lectura. `NC-0385`.

**Semilla `PARA-v2.15`:** un canal de enlace que depende de una lista cerrada
de preposiciones convierte una diferencia de redacción en una candidatura
perdida, y nada avisa — aquí sólo lo delató que el valor propuesto no
coincidiera con el `p` vigente.

## P5 · trámite

- `FP-391` y `FP-392` → **`FIRMADA`**, con `ADR-559` y el PR de este acto (A.12).
- `data/corrida0/decisiones.tsv`: `adopcion:relevo-tanda-2` y `estimando:RES-0028-personas`.
- **`cuenta_gen2` de `CALC-ENVIPE-RES0028-U4-DERIVADO-0001` NO se decide aquí: sigue `PENDIENTE-DE-MESA`** (`NC-0386`).
- **CONTADOR del acto: `cuenta_gen2` NO-APLICA** — no sella ninguna corrida.
- Recifrado L0: `python3 tools/cierre_acto.py --aplica` → `APLICADO: gobernanza 557->558 · L0 557->558 · tabla estado 557->558`.

```
$ python3 tests/check.py --baseline
  3 FAIL · 7601 WARN
  LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json
  WARN NUEVOS (estado, no adjudican): 2
  · T03: forense/encargos/2026-09-20-GEN2-RECIBO-CODEX-6.md: cita el anexo que `ACTO GEN2-RECIBO-CODEX-6` declaró NO-ENCONTRADO, que no existe
  · T03: forense/hallazgos.md: cita el anexo que `ACTO GEN2-RECIBO-CODEX-6` declaró NO-ENCONTRADO, que no existe
```

Los 3 `FAIL` son los de la línea base congelada (`T06`×2, `T08`×1). Los 2
`WARN` nuevos vienen de `ACTO GEN2-RECIBO-CODEX-6`, no de este acto.

## Módulo de auditoría — lectura del motor sobre México

Pasar a GEN2 da **trazabilidad, no validez**: cada cifra hereda su universo y
sus sesgos. `evasion_norma` es **por delito**. `tiene_ahorros` y `via_informal`
son de **personas 18+ en ENIF**, que sobre-representa a quien tiene contacto
financiero. `RES-0066` es de **no trabajadores**. `RES-0028` es la **razón
residual** de no denunciar entre personas víctimas: «otra razón» es una bolsa
—trámites largos, pérdida de tiempo, delito de poca monta— y **no debe leerse
como ausencia de miedo ni de desconfianza**. Clase (a) en los doce.

**Peligroso leído simplista: «12 cifras validadas en GEN2».** Son **once**
cifras cuya **procedencia** queda declarada, **ninguna re-medida**, y una que
ni siquiera eso.
