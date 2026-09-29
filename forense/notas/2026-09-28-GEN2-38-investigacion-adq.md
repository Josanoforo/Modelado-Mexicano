# GEN2-38 · investigación ADQ · 2026-09-28

Entorno: CAJA acreditada (`/home/pc0/mm-adq`, WSL, `data/raw` →
`/home/pc0/mm-corpus/raw`) y `https://www.inegi.org.mx/` respondió HTTP 200.
Selección de adquisición: cero elegidos; la salida completa, incluidos todos
los excluidos y su razón, vive en
`forense/adq-log/2026-09-28T170002-1081433-seleccion.json`.

## DEM-AHORRO-STOCK-DURACION-01

Definición: instrumento público mexicano que observe por separado
tenencia/ausencia de ahorro y duración suficiente del mismo stock, en persona
adulta.

Se ejecutaron CONSTRUCTO, HERMANAS y LATERAL mediante búsqueda web real:

- `site:edu.mx (encuesta OR cuestionario) ahorro "cuánto tiempo" ahorros México`:
  resultados universitarios homónimos, sin instrumento probabilístico de
  personas adultas que separe stock/ausencia y duración del mismo stock.
- `site:cnbv.gob.mx encuesta ahorro duración ahorros cuestionario personas México`:
  devolvió la página de encuestas CNBV, ENIF 2012/2015/2024 y una base agregada
  de ahorro financiero. ENIF es familia ya examinada; la base CNBV es agregada
  y no observa el par pedido por persona.

No apareció candidata pública nueva pertinente. La pregunta sigue ABIERTA y
el uso `horizonte_corto` sigue INCOMPATIBLE. Frontera no examinada concreta:
catálogos variable-por-variable de encuestas financieras de universidades
estatales distintas de IIEG y archivos históricos no indexados de CONDUSEF.
Cursor: buscar sólo instrumentos probabilísticos de adultos que separen
tenencia/ausencia y meses o días del mismo stock. Alternativa tras más de dos
ciclos sin avance: mesa elige entre mantener el bloqueo, relabel del uso
acotado autorizado por #772 o aprobar un proxy nuevo con alcance explícito.

## NC-0170

Definición: verificar el retro-sello de las excepciones históricas y la
decisión sobre si `[COLA]`/`[ADQ]` constituyen cuarta categoría exenta.

Se ejecutaron CONSTRUCTO, HERMANAS y LATERAL contra GitHub, fuera del corpus:

- `gh pr view 680`: MERGED, título `GEN2-R: completa árbitros del marco de 14 celdas`.
- `gh pr view 701`: MERGED, título `ADENDA GEN2-PUBLICACION-POST693: concilia cierres acreditados`.
- `gh pr view 759`: MERGED, modifica el encargo `GEN2-CONSUMIDO-RETRO-3`.
- `gh pr view 795`: MERGED, modifica los encargos asociados a #680 y #701.

La vía pública confirma la evidencia ya consignada: la mitad de retro-sello
fue ejecutada o reasentada. No es una necesidad de fuente externa ni produce
candidata adquirible. Queda una barrera de decisión: mesa debe decidir si
`[COLA]`/`[ADQ]` son cuarta categoría exenta. Evento de reactivación: firma de
mesa que resuelva esa categoría. No se tomó aquí esa decisión.

## NC-0246

Definición: consumir identidades ya recuperadas en CORR-0013 y en la serie F6.

Se ejecutaron CONSTRUCTO, HERMANAS y LATERAL contra la búsqueda pública de
código de GitHub:

- `gh api search/code?q=P3_27_AG+repo:Josanoforo/Modelado-Mexicano`: total 0,
  resultado incompleto del servicio.
- `gh api search/code?q=CORR-0013+repo:Josanoforo/Modelado-Mexicano`: total 0,
  resultado incompleto del servicio.
- `gh api search/code?q=mociba2015+repo:Josanoforo/Modelado-Mexicano`: total 0,
  resultado incompleto del servicio.

La búsqueda externa no sustituye el consumo interno firmado ni descubre un
objeto público nuevo. La necesidad es de implementación, no de adquisición.
Frontera concreta: el siguiente acto MEDICION-DEMANDA que tenga en perímetro
CORR-0013 debe enlazar `enadid2023:P3_27_AG`; F6-PANEL-CAJA-1 o sucesor debe
tratar MOCIBA 2015/2016/2017. Evento de reactivación: asignación de uno de esos
actos. ENUT 2024 y ENFIH 2019 no requieren acción.

No hubo descarga ni intento de objeto; por tanto no se consumieron checkpoints
de objetos, no se creó residual y no se tocó la cola ni el manifiesto.
