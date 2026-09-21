# Nota de cierre · ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1 · 20/sep/2026

**Universo, unidad, escala y clase de evidencia (primera línea obligatoria):** universo = el INSTRUMENTO (cuestionarios, FD y modelos de datos de ENIF 2012/2015/2018/2021/2024), no la población; unidad = par conducta × ola (40); escala = veredicto categórico en lista cerrada de cinco valores; clase de evidencia = lectura de texto público de INEGI (clase (a) por origen, pero **no es evidencia sobre México**: es evidencia sobre lo que se preguntó). Cero microdato abierto. **Contadores movidos: ninguno** — `cuenta_gen2 = NO-APLICA`, `N_corridas_selladas`, `N_resultados_*` y `adoptados_activos` intactos por diseño del encargo.

Encargo: `forense/encargos/2026-09-20-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1.md` (A.3). Insumo de mesa archivado: `forense/encargos/2026-09-20-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1-INSUMO-K1-K8.md`. Entregable: `data/credito-comparabilidad-texto-v1_0.tsv` + `.meta`, `tests/test_credito_comparabilidad_texto.py` (cableado en `verify.yml` y censado), fila en `data/INFRAESTRUCTURA-v1_0.md`.

## 0 · Arranque (crudo)

- Rama `acto/gen2-din-credito-comparabilidad-texto-1` sobre `bd9ed213` = `origin/main` al abrir (`git rev-list --count HEAD..origin/main` → 0). El SHA de redacción coincide; `8d639a01` es su ancestro (verificado). Árbol limpio. Duplicado (0.c): `git ls-remote --heads origin | grep -i credito-comparabilidad` → 0; `git worktree list` → sólo el propio; `gh pr list --search CREDITO-COMPARABILIDAD --state open` → 0. Higiene (0.d): `limpia_arbol.py --reporta` → base al día, `fuera_de_politica: 0`.
- `tools/entorno.py --arranque` → `ENTORNO-DERIVADO = CAJA`, `montado=SI archivos_examinados=419`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red PERMITIDA (200). Coincide con el encargo.
- `data/raw` enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre (gitignorados ambos, per-worktree).
- **0-bis con discordancia declarada:** dirección depositó en `descargas_mx` sólo el `.sha256` del encargo (`73c074de6486be46aa58494924c3677b03256ade87ab93763f9095175ea8054b`) y no el `.md`; el archivo archivado es el texto pegado en la sesión (tablas aplanadas), con su propio `.sha256`. No se colapsa: se declara en la cabecera del encargo archivado.
- **La lista K1–K8 no vivía en el árbol** (`grep` de «K4», «gota a gota», «empeño» en `canon/`, `forense/`, `milpa/`: sólo el propio encargo y dos documentos del corpus sin la lista) ni en `descargas_mx`. Se pidió a dirección con tres opciones (pegar / reconstruir y proponer / otra ruta), dirección la pegó y se archivó verbatim antes de escribir una sola fila.

## 1 · Compuerta (protege: abrir dato) — cumplida

`python3 tests/manifiesto.py --verifica --id <id>` para los 12 documentos de las cinco olas, salida cruda:

```
enif_2012_fd_enif2012 [data_raw]: COINCIDE -- sha256 y tamaño (148265 bytes) verificados contra data/manifiesto.yaml
enif_2012_modelo_enif2012 [data_raw]: COINCIDE -- sha256 y tamaño (17754 bytes) verificados contra data/manifiesto.yaml
enif_2015_enif_2015_fd [data_raw]: COINCIDE -- sha256 y tamaño (219503 bytes) verificados contra data/manifiesto.yaml
enif_2015_enif_2015_modelo_datos [data_raw]: COINCIDE -- sha256 y tamaño (981987 bytes) verificados contra data/manifiesto.yaml
enif2018_fd_xlsx [data_raw]: COINCIDE -- sha256 y tamaño (246905 bytes) verificados contra data/manifiesto.yaml
enif2018_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1688866 bytes) verificados contra data/manifiesto.yaml
enif2021_fd_zip [data_raw]: COINCIDE -- sha256 y tamaño (1229311 bytes) verificados contra data/manifiesto.yaml
enif2021_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1214633 bytes) verificados contra data/manifiesto.yaml
enif_2021_enif_2021_modelo_er_pdf [data_raw]: COINCIDE -- sha256 y tamaño (153624 bytes) verificados contra data/manifiesto.yaml
enif2024_fd_xlsx [data_raw]: COINCIDE -- sha256 y tamaño (122271 bytes) verificados contra data/manifiesto.yaml
enif2024_cuestionario_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1228366 bytes) verificados contra data/manifiesto.yaml
enif_2024_enif_2024_modelo_logico_pdf [data_raw]: COINCIDE -- sha256 y tamaño (124392 bytes) verificados contra data/manifiesto.yaml
```

A.1 sin colapsar: **12 COINCIDE · 0 AUSENTE · 0 raíz-no-configurada · 0 hash-discordante.** Ningún miembro de datos de ninguna ola se abrió; de 2024 sólo cuestionario, FD y modelo lógico (§7 a, respetado).

## 2 · Premisas verificadas (por rótulo)

| premisa | rótulo | resultado |
|---|---|---|
| cinco olas en manifiesto; cuestionario sólo en 2018/2021/2024 | EJECUTADO | Confirmado: el `grep` del encargo devuelve los seis ids; 2012 y 2015 sólo tienen FD (xlsx), modelo de datos (pdf) y bases. El modelo de datos 2015 es **una página imagen sin texto extraíble**; el de 2012 lista nemónicos por tabla. |
| `ENIF-FINTECH-SERIE-spec` líneas 17-20 (2018 sin canal; 18–70 vs 18+) | LEÍDO | Confirmado por texto, y ahora con el texto buscado citado (K7-2018). |
| único sitio del repo con crédito ENIF; ninguna spec cubre K1–K8 | EJECUTADO | Repetido con mi acceso: 22 archivos con `P6_` en prereg+corrida0 (ENSAFI, ENCUCI, FINTECH); 8 encargos con ENIF ∧ crédito (ENAFIN, tandas, fintech, docs) — ninguno hace comparabilidad por texto. **NO-ENCONTRADO** para el objeto. 30 NC abiertas con «crédito/enif», ninguna sucedida por este acto. |
| NC-0304 (P5_6 ≠ P5_7) | LEÍDO | Es exactamente la clase de defecto que la tabla deja escrita cuatro veces más (§4). |
| molde de la nota del piloto 3 §2 | LEÍDO | Reutilizado: tres columnas de cita + vocabulario. |
| 37 payloads / ENIGH 2024 (mesa) | REPORTADO | No usado como premisa; nada se descargó. |
| hipótesis del corpus (37.3 %, 22.6 % > 15.7 %, …) | REPORTADO | No usadas para validar ninguna lectura. Una de ellas queda **contaminada por instrumento** (K2 bancaria 2024, §4). |
| las cinco olas tienen sección de crédito identificable | SUPUESTO | **Cierto en las cinco** («SECCIÓN 6. CRÉDITO INFORMAL Y FORMAL» en 2012, 2015, 2018, 2021, 2024), con una salvedad: en 2015 la sección se reparte entre dos tablas del FD (6.1–6.5 en `TModulo1`, 6.6–6.21 en `TModulo2`). |

## 3 · P1 · Inventario por instrumento (A.15)

| ola | documento | sección literal | reactivos de crédito (campos FD) | notas de estructura |
|---|---|---|---|---|
| 2012 | FD `fd_enif2012.xlsx` `TMODULO1` filas 445-842; modelo `modelo_enif2012.pdf` | SECCIÓN 6. CRÉDITO INFORMAL Y FORMAL (6.1–6.20) | 109 campos `P6_*` | Filtro único 6.4; batería 6.6 con orden bancaria/departamental **invertido**; 6.5 razón de no tenencia **multirrespuesta**; sin «alguna vez tuvo»; 6.16 destino; 6.18 racionamiento parcial; 6.12 sobreendeudamiento autopercibido. Universo 18–70 (NOTAS ACLARATORIAS fila 15). |
| 2015 | FD `enif_2015_fd.xlsx` `TModulo1` filas 559-624 + `TModulo2` filas 9-332; modelo = imagen | SECCIÓN 6 (6.1–6.21) | 23 + 101 campos `P6_*` | 6.1 informal con **otro orden** (familiares, amigos, caja, empeño); 6.2 intereses por fuente; 6.4 filtro fusionado; 6.5 alguna vez; 6.6 razón **multirrespuesta**; 6.9 batería; 6.13 atraso en una variable de 5 códigos; 6.19 destino; 6.20 rechazo. Universo 18–70 (`EDAD [18-70]`). |
| 2018 | cuestionario pdf-págs 12-15; FD `TModulo` filas 410-599 | SECCIÓN 6. CRÉDITO INFORMAL Y FORMAL (6.1–6.19) | 89 campos | Filtro en **dos etapas** (6.3 → 6.4 → 6.5) antes de la batería 6.8; 6.2 y 6.12 destino (informal / formal filtrado a nómina-personal-grupal); sin canal de contratación; sin sobreendeudamiento (6.15 pago de tarjeta). Universo 18–70 («DE 18 A 70 AÑOS», pág 3). |
| 2021 | cuestionario pdf-págs 15-19; FD `TModulo` filas 611-899 | SECCIÓN 6. CRÉDITO INFORMAL Y FORMAL (6.1–6.18) | 96 campos | Batería 6.2 **directa** (sin filtro); 6.3 número de productos; 6.4 atraso; 6.7 canal; 6.8 institución; 6.14 alguna vez; 6.15 razón principal; 6.17 rechazo. **Sin destino.** Universo 18+ («DE 18 AÑOS Y MÁS», pág 5). |
| 2024 | cuestionario pdf-págs 16-20; FD `TMODULO` filas 665-903 | SECCIÓN 6. CRÉDITO INFORMAL Y FORMAL (6.1–6.17) | 84 campos | Como 2021 menos «cuántos tiene» y «institución»; 6.1a intereses (sólo ítems 3-5); 6.2.2 ampliada a «u otra institución financiera»; 6.12a cooperativa/microfinanciera. **Sin destino.** Universo 18+ (pág 4). |

Bancarización (D3-c, fuera de K1–K8, sólo se verifica): tenencia de cuenta existe en las cinco olas — 2012 5.3 (única), 2015 5.4 (única), 2018 5.4/5.5 filtro + 5.9 batería, 2021 5.4 batería directa, 2024 5.4 batería directa — con el **mismo patrón** de filtro previo en 2018 y anteriores que tiene crédito. El eje de segmento es construible; su comparabilidad fina no es de este acto.

## 4 · P2–P4 · La tabla, en cinco líneas y una matriz

`data/credito-comparabilidad-texto-v1_0.tsv`: 40 filas, 18 columnas, ola ancla 2021. Conteo derivado (`cut -f5 | sort | uniq -c`): MISMO-INSTRUMENTO 8 · CAMBIO-MENOR 11 · CAMBIO-DE-INSTRUMENTO 2 · NO-ESTIMABLE 3 · NO-VERIFICABLE-AQUÍ 16.

| | 2012 | 2015 | 2018 | 2021 | 2024 |
|---|---|---|---|---|---|
| K1 tenencia formal | NVA | NVA | CM | ancla | CM |
| K2 por familia | NVA | NVA | CM | ancla | **CDI (bancaria)** |
| K3 informal | NVA | NVA | CM | ancla | CM |
| K4 motivo (a)/(b) | NVA | NVA | CM | ancla | CM |
| K5 rechazo | NVA | NVA | CM | MI | MI |
| K6 atraso | NVA | NVA | CM | ancla | CM |
| K7 canal | NVA | NVA | **NE** | ancla | CM |
| K8 destino | NVA | NVA | **CDI (unidad P)** | **NE** | **NE** |

(NVA = NO-VERIFICABLE-AQUÍ · CM = CAMBIO-MENOR · MI = MISMO-INSTRUMENTO · CDI = CAMBIO-DE-INSTRUMENTO · NE = NO-ESTIMABLE.) La consecuencia de cada celda vive en la tabla; aquí sólo el mapa.

Lo que la tabla deja escrito y que el sucesor ya no tiene que redescubrir:

1. **2018 entra a la serie en K1–K6** (firma D2) con dos condiciones declaradas por fila: recorte de 2021/2024 a 18–70, y la regla blanco→No del filtro 6.3/6.4 (la batería sólo la responde quien dijo Sí en el filtro). 2018 **no** entra a K7 (NO-ESTIMABLE, texto buscado citado) ni a K8 como serie (unidad P, no PR).
2. **K2 bancaria 2024 es CAMBIO-DE-INSTRUMENTO**: 6.2.2 pasa de «tarjeta de crédito bancaria» a «tarjeta de crédito bancaria u otra institución financiera». La hipótesis REPORTADO «bancaria +5.2 pp desde 2021» mezcla este cambio de frontera con el cambio real y no se usa sin función de enlace. Departamental, nómina y automotriz sí son MISMO-INSTRUMENTO 2021↔2024.
3. **K4(a)/(b) es separable en 2018, 2021 y 2024** (razón principal, un código; opciones 1/3/2 = oferta, 6/7 = autoexclusión): la rama de P5 «K4b no separable en ninguna ola» **no se abre**; K4 es construible en ENIF. Dos matices que sí entran a la tabla: la base es «nunca ha tenido crédito formal», no «no tiene hoy» (los ex-usuarios reciben otro catálogo), y en 2012/2015 la pregunta es multirrespuesta (veredicto esperable CDI cuando llegue el cuestionario).
4. **K5 (rechazo) es el reactivo más estable**: texto idéntico en las cinco olas, universal, con «Nunca lo ha solicitado» separado desde 2012. D3(a) verificado.
5. **Cuatro colisiones de nemónico de la clase NC-0304**, ahora escritas: `P6_3_k` = «cuántos» (2021) vs «se atrasó» (2024); `P6_6_1/_2` de 2012 = bancaria/departamental (orden invertido respecto de 2015+); `P6_1_k` de 2015 con otro orden de fuentes informales; código 8 de razón de no tenencia = «Otro» (2018) vs «impuestos» (2021+).
6. **Fiado y gota a gota no tienen casilla en ninguna ola** (`texto_buscado` en las 5 filas de K3); empeño sí, en todas. La pieza de mesa «no fundir empeño con gota a gota» está a salvo por construcción: sólo uno de los dos se pregunta. 6.1a de 2024 («le cobran intereses») es EXISTE-NO-SATISFACE para gota a gota.
7. **K8 (destino) no existe en 2021 ni 2024** y en 2012–2018 existe con unidad P, multirrespuesta y (en 2018, verificado) filtrado a nómina/personal/grupal. El dominio no tiene K8 en la ola que sirve de piso.
8. Unidad (P3): K1, K3, K4, K5 son P en todas las olas; K2 es P por familia (2024 pierde el paso a PR al eliminar «cuántos»); K6 es PR por producto, agregable; K7 es PR «último crédito» (una observación por persona, sin saber de qué producto); K8 sólo existe como P.
9. Población base (P4): 18–70 en 2012, 2015 y 2018 (verificado por texto en las tres); 18+ en 2021 y 2024. Ninguna fila 2018 es MISMO-INSTRUMENTO por esta razón.

## 5 · P5 · D3 verificado por texto

(a) Rechazo: sí, cinco olas (K5). (b) Motivos con exclusión por oferta separable de autoexclusión: sí en 2018/2021/2024 con un código; en 2012/2015 multirrespuesta, separable en catálogo pero no en instrumento (K4). (c) Bancarización: sí, cinco olas (§3). **D3 se sostiene en las tres** para 2018+; ADR-35 no se toca (ninguna fila modela al prestamista; las razones de rechazo 6.18/6.17 son autorreporte del solicitante) y FP-61 no se toca.

## 6 · P6 · Ficha de límites (A.4)

- EXISTE-SATISFACE: K1, K2 (3 de 4 familias), K3 (empeño, conocidos), K4, K5, K6 en 2018/2021/2024; K7 en 2021/2024.
- EXISTE-NO-SATISFACE: K2 «durable» (sólo vía tarjeta departamental o destino); K3 gota a gota vía 6.1a de 2024 (interés ≠ prestamista predatorio); K8 en 2012–2018 (unidad P, no PR); 6.18 de 2012 (racionamiento parcial, sin serie); 6.12 de 2012 y 6.6/6.7 de 2021/2024 (sobreendeudamiento, catálogos distintos).
- NO-ENCONTRADO: fiado y gota a gota en los cinco instrumentos (términos y universo en `texto_buscado`); canal de contratación en 2018 (cuestionario completo + FD); destino en 2021/2024 (cuestionario completo + FD); la lista K1–K8 en el árbol al arrancar (resuelto por dirección).
- NO-ACCESIBLE: cuestionarios 2012 y 2015 (no en corpus; sucesor 3); texto del modelo de datos 2015 (imagen).
- Hueco de la RESERVA: el par «crédito por app» 2021×2024 (`P6_2_8 × P6_7` / `P6_2_8 × P6_6`) está visto y consumido en `CALC-ENIF-FINTECH-0001`; la fila K7 lo registra y no se relanza. La sección de crédito de 2024 sigue reservada: este acto sólo leyó cuestionario, FD y modelo lógico.

## 7 · P7 · El test, y por qué corrió primero en sintético

`tests/test_credito_comparabilidad_texto.py`: `verificar()` devuelve la lista de defectos; seis pruebas sintéticas (una tabla mínima válida como control positivo y cinco mutaciones que deben fallar: 39 filas, veredicto fuera de lista, NO-ESTIMABLE sin texto buscado, NO-VERIFICABLE-AQUÍ en ola con cuestionario, obligatoria vacía + positivo sin reactivo) y dos sobre la tabla real (forma + conteo por veredicto pinado). Corrió: 8/8 OK. El pin del conteo falló una vez a la primera —yo había tecleado 7/4 y la tabla dice 8/3— y ése es el defecto que D-22 existe para atrapar antes de declarar nada congelado. Cableado en `.github/workflows/verify.yml` (paso bloqueante) y censado en `forense/analisis/ci-guardias/censo-tests.tsv` (una fila; `ci_guardias.py --ejecuta-huerfanos` → 0 fallidos, ningún huérfano nuevo). No regeneré el censo entero con `--censo`: en esta caja reclasifica 74 filas ajenas por tener numpy/pandas, y eso es de otro acto.

## 8 · Latitud ejercida (§6)

Orden: inventario → 2021 (ancla) → 2024 → 2018 → FD 2012/2015 → tabla → test → cascada. Extracción: `pdftotext -layout`, `openpyxl` read-only, `zipfile` (no hay `unzip` en la caja). Columnas añadidas a las mínimas: `conducta_texto`, `comparado_con`, `alcance_del_veredicto`, `componentes_no_estimables`, `limite_fd`. El generador de la tabla vive en el scratchpad de la sesión y no se commitea: el artefacto es el TSV. Ninguna dependencia instalada; ningún defecto adyacente tocado; no se editó ningún archivo ajeno al perímetro.

## 9 · Preguntas a mesa (con recomendación; el acto siguió sin esperarlas)

1. **K8 sin instrumento en 2021/2024.** Opciones: (i) sacar K8 de la serie ENIF y buscarlo en ENSAFI 2023 / ENFIH 2019 como triangulación rotulada; (ii) redefinir K8 como «destino de créditos de nómina/personal/grupal, unidad P» y medirlo sólo en 2012–2018 como serie propia; (iii) mantener la definición PR y declararlo SIN-INSTRUMENTO. **Recomendación: (ii)** — es lo que el instrumento pregunta, y (i) puede sumarse después. `FP-402`.
2. **K2 bancaria 2024.** Opciones: (i) reportar bancaria 2021↔2024 sólo con la advertencia de frontera; (ii) construir en 2021 una «bancaria ampliada» = 6.2.2 ∪ 6.2.8 ∪ (6.2.9 con especifique, no disponible) y declararla cota; (iii) no comparar la familia. **Recomendación: (iii) para la serie, (i) rotulado para el descriptivo.** `FP-402` (mismo asiento, dos incisos).
3. K4b **no** requiere decisión: es separable. Se informa, no se pregunta.

## 10 · Auditoría (§5, tres líneas obligatorias)

1. Que dos olas pregunten lo mismo **habilita medir y no dice qué se va a encontrar**: ninguna fila de la tabla es una cifra sobre conducta.
2. El universo de ENIF es población de 18+ (18–70 hasta 2018) en viviendas particulares, con submuestreo conocido del mundo rural y de localidades pequeñas: cualquier conducta de crédito leída ahí **sobre-representa al urbano bancarizado**; el instrumento lo agrava en 2018 y antes, donde la batería de productos sólo la contesta quien pasó un filtro.
3. K4 va partido porque «no le gusta endeudarse» y «no cumplo los requisitos» **producen la misma conducta observada y significan cosas opuestas**; la tabla muestra que el instrumento las separa desde 2018 con un solo código, y que en 2012 la casilla de autoexclusión venía fundida con «no lo ha solicitado» — colapsar es leer estructura como cultura, y el instrumento viejo ya lo hacía a medias.

## 11 · Hallazgos, NC, FP

- `forense/hallazgos.md`: una línea (la colisión `P6_3_k` 2021/2024 y las otras tres, como clase).
- `NC-0423`: cuestionarios 2012/2015 no accesibles → 16 filas NO-VERIFICABLE-AQUÍ (DIFERIDO-A sucesor 3). `NC-0424`: K8 sin instrumento en 2021/2024 (DECISIÓN-DE-MESA-PENDIENTE, FP-402). `NC-0425`: K2 bancaria 2024 no comparable sin enlace (DECISIÓN-DE-MESA-PENDIENTE, FP-402).
- `FP-402`: las dos preguntas de §9.

## 12 · Sucesores (orden del encargo)

1. Marginales de crédito ENIF 2021 (y 2018 en K1–K6 con el recorte 18–70) — puede arrancar con esta tabla sin releer texto; su falsador es el de §10 del encargo.
2. Regla de elección del cruce del piloto de ahorro — dirección.
3. Adquisición de cuestionarios ENIF 2012 y 2015 → mesa → NUBE-MEDICIÓN; al llegar, las 16 filas NVA se resuelven con el `limite_fd` ya escrito (las de K7 pasan a NO-ESTIMABLE con el texto buscado que ya está; las de K4 y K8 esperan CDI).
