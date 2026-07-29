# Especificación técnica · MILPA
### `milpa-spec` · **v0.2** · El modelo, en detalle implementable

> | | |
> |---|---|
> | **ARCHIVO** | `milpa-spec-v0.2.md` |
> | **REEMPLAZA A** | `02-especificacion-tecnica-simulador.md` **y** `spec-tecnica-v0_2.md` — **borrar los dos** |
> | **VERIFICAS ASÍ** | §10 tiene el gate de ADR-25 con **tres condiciones (A, B, C)** · la regla `civico.voto.clientelar` está degradada a `MEDIA` |
> | **NOMBRE ESTABLE** | **`milpa-spec`** — cítalo así, **nunca por nombre de archivo** |

> **Serie MILPA — orden de lectura.** *(El `01/02/03` anterior codificaba el orden en el nombre y no la versión; ADR-36 lo invierte. El orden vive aquí, explícito.)*
>
> **1.** `milpa-whitepaper` — el **porqué** · **2.** `milpa-spec` — el **cómo** · **3.** `milpa-plan` — el **cuándo**

*Requiere haber leído `milpa-whitepaper`.*

> **v0.2 — 28/jul/2026. Dos correcciones, ambas de la misma familia: un número o un criterio que mide otra cosa de la que dice medir.**
> 1. **Se corrige la especificación del gate de ADR-25** — el S2 abierto más antiguo del programa. Ver §10.
> 2. **`civico.voto.clientelar` se degrada de `FUERTE` a `MEDIA`** y se marca como cifra de **laboratorio**. Ver abajo.

---

## 1. Vista general

```
   DATOS                MOTOR                        SALIDA
┌───────────┐    ┌────────────────────────┐    ┌──────────────┐
│ INEGI     │    │  world/   celdas       │    │ mapa espejo  │
│ CONEVAL   │───▶│  pop/     agentes      │───▶│ series       │
│ CNBV      │ETL │  net/     grafo        │tick│ trazas       │
│ SESNSP    │    │  engine/  reglas       │    │ bandas IC    │
│ CEEY, INE │    │  loop/    feedback     │    │ mapa conf.   │
└───────────┘    └────────────────────────┘    └──────────────┘
                          ▲
                  rules/*.yaml  ← compilado desde la FICHA CANÓNICA
```

Principio rector: **las reglas son datos, no código.** El motor es genérico; el conocimiento del corpus vive en YAML versionado, auditable y con tier + fuente por regla. Cambiar el modelo no debe requerir recompilar el motor.

---

## 2. Capa de mundo (`world/`)

### 2.1 Unidad espacial

- **Base:** municipio (≈2,470 unidades). Es el nivel donde existen datos administrativos (SESNSP, CONEVAL, censo).
- **Detalle urbano:** AGEB para zonas metropolitanas (permite modelar segregación intra-urbana, que es donde vive la mayor parte de la varianza de clase).
- **Máscara de exclusión:** municipios con sistema normativo indígena (p. ej. los 417 de usos y costumbres en Oaxaca) y localidades con alta densidad de lengua indígena → `scope: OUT_OF_MODEL`. No se simulan; se dibujan en gris.

### 2.2 Esquema de celda

```yaml
celda:
  id: "09014"                    # INEGI
  nombre: "Benito Juárez, CDMX"
  scope: IN_MODEL | OUT_OF_MODEL
  geom: <polígono>
  poblacion: 434153

  # --- capas estructurales (activan generadores) ---
  G1_confianza:
    confianza_institucional: {v: 0.34, ic: [0.28,0.40], src: ENCIG2025, sae: true}
    calidad_tramite: {v: 0.61, ...}          # discrecionalidad / digitalización
    impunidad: {v: 0.92, ...}
  G2_desigualdad:
    gini: {v: 0.45, ...}
    pobreza_multidim: {v: 0.08, src: CONEVAL2022}
    movilidad_ascendente: {v: 0.42, src: CEEY}
    discriminacion_tono_piel: {v: 0.31, src: CEEY, nota: "capa de trato recibido, NO biológica"}
  G3_informalidad:
    tasa_informalidad: {v: 0.31, src: ENOE, sae: true}
    cobertura_imss: {v: 0.66, ...}
    volatilidad_ingreso: {v: 0.22, ...}
  G4_violencia:
    homicidio_100k: {v: 8.1, src: SESNSP}
    extorsion_100k: {v: 41.0, ...}
    percepcion_inseguridad: {v: 0.44, src: ENSU}
    cifra_negra: {v: 0.93, src: ENVIPE, nivel_real: estatal}
  G5_familismo:
    tam_hogar: {v: 2.9}
    corresidencia_3gen: {v: 0.11}
    remesas_pc: {v: 120, src: Banxico}
    cobertura_cuidados: {v: 0.19}
  G6_jerarquia:
    calidad_gobierno_local: {v: 0.58}
    empleador_dominante: formal_grande | familiar | informal | agricola

  # --- infraestructura de acceso ---
  acceso:
    corresponsales_10k: 14.2        # OXXO, farmacias, etc. (CNBV)
    sucursales_cajeros_10k: 9.8
    internet_hogar: 0.86            # ENDUTIH
    unidades_salud_10k: 3.1
    farmacia_consultorio_10k: 5.4

  # --- estado dinámico (actualizado por el loop) ---
  estado:
    mora_agregada: 0.11
    confianza_local: 0.34
    adopcion_producto: {}
    participacion_ultima: 0.59
```

**Regla de honestidad de datos:** todo valor lleva `{v, ic, src, sae}`. Si vino de SAE (estimación en área pequeña desde un dato estatal o urbano), `sae: true` y el intervalo de confianza es ancho. El **mapa de confianza** de la interfaz se calcula directamente de estos metadatos — no es una capa aparte que alguien tenga que mantener a mano.

---

## 3. Capa de población (`pop/`)

### 3.1 Síntesis

Generación por **IPF (iterative proportional fitting)** contra las marginales censales de cada municipio: edad × sexo × escolaridad × ocupación × tamaño de hogar. Sobre esa base se asigna:

1. **Perfil (1–6)** — probabilísticamente, condicionado por la celda. Ejemplo de mapeo: alta informalidad + bajo acceso → sube P(perfil 2); empleo formal + escolaridad alta + urbano → sube P(perfil 1); edad 15–27 + internet alto + urbano → sube P(perfil 5); remesas altas + hogar con ausente → sube P(perfil 6).
2. **Modificadores** — género, generación, religiosidad *por práctica efectiva*, estatus migratorio, exposición global.
3. **Hogar** — los agentes se agrupan en hogares (unidad de decisión real para G5: corresidencia, pooling, remesas).

### 3.2 Esquema de agente

```yaml
agente:
  id: a_9f3c21
  celda: "09014"
  hogar: h_4412
  perfil: 2
  demo: {edad: 41, sexo: M, escolaridad: secundaria, generacion: X}
  mods: {religiosidad: practicante, migratorio: none, exposicion_global: baja}

  # parámetros DERIVADOS (no fijos): f(perfil, celda, estado)
  params:
    horizonte_temporal: 0.21
    radio_confianza: 0.34
    aversion_riesgo: 0.83
    sens_estatus: 0.50
    deferencia: 0.72
    familismo: 0.88
    exposicion_violencia: 0.61
    confianza_institucional: 0.19
    acceso: 0.38

  estado:
    empleo: informal
    ingreso_mensual: 8400
    volatilidad_ingreso: 0.31
    deuda: {monto: 12000, tipo: [bnpl, tienda], al_corriente: true}
    salud: {cronico: none, cobertura: none}
    capital_social: 0.44
    estres_financiero: 0.38
    productos: [tanda, tienda_credito]
```

**Punto crítico de diseño.** `params` **se recalcula cada tick** como función del perfil, la celda y el estado. Si el municipio se formaliza, `horizonte_temporal` sube *para los mismos agentes*. Si los parámetros fueran fijos por perfil, el simulador sería esencialista por construcción — exactamente lo que el corpus prohíbe.

```python
def derivar_params(agente, celda, gens):
    base = PERFIL_BASE[agente.perfil]          # punto de partida
    for g in gens:                              # G1..G6
        for p, coef in g.afecta.items():
            base[p] += coef * g.intensidad(celda) * g.peso_perfil[agente.perfil]
    return clamp(base, 0, 1)
```

---

## 4. Capa de red (`net/`)

### 4.1 Tipos de lazo

| Lazo | Peso | Generación | Transporta |
|---|---|---|---|
| **Familiar** | 0.8–1.0 | Hogar + parentesco extendido; con cola transnacional (perfil 6) | Pooling económico, cuidado, remesas, información de alta credibilidad |
| **Puente** | 0.4–0.7 | Compadrazgo, paisanaje, congregación religiosa, trabajo | Confianza radial hacia fuera, tandas, cooperación, difusión de productos, clientelismo |
| **Débil** | 0.1–0.3 | Vecindad, colegas, digital (perfiles 1,4,5) | Información de baja credibilidad, alcance amplio |

Generación: modelo de **homofilia + proximidad espacial** con cola pesada (los lazos a larga distancia son los que sostienen la migración y la difusión inter-regional). Grado medio calibrable contra datos de capital social (ENCUCI) y de participación en tandas (ENIF: 32.7%).

### 4.2 Difusión

Un producto, una creencia o una práctica se propagan por umbral: un agente adopta si `Σ(peso_lazo × adopción_vecino) > umbral(params.radio_confianza, params.aversion_riesgo)`. **Sin puente personal, el umbral efectivo se dispara** — que es la implementación literal de la regla **en HIPÓTESIS** "el canal de confianza vence a la campaña institucional".

> ⚠️ **CORREGIDO 28/jul/2026.** El texto original decía *"la regla **validada**"*. No lo está, y en dos sentidos: **ADR-20** la dejó explícitamente en `HIPÓTESIS`, y desde la Ronda 4 el generador que la sostiene —**G1b, difusión por confianza radial**— está **CONTRADICHO** por su propio registro: Nu (15M de clientes, sin sucursales, adopción rural = urbana) y Kueski/Aplazo **difundieron sin puente personal**. Sus coeficientes están a revisión.
> **Lo que sí se sostiene es G1a**, adopción *individual* mediada por puente personal — que es una afirmación distinta y más estrecha. Implementar el umbral como si la difusión radial estuviera validada codifica en el ejecutable una hipótesis contradicha.

---

## 5. Motor de decisión (`engine/`)

### 5.1 El DSL de reglas

Formato canónico, una entrada por regla:

```yaml
- id: dinero.ahorro.informal
  dominio: dinero
  situacion: le_ofrecen_ahorro_formal
  si:
    perfil: [2, 3, 6]
    params: {horizonte_temporal: "<0.4"}
    disparadores:
      puente_personal: false
      cobertura_formal: false
  entonces:
    - {conducta: ignora_producto, p: 0.74}
    - {conducta: adopta_cautelosa, p: 0.21}
    - {conducta: adopta_pleno,     p: 0.05}
  porque:
    generador: [G1, G3]
    mecanismo: "confianza institucional baja + sin respaldo visible"
  tier: FUERTE
  ic_p: 0.06                      # ancho de banda; función del tier
  fuente: [ENIF2024, "report:behavioral_finance", "validacion:OXXO_vs_CoDi"]
  falsable_si: "con respaldo visible y puente personal, adopta_pleno > 0.4"
```

```yaml
- id: civico.voto.clientelar
  dominio: civico
  situacion: le_ofrecen_despensa_preelectoral
  si:
    disparadores:
      quien_observa: "cree_que_su_voto_es_observable"
  entonces:
    - {conducta: voto_clientelar, p: 0.63}   # ⚠ CIFRA DE LABORATORIO
    - {conducta: toma_y_vota_libre, p: 0.37}
  porque: {generador: [G1], mecanismo: "percepción del secreto del voto"}
  tier: MEDIA                                # v0.2: era FUERTE
  procedencia_p: LABORATORIO                 # v0.2: campo nuevo, obligatorio
  fuente: ["validacion:V2_clientelismo", "Ascencio-Chang 2025"]
  # regla espejo: si NO cree observable → voto_clientelar p:0.06
```

> ⚠️ **CORREGIDO en v0.2 — el 0.63 es de laboratorio, no de campo.**
>
> El par **0.06 → 0.63** viene de **Ascencio-Chang (2025)**, un **experimento de laboratorio** sobre percepción del secreto del voto. La spec v0.1 lo compiló como probabilidad de conducta en campo **con tier `FUERTE`**. Son dos cosas distintas: un efecto de laboratorio mide **disposición declarada bajo condiciones controladas**, no incidencia observada en una elección real.
>
> **Qué se conserva:** el **signo y la magnitud relativa** del efecto —la percepción de observabilidad mueve muchísimo la conducta— están bien sostenidos y son el mecanismo de cesión de la autonomía del votante (`modelo §3.7`, P-02).
> **Qué se retira:** que **0.63 sea la probabilidad en campo**. Ninguna elección mexicana ha medido eso.
>
> **Campo `procedencia_p` obligatorio, nuevo en v0.2:** toda probabilidad de regla declara si es `CAMPO`, `LABORATORIO`, `DERIVADA` o `ASIGNADA`. *Es la misma disciplina de `procedencia.yaml` para los parámetros, que a las probabilidades de regla nunca se les aplicó.* **Una `p` de laboratorio no puede llevar tier `FUERTE`.**

Reglas de esquema (validadas en CI):
- Toda regla **debe** tener `tier`, `porque.generador` y `fuente`. Sin fuente no compila.
- `ic_p` se deriva automáticamente del tier: `FUERTE→±0.06`, `MEDIA→±0.15`, `HIPÓTESIS→±0.30`.
- Toda regla `FUERTE` **debe** tener `falsable_si`.

### 5.2 Evaluación

```
decidir(agente, situación, celda, red):
  1. d ← evaluar_disparadores(situación, agente, celda, red)   # los 7
  2. R ← reglas[dominio][situación] que hacen match con (perfil, params, d)
  3. si |R| = 0        → conducta_default + flag NO_COVERAGE
     si |R| > 1        → resolver por especificidad; empate → promediar y flag AMBIGUO
  4. p ← distribución de la regla, perturbada por ic_p (Monte Carlo)
  5. conducta ← muestreo(p)
  6. traza ← {regla.id, tier, generador, disparadores, p}     # auditabilidad total
```

**El flag `NO_COVERAGE` es un entregable, no un error.** Su acumulación por celda **es** el mapa de confianza: dice dónde el modelo está inventando.

---

## 6. Bucle de simulación (`loop/`)

Tick = **1 trimestre** (alineado con ENOE, que es la serie más frecuente y la que da dinámica de empleo).

```
para cada tick:
  1. aplicar_exogeno()        # políticas activas, choques programados
  2. derivar_params()         # G1..G6 × celda → params de cada agente
  3. muestrear_situaciones()  # quién enfrenta qué decisión este trimestre
  4. decidir()                # motor de reglas → distribución → muestra
  5. aplicar_efectos()        # estado del agente y del hogar
  6. difundir()               # red: información, productos, cooperación
  7. agregar()                # indicadores de celda
  8. retroalimentar()         # indicadores → capas estructurales
  9. registrar()              # trazas, IC, flags de cobertura
```

### 6.1 Bucles nombrados (la emergencia esperada)

| Bucle | Mecánica | Tier del coeficiente |
|---|---|---|
| **Espiral de desconfianza** | Victimización ↑ → no-denuncia ↑ → impunidad percibida ↑ → confianza institucional ↓ → menos denuncia | Dirección FUERTE; ritmo HIPÓTESIS |
| **Trampa de informalidad** | Informalidad ↑ → horizonte ↓ → menos ahorro/inversión formal → menos formalización | Dirección FUERTE; ritmo HIPÓTESIS |
| **Trampa social de la mordida** | Expectativa de que todos pagan → pagar es óptimo → se confirma la expectativa | Dirección FUERTE (Rothstein) |
| **Bomba de crédito** | Fricción baja → adopción ↑ → deuda ↑ → estrés ↑ → mora ↑ *(condicional a CAT alto y reporte incompleto a burós)* | Dirección MEDIA; umbral HIPÓTESIS |
| **Nivelación** | Prosperidad visible ↑ → envidia/extorsión ↑ → ocultamiento ↑ → inversión visible ↓ | MEDIA |
| **Círculo virtuoso de formalización** | Empleo formal ↑ → horizonte ↑ → ahorro/seguro ↑ → resiliencia ↑ | Dirección FUERTE (Progresa); magnitud MEDIA |

Nótese la columna derecha: **la dirección casi siempre está bien evidenciada; el ritmo casi nunca.** Es el hueco de `milpa-whitepaper §6.2`, hecho explícito en el código.

---

## 7. API de intervenciones (`interventions/`)

```yaml
- tipo: politica.formalizacion
  target: {estado: "Jalisco"}
  magnitud: {tasa_informalidad: -0.10}
  rampa_trimestres: 8

- tipo: politica.digitalizar_tramite
  target: {nacional: true}
  magnitud: {calidad_tramite: +0.35, discrecionalidad: -0.5}

- tipo: politica.cuidados
  target: {municipios: [...]}
  magnitud: {cobertura_cuidados: +0.4}

- tipo: choque.violencia
  target: {municipios: [...]}
  magnitud: {homicidio_100k: x2.5}
  duracion: 6

- tipo: producto.lanzamiento
  nombre: "cuenta_ahorro_X"
  friccion: baja | media | alta
  canal: institucional | puente_personal | retail_fisico
  respaldo_visible: true | false

- tipo: comunicacion.campana
  mensajero: institucional | figura_cercana | creador_digital
  # nota pedagógica: mensajero=institucional produce efecto ~nulo por diseño del modelo
```

Cada intervención registra su **contrafactual automático**: el sim corre en paralelo la rama sin intervención, de modo que la salida siempre es un **delta con banda**, nunca un nivel absoluto.

---

## 8. Salidas

1. **Mapa doble obligatorio** — conducta + su mapa espejo estructural, lado a lado. No se puede renderizar uno sin el otro (restricción de la capa de presentación, no una convención).
2. **Mapa de confianza** — palidez ∝ (SAE + IC + NO_COVERAGE). Gris de exclusión para `OUT_OF_MODEL`.
3. **Series con bandas** — nunca una línea limpia; siempre el fan chart del Monte Carlo.
4. **Trazas auditables** — para cualquier resultado se puede preguntar "¿por qué?" y obtener la cadena regla → tier → generador → capa estructural → fuente de dato.
5. **Diario narrativo (opcional, fuera del loop)** — un LLM traduce trayectorias de agentes representativos a viñetas legibles ("Don Rafa, tras dos trimestres de…"). **Nunca dentro del loop de decisión**: el LLM narra, no decide (reproducibilidad y velocidad).

---

## 9. Stack y escalabilidad

| Capa | Prototipo | Producción |
|---|---|---|
| ETL / datos | Python + DuckDB + Parquet | igual + orquestación (Dagster/Prefect) |
| SAE | modelos jerárquicos bayesianos (PyMC / `sae` en R) | igual, precomputado |
| Motor | Python + Mesa (10⁴ agentes, 1 municipio) | **Rust** (10⁶–10⁷ agentes) con bindings Python |
| Grafo | networkx | rustworkx / grafo propio CSR |
| Front-end | Streamlit para depurar | TypeScript + MapLibre/deck.gl (+ WASM si se quiere el motor en el navegador) |
| Reglas | YAML + validación de esquema | igual, con CI que corre los backtests en cada PR |

**Estrategia de escala:** el prototipo debe correr un municipio con 50k agentes en segundos. El salto a nacional (≈10⁷ agentes representando 130M con factor de expansión) exige el motor en Rust y muestreo por celda —no todos los agentes deciden todo cada tick—.

---

## 10. Pruebas (`tests/`)

Tres suites, todas bloqueantes en CI:

1. **Esquema** — toda regla tiene tier, generador y fuente; toda regla FUERTE tiene `falsable_si`.
2. **Hechos estilizados** — la corrida base debe reproducir marginales conocidas: informalidad ~55%, cifra negra ~93%, participación presidencial ~60% vs. judicial ~13%, IMOR de crédito popular 15–27%, penetración de tanda ~33%.
3. **Backtests forenses** — los cinco casos de `milpa-whitepaper §5.4`. Cada uno es un test con criterio de aprobación explícito.

---

### 10.1 · `bt.oxxo_vs_codi` — el gate de Fase 1 *(ADR-25, ESPECIFICACIÓN CORREGIDA en v0.2)*

> 🚩 **Éste es el go/no-go del programa.** Si pasa, MILPA Fase 1 arranca. Por eso importa **por qué** pasa.

**Lo que decía la v0.1, y por qué estaba mal:**

> *"Con **canal institucional frío y sin respaldo**, la adopción a 24 trimestres debe quedar por debajo del 10% de la adopción **por canal retail-efectivo**."*

El criterio está escrito **en términos de CANAL**. Canal es el mecanismo de **`modelo §3.1` / G1a** — *el producto ofrecido por canal de confianza personal se adopta*. Pero OXXO vs. CoDi existe para probar **`modelo §3.3`**: *utilidad vs. coerción con riesgo fiscal*. **La explicación canónica del fracaso de CoDi es riesgo fiscal percibido + fricción, NO desconfianza ni ausencia de puente personal.**

**Consecuencia exacta:** si MILPA implementa bien el mecanismo de confianza y mal el de coerción, **el backtest pasa igual** — y pasa por la razón equivocada. Un gate que no distingue cuál de dos mecanismos lo hizo pasar **no es un gate: es un espejo.**

**Especificación corregida — tres condiciones, las tres obligatorias:**

| | Condición | Qué prueba | Criterio |
|---|---|---|---|
| **A** | **Reproducción.** Con `coercitivo=true` y `riesgo_fiscal_percibido=true`, la adopción del servicio tipo CoDi a 24 trimestres queda **<10%** de la del canal retail-efectivo tipo OXXO Pay | Que el modelo reproduce el desenlace | Necesaria, **no suficiente** |
| **B** | **Prueba de mecanismo.** Al apagar **`riesgo_fiscal_percibido`** manteniendo **el canal constante**, la diferencia debe **colapsar** — la brecha se reduce ≥70% | Que el resultado lo produce §3.3 | **Si no colapsa, el modelo llegó al desenlace por otro camino** |
| **C** | **Anti-confusión.** Al apagar **el canal de confianza personal** manteniendo `riesgo_fiscal_percibido=true`, la diferencia debe **PERSISTIR** — se reduce <30% | Que el resultado **no** lo produce G1a | **Ésta faltaba entera en la v0.1.** Sin ella el gate no puede distinguir los dos mecanismos |

**El gate pasa solo si A **y** B **y** C.** Pasar A sola es lo que la v0.1 pedía, y es exactamente lo que ADR-25 denuncia.

⚠️ **Dependencias verificadas antes de escribir esto:**
- `riesgo_fiscal_percibido` es un **disparador de nivel 2** (ADR-26). La spec v0.1 solo implementaba el nivel 1, así que **el campo del que depende el gate era invisible para el bucle**. Con los 42 booleanos de dominio ya declarados, la condición B es evaluable.
- La **regla espejo** `tramite.gobierno_digital.util_sin_coercion` está restituida en `tramite.yaml` v0.2.0 precisamente para esto: sin ella, apagar `riesgo_fiscal_percibido` cae en **`NO_COVERAGE`** y **el gate pasaría por pérdida de cobertura, no por prueba de mecanismo**.
- ⚠️ **Probabilidades NO calibradas.** El corpus da la **dirección** (SPEI se adopta, CoDi no), no la magnitud. Los criterios de B y C (**≥70%**, **<30%**) son **ASIGNADOS**: se eligen porque un colapso parcial no distingue mecanismos, pero **no salen de ningún dato**. Calibrar contra series de adopción de SPEI antes de correr Fase 1.

**Y lo que el gate sigue sin poder hacer:** distinguir **coerción** de **fricción**. La explicación canónica del fracaso de CoDi tiene **dos** componentes, y `riesgo_fiscal_percibido` solo captura el primero. Un servicio coercitivo y de alta fricción falla por ambas, y este gate no separa cuál pesó. **Se declara como límite, no se resuelve aquí.**

Un cuarto modo, no automatizable pero obligatorio antes de cualquier publicación: **correr en modo sin-hipótesis** y reportar qué conclusiones sobreviven.

---

*Toda regla, coeficiente y capa de este sistema es trazable a una fuente del corpus o a una estadística pública con fecha. Lo que no lo sea, no entra — y si entra por necesidad de cierre del modelo, entra marcado como `HIPÓTESIS` y con su cláusula de falsación.*
