# SIGUIENTE ENCARGO · GEN2-F5-DOCUMENTAL-EJECUCION

Estado: **PENDIENTE DE FIRMA DE JONAS; NO LANZADO; NO AUTORIZA LLAMADAS**.
Base de preparación: `ACTO GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO`.
SHA de redacción: se fijará al firmar y mover a encargo VIVO; esta cola no es
autoridad de lanzamiento.
Entorno requerido: **CAJA para materializar corpus; NUBE/CLI sólo después de
probar transporte si el cliente firmado lo admite**.

## Resultado útil

Ejecutar FP-373 como recuperación documental en `DIN-M-01` y `TRA-M-07`, con
32 posiciones contemporáneas, fuentes nativas verificadas, identidad completa
y cero sustituciones. No probar transferencia, no emitir M, no estimar R nuevo
y no abrir F6.

## Compuertas previas, todas obligatorias

1. Este encargo debe ser firmado y movido desde `forense/encargos/cola/` a un
   encargo VIVO archivado verbatim antes de ejecutar.
2. El encargo 23, publicado como PR #720 con cabeza observada
   `67aa13d73e9300acd14c4b593e3bcfb6bc945712`, debe estar fusionado. Registrar
   el commit efectivo en `main` y la forma final de
   `SELECCION-TEMPORAL-v1`/`seleccion_transferencia`, o actualizar la spec si la
   interfaz final difiere. La cabeza abierta no es autoridad. No modificar el
   emisor aquí.
3. Jonás debe fijar proveedor, modelo exacto, cliente/versión, endpoint,
   herramientas, ventana, salida, parámetros, cuenta presupuestaria, tarifa y
   autorización explícita de las llamadas.
4. CAJA debe resolver contra `data/manifiesto.yaml` los cinco IDs DIN y tres
   IDs TRA de la spec, verificar hashes/tamaños y producir un manifiesto de
   transporte sin valores R ni tabulaciones derivadas.
5. Prueba seca: ambos paquetes caben, el cliente abre sus formatos, no trunca y
   devuelve identidad de archivo. Si falla, `TRANSPORTE-NO-VALIDADO`, cero
   llamadas experimentales.

## Diseño fijado

- Celdas: `DIN-M-01`, `TRA-M-07`.
- Brazos: `CONTEXTUAL-v2`, `FUENTE-DIRIGIDA-v1` conforme a
  `F5-panel-viabilidad-presupuesto-spec-v1_0.md` §4.2.
- Réplicas: 8 por celda/brazo; orden aleatorizado y congelado.
- Presupuesto: 32 llamadas lógicas; máximo dos reintentos por posición sólo
  para error técnico; techo 96 solicitudes facturables.
- Éxito por celda: >=6/8 puntos dirigidos trazables, cero sustituciones y
  mejora de cobertura >=4/8.
- Fuente ausente o transporte inválido: cancelar ambos brazos de la celda sin
  sustituto. Identidad/contaminación rota: parar todo el acto.

## Productos de cierre

Manifiesto de inputs y respuestas con hashes; 32 estados; conteo de tokens y
coste real por tarifa congelada; cobertura por brazo; traza documental por
punto; veredicto por celda; registro de reintentos; actualización de FP-373 y
NC-0160/NC-0152 sólo según firma y resultado. Mantener TRIADA-0002,
CALC-F5-REANALISIS-0001, FP-374 y NC-0161/0162 intactos.
