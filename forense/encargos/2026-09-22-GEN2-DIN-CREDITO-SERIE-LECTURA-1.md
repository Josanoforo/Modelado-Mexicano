# ENCARGO · ACTO GEN2-DIN-CREDITO-SERIE-LECTURA-1 · La serie de crédito 2012–2021 conmensurada, leída de los sellos: primer producto de la línea de dinero, con su frontera y sin tocar el emisor

> ENTORNO: **NUBE** — cero microdato: lee RESULT sellados. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **ABIERTO** · CONTADOR: cero mediciones; primer producto de crédito con cadena (una nota + una tabla derivada) · ids raíz de acto.

## 1 · OBJETIVO
Que exista, leída **solo** de RESULT sellados, la serie conmensurada de los pisos de crédito por eje y nacional — ENIF 2012 (`#943`), 2015, 2018 (`CALC-DIN-CREDITO-PISOS-ENIF2018-0001`), 2021 recortada 18-70 (`CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`, #1008) y K2-bancaria historia (`-0001`, con la `-0002` como réplica) — con la frontera FP-404 (2) escrita, la escala y unidad por celda, y el rótulo DESCRIPTIVO; y que quede claro qué de esto puede consumir el emisor y qué no (v2.16 §3: oferta antes que preferencia — cada marginal de crédito se publica con la medida de exclusión por oferta al lado, si está sellada; si no, se dice). «Hecho» = `forense/analisis/credito-serie-2012-2021/serie.tsv` (`regla · eje · celda · ola · punto · ic · n · universo · escala · CALC · RESULT`) derivado por comando; nota con la lectura (qué cambia entre olas, qué no es comparable y por qué, qué es CAMBIO-DE-INSTRUMENTO); ninguna cifra sin id de RESULT.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: FP-404 (2) (frontera del descriptivo), firma ff56-01 (a) (recorte 18-70), F1 de FIRMAS-7 (K2 `-0002` réplica). Ninguna nueva.

## 3 · LO QUE DIRECCIÓN SABE
- `[EXISTE]` los cinco CALC citados, sellados con asiento (dos sin fila en la vista hasta E11). `[LEÍDO]` v2.16 §3: «todo marginal de conducta de mercado (crédito, ahorro, canal) se publica con la medida de exclusión por oferta al lado». No sé si la exclusión por oferta está sellada por ola: **el acto lo busca por objeto**; si no está, cada fila lo declara.
- `[SUPUESTO]` Las definiciones K1–K6 son idénticas por texto en las cuatro olas (los actos de pisos lo verificaron por archivo). Si un K difiere en una ola, la serie lo marca `NO-COMPARABLE` con la diferencia.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls forense/analisis/ | grep -i "credito"` → reporta; `grep -rl "serie.*credito\|crédito.*serie" forense/notas/` → reporta. Ramas vivas: ninguna con este objeto.

## 5 · PIEZAS
- **P1 · Tabla derivada** por comando desde `resultados.json` de los cinco CALC (script en el mismo directorio, reproducible).
- **P2 · Lectura**, dos páginas: qué se mueve entre 2012 y 2021 por eje, con IC; qué es artefacto de instrumento; qué queda fuera por la frontera FP-404 (2). Módulo de auditoría de rigor extremo **sí carga** (afirma sobre México): pobreza/oferta vs preferencia; clase media urbana; rural.
- **P3 · Para el emisor:** qué RESULT son consumibles hoy como piso (rótulo, escala, universo) y qué exigiría una firma; ninguna edición de `tramite.yaml`.

## 6 · LATITUD
DECIDES TÚ: formato, orden. PREGUNTAS A MESA: si la exclusión por oferta no está sellada, ¿la serie se publica con la columna vacía y rotulada (recomendado) o espera? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar CALC · c) adoptar · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna. Orden sugerido: después de #1015 (F1 réplica en main).

## 9 · PERÍMETRO
Propio: `forense/analisis/credito-serie-2012-2021/` (nuevo) · nota · `canon/L0/<raíz>.md`. Ajeno: CALC, `tramite.yaml`, el informe (v1.3 la cita). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No mide, no adopta, no edita el emisor. Sucesor: informe v1.3 (dirección) y la firma de consumo por el emisor. Auditoría: contestada en la nota. Cierre por /acto.


