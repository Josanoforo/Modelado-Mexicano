# ACTO GEN2-ADQ-F6-DIRIGIDA-1 · nota de cierre

Encargo: `forense/encargos/2026-09-22-GEN2-ADQ-F6-DIRIGIDA-1.md` (0-bis `e7be565`, sello de cuerpo `8e8742ef…`). SHA de redacción `3f48be30` = `origin/main` al abrir (0 commits detrás). ENTORNO: NUBE (`cloud_default`), red a INEGI `200/200`, corpus no montado (`corrida0 --verifica`: 0 archivos examinados). MODO ABIERTO. ADR `ADR-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01`.

**Contadores movidos: cero mediciones, cero descargas, cero ids nuevos en el manifiesto.** Se mueven: `licencia` escrita en 34 entradas (588 → 554 sin licencia), 1 fila de cola, 1 FP, 5 NC nuevas y 2 enmiendas (NC-0161 y NC-0162).

## 1 · Hallazgo principal: lo que el encargo mandaba bajar ya estaba en el manifiesto

El encargo tomó sus premisas de `F6-falta-conseguir-v1_0.tsv` (fila «ya_en_manifiesto») y no del manifiesto por id (A.15). Consulta por id sobre `data/manifiesto.yaml` (1646 entradas, `yaml.safe_load`, patrón `enco|enpol|mociba|enaproce|encrige|issp|za6980` sobre `id` y `archivo`):

| Fila F6 | Premisa del encargo | Manifiesto, por id | Entró |
|---|---|---|---|
| R11 ENPOL 2016 | «no en manifiesto» | `enpol2016_bd_csv_zip` (`a405ed77…`, 16 801 537 B) y `enpol2016_fd_pdf` (`5b2c780f…`) | 16/sep, Codex GEN2-38 |
| R01 MOCIBA 2022 | «POR VERIFICAR» | `mociba_2022_mociba2022_fd` (`923fa85a…`), `_bd_csv` (`df186f09…`) y 4 formatos más de BD, `mociba_2022_cuestionario_pdf` | antes del 22/sep |
| R10 ENCO por mes | «faltan meses» | `enco_2025_junio_dbf_reservado` (`fd283a1a…`) y `enco_2026_junio_dbf_reservado` (`f1c10fb4…`), las dos olas que fijó GEN2-ENCO-DOS-OLAS-RESERVADAS-1, ya `RESERVADA-NO-ABIERTA-NO-INDEXAR-L`; más `c_enco_b_v4` y `enco_2026_agosto_dbf` | 16/sep y 3/sep |
| R08 ENCRIGE | «solo tabulados 2020» | `conjunto_de_datos_encrige_2020_csv` (datos abiertos, 1 630 532 B), `encrige2020_cuestionario`, `gen2_encrige2020_diseno_muestral`. El microdato no es público (§2) | 3/sep |

La tabla es entregable según §2 («encontrar un encargo mal fundado es entregable»). La premisa cayó en **logística**, no en qué se mide. El objetivo («que F6 tenga lo adquirible, con sha y licencia») se cumple con **cero descargas**, y el criterio literal de «hecho» («lista los ids **nuevos**») no puede cumplirse porque no quedó nada nuevo que registrar. Lo asienta `NC-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01` (`SUSTITUIDO-POR`, CERRADA).

Consecuencia sobre la regla de entorno: v2.16 §6 («Microdato se baja siempre desde CAJA», mandato del 21/sep) chocaba con el `ENTORNO: NUBE` del encargo. Como no hubo nada que bajar, el choque no llegó a ejecutarse. Si un sucesor necesita microdato nuevo, va a caja.

## 2 · Sondas de portal (GET, nunca `-I`; compuerta §8 «sonda VERDE antes de cada descarga»)

`curl -sS -L -o <f> -w '%{http_code} %{size_download}' --max-time 30 <url>` desde NUBE, 22/sep/2026:

```
https://www.inegi.org.mx/inegi/terminos.html            -> 200 10442   sha256 97e97599169f75f455877e85edffcf941d512f56c5c00197ebfec783d802c67a
https://www.inegi.org.mx/rnm/index.php/catalog/330       -> 200 147583  (ENAPROCE 2015)
https://www.inegi.org.mx/rnm/index.php/catalog/518       -> 200 167071  (ENAPROCE 2018)
https://www.inegi.org.mx/rnm/index.php/catalog?sk=encrige -> 200 41100  (lista: 264 = ENCRIGE 2016, 691 = ENCRIGE 2020, 601 = ECRIGE-CDMX 2019)
https://www.inegi.org.mx/rnm/index.php/catalog/264       -> 200 166697  (ENCRIGE 2016)
https://www.inegi.org.mx/rnm/index.php/catalog/691       -> 200 92876   (ENCRIGE 2020)
https://www.inegi.org.mx/programas/{enaproce/2015,enaproce/2018,encrige/2016,encrige/2020}/ -> 200 (SPA: solo título, sin enlaces -- no informa)
https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017 -> 000  curl: (56) CONNECT tunnel failed, response 403
https://search.gesis.org/research_data/ZA6980            -> 000  curl: (56) CONNECT tunnel failed, response 403
```

Sección «Condición de acceso», verbatim:

- **ENAPROCE 2015 y 2018** (catalog/330 y /518): «La información de la ENAPROCE a nivel microdato es confidencial; la descarga de la base de datos de este proyecto es restringida al público en general. Sin embargo, es posible acceder a la información de microdatos de manera indirecta a través del siguiente mecanismo: Laboratorio de análisis de datos para servidores públicos del Estado Mexicano, funcionarios de organismos internacionales e investigadores y estudiantes calificados…» → R03 `NADA-ADQUIRIBLE` por descarga pública. El laboratorio exige identidad, que es el PARO (e) del encargo, así que va a la bandeja del titular (`…-e7be-02`).
- **ENCRIGE 2020** (catalog/691): «Los microdatos de proyectos estadísticos en establecimientos no están abiertos al público en general, tal procedimiento violentaría el principio de confidencialidad establecido en la Ley. Sin embargo […] el INEGI ofrece acceso indirecto mediante Laboratorio de microdatos/Procesamiento remoto…»
- **ENCRIGE 2016** (catalog/264): «…el INEGI proporciona varias formas de acceso a los microdatos, así como el archivo descriptor…». No dice si hay descarga pública, así que queda **NO-VERIFICADO**. No se afirma ni se niega.
- **GESIS**: el 403 lo pone el proxy de egreso de la nube, no el host. NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO (A.5). Receta de un minuto: desde caja o un navegador, abrir la URL de arriba, leer la categoría de acceso de ZA6980 y los términos de uso de GESIS, y copiar el texto al campo `licencia` de `za6980_*`.

## 3 · Estado por fila (P1)

El archivo es `forense/prereg-duelo-v2/F6-falta-conseguir-v1_1.tsv` (nuevo; v1_0 queda intacta), con dos columnas nuevas: `estado_adquisicion` y `comando_de_verificacion`. Cada comando imprime los ids citados. Los 14 ids se comprobaron por comando al escribir el archivo, sin ningún ausente.

| Fila | estado_adquisicion |
|---|---|
| R09 ISSP | YA-EN-MANIFIESTO (`za6980_q_mx`); licencia GESIS no obtenida |
| R01 MOCIBA | YA-EN-MANIFIESTO (2021/2022/2023 FD; 2022 con BD y cuestionario) |
| R10 ENCO | YA-EN-MANIFIESTO (cuestionario, agosto 2026, junio 2025/2026 reservadas) |
| R11 ENPOL | YA-EN-MANIFIESTO (BD + FD 2016) |
| R08 ENCRIGE | DECISION-DE-MESA → `FP-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01` |
| R02 WBES | DECISION-DE-MESA → la misma FP |
| R03 ENAPROCE | NADA-ADQUIRIBLE por descarga pública (solo laboratorio) |
| R14 ENH | NADA-ADQUIRIBLE (sin cambio) |
| R12/R13/R07 | NADA-ADQUIRIBLE (sin cambio) |

**A.1 en tres estados**, con `python3 tests/manifiesto.py --verifica` (sale 0; la opción `--id` no filtra, así que corre sobre todo el manifiesto y se extraen las líneas de los ids de F6): `AUSENTE` (data_raw) ×6 (`mociba_2021/2022/2023_fd`, `mociba_2022_bd_csv`, `enpol2016_bd_csv_zip`, `enpol2016_fd_pdf`) · `RAÍZ NO CONFIGURADA` (descargas_mx) ×4 (`za6980_q_mx`, `conjunto_de_datos_encrige_2020_csv`, `c_enco_b_v4`, `enco_2026_agosto_dbf`) · `FUERA_DE_PERIMETRO` (reserva_respondentes) ×2 (las dos ENCO reservadas). Ninguno `hash-discordante`; 0 archivos examinados, de modo que no es un negativo (A.13). El sucesor en caja es `…-e7be-05`.

**Reservas (E.6).** Este acto no registra ninguna ola nueva, así que no escribe filas en `decisiones.tsv`. ENPOL 2016 entró el 16/sep sin `estado_reserva`. La regla `reserva:ola-nueva-de-encuesta-con-historia` (21/sep) se declara «NO es retroactiva», así que este acto no la reclasifica. Queda dicho aquí por si mesa quiere otra lectura.

## 4 · Licencias (P3)

Se escribieron **34** entradas: todas las de `data/manifiesto.yaml` con `url_origen` en `inegi.org.mx` y sin campo `licencia`. El texto sale de la página leída arriba (sha `97e97599…`). La inserción es de una línea por entrada, justo después de su `sha256`, y ningún otro campo cambió: el YAML re-parseado, comparado entrada por entrada, solo difiere en `licencia` de esas 34. Entre ellas están las cuatro de F6 que no tenían licencia: `c_enco_b_v4`, `enco_2026_agosto_dbf`, `conjunto_de_datos_encrige_2020_csv` y `encrige2020_cuestionario`. Quedan **554** sin licencia: otros dominios, `url_origen` no determinada, y las 4 de ZA6980 (GESIS). Van en `…-e7be-04`.

## 5 · Para PRODUCTO-DINERO y dirección: qué familias pueden ser panel de F6

- **Material completo, panel todavía no acreditado:** R01 MOCIBA (tres olas públicas 2021–2023; falta decidir si es la misma medida en las dos olas, NC-0237, y leer los FD en caja), R11 ENPOL (2016 + 2021; 2021 ya es CIV-12 del marco piloto, así que solo 2016 es libre y la familia sigue sin reserva) y R09 ISSP (una sola ola; falta leer v26 en caja). Ninguna es panel real hasta que corra `GEN2-F6-FACTIBILIDAD-CAJA-1`.
- **Material completo, pero no sirve a M tal como está:** R10 ENCO. Sus dos olas están adquiridas y reservadas, pero GEN2-ENCO-DOS-OLAS-RESERVADAS-1 ya advirtió que P10 mide la *posibilidad* de ahorrar, no la tenencia (`M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO` si M no trae enlace).
- **No lo serán por descarga pública nunca:** R03 ENAPROCE y el microdato de R08 ENCRIGE 2020 (solo por laboratorio), y R12/R13/R07 y R14 (el mundo no levantó la segunda ola o el reactivo). R02/R08 dependen de la FP de unidad; la recomendación es dejarlos fuera.

Conclusión para FP-374 (`EN-ESPERA-PANEL`): la adquisición dirigida por descarga pública **queda agotada**. Lo que falta para tener panel ya no es bajar nada, sino leer en caja y que mesa firme la unidad.

## 6 · Perímetro

Escrito: `data/manifiesto.yaml` (solo `licencia`, 34 líneas) · `data/curacion-registro/cola-adquisicion-registro.tsv` (1 fila propia, `…#R03`, `NO-ACCESIBLE`) · `forense/prereg-duelo-v2/F6-falta-conseguir-v1_1.tsv` (nuevo) · `forense/no-corrido.tsv` (enmiendas NC-0161/0162 añadidas al final del campo `sucesor`, sin reescribir nada; 5 NC nuevas) · esta nota. Cascada de cierre permanente (D-21): `forense/firmas-pendientes.tsv` (1 FP, A.12), `forense/hallazgos.md`, `canon/gobernanza-v1_15.md`, `canon/L0/ADR-260922-GEN2-ADQ-F6-DIRIGIDA-1-e7be-01.md`, `canon/registro-rotulos.tsv`. Sin tocar: `data/corrida0/decisiones.tsv` (no hubo ola nueva), todo CALC, specs, `milpa/` y el panel F5. `tools/adq_doctor.py --selecciona` no corre en esta nube (`ModuleNotFoundError: jsonschema`); no era necesario, porque la fila nueva es `NO-ACCESIBLE` y el agente no la camina.
