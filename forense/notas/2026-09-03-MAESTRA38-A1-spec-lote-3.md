# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — spec Lote 3 (COMMIT-1)

Lote 3 de 3, último: Intercensal 2015 · CSES · Reuters DNR · Pew.
Igual disciplina que Lotes 1-2.

## Identidad pública y ruta de acceso (verificada, no adivinada)

| candidata | nombre oficial | operador | ruta de acceso |
|---|---|---|---|
| Intercensal 2015 | Encuesta Intercensal 2015 | INEGI | **público, sin cuenta** — mismo patrón SPA+RNM que Lotes 1-2, alto tráfico (406k visitas, 23k descargas según su propia página) |
| CSES | Comparative Study of Electoral Systems | consorcio académico (cses.org / espejo GESIS) | **cuenta** — `cses.org/data-download/` exige "Register" antes de listar archivos (verificado: la página no trae ningún enlace `.zip/.dta/.sav` en el HTML servido, sólo el texto "Register") |
| Reuters DNR | Reuters Institute Digital News Report | Reuters Institute, U. of Oxford | **solicitud** — confirmado por fuente pública: "underlying data tables are available to **academic or industry researchers on request**"; sólo gráficas/tablas agregadas son de descarga libre, no microdato |
| Pew | Pew Research Center, Global Attitudes Survey | Pew Research Center | **parcialmente ya OBTENIDO** (topline+shortread, FP-29, manifiesto ya trae `pew_gas2025_social_trust_topline`/`_shortread`) — el **microdato completo** (`pewresearch.org/global/datasets/`) exige cuenta (confirmado: "You need to log in or create a free account to download datasets") |

## Corrección de premisa (declarada en COMMIT-1 de Lote 1, reafirmada aquí)

El encargo trata a Pew como "SIN-FETCH hasta este acto" para las 12; para
Pew específicamente eso es **parcialmente falso**: el topline/shortread ya
fue fetched (FP-29, previo a este acto). Lo que este lote resuelve es lo
que faltaba: el microdato completo, hoy detrás de cuenta.

## La pregunta de cada una

Ninguna de las cuatro tiene cita previa de regla/necesidad en el repo — las
cuatro son exploratorias por cobertura de universo (mismo criterio que
CONEVAL/ENH/ENJUVE en Lote 2), **excepto** que Intercensal 2015, por ser un
censo intermedio de gran escala (variables sociodemográficas estándar:
vivienda, hogar, educación, ocupación, lengua indígena, discapacidad,
migración), es candidata natural para **cualquier regla que necesite
n grande o desagregación geográfica fina** — no se fuerza una regla
específica aquí; se declara la propiedad (n grande, cobertura municipal)
para que un acto sucesor decida.

## Qué cuenta como "trae lo que se pide"

- **Intercensal 2015**: se descarga completo (público); no hay criterio de
  cierre de regla que aplicar — es cobertura.
- **CSES, Reuters DNR, Pew (microdato)**: no se sondea contenido — cuenta o
  solicitud detiene el acceso antes de leer nada. La "pregunta" para estas
  tres es la receta misma (ver abajo), no un criterio A.4.

## Frase de sello

Para Intercensal 2015: el primer resultado que produzca la descarga
directa es el que se registra. Para CSES/Reuters DNR/Pew-microdato: la
receta declarada aquí es la que se archiva para mesa — no se intenta un
rodeo (scraping autenticado, credenciales de terceros, etc.) para evitar
la cuenta o la solicitud.
