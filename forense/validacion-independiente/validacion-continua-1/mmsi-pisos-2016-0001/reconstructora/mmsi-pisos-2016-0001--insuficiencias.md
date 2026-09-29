# Insuficiencias de la spec humana · CALC-MMSI-PISOS-2016-0001

Los puntos (158 llaves) quedan fijados por la spec sin ambigüedad material. Las insuficiencias afectan al **IC95 de las 158 llaves**:

1. **Motor bootstrap no descrito en prosa.** La spec §4 remite a «Receta y motor por sha256 (los de ENDISEG, misma spec §4)», y ese material no está en el paquete. Faltan:
   - el esquema de réplica: Rao-Wu con m_h = n_h − 1 y reescalamiento, o bootstrap ingenuo con m_h = n_h. Usé Rao-Wu;
   - el orden en que se consume `PCG64(20260927)`: por bloque, por estrato y por UPM, además de la primitiva (`integers`, `choice` o `multinomial`). Por eso, aunque se use la misma semilla, las réplicas no son reproducibles bit a bit;
   - el significado de «bloques de 50». Lo leí como 40 bloques de 50 réplicas en el orden de consumo del generador;
   - la regla de percentil, es decir, la interpolación. Usé la lineal de numpy.
2. **«Contrato conservador» sin definición.** Lo leí así: no se descartan réplicas, y si alguna réplica deja el denominador en cero o la distribución es degenerada, el resultado es `NO-IDENTIFICADA`. En esta corrida ninguna llave cayó en ese caso, así que esta lectura no cambió ningún estado.
3. **`DivOcu_Act` en blanco por pase (1 372 personas no ocupadas actualmente).** La spec las deja «fuera». Eso define OCUPACION-DIRECTIVA como una proporción entre quienes tienen ocupación actual especificada, no sobre toda la población de 25 a 64 años. Seguí la spec literalmente.
4. **Tamaños chicos.** Algunos segmentos tienen n válido bajo; el mínimo es 14, en tonos extremos como A con subpoblación por sexo. La spec no fija un umbral de publicabilidad ni de estimabilidad, y no suprimí ninguna celda, como pide el encargo.
5. **Identidad de entrada.** El `sha256_entrada` indicado (`33f97f5f…`) no coincide con el sha256 de `paquete/datos/mmsi2016.csv` (`64848e9a…`). La spec §0 cita a su vez otro sha (`c37656bf…`) del zip original. Se escribió la identidad literal del encargo. No puedo verificar que el CSV del paquete sea el mismo insumo que usa la spec.
