# GEN2-ENADID-UNION-ACTUAL-CLI-1 · cierre de medición

## Resultado sustantivo

`CALC-ENADID-0001` mide situación conyugal **actual** en ENADID 2023. No
mide tipo de primera unión y no prueba el mecanismo de baja garantía
institucional. Fuentes verificadas contra manifiesto: base CSV
`995d448a…faa18`, FD `d56582b…4f34c` y cuestionario de hogar
`8b046a68…e3270`.

Entre 276 849 personas de 15+ con edad y P3_27 válidas, la unión libre es
**0.1905406** (EE 0.0015975; IC95% [0.1874290, 0.1936915]). Entre las 152 834
personas actualmente casadas o en unión libre, la unión libre es
**0.3464457** (EE 0.0026744; IC95% [0.3412224, 0.3517062]) y actualmente
casadas es **0.6535543**. Son dos denominadores, no dos nombres del mismo
estimando.

### Unión libre: punto y precisión por edad

| Edad | n distribución | Bruta | IC95% | n casada/UL | Condicional | IC95% |
|---|---:|---:|---:|---:|---:|---:|
| 15–17 | 18 709 | 0.035827 | [0.032113, 0.039954] | 694 | 0.948643 | [0.921468, 0.966753] |
| 18–29 | 65 507 | 0.237847 | [0.231781, 0.244021] | 22 676 | 0.699208 | [0.687980, 0.710202] |
| 30–44 | 73 324 | 0.288655 | [0.282633, 0.294752] | 50 944 | 0.416648 | [0.408465, 0.424877] |
| 45–59 | 66 069 | 0.170504 | [0.165270, 0.175869] | 47 308 | 0.238610 | [0.231432, 0.245940] |
| 60+ | 53 240 | 0.074361 | [0.070353, 0.078578] | 31 212 | 0.126698 | [0.119991, 0.133724] |
| 15+ | 276 849 | 0.190541 | [0.187429, 0.193691] | 152 834 | 0.346446 | [0.341222, 0.351706] |

El detalle de las siete categorías, numeradores y denominadores ponderados,
desconocidos, fuera de denominador, EE, IC y gl está en `resultados.csv`.
Distribución nacional: unión libre 19.0541%; separada de unión libre 4.1509%;
separada de matrimonio 2.9207%; divorciada 2.1882%; viuda 6.1575%; casada
35.9446%; soltera 29.5841%. Cierra en uno (residuo de serialización <2e-12).
Los cinco grupos de edad reconstruyen el total por masa: 99 982 443 personas
expandidas. No se promedian puntos.

## Calidad y diseño

`LLAVE_PER` es única; no hay enlace ni pérdida de enlace. Hay cero pesos
inválidos, cero P3_27 no especificadas dentro de edad conocida 15+ y cero
filas 15+ sin diseño. Hay 154 edades 999/no especificadas (masa 59 206), que
no se trataron como 15+ ni como respuestas negativas. Diseño acreditado:
659 `EST_DIS`, 15 214 pares `EST_DIS`/`UPM_DIS`, cero `UPM_DIS` que cruce
estratos. Hay 56 estratos singleton: no se les atribuyó varianza cero; cada
uno recibió el aporte promedio de los estratos no singleton. Taylor WR de
razón, dominio sobre muestra completa, IC logit-t, gl=14 555, sin FPC.

La primera ejecución diagnóstica sobre el COMMIT-1 `97c7094` reveló que la
regla inicialmente escrita «singleton sin aporte» contradecía el mandato.
Se descartó ese sello no publicado y `1c9afb3` corrigió la política antes de
la ejecución aceptada. La corrección no usa el valor del desenlace y conserva
los puntos; ensancha ligeramente EE/IC. También separa categorías válidas
fuera del denominador condicional de respuestas desconocidas.

## Legacy y correspondencia propuesta

| Resultado | Universo legacy | Punto anterior | Punto nuevo | Dictamen | Causa/delta |
|---|---|---:|---:|---|---|
| RES-0043 `union_libre` | ENADID 15+, situación actual, bruto | 0.1905 | 0.1905406 | COMPATIBLE con renombre de `situacion` | Mismo evento/unidad/denominador intencional; delta contra el valor publicado = +0.0000406. El cálculo legacy efectivo con `P3_27_AG` y `EDAD>=15` incluyó edad 999 y da 0.1905363; la nueva operación usa P3_27 documental y excluye edad desconocida. |
| RES-0044 `matrimonio_directo` | complemento aritmético del bruto | 0.8095 | 0.8094594 (`no unión libre`) | REQUIERE RENOMBRE | No significa matrimonio. Si se quiere situación actual casada: 0.3594462 bruta o 0.6535543 entre casada/UL; no se calcula delta porque cambia el evento/denominador. |
| CALC-EDER-0003 | EDER 2017, tipo de primera unión | 0.4809714 libre / 0.5189458 directo | no aplica | INCOMPATIBLE como reemplazo | Instrumento, evento y población distintos; queda como evidencia secundaria, nunca pin de estos puntos. |

Propuesta para Claude/B, **no consumo activo**: RES-0043 puede apuntar a
`RESULT-ENADID-UA-G-P-BRUTA` y cambiar `situacion: primera_union` por
`situacion: situacion_conyugal_actual`. RES-0044 debe renombrarse
`no_union_libre` si conserva el complemento bruto, o dividirse en un resultado
explícito `actualmente_casada` con universo declarado. No usar
`matrimonio_directo` para ninguna de esas dos alternativas.

## Controles, replay y estado

- `corrida0.py verify CALC-ENADID-0001`: `REPRODUCE`, contexto idéntico.
- Control independiente: módulo CSV estándar, sin importar medidor ni helpers;
  confirma ambos puntos nacionales y los denominadores de los seis grupos.
- Particiones completas y condicionales cierran en uno por edad; masas de los
  cinco grupos cierran contra total 15+.
- Receta: montar `data/raw -> /home/pc0/mm-corpus/raw`; ejecutar
  `python3 tools/corrida0.py verify CALC-ENADID-0001`; después ejecutar
  `python3 forense/analisis/enadid-union-actual-cli-1/control_independiente.py data/raw/base_datos_enadid23_csv.zip forense/analisis/enadid-union-actual-cli-1/resultados.csv forense/analisis/enadid-union-actual-cli-1/enadid-union-control-independiente.json`.

Estado separado: **medición terminada y sellada**; **validación independiente
terminada**; **publicación canónica pendiente**; **adopción ninguna**;
`cuenta_gen2=PENDIENTE-DE-MESA`. La publicación serial no se ejecuta porque
los carriles A/B del lanzamiento no están integrados en `origin/main`; no se
reescriben `corridas.tsv`, `resultados.tsv`, `usos.tsv`, demanda ni relevo en
esta rama antes de esa compuerta.
