# Diferencias del intento previo: preservación e interpretación documental

LEÍDO: dictámenes de #1202 en main, consultados como evidencia de auditoría. Ninguna de estas diferencias se entrega dentro de la entrada de futuro reconstructor. No se ejecutó recálculo.

| Componente | Llave exacta | Delta(s) independiente − referencia | Interpretación |
|---|---|---|---|
| ic | RESULT-ENCIG-MOR-A-P-SOL1 | ic95_inf=2.2548472403544073e-05; ic95_sup=0.00028201640558039864 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENCIG-MOR-B-P-DIG-SD | ic95_inf=0.0003755896244522633; ic95_sup=0.00035580980972746423 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENCIG-MOR-B-P-PRE-SD | ic95_inf=0.001340742151319227; ic95_sup=0.001859646493104522 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENCIG-MOR-C-P-ADOPTA | ic95_inf=-0.0005874286176904553; ic95_sup=-0.0011313535518204798 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENCUCI-A-P-CUALQUIERA | ic95_inf=0.000490901397377827; ic95_sup=3.369146371812182e-05 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENCUCI-B-P-URB-AGR | ic95_inf=0.00027250519571178633; ic95_sup=-0.0003155711899374969 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| ic | RESULT-ENFIH-A-P | ic95_inf=-0.0002407648423421449; ic95_sup=-0.00015779034769713984 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |
| punto | RESULT-ENIGH20-REMINT-PARTICIPACION-AGREGADA | punto=-4.440892098500626e-16 | Diferencia aritmética bajo tolerancia histórica cero; no prueba cambio de estimando. No se modifica la tolerancia. |
| punto | RESULT-ENIGH20-REMINT-REMESAS-MEDIA | punto=-1.8189894035458565e-12 | Diferencia aritmética bajo tolerancia histórica cero; no prueba cambio de estimando. No se modifica la tolerancia. |
| ic | RESULT-ENVIPE-DEN-P-C2-U4 | ic95_inf=-0.0006113455077487173; ic95_sup=-0.00017391955637335865 | La documentación metodológica permite evaluar inferencia; no identifica necesariamente realización RNG histórica. La diferencia conserva DISCREPA; contrato sucesor no la borra. |

EJECUTADO: preservadas las dos diferencias de punto y ocho de IC, con sus deltas, tolerancias e identidad/hash de cada dictamen en `../p1/discrepancias-previas-preservadas.tsv`. No se reclasifica el intento previo. Un eventual nuevo intento se registra con identidad y resultado propios.

PROPUESTO: evaluar por separado coincidencia bajo la tolerancia histórica, validez inferencial y posible contrato sucesor. La firma de un contrato nuevo no equivale a concordancia retrospectiva.
