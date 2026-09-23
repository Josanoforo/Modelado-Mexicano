# Recibo ASTRA-2: insumos ENCIG históricos para rutas de trámite

22/sep/2026. Consumidor: ejecutor ASTRA-2, borrador local
`/home/pc0/mm-astra-theta-1/forense/analisis/astra-theta/mapa-v1_0.tsv`,
SHA-256 `27f75addc4a6d03c3bdd0e69164b59d4a4ce37316ed6a93d19a0dc128d8f4f31`
(lectura de las filas AT-24 a AT-27 a las 20:50, hora de México). Es una propuesta
en curso, sin `seleccion.md` ni intervención adjudicada. No se abrió ninguna ola
reservada ni se calcularon desenlaces.

## Necesidad resuelta

El mapa propone ENCIG 2021/2023 para el trámite de gobierno digital y declara
pendientes la llave de trámite/persona y la geografía. El primer impedimento de
acceso era local: el worktree del ejecutor carece de `data/raw`, pero los seis
objetos requeridos ya están en `/home/pc0/mm-corpus/raw`. Se comprobó desde
`/home/pc0/mm-astra-theta-1` que los dos ZIP son legibles por ruta absoluta.
En el worktree propio se instaló la configuración local y el enlace ignorados
por Git mediante `tools/prepara_corpus.py --aplica`; seis IDs dieron `COINCIDE`.
No se creó ID, copia de payload ni entrada nueva en el manifiesto.

| ID del manifiesto | Ruta real bajo `/home/pc0/mm-corpus/raw/` | bytes | SHA-256 |
|---|---|---:|---|
| `encig_2021_encig21_base_datos_csv` | `encig2021/encig21_base_datos_csv.zip` | 41216579 | `4463e585062961fa1bb200ec830a30d84f1d915f7a3fe4c8454d8198b516b62c` |
| `encig23_base_datos_csv` | `encig23_base_datos_csv.zip` | 38309647 | `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d` |
| `encig2021_cuestionario_pdf` | `encig21_cuestionario.pdf` | 1918370 | `9ee829815e8dca5ebe562b26afb006dcec475840bf27a206a0b838534041e45a` |
| `encig23_cuestionario_pdf` | `encig23_cuestionario.pdf` | 2015393 | `65000ad38419da504e46b34a0a2426f218d1ba6e604ad37a14762bbd07881e1e` |
| `encig2021_estructura_base_datos_pdf` | `encig21_estructura_base_datos.pdf` | 2612238 | `365c031bf48af4c6d65a8e5422c6cf0362500efd37cd0e924e3c1fe38b965dd2` |
| `encig23_estructura_base_datos_pdf` | `encig23_estructura_base_datos.pdf` | 3100802 | `eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906` |

Los tamaños y SHA se revalidaron sobre los seis archivos, no se heredaron solo
del YAML. Licencia: se leyó el 22/sep/2026 el texto de [Términos de Libre Uso
del INEGI](https://www.inegi.org.mx/inegi/terminos.html), apartados 28–42 de
esa página. Permite copiar, adaptar y publicar con crédito al INEGI, y pide
identificar las transformaciones propias. Esta lectura actual no modifica el
campo histórico del manifiesto que dice que su registrador no había verificado
el texto completo. Fuentes de los seis objetos: las URL oficiales ya asentadas
en `data/manifiesto.yaml` bajo los IDs de la tabla.

## Estructura y equivalencia documental

Los descriptores oficiales de ambas olas, sección VII (`encig21_estructura_...`
páginas impresas 47–49; `encig23_estructura_...` páginas impresas 49–50),
permiten esta correspondencia **de campos**, aún sin tabular valores:

| Uso | ENCIG 2021 | ENCIG 2023 | Precisión |
|---|---|---|---|
| llave de trámite y persona | `ID_TRA`, `ID_PER`, `N_TRA` | `ID_TRA`, `ID_PER`, `N_TRA` | Sección VII, miembro `*_04_sec_7.csv` de cada ZIP. |
| entidad y municipio del domicilio muestral | `ENT`, `MUN` | `CVE_ENT`, `CVE_MUN` | Son campos de la unidad entrevistada; no sustituyen lugar del trámite. |
| entidad y municipio donde se realizó el trámite | `P7_1`, `P7_2` | `P7_1`, `P7_2` | `P7_1` admite 01–32 y 99; `P7_2` admite 000–570 y 999 (no sabe/no responde). |
| canal usado | `P7_3` | `P7_3` | Código 4 = Internet; 1 = instalaciones de gobierno; 5 = kiosco/cajero. |
| satisfacción | `P7_12` | `P7_12` | Escala ordinal 1–6 y 9 no respuesta; no es efecto causal por sí misma. |
| problemas del trámite | `P7_4_1` … `P7_4_11` | `P7_4_01` … `P7_4_11` | Cambia la escritura del sufijo, no se asume equivalencia semántica sin cotejo por ítem. |

La documentación de ENCIG declara representatividad nacional y estatal para
población de 18+ en ciudades de 100 mil habitantes o más. Aunque `P7_2` da una
llave municipal del lugar del trámite, **no acredita representatividad municipal**.
Una implementación municipal puede enlazarse documentalmente por entidad,
municipio y tipo de trámite; se deben justificar soporte, exposición efectiva,
fecha y unidad administrativa antes de estimar. `P7_3=4` es canal declarado,
no asignación a tratamiento.

## Acceso del ejecutor y siguiente faltante

Acceso inmediato sin modificar su worktree: abrir las rutas absolutas de la
tabla. Si necesita rutas `data/raw/...`, el dueño de ese worktree puede ejecutar
desde su raíz:

```sh
python3 tools/prepara_corpus.py --config-desde /home/pc0/Modelado-Mexicano/data/raices.local.yaml --id encig23_base_datos_csv --id encig_2021_encig21_base_datos_csv --id encig23_cuestionario_pdf --id encig2021_cuestionario_pdf --id encig23_estructura_base_datos_pdf --id encig2021_estructura_base_datos_pdf --aplica
```

El siguiente faltante es la **fuente primaria de asignación y operación** de
una intervención concreta de trámite, por entidad/municipio, tipo de trámite
y fecha aplicable al periodo ENCIG. Las filas AT-24 a AT-27 no nombran aún una
intervención ni fuente específica. Por eso no se puede adquirir un calendario
compatible ni inferir que no exista; cuando se nombre, distinguir anuncio,
norma y operación efectiva. Este recibo habilita el cotejo del diseño, no elige
θ ni autoriza lectura de resultados reservados.
