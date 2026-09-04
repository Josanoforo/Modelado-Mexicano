SHA de redacción: `68a3466` (#257, `origin/main`)
Entorno asignado: NUBE, repo-only. NO lo lances en Ubuntu — este acto no abre microdato ni corre red; toca solo `canon/`, `milpa/procedencia.yaml` (cabecera), `forense/`.
Estado: CONSUMIDO — rama `claude/sella-rutas-ajustado-metodologia-023jkq`, commit del sello (`ADR-102`, C2) + commit de cierre (C3: cascada, nota, hallazgos, este archivo). Sin PR abierto en esta sesión — nadie lo pidió; la rama queda lista para que mesa lo abra.

Texto completo del encargo, tal como se lanzó (sin resumir):

---

ENCARGO · SELLA-RUTAS — la metodología que "calcular" va a exigir deja de ser propuesta

SHA de redacción: `68a3466` (#257, `origin/main`) · Entorno: NUBE, repo-only · Estado: VIVO Gate: ninguno — lanzable ya, en paralelo con lo que sea (sus archivos no chocan con ningún carril vivo; la colisión de número de ADR es esperada y tiene protocolo). 🚫 Sin `--freeze`.

**Por qué este acto, con el hueco medido**

`ADR-49 (D2)` selló la clase `AJUSTADO` — reproduce momentos observados, NO identifica causalmente, contesta CUÁNTO nunca SI — y la dejó vacía a propósito. Pero el cómo ejecutarla vive en `forense/metodologia-identificacion-vs-ajuste-v0_1.md`, cuyo propio encabezado dice "31/jul/2026 · propuesta metodológica, sin sellar. No es canon." (`:50`), y cuyo §8 declara "No sella la clase AJUSTADO". Estado real de las magnitudes del modelo: 60 `ORDINAL→CARDINAL` + 74 `ASIGNADO` de 144 — juicio, no medición. El plan del programa es reemplazarlas por `MEDIDO` (fichas) y `AJUSTADO` (rutas); sin sellar el cómo, ningún acto puede poblar un `AJUSTADO` sin violar ADR-47. Este acto le pone la firma al tabulador para que se pueda pagar con él.

════ ARRANQUE ════ (idéntico al de CONF-07-CIERRE, puntos 1-5: clon no-superficial con `main` local actualizada · SHA contra `68a3466` · data/raw no se usa · firma A.2 de tres partes, nunca `curl -I` · toda cifra del clon.)

**VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe, contra `68a3466`**

```
la metodología:          forense/metodologia-identificacion-vs-ajuste-v0_1.md      EXISTE-SATISFACE
  §4 "Las cinco rutas" (:114) · §5 costo (:134) · §6 "La clase que falta" (:148) · §8 límites (:176)
rótulo sin canon:        :50 "propuesta metodológica, sin sellar. No es canon."    EXISTE-NO-SATISFACE (el sello)
clase ya sellada:        procedencia.yaml cabecera — "Sellada por ADR-49 (D2): nace VACÍA,
                         cero números AJUSTADO hoy" + campo `ruta:` obligatorio     EXISTE-SATISFACE
consumidores del sello:  procedencia.yaml cabecera cita "rutas argumentadas (propuesta sin
                         sello…) §4" — es el puntero que este acto vuelve firme     EXISTE-NO-SATISFACE
```

**PERÍMETRO**

`forense/metodologia-identificacion-vs-ajuste-v0_1.md` (solo rótulos de estado — `:50`, §8, encabezado a v1.0-SELLADA; ni una línea de contenido metodológico) · `milpa/procedencia.yaml` (solo el comentario de cabecera que cita la propuesta: pasa a citar el ADR) · `canon/gobernanza-v1_15.md` (ADR) · `canon/estado-programa-v1_10.md` cascada `:27`/`:101` (⚠️ FP-48) · `forense/notas/` · `hallazgos.md` (append) · `forense/encargos/`. NO toca ningún número de `procedencia.yaml`, ningún parámetro, ninguna ficha. Fuera de lista: PARA.

**C1 · La lectura de mesa — el acto ES este prompt**

Prepara para mesa un resumen fiel de §2 a §6 (una pantalla: qué es identificar vs. ajustar, las cinco rutas con la condición dura de cada una — incluida la regla de `composicion`: descomposición DECLARADA ANTES de ver los datos — y el costo del §5 sin suavizarlo). `AskUserQuestion` con opciones: (a) "sello las cinco rutas tal como están escritas" · (b) "sello con esta corrección: [texto]" · (c) "no se sella; razón: [texto]". Nada se escribe sin la respuesta. Si (b), la corrección de mesa entra verbatim como enmienda fechada del documento, nunca como reescritura silenciosa.

**C2 · El sello (solo con respuesta (a) o (b))**

ADR que canoniza la metodología (cita `ADR-49` como el sello de la clase y este como el del procedimiento; deja explícito que sellar el cómo no puebla nada: cada `AJUSTADO` futuro exige su propio acto con `ruta:` declarada y, para `composicion`, la regla pre-declarada). Rótulos del documento actualizados (`v1.0 — SELLADA`, `:50` reescrita con la fecha y el ADR, §8 gana la línea "la clase quedó operable por ADR-⟨n⟩"). Cabecera de `procedencia.yaml`: el paréntesis "(propuesta sin sello…)" pasa a citar el ADR. Falsador del sello, en el ADR (v2.3): si en tres meses ningún `AJUSTADO` se puebla por una ruta sellada, el sello no dañó nada pero se anota como capacidad ociosa; si alguno se puebla sin ruta declarada, T-alguno debe cazarlo — di cuál test lo vigila hoy o declara que ninguno, sin instrumentar aquí.

**C3 · Cierre**

ADR re-derivado dos veces · cascada · nota con el resumen presentado y la respuesta verbatim · `hallazgos.md` · encargo `CONSUMIDO`. Auditoría: contadores sobre México: cero. Lo que mueve: la fase de cálculo gana su instrumento legal — 134 de 144 magnitudes tienen, por primera vez, una vía sellada de reemplazo. Ninguna cifra tecleada. Si mesa responde (c), el acto cierra igual: la negativa fechada también es entregable, y la fila correspondiente queda abierta con la razón. NO hace: no puebla ningún `AJUSTADO` · no reclasifica ningún `ASIGNADO` · no toca fichas ni el pre-registro.

---

**Resultado de la ejecución.** Mesa respondió (a) — verbatim: *"Sello tal como están escritas."* — vía `AskUserQuestion`, sobre el resumen de §2-§6 presentado en el chat de este acto (reproducido íntegro en `forense/notas/2026-08-18-sella-rutas.md` §2). `ADR-102` sella §2/§4/§5 de `forense/metodologia-identificacion-vs-ajuste-v0_1.md` como procedimiento de la clase `AJUSTADO` (`ADR-49`, D2, sigue siendo el sello de la clase). Cascada, nota y `hallazgos.md` completos — ver `forense/notas/2026-08-18-sella-rutas.md` para el detalle comando por comando, incluido el defecto de cascada a medias que `T15`/`T16` atraparon y este mismo acto corrigió antes de cerrar.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-18-SELLA-RUTAS-ajustado-metodologia.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-18-consolida-2-fp38-propagaciones.md, forense/notas/2026-08-18-sella-rutas.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
