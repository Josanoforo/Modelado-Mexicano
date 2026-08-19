# ENCARGO · SELLO-FICHA-G3 (v2) — la decisión del primer coeficiente

**SHA de redacción:** `57984b5` (`origin/main`, declarado por el propio encargo en su cabecera) · **Entorno asignado:** NUBE · **Modelo:** Opus
**Estado:** CONSUMIDO — ejecutado por `ACTO SELLO-FICHA-G3-V2`, 19/ago/2026, este PR. `ADR-107` sella el diseño de `ficha-id-g3-v1_0.md` y adjudica la fila `ID-X` que `ENCARGO CORRIDA-IDG3` (5/ago/2026) había dejado propuesta sin adjudicar; `FP-11` → `FIRMADA`. No se escribió `EXEC-FICHA-G3` como corrida nueva — la ejecución ya había corrido con microdato real, dos semanas antes de que este encargo llegara a poder ejecutarse. Detalle completo: `forense/notas/2026-08-19-sello-ficha-g3-v2-adjudica-idx.md`.

Archivado por `A.3` (*"un encargo que solo existe en la salida de una conversación es invisible para el programa"*) en el mismo acto que lo ejecuta y lo cierra, no antes: el encargo llegó por conversación, sin archivo previo en `forense/encargos/`, y este documento es su registro verbatim.

---

## Texto del encargo, verbatim

Gate: `LANE-A-E0-E5` fusionado y `FP-15` cerrada — verifícalo con las cuatro señales del acta precedente. Delta v1→v2: el intento bloqueado ya dejó acta en main (#262: `forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md`) — cítala como precedente y no la reescribas; ADR base 104; si tu verificación de gate vuelve a fallar, repite exactamente su conducta (PARA + pregunta a mesa) y añade solo una línea fechada a esa misma acta.

**ARRANQUE:** los 5 estándar (clon sano, SHA re-derivado, sin `data/raw`, firma A.2, cifras con comando).

**VERIFICACIÓN (re-córrela):**

```
gate: FP-15 cerrada en tablero · milpa/src/ existe · Entrada 5 con veredicto en registro-recalculo
      · encargo LANE-A marcado CONSUMIDO con su PR                       → las 4 o PARA
la ficha: forense/ficha-id-g3-v1_0.md — RUTA-I · MxFLS olas 2-3 · AFORE · criterio en RR ·
      Paso 0 (contaminación confesada) · hereda D-10 (2005-2012)          EXISTE-SATISFACE
verificación independiente: notas 2026-08-05-s-idg3 §2(1),(3)             EXISTE-SATISFACE
payloads MxFLS en corpus: derívalo del manifiesto/censo — si faltan, EXEC nace gateado a adquisición y LO DICES
```

**PERÍMETRO:** `gobernanza` (ADR) · `ficha-id-g3` (solo bloque de estado → SELLADA, fecha, ADR) · tablero (`FP-11`) · `estado-programa` cascada (post-split: derívala) · notas · `hallazgos.md` · `forense/encargos/` (EXEC, VIVO). Fuera: PARA. 🚫 Sin `--freeze`.

**C1 · El prompt — resumen fiel, sin vender.** Una pantalla: qué estima · por qué RR · la contaminación del Paso 0 tal cual · la ventana D-10 y su no-extrapolabilidad · qué significa cada desenlace (ya declarado, B-bis). Opciones: (a) sello tal cual · (b) sello con corrección:[texto, entra verbatim como enmienda fechada] · (c) no se sella:[razón]. Nada sin respuesta.

**C2 · El sello (con (a)/(b)).** ADR: sella el diseño; declara que la ejecución es acto propio con microdato y que `0 de 15` se mueve allí, no aquí; la estampa A.10 del futuro coeficiente nace acotada 2005-2012. `FP-11` → FIRMADA (`firmada_en`=respuesta verbatim; `ejecutada_en` vacío, dicho).

**C3 · EXEC-FICHA-G3, escrito VIVO (no lanzado).** Ubuntu · gate: caja libre + payloads verificados. La ficha es la ley: COMMIT A congela lo ya congelado (re-derivar cortes = re-diseñar tras ver Fase C: prohibido) · COMMIT B corre y reporta en RR con IC · reglas A-bis 1-4 · desenlace leído contra lo pre-declarado · IC que no despeja = propuesta con reserva, no adjudicación · `procedencia.yaml` gana su primera entrada en escala del modelo solo si el criterio se cumple — y ahí, solo ahí, `0 de 15 → 1`, con estampa acotada.

**C4 · Cierre.** ADR ×2 · cascada · nota con prompt y respuesta verbatim · `hallazgos.md` · `CONSUMIDO`. Auditoría: México: cero aquí (el movimiento vive en EXEC — dilo). Peligro de simplificación: "el primer coeficiente" ≠ "el modelo ya calcula" — un parámetro, acotado, de 15; escríbelo.

---

## Desviación declarada de C2/C3, verificada contra el árbol antes de escribir nada

`C2`/`C3`, tal como el encargo los redactó, asumen que la ejecución (`EXEC-FICHA-G3`) no ha corrido — `C2` dice *"la ejecución es acto propio con microdato"* (futuro) y `C3` la describe *"escrito VIVO (no lanzado)"*. Verificado contra `milpa/procedencia.yaml:1005-1041` antes de redactar el ADR: esa premisa es falsa. `ENCARGO CORRIDA-IDG3` (5/ago/2026, `forense/notas/2026-08-05-corrida-idg3.md`) ya abrió microdato real y propuso la fila `ID-X` (compuerta inalcanzable), sin adjudicar. Este hallazgo se llevó a mesa en una segunda pregunta estructurada, separada de C1 — ver `forense/notas/2026-08-19-sello-ficha-g3-v2-adjudica-idx.md` §2 — y mesa decidió adjudicar en el mismo acto que sella el diseño, en vez de escribir `EXEC-FICHA-G3` como corrida nueva. `C2` se ejecuta con esa corrección: la ejecución no es "acto propio" a futuro, es un acto ya ocurrido, adjudicado aquí; `ejecutada_en` de `FP-11` no queda vacío, como C2 preveía, sino que cita `CORRIDA-IDG3` y este ADR — la fidelidad al hecho verificado pesa más que la instrucción literal escrita bajo una premisa que el árbol real desmiente, mismo criterio que el acto precedente (#262) ya aplicó al gate.
