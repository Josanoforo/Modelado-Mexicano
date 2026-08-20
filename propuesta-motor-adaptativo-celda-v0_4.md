# El motor adaptativo por celda: seleccionar el estimador, no imponerlo
### Propuesta sin sello · v0.4 · 12/ago/2026

> ⚠️ **Superseded 20/ago/2026 en §3 por `propuesta-motor-adaptativo-celda-v0_5.md`** (`ACT-PIL-1 · CONTRATO-v0_5`, `ADR-129`): el campo `rol` se abre a `BASELINE_INGENUO`/`ENSAMBLE` (+ `variante_corredor`), el campo `resultado` se parte en `resultado` (prosa) + `estado_decidibilidad` (enum validado), nace `margen_material` y `vocabulario_version` sube a `0.5`. Este archivo no se edita — historia de la propuesta.

> | | |
> |---|---|
> | **ARCHIVO** | `propuesta-motor-adaptativo-celda-v0_4.md` |
> | **REEMPLAZA A** | `propuesta-motor-adaptativo-celda-v0_3.md` — se conserva, no se borra. v0.1-v0.3 son historia de esta propuesta; no se editan (v0.3 gana un banner de una línea que apunta aquí) |
> | **CLASE** | Corrección de vocabulario, ordenada por `ADR-71(d)`: "el enum `fuerza` del contrato celda-D se corrige antes de E0". Aplica sobre el contrato ya adoptado por ADR-68 — no reabre ninguna otra decisión de v0.3, no reabre M1, no ejecuta celda alguna |
> | **ORIGEN** | ACTO V (12/ago/2026), sobre el hallazgo de raíz que las dos celdas-D semilla ya habían escrito: 2 de 2 escribieron fuera del enum de `fuerza` (`NO_DETERMINADO`, `MEDIDO·PARCIAL(x)`), con reserva escrita en su propio YAML, porque el enum describe el coeficiente que la condicional alimenta y ninguna de las dos celdas está describiendo un coeficiente |
> | **QUÉ CAMBIA DE v0.3** | §3: el campo `fuerza` se parte en dos — `fuerza_coeficiente` (mismo enum cerrado de siempre, ahora con su objeto correcto) y `procedencia_condicional` (vocabulario nuevo, extensible, para lo que la celda realmente compara). Nada más cambia |
> | **QUÉ NO DECIDE** | Sin cambio respecto a v0.3: ningún valor de ningún parámetro; la granularidad D de ningún eje; M1 sigue abierta. Tampoco decide el contenido final de `procedencia_condicional` más allá de su conjunto inicial de 4 valores — el vocabulario tiene su propio falsador y caducidad (§3, abajo), no se cierra por decreto en este acto |

---

## 0 · La tesis, en cuatro eslabones — sin cambio respecto a v0.3

Ver v0.3 §0. Esta versión no toca la tesis, ni la celda-D como unidad, ni ninguna de las cinco colisiones de vocabulario resueltas en v0.2/v0.3 §1.

## 1 · Cinco colisiones de vocabulario resueltas — sin cambio respecto a v0.3

Ver v0.3 §1.

## 2 · La celda-D — sin cambio respecto a v0.3

Ver v0.3 §2.

---

## 3 · El contrato de una celda-D — `fuerza` se parte en dos, porque son dos objetos

**El defecto que esta versión corrige, verificado antes de escribir una línea de vocabulario nuevo:** `fuerza: ASIGNADO | AJUSTADO | IDENTIFICADO` describe el **coeficiente de `milpa/procedencia.yaml`** que una condicional alimenta — no la condicional misma. Las dos celdas-D semilla que ya existen escribieron fuera del enum, cada una con su propia reserva razonada en el YAML: `familismo_obligacion.actitud` usó `NO_DETERMINADO` ("los tres valores del enum caracterizan un VALOR existente en `milpa/procedencia.yaml`, y aquí no hay valor que caracterizar"); `radio_confianza` usó `MEDIDO·PARCIAL(x)` ("ninguno de los tres nombra con precisión una medición condicional directa de microdato"). Diagnóstico de raíz (`radio_confianza`, en su propio archivo): el coeficiente que ese valor alimenta *sí* es `ASIGNADO` — "pero es un objeto distinto (el peso que el generador le da a la condicional), no la condicional misma que esta celda compara." Un campo intentando cargar dos preguntas independientes, con mecanismo para una sola.

```yaml
celda_d:
  id: <string>
  estimando: <string>
  tipo_adjudicacion: COMPARACION | FALSACION | CALIBRACION_CONJUNTA
  dominio: <FIN|MIG|TEC|CAP|CUL|SAL|SEG|TRA|EST|TIE>
  poblacion_objetivo: <string>
  unidad_objetivo: persona | hogar | establecimiento | agregado_geografico
  universo_candidatos: <qué se barrió, con qué mecanismo, en qué fecha>
  candidatos:
    - rol: BASELINE | CHALLENGER | COMPLEMENTO
      fuentes: []
      edicion_periodo: <string>
      universo_instrumento: <poblacion y periodo que el instrumento cubre>
      diseno_datos: panel | pseudo_panel | transversal | registro_administrativo |
                    experimento_natural | auditoria_campo | enlace_ecologico
      estrategia: pseudo_panel | momentos | composicion | transversal_con_seleccion
      regla_composicion: <declarada en fecha_declaracion> | NO-APLICA
      production_spec_refs: []
      resultado: GANO | PERDIO:<margen> | NO-EJECUTADO | INEJECUTABLE | NO-APLICA
  criterio_adjudicacion: {texto: <string>, escala: <string>}
  momentos_holdout_refs: []
  champion_actual: <rol.fuente o NINGUNO>
  output_nativo: {tipo: <7 tipos, v0.1 §3.6>, escala: <string>, valor_ref: <archivo dueño>}
  incertidumbre: {tipo: <string>, ref: <string>}
  supuesto_transporte: EXISTE-SATISFACE | ACOTADO-CON-SUPUESTO:<cual> | NO-TRANSPORTABLE:<por que>
  fuerza_coeficiente: ASIGNADO | AJUSTADO | IDENTIFICADO   # NUEVO nombre (v0.4) — describe el
                    # coeficiente de milpa/procedencia.yaml que la condicional alimenta,
                    # NO la condicional. Enum cerrado, sin cambio de vocabulario respecto al
                    # `fuerza` de v0.1-v0.3 — solo cambia su nombre, para que deje de
                    # pretender describir dos objetos distintos.
                    # sin_coeficiente_asociado: true  — declarar así, con razón, si esta
                    # condicional todavía no alimenta ningún coeficiente en milpa/procedencia.yaml
  procedencia_condicional: MEDICION_DIRECTA_MICRODATO | MEDICION_CONDICIONAL_MICRODATO |
                    # PROXY_PARCIAL | SIN_ESTIMACION_TODAVIA                        # NUEVO (v0.4)
                    # Vocabulario EXTENSIBLE, no cerrado — describe lo que la celda realmente
                    # compara. Conjunto inicial derivado de los dos casos reales que ya existían,
                    # de ningún otro lado. Reglas completas abajo.
  vocabulario_version: 0.4        # NUEVO (v0.4) — obligatorio; los conjuntos cerrados/extensibles
                    # de esta versión se citan por número de versión, no por nombre
  calibrado: <bool>
  estado_operativo: LISTO | LEGACY | PENDIENTE | EXCLUIDO
  requiere_decision_mesa: <bool>
  fecha_declaracion: <YYYY-MM-DD>
  commit_declaracion: <sha>
  fecha_adjudicacion: <YYYY-MM-DD>
  commit_adjudicacion: <sha>
  relacion_complemento: <id de la celda-D ligada> | NO-APLICA
```

**Reglas del vocabulario extensible `procedencia_condicional`, escritas aquí porque nacen con él:**

1. **No contiene, ni contendrá, un valor de "otro" / "no especificado" / "no determinado" como miembro.** Un vocabulario extensible con comodín es de facto cerrado y esconde justo la señal de que el vocabulario no cubre el espacio — razón declarada, con su fuente, en `ADR-71(d)`: práctica establecida en HL7 FHIR (binding strength) y adoptada independientemente por openEHR (SPECAM-68).
2. **Un valor fuera del conjunto se admite solo con dos condiciones**, ambas en el propio YAML de la celda: razón escrita **y** el valor más cercano del conjunto inicial citado explícitamente, o bien `sin_equivalente_canonico: true` declarado sin más.
3. **Cada celda declara la versión del vocabulario que usó** (`vocabulario_version: 0.4`, arriba). Los conjuntos — cerrado (`fuerza_coeficiente`) y extensible (`procedencia_condicional`) — se citan por versión, no por nombre suelto.
4. **Falsador y caducidad.** Si en los **tres meses** posteriores a esta versión ninguna celda-D nueva necesita un valor de `procedencia_condicional` fuera de los cuatro iniciales, el vocabulario se declara suficiente y el campo pasa a **cerrado** (mismo estatus que `fuerza_coeficiente`). Si en ese plazo **tres celdas-D nuevas** necesitan valores **distintos** fuera del conjunto, el vocabulario está mal cortado y **se rediseña** — no se parcha añadiendo miembros sueltos uno a uno.

**Deliberadamente sin instrumentar en esta versión, con la razón escrita:** ni la clausura de `fuerza_coeficiente` ni la regla de extensibilidad de `procedencia_condicional` ganan un validador de código en este acto. Regla de instrumentación (v2.3, citada por el propio ACTO V): antes de instrumentar se declara qué defecto **real, ya ocurrido**, la validación atraparía — no uno concebible. Bajo este diseño, las dos celdas existentes escriben `ASIGNADO` y un valor del conjunto inicial; no hay, hoy, ninguna instancia real de mal uso que un validador hubiera atrapado. El propio §3 ya trae su falsador (regla 4, arriba): si aparece, se instrumenta entonces.

### 3.1 · `rol: COMPLEMENTO` — un candidato que no compite (H1/H2) — sin cambio respecto a v0.3

Ver v0.3 §3.1.

### 3.2-3.9 · Resto del contrato — sin cambio respecto a v0.3

Ver v0.3 §3.2-3.9. La etiqueta histórica "D6 (fuerza/calibrado)" de ese resumen sigue refiriéndose a la misma categoría de decisión de contrato — solo el nombre del campo cambió, no la decisión.

---

## 4 · Relación con `propuesta-motor-matriz-v0_1.md` — sin cambio respecto a v0.3

Ver v0.3 §4.

## 4-bis · Celdas-D semilla, decididas por mesa el 10/ago — sin cambio respecto a v0.3

Ver v0.3 §4-bis. Los dos registros reales de celda-D (`G5.radio_confianza.encuci_vs_enbiare`, `G5.familismo_obligacion.actitud`) se reescriben con el vocabulario de esta versión en `data/curacion-registro/celdas-d/*.yaml` directamente — no en los bloques de ejemplo de este documento, que no llevan `fuerza`/`fuerza_coeficiente` en su forma abreviada y no necesitan tocarse.

## 5 · Vertical piloto — sin cambio respecto a v0.3

Ver v0.3 §5.

## 6 · Ejemplo trabajado — sin cambio respecto a v0.3

Ver v0.3 §6.

## 7 · Lo que esta propuesta no resuelve

Todo lo que v0.3 §7 ya declaraba, sin cambio, más: el contenido final de `procedencia_condicional` más allá de los cuatro valores iniciales (tiene su propio falsador, §3); si `fuerza_coeficiente`/`procedencia_condicional` deberían, en algún acto futuro, moverse de vocabulario **por celda** a vocabulario **por generador** de `milpa/procedencia.yaml` — no se vio evidencia de esa necesidad en las dos celdas existentes, y no se decide sin ella.

## 8 · Preguntas para mesa — resueltas, 12/ago/2026

La única pregunta que esta versión responde es la que `ADR-71(d)` ya adjudicó: el enum se corrige partiéndolo en dos, sin cajón de sastre. Las diez preguntas de v0.3 §8 siguen resueltas como estaban; ninguna se reabre aquí.

## 9 · Módulo de auditoría

**1-6** · No aplican, igual que v0.1-v0.3.

**7 · ¿Qué conclusión sería peligrosa simplificada?** Las de v0.3, sin cambio, más una séptima: *"partir `fuerza` en dos campos resuelve el vocabulario de celda-D para siempre"* — no lo hace; resuelve el defecto **verificado** de las dos celdas existentes. `procedencia_condicional` es extensible por diseño porque el programa espera 10-15 celdas más en el piloto y no hay evidencia hoy de qué necesitarán exactamente — la caducidad de tres meses (§3) es la señal que decide si el conjunto inicial bastó o si el corte estuvo mal hecho, no una promesa de que bastó.

**8 · ¿Qué fue derivado y qué no?** Derivado o verificado de primera mano en este acto: los dos valores fuera de enum (`NO_DETERMINADO`, `MEDIDO·PARCIAL(x)`) y sus dos reservas escritas, leídas contra los dos archivos YAML reales; el enum cerrado de `fuerza` (v0.3 §3, sin cambio de vocabulario); que `radio_confianza=0.15` en `milpa/procedencia.yaml` está marcado `magnitud: asignada`; que `familismo_obligacion` (G5) está marcado `ASIGNADO` con `SIN MAGNITUD` en el mismo archivo; que ningún código valida hoy el valor de `fuerza` (`tests/test_celdas_d.py`, verificado leyendo el archivo — valida presencia del campo, no su valor, declarado así en su propio docstring). El conjunto inicial de `procedencia_condicional` (4 valores) se derivó **solo** de los dos casos reales, ninguna otra fuente.

**Contadores movidos por el trabajo que produjo esta versión: 0.** Ninguna celda-D se ejecuta; este acto evita paros falsos en el gate de entorno de futuros actos (E0), no mide nada del programa.

**(v2.4) Cantidades y escalas:** ninguna cantidad estimada nueva se transcribe en esta versión.

---

## Changelog

**v0.3 → v0.4 · 12/ago/2026 (ACTO V, `ADR-71(d)`).**
1. §3: `fuerza` se parte en `fuerza_coeficiente` (mismo enum cerrado `ASIGNADO|AJUSTADO|IDENTIFICADO`, objeto correcto ahora — el coeficiente, no la condicional) y `procedencia_condicional` (vocabulario extensible nuevo, 4 valores iniciales, con regla de "sin cajón de sastre", regla de excepción declarada, y falsador/caducidad a tres meses).
2. §3: campo `vocabulario_version` nuevo, obligatorio.
3. `data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml` y `G5.radio_confianza.encuci_vs_enbiare.yaml` reescritas con el vocabulario nuevo, reservas verbatim conservadas — ver los propios archivos.
4. Ningún otro cambio: M1 sigue abierta, ninguna celda-D corre, ningún contador de canon se mueve.
