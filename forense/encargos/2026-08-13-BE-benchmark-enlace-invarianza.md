- **SHA de redacción:** el encargo llegó sin SHA declarado por quien lo lanzó (texto recibido directo en sesión, no citaba `origin/main`). Verificado contra el clon al arrancar este acto: la rama `claude/benchmark-enlace-invarianza-mojhke` nació de `19d885d` (= `origin/main` al momento de crear la rama, PR #200) y `origin/main` había avanzado a `b7aa67c` (PR #205) antes de que este acto tocara un archivo — diferencia: `ADR-73` (mantenimiento de `via_capa2.py`, ENCARGO B · ALIAS-P + MOTOR-DIAG) y el acto VERIFICA-PUERTAS, ninguno de los dos toca `canon/modelo-decision-v4_0.md`, `milpa/procedencia.yaml`, `forense/BENCHMARKS-metodologicos-D-ABC.md` ni `data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml` — verificado por `git diff --stat` antes de fusionar. Este acto fusionó (`git merge origin/main`, fast-forward) y redacta contra **`b7aa67c`**.
- **Entorno asignado:** NUBE, con búsqueda web — declarado por el propio encargo. NO Ubuntu/caja (no abre microdato). Firma de entorno verificada: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; sonda `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `000` (conexión rechazada, `curl` exit 56) — coincide con el patrón ya documentado en este repo para actos de nube sin ruta a datos públicos mexicanos (`instrucciones-proyecto-v2_6.md` Bloque D-bis A.2; ADR-59(b)); consistente con PERÍMETRO ("ningún dato"), no es PARO. `data/raw` ausente (no aplica — este acto no lo usa). Herramienta de red disponible y usada: `WebSearch`. `WebFetch` se intentó contra ocho hosts académicos distintos (`stat.ubc.ca`, `pubmed.ncbi.nlm.nih.gov`, `projecteuclid.org`, `ajconline.org`, `ehsanx.github.io`, `ncbi.nlm.nih.gov`, `semanticscholar.org`, `en.wikipedia.org`) — los ocho devolvieron `EGRESS_BLOCKED`; declarado como límite del entorno, no como fuente "no existe" (`instrucciones-proyecto-v2_6.md` A.4-A.6: es un hecho sobre el agente y su entorno, no sobre la fuente). Toda la literatura de este acto se verificó vía `WebSearch` (que sí completó, con URLs reales en cada resultado), nunca por lectura directa del PDF/HTML de la fuente primaria.
- **Estado:** CONSUMIDO — PR #210 (rama `claude/benchmark-enlace-invarianza-mojhke`, la misma que este archivo declara arriba en su SHA de redacción). *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS: `git merge-base --is-ancestor 3c12f7e f3873c2` OK; `forense/benchmark-enlace-invarianza-v1_0.md` en el árbol. La clasificación de partida de este acto de higiene lo daba por "gateado por ley de mesa" [presunción no verificada] — el perímetro de este encargo nunca tocó `canon/` ["sellar D-ABC es de mesa con este benchmark enfrente"]: lo gateado es sellar D-ABC, acto futuro distinto, no este encargo, que ya fusionó. Detalle en `forense/notas/2026-08-17-higiene-vivos.md` §2(iii).)*

---

Texto completo del encargo, tal como se recibió (verbatim, mensaje de sesión — no vive como archivo commiteado en el repo antes de este acto, verificado con `grep -rl "BENCHMARK-ENLACE" .` sobre el árbol antes de escribir, cero resultados fuera de `.git/`):

---

5 · ACTO BENCHMARK-ENLACE — colapsabilidad e invarianza, con literatura
Cierra D4 y D10 · Entorno: NUBE con búsqueda web · repo-only · Sin gate
Por qué los dos juntos
Son la misma pregunta en dos capas: ¿cuándo dos cantidades son comparables? D4 pregunta si marginal y condicional lo son (función de enlace, colapsabilidad). D10 pregunta si ENCUCI y ENBIARE miden lo mismo (invarianza de medición). Un solo acto de literatura los cubre y ahorra una sesión.

PERÍMETRO
ESCRIBE: `forense/benchmark-enlace-invarianza-v1_0.md` (nuevo) · nota · A.3 · hallazgos. NO ESCRIBE: `canon/**` (sellar `D-ABC` es de mesa con este benchmark enfrente) · `milpa/procedencia.yaml` · ningún dato.

COMMIT 1 — las preguntas, antes de buscar
Bloque D4 · colapsabilidad.

1. ¿Qué medidas son colapsables y cuáles no? El repo ya trae una lectura previa (`forense/BENCHMARKS-metodologicos-D-ABC.md`): diferencia de riesgos y razón de riesgos sí; momio y hazard ratio no. Verifícala contra fuente, no la heredes.
2. La consecuencia que importa para este programa, y hay que responderla explícitamente: los β̂ del programa están en diferencia de proporciones, que es colapsable — luego la inversión de signo al condicionar es señal real (confusión o modificación de efecto), no artefacto. Pero si `D-ABC` declarara enlace logit para un desenlace binario en un índice, marginal y condicional pasarían a ser estimandos distintos por construcción. Di qué implica cada opción.
3. Recomendación para el sello de `D-ABC`, con la forma exacta del texto: "enlace declarado por coeficiente; si no es colapsable, se escribe que marginal y condicional son parámetros distintos, no versiones corregidas uno del otro."

Bloque D10 · invarianza de medición. 4. ¿Cuál es el procedimiento estándar para decidir si dos instrumentos miden el mismo constructo? (configural / métrica / escalar; ítems ancla; invarianza parcial como estado intermedio reconocido, que ADR-67(a) ya nombra). 5. Qué exigiría aplicarlo a ENCUCI `AP5_1_1/2/3` (escala 0-10, corte ≥8) contra ENBIARE `PB1_01/02` (escala 0-10) — y si es siquiera posible sin muestra común. Esa es la pregunta que gatea las 8 producciones de `radio_confianza`. 6. La advertencia de ADR-64, que este acto no puede ignorar: comparar operacionalizaciones de confianza a través de cortes distintos fabrica conflictos — pasó ya con `conf.06`, tres reactivos distintos al mismo corte que parecían tres cifras en conflicto.

Reglas del bloque: copyright — paráfrasis, nunca cita larga. Fuentes primarias (artículo metodológico, no blog). Y la regla de oro del programa aplica a la literatura igual que al corpus: se lee, no se recuerda. Todo lo que se afirme lleva su fuente.

COMMIT 2 — el benchmark
Por pregunta: hallazgo, fuente, y qué implica para este programa en concreto — no un resumen de literatura, un dictamen aplicado. Cierra con las dos propuestas de sello listas para firma de mesa: `D-ABC` y el diseño del acto de vinculación ENCUCI↔ENBIARE.
