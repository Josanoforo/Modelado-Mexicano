# ENCARGO · FP29-RECONCILIA (v2) — el 22% se adjudica con la espec que ya existe

> **Archivado bajo A.3 por el propio acto que lo ejecuta** (ACTO FP29-RECONCILIA, 18/ago/2026).
> Texto verbatim del encargo tal como se lanzó. **Estado: CONSUMIDO** — ver cierre al pie.
> **Nota de desfase, registrada al archivar:** el encargo declara `SHA: 57984b5`; al abrir la
> sesión `origin/main` ya estaba en `f3d3f95` (8 commits después) y volvió a moverse a
> `e563e5d` durante el arranque. El acto se ejecutó contra `e563e5d`. Igualmente, "ADR base
> 104" quedó desfasado: el máximo sellado en `e563e5d` es **109**, sin huecos.

---

SHA: 57984b5 · Entorno: UBUNTU (corpus + red a fuentes) · Modelo: Opus · Estado: VIVO · Gate: caja libre (tras REFIRMA-OPACA en el orden vigente). El gate técnico (#260) ya está cumplido. Delta v1→v2: ADR base 104 · cascada post-split derivada (no asumas :101) · el hallazgo A.8 se mantiene: WVS y Latinobarómetro YA en manifiesto (12/ago) — el manifiesto manda sobre la cola vieja; solo Pew se sondea. 🚫 Sin --freeze · descargas fuera del namespace; apertura bajo unshare -Urn.

════ ARRANQUE ════ los 5 estándar de caja (worktree, SHA re-derivado, corpus montado con manifiesto como fuente-de-qué-hay, firma A.2, cifras con comando).

VERIFICACIÓN (re-córrela)
LA LEY: notas 2026-08-04-c06a §5 (qué calcular, sin calcular) · §6 (cuáles NO salen de ENCUCI)
        · §7 (qué desbloquea en R8.3) · §8 (límite)                              SATISFACE
ESTÁNDAR: benchmark-enlace-invarianza + ADR-76(d)(4)/ADR-80 "argumento de
        vinculación declarado" (ENCUCI 0-10 ≥8 ↔ binarios)                       SATISFACE
SERIES: WVS ✅ manifiesto · Latinobarómetro ✅ manifiesto · Pew ✗ (0)             PARCIAL
FILA: FP-29 ABIERTA con el método ya cableado (ADR-101)                          SATISFACE
RESERVA INTOCABLE: reconciliar conf.06 NO da falsador a R8.3 (marca C3)          SATISFACE
PERÍMETRO

data/manifiesto.yaml (altas de Pew si se obtiene; doble hash A.7 si trae token) · data_raw (⚠️ PR #77: payload al corpus compartido, verificado al cerrar) · notas (ficha y corrida) · gobernanza (ADR) · cascada derivada · tablero (FP-29) · hallazgos · encargos. Canon sustantivo NO — la propagación a las celdas que citan 16-26% es acto sucesor; deja su cola derivada en la nota. Fuera: PARA.

C1 · Pew — A.5/A.6, sin conocimiento previo

N intentos con salida cruda; desenlaces: obtenido-y-alta · "NO OBTENIDO POR ESTE AGENTE EN N INTENTOS" + receta manual <1 min · NO-ACCESIBLE (pago/afiliación; registro gratis no cuenta). La espec §5-§6 decide si 2 de 3 fuentes bastan o el veredicto queda acotado-con-Pew-pendiente — no tú.

C2 · Reconciliación — la espec como ley

Series abiertas (ENCUCI ya barrida por v7) → argumento de vinculación por par según ADR-80 (escala, corte, población, año; jamás promediar entre escalas) → por cada una de las cinco cifras: el veredicto que §5 especifica, con escala y denominador; discrepancias reportadas como discrepancias. B-bis antes de calcular: converge→rango adjudicado · diverge→rango con divergencia nombrada · insuficiente→INDECIDIBLE con qué faltó.

C3 · Cierre

Ficha de adjudicación en notas (tabla completa) · FP-29→FIRMADA/ejecutada · ADR con la reserva C3 repetida verbatim · cascada · hallazgos · CONSUMIDO · en la nota: cola derivada de celdas que citan 22%/16-26% (para el sucesor). Auditoría: este acto SÍ mide México — di qué mueve (magnitud de constructo) y qué no (coeficientes). Sesgo de marcos: WVS/Latinobarómetro/Pew son (c) — la vinculación declarada existe para eso; dilo en la ficha.

---

## CONSUMIDO

**Ejecutado por `ACTO FP29-RECONCILIA`, 18/ago/2026, sellado por `ADR-111`.** Base real `e563e5d` (no `57984b5`). Nota del acto: `forense/notas/2026-08-18-fp29-adjudicacion.md`. Corrida: `tests/fp29_series_externas.py`; salida: `data/fp29-series-externas-2026-08-18.json`.

**C1 · Pew — `obtenido-y-alta`.** 7 intentos con salida cruda; topline primario obtenido, A.7 verificado estable entre dos generaciones; dos altas al manifiesto, `--verifica` COINCIDE en las dos. No hubo fallo que declarar bajo A.5.

**C2 · Reconciliación — completa para lo testable, con lo no testable nombrado.** 18% CONFIRMADA exacta · 22% SIN PROCEDENCIA SOSTENIBLE (2 atribuciones refutadas, 1 error de categoría, 1 indecidible) · 12% INDECIDIBLE por falta de la ola 6 · las tres de ENCUCI intactas bajo `ADR-64`. Argumento de vinculación declarado por los cuatro ejes; ninguna escala promediada con otra.

**C3 · Cierre — completo.** Ficha de adjudicación (§4, tabla completa) · `FP-29` → `FIRMADA` con `ejecutada_en` · `ADR-111` con la reserva C3 repetida verbatim en su inciso (g) · cascada del conteo derivada y verificada · 6 líneas en `hallazgos.md` · cola derivada para el sucesor (§6) · auditoría con qué mueve y qué no (§7).

**Lo que el encargo pedía y este acto NO hizo, dicho en vez de omitido:** el encargo pedía `FP-29→FIRMADA/ejecutada` y eso se hizo; pero la decisión sobre qué debe decir el canon quedó **sin adjudicar a propósito** y abrió `FP-58` — adjudicarla habría sido el ejecutor decidiendo en vez de propagar (`ADR-76`/`ADR-79`), y el propio encargo excluía canon sustantivo del perímetro.
