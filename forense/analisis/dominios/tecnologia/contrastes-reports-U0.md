# ASTRA5 U4 · contraste de afirmaciones U0

La unidad de contraste es el componente observable de una afirmación del
report original (`U0`), no su tesis causal completa. Las fuentes primarias
de medición son INEGI ENDUTIH y MOCIBA; los reports son el objeto contrastado.
Los puntos/IC y sus hashes están en `tabla-principal.tsv`, que enlaza a cada
RESULT sellado. Los juicios propuestos no constituyen adopción: decide mesa
por merge. Tier = fuerza de evidencia **para el componente observado**.

| U0 del report | Componente observado y contraste | Juicio propuesto | Tier y falsador |
| --- | --- | --- | --- |
| Tecnología, `corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md` §Key Findings 3: 83.1% usó internet en 2024 y persiste brecha territorial | ENDUTIH 2024, `RESULT-ENDUTIH-PISOS-2024-TABLA`: 83.12% 6+ [82.66,83.59]; TLOC 100 mil+ 88.90% frente a <2,500 69.96%. | **CONFIRMA** el componente de uso y brecha observados. **Sin contraste directo** de que la estructura sea el «techo» causal, ni de población indígena, biometría o confianza. | **SÓLIDO** para prevalencia por localidad, fuente primaria mexicana. Falsaría el componente territorial un contraste de dominios equivalentes con IC de diseño que eliminara o invirtiera la brecha. Falsaría la causalidad sólo un diseño que identifique oferta frente a preferencias. |
| Tecnología, misma sección: entre no usuarios de internet habría barreras de alfabetización y no mera actitud | ENDUTIH 2024, 10,840 no usuarios muestrales: `P7_2=1` acceso 9.29%, `=4` recursos 10.77%, `=3` no interés/necesidad 16.55%, proporciones ponderadas entre no usuarios. `P7_2=2` (no sabe usarlo) no está en este CALC. | **MATIZA** sólo el reparto de motivos observado: coexistencia de acceso, costo y respuesta de interés. **Sin contraste directo** del peso de alfabetización o su causa. | **SÓLIDO** para categorías declaradas, **INDETERMINADO** para mecanismos. Falsador: mismo reactivo con desglose de habilidad, oferta y preferencia validado por dominio, o evidencia de clasificación errónea de `P7_2`. |
| Juventud, `corpus/reports/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md` §Key Findings 3: alto uso digital juvenil desigual | ENDUTIH 2024, 18–29: 96.50% [95.96,97.05] usó internet frente a 83.12% 6+ total. El report cita 18–24 y horas diarias, que este CALC no mide; 18–29 tampoco coincide con convención juvenil 15–29. | **MATIZA** el componente de alto uso para 18–29; **sin contraste directo** para horas, competencia instrumental ni cohorte generacional. | **SÓLIDO** para uso observado, **INDETERMINADO** para competencia. Falsador: microdato con 15–29/18–24, habilidades medidas y contraste de localidad que revierta la diferencia. |
| Sanción social, `corpus/reports/Sanción_Social_Horizontal_en_México__Chisme__Envidia_y_Mal_de_Ojo_como_Mecanismos_de_Nivelación.md` §Patrón 5: la funa digital amplifica sanción horizontal | MOCIBA 2016/2017 mide exposición a acoso y acciones de víctima. No pregunta por chisme, envidia, «funa», sanción por sobresalir ni intención del agresor. | **Sin contraste directo**. La prevalencia de acoso no se convierte en aceptación cultural ni mecanismo de nivelación. | **INDETERMINADO** para la tesis; evidencia primaria mexicana sólo para exposición. Falsador pertinente: reactivos representativos sobre motivo reputacional y contexto de sanción, diferenciando crítica legítima. |
| Tecnología §Patrón 2, gobierno digital coercitivo; ENDUTIH como posible proxy | `P7_35_4` = realizar trámites del gobierno por internet en 12 meses entre usuarios de internet de tres meses: 17.17% 2024. No hay marcador de obligatoriedad, sanción o riesgo fiscal. | **Sin contraste directo** de coerción o miedo fiscal. | **SÓLIDO** para actividad declarada y **SIN-EVIDENCIA** para coerción. Falsador: un reactivo que pregunte obligatoriedad y razón de uso/no uso en el mismo universo. |

La comparación con ENCIG/ENIF es conceptual; no se concatenan registros de
instrumentos distintos ni se fabrica un panel. Oferta de conectividad se
prioriza como explicación a probar antes de atribuir no uso a preferencia.
No se deduce causalidad de asociaciones univariadas, no se extrapola de
jóvenes conectados a toda la juventud, y ninguna genética poblacional
predice conducta de un grupo.

**Auditoría de rigor extremo.** Hay dos saltos especialmente peligrosos:
(1) convertir `P7_2=3` en «resistencia cultural» sin observar oferta ni
habilidad, y (2) convertir una víctima MOCIBA en evidencia de «funa».
Ambos quedan excluidos del juicio. Los IC sólo describen incertidumbre de
muestreo según diseño aproximado; no validan un mecanismo causal ni una
predicción para la siguiente ola.
