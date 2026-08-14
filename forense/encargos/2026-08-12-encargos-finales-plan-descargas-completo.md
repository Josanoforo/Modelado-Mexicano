# ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO — documento único

- **SHA de redacción**: `f8eb2e3` (base declarada por el propio documento: "base origin/main = f8eb2e3"; verificado en esta sesión — `f8eb2e3` es ancestro de `origin/main`, HEAD actual `11083af` tras el merge de PR #184).
- **Entorno asignado**: por acto, ver §0 ORDEN MAESTRO del texto abajo. **P·Lote-1, P·Lote-2, Q, M-APERTURA, R**: caja obligatoria (`sin_variable` + sonda 200), nunca nube. **M-ADQ**: nube o caja, el que esté libre, nunca los dos. Esta sesión ejecuta **ACTO M-ADQ** en caja (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir, firma Ubuntu-con-red) — declarado así porque otro worktree local (`mm-p-lote1-adquisicion`, rama `acto-p/lote1-adquisicion`) ya reclamó P·Lote-1 en caja; M-ADQ y P·Lote-1 corren en paralelo por diseño del propio documento (§0, perímetros disjuntos salvo el puntero de puertas, donde ambos solo añaden filas).
- **Estado**: `CONSUMIDO (parcial)` — **§0a/§1 (FIRMA DE CORTE)** ya estaban `CONSUMIDO`: PR #183 fusionado en `origin/main` (commit `e078e46`) con la firma de corte de mesa. **ACTO K (§8) ya corrido y fusionado** (PR #184, commit `11083af` — verificado en esta sesión, adjudicación de mesa ya reflejada en main). Esta sesión ejecuta **ACTO M-ADQ (§3)**, detalle en `forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md`. **P·LOTE-1 (§2) está en curso en otro worktree local** (no en esta rama). **P·LOTE-2 (§4), Q (§5), M-APERTURA (§6), R (§7) no se ejecutan en esta sesión** — quedan `VIVO`, gateados como el documento especifica.

Archivado por convención de este directorio (`forense/encargos/convencion.md`), como primer commit de este acto, antes de ejecutar el resto del bloque de ARRANQUE — Regla A.3 (`instrucciones-proyecto-v2_6.md`, Bloque D-bis). Texto reproducido idéntico al archivado independientemente por la sesión de P·Lote-1 (mismo documento fuente, dos actos distintos lo consumen).

---

## Texto completo del encargo, tal como se recibió

ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO — documento único
12/ago/2026 (noche) · base origin/main = f8eb2e3 · Este documento SUSTITUYE a ENCARGOS-DESCARGA-SECUENCIA-2026-08-12.md y re-emite completos los actos de adquisición de ENCARGOS-ADQUISICION-O-P-Q-R.md (Q y R) y de ENCARGOS-K-L-M-N-siguiente-paquete.md (M, partido en dos). NO re-emite U1→U2→U3 (viven en ENCARGOS-FINALES-cierre-brecha-U1-U2-U3.md y duplicar encargos vivos es el defecto ya pagado). ACTO O está CONSUMIDO (PR #183). ACTO N está SUPERADO por la firma del corte. ACTO K está corrido (PR #184, pendiente de adjudicación de mesa). L es repo-only y no es de este plan.

PROCEDENCIA. Toda cifra fue derivada por comando contra clon propio en la sesión que redacta (fetch final: origin/main = f8eb2e3; en ese momento #183 aún figuraba abierto y mesa/s-svystat-4celdas aún existía — si tu fusión ya corrió, los gates de abajo lo confirmarán por comando). Regla de la casa: quien ejecute verifica las premisas de ESTE documento contra su clon antes de obedecerlo.

§0 · ORDEN MAESTRO
#    Acto    Entorno    Gate (por comando, no por fe)    Puede correr en paralelo con
0a    Fusionar #183 con la FIRMA DE CORTE (§1)    GitHub (mesa)    —    —
0b    Borrar rama mesa/s-svystat-4celdas    GitHub (mesa)    verificado: su árbol está íntegramente superado por main (#179 + ADR-71(d))    —
1    ACTO P·LOTE-1 (§2)    caja    #183 fusionado + cola en main    M-ADQ, U1-U3
2    ACTO M-ADQ (§3)    nube o caja    ninguno    P·Lote-1, U1-U3
3    ACTO P·LOTE-2 (§4)    caja    PR de Lote-1 fusionado + firma de mesa de las 5 del lote (en el lanzamiento)    M-APERTURA, U1-U3
4    ACTO Q (§5)    caja    ninguno duro; cede la caja a P    P entre lotes
5    ACTO M-APERTURA (§6)    caja    M-ADQ cerrado y fusionado    P·Lote-2
6    ACTO R (§7)    caja    después de lotes 1-2    — (un dominio por sesión)
∥    U1→U2→U3    según su encargo    ya emitidos — NO se re-emiten aquí    intercalar donde quepan; no gastan red
∥    Adjudicación de #184 (corrida de K)    GitHub/repo-only (mesa)    cuando mesa quiera    todo — no consume caja ni red

Reglas que gobiernan los siete actos: se baja por demanda nombrada, nunca por completismo; el contador son los valores, no los gigabytes · los actos que mueven valores tienen prioridad de caja sobre los que llenan disco · si a mitad de cualquier acto aparece algo que desbloquea un cálculo, eso vale más que terminar el acto — repórtalo y para · cada acto cierra con embudo PRISMA contado o con la línea "no movió nada" · ningún ejecutor adjudica: propone, mesa firma.

§1 · FIRMA DE CORTE — texto para el comentario de merge de #183 (si ya fusionaste con este texto, este § está CONSUMIDO)

FIRMA DE CORTE (mesa, 12/ago/2026). Se firma el Lote 1 con ajuste sobre la propuesta de §5 de la nota: entran ISSP (palanca 1) · WVS (3) · EARLY_CHILDHOOD_EDUCATION_2012_2014 (4) · GPS (6) · CSES (7). Salen del lote — sin salir de la cola — BRASDEFER (2) y MOBILE_TUTORS (5): sus relaciones de destraba están clasificadas NEGATIVA en relaciones.tsv (curaduría MULTI2 / apertura negativa explícita, confianza MEDIA/ALTA) y adquirirlas sin reapertura previa no mueve nada; su reapertura queda como decisión de mesa aparte, a la vista del reporte E-CE v1.1, no de un lote de descarga. Lote 2 y 3 NO se firman aún: se firman al lanzar P·Lote-2, con lo aprendido del Lote 1. ACTO N (DESC-1) queda SUPERADO por esta cola: sus cinco fuentes viven en ella (ISSP=1, WVS=3, GPS=6, ENCOAP=17, LATINOBARÓMETRO=53); ISSP/WVS/GPS entran por el Lote 1, ENCOAP es candidata al Lote 2, Latinobarómetro espera su palanca. Motivo: dos encargos activos sobre las mismas fuentes es el defecto de duplicación ya pagado dos veces. La colisión N17/N24 declarada en §3.3 de la nota queda anotada para quien firme lotes: no contar esa necesidad dos veces.

════════ ARRANQUE — común a TODOS los actos de este documento; hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status. ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compárala con f8eb2e3 más lo que el gate de tu acto exija. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza al corpus compartido. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE + curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ — reporta los dos valores crudos. NUNCA curl -I. Firma de caja: sin_variable + sonda 200. Firma de nube: cloud_default sin sonda (ADR-59(b)). Cada acto declara abajo cuál exige.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

5-bis · REMOTO (línea pagada por la muerte de W1-P). Antes de CUALQUIER push, git remote -v debe apuntar a Josanoforo/Modelado-Mexicano. Si no cuadra: PARO.

Regla A.3: el texto del encargo del acto se archiva en forense/encargos/ como PRIMER commit del acto. R3: los actos abren en paralelo entre sí con perímetros disjuntos salvo forense/hallazgos.md (merge=union); rebase local antes del PR; el botón solo fusiona limpios; editor web prohibido.

═══════════════════════════════════════════════════════════════════════════════════════════

§2 · ACTO P·LOTE-1 — las cinco fuentes firmadas (caja · dos commits)

GATE (script, primer comando del acto):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
git merge-base --is-ancestor $(git rev-parse origin/main) HEAD 2>/dev/null; git checkout -q origin/main 2>/dev/null || true
ls data/cola-adquisicion-*.tsv | sort | tail -1        # esperado: data/cola-adquisicion-2026-08-12.tsv — si no existe, #183 no está fusionado: PARA
```

Además: la firma de corte visible en el PR #183 fusionado (cita su texto en la nota).

ENTORNO ASIGNADO: caja Ubuntu, worktree propio (sin_variable + sonda 200). NO lo lances en la nube.

PERÍMETRO Y CONCURRENCIA. Este acto toca: data/raw del corpus compartido (payloads) · data/manifiesto.yaml vía tests/manifiesto.py --registra · capa2 por la vía del motor (decisiones-adquisicion — jamás editar TSV a mano) · el puntero de puertas/activos documentales (conducto, ADR-70; solo FILAS nuevas) · forense/notas/ (1 nota) · forense/encargos/ (regla A.3) · forense/hallazgos.md (union). Corren en paralelo: M-ADQ (mismo puntero de puertas — cada quien añade filas, nadie edita filas ajenas) y U1-U3 (perímetros en sus encargos). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

Commit 1 — el lote congelado. Copia VERBATIM de data/cola-adquisicion-2026-08-12.tsv la fila completa (las 8 columnas) y la palanca de las cinco fuentes firmadas:

Palanca    Fuente    Necesidades    URL de la cola (a sondar)
1    ISSP    7: N2,N3,N12,N13,N14,N28,N30    https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017
3    WVS    2: N5,N15    VACIO — deriva el portal oficial de WVS-7 México y decláralo en este commit; candidata SIN-FETCH hasta abrir (A.6)
4    EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014    1: N13    https://microdata.worldbank.org/catalog/2661/study-description
6    GPS    5: N2,N4,N5,N6,N17    https://gps.econ.uni-bonn.de/home
7    CSES    4: N17,N25,N26,N27    https://cses.org/data-download/cses-module-5-2016-2021/

Más, por fuente: el criterio de cierre por clase A.4/A.5 (qué cuenta como EXISTE-SATISFACE para ESTA adquisición: payload íntegro + sha256 registrado + ficha documental localizada). Nota de contexto para ISSP: la cola dejó solo la URL del módulo Social Networks 2017; los otros dos módulos (social-inequality/2019, family-and-changing-gender-roles/2012) están declarados en §3.5 de la nota de O — este lote baja el módulo de la URL de la cola; si el portal ofrece los tres al mismo costo de sesión, se bajan y se registran los tres, declarándolo. Cierra el commit con la frase: "el primer resultado que produzca este procedimiento es el que se reporta."

Commit 2 — la ejecución. Por fuente, en este orden:

Sonda A.5 en sesión sobre la URL declarada. Si falla: NO OBTENIDO POR ESTE AGENTE EN N INTENTOS + los N intentos con salida cruda + receta manual <1 min para que el usuario lo baje en navegador — la receta es el entregable de mayor rendimiento del acto, no su consuelo. Prohibido concluir nada de un portal desde conocimiento de entrenamiento: si no se sondeó en esta sesión, no se sabe.
Descarga a data/raw del corpus compartido.
sha256 vía tests/manifiesto.py --registra.
Decisión de adquisición por la vía del motor (capa2). Si el motor no tiene vía para algo: hallazgo + EN-ESPERA-DE-VIA. Jamás editar TSV a mano.
Ficha RNM/documental localizada ⇒ fila de puerta + activo documental (conducto, ADR-70).
GESIS (ISSP) y WVS exigen registro gratuito: se declara y SE HACE. Registro gratuito NO es NO-ACCESIBLE. Pago o afiliación institucional ⇒ NO-ACCESIBLE declarado con receta manual, no se fuerza.
Nada se abre a nivel variable — la apertura es acto posterior, por demanda.

Cierre: conteos PRISMA (intentadas / sondeadas-200 / bajadas / íntegras / con-ficha / no-accesibles / no-obtenidas) + verificación PR#77 con el listado del corpus compartido a la vista. Contador: capa2 movida en las filas del lote. Si una fuente destraba un cálculo hoy (ISSP toca N12/N13/N14, tres SIN-RUTA abiertos): titular del cierre.

§3 · ACTO M-ADQ — adquisición DOCUMENTAL de ENSAFI 2023 + ENFIH 2019 hasta el universo mínimo ADR-69 (nube o caja · dos commits · NO abre microdato)

Por qué existe como acto propio (corrección de maestra 27, adoptada): abrir a nivel variable antes de tener el universo documental mínimo reproduce el defecto del 8/ago — media respuesta apoyada en encabezados. ENFIH ya tiene descriptor (838 variables, 16 hojas) pero está por debajo del universo mínimo de ADR-69, que pide llegar a ficha RNM y cuestionario; ENSAFI está por debajo de ENFIH. Los cuatro SIN-RUTA que M-APERTURA pretende resolver no pueden decidirse sobre encabezados.

GATE: ninguno. ENTORNO ASIGNADO: nube O caja, el que esté libre — declara cuál; firma de nube cloud_default sin sonda es correcta (ADR-59(b)). NO lo lances en los dos. Si corres en nube/contenedor de chat, recuerda el canal doble (sandbox 403 / herramientas web 200): la vía que responda es la que se usa y se declara.

PERÍMETRO Y CONCURRENCIA. Toca: puntero de puertas/activos documentales (FILAS nuevas) · conducto documental (los documentos van ahí, NO a data/raw — este acto no baja microdato) · forense/notas/ (1) · forense/encargos/ (A.3) · hallazgos (union). En paralelo: P·Lote-1 (mismo puntero — solo filas nuevas). Fuera de esta lista, PARA.

Commit 1 — pre-registro. Para cada fuente (ENSAFI 2023, ENFIH 2019): (a) qué exige el universo mínimo — se LEE de data/UNIVERSO-MINIMO-FUENTE-v1_0.md, que es la definición; este encargo no la parafrasea (R1); (b) qué de eso YA está en el conducto — derivado del puntero por comando, no de memoria; (c) qué falta, pieza por pieza; (d) dónde se buscará cada pieza (ficha RNM en la Red Nacional de Metadatos, portal INEGI del programa; candidatas SIN-FETCH hasta abrir, A.6); (e) criterio A.4 por pieza. Frase de cierre de siempre.

Commit 2 — ejecución. Por pieza faltante: sonda A.5 · apertura byte a byte de lo hallado · clasificación A.4 en la misma línea con universo+mecanismo+fecha (EXISTE-SATISFACE / EXISTE-NO-SATISFACE con qué falta / NO-ENCONTRADO con dónde y términos / NO-ACCESIBLE) · fila de puerta + activo documental por pieza (conducto) · fallas con NO OBTENIDO POR ESTE AGENTE EN N INTENTOS + receta manual <1 min.

Qué NO hace: no abre microdato a nivel variable (eso es M-APERTURA, §6) · no reabre ADR-52A/54 (de mesa, vía E-CE v1.1) · no calcula nada. Contador: piezas del universo mínimo pasadas de FALTANTE a EN-CONDUCTO por fuente — y el reporte que deja a M-APERTURA sin premisa floja. Si al cierre alguna pieza queda NO-ENCONTRADO/NO-ACCESIBLE: eso NO cancela M-APERTURA automáticamente — mesa decide con el reporte enfrente si la apertura procede acotada.

§4 · ACTO P·LOTE-2 — segundo lote, firma al lanzar (caja · dos commits · mismo molde que §2)

GATE (script): PR del Lote-1 fusionado (su nota visible en forense/notas/) + firma de mesa de las ≤5 fuentes de este lote, pegada verbatim en el texto con que se lanza este acto. Sin esa firma el acto no lanza — este documento deja las candidatas, no la decisión.

Candidatas que la firma del corte dejó nombradas (mesa elige ≤5 al lanzar, con lo aprendido del Lote 1):

Palanca    Fuente    Necesidades    URL de la cola    Nota para la firma
9    WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023    3: N22,N23,N32    https://microdata.worldbank.org/catalog/6453    la nota de O advierte: "dato organizacional propietario" posible — valor real quizá menor que su conteo
11    GDELT    2: N17,N27    https://www.gdeltproject.org/data.html    UNA sola de la familia de eventos (GDELT/ACLED/MASS_MOBILIZATION_×3); las otras cuatro se reevalúan con lo que ésta arroje (§5 de la nota de O)
17    ENCOAP    2: N2,N30    https://www.inegi.org.mx/programas/encoap/2023/default.html    promovida en la firma del corte: INEGI, sirve N30 (R8.3), donde el hueco de dato más pesa; su condicional declara "no representa ámbito rural" — se adquiere sabiéndolo
8    MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_2006_2010    3: N22,N23,N32    VACIO    misma advertencia que palanca 9; par redundante con ella — probablemente UNA de las dos
sig.    lo que la cola disponga por palanca tras las anteriores    —    —    derivar del TSV en sesión, no de este documento

ENTORNO ASIGNADO: caja. NO en nube. PERÍMETRO Y CONCURRENCIA: idénticos a §2; en paralelo con M-APERTURA si mesa lo dispone (perímetros disjuntos: P toca corpus/manifiesto/capa2, M-APERTURA toca registro de aperturas).

Commits 1 y 2: idénticos al molde de §2 — lote congelado verbatim de la cola con criterio A.4/A.5 por fuente y la frase de siempre; ejecución con sonda A.5 + descarga a corpus + sha256 + vía del motor + conducto + PRISMA + PR#77. Registro gratuito se hace; pago/afiliación ⇒ NO-ACCESIBLE con receta.

§5 · ACTO Q — EMOVI (CEEY) + LAPOP: de cita huérfana a insumo T0 (caja · dos commits)

GATE: ninguno duro; cede la caja a P si compiten. ENTORNO ASIGNADO: caja. NO en nube.

Premisas (script):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
grep -ci "emovi" data/curacion-universo/fuentes-t0.tsv    # esperado 0; si ≥1, re-deriva el alcance y repórtalo
grep -ci "lapop" data/curacion-universo/fuentes-t0.tsv    # esperado 0; ídem
```

(Contexto, no premisa: LAPOP también vive en la cola de adquisición sirviendo N30, en el grupo de 8 fuentes sin condición mecánicamente consultable — §3.3 de la nota de O. Este acto la trabaja como insumo T0; si un lote futuro la firma, quien lo lance verifica primero qué dejó Q, para no duplicar.)

PERÍMETRO Y CONCURRENCIA. Toca: data/curacion-universo/fuentes-t0.tsv SOLO por la vía que el commit 1 determine · corpus/manifiesto si descarga · conducto · forense/notas/ (1) · encargos (A.3) · hallazgos (union). En paralelo: P entre lotes. Fuera de la lista, PARA.

Commit 1 — pre-registro: qué edición se busca (EMOVI: la vigente del CEEY; LAPOP: olas México), términos, portales candidatos (SIN-FETCH hasta abrir — A.6), criterio por clase A.4, y la pregunta de vía declarada y RESPONDIDA LEYENDO tools/curador_registro/ antes de tocar nada: ¿los insumos T0 son config/dato (lista que se extiende) o código (parser nuevo = modificación de motor)? La respuesta se escribe con archivo:línea. Frase de siempre.

Commit 2 — ejecución: sonda + descarga + sha256 + manifiesto + ficha/puerta, como en P. La vía del insumo: si es config/dato ⇒ se extiende y se corre el snapshot por el motor; si exige código ⇒ NO se modifica el motor aquí — el parser se entrega como PROPUESTA (archivo en forense/notas/ con el diff exacto) y el insumo queda EN-ESPERA-DE-VIA, citando la ventana pre-piloto de ADR-70(d) para que mesa decida el acto de motor. LAPOP con registro/licencia: se declara lo que exige; registro gratuito se hace; afiliación ⇒ NO-ACCESIBLE con receta manual.

Contador: 2 fuentes de cita-huérfana a estado registrado (adquiridas, en-espera-de-vía, o no-accesibles con razón escrita).

§6 · ACTO M-APERTURA — ENFIH 2019 + ENSAFI 2023 a nivel variable (caja · dos commits POST-DATO)

GATE (script): M-ADQ (§3) cerrado y fusionado — su nota visible y el universo mínimo por fuente en estado EN-CONDUCTO o con la decisión acotada de mesa si algo quedó NO-ENCONTRADO. Además:

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
awk -F'\t' '$3=="ENFIH" || $3=="ENSAFI"' data/curacion-registro/relaciones.tsv | awk -F'\t' '{print $3" capa3="$11}' | sort -u   # esperado: EXISTE;COINCIDE;INTEGRO en ambas — repórtalo crudo
ls data/raw/ | grep -ci "enfih\|ensafi"    # payloads en corpus vía symlink; reporta el valor
```

ENTORNO ASIGNADO: caja. NO en nube. PERÍMETRO Y CONCURRENCIA: registro de aperturas por la vía del motor · forense/notas/ (1) · encargos (A.3) · hallazgos (union). En paralelo: P·Lote-2 (perímetros disjuntos). Fuera de la lista, PARA.

Commit 1 — términos pre-registrados ANTES de abrir. Por necesidad objetivo — los 4 SIN-RUTA cerrados por régimen: sens_estatus ×2 y aversion_riesgo ×2 (filas 3/4/6/11 del censo forense/censo-estimabilidad-coeficientes-v1_0.md §5), más cualquier condicional faltante que el censo nombre con candidato FIN —: los términos de búsqueda por diccionario, el universo de apertura (qué tablas/cuestionarios, ahora con el universo documental de M-ADQ en mano, no encabezados), y el criterio de cada clase A.4. Frase de siempre.

Commit 2 — veredictos. Apertura byte a byte de diccionarios y cuestionarios. Por celda necesidad × fuente × reactivo: EXISTE-SATISFACE / EXISTE-NO-SATISFACE (qué falta) / NO-ENCONTRADO (universo+términos+fecha) / NO-ACCESIBLE; texto del reactivo, escala, tabla, co-observación C1-C4, es_panel, llave ADR-57(c). Conteos PRISMA del embudo. Todo entra por el motor del registro.

Qué NO hace: no reabre ADR-52A/54 — eso es de mesa, vía E-CE v1.1, con este reporte enfrente (hasta 4 SIN-RUTA en juego) · no calcula β · no promete lo que no aparezca. Contador: aperturas nuevas en el registro + el reporte que pone la decisión de reapertura en manos de mesa.

§7 · ACTO R — DESCUBRIMIENTO ACOTADO, un dominio por sesión (caja · dos commits por dominio)

GATE: después de los lotes 1-2 de P (los actos que mueven valores van antes que los que llenan disco — y R ni siquiera llena disco: busca). ENTORNO ASIGNADO: caja (o nube si el dominio no exige portales fuera de allowlist — declara cuál). NO en los dos.

Población cerrada de dominios — DERÍVALA en sesión, no la copies: los huecos ESTRUCTURALES del censo (filas 10 y 14: co-observación sin muestra común) + condicionales faltantes sin candidato en el registro. Un dominio por sesión.

PERÍMETRO Y CONCURRENCIA: puntero de puertas (FILAS nuevas por candidata clasificada — conducto) · forense/notas/ (1) · encargos (A.3) · hallazgos (union). Fuera de la lista, PARA.

Commit 1 — pre-registro del dominio: la necesidad exacta (reactivo+desenlace que deben co-observarse, o el puente) · términos de búsqueda · tipos de puerta admisibles (encuestas nacionales, registros administrativos, paneles académicos) · el criterio de suficiencia, escrito antes de buscar: la sesión termina cuando una pasada completa de términos no produce candidatas nuevas. Frase de siempre.

Commit 2 — el barrido: candidatas por buscador ⇒ SIN-FETCH (A.6, jamás promovidas sin abrir) ⇒ sonda/apertura de portada ⇒ clasificación A.4 con universo+mecanismo+fecha ⇒ fila en el puntero de puertas por candidata clasificada. Ninguna palabra prohibida; "no apareció con estos términos en estos portales" es el techo de cualquier negativa.

Qué NO hace: no baja microdato (eso vuelve por la cola/P si la candidata prospera) · no promete resolver lo estructural — su entregable honesto puede ser "el hueco sigue, y ahora con universo de búsqueda declarado". Contador: filas nuevas de puertas/candidatas, con el embudo contado.

§8 · LO QUE ESTE DOCUMENTO NO TOCA
U1→U2→U3: vivos en ENCARGOS-FINALES-cierre-brecha-U1-U2-U3.md, se intercalan donde quepan. Re-emitirlos aquí sería tener dos textos vigentes del mismo acto — el defecto de duplicación.
PR #184 (corrida de K): medición terminada esperando firma de mesa. No consume caja ni red; no compite con este plan; mesa la adjudica cuando decida. Lo único que no conviene es dejarla abierta tanto que main se le mueva encima.
ACTO L (liberación de las 8 de radio): repo-only, conforme a ADR-71(a); no es de adquisición. Su encargo vive en ENCARGOS-K-L-M-N-siguiente-paquete.md y sigue vigente tal cual.
Reapertura de ADR-52A/54 y de las NEGATIVAS de BRASDEFER/MOBILE_TUTORS: decisiones de mesa, con los reportes de M-APERTURA y E-CE v1.1 enfrente. Ningún acto de este documento las toma.

El costo de este documento, contado: cero reglas nuevas. Todo es aplicación de reglas selladas (A.3-A.6, ADR-59(b), ADR-69, ADR-70, ADR-71, Bloque D, R1/R2/R3) más las decisiones que solo mesa puede tomar, señaladas donde van: la firma del corte (§1, quizá ya consumida), la firma del Lote 2 (§4, al lanzar), la adjudicación de #184 y las reaperturas (§8).

---

## ADENDA-1 al §6 (ACTO M-APERTURA) — firmada por mesa, 14/ago/2026

*Archivada por ACTO C (14/ago/2026) como propagación de estado medido, no como adjudicación nueva. Las dos cifras que la adenda declara se re-derivaron contra el árbol post-#236 antes de archivarla, con el propio script del gate: **ENFIH 7 `EXISTE;COINCIDE;INTEGRO` · 5 `NO_REFERENCIADO` · 8 `SI_O_PARCIAL`; ENSAFI 7 · 4 · 9** — coinciden exacto. Texto de mesa, verbatim:*

> ADENDA-1 al ENCARGO M-APERTURA (§6 del plan de descargas, forense/encargos/2026-08-12-…-completo.md) · 14/ago/2026 · mesa. (a) El gate de arranque se corrige a la realidad post-ENLACE-1/2. El texto original esperaba EXISTE;COINCIDE;INTEGRO uniforme por fuente; hoy, medido sobre el árbol de #236, cada fuente trae TRES valores (ENFIH: 7 EXISTE;COINCIDE;INTEGRO · 5 NO_REFERENCIADO · 8 SI_O_PARCIAL — ENSAFI: 7 · 4 · 9). Gate nuevo, leído así y solo así: procede si cada fuente tiene ≥1 fila con capa3 EXISTE;COINCIDE;INTEGRO (hoy 7 y 7 — sobra); los valores mixtos son estado esperado del registro, NO disparan PARO. El PARO queda reservado a: cero filas íntegras en alguna de las dos, o hash discordante contra disco. (b) El acto CONSUME data/lista-apertura-enlace2-2026-08-14.tsv y, como parte de su perímetro ya declarado sobre capa4 (precedente ENLACE-1), corrige las 17 celdas cuyo rótulo INDEXADO-NO-DESCARGADO es hoy factualmente falso (son adjudicadas-no-referenciadas; #236 lo midió) al rótulo que su apertura arroje. (c) Su reporte es el insumo directo de la firma de pares (A3) — lo dice en su nota de cierre. Gates: esta adenda + #236 fusionado. Todo lo demás del §6 queda verbatim.

**Estado del §6 tras esta adenda:** los dos gates están **cumplidos** — la adenda existe (este commit) y `#236` fusionó en `origin/main` (`cf0dd68`, 14/ago). M-APERTURA queda **lanzable**.
