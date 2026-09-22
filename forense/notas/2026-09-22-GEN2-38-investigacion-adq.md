# GEN2-38 · investigación ADQ · 2026-09-22

Entorno confirmado antes de caminar: WSL2, clon productivo
`/home/pc0/mm-adq`, `data/raw` enlazado a `/home/pc0/mm-corpus/raw` y
`https://www.inegi.org.mx/` respondió `HTTP 200` desde `200.23.8.5`.
`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` emitió cero
elegidos. Esta nota documenta las tres investigaciones entregadas por el
wrapper; no adopta una decisión científica.

## DEM-AHORRO-STOCK-DURACION-01

Definición: instrumento público mexicano que observe por separado
tenencia/ausencia de ahorro y duración suficiente del mismo stock.

Modos: CONSTRUCTO, HERMANAS, LATERAL.

Consultas web reales:

- `site:edu.mx encuesta finanzas personales cuestionario ahorro "meses" "ahorros" México`: devolvió publicaciones educativas y estudios locales; no acreditan instrumento probabilístico para adultos de México con ambos campos separados.
- `site:condusef.gob.mx encuesta cuestionario ahorro "cuántos meses" OR "cuanto tiempo"`: devolvió materiales de educación financiera, no un instrumento nuevo.
- `site:cnbv.gob.mx encuesta ahorro fondo emergencia meses cuestionario PDF`: devolvió ENIF 2015/2021/2024 y ENSAFI, familias ya examinadas. El resultado de ENIF 2015 sobre tiempo para disponer de activos no mide duración del mismo stock de ahorro.

Resultado: continúa. No hay candidata nueva respecto del corpus. La frontera
concreta no examinada queda en catálogos variable-por-variable de encuestas
financieras de universidades estatales y archivos históricos no indexados de
CNBV/CONDUSEF. Cursor: buscar un instrumento probabilístico con indicador de
tenencia/ausencia y meses o días del mismo stock. Tras más de dos ciclos sin
avance material, alternativa concreta para mesa: mantener el bloqueo,
re-etiquetar el uso acotado ya autorizado por #772, o aprobar un proxy nuevo
con alcance explícito; esta corrida no elige entre ellas.

## NC-0202

Definición: identificador público de UPM/estrato, réplicas o pesos que permitan
incertidumbre de diseño para ENNViH/MxFLS olas 2 y 3.

Modos: LATERAL, HERMANAS.

Consultas web reales:

- `"Berumen" "Mexican Family Life Survey" sample design 2007 pdf`: devolvió las guías ENNViH/MxFLS ya examinadas, que citan el documento de trabajo, y literatura secundaria; no una copia pública de Berumen (2007).
- `"Encuesta Nacional sobre Niveles de Vida de los Hogares" "Berumen" 2007 diseño muestral`: volvió a referencias bibliográficas sin objeto ejecutable.
- `site:mxfls.cide.edu "strata" OR "PSU" OR "UPM" data dictionary`: no devolvió un diccionario con UPM/estrato por observación.
- `site:icpsr.umich.edu/studies/118971 MxFLS documentation`: no devolvió documentación del estudio con réplicas o identificadores ejecutables.

Resultado: continúa. La identidad y el concepto están acreditados; el diseño
ejecutable sigue parcial. Frontera: copia pública de Berumen (2007) o archivos
que expongan UPM/estrato/réplicas. Cursor: continuar sólo por esos objetos, sin
repetir IHSN, UCLA ni las guías. Alternativa concreta: que el titular active
NC-0156 y el receptor verifique el contrato recibido; no imputar conglomerados.

## NC-0170

Definición vigente: decisión de mesa sobre si entregas `[COLA]`/`[ADQ]` son
cuarta categoría exenta; el retro-sello previo está ejecutado o reasentado.

Modos: CONSTRUCTO, HERMANAS, LATERAL.

Comprobaciones:

- Búsqueda local `rg -n "cuarta categoria exenta|\[COLA\].*\[ADQ\]|categoria exenta" forense canon data`: sólo devolvió la propuesta original, digestos y notas que declaran pendiente la decisión; no una firma posterior.
- Búsqueda web `site:github.com/Josanoforo/Modelado-Mexicano "cuarta categoria exenta"`: sin resultado pertinente.
- Búsqueda web `site:github.com/Josanoforo/Modelado-Mexicano "EXCEPCIÓN-COLA/ADQ"`: sin resultado pertinente.
- Búsqueda web `site:github.com/Josanoforo/Modelado-Mexicano "COLA" "ADQ" "exenta"`: sin resultado pertinente.

Resultado: barrera, porque el residual es una decisión humana y no una fuente
o variable adquirible. Frontera: conversación o firma de mesa todavía no
publicada/indexada. Cursor: no repetir búsqueda documental; reactivar cuando
mesa responda si `[COLA]`/`[ADQ]` integran la cuarta categoría exenta. La
alternativa concreta es mantenerlas como excepción explícita o incorporarlas
a la lista de categorías exentas; esta corrida no clasifica por mesa.
