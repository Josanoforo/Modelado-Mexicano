# Nota · ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4 · diff seco antes de `--apply`

## ARRANQUE
- Clon `/home/user/Modelado-Mexicano`, rama propia `acto/gen2-adopcion-bloque-y-pines-4` (0-bis en `1ad0d01d`, push inmediato).
- Base al día: `git rev-list --count HEAD..origin/main` → 0 tras `git fetch --prune` (HEAD ya coincidía con `origin/main`, `b64fff55`, PR #1115 · GEN2-CATALOGO-CONTRATO-Y-TEST-1). SHA de redacción `3252aaec` es ancestro (main avanzó un merge, GEN2-ADOPCION-BLOQUE-Y-PINES-3/#1114 + GEN2-CATALOGO-CONTRATO-Y-TEST-1/#1115); `git diff --stat 3252aaec..b64fff55` no toca `milpa/tramite.yaml` ni `tools/escribe_relevo_consumo.py` — el perímetro de este acto sigue intacto.
- Duplicado: `git ls-remote --heads origin | grep -i adopcion` → 0 filas nuevas; `git worktree list` → 1 (este); `search_pull_requests(is:pr is:open adopcion)` → 0. `tools/limpia_arbol.py --reporta`: 1 worktree, rama local fusionada = la propia, base al día.
- Entorno: `ENTORNO-DERIVADO = NUBE` (coincide con lo declarado por el encargo), corpus montado=NO, archivos_examinados=0, red denegada por política. Este acto no toca microdato.
- `data/raw`: ausente (no aplica — el acto no abre microdato).

## Premisa verificada (la que PINES-3 dejó como PARO-PREMISA)
`grep -c '^  - id:' milpa/tramite.yaml` → 22. `grep -c` de las tres conductas (`contexto_institucional_alto`, `atraso_credito`, `atraso_tarjeta`, `valora_afirmativamente`) → 0 las cuatro. Las tres reglas viven en `milpa/tramite-ola5-propuesta-v0.yaml` líneas 3985-4090, con `p`/`corrida0_resultado_id` verificados contra `data/corrida0/resultados.tsv` (vía `tools/vista.leer_resultados_join`) — coinciden EXACTO para los diez RESULT que sí tienen `p` (la conducta `contexto_institucional_alto_2021` es `p: null`/NO-ESTIMABLE y no se vuelve consumidor, mismo criterio que `tools/corrida0.py::_consumidores_conductas`).

`grep -c 'PROPUESTO-POR-EJECUTOR' milpa/tramite.yaml` → 0 antes de este acto.

## P1 · Escritor extendido — modo «crear desde propuesta»
`tools/escribe_relevo_consumo.py --crear-desde-propuesta` (sin `--apply`): copia VERBATIM (por texto, línea a línea — nunca re-serializado por PyYAML) el bloque `entonces:` y el resto de campos medidos (`fuente`, `ola_calibracion`, `ic95`, `n`, `ponderador`, `universo`, `sha256_payload`, `payload_manifiesto_id`, `escala_costo_percibido`, `preregistro_estimandos`, `spec`, `medido_en` — los que cada bloque de la propuesta trae; no los tres traen el mismo subconjunto, y el escritor no asume un esquema fijo). Los cuatro campos pendientes (`situacion`, `si.disparadores`/`disparadores_estado`, `porque`, `tier`, `falsable_si`) se redactan desde `forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml` y se rotulan `PROPUESTO-POR-EJECUTOR` en el propio YAML (comentario en línea) y aquí.

Autoverificación mecánica del propio escritor antes de imprimir el diff (falla cerrado, `ValueError`, si cualquiera no se sostiene):
1. Las tres reglas no están ya presentes en `milpa/tramite.yaml` (si lo estuvieran, no se re-crean).
2. Por cada conducta con `p` no nulo: el `p` de la propuesta identifica EXACTO al valor sellado en `resultados.tsv` para su `corrida0_resultado_id`; `corrida0_generacion == GEN2`; `rol_uso == proxy_descriptivo`.
3. El archivo resultante se carga con `milpa.src.emisor.cargar_reglas` (el mismo cargador que usa el motor) sobre un temporal — nunca sobre el archivo real hasta `--apply` — y el `p`/`corrida0_resultado_id` que el cargador interpreta de cada conducta coincide EXACTO con el de la propuesta (atrapa un error de indentación silencioso en el corte del bloque).
4. Ningún campo redactado trae comillas rectas sin escapar (se usan comillas angulares « » en la redacción; ver cabecera de `redaccion-reglas-v1_0.yaml`).

Las cuatro pasaron. `tests/test_escribe_relevo_consumo.py` (11 tests, datos sintéticos — no el `tramite.yaml` real, que tras `--apply` ya no podría ejercitar la ruta de creación) → VERDE.

## Diff seco (`--crear-desde-propuesta`, sin `--apply`)

```diff
--- a/milpa/tramite.yaml
+++ b/milpa/tramite.yaml
@@ -1626,3 +1626,117 @@
       total_descriptivo: {p_horizonte_corto: 0.520528, ic95: [0.507667, 0.533833], nota: "razón directa con diseño; no promedio de tasas"}
     sha256_payload: "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039"
     payload_manifiesto_id: enif_2024_enif_2024_bd_csv
+
+  # ══════════════════════════════════════════════════════════════════
+  # ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4 · 24/sep/2026 · regla nueva, copiada VERBATIM
+  # (texto, no re-serializada) de milpa/tramite-ola5-propuesta-v0.yaml
+  # (líneas 3985-4025; OBJETO 8 de la HOJA DE FIRMAS DE MESA 2026-09-15 (NC-0167), firma «Si a todas.», ACTO GEN2-FIRMAS-MESA-1, 15/sep/2026): `entonces:`/`fuente`/el resto de campos medidos,
+  # carácter por carácter -- ningún `p` ni cita de RESULT se retoca.
+  # Promoción al motor vivo autorizada por FIRMAS-7 (…369b-01, 21/sep/2026, bloque de diez RESULT ADOPTADOS) + Decisión 2 de ADOPCION-2 (W, 24/sep/2026: INTERPRETACIÓN-DECLARADA -- «regla existente» presuponía un hecho falso, la intención se preserva creando la regla) + cláusula de autonomía v1.0 (mesa, 24/sep/2026, forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md §3).
+  # `situacion`/`si.disparadores_estado`/`porque`/`tier`/
+  # `falsable_si` son PROPUESTO-POR-EJECUTOR
+  # (forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml); mesa
+  # los adopta o corrige al fusionar este PR (E.2).
+  # ══════════════════════════════════════════════════════════════════
+  - id: civico.contexto_institucional_victimas.lapop
+    situacion: victima_extorsion_evalua_contexto_institucional  # PROPUESTO-POR-EJECUTOR
+    si:
+      disparadores: {}
+      disparadores_estado: "PROPUESTO-POR-EJECUTOR: no hay disparador lógico condicional del motor detrás de esta salida -- es tasa base incondicional dentro del universo ya seleccionado y declarado en `universo:` («víctimas de extorsión (vic1ext = 1) con ponderador válido en la ola»), mismo patrón que `civico.denuncia.miedo_desconfianza` y `dinero.ahorro.tiene_ahorros` en este archivo."  # PROPUESTO-POR-EJECUTOR
+    entonces:
+      - {conducta: contexto_institucional_alto_2019, p: 0.7862745098039216, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-CTX-2019-P-ALTO, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO del contexto institucional entre víctimas de extorsión (vic1ext=1) en la ola LAPOP 2019: sólo consulta descriptiva, escenario o baseline dentro de ese universo; no es tasa general de la población, no es probabilidad empírica por evento, no falsa R10.3 ni construye el veredicto D2-h, y no se compara ni se agrupa entre olas"}
+      - {conducta: contexto_institucional_alto_2023, p: 0.7341176470588235, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-CTX-2023-P-ALTO, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO del contexto institucional entre víctimas de extorsión (vic1ext=1) en la ola LAPOP 2023: sólo consulta descriptiva, escenario o baseline dentro de ese universo; no es tasa general de la población, no es probabilidad empírica por evento, no falsa R10.3 ni construye el veredicto D2-h, y no se compara ni se agrupa entre olas"}
+      - {conducta: contexto_institucional_alto_2021, p: null, clase: "NO-ESTIMABLE·indice-incompleto",
+         corrida0_resultado_id: RESULT-CTX-2021-P-ALTO, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO sin estimación: la ola LAPOP 2021 no entrega el índice (falta `aoj12`, NO-ESTIMABLE-INDICE-INCOMPLETO). Se declara para que el hueco quede a la vista y nadie lo rellene por interpolación entre 2019 y 2023; no es tasa, no es probabilidad por evento, no falsa R10.3 ni construye el veredicto D2-h"}
+    porque: {generador: [G4], mecanismo: "Exposición a la extorsión (victimización) reconfigura la percepción de legitimidad/eficacia de las instituciones de justicia entre quienes la sufren -- G4, «Exposición a violencia + impunidad» -> «Conducta defensiva, retracción del espacio público», componente confianza_institucional[justicia] (canon/modelo-decision-v4_0.md línea 440). Evidencia GEN1: la victimización erosiona específicamente la confianza en policía y sistema judicial sin afectar la confianza interpersonal (Corbacho et al. 2015, citado en el report: ~10% de caída en confianza en policía local tras victimización, confianza en amigos/familia ~85% estable)."}  # PROPUESTO-POR-EJECUTOR
+    tier: MEDIA  # PROPUESTO-POR-EJECUTOR
+    falsable_si: "Si una ola LAPOP posterior (o un instrumento con el mismo índice de tres ítems aoj11/b18/aoj12) mide contexto institucional alto entre víctimas de extorsión fuera del rango 73-79% observado en 2019/2023, o si el patrón desaparece al condicionar por región o clase social, el proxy queda falsado como marcador estable del universo."  # PROPUESTO-POR-EJECUTOR
+    fuente: ["LAPOP-AmericasBarometer-MEX-2019", "LAPOP-AmericasBarometer-MEX-2021", "LAPOP-AmericasBarometer-MEX-2023"]
+    ola_calibracion: "tres olas LAPOP (2019, 2021, 2023); 2021 no entrega índice — dos olas con estimación"
+    ic95: [0.75, 0.8230792682926829]   # 2019; 2023 = [0.6843195210395104, 0.782010650766957]; 2021 = null
+    n: "N-UNIVERSO víctimas con ponderador válido: 520 (2019) · 505 (2021) · 428 (2023)"
+    ponderador: "wt (prescrito por la spec y aplicado)"
+    universo: "víctimas de extorsión (vic1ext = 1) con ponderador válido en la ola; nunca agrupadas entre olas"
+    sha256_payload: "c88f79ebb8e73c473cd78d894eb093261f172e736a35bd7bc677b4e8b1454a57"
+    payload_manifiesto_id: mexico_lapop_americasbarometer_2019_v1_0_w
+    spec: "prereg-caja-S13 — forense/prereg-caja/S13-R10-3-spec-v1_0.md, sha256 c41235b804b0834881b7d3467e25ab0b74946fc03ba14245918e9c7a2e69a515; cara local data/corrida0/CALC-0002/spec.yaml"
+    medido_en: "ACTO GEN2-E5 · CALC-0002, 8/sep/2026 — corrida sellada CALC-0002--f57ad1cd8f96, data/corrida0/CALC-0002/resultados.json"
+
+  # ══════════════════════════════════════════════════════════════════
+  # ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4 · 24/sep/2026 · regla nueva, copiada VERBATIM
+  # (texto, no re-serializada) de milpa/tramite-ola5-propuesta-v0.yaml
+  # (líneas 4041-4067; OBJETO 9 de la HOJA DE FIRMAS DE MESA 2026-09-15 (NC-0186 + NC-0164), firma «Si a todas.», ACTO GEN2-FIRMAS-MESA-1, 15/sep/2026): `entonces:`/`fuente`/el resto de campos medidos,
+  # carácter por carácter -- ningún `p` ni cita de RESULT se retoca.
+  # Promoción al motor vivo autorizada por FIRMAS-7 (…369b-01, 21/sep/2026, bloque de diez RESULT ADOPTADOS) + Decisión 2 de ADOPCION-2 (W, 24/sep/2026: INTERPRETACIÓN-DECLARADA -- «regla existente» presuponía un hecho falso, la intención se preserva creando la regla) + cláusula de autonomía v1.0 (mesa, 24/sep/2026, forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md §3).
+  # `situacion`/`si.disparadores_estado`/`porque`/`tier`/
+  # `falsable_si` son PROPUESTO-POR-EJECUTOR
+  # (forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml); mesa
+  # los adopta o corrige al fusionar este PR (E.2).
+  # ══════════════════════════════════════════════════════════════════
+  - id: dinero.credito.atraso_y_dano_por_producto_banxico
+    situacion: tiene_credito_formal_por_producto  # PROPUESTO-POR-EJECUTOR
+    si:
+      disparadores: {}
+      disparadores_estado: "PROPUESTO-POR-EJECUTOR: no hay disparador lógico condicional del motor detrás de esta salida -- es tasa base incondicional dentro del universo ya seleccionado y declarado en `universo:` (tenedores del producto de crédito, corte 2024), mismo patrón que `familia.seguro.volatilidad_ausencia_estado` en este archivo."  # PROPUESTO-POR-EJECUTOR
+    entonces:
+      - {conducta: atraso_credito_hipotecario_2024, p: 0.18510485270103624, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-BANXICO-2024-HIP-ATRASO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO por categoría de producto de crédito (Banxico 2024): sólo consulta descriptiva, escenario o baseline. No es probabilidad empírica por evento, no calibra ninguna p del motor, no identifica un efecto causal y no construye «cualquier daño». Son cambios entre cortes, no transiciones de las mismas personas, y no traen EE/IC porque el diseño necesario no quedó acreditado"}
+      - {conducta: atraso_tarjeta_credito_2024, p: 0.04235936236062071, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-BANXICO-2024-TDC-ATRASO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO por categoría de producto de crédito (Banxico 2024): sólo consulta descriptiva, escenario o baseline. No es probabilidad empírica por evento, no calibra ninguna p del motor, no identifica un efecto causal y no construye «cualquier daño». Son cambios entre cortes, no transiciones de las mismas personas, y no traen EE/IC porque el diseño necesario no quedó acreditado"}
+      - {conducta: atraso_credito_nomina_2024, p: 0.1035233151033609, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-BANXICO-2024-NOM-ATRASO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO por categoría de producto de crédito (Banxico 2024): sólo consulta descriptiva, escenario o baseline. No es probabilidad empírica por evento, no calibra ninguna p del motor, no identifica un efecto causal y no construye «cualquier daño». Son cambios entre cortes, no transiciones de las mismas personas, y no traen EE/IC porque el diseño necesario no quedó acreditado"}
+      - {conducta: atraso_credito_personal_2024, p: 0.08031777453105593, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-BANXICO-2024-PER-ATRASO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO por categoría de producto de crédito (Banxico 2024): sólo consulta descriptiva, escenario o baseline. No es probabilidad empírica por evento, no calibra ninguna p del motor, no identifica un efecto causal y no construye «cualquier daño». Son cambios entre cortes, no transiciones de las mismas personas, y no traen EE/IC porque el diseño necesario no quedó acreditado"}
+      - {conducta: atraso_credito_automotriz_2024, p: 0.04309263821900375, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-BANXICO-2024-AUT-ATRASO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO por categoría de producto de crédito (Banxico 2024): sólo consulta descriptiva, escenario o baseline. No es probabilidad empírica por evento, no calibra ninguna p del motor, no identifica un efecto causal y no construye «cualquier daño». Son cambios entre cortes, no transiciones de las mismas personas, y no traen EE/IC porque el diseño necesario no quedó acreditado"}
+    porque: {generador: [G3], mecanismo: "La volatilidad del ingreso y la ausencia de alternativas formales de suavización de consumo producen atraso recurrente en el pago de crédito, con independencia del producto -- G3, «Informalidad + volatilidad de ingreso» -> «Horizonte corto, ahorro informal, aversión» (canon/modelo-decision-v4_0.md línea 439). Evidencia GEN1: 27.3% de quienes tienen deudas han tenido retrasos en pagos (ENSAFI 2023), con la trampa más fuerte en hogares de ingreso volátil sin colchón."}  # PROPUESTO-POR-EJECUTOR
+    tier: MEDIA  # PROPUESTO-POR-EJECUTOR
+    falsable_si: "Si una ola Banxico posterior (o ENSAFI) muestra que las tasas de atraso por producto ya no covarían con indicadores de volatilidad de ingreso o informalidad -- por ejemplo, convergen entre tenedores formales e informales --, el driver G3 queda falsado para este proxy."  # PROPUESTO-POR-EJECUTOR
+    fuente: ["Banxico-2024", "data/banxico-producto-dano-medicion/ficha-consumo-banxico.md"]
+    escala_costo_percibido: "0-10 percibido (0=bajo, 10=alto) -- NO es CAT, tasa contractual ni monto"
+    preregistro_estimandos: "OBJETO 9 (NC-0164): mesa acepta y PRE-REGISTRA los estimandos Banxico como descriptivos/asociativos por categoría de producto -- cinco categorías de crédito, atraso y daño, corte 2024. Esto cierra el «si la mesa los acepta» del sucesor de NC-0164 en su cara de pre-registro. Lo que NC-0164 deja vivo y este OBJETO no cierra: localizar fuente mexicana con producto BNPL/digital o lender, CAT/tasa/fricción objetiva, daño, negativos y estrategia de identificación causal."
+    medido_en: "ACTO GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO (PR #746) — CALC-BANXICO-PRODUCTO-DANO-0001, 35 RESULT sellados; data/corrida0/CALC-BANXICO-PRODUCTO-DANO-0001/spec.yaml declara uso_motor: DESCRIPTIVO-NO-CALIBRA-NI-ADOPTA"
+
+  # ══════════════════════════════════════════════════════════════════
+  # ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4 · 24/sep/2026 · regla nueva, copiada VERBATIM
+  # (texto, no re-serializada) de milpa/tramite-ola5-propuesta-v0.yaml
+  # (líneas 4069-4089; OBJETO 9 de la HOJA DE FIRMAS DE MESA 2026-09-15 (NC-0186 + NC-0164), firma «Si a todas.», ACTO GEN2-FIRMAS-MESA-1, 15/sep/2026): `entonces:`/`fuente`/el resto de campos medidos,
+  # carácter por carácter -- ningún `p` ni cita de RESULT se retoca.
+  # Promoción al motor vivo autorizada por FIRMAS-7 (…369b-01, 21/sep/2026, bloque de diez RESULT ADOPTADOS) + Decisión 2 de ADOPCION-2 (W, 24/sep/2026: INTERPRETACIÓN-DECLARADA -- «regla existente» presuponía un hecho falso, la intención se preserva creando la regla) + cláusula de autonomía v1.0 (mesa, 24/sep/2026, forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md §3).
+  # `situacion`/`si.disparadores_estado`/`porque`/`tier`/
+  # `falsable_si` son PROPUESTO-POR-EJECUTOR
+  # (forense/analisis/adopcion-4/redaccion-reglas-v1_0.yaml); mesa
+  # los adopta o corrige al fusionar este PR (E.2).
+  # ══════════════════════════════════════════════════════════════════
+  - id: trabajo.prestaciones.valoracion_seguridad_social_motral
+    situacion: ocupado_valora_seguridad_social  # PROPUESTO-POR-EJECUTOR
+    si:
+      disparadores: {}
+      disparadores_estado: "PROPUESTO-POR-EJECUTOR: no hay disparador lógico condicional del motor detrás de esta salida -- es tasa base incondicional dentro del universo ya seleccionado (ocupados, MOTRAL 2015 reactivo P17, con/sin acceso a seguridad social), mismo patrón que `dinero.planeacion.formal_estable` en este archivo."  # PROPUESTO-POR-EJECUTOR
+    entonces:
+      - {conducta: valora_afirmativamente_seguridad_social_total, p: 0.823626705331, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-MOTRAL15-P17-TOTAL-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO de preferencia DECLARADA por seguridad social (MOTRAL 2015, reactivo P17): sólo consulta descriptiva, escenario o baseline. Es una comparación descriptiva, NO una clasificación de informalidad voluntaria; no es probabilidad empírica por evento y no calibra ninguna p del motor. R2.3 trabajo.prestaciones.formalidad_pesa_mas_que_salario SIGUE SIN MEDIRSE de forma estricta y este proxy no la mide"}
+      - {conducta: valora_afirmativamente_seguridad_social_con_acceso, p: 0.832233738, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO de preferencia DECLARADA por seguridad social (MOTRAL 2015, reactivo P17) en el subgrupo CON acceso: sólo consulta descriptiva, escenario o baseline. Comparación descriptiva, NO clasificación de informalidad voluntaria; el contraste con/sin acceso no identifica ningún efecto causal y no falsa R2.3"}
+      - {conducta: valora_afirmativamente_seguridad_social_sin_acceso, p: 0.790530962253, clase: "MEDIDO·p(proporcion ponderada)",
+         corrida0_resultado_id: RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P, corrida0_generacion: GEN2,
+         rol_uso: proxy_descriptivo, uso_motor: "PROXY-DESCRIPTIVO de preferencia DECLARADA por seguridad social (MOTRAL 2015, reactivo P17) en el subgrupo SIN acceso: sólo consulta descriptiva, escenario o baseline. Comparación descriptiva, NO clasificación de informalidad voluntaria; el contraste con/sin acceso no identifica ningún efecto causal y no falsa R2.3"}
+    porque: {generador: [G3], mecanismo: "La divisoria formal-informal organiza el acceso a una red de protección ante el riesgo: quienes carecen de acceso formal no pueden asumir riesgo sin red -- mismo mecanismo G3 (informalidad + volatilidad de ingreso). Evidencia GEN1: incluso los ocupados sin acceso valoran afirmativamente la seguridad social casi tan alto como quienes sí tienen acceso (79.1% vs 83.2%, MOTRAL 2015 P17) -- no hay devaluación defensiva del beneficio que no se tiene."}  # PROPUESTO-POR-EJECUTOR
+    tier: MEDIA  # PROPUESTO-POR-EJECUTOR
+    falsable_si: "Si una ola MOTRAL posterior (o un instrumento equivalente, p.ej. el módulo de informalidad de ENOE) muestra que la valoración de la seguridad social deja de variar con el acceso o la formalidad del empleo -- por ejemplo, ocupados sin acceso la valoran significativamente menos que con acceso, en vez de casi igual --, el driver queda falsado."  # PROPUESTO-POR-EJECUTOR
+    fuente: ["MOTRAL2015", "data/motral2015-valoracion-ss/ficha-uso.md", "data/motral2015-valoracion-ss/ficha-experimento-mexicano.md"]
+    ic95: [0.796632270795, 0.850621139866]
+    n: 5704
+    medido_en: "ACTO GEN2-N35 / MOTRAL (PR #747) — CALC-MOTRAL2015-VALORACION-SS-0001, 42 RESULT sellados; data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001/spec.yaml declara uso_motor: DESCRIPTIVO-NO-CALIBRA-NI-ADOPTA"

```
