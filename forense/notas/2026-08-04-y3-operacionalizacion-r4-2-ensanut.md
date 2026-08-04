# Operacionalización pre-registrada · `R4.2` · ENSANUT 2024 · Encargo Y, commit 1

*(Escrita antes de correr ninguna estadística de resultado. La ficha misma ordena el chequeo barato primero — línea 120: "Verifícalo primero: es lo más barato y decide si el resto vale la pena" — así que este commit registra el diseño que se hubiera corrido Y el resultado de ese chequeo, en el mismo acto, porque el chequeo barato decidió que no hay nada más que operacionalizar.)*

**Umbral de la ficha (línea 118):** "Diferencia hombre-mujer en posposición **<10 puntos**, controlando tipo de empleo y acceso a servicio." **Fila `D` declarada por la propia ficha (línea 120): "si la encuesta no cruza permiso laboral con conducta preventiva."**

## Diseño que se hubiera corrido (declarado por completitud, no ejecutado)

- Población: adultos de ENSANUT 2024 (tabla `integrantes`, universo con necesidad de salud reciente).
- Numerador esperado: pospuso un chequeo médico **por falta de permiso laboral**, comparado entre `sexo` = hombre vs. mujer.
- Denominador/controles: tipo de empleo (`H0321`-`H0324`) y acceso a servicio de salud.
- Ponderador `ponde_f`, estrato `estrato`/`est_sel`, UPM `upm` (tabla `integrantes_ensanut2024_w_ICB`).

## Chequeo barato — el cruce que el Umbral exige no existe

Verificado contra el cuestionario Hogar (`1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf`) y los catálogos de variables de `integrantes_ensanut2024_w_ICB` y `adultos_ensanut2024_w` (raíz `descargas_mx`, `/mnt/c/Users/PC0/Descargas MX/` — declarado, no disimulado: son los archivos reales, registrados en `data/manifiesto.yaml` con `raiz: descargas_mx`, fuera de `data/raw/` integrado):

1. **No existe una pregunta sobre "sin permiso laboral para atender su salud".** `grep -i "permiso"` sobre ambos cuestionarios PDF solo encuentra coincidencias en el módulo de tamizaje (§10.7), sin relación con trabajo.
2. La pieza más cercana es `H0405A/B/C` ("¿Por qué motivo no buscó atención?"), con la categoría genérica **"06 No tuvo tiempo"** — no distingue motivo laboral de otros (cuidado de hijos, etc.), y no menciona permiso.
3. La pieza de "chequeo" más cercana es `H0402=30` ("Chequeo o consulta médica") dentro de una lista de 40 motivos de última necesidad de salud en 3 meses — no es una pregunta dedicada a posposición de chequeos, y solo captura la **última** necesidad reportada (excluye a quien pospuso un chequeo pero tuvo una necesidad más reciente de otro tipo).
4. Reconstruir "pospuso el chequeo por falta de permiso laboral" exigiría encadenar `H0402=30 ∧ H0403=Sí ∧ H0404=No ∧ H0405∈{...,06,...}` — y aun así, el resultado sería una variable que mide "no tuvo tiempo" genérico, no "sin permiso laboral", que es exactamente lo que el Umbral pide controlar. No existe variable de formalidad/afiliación IMSS-ISSSTE en los catálogos de `integrantes`/`hogar` revisados (`grep -i "afiliad|derechohab|imss|issste"` sin resultados, salvo credencialización IMSS-BIENESTAR, que es cobertura de salud, no formalidad laboral).

**No es hueco de dato accidental ni de curaduría del repo — es que ENSANUT 2024 no formula la pregunta.** Coincide, letra por letra, con la fila `D` que la propia ficha pre-anticipó.

⚠️ **Nota de infraestructura, declarada por separado, no cambia el veredicto:** el zip `adultos_ensanut2024_w.csv.csv.zip` referenciado en `data/manifiesto.yaml` no contiene microdato de fila-por-persona en la carpeta `descargas_mx` — solo envuelve su propio catálogo (`.xlsx`) dos veces. El microdato individual relevante (sexo, tipo de empleo, motivo de no búsqueda de atención) vive en `integrantes_ensanut2024_w_ICB.csv.csv.zip`, no en el archivo "adultos". Esto no afecta el veredicto — la variable que el Umbral necesita no existe en ningún archivo del instrumento, independientemente de en cuál tabla se busque.

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta**: el chequeo barato, ejecutado antes de abrir ningún microdato de fila-por-persona, ya lo produjo. No se corre el resto del diseño.
