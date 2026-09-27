# Recibo solicitado · ASTRA6-C2-FRONTERA-1

EJECUTADO: cuatro decisiones instrumentales y dos paquetes diagnósticos completos para revisión. Recomendación: no lanzar ENSU con banda5pp por potencia insuficiente; no lanzar ENOE mientras el diseño no resuelva singleton; diferir contrato CESD ENSANUT y oro comparable MOCIBA. No se llenó cupo ni se diseñó retador. No se adoptó cifra ni se abrió ola reservada. Cuerpo recibido archivado una vez por#1191; SHA a737139ae2467db1a44346749798595a29f2bef316d8d1617f916fe467b846d7. Firma «Acordado» citada desde asiento C2-ENIF, no repetida.

LEÍDO: propuestas previas y cierre#1182, documentación limpia histórica; registros incidentales que mezclaban exposición están declarados en selección y excluidos del diseño. Firma sucesora B1 cubre suspensión digital; no habilita controles pendientes ni COMMIT3. Excepción de documentación CAJA por instrucción posterior «corre el encargo», declarada en frontera-arranque.json.

PROPUESTO: hoja-firma-frontera.md contiene objeto exacto, hashes, textos de firma recomendada y alternativa; frontera-inventario.json conserva hashes de todos los archivos terminados del paquete. Los YAML propuestos usan nombre instrumental para cumplir unicidad CLI: ensu-spec.yaml/enoe-spec.yaml. Son BORRADOR/PROPUESTO; no SELLADO-INTERNAMENTE como emisiones prospectivas, ENVIADO-A-ATESTACIÓN o ATESTIGUADO-EXTERNAMENTE.

## Objetos y comandos reproducibles

- Selección: seleccion/decision-instrumental.md; catálogos limpios CESD en seleccion/ensanut-catalogos-limpios.json. Calendario oficial limpio y ventanas inferidas en frontera-calendario-fuente.md.
- ENSU: paquetes/ENSU-CAMPECHE-INSEGURIDAD/ensu-spec-humana.md, ensu-spec.yaml, ensu_lector.py, ensu_prueba_sintetica.py, ensu-oro.json, ensu-sintetico-auditoria.json y ensu-hashes.sha256.
- ENOE: paquetes/ENOE-INFORMALIDAD/enoe-spec-humana.md, enoe-spec.yaml, enoe_lector.py, enoe_prueba_sintetica.py, enoe-oro.json, enoe-sintetico-auditoria.json y enoe-hashes.sha256.
- Desde cada carpeta de paquete: `python3 ensu_prueba_sintetica.py` o `python3 enoe_prueba_sintetica.py`; `sha256sum -c ensu-hashes.sha256` o `sha256sum -c enoe-hashes.sha256`. Las auditorías contienen receta del oro con payload completo verificado antes de abrirlo. Solo histórico autorizado, nunca2026/2027.
- Desde raíz del repo: `python3 forense/analisis/familias-2027-frontera-1/potencia/calcula.py --gold-se forense/analisis/familias-2027-frontera-1/paquetes/ENSU-CAMPECHE-INSEGURIDAD/ensu-oro.json --enoe-gold-se forense/analisis/familias-2027-frontera-1/paquetes/ENOE-INFORMALIDAD/enoe-oro.json`.
- Verificación de identidades y evidencia sin microdatos: `python3 forense/analisis/familias-2027-frontera-1/frontera-verifica.py`. El modo de creación de inventario se ejecutó después de terminar los objetos; no se usa para ocultar discordancias.
- Gate: `python3 tests/check.py --rapido --baseline`; resumen de salida en frontera-gate-final.txt. No se repara baseline/CI. Los primeros intentos mostraron colisiones T02 de nombres y rótulo T25 de era; se corrigieron nombres propios y prosa sin editar tests ni ampliar medición.
- Contador: `python3 tools/corrida0.py status`; `python3 tools/cierre_acto.py --sin-suite` confirmó celdas_validadas219→219, Δ0 al lanzamiento71cf040f. Diagnósticos y planificación no cuentan como adopciones.

## Reservas y recepción solicitada

ENOE conserva punto y SE nula por39 estratos singleton del marco completo; no se sustituye por Kish ni por colapso elegido tras potencia. ENSU falla criterio ex ante aun sin ruido temporal. MOCIBA no obtiene apertura de sus históricos F6. ENSANUT no fabrica corte clínico. No resultados futuros, COMMIT1/2 adoptados, R, COMMIT3, OTS, fusión ni revisión independiente obtenida.

Se solicita por el circuito de mesa en el PR un recibo independiente sobre selección, comparabilidad, lectores, oros, potencia y disposición propuesta. Las correcciones y cualquier aceptación se documentan como sucesores; no se afirma recibo concedido. NC/FP propias71cf conservan pendientes y objetos de firma. La secuencia real con gates está en secuencia-y-calendario.md. Corte en frontera-corte-final.json; resultado y NO-CORRIDO/CONSUMIDO en frontera-cierre.md.

Entrega: [PR#1195](https://github.com/Josanoforo/Modelado-Mexicano/pull/1195), rama codex/astra6-c2-frontera-1; recibo independiente solicitado en el cuerpo del PR, no concedido.

EJECUTADO, corrección solicitada en#1195: la decisión exige ambos grupos y escenarios completos, SE válidos y ningún bloqueo; cota conjunta nula ante familia parcial. Regresiones y evidencia en frontera-correccion-grupos.md. La recomendación actual de no lanzar ambos contratos permanece igual.
