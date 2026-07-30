# Gobernanza del programa · Psicología del Mexicano Contemporáneo
### `gobernanza` · **v1.14** · 30 de julio de 2026 · **46 ADR**

> | | |
> |---|---|
> | **ARCHIVO** | `gobernanza-v1.14.md` |
> | **REEMPLAZA A** | `gobernanza-v1.13.md` — **borrar** |
> | **VERIFICAS ASÍ** | ADR-36 tiene **adenda (c)** sobre series numeradas · §2 lista los tres `milpa-*` · §4 (registro del perímetro del Hito D) trae la corrección de RÓTULO fechada 29/jul — el perímetro sigue en **27** · §4 trae ADR-44 (publicación del repositorio, sin registro previo), ADR-45 (vocabulario de "prueba de falsación", D-05) y ADR-46 (unidad de contaminación es la SESIÓN, no la máquina — corrige `cola.yaml` E-03) |
> | **NOMBRE ESTABLE** | **`gobernanza`** — cítalo así, **nunca por nombre de archivo** |



*Documento vivo. Registra **qué se decidió, por qué, y qué se rompe si cambia**.
No repite el contenido del corpus: lo gobierna.*

**Versión de este documento:** 1.12 · **Estado del programa:** Ronda 4 cerrada y **auditada**; modelo v2 y glosario v5 consolidados; Fase 1 del simulador **pospuesta**. *(Corregido 29/jul/2026: decía 1.1, contradiciendo la cabecera de este mismo archivo, que ya dice 1.9 — hallazgo nuevo de esta sesión, no catalogado por `censo-integridad-v1_0.md`.)*

---

## 1. Qué gobierna esto (y qué no)

**Gobierna:** qué artefacto es fuente de verdad, cómo se propagan los cambios, qué decisiones están tomadas y cuáles siguen abiertas.

**No gobierna:** el contenido sustantivo (eso vive en los reports, el glosario y el modelo) ni las reglas de rigor (esas viven en `instrucciones-proyecto-v2.md`, que es un artefacto aparte y **canónico**).

**Por qué existe.** El programa creció de 10 reports a un corpus de 30 + glosario + integrador + modelo + validación forense + simulador, con varias decisiones **revertidas o refinadas sobre la marcha**. Sin registro, esas reversiones se ven como incoherencias y alguien las "corrige" de vuelta.

---

## 2. Cadena de dependencia y fuentes de verdad

```
instrucciones-proyecto-v2.md   ← CANÓNICO. Gobierna todo lo demás.
            │
            ▼
   31 reports temáticos         ← CANÓNICO (evidencia primaria)
            │
            ├── meta-auditoría comunicación   ← parche a un report
            ▼
   glosario-v5-consolidado      ← CANÓNICO. Donde los tiers se LEEN (ADR-02).
            │                     Único punto legítimo de entrada de un tier al programa.
            ▼
   integrador                   ← DERIVADO de reports + glosario
            │
            ▼
   modelo-decisiones-v2         ← CANÓNICO OPERATIVO
            │                     ▲
            │                     └── validaciones forenses (retropropagación, ADR-29)
            ▼
            │                     (la ficha derivada se ELIMINÓ — ADR-36.b:
            │                      era superficie de desincronización pura)
            ├──────────────┬──────────────────┐
            ▼              ▼                  ▼
      milpa/rules/*   masterclass.html   prompts verticales
      (ejecutable)     (enseñanza)        (operativo)
```

**Regla de oro de la cadena:** un artefacto **derivado** nunca se edita directamente. Se edita su fuente y se regenera. Si alguien edita la ficha canónica a mano, el modelo y la ficha divergen en silencio — el fallo exacto del vertical V1.

⚠️ **Cambio de v1.0:** el **glosario entra a la cadena**. En v1.0 no aparecía, pese a que ADR-02 lo hace depositario de los tiers. Esa omisión permitió que **el modelo creara reglas sin pasar por él** — la ruta por la que la regla estrella migró de dominio sin que nada rechinara (Hito 2). **Toda regla nueva del modelo debe tener constructo tierizado en el glosario o declararse explícitamente como propuesta sin tier.**

| Artefacto | Estado | Versión | Se regenera desde |
|---|---|---|---|
| `instrucciones-proyecto-v2.md` | **CANÓNICO** | v2 | — (se edita con ADR) |
| **31 reports** en `/mnt/project/` | **CANÓNICO** | Ronda 3. **3 parchados 28/jul** con nota fechada (consumidor · comunicación · foundational). *Eran "30" por conteo de memoria; verificado contra disco el 28/jul. Y los parches se registraban como hechos el 27/jul sin estarlo* | — |
| `glosario-v5.6.md` | **CANÓNICO** | **v5.6**, autocontenido | reports (mapas de evidencia) |
| `integrador-psicologia-mexicano.md` | DERIVADO | 31 reports | reports + glosario |
| `meta-auditoria-comunicacion.md` | CANÓNICO (parche) | 1.0 | — |
| `modelo-decision-v3.4.md` | **CANÓNICO OPERATIVO** | **v3.4, autocontenido** *(absorbe la ficha)* | integrador + glosario + validaciones |
| ~~`ficha-canonica-modelo.md`~~ | **ELIMINADA 28/jul** *(ADR-36.b)* | — | absorbida en `modelo` §0.1, §0.2 y §9 |
| **5 validaciones forenses** | **CANÓNICO** *(ADR-29.b)* | Ronda 4 | — |
| ~~`CHECKPOINT-v2.md`~~ · ~~`mapa-y-roadmap.md`~~ · ~~`inventario-corpus.md`~~ | **BORRADOS 28/jul** | — | **fusionados en `ESTADO-PROGRAMA.md`** |
| `estado-programa-v1.9.md` | **CANÓNICO (estado)** | v1.9, 29/jul | única fuente de estado |
| `ADR-30.md` | **BORRADO 28/jul** | — | incorporado a §4; además contenía la versión **superada** (retiraba `familismo` de G3, corregido en mesa) |
| `milpa/` (Fase 0) | DERIVADO | 0.1.0 | ⚠️ **ausente salvo 3 archivos** |
| `masterclass-mexico.html` | DERIVADO | foto Ronda 4 | ⚠️ **ausente** |
| **`milpa-whitepaper`** | CANÓNICO (programa) | v0.1 | — |
| **`milpa-spec`** | CANÓNICO (programa) | **v0.2** | — |
| **`milpa-plan`** | CANÓNICO (programa) | v0.1 | — |
| `modelo-decisiones-mexicano.md` v1 | **BORRADO** 27/jul | — | superado por v2 |
| `glosario` v2 / v3 / v4 | **BORRADOS** 27/jul | — | consolidados en v5 |
| `estado-proyecto-...md` | **BORRADO** 27/jul | — | superado |

⚠️ **Corrección 29/jul/2026 (sesión de correcciones):** la tabla de arriba citaba glosario v5.5, modelo v3.0 y estado v1.1 (los nombres de archivo exactos viven en el diff de este commit) pese a que este mismo documento ya iba en v1.9 — congelada desde una versión bastante anterior de `gobernanza`, nunca actualizada en los saltos de versión intermedios. Corregido a las versiones vigentes (glosario v5.6, modelo v3.3, estado v1.9). *(`censo-integridad-v1_0.md` C5-02.)*

**Tres nombres citados por `curaduria-archivos.md` (27/jul) que ningún documento declaró borrados o renombrados** *(gap encontrado por `tests/check.py` T03, bucket `nombrado_sin_borrado_explicito`; declarado aquí porque este §2 es donde vive el Registro de artefactos — el resto de borrados de esta sección ya sigue ese patrón)*:

| Nombre citado (27/jul) | Qué pasó | Certeza |
|---|---|---|
| `gobernanza-programa.md` v1.0 | Renombrado bajo la convención de ADR-36 (28/jul) a la serie versionada punto-menor de `gobernanza` (hoy `gobernanza-v1.12.md`) — es este mismo documento, con linaje continuo (ADR-26 a 29 incorporados, tal como `curaduria-archivos.md:37` pedía para su v1.1) | Alta — el propio ADR-36 describe la migración de nombre de todo archivo canónico |
| `glosario-v5.md` | Renombrado bajo ADR-36 a la serie versionada punto-menor de `glosario` (hoy `glosario-v5.6.md`) | Alta, mismo mecanismo |
| `CHECKPOINT-programa-psicologia-mexicano.md` | Probable antecesor de `CHECKPOINT-v2.md`, que esta misma tabla ya declara **BORRADO 28/jul, fusionado en `ESTADO-PROGRAMA.md`** (fila de arriba) | **Media** — el nombre no coincide exacto y no hay commit localizable que confirme el renombre `CHECKPOINT-programa-psicologia-mexicano.md` → `CHECKPOINT-v2.md`; se declara aquí como la lectura más probable, no como hecho verificado |

**Regla de borrado** *(aprendida el 27/jul):* un artefacto superado se borra **solo después** de que su sucesor sea autocontenido. El glosario se hizo bien; el modelo se borró antes de consolidar el v2 y se salvó por una copia temporal. **Consolidar primero, borrar después** — no es detalle de proceso, es lo único que separa "versión limpia" de "pérdida".

---

## 3. Protocolo de cambio (lo que evita la deriva)

Cuando algo cambia, se clasifica y se propaga. **Sin excepción.**

| Severidad | Qué es | Qué obliga |
|---|---|---|
| **S1 · Regla rota** | Una validación rompe o degrada una regla | ADR nuevo → modelo §7 → regenerar ficha → recompilar `milpa/rules` → validador → masterclass → **+ retropropagación (§3.1)** |
| **S2 · Cambio de alcance** | Entra o sale algo del modelo | ADR nuevo → revisar **todos** los derivados → verificar backtests → **+ retropropagación** |
| **S3 · Evidencia nueva** | Se añade un report o una validación confirma algo | Glosario → integrador → modelo → regenerar ficha |
| **S4 · Redacción** | Claridad, formato, ejemplos | Sin propagación; sin ADR |
| **S5 · Pendiente irresuelto** ⭐ | Una contradicción que **no** se resuelve | **Nuevo en v1.1** *(ADR-27)*. Se registra en §5.1 con su estado. No dispara propagación, pero **debe tener casillero** |

**Por qué existe S5.** El protocolo v1.0 solo sabía registrar *cambios*, y "seguimos sin saber esto" no es un cambio. Sin casillero, un pendiente se cae: de tres choques que registró el integrador, dos llegaron a ADR y **el tercero se perdió** porque no había dónde ponerlo.

### 3.1 Retropropagación *(ADR-29 — nuevo en v1.1)*

El protocolo v1.0 propagaba en **una sola dirección**: corpus → integrador → modelo → derivados. No había protocolo para cuando una validación rompe algo **aguas arriba**. Costó seis casos, uno irreparable.

Cuando una validación rompe o degrada una afirmación:

1. **El report dueño recibe nota de corrección fechada** *(29.a)*, en el archivo, no en un documento aparte.
2. **El artefacto forense se archiva como canónico** junto a los reports, **completo e incluyendo los casos descartados con su motivo** *(29.b)*.
3. **El modelo se sincroniza internamente** *(29.c)*: §3 no puede cargar tiers que §7 ya superó.
4. **El validador rechaza un artefacto forense sin tabla de descartes**, igual que rechaza un número sin procedencia *(adenda)*.

*Por qué el punto 4:* el defecto nunca fue que faltara el protocolo — fue que **nadie estaba obligado a ejecutarlo**. Con la misma plantilla, V1 archivó sus descartes y V3 no archivó ninguno. **Un principio necesita un artefacto de salida que falte visiblemente si no se cumple.**

**Checklist de propagación S1/S2:**

```
[ ] ADR escrito, con qué evidencia lo motiva
[ ] modelo §7 actualizado (confirma/matiza/rompe)
[ ] ficha canónica REGENERADA (no editada a mano)
[ ] glosario: ¿el constructo cambia de tier?
[ ] RETROPROPAGACIÓN: nota fechada al report dueño (ADR-29.a)
[ ] RETROPROPAGACIÓN: forense archivado completo, con descartes (ADR-29.b)
[ ] milpa/rules recompilado + validador en verde
[ ] backtests revisados: ¿alguno dependía de la regla que cambió?
[ ] masterclass actualizada si el cambio es visible al lector
[ ] registro de artefactos: versión actualizada arriba
```

**Regla anti-captura:** un cambio de regla **sin cambio de fuente** es olor a captura. Si la evidencia no cambió, la regla no debería cambiar.

---

## 4. Registro de decisiones (ADR)

*Formato: qué se decidió · por qué · qué rompería revertirla · estado.*

### Fundación

**ADR-01 · El integrador se vacía en la estructura del Bloque B.** Los patrones del Bloque B *son* los que cruzan el corpus. → **Vigente.**

**ADR-02 · Regla de oro: los tiers se leen, no se reconstruyen de memoria.** Toda síntesis se construye leyendo los mapas de evidencia. Revertirla invalidaría la trazabilidad del corpus. → **Vigente, y en `instrucciones v2`.**

**ADR-03 · Firewall genético: la genómica queda fuera del corpus conductual.** → **Superada por ADR-19** (reformulada, no eliminada).

**ADR-04 · Marcar procedencia: población EN México ≠ diáspora ≠ marco importado.** Fue *la* falla recurrente (simpatía, machismo, marianismo son de diáspora). → **Vigente, y regla del Bloque A.**

### Corrección del eslabón débil

**ADR-05 · El choque honor vs. dignidad se resuelve a favor de emociones morales.** Smith 2017: autopercepción de dignidad, r=.96 dignidad-face. El dato de Castillo se conserva; se retira la etiqueta "honor". → **Vigente. Ejecutado en la fuente el 27/jul.**

**ADR-06 · Hofstede pasa de causa a correlato (crítica calibrada, no rechazo).** McSweeney es validez de constructo, no inexistencia. → **Vigente. Ejecutado en la fuente el 27/jul.**

### Instrucciones v2

**ADR-07 · El Bloque B aplica solo a reports temáticos.** → **Vigente.**

**ADR-08 · Se añade el Bloque C (validación forense) con sus tres blindajes.** → **Vigente, con el límite de ADR-29 sobre anti-confusión.**

**ADR-09 · Sección 11 opcional: reglas SI-ENTONCES para reports que alimenten el modelo.** → **Vigente.**

### Re-alcance

**ADR-10 · El sistema indígena-comunal vivo queda FUERA POR DISEÑO.** Es *otro orden institucional*, no un México sub-medido. → **Vigente.** *(Originada por el usuario.)*

**ADR-11 · La huella indígena difusa NO necesita perfil propio.** → **Vigente.**

**ADR-12 · El perfil rural mestizo se funde en el perfil 2.** De 8 perfiles a 6. → **Vigente. Errata residual corregida en modelo v2** (§3 decía "ocho perfiles").

**ADR-13 · La limitación real es clase *dentro* de la modernidad.** → **Vigente.**

### Ronda 4 · Validación

**ADR-14 · La ficha canónica se vuelve fuente de verdad ejecutable.** Motivada por un fallo real: V1 no pudo leer los documentos y reconstruyó de memoria. → **Vigente. La decisión de arquitectura más importante del programa.**

**ADR-15 · "Calidad y dignidad > precio en populares" se degrada a NO VALIDADA.** → **Vigente.** ⚠️ *Matiz de Hito 2: la regla del modelo que V1 rompió era **fantasma**. El constructo se degrada por su propia evidencia, no por haber roto una regla.*

**ADR-16 · G2 se refina: opera mediado por la estructura de crédito.** → **Vigente.**

**ADR-17 · El riesgo del crédito popular se relocaliza al prestamista.** → **Vigente.** *(n=2: Famsa y Crédito Real. Certificado como "la estructura decidió estos dos", no como ley general.)*

**ADR-18 · La percepción del secreto del voto es el canal causal del clientelismo.** 0.06 → 0.63 según observabilidad. → **Vigente.**

**ADR-19 · El firewall genético se reformula (reemplaza ADR-03).** Prohibida la inferencia ascendencia → conducta de grupo; admitido un canal individual estrecho (ADH1B, CYP2A6). → **Vigente.**

**ADR-20 · La confianza radial como canal de difusión se queda en HIPÓTESIS.** → **Vigente.** ⚠️ *Dos correcciones: (a) el report de tecnología **ya la tenía tierada así** — ADR-20 la redescubrió porque el modelo no lo leyó; (b) el desdoblamiento **nunca llegó al motor** hasta el modelo v2.*

### Simulador MILPA

**ADR-21 · El LLM queda FUERA del loop de decisión.** Motor de reglas compilado, determinista, auditable. → **Vigente.**

**ADR-22 · Los `params` se derivan cada tick; nunca son fijos por perfil.** Con params fijos el simulador sería esencialista por construcción. → **Vigente. Innegociable.**

**ADR-23 · Mapa doble obligatorio: conducta + espejo estructural.** → **Vigente.**

**ADR-24 · No se construye motor ABM ni síntesis poblacional propios.** → **Vigente.**

**ADR-25 · Gate de Fase 1: `bt.oxxo_vs_codi` debe pasar sin tunear a mano.** → **Vigente. ✅ CORRECCIÓN APLICADA el 28/jul/2026** *(ver ADR-37)*. ⚠️ *Histórico del defecto: la spec v0.1 describía la salida esperada en términos de **canal** —"el producto con canal de confianza se adopta; el institucional-frío no"—, lo que **conflacionaba §3.1 (canal personal, G1a) con §3.3 (utilidad vs. coerción)**. La explicación canónica del fracaso de CoDi es **riesgo fiscal percibido + fricción**, no desconfianza. Con esa spec, si MILPA implementaba bien el mecanismo de confianza y mal el de coerción, **el backtest pasaba igual, por la razón equivocada.* **El defecto estuvo abierto desde la Ronda 4: era el S2 más antiguo del programa.**

### Ronda 5 · Auditoría de la validación *(nuevo en v1.1)*

**ADR-26 · Los disparadores de contexto tienen DOS niveles, no uno.** Siete globales + **42 palancas de dominio**, evaluadas contra `(perfil, params, d_global, d_dominio)`. El modelo siempre tuvo dos niveles; la spec implementó uno, y las palancas quedaron invisibles para el bucle. **El gate de Fase 1 depende de `riesgo_fiscal_percibido`, que vive en §3.3 y no existe entre los siete globales.** *Adenda: entran como **booleanos de contexto**, no como parámetros calibrables — son estados, no magnitudes.* → **Vigente. S2.**

**ADR-27 · El choque alegría vs. malestar es un ARTEFACTO DE AGREGACIÓN, no una contradicción.** México sale #10 mundial en satisfacción vital y a la vez registra 18.1M de carga de salud mental, 39.8% de soledad en mayores y 135,445 desaparecidos. **Ambos lados son verdaderos en sus segmentos y solo chocan al promediarlos en un número nacional.** Se prohíbe todo parámetro de bienestar agregado nacional (modelo §5.4): es el objeto que fabrica la paradoja. Las dos resoluciones fáciles —*"feliz a pesar de todo"* y *"eso es negación"*— son igual de esencialistas. **Pendiente real y separado:** la escalera de Cantril mide **evaluación vital, no alegría**. **Crea la severidad S5 y el casillero de §5.1.** → **Vigente. S2.** *(Reformulada en mesa: el ADR original la declaraba "irresuelta"; el usuario objetó que ambas pueden ser verdad, y el veredicto correcto resultó ser que la pregunta estaba mal planteada.)*

**ADR-28 · Cuatro cambios de esquema.**
- **28.a · `procedencia` obligatoria en cada número** (`MEDIDO`/`DERIVADO`/`ORDINAL→CARDINAL`/`ASIGNADO`); el validador rechaza sin ella. *De **144** números, 4 están medidos; hoy un 0.93 de ENVIPE y un 0.74 asignado se ven idénticos.* **Corolario, duplicado como guardarraíl de lectura:** ninguna salida con precisión decimal.
- **28.b · `confianza_institucional` de escalar a vector.** *Marina 89%, escuelas 77% vs. partidos 23.9%. Un escalar predice que quien desconfía de la policía desconfía de la Marina.*
- **28.c · Base por perfil solo con mecanismo estructural nombrado**, con **condición de dominancia** verificable: un agente del perfil 2 en celda de baja violencia debe quedar por debajo de uno del perfil 1 en celda de alta violencia. Si el orden no se invierte, la base domina al entorno y el parámetro es un rasgo.
- **28.d · `params_base` sale de una distribución, no de un punto.** *Con puntos, el modelo produce seis clases de mexicano — la forma estadística del esencialismo.*

→ **Vigente. S2.** *(28.b, 28.c y 28.d resultaron ser los parches de tres fallos que la batería de refutaciones confirmó después de redactarse el ADR.)*

**ADR-29 · La propagación es bidireccional.** Ver §3.1. Motivada por **seis casos consumados**, cinco reparados y uno no: **PD-01, 14 descartes irrecuperables.** → **Vigente. S2.**

**ADR-30 · `familismo` se desdobla en dos parámetros; no se curva uno.** `familismo_apoyo` (positivo) y `familismo_obligacion` (negativo o no monotónico). *Motivación: la refutación A.23 falló — `G5 → familismo: 0.50` es monotónico positivo, pero Cahill 2021 halla efecto protector, Zeiders 2013 halla que el familismo **obligatorio** no protege y puede ser riesgo, y Fuligni 1999 halla relación **curvilínea**. Un coeficiente monotónico no admite el hallazgo.* **Por qué desdoblar y no curvar:** apoyo y obligación son constructos distintos (Calzada 2012), no extremos de una escala; y un parámetro curvado **no puede estar en dos puntos de la curva a la vez** — que es la situación de la cuidadora, con apoyo alto y obligación alta simultáneos. **Check obligatorio:** una configuración donde `familismo_obligacion` alto mejore todos los desenlaces se rechaza en compilación. ⚠️ *Ambos parámetros son `ASIGNADO` y heredan marca **(b)**. Se pasa de un número inventado a dos.* → **Vigente. S2.** *(Corregida en mesa: la propuesta original retiraba `familismo` de G3; se conserva ahí como `familismo_apoyo`, porque en G3 el mecanismo es pooling —la tanda— y `§3.1` enruta el ahorro informal por ese canal.)*

---

### Ronda 6 · Saldo de deuda documental *(nuevo en v1.2 — 28/jul/2026)*

**ADR-31 · Se retira el "híbrido" de honor del report foundational.** El texto decía que México es un híbrido: honor en lo rural/tradicional, dignidad en lo urbano/educado. **Se retira**, por tres razones: (a) convierte una diferencia de **clase** en una diferencia de **cultura**, que es el movimiento que este corpus existe para evitar; (b) **dignidad y face correlacionan r=.96** — un "híbrido" presupone una oposición que los datos no muestran; (c) la clasificación honor/dignidad/face es un marco importado **(c)** que el sujeto mexicano, preguntado, no reconoce (Smith et al. 2017: 2.º en dignidad, 5.º en honor). **Lo que se conserva:** sensibilidad reputacional alta `[MEDIA]`, leída como **gestión de face bajo autopercepción de dignidad**. → **Vigente. S2.** *Cierra el tercero y último caso de propagación fallida reparable.*

**ADR-32 · Todo principio nuevo nace con su artefacto de salida.** Motivado por el hallazgo del 28/jul: **dos de los seis casos de propagación figuraban como ✅ sin estarlo**, y el glosario, el modelo y la gobernanza repetían el ✅ unos de otros. La causa raíz no fue negligencia: fue que **nada faltaba visiblemente** cuando el parche no se aplicaba. Se instituyen tres requisitos mecánicos:
- **a) Retropropagación (ADR-29.a):** un caso no se marca ✅ sin `grep` verificado contra el report dueño. El artefacto que debe existir es la **nota de corrección fechada en la fuente**.
- **b) Regeneración de la ficha:** toda regeneración adjunta **diff de cobertura** (reglas del motor por §, presentes en la ficha, lista nominal de ausentes). Sin diff, la regeneración no se da por hecha.
- **c) Constructo sin glosario:** el validador rechaza toda regla de `modelo §3` cuyo `PORQUE` nombre un constructo ausente del glosario. Comprobación mecánica por `grep`.
→ **Vigente. S2.** *Este ADR es la generalización del patrón que explica casi todos los fallos del programa: principio declarado sin requisito de salida.*

---

**ADR-33 · Se prohíbe la diagonal en el `ENTONCES` de una regla.** Motivado por `§3.7`: *"se vive como derecho **/** gratitud al líder"* pegaba dos hipótesis **rivales** —si el apoyo es un derecho no se debe gratitud a nadie y el titular es reemplazable; si es gratitud al líder es favor personalizado y no derecho—. **Una afirmación que contiene su propia negación no es falsable, y el defecto es de redacción, no de dato.** Al partirla aparecieron un tier mal leído (la mitad de atribución es `Media` correlacional según el forense, no `Fuerte`) y una rotura archivada que nunca bajó al motor (`conf.08`).
**Requisito de salida:** el validador rechaza toda regla cuyo `ENTONCES` contenga `/` u `o` entre dos predicados de conducta distintos. Comprobación mecánica. → **Vigente. S2.**

**ADR-34 · Todo forense cierra con TABLA DE PROPAGACIÓN, o no se archiva como canónico.** Motivado por el `barrido-propagacion-forense`: los cinco forenses produjeron **22 veredictos ROMPE/MATIZA** y **6 nunca bajaron al motor** (tasa de fuga ~41%), incluida una rotura que tocaba **G3, el único generador probado**. **El patrón no fue aleatorio: se fugó lo condicional.** Llegaron los veredictos binarios —"esto está roto"—, que caben en una línea de changelog; no llegaron los matices con condición —*"cede bajo proximidad y monitoreo"*, *"el techo está en 15–20%"*, *"parcialmente refutado como motor primario"*—, que obligan a reescribir la regla. **La retropropagación se ejecutó donde era barata.**
**Requisito de salida:** tabla con cuatro columnas — veredicto · regla del motor **citada textualmente** · edición concreta que exige · casilla de aplicado con fecha. Sin tabla, el forense no entra al canon. *ADR-29 ya ordenaba propagar; lo que faltaba era que el forense pudiera terminar sin dejar nada que faltara visiblemente.* → **Vigente. S2.**

**ADR-35 · Se amplía el alcance del motor al crédito, del lado del DECISOR — no del oferente.** Decidido el 28/jul para bajar P-04, P-05 y P-06 del barrido forense, que exigían reglas de crédito que el motor no tenía formuladas. Entran dos reglas en `§3.1` —**techo cuantificado de la disposición a pagar** (mora regulada 15–20%, viable solo con CAT de tres dígitos) y **advertencia condicional de la baja fricción** (`MEDIA`, tier asignado literalmente por V5)— y una prohibición dura en `§5.5` (**no afirmar burbuja**; el término admitido es *riesgo latente focalizado y vigilable*).
**Frontera explícita:** el motor **sigue sin entidad prestamista**. Modela al decisor. El hallazgo mejor sostenido del corpus sobre crédito —*el riesgo vive en el fondeo y el gobierno corporativo del prestamista, no en el deudor*— **no se puede representar aquí**, y su refutación sigue sin objeto. **Ampliar al lado de la oferta es una decisión distinta y mayor, que este ADR NO toma.** → **Vigente. S2.**

**ADR-36 · Nomenclatura versionada obligatoria, y se elimina la ficha canónica.** Dos partes de la misma decisión, motivadas por 22 versiones de archivo en una sola sesión y por la imposibilidad de distinguir dos archivos con el mismo nombre y la misma versión declarada.

**(a) Nomenclatura.** `<nombre-estable>-v<MAYOR>.<MENOR>.md`. MAYOR = estructura o alcance; MENOR = contenido. Cada archivo abre con bloque de **ARCHIVO · REEMPLAZA A (borrar) · VERIFICAS ASÍ · NOMBRE ESTABLE**. **Regla que lo sostiene: las referencias internas citan el NOMBRE ESTABLE, nunca el nombre de archivo** (*"ver `modelo §3.B`"*, no *"ver `modelo-decision-v3.0.md`"*), para que subir versión no deje referencias colgando. *Requisito de salida: un archivo sin bloque de cabecera no se sube.*

**(b) Se elimina `ficha-canonica-modelo.md`.** No contenía **ninguna afirmación propia**: era una compresión del modelo v1, que no era autocontenido. Desde el v2 el modelo lo es, así que la ficha solo aportaba **superficie de desincronización** — y esa desincronización **fue el mecanismo del Hito 2**: *de 13 reglas que los verticales dijeron estresar, 6 no existían en el motor y 4 divergían*. No inventaron: leyeron una ficha desfasada que omitía cuatro reglas `[FUERTE]` y degradaba una. Sus tres bloques con valor propio —leyenda de procedencia, alcance y frontera, e instrucción de cita textual— **se absorben en `modelo` §0.1, §0.2 y §9**. **Lo que se pega en los prompts pasa a ser el modelo íntegro.**
**Efecto medido:** un cambio típico pasa de tocar 6 archivos a tocar **1 o 2**. → **Vigente. S1** *(cambio de estructura del programa)*.

**(c) Adenda del 28/jul — las series numeradas también se versionan, con prefijo común y orden explícito.** Detectada al aplicar (a): los tres documentos de MILPA usaban `01/02/03` como nombre, y ese prefijo **era** su nomenclatura — codificaba **orden de lectura y dependencia**. Renombrar solo el `02` rompió la serie y dejó al documento diciendo *"Documento 2 de 3"* contra una numeración que ya no existía. **Es el defecto que ADR-36 existe para evitar, cometido al aplicarlo.**
**Regla:** una serie se renombra **completa**, con prefijo común (`milpa-whitepaper` · `milpa-spec` · `milpa-plan`), y **el orden de lectura pasa del nombre al cuerpo** — bloque explícito en la cabecera de los tres. *Un orden codificado en el nombre de archivo se pierde en cuanto el nombre cambia; escrito en el cuerpo, sobrevive a cualquier versión.*

**ADR-37 · El gate de Fase 1 exige TRES condiciones, no una: reproducción, prueba de mecanismo y anti-confusión.** Corrige la especificación que ADR-25 dejó pendiente desde la Ronda 4.

**(A) Reproducción** — con `coercitivo` y `riesgo_fiscal_percibido` encendidos, la adopción tipo CoDi queda **<10%** de la del canal retail-efectivo. *Necesaria, no suficiente: es lo único que pedía la spec v0.1.*
**(B) Prueba de mecanismo** — al apagar **`riesgo_fiscal_percibido`** con **el canal constante**, la brecha debe **colapsar ≥70%**. Si no colapsa, el modelo llegó al desenlace por otro camino.
**(C) Anti-confusión** — al apagar **el canal de confianza personal** con `riesgo_fiscal_percibido` encendido, la brecha debe **PERSISTIR** (se reduce <30%). **Ésta faltaba entera.** Sin ella el gate no distingue si pasó por §3.3 o por G1a — y **un gate que no distingue cuál de dos mecanismos lo hizo pasar no es un gate: es un espejo.**

**El gate pasa solo si A y B y C.**

**Dependencias verificadas:** `riesgo_fiscal_percibido` es disparador de **nivel 2** (ADR-26) y la spec v0.1 solo implementaba el nivel 1 —**el campo del que dependía el gate era invisible para el bucle**—; y la regla espejo `tramite.gobierno_digital.util_sin_coercion` ya está restituida en `tramite.yaml` v0.2.0, sin la cual apagar el disparador caería en `NO_COVERAGE` y **el gate pasaría por pérdida de cobertura, no por prueba de mecanismo**.

⚠️ **Los umbrales de B y C (≥70%, <30%) son ASIGNADOS**, no medidos: se eligen porque un colapso parcial no distingue mecanismos. **Calibrar contra series de adopción de SPEI antes de correr Fase 1.**
⚠️ **Límite declarado, no resuelto:** el gate **no separa coerción de fricción**. La explicación canónica del fracaso de CoDi tiene dos componentes y `riesgo_fiscal_percibido` solo captura el primero. → **Vigente. S2 → cerrado.** *Desbloquea `R3.4` del Hito D.*

**Hallazgo colateral, mismo día, misma familia:** la regla `civico.voto.clientelar` de la spec compilaba **`p: 0.63` con tier `FUERTE`**, y ese 0.63 es la cifra de **laboratorio** de Ascencio-Chang (2025), no de campo. **Se degrada a `MEDIA`** y se crea el campo obligatorio **`procedencia_p`** (`CAMPO` / `LABORATORIO` / `DERIVADA` / `ASIGNADA`): *es la disciplina de `procedencia.yaml` aplicada a las probabilidades de regla, a las que nunca se les había aplicado.* **Una `p` de laboratorio no puede llevar tier `FUERTE`.**

**Registro de decisión · Perímetro del Hito D = 27 reglas** *(28/jul/2026, antes de escribir el primer falsador)*. 20 `[FUERTE]` + 1 `[FUERTE como correlación]` + 1 compuesta `[FUERTE / MEDIA]` + **5** `[MEDIA-FUERTE]`. *(Eran 26; la partición de protesta/autodefensa por ADR-33 convirtió una en dos.)* Las `[MEDIA-FUERTE]` se falsan **contra la lectura fuerte**: si no sobreviven quedan **degradadas a `[MEDIA]`**, no refutadas. La compuesta lleva **un falsador por mitad**. La `[FUERTE como correlación]` se ataca **como correlación**, no como causa — atacar la causa fue el error de V1.

⚠️ **Corrección de RÓTULO, 29/jul/2026.** Este registro decía *"20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas"*, tratando a `R1.4` (`[FUERTE como correlación]`) como si fuera una segunda regla partida. **Solo existe una compuesta:** `R4.3` (`[FUERTE / MEDIA]`), cuya ficha en `hitoD-preregistro` se declara "dos falsadores, uno por mitad". `R1.4` es un tier distinto — `[FUERTE como correlación]` —, no una mitad: lleva un solo falsador, contra la correlación. **El perímetro NO cambia: siguen siendo las mismas 27 reglas de esta misma decisión del 28/jul, antes del primer falsador.** Propagado a `modelo §7` (cambio 34) y `estado §4·S2` y `§7`.

---

### Sesión de correcciones · 29/jul/2026 (tarde) — censo de integridad documental

**ADR-38 · Ningún hallazgo sobre la ausencia o el contenido de un texto en otro archivo baja al canon sin el `grep`/lectura literal contra ese archivo, con línea citada.** Motivado por el caso "pelón": `a79227e` afirmó haber corrido `grep -rn "pelón"` y reportó que la frase "no aparece en ese archivo, ni en ningún otro del repo"; el comando real da 4 resultados, incluida la línea exacta que se dijo vacía. **17 segundos después**, en el mismo lote de trabajo, `7d6535e` bajó esa afirmación sin re-verificarla a `canon/estado-programa` — ÚNICA FUENTE DE ESTADO — y de ahí se propagó una tercera vez a `TRANSFER-maestra-8.md`, citada como *ejemplo de método riguroso*. **Cubre la dirección que ADR-29 no cubre:** ADR-29 (§3.1, retropropagación) protege contra hallazgos **correctos** que nunca bajan del forense al canon. Este ADR protege lo contrario: hallazgos **falsos** que sí bajan, y bajan rápido. Requisitos:
- **a)** Toda afirmación de la forma *"F dice/no dice X"*, *"la cita a F:L no checa"*, *"el archivo F no existe/no contiene Y"* que entre a un artefacto de `canon/` lleva, en el mismo commit, el comando de verificación y su salida real — no basta con citar la nota que lo afirma.
- **b)** Una afirmación sobre el contenido de un archivo ajeno **no hereda verificación** de la nota que la reporta. Bajarla a canon exige correrla de nuevo contra el archivo, no contra el reporte del hallazgo.
- **c)** Candidato a test mecánico, no implementado (requiere extraer la cita del texto libre — "T-grep-de-cita", `censo-integridad-v1_0.md §6`): hasta que exista, este ADR es la salvaguarda de proceso.
→ **Vigente. S2.** *(Aprobado 29/jul/2026, sesión de correcciones sobre `censo-integridad-v1_1.md §3`.)*

**ADR-39 · Verificación de premisas antes de ejecución.** Quien ejecuta un encargo verifica sus premisas contra el archivo **antes** de obedecerlo. Si una premisa no se sostiene, **se detiene y lo reporta** — no la ejecuta, y no ajusta el texto del encargo ni del corpus para que cuadre con una premisa falsa. **Motivado por:** la sesión de correcciones que produjo ADR-38 se comisionó desde un reporte de conversación no verificado contra el repo. Verificar antes de ejecutar encontró, entre otras cosas: la cita de `censo-integridad-v1_0.md` a `estado-programa-v1_9.md:208,234` ("idéntico") apunta a una línea 234 que no existe en un archivo de 212 líneas — la premisa de "dos citas idénticas" no se sostenía tal como estaba escrita; y tratar las tres ocurrencias de "107 WARN" del mismo archivo con una corrección uniforme habría fabricado una afirmación histórica falsa en una entrada de changelog que era exacta cuando se escribió. **Por qué vive aquí y no solo en `instrucciones-proyecto-v2.md`:** esa regla ya existe del lado de las instrucciones de sesión (v2.1), pero un artefacto de `canon/` no puede citar una instrucción de chat — este ADR le da ancla citable dentro del corpus. Requisito: antes de aplicar cualquier corrección que un encargo describa con un hecho verificable (cifra, cita, archivo, estado), correr la verificación **antes** del primer edit; si el resultado contradice la premisa, el hallazgo se reporta como entregable — no se fuerza el edit para que la premisa parezca correcta. No aplica a juicios de valor o preferencias del encargo, solo a hechos sobre el estado del repo.
→ **Vigente. S2.** *(Aprobado 29/jul/2026, misma sesión.)*

⚠️ **Nota de la sesión, sobre versión de archivo:** ADR-36 pide bump de versión MENOR ante todo cambio de contenido canónico, lo que llevaría este archivo a la siguiente versión punto-menor y a un rename de archivo, con su cascada de referencias (`estado §0`, cabeceras cruzadas). **No se ejecuta aquí** — el encargo que aprobó estos dos ADR pidió aplicarlos con los números correspondientes, no el bump de versión completo, y ese es un cambio de mayor alcance que merece su propio diff aprobado por separado.

---

**ADR-40 · Forma canónica de un veredicto archivado; vive en un bloque designado del pre-registro, no en `estado` ni en prosa libre.** Corrige el diseño original de `T18` (T-PASO2-EJECUCION, sesión de tests, 29/jul/2026), rechazado dos veces:

- **Primer rechazo:** derivaba su conteo "real" leyendo `canon/estado-programa` y lo comparaba contra el contador declarado en el mismo archivo — no cruzaba frontera de archivo, el mismo alcance autorreferencial que `T05` (constructos contra una lista fija en `check.py`, no contra un tercer origen).
- **Segundo rechazo:** el rediseño movió la forma canónica a `hitoD-preregistro`, pero permitía que apareciera en cualquier prosa del archivo — **no distinguía emitir de citar o hipotetizar**. El propio primer borrador de la Nota 5 que archivaba el veredicto de `R1.1` disparó su propio patrón al citar, entre backticks, la narración vieja de `estado`. Un archivo append-only que existe para discutir fichas necesita poder decir *"si `R3.2` → veredicto `B`…"* como hipótesis sin que eso fabrique un veredicto falso.

**Forma canónica**, para que un test pueda derivarla mecánicamente: `` `RX.Y` → veredicto `Z` `` — ID de regla entre backticks (el de `modelo §7`, Registro congelado), flecha `→` (no `->` ni `=>`), la palabra `veredicto` literal en minúsculas, la letra `A`/`B`/`C`/`D` entre backticks. Puede llevar paréntesis explicativo después; no antes.

**Dónde vive:** en un bloque designado, append-only, al final de `hitoD-preregistro` (`## Registro de veredictos archivados`) — **la única sección que un test puede leer** para derivar el conteo real. Fuera de ese bloque, la forma canónica en cualquier prosa de cualquier documento es cita o hipótesis, nunca emisión, y ningún test la cuenta. `estado §7` sigue narrando el resultado y contando cuántos van (`estado:192`), pero no es la fuente del archivo — es un consumidor, igual que cualquier otro documento que la cite.

**(a) El detector de forma sospechosa es heurístico, no un aserto.** `T18` también busca, dentro del bloque, líneas con forma de veredicto que no cumplan la forma exacta (ID de regla + la palabra "veredicto" a poca distancia, sin la flecha/backticks correctos) — para que una variante no se archive invisible. Sus constantes de proximidad (≤20 caracteres entre el ID y "veredicto", ≤15 entre "veredicto" y la letra) están **afinadas a mano contra un solo caso real conocido** (flecha ASCII `->` en vez de `→`), no derivadas de un principio. Falsos negativos conocidos: cualquier variante que separe el ID de regla y "veredicto", o "veredicto" y la letra, más allá de esas ventanas no se detecta. Falsos positivos conocidos: antes de esta versión, la clase de carácter de la letra era insensible a mayúsculas (heredaba `re.I` de "veredicto"), lo que habría marcado la preposición española "a" como si fuera la letra `A`; corregido, la letra ahora exige mayúscula exacta — pero el detector sigue sin garantía formal contra cualquier prosa futura que combine, por casualidad, un ID de regla entre backticks con la palabra "veredicto" y una letra mayúscula A-D dentro de esas ventanas.

**(b) Propagación legítima vs. editar para que un test calle.** Este mismo ADR subió el conteo de ADR de la sesión anterior en una unidad, y eso obligó a corregir tres citas que todavía citaban el conteo viejo (`estado:25`, `estado:95`, `gobernanza:2`) para que `T15` no quedara en rojo. **Eso es propagación legítima:** el número de ADR cambió de verdad al aprobar este ADR, y las citas dependientes deben reflejar el nuevo estado real — es exactamente lo que `T15` existe para exigir. Es una jugada **distinta y prohibida** editar un documento —o inventar una excepción, un bloque, una exención— **para que un test deje de fallar sin que el hecho subyacente haya cambiado**. La diferencia no es el gesto (ambas son ediciones), es si el número editado corresponde a un cambio real verificado (aquí sí: `grep -c` contra `gobernanza` da 40) o si el edit existe únicamente para silenciar la alarma.

**(c) Una propiedad afirmada de un test se verifica con un caso real del corpus, no con una aserción en el comentario.** Precedente, el mismo día: el punto (a) de arriba, en su primer borrador, afirmaba que quitar `re.I` de la letra corregía el falso positivo de la preposición "a" — sin correr la línea vieja contra la línea nueva para comprobarlo. Se corrió: `` `El caso de \`R5.1\` tiene veredicto a evaluar todavía.` `` — el patrón viejo (con `re.I` heredado) la marcaba como veredicto `A`; el nuevo, no. La corrección quedó verificada, no solo declarada. **Regla general:** un comentario o docstring que describe qué hace o qué evita un test es una afirmación como cualquier otra en este corpus — pesa lo mismo que una cifra en `estado`, y se sostiene igual: con un caso real corrido, no con la autoridad de quien lo escribió.

**(d) Riesgo conocido: reformular prosa para no disparar un test.** El remedio se aplicó dos veces hoy, en la misma sesión que escribió este ADR: la Nota 5 de `hitoD-preregistro` se reescribió para no disparar `T18` (movió el archivo del veredicto fuera de la prosa narrativa), y el punto (b) de este mismo ADR se reescribió para no disparar `T15` (evitó el par dígito+"ADR" literal al explicar la propagación 39→40). **Es válido mientras el texto reformulado siga afirmando lo mismo** — ninguna de las dos reformulaciones cambió un hecho, solo la forma de decirlo. Pero **T18 tiene una zona designada que hace esa distinción estructural** (dentro del bloque cuenta, fuera no, sin importar la forma); `T14` y `T15` no tienen zona equivalente — su única defensa contra este mismo choque futuro es que quien escribe prosa sobre "cuántos reports" o "cuántos ADR" recuerde reformular a mano. Es una disciplina, no una garantía, y no tiene test que la verifique.
→ **Vigente. S2.** *(Aprobado 29/jul/2026, misma sesión de tests, revisado tres veces antes de aprobarse.)*

**ADR-41 · Una regla aprobada en chat no rige hasta que existe en archivo.** Antes de eso es hipótesis, aunque todos la estén siguiendo. **Motivado por:** seis de los elementos de la subida de `instrucciones-proyecto-v2.md` a v2.2 (tres reglas de v2.1, cuatro de v2.2 más su pregunta de auditoría — la unión real, no las dos listas de "cinco" que traía el traspaso, que no coincidían entre sí) existieron solo en conversación, gobernaron el trabajo de una sesión completa, y se perdieron cuando la sesión se hizo en un entorno sin commitear. El único respaldo fue el chat. **Es la misma familia que ADR-29** —hallazgo correcto que no baja al motor— un piso más arriba: regla correcta que no baja al canon.

**Segundo hallazgo, derivado en sesión el 29/jul/2026.** La capa de autoría del repo no registraba firmante humano. De 25 commits, **21 tienen a Claude como autor, 4 a `corpus@local`, cero a un humano** (verificado: `git log --format='%an <%ae>'`). El trailer `Co-Authored-By` nombraba a Claude en **17 líneas** —es decir, duplicaba al autor en vez de complementarlo— y en **cuatro formas distintas** (`Claude`, `Claude Opus 4.6 (1M context)`, `Claude Opus 5`, `Claude Sonnet 5`), una con especificación de ventana de contexto dentro del campo de identidad. **La historia previa no se reescribe:** es el registro fiel de cómo se hizo el trabajo, y falsificarla sería falsificar procedencia. De aquí adelante: **Jonas autor, Claude co-autor, una forma normalizada de la cadena de modelo.**
→ **Vigente. S2.** *(Aprobado 29/jul/2026.)*

**ADR-42 · Qué significa el verde en este repo.** El único control automático sobre `main` es `.github/workflows/verify.yml` (`push`/`pull_request`/`workflow_dispatch`, un job, `python3 tests/check.py --baseline`). Tres registros retroactivos, ninguno existía antes en archivo:

**(1) El control cambió de semántica sin ADR.** El commit `f320550` ("CI: usa el modo linea base en vez de check.py sin banderas") movió el paso de CI de `check.py` sin banderas a `check.py --baseline` — un cambio de qué cuenta como éxito del único gate automático del repo, hecho sin pasar por gobernanza. Este ADR lo registra ahora, no lo autoriza retroactivamente ni lo revierte.

**(2) Verde no significa "0 fallas".** Significa **"0 fallas nuevas frente a una línea base congelada"** — hoy esa línea base (`tests/baseline.json`, `head afa7c7f`) contiene **18 FAIL y 81 WARN**, y el CI pasa con esos 99 presentes. Mecanismo exacto: `_baseline_compare()` (`tests/check.py:824-848`) calcula `nuevos = current - known` sobre la unión de FAIL y WARN, y `return 1 if nuevos else 0` — el proceso solo falla si aparece algo que no estaba en el archivo congelado. Un checkmark verde en la página de Actions no es "sin defectos": es "sin defectos que no supiéramos ya".

**(3) Límite de la clave, descubierto en sesión — no es un defecto, es una propiedad que hay que declarar.** `_baseline_key()` (`tests/check.py:736-737`) normaliza cada mensaje quitándole el número de línea (`re.sub(r":\d+ ", ": ", msg, count=1)`) antes de convertirlo en clave de comparación — necesario: sin esa normalización, cualquier edición que desplace líneas produciría falsos positivos masivos contra un defecto ya conocido. **Consecuencia declarada:** si un defecto ya congelado se reproduce N veces más en el mismo archivo, la suite no detecta ninguna de las nuevas apariciones — la clave `(test, mensaje-sin-línea)` ya estaba en `known`, y cuenta como la misma. **Caso probado en sesión, no hipotético:** dos WARN de T03 sobre `forense/censo-integridad-v1_1.md` (líneas 49 y 85), ambos citando el mismo nombre de archivo histórico (estado-programa, versión ya superada), colapsan en una sola clave — 82 WARN crudos, 81 tras la normalización. **Corolario operativo:** `--baseline` protege contra defectos *nuevos*, no contra la *multiplicación* de uno ya conocido dentro del mismo archivo; contar cuántas veces se repite un defecto congelado exige leer la salida sin `--baseline`, no confiar en el veredicto de línea base.
→ **Vigente. S2.** *(Aprobado 29/jul/2026, derivado de auditoría de sesión contra `tests/check.py` y `.github/workflows/verify.yml`.)*

**ADR-43 · Esquema de co-autoría (precisión a ADR-41).** ADR-41 pidió "una forma normalizada de la cadena de modelo". Su primera aplicación, cinco commits después, produjo **dos** formas: `Claude Sonnet 5` (cuatro commits) y `Claude Fable 5` (uno) — porque cada commit se escribió con el modelo de sesión vigente en ese momento, y ADR-41 no distinguía si "normalizada" quería decir una cadena fija o un formato consistente. **La historia no se reescribe** — los cinco commits quedan como están. **Precisión, no corrección:** la forma normalizada es un **esquema**, no una cadena única — `Claude <modelo> <noreply@anthropic.com>`, con el nombre del modelo como campo variable y el resto fijo. Es deliberado, no una relajación: registrar **qué modelo** co-escribió cada commit es procedencia más fina, no más débil — la misma disciplina que `procedencia.yaml` exige para los números del modelo, aplicada a la autoría. Verificado: los cinco commits de la sesión de ADR-41 ya cumplen este esquema tal como queda definido aquí — ninguno necesita enmienda.
→ **Vigente. S2.** *(Aprobado 29/jul/2026.)*

**ADR-44 · El repositorio es público; la función del programa pasa de privado-descriptivo a público-auditable.** El repo quedó público el 29/jul/2026 sin registro de decisión — mismo patrón que ADR-42(1): un cambio de semántica del programa entero, hecho sin pasar por gobernanza. Este ADR lo registra ahora, no lo autoriza retroactivamente ni lo revierte, y fija sus requisitos de salida:

**(a) Capa legal en el árbol — verificado en sesión.** `LICENSE`, `AUTHORSHIP.md`, `USO-ACEPTABLE.md`, `AVISO-DE-ALCANCE.md` y `CITATION.cff` existen en la raíz (`git ls-files`, corrido el 30/jul/2026). Ninguno de los cinco falta.

**(b) Re-examen de deuda "asumida a propósito" (regla v2.2).** Toda deuda declarada en `§5` de este documento como "asumida a propósito" queda re-examinada a esta fecha, no solo re-declarada. El dictamen ítem por ítem ya se corrió — este ADR no lo repite ni lo reabre — y vive en `revision-publicacion-2026-07-30.md §1` (tabla "EL EJE"), verificado ahí contra `gobernanza §5`, `estado §4` y `cola.yaml`. Tres deudas caducaron por completo con la función pública (cero datos primarios propios, ya caducada dos veces; las ocho refutaciones sin objeto; el baseline con la autodeclaración falsa de `hitoD-preregistro:8`, congelada "por decisión de mesa" cuando la mesa todavía era privada); las demás siguen decisión con su forma o presentación ajustada, no con su fondo.

**(c) README sin cifra de estado no vigilada por test — PENDIENTE, es F6.** No se cumple hoy. `README.md` sigue teniendo cifras de estado (§"Estado del modelo", §"Falsos positivos conocidos") sin ningún test que las derive y las compare contra el árbol, más allá de la corrección puntual que esta misma sesión aplicó a `README:40` y a los conteos de T03/T10. El molde que cerraría esta condición (`T-README`, mismo patrón que `T16`) está en `cola.yaml` y **fuera del perímetro de la sesión que sella este ADR** — regla de sesión vigente: T-README es F6 y no se toca en sesiones de canon. Este requisito de salida queda abierto a propósito, no por descuido: se cierra cuando exista el test, no antes, y bloquea la apertura de cualquier vía de patrocinio — no el registro de este ADR.

**(d) Ninguna decisión de mesa futura asume lector interno.** Regla hacia adelante, no retroactiva: toda decisión que de aquí en más se registre en `cola.yaml`, en este documento o en `estado` se escribe asumiendo que quien la lee puede ser un desconocido, no el propio equipo. La deuda #12 de la tabla eje citada en (b) — "el repo es privado / esto solo lo leemos nosotros", nunca declarada ni medida — fue la última decisión de mesa que asumió lector interno sin decirlo; no se detectó otra de la misma clase en esta sesión.

**Dato de cierre, aportado por el encargo y no re-verificable desde esta sesión** (sin acceso autenticado a Settings/Insights de GitHub — mismo trato que un supuesto [S1] de `revision-publicacion-2026-07-30.md`, no una cifra derivada de este árbol): con "Preserve this repository" activo, ya existiría copia del árbol en el GitHub Archive Program. Si es correcto, el repliegue a privado **no revertiría la exposición** — cerraría, por el lado de los hechos y no de la decisión, la deuda #12 citada arriba: la restricción "el repo es privado" ya sería falsa incluso antes de este ADR. Verificarlo con acceso autenticado a GitHub queda en cola; este ADR no lo da por confirmado, lo registra como recibido.
→ **Vigente. S2.** *(Aprobado 30/jul/2026, sesión de canon F2/F4. (a) verificado en sesión; (b) referido a `revision-publicacion-2026-07-30.md`, no reabierto aquí; (c) declarado PENDIENTE, condición de salida no cumplida; (d) regla hacia adelante.)*

---

**ADR-45 · Vocabulario fijo de "prueba de falsación corrida"; tres poblaciones, nunca mezcladas sin marca.** Decisión de mesa del autor, 30/jul/2026, sobre la evidencia registrada en `cola.yaml` D-05 (derivada al intentar propagar la corrección de README:40 al canon: cinco líneas de `estado`, `modelo` y `gobernanza` invocaban "una prueba de falsación corrida" sin decir de cuál de tres poblaciones distintas hablaban, más una autocontradicción de `modelo` sobre si G1a está falsado). Las tres respuestas se fijan **antes** de ver resultados y no se renegocian al escribir:

**(1) Denominador — se reportan AMBOS, siempre con etiqueta explícita de cuál es cuál.** Nunca uno solo, nunca los dos en la misma celda sin distinguir. `27` = perímetro elegible del Hito D (`gobernanza §4`, ADR-37); `49` = reglas totales del motor (`modelo §3.B`/§7, T12). `27` es subconjunto de `49`: las dos fracciones son verdaderas a la vez — el defecto era no decir cuál se estaba reportando, no que una de las dos fuera falsa.

**(2) Un veredicto `D` cuenta como prueba corrida.** Se corrió el procedimiento pre-registrado y produjo un veredicto archivado (`R1.1` → `D`, inejecutable por hueco de mercado, no de dato). Condición: la letra viaja junto al conteo, siempre — "2 de 27 corridas (`D`, `B`)", nunca solo "2 de 27". Razón registrable: lo contrario haría que el programa reporte menos trabajo del que hizo, y escondería el hallazgo de `hitoD-R1.1` — que el mercado del seguro agrícola voluntario no existe para la población de volatilidad máxima (Seguro Agrícola Catastrófico no contratable por el productor; Fondos de Aseguramiento concentrados en riego/gran extensión; adopción voluntaria atada al financiamiento).

**(3) Las tres poblaciones se reportan separadas — nunca sumadas, nunca una presentada como otra.**
- **Hito D** — falsación de REGLAS del motor. Vocabulario `RX.Y → veredicto A-D`. Fuente única: el bloque append-only `## Registro de veredictos archivados` de `hitoD-preregistro` (ADR-40). Hoy: 2 de 27 corridas (`R1.1`→`D`, `R3.2`→`B`).
- **Hito C** — falsación de GENERADORES. Vocabulario ✅ probado / ⚠️ contradicho-contestado / ⬜ sin falsar. Fuente única: `forense/hitoC-prueba-generadores.md`. Hoy: G3 ✅, G1b ⚠️ contradicho, G2 ⚠️ contestado, G1a/G4/G5/G6 ⬜ sin falsar.
- **Ejercicio de glosario sobre G1a** (`glosario §6/§10`, 27/jul/2026, "utilidad + fricción baja > confianza", dominio seguro agrícola) — objeto propio. Origen `FORENSE` (`corpus/forense/Apuestas_Conductuales_sobre_el_Consumidor_Mexicano...md`, Etapa 3), veredicto informal B. **Anterior a que el Hito D existiera** (28/jul), **nunca pasó por el protocolo de ADR-40** ni entró al bloque archivado: no tiene ID de regla, no cuenta contra el 27 ni contra el 49, y no es "el Hito D".

**Requisito de salida.** Ninguna afirmación de conteo de veredictos o de corridas de falsación existe en `canon/` fuera de su bloque de fuente única sin decir cuál de las tres poblaciones cita y con qué denominador. `I-07` (candidato a test que mecanice esto) queda abierta — este ADR fija el vocabulario; no construye el instrumento que lo vigile.
→ **Vigente. S2.** *(Aprobado 30/jul/2026, sesión de canon. Cierra `cola.yaml` D-05. Propagado a `modelo` (v3.4, cambio 36, §0.1/§7), `estado` (§0, L5, §4·S3) y `glosario` (§6, §10).)*

---

**ADR-46 · La unidad de contaminación es LA SESIÓN, no la máquina ni el modelo — dos niveles, condición verificable.** Decisión de mesa del autor, 30/jul/2026, sobre la evidencia registrada en `cola.yaml` E-03 (declaraba "esta máquina queda INHABILITADA para pre-registrar contra las encuestas efectivamente descargadas" tras la tanda de Hito D Fase 1, ampliación del Paso 4). El texto original erraba en dos direcciones a la vez:

**(a) Demasiado amplio.** Un modelo no retiene contexto entre sesiones. Una sesión nueva arrancada en frío en la misma máquina no ha leído nada de lo que esa máquina procesó antes y está tan limpia como una sesión en la nube. Inhabilitar hardware desperdicia una vertiente entera del programa: bajo ese criterio, cada tanda de descargas quema la única máquina con salida real a INEGI.

**(b) Demasiado estrecho en lo que sí importa.** Lo que contamina no es dónde corrió el proceso de descarga: es qué puede LEER una sesión nueva en ese entorno — los payloads en `data/raw/`, y la bitácora que describe qué se exploró de la estructura de la fuente antes de bajarlos. Eso se controla con instrucción de encargo (qué archivos toca una sesión), no con qué hardware la ejecuta.

**Criterio fijado.**

**(1) Unidad de contaminación: LA SESIÓN — su contexto de lectura acumulado —, nunca la máquina ni el modelo que la corre.** Dos sesiones en la misma máquina, o la misma sesión reanudada en otra, no comparten contaminación por compartir hardware o proveedor de modelo; comparten contaminación solo si una leyó lo que la otra escribió.

**(2) Dos niveles de contacto con una fuente, que el texto original de `cola.yaml` E-03 colapsaba en uno:**
- **Descarga ciega** — url, sha256, tamaño, formato del payload. No contamina: la sesión no aprende nada sobre el CONTENIDO de la fuente por el solo hecho de haber movido bytes con una URL ya conocida de antemano.
- **Exploración de estructura** — descubrir qué ediciones existen, probar patrones de nombre de archivo, leer cómo el portal organiza sus descargas (títulos de página, JSON-LD, navegación, acordeones). Contamina PARCIALMENTE: no es leer variables ni valores, pero sí es aprender algo sobre la fuente que una sesión sin ese contexto no sabría. Declarar hasta dónde llegó la exploración es obligatorio — no basta con declarar que hubo descarga.

**(3) Condición verificable, que reemplaza la prohibición de hardware.** Una sesión puede pre-registrar contra una fuente **si y solo si** no ha leído `data/raw/` de esa fuente, **ni** la bitácora de la tanda que la bajó, **ni** ningún registro de exploración de su estructura. Es una condición sobre lo que esa sesión ha leído, verificable contra su propio historial de lectura — no una propiedad del entorno donde corre.

**(4) El conservador va del lado de declarar más exploración, no menos.** Cuando el registro de una tanda no permite distinguir con certeza si un contacto con la fuente fue descarga ciega o exploración de estructura, se trata como exploración de estructura completa. Aplicado retroactivamente a `cola.yaml` E-03: ninguna encuesta de la tanda del 30/jul calificó como descarga ciega — las cuatro efectivamente descargadas (ENCIG/`R3.1`, ENIF/`R1.2`, ENVIPE/`R7.2`, ENIGH-nc/`R5.1`) requirieron derivar la lista real del portal probando patrones de nombre por edición, y las tres que NO se descargaron (ENUT/`R5.2`, ENCUCI/`R8.3`, ENSANUT/`R4.2`) también tuvieron exploración de estructura real (JSON-LD, navegación, patrones de nombre) sin llegar a descarga — el E-03 original las declaraba libres de contaminación por no haberse descargado nada, sin ver que la exploración misma ya contamina parcialmente.

**(5) Aplicado a `cola.yaml` E-02.** Verificado en esta sesión: el texto de E-02 ya trazaba la unidad de contaminación sobre "esa conversación", no sobre una máquina — no tenía el defecto (a)/(b) que este ADR corrige en E-03. No requirió reescritura, solo esta constancia de que se revisó.

**Requisito de salida.** Ninguna entrada futura de `cola.yaml` que declare contaminación por descarga o exploración de una fuente usa "máquina" como unidad — usa "sesión" y, si hubo contacto con la fuente antes de la descarga (o en vez de ella), declara el nivel (descarga ciega / exploración de estructura) y hasta dónde llegó.
→ **Vigente. S2.** *(Aprobado 30/jul/2026, corrección ejecutada por una sesión distinta de la que bajó los datos de Hito D Fase 1 Paso 4 — ver `cola.yaml` E-04 sobre por qué esa separación es deliberada. Corrige `cola.yaml` E-03 con nota fechada, texto original conservado íntegro. Verificado contra E-02: sin el mismo defecto, no reescrita.)*

---

## 5. Deuda declarada (decisiones abiertas, conscientemente)

Esto **no** es una lista de pendientes: es deuda que se decidió asumir.

| Deuda | Estado | Decisión |
|---|---|---|
| **Sin datos primarios** (falla raíz) | Abierta | **Asumida a propósito.** Se trabaja con literatura tierizada y validación forense. |
| **Elasticidades / coeficientes** | Abierta, **con ruta** | Los 15 coeficientes son `ASIGNADO`; el corpus es transversal (da estados, no ritmos). ⭐ **`G3 → horizonte_temporal` es calibrable hoy** con el panel rotativo de la ENOE. Sería el **primer coeficiente MEDIDO** de los 107. |
| **Consumo popular D/E, rural** | Abierta | Vacío admitido; el mapa debe mostrarlo pálido, no interpolado. |
| **Confianza radial como canal medible** | Abierta | ADR-20. ⚠️ Ahora **contradicha** por los casos Nu y Kueski: G1b baja a HIPÓTESIS con coeficiente a revisión. |
| **Granularidad municipal** | Abierta | Techo de resolución real del simulador. |
| **Cuatro generadores sin falsar** ⭐ | Abierta | G1a, G4, G5, G6. G4 y G5 sin un solo caso disponible. |
| **Reglas del motor sin prueba de falsación pre-registrada** ⭐ | Abierta | **Es el Hito D** (bloque append-only de `hitoD-preregistro`): perímetro DECIDIDO de **27 reglas**, subconjunto de las **49** del motor. **2 de 27 corridas archivadas** — `R1.1` → `D`, `R3.2` → `B`; 25 de 27 sin corrida (47 de 49 sobre el motor completo). *(No confundir con el ejercicio informal de `glosario §6/§10` sobre G1a/seguro agrícola, 27/jul — ese NO es el Hito D: ver ADR-45.)* |
| **Ocho refutaciones sin objeto** ⭐ | Abierta | El modelo no tiene variable de esfuerzo, colorismo, salud mental ni entidad prestamista. Incluye `ref.A.02` —la única MUY_FUERTE de las 49—. **Decisión pendiente: ampliar el modelo o declarar el alcance y retirarlas.** |
| **PD-01 · 14 descartes** | **Cerrada — pérdida consumada** | Nunca se escribieron. **No reconstruir:** un descarte fabricado es indistinguible de uno real. |
| **Sistema indígena-comunal** | **Cerrada por diseño** | ADR-10. No es deuda: es otro modelo. |

### 5.1 Casillero de pendientes irresueltos *(nuevo en v1.1 — severidad S5)*

Contradicciones que **no se resuelven** y que sin este casillero se caen del sistema.

| # | Pendiente | Estado |
|---|---|---|
| **conf.02** | **Policronía** — Trabajo y Tiempo refutan el mismo mito con **mecanismos opuestos** | Abierto, sin ADR |
| **conf.04** | Alegría vs. malestar | ✅ **Resuelto por ADR-27**: artefacto de agregación. *Queda vivo el desajuste de instrumento (Cantril mide evaluación vital, no alegría).* |
| **conf.05** | **Consumo compensatorio** — Fuerte (consumidor) vs. Hipótesis (salud) | Abierto — **no promediar** |
| **conf.06** | **Magnitud de la confianza interpersonal** — 12% · 21.8% · 22% · 32.1% · 18%; **dos dicen ser la misma ENCUCI 2020 y difieren 10.3 puntos** | Abierto. **Ninguna cifra de confianza se usa como establecida hasta cerrarlo** |
| **honor híbrido** | `foundational` sostiene un híbrido (honor rural + dignidad urbana) que ADR-05 superó | Abierto **por decisión**: es posición matizada, no error, y retirar la etiqueta para todo México podría ser sobre-corrección urbana |

| **conf.07** | `modelo §3.7` empaquetaba **Fuerte + Hipótesis** bajo un solo tier | ✅ **Resuelto 28/jul: regla partida en dos** (v2.1). El ascenso HIPÓTESIS→FUERTE del cambio 10 se sostiene sobre la mitad con identificación causal ("conserva autonomía de voto"); la mitad subjetiva ("se vive como derecho") vuelve a `[HIPÓTESIS]` |

⚠️ **Antes de meter algo a este casillero, aplicar la prueba de ADR-27:** *¿es contradicción real, o alguien promedió?* Dos de los cuatro pueden ser artefactos de agregación y no choques.

---

## 6. Cómo abrir una conversación nueva del proyecto

Para que ninguna corrida vuelva a reconstruir de memoria (el fallo de V1):

| Si vas a… | Pega esto |
|---|---|
| Correr un report temático | `instrucciones-proyecto-v2.md` |
| Correr una validación forense | instrucciones v2 + **ficha canónica** + `prompts-verticales-validacion` **(parchada 27/jul)** |
| Trabajar sobre el modelo | **`modelo`** + este documento |
| Tierizar un constructo | **`glosario`** — único punto legítimo de entrada de un tier |
| Construir el simulador | whitepaper + spec + `milpa/` + ficha canónica |
| Retomar el programa en frío | **`estado`** + este documento |

**Antes de cualquier corrida nueva:** verificar que la ficha canónica esté sincronizada con el modelo (§3). ⚠️ **Hoy no lo está: la ficha es foto del v1.**

**Regla nueva de plantilla forense** *(Hito 2)*: toda regla que un encargo mande estresar se **cita textualmente del motor §3**, con tier, dominio y perfiles. Si no trae cita, se marca como propuesta nueva y su veredicto **no cuenta como validación del modelo**.

---

## 7. Bitácora de versiones de este documento

| Versión | Qué cambió |
|---|---|
| 1.0 | Creación. ADR-01 a ADR-25, registro de artefactos y protocolo de propagación tras cerrar Ronda 4 y Fase 0. |
| **1.14** | **30/jul/2026 — ADR-46: la unidad de contaminación es LA SESIÓN, no la máquina ni el modelo, corrige `cola.yaml` E-03.** El texto original de E-03 declaraba "esta máquina queda INHABILITADA" tras la tanda de descargas de Hito D Fase 1 — demasiado amplio (un modelo no retiene contexto entre sesiones; una sesión nueva en la misma máquina está tan limpia como una en la nube) y demasiado estrecho (lo que contamina es qué puede LEER una sesión nueva — `data/raw/` y la bitácora de la tanda —, no dónde corrió el proceso). Fija: (1) unidad = sesión; (2) dos niveles — descarga ciega (no contamina) vs. exploración de estructura (contamina parcialmente, declarar hasta dónde); (3) condición verificable — una sesión pre-registra contra una fuente si no leyó `data/raw/` de esa fuente, ni la bitácora de su tanda, ni ningún registro de exploración de su estructura; (4) el conservador declara más exploración, no menos — aplicado a E-03, NINGUNA de las siete encuestas de la tanda fue descarga ciega, incluidas las tres (ENUT/ENCUCI/ENSANUT) que el original declaraba libres solo por no haberse descargado. E-02 verificada: sin el mismo defecto, no reescrita. Corrección ejecutada por una sesión distinta de la que bajó los datos (`cola.yaml` E-04). |
| **1.13** | **30/jul/2026 — ADR-45: vocabulario fijo de "prueba de falsación corrida", cierra `cola.yaml` D-05.** Tres decisiones de mesa del autor: (1) denominador — 27 (perímetro del Hito D) y 49 (reglas del motor) se reportan siempre etiquetados, nunca uno sin decir cuál; (2) un veredicto `D` cuenta como corrida, la letra viaja con el conteo; (3) Hito D (reglas), Hito C (generadores) y el ejercicio suelto de `glosario §6/§10` sobre G1a (27/jul, sin bloque archivado) se reportan como tres poblaciones separadas, nunca sumadas ni una etiquetada como otra. Corrige `§5` (fila "48 de 49" mezclaba denominadores y etiquetaba el ejercicio de glosario como "Es el Hito D"). `I-07` queda abierta: sigue siendo patrón de proceso sin test. |
| **1.12** | **30/jul/2026 — ADR-44: registro retroactivo de la publicación del repositorio (29/jul), sin ADR previo.** Mismo patrón que ADR-42(1), un piso más arriba: la función del programa entero cambió de privado-descriptivo a público-auditable sin pasar por gobernanza. Fija cuatro requisitos de salida — capa legal verificada en el árbol, re-examen de deuda "asumida a propósito" (referido a `revision-publicacion-2026-07-30.md`), README sin cifra sin test (declarado **PENDIENTE**, es F6) y regla hacia adelante contra decisiones que asuman lector interno. *(Sesión de canon F2/F4; T-README y A1-A5 quedaron fuera de perímetro por regla de sesión. Nota: las filas 1.10 y 1.11 no existen en esta tabla — mismo hueco de autorreferencia que `censo-integridad-v1_0.md` C5-03 ya señaló para 1.9; no se reconstruyen aquí, es scope ajeno a este ADR.)* |
| **1.9** | **29/jul/2026 — Corrección de RÓTULO del perímetro del Hito D (ADR-37, §4).** El registro de decisión decía "20 [FUERTE] + 5 [MEDIA-FUERTE] + 2 compuestas", tratando a `R1.4` ([FUERTE como correlación]) como una segunda regla partida. Solo `R4.3` ([FUERTE / MEDIA]) es compuesta; `R1.4` es un tier distinto, con un solo falsador. El perímetro no cambia: siguen 27. Propagado a `modelo §7` (cambio 34) y `estado §4·S2`/`§7`. *(Fila añadida 29/jul/2026 en la sesión de correcciones — faltaba; `censo-integridad-v1_0.md` C5-03.)* |
| **1.8** | **28/jul/2026 — ADR-36 adenda (c):** las series numeradas se versionan completas, con prefijo común, y el **orden de lectura pasa del nombre al cuerpo**. Los tres docs de MILPA → `milpa-whitepaper` v0.1 · `milpa-spec` v0.2 · `milpa-plan` v0.1. |
| **1.7** | **28/jul/2026 — ADR-37: se cierra el S2 más antiguo del programa.** La spec del gate de Fase 1 pasa de una condición a **tres** (reproducción · prueba de mecanismo · anti-confusión). Desbloquea `R3.4`. Colateral: `civico.voto.clientelar` degradada de `FUERTE` a `MEDIA` — su `p: 0.63` era cifra de **laboratorio** compilada como campo; se crea el campo `procedencia_p`. |
| **1.6** | **28/jul/2026 — ADR-36: nomenclatura versionada y eliminación de la ficha.** Todo archivo canónico pasa a `<nombre-estable>-v<MAYOR>.<MENOR>.md` con bloque de cabecera obligatorio; las referencias internas citan **nombre estable**. La ficha canónica **se elimina** y sus tres bloques con valor propio se absorben en `modelo` §0.1, §0.2 y §9. Un cambio típico pasa de tocar 6 archivos a **1 o 2**. |
| **1.5** | ADR-35: ampliación de alcance a crédito del lado del decisor. Motor a **49 reglas**. |
| **1.4** | ADR-34: tabla de propagación obligatoria en forenses, tras el barrido (6 de 22 fugas). |
| **1.3** | ADR-33: prohibida la diagonal en el `ENTONCES`. |
| **1.2** | **28/jul/2026 — Ronda 6, saldo de deuda documental.** ADR-31 y ADR-32. Los tres casos de retropropagación **cerrados y verificados en la fuente** (dos figuraban como hechos sin estarlo). Glosario → **v5.1**; modelo → **v2.1**; ficha **regenerada con cobertura 43/43**; los tres YAML → **v0.2.0**. Conteo de números publicado: **107 → 144**. Perímetro del Hito D fijado: **20 reglas FUERTE, no 19**. `CHECKPOINT-v2` + `mapa-y-roadmap` + `inventario-corpus` **fusionados en `ESTADO-PROGRAMA.md`**; `ADR-30.md` borrado. Reports: **30 → 31**. Conflicto **conf.07** abierto y resuelto. |
| **1.1** | **ADR-26 a ADR-30 incorporados** (los archivos sueltos se borran). El **glosario entra a la cadena de dependencia** — su omisión permitió que el modelo creara reglas sin tier. **Retropropagación** añadida al protocolo (§3.1). **Severidad S5** y **casillero de pendientes irresueltos** (§5.1). Registro de artefactos actualizado: modelo v2, glosario v5, CHECKPOINT v2, forenses como canónicos, y los siete artefactos borrados el 27/jul. **Regla de borrado** (consolidar primero). ADR-25 marcado con corrección pendiente. Deuda ampliada con cuatro generadores sin falsar, 41 reglas sin prueba, ocho refutaciones sin objeto y PD-01. |
