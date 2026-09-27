# Sincronización y corrección CI · PR #1182

Solicitud posterior del usuario: «fetch sync solve ci». Autoriza esta corrección puntual de T02, inicialmente fuera del acto. Main sincronizado: `bf7aadc91d0607beaf5ab4c2af39334917cf4172`; integración: `c0d1c264`.

Se conservan ambos bloques de infraestructura. T02 reconoce tres pares exactos de salidas de replay independientes idénticas, el grupo exacto de resúmenes por expediente y acto y el recibo obligatorio de este acto. No excluye directorios ni modifica baseline. La procedencia de las ejecuciones está en replay-ejecutado.json.

Validación local: gate rápido con baseline, cero fallos nuevos; 23 pruebas materiales aprobadas; 231 archivos del inventario y 18 identidades del control intactos. Control negativo aislado: T02 detecta tanto una colisión ajena de nombres como una copia de contenido.

Los resultados rojos anteriores se conservan como testimonios de sus cortes. Esta nota sucede únicamente su estado CI. Recibo para Claude: recibo-para-claude.md. Firmas independientes, atestación externa y COMMIT-3 conservan sus estados; no se modifica contrato, spec ni resultado. PR abierto, sin fusión. El CI remoto del nuevo head es el juez final.
