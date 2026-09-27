# ENDIREH 2021 no física B/C · dos discrepancias de punto

EJECUTADO: investigación no ciega posterior a congelación `b816d9635a6bd315fb5919e7c879144462ab41c8`, reconstrucción SHA-256 `4068611e6ad521df6d82256a43ab4adbd17675d4f4284d6ba175e321c694cb82`. Solo se leyeron los dos dictámenes de punto, sus identidades desde el tar archivado, artefactos del cálculo independiente y porciones pertinentes del único productor CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001. Sin recalcular, cambiar tolerancias, comparar otra realización ni editar sello.

| Llave | Conducta y segmento | Punto original | Punto reconstruido | Delta reconstruido − original |
|---|---|---:|---:|---:|
| RESULT-ENDIREH2021-NF-BC-TABLA#494 | ayuda_bc · edad=60+ | 0.059119121098944002 | 0.058265519312162652 | -0.00085360178678135085 |
| RESULT-ENDIREH2021-NF-BC-TABLA#543 | denuncia_bc · edad=60+ | 0.087315198304587116 | 0.086617696390107385 | -0.0006975019144797312 |

EJECUTADO: las dos discrepancias corresponden a un único grupo, ayuda/denuncia entre afectadas B1/B2/C1 con edad 60+. La comparación usa tolerancia congelada abs=1e-10; el azar de bootstrap no explica una diferencia del punto ponderado.

La causa identificada en código es el tratamiento de EDAD desconocida: medidor.py:39–46 admite enteros de 15 a 120 y etiqueta todos los mayores de 59 como 60+; reconstruir.py:57–62 excluye EDAD≥98 del corte de edad. El FD recibido del paquete, sección TSDem/reactivo 2.4/variable EDAD, dice: 97 = 97 o más años; 98 = edad no especificada en personas de 15 años o más; 99 = edad no especificada. Por tanto 98/99 no son edades observadas de 60+; la clasificación del productor contradice la codificación del FD. SHA FD del paquete `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180`.

EJECUTADO: los originales de ambas celdas tienen n conocido=4439 y masa ponderada=1951619; diagnostico.tsv independiente reporta n conocido=4430 en ambas. Nueve respuestas menos junto con la exclusión explícita de edad desconocida constituyen evidencia consistente con este mecanismo. No se tabularon individuos por EDAD ni se ejecutó contrafactual: no se demuestra aquí que esos nueve sean exclusivamente 98/99 ni cuánto contribuye cada registro a la diferencia. El defecto semántico del productor está comprobado por código/FD; la atribución exhaustiva de la magnitud permanece hipótesis fundada.

Ambos códigos usan FAC_MUJ, unión de actos 1–38 y ayuda/denuncia P14_7_1/P14_7_2 entre afectadas B1/B2/C1. La reconstrucción conserva EDAD=98 en elegibilidad global, pero lo excluye en cortes por edad; el productor admite también 99 globalmente. Esto exige revisar fuera de este dictamen los universos nacional y etario; no se infiere que toda cifra nacional sea errónea ni se extiende la investigación a otras celdas.

LEÍDO/EJECUTADO: #494 y #543 aparecen literalmente en canon/catalogo-del-mexicano-v1_2.tsv y canon/tabla-de-piso-v1_1.tsv, ADOPTADO, dominio GENERO, área de consulta Violencia contra las mujeres, firma FP-260923-ASTRA5-U2-ENDIREH-6a2c-01. Son consumidores expuestos al defecto del corte 60+. Las diferencias son de aproximadamente −0.08536 y −0.06975 puntos porcentuales, respectivamente; no se probó un cambio de ranking, umbral o conclusión sustantiva.

PROPUESTO-POR-EJECUTOR: mantener DISCREPA con efecto cifra y alcance del corte etario; registrar el defecto de codificación desconocida y exigir un sucesor que excluya 98/99 de los cortes de edad y declare separadamente la inclusión de edad desconocida en universos nacionales. No adoptar automáticamente la reconstrucción ni sobrescribir cifras históricas. IC se examina aparte: RNG y marco de remuestreo afectan incertidumbre, sin justificar la discrepancia de punto.
