# ENCIG-MORDIDA · Ratificación sucesora del método de IC

### `prereg-caja-ENCIG-MORDIDA` · **v1.1** · 9 de septiembre de 2026

**Acto de origen:** `ACTO GEN2-MOTOR-SEMANTICA · D3` · firma de mesa · `NC-0112`
**Base inmutable:** `forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`,
`sha256 00c7c4a67a4a579fff8a64c01979deefe2d458c75cfbaa630de21fa05d37cf8a`
**Separación histórica:** `ACTO GEN2-CORRIDA0-REPLAY-CASCADA`, 10/sep/2026,
traslada a este archivo la ratificación que `be9b0c0` había añadido in situ a
la v1.0. No cambia el contenido normativo de la ratificación; restaura la
identidad del input sellado de `CALC-ENCIG-0001`.

---

## 8 · Enmienda fechada — 9/sep/2026

La v1.0 (§0–7) queda intacta. Esta sucesora no la reescribe: la complementa.

Mesa RATIFICA el método de IC declarado en §3.7 de la v1.0 (bootstrap de
`UPM_DIS` con reemplazo dentro de `EST_DIS`, conservando el número de UPM por
estrato, percentiles 2.5/97.5, 2 000 réplicas, `numpy.PCG64`, semilla
`20260909`) como **ESTÁNDAR PRE-REGISTRADO DE LA FAMILIA** para toda ranura
sin método propio. §3.7 declaraba esto como elegido por el ejecutor sobre
ranura vacía y elevado a mesa («nadie pre-registró el método de IC para estas
series»); esta enmienda cierra esa elevación: de aquí en adelante, una ranura
de esta familia sin método de IC pre-registrado hereda el de §3.7 sin
necesidad de que el ejecutor lo elija de nuevo. Cierra `NC-0112`.

No había plantilla de spec en `forense/prereg-caja/` a la fecha de la
ratificación (censada: ningún archivo `*plantilla*`/`*template*` en el
directorio). La línea que futuras specs heredarían, en vez de elegirse al
vuelo, queda pendiente hasta que exista una plantilla donde escribirla.
