ENCARGO · ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA

SHA de redacción: ea45e01 · 3/sep/2026, dirección (Fable) · v2.12 · Estado: LISTO PARA LANZAR — COMPUERTA: ninguna (los payloads ya están en origin/main:data/manifiesto.yaml, ids abajo).

ENTORNO ASIGNADO: UBUNTU (los .xls viven en descargas_mx/Descargas Manuales/). NO en NUBE. MODELO SUGERIDO: Opus (medidor de dos commits con falsador declarado por el modelo).

Invoca /acto. A.2 de tres partes: la tercera es ls "$(python3 -c 'import yaml;print(yaml.safe_load(open("data/raices.local.yaml"))["descargas_mx"])')/Descargas Manuales" | grep -c '\.xls$' → reporta el valor (dirección espera ≥ 9).

CARRILES: ver cabecera. Ningún otro acto toca milpa/procedencia.yaml ni milpa/tramite.yaml; este tampoco los edita.

FIRMAS DE MESA — verbatim. 2/sep/2026, firma p1 sobre MAESTRA34-L6 (transfer §4, ya propagada por N5/ADR-299): «tasa nacional ENDUTIH FUERTE como campo, no conducta». Es el precedente para que una tasa administrativa agregada entre al motor como campo. Y la firma c1 corregida, verbatim: «lo que hay descargado no es el universo desconocido sino el conocido» → coercitivo quedó NO-ENCONTRADO con universo declarado (ENCIG 2011-25, ENDUTIH 23/24/25, ENIF 2024, ENCUCI 2020, CoDi; NO-ACCESIBLE SAT/CNGF). Este acto amplía ese universo con el SAT ya en disco; no toma ninguna decisión nueva.

═══ VERIFICACIÓN DE EXISTENCIA (A.8), contra ea45e01 ═══ (1) ESTRUCTURA. Regla: milpa/tramite.yaml, entrada tramite.gobierno_digital.coercitivo (rechaza_servicio 0.91 / adopta 0.09, ambos ASIGNADO, tier MEDIA-FUERTE, falsable_si: "Si un servicio coercitivo con riesgo fiscal lograra adopción masiva, la regla se rompe", sin_dato_universo_examinado con firma c1). Procedencia: milpa/procedencia.yaml:795-798 («3.09M cuentas en 6 años es un volumen absoluto; 0.91 no se deriva de ahí»). Acumulador: milpa/tramite-ola5-propuesta-v0.yaml. Payloads: data/manifiesto.yaml. (2) CONTENIDO. grep -aE '^- id: (firelenumcert|firelenumcontri|portipocontribuyente|porentfed|decanuatipcon|ingresostributarios)' data/manifiesto.yaml → 6 (universo 1 102 ids); rutas Descargas Manuales/FirEleNumcert.xls, …/FirEleNumcontri.xls, …/PorTipoContribuyente.xls, etc.; fila SAT_MEXICO del registro → OBTENIDO (A1, «identidad verificada abriendo las hojas con xlrd»). → EXISTE, satisfacción por decidir en P0. Medición previa de coercitivo contra SAT: grep -ac 'FirEleNum' milpa/ forense/notas/ -r → reporta; dirección espera 0. → NO-ENCONTRADO (medición), universo milpa/ + forense/notas/. (3) COBERTURA RETROACTIVA. Los .xls entraron al manifiesto el 2/sep por ADR-310; ningún acto anterior pudo verlos (--escanea no entraba a subcarpetas). No hay trabajo invisible.

SPEC POR PIEZA (dos commits en P1: spec antes de abrir cifra alguna)

P0 · Censo A.4 de los 9 .xls, sin calcular nada. Por hoja: qué mide, unidad, periodo, si trae numerador (contribuyentes con e.firma vigente; buzón tributario habilitado si existe) y denominador (padrón activo total; por tipo — personas físicas asalariadas / con actividad empresarial / morales). Veredicto por objeto: EXISTE-SATISFACE / EXISTE-NO-SATISFACE (qué falta: p. ej. no distingue obligados de no obligados) / NO-ENCONTRADO. Si ningún par numerador/denominador comparte periodo y universo → PARO de pieza P1 con la tabla como entregable (misma salida que L5 P0 sobre ENCIG).

P1 · Tasa de adopción de e.firma (o buzón) entre obligados — COMMIT-1 antes de abrir la cifra. Estimando: p = (contribuyentes con e.firma vigente) / (padrón activo del universo obligado), último año completo disponible, y serie por año si el par existe en ≥3 años. Universo obligado: el que P0 defina con el diccionario del SAT, no por supuesto — si el .xls no permite excluir a los no obligados, se declara cota inferior sobre padrón total y se dice. Escala declarada (A-bis 3): proporción administrativa agregada, campo del entorno, no probabilidad individual de conducta; comparable con el 0.09 asignado solo en signo y orden de magnitud, nunca como «difiere en Z %». Falsador B-bis, congelado antes de ver el número: la regla dice adopta 0.09 bajo coerción con riesgo fiscal; (i) si p ≥ 0.50 → CONTRARIA por el propio falsable_si de la regla («adopción masiva»); (ii) si 0.20 ≤ p < 0.50 → ACOTADA: adopción no masiva pero un orden de magnitud sobre el prior; (iii) si p < 0.20 → CORROBORADA-PARCIAL (sin IC de diseño: es un censo administrativo, la incertidumbre es de definición de universo, no muestral, y se cuantifica con la cota inferior/superior del denominador). Precedencia: si la cota inferior y la superior caen en filas distintas → AMBIGUA-POR-UNIVERSO, no adjudica. Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta». COMMIT-2: resultado, sin editar el primero.

P2 · Entrada al acumulador, PENDIENTE-DE-MESA. Al pie de la propuesta: tramite.gobierno_digital.coercitivo con MEDIDO·p (campo administrativo SAT), fuente firelenumcontri + portipocontribuyente (ids del manifiesto), periodo, universo, cotas, veredicto, y la nota de que no es conducta individual (precedente p1). No se toca tramite.yaml ni procedencia.yaml: ese es el sello, y es de mesa (sin_dato_universo_examinado se amplía en el acto sucesor, no aquí).

PERÍMETRO Y CONCURRENCIA. Toca: tools/medidor_l13_sat_efirma.py (nuevo) · data/l13-sat-efirma-v1_0.json · data/INFRAESTRUCTURA-v1_0.md (alta del artefacto, §0.11) · milpa/tramite-ola5-propuesta-v0.yaml (append al pie, 0 borradas) · forense/notas/2026-09-0X-MAESTRA36-L13-*.md · forense/hallazgos.md · forense/firmas-pendientes.tsv · cascada. NO toca: milpa/tramite.yaml, milpa/procedencia.yaml, data/manifiesto.yaml, data/curacion-registro/**, los .xls (lectura únicamente). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

CONTADOR. Priors ASIGNADO sin dato: S1 1 → 0 si P1 produce p (es el contador de la línea 1 del tablero de programa); si P0 para, 1 → 1 declarado. Cargas al motor: 0.

Lo que NO hace. No sella; no amplía sin_dato_universo_examinado (sucesor); no descarga nada del SAT; no interpreta «adopción» como voluntariedad — la regla habla de coerción, y el dato mide cumplimiento bajo coerción, que es exactamente lo que el falsable_si pregunta.

Sucesores. N11 · SELLA-L13 (nube, con letra de mesa: cargar como campo o como conducta, ampliar sin_dato_universo_examinado, ajustar tier).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA` el 3/sep/2026, entorno
UBUNTU con corpus montado, worktree `/home/pc0/mm-maestra36-l13`, rama
`acto/maestra36-l13-coercitivo-sat-efirma`, base `origin/main = ea45e01` (el SHA
de redacción exacto; `main` no se movió durante el acto). `ADR-311`.

Commits: `ea3bf92` (`0-bis A.3`, este archivo) · `ef144d1` (`COMMIT-1`: spec y
falsador congelados + `P0` censo `A.4`) · `e9c2e31` (`COMMIT-2`: `P1` resultado +
`P2` acumulador) · el commit de cascada que trae este `## CONSUMIDO`.

Resultado: **`AMBIGUA-POR-UNIVERSO`** — `p_inf` `0.3684` (tramo `ACOTADA`),
`p_sup` `0.9211` (tramo `CONTRARIA`), tramos distintos, el acto **no adjudica**.
`P0` no paró. Cargas al motor: 0. Recibo `FP-260` para `N11 · SELLA-L13`.

Desviación declarada frente a la premisa del encargo: el control
`grep -ac 'FirEleNum' -r milpa/ forense/notas/` dio **5**, no el 0 esperado —
las cinco en `forense/notas/2026-09-02-MAESTRA36-A1-P0-barrido.md`, que es el
acto de adquisición que las registró, no una medición de la regla; en `milpa/`,
0. El veredicto `NO-ENCONTRADO` (medición) que el encargo pedía se sostiene.
