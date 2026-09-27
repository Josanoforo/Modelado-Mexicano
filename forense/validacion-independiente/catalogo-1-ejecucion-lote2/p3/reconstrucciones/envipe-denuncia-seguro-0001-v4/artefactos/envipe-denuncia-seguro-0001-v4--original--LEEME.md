# Reconstrucción independiente congelada antes de revelación

Se usaron exclusivamente `/entrada` y los insumos enumerados de `/raw`.
No se accedió a resultados esperados ni se solicitó revelación al preparador.
`entrada/` conserva los seis archivos recibidos, byte por byte. `recibo.json`
conserva el SHA-256 del manifiesto y verifica los hashes de sus entradas.
`inventario_insumos.json` conserva rutas, URLs, tamaños, hashes declarados y
observados. `inventario_zip.json` conserva las entradas del ZIP, tamaños y CRC;
`diagnostico.json` incluye el hash del miembro analizado. No se versionan raw,
PDF, extracciones de PDF ni filas de microdatos.

Ejecutar con Python 3 y NumPy: `python3 reconstruir.py /raw`.
Las versiones empleadas constan en el recibo. Las salidas se escriben junto al
script. `replicas.tsv` contiene las cuatro proporciones de cada réplica, sin
identificadores de personas ni de unidades de muestreo.

## Evidencia e identidad

La tabla de `entrada/metodo.md` identifica explícitamente las familias CON/SIN,
los códigos 1/2 de cobertura, los códigos 1/2 de denuncia y FAC_DEL. Se usa el
miembro y payload literales indicados, sin unir otras tablas ni inferir identidad.
Los catálogos `bpcod.csv`, `bp2_1.csv`, `bp1_20.csv`, `fac_del.csv`, `est_dis.csv`
y `upm_dis.csv` dentro de `tmod_vic_envipe2025/catalogos/` confirman las variables.
La descripción de archivos `fd_envipe2025.pdf` confirma BPCOD en página PDF 64,
BP1_20 en página PDF 72, BP2_1 en página PDF 77 y los campos de diseño en página
PDF 81 (página impresa 79). El cuestionario del módulo confirma las preguntas
1.20 y 2.1 en páginas PDF 4 y 6. El cuestionario principal está inventariado;
no fue necesario para resolver variables del módulo.

La pregunta 1.20 se refiere a acudir personalmente al Ministerio Público o
Fiscalía; no se amplía con BP1_21 ni otros medios de denuncia. El ponderador es
FAC_DEL, no FAC_DEL_AM. EST_DIS y UPM_DIS se leen como texto, sin convertirlos a
números ni sustituirlos por ESTRATO o UPM.

El TSV recibido contiene separadores escritos como secuencias literales
`\t` y `\r\n`. El lector reemplaza exclusivamente esas secuencias; el archivo
original preservado no se modifica. La salida sí es un TSV convencional UTF-8.

## Cálculo y convenciones reproducibles

Unidad observacional: delito. Escala numérica de salida: proporción entre 0 y 1.
Para cada cobertura, el denominador es la suma de FAC_DEL entre los delitos
BPCOD="01" con BP2_1 igual al código correspondiente. Cada numerador se cuenta
por separado usando BP1_20="1" o BP1_20="2". No se calcula ningún complemento
como 1-p. Se incluyen en el denominador todos los desenlaces del estrato de
cobertura; otros códigos de cobertura no se asignan a CON ni a SIN.

Para implementar el bootstrap se toma como universo el dominio BPCOD="01"
antes de separar cobertura. En cada EST_DIS se muestrean con reemplazo m_h UPM
entre las m_h UPM_DIS observadas en ese dominio. Las multiplicidades se aplican
a todas las filas de cada UPM y se recalculan numerador y denominador por
réplica. Se comparten los sorteos entre los cuatro estimandos. Se conservan en
el marco de remuestreo los delitos de cobertura no especificada, con contribución
cero a ambos denominadores. No se incorporan UPM ausentes del dominio a través
de otras tablas o delitos.

Se usa un solo Generator(PCG64(20260915)), 2 000 réplicas, con bucles en orden
réplica-estrato y estratos/UPM ordenados lexicográficamente por sus llaves de
texto. Cada sorteo usa `integers(0, m_h, size=m_h)`. EE usa `std(ddof=1)` y los
percentiles 2.5/97.5 usan interpolación lineal. Las UPM únicas permanecen fijas.
Si existen, se reporta `IC-CON-ESTRATOS-DE-UPM-UNICA`: conforme al método, el IC
se interpreta como límite inferior de la incertidumbre; no se interpreta el
extremo inferior del intervalo como una cota adicional del parámetro.

El método no fija explícitamente el marco de UPM para el bootstrap de dominios,
el orden de consumo aleatorio, ddof ni interpolación. Las convenciones anteriores
son decisiones de implementación, no asignaciones nuevas de identidad. Los
puntos estimados se desprenden directamente de los conteos. No se puede garantizar
coincidencia de EE/IC a 1e-10 con otra implementación que adopte convenciones
diferentes; no se utilizaron resultados esperados para elegirlas.

## Verificación y congelación

Se verifican hashes de las entradas y los cuatro insumos, existencia de nombres
literales, pesos positivos, llaves no vacías y denominadores de réplica positivos.
La suma de probabilidades se comprueba tras contar ambos numeradores, con la
tolerancia recibida. `validacion.json` registra una comprobación independiente de
los conteos mediante Decimal y una repetición determinista de las salidas.
`congelacion.sha256` registra los hashes de los archivos antes del commit, salvo
el propio listado. El commit incluye código, números, evidencia y entradas.
No se realizó una fase de revelación ni de comparación con resultados esperados.
