# Benchmark auditable del comportamiento del mexicano · catálogo v1.4

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-del-mexicano-v1_4.md` (sucesor de `catalogo-del-mexicano-v1_3.md`; v1.0–v1.3 quedan intactos — E.1) |
> | **NOMBRE ESTABLE** | `catálogo del mexicano` |
> | **ESTADO** | Producto consultable. Lo firmado hasta v1.3 entra citando su firma; lo sellado del `27–28/sep` entra como **bloque de adopción propuesto por instrumento**: el merge de mesa del PR que trae esta versión **es** la adopción (E.2). Sin merge, esta versión no existe en `main` |
> | **ACTO** | `GEN2-CIERRE-Y-PRODUCTO-3` (P1) · generación GEN2 · cero mediciones nuevas · consume lo sellado y registrado |
> | **TABLA** | [`catalogo-del-mexicano-v1_4.tsv`](catalogo-del-mexicano-v1_4.tsv) — una fila por estimador |
> | **BLOQUE** | [`bloque-adopcion-cifras-v1_4.tsv`](../forense/analisis/catalogo/v1_4/bloque-adopcion-cifras-v1_4.tsv) — propuesta por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / NO-ENTRA); mesa veta un instrumento pidiendo su retiro antes del merge |
> | **REGENERA** | `python3 forense/analisis/catalogo/genera_catalogo_v1_4.py` (esta portada incluida; los generadores v1.2 y v1.3 quedan intactos); `--sin-registro` reutiliza las constancias ya derivadas del registro (`adoptados-activos-v1_4.tsv`, `registro-semana-v1_4.tsv`, `status-v1_4.json`) |

**{{c:estimadores}} estimadores con RESULT sellado · {{c:mapa11_dominios_medidos}} de los {{c:mapa11_dominios}} dominios del mapa v1.1 con estimador (eran {{c:mapa11_dominios_medidos_v1_3}} en v1.3) · {{c:reports_medidos}} de los {{c:reports}} reports del corpus con dominio medido · {{c:celdas_validadas}} celdas validadas (definición vigente de `corrida0 status`), de las cuales {{c:celdas_validadas_prospectiva}} PROSPECTIVAS y {{c:celdas_validadas_retrospectiva}} RETROSPECTIVAS se reportan aparte.**

**Tesis.** Lo que hoy se puede afirmar sobre el mexicano con cifra propia sigue siendo **descriptivo y retrospectivo**. v1.4 añade {{c:bloque:filas}} filas de {{c:bloque:calcs}} CALC sellados esta semana, todas propuestas **con reserva de ancho**: {{c:bloque:pisos}} pisos de una ola (confianza institucional ENCIG 2023 y los pisos de dominio PDR1 que dan estimador por primera vez a AUTORIDAD, SANCION_SOCIAL, TIEMPO y RURAL_INDIGENA) y {{c:bloque:momentos}} contrastes de momento (CALC-ALT-*), {{c:bloque:momentos_holdout_gastado}} de ellos con su holdout ya gastado. Rotula además las {{c:vc3:lote3}} llaves del tercer lote de validación ciega y suspende, por firma, las {{c:vc3:SUSPENDIDA}} llaves ENVIPE 2024 retiradas del universo C1. Ninguna fila es predicción.

Contadores que mueve este acto, si mesa fusiona: «estimadores en catálogo con RESULT» ({{c:estimadores}}), «dominios del mapa con estimador» (`mapa11_dominios_medidos`: {{c:mapa11_dominios_medidos_v1_3}} → {{c:mapa11_dominios_medidos}}). No mueve `adoptados_activos` ({{c:adoptados_activos}} en el registro de este commit), `celdas_validadas` ni ningún contador del marcador: los lee. La vista publicada (`data/corrida0/corridas.tsv`) va atrasada respecto del disco (el `[deriva]` publica por trozos); el catálogo lee el registro derivado **del commit** con la misma función que `corrida0 status` y lo deja como constancia.

## Cómo leerlo

1. Cada fila cita su adopción en `firma_fp`: un `FP-…` FIRMADO en `forense/firmas-pendientes.tsv`, el objeto de su fila en `data/corrida0/decisiones.tsv` (`decisiones.tsv:<objeto>`), la firma verbatim de un encargo archivado (`forense/encargos/<archivo>.md#firma …`) o, **nuevo en v1.4**, `MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3` ({{c:bloque:filas}} filas): adopción por el merge del PR que trae el bloque (E.2), con la propuesta por instrumento en el TSV del bloque.
2. `result_id` + `celda` localizan la cifra: en los CALC de pisos, `RESULT-…-TABLA#i` es el registro `i` de la tabla sellada en `data/corrida0/<calc>/resultados.json`. En los CALC-ALT, `RESULT-…-TABLA#<ruta>` es el nodo de la tabla sellada por referencia (`tablas/tabla.json`, hash verificado al leer). Los hashes de cada CALC están en `forense/analisis/catalogo/v1_4/calcs-v1_4.tsv`.
3. `unidad`, `eje` y `segmento` gobiernan la lectura. Ninguna cifra de unidad delito o trámite se compara con una de unidad persona u hogar.
4. `estado_adopcion`: `ADOPTADO`, `ADOPTADO-CON-RESERVA-DE-ANCHO` (su IC es calibrado y ancho a propósito: no se llama cobertura) o `SUSPENDIDA-POR-FIRMA` ({{c:estado_adopcion:SUSPENDIDA-POR-FIRMA}} filas: la cifra sellada no mide el estimando de su spec humana; la fila se conserva con su `sucesor` y **no se usa como piso**). `alcance`: `PISO-DESCRIPTIVO-DE-OLA` (bloque v1.4: piso de una ola), `CONTRASTE-DE-MOMENTO` (bloque v1.4: diferencia entre dos grupos de una ola; **no es línea a vencer** y no entra a la tabla de piso), `DESCRIPTIVO-DE-OLA` (piso de una ola, sin uso predictivo), `ESTIMADOR-DE-CELDA` (piso t−1 adjudicado a una celda del marcador) o `PARAMETRO-DE-REGLA` (lo lee una regla del motor).
5. `temporalidad`: todo el catálogo es **RETROSPECTIVA** ({{c:temporalidad:RETROSPECTIVA}} filas). Las celdas PROSPECTIVAS del marcador que existían eran pisos de origen legacy y quedaron fuera (ver «Fuera por regla»).
6. `origen_piso`: `NUEVO` (medido desde microdato en su CALC; {{c:origen_piso:NUEVO}} filas) o `HEREDADO-DE-GEN2` (el punto de la ola t es el piso GEN2 de t−1; {{c:origen_piso:HEREDADO-DE-GEN2}} filas). **Ninguna fila es HEREDADO-DE-LEGACY.**
7. `oferta_exclusion`: en cada fila de `DINERO` va la medida de exclusión por oferta, o la declaración de que no existe una sellada para esa ola y conducta. `GEN2-DINERO-SERIES-CNBV-BANXICO-1` (`PR #1159`) no añadió columna de oferta a ningún piso de crédito o ahorro: su pieza P4 quedó `PARO-ENTORNO` (la serie BDIF de CNBV está en host denegado; NC `8dbe`), así que la columna sigue siendo la de `CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001`.
8. **Validación ciega (columna `validacion_ciega`).** Las {{c:vc:filas}} llaves del primer lote de validación ciega llevan el rótulo de la tabla del recibo `GEN2-RECIBO-ASTRA6-1` (firma `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02`): `SOSTENER` {{c:vc:SOSTENER}}, `SOSTENER-SIN-CORROBORACION` {{c:vc:SOSTENER-SIN-CORROBORACION}}, `ACOTADA` {{c:vc:ACOTADA}} (`DELTA-PUNTO-EN-VALIDACION-CIEGA` {{c:vc:ACOTADA:DELTA-PUNTO-EN-VALIDACION-CIEGA}}, `PUBLICABILIDAD-FRAGIL-AL-RNG` {{c:vc:ACOTADA:PUBLICABILIDAD-FRAGIL-AL-RNG}}) y `SUSPENDIDA` {{c:vc:SUSPENDIDA}}. El sello de su CALC no se toca: el sucesor es un CALC nuevo, nombrado en `sucesor` y no abierto aquí. Todas son RETROSPECTIVAS; unidad mujer.

{{t:validacion}}

9. **Validación ciega, tercer lote (columna `validacion_ciega_lote3`).** Las {{c:vc3:lote3}} llaves de `forense/validacion-independiente/catalogo-1-lote3/dictamen-lote3-v1_1.tsv` (`GEN2-C1-SUCESORES-Y-LOTE-3`) llevan su dictamen: `SOSTENER` {{c:vc3:LOTE3:SOSTENER}}, `SOSTENER-SIN-CORROBORACION` {{c:vc3:LOTE3:SOSTENER-SIN-CORROBORACION}} (incluye las del tercer lote que el gate de acceso no dejó lanzar: sostener sin corroborar no es validar), `ACOTADA` {{c:vc3:ACOTADA}} (CESD-7 de ENBIARE: `R26 (a)` excluye `EDAD=98`; sucesora `--R26A`) y `ACOTADA-PROPUESTA` {{c:vc3:ACOTADA-PROPUESTA}} (ENDIREH 2016, `60+` incluye `EDAD=98`; `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` ABIERTA: el rótulo es propuesta, no firma). El rótulo lleva `punto=` tal como lo escribe el dictamen: `DENTRO` es dentro de la tolerancia absoluta del comparador (`1e-10`), **no** igualdad exacta; `FUERA` trae su Δ en el dictamen. El IC no adjudica en ninguna fila (`IC-DIAGNOSTICO-R23-NO-ADJUDICA`). Todas RETROSPECTIVAS.
10. **Suspendidas por R21.** Las {{c:vc3:SUSPENDIDA}} llaves `RESULT-PISOS-ENVIPE2024-V2-*` (denuncia con seguro y evasión), retiradas del universo C1 por `FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02` (FIRMADA), pasan a `SUSPENDIDA-POR-FIRMA` con su `sucesor` por llave. Suspender no es borrar: la fila se queda, rotulada, y **no se usa como piso**.
11. **`holdout_gastado`** (solo contrastes de momento): el momento cuyo holdout consumió el CALC (`M13`, `M19`, `M22`, `M23`) o `NINGUNO`. Un momento con holdout gastado ya no sirve para validar prospectivamente ese momento; sirve para describir (E.6).

{{t:lote3}}

## P1 · Estimadores por dominio e instrumento

{{t:dominios}}

**Fuentes, una por firma.**

- **Pisos por instrumento — Firma T** (`GEN2-TRAMITE-FIRMAS-15` §1 T + ADENDA-1): ENOE (`FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01`), ENDIREH 2021, 2016, 2011 y 2006 (`FP-260923-ASTRA5-U2-ENDIREH-6a2c-01` a `-04`), ENDUTIH 2023–2025 (`FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01`: sin las celdas originales de empleo, sustituidas por `CALC-ENDUTIH-EMPLEO-15MAS-*`) y MOCIBA 2015–2017 (`-1f30-02`: 2015 no estimable). Una fila por celda publicable; cada una es piso descriptivo retrospectivo **sin uso predictivo**.
- **Marginales por piso t−1**: ENVIPE 2025 adoptada (`decisiones.tsv:adopcion:piso-t1-marginales-por-instrumento`) y ENIF 2024 **con reserva de ancho** (`FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`, IC calibrado de persistencia: conservador, un solo choque). ENCIG 2025 queda vetada en nivel (fuera).
- **Pisos de salud y bienestar — FIRMAS-16** (`GEN2-TRAMITE-FIRMAS-16`, «ejecuta GEN2-CATALOGO-V1-1-1»): ENSANUT 2021–2024 **con reserva de ancho** (`FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01`; sobre 2024 el IC es el calibrado de persistencia), ENCODAT 2016–2017 **con reserva de ancho** (`-6d56-02`; una sola ola, IC de diseño) y ENBIARE 2021 adoptado como piso de una ola (`-6d56-03`).
- **Parámetros de reglas y celdas R/M del marco** con consumo activo (la misma vista que `corrida0 status`), cada uno con la fila de `decisiones.tsv` de su CALC, su FP o la firma del encargo que lo relevó.
- **Pisos de FIRMAS-19** (`GEN2-TRAMITE-FIRMAS-19`, J1–J10; una fila por celda `-P` publicable de cada CALC, IC calibrado de persistencia donde el CALC lo trae):
  - J1 ENIGH 2016–2022, consumo del hogar (`CALC-ENIGH-CONSUMO-PISOS-0002`, `…-2d37-01`) **con reserva de ancho**; J3 (`…-2d37-03`) veta las filas de `-0001` construidas desde `gastoshogar` 2016/2018: el catálogo solo lee `-0002`. Trae el eje `ENTIDAD` (región).
  - J2 ENGASTO 2012 (`…-2d37-02`) con reserva de ancho, descripción de 2012 sin extrapolación.
  - J4 WVS 2018, J5 Latinobarómetro 2023, J6 PEW religión y autoridad, J7 LAPOP capital social (**sin serie**: cada ola se lee sola), J9 ENASIC 2022 y J10 PEW migración: con reserva de ancho.
  - J8 ENADID 2009/2014/2018 (`…-2a0e-01`): **adoptado** sin reserva.
- **Pisos de FIRMAS-20** (`GEN2-TRAMITE-FIRMAS-20` §1 A1–A6; una fila por celda `-P` con punto, IC calibrado de persistencia donde el CALC lo trae):
  - A1 ENSU (`FP-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-01`): pisos 2024T1/2025T3/2025T4 y serie trimestral, **con reserva de ancho**; los cuatro hábitos con «No aplica» en el denominador no se comparan con comunicados.
  - A2 CCPV 2010, A3 EMAT, A4 EDR, A5 ENPECYT (`FP-260926-GEN2-COLA-LOTE-1-3a49-01` a `-04`), **con reserva de ancho**. EMAT es matrimonio civil inscrito, no unión; EDR es composición de defunciones registradas (unidad defunción), nunca tasa por habitante; ninguno de los dos tiene IC de diseño (registro completo).
  - A6 (`FP-260926-GEN2-COLA-COMPLETA-1-0d4a-01`): ENDISEG 2021, MMSI 2016, ENASEM 2021, ENVIPE 2024 (percepción; unidad persona) y ENOE 2024T4 **adoptados**; Latinobarómetro 2023 (complemento), PEW 2024 y ENADID 2018 **con reserva de ancho**; **Intercensal 2015 VETADA** (payload solo del Estado de México): fuera, con fila por RESULT en `data/corrida0/decisiones.tsv`.
- **Bloque de adopción v1.4 — merge de mesa** (`MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3`; solo CALC que el registro del commit ve `SELLADA` con `cuenta_gen2=SI`, constancia `registro-semana-v1_4.tsv`). Dominio: PROPUESTO-POR-EJECUTOR, leído de la nota del acto emisor.

{{t:bloque}}

- **Bloque ENIGH — Firma M** (`GEN2-ADOPCION-BLOQUE-Y-PINES-1`): descriptores de intensidad de remesas 2016, 2018 y 2020 con IC bootstrap.

**Ejes.** Sexo, edad, escolaridad, localidad (tamaño) y entidad —el eje regional disponible con RESULT adoptado— salen de las tablas ENOE, ENDIREH, ENDUTIH y ENIGH-consumo; formalidad y cuenta, de las marginales ENIF. **NSE entra como eje con reserva de instrumento** (`FP-260924-GEN2-CLASE-AMAI-1-e773-01`, FIRMAS-16): ENIGH 2022 (regla AMAI reproducida), ENIF 2024 (aproximación conforme) y ENDUTIH 2023 como aproximación rotulada; ENDUTIH 2024–2025 (`DESVIADA`) quedan fuera por la letra de la firma ({{c:excluidos:NSE-FUERA-DE-RESERVA-DE-INSTRUMENTO}} celdas). La región de seis zonas de `canon/eje-regional-v1_0.md` es propuesta sin adopción: no aporta filas.

### Pendiente de firma (no entran; no es PARO)

{{t:pendientes}}

`SIN-FP-CITABLE`: RESULT con consumo activo que el contador de adoptados cuenta por la etiqueta de su propia spec (E.2), pero sin FP firmada, sin fila de mesa en `decisiones.tsv` para su CALC y sin firma de encargo en su pin. El catálogo no les inventa firma. La firma `FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01` (FIRMADA, opción a) los hace entrar en v1.2 citándola.

### Propuestas de reglas recibidas (no son filas del catálogo)

Heredado de v1.3 (FIRMAS-20 C: propuestas editoriales recibidas **sin adopción**). Las reglas con cifra de esta semana van al bloque de reglas [`canon/reglas-bloque-adopcion-1.md`](reglas-bloque-adopcion-1.md), no a esta tabla. Ninguna entra como regla SI-ENTONCES en v1.4: cada una necesita su comparador y su falsador antes de integrarse.

{{t:propuestas}}

### Fuera por regla

Detalle por llave en `forense/analisis/catalogo/v1_4/excluidos-v1_4.tsv`:

- Piso **HEREDADO-DE-LEGACY** ({{c:excluidos:PISO-HEREDADO-DE-LEGACY}} RESULT del censo de `GEN2-ENCIG-PISOS-GEN2-1`): `GEN2-PISOS-GEN2-2` cerró (`PR #1123`) re-midiéndolos con sucesores `-0002` sellados; **ninguna fila de esta tabla es HEREDADO-DE-LEGACY** (pisos por origen: `NUEVO` o `HEREDADO-DE-GEN2`).
- Celdas FIRMAS-19 con punto nulo: {{c:excluidos:CELDA-SIN-PUNTO}}.
- Celdas ENDUTIH originales de empleo excluidas por la propia firma: {{c:excluidos:EXCLUIDA-POR-FIRMA}}.
- Celdas sin punto publicable: suprimidas {{c:excluidos:CELDA-SUPRIMIDA}} + {{c:excluidos:CELDA-SUPRIMIDA-N-MENOR-100}} + {{c:excluidos:CELDA-SUPRIMIDA-N}}, no estimables {{c:excluidos:CELDA-NO-ESTIMABLE-SIN-EST_DIS}}.
- Intercensal 2015, vetada por FIRMAS-20 A6: {{c:excluidos:VETADO-POR-FIRMA}} celdas.
- Marginales sin adopción en nivel (ENCIG 2025, vetada): {{c:excluidos:MARGINAL-NO-ADOPTADA}}.
- Sellados de la semana que no son estimador de conducta: la evaluación `CALC-PISO-PERSISTENCIA-ERROR-0002` ({{c:excluidos:EVALUACION-NO-ESTIMADOR}} evaluaciones en total, con el duelo ENIGH) y la medida de oferta de cuenta ENIF 2024 ({{c:excluidos:MEDIDA-DE-OFERTA-NO-ESTIMADOR}}; va citada en `oferta_exclusion`).
- Nodos de tablas de momento sin punto estimable: {{c:excluidos:CELDA-NO-ESTIMABLE}}.
- Tablas ENIGH adoptadas por Firma M y no desagregadas en esta versión (perfil estructural y remesas en contexto): {{c:excluidos:ADOPTADO-TABLA-NO-DESAGREGADA}} CALC. La evaluación de origen móvil del duelo ENIGH mide error de candidatos, no una conducta.

## P3 · Cobertura de los reports del corpus

Unidad: los {{c:reports}} reports de `corpus/reports/` (el conteo de «dominios» de la ADENDA-2 y del README), cada uno asignado a su dominio primario por `forense/analisis/dominios/report-a-dominio-v1_0.tsv`; los conteos de afirmaciones salen de `canon/mapa-dominios-v1_1.tsv`. Regla, en orden (la primera que se cumple):

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
10. **Seguridad — denuncia con seguro (ENVIPE 2025, piso t−1, unidad delito) · SUSPENDIDA EN v1.4.** Sus dos RESULT quedan `SUSPENDIDA-POR-FIRMA` (R21, `fb50-02`): la regla **no se sostiene con cifra en esta versión** hasta que su sucesor se mida. Texto de v1.3, conservado para auditoría: **SI** el delito afecta a un bien asegurado **ENTONCES** se denuncia {{r:RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-ASEGURADO-P}}, contra {{r:RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-NO-ASEGURADO-P}} sin seguro — **PORQUE** la aseguradora exige la denuncia: incentivo, no confianza (adaptación racional) — **[FUERTE descriptiva; mecanismo MEDIA]**. Unidad delito: no se compara con proporciones de personas. Falsador: igual diferencia en delitos cuyo seguro no exige denuncia.

### Reglas nuevas con el bloque v1.4 (todas RETROSPECTIVAS, una ola, con reserva de ancho)

Las reglas contrastadas de la semana (`canon/reglas-contrastadas-v1_1.tsv`) tienen su propio bloque de adopción: [`canon/reglas-bloque-adopcion-1.md`](reglas-bloque-adopcion-1.md). Aquí solo se leen las cifras que dan estimador a un dominio por primera vez.

11. **Sanción social — `SANCION_SOCIAL` (ENSU 2024T1, persona `18+` urbana).** La proporción que declara lo que mide SANC-007 es {{r:RESULT-PDR1-ENSU2024-SANC007-PRINCIPAL-TOTAL-TODOS-P}}; mujeres {{r:RESULT-PDR1-ENSU2024-SANC007-PRINCIPAL-SEXO-MUJER-P}} contra hombres {{r:RESULT-PDR1-ENSU2024-SANC007-PRINCIPAL-SEXO-HOMBRE-P}} — **PORQUE** —(sin driver identificado: una ola urbana) — **[MEDIA descriptiva, CONFIRMA en conducta; universo urbano]**. Falsador: una ola rural o no urbana con IC que excluya el punto.
12. **Autoridad — `AUTORIDAD` (ENCUCI 2020, persona).** Confía mucho (`8–10`) en servidores públicos {{r:RESULT-PDR1-ENCUCI2020-AUTOR003-CONFIA-SERVIDORES-8A10}}; rural {{r:RESULT-PDR1-ENCUCI2020-AUTOR003-CONFIA-SERVIDORES-8A10-SEG-DOMINIO-R}} contra urbano {{r:RESULT-PDR1-ENCUCI2020-AUTOR003-CONFIA-SERVIDORES-8A10-SEG-DOMINIO-U}} — **[MEDIA descriptiva; una ola]**. No es «deferencia a la autoridad» como rasgo: mide confianza declarada, sin trato observado.
13. **Tiempo y comunidad — `RURAL_INDIGENA` (ENUT 2024, persona).** Participación en trabajo comunitario, rural menos urbano: {{r:RESULT-PDR1-ENUT2024-COMUN-PART-DIF-RURAL-URBANO-P}} — **PORQUE** la organización comunitaria es institución, no preferencia (hipótesis) — **[HIPÓTESIS RAZONABLE: una ola; el tamaño del efecto acota la «comunalidad» a unos puntos]**. Falsador: que la diferencia se anule al condicionar por tamaño de localidad y régimen de tenencia.
14. **Brecha rural e indígena en tecnología — `RURAL_INDIGENA` (ENADID 2023, diferencia de proporciones).** Brecha total de TEC-010 {{r:RESULT-PDR1-ENADID2023-BRECHA-TOTAL}}; crece con la edad: `15–29` {{r:RESULT-PDR1-ENADID2023-BRECHA-15_29}}, `60+` {{r:RESULT-PDR1-ENADID2023-BRECHA-60M}} — **[MEDIA descriptiva; MATIZA el report: sus `19 %` y `24.2 %` no reproducen]**. Es una brecha de acceso (oferta) antes que de disposición.
15. **Educación privada — `CONOCIMIENTO` (ENIGH 2022, hogar).** Diferencia de asistencia a escuela privada, deciles V–VIII menos I–IV, urbano: {{r:RESULT-PDR1-ENIGH2022-DIF-PRIV-URBANO-B2-MENOS-B1-P}}; rural {{r:RESULT-PDR1-ENIGH2022-DIF-PRIV-RURAL-B2-MENOS-B1-P}} — **PORQUE** el ingreso compra oferta privada donde la hay (estructura) — **[HIPÓTESIS RAZONABLE]**. Unidad hogar.
16. **Ahorro informal por tamaño de localidad — `DINERO` (ENSAFI 2023, contraste de momento M23, holdout gastado).** Ahorro solo informal: menos de `2 500` habitantes {{r:RESULT-ALT-M23-ENSAFI2023-TABLA#solo_informal/tloc=MENOS-2500}} contra `100 mil` y más {{r:RESULT-ALT-M23-ENSAFI2023-TABLA#solo_informal/tloc=100MIL-Y-MAS}}; contraste rural−urbano {{r:RESULT-ALT-M23-ENSAFI2023-TABLA#CONTRASTE:solo_informal_rural_menos_urbano}} — **PORQUE** oferta formal ausente en localidades chicas (oferta antes que preferencia) — **[MEDIA descriptiva]**. Oferta al lado: la exclusión por oferta sellada es de crédito ENIF y de cuenta ENIF 2024, no de ENSAFI (columna `oferta_exclusion`).
17. **Denuncia y miedo — `VIOLENCIA` (ENVIPE 2025, unidad DELITO, momento M22, holdout gastado).** Proporción de delitos no denunciados por miedo: {{r:RESULT-ALT-M22-ENVIPE2025-TABLA#no_denuncia_por_miedo/NACIONAL}} — unidad delito: no se compara con proporciones de personas.

## P4 · Dónde sí cambió

El dictamen por serie vive en [`canon/donde-cambio-el-mexicano-v1_0.md`](donde-cambio-el-mexicano-v1_0.md) (`GEN2-DONDE-CAMBIO-EL-MEXICANO-1`, RETROSPECTIVA, sin adopción). Conteo por comando sobre `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`: {{c:dc:series}} series · {{c:dc:ESTABLE}} `ESTABLE` · {{c:dc:CAMBIO-SOSTENIDO}} `CAMBIO-SOSTENIDO` ({{c:dc:CAMBIO-SOSTENIDO:SUBE}} suben, {{c:dc:CAMBIO-SOSTENIDO:BAJA}} bajan) · {{c:dc:SALTO-SIN-EXPLICAR}} `SALTO-SIN-EXPLICAR` (el `SALTO` del encargo) · {{c:dc:SIN-SERIE}} `SIN-SERIE`.

Lectura para el catálogo: los cambios sostenidos son todos ENOE y de décimas de punto; la mayoría de las series no tiene tres olas comparables. **La afirmación «el mexicano cambió en X» no tiene respaldo en este corpus fuera de esas series**, y ninguna frase de este catálogo la hace. «Cambió» es un hecho de la serie, no de la psicología.

## P4 · Cobertura por clase

Cita de [`forense/analisis/clase-amai/cobertura-por-clase-v1_0.md`](../forense/analisis/clase-amai/cobertura-por-clase-v1_0.md) (`GEN2-CLASE-AMAI-1`, RETROSPECTIVA): hay pisos por NSE AMAI en {{c:nse:celdas}} celdas (`pisos-nse-v1_0.tsv`); con la firma `FP-260924-GEN2-CLASE-AMAI-1-e773-01` entran al catálogo las de ENIGH 2022, ENIF 2024 y ENDUTIH 2023 (eje `NSE`). Las cifras por clase de este catálogo son esas filas; la lectura de abajo es la del documento citado. El hallazgo que el catálogo hereda como reserva: el corte de clase solo es posible hoy en dinero (ENIF), remesas (ENIGH) y tecnología (ENDUTIH). Lo cívico y el trato con el Estado (ENVIPE, ENCIG) no admiten NSE AMAI por construcción del cuestionario, y ahí el único corte socioeconómico es la escolaridad. Varios gradientes que parecen cultura (horizonte de ahorro corto, no usar internet por costo) son de clase según ese documento; la desconfianza declarada no muestra gradiente medible.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Cero mediciones. Si mesa fusiona: «estimadores con RESULT» y `mapa11_dominios_medidos` ({{c:mapa11_dominios_medidos_v1_3}} → {{c:mapa11_dominios_medidos}}); la adopción es el merge, no una decisión del ejecutor.
- **¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA?** Todo el catálogo es RETROSPECTIVA, bloque v1.4 y tercer lote incluidos (olas vistas). Los momentos con holdout gastado lo dicen en su fila: ya no pueden servir de prueba prospectiva de ese momento.
- **¿Pobreza, informalidad o violencia confundidas con cultura?** Las reglas de trabajo y tecnología leen primero estructura y oferta; ninguna regla atribuye un gradiente a «cultura mexicana».
- **¿Sobregeneralización desde la clase media urbana?** Los ejes de localidad (ENOE `MENOS-2K5`, ENDUTIH `TLOC_4`) están en la tabla. El eje NSE adoptado corta clase solo en dinero, remesas y tecnología: en lo cívico y en el trato con el Estado sigue sin corte de clase posible.
- **¿Qué cambia con foco rural o indígena?** El gradiente rural de informalidad y costo digital es el más grande del catálogo. Lo indígena-comunal queda fuera por diseño y ningún instrumento adoptado lo identifica.
- **¿Qué parece psicológico y es incentivo?** La denuncia con seguro (regla 10) y la denuncia de violencia (regla 6).
- **¿Evidencia débil con intuición fuerte?** Todos los PORQUE. Por eso llevan tier propio.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: toda cifra sale de un marcador de conteo o de RESULT de la plantilla (`forense/analisis/catalogo/v1_4/plantilla-v1_4.md`), y `tests/test_catalogo_v1_4.py` falla si aparece un dígito fuera de un identificador, un año o un placeholder resuelto.
- **¿Deuda asumida que caducó?** La regla 10 (denuncia con seguro) se sostenía en v1.3 con dos RESULT que R21 retiró del universo C1: queda suspendida, con texto conservado. La desagregación de las tablas ENIGH de Firma M, prometida para v1.4, no entra (NC re-diferida). Una fila `SOSTENER-SIN-CORROBORACION` del tercer lote no es una fila validada.
- **¿Qué cambia con foco rural o indígena?** v1.4 da por primera vez estimador al dominio `RURAL_INDIGENA` (ENUT, ENADID): diferencias de pocos puntos, que acotan cualquier lectura de «comunalidad» como rasgo; la huella indígena difusa se mapea, el sistema comunal vivo sigue fuera por diseño.
- **¿Sesgo de marcos o muestras importadas?** WVS, Latinobarómetro, PEW y LAPOP son marcos internacionales: sus ejes son los del cuestionario (clase subjetiva, ingreso subjetivo), no NSE AMAI, y ninguna fila se lee como rasgo nacional esencial. PEW migración mide disposiciones, no flujos.
- **¿Escala de cada cantidad y contra qué se compara?** Columna `unidad`. Solo se contrastan filas del mismo CALC, unidad y ola.
- **¿PROSPECTIVA y RETROSPECTIVA mezcladas?** No: todo el catálogo es RETROSPECTIVA, validación ciega incluida (se comparó contra cifras ya selladas). Las celdas validadas PROSPECTIVAS se citan aparte en la frase de portada.
- **¿Unidades promediadas?** No: persona (ENOE, ENDIREH, ENDUTIH, ENIF, ENSU, ENPECYT, WVS, LAPOP), hogar (ENIGH, ENGASTO, CCPV), matrimonio o contrayente (EMAT), defunción (EDR), delito (ENVIPE marginales, momento M22), empresa y unidad económica (ENCRIGE, ENVE: tabulados sin IC), puntos porcentuales de diferencia en diferencias (`RG-b913`) y evento de trámite (ENCIG) nunca se suman ni se comparan sin función de enlace.
- **¿Qué sería peligroso leído simplista?** Leer la tabla de ENOE como «la informalidad es rural por cultura», una prevalencia ENDIREH como tasa anual, la composición EDR como tasa de suicidio, o EMAT como «los mexicanos se casan menos» (mide inscripción civil, no unión).
