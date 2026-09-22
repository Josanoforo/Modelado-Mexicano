# ENCARGO · ACTO GEN2-VALIDACION-INDEPENDIENTE-LOTE-1 · LAS 44 CELDAS QUE HOY SOSTIENEN LA FRASE DEL PRODUCTO SE RECALCULAN DESDE LA SPEC, SIN LEER EL CÓDIGO

> ENTORNO: **CAJA** (ENIF 2021 y 2024; los 9 cruces ya abiertos del lote). NO es NUBE.
CABECERA · SHA de redacción `bda6b60c`; una sesión, rama `acto/gen2-validacion-independiente-lote-1` · MODO ABIERTO · **INDEPENDENCIA:** no abras `medidor.py`, `adjudicacion.py`, `tools/duelo/cruces_familia.py`, `tools/lote_enif2024/` ni sus tests; si ya los tienes en contexto, PARA · CONTADOR: no sella corridas de programa; produce una validación. **L0 de `canon/estado-programa-v1_14.md`: si choca, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa.** Procedimiento congelado o receta; latitud logística; toda duda de procedimiento se pregunta a mesa en una línea con opciones.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; el CI corre la suite completa. Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main.

## 1 · OBJETIVO
`#986` abrió el lote: 44 celdas primarias, C2 cubre 75 %, R2 88.6 %, ΔMAE 0.48 pp con IC [0.10, 0.72] → `PROPUESTA-CON-RESERVA`. Es la cifra más grande que el producto va a citar, y se reproduce (`REPRODUCE/IDENTICO`), pero reproducir no es validar (E.2). `#970` validó los tres pilotos y las specs bastaron; aquí la spec es más larga y el módulo genérico más nuevo. «Hecho»: R por celda (punto e IC95) y C2 por celda recalculados con código propio desde `DIN-lote-enif2024-spec-v1_0.md`, cuestionarios y descriptores; commit de tus números **antes** de abrir los `resultados.json`; comparación con tolerancia; ΔMAE y coberturas recalculadas; veredicto `COINCIDE` · `COINCIDE-CON-DIFERENCIA-EXPLICADA` · `DISCREPA`; informe en `forense/validaciones/`.

## 2 · FIRMAS — verbatim
E.2 (v2.16): «Tres preguntas que no se colapsan: ¿se reproduce? ¿pasó validación independiente? ¿se adopta?» §4: «la validación independiente recalcula desde la spec humana, el cuestionario y el descriptor, sin leer el código que produjo la cifra, y commitea sus números antes de abrir los sellados». «La validación no re-adjudica: si discrepa, el veredicto sellado no se toca y la discrepancia va a mesa como hallazgo, con su tamaño en pp» (`#970`, sellado por lanzamiento; rige aquí).

## 3 · LO QUE DIRECCIÓN SABE
- `[EXISTE]` spec `forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md` (+ sidecar; enmiendas v0.2/v0.3), `data/ahorro-comparabilidad-texto-v1_0.tsv`, los sellados `CALC-DIN-LOTE-ENIF2024-EMISIONES-0001` y `…-ADJUDICACION-0001` (léelos **después** de P1), los marginales 2024 de `#971` y el C2 sellado (`CALC-C2-COMPUESTO-IC-ENIF2024-0001`). `[LEÍDO: nota de #986]` 43 puntuadas de 44; `localidad × edad` fuera (consumido); formalidad NO-EMITIBLE (24 celdas, solo P2).
- `[LEÍDO: #970]` precedente de forma y de tolerancias: `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/`.

## 4 · YA HECHO
Validaciones de pilotos y de la serie ENVIPE; ninguna del lote. Repítela tú.

## 5 · PIEZAS
**P1 · A ciegas.** Código propio desde la spec: R por celda para los 5 pares primarios (IC por el diseño que la spec declare), C2 desde marginales, R2 = interacción 2021 encogida λ = ½ como la spec la define, ΔMAE con IC por réplica (tu remuestreo, declarado). Commit y push **antes** de abrir sellados.
**P2 · Comparación.** Celda a celda; tolerancia del tipo para puntos; para IC, la tuya declarada.
**P3 · Causas.** Cada diferencia mayor que la tolerancia hasta la línea de la spec que la origina, o `SIN-EXPLICAR`.
**P4 · Lo que cambia para el producto.** Con tus números: ¿0.48 pp, [0.10, 0.72], 75 %, 88.6 % se sostienen, se matizan o se rompen? Una línea. Si la spec no bastó en algún punto, ése es el hallazgo principal.

## 6 · LATITUD · 7 · PAROS
Latitud: lenguaje, método de varianza (declarado). PAROS: a) leer el código de los CALC o del módulo antes de P1 en `origin` · b) abrir `localidad × edad` o cualquier cruce RESERVADA · c) editar un sello o veredicto · d) entorno equivocado. Compuerta: «P1 en origin» protege abrir dato (los sellados). Perímetro: `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-LOTE-v1_0/`, nota, cascada. Fuera, PARA. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
