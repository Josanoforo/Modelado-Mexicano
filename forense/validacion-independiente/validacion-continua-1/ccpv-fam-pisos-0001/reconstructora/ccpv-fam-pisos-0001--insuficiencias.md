# Insuficiencias de la spec humana · CALC-CCPV-FAM-PISOS-0001

Firmas (según `paquete/FIRMAS-Y-ACCESO.md`): mesa firmó `CONTRATO-v3.md` (sha256 `821a5ecb…94eb`) como contrato de estados, y firmó el acceso C1 a este paquete: la reconstructora sin historial puede leer solo las columnas que nombra la spec humana. Esa firma no adopta cifras. El protocolo inferencial se aprobó solo como contrato diagnóstico. Leí solo las columnas autorizadas del encargo. Ninguna llave necesitó una columna fuera de esa lista.

Ninguna insuficiencia impidió calcular el punto de alguna llave: las 640 están `RECONSTRUIDO`. Lo que la spec no fija sí afecta sobre todo a los **IC** (las 640 llaves):

1. **Receta del bootstrap (todas las llaves, IC).** La spec remite a `tools/dominios/salud/pisos_diseno.py` «por sha256», pero ese archivo no está en el paquete. Por eso la prosa no fija lo siguiente:
   - el esquema de remuestreo: ingenuo con n_h extracciones, o Rao-Wu con n_h−1 y reescalado;
   - el orden de los estratos y las UPM al consumir el generador;
   - cómo se extrae (`integers`, `choice`, uniformes);
   - si todas las llaves comparten las réplicas;
   - el método de percentil.

   Elegí la opción de D11 (`diagnostico.json`). Con la misma semilla, una implementación distinta da extremos distintos.
2. **«contrato conservador» (todas las llaves, IC).** No se define. Lo interpreté como D12: una réplica con denominador cero deja el IC en `NO-IDENTIFICADA`. En los datos no ocurrió en ninguna llave, así que no tuvo efecto.
3. **«certeza para UPM única».** Lo implementé como multiplicador 1 fijo. Afecta a 18 826 de los 29 113 estratos, de modo que la amplitud de los IC depende bastante de esta lectura.
4. **HOG-60MAS-Y-MENOR-18 (46 llaves).** La spec dice «ídem» para el universo de HOG-CON-MENOR-18, pero para la condición conjunta no dice cuál es. Usé D2: se observan ambos, o todas las edades son conocidas.
5. **Ejes del jefe con atributo inválido** (EDAD-JEFE, ESCOLARIDAD-JEFE, SEXO-JEFE). La spec solo dice qué pasa con 0 o más de 1 jefe. No dice qué hacer con edad 999 o NIVACAD 99/vacío del jefe. Los excluí del eje (D8).
6. **PER60-VIVE-SOLO, «su total expandido (Σ factor, sin IC)».** El esquema no tiene llave para ese total. Lo dejé solo en `diagnostico.json` (D10).
7. **Lectura de `.dta`.** El encargo pide `pandas.read_stata`, pero `viv_15.dta` y `per_15.dta` están en formato Stata 110, que pandas no soporta. Los leí con `pyreadstat` desde `paquete/lib`, con `usecols` limitado a las columnas autorizadas (D14).
