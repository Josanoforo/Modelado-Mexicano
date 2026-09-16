<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO EXTERNO tipo 3 (brief emitido por dirección) — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Dirección → Astra
> - **Fecha nominal:** 17/sep/2026 · **fecha de archivo:** 2026-09-16 (fecha de ejecución del entorno; las dos se conservan, no se infiere una firma futura).
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `43f63e1fdf51f270f9d4bc5bcfa1a86161bee74d4e44b663695b4c97b757f5a6`
>   — coincide con el prefijo `43f63e1fdf51f270…` que el encargo declara.
>   Comando: `sha256sum <adjunto>` antes de copiar, y `sha256sum` del cuerpo extraído después.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1.md`, P0.
> - **Nota:** El brief que produjo el retorno de Astra. Se archiva porque dos de sus afirmaciones sobre el repo son falsas y el careo las registra como línea A.13 de dirección (P1 de este acto): «23 momentos» (son 22) y la columna `reglas_impacto` en la demanda (la columna es `consumidor`).

---

# ENCARGO EXTERNO · ASTRA · DISEÑO CIEGO DEL PRIMER PILOTO CELDA-D + ADVERSARIAL DE LA POLÍTICA "CADA CELDA SU ESTIMADOR"
**Dirección → Astra · 17/sep/2026 · árbol fijo `Josanoforo/Modelado-Mexicano @ b881ee6` (lee por `https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/<ruta>`; no leas `main`, se mueve). Tu retorno es insumo externo: no entra al canon sin un acto de verificación posterior. Dirección escribe su propio diseño sin leer el tuyo; se carean al final.**

## 0 · Contexto en diez líneas
El programa modela conducta de población mexicana por celda (segmento × regla). Tiene un motor matricial `g(x)=B·θ(x)` con 15 coeficientes de generador (B) y parámetros condicionados a atributos (θ) que hoy **no computa**: `θ.valor()` lanza para 43/43 nombres y una entrada de B no tiene magnitud (`G5 × familismo_obligacion`, "signo negativo o no monotónico"). Tiene además un contrato adoptado (ADR-68, 11/ago) llamado **celda-D**: `celda-D = (estimando) × (población objetivo)`, con candidatos que compiten bajo un criterio de adjudicación declarado **antes** del dato; existen tres celdas-D registradas. Tiene un árbitro R (puntos con IC por eje, de encuestas oficiales), un baseline de persistencia b (última ola de la misma serie) que en 9 celdas comunes yerra menos que todo lo demás (MAE 0.885 vs M 4.638), y un crosswalk que dice que **ningún** eje del árbitro es equivalente a un corte del modelo (dos son mapeo N-a-1, uno no tiene mapeo).

**Firma de mesa de hoy (mesa la pega verbatim aquí): [FIRMA M1 — A o B]**. En sustancia: cada celda tiene su estimador, su ruta y su dato; el motor no tiene un estimador único; la matriz compone y, donde compita, es un candidato más — nunca el estimador por defecto.

La decisión pendiente es qué celda-D se corre primero y cómo. Cuatro entregables, en orden.

## 1 · Elige la primera celda-D — y di por qué no las otras
Universo: las tres celdas-D registradas (`data/curacion-registro/celdas-d/*.yaml`), los 23 momentos del catálogo (`milpa/catalogo-momentos-v0_1.tsv`) y las 207 filas de demanda activa (`data/corrida0/demanda-resultados.tsv`). Criterios mínimos, cada uno con cita `archivo:línea`: (a) estimando nombrado con **escala y universo** declarados; (b) población objetivo expresable en cortes del modelo **y** en celdas del árbitro vía `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` — si el eje es mapeo N-a-1, di qué resolución se pierde; (c) dato ya adquirido y registrado en `data/manifiesto.yaml` (no propongas fuentes por bajar); (d) al menos **dos candidatos elegibles** de familias distintas; (e) baseline de persistencia construible o no, y por qué; (f) un consumidor identificado (`reglas_impacto` en la demanda) — sin consumidor no hay celda que valga la pena; (g) posibilidad de partición desarrollo/evaluación que no haya sido vista por nadie (U3 ya fue observada: no cuenta). Entrega una **tabla de eliminación**: candidata · criterio que falla · evidencia. Una sola ganadora. Si ninguna pasa los siete, ese es el hallazgo: dilo y para ahí en esta parte.

## 2 · Pre-registro ciego de esa celda (tu diseño v1.0)
Escríbelo como borrador YAML conforme al contrato v0.5 (`propuesta-motor-adaptativo-celda-v0_5.md` §3; v0.3 §2-3 para lo que v0.5 remite) **más** prosa. Obligatorio:
- **Estimando** con escala (proporción, índice, logit — una) y universo (poblacional o restringido; si restringido, a quién). Regla del programa: nunca comparar escalas distintas sin función de enlace declarada.
- **Población objetivo** en cortes del modelo y su celda del árbitro.
- **Candidatos**, mínimo tres: medición directa transversal; `B·θ(x)→h_r` (la matriz) como challenger de `estrategia: momentos` — di qué necesitaría para siquiera correr, incluida la magnitud de G5 si la ruta la toca; persistencia como `BASELINE_INGENUO`. Añade L (LLM con/sin corpus) si tiene sentido, con su dieta de información declarada.
- **Criterio de adjudicación antes del dato**, con escala y umbral, y las dos condiciones de `INDECIDIBLE` del programa citadas verbatim: *"si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)"* (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`). Skill = 1 − error/error(b): di si lo adoptas o por qué no.
- **Qué significa que ningún candidato refute** (regla B-bis del programa: la escala declara qué pasa si el falsador no refuta; si no hay fila para "sobrevivió", la escala está mal).
- **Incertidumbre tipada**: para cada candidato, qué contiene su intervalo (IC muestral / heterogeneidad intra-celda / predictivo / conjunto identificado / envolvente de escenarios) — una sola familia por candidato, no una banda universal.
- **Emitir ≠ decidir**: qué se emite si el intervalo cruza el umbral del consumidor, y cuándo la decisión automática se abstiene.
- **Datos de desarrollo vs evaluación**: cuáles, y qué hace que la evaluación no esté contaminada por la selección.
- **Parada**: qué resultado termina el piloto en factibilidad y cuál en desempeño.
- **Lo que tu diseño NO decide**, explícito.

## 3 · Adversarial: qué se rompe cuando "cada celda elige su estimador" es política de motor
Enumera modos de falla concretos, cada uno con: `nombre · mecanismo (una frase) · ejemplo mínimo con números · síntoma observable · mecanismo mínimo que lo atrapa (una regla o un test, no una capa) · estado en el contrato: YA-PREVISTO (cita v0.3/v0.5/RONDA1) / PREVISTO-SIN-MECANISMO / NO-PREVISTO`. Cubre al menos: selección post-hoc (jardín de senderos: elegir el candidato que dio el resultado que gustó); comparaciones múltiples al adjudicar muchas celdas; **incoherencia entre celdas** (dos vecinas adjudican estimadores que implican signos opuestos del mismo coeficiente — el programa tiene una etapa D8 de coherencia conjunta: di si basta); la persistencia como piso que ningún candidato supera y qué se hace entonces; sobreajuste al árbitro (prohibido por decisión propia — di cómo se detecta, no solo que está prohibido); circularidad ajuste/evaluación en corpus transversales de una sola ola; heterogeneidad de forma (una celda entrega banda, otra punto) al componer agregados; extrapolación fuera de soporte de x en celdas chicas; y **el costo del contrato**: cuántas celdas puede adjudicar el programa con el dato que tiene antes de que el aparato de adjudicación cueste más que lo que decide. Cierra con: *de estas fallas, ¿cuáles hacen que "cada celda su estimador" sea peor que "un estimador único con etiqueta" para un lector de salidas por celda?* — respuesta con argumento, no con preferencia.

## 4 · La interfaz que la composición exige
Si la matriz compone insumos heterogéneos (`m = Σ π(x)·h_r(B·θ(x), C(x))`, `propuesta-motor-matriz-v0_1.md:73-79`), especifica la **interfaz mínima** del catálogo de momentos para que un `h_r` consuma una celda que entrega banda y otra que entrega punto, con pesos π(x) sobre cortes que el árbitro solo cubre a mitad de resolución. Qué campos necesita cada entrada, qué está prohibido (p. ej., colapsar una banda a su punto medio en silencio), y qué prueba pre-composición detecta una escala mal declarada. Tres páginas máximo; si crees que la composición no es viable con estimadores de forma distinta, dilo con el argumento.

## 5 · Formato de retorno (obligatorio)
Cabecera: `investigador · fecha · herramienta · qué leyó (rutas @ b881ee6) · qué no pudo abrir (SIN-FETCH, con lista)`. Toda afirmación sobre el repo cita `archivo:línea` del árbol fijo; toda afirmación externa cita DOI/URL abierta. Citas textuales ≤15 palabras, una por fuente. Un "no encontré" declara dónde y con qué términos — es NO-ENCONTRADO, no "no existe". No leas microdato ni lo pidas; no propongas cifras del modelo; no adjudiques nada. Extensión libre en §2 y §3; §1 y §4 acotadas como se dice.

## 6 · Insumos (todos @ `b881ee6`)
`propuesta-motor-adaptativo-celda-v0_3.md` · `propuesta-motor-adaptativo-celda-v0_5.md` · `propuesta-motor-matriz-v0_1.md` · `forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md` · `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` · `forense/theta-cargable-por-celda-diseno-e1-v1_0.md` · `forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md` · `forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md` · `data/curacion-registro/celdas-d/` (3 yaml) · `milpa/catalogo-momentos-v0_1.tsv` · `data/corrida0/demanda-resultados.tsv` · `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` · `data/manifiesto.yaml` · `milpa/src/matriz.py` · `milpa/src/celdas.py`.
**Adjuntos que mesa pega:** `D-THETA-DOCUMENTO-v1_1-post-adversarial.md` (sha256 `8a6472a72631dfdc…`) y `ADVERSARIAL-D-THETA-v1_0.md` (`850f9cefe4334acd…`, tu propio adversarial — para que no te repitas).
