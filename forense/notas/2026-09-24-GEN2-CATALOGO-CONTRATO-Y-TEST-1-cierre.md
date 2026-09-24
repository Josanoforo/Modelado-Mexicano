# Nota de cierre · ACTO GEN2-CATALOGO-CONTRATO-Y-TEST-1 · 24/sep/2026

Cero mediciones. No adopta, no releva ninguna llave, no escribe el catálogo ni procedencia. Contadores sin mover en main.

## ARRANQUE
- Clon `/home/user/Modelado-Mexicano`, rama `acto/gen2-catalogo-contrato-y-test-1` (la del encargo), creada desde origin/main `3252aae`. Segundo acto en serie de la sesión; mesa: «Ambos, en serie». El primero (ADOPCION-3) quedó en PR #1114, rama `claude/new-session-9bylha`, sin archivos compartidos salvo TSV de gobierno (append).
- SHA de redacción `3d138c66`, ancestro de la base; main se movió (#1111–#1113), sin tocar el perímetro.
- Entorno: hook `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, archivos_examinados=0. Cero microdato.
- Ya hecho: `git ls-remote --heads origin | grep -i catalogo` → 0; PR abiertos ADOPCION/CATALOGO → 0.

## P1 · La contradicción, con las dos citas
1. **Contrato** (`forense/analisis/astra4-relevo/contratos-otros-consumidores.md` § Catálogo, versión de `3252aae`, l.44-52): «Un CALC no modifica el catálogo; la operación revisable es una **cita lateral** por `Mxx` con RESULT, CALC, sello y rol. El adaptador propio rechaza cualquier cambio de … bytes del catálogo sellado.»
2. **Test** (`tests/check.py`, bloque (c) de `t35_repro`, l.7716-7733 en `3252aae`): compara `u["valor_materializado"]` contra `destino["valor"]` del RESULT con `_compara_adopcion`; si no casan, `fail("T-REPRO", "(c) … valor materializado … != …")`.
3. **De dónde sale el valor materializado de un momento** (`tools/corrida0.py`): `_consumidores_momentos` (l.644-646) fija `valor_legacy=NO_DECLARADO`; `_ids_corrida0_declarados` (l.3198) solo lee `tramite.yaml` y `procedencia.yaml`; y el camino del pin (l.4481-4495) copia al consumidor ese mismo `valor_legacy`.

**Veredicto de P1:** la hipótesis [SUPUESTO] de dirección se **refuta en su mecanismo** y se **confirma en su efecto**. T-REPRO(c) no compara contra el valor legacy GEN1 del catálogo — ese valor no existe: compara `'NO-DECLARADO-EN-EL-REGISTRO'` contra el RESULT (texto literal del FAIL de ADOPCION-1, nota de ADOPCION-1 l.22-26). M08 no falla por la unidad DELITO; falla porque el catálogo no tiene dónde materializar una cifra. Por eso la cita lateral nunca puede pasar, y el test protege exactamente lo que dirección supone (que el consumidor lleve la cifra del RESULT). No aplica la rama «basta aceptar la cita lateral»: aceptarla sería aceptar cita sin valor (PARO b). La dirección de §1 aplica sin pregunta a mesa.

## P2 · Test y contrato coherentes
- `tools/corrida0.py`: `_marcas_catalogo()` lee columnas de relevo añadidas al final del catálogo (`valor_gen2, corrida0_resultado_id, corrida0_generacion, calc_gen2, sello_gen2, discrepancia_gen1`), con la misma llave de consumidor que la demanda. Cita incompleta (RESULT sin CALC o sin sello) no cuenta como cita. Hoy el catálogo no trae las columnas: cero marcas, cero cambio en el registro real.
- `tests/check.py` T-REPRO(c): nuevo rechazo «valor sin cita completa» para momentos. `(c)` valor == RESULT no cambió; exigencia no baja: hoy ninguna forma pasaba; ahora pasa solo valor + cita completa + valor igual.
- Contrato § Catálogo enmendado (fechado, no reescrito el resto).
- Tests nuevos en `tests/test_corrida0.py` (catálogo temporal; el real no se escribe):
  - positivo `t_catalogo_m08_valor_y_cita_pasa`: M08 con valor `0.7909064453831163`, cita completa y `discrepancia_gen1 = NO-REPRODUCE-GEN1: unidad DELITO` → T-REPRO sin FAIL para el catálogo. **Es la reproducción de M08 en rama pedida en el «Hecho».**
  - negativo `t_catalogo_valor_sin_cita_falla`: valor sin cita → `(c) … sin cita completa`; cita sin sello → `(d)` + `(c)`.
  - negativo `t_catalogo_cita_sin_valor_o_valor_distinto_falla`: cita sin valor → reproduce literal el FAIL de ADOPCION-1 (`'NO-DECLARADO-EN-EL-REGISTRO' != RESULT`); valor `0.78` → `(c) … !=`.

**Reserva (no bloquea):** la vara de adopción usa el grano del literal materializado (`_tol_adopcion_de`); un `valor_gen2` escrito con 2 decimales (`0.79`) pasaría contra `0.7909…`. El escritor (ADOPCION-4) debe escribir el valor a precisión completa; queda en NC para ese acto.

## P3 · Procedencia (propuesta, sin implementar)
`FP-260924-GEN2-CATALOGO-CONTRATO-Y-TEST-1-23e3-01`, texto en el contrato § Procedencia, marcado PROPUESTA. (a, recomendada) campos `corrida0_resultado_id`, `corrida0_generacion`, `clase_respaldo` en la propia entrada de `procedencia.yaml` (el registro ya lee los dos primeros ahí); (b) sidecar TSV de citas. Firma para (a): «Procedencia lleva la cita GEN2 en la propia entrada: corrida0_resultado_id, corrida0_generacion: GEN2 y clase_respaldo junto al valor; la escribe solo el escritor (ADOPCION-4).»

## P4 · Celdas-D (estado, no deuda)
`corrida0.py status`: `legacy_activas_por_consumidor__celdas_D=6`. `grep -rlE sucesor data/curacion-registro/celdas-d/` → 0 de 21 archivos examinados. Estado: las seis referencias de código no tienen sucesora adjudicada; el contrato (§ Celdas-D) exige una propuesta de sucesora con hash nuevo, que ningún acto ha emitido.
