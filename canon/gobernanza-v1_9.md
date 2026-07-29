# Gobernanza del programa · Psicología del Mexicano Contemporáneo
### `gobernanza` · **v1.9** · 29 de julio de 2026 · **37 ADR**

> | | |
> |---|---|
> | **ARCHIVO** | `gobernanza-v1.9.md` |
> | **REEMPLAZA A** | `gobernanza-v1.8.md` — **borrar** |
> | **VERIFICAS ASÍ** | ADR-36 tiene **adenda (c)** sobre series numeradas · §2 lista los tres `milpa-*` · §4 (registro del perímetro del Hito D) trae la corrección de RÓTULO fechada 29/jul — el perímetro sigue en **27** |
> | **NOMBRE ESTABLE** | **`gobernanza`** — cítalo así, **nunca por nombre de archivo** |



*Documento vivo. Registra **qué se decidió, por qué, y qué se rompe si cambia**.
No repite el contenido del corpus: lo gobierna.*

**Versión de este documento:** 1.1 · **Estado del programa:** Ronda 4 cerrada y **auditada**; modelo v2 y glosario v5 consolidados; Fase 1 del simulador **pospuesta**.

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
   30 reports temáticos         ← CANÓNICO (evidencia primaria)
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
| `glosario-v5.5.md` | **CANÓNICO** | **v5.5**, autocontenido | reports (mapas de evidencia) |
| `integrador-psicologia-mexicano.md` | DERIVADO | 30 reports | reports + glosario |
| `meta-auditoria-comunicacion.md` | CANÓNICO (parche) | 1.0 | — |
| `modelo-decision-v3.0.md` | **CANÓNICO OPERATIVO** | **v3.0, autocontenido** *(absorbe la ficha)* | integrador + glosario + validaciones |
| ~~`ficha-canonica-modelo.md`~~ | **ELIMINADA 28/jul** *(ADR-36.b)* | — | absorbida en `modelo` §0.1, §0.2 y §9 |
| **5 validaciones forenses** | **CANÓNICO** *(ADR-29.b)* | Ronda 4 | — |
| ~~`CHECKPOINT-v2.md`~~ · ~~`mapa-y-roadmap.md`~~ · ~~`inventario-corpus.md`~~ | **BORRADOS 28/jul** | — | **fusionados en `ESTADO-PROGRAMA.md`** |
| `estado-programa-v1.1.md` | **CANÓNICO (estado)** | v1.1, 28/jul | única fuente de estado |
| `ADR-30.md` | **BORRADO 28/jul** | — | incorporado a §4; además contenía la versión **superada** (retiraba `familismo` de G3, corregido en mesa) |
| `milpa/` (Fase 0) | DERIVADO | 0.1.0 | ⚠️ **ausente salvo 3 archivos** |
| `masterclass-mexico.html` | DERIVADO | foto Ronda 4 | ⚠️ **ausente** |
| **`milpa-whitepaper`** | CANÓNICO (programa) | v0.1 | — |
| **`milpa-spec`** | CANÓNICO (programa) | **v0.2** | — |
| **`milpa-plan`** | CANÓNICO (programa) | v0.1 | — |
| `modelo-decisiones-mexicano.md` v1 | **BORRADO** 27/jul | — | superado por v2 |
| `glosario` v2 / v3 / v4 | **BORRADOS** 27/jul | — | consolidados en v5 |
| `estado-proyecto-...md` | **BORRADO** 27/jul | — | superado |

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
| **48 de 49 reglas sin prueba de falsación** ⭐ | Abierta | Una corrida (veredicto B). Es el Hito D. **Perímetro DECIDIDO: 27 reglas.** |
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
| **1.8** | **28/jul/2026 — ADR-36 adenda (c):** las series numeradas se versionan completas, con prefijo común, y el **orden de lectura pasa del nombre al cuerpo**. Los tres docs de MILPA → `milpa-whitepaper` v0.1 · `milpa-spec` v0.2 · `milpa-plan` v0.1. |
| **1.7** | **28/jul/2026 — ADR-37: se cierra el S2 más antiguo del programa.** La spec del gate de Fase 1 pasa de una condición a **tres** (reproducción · prueba de mecanismo · anti-confusión). Desbloquea `R3.4`. Colateral: `civico.voto.clientelar` degradada de `FUERTE` a `MEDIA` — su `p: 0.63` era cifra de **laboratorio** compilada como campo; se crea el campo `procedencia_p`. |
| **1.6** | **28/jul/2026 — ADR-36: nomenclatura versionada y eliminación de la ficha.** Todo archivo canónico pasa a `<nombre-estable>-v<MAYOR>.<MENOR>.md` con bloque de cabecera obligatorio; las referencias internas citan **nombre estable**. La ficha canónica **se elimina** y sus tres bloques con valor propio se absorben en `modelo` §0.1, §0.2 y §9. Un cambio típico pasa de tocar 6 archivos a **1 o 2**. |
| **1.5** | ADR-35: ampliación de alcance a crédito del lado del decisor. Motor a **49 reglas**. |
| **1.4** | ADR-34: tabla de propagación obligatoria en forenses, tras el barrido (6 de 22 fugas). |
| **1.3** | ADR-33: prohibida la diagonal en el `ENTONCES`. |
| **1.2** | **28/jul/2026 — Ronda 6, saldo de deuda documental.** ADR-31 y ADR-32. Los tres casos de retropropagación **cerrados y verificados en la fuente** (dos figuraban como hechos sin estarlo). Glosario → **v5.1**; modelo → **v2.1**; ficha **regenerada con cobertura 43/43**; los tres YAML → **v0.2.0**. Conteo de números publicado: **107 → 144**. Perímetro del Hito D fijado: **20 reglas FUERTE, no 19**. `CHECKPOINT-v2` + `mapa-y-roadmap` + `inventario-corpus` **fusionados en `ESTADO-PROGRAMA.md`**; `ADR-30.md` borrado. Reports: **30 → 31**. Conflicto **conf.07** abierto y resuelto. |
| **1.1** | **ADR-26 a ADR-30 incorporados** (los archivos sueltos se borran). El **glosario entra a la cadena de dependencia** — su omisión permitió que el modelo creara reglas sin tier. **Retropropagación** añadida al protocolo (§3.1). **Severidad S5** y **casillero de pendientes irresueltos** (§5.1). Registro de artefactos actualizado: modelo v2, glosario v5, CHECKPOINT v2, forenses como canónicos, y los siete artefactos borrados el 27/jul. **Regla de borrado** (consolidar primero). ADR-25 marcado con corrección pendiente. Deuda ampliada con cuatro generadores sin falsar, 41 reglas sin prueba, ocho refutaciones sin objeto y PD-01. |
