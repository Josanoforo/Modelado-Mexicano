# Instrucción de una página · repetir el respaldo del corpus

Origen: `ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1` (21/sep/2026). Primera corrida: `/home/pc0/mm-respaldo-corpus/2026-09-21/` — **todavía no es un respaldo** (vive en el mismo disco que el corpus; mesa no nombró destino, firma 21/sep: «Sin destino por ahora»). Cuando mesa conecte un disco externo o nombre un remoto, el paso 2 cambia de `--destino`; los otros tres no cambian.

## Cada cuándo

- **Cada vez que `data/manifiesto.yaml` gane entradas con payload** (un `--promueve` o un `--descarga` nuevos), o al menos **una vez al mes**. Falsador a tres meses (§10 del encargo): si el 21/dic/2026 nadie repitió esto, la instrucción no sirve y se anota.
- Nunca mientras el agente de adquisición esté descargando (candado de `/adquiere`): un índice a medio escribir no coincide con el archivo terminado.

## Qué comandos — desde el worktree del acto que lo repite, FUERA del sandbox

```bash
R=forense/analisis/corpus-integridad-1/respaldo_corpus.py
DEST=/home/pc0/mm-respaldo-corpus/$(date +%F)     # o /mnt/<disco-externo>/mm-respaldo-corpus/$(date +%F)

# 1 · índice desde los ARCHIVOS (no desde el manifiesto): indice.tsv + SHA256SUMS
python3 $R --destino "$DEST" --indexa            # ~40 s por 19.8 GB en caché

# 2 · copia (rsync -rt --safe-links --no-links; omite el symlink en bucle raw/raw y .manifiesto.lock)
python3 $R --destino "$DEST" --copia             # ~3 min disco→disco

# 3 · verificación por hash EN DESTINO (rehashea todo)
python3 $R --destino "$DEST" --verifica          # VERDE o ROJO con la lista de NO-COINCIDE/FALTA
( cd "$DEST" && sha256sum -c --quiet SHA256SUMS && echo OK )   # verificación independiente del script

# 4 · prueba de restauración: un archivo por subdirectorio + N al azar (o N=1914 = todo)
python3 $R --destino "$DEST" --restaura 20       # copia a $DEST/../restauraciones-tmp y hashea; borra al final
```

Las tres raíces por defecto son las que el censo del 21/sep identificó como el corpus físico entero: `data_raw=/home/pc0/mm-corpus/raw` · `descargas_mx=/mnt/c/Users/PC0/Descargas MX` · `reserva_respondentes=/home/pc0/mm-corpus/reservas-respondentes`. Si aparece una raíz nueva en `data/raices.local.yaml`, se añade con `--raiz NOMBRE=RUTA`.

## Qué se pega en la nota del acto que lo repita

Las cuatro líneas de resumen (`INDICE: archivos=… bytes=…`, los `Total transferred file size` de rsync, `VERIFICA-DESTINO: … -> VERDE`, `RESTAURA-RESUMEN: … -> VERDE`) y, antes de todo, la salida cruda de `python3 tests/manifiesto.py --verifica` (A.1: tres estados sin colapsar) más la del censo por entrada:

```bash
python3 forense/analisis/corpus-integridad-1/censo_integridad.py \
    --salida forense/analisis/corpus-integridad-1/censo-$(date +%F).tsv \
    --busca-tambien reserva_respondentes=/home/pc0/mm-corpus/reservas-respondentes \
    --busca-tambien repo=$PWD
```

## Qué NO hace

No borra, mueve ni renombra nada del corpus (PARO b del encargo). No edita el manifiesto. No sube a ningún destino que mesa no haya nombrado (PARO d). No está automatizado a propósito (D-14): primero se ve si se repite a mano.

## Restaurar de verdad (si el disco falló)

`rsync -rt "$DEST/data_raw/" /home/pc0/mm-corpus/raw/` (y lo mismo para las otras dos raíces), luego `python3 tests/manifiesto.py --verifica` desde un worktree con `data/raw` enlazado y `data/raices.local.yaml` presente: 1 627 `COINCIDE` es el criterio de «restaurado».
