# RESIDUALES-P3-IC-v1 · PROPUESTO-POR-EJECUTOR

Contrato nuevo íntegro de reproducibilidad diagnóstica, pendiente de firma de contenido. No adoptado. No certifica cobertura nominal de diseño. Debe congelarse con entrada y entorno antes de un intento futuro. IC95 significa intervalo percentil de la distribución empírica de réplicas; hasta justificar diseño no se anuncia como intervalo poblacional con cobertura95%.

## Estimador, marco y dominios

Para cada identidad exacta del esquema, D_i indica pertenencia al dominio, K_i respuesta válida según su spec humana y y_i su desenlace. Numerador X=sum(w_i D_i K_i y_i), denominador Y=sum(w_i D_i K_i), estimador X/Y. No imputar NS/NR ni negativos a cero. Las medias conservan escala original; proporciones están en0..1. Y=0 es NO-ESTIMABLE, nunca cero. Variables, filtros, llaves y ponderadores se fijan por módulo; este contrato no permite cambiar el estimando.

Marco: todos los pares distintos (estrato,UPM) del universo base con ponderador finito positivo y diseño válido, antes de filtrar dominio o respuesta de una conducta. Incluye pares con X_hu=Y_hu=0. No reduce marco a observaciones conocidas del dominio. Filas sin diseño salen contadas. Población completa significa muestra completa elegible del módulo, no censo poblacional ni todas las olas. Join ambiguo o ausencia de campos es NO-ESTIMABLE-DISENO, sin probar llaves alternativas al ver cifras.

Por cada par calcular X_hu=sum(w_i D_i K_i y_i),Y_hu=sum(w_i D_i K_i); mantener ceros explícitos. Peso final sin normalizar, recalibrar ni estimar nuevamente por réplica. Se condiciona a ajustes de pesos entregados; no reproduce incertidumbre de la calibración o no respuesta. Sin FPC: aproximación con reemplazo a contribución de primera etapa; no afirma igualdad con muestreo sin reemplazo, multietapa o varianza oficial.

## Algoritmo de réplicas

Bootstrap empírico no reescalado de UPM: B=2000; por cada réplica r y estrato h con n_h pares, seleccionar n_h índices iid uniformes con reemplazo. Multiplicidad M_rhu determina X_r=sum(M_rhu X_hu),Y_r=sum(M_rhu Y_hu),t_r=X_r/Y_r. No remuestrear personas independientemente ni hogares fuera de su UPM.

Orden de pares: lexicográfico por cadena opaca de estrato y UPM; conservar bytes y ceros iniciales, no convertir a enteros ni rellenar. Validar UTF-8; comparación por puntos Unicode, sin trim implícito. Orden de contribuciones: filas en orden físico de la tabla base declarada: TENBIARE para ENBIARE, Individual para ENCODAT, SEC_4_5 para ENCUCI A, SEC_6_7_8 para ENCUCI B protesta y concentradohogar para ENIGH; uniones por llave única conservan orden de la base; sumas float64, totales por par en ese orden y acumulación de pares ordenados. Una diferencia por orden flotante afecta reproducción exacta y se declara, sin alterar tolerancia.

Referencia de RNG: numpy.random.Generator(numpy.random.PCG64(20260923)); una instancia nueva por identidad, sin saltos ni compartir estado entre conductas. Iteración réplica→estrato lexicográfico; por estrato usar rng.choice(indices_ordenados,n_h,replace=True), incluso singleton. Congelar versión NumPy, Python, plataforma y hash de la implementación independiente en acto futuro antes de leer valores; versiones distintas constituyen realizaciones distintas, no justificación para cambiar contrato tras ejecución. Esta receta especifica la operación pública de RNG; no promete bit a bit entre bibliotecas o plataformas.

Singleton: se sortea a sí mismo, no se colapsa ni descarta; contribución de varianza no identificable salvo evidencia de certeza. Registrar cantidad y marcar IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA. No llamar certeza por tener n_h=1 ni afirmar límite inferior matemático universal. La etiqueta histórica de límite inferior queda preservada en su acto, no ratificada aquí.

Una réplica Y_r=0 es NO-ESTIMABLE y conserva su posición. Si cualquiera no es finita o no estimable, intervalo y SE son nulos; no eliminar ni repetir sorteos. Para2000 réplicas finitas, ordenar t_(0)..t_(1999), cuantil q lineal tipo7: a=(B-1)q,j=floor(a),Q=(1-a+j)t_(j)+(a-j)t_(j+1), extremos q=.025,.975; si j=B-1 usar último. SE=sqrt(sum((t_r-mean(t))²)/(B-1)). No truncar o redondear extremos para comparar; publicar representación float64 de ida y vuelta, unidad original.

## Salida y uso

Campos por llave: identidad, estimando, unidad, tipo_incertidumbre, punto, ic_lo,ic_hi,se,n_conocidos,n_upm_marco,n_upm_conocidos,n_singleton,n_replicas_no_estimables,B,semilla,RNG,regla_marco,cuantil,estado,hash_contrato,hash_entrada,hash_entorno. Este documento define campos, no contiene números ejecutados. No entregar referencias históricas o dictámenes al reconstructor.

Regla de publicabilidad diagnóstica para proporciones: n_conocidos>=100,UPM con conocidos>=5,ancho<=.20,CV<=.30 para punto>0; punto0 se reporta separado sin división; cualquier réplica no estimable impide publicación. No transportar ancho.20 a medias0..10: esas medias quedan SIN-REGLA-PUBLICABILIDAD-ADOPTADA. Las reglas no acreditan validez inferencial.

Para cobertura defendible falta justificar probabilidades, etapas, fracciones, ajustes de peso y dominios contra documentación oficial, decidir singleton y evaluar cobertura bajo diseños declarados. Se recomienda mantener este contrato como referencia diagnóstica común; el estimador de varianza oficial por Taylor exige otro contrato sucesor explícito si mesa decide adoptarlo. Ningún margen de equivalencia numérica se crea: tolerancia histórica intacta; inferencia válida, igualdad de ley y realización bit a bit son tres preguntas diferentes.
