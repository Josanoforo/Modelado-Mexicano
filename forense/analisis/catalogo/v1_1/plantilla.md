# Benchmark auditable del comportamiento del mexicano · catálogo v1.1

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-del-mexicano-v1_1.md` (sucesor de `catalogo-del-mexicano-v1_0.md`, que queda intacto — E.1) |
> | **NOMBRE ESTABLE** | `catálogo del mexicano` |
> | **ESTADO** | Producto consultable: solo estimadores adoptados por firma citada por id |
> | **ACTO** | `GEN2-CATALOGO-V1-1-1` · generación GEN2 · cero mediciones nuevas · no adopta: consume adopciones firmadas |
> | **TABLA** | [`catalogo-del-mexicano-v1_1.tsv`](catalogo-del-mexicano-v1_1.tsv) — una fila por estimador adoptado |
> | **REGENERA** | `python3 forense/analisis/catalogo/genera_catalogo_v1_1.py` (esta portada incluida); `--sin-registro` reutiliza la vista de adoptados activos ya derivada |

**{{c:estimadores}} estimadores adoptados con RESULT sellado · {{c:dominios_medidos}} dominios del mapa medidos, en {{c:reports_medidos}} de los {{c:reports}} reports del corpus · {{c:celdas_validadas}} celdas validadas (definición vigente de `corrida0 status`), de las cuales {{c:celdas_validadas_prospectiva}} PROSPECTIVAS y {{c:celdas_validadas_retrospectiva}} RETROSPECTIVAS se reportan aparte.**

**Tesis.** Lo que hoy se puede afirmar sobre el mexicano con cifra propia es **descriptivo y retrospectivo**: cuánto, dónde y en qué segmento, medido desde microdato con su intervalo de diseño. Casi todo el peso del catálogo está en trabajo (ENOE), violencia contra las mujeres (ENDIREH) y tecnología (ENDUTIH, MOCIBA). Ninguna fila es predicción ni efecto causal. Y donde el gradiente es de localidad, escolaridad o formalidad, la primera lectura es de **estructura y oferta**, no de cultura (§3 de las instrucciones).

Contadores que mueve este acto: «estimadores en catálogo con RESULT» (de las filas de v1.0, que censaban lecturas con estado, a {{c:estimadores}} adopciones citadas por FP) y «dominios MEDIDOS» ({{c:dominios_medidos}}). No mueve `adoptados_activos`, `celdas_validadas` ni ningún contador del marcador: los lee.

## Cómo leerlo

1. Cada fila es un estimador **adoptado por una firma de mesa citada por id** en la columna `firma_fp`: un `FP-…` FIRMADO en `forense/firmas-pendientes.tsv`, el objeto de su fila en `data/corrida0/decisiones.tsv` (`decisiones.tsv:<objeto>`) o la firma verbatim de un encargo archivado (`forense/encargos/<archivo>.md#firma …`).
2. `result_id` + `celda` localizan la cifra: en los CALC de pisos, `RESULT-…-TABLA#i` es el registro `i` de la tabla sellada en `data/corrida0/<calc>/resultados.json`. Los hashes de cada CALC están en `forense/analisis/catalogo/v1_1/calcs.tsv`.
3. `unidad`, `eje` y `segmento` gobiernan la lectura. Ninguna cifra de unidad delito o trámite se compara con una de unidad persona u hogar.
4. `estado_adopcion`: `ADOPTADO` o `ADOPTADO-CON-RESERVA-DE-ANCHO` (su IC es calibrado y ancho a propósito: no se llama cobertura). `alcance`: `DESCRIPTIVO-DE-OLA` (piso de una ola, sin uso predictivo), `ESTIMADOR-DE-CELDA` (piso t−1 adjudicado a una celda del marcador) o `PARAMETRO-DE-REGLA` (lo lee una regla del motor).
5. `temporalidad`: todo el catálogo es **RETROSPECTIVA** ({{c:temporalidad:RETROSPECTIVA}} filas). Las celdas PROSPECTIVAS del marcador que existían eran pisos de origen legacy y quedaron fuera (ver «Fuera por regla»).
6. `origen_piso`: `NUEVO` (medido desde microdato en su CALC; {{c:origen_piso:NUEVO}} filas) o `HEREDADO-DE-GEN2` (el punto de la ola t es el piso GEN2 de t−1; {{c:origen_piso:HEREDADO-DE-GEN2}} filas). **Ninguna fila es HEREDADO-DE-LEGACY.**
7. `oferta_exclusion`: en cada fila de `DINERO` va la medida de exclusión por oferta, o la declaración de que no existe una sellada para esa ola y conducta.

## P1 · Estimadores por dominio e instrumento

{{t:dominios}}

**Fuentes, una por firma.**

- **Pisos por instrumento — Firma T** (`GEN2-TRAMITE-FIRMAS-15` §1 T + ADENDA-1): ENOE (`FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01`), ENDIREH 2021, 2016, 2011 y 2006 (`FP-260923-ASTRA5-U2-ENDIREH-6a2c-01` a `-04`), ENDUTIH 2023–2025 (`FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01`: sin las celdas originales de empleo, sustituidas por `CALC-ENDUTIH-EMPLEO-15MAS-*`) y MOCIBA 2015–2017 (`-1f30-02`: 2015 no estimable). Una fila por celda publicable; cada una es piso descriptivo retrospectivo **sin uso predictivo**.
- **Marginales por piso t−1**: ENVIPE 2025 adoptada (`decisiones.tsv:adopcion:piso-t1-marginales-por-instrumento`) y ENIF 2024 **con reserva de ancho** (`FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`, IC calibrado de persistencia: conservador, un solo choque). ENCIG 2025 queda vetada en nivel (fuera).
- **Pisos de salud y bienestar — FIRMAS-16** (`GEN2-TRAMITE-FIRMAS-16`, «ejecuta GEN2-CATALOGO-V1-1-1»): ENSANUT 2021–2024 **con reserva de ancho** (`FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01`; sobre 2024 el IC es el calibrado de persistencia), ENCODAT 2016–2017 **con reserva de ancho** (`-6d56-02`; una sola ola, IC de diseño) y ENBIARE 2021 adoptado como piso de una ola (`-6d56-03`).
- **Parámetros de reglas y celdas R/M del marco** con consumo activo (la misma vista que `corrida0 status`), cada uno con la fila de `decisiones.tsv` de su CALC, su FP o la firma del encargo que lo relevó.
- **Bloque ENIGH — Firma M** (`GEN2-ADOPCION-BLOQUE-Y-PINES-1`): descriptores de intensidad de remesas 2016, 2018 y 2020 con IC bootstrap.

**Ejes.** Sexo, edad, escolaridad, localidad (tamaño) y entidad —el eje regional disponible con RESULT adoptado— salen de las tablas ENOE, ENDIREH y ENDUTIH; formalidad y cuenta, de las marginales ENIF. **NSE entra como eje con reserva de instrumento** (`FP-260924-GEN2-CLASE-AMAI-1-e773-01`, FIRMAS-16): ENIGH 2022 (regla AMAI reproducida), ENIF 2024 (aproximación conforme) y ENDUTIH 2023 como aproximación rotulada; ENDUTIH 2024–2025 (`DESVIADA`) quedan fuera por la letra de la firma ({{c:excluidos:NSE-FUERA-DE-RESERVA-DE-INSTRUMENTO}} celdas). La región de seis zonas de `canon/eje-regional-v1_0.md` es propuesta sin adopción: no aporta filas.

### Pendiente de firma (no entran; no es PARO)

{{t:pendientes}}

`SIN-FP-CITABLE`: RESULT con consumo activo que el contador de adoptados cuenta por la etiqueta de su propia spec (E.2), pero sin FP firmada, sin fila de mesa en `decisiones.tsv` para su CALC y sin firma de encargo en su pin. El catálogo no les inventa firma; esperan `FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01`.

### Fuera por regla

Detalle por llave en `forense/analisis/catalogo/v1_1/excluidos.tsv`:

- Piso **HEREDADO-DE-LEGACY** ({{c:excluidos:PISO-HEREDADO-DE-LEGACY}} RESULT del censo de `GEN2-ENCIG-PISOS-GEN2-1`): re-medidos por `GEN2-PISOS-GEN2-2` (`PR #1123`) con pisos y sucesores `-0002` sellados, **sin adopción firmada**: siguen fuera hasta que mesa los adopte.
- Celdas ENDUTIH originales de empleo excluidas por la propia firma: {{c:excluidos:EXCLUIDA-POR-FIRMA}}.
- Celdas sin punto publicable: suprimidas {{c:excluidos:CELDA-SUPRIMIDA}} + {{c:excluidos:CELDA-SUPRIMIDA-N-MENOR-100}} + {{c:excluidos:CELDA-SUPRIMIDA-N}}, no estimables {{c:excluidos:CELDA-NO-ESTIMABLE-SIN-EST_DIS}}.
- Marginales sin adopción en nivel (ENCIG 2025, vetada): {{c:excluidos:MARGINAL-NO-ADOPTADA}}.
- Tablas ENIGH adoptadas por Firma M y no desagregadas en esta versión (perfil estructural y remesas en contexto): {{c:excluidos:ADOPTADO-TABLA-NO-DESAGREGADA}} CALC. La evaluación de origen móvil del duelo ENIGH ({{c:excluidos:EVALUACION-NO-ESTIMADOR}} CALC) mide error de candidatos, no una conducta.

## P3 · Cobertura de los reports del corpus

Unidad: los {{c:reports}} reports de `corpus/reports/` (el conteo de «dominios» de la ADENDA-2 y del README), cada uno asignado a su dominio primario por `forense/analisis/dominios/report-a-dominio-v1_0.tsv`; los conteos de afirmaciones salen de `canon/mapa-dominios-v1_0.tsv`. Regla, en orden (la primera que se cumple):

- `MEDIDO` — el dominio tiene al menos un estimador en esta tabla.
- `EN-MEDICIÓN` — hay CALC con `cuenta_gen2: SI` sellados para un instrumento del dominio, sin adopción todavía (ENCUP/LAPOP/INE, ENADID, ENCUCI y los demás instrumentos de la regla del generador).
- `MEDIBLE-EN-CORPUS-SIN-CALC` — el mapa dictamina afirmaciones medibles con lo que ya hay en el corpus, pero nadie corrió el mecanismo. Es un «nadie corrió» (§2), no un «no se puede»: por eso no se funde con la categoría siguiente.
- `MEDIBLE-CON-ADQUISICIÓN` — solo medible si se adquiere el instrumento.
- `NO-MEDIBLE-POR-DISEÑO` — todas sus afirmaciones lo son.

| estado | reports |
|---|---:|
| MEDIDO | {{c:cobertura:MEDIDO}} |
| EN-MEDICIÓN | {{c:cobertura:EN-MEDICIÓN}} |
| MEDIBLE-EN-CORPUS-SIN-CALC | {{c:cobertura:MEDIBLE-EN-CORPUS-SIN-CALC}} |
| MEDIBLE-CON-ADQUISICIÓN | {{c:cobertura:MEDIBLE-CON-ADQUISICIÓN}} |
| NO-MEDIBLE-POR-DISEÑO | {{c:cobertura:NO-MEDIBLE-POR-DISEÑO}} |
| SIN-AFIRMACIONES-EN-MAPA | {{c:cobertura:SIN-AFIRMACIONES-EN-MAPA}} |

{{t:cobertura}}

Varios reports comparten dominio (dos de movilidad, dos de familia y cuidados): un dominio medido cuenta como medido en cada report que lo tiene como primario. El conteo por dominio del mapa está en la portada.

## P2 · Reglas SI-ENTONCES

Formato §5: **SI** [segmento] **ENTONCES** [conducta] — **PORQUE** [driver] — [TIER]. El tier **FUERTE** se reserva a la frecuencia que un RESULT GEN2 adoptado sostiene. El PORQUE es un mecanismo propuesto y lleva tier propio: ninguna de estas comparaciones lo identifica. Todas las cifras son RETROSPECTIVAS.

### Revisión de las reglas de v1.0

1. **Trámites — canal (v1.0 regla 1) · CONFIRMA.** **SI** el trámite ENCIG 2025 es presencial (urbano) **ENTONCES** la proporción de eventos con mordida es {{r:RESULT-ENCIG-MOR-B-P-PRE-SD}}; **SI** es digital, {{r:RESULT-ENCIG-MOR-B-P-DIG-SD}} — **PORQUE** registro y menor discrecionalidad (mecanismo `modelo §3.3`) — **[FUERTE como frecuencia por evento; mecanismo MEDIA, no identificado]**. Mismos RESULT que en v1.0, ahora con firma citada (`decisiones.tsv:CALC-ENCIG-0001`). La unidad es el evento de trámite, no la persona. Falsador: igualar tipo de trámite y soporte entre canales y que la diferencia desaparezca.
2. **Familia — remesas (v1.0 regla 2) · MATIZA.** v1.0 daba un solo punto (ENIGH 2022, {{r:RESULT-B-ENIGH-2022-P}}). v1.1 añade la serie adoptada de prevalencia: 2016 {{r:RESULT-ENIGH16-REMINT-PREVALENCIA}}, 2018 {{r:RESULT-ENIGH18-REMINT-PREVALENCIA}}, 2020 {{r:RESULT-ENIGH20-REMINT-PREVALENCIA}}. El orden de magnitud se sostiene en cuatro olas. DONDE-CAMBIO dictamina la prevalencia `SIN-SERIE` y la participación agregada de remesas en el ingreso `ESTABLE`, así que el catálogo no afirma tendencia. **SI** el hogar recibe remesas **ENTONCES** en la mediana de receptores el ingreso por remesas es {{r:RESULT-ENIGH20-REMINT-REMESAS-MEDIANA}} pesos trimestrales en 2020 — **PORQUE** la familia como seguro ante volatilidad y ausencia estatal (`modelo §3.5`) — **[FUERTE como descripción; mecanismo HIPÓTESIS en este catálogo]**. Unidad: hogar. Falsador del mecanismo: medir volatilidad y cobertura estatal junto con las transferencias.

### Reglas nuevas por dominio que entra

3. **Trabajo — informalidad por tamaño de localidad (ENOE, `TRABAJO`).** **SI** la persona ocupada vive en una localidad de menos de dos mil quinientos habitantes (`MENOS-2K5`) **ENTONCES** la proporción en empleo informal en 2025T4 es {{r:RESULT-ENOE-PISOS-TABLA#25676}}, contra {{r:RESULT-ENOE-PISOS-TABLA#25673}} en localidades `100K+` y {{r:RESULT-ENOE-PISOS-TABLA#25662}} nacional — **PORQUE** la oferta de empleo con seguridad social se concentra en ciudades (estructura, no preferencia) — **[FUERTE como gradiente descriptivo; mecanismo MEDIA]**. El gradiente ya estaba en 2005T1: {{r:RESULT-ENOE-PISOS-TABLA#14}} contra {{r:RESULT-ENOE-PISOS-TABLA#11}}. Falsador: que el gradiente se anule al condicionar por sector y tamaño de establecimiento.
4. **Trabajo — contrato escrito (ENOE).** **SI** ocupado en `MENOS-2K5` **ENTONCES** sin contrato escrito {{r:RESULT-ENOE-PISOS-TABLA#25911}} (2025T4), contra {{r:RESULT-ENOE-PISOS-TABLA#25908}} en `100K+` — **PORQUE** agricultura y autoempleo dominan la estructura local — **[FUERTE descriptiva; mecanismo MEDIA]**. Falsador: la misma brecha dentro de asalariados de establecimientos comparables.
5. **Género — violencia física de pareja (ENDIREH 2021, `GENERO`).** **SI** mujer de quince años o más con pareja actual **ENTONCES** violencia física de pareja alguna vez en la relación {{r:RESULT-ENDIREH2021-PF-TABLA#0}} y desde octubre de 2020 {{r:RESULT-ENDIREH2021-PF-TABLA#46}} — **PORQUE** —(el catálogo no propone driver: ENDIREH mide prevalencia y no la separa de desigualdad económica ni de violencia ambiental) — **[FUERTE como prevalencia; causa sin tier]**. Las ventanas distintas no se restan ni se promedian. Falsador de la generalización: una ola con el mismo instrumento cuyo IC excluya estos puntos.
6. **Género — denuncia (ENDIREH 2021).** **SI** mujer que vivió violencia (módulo de ayuda) **ENTONCES** denuncia {{r:RESULT-ENDIREH2021-AYU-TABLA#46}} — **PORQUE** costo y desconfianza en la institución receptora (adaptación racional, hipótesis) — **[FUERTE descriptiva; mecanismo HIPÓTESIS]**. No es rasgo cultural del silencio: sin medir el trato institucional, la hipótesis de incentivo es la primera. Falsador: una mejora medida del trato institucional sin cambio en la denuncia.
7. **Tecnología — no usar internet: costo contra preferencia (ENDUTIH 2025, `TECNOLOGIA`).** **SI** la persona sin internet vive en localidad `TLOC_4` (menos de dos mil quinientos habitantes) **ENTONCES** la razón «costo» es {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#327}} y «no le interesa» {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#374}}; en `TLOC_1` (cien mil o más), costo {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#324}} y preferencia {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#371}} — **PORQUE** la exclusión por precio pesa más abajo en la jerarquía urbana y el desinterés declarado pesa más arriba (oferta antes que preferencia, §3) — **[FUERTE descriptiva; mecanismo MEDIA]**. El uso de internet va de {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#42}} (`TLOC_1`) a {{r:RESULT-ENDUTIH-PISOS-2025-TABLA#45}} (`TLOC_4`). Falsador: que la brecha de costo desaparezca al controlar por ingreso del hogar.
8. **Tecnología — ciberacoso (MOCIBA 2017).** **SI** usuario de internet de doce años o más **ENTONCES** reporta ciberacoso {{r:RESULT-MOCIBA-PISOS-2017-TABLA#40}} y lo denuncia {{r:RESULT-MOCIBA-PISOS-2017-TABLA#122}} — **PORQUE** —(sin driver propuesto) — **[FUERTE descriptiva, una ola; no se compara con 2015, no estimable]**.
9. **Dinero — ahorro solo informal por formalidad (ENIF 2024, `DINERO`, CON RESERVA DE ANCHO).** **SI** la persona no tiene seguridad social **ENTONCES** ahorra solo por vía informal con punto {{r:RESULT-ENIFPIC-D9-FORMALIDAD-SIN-SEGURIDAD-SOCIAL-PISO-P}}, contra {{r:RESULT-ENIFPIC-D9-FORMALIDAD-CON-SEGURIDAD-SOCIAL-PISO-P}} con seguridad social (IC calibrados de persistencia) — **PORQUE** la oferta formal (cuenta, nómina) sigue a la formalidad laboral — **[MEDIA: los IC calibrados se traslapan; el catálogo no afirma diferencia]**. Oferta al lado: no existe exclusión por oferta sellada para ahorro ENIF 2024 (columna `oferta_exclusion`). Falsador: igualar tenencia de cuenta y que la brecha subsista.
10. **Seguridad — denuncia con seguro (ENVIPE 2025, piso t−1, unidad delito).** **SI** el delito afecta a un bien asegurado **ENTONCES** se denuncia {{r:RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-ASEGURADO-P}}, contra {{r:RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-NO-ASEGURADO-P}} sin seguro — **PORQUE** la aseguradora exige la denuncia: incentivo, no confianza (adaptación racional) — **[FUERTE descriptiva; mecanismo MEDIA]**. Unidad delito: no se compara con proporciones de personas. Falsador: igual diferencia en delitos cuyo seguro no exige denuncia.

## P4 · Dónde sí cambió

El dictamen por serie vive en [`canon/donde-cambio-el-mexicano-v1_0.md`](donde-cambio-el-mexicano-v1_0.md) (`GEN2-DONDE-CAMBIO-EL-MEXICANO-1`, RETROSPECTIVA, sin adopción). Conteo por comando sobre `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`: {{c:dc:series}} series · {{c:dc:ESTABLE}} `ESTABLE` · {{c:dc:CAMBIO-SOSTENIDO}} `CAMBIO-SOSTENIDO` ({{c:dc:CAMBIO-SOSTENIDO:SUBE}} suben, {{c:dc:CAMBIO-SOSTENIDO:BAJA}} bajan) · {{c:dc:SALTO-SIN-EXPLICAR}} `SALTO-SIN-EXPLICAR` (el `SALTO` del encargo) · {{c:dc:SIN-SERIE}} `SIN-SERIE`.

Lectura para el catálogo: los cambios sostenidos son todos ENOE y de décimas de punto; la mayoría de las series no tiene tres olas comparables. **La afirmación «el mexicano cambió en X» no tiene respaldo en este corpus fuera de esas series**, y ninguna frase de este catálogo la hace. «Cambió» es un hecho de la serie, no de la psicología.

## P4 · Cobertura por clase

Cita de [`forense/analisis/clase-amai/cobertura-por-clase-v1_0.md`](../forense/analisis/clase-amai/cobertura-por-clase-v1_0.md) (`GEN2-CLASE-AMAI-1`, RETROSPECTIVA): hay pisos por NSE AMAI en {{c:nse:celdas}} celdas (`pisos-nse-v1_0.tsv`); con la firma `FP-260924-GEN2-CLASE-AMAI-1-e773-01` entran al catálogo las de ENIGH 2022, ENIF 2024 y ENDUTIH 2023 (eje `NSE`). Las cifras por clase de este catálogo son esas filas; la lectura de abajo es la del documento citado. El hallazgo que el catálogo hereda como reserva: el corte de clase solo es posible hoy en dinero (ENIF), remesas (ENIGH) y tecnología (ENDUTIH). Lo cívico y el trato con el Estado (ENVIPE, ENCIG) no admiten NSE AMAI por construcción del cuestionario, y ahí el único corte socioeconómico es la escolaridad. Varios gradientes que parecen cultura (horizonte de ahorro corto, no usar internet por costo) son de clase según ese documento; la desconfianza declarada no muestra gradiente medible.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Dos del catálogo («estimadores con RESULT», «dominios MEDIDOS»). Cero mediciones y cero adopciones.
- **¿Pobreza, informalidad o violencia confundidas con cultura?** Las reglas de trabajo y tecnología leen primero estructura y oferta; ninguna regla atribuye un gradiente a «cultura mexicana».
- **¿Sobregeneralización desde la clase media urbana?** Los ejes de localidad (ENOE `MENOS-2K5`, ENDUTIH `TLOC_4`) están en la tabla. El eje NSE adoptado corta clase solo en dinero, remesas y tecnología: en lo cívico y en el trato con el Estado sigue sin corte de clase posible.
- **¿Qué cambia con foco rural o indígena?** El gradiente rural de informalidad y costo digital es el más grande del catálogo. Lo indígena-comunal queda fuera por diseño y ningún instrumento adoptado lo identifica.
- **¿Qué parece psicológico y es incentivo?** La denuncia con seguro (regla 10) y la denuncia de violencia (regla 6).
- **¿Evidencia débil con intuición fuerte?** Todos los PORQUE. Por eso llevan tier propio.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: toda cifra sale de un marcador de conteo o de RESULT de la plantilla (`forense/analisis/catalogo/v1_1/plantilla.md`), y `tests/test_catalogo_v1_1.py` falla si aparece un dígito fuera de un identificador, un año o un placeholder resuelto.
- **¿Deuda asumida que caducó?** FIRMAS-16 ya fusionó y sus pisos entraron; quedan pendientes los adoptados activos sin FP citable (`FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01`). Sucesor: v1.2.
- **¿Escala de cada cantidad y contra qué se compara?** Columna `unidad`. Solo se contrastan filas del mismo CALC, unidad y ola.
- **¿PROSPECTIVA y RETROSPECTIVA mezcladas?** No: todo el catálogo es RETROSPECTIVA. Las celdas validadas PROSPECTIVAS se citan aparte en la frase de portada.
- **¿Unidades promediadas?** No: persona (ENOE, ENDIREH, ENDUTIH, ENIF), hogar (ENIGH), delito (ENVIPE) y evento de trámite (ENCIG) nunca se suman.
- **¿Qué sería peligroso leído simplista?** Leer la tabla de ENOE como «la informalidad es rural por cultura», o una prevalencia ENDIREH como tasa anual.
