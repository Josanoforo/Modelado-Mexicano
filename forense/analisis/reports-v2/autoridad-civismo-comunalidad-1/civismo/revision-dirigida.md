# Revisión dirigida y decisiones editoriales · Civismo

**Leído:** v1 completo, líneas 1–314; 43 filas de `canon/mapa-dominios-v1_1.tsv` referidas al homónimo; lectura política previa `forense/analisis/dominios/lectura-politica-v1_0.tsv`. El original SHA-256 de mapa es `8d98900588d3f07e05839c2252c8b0945ecd405512d47cf43f55cae90738d4`; el encargo cita blob Git `24103b6ae61db38323506c4d4ba743b163400201`. El juicio nuevo vive en `producir.py` y se materializa en `afirmaciones.tsv`: 43 filas de mapa, tres desdobles de cláusulas compuestas y catorce cláusulas materiales ausentes del mapa. Estas últimas son `EXTRA-CIV-01` a `EXTRA-CIV-14` en el mismo orden de la tabla siguiente; no se copia automáticamente `dictamen` del mapa.

## Revisión manual de ROMPE y del contraste electoral

| Tesis original | Cambio y prueba | Reserva |
|---|---|---|
| POL-010 y POL-010-JUD: 59.8% presidencial 2024 frente a 12.86% judicial como pares del mismo electorado. | **MATIZA** 59.8%: el INE publica esa cifra en estudio muestral y 61.04% en cómputo presidencial, productos distintos. **SIN-CIFRA** 12.86% judicial: falta cargo, acta y corte rastreable. La diferencia entre procesos no identifica motivo ni mismas personas. | Ver `INE24-MUESTRA`, `INE24-COMPUTO`, `INE25-JUDICIAL`; no se impone otro porcentaje judicial sin corte. |
| POL-018/POL-036 y desdobles AGENCIA: transferencia directa «sin broker» y autonomía de voto asegurada. | **ROMPE** sólo la cláusula universal «sin broker»: FP-57 la retiró del motor y LANGSTON25 documenta agentes de inscripción, información y atribución al Ejecutivo. **SIN-CIFRA** autonomía/derecho/gratitud: BALLOT25 muestra que una oferta puede afectar percepción de secreto, pero no observa votos de beneficiarios actuales. | No hay evidencia de monitoreo del voto individual por esos agentes; autonomía efectiva queda abierta. |
| EXTRA-CIV-08 / EXTRA-CIV-11 | La universalidad de una pensión no elimina intermediación de inscripción/propaganda; la informalidad laboral no equivale a evasión individual. | LANGSTON25; definición de TIL1 del INEGI (`ENOE-DEFINICION`). |

## Cláusulas materiales del v1 ausentes o compuestas en el mapa

| Localizador v1 | Cláusula separada | Juicio | Por qué y prueba faltante |
|---|---|---|---|
| L22/L129 | «31 de 32 entidades» como argumento de ausencia de clivaje | MATIZA | El resultado por estado no sustituye composición por clase, municipio y voto individual. Requiere microdatos postelectorales comparables; el cómputo INE sólo prueba geografía. |
| L24/L145 | «polarización menor que EE. UU.» | SIN-CIFRA, no comparabilidad | Instrumento, periodo y unidad (líder/partido) difieren. Se necesitaría termómetro armonizado misma ola en ambas poblaciones. |
| L85–L89 | Mayor confianza atribuida a menor contacto extractivo | SIN-CIFRA, instrumento inadecuado | ENCIG permite relación perceptual transversal; exposición real/contacto no queda identificado en la comparación citada. |
| L103 | Diferencia de motivo de no denuncia por sexo | SIN-CIFRA, falta de ejecución | Se leyó el boletín agregado, no un contraste por sexo con error de muestreo; no se conserva la cifra puntual del v1. |
| L117 | Complejidad de boletas y resultado decidido como causa de abstención | SIN-CIFRA, identificación | El agregado electoral no pregunta percepción previa a quienes se abstuvieron; requiere encuesta preelectoral o cambio exógeno de diseño. |
| L133 | Mal desempeño de seguridad entre quienes aprueban presidenta | SIN-CIFRA, no comparabilidad | No se cotejó microdato conjunto, fecha de campo ni casa; no pasa a conclusión. |
| L145 | Líder/partido como eje «único» de México, EE. UU. y Perú | SIN-CIFRA, adquisición pendiente | Índices comparados históricos no se recalcularon y no se validó el umbral común. |
| L159 | Universalidad de pensión implica inexistencia de intermediación | ROMPE | Universalidad legal no elimina inscripción/comunicación de agentes; separar broker de acceso, movilización y monitoreo. |
| L181 | Linchamientos crecen *con* criminalidad e impunidad | SIN-CIFRA, adquisición pendiente | Una coocurrencia espacial y cobertura de prensa no identifican asociación ni mecanismo; requiere panel municipal con definición constante. |
| L195 | 8M y búsqueda son «las formas más vitales» | SIN-CIFRA, instrumento inadecuado | No hay marco nacional común de eventos ni participación para ordenar modalidades. |
| L208 | Informalidad equivale a evasión de subsistencia | ROMPE de equivalencia conceptual | Empleo informal puede no implicar evasión voluntaria del trabajador; no hay reactivo conjunto. La cifra ENOE del v1 no se replica aquí. |
| L214/L216 | Generaciones y religiosidad determinan cívica | SIN-CIFRA, instrumento inadecuado | Edad, cohorte, escolaridad, región y religión confunden; exige interacciones y periodos múltiples. |
| L224 | Policía comunitaria como rasgo distintivamente mexicano | SIN-CIFRA, comparación ausente | Requiere tipología de organizaciones comunitarias en otros países y alcance local del caso mexicano. |
| L236 | Colectivos «más legítimos y efectivos» | SIN-CIFRA, desenlace indefinido | Legitimidad de quién y efectividad para qué necesitan indicadores propios; su existencia no da ranking. |

## Juicios transversales y cambios de tesis

| Tesis v1 | v2 usable | Evidencia principal | Próxima observación que obligaría a cambiar |
|---|---|---|---|
| Desconfianza = calibración racional | Jerarquía de confianza declarada por institución y encuesta; mecanismo abierto. | ENCIG25, ENCUCI20 | Panel de contactos/desempeño y confianza antes/después. |
| No denuncia = tolerancia o cálculo | Cifra negra alta con razones declaradas heterogéneas; ninguna etiqueta psicológica única. | ENVIPE25 | Intervención de protección/rapidez y medición de denuncia y carpeta. |
| Participación contingente = cálculo individual | Participación difiere por elección y segmento; motivo no identificado. | INE24-MUESTRA, INE24-COMPUTO, INE25-JUDICIAL | Panel con relevancia percibida previa y participación verificada. |
| Clientelismo sin broker = voto libre | Intermediación de inscripción y propaganda existe; monitoreo individual no demostrado. | FP-57, LANGSTON25, BALLOT25 | Medición separada de oferta, inscripción, coerción percibida y voto. |
| Mordida = trampa social | Experiencia de corrupción en trámites urbanos; expectativas y causalidad abiertas. | ENCIG23/25 | Comparación de oficinas con cambio de discrecionalidad. |
| Protesta/autodefensa = vacío estatal | Formas cívicas locales diferentes; no ranking ni causa universal. | Original, límites de fuentes | Panel municipal y etnografía situada de autoridad/redes. |

## Reglas propuestas

| Regla | Consumidor posible | Condición | Falsador |
|---|---|---|---|
| CIV-P1 | Analista electoral | Comparar tasas sólo tras fijar cargo/corte/lista y producto. | Actas que acrediten identidad de definiciones y reversión del contraste. |
| CIV-P2 | Servicio de denuncia | Separar denuncia de apertura de carpeta y motivos declarados. | Misma ola/definición con conjuntos idénticos de no denuncia y cifra negra. |
| CIV-P3 | Evaluación de programas | Medir etapas de intermediación y percepción de secreto antes de atribuir voto a beneficio. | Diseño creíble donde omitir etapas no cambie resultado ni signo. |

**No adoptadas.** Son reglas analíticas propuestas para mesa, no probabilidades del motor. Ninguna requiere abrir una ola reservada.
