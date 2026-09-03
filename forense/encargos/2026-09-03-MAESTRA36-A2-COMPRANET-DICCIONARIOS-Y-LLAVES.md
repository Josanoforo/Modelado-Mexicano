# ENCARGO · ACTO MAESTRA36-A2 · COMPRANET-DICCIONARIOS-Y-LLAVES

**SHA de redacción:** 9af8407 · 3/sep/2026, dirección (Fable) · instrucciones v2.12
**Entorno asignado:** UBUNTU, clon `/home/pc0/mm-adq`. NO en NUBE.
**Estado:** VIVO

> Archivado verbatim por A.3 (0-bis). El texto de abajo es el que llegó a la sesión.

---

## Texto del encargo, verbatim

ENCARGO · ACTO MAESTRA36-A2 · COMPRANET-DICCIONARIOS-Y-LLAVES

SHA de redacción: 9af8407 · 3/sep/2026, dirección (Fable) · v2.12 · Estado: GATED — por producto: git log --format=%s origin/main | grep -c 'MAESTRA36-A1' → ≥ 1 con ## CONSUMIDO en su encargo archivado (A1 fusionado; comparten data/manifiesto.yaml y data/curacion-registro/**). No cumplida → cero commits.

ENTORNO ASIGNADO: UBUNTU, en el clon /home/pc0/mm-adq (allowlist *.gob.mx, Bash(curl *)), lanzado a mano fuera de la ventana del cron (no entre 07:25 y 08:00). NO en NUBE (403 de buengobierno.gob.mx verificado desde nube, 3/sep). MODELO SUGERIDO: Sonnet (adquisición por receta) — Opus solo si P2 exige juicio sobre llaves.

CARRILES: N1//despacha en nube, disjuntos. Ningún otro acto de adquisición en caja hasta que este fusione.

FIRMAS DE MESA — verbatim, 2/sep/2026: mesa entregó la liga https://comprasmx.buengobierno.gob.mx/datos-abiertos#datos_relevantes_de_los_contratos_ingresados_a_la_plataforma. Dirección lo leyó como firma de «abrir esta fuente»; la decisión de bajar la serie completa 2010–2025 no está firmada y este acto no la toma.

═══ VERIFICACIÓN DE EXISTENCIA (A.8), contra 9af8407 ═══ (1) ESTRUCTURA. Fila cola-adquisicion-v1_0.tsv:63 (EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6, NO-OBTENIDO-POR-ESTE-AGENTE(2 intentos), url_conocida=https://upcp-compranet.buengobierno.gob.mx/); necesidad en data/cola-ext-oficial-2026-08-06.tsv:4 (EXT-OF-05: «¿hay llaves estables persona-proveedor-procedimiento-contrato-sanción?», destino R3.1/R3.2). Vía: /adquiere §2–§7 + tres capas del curador (GUÍA §«alta de fuente nueva»). (2) CONTENIDO. grep -ci 'compranet\|comprasmx' data/manifiesto.yaml → 0 (1 070 ids). Índice HTML plano con los archivos estáticos, abierto entero por dirección el 2/sep: https://canvas-compranet.buengobierno.gob.mx/informacion_ayuda/datos_abiertos.html. Un archivo abierto byte a byte desde nube (mime xlsx): https://comprasmx.buengobierno.gob.mx/cnetassets/datos_abiertos_contratos_expedientes/Contratos_CompraNet5.xlsx. Los CSV en upcp-compranet.funcionpublica.gob.mx/cnetassets/... y el reporte RUPC en upcp-cnetservicios.funcionpublica.gob.mx/norah/documentos/recursos/lck/hc/obtener: NO OBTENIDOS POR ESTE AGENTE (1 intento, robots) — hecho sobre el fetcher de nube, no sobre la fuente. → EXISTE-NO-VERIFICADO para la caja. (3) COBERTURA RETROACTIVA. La fila 63 es del 6/ago; su rótulo dice EXT_OF_07 pero el contenido es EXT-OF-05 (la 07 es IFT) — se corrige en la nota, no en la fila.

SPEC POR PIEZA (un PR, un ADR, un recibo)

P1 · Cuatro archivos, no dieciséis años. /adquiere sobre la fila 63 con estas URL exactas: DD_PIC_CONTRATOS_2400703.xlsx y DD_PIC_EXPEDIENTES.xlsx (upcp-compranet.funcionpublica.gob.mx/publicas/), DD_RUPC_240912.xlsx (mismo host) y el reporte RUPC (.../norah/documentos/recursos/lck/hc/obtener). Si funcionpublica bloquea, probar el mismo path bajo comprasmx.buengobierno.gob.mx (espejo verificado para cnetassets/). A.7 doble descarga; A.5: cada fallo con salida cruda y receta de navegador ≤1 min. Registro por las tres capas: --registra (aquí sí: van a data/raw/ = corpus compartido, verificar anti-PR#77), cola fila 63 → OBTENIDO parcial con ids_manifiesto, relaciones.tsv+procedencia+utilidad contra la necesidad de EXT-OF-05 (alta de alias compranet sin fusionar), baseline.json recifrado, via_capa2.py en verde, vista T26.

P2 · La pregunta de llaves, contestada con los diccionarios y nada más. Tabla de una página: para contratos, expedientes y RUPC, ¿qué campo identifica proveedor (RFC / folio RUPC), procedimiento (código de expediente), contrato y sanción? ¿Cruzan entre sí y con directoriosancionados.funcionpublica.gob.mx? Veredicto A.4 sobre la necesidad EXT-OF-05: EXISTE-SATISFACE (llaves estables, panel reproducible) / EXISTE-NO-SATISFACE (qué falta) / NO-ENCONTRADO (universo: los tres diccionarios). Sin abrir ningún CSV de contratos.

P3 · Propuesta a mesa, sin ejecutar. Si P2 = EXISTE-SATISFACE: lista de la serie (zips 2010–2022, CSV 2020–2025, tamaños si los headers los dan) con una estimación de bytes y la fila 63 dividida en sub-filas por año; no se descarga. Si no: se cierra la fila con el veredicto y se anota en hallazgos.md que la trazabilidad administrativa de R3.1/R3.2 no cruza.

PERÍMETRO Y CONCURRENCIA. Toca: data/raw/ (payloads, gitignorado) · data/manifiesto.yaml · data/curacion-registro/{cola-adquisicion-registro.tsv, relaciones.tsv, evidencias.tsv, utilidad-modelo.tsv, aliases-fuentes.tsv, baseline.json} · data/cola-adquisicion-v1_0.tsv (vista) · data/INFRAESTRUCTURA-v1_0.md · forense/notas/2026-09-0X-MAESTRA36-A2-*.md · forense/hallazgos.md · forense/firmas-pendientes.tsv · cascada. NO toca: milpa/**, tests/manifiesto.py, tools/adquiere_cron.sh. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS. Candidato ADR 312 y FP-264 (recibo), re-derivados al arrancar (A1, N1 y L12 pueden ir delante).

CONTADOR. Payloads OBTENIDO +4 (o los que se obtengan, con los fallos declarados) · necesidad EXT-OF-05 con veredicto A.4 por primera vez. Medición de modelo: cero directo, declarado.

Lo que NO hace. No baja la serie de contratos. No toca reglas ni el motor. No responde nada sobre R3.1/R3.2 más allá de si las llaves cruzan.

Sucesores. Si EXISTE-SATISFACE: A3 · COMPRANET-SERIE con la lista de P3, firmado por mesa; y una fila nueva de necesidad para «trazabilidad administrativa» si R3.1/R3.2 la exigen.

---

## ENMIENDA DE DIRECCIÓN, 3/sep/2026 — archivada verbatim por A.3

> Recibida **después** de ejecutado el acto. El texto de abajo es el que llegó a la sesión.

ENMIENDA de dirección, 3/sep/2026, contra ea45e01. Este acto se ejecutó bajo la v1 del encargo (SHA de redacción 9af8407). La v3 —que lo sustituía— difería solo en: cabecera (ea45e01, COMPUERTA: ninguna, cumplida por producto: ## CONSUMIDO de A1 con PR #500, ADR-310 — verificado por este acto); CARRILES (N2 nube, L12/L13 caja, disjuntos de data/curacion-registro/**); firma de mesa verbatim del 2/sep (la liga comprasmx.buengobierno.gob.mx/datos-abiertos#…; «la serie 2010–2025 no está firmada», y este acto no la bajó); A.8 §(3): la fila 63 rotula EXT_OF_07 lo que el mapa llama EXT-OF-05 (la 07 es IFT), anotado, no renombrado; y la cita de FP-258 al editar la fila 63 por línea. Nada de eso cambia P1–P3 ni su resultado. Candidatos derivados al cierre: ADR y FP siguientes libres tras #503 y L13 (renumera quien fusiona segundo).

### Lectura de la enmienda por este acto (no la interpreta, la verifica)

Los cinco puntos de diferencia entre v1 y v3 se verificaron **contra el árbol**, uno por uno, y ninguno mueve `P1`–`P3`:

1. **Cabecera / compuerta.** El acto ya la verificó **por producto** antes de escribir: `git log --format=%s origin/main | grep -c 'MAESTRA36-A1'` → `1`, y `git show origin/main:forense/encargos/2026-09-02-MAESTRA36-A1-ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS.md | grep -n '^## '` → `175:## CONSUMIDO`. `PR #500` = `ea45e01`, `ADR-310`. Es exactamente lo que la v3 pedía.
2. **CARRILES.** Ningún archivo de este acto está fuera de `data/curacion-registro/**`, `data/manifiesto.yaml`, `data/cola-adquisicion-v1_0.tsv`, `forense/**` y la cascada de canon — disjunto de `N2` (que tocó `forense/prereg-duelo-v2/**`) y de `L12`/`L13`. El merge de `origin/main` en esta rama entró **sin conflicto**.
3. **Firma de mesa del 2/sep.** La liga que la mesa entregó es el ancla que este acto reprodujo en caja (`comprasmx.buengobierno.gob.mx/cnetassets/…`). **La serie 2010–2025 no se bajó**, y `P3` explica por qué ni siquiera se propuso: `P2` no dio `EXISTE-SATISFACE`.
4. **A.8 §(3), rótulo de la fila 63.** Ya está así: la corrección `EXT_OF_07` → contenido `EXT-OF-05` se escribió **en la nota de la fila**, no en `fuente_canonica`. La fila no se renombró.
5. **`FP-258`.** Se cumplió el fondo de la cita: la fila 63 se editó **línea por línea**, nunca con round-trip de `csv`. La cita explícita a `FP-258` se agrega al cerrar, en la nota y en el ADR.

**Numeración al cierre**, re-derivada contra `origin/main` **después** de fusionar `PR #503` y `PR #504` (`1d4c67d9`): `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` → `311`, sin duplicados; candidato `ADR-312`. Máximo de `forense/firmas-pendientes.tsv` → `260`; candidatas `FP-261` y `FP-264`. `L12`/`L13` seguían abiertos: si alguno fusionaba primero, **renumera quien fusiona segundo**. **Y ocurrió**: `PR #502` (`ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA`) fusionó mientras este acto cerraba y se llevó `ADR-312` y `FP-261`, así que la numeración final, re-derivada contra `origin/main = 18fd2bd3`, es **`ADR-314`**, **`FP-264`** (recibo) y **`FP-265`** (esquema).

---

## CONSUMIDO

`ACTO MAESTRA36-A2 · COMPRANET-DICCIONARIOS-Y-LLAVES`, 3/sep/2026, `ADR-314`. `P1`/`P2`/`P3` ejecutados y cerrados; la ENMIENDA de dirección del 3/sep archivada verbatim arriba y verificada punto por punto contra el árbol. Veredicto `A.4` de `EXT-OF-05`: **`EXISTE-NO-SATISFACE`**. Recibo `FP-264`; decisión de esquema `FP-265`. Nota de cierre: `forense/notas/2026-09-03-MAESTRA36-A2-P1-P3-compranet-llaves.md`. **La fusión de este PR es la firma.**
