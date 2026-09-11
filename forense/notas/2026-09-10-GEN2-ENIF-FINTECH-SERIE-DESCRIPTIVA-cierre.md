# ACTO GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA · cierre

Fecha: 10/sep/2026 (ejecución sellada 11/sep UTC). Entorno: CAJA
(Ubuntu/WSL2), corpus compartido montado. Rama:
`acto/gen2-enif-fintech-serie`. Cero llamadas nuevas a modelos. Encargo
archivado verbatim en
`forense/encargos/2026-09-10-GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA.md`.

## 1. Resultado útil

La extensión posible no forma una serie continua de tres olas. ENIF 2018 es
`NO-ESTIMABLE` para este objeto: no tiene una categoría identificable de
cuenta/crédito fintech y tampoco pregunta el canal del último producto. ENIF
2021 sí mide el proxy. ENIF 2024 permanece como antecedente publicado, no como
otra medición de este acto.

En 2021, entre personas con cuenta contratada por Internet/app y canal válido
del último producto (n=337; masa=2,257,763), la distribución ponderada fue:
sucursal 49.73% (IC95 [41.73%, 57.72%]), app 22.53% [15.49%, 29.57%], empleador
13.71% [8.85%, 18.58%], página web 11.12% [5.37%, 16.88%], promotor 2.26%
[0.74%, 3.77%], establecimiento 0.66% [0.00%, 1.38%] y otro 0.00%. Esta
cuenta **no admite delta** con 2024: el criterio 2024 añade “no bancaria”,
cambia proveedores de ejemplo y amplía/reordena el catálogo de canal.

En 2021, entre personas con crédito contratado por Internet/app y canal
válido (n=58; masa=345,435), app concentró 69.80% [56.10%, 83.50%], página web
12.14% [3.88%, 20.41%], sucursal 8.23% [1.78%, 14.68%], establecimiento 4.97%
[0.00%, 11.91%], promotor 3.57% [0.00%, 9.09%] y otro 1.28% [0.00%, 3.11%].
Frente a los porcentajes 2024 ya publicados, los cambios descriptivos
2024−2021 son: app −12.30 pp, web +8.46 pp, sucursal +3.27 pp, otro +1.82 pp,
promotor +0.63 pp y establecimiento −1.67 pp. La comparación conserva la
deriva del ejemplo Playbusiness→YoTePresto y el redondeo de 2024 induce
±0.05 pp por categoría. Son cortes transversales, no panel ni efecto del
crecimiento fintech.

Tabla exacta: `data/corrida0/enif-fintech-serie-v1_0.tsv`. Figura derivada:
`data/corrida0/enif-fintech-serie-v1_0.svg`. La figura da IC sólo a 2021;
2024 no los publicó. La tabla antecedente de cuenta 2024 publica denominador
n=1,407 pero sólo siete categorías que suman n=1,406; esta entrega conserva
una fila `otro_no_publicado` sin inventar su n ni su porcentaje.

## 2. Correspondencia antes del cálculo

La correspondencia completa está en
`data/corrida0/enif-fintech-correspondencia-v1_0.tsv` y se congeló antes del
primer resultado 2021. Se leyeron los cuestionarios y FD de 2018, 2021 y 2024;
la ausencia de texto en el inventario no se usó como prueba semántica.

| ola/familia | criterio | canal | población | decisión |
|---|---|---|---|---|
| 2018 cuenta | no hay categoría fintech; `P5.23` es banca celular en cuenta bancaria | no existe pregunta de canal del último producto | persona elegida 18–70 | `NO-ESTIMABLE`, ruptura estructural |
| 2018 crédito | batería tradicional + “otro”, sin Internet/app identificable | no existe pregunta de canal del último producto | persona elegida 18–70 | `NO-ESTIMABLE`, ruptura estructural |
| 2021 cuenta | `P5_4_8=1` | `P5_17` (1..7; 9 no sabe) | persona elegida 18+ | medir; lado a lado con 2024, sin delta |
| 2021 crédito | `P6_2_8=1` | `P6_7` (1..6; 9 no sabe) | persona elegida 18+ | medir; comparable con deriva de ejemplos |
| 2024 cuenta | `P5_4_8=1`, añade “no bancaria” | `P5_16` (1..8; catálogo ampliado) | persona elegida 18+ | referencia con ruptura |
| 2024 crédito | `P6_2_8=1` | `P6_6` (1..6) | persona elegida 18+ | referencia comparable |

No se recodificó “otro” de 2018 como fintech ni “recomendación de conocidos”
como canal. Los ponderadores se resolvieron por ola: `FAC_ELE` en 2021 y
`FAC_PER` sólo para el control 2024. Diseño: `EST_DIS`/`UPM_DIS`.

## 3. Congelamiento, medición y controles

La spec humana y el medidor quedaron congelados y publicados en
`5b92cee28946453c7d9716df632da7089e33e418`, antes del primer resultado. El
prerregistro tiene sha256
`4b3805b521cf5644e64a0dd5c19b5efc508d16927a798774e0c39973d152d0db`.
`spec-check` verificó 11/11 pares físicos contra 317,718 filas de inventario.

Corrida `CALC-ENIF-FINTECH-0001--5b92cee28946`; fuente primaria
`enif2021_csv`, sha256
`0f314fa3733b4b5519486ed4015fca1c9e0864840bcd5944aa7de27796fe5cd9`;
control `enif2024_csv`, sha256
`a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c`.
Secuencia: preflight VERDE → run exit 0 → verify **REPRODUCE**, contexto
**IDENTICO**, 131/131 resultados. `sello.json` sha256
`e313b5413f65e7c92a6def2d07b70fb3a8f191851ccb68cea9f0d7aab4753b05`.

El punto usa `FAC_ELE`; EE e IC95 usan linealización de razón por UPM dentro
de estrato sobre la muestra completa para los dos dominios. Hay 235 estratos,
2,011 UPM, cero estratos de UPM única, cero filas del dominio sin diseño y
cero pesos inválidos. Todos los filtros `sí` tuvieron canal sustantivo: cuenta
337/337 y crédito 58/58; no hubo blanco, no sabe ni fuera de catálogo. Las
categorías cierran a 1 con tolerancia `1e-10`.

El medidor sólo repitió un control 2024 previamente conocido: crédito/app
reprodujo n=200, masa redondeada 1,178,431 y p redondeada 0.575. No emitió
resultados numéricos 2024 nuevos. Después del sello,
`control_independiente.py` —implementación separada, sin importar el medidor—
reconstruyó crédito/app 2021: numerador n=33 y masa=241,124; denominador n=58
y masa=345,435; p=0.698030020120. Coincide con las cinco salidas primarias a
las tolerancias congeladas. Recibo:
`data/corrida0/CALC-ENIF-FINTECH-0001/control-independiente.json`.

## 4. Objeto, consumidor y propuesta de procedencia

El comando `python3 tools/ya_medido.py dinero.credito.scoring_alternativo`
resolvió el consumidor a `R1.6` y devolvió `NUNCA-MEDIDA`. Este cálculo no
mide la probabilidad de esa regla: aporta contexto descriptivo sobre canal y
queda rotulado `DESCRIPTIVO-NO-CALIBRA`. No altera tasas del motor, el mapa
id↔R-n ni el M congelado de F5.

La actualización propuesta al acto dueño de `milpa/procedencia.yaml` es la
siguiente; **no se escribe en `milpa/` desde este acto**:

```yaml
serie_descriptiva_propuesta:
  objeto: "canal del último producto entre personas con tenencia fintech; no canal del producto fintech exacto"
  uso_motor: "DESCRIPTIVO-NO-CALIBRA"
  consumidor_contextual: "dinero.credito.scoring_alternativo (R1.6)"
  fuente_2021: "CALC-ENIF-FINTECH-0001--5b92cee28946"
  cuenta:
    2018: {estado: "NO-ESTIMABLE-RUPTURA-ESTRUCTURAL"}
    2021: {n: 337, poblacion_expandida: 2257763, porcentajes: {sucursal: 0.497268756730, app_celular: 0.225282724538, empleador: 0.137135740111, pagina_internet: 0.111203434550, promotor: 0.022550196810, establecimiento: 0.006559147262, otro: 0.0}}
    comparabilidad_2024: "RUPTURA-DEFINICIONAL; LADO-A-LADO-SIN-DELTA"
  credito:
    2018: {estado: "NO-ESTIMABLE-RUPTURA-ESTRUCTURAL"}
    2021: {n: 58, poblacion_expandida: 345435, porcentajes: {app_celular: 0.698030020120, pagina_internet: 0.121420817230, sucursal: 0.082313604586, establecimiento: 0.049728603066, promotor: 0.035688334998, otro: 0.012818620001}}
    delta_2024_menos_2021_pp: {app_celular: -12.3030020120, pagina_internet: 8.4579182770, sucursal: 3.2686395414, establecimiento: -1.6728603066, promotor: 0.6311665002, otro: 1.8181379999}
    comparabilidad_2024: "COMPARABLE-CON-DERIVA-DE-EJEMPLOS; 2024 REDONDEADO"
```

## 5. Obligaciones y administración

- `NC-0121` cierra por ejecución: 2021 quedó medido y 2018 quedó
  `NO-ESTIMABLE` con prueba de reactivos, no convertido en cero.
- `NC-0122` permanece ABIERTA como límite estructural: ninguna de las tres
  olas liga el canal al producto fintech específico. D10 ya aceptó el proxy;
  no se solicita otra firma ni se reabre esa decisión.
- El asiento `VERIFY-ESTRUCTURADO` identifica spec, script e inputs en
  `forense/replay-evidencia.tsv`. Las vistas corrida0 se publican por lote
  propio después de integrar el acto publicador; cero transiciones ajenas.
- `cuenta_gen2=SI` por la autorización explícita del encargo para este objeto
  científico nuevo; una medición nueva, no dos por el control ni por 2024.
- No se modificaron `milpa/`, `tools/corrida0.py`, `tools/ya_medido.py` ni la
  configuración del cron. No se adquirió ni se versionó microdato.

## 6. Validación

- `python3 -m unittest tests/test_enif_fintech_serie.py`: 5/5 OK.
- `python3 tools/corrida0.py spec-check CALC-ENIF-FINTECH-0001`: 11 OK, 0
  FAIL.
- `preflight` / `run` / `verify`: VERDE / 0 / REPRODUCE-IDENTICO 131/131.
- Control independiente: `VALIDACION-INDEPENDIENTE-COINCIDE`.
- `python3 tools/corrida0.py registro --lote CALC-ENIF-FINTECH-0001
  --fuentes`: seco estable, 151/3,466/207 filas en
  `corridas/resultados/usos`.
- `python3 tests/check.py --baseline`: línea base VERDE, sin fallos nuevos;
  conserva únicamente los tres `FAIL` históricos T06×2/T08 y 2,757 avisos.
- `tools/cierre_acto.py`: cascada reconciliada a `ADR-466`; rótulo y L0
  presentes, `NC` sin huérfanas.
- `git diff --check` es limpio para los cambios manuales. El diff completo
  conserva el tabulador final que el escritor canónico de `resultados.tsv`
  emite para representar el campo sucesor vacío; la vista seca es byte a byte
  estable y el mismo patrón existe en publicaciones previas de la herramienta.
- PR revisable [#706](https://github.com/Josanoforo/Modelado-Mexicano/pull/706),
  abierto sin fusionar; el merge pertenece a mesa. La sincronización final
  del HEAD remoto se verifica después del commit administrativo de consumo.
