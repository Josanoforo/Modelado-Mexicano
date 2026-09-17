# Archivo de encargo · GEN2-ENCRIGE-CARGA-INTENSIDAD-1

**SHA de redacción:** `e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5` (`origin/main`).
**Entorno asignado:** Codex CLI, repo-only; no microdatos ni descargas.
**Estado:** `VIVO`.
**Procedencia:** archivo entregado por Jonás al lanzar la sesión el 16/sep/2026
en America/Mexico_City; el propio texto fue emitido 17/sep/2026 UTC.
**Consumo:** pendiente de la ejecución y PR de este acto.

## VERIFICACIÓN DE EXISTENCIA

- Estructura: no existían rama, worktree ni PR del rótulo tras actualizar
  `origin/main`.
- Contenido: el producto exacto no estaba en `main`; sí estaba el padre
  sellado `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`.
- Cobertura retroactiva: no aplica; ésta es la primera ejecución del derivado.

## Texto verbatim del lanzamiento

<!-- INICIO TEXTO VERBATIM -->

# ENCARGO · GEN2-ENCRIGE-CARGA-INTENSIDAD-1

**Entorno:** Codex CLI o Claude Cloud; repo-only.  
**Producto:** análisis reproducible que separe alcance de la corrupción, intensidad entre empresas afectadas y concentración del volumen por tamaño, usando la extracción oficial ya sellada de ENCRIGE 2020. No abre microdatos ni vuelve a descargar tabulados.

## 1. Pregunta que aporta algo nuevo

El resultado fusionado en #826 ya describe prevalencia e incidencia por tamaño. Este encargo responde: **¿las diferencias de incidencia se deben aritméticamente a la fracción de empresas afectadas o al número de trámites/inspecciones con corrupción entre ellas, y dónde se concentra cada volumen?**

Es una descomposición descriptiva, no causal. «Intensidad» aquí significa el cociente del recuento que publica INEGI entre empresas afectadas del mismo universo; no reincidencia temporal, riesgo por interacción, dinero perdido ni número de actos por persona. No llamar frecuencia longitudinal a datos transversales.

Insumos existentes:

- `forense/analisis/encrige-descriptiva-1/encrige-corrupcion-por-tamano.csv`.
- `forense/analisis/encrige-descriptiva-1/lectura-TRA.md` y `forense/notas/2026-09-16-GEN2-ENCRIGE-DESCRIPTIVA-1-cierre.md`.
- `data/corrida0/CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001/`: spec, medidor, resultados y sellos, sólo lectura.
- F-19/NC-0233 y fila R08 del panel: uso descriptivo empresarial admitido; no transferencia al motor de personas.

El CSV contiene cinco dominios y dos indicadores, con numeradores/denominadores expandidos. No son tamaños muestrales. No contiene IC/EE/CV utilizables; la derivación no puede crearlos. La proporción de microempresas afectadas ya se discutió: no presentar ese dato previo como hallazgo nuevo. El aporte principal es intensidad, participación en el volumen de trámites/inspecciones y descomposición.

## 2. Contrato previo de la derivación

Antes del cálculo derivado, escribir y comprometer una spec breve con identidades del padre, hashes y fórmulas. Declarar que los puntos originales ya fueron observados y que se trata de análisis exploratorio de resultados publicados, no preregistro ciego.

Para cada dominio s —nacional, Micro, Pequeña, Mediana y Grande— definir:

- `N_s`: unidades económicas expuestas a al menos un trámite/inspección, denominador expandido.
- `A_s`: unidades que experimentaron al menos un acto, numerador de prevalencia.
- `T_s`: recuento expandido de trámites/inspecciones con experiencia de corrupción, numerador de incidencia según la definición acreditada del padre.
- `p_s = A_s / N_s`: proporción de empresas expuestas afectadas.
- `m_s = T_s / N_s`: trámites/inspecciones con corrupción por empresa expuesta.
- `r_s = T_s / A_s`: trámites/inspecciones con corrupción por empresa afectada.
- Identidad: `m_s = p_s * r_s`.

Antes de unir las dos filas de indicador, confirmar mismo dominio, unidad empresarial, periodo y denominador, y que T cuenta exactamente lo declarado. Si la documentación disponible no permite interpretar T/A así, no cambiarle el nombre al numerador para salvar la fórmula: entregar las participaciones que sí se sostienen y el impedimento preciso del cociente. La identidad algebraica sola no acredita equivalencia de universos.

Usar los absolutos publicados de máxima precisión y contrastar con las tasas oficiales; no derivar desde porcentajes redondeados a dos decimales. Declarar tolerancia según el redondeo que viaja en el CSV padre; no exigir identidad de precisión inexistente ni aflojarla después de ver una discrepancia.

Para los cuatro tamaños, sin incluir el total nacional como quinta parte:

- participación en exposición `N_s / ΣN_s`;
- participación en empresas afectadas `A_s / ΣA_s`;
- participación en trámites/inspecciones con corrupción `T_s / ΣT_s`.

Contrastar cada suma con el nacional del padre. Si no reconstruye por redondeo dentro de tolerancia, reportar residuo y no forzar la suma a uno contra una partición falsa. No sumar tasas ni promediarlas sin masas. No imponer que r o m estén entre cero y uno: son razones de recuentos.

### Diferencias de intensidad por tamaño

Referencia fija: Micro, por ser la categoría mayoritaria del universo ya documentado. Para Pequeña, Mediana y Grande, descomponer la diferencia de incidencia frente a Micro mediante:

`m_s - m_micro = 0.5*(p_s - p_micro)*(r_s + r_micro) + 0.5*(r_s - r_micro)*(p_s + p_micro)`.

Primer término: contribución aritmética asociada a prevalencia. Segundo: contribución aritmética asociada a intensidad condicional. La forma simétrica evita depender del orden de sustitución. Reportar términos en trámites/inspecciones por empresa expuesta, no en puntos porcentuales; p sí admite diferencias en pp. Si la diferencia total es casi cero, no dividir cada término por ella para fabricar porcentajes enormes. No denominar «efecto del tamaño» a ninguno de los términos.

No derivar por sector, estado ni año: esos insumos no están dentro de este encargo. Tampoco estimar probabilidad por trámite sin un denominador de todas las interacciones.

## 3. Implementación y producto

1. Verificar la identidad del CSV padre frente a su CALC/sello con el mecanismo disponible, sin relanzar el medidor que necesita corpus. Si falta vínculo suficiente, consignar la copia exacta usada y su SHA; no inventar que está sellada. No modificar el padre para subsanarlo.
2. Escribir script pequeño propio que lea sólo el CSV autorizado y produzca la tabla ampliada, tabla de participaciones y tres contrastes. Preferir Decimal o precisión suficiente para preservar el grano publicado; ninguna estadística de respondentes.
3. Comprometer especificación/código y ejecutar la derivación. Si el contrato del programa requiere CALC para este resultado, usar un **CALC derivado nuevo**, sugerido `CALC-ENCRIGE-CARGA-INTENSIDAD-0001`, con origen del padre declarado y sin afirmar que sea fuente o medición independiente. No tocar el runner compartido ni aumentar un contador científico por la nueva envoltura.
4. Crear una figura exportable SVG/PNG con participaciones por tamaño para exposición, empresas afectadas y recuento de trámites/inspecciones; etiquetas de denominador completas y colores consistentes. Herramientas estándar de gráficos, sin imágenes generativas. No dibujar bandas de incertidumbre inventadas ni tamaños de muestra a partir de masas expandidas.
5. Entregar lectura de máximo dos páginas: qué domina la incidencia en cada contraste, cómo cambia la prioridad descriptiva según se mire prevalencia o volumen, y qué observación adicional permitiría distinguir explicaciones. Comparar sólo dentro de ENCRIGE; WBES está en otra sesión y no se usa aunque termine durante el encargo.

Toda la salida conserva: universo empresarial cubierto por ENCRIGE, exposición a trámites/inspecciones, periodo enero–entrevista 2020, cortes oficiales de tamaño y ausencia de incertidumbre muestral. No declarar significancia, causalidad, tendencia ni intervención óptima. Se admite priorizar preguntas descriptivas; no recomendar una asignación de recursos basada en un supuesto efecto causal.

## 4. Verificación proporcional

Comprobar: denominadores compatibles; suma por tamaños frente al nacional; `m=p*r`; suma de ambos términos igual a la diferencia; separación porcentaje/razón; ausencia de total nacional duplicado en las partes. Casos sintéticos mínimos: A=0 (intensidad no estimable, nunca infinito o cero imputado), denominadores incompatibles y razón mayor que uno válida. No añadir una batería general.

La igualdad T>=A, si procede de las definiciones acreditadas, es una guarda semántica; si falla no recortar a A ni esconderlo como redondeo sin comprobarlo. Una corrida real y estas comprobaciones bastan. No bootstrapping de cinco dominios ni tratar dos estimaciones de la misma encuesta como independientes.

## 5. Perímetro y terminado

Permitidos:

- `forense/analisis/encrige-carga-intensidad-1/`: spec, tablas, figura, lectura y recibo de reproducción.
- `tools/encrige_carga_intensidad.py` y prueba focal propia si hace falta.
- CALC derivado nuevo si corresponde al contrato vigente; encargo y cierre propios.

No editar `forense/analisis/encrige-descriptiva-1/`, CALC padre, WBES, manifiesto, `tools/corrida0.py`, `tools/relevo_usos.py`, F6 ni informe compartido. La lectura queda lista para incorporación serial a TRA.

Cierre pleno: un comando reproduce tablas/figura y la lectura responde la pregunta con las limitaciones correctas. Un resultado derivado no aumenta el número de instrumentos ni constituye una validación adicional del motor. Si no es posible r por semántica, terminar con participaciones verificadas, límites y el único documento requerido; no ampliar a adquisición.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. WBES2023-DESCRIPTIVA-1, ENCO-DOS-OLAS-RESERVADAS-1 y L8-LINAJE-HEREDADO-1 están corriendo por indicación de Jonás. L8 conserva tools/corrida0.py; ENCO sus nuevas entradas de manifiesto y reserva; WBES su CALC y análisis. ENCIG2023-AGREGADO-CONDICIONAL-1 (#831) y ENVIPE-RES0028-DERIVADO-U4-1 (#830) ya están integrados en este corte: reutilizar sus resultados sin repetirlos. F6 mantiene su preparación y reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. La única excepción adicional en esta tanda es la vista derivada de relevos para F-3, delimitada en su propio perímetro. No autoriza registro global ni ediciones de manifiesto.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.


## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-ENCRIGE-CARGA-INTENSIDAD-1 en CLI o Claude Cloud. Autorizo la derivación descriptiva desde el resultado ENCRIGE ya publicado: spec, código, tablas, figura, lectura y CALC derivado si el contrato vigente lo requiere; pruebas, commits, push y PR; fusión conmigo. No abras microdatos, descargues fuentes, repitas el padre, consultes el resultado WBES en curso ni generes adopciones. Aplica cascada diferida. Separa prevalencia, intensidad por empresa afectada y volumen, sin inferencia causal o IC inventado. Si esta sesión proviene de una rama fusionada, conserva su trabajo y abre la sucesora desde origin/main. Entrega el análisis reproducible y una explicación útil para TRA.

<!-- FIN TEXTO VERBATIM -->

