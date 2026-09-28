# Revisión dirigida de ASTRA6 tanda 4 · 27/sep/2026

Este dictamen recibe evidencia para revisión de mesa. No fusiona, adopta ni autoriza reconstrucciones ciegas.

| Entrega | Corte de producto revisado | Disposición |
|---|---|---|
| Entradas residuales · #1229 | `0f2196d121e66d8e26bf7375274f8d493af5aa09` | Favorable para recepción documental. Firmar contratos nuevos por cohorte y hash antes de recálculo. |
| Aislamiento y adaptador · #1221 | `509033837f8e6e4429d7fd7fe118051f9fc57284` | Recibible como producto portable con la corrección de prueba TAR de esta rama. Mantener `NO-LANZAR-COMO-CIEGA` en esta caja. |
| ENOE inferencia · #1222 | `8b029563fb2e9c768c11b768a6bec651df21160a` | Favorable como diagnóstico `NO-LANZAR-TODAVIA`; resolver incertidumbre de diseño antes de cifras. |

**Entradas residuales.** La revisión dirigida contó 368 componentes y 312 identidades. El verificador P4 pasó con cuatro contenedores, 40 miembros y bytes reproducibles; 49 hashes comprobados sin discrepancias. No se detectó defecto material. El aviso de `diff --check` procede de la línea final de un brief archivado íntegramente: no se deben reescribir sus bytes. El HEAD de #1229 posterior al corte revisado cambió asientos de cierre y hashes, no el producto P1/P4.

**Aislamiento.** Pasaron siete pruebas dirigidas y el verificador de entrega de 30 objetos. La implementación rechazó recorrido de directorios, enlaces y nombres duplicados con una allowlist válida. La prueba original `test_dangerous_archive_members` pasaba una allowlist vacía y fallaba antes de inspeccionar los miembros del TAR. Esta rama corrige esa cobertura, ejecuta los tres subcasos y actualiza el hash del test en el manifiesto. El aislamiento real de esta caja sigue sin acreditar canarios interiores ni sesión nueva, por lo que no hay permiso de lanzamiento ciego. Los commits posteriores de #1221 añadieron asientos de cierre e integraron `main`; no modificaron esa prueba.

**ENOE.** Los 39 singleton aparecen en el marco completo y son compartidos por ambos grupos; el filtro no los crea. La potencia exige ambos grupos y seis escenarios, deja las métricas `null` y conserva p0 histórico. Pasaron cinco casos sintéticos, cinco pruebas del sucesor y seis regresiones; 17 hashes sin discrepancia. Falta tratamiento oficial de singleton, certeza y réplicas, y aclarar el significado de UPM repetidas entre estratos. El HEAD posterior de #1222 solo actualizó el acta de ejecución.

**Límites.** No se repitió lectura de microdato ni descarga documental, suite general, replay de todos los sidecars o inspección exhaustiva de PDF. #1220 de derivados se deja al circuito automático. La sonda de acceso a INEGI respondió HTTP 200 fuera del sandbox.
