# P3 · Disponibilidad y entrega · preparación no ciega

EJECUTADO: 59 paquetes íntegros / 32772 estimadores del corte original, con identidad SAFE y tolerancia previa preservadas. 11 paquetes / 425 estimadores preparados y materializados; 48 paquetes / 32347 estimadores no preparados, con impedimento y acción en `lanzamientos-lote2.md` y evidencia íntegra en `p3-verificacion.json`. Estos conteos describen preparación, nunca validación.

EJECUTADO: copias independientes sin enlaces en `/home/pc0/astra6-c1-aislado/lote2-P3-final-20260926-r2/`, con recibo de versión real y hashes originales/sucesores/insumos. Las cinco copias v2 provisionales en `/tmp/astra6-c1-lote2-p3-materializacion/` y la materialización intermedia fuera del clon se preservaron; no son el conjunto final para lanzar. La inspección humana retiró historia de productor y detectó métodos parciales antes de cualquier validador.

EJECUTADO: `25` esquemas de entrada distintos probados por el lanzador compartido `--prueba`, todos retorno cero. Esta prueba usa raw vacío y acredita aislamiento de contenedor; `3` esquemas de materialización real también pasaron `--prueba`. `48` materializaciones bloqueadas fueron rechazadas sin escribir. `14` casos dirigidos de transporte/tar/hash/versión/identidad documental/ENIF/symlink comprobados por `p3-pruebas-negativas.py`. No se ejecutaron validadores ni productores; no se abrieron resultados sellados del catálogo ni valores de raw reservado. La inspección documental de preparación sí identificó cifras publicadas en documentos mixtos, que quedaron excluidos de las entradas.

EJECUTADO/LEÍDO: revisión propia por tipo de documento, instrumento y ola, con páginas/campos/rangos de método y hash del paquete en `p3-revision-documentos.json`. ENBIARE2021 y ENFIH2019 se interpretan como olas históricas únicas permitidas por misión, sin serie que reserve una ola posterior; la interpretación queda en cada autorización. ENCODAT2016 fue revisada (2 cuestionarios y 3 catálogos Variables/Valores) y copiada sólo por hash; no se leyeron registros. ENSANUT2024 conserva reserva reserva de última ola de sus cuatro tablas; propuesta no adoptada en `p3-propuesta-ensanut2024.md`. ENOE v3 retiró el encargo administrativo ausente. ENDIREH2021 queda bloqueada por ser última ola de una serie sin apertura específica verificada. ENIF2024 integral y ENUT2024 integral permanecen prohibidos. No se confunde existencia/hash con permiso.

Corte verificado: `3e4292f8e82407535e477387e05a661400a0bb41`; índice usado SHA256 `2b04933eb9af572532cfa8f28a19832b652867bae64bf92e5a5181eff37c8460`; revisión P3 SHA256 `5211c918730e65e02ee5f0620bf27c7c273d0724fab463d75b4a32f7eb47f6f3`. El índice debe permanecer inmutable durante cada corrida y cada override corresponde exactamente a manifiesto/contenedor, sin transferir revisiones entre versiones.

Comando de comprobación del conjunto entregado:

```bash
python3 tools/validacion/astra6_paquetes_lote2.py --verifica-materializados /home/pc0/astra6-c1-aislado/lote2-P3-final-20260926-r2 --prueba-aislamiento --prueba-contenedores --lanzamientos forense/validacion-independiente/catalogo-1-preparacion-lote2/lanzamientos-lote2.md
```

PROPUESTO-POR-EJECUTOR: adaptar por acto propio `tools/validacion/astra6_catalogo/astra6_compara_catalogo.py` a las identidades/hash de las nuevas versiones antes de revelación. El comparador anterior no acepta esos SHA; no sustituir el SHA recibido por el original ni cambiar los nueve inputs de sesión01. No hubo comparación ni revisión independiente de resultados en esta pieza.

Revalidación final sobre corte `3e4292f8e82407535e477387e05a661400a0bb41`:11 copias,59 identidades y hashes conservados. Pruebas de aislamiento preservadas del corte `c6c98c3458d12ceb9a71c9e4a975281be6c3bd37`; cambio heredado sólo bitácora bloqueos.tsv, sin nueva ejecución bwrap.
