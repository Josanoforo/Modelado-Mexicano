---PARTE ÚNICA · ENCARGO · ACTO MAESTRA38-A6 · RE-SONDEO-DE-NEGATIVOS-CON-CAPACIDAD-COMPLETA — invoca /acto (formato D-12)---

**Cabecera obligatoria (convención de `forense/encargos/`).**
SHA de redacción: `ef9ba36` · Entorno asignado: **UBUNTU** con corpus y red, fuera del sandbox de bash — **no** nube · Estado: **VIVO** · Modelo: Opus (puede subir, nunca bajar).

Texto verbatim, tal como se lanzó, abajo. No se edita en ningún punto (A.3).

---

ENCARGO · ACTO MAESTRA38-A6 · RE-SONDEO-DE-NEGATIVOS-CON-CAPACIDAD-COMPLETA — caja, Opus, invoca /acto

SHA ef9ba36 · COMPUERTA: CRON fusionado (sólo porque comparten mm-adq si mesa usa esa caja; si A6 corre en otro clon de la misma máquina, compuerta ninguna) · ENTORNO: UBUNTU con corpus y red, fuera del sandbox · MODELO: Opus. Puede subir, nunca bajar. Por qué existe (medido, no supuesto). A4 y A5 convirtieron en OBTENIDO cuatro cierres que sesiones anteriores rotularon como imposibles: PDN (fila 28, cerrada el 3/sep con la raíz de un host que sí sirve rutas), UNAM (403 de directorio leído como ausencia, con los archivos dentro en 200), ECOPRED (API SPA en mantenimiento, URL por convención viva), ICPSR (paquete de documentación tomado por el de datos). Cada uno se cerró con una ruta. Este acto reabre todo negativo de la tabla que gobierna y lo somete al protocolo que sí funcionó.

Regla de cierre (manda sobre todo lo demás). Ningún objeto vuelve a un rótulo negativo sin ≥ 4 rutas distintas con comando y salida cruda pegados (/adquiere v2.2: URL directa · API o descarga masiva · formato alterno o espejo institucional · espejo académico/Wayback/datos.gob.mx), más la receta manual ≤ 1 min cuando la última barrera sea cuenta o sesión. Tres hallazgos por ruta, nunca colapsados: RED / SERVIDOR / VACÍO (A.13: bytes y Content-Type). Una raíz de host que responde nginx vacío no es evidencia sobre sus rutas; un 403 de directorio no es evidencia sobre sus archivos; un «página en mantenimiento» de API no es evidencia sobre la URL por convención (los tres, medidos por A4). Vocabulario A.4 + D5; NO-OBTENIDO-POR-ESTE-AGENTE EN N INTENTOS lleva N ≥ 4 rutas distintas, no N intentos de la misma.

P0 · Reconciliación notas → cola (pieza D, antes del COMMIT-1). grep -rn "NO-OBTENIDO-POR-ESTE-AGENTE" forense/ data/ → 43 archivos hoy (1 294 examinados). Por cada mención: extrae el objeto; cruza contra data/curacion-registro/cola-adquisicion-registro.tsv (col. 2). Tres salidas: YA-EN-COLA (con su estado actual) · SIN-FILA → se da de alta en la cola con NO-OBTENIDO-POR-ESTE-AGENTE heredado y nota: «alta por reconciliación A6, origen archivo:línea» · YA-OBTENIDO (la nota quedó vieja) → se anota en hallazgos.md, una línea por caso, no se cataloga. Las SIN-FILA entran a la lista de P1. Salida: forense/notas/2026-09-0X-MAESTRA38-A6-reconciliacion.md con la tabla completa.

P1 · COMMIT-1: la lista congelada. Derivada hoy de la cola (awk -F'\t' 'NR>1 && $5!~/^OBTENIDO$|CERRADA|SUPERADA/' → 23 filas) más lo que P0 añada. Por objeto: id · estado actual · URL de la cola · pregunta que responde (necesidad-objeto-modelo.tsv / relaciones) · rutas específicas (mínimo las cuatro genéricas, más las de abajo donde aplican) · criterio de éxito por objeto. Se cierra con «el primer resultado que produzca este procedimiento es el que se reporta».

Clase    Objetos (id de la cola)    Rutas específicas además de las 4 genéricas
A1 NO-OBTENIDO    SICEE (1 intento; https://sicee.ine.mx/) · BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO (31 intentos: contar cuántas rutas distintas fueron, pegando la nota origen)    SICEE: receta de navegador ya escrita en 2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md l.183-198 → convertirla en curl con cookie jar; datos.ine.mx / computos como espejo. Protesta: MMAD (massmobilization.github.io), ACLED (registro gratuito = permitido), GDELT (público, api.gdeltproject.org), Cline Center; cada una con EXISTE-SATISFACE / -NO-SATISFACE contra la pregunta de la fila
A2 NO-ENCONTRADO    CANAL_DE_ADQUISICION_REFERIDOS_FINTECH · SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS    A.4: universo declarado (qué se buscó, dónde, con qué términos); paralelas por constructo (ENIF 2021 y ENSAFI 2023 ya en corpus; ENASIC 2022 para cuidados)
A3 NO-ACCESIBLE — verificar la etiqueta    OECD · PI · DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO    D5: NO-ACCESIBLE = pago, afiliación o ley. OECD Data Explorer y su API SDMX (sdmx.oecd.org/public/rest/) son públicos → si baja, la etiqueta estaba mal y se dice. PI: leer primero qué es (la fila lo dice), luego rutas. Denuncia+seguro: CONDUSEF/ENVIPE como paralelas
A4 OBTENIDO-PARCIAL    EXT_OF_07 (CompraNet 951 MB + PDN bulk ya en corpus → probablemente completable hoy) · PRICE_AND_INFORMATION… (microseguros; WB/J-PAL dataverse) · ENAFIN (WB hermana) · ENJUVE (microdato: IMJUVE, datos.gob.mx, Wayback de imjuventud.gob.mx) · REUTERS_DNR    Por cada uno: qué falta exactamente, y si lo que falta ya está por otra vía
A5 PENDIENTE-DE-MESA que caja puede bajar    CNBV_PORTAFOLIO_IMOR_CONSUMO (portafolio de información CNBV: público, sin cuenta) · ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF (FD en INEGI por URL de convención; CONDUSEF datos.gob.mx)    Si bajan, salen de PENDIENTE-DE-MESA sin firma intermedia (decidido)
A6 SIN-FETCH    INE · FINTECH_LENDING_TO_BORROWERS… — abrir byte a byte. Y corregir las 6 etiquetas caducas: UNAM, ECOPRED, Cultura Constitucional (ya OBTENIDO por A4), CNGMD (646 entradas en corpus), y las 2 que P0 identifique    Etiqueta vieja a nota:
B NO-ADQUIRIDA-POR-COSTO    Homescan/NielsenIQ · Kantar Worldpanel · Tanda+ ×2 · Mercer/GPTW    No se re-bajan. Una sonda por objeto (¿muestra pública, reporte abierto, dataset académico derivado?) y paralelas: ENIF 2021 (tandas, en corpus), ENIGH/ENCO (panel de compra), ENOE módulos (clima laboral) — resultado PARALELA-CUBRE / -PARCIAL / -NINGUNA con la necesidad que la fila cita
C relaciones NO-ENCONTRADO (28: ENFIH 7, ENSAFI 6, ENBIARE 3, ENASIC 3, CSES 2, MMAD 2, ISSP, otros)    No es fallo de descarga: es contenido. No se reabre aquí — entra al LOTE-CRUCE como pieza N16-bis: mismo método (paralelas por constructo con texto a la vista). Este acto sólo pega la lista derivada en su nota para que el cruce no la vuelva a derivar    —

P2 · COMMIT-2, por objeto y en orden de clase (A1→A6, luego B). Cada objeto: rutas con salida cruda → veredicto con vocabulario A.4/D5 → si baja: A.7 doble descarga por dos transportes, testzip, registro por las tres capas, depósito en el corpus compartido (anti-PR#77: ls -la del corpus al cerrar, no del worktree), estado de cola actualizado con etiqueta vieja en nota:, alta_relacion.py si la fuente es nueva. Si no baja: NO-OBTENIDO-POR-ESTE-AGENTE EN N RUTAS + receta ≤ 1 min → PAQUETE-RECETAS-11 (sólo lo que exija cuenta, sesión o solicitud; caja baja todo lo público). Una pieza que PARA no tumba el acto.

P3 · Cierre. forense/notas/2026-09-0X-MAESTRA38-A6-resultados.md con tabla: objeto · estado antes · rutas corridas (n) · estado después · bytes · dónde. Enmienda append en FP-314 si algún objeto de PAQUETE-RECETAS-10 cayó aquí. Estampa A.10 en cada veredicto negativo (universo = rutas corridas + fecha). Los cierres previos que este acto vuelva OBTENIDO se marcan VENCIDO EN ALCANCE en su nota origen (append, no edición).

PERÍMETRO. Toca: manifiesto (+N) · staging (transitorio) · cola + vista (estados, nota:) · relaciones sólo vía alta_relacion.py · PAQUETE-RECETAS-11 · forense/notas/2026-09-0X-MAESTRA38-A6-{reconciliacion,spec,resultados}.md · hallazgos · tablero (recibo + enmienda FP-314) · INFRAESTRUCTURA · A.3 · cascada. NO toca: milpa/** · canon (salvo ADR) · specs · data/l*-* · Downloads. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo. CONCURRENCIA: en paralelo pueden correr L2 y LOTE-ENSANUT (sus archivos: data/l2-*, data/l16-*, data/l17-*, propuesta, notas propias, cascada). LOTE-CRUCE y C1 esperan a A6 (C1 comparte cola/relaciones; CRUCE recibe la lista C). Lo que NO hace: no mide ninguna regla · no reabre las 28 relaciones (las entrega al cruce) · no toca los tiers · no pide credenciales a nadie: donde la barrera es cuenta o solicitud, entrega receta. CONTADOR: filas negativas de la cola 23 → declara · etiquetas corregidas 0 → declara · objetos OBTENIDO desde negativo 0 → declara · payloads +N · notas históricas sin fila en cola 0 → declara (P0) · medición: cero (adquisición). Necesito que uses todos tus trucos habidos y por haber.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-A6 · RE-SONDEO-DE-NEGATIVOS-CON-CAPACIDAD-COMPLETA`,
6/sep/2026, worktree `/home/pc0/mm-maestra38-a6`, rama
`acto/maestra38-a6-resondeo-negativos`, **`PR #561`** (no fusionado por el
ejecutor: el merge es de mesa). `ADR-353` · `FP-324`.

Commits: `17f7b91` (0-bis A.3) · `f774e88` (P0, reconciliación) ·
`43d71a2` (COMMIT-1, lista congelada) · `30997fd` (COMMIT-2, resultados) ·
`296ee5a` (cascada).

**Tres premisas del encargo no se reprodujeron** y quedan declaradas en la
nota de resultados §4, no corregidas en silencio: el denominador de P0
(2 788, no 1 294) · la clase A6 (0 etiquetas caducas: los 6 objetos que
nombra ya estaban `OBTENIDO`, y `SIN-FETCH` sólo vive en la columna `nota`) ·
la clase C (29 relaciones `NO-ENCONTRADO`, no 28).

**Una desviación de orden del propio ejecutor**, declarada en el §0 del
COMMIT-1: `SICEE`, `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` y `PI` se
sondearon antes de congelar la lista que el encargo manda congelar primero.
