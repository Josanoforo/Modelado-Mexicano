# ASTRA5-U5 · lote documental independiente 1

Fecha: 2026-09-23. Rama propia `codex/adq-astra5-u5-20260923`, base `origin/main` `6a2cd6c7`. Consumida la hoja `forense/analisis/dominios/hoja-adquisicion.md` de #1079 en `codex/astra5-mapa-dominios-1` (HEAD `4270328c`) y su contrato TEC-010/MER-004..007. El registro es documental; no contiene cálculos ni adopciones.

Los cinco archivos ya estaban físicamente en `/home/pc0/mm-corpus/raw`. Se buscaron id, nombre y SHA en `data/manifiesto.yaml` de la base antes del alta: cero coincidencias. Se recalcularon SHA256 y bytes sobre cada archivo. La copia de ENADID había sido leída por U0; las cuatro altas ENIGH/ENCIG fueron preparadas por U0 en `codex/astra5-mapa-dominios-1` fuera de su perímetro de solo lectura y se transfieren aquí conservando su autoría, fuente y fecha. No se borra el registro previo de U0.

| Consumidor/pregunta | id · archivo · versión | Fuente primaria y licencia leída | SHA256 físico · bytes |
|---|---|---|---|
| U4/U0 TEC-010: universo, factor y varianza para autoadscripción P3_12 por edad/sexo ENADID 2023 | `enadid2023_diseno_muestral_pdf` · `889463916413.pdf` · diseño ENADID 2023 | [INEGI, diseño](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463916413.pdf); términos INEGI | `546b6b1b832ff5e7abe8e93b2139ce867d24ed121d0158e4a7bc2f1838b4f883` · 1581078 |
| U0 MER-004..005: fuente publicada del Gini ENIGH 2024 con/sin transferencias | `enigh2024_reporte_resultados_pdf` · `enigh2024_reporte_resultados.pdf` · reporte 23/25 | [INEGI, reporte](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/enigh/ENIGH2024_RR.pdf); términos INEGI | `6b091e2d640b6682ca568203637d2a327fbcae950ba7ef66c441c5970568903d` · 1150732 |
| U0 MER-006..007: universo urbano 18+, diseño y expansión ENCIG 2025 | `encig2025_diseno_muestral_pdf` · `encig2025_diseno_muestral.pdf` · diseño ENCIG 2025 | [INEGI, diseño](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463930778.pdf); términos INEGI | `de74a89623696e54e2d409a5cb5ae2b41dcd54a73c9deef1102b5793d875175e` · 1343631 |
| U0 MER-006: pregunta de percepción frecuente de corrupción ENCIG 2025 | `encig2025_boletin_pdf` · `encig2025_boletin.pdf` · comunicado 21-may-2026 | [INEGI, boletín](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/encig/ENCIG2025_CP.pdf); términos INEGI | `6515cb698a8a7f0821a225827ac2402d06cd6405cabf76208f0d6c529b29eaa4` · 329663 |
| U0 MER-007: escala de confianza federal ENCIG 2025 | `encig2025_principales_resultados_pdf` · `encig2025_principales_resultados.pdf` · presentación 51 pp. | [INEGI, presentación](https://www.inegi.org.mx/contenidos/programas/encig/2025/doc/encig2025_principales_resultados.pdf); términos INEGI | `476cf06ee8cb18727f2326c0d80e5f113ca3554a0851f89f3414ab1a03113548` · 970921 |

[Términos de Libre Uso del INEGI](https://www.inegi.org.mx/inegi/terminos.html) leídos el 23/sep/2026: permiten copia y difusión conservando metadatos, con crédito al Instituto y distinción de transformaciones propias. El manifiesto registra el URL de cada versión. `tests/manifiesto.py --verifica` informa AUSENTE para estos cinco en la raíz local `data_raw` de este worktree, que apunta fuera del corpus compartido; la comparación física se hizo contra `/home/pc0/mm-corpus/raw` y coincide en los cinco. El resultado AUSENTE no se presenta como COINCIDE.

## Recibos por consumidor

- **U4, TEC-010:** puede consumir `enadid2023_diseno_muestral_pdf` junto a cuestionario, FD y dato ya registrados; el registro no habilita una medición ni equivale a P3_12 de lengua hablada.
- **U0, MER-004..007:** puede consumir los cuatro ids ENIGH/ENCIG al actualizar #1079. El boletín ENOE 2026T1 consultado por U0 queda excluido de esta alta; U0 debe registrar su exposición, sin solicitar autorización retroactiva de adquisición.

## No corrido y reservas

No se abrió ZIP de microdato, no se accedió de nuevo a ENOE 2026T1 ni ENVIPE 2026, y no se consultó material de resultados reservados. La decisión CED que U0 conservó en HTML requiere condiciones de reproducción precisas antes de alta; permanece con su SHA y ubicación originales en la hoja de #1079. No se elimina esa evidencia. ENDIREH 2006/2011 y diseño 2003 se atienden como lote documental separado.
