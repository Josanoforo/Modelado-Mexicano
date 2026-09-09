ENCARGO · ACTO GEN2-CIERRES-CON-CITA · OCHO FILAS QUE YA SE GANARON SU CIERRE Y NADIE ASENTÓ — cada una con su evidencia enfrente, cero trabajo nuevo
Cabecera: NUBE, Sonnet (cierres registrales con cita; cero juicio de contenido) · COMPUERTA: ninguna · redactado contra `origin/main = 8b9f9d49` (PR #646) · candidatos: deriva con `cierre_acto.py`, no heredes (PRIMERA-SILLA y PILOTO pueden renumerar en paralelo). CONCURRENCIA: PRIMERA-SILLA toca `tools/`+`data/corrida0/` — disjunto; si toca `no-corrido.tsv` primero, re-deriva y sigue.
FIRMA DE MESA, verbatim del 8/sep/2026: «dame el encargo de cierres» — sobre el barrido de dirección de esta tarde (derivado de las cinco superficies, no de memoria).
REGLA DEL ACTO: cada cierre lleva su cita verificada por el ejecutor en esta sesión (comando pegado) — si alguna evidencia no reproduce contra tu main, esa fila NO se cierra y se reporta como hallazgo (A.8: encontrar que la premisa del encargo falla es entregable). Vocabulario A.16: el token va en el campo, la historia en la glosa.
LAS OCHO, con la evidencia que el ejecutor re-verifica:

1. NC-0037 (las 10 filas vivas del cruce FP-286/343) → CERRADA. Cita: las diez quedaron resueltas por firmas de mesa Grupo A/B/C del 8/sep propagadas en PR #630 (cierres+estampa), #639 (ENAFIN cerrado con dato del corpus; tandas clasificado), #643 (timbre preparado, CIDE declinada, CNBV diferida). Verificar: los estados en la cola de adquisición.
2. NC-0002 (retrofit V1, veredicto por fila) → CERRADA. Cita: FP-343 llegó a su desglose final (18+6 cerradas, vivas resueltas en la fila 1 de arriba) — `grep FP-343 forense/firmas-pendientes.tsv` muestra su token final.
3. NC-0017 (E7.C3, raíz inyectable) → CERRADA. Cita: su sucesora FP-346 está FIRMADA desde T9 — pegar la fila.
4. NC-0035 (convención de nombre de rama de T11) → CERRADA. Cita: mesa la aceptó al fusionar PR #624/#628 — el merge es la firma; ninguna objeción registrada desde.
5. NC-0036 (fusión de la nota revisa-619 / PR #621) → verificar y cerrar. La rama `claude/revisa-post-hoc-619` ya NO existe en el remoto (`git ls-remote`). Determinar con `git log --all --grep="revisa-post-hoc-619"` o el historial de merges si la nota entró (¿#62X?) o si el PR se cerró sin fusionar; cerrar la fila con lo que el árbol diga — CERRADA-FUSIONADA o CERRADA-DESISTIDA, con cita. Si no es determinable desde aquí, la fila queda con esa palabra y el comando, no se adivina.
6. NC-0055 (tablero: relanzamiento con adjunto) → CERRADA. Cita: el relanzamiento ocurrió y fusionó como PR #638 (`4f26fb92`); B1 aterrizó — `grep -c '#633' forense/tablero/TABLERO-PROGRAMA.md ≥ 1`.
7. Estado rancio del encargo E5-0 → `forense/encargos/cola/2026-09-07-GEN2-E5-0-SPECS-EJECUTABLES.md` dice `EN-EJECUCIÓN`; fusionó como PR #629 esta mañana. Token → `CONSUMIDO — PR #629`, bitácora con fecha.
8. PILOTO-CAJA sin línea de estado → `2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md` no trae `ESTADO:`; añadirla — `GATEADO` ya-cumplido o `LISTO-CAJA` según su compuerta re-derivada (SONDA-3 fusionó como #642), para que `/despacha` lo vea.

PERÍMETRO: `forense/no-corrido.tsv` (tokens de las filas 1-6) · `forense/encargos/cola/` (líneas de estado 7-8) · `forense/hallazgos.md` (una línea: «ocho cierres con cita; la deuda de cierre se barre, no se acumula») · nota corta · 0-bis · cascada. No toca firmas-pendientes (ninguna FP cierra aquí — las seis abiertas son frescas y de otros actos), ni tools, ni data. Si escribes fuera, PARA. CONTADOR: cero GEN2 — trámite declarado. Lo que mueve: el tablero de pendientes vuelve a decir solo la verdad, y `no_corrido_abiertas` baja ~6 — señal menos ruidosa para el WARN diario. `## NO-CORRIDO / RESERVAS` obligatoria: «Ninguno.» esperado — o la fila que no reprodujo, que vale más.

## NO-CORRIDO / RESERVAS

- **qué:** Fila 1 (`NC-0037` → CERRADA), verbatim del encargo.
  **por qué:** `PARO-PREMISA` — 9 de las 10 filas VIVAS del cruce FP-286/343 sí avanzaron (6 cerradas por Grupo A, `PI` diferido con sucesor, `ENAFIN` `OBTENIDO-PARCIAL`/EXISTE-SATISFACE, `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` `SOLICITUD-PREPARADA`), pero `REGISTRO_DE_TANDAS_Y_REPUTACION` sigue `NO-ADQUIRIDA-POR-COSTO`/`MESA-DECIDE` sin ningún avance material, y la cita del encargo («CIDE declinada, CNBV diferida») corresponde a otra fila (`NC-0057`, búsqueda académica de tandas/CIDE-Colmex-UNAM, no esta fila de convenio comercial).
  **impacto:** `no_corrido_abiertas` no baja por esta fila; `NC-0037` sigue `ABIERTA`.
  **sucesor:** mesa, sobre la respuesta de `equipo@tandamas.mx` (misma fila hermana ya en `SOLICITUD-PREPARADA`) o decisión explícita de declinar/gastar en `REGISTRO_DE_TANDAS_Y_REPUTACION`.
- **qué:** Fila 6 (`NC-0055` → CERRADA), verbatim del encargo.
  **por qué:** `PARO-PREMISA` — `grep -c '#633' forense/tablero/TABLERO-PROGRAMA.md` da `0`, no `≥1`; el PR citado como relanzamiento (`PR #638`) fusionó bajo el título «`PARO-PREMISA` en B1, B2 ejecutada» y no toca `TABLERO-PROGRAMA.md` en su diff — B1 (el reemplazo del cuerpo curado) volvió a pararse, no aterrizó.
  **impacto:** `no_corrido_abiertas` no baja por esta fila; `NC-0055` sigue `ABIERTA`, sin nuevo relanzamiento intentado por este acto (fuera de perímetro: este acto cierra con cita, no relanza).
  **sucesor:** `GEN2-TRAMITE-TABLERO-2` (ya nombrado en la propia fila) o un tercer relanzamiento que regenere el adjunto contra la señal post-firma vigente.

Todo lo demás del encargo (filas 2-5, 7-8) corrió tal como se pidió.
