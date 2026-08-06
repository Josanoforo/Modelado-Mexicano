# RE-VERIFICACIÓN COMPLETA · TODA LA DEMANDA vs EL UNIVERSO REAL
### v1.0 · 7/ago/2026 · mesa Fable contra `origin/main = 9fd49db` (PR #155) · encargo directo del usuario, tercera formulación — esta responde a la pregunta completa

**Qué corrige este documento respecto a mis entregas anteriores.** Verifiqué ID-X cuando pediste TODO; usé 492 payloads y 134 fuentes como denominador cuando el denominador es ~24,000 URLs. Este documento pone del lado izquierdo **cada necesidad del programa** (15 elasticidades, 16 entradas condicionales, 14 reglas abiertas, 6 sellos expuestos) y del lado derecho **el universo completo**, con el inventario explícito de lo que nadie ha mirado.

---

## §0 · Denominadores, re-derivados en esta sesión (comandos en el cuerpo)

| Cifra | Valor derivado | Coincide con tu captura |
|---|---|---|
| Índice Descarga Masiva | **7,930 URLs · 137 programas** (135 limpios + 1 programa en blanco con 420 URLs + 1 duplicado de caja `Cnije`) | ✔ |
| `en_manifiesto` (col 7) | **sí = 69 · no = 7,861** → 0.87% | ✔ 99.1% no bajado |
| Canastas U2 parseadas | **0** — `ls data/` sin ÍNDICE-2, sin artefactos de canasta; DESC-2 nunca corrió | ✔ |
| Universo real de puertas | 7,930 + ~16,270 = **~24,200 URLs** | ✔ |
| Mapa | **134 fuentes · Σ n_urls_portal = 3,754 · solo 34 fuentes con slug de portal** | ✔ |
| **Jamás atribuido** | **~103 programas del índice sin NINGUNA fuente en el mapa · ≈4,176 URLs** (7,930 − 3,754) | la consecuencia que importa |

**Una precisión que evita sobre-corregir:** `en_manifiesto` es un *join por URL* contra esta canasta — 69 no es "lo que hay en disco" (hay 492 payloads íntegros); es "URLs de esta canasta que el manifiesto reconoce URL a URL". Ejemplo: `enigh` tiene 960 URLs y 0 en `sí` — y sin embargo R5.1 corrió sobre microdato ENIGH en disco, llegado por otra vía. Las dos afirmaciones son ciertas y distintas: *"99.1% de la canasta no está bajado"* ✔ y *"el disco tiene 492 payloads"* ✔. Lo que tu captura clava es la tercera: **CUBIERTA=0 era una afirmación sobre el disco, no sobre México** — y este documento es el primer cruce contra el índice completo.

**Estado de main al derivar (movió desde mi turno anterior):** PR #153 **VERIF-3 fusionado — los cuatro archivos abiertos byte a byte dan `EXISTE-NO-SATISFACE`** (ACLED_HDX, PUB, SICS, ECCO); PR #154/#155 documentan un *major outage* de GitHub Actions (fusión verificada localmente, causa establecida); EXPLORA-2 con rama viva (`explora2-1786042858`) sin fusionar.

---

## §1 · El inventario de lo jamás mirado — programa por programa

**Cubiertos por el mapa (34 slugs):** ccpv, cngf, cngmd*, eder, edr, elcos, enadid, enadis, enafin, enaid, enaproce, enasem, encig, encoap, encrige, encuci, endireh, endutih, ene, enestyc, enfih*, enif, enigh, enoe, enpol, ensafi*, ensanut, ensu, enti, enut, enve, envi, envipe, mociba. *(que un slug esté "en el mapa" significa que existe una fila de fuente — no que sus URLs estén bajadas: de estos 34, la mayoría tiene 0 en `en_manifiesto`.)*

**Los ~103 sin ninguna fuente, por familia y con sus URLs (top, derivado completo en la sesión):**

- **Censos de gobierno, justicia y transparencia — la masa jamás tocada (~2,600 URLs):** justiciapenal 558 · cngspspe 361 · cnije 346+20 · cnpje 272 · cleu 195 · cnpj 136 · cnijf 131 · cntaippdpf 105 · cntaippdpe 104 · cndhf 61 · cndhe 61 · cnple 52 · cnspef 36 · cnspf 23. *(cngmd 219 sí tiene fila en el mapa pero 0 bajadas.)*
- **Sociodemográficas grandes:** mcs 177 · intercensal 131 · enh 48 · dh 47 · natalidad 40 · mortalidad 19 · nupcialidad 19 · migracion 2.
- **Encuestas sociales y de hogares chicas — donde viven reactivos psicológicos que nadie inventarió:** biare 18 + enbiare 5 (bienestar autorreportado) · **eness 18** (empleo y seguridad social) · **ensafi 2** (salud financiera 2023) · **enfih 5** (finanzas de los hogares) · **enasic 3** (cuidados 2022) · enasjup 6 · ecopred 2 · endiseg 3 · envif 2 · envin 2 · encevi 5 · enape 2 · enccum 2 · enilems 6 · enecap 4 · motral 4 · mti 15 · molec 34 · modecult 44 · mopradef 64 · enco 43 · accidentes 31.
- **Registros administrativos laborales:** **rellaborales 11 + rellaboralesprueba 5** — conflictos laborales/huelgas/emplazamientos.
- **Económicas de establecimientos (~150 URLs):** ce 27 · esidet 23 · enamin 16 (micronegocios) · enece 14 · immex, emim, eaim, eia, emec, emoe, indmaq, peme, emat, ems, eti, eac, ca, cae, caas, comext, eod, esmng, mohoma, eim/eima/eima, easpnf, ilmm 9, amca, cagf 8, cjm 6, museos 6, salud 8, adicciones 2, ecosep, ecadefi, evf, enpl, enaf, enpetah, eneu 20, ed/edf 24, ecovidie 12, engspjm 15, judicialespenal 16.
- **El programa en blanco: 420 URLs sin campo `programa`** — defecto del propio índice, nadie lo ha caracterizado. Va a ÍNDICE-2 como fila obligatoria.

---

## §2 · La demanda, completa

### A · Las 15 elasticidades (censo, extraído fila por fila)

| # | Gen | Coeficiente | Ruta | Qué necesita exactamente |
|---|---|---|---|---|
| 1 | G1 | confianza_institucional −0.60 | RUTA-A | ENCIG 2023 P11_1_23 × P8_3_x (co-observación viva) |
| 2 | G1 | radio_confianza −0.35 | RUTA-A | ENCUCI 2020 AP5_1_x × AP5_17/18 |
| 3 | G2 | sens_estatus 0.55 | SIN-RUTA | desenlace SÍ (ENIGH gastotarjetas); **falta reactivo** — búsqueda cerrada ADR-54 sobre 5 instrumentos |
| 4 | G2 | aversion_riesgo 0.20 | SIN-RUTA | **falta reactivo** — cerrada ADR-52A (ENIF P5_2 descartado) |
| 5 | G3 | horizonte_temporal −0.60 | RUTA-I | ENNViH panel — **gate ID-X: inalcanzable, adjudicación pendiente** |
| 6 | G3 | aversion_riesgo 0.40 | SIN-RUTA | mismo reactivo que fila 4 |
| 7 | G3 | familismo_apoyo 0.20 | RUTA-A | ENIF 2024 p9_9_4 × P4_10 |
| 8 | G4 | exposicion_violencia 0.70 | RUTA-C | ENVIPE 2025, candidato "Parcial" nombrado — límite estructural declarado |
| 9 | G4 | confianza_inst[justicia] −0.40 | RUTA-C | mismo instrumento/join |
| 10 | G4 | horizonte_temporal −0.20 | SIN-RUTA | falta reactivo (proxy ENIF P4_10 falla C3) |
| 11 | G4 | sens_estatus −0.15 | SIN-RUTA | = fila 3 |
| 12 | G5 | familismo_apoyo 0.50 | SIN-RUTA | reactivo ENIF circular con su desenlace — falta reactivo NO-ENIF |
| 13 | G5 | familismo_obligacion | SIN-RUTA | solo proxy ENUT 6.11 con supuesto; forma PENDIENTE |
| 14 | G5 | radio_confianza 0.15 | SIN-RUTA | reactivo en ENCUCI, desenlace en ENIF — **falta puente entre instrumentos** |
| 15 | G6 | deferencia 0.45 | SIN-RUTA | solo Latinobarómetro P4NOIJ n=1,200 |

### B · Condicionales — reparto de clases derivado: **9 MEDIDO·PARCIAL · 5 MEDIDO· · 1 PENDIENTE · 1 GATE·ID**. Las que faltan por poblar se derivan de ahí (mesa: `grep 'clase:' milpa/procedencia.yaml` y listar las no-PARCIAL con su θ).

### C · Las 14 reglas abiertas (condición del Umbral + qué falta — tabla PASO 3 del mapa, ahora con el veredicto VERIF-3 encima):

R1.4 panel consumo por marca D/E — **propietario** · R2.1 tasa conductual de reporte de errores — **propietario** (ECCO: NO-SATISFACE con dato) · R2.2 rotación×liderazgo — **propietario** · R3.4 series Banxico + separar riesgo-fiscal/fricción — **en curso** (EXPLORA-2/MED) · R7.1 casilla concurrente/no-concurrente — INE, verificar pre-armado · R7.3 RDD PUB×INE — **PUB: NO-SATISFACE** (leer qué le faltó en la nota de VERIF-3) · R7.4/R7.5 registro de eventos de respuesta colectiva codificable — **ACLED_HDX: NO-SATISFACE** · R8.1 inventario de comités con/sin sanción — **SICS: NO-SATISFACE** (520 bytes) · R8.2 tandas digitales — **propietario** · R8.3 condición A/C3 — conceptual, no de fuente · R10.1 actos de habla — **académico** · R10.2 = R2.1 · R10.3 — **bloqueo ético, correcto no buscar**.

### D · Sellos expuestos (auditoría del turno anterior): R5.1-A (4 reservas + DiD/ENASEM en #139) · R1.1-D (AGROASEMEX no buscado) · R4.1-D, R4.3-D×2 (antecedentes "si no existe X") · R9.2-D (fuente independiente) · R1.3-E pierna 3 (CNBV).

---

## §3 · EL CRUCE — demanda × 137 programas del índice (todo `CANDIDATO·SIN-FETCH`: nombre de programa ≠ contenido verificado; nadie promueve nada aquí — A.6)

**El hallazgo mayor, y exige decisión de mesa:** las búsquedas de reactivo de `aversion_riesgo` (ADR-52A) y `sens_estatus` (ADR-54) se **cerraron sobre un régimen de cinco instrumentos** — y el índice sirve, sin que nadie las haya mirado, **ENSAFI** (Salud Financiera 2023: estrés financiero, actitudes ante deuda y riesgo) y **ENFIH** (Finanzas de los Hogares: hoja de balance, decisiones de crédito). Dos instrumentos de psicología financiera **fuera del universo sobre el que se cerró la búsqueda**. Eso no reabre los ADR automáticamente — pero convierte "búsqueda cerrada" en "búsqueda cerrada sobre 5 de 137", y la decisión de reabrirla es de mesa con esto a la vista. Impacto potencial: filas 3, 4, 6, 11 del censo (4 de los 9 SIN-RUTA) + la fila 14 (ENSAFI podría traer confianza y finanzas en el MISMO instrumento — el puente que falta).

| Necesidad | Candidatos del índice (SIN-FETCH) | O bien |
|---|---|---|
| aversion_riesgo / sens_estatus (filas 3,4,6,11) | **ENSAFI · ENFIH** | reabrir ADR-52A/54 es decisión de mesa |
| familismo (12, 13) | **ENASIC** (cuidados) · **ENESS** (apoyo familiar como aseguramiento) · ENH | — |
| radio_confianza puente (14) | **ENSAFI** (¿confianza + finanzas en un instrumento?) | — |
| horizonte_temporal G4 (10) | ENSAFI (planeación/expectativas) | — |
| llaves RUTA-I nuevas (censo v1.1) | **ENOE** (panel rotatorio, 380 URLs) · **EDER/EDR** (historias de vida retrospectivas) · ENASEM (ya en disco, ya nombrado) | — |
| deferencia (15) | ENADIS (actitudes) — débil; el hueco es real | mayormente FUERA-INEGI (valores) |
| **R7.4/R7.5** eventos de respuesta colectiva | **RELLABORALES** — registros administrativos de conflictos laborales/huelgas: eventos colectivos ante agravio, con registro. Es el primer candidato genuinamente nuevo tras el NO-SATISFACE de ACLED | — |
| **R8.1** comités con/sin sanción | **CNGMD** (219 URLs — Censo de Gobiernos Municipales: módulos de participación/comités, a verificar) · cngf | — |
| R7.1 | INE (fuera de índice) — sin candidato nuevo aquí | — |
| condicionales de seguridad sin poblar | **ENSU** (52, trimestral) · ENVIPE olas · ENDIREH | — |
| bienestar/θs subjetivos | **BIARE/ENBIARE** — nadie los ha inventariado | — |
| R5.1 re-examen / pensiones | ENASEM (disco) · **ENASJUP** (a caracterizar) · ENESS | — |
| R1.4, R2.1/R2.2/R10.2, R8.2 | — | **FUERA-DE-FORMA-INEGI (propietario)** — y VERIF-3 acaba de sellarlo con dato para ECCO. Honestidad: ni el microdato real de ENAPROCE mediría "tasa de reporte de errores"; el hueco es del mundo, no del portal |
| R10.1 | — | FUERA (réplicas académicas — ASIGNA-1b) |
| R10.3 | — | NO SE BUSCA (ético) |
| **420 URLs sin programa** | fila obligatoria de ÍNDICE-2 | — |

---

## §4 · Lo que este documento NO pudo examinar, dicho con su tamaño

1. **~16,270 URLs de las 5 canastas U2** — viven en `descargas_mx`, raíz gitignorada: el clon no las tiene. **ÍNDICE-2 es un acto de la caja del corpus** (parsear 5 XML → TSV homólogo al índice, misma columna `en_manifiesto`) y es la condición para que el cruce de §3 pase de 7,930 a ~24,200. Encargo de ~30 líneas; listo para redactarse hoy.
2. **El contenido real de cada candidato** — todo §3 es nivel-programa. La promoción exige abrir byte a byte (DESC-2/ASIGNA), nunca este documento.
3. **No-INEGI** (Banxico en curso; CNBV/CONDUSEF/AGROASEMEX/SINERHIAS/ONG/académico) — ASIGNA-1b, ya especificado en el plan anterior, ahora con §3 como semilla.

## §5 · Re-etiquetado de las cifras que veníamos citando

- `CUBIERTA = 0 de 14` → se lee: *"0 de 14 contra 134 fuentes canónicas y 492 payloads en disco (join-URL: 0.87% de una canasta); **no afirma nada** sobre 4,176 URLs no atribuidas ni sobre ~16,270 sin parsear"*. El mapa sigue siendo válido **como mapa del disco**; era inválido como mapa del mundo, y así se citaba.
- Los "NO EXISTE" del cruce v2_0 quedan doblemente acotados: por A.4 (vocabulario) y ahora por denominador (universo de búsqueda ≪ universo real).
- VERIF-3 sí movió el estado real: 4 celdas pasaron de "sin verificar byte a byte" a **EXISTE-NO-SATISFACE con dato** — eso es conocimiento nuevo y en la dirección correcta, aunque el contador no se mueva.

## §6 · Sobre reiniciar el proyecto — el estado completo para tu decisión

**Lo que sobrevive a cualquier reinicio** (activos, no proceso): 492 payloads íntegros con manifiesto verificado · las corridas con espec congelada y dos commits (reproducibles independientemente de cómo se gestione el resto) · el índice de 7,930 y las 5 canastas · este cruce. **Lo que un reinicio no arregla por sí solo:** el defecto nunca fue tener poco — fue **citar el poco como si fuera el todo**. Reiniciar sin cambiar eso reproduce el gap con carpetas nuevas.

**La alternativa concreta a reiniciar-de-cero:** re-fundar la capa de asignación, no el programa. Un solo artefacto rector — **REGISTRO DEMANDA↔UNIVERSO** (cada necesidad de §2 × cada candidato × estado A.4 × denominador declarado), del cual mapa, censo y cruce pasan a ser vistas derivadas — alimentado por tres actos ya especificables hoy: **ÍNDICE-2** (caja, 30 líneas), **CRUCE-24K** (mesa Opus, con este documento como fila cero), y **la decisión de mesa sobre ADR-52A/54** con ENSAFI/ENFIH sobre la mesa. Si aun con esto decides reiniciar, este documento es el inventario de arranque del proyecto nuevo — que era exactamente lo que faltaba la primera vez.

---
**CONTADOR: cero, y declarado.** Lo que mueve: el denominador de todas las conversaciones que siguen.
