# Contrato previo · ENCRIGE 2020, carga e intensidad por tamaño

Estado: `FIJADO-ANTES-DEL-CALCULO-DERIVADO`. Los puntos de entrada ya fueron
observados y publicados por el acto padre; esto es análisis exploratorio de
resultados oficiales, no un preregistro ciego ni una medición independiente.

## Padre e identidad

Única tabla de entrada autorizada:
`forense/analisis/encrige-descriptiva-1/encrige-corrupcion-por-tamano.csv`,
SHA-256 `632ce31b2c2cf70e22871319b5842e6168592f065588b69b11010e3552b48c26`.
Proviene de `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`; su
`resultados.json` publica el mismo SHA y está cubierto por el sello
`dd2bc7dc912585301632789ac3b3bc2208c0ab5d9b8c1db83afa18fa2233a39a`.

Para cada dominio `s` (nacional, Micro, Pequeña, Mediana y Grande):

- `N_s`: unidades económicas expuestas a al menos un trámite o inspección;
- `A_s`: unidades económicas con al menos un acto de corrupción;
- `T_s`: trámites o inspecciones con experiencia de corrupción;
- `p_s=A_s/N_s`: proporción de empresas expuestas afectadas;
- `m_s=T_s/N_s`: trámites/inspecciones con corrupción por empresa expuesta;
- `r_s=T_s/A_s`: trámites/inspecciones con corrupción por empresa afectada;
- identidad: `m_s=p_s*r_s` cuando `A_s>0`.

Antes de unir indicadores se exige igualdad exacta de dominio, tipo de
dominio, periodo, denominador y unidad expandida. También se exige la semántica
publicada del numerador de incidencia. Si `A_s=0`, `r_s` se emite
`NO-ESTIMABLE-A-CERO`; nunca infinito ni cero imputado. Si las definiciones
acreditadas implican `T_s>=A_s`, una violación detiene la derivación.

## Participaciones y contrastes

Las cuatro categorías de tamaño, sin incluir el nacional como quinta parte,
producen `N_s/ΣN_s`, `A_s/ΣA_s` y `T_s/ΣT_s`. Cada suma de masas se contrasta
contra el nacional; se informa el residuo y no se renormaliza contra éste.

Micro es la referencia fija. Para cada `s` en Pequeña, Mediana y Grande:

`m_s-m_micro = 0.5*(p_s-p_micro)*(r_s+r_micro) + 0.5*(r_s-r_micro)*(p_s+p_micro)`.

El primer término es contribución aritmética asociada a prevalencia y el
segundo a intensidad condicional. Ambos se expresan como trámites/inspecciones
con corrupción por empresa expuesta; la diferencia de `p` también se muestra
en puntos porcentuales. No son efectos causales.

## Precisión, salida y límites

Los absolutos publicados tienen cuatro decimales. Antes de observar los
residuos se fija tolerancia absoluta `0.0003` unidades expandidas para la suma
de cuatro tamaños frente al nacional: cinco redondeos a `0.0001` pueden
acumular hasta `0.00025`. Para tasas/identidades se fija `1e-12`; los cálculos
usan `Decimal` y los CSV emiten razones a doce decimales. No se exige que `m`
o `r` pertenezcan a `[0,1]`.

Se producirán tabla ampliada, participaciones, tres contrastes, controles JSON
y figura SVG. El universo sigue siendo empresas privadas con instalaciones
fijas en los sectores cubiertos por ENCRIGE, expuestas a al menos un trámite o
inspección, durante enero–entrevista de 2020. Los absolutos son estimaciones
expandidas, no tamaños muestrales. No hay EE, CV o IC utilizables; no se
declaran significancia, causalidad, tendencia, riesgo por interacción ni
intervención óptima.

