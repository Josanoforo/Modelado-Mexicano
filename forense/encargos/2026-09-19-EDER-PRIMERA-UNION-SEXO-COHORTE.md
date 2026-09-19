# Encargo 3 · EDER 2017: primera unión por sexo y cohorte

Archivo fuente íntegro: `/mnt/c/Users/PC0/Descargas MX/03-EDER-PRIMERA-UNION-SEXO-COHORTE.md`.

Rama autorizada: `codex/gen2-eder2017-primera-union-sexo-cohorte-cli-1`.
CALC propuesto: `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001`.

La pregunta es cómo cambia la composición de primera unión por sexo dentro de
cohortes y cuánto cambia la diferencia mujer−hombre al usar una composición
común de cohortes. Reutiliza el padre `CALC-EDER-0003`; no mide ENADID ni
situación conyugal actual. El encargo original exige auditoría de enlaces,
partición libre/directo/sin clasificar, ocho perfiles sexo×cohorte, cuatro
contrastes, diferencia cruda comparable y estandarizada, bootstrap de UPM en
estrato (2,000 réplicas PCG64), control independiente, artefactos procesables,
lectura y replay. Prohíbe tocar motor, milpa, gobierno, CRON, piloto 3,
PR889, tests/check.py, baseline y workflows.

La fuente autorizada es `eder_2017_eder2017_bases_csv`, SHA-256
`bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`, con FD
`eder_2017_eder2017_fd`. Antes de abrir respuestas debe resolverse sexo por
FD; la resolución congelada abajo es `persona.csv: sexo`, llave
`(folioviv, foliohog, id_pobla)`, códigos `1=Hombre`, `2=Mujer`.

Este archivo conserva el encargo recibido; sus restricciones y detalles
operativos prevalecen sobre este resumen.
