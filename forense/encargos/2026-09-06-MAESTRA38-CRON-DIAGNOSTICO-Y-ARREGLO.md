ENCARGO · ACTO MAESTRA38-CRON · DIAGNOSTICO-Y-ARREGLO — caja mm-adq, Sonnet, invoca /acto

SHA a5350e59→ef9ba36 · COMPUERTA: ninguna · ENTORNO: la caja donde vive el cron (/home/pc0/mm-adq), no un worktree nuevo · MODELO: Sonnet (Opus si el arreglo exige juicio sobre git). Hechos del repo (A.10): [CENSO] 2026-09-04 commit a60c661 23:39, mensaje del rename «(cron 23:39)» → el cron disparó a las 23:39 del 4/sep. Línea sugerida en el runbook: 30 7 * * 1-5 cd <clon> && ./tools/adquiere_cron.sh >> forense/adq-log/cron-stdout.log 2>&1 (forense/agente-adquisicion-v1_0.md:174). El script escribe un archivo nuevo por día → siempre commit, siempre rama censo/<fecha> + PR. No existe censo/2026-09-05 (git ls-remote --heads origin | grep censo → 0; commits examinados: 333). El log está gitignorado (.gitignore:33): sólo la caja lo tiene. P0 · Lectura, pega salida cruda de los cinco:

crontab -l
ls -la forense/adq-log/ forense/censo-raiz/
tail -40 forense/adq-log/2026-09-05.log 2>/dev/null; tail -20 forense/adq-log/cron-stdout.log 2>/dev/null
git branch --show-current; git status --short | head
systemctl is-active cron; grep CRON /var/log/syslog 2>/dev/null | grep -i adquiere | tail -5

Lecturas pre-declaradas (una manda, se dice cuál):

(a) crontab -l sin la línea, o con hora ≠ 30 7 → el disparo de las 23:39 fue una línea de prueba: se instala la línea del runbook (zona horaria verificada con date; si la caja está en UTC, 30 13).
(b) Línea correcta y log del 5/sep con git checkout main/git pull fallando, o PARO: data/raw ausente → el defecto es del script: la corrida anterior deja el clon en censo/<fecha> con data/manifiesto-staging.yaml modificado. Arreglo (COMMIT): al arrancar, git checkout -- data/manifiesto-staging.yaml && git checkout -f main && git pull --ff-only; al terminar, volver a main. Se añade una línea de log con git branch --show-current al inicio y al final.
(c) Línea correcta, servicio activo, sin log del 5/sep → el cron no ejecutó: ruta del clon o PATH (cron no carga ~/.bashrc; gh, python3, claude pueden no resolverse). Arreglo: rutas absolutas en la línea de crontab y PATH= explícito en la primera línea del crontab.
(d) Log del 5/sep con [CENSO] commiteado y empujado pero sin PR → gh pr create falló (auth). Se lee el log; se autentica gh o se deja la URL de compare, que ya está prevista. P1 · Prueba de extremo a extremo hoy (domingo, sin esperar al lunes): ./tools/adquiere_cron.sh a mano desde mm-adq; éxito = rama censo/2026-09-06 + PR abierto, con Total en disco en el mensaje. Si mesa ya depositó MEX_2016_APIPIE_v01_M_Stata.zip, ese censo lo debe traer como «nuevos: 1» — es el control positivo. P2 · Verificación del programador: queda declarada, no cerrada: la prueba real es censo/2026-09-07 a las 07:30 del lunes. El ADR lo dice con esas palabras. PERÍMETRO: tools/adquiere_cron.sh (sólo si (b)/(c)) · forense/agente-adquisicion-v1_0.md (línea de crontab real, con zona horaria) · forense/notas/2026-09-06-MAESTRA38-CRON-diagnostico.md · hallazgos · tablero (recibo) · A.3 · cascada. NO toca: nada más. Si te encuentras escribiendo fuera de esta lista, PARA. CONTADOR: censos diarios producidos por el programador 1 → declara · medición: cero.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-CRON · DIAGNOSTICO-Y-ARREGLO`, 6/sep/2026. Ninguna de las cuatro
lecturas pre-declaradas se cumplió; `censo/2026-09-05` estaba ausente porque el 5 de septiembre
de 2026 fue sábado, fuera de la ventana `1-5` de la propia línea de crontab — no un defecto.
`crontab -l` ya trae la línea correcta y `tools/adquiere_cron.sh` no se tocó. Prueba de extremo a
extremo hoy con éxito completo: `censo/2026-09-06` + PR. Detalle en
`forense/notas/2026-09-06-MAESTRA38-CRON-diagnostico.md`, `canon/gobernanza-v1_15.md` `ADR-352`,
`forense/firmas-pendientes.tsv` `FP-323` (verificación real pendiente: `censo/2026-09-07`, lunes).
PR: (se registra al abrir, ver git log de la rama `acto/maestra38-cron-diagnostico`).
