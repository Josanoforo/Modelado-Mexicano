# Pre-registro de la corrida del duelo `ADV1-M2` — hashes antes de `R`, elicitación congelada, `L-solo` como comparación principal

**Acto:** `PREREG-CORRIDA` (nube, `cloud_default`). Redactado contra `SHA` `9c25f28`, 26/ago/2026. No UBUNTU, no doble. CONTADOR: cero por diseño — este acto no corre ninguna `L`, no computa ningún `R` ni CV, no toca el sorteo, el congelado ni los corredores (solo los hashea), no fija la banda por mesa.

**Orden sagrado del diseño, repetido aquí porque gobierna todo lo que sigue:** hashes → L → R → scoring. Jamás `R` antes de los hashes. Las sesiones `L` jamás ven `R`.

---

## F0 · Compuertas

**F0.1 — RANURA 1 (cuál-`L`), candado `FP-63`.**

> **FIRMO `comparacion_principal_id = L-solo`. `L+corpus` corre como auxiliar no-gating.**

Precargada por decisión de mesa del 25/ago/2026, verbatim:

> «si el motor le gana al modelo pues sí podría ser mérito del corpus y si es así está bien, es lo que venimos trabajando, ¿o me quieres decir que Claude tiene acceso a esta misma data de forma centralizada?»

Respuesta de dirección, para el registro: no — el corpus curado no está centralizado en ningún modelo; lo único que un Claude pelado puede traer son fragmentos de tabulados públicos en su entrenamiento, y ese riesgo ya lo acota la cuota de publicadas del sorteo (2 de 15, ver `sorteo-resultados-v1_0.md`). Consecuencia operativa: si `L-solo` (sin corpus adjunto) queda cerca de `R`, la explicación "el modelo ya tenía la data centralizada" no aplica — lo que puede aplicar es memorización de tabulados públicos ya acotada por esa cuota del 20% (dura, no al límite: 2 ≤ ⌊0.20·15⌋ = 3). `L+corpus` se reporta siempre (universo auxiliar propio, `escala-cinco-casillas-piloto-v2_0.md` nota post-`PR #330`), pero no gatea ninguna lectura de las cinco casillas de `ADV1-M5`; el universo principal que el ejecutable de `scoring-adv1-m3.py` materializa es el pareo de `L-solo` con `M`.

Con esta línea, F0.1 queda satisfecha — el `PARO` que el encargo condiciona a su ausencia no aplica.

**F0.2 — RANURA 2 (D-iii, quién corre la tubería `L`).**

> **DESIGNO para las corridas `L`: sesiones limpias fuera del proyecto, mismo patrón que las adversariales.**

Esto adopta literalmente lo que `pipeline-L-adv1-m2.py` ya declara en su docstring (`ejecutor: str = "sesión limpia fuera del proyecto (D-iii)"`, línea 67, y el párrafo de cabecera líneas 10-16): ninguna sesión que haya leído este pre-registro, el sorteo, el marco congelado o el árbol `forense/prereg-duelo-v2/` corre una celda de `L` — la elicitación es ciega por construcción de sesión, no solo por prompt. Este acto no designa una identidad concreta de sesión (eso es un detalle de ejecución posterior, no de pre-registro); designa el **patrón**: limpia, fuera del proyecto, análoga a las cuatro corridas adversariales ya archivadas en `forense/adv-duelo/`.

**F0.3 — A.8 en fresco, verificado contra `9c25f28`.**

- `find forense/prereg-duelo-v2 -iname "*arbitr*" -o -iname "*-R-*" -o -iname "*resultado-R*"` → vacío. Cero salidas de árbitro en el árbol.
- Ningún archivo `prereg-corrida*.md` preexistía en `forense/prereg-duelo-v2/` antes de este acto.
- `data/raw/` ausente para este acto — OK, no se requiere microdato ni red (`cloud_default`); se salta la sonda de fuente y se registra el negativo con conteo, no con inferencia: **1 sonda saltada, razón declarada** (entorno nube sin red/microdato).

Ambas compuertas de F0 quedan abiertas para que F1-F4 procedan.

---

## F1 · Hashes comprometidos — antes de que `R` exista

**Frase que gobierna esta sección, tal como el encargo la exige:** *estos hashes se comprometen antes de que exista cualquier valor de árbitro; toda corrida posterior se verifica contra ellos.*

`sha256sum` sobre el árbol de trabajo en `9c25f28`, calculado por este acto y no copiado de ningún registro previo:

| Archivo | `sha256` |
|---|---|
| `pipeline-L-adv1-m2.py` | `a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d` |
| `corredor-B-tasa-base.py` | `14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1` |
| `corredor-E-combinacion-LM.py` | `7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d` |
| `scoring-adv1-m3.py` | `beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb` |
| `marco-congelado-piloto-v1_0.tsv` | `3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2` (coincide con `CONGELADO-v1_0.sha256`, ya sellado — no se re-deriva un valor distinto) |
| `sorteo-resultados-v1_0.md` | `140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11` |

Los cuatro corredores son `L` (`pipeline-L-adv1-m2.py`), `B` (`corredor-B-tasa-base.py`), `E` (`corredor-E-combinacion-LM.py`) y el ejecutable de puntaje `scoring-adv1-m3.py` que materializa `M` vía el motor de decisión existente y adjudica las cinco casillas. Ninguno de los cuatro fue modificado por este acto — se hashea el árbol tal como llegó, `git status` limpio antes y después.

**Regla de enmienda, no de silencio:** si cualquiera de estos seis archivos cambia después de este commit y antes de que `R` corra, la fila correspondiente de esta tabla NO se sobreescribe — se agrega una fila nueva fechada, con el hash viejo, el hash nuevo, y la razón del cambio, bajo un encabezado `## F1 · enmienda AAAA-MM-DD`. Un cambio silencioso de hash invalidaría exactamente la garantía que esta sección existe para dar.

---

## F2 · Spec de elicitación ADV1-M2, congelada

Fuente normativa, verbatim (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B, ya citada en la cabecera de `pipeline-L-adv1-m2.py`):

> «ADV1-M2 · Elicitación mecánica y ciega. Un script toma la spec y produce las respuestas sin humano en el bucle: L con modelo+versión+fecha+temperatura fijados, k=5-10 corridas, agregado pre-registrado (mediana+cuantiles; self-consistency en categóricas), TODAS las corridas registradas sin descarte, dispersión reportada; las sesiones L las corre alguien/algo ajeno a las celdas de M (sesiones limpias, como estas adversariales); dos variantes L-solo / L+corpus. M emite punto e intervalo de su incertidumbre de parámetros. Hashes de los cuatro corredores comprometidos antes de que R exista.»

Este acto fija, ANTES de correr una sola celda, los siete puntos que el encargo pide:

**(a) Modelo, versión, fecha, temperatura — sellados aquí.**

| Parámetro | Valor sellado | Razón |
|---|---|---|
| `modelo_id` | `claude-opus-4-6` (el modelo de mayor capacidad general disponible al momento de sellar; no `claude-sonnet-5` ni `claude-fable-5`, que son de la misma familia pero de tier distinto) | Mismo patrón que las cuatro corridas adversariales previas de `forense/adv-duelo/`, que usaron Opus para el rol de lector adversarial de máxima capacidad — `L` ocupa aquí un rol análogo (estimador ciego de máxima capacidad, no el motor barato). Fijado por este acto leyendo ADV1-M2 y el patrón adversarial previo; mesa puede sustituirlo antes de que la sesión ejecutora arranque. |
| `version_declarada` | la cadena de versión textual que el proveedor devuelva en el momento real de la corrida (no se inventa una fecha de build que este acto no puede observar) | ADV1-M2 exige "fijados", no "adivinados" — la sesión ejecutora real registra la cadena verbatim que el proveedor reporta, no una que este acto proponga sin haber corrido nada. |
| `fecha_congelacion` | `2026-08-26` (fecha de este pre-registro) | Es la fecha en que estos parámetros quedan sellados en repo, conforme al campo `fecha_congelacion` de `ParametrosCorredorL` (`pipeline-L-adv1-m2.py:62`). |
| `temperatura` | `1.0` | Ni el extremo determinista (`0.0`, que suprimiría la dispersión entre corridas que ADV1-M2 pide reportar — "dispersión reportada" no tiene sentido con temperatura 0) ni un extremo alto que introduciría ruido no controlado; `1.0` es el default del proveedor y es lo que las corridas adversariales previas usaron para el mismo rol de estimador ciego. |

**(b) `k` fijado dentro de 5-10.**

`k = 8`. Razón: el rango que ADV1-M2 exige es 5-10; `8` es el punto medio, ni el mínimo (que dejaría poco margen para que la mediana+IQR de F2(c) sea informativa con datos categóricos de pocas categorías) ni el máximo (que multiplicaría el costo de 15 celdas × 2 variantes × k corridas sin razón declarada). `ParametrosCorredorL.__post_init__` (`pipeline-L-adv1-m2.py:69-71`) ya rechaza cualquier valor fuera de `[5,10]` — `k=8` pasa esa validación.

**(c) Agregado pre-registrado.**

Ya implementado literalmente en `pipeline-L-adv1-m2.py` §5 (`agregar_continua`, `agregar_categorica`), no reinventado por este acto:

- Numéricas: mediana + cuantiles (`q10`, `q90`, más `q25`/`q75` para el IQR de dispersión).
- Categóricas/ordinales: self-consistency (moda / n) + distribución completa de las k respuestas.

**(d) Cero descartes.**

`correr_celda` (`pipeline-L-adv1-m2.py:189-206`) registra las `k` corridas sin excepción, incluidas negativas, ambiguas o de rechazo de contenido (un rechazo de contenido es una corrida válida, se cuenta, no se relanza — `llamar_modelo` docstring, línea 179-181). La dispersión entre corridas es resultado, no ruido a limpiar.

**(e) Formato de captura por celda × corrida × variante.**

Estructura JSON, una entrada por `(id_celda, variante, índice_corrida)`:

```json
{
  "id_celda": "CIV-08",
  "variante": "L-solo",
  "corridas": [
    {"indice": 1, "texto_crudo": "...", "valor_extraido": null, "fuente_citada": null, "timestamp": "..."},
    "... hasta indice=8 ..."
  ],
  "agregado": {"mediana": null, "q10": null, "q90": null, "dispersion_iqr": null, "n": 8},
  "params": {"modelo_id": "claude-opus-4-6", "version_declarada": "...", "fecha_congelacion": "2026-08-26", "temperatura": 1.0, "k_corridas": 8, "variante": "L-solo"}
}
```

Una entrada así por cada una de las 15 celdas sorteadas (`sorteo-resultados-v1_0.md`) × 2 variantes (`L-solo`, `L+corpus`) = 30 entradas, cada una con 8 corridas = 240 llamadas al modelo en total. Este formato es exactamente lo que `RespuestaCorrida` (dataclass, `pipeline-L-adv1-m2.py:166-172`) y `agregar_continua`/`agregar_categorica` ya producen — no se introduce un formato paralelo.

**(f) Plantilla de prompt por celda.**

Ya congelada en `pipeline-L-adv1-m2.py` §3 (`PLANTILLA_L_SOLO`, `PLANTILLA_L_CORPUS`), derivada solo de los campos de `SpecCelda` (`encuesta`, `ola`, `universo`, `variable`, `estimador`, `escala`) que a su vez vienen de `marco-candidatas-piloto-v1_0.tsv`. Verificado por lectura: ninguna de las dos plantillas menciona árbitro, banda, margen material, ni ninguna fuente de referencia — la sonda canario ("cita la fuente de tu estimación si la tienes") es la única instrucción sobre procedencia, y es genérica, no apunta a ningún artefacto de este árbol.

**(g) `comparacion_principal_id`.**

`comparacion_principal_id = "L-solo"`, para que `scoring-adv1-m3.py` la lea en el campo que `#330` exige sin default (`scoring-adv1-m3.py:85,205-209,291-295`). `L+corpus` corre y se reporta (universo auxiliar propio, `escala-cinco-casillas-piloto-v2_0.md:31`) pero no gatea ninguna de las cinco casillas de `ADV1-M5` — no-gating, tal como RANURA 1 lo fija en F0.1. No se necesita enmienda al doc de interfaz: la nota de `escala-cinco-casillas-piloto-v2_0.md:31` ya reservaba exactamente esta decisión ("sigue sin resolver cuál variante L ocupa el rol adjudicante") y este acto la resuelve sin reescribir esa nota — queda como registro histórico de la reserva, resuelta aquí por la firma de RANURA 1.

---

## F3 · Banda TOST y margen material — derivados, no inventados

`banda-tost-margen-v1_0.md` ya cumplió el mandato de `D-iv` (derivar y traer el número con su justificación, sin auto-sellarse) en un acto anterior (`DUELO-PREREG-V2`, 20/ago/2026). Este acto no recomputa esa derivación — la cita y no la toca, conforme a la instrucción del encargo de "aplicar el método sellado... al set sorteado":

- **Margen material:** `Δ_material = 0.5 · EE(R)` de la celda evaluada — misma constante que `ADV1-M3` ya usa para su condición `INDECIDIBLE`.
- **Banda TOST:** equivalencia si la diferencia entre corredores cae dentro de `[-0.5·EE(R), +0.5·EE(R)]`, dos tests unilaterales estándar (`α=0.05`).
- **Insumo real:** los únicos dos EE empíricos que el corpus adquirido trae (`U2/EV-1`: CV 1.39% y 1.60%, ambos totales poblacionales, banda Alta de CAC-007/01/2018) — no hay artefacto oficial de EE por reactivo para ninguna de las 15 celdas sorteadas (verificado por las cinco vías de `banda-tost-margen-v1_0.md §1`, no re-verificado aquí).
- **Límite explícito, propagado sin editar:** la banda es una **regla de forma** (fracción del EE propio de cada celda, calculado por `ArbitroR.ee` cuando `R` corra), no una constante numérica fija — porque solo hay 2 filas de EE reales y ninguna del mismo tipo de reactivo que el piloto evalúa. Donde una celda no tenga su `EE(R)` calculable aún (porque `R` no ha corrido), la banda de esa celda queda condicionada al árbitro y se dice así — no se rellena con un EE de otra variable ni con un EE de diseño teórico.

**Este acto no sella la constante `0.5`.** Conforme al mismo mandato citado por el encargo — «firmar una constante a ciegas sería el defecto v2.1 de siempre» (`CAREO` D-iv, verbatim) — la fila queda abierta para mesa en `firmas-pendientes.tsv` (`FP-162`, ver F4). Lo que faltaba y que `banda-tost-margen-v1_0.md §4` ya enumeraba (confirmar/rechazar `0.5·EE(R)`, decidir si la banda es siempre fracción del EE o si mesa prefiere una constante absoluta por subclase de reactivo, y registrar la firma) sigue pendiente en esos mismos términos — este acto no los resuelve, solo confirma que la derivación sigue siendo la única disponible y la propaga al set de 15 celdas ya sorteadas.

---

## F4 · Cierre

Ver tablero (`forense/firmas-pendientes.tsv` `FP-161`/`FP-162`), `canon/gobernanza-v1_15.md` `ADR-194`, `canon/estado-programa-v1_10.md`, y la nota `forense/notas/2026-08-26-prereg-corrida-cierre.md`.

## Lo que este acto NO hace

No corre ninguna `L`. No computa ningún `R` ni CV. No toca el sorteo, el congelado ni los corredores (solo los hashea, F1). No fija la banda TOST/margen material por mesa (F3, queda `ABIERTA`). No decide quién corre `L` más allá de propagar la RANURA 2 (F0.2, designa el patrón, no una sesión concreta). Orden sagrado del diseño: hashes → L → R → scoring — jamás `R` antes de los hashes, y las sesiones `L` jamás ven `R`.
