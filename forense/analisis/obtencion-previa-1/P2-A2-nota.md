# P2 · A2 · dónde vive el detalle real de los momentos 09–22

Sesión 28/sep/2026, rama claude/new-session-sbqki2, entorno nube.

## Dónde vive el detalle
- [EJECUTADO] `rg -n "RES-01(8[4-9]|9[0-7])"`: los 14 slots **sí están** en `forense/analisis/relevo-consumidores/tabla-consumidores-v1_0.tsv` líneas 186–199 (y v1_1 186–199), pero en la columna `slot`, no en `result`; su `razon` es la genérica de la NC y su `sucesor` remite a `cotejo-documental-catalogo.md`. La premisa del encargo (§3, «ninguna fila») es verdadera para `result/consumidor/razon` y falsa para `slot`: hallazgo, no PARO.
- [LEÍDO] El detalle por momento vive en `forense/analisis/astra4-relevo/cotejo-documental-catalogo.md` (tabla, filas «momento 09 / 0184» … «momento 22 / 0197») y en `forense/analisis/astra4-relevo/plan-catalogo-23.tsv` líneas 10–23 (columnas dependencia/operacion).
- [LEÍDO] `milpa/catalogo-momentos-v0_1.tsv` M09–M22: todos HOLDOUT, nivel persona, instrumento POR DECLARAR, estatus NO-VERIFICADO.
- [EJECUTADO] `consulta.py result RES-0184..0197`: 14 × valor=PENDIENTE, CORR-0085, estado PENDIENTE.

## Momento 19
- [LEÍDO] `forense/hitoD-preregistro-v2_0.md` 265–277 (regla R8.3) y 1183 (veredicto A archivado); `forense/hitoD-R8_3-abridor-v1_0.md` §1–2. El abridor responde unidad (persona), universo (WVS7 México 2018) y disparador (puente × enforcement), pero no es RESULT GEN2 (sin CALC/sello): EXISTE-NO-SATISFACE; sucesor natural = CALC GEN2 de reproducción desde WVS7 en corpus.

## Red
- [EJECUTADO] Proxy de egreso: inegi.org.mx 200; datos.gob.mx, www.gob.mx, zenodo.org, dataverse.harvard.edu, banxico.org.mx, cses.org, coneval.org.mx rechazados (CONNECT 403 / 000). Ningún payload bajado; `data/raw/obtencion-previa-1/p2/` queda vacío.
- Búsquedas (WebSearch) y términos: en la columna `terminos` del TSV. Todo lo hallado por búsqueda queda SIN-FETCH.
