# HITO D · `R10.1` — codificación 1, SELLADA por hash antes de existir la codificación 2

### `hitoD-R10.1-codificacion1-v2_1` · Fase A de `ACTO CORRE-R10.1-v2` · 25 de agosto de 2026 · ENTORNO UBUNTU

> | | |
> |---|---|
> | **QUÉ ES** | El compromiso criptográfico de la codificación del **codificador 1** (el ejecutor de este acto) sobre las 12 unidades, bajo el esquema `§2` de `hitoD-R10.1-spec-v2_0-propuesta` (SELLADA, `FP-128`). Se sella **antes** de que exista la codificación del segundo codificador. |
> | **QUÉ NO ES** | **CONTADOR: cero.** No calcula ninguna tasa, ningún `κ`, ningún IC, y no propone fila alguna de la escala `§6`. No adjudica `R10.1`. No toca el bloque append-only del preregistro ni los tres documentos `v1` de `R10.1`. |
> | **VERIFICAS ASÍ** | en la Fase B se revela el texto en claro y su `sha256` debe coincidir, dígito por dígito, con el que esta ficha commitea hoy. |

**el primer resultado que produzca este procedimiento es el que se reporta**

---

## 1 · Los sellos

| objeto | `sha256` |
|---|---|
| **tabla canónica de los 12 códigos** (`unidad · contexto · nivel1 · nivel2`, TSV) | `dae1048de7e4a04ac8ece168dc3d8f0f6fde64e28675069e9716c4fced33ec90` |
| **razonamiento unidad por unidad** (texto en claro con la tabla y sus motivos) | `c380f81e1b8705d80c68b9a08085e715c5ff1dc00cc75ac7226661979b2605d2` |
| **paquete entregado al codificador 2** (`forense/hitoD-R10_1-paquete-codificador2.md`) | `15e1a594473dc8c49f882fe4e879fde678507a6771332bd1b96c4c45f1fda1bd` |
| **material de origen** (`forense/notas/2026-08-20-r10-1-rechazo-poder-salida.txt`) | `c5d39e81f397675047acbba606b9eba07f5b064f93404e2ba63d177adb9ca59d` |

**Dónde vive el texto en claro, y por qué ahí.** `/home/pc0/mm-corre-r10-1-SELLO/`, **fuera del
repositorio**, dos archivos: `codificacion1-codigos.tsv` y `codificacion1-PLANTEXTO.md`.

El encargo autoriza commitear *"sus 12 códigos **(o su sha256)**"*. Se elige el `sha256` porque
el propósito de A1 es **comprometer**, no **publicar**: el segundo codificador es una persona
con acceso plausible a este repositorio, y publicar los códigos en claro durante el interludio
abriría un canal de contaminación que anularía el `κ` —es decir, anularía justo la pieza que
este acto existe para construir—. El hash compromete con la misma fuerza y sin ese canal.

**Riesgo residual, declarado.** Si esos dos archivos se perdieran antes de la Fase B, la
recuperación honesta **no** es re-codificar (eso sería codificar ya sabiendo lo del otro, el
defecto exacto que `§3.2` documenta): sería declarar la pérdida y re-correr la Fase A completa
con una codificación 1 nueva, sellada de nuevo, antes de recibir la tabla ajena.

---

## 2 · Método, declarado en fresco

- **Esquema:** `§2` de la spec SELLADA, reglas `2.1` a `2.5`, sin añadidos. `2.4` (negaciones que
  no son la cabeza) y `2.5` (interacciones sin rechazo consumado) se aplicaron unidad por unidad,
  no como excepción de última hora.
- **Unidades:** 12, en orden de archivo, `U01`…`U12`. Se usan identificadores propios porque la
  numeración del corpus **colisiona** —el escenario `Rechazos 3-4` rotula sus dos transcripciones
  como `Rechazo 1` y `Rechazo 2`, los mismos rótulos que el escenario `Rechazos 1-2`—. Reparto por
  brazo: `+P` = `U01`–`U06`, `−P` = `U07`–`U12`, seis y seis.
- **Nivel 1:** `DIRECTO` · `INDIRECTO` · `NO-RECHAZO`. **Nivel 2:** `DIRECTO` · `EXCUSA` ·
  `APLAZAMIENTO` · `ALTERNATIVA` · `EVASION` · `NO-RECHAZO`.
- **Cuatro casos limítrofes** quedaron identificados y razonados por escrito en el texto sellado,
  nombrados como candidatos a discrepancia **antes** de ver la codificación ajena.

---

## 3 · Asimetría entre los dos codificadores, declarada y no disimulada

El **codificador 2 es ciego**; el **codificador 1 no lo es**. El material de origen trae, en el
mismo archivo, la codificación `v1` y su resultado, y no hay manera de leer las transcripciones
sin verlos. Esta asimetría es exactamente la que `§3.2` de la spec describe al explicar por qué
un codificador único que ya vio el resultado no puede recodificar solo — y es la razón de ser de
la Pieza 2. Se declara aquí, en la ficha, para que viaje pegada al `κ` que se reporte.

---

## 4 · `U10` viene pre-decidida por el propio esquema — instrucción pre-registrada para la Fase B

La regla `2.5` nombra `Rechazo 10` como su caso documentado, con su cita de cierre. El esquema va
**verbatim** en el paquete, tal como el encargo ordena; por tanto esa unidad llega **pre-decidida
para los dos codificadores**, y su acuerdo no es evidencia de acuerdo.

**La Fase B reportará `κ` dos veces:** sobre las **12** —la cifra del gate, tal como `§3.4` la
define— y sobre las **11** restantes, como diagnóstico honesto que **no** es gate. Si ambas caen
del mismo lado de `0.60`, la distinción no cambia nada. Si caen de lados distintos, manda la de
12 por spec, y la de 11 viaja escrita como reserva del veredicto.

Esto se pre-registra **hoy**, en la Fase A, sin conocer ninguna de las dos codificaciones ajenas
ni ninguna tasa.

---

## 5 · Qué falta para la Fase B

La tabla de 12 códigos de **Jonatan Guadarrama**, designado segundo codificador por mesa en el
lanzamiento del 25/ago/2026, con su declaración de no haber leído
`hitoD-R10_1-especificacion-v1_0.md`, `hitoD-R10_1-veredicto-v1_0.md` ni
`hitoD-R10_1-defecto-spec-v1_0.md`. Se ingesta verbatim, con su `sha256` en el commit, y solo
entonces se calcula `κ`.
