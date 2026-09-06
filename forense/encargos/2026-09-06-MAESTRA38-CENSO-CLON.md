ENCARGO · ACTO MAESTRA38-CENSO-CLON · UN-CLON-UN-OBJETO — nube, Sonnet, invoca /acto

SHA ef9ba36 · COMPUERTA: #556 fusionado (para que el test de abajo tenga el censo real como caso) · sin red, sin corpus (el caso de prueba se construye con un tmpdir que contiene .git/). Regla (COMMIT-1, congelada): en tests/manifiesto.py --escanea, una carpeta que contiene .git/ es un objeto: se reporta una sola línea CLON <ruta> · commit <sha de HEAD leído de .git> · <n> archivos en una sección nueva CLONES (k):, y ninguno de sus archivos entra a «nuevos» ni a «páginas guardadas». Los archivos dentro del clon que ya estén en manifiesto.yaml siguen contando en «ya registrados» (se listan bajo el clon). El staging no recibe entradas por los archivos del clon. La heurística de url_origen no se aplica a HTML (.html/.htm): esos archivos no sugieren nada. COMMIT-2: el cambio + test en tests/ (tmpdir con .git/HEAD, un archivo registrado y dos no: esperado 1 línea CLON, 0 nuevos, 1 ya registrado) + re-corrida de --escanea sobre el árbol de prueba pegada · data/INFRAESTRUCTURA-v1_0.md: fila de censo-raiz gana la frase «un clon git = un objeto» · hallazgos.md, dos líneas: (i) 136 residuos del clon de L2-LISTA contados como nuevos el 6/sep; (ii) heurística de token dominante mordiendo HTML (jquery). check.py --baseline VERDE. PERÍMETRO: tests/manifiesto.py · test nuevo · INFRAESTRUCTURA · hallazgos · notas · tablero (recibo) · A.3 · cascada. NO toca: manifiesto · staging · cola · corpus. Si te encuentras escribiendo fuera de esta lista, PARA. CONTADOR: falsos «nuevos» por clon 136 → 0 en el siguiente censo · medición: cero.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-CENSO-CLON · UN-CLON-UN-OBJETO`, rama
`claude/censo-clon-git-objeto-e0pjr7`, `ADR-355` (renumerado dos veces al
re-sincronizar con `origin/main`: `352`→`354` cuando fusionaron primero
`ADR-352`/`ADR-353` de `MAESTRA38-CRON`/`MAESTRA38-A6`, y `354`→`355`
cuando fusionó primero `ADR-354` de `MAESTRA38-CRON-3` — regla de la casa,
renumera quien fusiona segundo).
[PR #559](https://github.com/Josanoforo/Modelado-Mexicano/pull/559)
(sin fusionar — el merge es de mesa).
