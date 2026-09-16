# F6 · factibilidad de transferencia R01/R09 · preparación v1.0

Estado: **PREPARADA-PARA-MESA · NO AUTORIZA EMISIONES NI R**. Esta spec no
abre FP-374, no ejecuta el piloto de seis familias firmado por F-16 y no
convierte dos familias en evidencia confirmatoria. Es una prueba de
factibilidad cerrada sobre R01 y R09; no busca sustitutas.

Base documental y de código: `origin/main` en
`9dffd6455c67e2ca99740e79f90be59a13f250e1`. Tarjetas ejecutables por el
preflight: `tarjetas.yaml`. Fixtures: `fixtures/SINTETICO-NO-MEDICION.json`.

## 1. Decisión corta

La preparación técnica está materializada y probada, pero **ninguna celda es
elegible para llamadas** con el contrato actual:

| candidata | definición de R | enlace de M | reserva | decisión de preparación |
| --- | --- | --- | --- | --- |
| R01 · MOCIBA 2021/2022 | `FILTRO-NO-ACREDITADO`: los FD prueban variable, códigos, peso y diseño, pero no el flujo que hace aplicable P12 | `CANDIDATO-NO-ELEGIBLE`: no denuncia por miedo/desconfianza entre no denunciantes no es el complemento de denuncia total | limpia; no se abrió BD ni R | rechazo explícito de las dos celdas |
| R09 · ISSP ZA6980 por `SEX` | formulario y etiqueta v26 coinciden semánticamente; falta el codebook integrado que acredite etiquetas de valor, sin inferir el cruce | `CANDIDATO-NO-ELEGIBLE`: recibir dinero familiar para vejez no es intención de acudir a familiares o amigos por un préstamo | `EXPUESTA-OBJETIVO`: apareció incidentalmente un tabulado v26 versionado durante la búsqueda | rechazo explícito de las dos celdas y retiro de pretensión ciega |

La consecuencia no es fabricar una transformación: el presupuesto viable es
cero llamadas. El preflight conserva las cuatro tarjetas para que mesa vea
exactamente qué pieza falla y para que una futura sucesora no tenga que
rediseñar códigos, filtros ni contratos.

## 2. Lista cerrada, familias y celdas

Hay dos familias, aunque cada una tenga dos celdas:

1. `R01-CIV-MOCIBA-DENUNCIA`: `R01-MOCIBA-2021` y
   `R01-MOCIBA-2022`.
2. `R09-FAM-ISSP-APOYO-DINERO`: `R09-ISSP-2017-SEX-1` y
   `R09-ISSP-2017-SEX-2`.

Olas y dominios son cobertura intrafamilia, no cuatro observaciones
independientes. No entran MOCIBA 2024/2025, ZA5900, otras variables de ZA6980,
ENIF 2024 `localidad × edad` ni sustitutas del panel.

## 3. Definiciones de R

### 3.1 R01 · MOCIBA

Los dos FD coinciden en `P12_5`: `1=Sí`, `2=No`; 2022 además documenta
`b=blanco`. `FACTOR` es ponderador; `UPM_DIS` y `EST_DIS` son unidades y
estratos de diseño. `P4_01..P4_13` identifica la batería de situaciones de
ciberacoso, pero el FD compacto no contiene una nota *Aplica* ni una
instrucción que pruebe que “al menos una P4=1” sea exactamente el universo que
recibe P12. Por ello:

- un `1` de `P12_5` es evento y un `2` es no-evento;
- blanco, salto y no respuesta quedan fuera del denominador;
- nunca se recodifica blanco como `No`;
- no se abre la BD para inferir el flujo empíricamente;
- ambas celdas quedan `FILTRO-NO-ACREDITADO` hasta obtener cuestionario o
  manual/flujo ya adquirido que cite la secuencia.

Fuentes efectivamente usadas y verificadas por hash:

- MOCIBA 2021 FD, hoja `TMOCIBA`: filas físicas 38, 2306, 2503–2504,
  2531, 2542–2543, 2576–2578; SHA-256
  `375bf7c1bcdbcc9b0716cd3b63fe940906a97783a3b69f2afad35f35950b1e25`.
- MOCIBA 2022 FD, hoja `TMociba`: filas físicas 38, 2510, 2728–2730,
  2765, 2776–2777, 2810–2812; SHA-256
  `923fa85a665219200d6c87d1f5af25090870bf91957d16f1008726e78edc396e`.

### 3.2 R09 · ISSP ZA6980

El evento propuesto es exactamente la categoría conjunta
**“Familiares o amigos cercanos”** como primera fuente hipotética para pedir
prestada una gran suma. No separa familiares de amigos y no significa recibir
dinero. El filtro propuesto es `c_alphan=MX`; los dominios son `SEX=1` y
`SEX=2`; `SEX=9` queda fuera. `WEIGHT` es el ponderador. Para `v26`, `1` es el
evento, `2..7` no-evento, y `8 No puedo elegir`, `9`/missing quedan fuera del
denominador.

El cuestionario mexicano acredita Q8a y los códigos nacionales. El inventario
de metadatos acredita `v26 = Q8a`, además de `c_alphan`, `WEIGHT` y `SEX`, sin
abrir filas de respondentes en este acto. No obstante, los dos hechos no son
por sí solos un codebook integrado de etiquetas de valor: la correspondencia
de `1` nacional a `1` en `v26` no se afirma por inferencia. Falta el documento
integrado exacto.

Fuentes usadas:

- `ZA6980_q_mx.pdf`, PDF p.3 / impresa p.2, Pregunta 8a; SHA-256
  `61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed`.
- `ZA6980_backgroundvar_mx.pdf`, ficha `SEX`; SHA-256
  `6004c300ca1331bfd15f163c4deaa726c71b66b46ae9e05361f40ae8cc26ca5f`.
- `data/inventario-reactivos-descargas-mx-v1_2.tsv`, líneas 47019, 47089,
  47101 y 47124; SHA-256
  `a2771a7066fdb8f5684eb81241981b81b93ba749a33fa652b23cc12141212756`.

Durante esa búsqueda apareció incidentalmente en
`data/apertura-issp-variables-2026-08-13.tsv` una distribución ya calculada de
`v26`. No se reproduce aquí. La exposición afecta ambas celdas de la misma
familia, se registra como `EXPUESTA-OBJETIVO` y retira la pretensión de una
evaluación ciega de R09 con este procedimiento.

## 4. Qué emitiría M y por qué no alcanza

El emisor M de F5 y el motor matricial `B·θ` son objetos distintos.

- R01 apunta a `civico.denuncia.miedo_desconfianza`. Su estimando preexistente
  está condicionado a víctimas adultas con delitos no denunciados y mide una
  razón de no denuncia. No emite denuncia total, no cubre todo motivo de no
  denuncia y no se puede complementar para obtener `P12_5`.
- R09 apunta a `familia.apoyo.recibe_dinero_familiares`, calibrada sobre
  recepción efectiva de dinero familiar para vejez en un universo ENIF
  restringido. No emite una preferencia hipotética de apoyo y mucho menos
  separa la categoría ISSP conjunta.

No existe en el snapshot un camino explícito que produzca ninguno de esos
desenlaces. Afinar M, escoger una transformación después de ver R o tratar
cercanía semántica como función predictiva está prohibido. Las cuatro tarjetas
quedan `CANDIDATO-NO-ELEGIBLE`.

`B` tampoco se simula: no hay referencia temporal independiente predeclarada.
Si su construcción exigiera abrir un R reservado, se excluye antes de
emisiones. Compartir la letra M/B con otra pieza no crea sustituibilidad.

## 5. Dieta, transporte e identidad

Una ejecución sucesora sólo podría usar una nueva ubicación exclusiva de F6.
No reutilizaría capturas pre-GEN2 ni directorios del piloto de Opus.

- M recibe tarjeta, semántica de su regla y snapshot preexistente con hash;
  nunca R, microdatos, frecuencias o derivados del objetivo.
- `L_SOLO` recibe sólo la tarjeta y el formato de salida. Son ocho réplicas por
  celda; abstención conserva falta de cobertura.
- `L_CORPUS` no se incluye.
- Antes de cualquier llamada se firman proveedor, modelo/versión, endpoint,
  cliente, cuenta/proyecto sin secretos, plantillas y hashes, herramientas,
  temperatura/top-p/seed, ventana, truncación, orden, parser y horario.
- Máximo dos reintentos por posición, sólo por error técnico. Posiciones,
  intentos, turnos y unidades facturadas se registran por separado.

## 6. Orden ciego y prueba temporal

El orden obligatorio de una sucesora elegible es:

1. commit de spec, tarjetas, snapshot, identidad y orden;
2. firma de mesa y autorización explícita de llamadas;
3. emisiones M y `L_SOLO` selladas; B sólo si ya era construible sin R;
4. verificación de que los commits/timestamps de todas las emisiones preceden
   cualquier acceso a R;
5. apertura de R, estimación y comparación;
6. publicación de puntos, cobertura, abstenciones y limitaciones.

Una exposición, identidad discordante o contrato roto detiene la celda. Nunca
se para porque un resultado guste o cruce significación. El aprendizaje de
factibilidad no se recicla como confirmación del procedimiento ajustado.

## 7. Comparación posterior, si existieran celdas elegibles

Escala común: toda predicción y R se expresa como proporción `0..1`; el error
absoluto se convierte explícitamente a puntos porcentuales:

`error_pp = 100 × |predicción_proporción − R_proporción|`.

La primaria es M frente a la mediana de hasta ocho réplicas válidas de
`L_SOLO`. Una abstención no es cero. Se reportan por celda error pareado,
cobertura y causa de pérdida; luego se promedian celdas dentro de cada familia.
Dos olas o dos sexos siguen contando como una familia.

La incertidumbre de encuesta de R, la variación de réplicas L y la variación
entre familias se mantienen separadas. Sin diseño muestral acreditado, R se
reporta descriptivamente. Con dos familias no se produce IC poblacional de
transferencia, no se remuestrean réplicas L como familias y no se asigna
varianza cero a R. Esta factibilidad no decide H0 ni recupera el tamaño de
diseño del protocolo confirmatorio.

## 8. Presupuesto propuesto, no autorizado

| concepto | nominal si las 4 celdas fueran elegibles | viable hoy |
| --- | ---: | ---: |
| familias | 2 | 0 |
| celdas | 4 | 0 |
| posiciones lógicas `L_SOLO` (8/celda) | 32 | 0 |
| emisiones M | 4 | 0 |
| estimaciones R | hasta 4 | 0 |
| B | 0 | 0 |
| intentos máximos (2 reintentos técnicos) | 96 | 0 |

El nominal de 32 posiciones no es autorización ni plan ejecutable. Turnos y
unidades facturadas dependen del cliente que mesa firme y no se confunden con
posiciones o intentos. No hay tarifa verificable porque modelo/modalidad no
están firmados; coste monetario queda pendiente. Se hicieron cero llamadas
para estimarlo.

## 9. Preflight y fixtures

Comando reproducible, limitado al YAML:

```bash
python3 tools/f6_factibilidad_prepara.py \
  --cards forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml \
  --json
```

El preflight valida campos, escala, máximo de familias/celdas y gates de
definición, M, reserva y firma. `payload_ref` es declarativo y nunca se
resuelve. Un YAML parseable no se vuelve elegible ni autorizado. El módulo
también expone transformaciones pequeñas para fixtures inequívocamente
`SINTETICO-NO-MEDICION`: denominador, categoría conjunta, escala, pesos,
abstenciones y agregación familiar.

## 10. Decisión de mesa y texto propuesto de firma

Máximo tres decisiones materiales:

1. **R01:** rechazar estas celdas o exigir, conjuntamente, flujo documental de
   P12 y un enlace predictivo de M definido antes de R.
2. **R09:** excluir del duelo ciego actual por exposición y falta de enlace de
   constructo; decidir sólo si conserva valor descriptivo no ciego.
3. **Llamadas:** con cero celdas elegibles, no autorizar posiciones M/L/R/B.

Texto propuesto, **no firmado ni adoptado**:

> TEXTO DE FIRMA SUGERIDO F6-FACTIBILIDAD-PREPARACION-1 — autoridad y fecha por completar:
> se adopta la lectura de factibilidad de `spec.md` y `tarjetas.yaml`; R01
> queda condicionada al flujo documental de P12 y a un enlace M pre-R; R09 se
> excluye de evaluación ciega por exposición y desalineación de constructo.
> Se autorizan cero llamadas, cero emisiones M/L/B y cero aperturas R. Una
> ejecución futura exige spec sucesora, identidad de modelo/cliente, presupuesto
> recalculado y nueva autorización explícita.

## 11. Lo que no decide

No decide θ, G5, el parámetro M uno, corte de edad, crosswalk, adopción de candidatas,
generalización confirmatoria, cierre de FP-374 ni NC de transferencia. No abre
ENIF 2024 `localidad × edad`, no modifica el motor, no escribe gobernanza ni
registros compartidos y no hace medición.
