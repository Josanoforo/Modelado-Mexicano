# Insuficiencias · RESULT-ENIGH-A-P-COMPLEMENTO

Ninguna impidió estimar ni el punto ni el IC. Faltaron las siguientes precisiones; para cada una se tomó una decisión, registrada en `diagnostico.json` → `decisiones`:

1. **Orden de suma del punto frente al del IC.** La spec del punto pide sumar «en orden fijo de llave», y la del IC pide sumar en el «orden físico» de concentradohogar. Ninguna dice si el orden de llave compara cadenas o números, ni cuál de los dos órdenes produce el punto que se publica. Decisión: el punto usa el orden lexicográfico de las cadenas (folioviv, foliohog), y las réplicas usan el orden físico. Los dos órdenes pueden dar resultados distintos en los últimos bits.
2. **Qué cuenta como «nulo».** La spec no dice cómo se ve un nulo de remesas en el CSV. Decisión: una celda vacía. Tampoco declara el trato de los valores no numéricos; aquí se tratan como fuera de mapa. En los datos no hubo ni nulos ni valores no numéricos, así que esto no cambió el resultado.
3. **Singleton y `estado_ic`.** El contrato IC pide «marcar» y no dice si el marcador obliga a usar `NO-IDENTIFICADA`. No aplicó, porque hay n_singleton = 0.
4. **Columnas de diagnóstico.** No se definen `hash_contrato`, `hash_entorno`, `n_upm_conocidos` ni el formato de `tipo_incertidumbre`. Se usaron las definiciones registradas en las decisiones.
5. **Firma subordinada a un protocolo ausente.** La firma R26 de la receta IC está «subordinada al protocolo» FP-260926-…-157c-01 (sha256 26746fee…). Ese documento no está en el paquete y no se pudo verificar. Además, «el margen de equivalencia y el control simultáneo se fijarán por mesa». El IC entregado es solo reproducción diagnóstica y no certifica una cobertura del 95 %.
6. **Payload.** El acceso firmado identifica el payload por el sha256 del zip `enigh2022_nc_csv.zip` (3b2b0bc9…). El paquete solo trae el CSV extraído (sha256 b499ac9b…), así que no se pudo verificar que el CSV salga de ese zip.
7. **`enigh-complemento-restaurado.md` sin firma registrada.** No aparece en FIRMAS-Y-ACCESO.md. Se usó como spec del punto porque así lo indica el encargo.
