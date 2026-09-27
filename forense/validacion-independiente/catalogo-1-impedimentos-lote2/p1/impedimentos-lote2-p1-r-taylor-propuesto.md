# Árbitros R: contrato inferencial humano nuevo

PROPUESTO-POR-EJECUTOR. Firma de contenido previa. No completa retrospectivamente
el método congelado ni demuestra qué algoritmo produjo los árbitros históricos.
Los 14 contratos JSON propios fijan por identidad tabla, variable, universo,
codificación, peso y diseño desde codificacion-R-v1_2.tsv. Se excluyeron de la
transcripción sus conteos observados y alusiones al productor. La insuficiencia
histórica EE/IC permanece D-15, separada del punto reproducible.

Unidad y código son los del JSON individual. CSV/DBF conserva cadenas; códigos
numéricos equivalentes 1 y 1.000000000000000 se normalizan solo en reactivos,
nunca en llaves de diseño. Diseño textual opaco; no rellenar ni convertir a
entero. Peso finito positivo. Nulos/NS/NR/blancos se cuentan y excluyen conforme
al universo individual; ninguna ausencia se transforma en cero. Miembro físico
no declarado se obtiene por inventario de metadatos y FD con hash y se congela
antes del recálculo: tabla lógica no autoriza escoger entre homónimos.

Punto: p = sum_i(w_i d_i y_i) / W, W = sum_i(w_i d_i), donde d identifica el
dominio válido. W=0 devuelve NO-ESTIMABLE-UNIVERSO-VACIO. El marco conserva todas
las filas con peso/diseño válidos del archivo, aunque d=0. Si falta diseño en
alguna fila con d=1, conservar punto y devolver EE/IC nulos con causa contada.
Definir estrato h y conglomerado j por el par (h,j), no por j global. Cada UPM
fuera del dominio aporta cero; contar m_h en el marco completo.

Taylor de razón con reemplazo, sin corrección de población finita:

    Z_hj = sum_{i en (h,j)} w_i d_i (y_i-p)
    Zbar_h = sum_j Z_hj / m_h
    V(p) = sum_{h:m_h>1} [m_h/(m_h-1) * sum_j (Z_hj-Zbar_h)^2] / W^2
    EE = sqrt(V(p))
    gl = sum_{h:m_h>1}(m_h-1)
    IC95 = [max(0,p-t_0.975,gl*EE), min(1,p+t_0.975,gl*EE)]
    CV_por_ciento = 100*EE/abs(p) si p!=0; en otro caso null

t es el cuantil de Student obtenido como inversa de la CDF con gl grados de
libertad; no usar cuantiles bootstrap ni reemplazarlo por 1.96 sin enmienda.
Si gl=0 o varianza no finita, EE/IC nulos. Varianza exactamente cero se informa
como VARIANZA-DEGENERADA, con EE=0 e IC=[p,p], nunca como precisión probada.
Estrato singleton conserva masa y aporta cero a V; reportar número/masa y
rotular IC-CON-SINGLETONS. No se colapsan estratos; el intervalo ignora variación
no identificada de esas UPM, sin asegurar una cota matemática de su anchura.
Sumas float64 por orden de archivo, subtotales por estrato/UPM ordenados
lexicográficamente como texto. Contar n, n_codigo_invalido, n_peso_invalido,
n_sin_diseno, estratos, UPM, gl y singleton; no suprimir silenciosamente.

DIN-M-01-v4 usa la fila humana DIN-M-01b: join de fac_3b por folio+ls, ambos
archivos únicos por llave y cobertura completa; h=CONSTANTE, j=folio. Este es
un diseño aproximado por hogar, explícitamente distinto de la estratificación
y UPM reales ENNViH no publicadas. EE/IC quedan rotulados APROXIMADOS-HOGAR y
no acreditan incertidumbre de diseño real. Sin factor o join exacto, no estimar.

Las tolerancias históricas no se cambian aquí. La firma debe escoger este
contrato nuevo para un sucesor inferencial; el recálculo puntual del histórico
puede realizarse por separado. No comparar IC nuevos con IC históricos como
identidad algorítmica. Ningún resultado ni código productor es fuente.
