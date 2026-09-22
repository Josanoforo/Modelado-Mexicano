# GEN2-PENDIENTES-CAJA-1 · nota de cierre

Encargo: `forense/encargos/2026-09-22-GEN2-PENDIENTES-CAJA-1.md` (0-bis `c09babc9`, sello de cuerpo `648d285d…`).
Base: `origin/main = ccd7c0eb` al abrir (= SHA de redacción); fusionado `02eda845` (#998, #999) antes del cierre.
Entorno: `ENTORNO-DERIVADO = CAJA`, corpus montado (436 archivos examinados), red permitida (`http_code=200`).
Adjunto: `PENDIENTES-PROGRAMA.md`, sha256 `8d02b03e920c74611abdb66b623cd462c1dc5e450fc166646874059bbb5cbe3c` (COINCIDE con el declarado). `GEN2-PENDIENTES-RECONCILIA-1` no había fusionado al abrir (hoy es #1000, abierto): manda §5 tal cual, 49 filas.

**Contadores.** Cero mediciones nuevas. `corrida0 status` antes y después es idéntico (`N_corridas_selladas=154`, `N_resultados_gen2_sellados=44177`): `status` deriva en vivo del disco y ya contaba estas corridas; lo que no está al día es la vista publicada (§1.3). `no_corrido_abiertas` baja 18 y sube 3 (propias). No adopta nada: `usos.tsv` sin diferencia (231 filas).

**Tabla del «Hecho».** `forense/notas/2026-09-22-GEN2-PENDIENTES-CAJA-1-verificacion.tsv`, una fila por ítem (`id · comando · salida_resumida · veredicto · cita · espera_real`):

```
awk -F'\t' 'NR>1{print $4}' <tsv> | sort | uniq -c
     12 DE-MESA
      5 HUMANO
      7 RESUELTO
     11 RESUELTO-ANTES
     14 VIGENTE-CAJA
```

Las 18 `RESUELTO`/`RESUELTO-ANTES` quedan `CERRADA` en `forense/no-corrido.tsv` con `cerrado_por = ACTO GEN2-PENDIENTES-CAJA-1 (…)`. Ninguna `HUMANO` ni `DE-MESA` cambia de estado.

## 1 · P1 · Registro y verificación

### 1.1 Qué faltaba de verdad

Las NC de registro que el inventario daba por pendientes ya estaban hechas: NC-0228, NC-0257 y NC-0284 tienen fila y asiento `REPRODUCE/IDENTICO` desde #866 y #871. El hueco real era otro, **y no estaba en el inventario**. Sobre la vista publicada en `ccd7c0eb`:

- 18 corridas selladas en disco sin fila en `corridas.tsv` (ARBITRO-MARGINALES-2 ×3, ENIGH-DUELO ×3, serie ENIGH 2016/2018/2020 ×9, DIN-CREDITO-PREDICCION-2024 ×2, PISOS-ENIF2021-RECORTE1870 ×1), más 3 filas `SPEC-FIJADA` que ya habían sellado (K2-BANCARIA-HISTORIA, DIN-LOTE-ENIF2024-ADJUDICACION/EMISIONES);
- 13 filas selladas con `NO-VERIFICADO`: 9 sin asiento y 4 con `ASIENTO-NO-VIGENTE` (su identidad cambió desde el asiento: EDER2017-…-0002, ENIGH-DUELO-EMISIONES, L-DESDE-CAPTURAS, PISO-PERSISTENCIA-ERROR).

Pregunta de mesa del encargo (§6), respuesta verbatim: «Sí, asentarlas también (Recomendado)».

`tools/verifica_aislada.py <CALC>` (un intérprete nuevo por CALC) sobre las 30 que tienen `ejecucion.json`; las 13 `NO-CORRIDA` restantes son predecesoras que nunca se ejecutaron y no hay nada que verificar. Resultado: **29 `REPRODUCE/IDENTICO`, 1 `NO-EJECUTABLE`**. Asentadas por append de línea en `forense/replay-evidencia.tsv` (`git diff --numstat`: `30 0`), con la identidad verificada contra cada `ejecucion.json`. Evidencia compacta en `forense/notas/2026-09-22-GEN2-PENDIENTES-CAJA-1-evidencia-replay.json` (el JSON completo pesa 2.9 MB; queda su sha256 `6bdbc76f…`).

- `CALC-ARBITRO-MARGINALES-2-LAPOP-0001`: dentro del sandbox da `NO-EJECUTABLE/DISTINTO` (`input_cambiado` en los dos `.dta`), pero es artefacto: la raíz `descargas_mx` vive en `/mnt/c`, que el sandbox no lee. Fuera del sandbox: `REPRODUCE/IDENTICO`. Se asienta esta última y el asiento lo declara.
- `CALC-PISO-PERSISTENCIA-ERROR-0001`: `NO-EJECUTABLE` con `CONTEXTO=IDENTICO` y `outputs_faltantes`. Causa: el medidor importa `tools/marcador_segmento.py` **vivo** y deriva el marcador del árbol (`M.deriva()`), sin hash en la spec; el archivo cambió 7 veces después del sello `24afe8b9` (el último, `0ecf1caf`, hoy). No es un NO-REPRODUCE y no se fuerza: NC `…-c09b-03`.
- Efecto colateral: el verify de `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001` hace que su medidor **escriba** `forense/analisis/ensafi2023-estrategias-conjuntas-cli-1/` (5 CSV), que choca con la carpeta `-v1_1` en T02 (5 FAIL). Se movió fuera del árbol; no está en ningún commit.

### 1.2 Arreglo adyacente: `repite_de` en abanico no es sucesión

Seco de `registro` (sin escribir): las tres corridas `CALC-ENIGH2022-*` habrían pasado a `SUPERADO→CALC-ENIGH2020-*`. Las 9 specs ENIGH 2016/2018/2020 (sello `d1a27b7d`, GEN2-ENIGH2024-SERIE-Y-COMMIT-1) declaran `repite_de: CALC-ENIGH2022-*` con sentido «misma receta, otra ola» (ids de RESULT distintos: `ENIGH16/20/22`); `registro()` leía todo `repite_de` como sucesión y, con tres hijos, ganaba el último. Mesa, verbatim: «Arreglo ≤10 líneas + registro (Recomendado)».

- Primer criterio probado y **descartado**: «sucesión sólo si comparten ids de RESULT». Deshacía sucesiones legítimas (`CALC-ENVIPE-U4-2012→v1_1`, `CALC-0001`, ENADID, ENSAFI…), que renombran ids.
- Criterio adoptado: sucesión sólo si **un único** hijo declara ese padre (`tools/corrida0.py::_sucesor_de`, 10 líneas). Medido sobre las specs del árbol: 62 padres, 68 hijos, y los únicos tres abanicos son exactamente los tres ENIGH2022.
- Prueba de aceptación: diferencia entre el seco sin arreglo y con arreglo = sólo las 3 filas ENIGH2022 y sus RESULT (el resto son líneas de contexto del diff que se desplazan). Test: `tests/test_registro_repite_de_abanico.py` (sintético + control de que la regla vieja sí marcaba el abanico + propiedad sobre la vista).

### 1.3 La vista no puede publicarse por PR

`registro --escribe --lote <los 30>` escribió sin parar (cero `REPLAY-PISADO`) y la vista quedó en punto fijo. Pisadas medidas contra `origin/main`, columna por columna: `estado` no cambia en ninguna fila existente; `resultado/contexto_replay` sólo en las 13 del lote; `fuente_replay` en esas 13 y en 3 DIN-LOTE-ORO (proyectan un asiento de DIN-LOTE-ENIF2024-COMMIT-1 que ya estaba en main); `motivo_cuenta_gen2` en 17 (firmas de `decisiones.tsv` más nuevas, p. ej. `c3df2794`); en `resultados.tsv` sólo altas (20 449) y `fuente_replay`.

**Pero esa vista no viaja.** Desde #984 (TUBERÍA-EFICIENCIA-1, firma de mesa 21/sep §2(2)) la guarda bloqueante `verify.yml:546` impide que un PR toque un `DERIVADO — NO EDITAR`, y el job del push a `main` excluye a propósito `registro` porque exige `--lote` (`verify.yml:365-392`). Resultado: **ningún acto puede cumplir E.7**. Ésa es la causa de las 18 corridas sin fila, y de que `344739d1` revirtiera las de otro acto. Mesa, verbatim: «PR sin derivados + FP a mesa (Recomendado)». La vista re-derivada queda identificada por hash (`corridas.tsv` `fd903c41…`, `resultados.tsv` `0e27682f…`) y el comando para reproducirla está en NC `…-c09b-01`. Sucesor: FP `…-c09b-02`.

## 2 · P2 · FD y catálogos

### 2.1 NC-0270 — `tloc` (ENIF 2024) contra `tam_loc` (ENIGH 2022)

`enif2024_csv.zip::conjunto_de_datos_{tmodulo,tsdem}_enif_2024/catalogos/tloc.csv` y `enigh2022_nc_csv.zip::conjunto_de_datos_concentradohogar_enigh2022_ns/catalogos/tam_loc.csv`, por texto: `1` 100 000 y más · `2` 15 000 a 99 999 · `3` 2 500 a 14 999 · `4` menos de 2 500 habitantes, en los tres archivos. **Confirma**: MAPEO-N-A-1 no cambia. La subida de `evidencia_grado` en el crosswalk de ejes queda fuera de perímetro (NC `…-c09b-02`).

### 2.2 NC-0301 — códigos 97/98/99 de edad

| instrumento | archivo | 97 | 98 | 99 |
|---|---|---|---|---|
| ENVIPE 2025 | `envipe2025_csv.zip::tsdem_envipe2025/catalogos/edad.csv` | 97 o más años | no especificada, 18+ | no especificada, ≤17 |
| ENIF 2024 | `…tmodulo…/catalogos/edad_v.csv` (EDAD_V) · `…tsdem…/edad.csv` | 97 años y más | no especificada, 18+ | (tsdem) no especificada, ≤17 |
| ENCIG 2025 | `encig25_estructura_base_datos.pdf`, pregunta 2.5 `EDAD` (el `.sav` no trae etiquetas de valor) | 97 años o más | no especificada, 18+ | no especificada, ≤17 |

En los tres, **97 es una edad real (tope)**. La premisa de `MAESTRA35-L1` §1.3 («97/98/99 = no especificada») es falsa para el 97: `60+` opera como 60–96 y deja fuera a la población de 97 y más. Por la regla que la propia nota del CORTE-EDAD escribió, el veredicto bajaría a NO-EQUIVALENTE. Toca lo que se mide, así que no se corrige aquí: FP `…-c09b-01`, con tres opciones y recomendación.

### 2.3 NC-0437

`find -L data/raw -name enif_2024_bd_csv.zip` → `data/raw/enif_2024_bd_csv.zip`, sha256 `00e4b0b4…` = `data/manifiesto.yaml`. El payload está en el corpus compartido.

### 2.4 Acreditaciones masivas: sólo se mide el tamaño

- NC-0236: 1 153 filas físicas (`data/reactivos-contexto-residual-v1_1.tsv`: ENVIPE 2025 643 ambiguas + 451 etiqueta técnica; ENCUCI 2020 26 + 32; ENIF 2024 1). Sin cambio desde el 15/sep; `CORR-0007` sigue `EXISTE-NO-SATISFACE 6/8`.
- NC-0259: 190 filas `IDENTIDAD-INSUFICIENTE` (`data/crosswalk-tablas-fd-residual-v1_0.tsv`): MOCIBA2015.sav 159 + ENASEM 2021 `SECT_B_NON_RESIDENT_FOLLOW_UP_2021.csv` 31. El texto de la NC nombra además ENASEM 2018 `SECT_B_*` (44), que no está en ese motivo: el total cuadra, el desglose no.

## 3 · P3 · Sondas

### 3.1 NC-0120 — recuperación real de `StartWhenAvailable`

`Get-WinEvent` sobre `Microsoft-Windows-TaskScheduler/Operational`, filtro XPath por `TaskName = \ModeladoMexicano\AdquiereCron` (fuera del sandbox: el registro vive en Windows). Desde el 15/sep: 670 eventos. **Evento 114, 5 veces**: «no pudo iniciar la tarea … tal y como estaba programada. La instancia … se inició ahora como lo requiere la opción de configuración que indica que la tarea se debe iniciar cuando sea posible». RecordId 11731 (16/sep 08:45), 14012 (17/sep 09:10), 18279 (18/sep 20:11), 23786 (21/sep 09:07), 26165 (22/sep 09:40); las instancias de 16/sep, 21/sep y 22/sep cerraron con 102 (RecordId 11790, 23973, 26328). El inventario la clasificaba como «una espera»: ya había ocurrido cinco veces.

### 3.2 Sondas de `gh` (baca-01; parte (a) de b6dc-03)

- `gh api repos/…/branches/main/protection` → 404 «Branch not protected»; pero `branches/main.protected = true`: la protección vive en el ruleset `20030401` «main protegida», activo: check requerido `check`, `strict_required_status_checks_policy = false` (**no exige ramas al día**), `non_fast_forward`, bypass sólo `RepositoryRole 5` en modo `pull_request`.
- `actions/permissions/workflow` → `default_workflow_permissions = read`, `can_approve_pull_request_reviews = false`. Un job de Actions no empuja a `main` sin cambiar esos permisos y sin pasar el check requerido; `github-actions` no está entre los `bypass_actors`.
- `gh pr checks 994` lee el CI del propio PR.

### 3.3 Red (un intento cada una)

`curl -sL -w '%{http_code}'` desde caja; el proxy no negó ningún host (sin `sandbox_violations`), así que los códigos son del sitio:

| NC | URL | resultado |
|---|---|---|
| NC-0202 | `ennvih-mxfls.org/english/documentation.html` | 404 |
| NC-0202 | `rand.org/…/FLS/MxFLS.html` | 403 |
| NC-0202 | `icpsr.umich.edu/…?q=Mexican+Family+Life+Survey` | 403 |
| NC-0202 | `openicpsr.org` | 403 |
| NC-0278 | `jmlr.org/papers/volume11/cawley10a/cawley10a.pdf` | 200, sha256 `db01ac8f…` |
| NC-0278 | `doi.org/10.1111/j.2517-6161.1995.tb02031.x` → `academic.oup.com` | 403 |
| NC-0278 | `otexts.com/fpp3/accuracy.html` | 200, sha256 `dc2216dc…` |

NC-0278, lo que dicen las dos abiertas: Cawley & Talbot (2010), resumen: «some common performance evaluation practices are susceptible to a form of selection bias as a result of this form of over-fitting and hence are unreliable»; FPP3 §5.8: «The accuracy of forecasts can only be determined by considering how well a model performs on new data that were not used when fitting the model». Coinciden con lo que el careo les atribuye. Lo no obtenido: NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO (recetas H3/H4).

## 4 · Devolución

**HUMANO** (receta de un minuto; ninguna cambia de estado):

- **H1 · NC-0156.** El titular envía desde su correo institucional el expediente `forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/03-ENNVIH-DIN-S6.md` al contacto de datos de ENNViH, pidiendo pesos replicados o servicio de varianza para los cuatro estimandos. Se espera: una vía operativa o una negativa por escrito.
- **H2 · NC-0166.** El titular de N35 escribe al autor de correspondencia de *Do Workers Value Formal Jobs?* pidiendo Appendix C, la asignación de los 64 bloques, el microdato anonimizado y el código de las tablas 2–5. Se adjunta la cita del paper. Se espera: paquete o negativa.
- **H3 · NC-0202.** En un navegador: abrir `https://www.ennvih-mxfls.org` (la ruta `/english/documentation.html` da 404: buscar «Documentation» desde la portada), la página MxFLS de RAND e ICPSR/openICPSR con la búsqueda «Mexican Family Life Survey»; guardar el PDF o la URL con fecha. Se espera: documentación oficial de pesos o su ausencia.
- **H4 · NC-0278.** En un navegador con acceso institucional: abrir `https://doi.org/10.1111/j.2517-6161.1995.tb02031.x` y copiar la frase del resumen que distingue FDR de FWER. Se espera: una cita.
- **H5 · NC-…-3d08-02.** Mesa pega el texto de las dos adendas (PILOTO-3-P0 del 20/sep y LIMPIEZA-RAMAS-LOCALES-3) como `<encargo>-ADENDA-N.md`.

**DE-MESA** (la pregunta en una línea): NC-0161 (#998 la re-selló ABIERTA; espera la orden de adquisición dirigida) · NC-0246 (serie MOCIBA del panel F6: depende de NC-0237) · NC-0259 (¿se acredita a mano el emparejamiento de esas 190 filas?) · NC-0316/0320/0321/0322/0326 (el registro ya está hecho; ¿se integran esas lecturas en TRA?) · NC-0375 y NC-…-308c-01 (¿se abre un núcleo común ENUT 2019/2024?) · NC-0448 (¿las 4 celdas de 3D pasan a consumir el árbitro GEN2 ya medido?) · NC-…-b6dc-03 (b) (¿se quiere la auditoría de los 16 commits?).

## 5 · Lo que el inventario decía que esperaba a caja y lo que de verdad esperaba

Columna `espera_real` de la tabla: de las 49 filas, **6 necesitaban caja de verdad** (`CAJA` 5: NC-0270, 0301, 0437, 0447, baca-01; más NC-0120, que necesitaba el registro de eventos de Windows y ya había ocurrido). 12 ya estaban resueltas antes de este acto (`NINGUNA-YA-OCURRIO`, 11 de ellas `RESUELTO-ANTES`), 12 esperan a mesa, 5 a un humano, 4 a TUBERÍA, 4 a una medición nueva y el resto a relevo, acreditación, pre-registro o dirección. La etiqueta «espera a caja» se ponía cuando una sesión de nube no podía algo, no cuando la fila necesitaba caja. Y el hueco real de caja (18 corridas sin fila y el canal de publicación cerrado) no estaba en la lista.

## 6 · Concurrencia

Compuerta §8 al arrancar: ninguna rama en vuelo tocaba los derivados compartidos (#998 y #999 tocaban `no-corrido.tsv`; ya fusionados y reconciliados). **Al cerrar hay tres actos de caja en vuelo que arrancaron después**: `mm-din-credito-escolaridad-2` (con `corridas/resultados/replay-evidencia` modificados sin commitear en su worktree), `mm-gen2-din-credito-k2-historia-run-1` y `mm-gen2-duelo-envipe2026-ejecucion-1`. Tres ramas remotas tocan `no-corrido.tsv` (TRAMITE-FIRMAS-6, MARGINALES-ADOPCION-1 —además `tools/corrida0.py`—, PENDIENTES-RECONCILIA-1). Este PR sólo añade filas a `replay-evidencia.tsv` y edita en `no-corrido.tsv` las filas propias, por id. Quien fusione después re-aplica por id, sin renumerar. Quien corra `registro` sin `_sucesor_de` volverá a proyectar ENIGH2022 como SUPERADO.
