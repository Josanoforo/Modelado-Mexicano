# Recibo Codex → Claude · ASTRA5-U2 ENDIREH completo

**PR sucesor borrador [#1099](https://github.com/Josanoforo/Modelado-Mexicano/pull/1099)** · rama `codex/astra5-genero-endireh-sucesor-1` · worktree `/home/pc0/mm-astra5-genero-endireh-sucesor-1`. Partió de `origin/main` `6a2cd6c7` tras #1093 e integró después `origin/main` `72595501` mediante merge; los commits de spec previa a cálculo y de primer sello no se reescribieron. #1099 no se fusionó.

## EJECUTADO

- Los nueve CALC sellados de #1093 se leyeron por resultado, código, tabla, matriz y replay sin volver a medirlos. Se completaron seis CALC: 2021 pareja no física A/B/C y ayuda/denuncia B/C, 2021 empleo 8.3; 2016 ámbitos/servicios/economía y empleo 7.3; 2011 A/B/C; 2006 MC/MD/MS. El intento 2006 0001 falló sin sello por acceso a una conducta exclusiva de MC; la versión 0002 preservó esa historia y produjo el primer resultado exitoso.
- [Seis tablas](2026-09-23-endireh-matriz-y-pendientes.md) con 6,617 celdas (6,008 publicables; 609 suprimidas), IC95 de diseño, 200 réplicas agregadas por celda publicable, soporte y hash. [Matriz](endireh-matriz-conducta-ola-ambito.tsv) de 365 dictámenes; [registro de cierre](endireh-registro-cierre.tsv) por CALC/RESULT/sello. Los seis `verify` dieron **REPRODUCE, CONTEXTO=IDENTICO** y tienen asiento REAL en `forense/replay-evidencia.tsv`.
- [Dictamen 2003](endireh-2003-dictamen-documental.md): diseño oficial sí documentado, pero falta asignación UPM/estrato por fila o pesos replicados del CSV público. Sin tabla 2003 bajo el contrato de IC; no se añadió una quinta ola comparable. Cinco FP abiertas de mesa y tres NC abiertas en registros formales con operación exacta.
- Las pruebas sintéticas nuevas pasan **18/18**. Guardia posterior a integrar main: **105 ejecutadas, 71 saltadas, 0 fallidas**. `python3 tests/check.py --baseline`: **VERDE, 0 FAIL nuevos, 3 heredados**. `git diff --check` limpio.

## LEÍDO Y REPORTADO

Encargo original, corpus/manifiesto por alias, cuestionarios y FD de cinco olas, diseño muestral oficial 2003, los nueve RESULT de #1093 y contrato U0 GEN-001. El contraste U0 es limitado: los componentes de violencia y discriminación se miden por población y ventana; el agregado 70.1% no se reprodujo ni se obtuvo sumando ámbitos. Ayuda/denuncia no estima subregistro total. No hay IC predictivo calibrado, inferencia causal, adopción ni adjudicación de psicología/cultura/genética a grupos. Estado de los RESULT: **sellados en disco, no registrados** hasta canal de publicación y firma de mesa.

## NO-CORRIDO / RESERVAS

- `NC-260923-ASTRA5-U2-ENDIREH-6a2c-01`: tabla 2003 con IC, pendiente de llave oficial por registro para UPM/estrato o pesos replicados y documentación del factor actualizado.
- `NC-260923-ASTRA5-U2-ENDIREH-6a2c-02`: serie homologada, calibración y contraste de cambio, pendiente de actos/denominadores homologados y transición independiente.
- `NC-260923-ASTRA5-U2-ENDIREH-6a2c-03`: unión oficial 70.1% y subregistro total, fuera del estimando de las tablas; exige spec nueva por mujer y, para subregistro, validación externa.
- ENCO, ENVIPE 2026 y la ola ENOE reservada no se abrieron. Ninguna reserva ENDIREH explícita impidió las mediciones 2006–2021.

## CONSUMIDO · saldo

La [nota de cierre](../../../notas/2026-09-23-ASTRA5-U2-ENDIREH-sucesor-cierre.md), [ADR raíz](endireh-adr-raiz.md) y [FP/NC](endireh-fp-nc.md) contienen evidencia y límites. El universo pendiente enumerado tras #1093 queda cubierto por medición o dictamen concreto; 2003 conserva dependencia externa, y la publicación/adopción conserva cinco firmas pendientes. Los contadores finales tras integrar main son 228 corridas selladas, 65,586 RESULT GEN2 sellados y 219 celdas validadas. Mesa revisa #1099; no se solicitó ni ejecutó merge.
