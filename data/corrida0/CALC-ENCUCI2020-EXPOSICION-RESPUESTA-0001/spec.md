# CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001

Especificación humana congelada el 19 de septiembre de 2026 para describir,
en ENCUCI 2020, el contacto con diez tipos de autoridad y la distribución
conjunta de solicitud/entrega de dádivas. Se escribió antes de abrir registros
del DBF en este acto. El primer resultado se conserva.

## Identidad, documentación y exposición previa

- Fuente: `encuci2020_bd_dbf`, `BD_ENCUCI2020_dbf.zip`, SHA-256
  `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283`.
- Miembro: `ENCUCI_2020_SEC_4_5.dbf`; unidad: persona seleccionada de 15 años
  o más; una ola, ENCUCI 2020.
- Descriptor: `encuci2020_fd_pdf`, SHA-256
  `6cd6f7475a0b5db27a84cf0e047db5b7ed98f73c3480a9e64ea084bc7d475638`.
  Acredita `FAC_SEL` para el informante seleccionado, `DOMINIO={U,C,R}` y el
  diseño `EST_DIS`/`UPM_DIS`.
- El descriptor transcribe 5.16: contacto en los últimos 12 meses (agosto de
  2019 a la entrevista), incluso mediante intermediario, con diez tipos de
  servidores; códigos 1 Sí, 2 No, 9 NS/NR. 5.17 pregunta si alguno pidió una
  dádiva/favor/dinero extra y 5.18 si la persona tuvo que darla, con códigos
  1/2/9/blanco. El blanco de 5.17/5.18 es salto, no negativo.
- Se leyeron antes de congelar el encargo, la especificación, resultados y
  medidor de `CALC-ENCUCI-0001`, el preregistro
  `ENCUCI-MORDIDA-PROTESTA` y la resolución F2. Esta corrida no es ciega. La
  tasa nacional sellada de la unión se usa sólo como control sobre idéntico
  universo; no se presenta como hallazgo nuevo ni se reabre F2.
- Búsqueda por contenido en `origin/main` y en las ramas locales con nombre
  ENCUCI no encontró este CALC ni tablas equivalentes con conteo exacto de
  tipos y distribución conjunta condicionada.

## Universos y transformaciones

El marco son todas las filas con `FAC_SEL` finito y positivo. Para cada inciso
de 5.16 se estima Sí entre respuestas 1/2 y se publica por separado la masa
desconocida. Contacto cualquiera vale Sí si existe al menos un 1; vale No sólo
si los diez son 2; en los demás casos es desconocido. El número exacto de
tipos existe sólo cuando los diez códigos están en {1,2}; se agrupa 0, 1, 2,
3 o más y se publica la cobertura de casos completos.

La tabla conjunta usa personas con contacto acreditado y AP5_17/AP5_18 ambos
en {1,2}. Sus cuatro celdas exhaustivas son ninguna (2,2), sólo solicitud
(1,2), sólo entrega (2,1) y ambas (1,1). Se estima para: total; conteo exacto
1, 2 y 3+; y cada valor nativo U, C y R de `DOMINIO`, sin cruzar ejes. Cada
grupo informa n/masa base y cobertura del filtro de respuestas válidas. También
informa P(entrega|solicitud) y P(entrega|no solicitud); denominador vacío da
`null`/NO-ESTIMABLE y no impide las otras celdas.

Los contrastes preespecificados son 2−1 y 3+−1 tipos para P(solicitud o
entrega), y para la brecha P(entrega|solicitud)−P(entrega|no solicitud). Son
asociaciones descriptivas de personas, no riesgos por trámite ni efectos del
contacto. Los tipos pueden coexistir y no representan frecuencia o número de
trámites. Solicitud/entrega coobservadas no prueban una misma transacción ni
permiten atribuir la dádiva a una autoridad concreta.

## Diseño e incertidumbre

El punto usa `FAC_SEL`. Todas las razones son dominios del marco completo. Se
generan 2,000 réplicas de bootstrap de UPM con reemplazo dentro de `EST_DIS`,
con `numpy.PCG64` y semilla 20260919. El sorteo es único y compartido por todas
las celdas: contrastes y diferencias condicionales se calculan réplica a
réplica, preservando covarianza. Una UPM única se autorremuestrea y aporta
varianza cero; si existe, el método queda rotulado y los intervalos pueden ser
estrechos. Si cualquier fila del marco carece de estrato/UPM, los puntos se
conservan y todos los IC quedan no disponibles. No se usa bootstrap iid ni se
forman IC dividiendo límites marginales.

## Comprobaciones y salida

Se exige llave `ID_PER` única; se publican estratos, UPM y singletons. Las
pruebas verifican desconocidos del vector, contactos múltiples y denominador
condicional vacío. En datos se comprueban: suma de las cuatro celdas = 1 e
identidad unión = solicitud + entrega − ambas. Los RESULT tabulares son JSON
canónico dentro de valores de texto, para conservar tablas completas sin
seleccionar sólo grupos detectables. El mapa RESULT→estimando/universo se
documenta en la nota de ejecución.
