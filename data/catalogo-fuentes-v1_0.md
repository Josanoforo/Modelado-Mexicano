# Catálogo unificado de fuentes de datos — v1.0

**Este archivo es derivado. No se edita a mano.** Se regenera con:

```
python3 tests/catalogo.py && python3 tests/dedup.py
```

Insumo: los 10 inventarios ciegos de `data/inventarios/`, compilados el 30/jul/2026.

**Verificación de receta.** `catalogo.py` imprime, antes de cualquier cifra, la comparación entre lo que parsea y el conteo crudo de encabezados numerados de cada archivo. Los tres formatos que conviven ahí (`## N.`+tabla, `### N.`+tabla, `### N.`+viñetas) rompieron la primera versión del parser **en silencio**: se comió 3 archivos enteros y habría reportado 91 fuentes en vez de 119. Si esa verificación imprime `INCONSISTENTE`, las cifras de abajo no valen.

**Nota de lectura:** `catalogo.py` imprime conteos intermedios **sin deduplicar**. Las cifras de este archivo salen de `dedup.py`, que agrupa por acrónimo *y* nombre normalizado — sin eso `CPV`, `Censo de Población y Vivienda` y `ENNVIH / MXFLS` cuentan como fuentes distintas.


## Cifras derivadas

| Magnitud | Valor |
|---|---|
| Inventarios leídos | 10 |
| Entradas de fuente (con repetición entre dominios) | 183 |
| **Fuentes únicas** | **119** |
| Con microdatos declarados | 52 |
| Sin microdatos (solo agregados) | 32 |
| Microdatos indeterminado — hueco de VERIFICACIÓN, no de dato | 35 |
| **Operables** (microdato + acceso libre/sin registro) | **38** |
| Operables ya en `data/manifiesto.yaml` | 6 |
| **Operables NO bajadas todavía** | **32** |
| Transversales (3+ dominios) | 16 |
| Mono-dominio | 88 |

> El conteo que circulaba en conversación era **~61 fuentes**, marcado en su momento como no auditable. El valor derivado es **119**.


## Espina dorsal — 3 o más dominios

| Acrónimo | Dominios | micro | libre | disco | Nombre |
|---|---|---|---|---|---|
| **CPV** | 8 · CAP CUL MIG SAL TEC TRA EST TIE | sí | sí | — | Censo de Población y Vivienda (CPV) — antes Censo General de Población |
| **ENIGH** | 6 · FIN MIG SAL TEC TRA TIE | sí | sí | SI | Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) |
| **ENASEM** | 5 · FIN MIG SAL TRA TIE | sí | sí | — | Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM) / Me |
| **ENCIG** | 5 · CAP CUL SEG TEC EST | sí | sí | SI | Encuesta Nacional de Calidad e Impacto Gubernamental (ENCIG) |
| **ENCUCI** | 4 · CAP CUL SEG EST | sí | sí | SI | Encuesta Nacional de Cultura Cívica (ENCUCI) |
| **ENNVIH** | 4 · FIN MIG SAL TRA | sí | sí | SI | Encuesta Nacional sobre Niveles de Vida de los Hogares (ENNViH) / Mexi |
| **ENSANUT** | 4 · CUL SAL EST TIE | sí | sí | — | Encuesta Nacional de Salud y Nutrición — componentes de creencias y co |
| **ENVIPE** | 4 · CAP CUL SEG EST | sí | sí | SI | Encuesta Nacional de Victimización y Percepción sobre Seguridad Públic |
| **ENADID** | 3 · MIG SAL TIE | sí | sí | — | Encuesta Nacional de la Dinámica Demográfica (ENADID) |
| **ENDIREH** | 3 · SEG EST TIE | sí | sí | — | Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares ( |
| **ENIF** | 3 · FIN MIG TEC | sí | sí | SI | Encuesta Nacional de Inclusión Financiera (ENIF) |
| **ENOE** | 3 · MIG TRA TIE | sí | sí | — | Encuesta Nacional de Ocupación y Empleo (ENOE) / ENOE Nueva Edición (E |
| **ENSU** | 3 · CAP SEG EST | sí | sí | — | Encuesta Nacional de Seguridad Pública Urbana (ENSU) |
| **ENUT** | 3 · CAP TRA TIE | sí | sí | — | Encuesta Nacional sobre Uso del Tiempo (ENUT) |
| **LAPOP** | 3 · CUL MIG EST | sí | ? | — | Barómetro de las Américas / AmericasBarometer (LAPOP) |
| **LATINOBARÓMETRO** | 3 · CAP CUL EST | sí | ? | — | Latinobarómetro — muestra de México |

## Operables no bajadas

| Acrónimo | Dom. | Nombre |
|---|---|---|
| CPV | 8 | Censo de Población y Vivienda (CPV) — antes Censo General de Población y Vivie |
| ENASEM | 5 | Encuesta Nacional sobre Salud y Envejecimiento en México (ENASEM) / Mexican He |
| ENSANUT | 4 | Encuesta Nacional de Salud y Nutrición — componentes de creencias y confianza |
| ENADID | 3 | Encuesta Nacional de la Dinámica Demográfica (ENADID) |
| ENDIREH | 3 | Encuesta Nacional sobre la Dinámica de las Relaciones en los Hogares (ENDIREH) |
| ENOE | 3 | Encuesta Nacional de Ocupación y Empleo (ENOE) / ENOE Nueva Edición (ENOEN) |
| ENSU | 3 | Encuesta Nacional de Seguridad Pública Urbana (ENSU) |
| ENUT | 3 | Encuesta Nacional sobre Uso del Tiempo (ENUT) |
| EDER | 2 | Encuesta Demográfica Retrospectiva (EDER) |
| EDR | 2 | Estadísticas de Defunciones Registradas (EDR) — subconjunto de defunciones por |
| ELCOS | 2 | Encuesta Laboral y de Corresponsabilidad Social (ELCOS) **[parcialmente verifi |
| ENAPROCE | 2 | Encuesta Nacional sobre Productividad y Competitividad de las Micro, Pequeñas  |
| ENCUP | 2 | Encuesta Nacional sobre Cultura Política y Prácticas Ciudadanas (ENCUP) |
| ENDUTIH | 2 | Encuesta Nacional sobre Disponibilidad y Uso de Tecnologías de la Información  |
| ENPOL | 2 | Encuesta Nacional de Población Privada de la Libertad (ENPOL) |
| ENTI | 2 | Encuesta Nacional de Trabajo Infantil (ENTI) |
| MOCIBA | 2 | Módulo sobre Ciberacoso (MOCIBA) |
| ACS | 1 | American Community Survey (ACS) y Puerto Rico Community Survey (PRCS) |
| CNGF | 1 | Censo Nacional de Gobierno Federal (CNGF) y censos nacionales de gobierno en e |
| CNGMD | 1 | Censo Nacional de Gobiernos Municipales y Demarcaciones Territoriales de la Ci |
| CPS | 1 | Current Population Survey (CPS) y Annual Social and Economic Supplement |
| ECOVID-ML | 1 | Encuesta Telefónica sobre COVID-19 y Mercado Laboral (ECOVID-ML) |
| EIC | 1 | Encuesta Intercensal (EIC) 2015 |
| ENCUESTA NACIONAL DE BIENESTAR | 1 | Encuesta Nacional de Bienestar Autorreportado |
| ENCUESTA NACIONAL PARA EL SIST | 1 | Encuesta Nacional para el Sistema de Cuidados |
| ENFIH | 1 | Encuesta Nacional sobre las Finanzas de los Hogares (ENFIH) |
| ENSAFI | 1 | Encuesta Nacional sobre Salud Financiera (ENSAFI) |
| ESTADÍSTICA EDUCATIVA | 1 | Estadística educativa — Formato 911 / SIGED |
| ESTADÍSTICAS DE NATALIDAD / NA | 1 | Estadísticas de Natalidad / Nacimientos registrados |
| GLOBAL FINDEX DATABASE | 1 | Global Findex Database (México como país incluido) |
| REGISTROS ADMINISTRATIVOS DE E | 1 | Registros administrativos de estadísticas vitales y nupcialidad |
| SAEH | 1 | Subsistema Automatizado de Egresos Hospitalarios (SAEH) |

## Las 35 indeterminadas

El campo `Microdatos` del inventario no permite decidir sí/no. **No son fuentes sin microdato: son fuentes sin verificar.** Resolverlas es consulta de página, no descarga, y el conteo de operables solo puede subir.

| Acrónimo | Dom. | Nombre |
|---|---|---|
| CENSOS NACIONALES DE GOBIERNO | 2 | Censos Nacionales de Gobierno (CNGF, CNGE, CNGMD) y Censo Nacional de Transpar |
| CNARTYS | 1 | Catálogo Nacional de Regulaciones, Trámites y Servicios (CNARTyS) |
| DTM | 1 | Matriz de Seguimiento del Desplazamiento (DTM), México |
| ENAFIN | 1 | Encuesta Nacional de Financiamiento de las Empresas (ENAFIN) |
| ENAID | 1 | Encuesta Nacional de Acceso a la Información Pública y Protección de Datos Per |
| ENCOAP | 1 | Encuesta Nacional de Confianza en la Administración Pública (ENCOAP) |
| ENCODAT | 1 | Encuesta Nacional de Consumo de Drogas, Alcohol y Tabaco (ENCODAT) y la serie  |
| ENCODE | 1 | Encuesta Nacional de Consumo de Drogas en Estudiantes (ENCODE) |
| ENCRIGE | 1 | Encuesta Nacional de Calidad Regulatoria e Impacto Gubernamental en Empresas ( |
| ENCUESTA NACIONAL DE NIÑOS, NI | 1 | Encuesta Nacional de Niños, Niñas y Mujeres (ENIM / MICS México) |
| ENCUESTA NACIONAL DE OPINIÓN C | 1 | Encuesta Nacional de Opinión Católica |
| ENCUESTA NACIONAL DE RELIGIÓN, | 1 | Encuesta Nacional de Religión, Secularización y Laicidad |
| ENCUESTA NACIONAL SOBRE CREENC | 1 | Encuesta Nacional sobre Creencias y Prácticas Religiosas en México |
| ENCUESTAS ECONÓMICAS NACIONALE | 1 | Encuestas Económicas Nacionales mensuales y anuales (EMIM, EMEC, EMS, ENEC, EM |
| ENE | 1 | Encuesta Nacional de Empleo (ENE) y Encuesta Nacional de Empleo Urbano (ENEU)  |
| ENESTYC | 1 | Encuesta Nacional de Empleo, Salarios, Tecnología y Capacitación en el Sector  |
| ENVI | 1 | Encuesta Nacional de Vivienda (ENVI) |
| ESTADÍSTICAS Y REGISTROS DEL S | 1 | Estadísticas y registros del sector cultural |
| ETOE | 1 | Encuesta Telefónica de Ocupación y Empleo (ETOE) |
| GATS | 1 | Encuesta Global de Tabaquismo en Adultos (GATS) |
| IEDMX | 1 | Índice de Estado de Derecho en México (IEDMX) e Índice Global de Estado de Der |
| INCBG | 1 | Índice Nacional de Corrupción y Buen Gobierno (INCBG) — serie descontinuada |
| MGA | 1 | Métrica de Gobierno Abierto (MGA) |
| MÓDULOS Y ENCUESTAS COMPLEMENT | 1 | Módulos y encuestas complementarias del INEGI con contenido parcial del domini |
| OTROS SUBSISTEMAS DE LA DGIS | 1 | Otros subsistemas de la DGIS (cubos dinámicos y datos abiertos) |
| REDECO | 1 | REDECO, REUNE y Buró de Entidades Financieras |
| REGISTRO ADMINISTRATIVO DE ASO | 1 | Registro administrativo de asociaciones religiosas |
| REGISTROS ADMINISTRATIVOS DE S | 1 | Registros administrativos de servicios de cuidado infantil y asistencia social |
| RESULTADOS Y ESTADÍSTICA ELECT | 1 | Resultados y estadística electoral |
| RFOSC / CLUNI | 1 | Registro Federal de las Organizaciones de la Sociedad Civil (RFOSC / CLUNI) |
| RNPDNO | 1 | Registro Nacional de Personas Desaparecidas y No Localizadas (RNPDNO) |
| SERIES DERIVADAS Y COMPILACION | 1 | Series derivadas y compilaciones de terceros |
| SISAI 20 | 1 | Plataforma Nacional de Transparencia — Sistema de Solicitudes de Acceso a la I |
| SISTEMA NACIONAL DE VIGILANCIA | 1 | Sistema Nacional de Vigilancia Epidemiológica — Anuarios de Morbilidad |
| SISVEA | 1 | Sistema de Vigilancia Epidemiológica de las Adicciones (SISVEA) |
