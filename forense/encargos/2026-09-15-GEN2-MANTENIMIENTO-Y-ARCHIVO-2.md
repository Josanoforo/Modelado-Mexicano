# ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2

> Archivado por A.3 (0-bis) — texto **verbatim** del mensaje de dirección que
> lanzó este acto, 15/sep/2026. No se edita en ningún otro punto salvo las
> secciones `## NO-CORRIDO / RESERVAS` y `**Enmienda fechada al integrar `origin/main` en el cierre (15/sep/2026, mismo acto).**
Mientras este acto corría, `main` avanzó de `0cdbd72` a `ce79136` y dos de las
siete filas de arriba cambiaron de estado. Se declara en vez de reescribirlas:

- **Fila 1 — la hoja de firmas 2 SÍ existía, por otra vía.** `PR #792` (commits
  `def4176` «Registrar Hoja de firmas 2 (F-1..F-16)» y `56ee620` «Propaga Hoja de
  firmas de mesa 2») la registró y la propagó, y se fusionó a `main` mientras esta
  sesión trabajaba. **Lo que la fila dice sigue siendo cierto de esta sesión:** la
  hoja no viajó en el mensaje que lanzó este acto, y por eso no se infirió. La fila
  se asienta como `NC-0226` y se **cierra en el acto** con `SUSTITUIDO-POR` el acto
  de `PR #792`, que la absorbe íntegra — la secuencia queda auditable en vez de
  desaparecer. **Lo que el sustituto NO absorbe:** `NC-0210`. Verificado contra el
  árbol nuevo: `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-2.md` **no menciona**
  `NC-0210` ni la cifra `0.668937` (0 coincidencias), así que la fila 2 de arriba
  **se mantiene tal cual** y esa deuda de milpa sigue sin autorizar.
- **Fila 3 — `NC-0219` ya está CERRADA.** `ACTO GEN2-ARCHIVO-LECTURA-F5-1`
  (`PR #794`) recibió de mesa los textos y los commiteó verbatim con cabecera de
  procedencia y `sha256` re-derivado. **Lo que la fila dice sigue siendo cierto de
  esta sesión:** los adjuntos no llegaron aquí, y no se reconstruyeron. La fila
  cerrada de `origin` se conserva **intacta**; este acto no la re-anota. Su residuo
  (un tercer texto aún pendiente) vive en la `NC-0225` de ese acto, que no es de
  este.

Renumeración por la regla de la casa (**renumera quien fusiona segundo**): las
cuatro filas nuevas de este acto pasan de `NC-0225..0228` a **`NC-0226..0229`**,
porque `PR #794` tomó `NC-0225` primero. `ADR-517` **no** colisiona: el máximo real
en `origin/main` es `516`.

## CONSUMIDO` que la cascada añade al
> final (pasos 10 y 11 de `/acto`).

---

NUBE · ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2 (Sonnet; un solo acto para todo lo mecánico, y propaga la hoja de firmas 2)

* Registro/herramientas: NC-0199 (lectura de `repite_de` en corrida0.py), NC-0191 (T16 self-check timeout: evaluar `tests/check.py:773-826`), NC-0212 (declarar el enlace de `CALC-ENIF-0002`), NC-0213 (id de corrida natural en `demanda_que_releva`, sucesión), NC-0174 (curación de demanda con permiso sobre `data/curacion-registro/`).
* Documentos/sellos: NC-0170 (retro-sello `## CONSUMIDO` a los 8 encargos listados), NC-0176 (`acto.md` → estado-programa v1_13), NC-0050 (propagar texto a las líneas 45/58 del ENCARGO maestro), NC-0209 (`diseno-muestral.yaml` por append; S6-L16), NC-0210 (reconciliar la cifra de `tramite-ola5-propuesta`), NC-0218 (incorporar el sello de D-A al informe; §A.3 re-sellada).
* NC-0219 · archivo verbatim de los dos documentos de mesa sobre los que la firma del 15/sep se pronuncia — viajan adjuntos: `ADVERSARIAL-ASTRA-1-LECTURA-F5-2026-09-15.md` (sha `1de3c74203f8…`) y el segundo texto de Astra (mesa lo pega; la cabecera de procedencia ya está en `ASTRA-RECOMENDACIONES-2-…`), más `LECTURA-ESTRATEGICA-F5-v1_1` (sha `a51daa0976e7…`). Si un adjunto no viaja, esa pieza PARA.
* Propaga la hoja de firmas 2 (abajo) en `decisiones.tsv` y cierra sus NC. Perímetro: tools/, docs, notas, no-corrido, decisiones; milpa solo donde una firma lo autorice.

## NO-CORRIDO / RESERVAS

Siete filas. La primera gobierna a la segunda.

| # | qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|---|
| 1 | «Propaga la hoja de firmas 2 (**abajo**) en `decisiones.tsv` y cierra sus NC» | `PARO-PREMISA` | **La hoja no viajó: abajo no hay nada.** La línea del perímetro es la última del mensaje — el texto archivado verbatim arriba es la prueba, no una interpretación. `data/corrida0/decisiones.tsv` no gana ninguna fila y ningún contador se mueve. No se infiere una firma: escribir en `decisiones.tsv` una autorización que nadie envió sería fabricar autoridad. Contraste verificable: la hoja de firmas **1** sí existe (`forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`, «Si a todas.») y de ella se verificaron FP-371/FP-372 para cerrar NC-0209 aquí mismo. | `NC-0226` — mesa/dirección pega la hoja 2; un acto de trámite la propaga |
| 2 | `NC-0210` (reconciliar la cifra de `tramite-ola5-propuesta`) | `DECISIÓN-DE-MESA-PENDIENTE` | Cae con la fila 1 por la propia regla del encargo — «milpa **solo donde una firma lo autorice**». Verificado que la hoja 1 **no** la autoriza: su tabla declara que la cifra `0.668937` «no es una» de las cuatro glosas autorizadas. La cifra sigue sin reproducir a 6 decimales. | `NC-0210` (sigue ABIERTA) · gatea la hoja 2 |
| 3 | `NC-0219` · archivo verbatim de los dos documentos de mesa | `PARO-PREMISA` | **Los adjuntos no viajaron** — y la cláusula del propio encargo manda: «Si un adjunto no viaja, esa pieza PARA». Re-verificado (A.13): `find . -name 'ADVERSARIAL-ASTRA-1*'` = 0; `grep -rl "LECTURA ESTRAT" canon/ forense/` = 7 sobre 3 694 archivos, y las 7 son **referencias** al documento, no el documento. No se parafrasea un verbatim que no se tiene. | `NC-0219` (sigue ABIERTA) |
| 4 | `NC-0212` (enlace de `CALC-ENIF-0002`) y `NC-0213` (id de corrida natural, **sucesión**) | `FUERA-DE-PERÍMETRO` | Las dos exigen tocar una **spec sellada** o abrir su sucesora, y `E.3` lo prohíbe: el perímetro de este acto es `tools/`, docs, notas, `no-corrido`, `decisiones` — no `data/corrida0/*/spec.yaml`. Una sucesión además no se sella sin CAJA (esta sesión es NUBE, `corpus=NO`, 0 archivos examinados). La adopción de RES-0065 sigue rotulada `control_c0=NO-DERIVABLE-DESDE-LA-SPEC` y la etiqueta de `CALC-ENVIPE-0001` sigue citando CORR-0009 donde el dato dice CORR-0007. Ninguna cifra cambia. | `NC-0212`/`NC-0213` (siguen ABIERTAS) — el acto que suceda a esas specs, en caja |
| 5 | `NC-0174` (curación de demanda con permiso sobre `data/curacion-registro/`) | `FUERA-DE-PERÍMETRO` | El permiso que la fila nombra es exactamente el que este encargo **no** concede: toca `data/curacion-registro/` y `milpa/demanda`, y la regla de milpa exige firma. Los enlaces demanda↔ficha Banxico/MOTRAL/SHED no se crean ni se verifican. | `NC-0174` (sigue ABIERTA) |
| 6 | `NC-0218` (incorporar el sello de D-A; §A.3 re-sellada) | `DIFERIDO-A: ACTO D-A` | **No hay sello que incorporar.** D-A re-verificado AUSENTE con universo declarado (A.13): 0 coincidencias sobre 4 ramas remotas y 0 sobre 562 encargos. La fila decía «sin esperarlo», y no se esperó: se midió. §A.3 del ANEXO sigue correctamente como DERIVACIÓN PROPIA con control positivo, no como el sello. Ningún contador se mueve. | `ACTO D-A` (`NC-0218` sigue ABIERTA) |
| 7 | `NC-0170` (retro-sello a «los 8 encargos listados») — **parcial, 2 de 8** | `DECISIÓN-DE-MESA-PENDIENTE` (el residuo) | La lista de 8 quedó vieja y se **re-derivó** PR por PR: 2 ya los había sellado `GEN2-CONSUMIDO-RETRO-3` (#739, y #737 como PR #742); **2 se retro-sellaron aquí** (#680, #701); y **4 no son retro-sellables** — #682, #719, #726, #728 **no tienen encargo archivado** (0 coincidencias de su rótulo sobre 497), así que lo que falta no es la sección sino el archivo `A.3` mismo, que no se rellena hacia atrás sin el texto original. #728 es además un PR de *preparación* cuyo encargo sigue legítimamente en cola: sellarlo sería falso. La segunda mitad de la fila (¿`[COLA]`/`[ADQ]` como cuarta categoría exenta?) sigue sin decidir. | `NC-0227` — mesa elige entre huérfanos aceptados o ficha de procedencia |

**Reserva sin fila propia.** `NC-0199` se cierra, pero su *efecto* en las vistas
derivadas no se publica aquí: exige `registro --escribe` con corpus montado y
esta sesión es NUBE sin `data/raw`. Reasentado en `NC-0228`, que conviene que
absorba también `NC-0145`, que PARA por la misma causa. El arreglo del lector
viaja igual y ningún número de este acto depende de esa escritura.

**Hallazgo que corrige una fila, no la absorbe.** `NC-0199` declaraba su impacto
«cosmético, no numérico». Medido aquí: es más ancho (6 de 104 specs, no 1) y más
grave — sin el arreglo, una sucesora que repita ids de RESULT hace **PARAR** a
`registro` con `ID-DUPLICADO`, verificado por reversión del parche. En el árbol
real no ocurría sólo porque las 6 sucesoras renombraron sus RESULT.

## CONSUMIDO · PR #795

Ejecutado por `ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2` (`ADR-517`), 15/sep/2026,
NUBE Sonnet, **contador cero**. Cierra por producto `NC-0050`, `NC-0176`,
`NC-0191`, `NC-0199` y `NC-0209`; deja anotadas con medición nueva `NC-0170`,
`NC-0218` y `NC-0219`; abre `NC-0226`, `NC-0227`, `NC-0228` y `NC-0229`.

**Lo que este acto NO hizo, y por qué está arriba y no escondido aquí:** la
**hoja de firmas 2 no viajó** — el mensaje termina en la línea del perímetro, y
el texto verbatim de este mismo archivo es la prueba —, así que
`data/corrida0/decisiones.tsv` **no gana ninguna fila** y `NC-0210` cae con ella.
Los adjuntos de `NC-0219` tampoco llegaron y su propia cláusula manda PARAR.
Ninguna de las dos se rodeó: una firma de mesa no se infiere y un verbatim no se
reconstruye de paráfrasis.

`tests/check.py --baseline`: `3 FAIL · 4350 WARN`, **LÍNEA BASE VERDE** — los 3
FAIL son los congelados (`T06`×2, `T08`×1), ninguna entrada nueva. `T16` corrió
en 166 s sin topar el límite que este mismo acto subió. El ejecutor no fusiona el
PR: esa decisión es de mesa.
