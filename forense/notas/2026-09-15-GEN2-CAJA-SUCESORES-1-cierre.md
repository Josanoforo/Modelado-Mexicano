# ACTO GEN2-CAJA-SUCESORES-1 · lo que RELEVO y FIRMAS no pudieron cerrar sin corpus — nota de cierre

**Acto:** `ACTO GEN2-CAJA-SUCESORES-1`, 15/sep/2026, CAJA (Ubuntu/WSL2;
`data/raw` montado vía symlink a `/home/pc0/mm-corpus/raw`,
`numpy`/`pandas`/`scipy`/`pyreadstat` presentes — verificado con
`python3 tools/entorno.py`).
**Base observada al arrancar:** `origin/main = 0cdbd72` (merge de `PR #789`,
`ACTO GEN2-MEDICION-DEMANDA-2`).
**Encargo archivado verbatim (0-bis A.3):**
`forense/encargos/2026-09-15-GEN2-CAJA-SUCESORES-1.md`.

Cuatro piezas nombradas por número de `NC`, cada una una pieza que quedó
`NUBE`-bloqueada por falta de corpus o de perímetro. Ninguna mide ciencia
nueva; todas son cableado, verificación contra corpus real, o corrección de
un verificador.

## P1 · NC-0211 — `corrida0 registro --verifica --escribe`

`python3 tools/corrida0.py registro --verifica --fuentes` (sin `--escribe`)
corrido dos veces en seco para separar señal de ruido: la primera pasada
proyectó `NO-REPRODUCE · CONTEXTO-DISTINTO` para `CALC-M-marco-M-sorteado-v1_3`
(la inestabilidad ya conocida y cerrada por `NC-0182`, ver
`forense/hallazgos.md` 2026-09-14 ×3); `verify` aislado de ese mismo CALC,
corrido dos veces, dio `REPLICA-RESULTADO · CONTEXTO-DISTINTO` estable en las
dos (las 33 `RESULT` reproducen exacto); una segunda pasada en seco del lote
completo dio diff vacío. Con eso, `--escribe` no necesitó `--lote`: escribió
las tres vistas (`corridas.tsv` 186 filas, `resultados.tsv` 5 239,
`usos.tsv` 207) **byte-idénticas** a lo ya commiteado — confirma, no
corrige. Esto es exactamente lo que `NC-0211` pedía: las 17 corridas
publicadas ajenas que `NUBE` no pudo re-verificar (`numpy`/`pandas`/`scipy`
ausentes allí) genuinamente `REPRODUCE`/`IDENTICO` contra el corpus real de
esta caja. **CERRADA.**

## P2 · NC-0215 — declarar el pin por CALC (11 slots `LISTADO-PARA-MESA`)

Las seis `CALC` que `RELEVO-USOS-1` encontró selladas
(`CALC-ENIGH-0001`, `CALC-ENFIH-0001`, `CALC-EDER-0003`, `CALC-ENUT-0001`,
`CALC-L8-CONVERSION-0001`, `CALC-ENSANUT-0001`) ya traen, cada una, un par
`RESULT-*-DELTA-VS-GEN1` / `RESULT-*-REPRODUCE-GEN1` **sellado y calculado
contra la cifra GEN1 de referencia** — el delta ya está hecho, sólo faltaba
el pin (`RES-#### -> RESULT-id`). No se editó ningún `spec.yaml` sellado
(E.3): el pin se declara aquí, por lectura y cita verbatim de la `unidad` de
cada `RESULT` en su `spec.yaml`, sin inferir por parecido.

| slot | CALC | RESULT pin | delta vs GEN1 | veredicto |
|---|---|---|---|---|
| RES-0036 (no_recibe_remesas) | CALC-ENIGH-0001 | RESULT-ENIGH-A-P-COMPLEMENTO | 9.96e-08 | REPRODUCE |
| RES-0037 (tiene_afore) | CALC-ENFIH-0001 | RESULT-ENFIH-A-P | 2.87e-07 | REPRODUCE |
| RES-0038 (no_tiene_afore) | CALC-ENFIH-0001 | RESULT-ENFIH-A-P-COMPLEMENTO | 2.87e-07 | REPRODUCE |
| RES-0043 (union_libre) | CALC-EDER-0003 | RESULT-EDER-UNION-A-P-LIBRE | `NO-APLICA-ESTIMANDO-DISTINTO` | **NO COMPARABLE** |
| RES-0044 (matrimonio_directo) | CALC-EDER-0003 | RESULT-EDER-UNION-A-P-DIRECTO | `NO-APLICA-ESTIMANDO-DISTINTO` | **NO COMPARABLE** |
| RES-0045 (share_horas_mujeres_40mas) | CALC-ENUT-0001 | RESULT-ENUT-A-R | -1.85e-05 | REPRODUCE |
| RES-0050 (participa_p0_minimo) | CALC-L8-CONVERSION-0001 | RESULT-L8CONV-A-P-MINIMO | 0.0 | REPRODUCE |
| RES-0051 (participa_p0_maximo) | CALC-L8-CONVERSION-0001 | RESULT-L8CONV-A-P-MAXIMO | 0.0 | REPRODUCE |
| RES-0052 (participa_p0_media) | CALC-L8-CONVERSION-0001 | RESULT-L8CONV-A-P-MEDIA | 0.0 | REPRODUCE |
| RES-0063 (razon_no_vacunacion_logistica) | CALC-ENSANUT-0001 | RESULT-ENSANUT-A-P-LOGISTICA | -3.59e-07 | REPRODUCE (verificado contra corpus real en P3, ver abajo) |
| RES-0064 (razon_no_vacunacion_no_logistica) | CALC-ENSANUT-0001 | RESULT-ENSANUT-A-P-NO-LOGISTICA | -3.59e-07 | REPRODUCE (ídem) |

**9 de 11 son `REPRODUCE`** con delta ≈0 (`NO-MATERIAL` por cualquier
umbral razonable — el propio `A-REPRODUCE-GEN1` sellado de cada CALC ya lo
certifica). Bajo la regla de bloque de `RELEVO-USOS-1` («los NO-MATERIALES
entran en bloque»), estos 9 son candidatos limpios de adopción en bloque —
pero **este acto no adopta**: el encargo lo excluye del perímetro
(«no toca milpa ni cola»). Queda para el sucesor `NC-0243`.

**2 de 11 (RES-0043/0044, `CALC-EDER-0003`) NO son comparables.** El propio
CALC lo declara: `RESULT-EDER-UNION-A-DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-
DISTINTO -- GEN1 mide ENADID 2023 (situacion conyugal actual), esta corrida
mide EDER 2017 (tipo de primera union)`. Confirmado contra `milpa/tramite.
yaml:1031-1046`: el `p` de GEN1 (0.190500/0.809500) está etiquetado
`MEDIDO·p(...; ENADID 2023, p3_27_ag)` — un instrumento y una pregunta
distintos de lo que `CALC-EDER-0003` mide (cohortes de primera unión,
EDER 2017). `milpa/tramite.yaml` ya cita EDER2017 como eje de
**corroboración** (`segmentacion_ejes_eder2017_enadid2023.eje_cohorte_
eder2017`, veredicto `CORROBORADA`) — no como reemplazo del `p` primario —
y las cuatro celdas por cohorte que `RESULT-EDER-UNION-B-COHORTE-P-LIBRE`
sella coinciden dígito a dígito con las ya citadas
(`1961-1970`: 0.304657 en ambos lados). **No hay pin que declarar aquí que
no sea, de hecho, lo que `milpa/` ya tiene como eje secundario.** Se rotula,
no se calla.

(Rótulo consistente: los sucesores de este párrafo — adopción en bloque de
los 9 `REPRODUCE` y disposición de mesa sobre los 2 `NO-COMPARABLE` — van
al mismo `NC-0243`, no a filas separadas, porque son la misma acción de
sucesor: escribir/decidir sobre `milpa/`.)

**Hallazgo nuevo, no pedido por este encargo:** `RES-0047`/`RES-0049` — YA
ADOPTADOS por `RELEVO-USOS-1` P4 citando `CALC-ENIF-0001` — salen ahora
`CONFLICTO-ENTRE-CANALES` en la re-derivación: `CALC-HORIZONTE-VIA-
DERIVADOS-0001-v1_1` (sellada por `MEDICION-DEMANDA-1`, posterior a la
adopción) declara, por `C2-RESULTADO`, el mismo relevo para los mismos dos
slots. Las cifras **no discrepan** (`RESULT-HVD-A-HORIZONTE-NO-CORTO-SIN-SS`
= 0.458657, `RESULT-HVD-A-HORIZONTE-NO-CORTO-CON-SS` = 0.62687 — idénticas a
las ya adoptadas), así que la cita vigente en `milpa/tramite.yaml` no está
mal. Es un conflicto de **procedencia** (dos CALC independientes se
adjudican el mismo relevo), y el propio registro dice que la decisión es de
mesa, no de este canal. Sucesor: `NC-0244`.

`tools/relevo_usos.py --escribe` corrido (sin tocar `spec.yaml` de ningún
CALC): `data/corrida0/relevo-usos-v1_0.tsv` refleja el árbol post-`#789`
(`GEN2-MEDICION-DEMANDA-2`), que añadió 4 slots `LISTADO-PARA-MESA` más
(`RES-0039..0042`, `CALC-ENVIPE-DENUNCIA-SEGURO-0001`/`CALC-EVASION-NORMA-
0001(-v1_1)`) — fuera del alcance de los seis CALC de este encargo, se
declaran y no se tocan.

No se corrió `corrida0 delta` con un contrato nuevo: el delta que ese
comando calcularía **ya está sellado dentro de cada CALC**
(`RESULT-*-DELTA-VS-GEN1`), recomputarlo por fuera sería redundante y, peor,
exigiría teclear un contrato a mano — exactamente lo que
`tools/relevo_usos.py --contrato` existe para evitar. La cita del delta
sellado (tabla de arriba) cumple el mismo objeto con más rigor (es el
propio CALC verificándose contra GEN1, no una segunda vía externa).

**CERRADA** (el pin queda declarado y evidenciado). Sucesores: `NC-0243`
(adopción en bloque de los 9 `REPRODUCE`) y `NC-0244` (conflicto de
procedencia RES-0047/0049).

## P3 · NC-0169 — ENSANUT L17, emisión contra corpus real

El payload real (`adultos_ensanut2024_w.stata.stata.zip`, único miembro que
`CORR-0017` usa — la Rama C/adolescentes no tiene `RESULT` en este `CORR`)
está espejado en `/home/pc0/mm-corpus/descargas_mx_espejo/ENSANUT2024-
v2026-09-01/`, `sha256` coincide con `data/manifiesto.yaml`. El script viejo
citado por `NC-0169` (`tools/medidor_l17_vacunacion_disponible.py`) no
expone la interfaz `medir(inputs, contrato)` que `corrida0` exige — es un
script de una sola pieza, anterior al registro. `CALC-ENSANUT-0001`
(escrito y sellado por `ACTO GEN2-MEDICION-DEMANDA-1`, 15/sep/2026, sobre la
Rama B de la misma spec `prereg-caja-S7-L17`) **es** la pieza ejecutable
para este `CORR`, y hasta ahora **sólo se había probado contra payload
sintético**.

```
python3 tools/corrida0.py verify CALC-ENSANUT-0001
...
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)
```

Las 28 `RESULT` reproducen exacto contra el corpus real: `A-P-LOGISTICA` =
0.7777616409222661 (delta −3.59e-07 vs el `p=0.777762` sellado en `milpa/`),
`A-P-NO-LOGISTICA` = 0.22223835907773398, `A-REPRODUCE-GEN1 = REPRODUCE`,
universo idéntico al de GEN1 (254 menciones, 179 personas, mismo desglose
por razón). **Esto es la emisión que `NC-0169` declaraba pendiente** — «el
registro existe; la emisión no» — ya no aplica: el registro existe y ahora
también corrió contra dato real, no sintético.

Lo que este acto NO hace, por perímetro explícito del encargo («no toca
milpa»): escribir `corrida0_resultado_id`/`corrida0_generacion: GEN2` en
`milpa/tramite.yaml` (hoy ~línea 1406-1407, desplazada desde la 1303-1304
que `NC-0169` citaba). Los dos `RESULT` a citar son exactamente los que P2
pineó arriba (`RESULT-ENSANUT-A-P-LOGISTICA` / `-A-P-NO-LOGISTICA`).
**CERRADA** (la emisión). Sucesor `NC-0243` (la cita en `milpa/`, junto con
el resto del bloque `REPRODUCE` de P2 — mismo acto, mismo perímetro).

## P4 · NC-0208 — verificador F5 bajo el contrato v1.2

`F5-documental-ejecucion-v1_2.md` (`NC-0178`, firmado 15/sep/2026) fija
`sha256_manifiesto_fuentes` a las 8 entradas de `data/manifiesto.yaml` que
el duelo usa (5 de `DIN-M-01`, 3 de `TRA-M-07`), no al archivo entero —
serialización canónica declarada: orden por `id`, `json.dumps(sort_keys=
True, ensure_ascii=False, separators=(',',':'))`, sha256 UTF-8. Validado
ANTES de tocar el runner: reconstruido a mano sobre `git show 582d4e9:data/
manifiesto.yaml`, el algoritmo reproduce exacto el valor que el contrato
registra como «evidencia de redacción»
(`b811a57f3b7cf2a243717b5ca68142783c7da2af80295bbf6c1f402814f488df`).

`tools/f5_documental.py` (fuera de perímetro de `FIRMAS-MESA-1`, dentro del
de este acto): nueva función `sha256_manifiesto_fuentes_v1_2`, reemplaza el
`sha_archivo(MANIFIESTO_FUENTES)` de `materializar()`. `--verify` con el
código viejo mostraba una única diferencia contra la materialización
congelada (el campo `sha256_manifiesto_fuentes`; las 8 fuentes, las tablas,
los documentos y los ancestros ya coincidían byte a byte). `--prepare`
(sin `--authorization-file`, cero solicitudes al proveedor, cero `capturas/`
tocadas) re-escribió `F5-documental-materializacion-v1_0.json` con el valor
nuevo — mismo valor que la reconstrucción manual contra `582d4e9` porque las
8 fuentes del duelo no cambiaron desde entonces, aunque el manifiesto
entero sí (crecimiento ajeno).

```
python3 tools/f5_documental.py --verify
OK: fuentes, paquetes y ancestros reproducen
```

No reabre `TRIADA-0002` ni ningún veredicto (12 `PUNTO` / 10 `ABSTENCION`
intactos, confirmado con `--summary`), no toca `sha256_manifiesto_contexto`,
no gasta ledger (94/96 sin cambio), no reabre la firma
(`F5-documental-firma-v1_0.md` intacta). **CERRADA.**

## Opcional · NC-0202 — reintento del `curl`/`WebFetch`

Esta caja **sí tiene salida a internet** vía `WebFetch` (`curl` directo
desde Bash sigue bloqueado por la política de sandbox de esta sesión,
`exit=7`/connection refused — distinto mecanismo, mismo efecto práctico).
`icpsr.umich.edu` y `rand.org` devuelven `403` (bloqueo de bot a nivel de
sitio, no de red). `ennvih-mxfls.org` **responde con contenido real**:

- `weights2.html`/`weights3.html`: sólo pesos transversales/longitudinales
  descargables (`.zip`), **sin** documentación de diseño/estrato/UPM/pesos
  de réplica — no resuelve `NC-0156` por sí solo.
- `documentation2.html` -> `assets/calculation_weights_mxfls.pdf`
  (extraído localmente con `pypdf`, 11 páginas, 16 483 caracteres): **sí**
  describe el diseño multi-etapa con notación formal — región, estrato
  (`h`), SPU, USM — y la fórmula de probabilidad conjunta de selección de
  la unidad última. Es documentación de diseño **pública, sin necesidad de
  correo**, aunque describe el cálculo del factor de expansión, no
  pesos de réplica per se.

No resuelve `NC-0156` (que sigue `ABIERTA`, sin tocar su fila): es evidencia
nueva para que mesa decida si basta para un IC de diseño construido en casa
en vez de esperar el correo a `support@ennvih-mxfls.org`. Se declara, no se
decide.

## Cascada y contador

`tests/check.py --baseline` y `tools/cierre_acto.py --aplica` corridos al
cierre (ver PR). **Contador: cero mediciones propias** — todo lo de arriba
es verificación contra corpus real, declaración de pin, o corrección de un
verificador; `dependencias_numericas_legacy_activas` (189) y
`N_resultados_gen2_adoptados_activos` (18) no se mueven, como corresponde a
un acto que no adopta.
