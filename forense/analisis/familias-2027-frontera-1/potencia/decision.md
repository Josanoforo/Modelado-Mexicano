# P3 · factibilidad y decisión

PROPUESTO-POR-EJECUTOR. **No lanzar aún ENSU.** La preparación del paquete
sí es útil; aprobar un lector y ejecutar oro no acreditan capacidad futura.
ENSANUT y MOCIBA no reciben potencia numérica prestada de ENSU: su
dictamen instrumental corresponde a P1. ENOE es un candidato marginal
independiente y exige su propio oro, no inferencia longitudinal de personas.
Cero retadores.

EJECUTADO: `python3 forense/analisis/familias-2027-frontera-1/potencia/calcula.py`.
Criterios documentados antes de correr en `criterios-previos.md`; integración
normal analítica, sin simulación ni semilla. `frontera-potencia-resultados.json` y `escenarios.tsv`
contienen valores generados por comando y todos los supuestos explícitos.

La familia usa dos sexos y una sola ola objetivo. Error familiar .05 mediante
Bonferroni; banda propuesta de persistencia ±.05; potencia objetivo .80.
El MDE de cambio respecto al oro no mide por sí solo la capacidad de confirmar
persistencia: se exige que el IC simultáneo quede enteramente dentro o fuera
de la banda. Los escenarios muestran que detectar un cambio de .10 puede ser
posible mientras una conclusión de persistencia sigue siendo inconclusa.

La varianza del oro y la del objetivo entran por separado; en las proyecciones
SE futura=SE histórica es un supuesto, nunca un resultado. La dispersión
temporal adicional .00/.01/.03 es independiente y asumida: no se calcula de
réplicas del oro. La cobertura nominal del IC se refiere al cambio realmente
ocurrido; integrar dispersión temporal estima cuán a menudo ese cambio será
distinguible, bajo el escenario elegido. Se usa normal sin truncar para el
cambio local; no sirve para prevalencias cerca de 0 o 1.

La cobertura .05 familiar es nominal bajo aproximación normal y SE de diseño
correcto; no se afirma exactitud finita. ENSU tiene pocos casos por sexo y
usar cuantiles t de diseño ensancharía el intervalo: el fracaso de factibilidad
con normal no se cura por esa corrección. Se requiere evaluar diseño real antes
de cualquier inferencia adoptada.

ENSU CD01 dos años aparte: rho=0 es la decisión conservadora hasta documentar
covarianza. rho=.5/.8 solo muestra sensibilidad a dependencia muestral; no
autoriza adjudicar precisión. Sexos comparten UPM, estratos y calibración.
Bonferroni es válido con esa dependencia y la cota conjunta de informatividad
no multiplica probabilidades como si fueran independientes. Inferencia
definitiva debe calcular covarianza entre sexos y entre olas con diseño real.

ENOE requeriría trimestre fijo, cambios de cuestionario/desempeño de diseño y
agrupación de panel por hogar/UPM; la rotación impide usar olas cercanas como
réplicas independientes. Para 2024→2027 no se presume solapamiento del panel.
No se convierte el número de olas en tamaño efectivo.

Un sucesor puede recomendar lanzamiento si se valida comparabilidad histórica
y futura, inferencia de diseño del oro y ambos sexos satisfacen .80 de
informatividad bajo estabilidad y cambio material, incluido el escenario
temporal adverso. El criterio no se ajusta tras ver resultados. Si no pasa,
ampliar banda o cambiar ciudad requiere un contrato nuevo justificado; no se
optimiza esta propuesta después de abrir la reserva.

ENSU: oro ejecutado y SE Taylor del paquete integrado con `--gold-se
forense/analisis/familias-2027-frontera-1/paquetes/ENSU-CAMPECHE-INSEGURIDAD/ensu-oro.json`.
La conclusión no depende de inventar incertidumbre temporal: aun con sigma
temporal cero y SE futura igual al oro, el IC de cambio es más ancho que la
banda y la probabilidad de decisión informativa está lejos del criterio.
Los valores exactos y MDE constan en el JSON generado. Ampliar la muestra o
agregar ciudades altera la pregunta local y exige propuesta nueva, no una
presentación de este resultado como lanzable.

`power_change` y `mde` contrastan cambio cero, no pertenencia a la banda.
Las columnas `probability_informative_*` evalúan IC físico de dos poblaciones.
Las columnas `conditional_fixed_p0_*` evalúan futuro contra la emisión p0
fija usando solo SE futuro: son un diagnóstico distinto. La emisión p0 del
paquete no se altera ni se le adjudica ruido al evaluarla. El dictamen P3
conservador incluye error del oro para no confundir persistencia del número
histórico con persistencia de la población. La cota conjunta de dos sexos
usa ambas probabilidades; solo los escenarios genéricos suponen sexos con
igual precisión. No se presume independencia entre ambos.

ENOE: oro 2024T4 ejecutado (`paquetes/ENOE-INFORMALIDAD/enoe-oro.json`),
pero inferencia Taylor bloqueada: 39 estratos tienen una sola UPM en el marco
leído, ambos sexos, y el lector devuelve SE nula en vez de fingir precisión.
`gold_inference_blocks` registra por comando las identidades exactas. **No
lanzar ENOE todavía.** El n efectivo Kish no sustituye diseño estratificado
conglomerado; no se convirtió en SE ni MDE acreditado. Para desbloquear:
verificar marco completo de UPM, obtener réplica oficial o regla de tratamiento
de singleton documentada antes de volver a inferir. Colapsar estratos después
de observar potencia para forzar lanzamiento no es un sucesor aceptable.
El cálculo conserva los escenarios hipotéticos de factibilidad, sin atribuir
a ENOE un SE histórico que no puede obtenerse con este diseño disponible.
