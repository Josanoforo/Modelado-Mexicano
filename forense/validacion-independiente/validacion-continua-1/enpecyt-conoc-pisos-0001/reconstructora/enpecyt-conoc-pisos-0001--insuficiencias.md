# Insuficiencias de la spec humana (ENPECYT-CONOC-PISOS v1.0)

## Ola 2015 — las 100 llaves (IC calibrado del piso)
- **τ² sin estimador en prosa.** La spec dice «τ² por conducta × eje × categoría sobre 2011→2013→2015»
  y el IC `expit(logit p ± z·√(ee_2015² + τ²))`, pero no fija cómo se estima τ² (varianza muestral de
  logits con ddof 0 o 1, método de momentos/DerSimonian-Laird que descuente varianza muestral —imposible
  en 2011, que no tiene EE—, u otro), ni su escala (se infiere logit solo por la fórmula), ni el truncamiento en 0.
- **Escala de ee_2015** dentro de `ic_calibrado` (EE bootstrap de p vía delta, o DE de logits replicados)
  y valor de **z** (presumiblemente 1.96) no están escritos; `ic_calibrado` pertenece a una «receta» ausente del paquete.
- Resultado: punto reconstruido, `estado_ic = NO-IDENTIFICADA`. El EE y el percentil bootstrap 2015 están
  solo en `diagnostico.json`, no como IC de la llave.
- **RESPETA-10-INVENTOR 2015 (10 llaves):** además, τ² sobre 2011→2015 no existe: el reactivo solo está en 2015.

## Ola 2013 — las 90 llaves (IC bootstrap)
- «receta común» y «contrato conservador» no se describen en prosa. No fijados: tamaño de remuestreo por
  estrato (n_h vs n_h−1 con reescalamiento Rao-Wu), orden de consumo del generador PCG64(20260925)
  (orden de estratos/UPM, réplica-externa vs estrato-externo, un generador por ola o uno compartido),
  forma del IC (percentil, normal o logit-normal) y qué hace «conservador». Se tomó una lectura
  (decisiones D9–D10 en `diagnostico.json`); otra lectura legítima da otros extremos del IC.

## Ola 2011 — las 90 llaves
- Ninguna de método: la spec fija P ponderada sin IC (`SIN-IC`).

## Todas las olas (menores, resueltas con decisión declarada)
- «sólo llaves únicas»: no dice si una llave duplicada se descarta completa o se conserva una ocurrencia
  (afecta 2015: 3 personas; D1).
- `EST_DIS` 2015 viene con 3 caracteres y valores 001–096, contra 1–4 del FD (D4); no cambia el número de estratos.
- Código 11 en S4P14_* de 2011 no está en el descriptor (01–10); la regla «= 10 de 1–10» lo excluye (D5).
