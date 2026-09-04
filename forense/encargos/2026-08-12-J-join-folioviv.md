- **SHA de redacción:** `3e071f0` (Merge PR #175, `origin/main`, 12/ago/2026) — verificado exacto contra `origin/main` al arranque de este acto, 0 commits de diferencia.
- **Entorno asignado:** CAJA LOCAL (microdato ENIGH en disco). NO nube, NO contenedor de chat, NO en paralelo en otro entorno.
- **Estado:** CONSUMIDO — PR de la rama `mesa/j-join-folioviv` (dos commits: `7525b70` especificación congelada, y el commit de resultados/arreglo que lo sigue). Detalle en `forense/notas/2026-08-12-j-alcance-folioviv.md`.

---

ENCARGO FINAL · CAJA LOCAL · ACTO J — medir el alcance de folioviv, aplicar la normalización y proponer remediación (DOS COMMITS)
12/ago/2026 · borrador de Opus ADJUDICADO por dirección: APROBAR CON SEIS AJUSTES, integrados abajo · construcción bajo R1 (cero citas fuera del repo) · R2 (premisas como script) · R3 (abre en paralelo; se serializa el merge)

ADJUDICACIÓN DEL BORRADOR (para el registro). El diseño de Opus es correcto en lo que importa: dos commits POST-DATO, la normalización heredada de e4c commit 3 y no reinventada, el test de cobertura por entidad que validar_contra_publicado() nunca dio, las dos reglas A-bis (escala nativa por veredicto; universos distintos no se comparan sin decirlo), el alcance acotado (medir, no adjudicar), y "magnitud despreciable = entregable". Seis ajustes de dirección, verificados por comando contra origin/main = 3e071f0:

El gate se vuelve comando, no espera ciega. "Espera el merge de #176" era necesario cuando no sabíamos si e4c tocaba estos archivos. Verificado hoy: git diff --name-only origin/main...origin/e4c/r5-1-d2 ∩ {r5_1_pension, p3_lca} = ∅. El gate real es esa intersección vacía, re-derivada en sesión (script abajo) — J puede abrir sin esperar #176, con hallazgos.md resuelto por merge=union y rebase local (R3). Si e4c empuja algo que vuelva la intersección no-vacía a mitad del acto: PARA.
La ambigüedad medir-vs-arreglar se resuelve por escrito: este acto SÍ aplica la normalización zfill(10) a los scripts del perímetro y SÍ deja el test nuevo pasando en HEAD — y NO re-corre ningún protocolo ni produce veredictos: los veredictos sellados citan sus SHAs y quedan intactos y reproducibles en su historia. Arreglar sin re-correr es correcto en ambos escenarios de mesa (si la magnitud es despreciable, los scripts quedan sanos para usos futuros; si es grande, las re-corridas usan los scripts ya sanos).
ADR-NN(c) era una cita fantasma (clase R1). El mecanismo de vencimiento se cita con su ancla real: ADR-67, preámbulo (canon/gobernanza-v1_15.md:862 y ss.) — "un sello cuyo universo creció queda VENCIDO EN ALCANCE… la anterior conservada verbatim".
"Todas las olas en disco" era premisa afirmada, no derivada. Derivado hoy del manifiesto: ENIGH 2012 · 2014 · 2016 · 2018 · 2020 · 2022 (seis olas). El ejecutor re-deriva en sesión; el universo del commit 1 es lo que su derivación dé.
La huella de entorno se precisa: este acto NO necesita red. La sonda es solo huella: cloud_default = nube = PARA; sin_variable + sonda 403 = contenedor de chat = PARA; sin_variable + 200 (o sin red pero con el corpus montado) = caja local = adelante.
El test demuestra que faltaba: antes de aplicar el arreglo, corre el test nuevo UNA vez contra el código pre-arreglo y archiva la falla en la nota — esa corrida es la prueba de que validar_contra_publicado() pasaba verde con el join roto.

════════ ARRANQUE — hazlo antes de leer el resto ════════ 1 · REPO: clon existente; ruta · git log -1 · git status. No arranques del home. 2 · SHA: compara con 3e071f0; si main avanzó, re-deriva y reporta. 3 · data/raw: se enlaza a la raíz del corpus (data/raices.local.yaml); este acto NO descarga. 4 · ENTORNO: huella según ajuste 5 — reporta los dos valores crudos. 5 · ESPEJO: nada del espejo. ═══════════════════════════════════════════════════════

ENTORNO ASIGNADO — y el que NO. Caja local (microdato ENIGH en disco). NO nube, NO contenedor de chat, NO en paralelo en otro entorno.

PERÍMETRO. SOLO: tests/r5_1_pension_bienestar.py · tests/p3_lca_data.py y hermanos que crucen la misma llave (grep -rln "folioviv" tests/ tools/ lo deriva; repórtalos) · un test nuevo (tests/test_join_folioviv.py) · forense/notas/ (1 nota) · forense/hallazgos.md (append, cierre) · forense/encargos/ (este encargo archivado). NO toca: canon/, milpa/, data/curacion-*, el bloque append-only de hitoD-preregistro, ni archivos de las ramas vivas. La adjudicación de R5.1/D5 es acto propio de mesa, posterior. Fuera de la lista: PARA.

PASO 1 · Premisas (script literal — un PARA detiene y se reporta con salida cruda)
```bash
set -u; cd "$(git rev-parse --show-toplevel)"; git fetch -q origin
i=$(git diff --name-only origin/main...origin/e4c/r5-1-d2 2>/dev/null | grep -cE "r5_1_pension|p3_lca" || true)
[ "${i:-0}" = "0" ] && echo "PASA interseccion-e4c-vacia" || echo "PARA e4c-toca-mis-archivos($i)"
grep -oE "enigh[_-]?20[0-9]{2}" data/manifiesto.yaml | grep -oE "20[0-9]{2}" | sort -u | tr '\n' ' '   # universo de olas — repórtalo
grep -q "2018" <(grep -oE "enigh[_-]?20[0-9]{2}" data/manifiesto.yaml) && echo "PASA ola-2018-presente" || echo "PARA sin-2018"
ls tests/r5_1_pension_bienestar.py tests/p3_lca_data.py >/dev/null && echo "PASA scripts" || echo "PARA scripts"
```
COMMIT 1 — especificación congelada, ANTES de abrir ningún dato

Declara, y cierra con la frase "el primer resultado que produzca este procedimiento es el que se reporta":

Qué se mide: por cada ola de ENIGH en disco (las que tu derivación dé; 2018 es la única verificada con el defecto y 2022 está limpia — ninguna otra se ha mirado), la proporción de filas de poblacion e ingresos con folioviv de 9 caracteres, y la lista de entidades afectadas. Ola por ola, tabla por tabla.
Cómo: la normalización es folioviv.str.zfill(10), ya declarada y verificada por e4c commit 3 contra el valor real de concentradohogar. No se reinventa.
El test que faltaba: tests/test_join_folioviv.py ejercita el join con cobertura por entidad y falla si alguna entidad pierde filas silenciosamente. validar_contra_publicado() no lo hace — solo suma columnas de concentradohogar — y por eso pasó verde con el join roto. Jamás silencies; si --baseline gana entradas, repórtalas.
El efecto sobre los estimandos, en escala declarada (A-bis regla 3): la diferencia se reporta en la escala nativa de cada veredicto — R5.1 y D5 — y no se compara a través de escalas. Si están en escalas distintas, se reportan por separado y no se agregan.
Universo, declarado por ola: qué tablas, qué llave, qué filas entran. Y la advertencia de A-bis regla 4: si el arreglo cambia la composición del universo estimado, el marginal corregido no se compara contra el marginal viejo sin decir que son universos distintos.
Qué NO se hace aquí: no se re-corren R5.1 ni P3-LCA para producir veredictos nuevos; no se toca el bloque append-only; no se adjudica nada.
COMMIT 2 — resultados y arreglo, sin editar el commit 1
La demostración del hueco: corrida única del test nuevo contra el código pre-arreglo, falla archivada en la nota (ajuste 6).
La magnitud: por ola y por tabla — proporción de filas con folioviv de 9 caracteres, entidades afectadas, y filas que el join viejo perdía (conteo directo: llaves de 9 que no casan sin zfill).
El arreglo: normalización aplicada a los scripts del perímetro; test nuevo pasando en HEAD; suite --baseline cruda.
El plan de remediación, PROPUESTO a mesa: (i) qué actos re-correr y en qué orden; (ii) qué veredictos quedan expuestos (R5.1→A de ADR-58; D5-INESTABLE de ADR-53) y cuánto se moverían, si es que se mueven, en su escala nativa; (iii) costo estimado. Si la magnitud resulta despreciable, decirlo es el entregable — descartar con rigor no es fracaso y ahorra dos re-corridas. Si la especificación estaba mal, lo dice un tercer commit — nunca se corrige hacia atrás.
CIERRE

Rebase local sobre origin/main fresco (driver union en el árbol; el editor web de conflictos está prohibido), PR mesa/j-join-folioviv sin conflicto, NO FUSIONAR. Siete líneas. Contador esperado: filas nuevas de registro con la magnitud por ola. La adjudicación de R5.1/D5 no la hace este acto — y si mesa la hace después, es entrada fechada nueva que vence en alcance a la anterior, con la anterior conservada verbatim (ADR-67, preámbulo, gobernanza:862). Regla de señal: este acto MIDE; si a mitad aparece algo que desbloquea un cálculo mayor, eso vale más que terminar el acto — repórtalo y para.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-12-J-join-folioviv.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-12-j-alcance-folioviv.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
