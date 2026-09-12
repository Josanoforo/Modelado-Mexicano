#!/usr/bin/env python3
"""Hace utilizables las fuentes adquiridas para NC-0164/N34.

El acto es de adquisición y estructura: cuenta observaciones y denominadores
disponibles, pero no estima asociaciones, efectos causales ni parámetros del
modelo. Los payloads permanecen fuera de Git bajo ``data/raw``; las tablas
pequeñas derivadas sí se versionan.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "GEN2_N34_PRODUCTO_DANO"
OUT = ROOT / "data" / "n34-producto-dano"

BANXICO_XLSX = RAW / "banxico_satisfaccion_usuarios_2019_2024.xlsx"
SHED_ZIP = RAW / "shed_2025_public_csv.zip"
CFPB_PDF = RAW / "cfpb_bnpl_unsecured_debt_2025.pdf"

PRODUCTOS = {
    "tdc": "tarjeta_credito",
    "hip": "credito_hipotecario",
    "per": "credito_personal",
    "nom": "credito_nomina",
    "aut": "credito_automotriz",
}

SALIDAS = {
    "banxico": OUT / "banxico-cobertura-producto-ola.csv",
    "shed": OUT / "shed-bnpl-cobertura.csv",
    "cfpb": OUT / "cfpb-bnpl-default-tabla3.csv",
    "candidatos": OUT / "candidatos-n34.csv",
}


def _columna_xlsx(ref: str) -> int:
    letras = re.match(r"[A-Z]+", ref)
    if not letras:
        raise ValueError(f"referencia XLSX sin columna: {ref!r}")
    valor = 0
    for letra in letras.group(0):
        valor = valor * 26 + ord(letra) - 64
    return valor - 1


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    nombre = "xl/sharedStrings.xml"
    if nombre not in zf.namelist():
        return []
    strings: list[str] = []
    with zf.open(nombre) as handle:
        for _, elem in ET.iterparse(handle, events=("end",)):
            if elem.tag.endswith("}si"):
                strings.append("".join(t.text or "" for t in elem.iter()
                                       if t.tag.endswith("}t")))
                elem.clear()
    return strings


def _valor_celda(celda: ET.Element, compartidas: list[str]):
    tipo = celda.attrib.get("t")
    valor = next((e.text for e in celda if e.tag.endswith("}v")), None)
    if tipo == "inlineStr":
        return "".join(e.text or "" for e in celda.iter()
                       if e.tag.endswith("}t"))
    if valor is None:
        return None
    if tipo == "s":
        return compartidas[int(valor)]
    if tipo in {"str", "e"}:
        return valor
    numero = float(valor)
    return int(numero) if numero.is_integer() else numero


def iterar_primera_hoja_xlsx(path: Path):
    """Lee la primera hoja con stdlib para no añadir una dependencia a CI."""
    with zipfile.ZipFile(path) as zf:
        compartidas = _shared_strings(zf)
        hoja = "xl/worksheets/sheet1.xml"
        if hoja not in zf.namelist():
            raise ValueError(f"{path}: no contiene {hoja}")
        with zf.open(hoja) as handle:
            for _, elem in ET.iterparse(handle, events=("end",)):
                if not elem.tag.endswith("}row"):
                    continue
                valores: dict[int, object] = {}
                for celda in elem:
                    if celda.tag.endswith("}c"):
                        valores[_columna_xlsx(celda.attrib["r"])] = _valor_celda(
                            celda, compartidas
                        )
                largo = max(valores, default=-1) + 1
                yield [valores.get(i) for i in range(largo)]
                elem.clear()


def _csv_text(campos: list[str], filas: list[dict[str, object]]) -> str:
    salida = io.StringIO(newline="")
    writer = csv.DictWriter(salida, fieldnames=campos, lineterminator="\n")
    writer.writeheader()
    writer.writerows(filas)
    return salida.getvalue()


def _valido(valor, permitidos: set[int]) -> bool:
    try:
        return int(valor) in permitidos
    except (TypeError, ValueError):
        return False


def extraer_banxico(path: Path = BANXICO_XLSX) -> str:
    filas = iterar_primera_hoja_xlsx(path)
    cabecera = [str(v) for v in next(filas)]
    if len(cabecera) != 142:
        raise ValueError(f"Banxico: se esperaban 142 columnas, hay {len(cabecera)}")
    requeridas = {"fecha", "ponderador"}
    for prefijo in PRODUCTOS:
        requeridas.update({
            f"{prefijo}_filtro", f"{prefijo}_intereses",
            f"{prefijo}_comp_pago", f"{prefijo}_problemas",
            f"{prefijo}_reclamacion", f"{prefijo}_vulnerabilidad",
        })
    faltantes = sorted(requeridas - set(cabecera))
    if faltantes:
        raise ValueError(f"Banxico: faltan columnas {faltantes}")
    idx = {c: cabecera.index(c) for c in requeridas}
    conteos = defaultdict(lambda: defaultdict(float))
    total = 0
    por_ola = defaultdict(int)
    for valores in filas:
        total += 1
        ola = int(valores[idx["fecha"]])
        por_ola[ola] += 1
        peso = float(valores[idx["ponderador"]])
        for prefijo in PRODUCTOS:
            if not _valido(valores[idx[f"{prefijo}_filtro"]], {1}):
                continue
            c = conteos[(ola, prefijo)]
            c["n_tenedores"] += 1
            c["masa_tenedores"] += peso
            costo = _valido(valores[idx[f"{prefijo}_intereses"]], set(range(11)))
            pago = _valido(valores[idx[f"{prefijo}_comp_pago"]], {1, 2, 3, 4})
            problema = _valido(valores[idx[f"{prefijo}_problemas"]], {1, 2})
            reclamo = _valido(valores[idx[f"{prefijo}_reclamacion"]], {1, 2})
            vulnerabilidad = _valido(
                valores[idx[f"{prefijo}_vulnerabilidad"]], {1, 2, 3, 4}
            )
            for nombre, presente in (
                ("n_costo_valido", costo), ("n_pago_valido", pago),
                ("n_problema_valido", problema), ("n_reclamo_valido", reclamo),
                ("n_vulnerabilidad_valida", vulnerabilidad),
                ("n_costo_pago_validos", costo and pago),
                ("n_costo_pago_problema_validos", costo and pago and problema),
            ):
                c[nombre] += int(presente)
    esperado = {2019: 2072, 2020: 2075, 2021: 2071,
                2022: 2060, 2023: 2070, 2024: 2060}
    if total != 12408 or dict(por_ola) != esperado:
        raise ValueError(f"Banxico: corte inesperado total={total}, olas={dict(por_ola)}")
    salida = []
    for ola, prefijo in sorted(conteos):
        c = conteos[(ola, prefijo)]
        salida.append({
            "pais": "Mexico",
            "periodo": ola,
            "unidad": "persona_usuaria_ola",
            "producto": PRODUCTOS[prefijo],
            "n_tenedores": int(c["n_tenedores"]),
            "masa_ponderada_tenedores": f'{c["masa_tenedores"]:.6f}',
            "n_costo_interes_valido": int(c["n_costo_valido"]),
            "n_pago_valido": int(c["n_pago_valido"]),
            "n_problema_valido": int(c["n_problema_valido"]),
            "n_reclamacion_valido": int(c["n_reclamo_valido"]),
            "n_vulnerabilidad_valida": int(c["n_vulnerabilidad_valida"]),
            "n_costo_y_pago_validos": int(c["n_costo_pago_validos"]),
            "n_costo_pago_y_problema_validos": int(
                c["n_costo_pago_problema_validos"]
            ),
        })
    campos = list(salida[0])
    return _csv_text(campos, salida)


def extraer_shed(path: Path = SHED_ZIP) -> str:
    variables = {
        "BNPL1": ("uso_bnpl_ultimo_ano", "todas_las_personas"),
        "BNPL3": ("atraso_pago_bnpl", "usuarios_bnpl"),
        "BNPL3A": ("cargo_extra_por_atraso_bnpl", "usuarios_bnpl_con_atraso"),
        "BNPL1A": ("sobregiro_o_nsf_disparado_por_bnpl", "subuniverso_del_cuestionario"),
        "BNPL4_e": ("bnpl_unica_forma_de_poder_pagar", "usuarios_bnpl"),
    }
    with zipfile.ZipFile(path) as zf:
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if csvs != ["public2025.csv"]:
            raise ValueError(f"SHED: miembros CSV inesperados: {csvs}")
        with zf.open(csvs[0]) as raw, io.TextIOWrapper(raw, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if len(reader.fieldnames or []) != 815:
                raise ValueError(f"SHED: se esperaban 815 columnas")
            faltantes = sorted(({"shedid", "weight", *variables}) - set(reader.fieldnames or []))
            if faltantes:
                raise ValueError(f"SHED: faltan columnas {faltantes}")
            stats = defaultdict(lambda: defaultdict(float))
            ids = set()
            total = 0
            for row in reader:
                total += 1
                ids.add(row["shedid"])
                peso = float(row["weight"])
                for var in variables:
                    valor = row[var]
                    if valor not in {"Yes", "No"}:
                        continue
                    stats[var]["n_valido"] += 1
                    stats[var]["masa_valida"] += peso
                    stats[var][f"n_{valor.lower()}"] += 1
                    stats[var][f"masa_{valor.lower()}"] += peso
    if total != 12934 or len(ids) != total:
        raise ValueError(f"SHED: filas/id inesperados: filas={total}, ids={len(ids)}")
    salida = []
    for var, (concepto, universo) in variables.items():
        s = stats[var]
        salida.append({
            "pais": "Estados_Unidos",
            "periodo": 2025,
            "unidad": "persona",
            "variable": var,
            "concepto": concepto,
            "universo_documentado": universo,
            "n_valido": int(s["n_valido"]),
            "n_si": int(s["n_yes"]),
            "n_no": int(s["n_no"]),
            "masa_muestral_ponderada_valida": f'{s["masa_valida"]:.6f}',
            "masa_muestral_ponderada_si": f'{s["masa_yes"]:.6f}',
            "nivel_uso": "descriptivo_asociativo_no_causal",
        })
    return _csv_text(list(salida[0]), salida)


def _parsear_tabla_cfpb(texto: str) -> list[dict[str, object]]:
    inicio = texto.find("TABLE 3:      ORIGINATIONS AND DEFAULTS BY CREDIT SCORE CATEGORY")
    if inicio < 0:
        raise ValueError("CFPB: no se encontro el encabezado de Table 3")
    bloque = texto[inicio:texto.find("Note:", inicio)]
    patron = re.compile(
        r"^\s*(No Score|Deep Subprime|Subprime|Near Prime|Prime|Super-prime)"
        r"\s+(\d+\.\d+)%\s+(\d+\.\d+)%\s*$",
        re.MULTILINE,
    )
    obs = re.search(r"Observations\s+([\d,]+)", bloque)
    filas = [
        {
            "pais": "Estados_Unidos",
            "periodo": "2021-2022",
            "unidad": "originacion_bnpl_pay_in_four",
            "categoria_fico": m.group(1),
            "participacion_originaciones_pct": m.group(2),
            "tasa_default_pct": m.group(3),
            "observaciones_tabla": int(obs.group(1).replace(",", "")) if obs else 0,
            "ubicacion": "Table 3, pagina impresa 14",
            "nivel_uso": "asociativo_agregado_no_causal",
        }
        for m in patron.finditer(bloque)
    ]
    if len(filas) != 6 or not obs or filas[0]["observaciones_tabla"] != 892668:
        raise ValueError(f"CFPB: Table 3 incompleta: {filas!r}")
    return filas


def extraer_cfpb(path: Path = CFPB_PDF) -> str:
    if shutil.which("pdftotext") is None:
        raise RuntimeError("CFPB: falta pdftotext (poppler-utils)")
    proceso = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True, capture_output=True, text=True,
    )
    filas = _parsear_tabla_cfpb(proceso.stdout)
    return _csv_text(list(filas[0]), filas)


def tabla_candidatos() -> str:
    campos = [
        "candidato", "pais_periodo", "unidad", "producto_exposicion",
        "costo_condicion_friccion", "desenlace", "denominador", "nivel",
        "estado_bytes", "decision",
    ]
    filas = [
        {
            "candidato": "Banxico_satisfaccion_usuarios_2019_2024",
            "pais_periodo": "Mexico_2019_2024",
            "unidad": "persona_usuaria_ola",
            "producto_exposicion": "tarjeta_hipotecario_personal_nomina_automotriz",
            "costo_condicion_friccion": "percepcion_intereses_comisiones_y_facilidad_contrato",
            "desenlace": "pago_atraso_impago_problema_reclamacion_vulnerabilidad",
            "denominador": "tenedores_por_producto_con_ponderador",
            "nivel": "asociativo_potencial_no_causal",
            "estado_bytes": "OBTENIDO_MICRODATO_DICCIONARIO_INFORME",
            "decision": "PRIORIZADO_UTILIZABLE",
        },
        {
            "candidato": "Federal_Reserve_SHED_2025",
            "pais_periodo": "Estados_Unidos_2025",
            "unidad": "persona",
            "producto_exposicion": "BNPL_uso_ultimo_ano",
            "costo_condicion_friccion": "asequibilidad_cargo_extra_sobregiro_NSF",
            "desenlace": "atraso_BNPL_cargo_extra_sobregiro",
            "denominador": "12934_personas_y_subuniversos_con_weight",
            "nivel": "descriptivo_asociativo_no_causal_extranjero",
            "estado_bytes": "OBTENIDO_MICRODATO_CODEBOOK",
            "decision": "PRIORIZADO_MECANISMO_NO_TASA_MEXICANA",
        },
        {
            "candidato": "CFPB_BNPL_unsecured_debt_2025",
            "pais_periodo": "Estados_Unidos_2021_2022",
            "unidad": "originacion",
            "producto_exposicion": "pay_in_four_seis_firmas",
            "costo_condicion_friccion": "categoria_FICO",
            "desenlace": "default_120_dias",
            "denominador": "892668_originaciones_emparejadas",
            "nivel": "asociativo_agregado_no_causal_extranjero",
            "estado_bytes": "OBTENIDO_PDF_TABLA_SIN_MICRODATO",
            "decision": "UTIL_COMO_CORROBORACION_AGREGADA",
        },
        {
            "candidato": "Compartamos_AEJ_RCT",
            "pais_periodo": "Mexico_Nogales_experimento_publicado",
            "unidad": "mujer_18_60_en_conglomerado",
            "producto_exposicion": "oferta_aleatoria_credito_grupal_Compartamos",
            "costo_condicion_friccion": "no_observa_CAT_ni_reporte_buro",
            "desenlace": "mora_administrativa_y_venta_activos",
            "denominador": "16560_endline_238_conglomerados",
            "nivel": "causal_acreditado_estrecho_con_reservas",
            "estado_bytes": "YA_OBTENIDO_116334_v1_NO_REDESCARGADO",
            "decision": "REUTILIZAR_NO_DUPLICAR",
        },
        {
            "candidato": "CFPB_Making_Ends_Meet_PUF",
            "pais_periodo": "Estados_Unidos_2022",
            "unidad": "persona_mas_registro_crediticio",
            "producto_exposicion": "BNPL",
            "costo_condicion_friccion": "credito_tradicional_y_alto_interes",
            "desenlace": "delincuencia_estres_financiero",
            "denominador": "documentado_en_reporte_no_adquirido",
            "nivel": "asociativo_no_causal",
            "estado_bytes": "NO_OBTENIDO_ACEPTACION_TOS_REQUERIDA",
            "decision": "DESCARTADO_POR_COMPROMISO_NO_AUTORIZADO",
        },
        {
            "candidato": "Di_Maggio_Williams_Katz_BNPL_w30508",
            "pais_periodo": "Estados_Unidos_panel_privado",
            "unidad": "usuario_transaccion",
            "producto_exposicion": "BNPL_rollout",
            "costo_condicion_friccion": "baja_friccion_bajo_interes",
            "desenlace": "gasto_no_dano_financiero_directo",
            "denominador": "panel_no_publico",
            "nivel": "causal_en_paper_sin_datos_replicables_publicos",
            "estado_bytes": "NO_OBTENIDO_SIN_REPOSITORIO_PUBLICO_DE_DATOS",
            "decision": "DESCARTADO_PARA_ADQUISICION",
        },
    ]
    return _csv_text(campos, filas)


def construir() -> dict[Path, str]:
    return {
        SALIDAS["banxico"]: extraer_banxico(),
        SALIDAS["shed"]: extraer_shed(),
        SALIDAS["cfpb"]: extraer_cfpb(),
        SALIDAS["candidatos"]: tabla_candidatos(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifica", action="store_true",
                        help="reconstruye en memoria y compara con las tablas versionadas")
    args = parser.parse_args()
    generadas = construir()
    if args.verifica:
        distintas = []
        for path, texto in generadas.items():
            if not path.exists() or path.read_text(encoding="utf-8") != texto:
                distintas.append(str(path.relative_to(ROOT)))
        if distintas:
            print("NO-COINCIDE: " + ", ".join(distintas), file=sys.stderr)
            return 1
        print("COINCIDE: 4 tablas reproducidas byte a byte")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for path, texto in generadas.items():
        path.write_text(texto, encoding="utf-8")
        print(f"escrito {path.relative_to(ROOT)}: {texto.count(chr(10)) - 1} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
