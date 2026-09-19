# GEN2-MARCADOR-ADOPCION-CLI-1 — cierre

Fecha: 2026-09-19. Base revisada: `7453f513b8c03fd4c3b155addc6b2fb539ddf439`; integración final sobre el delta de `origin/main` hasta `843a5f977e024ef5d74863e95856c763bee9e58d`. Estado: **propuesto; mesa fusiona**.

## Resultado

`milpa.src.motor.estimar_segmento()` recibe la identidad completa —regla, desenlace, instrumento, periodo, universo, ejes y categorías— y devuelve punto, IC95, clase de incertidumbre, CALC/RESULT fuente, `n`, denominador ponderado y estados separados. Si la identidad no existe devuelve ausencia explícita (`None`): no sustituye por nacional, otro desenlace, otro universo ni promedio.

El mapa ejecutable contiene 59 estimadores con 59 RESULT primarios distintos: 20 cruces C2 ya adjudicados y 39 pisos marginales corregidos. El consumidor lee `milpa/estimadores-por-segmento.yaml`; funciona sin R, microdatos y sin `data/corrida0/marcador-segmento.tsv`. Este último es una vista derivada, no la fuente de ejecución.

## Acceso y replay recuperado

Las rutas personales viven sólo en `data/raices.local.yaml`, ignorado por Git. El mecanismo persistente `tools/prepara_corpus.py --aplica` enlaza `data/raw` y resuelve las raíces lógicas en terminales y subprocesos nuevos. En Git quedan sólo los ids e identidades:

| input | formato | bytes | SHA-256 | resolución/preflight/replay |
|---|---:|---:|---|---|
| `conjunto_de_datos_encrige_2020_csv` | ZIP/CSV | 1,630,532 | `06864904426a6b2c18cdad63a8b7bcb995fd35333c44448ba3fb5a973b822c5a` | verificada · `COINCIDE` · `REPRODUCE/IDENTICO` |
| `encrige2020_cuestionario` | PDF | 1,532,744 | `f410156bf5131921f6699b47f07fba302b168de187ea638a5f601732097cd8c1` | verificada · `COINCIDE` · `REPRODUCE/IDENTICO` |
| `adultos_ensanut2024_w_stata_stata__v2026_09_01` | ZIP/Stata | 4,196,284 | `0fa8f4436fa427cc23d1d43164d449462c09eb787cb45ad20961576cb095a6c4` | verificada · `COINCIDE` · `REPRODUCE/IDENTICO` |

La evidencia de los 41 asientos recuperados está en `forense/evidencia-replay-aislado-2026-09-19.json`: 38 identidades vigentes proyectan `REPRODUCE/IDENTICO`; DIN emisiones conserva el veredicto global `NO-REPRODUCE/IDENTICO`, `NC-0313` y acredita sus C2 por RESULT; ENCRIGE y ENSANUT dejaron de estar bloqueadas al resolver los payloads y su nueva evidencia concluyente aislada está en `forense/evidencia-replay-acceso-restablecido-2026-09-19.json`. No se borró ni reinterpretó ningún asiento histórico. Una segunda proyección no propone cambios.

## Pisos corregidos y sucesión

Se conservaron los CALC sellados defectuosos y se crearon tres sucesores reconocidos por el registro:

| sucesor | celdas activas | corrección acreditada |
|---|---:|---|
| `CALC-PISOS-ENCIG2023-EJES-0002` | 10 | `N_TRA=01`, denominador comparable `P7_3`, numerador 4/5; sexo, cuatro edades y cuatro escolaridades |
| `CALC-PISOS-ENIF2021-EJES-0002` | 14 | localidad `TLOC {1,2}`/`{3,4}`, cuenta por `P5_4`, D9/`P5_7` para ahorro formal; sexo, edad, escolaridad, localidad y cuenta |
| `CALC-PISOS-ENVIPE2024-EJES-0002` | 15 | universo válido `BP1_20` para evasión y universo propio de robo total de vehículo para denuncia por seguro |

Edad admite 18–96 y excluye sentinelas/ausencias sin crear `"nan"`; escolaridad usa las cuatro categorías selladas. Los tres sucesores son `REPRODUCE/IDENTICO`, con puntos, IC, `n` y denominadores en RESULT; la evidencia aislada está en `forense/evidencia-replay-pisos-corregidos-2026-09-19.json`. Los 39 pisos son el total que producen las definiciones construibles, no una cuota impuesta. No se amplió a formalidad ni al desenlace secundario ENIF.

## Marcador, usos y conteos

El marcador distingue `evidencia`, `evaluacion`, `adjudicacion`, `implementacion`, `consumo` y `diagnostico_emisor`. El mapa por sí solo no cuenta como adopción: los 59 consumidores activos se publican en `data/corrida0/usos.tsv`, uno por identidad y RESULT primario.

| derivado | antes | después |
|---|---:|---:|
| estimadores segmentados activos | 20 | 59 |
| C2 / marginales corregidas | 20 / 0 | 20 / 39 |
| `corridas.tsv` | 207 | 210 |
| `resultados.tsv` | 6,923 | 7,122 |
| `usos.tsv` | 228 | 267 |

## Límites y reservas

- HOLDOUT permanece cerrado; ninguna fuente `ARBITRO` entra al consumidor.
- `ahorro_solo_informal` e `informal_cualquiera` siguen siendo desenlaces distintos.
- `NC-0313` conserva alcance global DIN `NO-REPRODUCE`; sólo los RESULT C2 coincidentes sustentan esas celdas.
- Edad × dominio ENVIPE permanece `CONSUMIDA-SIN-PILOTO`: no se promociona a C2 ni se fabrica otro punto.
- Las reservas sin RESULT y los cruces no adjudicados continúan reservados; la ausencia no tiene fallback.
- Los estados aquí son hechos de esta rama; la adopción consolidada queda condicionada al merge de mesa.

## Comandos de reproducción y consumo

```bash
python3 tools/marcador_segmento.py
python3 tools/corrida0.py registro
python3 -m unittest tests.test_estimadores_segmento tests.test_pisos_ejes_v2
python3 - <<'PY'
from milpa.src.motor import estimar_segmento
print(estimar_segmento(regla="DIN", desenlace="ahorro_solo_informal",
    instrumento="ENIF", periodo="2024", universo="persona_elegida_18_mas",
    ejes={"localidad": "menos-15000"}))
PY
```

Pruebas y baseline exactos se consignan en el PR; `tests/gonogo_marcador.py` conserva sus seis checks históricos y declara expresamente que no acredita este nuevo consumidor.
