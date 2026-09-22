# ENCARGO · ACTO GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1 · Por qué el piso t−1 de ENIF cubre R en 6 de 32: un intervalo de persistencia que incluya el cambio entre olas, calibrado en 2015→2018→2021 y evaluado en retrospectiva contra 2024, rotulado así

> ENTORNO: **CAJA** — abre ENIF 2015, 2018, 2021 (marginales por eje); lee los marginales 2024 **sellados** (no abre 2024). Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 (calibración pre-registrada) · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI`, **no adopta**; ningún `celdas_validadas` se mueve (es RETROSPECTIVA-MECÁNICA por definición) · CALC-id reservado: `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` · ids raíz de acto.

## 1 · OBJETIVO
Que el diferimiento de ENIF en `MARGINALES-ADOPCION-1` tenga salida: un intervalo de persistencia por celda que sume al error muestral la **variación empírica del cambio entre olas** (2015→2018 y 2018→2021, por celda del mismo eje), pre-registrado en COMMIT-1, y su cobertura de R 2024 medida y rotulada **RETROSPECTIVA-MECÁNICA** (R 2024 ya vista; sin selección de variante). «Hecho» = `verify` REPRODUCE; 32 RESULT con `ic_calibrado_inf/sup`, `tipo_incertidumbre = muestral + cambio-entre-olas`, cobertura por celda y por conglomerado con intervalo binomial (v2.16 §4), rótulo RETROSPECTIVA-MECÁNICA en todos; **ninguna frase de producto mezcla** la cobertura calibrada con la prospectiva de los pilotos.

## 2 · FIRMAS DE MESA
Ninguna nueva: es calibración (v2.16 E.6: «un cruce ya visto sigue sirviendo para describir, calibrar y evaluar en retrospectiva, rotulado así»). La adopción de ENIF con el IC calibrado es **otra** FP, que este acto abre y no firma.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` FP `…ARBITRO-MARGINALES-1-ed7d-02`: ENIF 2024 6/32 = 0.19 [0.09, 0.35] — el IC muestral de la ola anterior no cubre un cambio real de tres años. `[EXISTE]` pisos por eje ENIF 2021 (`#866/#871/#874`: `CALC-PISOS-ENIF2021-EJES-0001`), marginales 2024 sellados (`tramite-ola5-propuesta-v0.yaml`), `enif2015_csv`, `enif2018_csv` en manifiesto. No sé si los marginales 2015/2018 por eje están sellados: **el acto lo busca por id de CALC**; si no, los deriva (son olas de desarrollo).
- `[SUPUESTO]` Los reactivos de ahorro/crédito son comparables por texto entre 2015, 2018 y 2021 (A.15c; `P5_6`/`P5_7` ya enseñó que por nombre no). Si una celda no es comparable en alguna ola, su calibración usa las olas que sí y lo declara; si ninguna, `NO-CALIBRABLE`.
- `[SUPUESTO]` Dos cambios por celda bastan para una varianza empírica útil si se **agrupa por eje** (pooling declarado en COMMIT-1), no por celda sola. Si resulta falso —el intervalo calibrado cubre < 0.5 igual—, el hallazgo es que la persistencia trienal no es piso en ENIF, y va al informe.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-*ENIF*PERSISTENCIA*` → reporta; `grep -rl "IC calibrado\|cambio entre olas" forense/prereg-caja/` → reporta (al redactar: NO-ENCONTRADO en ambos). Ramas vivas: ninguna.

## 5 · PIEZAS
- **COMMIT-1:** spec congelada: celdas (las 32 evaluadas, por id), fórmula del intervalo (muestral 2021 ⊕ varianza empírica del cambio logit por eje, pooling declarado), regla de cobertura, rótulo RETROSPECTIVA-MECÁNICA, comparabilidad por texto por ola, seed, tolerancias; **la regla se fija antes de abrir el dato y no se ajusta con el resultado** (v2.16 §4).
- **COMMIT-2:** marginales 2015/2018 por eje si faltan, cambios, intervalo calibrado, cobertura contra 2024 sellado; registro y asiento en el mismo acto.
- **P3:** FP nueva para mesa: «adoptar ENIF con IC calibrado si cobertura ≥ X» — X lo propone el acto **desde la spec**, no desde el resultado.

## 6 · LATITUD
DECIDES TÚ: forma exacta del pooling, orden, enlazar `data/raw`. PREGUNTAS A MESA: si 2015 no es comparable por texto en la mayoría de celdas, ¿calibrar solo con 2018→2021 (recomendado, declarado) o esperar? NO DECIDES: §7.

## 7 · PAROS
a) abrir ENIF 2024 (sus marginales son sellados: se leen del yaml) · b) forzar o editar sellados · c) adoptar · d) cambiar la fórmula o la regla congeladas con el resultado a la vista · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«Spec congelada en COMMIT-1 antes de abrir 2015/2018 — protege: congelar spec.» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md` (+ sidecar, yaml) · `data/corrida0/CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001/` · derivados por comando · `replay-evidencia.tsv` · `firmas-pendientes.tsv` (una FP nueva) · nota · `canon/L0/<raíz>.md`. Ajeno: `estimadores-por-segmento.yaml` (lo escribe el marcador), los CALC de pisos existentes (lectura). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no re-evalúa prospectivamente, no toca el yaml. Sucesor: `MARGINALES-ADOPCION-2` (ENIF) con la FP de P3 firmada. Auditoría: no aplica (calibra el aparato; las cifras sobre México ya están selladas). Cierre por /acto.
