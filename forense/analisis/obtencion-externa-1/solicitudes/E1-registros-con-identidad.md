# Registros con identidad · E1 de mesa · sólo se listan

Estado: LISTADO. Son E1 de mesa (§1-P4 del encargo): esta sesión no crea cuentas ni acepta términos. URL comprobadas hoy con `curl -sL -A <UA navegador> -w '%{http_code} %{size_download} %{url_effective}'` (27/sep/2026, caja).

| fuente | objeto que falta | estado en cola hoy | URL de registro / acceso (código hoy) |
|---|---|---|---|
| LAPOP | bases completas México 2018/19 y 2023 (en corpus: cuestionarios y 2004, fila `LAPOP` OBTENIDO en su parte pública) | OBTENIDO (parcial por objeto) | https://www.vanderbilt.edu/lapop/raw-data.php → redirige a **https://www.vanderbilt.edu/cgd/data-access/** (200, 147 365 B) |
| WVS | longitudinal 1981–2022 y olas de comparación (México ola 7 ya en corpus) | `WVS-LONGITUDINAL_1981-2022`, `WVS-EEUU-JAPON_7`: NO-ACCESIBLE | https://www.worldvaluessurvey.org/WVSEVStrend.jsp (200, 24 312 B) · https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp (200, 13 504 B) |
| EMOVI (CEEY) | bases 2011 y 2023 | `EMOVI_2011`, `EMOVI_2023`: NO-ACCESIBLE | https://ceey.org.mx/emovi/ (200, 315 109 B); 2011 también en ICPSR 35333 (https://www.icpsr.umich.edu/web/ICPSR/studies/35333, citado en la cola) |
| Latinobarómetro | olas no bajadas (2023 y 2024 ya OBTENIDO) | `LATINOBARÓMETRO`, `LATINOBAROMETRO_2023`: OBTENIDO | https://www.latinobarometro.org/latContents.jsp (200, 18 274 B) |

Receta de un minuto (común): abrir la URL en navegador normal → «Register / Registrarse» con el correo institucional de mesa → aceptar los términos de uso académico → descargar el archivo de la ola → dejarlo en `Descargas MX` y avisar al sucesor (`GEN2-OBTENCION-EXTERNA-2`) para registrarlo por `/adquiere` con sha y licencia.
