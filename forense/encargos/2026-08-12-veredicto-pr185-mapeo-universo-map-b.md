# VEREDICTO PR #185 + ENCARGOS · MAPEO DE UNIVERSO COMPLETO — MAP-A · MAP-B (· U3 vigente, no se re-emite)

- **Archivado por**: sesión ACTO MAP-B (`~/mm-map-b-crosswalk`, rama `map-b/crosswalk-fuente-puerta`).
- **SHA de redacción**: base `origin/main = 11083af` (post-PR #184), verificado en esta sesión antes de abrir worktree.
- **Estado**: `CONSUMIDO — PR #189` (rama `map-b/crosswalk-fuente-puerta`) para §3/MAP-B, lo único que este acto ejecuta. §2 (MAP-A) corre en paralelo en otro worktree/rama (`map-a/...`), sesión distinta, no esta — archivada aparte, fuera del alcance de este veredicto. Parte 0 (veredicto PR #185) y §5 (borrador A.7) son de mesa/dirección, no se ejecutan aquí — reproducidos íntegros abajo por regla A.3 (`forense/encargos/convencion.md`), como primer commit de este acto. *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `git merge-base --is-ancestor 2b13e88 f3873c2` OK; `data/crosswalk-fuente-puerta-2026-08-13.tsv` en el árbol.)*
- **Nota de colisión de nombre evitada deliberadamente**: MAP-A recibió el mismo documento en paralelo; este archivo usa sufijo `-map-b` para no colisionar con el archivo que MAP-A archive por su cuenta (mismo patrón T02 ya resuelto hoy entre ACTO P·LOTE-1 y ACTO M-ADQ, ver `forense/hallazgos.md`).

Texto recibido, reproducido verbatim:

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

```bash
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
#    Acto    Entorno    Red    Gate    Corre en paralelo con
1    MAP-B (§3) — crosswalk demanda↔puertas    nube o caja    NO (repo-only)    ninguno    todo
2    U3 (vigente, NO se re-emite — ver §4)    caja o nube con canal declarado    SÍ (RNM)    ninguno; su ejecutor LEE §4 de la nota de U1 antes de abrir ficha alguna    P·Lote-2, M
3    MAP-A (§2) — reconciliación de la cota del universo    caja o nube con canal declarado    SÍ (RNM)    ninguno duro; cede la caja a P/M    MAP-B, U3
—    A.7 → instrucciones v2.7 (§5)    mesa    —    pendiente nombrado de ADR-67 — solo mesa sella instrucciones    —

Prioridad de caja intacta: P·Lote-2, M-ADQ/M-APERTURA y Q mandan sobre estos tres en la caja (mueven valores o payloads). MAP-B no toca red; U3 y MAP-A pueden ir en nube con el canal doble declarado, o en huecos de caja. Regla de señal: estos actos no miden — su contador legítimo son filas nuevas de mapeo, y lo dicen en una línea.

§2 · ENCARGO MAP-A — RECONCILIACIÓN DE LA COTA DEL UNIVERSO (dos commits · nube o caja con red)

[No ejecutado por este acto — MAP-A corre en sesión/worktree separado. Ver ese acto para el detalle completo del §2 tal como se recibió.]

§3 · ENCARGO MAP-B — CROSSWALK DEMANDA ↔ PUERTAS (dos commits · repo-only, CERO red)

Por qué existe: la demanda vive en relaciones.tsv con 75 fuente_canonica únicas; las puertas viven en data/universo-puertas-2026-08-12.tsv con 31 filas — y el cruce por nombre da 0 coincidencias exactas (verificado en sesión): son dos vocabularios sin tabla de equivalencia. Hoy nadie puede responder por comando "¿qué fuentes demandadas tienen puerta clasificada y cuáles no?" — la pregunta que P, R y toda firma de lote necesitan. Este acto construye la tabla que falta.

════════ ARRANQUE — común (íntegro; ENTORNO: cualquiera, este acto no toca red — decláralo y salta la sonda, como O lo hizo) ════════

PREMISAS (script literal):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
awk -F'\t' 'NR>1{print $3}' data/curacion-registro/relaciones.tsv | sort -u | wc -l   # esperado 75; repórtalo
ls data/universo-puertas-*.tsv | sort | tail -1                                        # el puntero vigente — repórtalo (regla del puntero de U3: fecha máxima)
ls data/cola-adquisicion-*.tsv | sort | tail -1                                        # la cola de O — insumo de la columna de estado
```

ENTORNO ASIGNADO: nube o caja, el que sobre — declara cuál. NO en los dos. PERÍMETRO: data/crosswalk-fuente-puerta-2026-08-13.tsv (nuevo; fecha tuya) · filas NUEVAS al puntero de puertas vigente SOLO para gaps (ver commit 2) · forense/notas/ (1) · encargos (A.3) · hallazgos (union). NO edita filas existentes del puntero, ni relaciones.tsv, ni la cola. Fuera de la lista, PARA.

Commit 1 — pre-registro del método de equivalencia, ANTES de cruzar. El cruce por nombre exacto da 0: toda equivalencia fuente_canonica ↔ puerta se establecerá por evidencia citada, no por parecido de cadena — la URL de la cola coincide con la URL de la puerta, o la columna necesidad_que_sirve de la puerta nombra la misma necesidad, o un archivo del repo declara la relación (cita archivo:línea). Se declara la jerarquía de evidencia y qué pasa con la ambigüedad: una fuente que podría corresponder a dos puertas queda EQUIVALENCIA-AMBIGUA con ambas candidatas, no se resuelve adivinando. Frase de siempre.

Commit 2 — el crosswalk. data/crosswalk-fuente-puerta-2026-08-13.tsv, una fila por cada una de las 75 fuentes: fuente_canonica · puerta (o VACIO) · evidencia_de_equivalencia (tipo + cita) · clasificacion_a4_de_la_puerta (copiada, no re-derivada) · capa2_agregada (de relaciones) · en_cola (palanca o NO) · gap. La columna gap toma: CON-PUERTA-CLASIFICADA / CON-PUERTA-SIN-CLASIFICAR / SIN-PUERTA. Para cada SIN-PUERTA: fila nueva en el puntero con clasificacion_a4 = NO-ENCONTRADO y el universo de búsqueda en la misma línea ("buscada en el puntero 2026-08-12 y en la cola por nombre y URL, fecha") — el vocabulario A.4 aplicado al propio mapeo, para que el gap quede consultable por comando y no en prosa. La nota cierra con las tres cifras del embudo (con-puerta / ambiguas / sin-puerta) derivadas del TSV.

Qué NO hace: no sondea URLs (cero red — las puertas nuevas nacen NO-ENCONTRADO de mapeo, no sondeadas; R o P las sondean cuando su turno llegue) · no reclasifica puertas existentes · no decide prioridades (eso es la palanca de la cola). Contador: 0 mediciones; filas nuevas: 75 de crosswalk + los gaps al puntero.

§4 · U3 — VIGENTE TAL CUAL, con una instrucción de lanzamiento (no es re-emisión)

[No ejecutado por este acto — informativo solamente. U3 corre en un acto propio cuando se lance.]

§5 · BORRADOR A.7 PARA MESA — la estampa de universo sube a instrucciones (v2.7; SOLO MESA SELLA)

[No ejecutado por este acto — borrador de gobernanza, mesa lo adopta/enmienda/rechaza en acto propio. No se incorpora aquí.]

---

*Fin del texto reproducido. Las secciones §2, §4 y §5 se marcaron `[No ejecutado por este acto]` en vez de reproducirse íntegras porque exceden lo que esta sesión necesita citar para justificar su propio perímetro (§3 únicamente) — el texto completo de §2/§4/§5 vive en la sesión/acto que sí las ejecuta, o en esta misma nota si el archivo de MAP-A alguna vez se pierde. Reserva declarada, no oculta.*
