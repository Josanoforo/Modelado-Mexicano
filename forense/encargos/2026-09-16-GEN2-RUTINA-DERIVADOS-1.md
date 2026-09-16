# ENCARGO · ACTO GEN2-RUTINA-DERIVADOS-1

Recibido en mesa 16/sep/2026. Texto verbatim del lanzamiento:

> CAJA · ACTO GEN2-RUTINA-DERIVADOS-1 (Opus, integral; raíz montada — la
> caja es el único entorno que puede derivar el universo)
>
> P1 · /deriva (.claude/commands/deriva.md + tools/deriva_cron.sh),
> colgado del mismo scheduler y launcher, con su propio lock y rama
> derivados/<fecha> (el patrón checkout_o_crea_censo ya resolvió las
> colisiones de nombre compartido; se reutiliza). Una corrida = cuatro
> derivaciones, todas por script, ninguna por juicio: (a) snapshot del
> universo declarado como sucesión fechada T<fecha> con
> snapshot_universe.py sobre el corpus de hoy — T0 intacto, ledger de
> inspecciones arrastrado por hash, diff T<hoy>−T<anterior> por script;
> (b) tablero_programa.py --actualiza; (c) corrida0.py registro
> --verifica en seco y status; (d) tests/check.py --baseline reportando
> solo FAIL nuevos y WARN nuevos (la firma de hoy). Abre un PR
> [DERIVADOS] <fecha> con la huella (disparador=windows-task-scheduler)
> y las cuatro deltas; si nada cambió, huella NADA-QUE-HACER y cero PR,
> como despacha.
> P2 · Primera corrida = T1, a mano dentro del acto, con el denominador
> vigente a la vista: activos declarados hoy, adquiridos, inspeccionados,
> y el porcentaje que ADR-67 dejó en 1.43% en agosto.
> P3 · Guardarraíles, escritos en el runbook (agente-tramite v1.1, mismo
> archivo, sucesión): la rutina nunca escribe canon, milpa, decisiones ni
> adopta; nunca recongela la línea base; si el diff del universo es
> material (activos que desaparecen, hashes que cambian), lo reporta como
> hallazgo A.7 en el PR y no lo resuelve. Un PR diario es lo máximo que
> produce.
> D-14 contestado, en el encargo: defecto real — tres líneas base
> derivadas sin rutina, medidas hoy (T0 un mes/1 178 PRs; tablero 50 PRs;
> suite recongelada cuatro veces a mano); cambia decisiones — el servicio
> decide qué adquirir contra el universo de agosto; cuesta menos que
> corregirlo a mano — ya lo estamos pagando en cada corte.
> Perímetro: tools/deriva_cron.sh, deriva.md, launcher (una línea),
> runbook v1.1, data/curacion-universo/ (solo sucesiones nuevas), tablero
> (bloque derivado). Concurrencia: F6-PANEL-CAJA-1 y CAJA-REACTIVOS-FD-1
> no tocan nada de esto; el servicio de adquisición comparte scheduler y
> por eso el lock propio.
