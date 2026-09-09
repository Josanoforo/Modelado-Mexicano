# ACTO GEN2-TRAMITE-BANDEJA · nota del acto

Encargo archivado verbatim: `forense/encargos/2026-09-08-GEN2-TRAMITE-BANDEJA.md`.

## §0 · Qué hace esta nota

Propaga cuatro decisiones de mesa del 8/sep/2026 sobre tres piezas de registro (P1-P3) y deriva, por primera vez como artefacto y no como conversación, la bandeja completa de lo que sigue pendiente de un humano en la cola de adquisición (P4). No decide nada nuevo: cada pieza cita la firma verbatim que la autoriza.

## §1 · P1 · Fila `D-14` → `DECLINADA-POR-PROCESO`

Firma de mesa verbatim, 8/sep/2026: «pues sobre todo son encargos que vienen de chatgpt, mejor lo que haré es pasarlos por ti antes de mandarlos yo directamente, es que luego te tengo trabajando en otras cosas, pero eso se corrige yo dejándolo de hacer.»

`D-14` candidateaba un `WARN` mecánico en la suite para cuando un merge tocara `.claude/commands/`, una cola de adquisición o `canon/` sin encargo archivado en el mismo diff — el defecto que `PR #632` y `PR #635` ya habían demostrado el mismo día. Mesa no lo rechaza por desacuerdo con el diagnóstico: elige un remedio distinto, de proceso — todo encargo que llegue redactado fuera del repo (ChatGPT u otro origen externo) pasa por dirección antes de lanzarse — en vez de instrumentar el `WARN`. Es la misma jerarquía de `AGENTS.md` (`La instrucción explícita más reciente de la mesa... puede apartarse de una regla anterior») aplicada a un candidato de gobernanza que nunca llegó a implementarse.

La fila no se cierra ni se borra: `#632`/`#635` quedan como su serie histórica (dos casos del mismo linaje, el mismo día), y queda escrita la condición de reapertura — si un acto vuelve a fusionar sin fichar pese al proceso ya adoptado, la fila revive con el caso nuevo y el `WARN` se reconsidera desde cero, no desde donde se dejó.

`forense/firmas-pendientes.tsv`: `D-14` `ABIERTA` → `DECLINADA-POR-PROCESO`, `firmada_en` = la firma verbatim de arriba, `ejecutada_en` = este acto (`ACTO GEN2-TRAMITE-BANDEJA`, `ADR-420`).

## §2 · P2 · `NC-0057` → `CERRADA-DECLINADA`

Firma de mesa verbatim: «ahorita no agregan valor.» — sobre la vía CIDE/Colmex/UNAM para un microdato mexicano de tandas/ROSCA con reputación (`NC-0057`, abierta por `ACTO GEN2-UNIVERSO-C`, 8/sep/2026).

Respuesta técnica de dirección para el registro, para que el cierre no lea solo como una opinión sino como una razón medida: la búsqueda dirigida por autor/paper concreto en esos tres repositorios institucionales **es** semi-automatizable (consultas parametrizadas por autor a los repositorios y a Google Scholar) — el costo no es técnico. Lo que no compensa las horas es la razón señal/ruido sin una pista previa: la sesión que abrió `NC-0057` ya corrió 4 consultas generales y no rindió un dataset específico, solo referencias institucionales sin depósito confirmado (`SIN-FETCH`). Insistir sin un autor o paper nombrado repite el mismo resultado. `SONDA-3` (`.claude/commands/sonda.md`, `S5-bis`/`S8`, `ACTO GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`) queda como vía de piloto futuro si una pista concreta aparece — el mismo criterio que su propio piloto gateado (`forense/encargos/cola/2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md`) ya declara para `RUPC`.

`forense/no-corrido.tsv`: `NC-0057` `ABIERTA` → `CERRADA-DECLINADA`, `cerrado_por` = `ACTO GEN2-TRAMITE-BANDEJA (ADR-420)`, `fecha_cierre` = 2026-09-08. El texto original de la fila (razón, impacto) no se borra — la glosa de cierre se añade con `||`, mismo patrón que `OECD`/`RUPC` en la cola. Reabre únicamente con un autor o paper concreto citado, nunca con curiosidad sola.

## §3 · P3 · El timbre de las tanderas → `SOLICITUD-PREPARADA`

Firma de mesa verbatim: «Ok, hay 2 elementos así, de timbres, pero hay descargas manuales que efectivamente yo tengo que correr, pero otras que con los arreglos de la sonda se obtienen.» El primer timbre ya se ejecutó (`OECD` Trust Survey PUM, `ACTO GEN2-CIERRES-GRUPO-A`, 8/sep/2026); este acto ejecuta el segundo.

Fila objetivo: `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` (`data/curacion-registro/cola-adquisicion-registro.tsv`) — es la fila cuya nota ya citaba, desde el 4/sep, el contacto exacto de convenio: `equipo@tandamas.mx` (Tanda+). Su fila hermana `REGISTRO_DE_TANDAS_Y_REPUTACION` (tanda.mx/tandamas.mx) comparte dominio de contacto pero no tiene un correo confirmado propio — queda con una nota cruzada, sin cambiar de estado, hasta que una respuesta real la reclasifique.

Receta de envío para mesa (el agente no envía correos), mismo patrón que `OECD`:

> Destinatario: `equipo@tandamas.mx`
>
> Texto sugerido (español, ≤10 líneas): «Estimado equipo de TandaMás: somos un equipo de modelado del comportamiento financiero de los hogares en México, con datos públicos y agregados. Nos interesa saber si cuentan con estadísticas agregadas y anonimizadas de incumplimiento o reputación dentro de sus tandas digitales (por ejemplo, tasa de atraso o de expulsión por cohorte, sin identificar personas), y bajo qué términos y en qué formato podrían compartirlas. No buscamos comprometer ningún convenio existente: solo queremos entender el alcance antes de solicitar formalmente. Quedamos atentos y agradecemos su tiempo. Saludos, [nombre de mesa].»

`data/curacion-registro/cola-adquisicion-registro.tsv` / `data/cola-adquisicion-v1_0.tsv` (vista regenerada por `tools/vista_cola_adquisicion.py`): `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` `NO-ADQUIRIDA-POR-COSTO` → `SOLICITUD-PREPARADA`, con fecha 8/sep/2026. El envío físico queda `DECISIÓN-DE-MESA-PENDIENTE` (`NC-0061`, ver `## NO-CORRIDO / RESERVAS` del encargo).

## §4 · P4 · La bandeja de mesa, derivada

Comando base sobre la cola vigente: `awk -F'\t' 'NR==1{next}{print $2}' data/cola-adquisicion-v1_0.tsv | sort | uniq -c` (138 filas, 8/sep/2026) → 107 `OBTENIDO` + 8 `OBTENIDO-PARCIAL` + un resto de filas cerradas (`CERRADA*`, `SUPERADA-POR`, `NO-ENCONTRADO` sin candidata viva) que no piden nada de nadie. El universo de partida de esta bandeja son las filas que sí piden algo: cruzadas contra `forense/notas/2026-09-06-MAESTRA38-A6-PAQUETE-RECETAS-11.md` (las 5 recetas de navegador vigentes, cada una declarada ejecutable «por una persona o por Claude in Chrome en ≤ 1 minuto») y contra `forense/encargos/cola/2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md` (que nombra `RUPC` y `DD_COMPRANET_DICCIONARIOS_DE_DATOS` como objeto/demostración del piloto).

Criterio de corte: una receta de navegador va a **(a)** salvo que la fila ya esté nombrada como objeto de un piloto de `SONDA-3` o su barrera sea explícitamente un bloqueo de agente/red ya confirmado (no una sesión que cualquier navegador —de mesa o de un futuro `Claude in Chrome`— resolvería igual de rápido). Dos filas quedan fuera de ambas columnas porque no piden acción, aunque su token siga abierto: `MERCER_GPTW_CLIMA_DESEMPENO` (`NO-ADQUIRIDA-POR-COSTO`, pero con veredicto D ya firmado — `ADR-196`/`ADR-199` — mesa ya decidió no perseguirla) y `PI` (`DIFERIDO-A` la spec GEN2 de `dinero.credito.scoring_alternativo`, sin acción hoy — hereda el export cuando esa spec se escriba).

### (a) SOLO-MESA — exige manos o identidad de mesa

| Fila / objeto | Qué es | Minutos de mesa |
|---|---|---|
| `OECD` — Trust Survey PUM | Enviar el correo ya redactado a `govtrustinfo@oecd.org` con el formulario adjunto (`ACTO GEN2-CIERRES-GRUPO-A`) | ~2 min |
| `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` — Tanda+ | Enviar el correo de §3 a `equipo@tandamas.mx` | ~2 min |
| Global Findex 2025, microdato individual (`NC-0056`) | Abrir cuenta gratuita en `microdata.worldbank.org` y bajar el microdato | ~15 min (registro + verificación) |
| `ENAFIN`, microdato de empresa individual (`NC-0056`) | Trámite presencial, Laboratorio de Microdatos INEGI (servidor público/investigador calificado) | No es tarea de minutos — trámite formal presencial, días-semanas; el tabulado ya `OBTENIDO` satisface `N19` por segmento, así que esto no bloquea nada hoy |
| `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | Receta de navegador, postback ASP.NET sin enlace estático (`PAQUETE-RECETAS-11` §3) | ≤1 min |
| `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` | Receta de navegador, URL real solo la inyecta el JS del programa (`PAQUETE-RECETAS-11` §4) | ≤1 min |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` (Bauchet, SSRN 2474620) | Receta manual `cenfri.org` en navegador, A.5, objeto exacto detrás de Cloudflare/login SSRN por 5 rutas de agente agotadas | ≤1 min |

Total de escritorio (excluyendo el trámite presencial de ENAFIN): ~22 minutos repartidos en 6 tareas — 2 correos, 1 cuenta, 3 descargas de navegador.

### (b) RE-INTENTO-VÍA-SONDA — espera al piloto, no le cuesta un minuto a mesa

| Fila / objeto | Barrera | Pista para `SONDA-3` |
|---|---|---|
| `RUPC`, objeto vivo (el histórico 2019 vía `datamx.io` ya está `OBTENIDO-PARCIAL`) | `EXIGE-SESION-NAVEGADOR`; sonda lateral (`ACTO GEN2-SONDA-2`) ya confirmó la red de esta sesión NUBE bloqueada hacia `buengobierno.gob.mx` | Repo `humandesignlab/veta` documenta 3 rutas CompraNet vivas hoy (`Contratos_CompraNet{2023,2024,2025}.csv`, `Expedientes_PICompraNet2025.csv`, 72-188MB c/u, `200 OK` verificado) y el esquema de firma RSA que la API `Whitney` exige (`adele/interoperabilidad/tp/reloj`) — explícitamente no implementado por exceder el alcance del acto que lo encontró («bypass de anti-bot, fuera de alcance»). Ya es el objeto de demostración nombrado en `forense/encargos/cola/2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md` |
| `DD_COMPRANET_DICCIONARIOS_DE_DATOS` | `EXIGE-SESION-NAVEGADOR` (SPA Angular sin enlace estático; el bundle de 2 647 141 B no trae ninguna cadena `DD_`) | Mismo dominio/familia que `RUPC` (`comprasmx.buengobierno.gob.mx`); el gap es de renderizado JS, no de sesión con credencial — inspección de red / render headless podría hallar el endpoint real que el Angular llama, sin identidad de mesa. Nombrada junto con `RUPC` en el mismo encargo piloto |
| `ROSCA_ACADEMICO_MEXICO_BUSQUEDA` (tandas/ROSCA con reputación, `NC-0057` recién cerrada arriba) | `SIN-FETCH`: candidatas institucionales sin dataset confirmado en `repositorio-digital.cide.edu` / `repositorio.colmex.mx` | `SONDA-3` `S5-bis` (segunda pasada crítica, sin cuota universal) ataca exactamente esto — búsqueda dirigida por autor/paper si mesa o una sesión futura nombra uno; hasta entonces, no repetir la misma consulta general |

Una línea para `forense/hallazgos.md`: la bandeja de mesa deja de ser folclore de conversación; vive derivada.
