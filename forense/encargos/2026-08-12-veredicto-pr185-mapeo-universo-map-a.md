Archivado por convención de este directorio (`forense/encargos/convencion.md`), como primer commit de ACTO MAP-A — Regla A.3 (`instrucciones-proyecto-v2_6.md`, Bloque D-bis). Texto recibido como mensaje pegado en sesión de chat (no vive como archivo commiteado en el repo — verificado, `git ls-tree -r origin/main` no lo encuentra bajo ningún nombre relacionado a "encargos-finales"/"mapeo-universo"). Reproducido idéntico al archivado independientemente por el acto hermano MAP-B (mismo documento fuente, dos actos distintos lo consumen) — **nombrado con sufijo `-map-a` deliberadamente para evitar la colisión de nombre normalizado (T02) que ya ocurrió hoy entre ACTO P·LOTE-1 y ACTO M-ADQ (PRs #186/#187) sobre este mismo patrón de documento compartido.**

---

VEREDICTO PR #185 + ENCARGOS · MAPEO DE UNIVERSO COMPLETO — MAP-A · MAP-B (· U3 vigente, no se re-emite)
12-13/ago/2026 · base verificada en sesión: origin/main = 11083af (post-#184) · revisión de #185 hecha por dirección contra clon propio, con merge de prueba local ejecutado · construcción R1/R2/R3

PROCEDENCIA. Toda cifra derivada por comando contra el clon en esta sesión (197 relaciones · 75 fuentes únicas · capa2 = 105/24/68 · puntero de puertas vigente 2026-08-12, 31 filas, RNM presente ×4 · cota del universo declarada COTA_SUPERIOR_NO_RECONCILIADA en gobernanza:862, ADR-67). Quien ejecute verifica premisas contra su clon antes de obedecer.

PARTE 0 · VEREDICTO DE REVISIÓN — PR #185 (U1/E4b′): APTO — PROPUESTO A MESA, con UN paso mecánico antes del botón

Lo verificado por dirección, comando a comando:

Sello de dos commits íntegro. Commit 1b (0edc008) enmienda SOLO la spec (periodo_levantamiento + criterio_parada por consistencia interna, con verificación de que criterio_parada no es gate operativo — grep contra produce.py citado). Commit 2 (8565c17) NO toca especificaciones-produccion.json; sobre la nota es append-only puro (0 líneas borradas, verificado por diff). Frase de sello en ambos.
Enmienda pre-dato legítima: CORRIDA-B produjo 0 cálculo (ningún resultado fue visto) y ADR-69(b) autorizó por escrito este tercer commit sobre su propia especificación.
Ficha 922 releída de primera mano, no heredada; discrepancia interna tabla-vs-prosa (16-dic vs 10-dic) resuelta POR ESCRITO ANTES de adoptar — tabla adoptada, prosa citada como reserva, sin conciliar los seis días. Exactamente lo que el encargo pedía. Método de extracción declarado (parseo <tr>/<td> sobre HTML crudo).
§3 corrigió una premisa FALSA del propio encargo verificando contra código: documentacion_fuente SÍ existe (ADR-70/#177); la razón real de no poblarlo es la lista cerrada de exención validate.py:52-57 que nombra a ESP-OPACA-B-d13ec4fe. Conclusión operativa correcta por la razón correcta — "verificación de premisas antes de ejecución" hecha bien.
Resultado disciplinado: motor cegado, reproducción byte a byte con hashes_analista_confiados: false; universo del instrumento declarado con precisión excepcional (TPER_ELE, persona elegida 15-60, distinguido de los TRES universos traslapados que comparten P7_12_7); escala nativa; n por categoría; EE + IC95 por categoría; proporciones suman 1.0000; hashes de microdato y spec en el expediente; reserva FAC_SEL/FAC_ELE ya registrada pre-acto, citada.
No adjudica nada: requiere_decision_mesa: true intacta, estado_operativo: PENDIENTE, estado_uso_modelo: NO_LISTA_DECISION_HUMANA_PENDIENTE derivado por máquina. Celda-D actualizada por precedente citado (celda hermana de radio), no por criterio inventado. Suite --baseline VERDE sin cambio.
§4 es oro para U3: el fetch resumido por IA atribuyó mal filas de DOS tablas de fechas (verificado contra <tr> crudo); regla operativa: HTML crudo + parseo explícito para toda ficha RNM con más de una tabla de fechas. U3 abre ocho de la misma familia.

EL PASO MECÁNICO ANTES DEL BOTÓN. El PR nació en e078e46 (post-#183) y main ya está en 11083af (post-#184); ambos añaden líneas al final de forense/hallazgos.md. GitHub NO honra el driver union del lado servidor (#182): el botón lo verá en conflicto. El merge local con el driver en el árbol fusiona limpio y conserva todo — lo ejecuté como prueba: las entradas de #184 (commits 8, 9, 10, ACTO O) y la línea de U1 coexisten. Quien tenga push a la rama corre:

```
cd <clon> && git fetch origin && git checkout u1/e4b-prime-recorrida
git merge origin/main        # el driver union resuelve hallazgos.md solo; NINGÚN otro archivo choca (verificado)
grep -c "2026-08-12" forense/hallazgos.md   # debe conservar TODAS las líneas de #184 + la de U1
git push origin u1/e4b-prime-recorrida      # el botón queda limpio
```

Dos observaciones para mesa (no bloquean):

(a) Singletons: ni resumen.json ni resultado.tsv traen el contador de singletons junto a los EE (disciplina escrita para las vías svystat de K/U2; la vía aquí fue produce.py/Taylor). Red de seguridad ya prevista: U2/EV-1 debe incluir la fila de ENASIC — su propio texto dice "y la de ENASIC si U1 ya corrió"; U1 ya corrió. El cruce EE-vs-EE contra el validador oficial (922/download/29534) atrapará cualquier EE mal calculado.
(b) Divergencia de letra del encargo, resuelta por canon: el encargo decía "expediente nuevo que lo cita"; el acto escribió sobre el expediente existente porque la vía del motor lo determina (el expediente es función del ID de spec) y ADR-69(b) autorizó "sobre su propia especificación". Nada se perdió (el estado previo era NO_DETERMINADO, preservado en git y en la nota de CORRIDA-B). La nota no nombra la divergencia explícitamente — queda nombrada aquí.

ACTUALIZACIÓN DE ESTADO QUE CAMBIA TU ADJUDICACIÓN PENDIENTE DE K: #184 entró a main con commits 9 y 10, que revisan el veredicto propuesto de la corrida: con el proxy correcto (gasto_mon, la metodología sellada), el monto NO se documenta suficiente (29.0% media ponderada; IC95 de la razón despeja POR DEBAJO del piso de 33% en las dos variantes) → por la precedencia sellada de ADR-71(b), "monto insuficiente" gana sobre A → la propuesta vigente es fila B, EJERCIDA_INDECISA — no la fila A que te reporté de la conversación de Opus (era correcta entonces; el commit 9 la retiró sin editarla). Los DiD/DDD de commit 8 no cambian. Tu acto de adjudicación de la llave debe partir de B.

Contador que #185 propone (mesa firma): primera θ de familismo_obligacion — 0.6933 [0.6725, 0.7140] "De acuerdo" — con la reserva de encuadre de género (ADR-67(b)) intacta y SIN resolver. Resolver esa reserva es el acto de mesa que convierte la θ en LISTA.

PARTE 1 · ORDEN DE LOS ACTOS DE MAPEO (no compiten con la caja de descargas)

| # | Acto | Entorno | Red | Gate | Corre en paralelo con |
|---|---|---|---|---|---|
| 1 | MAP-B (§3) — crosswalk demanda↔puertas | nube o caja | NO (repo-only) | ninguno | todo |
| 2 | U3 (vigente, NO se re-emite — ver §4) | caja o nube con canal declarado | SÍ (RNM) | ninguno; su ejecutor LEE §4 de la nota de U1 antes de abrir ficha alguna | P·Lote-2, M |
| 3 | MAP-A (§2) — reconciliación de la cota del universo | caja o nube con canal declarado | SÍ (RNM) | ninguno duro; cede la caja a P/M | MAP-B, U3 |
| — | A.7 → instrucciones v2.7 (§5) | mesa | — | pendiente nombrado de ADR-67 — solo mesa sella instrucciones | — |

Prioridad de caja intacta: P·Lote-2, M-ADQ/M-APERTURA y Q mandan sobre estos tres en la caja (mueven valores o payloads). MAP-B no toca red; U3 y MAP-A pueden ir en nube en huecos de caja. Regla de señal: estos actos no miden — su contador legítimo son filas nuevas de mapeo, y lo dicen en una línea.

§2 · ENCARGO MAP-A — RECONCILIACIÓN DE LA COTA DEL UNIVERSO (dos commits · nube o caja con red)

Por qué existe: ADR-67 (gobernanza:862) dejó la doctrina de estampa de universo con un denominador vacío: "el universo desconocido no tiene denominador (tablero: COTA_SUPERIOR_NO_RECONCILIADA)". Cada sello desde entonces porta un universo cuyo total nadie ha contado. Los números que hoy circulan — 509/35,708 activos inspeccionados (1.43%), régimen de cierres de 5 instrumentos "de 958 programas hoy conocidos" (0.52%) — mezclan tres denominadores distintos (activos T0, programas conocidos, demanda del modelo) y el "958" no tiene receta citable. Este acto les pone universo, mecanismo y fecha a los tres, y propone a mesa el rótulo que sustituye la cota no reconciliada.

════════ ARRANQUE — común (el bloque completo vive en ENCARGOS-FINALES-PLAN-DESCARGAS-2026-08-12.md; ejecútalo íntegro: REPO · SHA contra 11083af o posterior · data/raw no aplica-decláralo · ENTORNO con firma declarada (caja sin_variable+200 / nube cloud_default; si usas el canal doble del contenedor de chat, decláralo como tal) · ESPEJO nada · REMOTO Josanoforo/Modelado-Mexicano) ════════

PREMISAS (script literal):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
grep -c "COTA_SUPERIOR_NO_RECONCILIADA" canon/gobernanza-v1_15.md   # esperado ≥1; repórtalo
wc -l < data/curacion-universo/universo-declarado-t0.tsv            # esperado 35709 (35,708 + header); repórtalo crudo
grep -rn "958" canon/gobernanza-v1_15.md | head -3                  # la cifra sin receta — repórtala tal cual aparece
c=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "https://www.inegi.org.mx/rnm/index.php/catalog"); echo "rnm=$c"  # 200=adelante; otro=canal alterno declarado o NO OBTENIDO con receta
```

ENTORNO ASIGNADO: caja O nube — declara cuál. NO en los dos. PERÍMETRO: data/universo-cota-2026-08-13.tsv (nuevo; fecha tuya) · forense/notas/ (1) · forense/encargos/ (A.3) · forense/hallazgos.md (union). NO toca canon/, milpa/, el tablero, ni ningún TSV existente. Fuera de la lista, PARA.

Commit 1 — pre-registro del mecanismo de conteo, ANTES de contar. Declara: (a) qué población cuenta cada denominador — D1: activos declarados T0 (receta: wc -l menos header sobre universo-declarado-t0.tsv, más el desglose por tipo que sus columnas permitan); D2: programas del catálogo RNM (el mecanismo exacto de enumeración: paginación del catálogo rnm/index.php/catalog por HTML crudo — la lección de U1 §4: parseo <tr>/<td> explícito, PROHIBIDO fetch resumido por IA — o el endpoint de búsqueda si expone total; se declara cuál y por qué); D3: demanda del modelo (receta: fuentes únicas de relaciones.tsv = 75, relaciones = 197, derivadas en commit 2 con comando a la vista); (b) qué es "programa conocido" y de dónde salió el 958 — se rastrea la cifra en el repo; si no tiene receta reproducible, se declara CIFRA-SIN-RECETA y D2 la sustituye; (c) el criterio de cierre: si la enumeración RNM no se puede completar (paginación truncada, bloqueo), el entregable es la cota PARCIAL con su universo declarado — "conté hasta la página N con este mecanismo" — jamás un total inferido. Frase de siempre.

Commit 2 — el conteo y la reconciliación. data/universo-cota-2026-08-13.tsv: una fila por denominador — denominador · valor · universo_de_conteo · mecanismo · fecha · comando_o_url. Más, en la nota: la reconciliación (qué fracción de D2 está en D1; qué fracción de D3 está en D1 con payload; dónde D1 excede D2 y por qué — activos no-RNM), y la PROPUESTA a mesa del rótulo que sustituye COTA_SUPERIOR_NO_RECONCILIADA (p. ej. COTA_RNM=N (mecanismo, fecha) + NO_RNM_SIN_COTA si eso es lo que el conteo sostiene). Mesa firma el rótulo en acto propio — este acto NO edita gobernanza ni el tablero.

Qué NO hace: no descarga payloads · no clasifica fuentes (eso es A.4 de P/R) · no reabre cierres. Contador: 0 mediciones; filas nuevas: los denominadores con receta. Y si al enumerar RNM aparece una fuente que destraba un SIN-RUTA abierto: repórtalo y para — vale más que terminar el conteo.

§3 · ENCARGO MAP-B — CROSSWALK DEMANDA ↔ PUERTAS (dos commits · repo-only, CERO red)

Por qué existe: la demanda vive en relaciones.tsv con 75 fuente_canonica únicas; las puertas viven en data/universo-puertas-2026-08-12.tsv con 31 filas — y el cruce por nombre da 0 coincidencias exactas (verificado en sesión): son dos vocabularios sin tabla de equivalencia. Hoy nadie puede responder por comando "¿qué fuentes demandadas tienen puerta clasificada y cuáles no?" — la pregunta que P, R y toda firma de lote necesitan. Este acto construye la tabla que falta.

[Texto completo de §3 (MAP-B), §4 (U3, vigente no re-emitida) y §5 (borrador A.7 para mesa) recibido en el mismo mensaje — no repetido en esta copia porque MAP-A no ejecuta esas partes; ver el acto MAP-B para su propia copia íntegra de §3, y PR #185/canon/gobernanza para §4/§5.]

§5 · BORRADOR A.7 PARA MESA — la estampa de universo sube a instrucciones (v2.7; SOLO MESA SELLA)

ADR-67 dejó esto como "pendiente nombrado de mesa, no se sella aquí". Ningún ejecutor lo incorpora — MAP-A no toca instrucciones-proyecto-*.md ni canon/gobernanza bajo ninguna circunstancia.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-12-veredicto-pr185-mapeo-universo-map-a.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-12-map-a-cota-universo.md, forense/notas/2026-08-14-t-firmas.md, forense/notas/2026-08-19-u2-ev1-paro-red.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
