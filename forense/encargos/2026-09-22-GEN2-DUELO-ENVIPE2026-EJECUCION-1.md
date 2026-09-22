# ENCARGO · ACTO GEN2-DUELO-ENVIPE2026-EJECUCION-1 · El duelo prospectivo ENVIPE 2026 se congela con el payload presente, emite a ciegas, y adjudica abriendo la ola reservada solo con el código congelado

> ENTORNO: **CAJA** — abre ENVIPE 2018–2025 (emisiones) y, únicamente en COMMIT-3 y por `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001`, ENVIPE 2026. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** (spec y medidores congelados por `GEN2-DUELO-ENVIPE2026-CONGELA-1`/`COMMIT-1`; la latitud es logística) · CONTADOR: +2 corridas selladas y registradas (`EMISIONES-0001`, `ADJUDICACION-0001`), `cuenta_gen2 = SI`, **no adopta**; `celdas_validadas` sube por cada celda con veredicto (derivado); la reserva `reserva:envipe2026` pasa de RESERVADA a CONSUMIDA-POR-DUELO en COMMIT-3 · ids raíz de acto.

## 1 · OBJETIVO
Que el duelo diseñado en `GEN2-DUELO-ENVIPE2026-CONGELA-1`/`COMMIT-1` corra de punta a punta como su nota §4 lo dejó escrito: (1) `preflight` VERDE con `envipe2026_csv` COINCIDE; (2) `run` de las emisiones, ciegas a 2026; (3) COMMIT-3a: el sha de `EMISIONES-0001/resultados.json` en `ADJUDICACION-0001/spec.yaml` (`parametros.commit_3a`), nada más; (4) COMMIT-3: `run` de la adjudicación (abre 2026 solo ahí), sello, registro, veredicto con las palabras de la spec; nacional leído con `CALC-DUELO-ORIGEN-MOVIL-0001` a la vista (F7 A). «Hecho» = `verify` REPRODUCE en los dos CALC; `git log --format=%s` muestra COMMIT-2 antes de COMMIT-3a antes de COMMIT-3; ninguna lectura de `envipe2026_csv` en el historial antes del commit de COMMIT-3 (`git log -p -S envipe2026 -- data/corrida0/CALC-DUELO-ENVIPE2026-EMISIONES-0001` vacío); `decisiones.tsv` con la fila de consumo de la reserva.

## 2 · FIRMAS DE MESA
- Ya en el repo (se citan): `reserva:envipe2026` (`decisiones.tsv`: «bajar el payload está permitido; abrirlo, derivar de él o leer sus tabulados, no, **fuera del código que se congele para ello**. Rige E.6»); las dos FP de `GEN2-DUELO-ENVIPE2026-COMMIT-1` (`ejecutada_en`, según su nota §5).
- *Propuesta de dirección, mesa sella con el lanzamiento o borra:* «Se autoriza el COMMIT-3 del duelo ENVIPE 2026 —la única lectura de la ola reservada— exclusivamente por `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` congelado, con el sha de las emisiones escrito antes en COMMIT-3a. Fila L: NO-ENTRA (spec §5).» Sin texto → **PARO antes de COMMIT-3**; COMMIT-1 y COMMIT-2 sí se hacen.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `data/manifiesto.yaml:30381` `envipe2026_csv` con `sha256: dd79f589…`, anotación «RESERVA F7: solo se baja y se hashea, no se descomprime/lista/abre»; también `envipe2026_fd_pdf`, `_cuest_principal_pdf`, `_cuest_modulo_pdf`.
- `[LEÍDO]` `forense/notas/2026-09-21-GEN2-DUELO-ENVIPE2026-COMMIT-1-nota.md` §3 («COMMIT-1 de 2026 queda NO-CONGELADO por el requisito 1 (payload ausente) … la única edición autorizada es `preflight` VERDE sobre ese input — ningún parámetro, fórmula ni id cambia (spec §10)») y §4 (los cinco pasos que este OBJETIVO copia). `[EXISTE]` `data/corrida0/CALC-DUELO-ENVIPE2026-EMISIONES-0001/`, `…-ADJUDICACION-0001/` (`SPEC-FIJADA`), `CALC-DUELO-ORIGEN-MOVIL-0001` (sellado, REPRODUCE), `tools/duelo/` (3), `tests/test_duelo_prospectivo.py`.
- `[SUPUESTO]` `preflight` pasará con el payload ahora presente sin otra causa de bloqueo. Si resulta falso por **cableado puro** (D-18: ruta de spec, sha de input origen-repo, `dependencias_materiales`, `permite_no_estimable`), se corrige en commit propio declarado y no es PARO; si es otra cosa, PARO g).
- `[SUPUESTO]` El FD 2026 no cambió los reactivos de los desenlaces del duelo. **Antes de COMMIT-3** el acto lo verifica **por texto** contra `envipe2026_fd_pdf` (que sí puede abrir: es FD, no microdato); un reactivo con texto distinto → esa celda `NO-CONSTRUIBLE`, declarada, y el duelo sigue con las demás.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-DUELO-ENVIPE2026-*` → 2 (SPEC-FIJADA); `grep -c "envipe2026" data/corrida0/corridas.tsv` → reporta (al redactar, ninguna corrida abrió 2026); `grep "reserva:envipe2026" data/corrida0/decisiones.tsv` → RESERVADA. Ramas vivas: ninguna.

## 5 · PIEZAS
- **COMMIT-1 (congelación real):** `preflight` VERDE con `envipe2026_csv` COINCIDE; sha de spec/medidores pegados e idénticos a los de #968/#982; verificación por texto del FD 2026 (arriba). **Ninguna edición** salvo cableado D-18 declarado.
- **COMMIT-2 (emisiones ciegas):** `run` de `EMISIONES-0001` sobre 2018–2025; sello; asiento; registro. Test que asierta desde el historial que el directorio de emisiones no contiene ninguna lectura de 2026 (precedente piloto 2).
- **COMMIT-3a:** solo `parametros.commit_3a` en la spec de adjudicación.
- **COMMIT-3:** `run` de `ADJUDICACION-0001`; veredicto por contendiente y general con el vocabulario de la spec (`VENCE-AL-PISO` / `PROPUESTA-CON-RESERVA` / `NO-VENCE` / `C-PISO-ADOPTADO`, ADR del diseño); cobertura reportada con intervalo binomial por celda y por conglomerado (v2.16 §4); rótulo **PROSPECTIVA** en todo marcador (la emisión se selló antes de que existiera R). Registro y asiento en el mismo acto; `decisiones.tsv`: reserva consumida por este duelo, con la lista de lo que quedó sin abrir (si algo).
- **P5 · Lo que mesa lee primero:** una tabla como la del duelo ENIGH 2024 (`…ENIGH2024-DUELO-COMMIT-2-3-cierre.md` §4), sin adoptar.
- «si `[SUPUESTO]` resulta falso»: dicho en §3, por pieza.

## 6 · LATITUD
DECIDES TÚ: enlazar `data/raw`, dependencias, orden de los checks, ≤ 10 líneas adyacentes (cableado D-18) declaradas. PREGUNTAS A MESA (y sigues hasta COMMIT-3a): si el FD 2026 renumeró un catálogo y el mapeo por texto es inequívoco, ¿se aplica el mapeo declarándolo (recomendado) o la celda queda NO-CONSTRUIBLE? NO DECIDES: §7.

## 7 · PAROS
**a) cualquier lectura de `envipe2026_csv` fuera de `ADJUDICACION-0001` en COMMIT-3 — incluidos `head`, `unzip -l`, scratch** · b) editar spec/medidores congelados o forzar · c) adoptar · d) cambiar estimando, umbral, λ, candidatos o B-bis · e) nube · f) inalcanzable · g) el código congelado no corre → no se parcha.

## 8 · COMPUERTAS
«`preflight` VERDE con payload COINCIDE — protege: congelar spec.» «Firma de §2 presente — protege: abrir dato (COMMIT-3).» «Emisiones selladas en `origin` antes de COMMIT-3a — protege: abrir dato.»

## 9 · PERÍMETRO
Propio: los dos CALC del duelo (sus `ejecucion.json`, `resultados.json`, sellos; `spec.yaml` de adjudicación solo `commit_3a`) · derivados por comando · `replay-evidencia.tsv` · `decisiones.tsv` (una fila) · test propio (huérfano en CI) · nota · `canon/L0/<raíz>.md` · celda-D/marcador **no** (su dueño; se le deja el veredicto por id). Ajeno: `tools/duelo/` (lectura), `CALC-DUELO-ORIGEN-MOVIL-0001`, todo lo demás. Otro acto en vuelo: ninguno verificado; ningún otro acto de caja mientras corre. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no corre L, no toca la celda-D ni el marcador (sucesor: su dueño consume el veredicto). Auditoría: la spec ya la trae (afirma sobre México); la nota la contesta de nuevo sobre el resultado. Cierre por /acto.


