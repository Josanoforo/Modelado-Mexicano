# Cierre · GEN2-ENCRIGE-DESCRIPTIVA-1

Fecha: 16 de septiembre de 2026. Rama: `acto/gen2-encrige-descriptiva-1`. Base: `origin/main` `9dffd6455c67e2ca99740e79f90be59a13f250e1`.

## Resultado sustantivo

Se extrajeron de tabulados oficiales ENCRIGE 2020 dos indicadores para el total nacional y cuatro tamaños oficiales. El indicador primario es la proporción de unidades económicas expuestas a trámites o inspecciones que experimentaron al menos un acto de corrupción. El secundario es el número de trámites o inspecciones con experiencia de corrupción por unidad económica expuesta; se conserva separado y no se denomina prevalencia.

| Dominio | Prevalencia | Experiencias por unidad expuesta |
|---|---:|---:|
| Total nacional | 5.10% | 0.240 |
| Micro | 5.51% | 0.237 |
| Pequeña | 2.24% | 0.233 |
| Mediana | 4.41% | 0.234 |
| Grande | 6.69% | 1.168 |

Los puntos son resultados oficiales reproducidos mediante extracción determinista. No son una reestimación propia del diseño de INEGI. La extracción y normalización son nuevas; la medición propia es `NINGUNA`; el CALC sí quedó sellado y reproducible; adopción, calibración y transferencia son `NINGUNA`.

## Productos

- `forense/analisis/encrige-descriptiva-1/encrige-corrupcion-por-tamano.csv`: 10 filas indicador-dominio con cifras originales, transformación, normalizados, numerador/denominador expandidos, ausencia tipada de n/incertidumbre, periodo, cuadro y localizador. SHA-256 `632ce31b2c2cf70e22871319b5842e6168592f065588b69b11010e3552b48c26`.
- `forense/analisis/encrige-descriptiva-1/lectura-TRA.md`: lectura sustantiva, población, cortes de tamaño y límites.
- `data/corrida0/CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001/`: spec, medidor y artefactos de corrida.
- `tests/test_encrige_descriptiva.py`: guardia contra confundir tasa por 10 000 con porcentaje y contra una escala incompatible con numerador/denominador.

## Identidad, secuencia y recibos

Los tres objetos registrados coincidieron con manifiesto:

- tabulados ZIP: `06864904426a6b2c18cdad63a8b7bcb995fd35333c44448ba3fb5a973b822c5a`;
- cuestionario: `f410156bf5131921f6699b47f07fba302b168de187ea638a5f601732097cd8c1`;
- diseño muestral: `3f314258dc4ad0ddc5a4b94b327c763f3ff8c2abacf0bcac0a171519ce479961`.

La spec y el medidor se congelaron en `4cbeaa28dc490965de6f9e795048635cedc8ee01`, antes de la primera ejecución. La corrida fue `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001--4cbeaa28dc49`, salida 0. Los artefactos y la lectura quedaron en `92c0690e80d03d0dbf8764686a081a7938f6e329`. El sello `dd2bc7dc912585301632789ac3b3bc2208c0ab5d9b8c1db83afa18fa2233a39a` coincide.

La tasa primaria de `t6_33` coincide exactamente con la segunda lectura `t6_36` en los cinco dominios. La discrepancia máxima de `numerador / denominador * 10 000` frente a la tasa publicada es `2.120388857967e-11`, inferior al umbral `1e-9`.

Comandos ejecutados:

```bash
python3 tools/prepara_corpus.py --config-desde /home/pc0/Modelado-Mexicano/data/raices.local.yaml --id conjunto_de_datos_encrige_2020_csv --id encrige2020_cuestionario --id gen2_encrige2020_diseno_muestral --aplica
python3 tools/corrida0.py spec-check CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py preflight CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py run CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 -m unittest tests.test_encrige_descriptiva
python3 tools/corrida0.py verify CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
python3 tools/corrida0.py registro --lote CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001
```

Recibos: `spec-check` 0 OK/0 FAIL sobre una spec de tabulados sin variables de microdato; preflight `VERDE`; dos pruebas dirigidas `OK`; verify `REPRODUCE · CONTEXTO=IDENTICO`, 15/15 resultados.

## Registro, contador y reservas

El último comando fue estrictamente seco: no se pasó `--escribe`. Aun acotado con `--lote`, el mecanismo proyecta reescribir las tres vistas comunes completas y arrastra diferencias ajenas. Por ello se difiere el registro global; la carpeta CALC queda sellada y verificable de forma independiente. `cuenta_gen2=PENDIENTE-DE-MESA`; no se escribió `decisiones.tsv` ni una firma de contador.

Reservas materiales:

- El CSV no publica n muestral, EE, CV ni IC. Los ODT explican la semaforización de CV, pero no conservan la asociación celda-color; no se pueden hacer afirmaciones de significancia entre tamaños.
- El periodo es durante 2020, de enero a la fecha de entrevista, no un año calendario completo inferido por el nombre de la edición.
- El universo excluye sectores primarios y gobierno, y el denominador exige al menos un trámite o inspección.
- La incidencia por unidad no es prevalencia ni riesgo por interacción; en empresas grandes puede superar uno porque admite varias experiencias por unidad.

## Integración diferida

CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4. En la integración serial posterior: incorporar la sección descriptiva al informe TRA, decidir `cuenta_gen2` y rederivar el registro global desde el estado entonces vigente. No hay números reservados, cambios al panel F6, adopción al motor ni despliegue.
