# DIN-OFERTA-EXCLUSION-ENIF · spec v1.0 · ENIF 2012/2015/2018/2021

El primer resultado que produzca este procedimiento es el que se reporta.

Unidad P (persona 18–70), proporciones [0,1]. Cada ola mide dos conductas
distintas: sin crédito formal y sin cuenta o tarjeta formal (NO ahorro activo).
Denominador primario: todas las personas sin el producto respectivo cuyo
estado de uso es conocido, peso personal positivo y diseño estrato×UPM válido,
en cada dominio de sexo, edad, escolaridad, localidad, formalidad o nacional.
Edad es filtro universal antes de los dominios. Los ejes y el filtro de uso
siguen `DIN-CREDITO-PISOS-HISTORIA-mapa-v1_1.tsv`, con cortes del medidor
sellado `CALC-PISOS-ENIF2021-EJES-0003`. Formalidad sólo 2018/2021: seguro
social **por parte del trabajo**, 1..5 vs 6; 2012/2015 preguntan
derechohabiencia general y son NO-CONSTRUIBLE para ese eje. No se rebautiza.

## Texto, pase y clases

El mapa exacto pregunta/opción/clase/fuente es `conmensuracion-v1_0.tsv`.
Se lee el cuestionario completo de cada ola y su FD antes de bytes de casos.
Cuenta 2012: 5.3 No → 5.4 múltiple. Crédito 2012: 6.4 No → 6.5 múltiple.
Cuenta 2015: 5.4 No → 5.5 ex usuario; 5.6 razón principal si nunca;
5.8 múltiple si ex usuario. Crédito 2015: 6.4 No → 6.5 ex usuario;
6.6 múltiple si nunca; 6.7 múltiple si ex usuario. Cuenta 2018: 5.4 y 5.5
No → 5.6 ex usuario; 5.7 principal si nunca; 5.8 principal si ex usuario.
Crédito 2018: 6.3 y 6.4 No → 6.5 ex usuario; 6.6 principal si nunca;
6.7 principal si ex usuario. Cuenta 2021: 5.4.1–9 todas No → 5.20 ex
usuario; 5.21 principal si nunca; 5.22 principal si ex usuario. Crédito
2021: 6.2.1–9 todas No → 6.14 ex usuario; 6.15 principal si nunca;
6.16 principal si ex usuario. No se sustituye no uso actual por nunca uso.

OFERTA: rechazo anticipado, requisitos, distancia/ausencia, intereses,
comisiones, saldo mínimo, cierre de sucursal/institución. El texto «no cumple
requisitos (no tiene trabajo, ingresos insuficientes)» es OFERTA por el
encabezado requisitos; NO se reinterpreta el ingreso como costo. PREFERENCIA:
no necesitar/interesar, no querer endeudarse, preferir ahorro/préstamo informal,
no usarla, desinterés tras trabajo/apoyo. Desconfianza *o mal servicio* es
OTRO/NS por ambigüedad de una sola opción: ni se adjudica unilateralmente a
preferencia ni se infiere causalidad. Ingreso insuficiente solo, impuestos,
fraude, mala experiencia inespecífica, desconocimiento y «otro» son OTRO/NS.
Las opciones ausentes entre olas quedan NO-COMPARABLE para ese contraste.

Razón principal: clase única. Multirrespuesta: solo oferta, solo preferencia,
OTRO/NS (incluye mixta, otro explícito, no respuesta y pase estructural).
Además se emiten cualquier oferta, cualquier preferencia e intersección;
pueden sumar >1. Si una respuesta múltiple marca oferta y otro, permanece
OTRO/NS en la partición, con prevalencia de cualquier oferta. Cobertura es
la fracción de no usuarios con al menos una opción observada. Pase estructural
es estado de ex usuario desconocido; no respuesta es estado de pase conocido
pero sin motivo válido. No se fabrican ceros si la pregunta entera falta.

## Diseño y ejecución

Bootstrap de UPM con reposición dentro de estrato, pesos de persona, 10 000
réplicas numpy.PCG64(42), mismo plan por todas las celdas de la ola, IC95
percentil 2.5/97.5. Los dominios retienen el marco completo. El medidor
sellado de `CALC-PISOS-ENIF2021-EJES-0003` (sha256
`d069f38bd75c47fd5550015b179c7b2e61f1ab20ce6b22c630c66392afea06a3`)
aporta cortes y bootstrap; singleton queda fijo, denominador cero produce
P/IC nulos, y se reporta B-VALIDAS. Tolerancia de replay absoluta 1e-10.
No hay selección de método por anchura. No se documentan pesos replicados
oficiales pertinentes en los FD de estas bases; se usa UPM×estrato como
los pisos sellados. Una ola no construible no impide las demás.

Antes del freeze sólo se leyeron cuestionarios, FD, manifiesto, specs,
medidores y RESULT ya sellados de crédito, y se verificaron hashes/presencia
de ZIP; no valores de estos cuatro payloads en esta sesión. Se usará el
payload histórico de cada piso: 2012 DBF `7bafcf6fdd3747bf330099dd752f2010441e0cd18fe942c35b15249d98092e55`,
2015 DBF `284e8a0c57f92256efc9743785c756986fb118fff424061bdb991f28779ce5fd`,
2018 CSV `51f33ec74ccd596dc74b695587310d02e651923467255520aadc4d9fe13461d5`,
2021 CSV `0f314fa3733b4b5519486ed4015fca1c9e0864840bcd5944aa7de27796fe5cd9`.
El cargador DBF/CSV de los pisos históricos se importa por ruta/hash
`2981eed066ac5376425f7829255fc5a75332e8bcdeca58839122f5ccb426bc4a`;
no se modifica. Los identificadores, resultados y hashes completos viven en
los cuatro `spec.yaml`. `cuenta_gen2: SI`, `adopta: NO`, origen MICRODATO.

No se abre ENIF 2024 ni las otras reservas de la misión. No se reestima piso,
no se atribuye causa, no se calibra ni se adopta esta descripción.
