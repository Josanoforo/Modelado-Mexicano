# MAESTRA33-C1 · RE-SPEC-CORRESIDENCIA — COMMIT-1 (spec congelada, antes de abrir el desenlace)

Acto: `MAESTRA33-C1`. Encargo archivado: `forense/encargos/2026-08-31-MAESTRA33-C1-RESPEC-CORRESIDENCIA.md` (A.3, verbatim). Ejecuta `FP-204`. Worktree `/home/pc0/mm-c1-respec-corresidencia`, rama `acto/maestra33-c1-respec-corresidencia`, HEAD de arranque `6a12244` (== `origin/main` exacto, 0 commits de diferencia con el SHA de redacción — sin drift que reconciliar).

**Nota de modelo.** El encargo sugiere `Opus` ("medidor de dos commits"); D-13 dice "quien lanza puede subir de modelo, nunca bajar en actos que midan". Esta sesión corre en `claude-sonnet-5`, fijo para la sesión — no es una decisión de este acto y no puede corregirse desde aquí. Se declara, no se oculta. Compensación aplicada: cada afirmación cuantitativa de este documento está verificada por comando propio (no heredada de sub-agentes de reconocimiento sin reverificación), con la salida cruda pegada.

## §0 · Premisas verificadas contra el árbol (no heredadas del encargo)

- **ARRANQUE completo** (skill `/acto`, `.claude/commands/acto.md`, `ADR-237`): REPO (worktree nuevo sobre `origin/main`), SHA (0 commits de diferencia con `6a12244`), `data/raw` (ausente al crear el worktree — gitignorado, como espera Bloque D; enlazado a `/home/pc0/mm-corpus/raw`, 321 entradas), ENTORNO A.2 (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`=`sin_variable`; sonda red `https://www.inegi.org.mx/`→`200`; corpus compartido montado, confirmado), ESPEJO (ninguna cifra de este documento sale del espejo del proyecto).
- **COMPUERTA**: el encargo declara "COMPUERTA: ninguna de merge" — no hay línea `GATED a X`; no aplica verificación de compuerta.
- **PRECONDICIÓN EDER 2017**: `data/raw/eder2017/` contiene 6 archivos (`eder2017_bases_csv.zip`, `_dbf.zip`, `_dta.zip`, `_sav.zip`, `_descripcion_calculoR.pdf`, `_fd.pdf`) — verificado con `find -L` (el `find` sin `-L` sobre el symlink de `data/raw` da 0 archivos, falso negativo A.13 detectado y corregido en el propio arranque). **No es PARO.**
- **Hash del payload**, verificado por comando propio (no heredado de manifiesto ni de sub-agente): `sha256sum data/raw/eder2017/eder2017_bases_csv.zip` → `bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3` — coincide exacto con `data/manifiesto.yaml:4331` (id `eder_2017_eder2017_bases_csv`). `usado_para: sin uso asignado` en el manifiesto es un campo obsoleto (ya señalado por [[feedback_manifiesto_usado_para_stale]]): el payload sí fue usado, por `ACTO MAESTRA32-E16`/`E18`.
- **A.8, re-verificado independientemente** (no se acepta el "ya lo verifiqué" del encargo sin re-correrlo, [[feedback_encargo_premisa_se_verifica_contra_el_arbol]]):
  - `milpa/tramite-ola5-propuesta-v0.yaml:93-117` (líneas reales confirmadas por `sed`) contiene únicamente la entrada `DEVUELTA-POR-MESA · FP-200=b · 31/ago/2026`: cabecera con la firma de mesa verbatim, la re-especificación nombrada (ventana=actual, instrumento=EDER, ejecutor=caja), y el cuerpo intacto (`p: 0.996086`, `ic95: [0.994794, 0.997250]`, `n: 14887`, `ponderador: factor`, `universo:` con la fórmula `padre_cor/madre_cor/hnos_cor/suegro_cor/suegra_cor`). Confirmado byte a byte.
  - `grep -n "corresidencia" milpa/tramite.yaml` → 1 coincidencia, línea 175, y es un **comentario** ("# NO se carga familia.corresidencia.adulto_familiar: mesa la DEVOLVIO a..."), no una regla cargada. `tramite.yaml` tiene 8 reglas totales (confirmado por la narrativa de `FP-205`: "motor 5 -> 8 reglas"); `corresidencia` aparece en 0 de esas 8. Coincide exacto con el "0 de 8" del encargo.
  - `FP-204` (`forense/firmas-pendientes.tsv:196`) existe, `ABIERTA`, texto idéntico al citado por el encargo. `FP-200` (`:192`) `FIRMADA`, con la cita verbatim de mesa "sellar 4 y devolver familia.corresidencia a re-especificacion... la re-especificacion obvia es ventana actual (corresidencia hoy), medible en el mismo EDER." — confirmado, no parafraseado.
  - Conclusión A.8: **la re-spec no existe medida en ningún punto del árbol** (`grep -rl "adulto_familiar_actual" .` → vacío, 1 archivo de patrón buscado en todo el árbol salvo `data/raw` y `.git`, A.13). El encargo procede.

## §1 · Qué se hereda de la corrida del 0.996 (releído del cuerpo intacto y de su procedencia — no de memoria)

Releídos: `milpa/tramite-ola5-propuesta-v0.yaml:80-126`, `tools/tasas_base_fase1.py` (398 líneas, completo), `tools/medicion_familismo.py` (672 líneas, completo, citado por la propuesta como fuente del universo/colapso), `forense/notas/2026-08-31-reglas-fase1-spec.md`, `forense/notas/2026-08-31-reglas-fase1-cierre.md`.

- **Instrumento**: EDER 2017, mismo payload (`sha256` arriba).
- **Universo base heredado**: `vivienda.csv` con `tipo_adqui` no vacío tras `strip()` ("no blanco"). Verificado por comando propio sobre el CSV real: **14,690 viviendas no-blanco de 23,548 totales** — coincide exacto con el `n_universo_viviendas_tipo_adqui_no_blanco: 14690` que reporta `forense/notas/2026-08-31-reglas-fase1-cierre.md:53`. Confirma que mi lectura del CSV reproduce la del acto anterior.
- **Ponderador heredado**: columna `factor` de `vivienda.csv`.
- **Estimador heredado**: proporción ponderada — `Σ(factor_i · desenlace_i) / Σ(factor_i)` (`tools/tasas_base_fase1.py:51`).
- **IC95% heredado**: bootstrap 10,000 réplicas, `seed=42`, remuestreo simple con reemplazo de filas-persona (NO por UPM/estrato, aunque `vivienda.csv` sí trae `est_dis`/`upm` — la corrida del 0.996 declaró explícitamente el fallback a bootstrap simple para las 5 reglas de fase 1 por no tener "un estimador de diseño reproducible... en la corrida única"). `seed=42` está firmado por mesa: `FP-168`, `FIRMADA` 30/ago/2026, ACTO MAESTRA32-E9 · PROPAGA-2, verbatim: *"Las decisiones que tomamos intégralas ya como firmadas."* — `nivel_ic=0.95, seed=42`. Método del IC: percentil (2.5/97.5).
- **Dicotomización de parentesco heredada, con una imprecisión que se hereda declarada, no corregida**: la corrida 0.996 define `desenlace=1` si `padre_cor='1' ∨ madre_cor='1' ∨ hnos_cor='1' ∨ suegro_cor='1' ∨ suegra_cor='1'` en cualquier fila de `historiavida.csv` para esa persona (`tools/medicion_familismo.py:86,143-146`; `tools/tasas_base_fase1.py:260`). El nombre de la conducta (`coreside_con_ascendiente_o_suegro_en_algun_momento_de_vida`) dice "ascendiente o suegro", pero el cómputo real incluye `hnos_cor` (hermanos) — ninguna nota de las cuatro revisadas (spec/cierre de fase1, spec de lote-nube-1, la propuesta yaml) explica ni señala esta discrepancia; se hereda mecánicamente de `medicion_familismo.py` sin re-examinarse. **Este acto no corrige esa imprecisión hacia atrás** (la entrada `DEVUELTA` no se toca, ni una letra). Para la ventana ACTUAL, §2 explica por qué el instrumento actual no permite replicar el componente `hnos_cor` de todos modos — la restricción hace la pregunta parcialmente moot, ver abajo.

## §2 · Qué cambia — la ventana, y lo que la ventana fuerza a cambiar con ella

**Hallazgo estructural (verificación de la restricción antes del diseño, v2.2): ni `tools/medicion_familismo.py` ni `tools/tasas_base_fase1.py` contienen NINGUNA lógica de ventana temporal sobre `historiavida.csv`.** El colapso "alguna vez en la vida" es simplemente "cualquier fila del panel retrospectivo de esa persona, sin restricción". No existe un parámetro que se pueda voltear; la ventana ACTUAL exige una variable distinta, de una tabla distinta.

**La variable ACTUAL**: `persona.csv` (mismo ZIP, `sha256` arriba; ruta interna confirmada con `zipfile.namelist()`: los 5 miembros están en la raíz del zip, sin carpeta anidada — `persona.csv, vivienda.csv, antecedentes.csv, historiavida.csv, hogar.csv`), columna `parentesco`. Es el roster de hogar de la ENH 2017 (el "marco" sobre el que se monta EDER 2017), pregunta B5 "¿Qué es (NOMBRE) del jefe?" (`eder2017_fd.pdf`, entrada #8, pág. 37). Códigos verificados contra el FD y contra el encabezado real del CSV: `1=Jefe(a) · 2=Esposa(o)/compañera(o) · 3=Hija(o) · 4=Nieta(o) · 5=Nuera o yerno · 6=Madre o padre · 7=Suegra(o) · 8=Otro · 9=Sin parentesco`.

**El hallazgo que gobierna todo el diseño de este COMMIT-1**: `parentesco` está codificado **relativo al jefe(a) de hogar**, no relativo al entrevistado EDER. No existe columna `id_padre`/`id_madre` ni ninguna otra que ligue a un integrante con su propio ascendiente/suegro directamente — la única relación registrada es "respecto al jefe". Verificado empíricamente (no solo por el FD) abriendo `persona.csv`+`historiavida.csv`+`antecedentes.csv` completos (lectura estructural, no de desenlace — ver nota de perímetro abajo):

```
personas únicas en historiavida.csv:  23,831  (idéntico a antecedentes.csv, mismos ids exactos — mismo universo respondiente, edad 20-54, confirmado min=20 max=54)
distribución de parentesco PROPIO del entrevistado, entre esas 23,831 personas:
  1 (Jefe):          9,771  (41.0%)
  2 (Cónyuge):        6,916  (29.0%)
  3 (Hijo/a):          5,565  (23.4%)
  5 (Nuera/yerno):       561   (2.4%)
  8 (Otro):              474   (2.0%)
  4 (Nieto/a):           290   (1.2%)
  9 (Sin parentesco):    206   (0.9%)
  6 (Madre/padre):        30   (0.1%)
  7 (Suegro/a):           18   (0.1%)
```

Para `ego` con parentesco propio ∈ {1,2}, la traducción a "mi ascendiente/suegro está en este hogar" es directa y sin ambigüedad (leer los códigos de los demás integrantes del mismo `folioviv+foliohog`, invertidos si `ego`=cónyuge, porque "madre/padre DEL JEFE" y "suegro/a DEL JEFE" cambian de referente según quién es `ego`). Para las demás posiciones la traducción **no** es limpia: para `hijo/a`, el jefe está SIEMPRE presente por diseño del roster (pregunta B1 empieza "por la jefa o el jefe") y ES su ascendiente — es decir, "ascendiente presente" sería tautológicamente 1 para todo `hijo/a`, no una medición; y "suegro" no tiene código representable para esa posición en absoluto (el catálogo no tiene "suegro del hijo del jefe"). Simétricamente para `nuera/yerno`: "suegro presente" es tautológico (jefe = su suegro por definición del código 5) y "ascendiente" no es representable. Para `nieto/a`/`otro`/`sin parentesco` ninguna de las dos relaciones es derivable del catálogo sin inferencia adicional no soportada por el diccionario (p. ej. el código `8=Otro` mezcla hermano, tío, primo, abuelo y cualquier pariente no listado — no se puede aislar "hermano" de ahí, que es además la razón por la que el componente `hnos_cor` heredado en §1 **no tiene análogo limpio en la ventana ACTUAL**: se declara imposible de replicar con este instrumento, no se aproxima con `8=Otro`).

**Decisión de universo para este COMMIT-1**: se restringe el universo evaluable a `ego` con `parentesco` propio ∈ {1 (Jefe), 2 (Cónyuge)} — el subconjunto donde ambas relaciones objetivo (ascendiente, suegro) son derivables del catálogo sin inferencia tautológica ni ambigua. Es **70.0%** de los 23,831 respondientes EDER elegibles (16,687 personas, verificado por conteo). Esta restricción es consecuencia estructural del único instrumento disponible para la ventana ACTUAL, no una elección independiente — se declara aquí, antes de abrir el desenlace, seguiendo la regla de verificación de la restricción antes del diseño (v2.2, instrucciones-proyecto-v2_11.md líneas 65-69). **Es la única desviación real de "lo único que cambia es la ventana"**: la ventana, tal como el único instrumento actual la codifica, fuerza también un recorte de universo — se reporta como tal, no se disfraza de "mismo universo".

Aplicando además el filtro heredado de §1 (`vivienda.tipo_adqui` no blanco) sobre ese subconjunto: de 16,687 con parentesco∈{1,2}, 7,290 viven en vivienda `tipo_adqui` blanco (excluidas) o sin `factor` legible (0 casos de esto último) → **universo final: 9,397 personas** (verificado por comando propio, ver §3).

## §3 · Declaración exacta, ejecutable, del procedimiento (congelada — no se re-abre)

- **Variable(s) exactas**:
  - `persona.csv[parentesco]` del propio `ego` (para clasificar el universo).
  - `persona.csv[parentesco]` de los demás integrantes del mismo `folioviv+foliohog` (para derivar el desenlace).
  - `vivienda.csv[tipo_adqui]`, `vivienda.csv[factor]` (universo y ponderador, heredados).
  - Llave de persona: `folioviv (columna real detectada por sufijo, por el BOM UTF-8 'ï»¿' que antepone el CSV — mismo defecto que ya resuelve `_folioviv_key` en `medicion_familismo.py`) + foliohog + id_pobla`.
- **Universo**: personas EDER 2017 (20-54 años, con fila en `historiavida.csv`/`antecedentes.csv` — mismo universo respondiente de la corrida heredada), con `parentesco` propio ∈ {`1`,`2`}, en vivienda con `tipo_adqui` no vacío. **n del universo (no ponderado): 9,397**, verificado por comando propio, ejecutado antes de tocar ninguna variable de desenlace.
- **Ponderador**: `factor` de `vivienda.csv` (heredado). **Reserva metodológica declarada, no ejecutada**: el FD (`eder2017_fd.pdf` §1.1.3, líneas 196-207) y el script R oficial de INEGI (`eder2017_descripcion_calculoR.pdf`, `svydesign(..., weights=~factor_per)`) indican que el ponderador correcto para análisis anclados en el entrevistado EDER seleccionado (20-54 años) es `factor_per` de `antecedentes.csv`, no `factor` de `vivienda.csv` — hallazgo que la corrida 0.996 no tenía y que este acto no tenía por qué buscar, pero encontró. El encargo instruye heredar el ponderador sin cambio ("lo ÚNICO que cambia es la ventana"); cambiarlo también sería exceder el perímetro autorizado. **Se declara la reserva, se usa `factor` como instruye el encargo, y se deja para mesa o un acto sucesor decidir si corresponde un COMMIT-3 o una re-especificación adicional.**
- **Desenlace** (`corresidencia_actual_ascendiente_o_suegro`): para cada `ego` del universo, `= 1` si existe algún otro integrante del mismo hogar (`folioviv+foliohog`, `id_pobla` distinto) tal que:
  - si `ego.parentesco='1'` (Jefe): el otro tiene `parentesco='6'` (ascendiente) **o** `parentesco='7'` (suegro);
  - si `ego.parentesco='2'` (Cónyuge): el otro tiene `parentesco='7'` (ascendiente, invertido) **o** `parentesco='6'` (suegro, invertido);

  `= 0` en cualquier otro caso (incluida la ausencia de tal integrante).
- **Estimador**: tasa base ponderada — `p̂ = Σ(factor_i · desenlace_i) / Σ(factor_i)`, sobre el universo de 9,397 (misma fórmula que `tools/tasas_base_fase1.py:51`, heredada).
- **IC95%**: bootstrap 10,000 réplicas, `seed=42` (firmado, `FP-168`), remuestreo simple con reemplazo de personas, método percentil (heredado, mismo código que `tools/tasas_base_fase1.py:44-63`).
- **n**: tamaño de muestra no ponderado del universo = 9,397 (a confirmar en COMMIT-2 que el conteo final tras el mismo código coincide).
- **Escala**: [0,1], proporción.
- **Script**: `tools/tasas_base_corresidencia_actual.py` (nuevo, COMMIT-2), reutilizando `wprop_ic_bootstrap()` de `tools/tasas_base_fase1.py` por consistencia de método (misma firma, mismos parámetros `N_BOOT=10000, SEED=42`).

**El primer resultado que produzca este procedimiento es el que se reporta.**

## §4 · Lo que este COMMIT-1 verificó y no es medición de desenlace (nota de perímetro, A-bis)

Antes de este commit se abrieron `persona.csv`, `historiavida.csv`, `antecedentes.csv`, `vivienda.csv` completos — pero únicamente para verificar **estructura**: nombres de columna reales (BOM), conteos de universo (personas totales, distribución de `parentesco` propio, viviendas no-blanco), y confirmar que ambas llaves (`historiavida`/`antecedentes`) son el mismo conjunto de 23,831 personas. **En ningún momento se leyó ni se agregó el valor de `desenlace` (presencia de código 6/7 en los demás integrantes del hogar)** — eso es §5, COMMIT-2. Es la misma distinción que v2.2 traza entre "verificar que la restricción existe" (permitido, y exigido, antes del diseño) y "consultar el resultado" (contaminaría el pre-registro): aquí se verificó la restricción (cómo está codificado `parentesco`, quién puede clasificarse) y no el resultado (si esas personas efectivamente coresiden con un ascendiente/suegro hoy).
