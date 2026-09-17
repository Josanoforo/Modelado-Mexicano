# Recibo de reproducción · ENCRIGE carga e intensidad

Fecha de ejecución: 16 de septiembre de 2026 (America/Mexico_City).

## Cadena

- Padre: `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`, sin relanzar.
- CSV usado: `forense/analisis/encrige-descriptiva-1/encrige-corrupcion-por-tamano.csv`.
- SHA-256 del CSV: `632ce31b2c2cf70e22871319b5842e6168592f065588b69b11010e3552b48c26`.
- El SHA coincide con `RESULT-ENCRIGE-DES-G-CSV-SHA256`; el sidecar del padre
  valida `sello.json` y éste valida `resultados.json`, `spec.yaml`,
  `medidor.py` y `ejecucion.json`.
- Derivado: `CALC-ENCRIGE-CARGA-INTENSIDAD-0001`.
- Commit ejecutado: `55259dbe975fbd625154cbec8af233bce6a334bf`.
- Corrida: `CALC-ENCRIGE-CARGA-INTENSIDAD-0001--55259dbe975f`.
- Sello: `c94f098f8a7c53e14ac737f4bd1ce89b343954aef5504000c05b6f7f5ae742f5`.

La spec y el código se fijaron primero en `18a8c46`. Los puntos del padre ya
eran observados; este orden acredita un contrato previo de derivación, no un
preregistro ciego.

## Comando único de producto

Desde la raíz del repositorio:

```bash
python3 tools/encrige_carga_intensidad.py
```

Reproduce determinísticamente:

- `tabla-ampliada.csv`;
- `participaciones-por-tamano.csv`;
- `contrastes-vs-micro.csv`;
- `controles.json`;
- `participaciones-por-tamano.svg`.

Hashes sellados de los cinco artefactos, en ese orden:

```text
1b6d64794a3c1cddaedf9c19b30518aad37df7b1882084386d86daefde465628
c2056ca23066d7884dad8f3a21f3159570a87b5ec2cb5ca45530c1541253643b
91065de95a8c8b3793b3007dab7efc6462532effe648271c5fa3f63a2806d722
7469a64cfabf58fe21af983ec90e3d2f307e618b340c860a65d4ec5cf27e9cac
076b53a8d30154f0caf3e0d51a6d6c0ce956347124258649c7bc8234aa7730e6
```

## Comandos de control ejecutados

```bash
python3 tools/corrida0.py spec-check CALC-ENCRIGE-CARGA-INTENSIDAD-0001
python3 tests/test_encrige_carga_intensidad.py
python3 tools/corrida0.py preflight CALC-ENCRIGE-CARGA-INTENSIDAD-0001
python3 tools/corrida0.py run CALC-ENCRIGE-CARGA-INTENSIDAD-0001
python3 tools/corrida0.py verify CALC-ENCRIGE-CARGA-INTENSIDAD-0001
```

Resultados: `spec-check` 0 fallos; cinco pruebas focales, cinco correctas;
preflight verde desde árbol limpio; corrida exitosa y sellada; verify
`REPRODUCE (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)` para 31 resultados.

Controles sustantivos: denominadores compatibles; cuatro tamaños reconstruyen
exactamente los nacionales de `N`, `A` y `T`; identidad `m=p*r`; tres
descomposiciones con residuo máximo `2e-41`; nacional excluido de las partes.
No se abrió microdato, no se calculó estadística de respondentes y no se
modificó el padre.
