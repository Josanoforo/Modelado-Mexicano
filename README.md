# Psicología del Mexicano Contemporáneo

Corpus de evidencia, modelo de decisión segmentado y aparato de falsación.

> **No es un almacén de documentos.** Es un modelo que hace afirmaciones
> falsables sobre conducta, con la maquinaria para refutarlas. La regla que
> lo gobierna todo: *si escribes un principio y no le das un artefacto que
> falte visiblemente cuando no se cumple, no obliga a nada.*

```bash
python3 tests/check.py            # verificación completa
python3 tests/check.py --strict   # los WARN también fallan
```

---

## Estructura

| Carpeta | Qué contiene | Regla |
|---|---|---|
| `corpus/reports/` | **31 reports temáticos** | Evidencia primaria. **Append-only** |
| `corpus/forense/` | **5 validaciones forenses** | ADR-29.b: mismo rango que los reports. **Append-only** |
| `canon/` | `modelo` · `glosario` · `gobernanza` · `estado` · `integrador` | Versionado, una sola versión viva de cada uno |
| `milpa/` | whitepaper · spec · plan + 3 YAML | Simulador. **Fase 1 ya NO pospuesta — arquitectura objetivo del programa (ADR-50/51), calibrada por AJUSTE** |
| `forense/` | Auditorías, barridos, pre-registros | **Fechados, append-only** |
| `tests/` | La suite | Un ADR sin test aquí es decorativo |

**Orden de lectura en frío:** `canon/estado-programa` → `canon/gobernanza`.

---

## Estado del modelo

**49 reglas · 20 `[FUERTE]`.** <!-- 49: python3 tests/validador_registro_ids.py · 20 [FUERTE]: T12 en tests/check.py (motor_rules()+rule_tier() sobre §3.B) -->

- **13 de 27** corridas del Hito D con veredicto archivado — **7D·2B·2A·2E** <!-- bloque "## Registro de veredictos archivados" de forense/hitoD-preregistro-v2_0.md, parser _VEREDICTO_CANONICO (tests/check.py:684, T18); +R1.3→E, ADR-63 -->
- **Condicionales medidas 9 de 14** <!-- grep -c 'clase: "MEDIDO·PARCIAL' milpa/procedencia.yaml -->
- **Coeficientes en escala del modelo 0 de 15** — tres asociaciones marginales (β̂) existen para tres de los quince, pero ADR-57(a) las rotula asociaciones, no coeficientes: ninguna sobrevive condicionar y no cuentan aquí <!-- modelo §2.2 ("Los quince coeficientes son ASIGNADO. Ninguno es medido"); milpa/procedencia.yaml: asignados_coeficiente / coeficientes_generador_medidos -->
- **[MESA-M4] `4 de 144`** congelado 31/jul/2026, no se recalcula <!-- forense/hallazgos.md, 2026-07-31: "Congelamiento de `4 de 144`" — decisión de mesa, no ADR -->

**Es una síntesis rigurosa de literatura con tiers leídos, no un artefacto
validado.** Un tier derivado de lectura disciplinada es evidencia legítima —
pero la diferencia importa cuando alguien lo use para decidir algo caro.

- **Cero datos primarios propios** — deuda S1 del programa
- Los 42 disparadores de contexto **no** cuentan como números: son booleanos

---

## Primera corrida de la suite · 28/jul/2026

**18 FAIL · 110 WARN.** Y la mitad de los FAIL son hallazgos **nuevos**: una
auditoría manual de los cuatro pivotes, hecha ese mismo día, los subcontó.

| Test | Auditoría manual | La suite | |
|---|---|---|---|
| `T06` valores de **Gini** | 4 | **7** | leyó 36 archivos, no 4 |
| `T06` valores de **confianza interpersonal** | 4 | **12** | |
| `T07` vocabularios de tier ajenos | 4 | **7** (`SÓLIDO`×44 · `MEDIO`×29 · `HIPÓTESIS RAZONABLE`×22) | |
| `T08` reports sin mapa de evidencia | 7 | **7** ✅ | el glosario declaraba 5 |
| `T09` marco **(c)** usado como causa | en 4 pivotes | **8**, en todo el corpus | |
| `T11` afirmación de estado absoluta | 1 | **1** ✅ | atrapada automáticamente |

**`T11` es el que justifica el repo entero.** Un parche del 28/jul declaraba
tres ediciones como *"las únicas que el report requería"* y dejaba **diez**
líneas sin marcar. Se descubrió leyendo a mano, un turno después. La suite lo
tumba en tres segundos, y no lo dejaría entrar por PR.

**`T05` es el segundo.** De los cinco constructos que el motor usa sin entrada
en el glosario, **dos los introdujo quien escribió el check** — porque la lista
de términos se construyó desde los constructos que ya se sabía que faltaban.
Un validador cuyo alcance fija quien introduce las reglas no valida nada.

### Falsos positivos conocidos *(corrida del 30/jul/2026)*

- **`T03` (21)** — en su mayoría, cabeceras que citan `…-v3.2.md` cuando la
  plataforma renombró a `…-v3_2.md`. Real, pero cosmético.
- **`T10` (65)** — la lista de palabras clave de diáspora es laxa y pesca
  líneas sin fuente **(b)**. Hay que afinarla antes de subirla a FAIL.

---

## Deudas abiertas

**S1** · Cero datos primarios propios · **PD-01**: 14 descartes irrecuperables, *no reconstruir*

**S2** · Los **90 parámetros de dispersión** de ADR-28.d no existen en archivo — el check de varianza no puede correr · Los **30 componentes** de `confianza_institucional` por perfil, declarados y sin poblar · **8 refutaciones sin objeto**, incluida `ref.A.02` · El motor **no tiene entidad prestamista** (frontera de ADR-35)

**S3** · 15 coeficientes sin validar · 36 de 49 reglas sin falsación pre-registrada corrida <!-- 49 (validador_registro_ids.py) − 13 (fichas del bloque append-only, T18) = 36; +R1.3→E, ADR-63 --> · 74 números asignados · **3 de 5 forenses sin tabla de descartes**

**S5** · `conf.02` · `conf.05` · **`conf.06`** — resuelto 28/jul: eran **tres reactivos distintos** de la misma escala (62.1% conocidos · 32.1% vecinos · 21.8% la mayoría), leídos como una sola cifra

---

## Cómo se contribuye

Ver **`CONTRIBUTING.md`**. Lo esencial:

1. Corre la suite **antes** de tocar nada — declara de qué estado partes
2. `corpus/` y `forense/` son **append-only**: se corrigen con nota fechada, nunca en silencio
3. Los tiers **se leen**, no se reconstruyen
4. La marca de procedencia **(a)/(b)/(c) viaja** con el constructo
5. **Prohibido el cuantificador absoluto** en afirmaciones de estado
6. Las consultas de búsqueda **se pre-registran**, con una **adversaria** obligatoria
7. Todo principio nuevo **nace con su test**
