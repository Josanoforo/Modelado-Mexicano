# Recibo técnico solicitado a Claude · ASTRA6-C3-GENETICA-GENOMICA-1

**EJECUTADO.** Dos homónimos v2 completos: [genética/conducta](../../../../corpus/reports-v2/Genetica_y_Conducta_del_Mexicano_Contemporaneo__Canal_Individual_vs__Estructura.md) y [genómica poblacional](../../../../corpus/reports-v2/Mexican_Population_Genomics__2025-2026_Scientific_and_Market_Opportunity_Update.md). El [índice local](indice-local.md) enlaza la tabla, decisiones, síntesis y hoja propuesta. Ambos v1 permanecen intactos. El producto separa asociación, mecanismo, predicción, validez y utilidad clínica, autorización y mercado. Ninguna frecuencia genética se convierte en parámetro de conducta.

**EJECUTADO.** La tabla derivada cubre 71 identidades del mapa (38 conducta, 33 genómica) exactamente una vez y añade siete afirmaciones materiales del v1: 78 registros editoriales con 6 CONFIRMA, 36 MATIZA, 12 ROMPE y 24 SIN-CIFRA. `SIN-CIFRA` distingue adquisición, instrumento o no comparabilidad. Cero `RESULT` genético, mediciones, celdas, adopciones o cambios en CALC, mapa, catálogo, motor, manifiesto y CI. La firma «Acordado» de misión/adenda se cita desde el asiento del 26/sep en `forense/encargos/2026-09-26-ASTRA6-C3-CONSUMO-FAMILIA-1.md` §2; no se duplica.

| Objeto | SHA-256 |
|---|---|
| Report v2 genética/conducta | `fdf4075eb8e830c5ea5eb6bbf75f708db7ffeb15d8fa8f6ab439812842c92281` |
| Report v2 genómica | `1c71c6abf69dc0ca75a4c65cb63148f4a0d0284ce5efa9685b9532cf38f453ee` |
| Tabla `tabla-afirmaciones.tsv` | `4a53dd8c0fe57a9cd77582bbf5d25b1f27b9dc23dc44549d7c185f2edde5bb8d` |
| Decisiones de conducta | `0c2fa02b4e5faf81c20532588730c4825936b7b90c3d1b75fdfd7daaf361f776` |
| Decisiones de genómica | `290b9f7c4b9b377a82d1014a848df9aa01ec18bb851ff99546319933ad4c6032` |
| Encargo recibido, bytes antes del cierre | `63005824c52312a0a44999405908a14883323661a7955c35c618b1e6d6129824` |
| Sello normalizado del cuerpo | `ef1bfbf92404ba82df64ffb6b75bfef731d4e35a0b35aa5ff544dee5ca437028` |

**LEÍDO.** Fuentes primarias dirigidas incluyen Holmes/ADH1B, Lerman/NMR, Borrego-Soto/CYP2A6, el estudio intrafamiliar MCPS 2026, MXB/MexVar, MUC19, la decisión FDA K260235 y la ley mexicana de datos vigente con reforma de noviembre de 2025. Los reports y fichas distinguen artículos completos, abstract y referencias v1 no cotejadas. La autorización FDA de CellDx-Tissue es específica para perfilado tumoral; no prueba la alegación de supervivencia. Las cifras comerciales IMARC se identifican por edición y quedan como estimación no auditada, no ingresos observados.

**EJECUTADO.** Comandos:

```text
git hash-object corpus/reports/<cada original>
python3 tools/sella_sha256.py --cuerpo --verifica forense/encargos/2026-09-27-ASTRA6-C3-GENETICA-GENOMICA-1.md  → SELLO_COINCIDE
python3 forense/analisis/reports-v2/genetica-genomica-1/produce.py             → VERDE
python3 forense/analisis/reports-v2/genetica-genomica-1/verifica.py             → PASS, errores=[]
python3 tests/check.py --baseline --parallel | tail -n 30                       → exit 0, sin FAIL nuevos frente a baseline
git diff --check                                                              → sin errores
```

**LEÍDO / reserva.** El verificador prueba identidad, trazas existentes, enlaces locales y actualidad de tabla/hash; no sustituye la revisión científica del significado de una fuente. No se abrió microdato reservado ni dataset genómico individual. Algunas cifras históricas del v1 y contratos, métodos comerciales o registros institucionales carecieron de fuente primaria recuperable: las afirmaciones se retiraron o acotaron sin convertir ausencia en refutación. La comparación causal universal entre estructura y genética sigue no identificada.

**PROPUESTO-POR-EJECUTOR.** Siete reglas para consideración de mesa en la [hoja](hoja-reglas-propuestas.md), con consumidor, tier y falsador. Recomendación: recibir los reports como revisión editorial con sus límites y conservar reglas en propuesta hasta decisión de contenido. Este documento solicita `GEN2-RECIBO-ASTRA-PRODUCTO-N`; no acredita un recibo independiente ni autorización de fusión.

## NO-VERIFICADO / sucesor

| Objeto | Límite | Sucesor |
|---|---|---|
| Utilidad clínica de paneles, PRS y biomarcadores en México | Frecuencia, asociación o ensayo importado no estiman beneficio local | Validación prospectiva con indicación, comparador, calibración y desenlace |
| Estimación comercial histórica y afirmaciones de proveedores | Método/contrato o desenlace auditado no accesible | Documento primario de edición y resultados verificables |
| Recibo independiente y firma de contenido | Circuito de mesa pendiente | Claude revisa el PR; mesa decide recepción, adopción y fusión |
