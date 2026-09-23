# GEN2-38 · investigación ADQ · 2026-09-23

Entorno confirmado antes de caminar: WSL2, clon productivo
`/home/pc0/mm-adq`, `data/raw` enlazado a `/home/pc0/mm-corpus/raw` y
`https://www.inegi.org.mx/` respondió `HTTP 200`. El selector contractual
`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` emitió cero
elegidos; su salida completa está en
`forense/adq-log/2026-09-23T072436-138649-seleccion.json`. Esta nota documenta
las tres investigaciones elegidas por el wrapper y no adopta decisiones
científicas.

## DEM-AHORRO-STOCK-DURACION-01

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`. Modos:
CONSTRUCTO, HERMANAS y LATERAL.

Estado de entrada: ENIF, EACF, ENSAFI, Findex, ENFIH e IIEG Jalisco ya
examinados; P4_10 de ENIF 2024 mezcla «menos de una semana» y «no tiene
ahorros», por lo que no acredita duración condicionada del mismo stock.

Consultas web reales nuevas:

- `site:uanl.mx encuesta bienestar financiero ahorro "meses" cuestionario`
- `site:uv.mx encuesta finanzas personales ahorro "fondo de emergencia" cuestionario México`
- `site:udg.mx encuesta ahorro "cuántos meses" cuestionario finanzas`
- `site:repositorio.cide.edu encuesta ahorro duración "meses" México`

Resultados: UANL devolvió una propuesta metodológica que operacionaliza
variables de ENIF 2024, no un instrumento distinto; UV devolvió divulgación y
material educativo; UDG devolvió una encuesta empresarial sobre meses que los
fondos del negocio soportarían costos, con unidad establecimiento, no persona;
CIDE no devolvió un instrumento pertinente. La búsqueda local
`python3 tools/busca_reactivos.py --palabra ahorro --limite 30` examinó 240072
identidades y volvió a reactivos ENIF ya cubiertos.

Resultado: `continua`, sin candidata pública nueva respecto del corpus.
Frontera no examinada: catálogos variable-por-variable de encuestas financieras
de otras universidades estatales y archivos históricos no indexados de
CNBV/CONDUSEF. Cursor: buscar sólo instrumentos probabilísticos de personas
adultas que separen tenencia/ausencia de ahorro y meses o días del mismo stock.
Alternativa concreta tras más de dos ciclos sin avance: mesa mantiene el
bloqueo, re-etiqueta el uso acotado autorizado por #772 o aprueba un proxy
nuevo con alcance explícito; esta corrida no elige.

## NC-0202

Versión: `2026-09-15-ennvih-diseno-publico-v1`. Modos: LATERAL y HERMANAS.

Estado de entrada: IHSN 7063, el resumen UCLA y las guías oficiales de olas 2
y 3 ya están obtenidos; acreditan identidad y descripción del muestreo, pero
no exponen UPM/estrato/réplicas ejecutables.

Consultas web reales nuevas:

- `"Sample Design of the Mexican Family Life Survey"`
- `"Berumen" "Mexican Family Life Survey" filetype:pdf -guide`
- `site:repositorio.ibero.mx "Berumen" "ENNViH"`
- `site:mxfls.cide.edu "psu" OR "stratum" OR "cluster"`

Resultados: el buscador localizó la página oficial viva de MxFLS y las guías
oficiales públicas `userGuideV1.pdf`, `usersguidev2.pdf` y
`usersguidemxfls-3.pdf`. Las guías nombran `INEGI (2004) Sample Design` y
`Berumen (2007) Sample Design`, describen muestreo probabilístico,
estratificado, multietápico y por conglomerados, y documentan factores; no
publican identificadores de UPM/estrato por observación ni réplicas. Un `curl`
a la portada oficial respondió, pero la ruta supuesta `/english/download.html`
dio `HTTP 404` y no expuso adjuntos adicionales. No se repitieron IHSN, UCLA
ni las guías como adquisición.

Resultado: `continua`. Frontera no examinada: copia pública independiente de
Berumen (2007), el adjunto INEGI (2004) o un archivo oficial que exponga
UPM/estrato/réplicas. Cursor: seguir sólo por esos objetos ejecutables.
Alternativa concreta: el titular activa NC-0156 y el receptor verifica el
contrato recibido; no imputar conglomerados.

## NC-0246

Versión: `AUTO-NC-v1-90c5468401ca`. Modos: CONSTRUCTO, HERMANAS y LATERAL.

Estado de entrada: el objeto no es falta de bytes. El corpus ya contiene y el
manifiesto acredita ENADID 2023 y MOCIBA 2015/2016/2017; además
`CALC-ENADID-0001` ya consume `P3_27_AG`. La parte restante es consumo por un
acto sucesor y decisión de mesa para la serie MOCIBA.

Consultas web reales nuevas:

- `site:inegi.org.mx/programas/enadid/2023 P3_27_AG diccionario datos`
- `site:inegi.org.mx/programas/mociba/2015 "P12" denuncia autoridad`
- `site:inegi.org.mx/programas/mociba/2016 "P12" denuncia autoridad`
- `site:inegi.org.mx/programas/mociba/2017 "P12" denuncia autoridad`

Resultados: la RNM oficial de INEGI confirmó los materiales, microdatos,
estructura, diseño y metadatos públicos de ENADID 2023. Las consultas MOCIBA
no ofrecieron un objeto público nuevo; las tres olas y sus FD ya están en el
corpus con hash coincidente. La verificación local vigente en
`forense/notas/2026-09-22-GEN2-PENDIENTES-CAJA-1-verificacion.tsv` registra
que `enadid2023:P3_27_AG` ya fue consumido por `CALC-ENADID-0001` y que la
parte MOCIBA depende de NC-0237.

Resultado: `barrera`, no por acceso sino porque la acción restante es
implementación/decisión y no investigación externa. Frontera: ninguna ruta
pública adicional puede ejecutar el consumo o resolver la equivalencia de
opciones MOCIBA. Evento de reactivación: mesa resuelve NC-0237 o se asigna el
acto consumidor del panel F6. Alternativa concreta: retirar esta necesidad de
LISTA_SONDA y enrutarla al acto MEDICION-DEMANDA/F6 correspondiente; esta
corrida no reclasifica por cuenta propia.
