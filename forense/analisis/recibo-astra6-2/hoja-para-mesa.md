# Hoja para mesa · 15 FP abiertas por Codex (Astra tanda 3 y anteriores) · ACTO GEN2-RECIBO-ASTRA6-2

Fecha: 27/sep/2026 · Dirección resuelve, mesa sella · La asienta FIRMAS-21.
Universo: 15 ids de `forense/firmas-pendientes.tsv` con `estado = ABIERTA` cuyo id termina en `ee49-01`, `ee49-02`, `13c5-01`, `13c5-02`, `9df0-01`, `fb50-01..04`, `157c-01..04`, `71cf-01`, `39de-01`.

[EJECUTADO] Comando (lector CSV, no línea física):

```
python3 - <<'E'
import csv
r=list(csv.DictReader(open('forense/firmas-pendientes.tsv'),delimiter='\t'))
for s in "ee49-01 ee49-02 13c5-01 13c5-02 9df0-01 fb50-01 fb50-02 fb50-03 fb50-04 157c-01 157c-02 157c-03 157c-04 71cf-01 39de-01".split():
    m=[x for x in r if x['id'].endswith(s)]; print(s, len(m), [(x['id'],x['estado']) for x in m])
E
```

Resultado: 15/15 sufijos casan con exactamente 1 id cada uno; los 15 en `ABIERTA`. Ningún sufijo sin casar, ninguno duplicado.

Contexto de firmas [EJECUTADO, mismo lector]: `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-01` y `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02` constan en el TSV como `ABIERTA`; mesa las firmó hoy en chat y su asiento lo hace CIERRE-SEMANAL-2 (en vuelo). Esta hoja las trata como firmadas por mandato del encargo §2 y las cita por id, sin editarlas.

Reglas que gobiernan los dictámenes: regla 6 (sin retadores, pilotos ni duelos sobre olas vistas), E.2 (adopción solo por merge de mesa), E.6 (reservas; una exposición se adjudica por categoría, no por contenido), D-22, A.7 (listar miembros de un zip no es abrirlo), y «recomendar a mesa solo con la razón escrita».

---

### FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-01
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO `forense/validacion-independiente/catalogo-1-reempaqueta-ventana/hoja-de-firma-acceso-futuro.md` l.1–25] Codex (#1203) reempaquetó las entradas con la ventana restaurada y pide permiso para que una sesión nueva vuelva a leer ENDIREH 2021 y recalcule a ciegas. Su hoja dice «levantar únicamente la reserva necesaria». [EJECUTADO `data/manifiesto.yaml` por lector YAML] las 12 entradas ENDIREH 2021 no traen ningún campo de reserva: no hay reserva que levantar.
**Qué se pide.** Autorizar una sesión de validación ciega nueva sobre ENDIREH 2021, delimitada por módulos y campos, sin cambiar método ni tolerancias.
**Opciones.** (1) Firmar tal cual: queda escrito como «levantar reserva» algo que no está reservado (rótulo falso en el tablero). (2) Firmar con el rótulo correcto y la compuerta de paquete archivado. (3) No firmar: el lote 2 de 2021 se queda sin validación ciega.
**Recomendación.** Opción 2. Razón: lo que se pide es autorizar una sesión ciega nueva, no abrir una reserva; y una sesión sin paquete archivado antes no es ciega (compuerta del encargo, E.2). Texto de firma: «Autorizo una sesión de validación ciega NUEVA sobre ENDIREH 2021 (ola no reservada por manifiesto; esto no es apertura de reserva), limitada a las identidades, módulos y campos de `hoja-de-firma-acceso-futuro.md`, sin cambiar estimando, universo, recodificaciones, ponderadores, bootstrap ni tolerancias. Condiciones antes de lanzar: paquete archivado en el repo con sha antes de la sesión, columna `ventana` presente en cada `estimandos.tsv` verificada por archivo, y constancia de aislamiento. No adopta resultados».
**Plazo.** Sin urgencia; gatea solo el intento nuevo de C1. Firmar después del recibo de #1203 (este acto).

### FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-02
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** Igual que ee49-01, para ENDIREH 2016. [EJECUTADO] las 20 entradas ENDIREH 2016 del manifiesto no traen campo de reserva.
**Qué se pide.** Autorizar una sesión ciega nueva sobre ENDIREH 2016, delimitada.
**Opciones.** (1) Tal cual. (2) Con rótulo correcto y compuerta. (3) No firmar.
**Recomendación.** Opción 2, misma razón. Texto: el de ee49-01 cambiando «ENDIREH 2021» por «ENDIREH 2016».
**Plazo.** Igual que ee49-01.

### FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-01
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO `forense/analisis/reports-v2/cuidado-migracion-pareja-1/hoja-firma.md` l.1–13] Tres reports (cuidado, migración, pareja) con reglas SI-ENTONCES como propuestas acotadas.
**Qué se pide.** Recibirlos para revisión, sin adopción en el motor ni aperturas nuevas.
**Opciones.** (1) Firmar tal cual. (2) Devolver una regla concreta con su defecto. (3) No firmar (los reports quedan en limbo).
**Recomendación.** Opción 1. Razón: recibir no adopta (E.2); el texto ya excluye motor y aperturas. La «recepción editorial independiente» que el texto remite al recibo de Claude la entrega este acto (nota de #1197).
**Plazo.** Esta semana; no bloquea nada.

### FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-02
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO `forense/analisis/reports-v2/cuidado-migracion-pareja-1/incidente-reserva.md` l.1–11] Un ejecutor abrió un PDF público de ENADID 2023 antes de reconocer la reserva de la conducta PERSONA60+. Se detuvo, se excluyó la fuente (ASTRA5-U0-VEJEZ-002 y -038) y el ejecutor declara que ningún RESULT depende de ella [REPORTADO].
**Qué se pide.** Adjudicar el incidente: excluir la fuente, mantener la reserva, sin permiso retroactivo.
**Opciones.** (1) Firmar tal cual. (2) Declarar la ola consumida para ese cruce (más severo). (3) Conceder permiso retroactivo (prohibido en espíritu por E.6).
**Recomendación.** Opción 1. Razón: es exactamente lo que E.6 pide (se recibe la categoría, no el contenido; se conserva la reserva; lo expuesto no alimenta cifras). La dependencia «ninguna» es autoinforme; queda como reserva, no como certificación.
**Plazo.** Esta semana; gatea solo la recepción de la pieza vejez.

### FP-260926-ASTRA6-C3-DINERO-TECNOLOGIA-CONOCIMIENTO-1-9df0-01
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO `forense/analisis/reports-v2/dinero-tecnologia-conocimiento-1/hoja-para-mesa.md` l.1–9] Reglas SI-ENTONCES de tres reports.
**Qué se pide.** Recibirlas para evaluación futura, sin adoptar contenido causal ni tocar motor o catálogo.
**Opciones.** (1) Tal cual. (2) Mantenerlas solo como orientación local. (3) No firmar.
**Recomendación.** Opción 1. Razón: no adopta (E.2) y conserva la separación oferta/acceso/decisión que §3 exige.
**Plazo.** Esta semana; no bloquea.

### FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-01
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO `forense/validacion-independiente/catalogo-1-impedimentos-lote2/impedimentos-lote2-hoja-decisiones.md` l.1–16] Contratos sucesores por identidad (puntos ENOE separados de IC, B2022 aislado, contrato inferencial nuevo para árbitros/AMAI). La propia hoja dice que una firma debe nombrar identidad, opción y hash, no aprobar la carpeta.
**Qué se pide.** Aprobar esos contratos sucesores.
**Opciones.** (1) Tal cual (aprobación genérica que la hoja misma desaconseja). (2) Recibir y diferir la elección por identidad. (3) No firmar.
**Recomendación.** Opción 2. Razón: la parte inferencial depende del protocolo de 157c-01, aún sin margen de equivalencia; firmar en bloque adoptaría sin identidad. Texto: «Recibo los contratos sucesores propuestos en `impedimentos-lote2-hoja-decisiones.md` (manifiesto `3d508f7e…1c50`) sin adoptarlos. Cada contrato se firmará por identidad, opción y hash en un trámite posterior; el contrato inferencial de árbitros/AMAI espera la resolución de FP-…-157c-01. No cambio contratos ni sellos originales».
**Plazo.** Sin urgencia; gatea sucesores C1 del lote 2.

### FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO misma hoja, fila fb50-02] Dictámenes documentales ENDIREH 2006 (ventana MC/MD) y 2016 (bins NIV propios), y retiro de quince llaves ENVIPE 2015 con sucesor 2024 por delito.
**Qué se pide.** Elegir por separado ventana, bins y retiro/sucesor.
**Opciones.** (1) Tal cual (incluye un retiro del producto). (2) Recibir los dictámenes y mandar el retiro al circuito de catálogo. (3) No firmar.
**Recomendación.** Opción 2. Razón: retirar filas del catálogo es competencia de CIERRE-SEMANAL-2 y cambia producto; los dictámenes documentales sí pueden recibirse ya. Texto: «Recibo los dictámenes ENDIREH 2006 (separar MD postseparación del anual) y ENDIREH 2016 (bins NIV propios desde FD) como base de contratos sucesores, sin reescribir llaves ni sellos. El retiro de las quince llaves ENVIPE 2015 se propone al circuito de catálogo como PROPONER-SUSPENDER con sucesor por CALC nuevo; no se ejecuta por esta firma».
**Plazo.** Siguiente corte de catálogo.

### FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-03
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO misma hoja, fila fb50-03] Dos etapas: (1) inventario custodial del directorio de ZIP; (2) proyección por fuente/miembro/columna/finalidad. ENUT conserva su cruce reservado (FP-bda6-02).
**Qué se pide.** Autorizar la custodia en dos etapas con firmas distintas.
**Opciones.** (1) Tal cual (las dos etapas en una firma). (2) Solo etapa 1 ahora; etapa 2 por fuente. (3) No firmar.
**Recomendación.** Opción 2. Razón: A.7 dice que listar miembros de un zip es envoltura, no dato: la etapa 1 no abre nada; la etapa 2 sí abre y exige firma propia por fuente. Texto: «Autorizo únicamente la etapa 1 (inventario de miembros —nombre, CRC, tamaño— de los ZIP, A.7), con custodio distinto del analista. La etapa 2 requiere una FP por fuente con miembro, columna, finalidad y hash; ENUT conserva FP-bda6-02 y no se abre su cruce reservado».
**Plazo.** Sin urgencia.

### FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-04
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO misma hoja, fila fb50-04] Ocho contratos de tolerancia ENDUTIH/MOCIBA fijados antes de revelar objetivos; ENDUTIH 2025 sigue reservada.
**Qué se pide.** Fijar esas tolerancias.
**Opciones.** (1) Tal cual. (2) Diferir. (3) No firmar.
**Recomendación.** Opción 1. Razón: fijar la tolerancia antes de ver el dato es lo que §4 exige («la regla y el umbral se fijan antes»); no abre reserva ni adopta.
**Plazo.** Antes de cualquier comparación futura del lote.

### FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO `forense/validacion-independiente/catalogo-1-incertidumbre-spec/p1/protocolo-propuesto.md` l.1–11] Protocolo de bootstrap de referencia para comparar IC. El propio texto dice que no es el estimador de varianza adecuado del diseño INEGI y que no propone margen de equivalencia.
**Qué se pide.** Aprobar el protocolo antes de un nuevo intento.
**Opciones.** (1) Tal cual (podría leerse como IC adoptable). (2) Aprobarlo solo como protocolo diagnóstico de replay. (3) No firmar.
**Recomendación.** Opción 2. Razón: sin margen de equivalencia ni validación de diseño, solo sirve para acreditar implementación. Texto: «Apruebo el protocolo como contrato DIAGNÓSTICO de reproducción de IC para intentos futuros; no es estimador de IC adoptable ni recertifica IC históricos. El margen de equivalencia y el control simultáneo se fijarán por mesa antes del siguiente conjunto sin revelar».
**Plazo.** Antes del siguiente intento C1.

### FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-02
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO `…/p3/astra6-c1-p3-spec-hoja-firma.md` l.1–15] Dos carriles: transporte fiel de la ventana (767 identidades) y contratos nuevos (escolaridad NIV, leyes vs. servicios, edad 98/99).
**Qué se pide.** Autorizar la restauración de ventana y decidir los contratos nuevos por bloque.
**Opciones.** (1) Tal cual (mezcla ambos carriles). (2) Firmar el transporte; cada contrato nuevo, por bloque. (3) No firmar.
**Recomendación.** Opción 2. Razón: la hoja misma pide no mezclar transporte con cambios de estimando; la exclusión de EDAD 98/99 se decide junto con 39de-01. Texto: «Autorizo el carril de transporte: copiar la ventana literal del catálogo v1.2 a las 767 identidades, sin cambiar método ni el DISCREPA/NO-RECALCULABLE histórico. Los contratos nuevos (NIV-terminal-v1, P14_22_14 leyes, exclusión EDAD 98/99) quedan pendientes de firma por bloque; ninguno se presenta como equivalente del histórico».
**Plazo.** Antes de firmar ee49-01/02.

### FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO `…/p2/astra6-c1-p2-publicabilidad-nota.md`, rg por «sesión01»] Conservar los umbrales CV ≤ 0.30 y ancho ≤ 0.20; seis casos 2011 dependen de sesión01.
**Qué se pide.** Adjudicar publicabilidad con esos umbrales.
**Opciones.** (1) Tal cual. (2) Relajar umbrales (sería ajustar la regla al resultado; prohibido por §4). (3) No firmar.
**Recomendación.** Opción 1. Razón: mantener el umbral sellado es lo correcto; el trato de las filas concretas (ACOTAR / PROPONER-SUSPENDER #2039) ya lo firmó mesa en FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02 y esta firma no lo cambia.
**Plazo.** Esta semana.

### FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-04
DICTAMEN: YA-CUBIERTA-POR ADR-270927-GEN2-RECIBO-ASTRA6-2-627e-01

**Situación.** Pide «solicitar recibo de Claude de este PR» (#1194).
**Qué se pide.** Un recibo.
**Opciones.** (1) Cerrarla por producto. (2) Dejarla abierta.
**Recomendación.** Opción 1. Razón: este acto entrega el recibo post-merge de #1194 (nota `pr-1194.md`); se cierra por producto citando su ADR.
**Plazo.** Al cierre de este acto.

### FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01
DICTAMEN: RECOMENDAR-FIRMAR-TAL-CUAL

**Situación.** [LEÍDO `forense/analisis/familias-2027-frontera-1/hoja-firma-frontera.md` l.1–40] Cuatro instrumentos para familias 2027: no lanzar ENSU-Campeche (potencia) ni ENOE-informalidad (SE de diseño), diferir ENSANUT CESD-7 y MOCIBA (oro inconmensurable; 2021/2022 conservan reserva F6).
**Qué se pide.** Recibir los artefactos y aceptar esas disposiciones, sin adoptar diagnósticos ni autorizar reservas.
**Opciones.** (1) Tal cual. (2) Devolver una pieza con pregunta sucesora. (3) No firmar.
**Recomendación.** Opción 1. Razón: no abre reservas, no adopta, y declinar lanzar con potencia insuficiente es lo que manda el pre-registro (§4); coherente con regla 6 (frente prospectivo 2027).
**Plazo.** Antes de preparar COMMIT-1 de familias 2027.

### FP-260926-ASTRA6-C1-ADJUDICACION-PUNTOS-1-39de-01
DICTAMEN: RECOMENDAR-FIRMAR-CON-CAMBIO

**Situación.** [LEÍDO `forense/validacion-independiente/catalogo-1-adjudicacion-puntos/c1-puntos-hoja-para-mesa.md` l.1–11] Cuatro cosas: (a) retiro temporal de 679 identidades con defecto documental; (b) denominador institucional; (c) elegibilidad nacional (98/99 excluidos); (d) sucesores 2011/2021 como CALC nuevos sin adopción automática.
**Qué cubre beee-02** [LEÍDO fila de `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02` y nota RECIBO-ASTRA6-1 §2–§3]: PROPONER-SUSPENDER las 6 filas institucionales 2011 (#1656–#1661, donde la spec dice «entre mujeres con al menos un acto» y el medidor condicionó a solicitantes) más #2039, y ACOTAR 689; sello intacto, sucesor por CALC nuevo. Cubre **el trato en producto** de (a) y de las cifras de (b) — con otra forma: acotar con reserva visible, no retirar las 679. **No cubre**: la elección del denominador del sucesor (b), la regla 98/99 (c), ni la autorización de sucesores (d). Por eso no es YA-CUBIERTA-POR.
**Qué se pide.** Las cuatro decisiones de contenido.
**Opciones.** (1) Tal cual: el «retiro de 679» contradice lo ya firmado en beee-02 (acotar). (2) Firmar solo (c) y (d), remitir (a) a beee-02 y dejar (b) para la spec del sucesor. (3) No firmar.
**Recomendación.** Opción 2. Razón: evita dos tratos distintos para las mismas filas y respeta que el denominador es decisión de contenido que la propia hoja propone dejar pendiente. Texto: «El trato en producto de las identidades con defecto documental y de las seis filas institucionales 2011 es el firmado en FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02 (suspender/acotar; sellos intactos); no se añade retiro distinto. Autorizo preparar y ejecutar, en actos posteriores y CALC nuevos, los sucesores 2011/2021 del expediente ASTRA6-C1-ADJUDICACION-PUNTOS-1, sin adopción automática: su adopción requiere recibo y merge de mesa. Para universos nacionales: edades observadas; 98/99 excluidos salvo evidencia documental independiente incorporada antes de COMMIT-1. El denominador institucional del sucesor se fija en su spec antes de COMMIT-1 y se firma entonces; no se sustituye por frecuencia entre afectadas sin esa firma».
**Plazo.** Antes del run de cualquier sucesor 2011/2021.

---

## Resumen

| id | dictamen |
|---|---|
| FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-01 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-02 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-01 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-02 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-ASTRA6-C3-DINERO-TECNOLOGIA-CONOCIMIENTO-1-9df0-01 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-01 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-03 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-04 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-02 | RECOMENDAR-FIRMAR-CON-CAMBIO |
| FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-04 | YA-CUBIERTA-POR ADR-270927-GEN2-RECIBO-ASTRA6-2-627e-01 |
| FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 | RECOMENDAR-FIRMAR-TAL-CUAL |
| FP-260926-ASTRA6-C1-ADJUDICACION-PUNTOS-1-39de-01 | RECOMENDAR-FIRMAR-CON-CAMBIO |
