# Nota de cierre · ACTO GEN2-RELEVO-MOTOR-34-1

24/sep/2026 · encargo `forense/encargos/2026-09-24-GEN2-RELEVO-MOTOR-34-1.md`
(SHA de redacción `8358b891`, sello de cuerpo `b7ecc775…` = sha del adjunto) ·
ADR `ADR-260924-GEN2-RELEVO-MOTOR-34-1-a157-01` · 0-bis `a157ae3c`.

**Contadores movidos: dos** — `legacy_activas_por_consumidor__motor` 34 → 25 y
`N_resultados_gen2_adoptados_activos` 72 → 81, los dos en árbol re-derivado
(§3) y los dos sujetos a merge de mesa (E.2). El «Hecho» del encargo se
cumple por su segunda rama: residuo 25 con una NC por lectura.

## 1 · Arranque

- Repo `/home/user/Modelado-Mexicano`, `HEAD = 8358b891` = SHA de redacción;
  `git rev-list --count HEAD..origin/main` → 0; árbol limpio.
- Duplicado (0.c): `git ls-remote --heads origin | grep -i relevo` → 0;
  `git worktree list` → 1 (el propio); `search_pull_requests "RELEVO is:open"` → 0.
- Rama: `claude/new-session-y5cznd`, la que fijó la plataforma (el encargo
  sugiere `acto/gen2-relevo-motor-34-1` «o la que fije la plataforma; se declara»).
- Entorno (hook `SessionStart`, crudo): `ENTORNO-DERIVADO = NUBE` ·
  `senal-corpus: montado=NO archivos_examinados=0` ·
  `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` ·
  `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403)`. El encargo
  declara NUBE: coinciden. Ninguna pieza de este acto abrió microdato; las que
  lo exigen van a NC con sucesor en CAJA (§4). `data/raw` ausente: creada vacía.
- COMPUERTA: ninguna (sin línea `GATED a` ni `COMPUERTA:`). MODO: el encargo
  dice «AUTÓNOMO», fuera del vocabulario ABIERTO/RÍGIDO de D-18; se trató como
  ABIERTO (no congela ni ejecuta spec con reserva) con la cláusula de autonomía
  v1.0 como latitud.

## 2 · Premisas re-verificadas

| premisa del encargo | rótulo | verificación | resultado |
|---|---|---|---|
| motor 34 / procedencia 40 / catálogo 23 / marco 43 / celdas-D 6 | EJECUTADO | `corrida0.py status` sobre `8358b891` | se sostiene |
| las 34 = «las que responden al usuario» | — | `corrida0.py:4989`: bucket `motor` = `milpa/tramite.yaml` (28) + `milpa/src/` (6, `celdas.py:CORTES_C1`) | se sostiene con matiz: 6 son cortes categóricos, no probabilidades |
| «la mayoría de las 34 tienen RESULT GEN2 por conducta» | SUPUESTO | `relevo_usos.py --json`: 13 SIN-CANDIDATO, 8 NO-ADOPTABLE-POR-VEREDICTO-SELLADO, 7 LISTADO-PARA-MESA, 1 VETADO, + 6 cortes SIN-CANDIDATO | **no se sostiene**: 9 de 34 tenían un camino GEN2 legítimo, 5 de ellos solo tras crear un derivado |
| CATALOGO-1 fusionó (#1115) | LEÍDO | fuera del perímetro de este acto (catálogo es de RELEVO-CONSUMIDORES-2) | no se usó |
| pines existentes: vías i 14 / ii 13 / iii 1 | EJECUTADO | `status`: i 14 · ii 13 · iii 0 (el pin iii de RES-0028 queda `PIN-SOBRE-CONSUMIDOR-YA-MARCADO`) | ninguno firmado quedaba sin aplicar sobre el motor |

Premisa de logística que cayó y cómo se replanteó: para `milpa/tramite.yaml`
la salida natural de legacy **no es un pin** — `corrida0.py:4485-4524` aplica
un pin solo a consumidores que no declaran `corrida0_generacion`; el motor sí
puede declararla. La vía es el escritor con las mismas cuatro guardas de 4.1
(+D6: eje RESULTADO), que V3 importa de `tools/pines_mesa.py` sin copiarlas.
No se escribió ninguna fila nueva en `pines-de-mesa.tsv`.

## 3 · Tabla final «34 → vía → estado» (P4)

Derivada por `python3 forense/analisis/relevo-motor/inventario_motor34.py` →
`forense/analisis/relevo-motor/inventario-34-v1_0.tsv` (universo: usos activos
LEGACY-GEN1 del bucket `motor` en `origin/main`).

| lecturas | vía | CALC / RESULT | estado |
|---|---|---|---|
| RES-0039/0040/0041/0042 (denuncia con/sin seguro) | (i) crudo | `CALC-ENVIPE-DENUNCIA-SEGURO-0001` · `RESULT-ENVIPE-SEG-{CON,SIN}-P-{DENUNCIA,NO-DENUNCIA}` | RELEVADAS; `p` pasa al RESULT a 6 decimales (0.790900→0.790906, 0.209100→0.209094, 0.672000→0.672014, 0.328000→0.327986) |
| RES-0004/0014/0016/0022 (complementos ENCIG) | (iii) derivado | `CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001` (nuevo) · `RESULT-ENCIGDER-{A,B-PRE-SD,B-DIG-SD,C}-Q` | RELEVADAS; `p` sin cambio (\|q−legacy\| ≤ 4.5e-7) |
| RES-0006 (complemento ENCUCI) | (iii) derivado | `CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001` (nuevo) · `RESULT-ENCUCIDER-A-Q` | RELEVADA; `p` sin cambio (delta 3.9e-7) |
| 8 ASIGNADO con hermano GEN2 (0001/0002/0007/0008/0019/0020/0023/0024) | — | — | NC `a157-01..`; DECISIÓN-DE-MESA-PENDIENTE; FP `a157-01` |
| 2 ASIGNADO sin medición GEN2 (0017/0018) | — | — | NC; DIFERIDO-A CAJA |
| 4 NO-ADOPTAR-NC-0107 (0009–0012) | — | — | NC; DECISIÓN-DE-MESA-PENDIENTE; FP `a157-02` |
| 2 ENNViH/MxFLS (0029/0030) | — | — | NC; DIFERIDO-A CAJA (payloads `ennvih2_2005_*`, `ennvih3_2009_*` en el manifiesto) |
| 3 L8 (0050–0052) | — | `CALC-L8-CONVERSION-0001` reproduce pero **ingiere** un JSON GEN1 | NC; DIFERIDO-A CAJA (4.1: ingerir GEN1 no cuenta nunca) |
| 6 cortes `CORTES_C1` (0165–0170) | — | — | NC; DECISIÓN-DE-MESA-PENDIENTE; FP `a157-03` |

`status`, crudo, antes (`origin/main`, worktree temporal) y después (árbol con
este diff y la vista re-derivada con `registro --escribe --lote <los dos CALC>`,
descartada después: la publica el canal `[deriva]` de CI desde los asientos):
`forense/analisis/relevo-motor/status-antes.txt` y `status-despues.txt`.
Después: `legacy_activas_por_consumidor__motor=25`,
`dependencias_numericas_legacy_activas=137`,
`N_resultados_gen2_adoptados_activos=81`; procedencia 40, catálogo 23,
marco 43, celdas-D 6 sin cambio.

## 4 · Por qué el residuo no se relevó (lo que mesa decide)

1. **ASIGNADO con hermano medido (8).** `tramite.yaml:65-67` dice que
   `emitir_binaria` sigue devolviendo el par ASIGNADO para `paga_mordida` /
   `tramite_normal`. Sustituir su `p` por el hermano medido cambia el estimando
   (discrecional: 0.62 asignado frente a 0.085118 de *solicitud* medida,
   `SEMANTICA D4, NC-0113`): no es relevo, es otra respuesta del motor. §4 de
   las instrucciones: un estimando restringido no se compara con uno
   poblacional sin recalcularlo al mismo universo. FP `a157-01`.
2. **NO-ADOPTAR-NC-0107 (4).** El propio motor las rotula «conservar sólo
   como historia», y el registro las tiene NO-ADOPTABLE por veredicto sellado.
   Quitarlas del consumo vivo es una decisión sobre el motor. FP `a157-02`.
3. **Cortes (6).** `CORTES_C1` es dato sellado (edición autorizada solo bajo
   ADR-100(2)); ni hay RESULT numérico que los releve ni este acto puede
   sacar `corte_pi` del contador (sería mover un contador a mano, PARO c).
   FP `a157-03`.
4. **CAJA (7: 0017/0018, 0029/0030, 0050–0052).** Exigen CALC nuevo desde
   microdato con COMMIT-1 de códigos resueltos desde codebook (E.5). La
   sesión es NUBE sin corpus; abrir un entorno hermano no estaba disponible
   aquí. Sucesor `GEN2-RELEVO-MOTOR-34-2-CAJA`.

## 5 · Qué se hizo y dónde

- **COMMIT-1** `413bc8d7`: specs + medidor + prueba sintética de los dos CALC
  derivados, antes de cualquier corrida. **COMMIT-2** `729fadd5`, `6eab41b4`:
  corridas selladas; `verify` → `REPRODUCE · IDENTICO` las dos (salida cruda
  en `forense/analisis/relevo-motor/verify-*.txt`); asientos en
  `forense/replay-evidencia.tsv` (E.7). La vista la publica CI
  (`verify.yml:443-451`, `lote_desde_asientos.py` los recoge — verificado).
- **Escritor V3** (`tools/escribe_relevo_consumo.py --relevo-motor-34`):
  `RELEVOS_V3` liga cada conducta a un RESULT; `guardas_v3` = sello que
  cubre los bytes + estado SELLADA + `cuenta_gen2=SI` + replay afirmativo en
  RESULTADO; vía (i) exige crudo sin ingestión y el mismo payload del
  manifiesto en la regla y en el CALC; vía (iii) usa
  `pines_mesa._valida_derivado` (padre único, sellado, que cuenta, replay
  afirmativo, que no ingiere) y exige que la spec del derivado declare ese
  consumidor. Vía (iii) no puede cambiar `p`. Autoverifica cargando con
  `milpa.src.emisor.cargar_reglas`. Diff seco:
  `forense/analisis/relevo-motor/diff-seco-escritor-v3.txt` (= diff aplicado,
  salvo etiquetas de hunk). `milpa/tramite.yaml` sin edición manual.
- **Tests:** `tests/test_escribe_relevo_motor34.py` (una prueba por llave,
  9, + 8 de guardas) y `tests/test_relevo_motor34_derivados.py` (24
  sintéticas: todas las ramas terminales del medidor, sin `None` ni `NaN`
  emitidos, rechazo de sello, spec_id, veredicto, método, límites). 41/41.
- **Motor carga y emite:** los tests de `tests/test_emisor_*` y
  `tests/test_motor_*` dan 26 pasan / 3 fallan **idénticos antes y después**
  del diff (comparado por nombre con `git stash`); ver hallazgos.

## 6 · Hallazgos (una línea cada uno, a `forense/hallazgos.md`)

- 3 tests de motor fallan en `main` sin este acto y no están en CI:
  `test_emisor_fidelidad::test_tramite_cinco_reglas_diez_probabilidades`,
  `test_motor_gen2_explicito::test_01_…`, `::test_08_…`.
- `tramite_normal_encig2025` y `rechaza_servicio_encig2025_luz` llevan
  `clase: "MEDIDO·…"` aunque son complementos `1−p`; el comentario de la
  primera ya lo decía (DERIVADO-NO-MEDIDO). No se tocó la clase.
- `civico.denuncia.{con,sin}_seguro` conservan `ic95`/`n` GEN1 a nivel de regla
  (IC [0.752301, 0.827811] frente a [0.749985, 0.831673] del RESULT).
- El relevo por marca del consumidor funde la clase (iii) en el conteo
  general: `relevadas_por_pin_de_mesa__iii` sigue en 0 aunque seis lecturas
  del motor (RES-0028 y las cinco de aquí) salen por derivado. 4.1 pide «las
  clases sin fundirlas».
- `corrida0 spec-check` da FAIL de inventario en todo CALC derivado (también
  en el precedente sellado RES-0028): no aplica a insumos `origen: repo`.
- `registro --escribe` local escribe un `resultados.tsv` con un campo > 10 MB
  que `relevo_usos.py` ya no puede leer (límite de `csv`), coherente con el
  hallazgo de VISTA-NORMALIZADA-3.

## 7 · Módulo de auditoría (§5)

- ¿Cuántos contadores movió? Dos (arriba). ¿Qué cifra es PROSPECTIVA y cuál
  RETROSPECTIVA? Ninguna de las nueve es marcador: son relevos de
  procedencia; no se mezclan en ninguna frase de producto.
- ¿Escala y unidad? Todas proporciones `[0,1]`; ENVIPE en unidad **delito**
  (FAC_DEL), ENCIG A en usuario, B en trámite por canal, C en trámite
  N_TRA=01, ENCUCI en persona con contacto. No se promedian entre sí.
- ¿Algo escrito a mano y no derivado? El mapa `RESIDUO` de `inventario_motor34.py`
  (la razón por lectura) es juicio del ejecutor, rotulado; los conteos se
  derivan.
- ¿Desigualdad/violencia confundidas con cultura? Las cifras de denuncia
  describen conducta ante robo de vehículo con/sin seguro (incentivo del
  trámite del seguro), no un rasgo cultural; el relevo no cambia esa lectura.
