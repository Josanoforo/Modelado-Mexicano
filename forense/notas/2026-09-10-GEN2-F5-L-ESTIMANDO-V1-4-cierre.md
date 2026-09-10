# GEN2-F5-L-ESTIMANDO-V1-4 · cierre

## Veredicto

**VEREDICTO DE CAUSA DE COBERTURA: CAUSA MATERIAL DEMOSTRADA.** En 11 de las
14 celdas, la pregunta v1.3 no entregó a L el mismo estimando primario que R
arbitra: ocho usaron un texto de censo/no-estimación como universo y tres TRA
usaron como conducta un alias del consumidor ENCIG 2025 en lugar del reactivo
de su encuesta y ola. Las respuestas históricas muestran que L tomó esas
incoherencias como razones explícitas para abstenerse o para cambiar de
denominador; esto demuestra capacidad causal material, no que sea la única
causa de abstención ni que v1.4 vaya a producir una cifra.

**P7: `REQUIERE-CORPUS-SUCESOR-ANTES-DE-RECAPTURA`.** La target card y
`L-spec-v1_4.json` quedan listas y selladas, pero no deben ejecutarse todavía:
el ensamblado actual de `L+corpus` trunca las 11 celdas de recaptura en 600 000
caracteres y no entrega en ninguna una mención de la encuesta ni de
encuesta+ola. Corregir solo la pregunta dejaría un brazo documental
materialmente defectuoso.

## P1 · censo de identidad semántica 14/14

La clasificación no usa acierto, error ni valor alguno contra R.

| id | pregunta v1.3 | estimando primario R | universo R | evento binario R | alineación | defecto | recaptura necesaria |
|---|---|---|---|---|---|---|---|
| CIV-M-01 | Universo “NO ESTIMADO…”; `denuncia_con_miedo_o_desconfianza` | Proporción ponderada por delito de BP1_23 en el grupo 01/02/06 | Delitos no denunciados de todos los tipos con razón principal válida | Miedo al agresor, miedo a extorsión o desconfianza, frente a las otras seis razones válidas | DESALINEADA-MATERIAL | El placeholder niega el acto estimativo y el alias puede leerse como denuncia realizada | ambos brazos |
| CIV-M-02 | Igual, ENVIPE 2013 | Igual construcción BP1_23 | Igual universo por delito de la ola | Igual partición 01/02/06 frente a 03/04/05/07/08/09 | DESALINEADA-MATERIAL | Mismo defecto de universo y sentido | ambos brazos |
| CIV-M-04 | Igual, ENVIPE 2015 | Igual construcción BP1_23 | Igual universo por delito de la ola | Igual partición conceptual | DESALINEADA-MATERIAL | Mismo defecto de universo y sentido | ambos brazos |
| CIV-M-10 | Igual, ENVIPE 2021 | Igual construcción BP1_23 | Igual universo por delito de la ola | Igual partición conceptual | DESALINEADA-MATERIAL | Mismo defecto de universo y sentido | ambos brazos |
| CIV-M-12 | Igual, ENVIPE 2023 | Igual construcción BP1_23 | Igual universo por delito de la ola | Igual partición conceptual | DESALINEADA-MATERIAL | Mismo defecto de universo y sentido | ambos brazos |
| CIV-M-13 | Igual, ENVIPE 2024 | Igual construcción BP1_23 | Igual universo por delito de la ola | Igual partición conceptual | DESALINEADA-MATERIAL | Mismo defecto de universo y sentido | ambos brazos |
| DIN-M-01 | Universo “NO ESTIMADO…”; `tiene_ahorros` | Proporción ponderada de respuesta Sí a cr27 | Personas del libro 3B/sección CR con respuesta Sí/No válida | Declara tener ahorros | DESALINEADA-MATERIAL | Sin denominador estimable en el prompt | ambos brazos |
| FAM-M-01 | Universo “NO ESTIMADO…”; alias de recepción de dinero | Proporción ponderada de Sí a p9_9_4 | Personas seleccionadas de tmodulo2/sección 9.9 con respuesta válida | Piensa cubrir la vejez con dinero de pareja, hijos u otros familiares | DESALINEADA-MATERIAL | Placeholder y alias cambian apoyo esperado para la vejez por recepción actual | ambos brazos |
| FAM-M-05 | Hogares de concentradohogar; `remesas > 0` | Proporción ponderada de hogares con remesas positivas | Universo completo de hogares ENIGH 2016 NS | `remesas > 0` | ALINEADA | ninguno material | reutilizar v1.3 |
| FAM-M-06 | Igual, ENIGH 2018 | Igual estimando de remesas | Universo completo de hogares ENIGH 2018 NS | `remesas > 0` | ALINEADA | ninguno material | reutilizar v1.3 |
| FAM-M-07 | Igual, ENIGH 2020 | Igual estimando de remesas | Universo completo de hogares ENIGH 2020 NS | `remesas > 0` | ALINEADA | ninguno material | reutilizar v1.3 |
| TRA-M-02 | ENCUCI 2020, pero conducta `paga_mordida_encig2025` | Proporción ponderada del OR AP5_17/AP5_18 | Persona seleccionada 15+ con contacto reciente con funcionario; combinaciones que definen el OR | Le pidieron dádiva/favor/dinero extra O tuvo que darlo | DESALINEADA-MATERIAL | Alias de otro instrumento colapsa solicitud y entrega y oculta el OR; universo v1.3 incluía texto de auditoría en vez de regla limpia | ambos brazos |
| TRA-M-03 | ENCIG 2013, pero conducta `paga_mordida_encig2025` | Proporción ponderada de Sí a P8_3 | Personas 18+ con respuesta individual válida en sección VIII | Servidor público intentó apropiarse o solicitó directamente un beneficio; reactivo único 2013 | DESALINEADA-MATERIAL | Alias de otra ola oculta que 2013 usa P8_3, no una batería 2025; denominador no estaba afirmado limpiamente | ambos brazos |
| TRA-M-07 | ENCIG 2021, pero conducta `paga_mordida_encig2025` | Proporción ponderada de Sí a P8_3_1 | Personas 18+ de sección VIII con respuesta válida | Primer inciso: apropiación o solicitud directa por servidor público | DESALINEADA-MATERIAL | Alias de otra ola no define el inciso real ni su denominador | ambos brazos |

Fuentes estructurales: specs activas `data/corrida0/CALC-R-*/spec.yaml`,
`codificacion-R-v1_2.tsv` y los diccionarios/specs citados en la target card.
Evidencia del uso explícito del defecto por L, entre otras capturas:
`L-CIV-M-01-M__L+corpus__08__v1_3.json`,
`L-FAM-M-01-M__L+corpus__07__v1_3.json`,
`L-TRA-M-02-M__L+corpus__08__v1_3.json` y
`L-TRA-M-07-M__L+corpus__05__v1_3.json`.

## P2–P5 · contrato y recaptura

`L-estimandos-v1_4.tsv` es la fuente humana 14/14. Para CIV conserva la
unidad delito y la partición completa de BP1_23; para DIN declara cr27; para
FAM-M-01 reproduce el significado del inciso; para TRA conserva por separado
el OR solicitud/entrega de ENCUCI, el reactivo único P8_3 de ENCIG 2013 y el
primer inciso P8_3_1 de ENCIG 2021. No contiene respuestas R/M/TRIADA ni
conteos de desenlace.

`L-spec-v1_4.json` mantiene la plantilla de estimación puntual y la salida
epistémicamente honesta (“si no conoces el dato… no inventes”). El validador
falla ante placeholder, alias TRA, universo/evento vacío, cardinalidad distinta
de 14 o ids distintos del marco. Las tres ENIGH conservan literalmente su
pregunta v1.3.

Derivación mecánica: **11 celdas requieren recaptura de ambos brazos**. Futuro
total: **11 × 2 × k=8 = 176 invocaciones**. Este acto hizo cero invocaciones.

## P6 · diagnóstico mínimo del corpus actual

| id | disponibles | incluidos antes del límite | chars | truncado | encuesta | encuesta+ola | evidencia directa del evento |
|---|---:|---:|---:|---|---|---|---|
| CIV-M-01 | 31 | 20 | 600000 | SI | NO | NO | NO |
| CIV-M-02 | 31 | 20 | 600000 | SI | NO | NO | NO |
| CIV-M-04 | 31 | 20 | 600000 | SI | NO | NO | NO |
| CIV-M-10 | 31 | 20 | 600000 | SI | NO | NO | NO |
| CIV-M-12 | 31 | 20 | 600000 | SI | NO | NO | NO |
| CIV-M-13 | 31 | 20 | 600000 | SI | NO | NO | NO |
| DIN-M-01 | 37 | 19 | 600000 | SI | NO | NO | DUDOSA |
| FAM-M-01 | 32 | 19 | 600000 | SI | NO | NO | DUDOSA |
| TRA-M-02 | 32 | 20 | 600000 | SI | NO | NO | DUDOSA |
| TRA-M-03 | 31 | 20 | 600000 | SI | NO | NO | DUDOSA |
| TRA-M-07 | 31 | 20 | 600000 | SI | NO | NO | DUDOSA |

La clasificación final es exploratoria: las coincidencias DUDOSA son discusión
general de ahorro, apoyo familiar o corrupción, no evidencia de la encuesta,
ola y evento objetivo. El TSV durable añade el criterio por celda. No se
reconstruyó el paquete, no se cambió 600k y no se implementó retrieval.

## P8 · NC-0146 y límites

`NC-0146` permanece **ABIERTA**. `CALC-TRIADA-0001` conserva plena validez bajo
su spec sellada y su resultado histórico `SIN-GANADOR-UNICO` no se reescribe.
Este acto explica por qué su cobertura no basta para adjudicar la pregunta
central: 11 targets eran materialmente desalineados y el tratamiento documental
actual tampoco entrega evidencia específica. El sucesor inmediato es un corpus
sucesor; después, la recaptura v1.4 de 176 invocaciones.

No se corrió L, no se llamó `claude -p`, no se calcularon errores contra R, no
se recalculó ni adjudicó TRIADA, no se tocó `NC-0147`/`NC-0148`, y no se editó
ningún artefacto histórico v1.3, R, M o `milpa/`.

## Verificación

- `genera_valida_l_v1_4.py --valida --diff-semantico --dry-run`: 14/14,
  cinco falsadores rechazados, 11 recapturas, 22 prompts y 176 rutas futuras;
  cero invocaciones.
- `sha256sum -c`: target card, spec y diagnóstico `OK`.
- `python3 -m py_compile genera_valida_l_v1_4.py`: `OK`.
- `runner_l_cli.py --dry-run` (regresión del ensamblador histórico): `OK`,
  176 rutas históricas construidas y ningún subproceso `claude` invocado.
- `tests/check.py --baseline`: línea base VERDE; 3 FAIL y 2218 WARN heredados
  (T06=2, T08=1), sin fallo nuevo. Los dos `demanda-*.tsv` de `NC-0141`
  fueron respaldados y restaurados; hashes antes/después idénticos.
- `git diff --check`: limpio.
