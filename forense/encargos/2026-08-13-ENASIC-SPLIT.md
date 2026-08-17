# ENCARGO ENASIC-SPLIT · CAJA con corpus · dos medidas donde hoy hay una

- **SHA de redacción:** `19d885d` (`origin/main`, merge PR #200/wt-apertura-issp-1786589980, que a su vez ya trae fusionado PR #202/capa3-reconcilia — confirmado: es exactamente el commit sobre el que se abrió el worktree `~/mm-enasic-split` de este acto, `python3 tests/bitacora.py --abre` sin divergencia HEAD/origin-main)
- **Entorno asignado:** CAJA con corpus (Ubuntu/WSL local, worktree dedicado). **NO** se lanza en la nube: este acto abre `data/raw/enasic2022/` (PDF + diccionario xlsx) de primera mano — la nube no trae `data/raw` montado (mismo criterio declarado por E4b/PR #173 y U1/PR #185 para el mismo corpus).
- **Estado:** CONSUMIDO — PR #206 (rama `enasic-split`). *(Re-verificado 17/ago/2026, ACTO E-HIG/HIGIENE-VIVOS, contra `f3873c2`: `git merge-base --is-ancestor 959006a f3873c2` OK; `forense/notas/2026-08-13-enasic-split-verificacion.md` en el árbol.)*

---

Texto del encargo, verbatim, tal como se recibió:

---

4 · ACTO ENASIC-SPLIT — dos medidas donde hoy hay una
Cierra D3 · Entorno: CAJA con corpus · Sin gate
Por qué, y las dos cosas sin verificar

Mesa decidió partir: norma de género por un lado, obligación medida por otro — dos medidas, dos análisis. Es mejor que lo que ADR-67(b) selló, y por eso este acto enmienda ese inciso en vez de aplicarlo.

Pero hay dos supuestos que nadie ha verificado y de los que depende que la partición sea posible:

(1) El reactivo es UN ítem con un paréntesis: "Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos." Eso admite dos lecturas: (i) el entrevistador lee la versión que corresponde al sexo del informante — y entonces la partición sale sola, porque el acuerdo por sexo es interpretable; (ii) es fórmula genérica y no hay dos versiones que diferenciar. Se resuelve abriendo el cuestionario. data/manifiesto.yaml tiene enasic_2022_889463927082 (enasic2022/889463927082.pdf, usado_para: sin uso asignado) — empieza por ahí, y si no es el cuestionario, dilo y busca en el fd_xlsx.

(2) El candidato de "obligación medida" es débil. ABRIR-4 describe P6_38 ("¿usted las cuida por... obligación?") como "variable única, código válido '1', sin desglose visible de otras razones en el diccionario — posible batería incompleta, no perseguido más allá en este acto". Puede no sostener una θ. Verifícalo en el diccionario antes de proponerlo.

COMMIT 1 — pre-registro

Qué se busca en el cuestionario para resolver (1) · qué se busca en el diccionario para resolver (2) · y el criterio de qué constituye "dos medidas separables", escrito antes de mirar: no basta con que existan dos variables, tienen que medir constructos distintos y decirse cuáles. Falsación (B-bis): si el cuestionario resuelve (1) por la lectura (ii) —fórmula genérica—, la partición no es posible con este instrumento y eso es el resultado. Se reporta, no se fuerza. Y si P6_38 no sostiene θ, se dice y la obligación medida queda sin operacionalización, con lo que haría falta.

COMMIT 2 — veredicto

Las dos medidas propuestas, cada una con: variable, texto literal, escala, tabla, N, y qué constructo ampara. Más el diff exacto de la enmienda a ADR-67(b) para que mesa la firme — este acto no la sella. Contador: si la partición procede, condicionales 9 de 14 se mueve cuando mesa firme; este acto no lo mueve.

---

**Nota de arranque sobre este texto (no forma parte del encargo, es glosa de quien lo ejecuta):** el encargo no trae el bloque ARRANQUE de `instrucciones-proyecto` Bloque D ni declara PERÍMETRO Y CONCURRENCIA explícitos — ambos se derivan y reportan en `forense/notas/2026-08-13-enasic-split-verificacion.md` §0, no se inventan aquí. "D3" (línea 2 del encargo) no correspondió a ningún identificador rastreable en `canon/` ni en `forense/hallazgos.md` tras búsqueda dirigida (ver la misma nota, §0) — se interpreta como numeración externa de mesa (este acto es el "4·" de una lista propia de mesa), no como un ID que este acto deba resolver dentro del canon; no bloquea, el resto del encargo es autocontenido.
