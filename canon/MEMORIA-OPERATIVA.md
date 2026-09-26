# MEMORIA OPERATIVA · Modelado Mexicano · se lee al arrancar, antes de explorar
Última mano de dirección: 26/sep/2026 · derivada: ⟲ por /tramite

## 1 · Régimen vigente (no lo re-diagnostiques)
- Instrucciones v2.16 (+ cláusula de autonomía v1.0: resuelve, interpreta, redacta rotulado, PARA solo por D-19 estricta). Plantilla de encargo v2.1 (v2.2 en trámite).
- Canal de publicación: el job de derivados corre en cada push a main y abre un PR [deriva] que se auto-fusiona; también se dispara a mano (Actions → Run workflow). status lee las vistas: si no hay [deriva] reciente, main va atrasado y se dice.
- Auto-merge solo: [deriva], claude/encola-*, acto/gen2-tramite-*. Todo lo que sella corridas o escribe en milpa/ lo fusiona mesa. Ramas codex/*: recibo de Claude obligatorio (R(a)).
- Recibo: forense/analisis/<unidad>/recibo-para-claude.md, EJECUTADO/LEÍDO por frase.
- Reservas: ola más reciente de todo programa con historia; ENVIPE 2026; ENCO; ENIGH 2024 salvo seis columnas AMAI (C7). ENCIG 2025 y ENVIPE 2025: abiertas.
- Etapa de retadores: cerrada (seis evaluaciones; el piso no pierde). Regla 6: sin retadores, pilotos ni duelos sobre olas vistas. Frente prospectivo = familias 2027.

## 2 · Herramientas (úsalas antes de abrir un archivo)
- tools/consulta.py result|corrida|celda|payload|fp|nc <id> → una línea. tools/vista.py → vistas por referencia (valor_de). tools/benchmark.py → consulta de producto (cuando fusione).
- corrida0.py status (contadores) · demanda (cola) · verify <CALC> · registro --escribe (solo el job).
- tools/entorno.py --arranque (firma de entorno). docs/sesiones.md (clon parcial). tools/escribe_relevo_consumo.py (único que escribe milpa/). tools/marcador_segmento.py --escribe (solo el job).
- Índice de tools/ con docstring ⟲: forense/analisis/cableado/herramientas.tsv. Hook de lectura: tools/hook_lectura.py (registro: forense/analisis/cableado/bloqueos.tsv).
- Mapa de dominios: canon/mapa-dominios-v1_1.tsv; cola de medición: forense/analisis/dominios/cola-medicion-v1_0.tsv; corpus: forense/analisis/corpus-completo/tabla-final-v1_0.tsv (131 programas).

## 3 · Ya se intentó y no (no lo vuelvas a proponer)
- Git LFS (cuota); sacar la vista del canal (E.7); deploy key para empujar directo (el canal abre PR); bypass de GitHub Actions en rulesets (no existe).
- Pin i-CRUDO al catálogo de momentos: rompe T-REPRO(c); el catálogo lleva valor GEN2 + cita + discrepancia_gen1 (#1115).
- Contar adopciones desde milpa/tramite.yaml a mano: status lee usos.tsv, que solo publica el canal.
- Reglas del motor "existentes" para los diez RESULT de Banxico/CTX/MOTRAL: no existían; se crearon por el escritor (ADOPCION-4).
- Buscar "¿lanzado?" por rama: la plataforma nombra ramas claude/new-session-*; búscalo por archivo en forense/encargos/ y por CONSUMIDO.
- Marcar PROSPECTIVA por el champion vigente: la marca vive en la evaluación original; un sucesor re-medido es RETROSPECTIVA-MECÁNICA y no la borra.

## 4 · Decisiones activas por objeto ⟲ (FIRMADA del último corte, id → una línea)
<!-- T-MEM:INICIO -->
- Corte 2026-09-26 · 123 FIRMADA en 14 días · se muestran 12 · todas: `python3 tools/memoria_operativa.py --lista`
- FP-260926-GEN2-FRONT-3-PORTADA-1-8914-02 · congelar (texto de portada) · 26/09
- FP-260926-GEN2-FRONT-3-PORTADA-1-8914-01 · borrar / reescribir (movimiento de raíz) · 26/09
- FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-03 · adoptar (pisos 03 del acto; ninguna regla consumidora todavia) · 26/09
- FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-02 · adoptar (pisos 02 del acto; ninguna regla consumidora todavia) · 26/09
- FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01 · adoptar (pisos 01 del acto; ninguna regla consumidora todavia) · 26/09
- FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-03 · vetar (filas de 0001) · 26/09
- FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-02 · adoptar (pisos 02 del acto) · 26/09
- FP-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-01 · adoptar (pisos 01 del acto; ninguna regla consumidora todavia) · 26/09
- FP-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-04 · adopcion de los pisos LAPOP 2004/2006/2019 · 26/09
- FP-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-03 · adopcion de los pisos PEW Global Attitudes 2013-2024 · 26/09
- FP-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-02 · adopcion de los pisos Latinobarometro 2023 · 26/09
- FP-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-01 · adopcion de los pisos WVS 2018 · 26/09
<!-- T-MEM:FIN -->

## 5 · Dónde está cada cosa
- Encargos y adendas: forense/encargos/ (CONSUMIDO al pie). Notas de cierre: forense/notas/. ADR: canon/L0/. Firmas: forense/firmas-pendientes.tsv. Deuda: forense/no-corrido.tsv (razón A.14).
- Producto: canon/catalogo-del-mexicano-v1_N, canon/informe-programa-v1_N, canon/tabla-de-piso-v1_N, docs/ (Pages). Tablero: canon/TABLERO-PROGRAMA.md (solo el bloque derivado; árbol == origin/main True o inválido).
- Sellos: data/corrida0/CALC-*/sello.json; manifiesto de sellos: forense/sellos/. Corpus: data/manifiesto.yaml (por id; nunca cat).
