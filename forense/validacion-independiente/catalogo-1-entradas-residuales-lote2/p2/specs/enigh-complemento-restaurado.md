# ENIGH 2022 · hogares sin remesas · entrada humana sucesora

Estado: RESTAURACION-DE-ENTREGA. Fuente humana sellada de 15/sep/2026 §1.3 y §2.1–2.2. No crea contrato ni adopción.

Identidad: `RESULT-ENIGH-A-P-COMPLEMENTO`; celda `A-P-COMPLEMENTO`; conducta `no_recibe_remesas`; unidad HOGAR; segmento TOTAL; proporción [0,1].

Payload enigh2022_nc_csv, tabla concentradohogar Nueva Serie. Llave única folioviv+foliohog. Universo completo de hogares, sin selección por recepción de remesas. Usar factor finito y >0 y remesas no nula. Nulos de remesas causan NO-ESTIMABLE-NULOS-INESPERADOS; nunca sustituirlos por cero. est_dis y upm son llaves textuales opacas y han de estar presentes en cada fila válida.

Definir d=1 si remesas>0; d=0 si remesas==0. A-P-COMPLEMENTO se cuenta directamente: Σ(factor · 1[d=0])/Σ(factor), sumas en orden fijo de llave. Remesas negativa no tiene categoría declarada: parar como NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA, sin incluirla como no recepción. El complemento no se obtiene restando una cifra publicada. Verificar cierre de las categorías sobre el mismo universo; no ocultar filas fuera de mapa usando 1-p.

Salida comparada: documento y filas exactamente según `esquema-salida-v2.md` del contenedor; `llave` y `unidad` se copian literalmente de `esquema-identidades.tsv`, `punto` contiene la proporción reconstruida y `estado_ic=SIN-IC` si no se calcula intervalo. Celda A-P-COMPLEMENTO, segmento TOTAL, unidad de observación HOGAR, n válido, peso denominador y exclusiones son metadatos auxiliares separados de la salida comparada. IC solo bajo contrato P3. No contiene referencias ni tolerancias nuevas.
