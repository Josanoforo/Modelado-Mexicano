# GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL · cierre técnico

Fecha de ejecución: 10 de septiembre de 2026. Entorno: CAJA/WSL2, corpus
compartido montado. Base: `origin/main=e76f3a1d476049d0c7adcba87535e60f507c8d91`.
Encargo archivado en
`forense/encargos/2026-09-10-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL.md`.

## Resultado útil

La discrepancia histórica no admite un desempate por el instrumento.
`ID_TRA` es la unidad persona × tipo de trámite; `NT_TIPO=01..03` distingue
los últimos eventos de ese trámite y `P7_3` describe el lugar o medio de cada
evento. Elegir la primera o última fila colapsaría eventos legítimos y, en 501
grupos, asignaría un canal sin fundamento. Se entrega una sensibilidad
exploratoria reproducible, sin adopción, y la demanda general `NC-0153` queda
enrutada hasta la selección seca de adquisición.

No se creó `CALC` sucesor: el diagnóstico se hizo después de conocer los
resultados históricos, no define un nuevo estimando de producción y queda
marcado `EXPLORATORIO-NO-ADOPTAR`. Tampoco se cambió `milpa/`: r2 ya está
limitada por dominio y las variantes discrepantes ya están prohibidas.

## F1 · unidad y duplicados

El descriptor oficial define `ID_TRA` como “Identificador del trámite”,
`NT_TIPO` como “Número de trámite / Último evento” con códigos 01–03, y `P7_3`
pregunta “¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el
trámite o pago?”. La tabla `sec_7` confirma que `(ID_TRA,NT_TIPO)` es llave
única; `sec_8`, donde vive `P8_4`, tiene `ID_TRA` único.

Comando reproducible:

```bash
python3 tools/diagnostico_encig_unidad_canal.py
```

El script verifica antes de medir el SHA-256 del ZIP
`47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`, la
unicidad de ambas llaves y la constancia de `FAC_TRA` dentro de `ID_TRA`.

| diagnóstico de `sec_7` | resultado |
|---|---:|
| filas evento | 124,314 |
| `ID_TRA` | 113,717 |
| `ID_TRA` repetidos | 7,430 |
| distribución 1 / 2 / 3 eventos | 106,287 / 4,263 / 3,167 |
| repetidos con contenido igual salvo `NT_TIPO` | 6,929 |
| repetidos con `P7_3` discordante | 501 |

Los 6,929 grupos de contenido coincidente tampoco son “duplicados exactos”:
`NT_TIPO` difiere y es precisamente la variable que el instrumento usa para
conservar eventos repetidos. No se colapsan.

Dentro del recorte histórico con `P8_4` observado hay 21,139 `ID_TRA` y
24,974 filas evento. Son 160 grupos con código `P7_3` discordante; 141 cambian
de clase agregada y 95 mezclan presencial `{1}` con digital `{3,4,5}`. Estos
95 pesan 143,629, 0.2476% de la masa del foco presencial/digital. Toda clase
mezclada pesa 204,737, 0.2879% de la masa observada.

## F2 · sensibilidad, comparación y consumo

La sensibilidad colapsa una sola vez los `ID_TRA` cuyo canal agregado es
consistente. Para los 95 mixtos P+D no elige fila: la envolvente asigna por
separado los ambiguos negativos y positivos al canal que produce cada extremo.
Es un límite descriptivo de una asignación forzada, no una regla de adopción.

| versión | presencial | digital | lectura |
|---|---:|---:|---|
| antigua CD sellada | 0.116000 | 0.027358 | deduplicación histórica no reproducible; `RES-0009/0011` siguen sin adopción |
| CD reconstruida por CALC-ENCIG-0001 | 0.115968 | 0.027356 | no reproduce a 1e-6 |
| r2, evento sin deduplicar | 0.141041 | 0.029868 | adoptada sólo con `P8_4` observado |
| `ID_TRA` de canal consistente | 0.115018 | 0.026635 | exploratoria |
| envolvente por los 95 P+D mixtos | [0.114571, 0.115771] | [0.026522, 0.027538] | exploratoria, no asigna canal real |

La diferencia entre r2 y el colapso consistente no es un error de redondeo:
r2 estima por fila evento; el diagnóstico estima por `ID_TRA` y deja visibles
los mixtos. Cambiar entre ambas unidades es cambiar el estimando.

Propuesta de consumo acotada ya satisfecha por las funciones actuales:

- evento: `P8_4=1`, solicitud/insinuación señalada para ese `ID_TRA`;
- universo: trámites de personas que ya declararon corrupción y tienen
  `P8_4` observado, no todos los trámites;
- activador: `p8_4_observado=true` y `canal_p7_3=presencial` o
  `digital_registrado`;
- consumidor: `emitir_binaria_en_contexto`; fuera del dominio devuelve
  `NO-EMITIBLE-DOMINIO`.

Para ese uso restringido r2 basta. No se necesita otro parámetro. Para el uso
general, r2 no basta y no se extrapola.

## F3 · fuente general y adquisición

Se examinaron primero los candidatos ya presentes. Cada uno aporta parte del
objeto, pero ninguno observa solicitud y canal sobre la misma unidad evento.

| fuente / periodo | numerador propio | denominador propio | unidad y diseño | resultado para NC-0153 |
|---|---|---|---|---|
| ENCUCI 2020 | `AP5_17=1` solicitud; `AP5_18=1` entrega; unión `S∪E` | 13,411 personas de 15+ con contacto con funcionario y respuesta válida | persona, `FAC_SEL`; diseño ENCUCI disponible | `P(S)=0.106319`, `P(E)=0.073640`, `P(S∪E)=0.126006`; no trae canal ni unidad evento |
| UNAM-IIJ, Corrupción y Cultura de la Legalidad, 2015 | `p4_j=2`, le solicitaron dinero extra | `p4_j∈{1,2}`, quienes realizaron cada trámite en el último año | persona, `Pondi2`; microdato y descripción disponibles | cuatro tasas generales, pero sin canal |
| ENCIG 2025 r2 | `P8_4=1` | sólo `P8_4` observado entre declarantes previos | `ID_TRA`/evento ambiguo, `FAC_TRA`, diseño disponible | condicional; no es tasa general |

Detalle UNAM-IIJ, tabulación separada (`n` / numerador no ponderado / tasa
ponderada): reconexión de luz 1,093 / 377 / 0.334828; licencia de conducir
1,051 / 322 / 0.279622; incapacidad médica 1,029 / 216 / 0.194481; licencia de
construcción 1,016 / 262 / 0.212140. Estas cifras no se promedian ni se
presentan como tasa de todos los trámites.

La demanda exacta se incorporó, sin crear otra NC, como fila canónica
`TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO` en
`data/curacion-registro/cola-adquisicion-registro.tsv`, estado `PENDIENTE`, y
se regeneró la vista `data/cola-adquisicion-v1_0.tsv`. La fila exige:

- unidad evento de trámite elegible en México;
- numerador solicitud o insinuación ligada al evento;
- denominador todos los eventos elegibles del mismo canal;
- canal observado en ese evento;
- periodo y diseño disponibles.

Prueba seca nominal, sin red ni descarga:

```text
ELEGIDO TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO
estado=PENDIENTE prioridad=0 razon=sin intento previo registrado
```

El siguiente paso es SONDA dirigida en fuentes primarias del productor. No se
lanzó adquisición productiva para no competir con el cron y no se envió
ninguna solicitud.

## F4 · obligaciones

| obligación | evidencia | estado | siguiente acción |
|---|---|---|---|
| NC-0107 | unidad reconstruida; 501 discordantes; sensibilidad sin desempate | ABIERTA | mesa retira/sustituye RES-0009/0011 o define nueva unidad prospectiva |
| NC-0111 | r2 sigue condicionada; dos candidatos parciales no cubren canal × evento | ABIERTA | conservar límite estructural y consumir r2 sólo en dominio |
| NC-0153 | fila canónica, vista y selección seca efectivas | ABIERTA | SONDA primaria y luego medición sólo si una fuente satisface el objeto exacto |

## A.13 y reservas

Se abrieron 2 tablas del ZIP ENCIG (`sec_7` y `sec_8`, ya usadas por
CALC-ENCIG-0001), el descriptor ENCIG, 1 microdato UNAM-IIJ con 1,200 filas ×
255 variables y sus etiquetas, y los resultados/spec de ENCUCI ya sellados.
No se descargó ningún payload. La sonda de red de arranque dio HTTP 000; no
afecta las comprobaciones locales ni se interpreta como ausencia de fuente.
