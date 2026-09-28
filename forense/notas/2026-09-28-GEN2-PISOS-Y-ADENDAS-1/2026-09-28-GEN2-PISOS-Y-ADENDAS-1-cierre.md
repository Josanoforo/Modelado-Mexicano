# GEN2-PISOS-Y-ADENDAS-1 · cierre

28/sep/2026 · `ACTO GEN2-PISOS-Y-ADENDAS-1` · CAJA (`tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red 200, corpus montado, 514 archivos examinados) · rama `acto/gen2-pisos-y-adendas-1`, worktree `~/mm-gen2-pisos-y-adendas-1` · 0-bis `fa42a3c1` sobre `origin/main = 723b62c1` (15 commits por delante del SHA de redacción `65da69fd`; no es PARO) · ADR `ADR-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01`. Modelo: **Opus 5.5** todo el acto (encargo: Opus). Subagentes en Sonnet sólo para ejecutar: cuatro sondas de lectura (P1–P4) y el recalculador de P4; lo que se juzga (premisas, specs, compuertas, comparaciones, dictámenes) lo hizo el hilo principal.

**CONTADOR.** `cuenta_gen2`: **+2 CALC** con cadena E.2 (`CALC-ENCIG2023-CONFIANZA-PISOS-0001`, 5 460 RESULT; `CALC-PISO-PERSISTENCIA-ERROR-0002`, 317 RESULT), ambos **sellados en disco, no registrados** en la vista: el registro lo hace el job `[deriva]` al fusionar (NC `…-fa42-04`). No adopta: la adopción es de mesa por el merge (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR), sin fila FP propia (encargo §6: «PREGUNTA A MESA: ninguna»). `celdas_validadas`: 219 @ HEAD, Δ0 (no hay R; `cierre_acto.py` no deriva el valor en el 0-bis). P3 y P4: cero mediciones.

## 1 · Qué se hizo, por pieza (orden P3 → P4 → P1 → P2, el del encargo)

| pieza | firma | commits | resultado |
|---|---|---|---|
| **P3** F3 (1a, 2a, 3a) | mesa 28/sep | `7ea1b372` | 1(a) ratificado sin tocar nada. 2(a): los dos PDF de MOCIBA copiados a `data/raw/MOCIBA/` (corpus compartido `mm-corpus/raw/MOCIBA`) y sus dos `archivo:` editados en el manifiesto (diff 2+/2−, sin re-serializar): `--verifica` **COINCIDE 2/2**; control con el manifiesto anterior **AUSENTE 2/2**. 3(a): los cuatro `enco_*_reservado` verificados por comando con los tres estados A.1: **COINCIDE 4/4** (4 archivos examinados, hasheados sin abrir); sin raíz, `RAIZ-NO-CONFIGURADA 4/4`; `manifiesto.py --verifica` da `FUERA_DE_PERIMETRO 4/4`. Salidas crudas: `p3-verifica-mociba.txt`, `p3-verifica-enco.txt`, script `p3_verifica_enco.py` (esta carpeta). |
| **P4** D-15 | no requiere | `5c274ce3` → `fd54ddbd` → `5b257360` | Tres adendas `forense/prereg-caja/ENDIREH-PISOS-2021-{DISCRIMINACION,NOFISICA-BC,AYUDA}-spec-v2_0.md` (+ sidecar) y protocolo con tolerancia, commiteados **antes** de recalcular; recalculación de las 32 llaves afectadas por un subagente con sólo adenda + FD + cuestionario + microdato, commiteada y empujada **antes** de abrir los sellados; dictamen **PASA 3/3** (§3). |
| **P1** H4 (a) | mesa 28/sep | `4baf555e` → `d63e9001` | `CALC-ENCIG2023-CONFIANZA-PISOS-0001`: confianza institucional ENCIG 2023, 25 reactivos × 43 celdas, sellado al primer `run` (15 s), `verify` aislado REPRODUCE/IDENTICO (§4). |
| **P2** F4 (a) | mesa 28/sep | `6d19b282` → `83348589` | `CALC-PISO-PERSISTENCIA-ERROR-0002`: mismo estimando que 0001 contra una constancia congelada; 317/317 RESULT iguales a los de 0001 (RETROSPECTIVA-MECÁNICA, §5); `verify` aislado REPRODUCE/IDENTICO. |

E.7: `forense/replay-evidencia.tsv` +2 filas (`3fe35aa7`), evidencia `evidencia-replay-gen2-pisos-y-adendas-1-2026-09-28.json`. Otros: `ccc4781b` (T02: nombres únicos en P4 con `git mv`, comparación re-derivada idéntica byte a byte; T25: censo del encargo, que cita momentos del catálogo sin medirlos).

### 1.1 · Premisas que cayeron, interpretaciones y ejecuciones declaradas

- **[SUPUESTO] del encargo §3 («la letra F4 cita el CALC y el archivo por nombre»): se sostiene.** La hoja `forense/analisis/nc-decisiones/hoja-2026-09-27.md` §F4 nombra `CALC-PISO-PERSISTENCIA-ERROR-0001` y `tools/marcador_segmento.py`. P2 no paró.
- **P2 · «marcador vigente» — INTERPRETACIÓN-DECLARADA** (escrita en la spec v1.1 antes del COMMIT-1). La hoja pide congelar «el marcador-segmento vigente» **y** reproducir los 317 RESULT; el marcador de hoy ya no produce esos ids (verify del 22/sep; además celdas `SOLO-PISO` pasaron a `EVALUADA` con los R GEN2 del árbitro, medidas por `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`). Se congeló el marcador vigente **en el sello de 0001** (`24afe8b9`), derivado con el `tools/marcador_segmento.py` de ese commit sobre un `git archive` del árbol (determinista: dos derivaciones idénticas, sha `66a2adff…`). Hallazgo lateral: además del módulo, `milpa/tramite-ola5-propuesta-v0.yaml` también cambió desde el sello (sha HEAD `f19f2c51…` ≠ `93dfa3f9…` declarado); los otros cuatro insumos de 0001 COINCIDEN. Mesa ratifica o corrige (NC `…-fa42-02`, FP `…-fa42-01`).
- **P2 · ejecución previa (E.5).** Antes del COMMIT-1 el medidor de 0002 corrió una vez como prueba de humo e imprimió su línea de resumen (`53 / 53 / PERSISTE 22 / CAMBIA 31`); declarada en la spec antes de congelar. Procedimiento determinista; ése es el resultado que selló `run`.
- **P1 · ENCIG 2025.** `canon/MEMORIA-OPERATIVA.md` §1 dice «ENCIG 2025: abierta», pero el PARO (a) del encargo veda abrirla fuera de lo que abrió su árbitro (la rejilla de gobierno digital, no la sección XI): P1 usa 2023, tal como el encargo prevé.
- **P1 · tamaño de localidad: NO-CONSTRUIBLE** por texto (A.15): ninguna variable de tamaño en el descriptor (seis tablas) ni en el cuestionario; la encuesta sólo cubre ciudades de 100 mil habitantes y más. `AREAM` y `EST` no se sustituyen (NC `…-fa42-01`).
- **P3 · 3(a).** La opción firmada decía «añadir `reserva_respondentes` a `RAICES_ESCANEABLES` y a `raices.local.yaml`»; el encargo la tradujo como «verificar por comando los cuatro archivos». Se hizo lo que el encargo pide (script propio, estados A.1, salida cruda); el cambio de código en `tests/manifiesto.py:358` no se hizo (fuera del perímetro §9) y queda para mesa (NC `…-fa42-03`, FP `…-fa42-02`).
- **P4 · nombres.** El protocolo §2 nombra `recalculo.py/.tsv` y `ambiguedades.md`; por T02 pasaron a `recalculo-<calc>.*` y `ambiguedades-<calc>.md` con `git mv` después del dictamen. El orden de commits (números antes de apertura) no cambia: `fd54ddbd` precede a `5b257360`.

## 2 · P3 — lo esencial de la salida cruda

```
mociba_2021_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (847961 bytes)
mociba_2022_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1044877 bytes)
  (control, manifiesto de fa42a3c1: AUSENTE 2/2 -- ruta forense/produccion/... no está en data_raw)
enco_2025_junio_dbf_reservado · enco_2026_junio_dbf_reservado · enco_fd_v5_reservado · enco_manual_procedimientos_reservado
  manifiesto.py --verifica:                 FUERA_DE_PERIMETRO 4/4
  p3_verifica_enco.py (sin raíz):           RAIZ-NO-CONFIGURADA 4/4 · archivos_examinados=0
  p3_verifica_enco.py /home/pc0/mm-corpus/reservas-respondentes: COINCIDE 4/4 · archivos_examinados=4
```

## 3 · P4 — dictamen (RETROSPECTIVA-MECÁNICA; tolerancia fijada en `protocolo-recalculo-v1_0.md` §3 antes de recalcular)

| CALC sellado | adenda | llaves | cumplen | dictamen |
|---|---|---|---|---|
| `CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001` | `…-DISCRIMINACION-spec-v2_0.md` | 23 | 23 | **PASA** |
| `CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001` | `…-NOFISICA-BC-spec-v2_0.md` | 8 | 8 | **PASA** |
| `CALC-ENDIREH-PISOS-2021-AYUDA-0001` | `…-AYUDA-spec-v2_0.md` | 1 | 1 | **PASA** |

32/32: estado y `n` idénticos, `|Δ punto|` máximo 0.0, y el IC coincide además a `1e-10` en las 32 (no se exigía). Detalle: `forense/validacion-independiente/pisos-y-adendas-1/{comparacion,dictamen}.tsv`. El recalculador anotó ambigüedades menores (`ambiguedades-<calc>.md`), ninguna con efecto en el número. La identidad corregida de `#115` es «No sabía que existían leyes para sancionar la violencia» (FD p. 632). Specs selladas, medidores y RESULT de los tres CALC: intactos. Cierra `NC-…-beee-02` y `NC-…-beee-03`.

## 4 · P1 — pisos de confianza institucional, ENCIG 2023 (RETROSPECTIVA; persona 18+; ciudades de 100 mil y más)

Marco: 38 966 personas (sección XI), 0 sin enlace a residentes, 8 928 UPM, 347 estratos; `N-OTRO` = 0 en los 25 reactivos; 185 personas sin categoría de edad (98/99). «Mucha o algo de confianza» entre quienes respondieron 1–4; escala de 4 puntos de ENCIG, sin enlace con otras escalas. Entidad: mínimo y máximo de las 32 (clave INEGI). Todos los valores son RESULT del CALC (consulta con `tools/consulta.py result <id>`).

| id | reactivo | % nacional [IC95] | N | entidad mín – máx | escolaridad NINGUNA / BÁSICA / MEDIA-SUP / SUPERIOR | NS/NR |
|---|---|---|---|---|---|---|
| I01 | Universidades públicas | 86.6 [86.0, 87.1] | 34598 | 72.7 (20) – 91.7 (03) | 79.7 / 83.4 / 87.8 / 89.1 | 3669 |
| I02 | Policías | 37.3 [36.6, 38.1] | 38548 | 25.1 (02) – 60.9 (31) | 35.8 / 37.9 / 38.2 / 36.1 | 383 |
| I03 | Hospitales públicos | 71.2 [70.4, 72.0] | 37937 | 63.8 (08) – 77.1 (03) | 72.9 / 72.7 / 72.7 / 68.2 | 918 |
| I04 | Presidencia y Secretarías | 60.7 [59.9, 61.5] | 37778 | 50.6 (16) – 78.5 (12) | 73.4 / 68.1 / 61.4 / 51.2 | 1149 |
| I05 | Empresarios(as) | 51.9 [51.0, 52.8] | 34990 | 43.2 (09) – 64.4 (06) | 45.3 / 49.6 / 50.7 / 55.4 | 3760 |
| I06 | Gubernatura / Jefatura CDMX | 50.0 [49.2, 50.9] | 37492 | 36.3 (17) – 65.1 (28) | 55.0 / 53.5 / 50.3 / 45.9 | 1431 |
| I07 | Compañeros(as) del trabajo | 81.1 [80.3, 81.9] | 24274 | 75.0 (08) – 86.4 (02) | 72.5 / 75.7 / 80.2 / 86.6 | 1981 |
| I08 | Presidencias municipales / Alcaldías | 51.7 [50.9, 52.5] | 37513 | 41.2 (07) – 66.8 (28) | 54.4 / 53.8 / 53.0 / 48.2 | 1385 |
| I09 | Parientes | 88.3 [87.9, 88.8] | 38399 | 80.7 (29) – 91.5 (15) | 86.3 / 85.1 / 89.1 / 91.5 | 463 |
| I10 | Sindicatos | 44.8 [43.9, 45.6] | 32588 | 32.8 (20) – 59.1 (12) | 40.3 / 44.2 / 47.0 / 43.9 | 5289 |
| I11 | Vecinos(as) | 73.2 [72.5, 73.9] | 37722 | 67.8 (29) – 80.8 (03) | 69.2 / 70.6 / 72.6 / 76.8 | 1145 |
| I12 | Cámaras de Diputados y Senadores | 37.4 [36.5, 38.2] | 35654 | 27.8 (09) – 52.9 (12) | 42.6 / 40.3 / 38.7 / 33.1 | 3155 |
| I13 | Medios de comunicación | 50.7 [49.9, 51.6] | 37643 | 43.9 (09) – 63.2 (12) | 62.7 / 55.7 / 51.5 / 44.1 | 1293 |
| I14 | Institutos electorales | 56.6 [55.7, 57.5] | 37437 | 44.9 (07) – 69.1 (12) | 53.8 / 57.1 / 56.7 / 56.2 | 1503 |
| I15 | Comisiones de derechos humanos | 64.6 [63.8, 65.4] | 35765 | 54.6 (07) – 75.3 (05) | 64.3 / 64.7 / 65.4 / 63.9 | 3110 |
| I16 | Escuelas públicas de nivel básico | 82.8 [82.1, 83.4] | 36173 | 76.1 (27) – 88.1 (02) | 80.5 / 83.0 / 83.6 / 82.1 | 2203 |
| I17 | Jueces y Magistrados | 42.9 [42.1, 43.8] | 35557 | 31.2 (02) – 57.9 (18) | 44.8 / 41.9 / 43.6 / 43.3 | 3302 |
| I18 | Instituciones religiosas | 63.4 [62.6, 64.2] | 37290 | 51.5 (09) – 76.4 (12) | 75.1 / 68.5 / 62.5 / 57.5 | 1534 |
| I19 | Partidos políticos | 29.8 [29.0, 30.5] | 37623 | 21.7 (02) – 45.6 (12) | 38.8 / 33.3 / 31.0 / 24.3 | 1293 |
| I20 | Guardia Nacional | 68.3 [67.5, 69.0] | 37305 | 52.3 (11) – 79.2 (18) | 70.8 / 71.3 / 71.1 / 62.8 | 1628 |
| I21 | Ejército y Marina | 74.1 [73.4, 74.8] | 37489 | 60.7 (11) – 83.2 (18) | 76.0 / 76.1 / 76.3 / 70.1 | 1448 |
| I22 | Ministerio Público / Fiscalía Estatal | 40.6 [39.8, 41.4] | 36862 | 27.5 (09) – 58.2 (31) | 43.7 / 42.7 / 42.9 / 36.5 | 2042 |
| I23 | Servidores(as) públicos(as) | 51.3 [50.6, 52.2] | 37845 | 42.5 (09) – 65.3 (12) | 57.0 / 51.7 / 52.5 / 49.7 | 1101 |
| I24 | Organizaciones de la Sociedad Civil | 67.5 [66.7, 68.3] | 34959 | 51.9 (07) – 81.0 (05) | 62.6 / 65.7 / 68.2 / 68.9 | 3845 |
| I25 | Organismos Públicos Autónomos | 72.6 [71.8, 73.3] | 36024 | 65.1 (20) – 83.1 (18) | 69.7 / 71.6 / 72.8 / 73.7 | 2871 |

Soporte: `N` de escolaridad NINGUNA = 627 en I01 (la celda más chica de ese eje); `N` mínimo por entidad = 286 (sobre las 800 celdas de entidad); IC más ancho 16.3 pp (I07 × NINGUNA). I07 tiene 12 711 «No aplica» (no trabajan): su `N` es la población ocupada, no el marco.

**Lectura, rotulada.** Descriptivo, sin causa: la confianza más alta está en redes cercanas y en servicios de contacto directo (parientes, universidades y escuelas públicas, compañeros de trabajo) y la más baja en partidos, policías, Congreso y Ministerio Público. En Presidencia, partidos, medios e instituciones religiosas la confianza baja con la escolaridad; en universidades, empresarios, vecinos y compañeros de trabajo sube. Son marginales: no dicen por qué.

## 5 · P2 — `CALC-PISO-PERSISTENCIA-ERROR-0002` contra 0001 (RETROSPECTIVA-MECÁNICA)

`p2_compara_0001.py` → `p2-comparacion-0001-0002.tsv`: `ids_0001 = 317 · ids_0002 = 317 · difieren = 0 · max |Δ| = 4.44e-16` → **REPRODUCE** (tolerancia `abs 1e-10` de la spec v1.0). Punto e IC de cada celda y de cada agregado son los de 0001: el sucesor cambió el input, no el número. 0001 queda como evidencia histórica, intacto (E.3); 0002 declara `repite_de` en la raíz y cierra `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-03`. Lo que 0002 **no** es: una medición del marcador de hoy (§1.1).

## 6 · Auditoría (P1 y P2 afirman sobre México)

- **Contadores:** +2 CALC en `cuenta_gen2` (sellados en disco, no registrados); cero adopciones; `celdas_validadas` Δ0.
- **Unidad y escala:** P1, persona 18+, proporción en la escala de 4 puntos de ENCIG; no se compara con LAPOP 1–7, WVS 1–4 ni ENBIARE 0–10 sin enlace. P2, la unidad del piso y la del R de cada celda (persona, trámite o delito según instrumento), declarada por celda; nunca se promedia entre instrumentos.
- **PROSPECTIVA / RETROSPECTIVA:** todo RETROSPECTIVO (P1) o RETROSPECTIVA-MECÁNICA (P2, P4); ninguna cifra es PROSPECTIVA.
- **¿Qué parece psicológico y es incentivo o exposición?** La variación por entidad en policías (25 % a 61 %), Guardia Nacional o Ejército refleja primero exposición y desempeño —victimización, despliegue, trato en trámites—, no una «actitud regional». El gradiente por escolaridad hacia Presidencia o partidos puede ser información, empleo formal o alineamiento político, no «cultura».
- **Sobregeneralización:** universo sólo urbano de 100 mil habitantes y más; nada describe al México rural, indígena o de localidades pequeñas (y por eso el eje de localidad es NO-CONSTRUIBLE). Procedencia: (a) datos primarios en México (INEGI); nada es (b) ni (c).
- **Lectura simplista peligrosa:** «los mexicanos no confían en la policía» — es una marginal urbana de 2023 con una dispersión entre entidades de 36 pp; no es un rasgo.
- **Cifra escrita a mano:** ninguna; toda cifra de esta nota sale de un RESULT sellado, de un TSV de esta carpeta o de una salida cruda citada.

## 7 · Firmas asentadas (A.12) y NC

FIRMADA por este acto al ejecutarlas: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-21` (F3), `…-f2e5-22` (F4), `…-f2e5-27` (H4). NC cerradas: `NC-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-02` (P3), `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-03` (P2), `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-02` (P1), `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-02` y `-beee-03` (P4). NC nuevas `NC-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01…04` y FP nuevas `FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01…02`: ver `## NO-CORRIDO / RESERVAS` del encargo.
