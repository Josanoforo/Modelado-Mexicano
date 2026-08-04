# Declaración de fuente · `R4.3` (mitad A + mitad B) · Encargo Z, commit 1

*(Escrita antes de abrir un solo ZIP de microdato. Ficha compuesta — la regla del perímetro exige un falsador por mitad; esta declaración cubre ambas, y §3(c) del encargo exige que se corran y archiven por separado más adelante. Advertencia de la propia ficha, línea 130, incorporada aquí antes de correr nada: "familia cuidadora" co-varía con corresidencia, que co-varía con ingreso — sin control socioeconómico se mediría pobreza compartida, no G5.)*

## Candidatas del catálogo — todas, con la razón de la elección

Dominio: **SAL**, con componente de adherencia terapéutica y estructura del hogar.

| Candidata | Cubre el dominio | Por qué se descarta o se elige |
|---|---|---|
| **ENSANUT CONTINUA 2024** | Sí — módulos de enfermedades crónicas (Diabetes, Hipertensión) en el Cuestionario de Adultos, con preguntas dedicadas de suspensión de tratamiento y motivo | **Elegida**, única candidata con variable de motivo de interrupción que distingue desabasto de otras causas. |
| ENIGH | Parcial (SAL, gasto en medicamentos) | Descartada: mide gasto, no continuidad de tratamiento ni motivo de interrupción. |
| ENASEM/MHAS | Parcial (SAL 50+, panel) | Descartada por edad para mitad A (población general); podría cubrir mitad B en la subpoblación 50+, pero no se identifica variable de "cuidadora presente + medicamento surtido" en su cuestionario — no verificado a nivel de variable, no promovida sin abrir su instrumento. |

## La elegida, contra el Umbral concreto de cada mitad

**Fuente elegida: ENSANUT CONTINUA 2024**, Cuestionario de Adultos, secciones III (Diabetes Mellitus) y IV (Hipertensión Arterial). Verificado por lectura directa de `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` (raíz `descargas_mx`).

**Mitad A — Umbral (línea 127):** "Caída de adherencia <15% ante un episodio de desabasto documentado ≥3 meses."
- `A0313` ("¿ha suspendido algún medicamento más de una vez a la semana en los últimos 6 meses?") da la variable de conducta (abandono/intermitencia).
- `A0313a` da la duración de la suspensión, en 4 categorías: 1 día, 2-6 días, 1-3 semanas, **"1 mes o más"** (categoría abierta, sin desagregar).
- `A0314` da la causa, con tres categorías que son desabasto en sentido estricto: "05 No le surtieron los medicamentos en la unidad médica", "06 No encontró el medicamento en la farmacia", "10 Se le terminó el medicamento antes de surtir su siguiente receta" — distinguibles de causas no estructurales (olvido, miedo a efectos secundarios, falta de dinero).

**Mitad B — Umbral (línea 128):** "Diferencia <10 puntos, controlando gravedad y nivel socioeconómico, entre pacientes con cuidadora presente + medicamento surtido vs. sin cuidadora."
- No se encontró variable de "cuidadora" o "persona a cargo del cuidado" en el Cuestionario de Adultos ni en el roster del Hogar (`grep -i "cuidad\|parentesco\|corresiden"` — solo aparece `parentesco` genérico del roster, y una mención de "cuidadora" como informante-proxy de un menor, sin relación con adherencia de un adulto).
- El único proxy disponible para "familia cuidadora" es **corresidencia** (derivable del roster de hogar) — exactamente el proxy que la propia ficha, línea 130, advierte que confunde estructura con pobreza compartida.

## Qué condición del Umbral no está cubierta

**Ambas mitades comparten el mismo obstáculo, por el mismo motivo:** la escala propia de la ficha declara, columna `D` (línea 132): **"si solo hay adherencia auto-reportada"**. La única variable de adherencia disponible en ENSANUT — o en cualquier otra candidata del catálogo revisada — es `A0313`, un recuento de suspensión por entrevista (recuerdo del último semestre). No existe en el catálogo una medida de adherencia por surtimiento (registro de farmacia/receta electrónica), que es exactamente lo que la columna `C` de la ficha (línea 132) describe como lo que haría falta: "exigiría cohorte con adherencia medida por surtimiento, no auto-reporte". Esto no es específico de una mitad — aplica a las dos, porque ambas miden adherencia con la misma variable.

Adicionalmente, específico de cada mitad:
- **Mitad A:** la duración del desabasto tiene un techo abierto en "1 mes o más" — no permite aislar el episodio ≥3 meses exacto que el Umbral pide; solo permite un umbral más laxo (≥1 mes).
- **Mitad B:** no existe variable de cuidadora en absoluto (más allá del proxy de corresidencia, ya señalado como confundido por la propia ficha).

## Variables exactas, universo, ponderador, estrato, UPM

- Tabla: `adultos_ensanut2024_w` (secciones III/IV), roster `integrantes_ensanut2024_w_ICB` para el proxy de corresidencia; raíz `descargas_mx`.
- Universo previsto: adultos con diagnóstico médico de diabetes (`3.1`/`A0301` área) o hipertensión (sección IV) que además reportan tratamiento farmacológico activo.
- Mitad A: numerador `A0313`=Sí ∧ `A0314`∈{05,06,10} (suspensión por desabasto); denominador todos los que iniciaron tratamiento farmacológico.
- Mitad B: numerador/denominador requerirían el proxy de corresidencia (roster) cruzado con `A0313`=No (adherencia sostenida) — no operacionalizable sin el confusor declarado.
- Diseño muestral: ponderador `ponde_f`, estrato `estrato`/`est_sel`, UPM `upm` (misma convención que Nota 17).

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta**, para cada mitad por separado.
