# PISOS ENVIPE 2024 · especificación congelada v1.0

Congelada el 19/sep/2026, antes de abrir respuestas individuales.  Mide la
persistencia marginal `p_2024(evade_norma | eje=categoria)` para el consumidor
`tramite.evasion_norma_ejes_envipe2025` y, separadamente,
`p_2024(denuncia | cobertura_seguro)` para
`civico.denuncia.con_seguro_ejes_envipe2025`. No abre ENVIPE 2025.

Unidad: delito en `conjunto_de_datos_tmod_vic_envipe2024.csv`.  Para evasión,
el universo es `BP1_20 in {1,2}`, peso `FAC_DEL`, y el indicador es
`BP1_20=2 and BP1_23 in {04,05,06,08}`. Sexo y edad viven en el delito;
escolaridad se une por `ID_PER` a `tsdem` sin multiplicar delitos; dominio es
`DOMINIO in {U,C,R}`. Las edades son 18--29, 30--44, 45--59 y 60+; escolaridad
usa la conversión acreditada de `NIV` del árbitro; dominio conserva
Rural/Complemento urbano/Urbano. Registros sin una categoría válida se cuentan
y no se imputan.

Para denuncia con seguro el universo adicional es robo total de vehículo y
la capa de cobertura acreditada por el consumidor; sólo se construye si el
catálogo 2024 confirma el reactivo y sus códigos. Una diferencia de texto,
universo o catálogo frente a 2025 produce `NO-CONSTRUIBLE` de esa celda.

Varianza: bootstrap estratificado por `EST_DIS`, UPM `UPM_DIS`, 10 000
réplicas, `numpy.PCG64(42)`, muestreo de UPM con reemplazo dentro de estrato.
Un estrato con una UPM se remuestrea a sí mismo; denominador vacío deja punto e
IC nulos con causa. Punto, IC95 percentil, n no ponderado y denominador
ponderado se emiten por celda. El IC describe incertidumbre muestral de 2024,
no predicción de 2025, deriva temporal ni causalidad.

Consumidor previsto: vocabulario celda-D v0.6 / acto 03 (no implementado por
este acto). La firma del 17/sep adopta el piso no vencido; esta especificación
no escribe `ADOPTADO_ACTIVO`.
