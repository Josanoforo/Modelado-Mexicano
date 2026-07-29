# Curaduría del proyecto
### Qué se queda, qué se va, qué se consolida · 27 de julio de 2026

*Estado verificado por lectura: **60 archivos** — 36 de contenido, 24 de gobierno/meta.*

---

## El principio que ordena la decisión

Todo lo que sigue se decide con una regla, y conviene enunciarla antes porque el proyecto ya la violó tres veces:

> **El proyecto es el conjunto de trabajo, no el archivo histórico.**
> Cada archivo aquí es algo que una búsqueda semántica puede devolver a mitad de una tarea. Un artefacto superado no es historia inofensiva: es una mina. La trazabilidad vive en el ADR que registró el cambio y en el historial de conversaciones — **no en un archivo que sigue siendo recuperable como si fuera vigente**.

El caso que lo prueba: `estado-proyecto` lleva tres sesiones marcado como superado, con tiers distorsionados, y sigue aquí. Y el report de consumidor sostuvo `Fuerte` sobre Hofstede durante dos días **mientras el glosario decía `Media`** — porque nadie borró ni corrigió la versión vieja.

---

## 1 · SE VA (4 archivos)

| Archivo | Por qué |
|---|---|
| **`estado-proyecto-psicologia-mexicano.md`** | **SUPERADO desde hace tres sesiones.** `gobernanza §2` lo marca *"no usar"*; la verificación del red team lo identifica como *"el artefacto sobre-confiado de verdad"* —el que convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón—. Es contaminación activa: cualquier búsqueda puede devolver sus tiers muertos. **Borrar.** |
| **`glosario-corregido-v2.md`** | Superado por v3, que a su vez fue superado dos veces. Tres generaciones atrás. |
| **`glosario-v3.md`** | Superado por v4 y v5. ⚠️ **Solo tras consolidar v5** (ver §3) |
| **`glosario-v4.md`** | Superado por v5. ⚠️ **Solo tras consolidar v5** (ver §3) |

---

## 2 · SE QUEDA

### 2.1 Canónico de gobierno (6)

| Archivo | Estatus | Acción pendiente |
|---|---|---|
| `instrucciones-proyecto-v2.md` | **CANÓNICO raíz** | — |
| `gobernanza-programa.md` | **CANÓNICO**, v1.0 | Incorporar ADR-26 a 29 → pasa a v1.1 |
| `modelo-decisiones-mexicano.md` | **CANÓNICO OPERATIVO** | Corregir "ocho perfiles"→seis (§3, disparador 7); reformular alcance de la regla de utilidad (§3.3 vs §7) |
| `ficha-canonica-modelo.md` | **DERIVADO vigente** | Regenerar: restaurar los dos caveats perdidos + propagar procedencia (a)/(b)/(c) |
| `CHECKPOINT-programa-psicologia-mexicano.md` | **Estado**, parcialmente obsoleto | Su §11 pide 48 archivos; su narrativa de pérdida ya no aplica. Actualizar o marcar |
| `glosario-v5.md` | **CANÓNICO vigente** | Consolidar (§3) |

### 2.2 ADR sin incorporar (2) — *transitorios*

`ADR-26-27-28.md` · `ADR-29.md` — **se quedan hasta que los apruebes**. Al incorporarse a `gobernanza §4`, **se van**: mantener el ADR suelto y su copia en gobernanza es duplicar la fuente de verdad, que es el defecto que este proyecto combate.

⚠️ **ADR-29 sigue sin aprobar**, y es el que ordena propagar hacia atrás. Los tres parches de hoy son el cuarto, quinto y sexto caso del defecto que ese ADR existe para cerrar.

### 2.3 Evidencia primaria (36) — **todo se queda**

- **30 reports temáticos** — incluidos los dos fuera del modelo por diseño (`El_México_Rural_e_Indígena`, ADR-10; `Mexican_Population_Genomics`, firewalleado como biología y mercado)
- **1 prueba del canal genético** (`Genetica_y_Conducta`) — artefacto de ADR-19
- **4 verticales forenses** — V1 consumo · V2 clientelismo · V3 crédito auditado · V4 sobreendeudamiento
- **1 registro de apuestas**

**Ninguno se descarta.** Incluso los que fallaron —V1 no pudo leer los documentos del proyecto— son evidencia de qué se intentó y con qué resultado. ADR-29.b es explícito: los forenses son evidencia primaria del mismo rango que los reports.

**Ya reemplazados hoy** ✅ (verificado, los parches llegaron):
- `Psicología_del_Consumidor` — tres puntos de Hofstede
- `La_arquitectura_invisible` — honor retirado, HCHS/SOL marcado, Díaz-Guerrero fechado

### 2.4 Auditorías y forenses de método (5)

| Archivo | Por qué se queda |
|---|---|
| `meta-auditoria-comunicacion.md` | Parche canónico. ⚠️ **Estatus cambia hoy:** su orden de retirar "honor" ya se ejecutó en la fuente. Sigue vigente por lo demás |
| `verificacion-red-team-vs-corpus.md` | Registro de qué ataques sobrevivieron. Su prescripción de leer los cuatro pivotes **ya se ejecutó** |
| `red-team-cuatro-verticales.md` | Origen del hallazgo del modelo fantasma |
| `lectura-cuatro-pivotes.md` | Tiers corregidos palabra por palabra. **Ya en el proyecto** ✅ |
| `Apuestas_Conductuales...` | Contado arriba como evidencia primaria |

### 2.5 Simulador (3 + 3 yaml)

`01-whitepaper` · `02-especificacion` · `03-plan` — se quedan. La spec tiene un error conocido en §4.2 (llama "validada" a una HIPÓTESIS) que hay que corregir.

`refutations.yaml` · `procedencia.yaml` · `tramite.yaml` — se quedan. Son 3 de ~15 archivos de MILPA Fase 0; el resto sigue ausente.

### 2.6 Plantillas (1)

`prompts-verticales-validacion.md` — se queda, **con dos parches obligatorios antes de volver a usarse**:
1. **Fuga de infalsabilidad en el confundidor (c).** Las creencias sobre si la contraparte cumple **son confianza**, fundadas o no.
2. **Tabla de descartes obligatoria.** Su ausencia causó PD-01.
3. *(Añadido por el Hito 2)* **Las reglas a estresar se citan textualmente del motor §3**, con tier y alcance — o se declara que se propone una regla nueva. Sin esto, 6 de 13 reglas volverán a ser fantasmas.

---

## 3 · SE CONSOLIDA — el problema que bloquea el borrado

**Los cuatro glosarios son deltas encadenados, no versiones completas.**

```
v2  →  v3 (casi completo)  →  v4 ("Sin cambios respecto al v3…")  →  v5 ("Sin cambios respecto a v3/v4"; "v4 §5 y §6")
```

`v5 §6` remite a v3 y v4 para interacción, emoción moral, firewall genético y los 107 números. **Borrar v3 o v4 hoy rompe el glosario vigente.** No es preferencia: es dependencia verificada por lectura.

**Dos salidas:**

| Opción | Consecuencia |
|---|---|
| **(a) Consolidar v5 en documento autocontenido**, y luego borrar v2, v3, v4 | Un solo glosario. Recomendada |
| (b) Conservar la cadena | Cuatro glosarios en rango de búsqueda semántica — **es `estado-proyecto` multiplicado por cuatro**, y con tiers que se contradicen entre versiones |

**Recomiendo (a).** El corpus ya aprendió esta lección una vez, y le costó el eslabón débil. La consolidación es mecánica: traer a v5 las secciones que hoy están por referencia.

---

## 4 · SE AÑADE (3 archivos que faltan del trabajo de esta sesión)

| Archivo | Estado |
|---|---|
| `hito2-modelo-fantasma.md` | **Listo para subir.** Forense de método: 6 fantasma / 4 diverge / 3 fiel |
| `mapa-y-roadmap.md` | ⚠️ **Actualizar antes de subir.** El Hito 2 ya se ejecutó y el trabajo de glosario también; subirlo tal cual mete un roadmap obsoleto al proyecto |
| `inventario-corpus.md` | ⚠️ **Corregir antes de subir.** Omite `glosario-v4.md`. Subirlo así propaga una lista de archivos equivocada — el defecto exacto que el inventario existe para evitar |

**No subir** `auditoria-glosario-v4.md`: sus hallazgos están incorporados en v5 y en `lectura-cuatro-pivotes`. Es andamiaje, no artefacto.

---

## 5 · Resultado neto

| | Antes | Después |
|---|---|---|
| Archivos | 60 | **59** |
| Glosarios | 4 | **1** |
| Artefactos superados en rango de búsqueda | 4 | **0** |
| Forenses de método archivados | 1 | **3** |

Baja de uno en total, pero **el cambio real es de calidad**: desaparecen los cuatro artefactos que pueden devolver información contradictoria a mitad de una tarea.

---

## 6 · Orden de ejecución

```
1. [ ] Borrar estado-proyecto-psicologia-mexicano.md          ← inmediato, sin dependencias
2. [ ] Consolidar glosario-v5 (autocontenido)
3. [ ] Borrar glosario-corregido-v2, v3, v4                   ← solo después del paso 2
4. [ ] Corregir inventario-corpus (añadir v4) y subirlo
5. [ ] Actualizar mapa-y-roadmap y subirlo
6. [ ] Subir hito2-modelo-fantasma
7. [ ] Parchar prompts-verticales-validacion (3 correcciones)
8. [ ] Aprobar ADR-26/27/28/29 → incorporar a gobernanza → borrar los ADR sueltos
9. [ ] Correcciones puntuales: modelo §3 "ocho→seis" · spec §4.2 · refutations meta 41→49 · CHECKPOINT §11
```

Los pasos 1 y 2-3 son los que importan. El resto es higiene.

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** No aplica: es una decisión de archivo.

**¿Qué sobregeneraliza?** La regla del §0 —"un artefacto superado es una mina"— es correcta para búsqueda semántica, pero no para todo. Si alguna vez hay que auditar **cómo** derivó un tier, la cadena de glosarios es justamente lo que se necesita. Por eso la salida no es borrar sin más: es **consolidar primero**, que preserva el contenido y elimina la ambigüedad.

**¿Qué está sesgado por marcos externos?** Nada aquí.

**¿Qué cambiaría con otro foco?** Si el objetivo fuera auditoría metodológica en vez de operación, la decisión se invierte: conservar las cuatro versiones y documentar la deriva entre ellas sería el entregable. La curaduría depende de para qué es el proyecto, y aquí es **operativo**.

**¿Qué parece problema de archivo y es otra cosa?** Que haya cuatro glosarios no es desorden: es el síntoma de que **cada glosario se escribió con un corpus distinto a la vista** —v3 con 34 archivos, v4 con 43 durante la pérdida, v5 con 60—. La proliferación es consecuencia de la inestabilidad del archivo, no de descuido. Si el archivo se estabiliza, deja de pasar.

**¿Dónde hay evidencia débil e intuición fuerte?** En recomendar borrar v2 y v3. Verifiqué que **v5 depende de v3/v4** por referencia explícita, pero no leí v2 completo para confirmar que nada dependa de él. Es el eslabón menos verificado de esta curaduría.

**¿Qué conclusión sería peligrosa mal usada?** Borrar los cuatro glosarios **antes** de consolidar. Sería la pérdida más grave del programa hasta la fecha: el glosario es el único artefacto donde los tiers se leen de los reports, y v5 hoy no se sostiene solo. El orden del §6 no es sugerencia — el paso 3 depende del paso 2.
