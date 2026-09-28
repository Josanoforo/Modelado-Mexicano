# P3 · D1 · verificación de descontinuación (GEN2-OBTENCION-PREVIA-1)

Contadores movidos: 0 (pieza de verificación documental; no mide).

Fecha: 2026-09-28 · entorno NUBE con red (INEGI 200) · curl -sSL (sin -I). Tabla: `P3-D1-descontinuados.tsv`. Payloads: `data/raw/obtencion-previa-1/d1/` (sha256 en la tabla).

## Resultado
Ninguno de los 4 obtuvo DESCONTINUADO-CITABLE: ninguna página de programa trae texto de baja (los cuerpos se cargan por JS).
- CAAS 2015 → SUCESORA-EXISTE: el CAAS se volvió a levantar dentro del CPV 2020 (descriptor 200; `cpv2020_caas_*` ya en manifiesto).
- ENG 2009 → SUCESORA-EXISTE: los ids `cc1_inegi_eng_2009__*` apuntan a `/eng/2010/` = ENGPEE 2010. Tuvo como sucesor el CNGSPSPE 2011 y ahora es el CNGE (2024 y 2025 en portal). Hallazgo: el rótulo de ola "2009" no coincide con la URL (2010).
- ENCRIGE 2016 → SUCESORA-EXISTE: ENCRIGE 2020 ya está en el corpus (`conjunto_de_datos_encrige_2020_csv`, `encrige2020_cuestionario`, `gen2_encrige2020_diseno_muestral`). Entonces 2016 no es la ola más reciente, y la premisa de D1 («programa descontinuado») no se sostiene para ENCRIGE. En el portal, 2022/2023/2024/2025 dan «Página no encontrada» (A.13: examiné 4 URL).
- MIGRACIÓN 2002 (Módulo Sobre Migración) → NO-VERIFICABLE-DESDE-NUBE: la página del programa solo trae el título. Calendario de difusión: NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS (`/app/calendario/` y `/app/calendario/default.html` devuelven «Página no encontrada»). Receta de un minuto: abrir en navegador https://www.inegi.org.mx/app/calendario/ (o Programas de información → Encuestas en hogares → Módulos), buscar «migración», anotar si aparece un módulo sucesor, y consultar el RNM (https://www.inegi.org.mx/rnm/index.php/catalog, buscar «MSM 2002»). No se consultaron ni el RNM ni los comunicados para ninguno de los 4 programas.

## Olas nuevas vistas (E.6: solo se reportan, no se abrieron)
CNGE 2025: solo vi el título de la página por curl. No bajé ni guardé nada de esa ola; sale del alcance de D1 (es otro programa).

## Implicación para mesa
Los resultados no sostienen la opción (a) tal como está escrita («programas descontinuados sin sucesora»): 3 de los 4 tienen sucesora. En CAAS y ENG la sucesora es otro instrumento, así que el razonamiento de «no hay ola futura comparable» puede seguir en pie, pero mesa tiene que decidirlo. En ENCRIGE, 2016 ya no es la ola más reciente (lo es 2020), por lo que la regla E.6 no la alcanza en su letra: es un caso de reserva mal aplicada, no de descontinuación.

## NO-CORRIDO / RESERVAS
- No revisé la ficha RNM ni los comunicados (DIFERIDO-A: una sesión con navegador; ver la receta de arriba).
- No abrí ni leí contenido de microdato ni de tabulados reservados. El descriptor CAAS 2020 que bajé pertenece al CPV 2020, que no está reservado en el manifiesto.
