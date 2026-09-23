#!/usr/bin/env python3
"""Genera seis borradores condicionales de familia, sin leer olas futuras."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/prereg-caja"

# Estimandos disjuntos por mecanismo y denominador. Cada piso se comprueba
# contra el CALC sellado vigente, no contra una copia de U1.
FAMILIES = [
    ("ENIF-AHORRO-FORMAL", "ENIF", "2027", "2024", "persona", "proporción [0,1]", "acceso a ahorro formal entre personas en el denominador B de ENIF AHO", "CALC-ENIF-0001", "RESULT-ENIF-AHO-B-P-FORMAL-P", "0c90801873c91ac109219fbe3bf88632fc6aa8a6bcef637f9876398e95f76de6"),
    ("ENIF-HORIZONTE-AHORRO", "ENIF", "2027", "2024", "persona", "proporción [0,1]", "horizonte de ahorro por ambas vías bajo la definición HVD", "CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1", "RESULT-HVD-A-AMBAS-VIAS", "1c8b329fb2088d24298acb3081e9bb2d2366dce05c6e238d282271d251d92609"),
    ("ENCIG-PAGO-DIGITAL", "ENCIG", "2027", "2025", "trámite", "proporción [0,1]", "pago de luz por canal digital en el universo C de ENCIG MOR", "CALC-ENCIG-0001", "RESULT-ENCIG-MOR-C-P-ADOPTA", "9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7"),
    ("ENCIG-SOLICITUD-MORDIDA", "ENCIG", "2027", "2025", "persona", "proporción [0,1]", "solicitud de mordida en el universo A de ENCIG MOR", "CALC-ENCIG-0001", "RESULT-ENCIG-MOR-A-P-SOL1", "9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7"),
    ("ENVIPE-DENUNCIA-U4", "ENVIPE", "2027", "2025", "persona", "proporción [0,1]", "motivo de no denuncia C2, universo U4 y FAC_ELE", "CALC-ENVIPE-0001", "RESULT-ENVIPE-DEN-P-C2-U4", "18310f8adb6fb5963038d67c2e8a7eaba50e09c062dddbc579e918f090cbde16"),
    ("ENVIPE-EVASION-NORMA", "ENVIPE", "2027", "2025", "persona", "proporción [0,1]", "evasión de norma bajo la codificación A vigente", "CALC-EVASION-NORMA-0001-v1_1", "RESULT-EVASIONNORMA-A-P-EVADE", "8076d9ff1e18ab1fe6ac7168600810580cabe99c1df9373ee21c8b40e9d2abe8"),
]


def main() -> None:
    for slug, instrument, target, prior, unit, scale, estimand, calc, result, expected_hash in FAMILIES:
        folder = ROOT / "data/corrida0" / calc
        actual = hashlib.sha256((folder / "sello.json").read_bytes()).hexdigest()
        assert actual == expected_hash, (calc, actual)
        sidecar = (folder / "sello.sha256").read_text().split()[0]
        assert sidecar == expected_hash
        values = json.loads((folder / "resultados.json").read_text())["resultados"]
        assert result in values and isinstance(values[result], (int, float))
        path = OUT / f"FAMILIA-2027-{slug}-spec-v1_0.md"
        body = f"""# FAMILIA-2027-{slug} · spec humana condicional v1.0

**Estado: CONDICIONAL, NO LISTA PARA FIRMA DE APERTURA.** El nombre 2027 es un identificador de carpeta, no una fecha publicada. Consultado el calendario INEGI 2026 el 23/sep/2026; fecha oficial de publicación de {instrument} {target}: **NO-CONFIRMADA**. No se abre dato futuro con este borrador.

## Estimando cerrado y piso

- Instrumento/ola objetivo: {instrument} {target}; levantamiento y publicación: NO-CONFIRMADOS. Antes de firmar, mesa coteja cuestionario futuro, FD, pesos, población y periodicidad con la ola {prior}.
- Estimando único: {estimand}. Unidad de observación: **{unit}**; escala del punto **{scale}**. No se agregan otros estimandos tras observar R.
- Piso congelado en este borrador: `{result}` de `{calc}` (ola {prior}); SHA-256 de `sello.json`: `{expected_hash}`. Su valor se lee del RESULT, no se transcribe como parámetro de producto. Si una ola intermedia cambia la identidad, esta spec se declara NO-ELEGIBLE; no se sustituye el piso a posteriori.

## Regla futura de evaluación del piso

El ejecutor futuro congela en COMMIT-1 la spec YAML, el medidor efectivo, los códigos, el marco de bootstrap UPM dentro de estrato y el universo elegible **antes de leer** la nueva ola. El primer resultado que produzca el procedimiento es el que se reporta, incluso adverso o NO-ESTIMABLE. Habrá un solo acceso de evaluación a R para lo sellado a tiempo; una regla añadida después de R no entra. Reserva de la nueva ola por canal de adquisición; solo la levanta el código congelado o decisión escrita de mesa.

Métrica primaria de piso: error absoluto en puntos porcentuales entre el punto histórico fijo y el R futuro del mismo estimando, además del indicador de si R cae en el IC histórico si ese IC tiene calibración acreditada. El IC de incertidumbre para el error se obtendrá de réplicas del R futuro con el piso fijo, con unidad y regla de soporte idénticas. No hay segundo contendiente: **ΔMAE, victoria frente a otro modelo y B-bis de superioridad = NO-APLICABLE**. Vocabulario cerrado para el piso: `CALIBRADO`, `SUBCOBERTURA`, `NO-ESTIMABLE`, `NO-COMPARABLE`. Se informa también el error como magnitud continua; no se elige un umbral después de R.

## Condiciones para firma

1. Fecha oficial de publicación de {instrument} {target} dentro de la ventana 23/sep/2026–23/mar/2028 y texto de cuestionario futuro aún pendientes.
2. Umbral material, soporte mínimo, tratamiento de faltantes y regla de comparabilidad por cambio de reactivo deben fijarse por mesa antes de COMMIT-1. No se hereda automáticamente el 0.5 pp de otras evaluaciones.
3. Precisión/potencia de la regla de piso: **NO-CALCULABLE** desde este RESULT puntual. Faltan el vector histórico de réplicas emparejadas, n efectivo y varianza de diseño de la diferencia para fijar efecto mínimo detectable, α y potencia objetivo. No se reconstruye varianza desde extremos de IC.
4. Resultado si el futuro falsador no refuta: conservar el piso solo para el estimando, unidad, ola y tolerancia sellados; nunca concluir persistencia general de conducta ni detectar cambios entre olas.

Fuente de selección: catálogo U1, commit `0ac21b6c`, contrastado aquí con RESULT y sello del CALC. Comparte apertura de {instrument} {target} con otras familias de ese instrumento, sin consumir R más de una vez.
"""
        path.write_text(body)
        digest = hashlib.sha256(body.encode()).hexdigest()
        path.with_name(path.name + ".sha256").write_text(f"{digest}  {path.name}\n")
    print(f"familias_condicionales={len(FAMILIES)}")


if __name__ == "__main__":
    main()
