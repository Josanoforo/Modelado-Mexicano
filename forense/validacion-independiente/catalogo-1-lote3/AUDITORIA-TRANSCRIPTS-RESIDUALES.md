# Auditoría de los cuatro transcripts · C1-SUCESORES-Y-LOTE-3 · antes de revelar

Comando: `audita_residuales.py` (regla de C1-LOTE-3, con los campos de `allowlist.json`). Salida cruda en `<paq>/reconstructora/<abrev>--auditoria.json`.

| Paquete | CERO-LECTURAS-FUERA (bruto) | SIN-RED (bruto) | CAMPOS-DENTRO | SOLO-OPUS | Adjudicación de la receptora |
|---|---|---|---|---|---|
| enbiare | NO (2 aciertos) | SÍ | SÍ | SÍ | Los 2 aciertos son `/g` de `sed 's/…/g'` sobre su `$TMPDIR` privado: falso positivo del patrón. **Ciega.** |
| encodat | NO (2) | SÍ | SÍ | SÍ | `/list` es texto dentro de un `sed`; `/tmp/claude-1000/-home-pc0-c1-sucesores-rec-encodat…/tasks/…output` es la salida de una tarea de la propia sesión, dentro de su tmpfs privado (namespace con `/tmp` vacío, sonda). Falsos positivos. **Ciega.** |
| encuci | SÍ | SÍ | SÍ | SÍ | **Ciega.** |
| enigh | SÍ | NO (1) | SÍ | SÍ | El acierto es `cd ..; git log` en su directorio de trabajo: `fatal: not a git repository` (el directorio está fuera de todo repo y `/home/pc0` enmascarado). Es un intento de leer historial fuera del paquete, sin contenido obtenido y sin red. Se declara; **ceguera conservada** porque no se leyó nada fuera del paquete. |

Ninguna sesión leyó microdato fuera de los campos autorizados (tokens de reactivo no autorizados: 0 en las cuatro). Rótulo: CIEGA-POR-CONTEXTO-NUEVO (no broker; el proceso `claude` tuvo red hacia la API).
