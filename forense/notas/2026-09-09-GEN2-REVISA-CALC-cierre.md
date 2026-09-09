# `ACTO GEN2-REVISA-CALC` — nota de cierre

**9 de septiembre de 2026 · NUBE, Opus (diseño de runbook + calibración documental) · rama `claude/jolly-darwin-te6yf8` · base `main = 95ef598` (`PR #652` fusionado)**

Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-09-GEN2-REVISA-CALC.md`.
Compuerta `PR #652 fusionado`: **CUMPLIDA**, verificada por producto — `git merge-base --is-ancestor 95ef598 origin/main` confirma que nuestro `HEAD` es exactamente el commit de merge del `PR #652` (`Merge pull request #652 from Josanoforo/acto/gen2-obra-v11`).

**`CONTADOR: cero`, declarado.** Este acto no mide nada sobre México — diseña un bloque de revisión de infraestructura de proceso y transporta dos documentos. No hay firma de contador que traer.

---

## 0 · Qué hace este acto, en una línea por pieza

- **P0(a)** — archiva verbatim la propuesta final de Astra en `forense/notas/2026-09-09-PROPUESTA-FINAL-AUTOMATIZACIONES-POSTCALCULOS-astra.md`, con cabecera de procedencia.
- **P0(b)** — archiva verbatim la revisión adversarial del PR #649 en `forense/notas/2026-09-09-REVISION-ADVERSARIAL-PR649-astra.md`, con cabecera de procedencia + advertencia de no-reapertura + sha256 re-derivado.
- **P0(c)** — cierra `NC-0082` (transporte de fuente que faltó) citando ambos archivos, el hash, y este acto.
- **P1** — añade el bloque `## 2-bis · REVISA-CALC` a `.claude/commands/revisa.md`, dentro del mismo informe/comentario único del revisor vigente.
- **P2** — esta sección, calibración documental contra cuatro casos históricos (abajo).

## 1 · P0 — verificación del transporte

Hash re-derivado en esta sesión, contra el adjunto tal como llegó:

```
$ sha256sum REVISION-ADVERSARIAL-PR649.md
ccd2219a5522a00db60feebb81eda6353bb9b1153dd4931c2c8df2c2212139fd  REVISION-ADVERSARIAL-PR649.md
```

MATCH exacto con el sha256 declarado en el encargo y en el pie de la propuesta de Astra (Anexo B). Verificación adicional de que los bytes archivados en `forense/notas/2026-09-09-REVISION-ADVERSARIAL-PR649-astra.md` son idénticos, byte a byte, al cuerpo del documento original (excluyendo solo la cabecera de procedencia que este acto antepone):

```
$ tail -n +14 forense/notas/2026-09-09-REVISION-ADVERSARIAL-PR649-astra.md | sha256sum
ccd2219a5522a00db60feebb81eda6353bb9b1153dd4931c2c8df2c2212139fd  -
```

Coincide exactamente. `NC-0082` cierra con esta evidencia — el hueco que declaraba («el texto verbatim de la revisión NO llegó») queda resuelto: el texto llegó como adjunto de esta sesión, se verificó su hash contra el declarado, y se archivó sin editar.

## 2 · P2 — calibración documental, cuatro casos históricos

El bloque `## 2-bis · REVISA-CALC` (P1) no es una receta abstracta: se calibró releyendo cuatro episodios que el programa ya vivió, para que quien lo aplique tenga vara de qué "afirmación material falsa" y "sucesión reconocida sin reescritura" significan en la práctica de este repo. Ningún replay de CAJA se ejecutó para esta calibración — es lectura de historial ya fusionado, con los comandos de existencia (A.13) de abajo.

### #634 / #644 — semántica de verificación

```
$ git log --oneline --all | grep -iE "634|644" | head -5
```

Los PR #634 y #644 fijan la distinción que el bloque `REVISA-CALC` hereda en su fila "Replay" de la tabla de comprobaciones: un `verify` que **corroboró** activamente un resultado (leyó los bytes, ejecutó `medir`, comparó) no es lo mismo que un `verify` que simplemente **no encontró motivo para objetar** (contexto no verificable, biblioteca ausente). Colapsar ambos en "verde" es el defecto que ese par de actos corrigió y que el bloque nuevo hereda como los "seis estados de fallo que no se confunden".

### #647 — adopción con delta al grano

```
$ git log --oneline --all | grep -i "647"
```

`PR #647` es el precedente citado en la propia propuesta de Astra (§4, "Caso positivo #647"): un cambio de representación entre `0.045694` y `0.04569409956405095` es igual al grano publicado de seis decimales — equivalencia de representación, no mejora del modelo. La fila "Adopción" del bloque `REVISA-CALC` hereda exactamente esta distinción: "compatibilidad del estimando con el parámetro; una nota no es una ranura de p".

### #649 → #651 — el negativo y el positivo de la misma cadena

```
$ git log origin/main --oneline | grep -E "#649|#651"
```

Éste es el caso que más pesa en el bloque nuevo, porque es el ÚNICO de los cuatro donde la reproducción mecánica *pasó por completo* y aun así hubo un defecto que corregir:

- **#649 (negativo).** La revisión adversarial de Astra (archivada íntegra por P0(b) de este mismo acto) reprodujo **152 de 152 resultados exactamente** verificando los 260 sha-256 de los insumos declarados por `CALC-C0D-MARCADOR-v2`, y aun así encontró que la adjudicación de la comparación pareada (`NO-DISCRIMINA` → `EXPLICADO-POR-METRICA`) convertía una incertidumbre no resuelta (IC95 que cruza cero) en una explicación que los datos no demostraban. **La reproducción no validó la inferencia** — la validó, y por separado, hubo que corregir qué conclusión permitía esa evidencia. Es exactamente la distinción que el bloque `REVISA-CALC` escribe en su fila "Inferencia": *"¿la conclusión excede al intervalo, al universo o al diseño?"*
- **#651 (positivo, correctivo).** `ACTO GEN2-C0-D-CORRECTIVO` reconoció la sucesora correcta (`CALC-C0D-MARCADOR-v3`) sin pedir que se reescribiera la historia de `v2`: los sellos de `v1.0`, `v1.1`, `CALC-C0D-MARCADOR` y `CALC-C0D-MARCADOR-v2` quedan **intactos** (verificado en `NC-0081`, cerrada por el mismo acto), y el destino de la adjudicación pasa de `EXPLICADO-POR-METRICA` a `INCONCLUSO` con una spec sucesora (v1.2 §5) que deriva la adjudicación **solo** del veredicto de la pareada — sin veto de universo y sin un `else` mudo que colapsara `CORPUS-AYUDA` con la misma etiqueta neutra que `NO-DISCRIMINA`. Dos `RESULT` de destino cambiaron; nada del historial de `v2` se tocó.

Este es el caso que el bloque nuevo cita textualmente en su sección de calibración: *"#649 pasó la reproducción, 152/152 resultados exactos, y aun así necesitó corrección"* — no se exige que la máquina descubra sola el problema estadístico; se exige que la fila humana "Inferencia" de la tabla lo haga visible cuando aplique.

### Pasa cuando (los tres criterios de aceptación del encargo, verificados contra estos cuatro casos)

1. **Detecta una afirmación material falsa aunque la reproducción numérica sea exacta** — cubierto por #649: 152/152 exacto, adjudicación falsa igual.
2. **Reconoce la sucesora correcta sin pedir reescritura histórica** — cubierto por #651: sellos de `v2` intactos, sucesión declarada y cubierta.
3. **Conserva una reserva de entorno declarada sin inventar divergencia** — cubierto por la distinción #634/#644 heredada en los seis estados de fallo, que el bloque nuevo aplica explícitamente a cualquier `NO-VERIFICADO` de CAJA.

La calibración documental de esta sección **no se rotula como replay de CAJA**: ningún comando de esta nota abrió microdato ni ejecutó `medir` de nuevo — son lecturas de PR ya fusionados, con `git log`/`grep` como evidencia de existencia (A.13).

## 3 · Lo que este acto explícitamente no hace

Conforme al encargo, este acto **no** implementa `lote`, `delta`, `vigencia` ni `siguiente` (quedan como contratos archivados en la propuesta de Astra, backlog citable), **no** añade ejecución de CAJA a NUBE, **no** crea segundo comentario/revisor paralelo/script nuevo/rutina programada, **no** reabre el #649 (el documento histórico entra como fuente archivada, con advertencia explícita de no-reapertura en su propia cabecera), y **no** toca los sellos de ningún CALC.

## 4 · Excepciones de test documentadas (T03/T22)

Este acto añade tres nombres a `HISTORICOS` de `tests/check.py::t03_dangling_refs` (`revisa.md` — mismo defecto de cobertura del glob oculto ya documentado para `tramite.md`; `REVISION-ADVERSARIAL-PR649.md` — mismo patrón que `PROPUESTA-GOBIERNO-DECISIONES-PENDIENTES.md`: el nombre que el propio documento de Astra se dio, contra el basename con convención de fecha que el repo usa al archivarlo) y una entrada a `_T22_ARCHIVOS_CONOCIDOS` para el propio encargo (`forense/encargos/2026-09-09-GEN2-REVISA-CALC.md`, que menciona el nombre de archivo a archivar en la misma línea donde cita "regla de mesa 4" — mención del nombre, no una decisión nueva esperando firma). `tests/check.py --baseline` corre en VERDE tras estas tres exenciones, cada una con su comentario in situ citando el precedente exacto que sigue.
