#!/usr/bin/env python3
"""Extrae los objetos financieros de #717 y su continuación efectiva.

Lee exclusivamente payloads declarados en ``data/manifiesto.yaml`` y produce
tablas descriptivas.  No calibra el motor ni interpreta reclamaciones como
prevalencia entre clientes.

Uso:

    python3 tools/extrae_fuentes_financieras.py
    python3 tools/extrae_fuentes_financieras.py --verifica
    python3 tools/extrae_fuentes_financieras.py --salida /tmp/fuentes-20

``--verifica`` reconstruye cada CSV en memoria y exige igualdad byte a byte
con la salida versionada.  La raíz física nunca se escribe en las tablas: se
resuelve por el nombre lógico del manifiesto y ``data/raices.local.yaml``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
import sys
import unicodedata
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile

import yaml


RAIZ_REPO = Path(__file__).resolve().parents[1]
MANIFIESTO = RAIZ_REPO / "data" / "manifiesto.yaml"
RAICES_LOCAL = RAIZ_REPO / "data" / "raices.local.yaml"
SALIDA_PREDETERMINADA = RAIZ_REPO / "data" / "fuentes-financieras-20"
REGISTRO_ADQUISICION = (
    RAIZ_REPO / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv"
)
NO_CORRIDO = RAIZ_REPO / "forense" / "no-corrido.tsv"
ENCARGO_CONTINUACION = (
    "forense/encargos/"
    "2026-09-11-GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA.md"
)

ID_CNBV = "gen2_cnbv_040_1a_r16_imor_tipo_cartera"
ID_BANXICO_IMOR = "gen2_banxico_imor_consumo_producto_mensual_2026t1_html"
ID_ENCRIGE_DATOS = "conjunto_de_datos_encrige_2020_csv"
ID_ENSAFI_DATOS = "ensafi2023_bd_csv_zip"
ID_ENSAFI_FD = "ensafi2023_fd_xlsx_zip"
ID_ENSAFI_CUESTIONARIO = "ensafi2023_cuestionario_pdf"
ID_ENSAFI_DISENO = "gen2_ensafi2023_diseno_muestral"
ID_ENSAFI_RESULTADOS = "gen2_ensafi2023_presentacion_resultados"
PREFIJO_CONDUSEF = "A6_CONDUSEF_DATOS_ABIERTOS/"
CARPETA_CONDUSEF = "condusef_redeco_reune/"

URL_CNBV = (
    "https://portafolioinfdoctos.cnbv.gob.mx/Documentacion/"
    "minfo/XLS/40/040_1a_R16.xls"
)
URL_BANXICO_IMOR = (
    "https://www.banxico.org.mx/TablasWeb/informes-trimestrales/"
    "enero-marzo-2026/B133C3DC-462F-40C1-B2BA-04086A1CFAB1.html"
)


def carga_manifiesto(path: Path = MANIFIESTO) -> list[dict]:
    datos = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(datos, list):
        raise ValueError("data/manifiesto.yaml no es una lista")
    return [x for x in datos if isinstance(x, dict)]


def mapa_raices() -> dict[str, Path]:
    raices = {"data_raw": RAIZ_REPO / "data" / "raw"}
    if RAICES_LOCAL.exists():
        locales = yaml.safe_load(RAICES_LOCAL.read_text(encoding="utf-8")) or {}
        for nombre, ruta in locales.items():
            if nombre == "data_raw" or not ruta:
                continue
            raices[str(nombre)] = Path(str(ruta)).expanduser()
    return raices


def indice_por_id(entradas: Iterable[dict]) -> dict[str, dict]:
    salida: dict[str, dict] = {}
    for entrada in entradas:
        identificador = entrada.get("id")
        if not identificador:
            continue
        if identificador in salida:
            raise ValueError(f"id duplicado en manifiesto: {identificador}")
        salida[identificador] = entrada
    return salida


def ruta_payload(entrada: dict, raices: dict[str, Path]) -> Path:
    archivo = entrada.get("archivo")
    if not archivo:
        raise ValueError(f"entrada sin archivo: {entrada.get('id')}")
    nombre_raiz = str(entrada.get("raiz") or "data_raw")
    if nombre_raiz not in raices:
        raise FileNotFoundError(f"raíz {nombre_raiz!r} no configurada")
    ruta = raices[nombre_raiz] / str(archivo)
    if not ruta.is_file():
        raise FileNotFoundError(f"payload ausente para {entrada.get('id')}: {ruta}")
    return ruta


def verifica_payload(entrada: dict, ruta: Path) -> None:
    esperado = entrada.get("sha256")
    if not esperado:
        raise ValueError(f"payload sin sha256: {entrada.get('id')}")
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != esperado:
        raise ValueError(
            f"sha256 distinto para {entrada.get('id')}: {real} != {esperado}"
        )
    tamano = entrada.get("tamano_bytes")
    if tamano is not None and ruta.stat().st_size != int(tamano):
        raise ValueError(f"tamaño distinto para {entrada.get('id')}")


def decodifica_csv(contenido: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            return contenido.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", contenido, 0, 1, "codificación no reconocida")


def lee_csv(ruta: Path) -> tuple[list[str], list[list[str]], str]:
    texto, encoding = decodifica_csv(ruta.read_bytes())
    lector = csv.reader(io.StringIO(texto, newline=""))
    filas = list(lector)
    if not filas:
        raise ValueError(f"CSV vacío: {ruta}")
    return filas[0], filas[1:], encoding


def lee_csv_dicts(ruta: Path) -> tuple[list[str], list[dict[str, str]]]:
    texto, _ = decodifica_csv(ruta.read_bytes())
    lector = csv.DictReader(io.StringIO(texto, newline=""))
    if lector.fieldnames is None:
        raise ValueError(f"CSV sin cabecera: {ruta}")
    filas = []
    for numero, fila in enumerate(lector, start=2):
        if None in fila:
            raise ValueError(f"fila {numero} más ancha que cabecera en {ruta.name}")
        filas.append({str(k): (v or "").strip() for k, v in fila.items()})
    return list(lector.fieldnames), filas


def texto_normalizado(valor: str) -> str:
    return " ".join(valor.strip().casefold().split())


def texto_sin_acentos(valor: str) -> str:
    base = unicodedata.normalize("NFKD", texto_normalizado(valor))
    return "".join(c for c in base if not unicodedata.combining(c))


def decimal(valor: str) -> Decimal:
    limpio = valor.strip().replace(",", "")
    if not limpio:
        return Decimal(0)
    try:
        return Decimal(limpio)
    except InvalidOperation as exc:
        raise ValueError(f"valor no numérico: {valor!r}") from exc


def entero_conteo(valor: str) -> int:
    numero = decimal(valor)
    if numero != numero.to_integral_value():
        raise ValueError(f"conteo no entero: {valor!r}")
    if numero < 0:
        raise ValueError(f"conteo negativo: {valor!r}")
    return int(numero)


def porcentaje(numerador: Decimal | int, denominador: Decimal | int) -> str:
    den = Decimal(denominador)
    if den == 0:
        return ""
    valor = Decimal(numerador) * Decimal(100) / den
    return f"{valor:.10f}".rstrip("0").rstrip(".")


def asegura_unicos(filas: Iterable[dict], campos: tuple[str, ...], objeto: str) -> None:
    vistos: set[tuple[str, ...]] = set()
    for fila in filas:
        llave = tuple(str(fila[c]) for c in campos)
        if llave in vistos:
            raise ValueError(f"llave duplicada en {objeto}: {llave}")
        vistos.add(llave)


class _TablasHTML(HTMLParser):
    """Extrae texto de celdas conservando el orden de cada fila HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.filas: list[list[str]] = []
        self._fila: list[str] | None = None
        self._celda: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() == "tr":
            self._fila = []
        elif tag.casefold() in {"td", "th"} and self._fila is not None:
            self._celda = []

    def handle_data(self, data: str) -> None:
        if self._celda is not None:
            self._celda.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"td", "th"} and self._celda is not None:
            assert self._fila is not None
            self._fila.append(" ".join("".join(self._celda).split()))
            self._celda = None
        elif tag.casefold() == "tr" and self._fila is not None:
            if self._fila:
                self.filas.append(self._fila)
            self._fila = None


MESES_ES = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
}


def periodo_banxico(valor: str) -> str:
    pareja = re.fullmatch(r"([a-záéíóú]{3})-(\d{2})", texto_sin_acentos(valor))
    if not pareja or pareja.group(1) not in MESES_ES:
        raise ValueError(f"periodo Banxico inesperado: {valor!r}")
    return f"20{pareja.group(2)}-{MESES_ES[pareja.group(1)]:02d}"


def periodos_mensuales(inicio: str, fin: str) -> list[str]:
    ano, mes = map(int, inicio.split("-"))
    ano_fin, mes_fin = map(int, fin.split("-"))
    salida = []
    while (ano, mes) <= (ano_fin, mes_fin):
        salida.append(f"{ano:04d}-{mes:02d}")
        mes += 1
        if mes == 13:
            ano += 1
            mes = 1
    return salida


def extrae_banxico_imor(
    entrada: dict, raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    """Lee la tabla oficial equivalente de Banxico, no la plantilla R16."""
    ruta = ruta_payload(entrada, raices)
    verifica_payload(entrada, ruta)
    texto = ruta.read_text(encoding="utf-8")
    texto_norm = texto_sin_acentos(texto)
    for marca in (
        "a partir de enero de 2022",
        "saldo de la cartera clasificada como etapa 3",
        "sofomes er subsidiarias",
        "se excluyen los datos de ci banco",
    ):
        if marca not in texto_norm:
            raise ValueError(f"la publicación Banxico perdió la nota metodológica: {marca}")

    parser = _TablasHTML()
    parser.feed(texto)
    filas_fuente = [
        fila for fila in parser.filas
        if len(fila) == 12 and re.fullmatch(r"[a-záéíóú]{3}-\d{2}", fila[0].casefold())
    ]
    if not filas_fuente:
        raise ValueError("no se localizaron meses en la tabla Banxico")
    periodos = [periodo_banxico(fila[0]) for fila in filas_fuente]
    if periodos != periodos_mensuales(periodos[0], periodos[-1]):
        raise ValueError("la tabla Banxico tiene meses duplicados, faltantes o fuera de orden")
    if (periodos[0], periodos[-1]) != ("2016-01", "2026-03"):
        raise ValueError(f"cobertura Banxico inesperada: {periodos[0]}..{periodos[-1]}")

    productos = [
        (7, "Consumo total"),
        (8, "Tarjetas de crédito"),
        (9, "ABCD"),
        (10, "Nómina"),
        (11, "Personales"),
    ]
    salida = []
    for periodo, fila in zip(periodos, filas_fuente, strict=True):
        regimen = "IFRS9_ETAPA_3" if periodo >= "2022-01" else "PRE_IFRS9_CARTERA_VENCIDA"
        numerador = (
            "saldo de cartera clasificada como etapa 3"
            if regimen == "IFRS9_ETAPA_3" else
            "saldo de cartera vencida"
        )
        for indice, producto in productos:
            valor_texto = fila[indice].strip()
            if not valor_texto:
                valor = ""
                faltante = "faltante en el original; no se imputa ni se convierte a cero"
            else:
                valor_decimal = decimal(valor_texto)
                if valor_decimal < 0 or valor_decimal > 100:
                    raise ValueError(f"IMOR Banxico fuera de 0..100: {valor_decimal}")
                valor = str(valor_decimal)
                faltante = "sin faltante"
            salida.append({
                "fecha": periodo,
                "producto": producto,
                "indicador": "IMOR",
                "numerador": numerador,
                "denominador": "saldo de la cartera total del mismo producto",
                "valor": valor,
                "unidad": "porcentaje",
                "frecuencia": "mensual",
                "universo_institucional": (
                    "banca comercial; incluye Sofomes ER subsidiarias de instituciones "
                    "bancarias y grupos financieros; excluye CI Banco"
                ),
                "regimen_definicion": regimen,
                "fuente": ID_BANXICO_IMOR,
                "nota": (
                    f"publicación oficial equivalente, no R16 CNBV; {faltante}; "
                    f"ABCD incluye bienes muebles y automotriz; URL {URL_BANXICO_IMOR}"
                ),
            })
    asegura_unicos(salida, ("fecha", "producto"), "IMOR Banxico")
    return list(salida[0]), salida


def lee_csv_zip_dicts(zipf: ZipFile, nombre: str) -> list[dict[str, str]]:
    candidatos = [n for n in zipf.namelist() if Path(n).name == nombre]
    if len(candidatos) != 1:
        raise ValueError(f"se esperaba un {nombre} en ENSAFI; hay {candidatos}")
    texto, _encoding = decodifica_csv(zipf.read(candidatos[0]))
    lector = csv.DictReader(io.StringIO(texto, newline=""))
    if lector.fieldnames is None:
        raise ValueError(f"{nombre} sin cabecera")
    return [
        {str(k): (v or "").strip() for k, v in fila.items()}
        for fila in lector
    ]


def resumen_ponderado(
    filas: list[dict[str, str]],
    campo_peso: str,
    es_denominador,
    es_numerador,
) -> dict[str, str]:
    denominador = [fila for fila in filas if es_denominador(fila)]
    numerador = [fila for fila in denominador if es_numerador(fila)]
    pesos_den = sum((decimal(fila[campo_peso]) for fila in denominador), Decimal(0))
    pesos_num = sum((decimal(fila[campo_peso]) for fila in numerador), Decimal(0))
    if pesos_den <= 0:
        raise ValueError("denominador ENSAFI vacío o sin peso positivo")
    return {
        "n_muestra_denominador": str(len(denominador)),
        "masa_expandida_denominador": str(pesos_den),
        "n_muestra_numerador": str(len(numerador)),
        "masa_expandida_numerador": str(pesos_num),
        "porcentaje_ponderado": porcentaje(pesos_num, pesos_den),
    }


def extrae_ensafi_hogar(
    entrada: dict, raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    ruta = ruta_payload(entrada, raices)
    verifica_payload(entrada, ruta)
    with ZipFile(ruta) as zipf:
        if zipf.testzip() is not None:
            raise ValueError("ZIP ENSAFI corrupto")
        filas = lee_csv_zip_dicts(zipf, "THOGAR.csv")
    if len({fila["LLAVEHOG"] for fila in filas}) != len(filas):
        raise ValueError("LLAVEHOG duplicada en ENSAFI")
    productos = [
        (1, "tarjeta o crédito bancario, financiero o de tienda departamental"),
        (2, "caja de ahorro, familiares o amistades"),
        (3, "casa de empeño"),
        (4, "prestamistas o agiotistas"),
    ]
    salida = []
    for indice, producto in productos:
        deuda = f"P4_7_{indice}"
        atraso = f"P4_8_{indice}"
        expuestos = [fila for fila in filas if fila[deuda] == "1"]
        desconocidos = [fila for fila in expuestos if fila[atraso] == "9"]
        resumen = resumen_ponderado(
            filas,
            "FAC_HOG",
            lambda fila, d=deuda, a=atraso: fila[d] == "1" and fila[a] in {"1", "2"},
            lambda fila, a=atraso: fila[a] == "1",
        )
        salida.append({
            "periodo": "último mes antes de la entrevista de 2023",
            "unidad_observacion": "hogar",
            "poblacion": "hogares en México con la clase de deuda indicada",
            "producto_clase": producto,
            "dano": "atraso en el pago de esa deuda",
            "variable_exposicion": deuda,
            "variable_dano": atraso,
            "n_muestra_expuestos": str(len(expuestos)),
            "n_muestra_dano_desconocido": str(len(desconocidos)),
            **resumen,
            "factor_expansion": "FAC_HOG",
            "escala": "porcentaje de hogares expuestos con respuesta sí/no válida",
            "fuente": ID_ENSAFI_DATOS,
            "uso": "prevalencia descriptiva poblacional por clase amplia de deuda",
            "limite": (
                "no identifica institución, CAT, BNPL ni causalidad; la clase formal agrupa "
                "banco, institución financiera y tienda; los cuatro renglones no son excluyentes"
            ),
        })
    asegura_unicos(salida, ("producto_clase",), "ENSAFI hogar")
    return list(salida[0]), salida


def extrae_ensafi_persona(
    entrada: dict, raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    ruta = ruta_payload(entrada, raices)
    verifica_payload(entrada, ruta)
    with ZipFile(ruta) as zipf:
        if zipf.testzip() is not None:
            raise ValueError("ZIP ENSAFI corrupto")
        filas = lee_csv_zip_dicts(zipf, "TMODULO.csv")
    if len({fila["LLAVEMOD"] for fila in filas}) != len(filas):
        raise ValueError("LLAVEMOD duplicada en ENSAFI")

    salida = []
    deuda = resumen_ponderado(
        filas,
        "FAC_ELE",
        lambda fila: fila["P6_8"] in {"1", "2", "3", "4"},
        lambda fila: fila["P6_7"] == "1",
    )
    if Decimal(deuda["porcentaje_ponderado"]).quantize(Decimal("0.1")) != Decimal("27.3"):
        raise ValueError("el atraso ENSAFI no reproduce el 27.3% oficial")
    salida.append({
        "periodo": "sin periodo de referencia explícito para P6_7; levantamiento 2023",
        "unidad_observacion": "persona de 18 años y más seleccionada",
        "poblacion_denominador": "personas que declararon deuda excesiva, alta, moderada o baja (P6_8=1..4)",
        "estimando": "se ha atrasado en uno de sus préstamos o créditos",
        "variable_numerador": "P6_7=1 y P6_8=1..4",
        "variable_denominador": "P6_8=1..4",
        **deuda,
        "factor_expansion": "FAC_ELE",
        "escala": "porcentaje ponderado",
        "contraste_publicado": "27.3",
        "fuente": ID_ENSAFI_DATOS,
        "uso": "prevalencia descriptiva poblacional de atraso entre personas con deuda",
        "limite": "P6_7 no identifica cuál producto se atrasó ni establece que baja fricción o tasa usuraria causó el atraso",
    })

    estrategias = [
        (1, "pidió prestado a familiares o amistades"),
        (2, "utilizó ahorros"),
        (3, "redujo gastos"),
        (4, "vendió o empeñó algún bien"),
        (5, "solicitó adelanto salarial, horas extra o trabajo temporal"),
        (6, "usó tarjeta o solicitó crédito formal/de tienda"),
        (7, "se atrasó en el pago de un crédito o préstamo"),
        (8, "pidió a cajas de ahorro, prestamistas o agiotistas"),
    ]
    for indice, estrategia in estrategias:
        variable = f"P6_10_{indice}"
        resumen = resumen_ponderado(
            filas,
            "FAC_ELE",
            lambda fila, v=variable: fila["P6_9"] == "2" and fila[v] in {"1", "2"},
            lambda fila, v=variable: fila[v] == "1",
        )
        salida.append({
            "periodo": "último mes antes de la entrevista de 2023",
            "unidad_observacion": "persona de 18 años y más seleccionada",
            "poblacion_denominador": "personas cuyo ingreso no alcanzó para cubrir gastos sin endeudarse (P6_9=2)",
            "estimando": estrategia,
            "variable_numerador": f"{variable}=1 y P6_9=2",
            "variable_denominador": "P6_9=2; respuesta válida sí/no en P6_10",
            **resumen,
            "factor_expansion": "FAC_ELE",
            "escala": "porcentaje ponderado",
            "contraste_publicado": "",
            "fuente": ID_ENSAFI_DATOS,
            "uso": "respuesta descriptiva ante insuficiencia de ingreso; categorías múltiples",
            "limite": "no atribuye la estrategia a un producto concreto ni identifica un efecto causal de crédito de baja fricción/usura",
        })
    asegura_unicos(salida, ("estimando",), "ENSAFI persona")
    return list(salida[0]), salida


def clasifica_condusef(archivo: str) -> tuple[str, str, str]:
    nombre = archivo.casefold()
    casos = [
        ("acciones_defensa", "acciones de atención/defensa", "Los canales pueden ser etapas superpuestas; no se suman como expedientes únicos."),
        ("indice_reclamacion", "índice publicado por institución", "El CSV no documenta el denominador del índice; se inventaría una tasa si se reconstruyera."),
        ("instituciones_mas_reclamadas", "reclamaciones por institución y sistema", "Conteos administrativos; no hay denominador de clientes ni causa de reclamación."),
        ("evaluacion_producto", "reclamaciones por institución-producto", "El corte temporal no está dentro del CSV; las ediciones no forman una serie comparable."),
        ("sanciones", "sanciones por clase", "Sanción firme no equivale a reclamación ni a hecho judicial individual."),
        ("herramientas_web", "accesos a herramientas", "Accesos web, no personas ni reclamaciones."),
        ("comportamiento_general", "ficha BEF por institución", "Mezcla conteos, índices y calificaciones; no se suman columnas heterogéneas."),
        ("plan_apertura", "catálogo administrativo", "Metadato de publicación, no observaciones de usuarios."),
        ("seguro_automovil", "cotizaciones/registro de seguro de automóvil", "Oferta por institución y estado, no reclamaciones."),
        ("seguro_vida", "cotizaciones/registro de seguro de vida", "Oferta por institución y perfil, no reclamaciones."),
        ("calificaciones_producto", "supervisión por producto", "Calificación de supervisión, no frecuencia entre contratos o clientes."),
        ("clausulas_abusivas", "cláusulas observadas en supervisión", "Casos contractuales identificados; no prevalencia ni prueba de usura."),
        ("observaciones_producto", "observaciones de supervisión", "Observaciones a documentos, no reclamaciones de usuarios."),
        ("despachos_cobranza", "directorio REDECO de despachos", "Directorio de prestadores; no contiene quejas, causas ni actos de cobranza."),
        ("redeco_datosabiertos", "directorio REDECO de despachos", "Directorio de prestadores; no contiene quejas, causas ni actos de cobranza."),
        ("reune_unidades", "directorio REUNE de unidades especializadas", "Directorio de contacto; no contiene reclamaciones."),
        ("unidades_especializadas", "directorio de unidades especializadas", "Directorio de contacto; no contiene reclamaciones."),
    ]
    for aguja, unidad, limite in casos:
        if aguja in nombre:
            return aguja, unidad, limite
    return "otro", "unidad declarada por columnas", "Requiere lectura de columnas antes de agregar."


def periodo_inventario(archivo: str, cabecera: list[str], filas: list[list[str]]) -> str:
    if "periodo" in cabecera:
        indice = cabecera.index("periodo")
        valores = sorted(
            {r[indice].strip().removesuffix(".0") for r in filas if len(r) > indice and r[indice].strip()}
        )
        return "|".join(valores)
    nombre = archivo.casefold()
    patrones = [
        (r"30_09_25", "corte_en_nombre:2025-09-30"),
        (r"1ertrim_2026", "corte_en_nombre:2026T1"),
        (r"310326", "corte_en_nombre:2026-03-31"),
        (r"30sept2025", "corte_en_nombre:2025-09-30"),
        (r"julio_2025", "corte_en_nombre:2025-07"),
        (r"3trimestre[s]?_?(?:20)?25", "corte_en_nombre:2025T3"),
        (r"4trimestre[s]?_?(?:20)?25|4t2025", "corte_en_nombre:2025T4"),
        (r"4_trim_26", "edicion_en_nombre:4_trim_26; periodo_no_incluido"),
    ]
    for patron, rotulo in patrones:
        if re.search(patron, nombre):
            return rotulo
    return "NO_INCLUIDO_EN_CSV"


def inventario_condusef(
    entradas: list[dict], raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    filas_salida = []
    for entrada in sorted(entradas, key=lambda x: str(x["archivo"])):
        ruta = ruta_payload(entrada, raices)
        verifica_payload(entrada, ruta)
        cabecera, filas, encoding = lee_csv(ruta)
        anchos = [len(f) for f in filas] or [len(cabecera)]
        categoria, unidad, limite = clasifica_condusef(str(entrada["archivo"]))
        filas_salida.append(
            {
                "id_manifiesto": entrada["id"],
                "archivo": entrada["archivo"],
                "sha256": entrada["sha256"],
                "tamano_bytes": str(entrada.get("tamano_bytes", ruta.stat().st_size)),
                "filas_datos": str(len(filas)),
                "columnas_cabecera": str(len(cabecera)),
                "ancho_minimo": str(min(anchos)),
                "ancho_maximo": str(max(anchos)),
                "filas_ancho_distinto": str(sum(len(f) != len(cabecera) for f in filas)),
                "encoding": encoding,
                "categoria": categoria,
                "periodo_o_corte": periodo_inventario(str(entrada["archivo"]), cabecera, filas),
                "unidad_observada": unidad,
                "columnas": "|".join(c.replace("\n", " ").strip() for c in cabecera),
                "limite_interpretacion": limite,
            }
        )
    campos = list(filas_salida[0])
    asegura_unicos(filas_salida, ("id_manifiesto",), "inventario CONDUSEF")
    return campos, filas_salida


def entradas_categoria(entradas: list[dict], categoria: str) -> list[dict]:
    return [
        e for e in entradas
        if clasifica_condusef(str(e.get("archivo", "")))[0] == categoria
    ]


def agrega_acciones(
    entradas: list[dict], raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    conteos: defaultdict[tuple[str, str, str, str], int] = defaultdict(int)
    unidades: defaultdict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    for entrada in entradas_categoria(entradas, "acciones_defensa"):
        ruta = ruta_payload(entrada, raices)
        cabecera, filas = lee_csv_dicts(ruta)
        canales = [c for c in cabecera if c == "asesorias" or c.startswith("reclamaciones_")]
        if not canales:
            raise ValueError(f"sin canales de acción en {ruta.name}")
        campo_unidad = "delegacion" if "delegacion" in cabecera else "unidad_atencion"
        for fila in filas:
            periodo = fila["periodo"].removesuffix(".0")
            sector = texto_normalizado(fila["sector"])
            clase = texto_normalizado(fila["clase"])
            unidad = texto_normalizado(fila[campo_unidad])
            for canal in canales:
                llave = (periodo, sector, clase, canal)
                conteos[llave] += entero_conteo(fila[canal])
                unidades[llave].add(unidad)
    totales: defaultdict[tuple[str, str], int] = defaultdict(int)
    for (periodo, _sector, _clase, canal), cuenta in conteos.items():
        totales[(periodo, canal)] += cuenta
    salida = []
    for llave in sorted(conteos):
        periodo, sector, clase, canal = llave
        cuenta = conteos[llave]
        salida.append(
            {
                "periodo": periodo,
                "sector": sector,
                "clase": clase,
                "canal_accion": canal,
                "conteo": str(cuenta),
                "n_unidades_atencion": str(len(unidades[llave])),
                "participacion_dentro_periodo_canal_pct": porcentaje(cuenta, totales[(periodo, canal)]),
                "unidad": "acciones administrativas registradas",
                "nota": "distribución dentro del mismo canal; los canales pueden superponerse y no se suman como casos únicos",
            }
        )
    asegura_unicos(salida, ("periodo", "sector", "clase", "canal_accion"), "acciones CONDUSEF")
    return list(salida[0]), salida


def agrega_reclamaciones_clase(
    entradas: list[dict], raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    conteos: defaultdict[tuple[str, str, str, str], int] = defaultdict(int)
    instituciones_archivo: defaultdict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    instituciones_positivas: defaultdict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    llaves_institucion: set[tuple[str, str, str, str]] = set()
    for entrada in entradas_categoria(entradas, "instituciones_mas_reclamadas"):
        ruta = ruta_payload(entrada, raices)
        _cabecera, filas = lee_csv_dicts(ruta)
        for fila in filas:
            periodo = fila["periodo"].removesuffix(".0")
            sector = texto_normalizado(fila["sector"])
            clase = texto_normalizado(fila["clase"])
            institucion = texto_normalizado(fila["instituciones"])
            llave_inst = (periodo, sector, clase, institucion)
            if llave_inst in llaves_institucion:
                raise ValueError(f"institución duplicada en cortes CONDUSEF: {llave_inst}")
            llaves_institucion.add(llave_inst)
            condusef = entero_conteo(fila["reclamaciones_condusef"])
            reune = entero_conteo(fila["reclamaciones_reune"])
            total = entero_conteo(fila["total_reclamaciones"])
            if condusef + reune != total:
                raise ValueError(f"total superpuesto/inconsistente en {llave_inst}")
            for sistema, cuenta in (("CONDUSEF", condusef), ("REUNE", reune)):
                llave = (periodo, sistema, sector, clase)
                conteos[llave] += cuenta
                instituciones_archivo[llave].add(institucion)
                if cuenta > 0:
                    instituciones_positivas[llave].add(institucion)
    totales: defaultdict[tuple[str, str], int] = defaultdict(int)
    for (periodo, sistema, _sector, _clase), cuenta in conteos.items():
        totales[(periodo, sistema)] += cuenta
    salida = []
    for llave in sorted(conteos):
        periodo, sistema, sector, clase = llave
        cuenta = conteos[llave]
        salida.append(
            {
                "periodo": periodo,
                "sistema_registro": sistema,
                "sector": sector,
                "clase": clase,
                "conteo_reclamaciones": str(cuenta),
                "n_instituciones_archivo": str(len(instituciones_archivo[llave])),
                "n_instituciones_con_conteo": str(len(instituciones_positivas[llave])),
                "participacion_dentro_periodo_sistema_pct": porcentaje(cuenta, totales[(periodo, sistema)]),
                "unidad": "reclamaciones registradas",
                "nota": "CONDUSEF y REUNE se mantienen separados; sin denominador de clientes y sin causa en estos CSV",
            }
        )
    asegura_unicos(salida, ("periodo", "sistema_registro", "sector", "clase"), "reclamaciones CONDUSEF")
    return list(salida[0]), salida


def agrega_reclamaciones_producto(
    entradas: list[dict], raices: dict[str, Path]
) -> tuple[list[str], list[dict]]:
    conteos: defaultdict[tuple[str, str, str], int] = defaultdict(int)
    instituciones: defaultdict[tuple[str, str, str], set[str]] = defaultdict(set)
    for entrada in entradas_categoria(entradas, "evaluacion_producto"):
        ruta = ruta_payload(entrada, raices)
        _cabecera, filas = lee_csv_dicts(ruta)
        edicion = ruta.stem
        for fila in filas:
            sector = texto_normalizado(fila["sector"])
            producto = texto_normalizado(fila["producto"])
            llave = (edicion, sector, producto)
            conteos[llave] += entero_conteo(fila["total_reclamacion"])
            instituciones[llave].add(texto_normalizado(fila["institucion"]))
    totales: defaultdict[str, int] = defaultdict(int)
    for (edicion, _sector, _producto), cuenta in conteos.items():
        totales[edicion] += cuenta
    salida = []
    for llave in sorted(conteos):
        edicion, sector, producto = llave
        cuenta = conteos[llave]
        salida.append(
            {
                "edicion_archivo": edicion,
                "periodo": "NO_INCLUIDO_EN_CSV",
                "sector": sector,
                "producto": producto,
                "conteo_reclamaciones": str(cuenta),
                "n_instituciones": str(len(instituciones[llave])),
                "participacion_dentro_edicion_pct": porcentaje(cuenta, totales[edicion]),
                "unidad": "reclamaciones por institución-producto",
                "nota": "corte temporal ausente del payload; comparar ediciones como serie sería una inferencia no documentada",
            }
        )
    asegura_unicos(salida, ("edicion_archivo", "sector", "producto"), "productos CONDUSEF")
    return list(salida[0]), salida


def periodo_cnbv(valor: object) -> str:
    if isinstance(valor, float) and valor.is_integer():
        texto = str(int(valor))
    else:
        texto = str(valor).strip()
    if not re.fullmatch(r"\d{6}", texto) or not 1 <= int(texto[4:]) <= 12:
        raise ValueError(f"periodo CNBV inesperado: {valor!r}")
    return f"{texto[:4]}-{texto[4:]}"


def valida_filas_imor(filas: list[dict]) -> None:
    asegura_unicos(filas, ("fecha", "producto_universo"), "IMOR CNBV")
    for fila in filas:
        if fila["unidad"] != "porcentaje":
            raise ValueError("IMOR debe permanecer en porcentaje, no en fracción")
        if fila["valor"]:
            valor = decimal(fila["valor"])
            if valor < 0 or valor > 100:
                raise ValueError(f"IMOR fuera de 0..100: {valor}")
        elif "faltante" not in texto_sin_acentos(fila["notas"]):
            raise ValueError("un valor vacío debe quedar rotulado como faltante")


def extrae_cnbv(entrada: dict, raices: dict[str, Path]) -> tuple[list[str], list[dict]]:
    try:
        import xlrd
    except ImportError as exc:  # pragma: no cover - mensaje de operación
        raise RuntimeError("falta xlrd; instalar requirements.txt") from exc
    ruta = ruta_payload(entrada, raices)
    verifica_payload(entrada, ruta)
    libro = xlrd.open_workbook(str(ruta), on_demand=True)
    hoja = libro.sheet_by_name("MINFO")
    if texto_sin_acentos(str(hoja.cell_value(7, 1))) != "cifras expresadas en porcentajes":
        raise ValueError("la plantilla CNBV dejó de declarar porcentajes")
    universo = str(hoja.cell_value(8, 2)).strip()
    fecha = periodo_cnbv(hoja.cell_value(9, 2))
    filas = []
    dentro_consumo = False
    for numero in range(hoja.nrows):
        etiqueta = " ".join(str(hoja.cell_value(numero, 1)).split())
        etiqueta_norm = texto_sin_acentos(etiqueta)
        if etiqueta_norm == "imor cartera total de consumo":
            dentro_consumo = True
        if etiqueta_norm == "imor cartera total de vivienda":
            break
        if not dentro_consumo or not etiqueta_norm.startswith("imor "):
            continue
        producto = re.sub(r"^IMOR\s+", "", etiqueta, flags=re.IGNORECASE)
        celda = hoja.cell_value(numero, 2)
        faltante = celda == "" or celda is None
        valor = "" if faltante else str(celda)
        filas.append(
            {
                "fecha": fecha,
                "producto_universo": producto,
                "indicador": "IMOR = cartera vencida / cartera total del segmento",
                "valor": valor,
                "unidad": "porcentaje",
                "fuente": ID_CNBV,
                "notas": (
                    "faltante en el original; CNBV indica que vacío significa no reportado, no cero"
                    if faltante else
                    f"{universo}; foto cacheada del XLS, no serie histórica pública; URL {URL_CNBV}"
                ),
            }
        )
    libro.release_resources()
    if not filas or texto_sin_acentos(filas[0]["producto_universo"]) != "cartera total de consumo":
        raise ValueError("no se localizó el bloque de consumo en MINFO")
    valida_filas_imor(filas)
    return list(filas[0]), filas


def csv_en_zip(zipf: ZipFile, base: str) -> list[list[str]]:
    candidatos = [
        n for n in zipf.namelist()
        if "I_Cumplimiento_de_contratos_2020" in n and n.endswith("/" + base)
    ]
    if len(candidatos) != 1:
        raise ValueError(f"se esperaba un {base} de cumplimiento; hay {candidatos}")
    texto = zipf.read(candidatos[0]).decode("cp1252")
    return list(csv.reader(io.StringIO(texto, newline="")))


def fila_nacional(tabla: list[list[str]], nombre: str) -> list[str]:
    filas = [f for f in tabla[1:] if f and f[0].strip() == "Estados Unidos Mexicanos"]
    if len(filas) != 1:
        raise ValueError(f"fila nacional no única en {nombre}")
    return filas[0]


def registro_encrige(
    tabla: str,
    reactivo: str,
    universo: str,
    indicador: str,
    denominador: str,
    numerador: str,
    publicado: str,
    nota: str,
) -> dict:
    calculado = Decimal(numerador) * Decimal(100) / Decimal(denominador)
    if abs(calculado - Decimal(publicado)) > Decimal("0.0000001"):
        raise ValueError(f"porcentaje publicado inconsistente en {tabla}/{indicador}")
    return {
        "periodo": "2020",
        "tabla": tabla,
        "reactivo": reactivo,
        "actor_observado": "empresa encuestada frente a contrapartes privadas",
        "universo": universo,
        "indicador": indicador,
        "denominador_expandido": denominador,
        "numerador_expandido": numerador,
        "porcentaje_publicado": publicado,
        "unidad": "estimación ponderada de unidades económicas / porcentaje",
        "ponderacion_diseno": "factor de expansión = inverso de probabilidad; ajuste por no respuesta en dominio-estrato; diseño probabilístico estratificado",
        "fuente": ID_ENCRIGE_DATOS,
        "nota": nota,
    }


def extrae_encrige(entrada: dict, raices: dict[str, Path]) -> tuple[list[str], list[dict]]:
    ruta = ruta_payload(entrada, raices)
    verifica_payload(entrada, ruta)
    with ZipFile(ruta) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP ENCRIGE corrupto")
        t15 = fila_nacional(csv_en_zip(z, "t1_5.csv"), "t1_5")
        t19 = fila_nacional(csv_en_zip(z, "t1_9.csv"), "t1_9")
        t115 = fila_nacional(csv_en_zip(z, "t1_15.csv"), "t1_15")
        t119 = fila_nacional(csv_en_zip(z, "t1_19.csv"), "t1_19")
    filas = [
        registro_encrige(
            "t1_5", "4.2",
            "empresas privadas con instalaciones fijas; incluye micro; nacional",
            "tuvo problemas de cobranza o incumplimiento de contratos",
            t15[1], t15[2], t15[3],
            "incluye contraparte inversionista, proveedora, compradora, arrendataria u otra; excluye 140 513 no sabe/no responde del reparto sí/no",
        ),
        registro_encrige(
            "t1_9", "4.3 (acuerdo entre particulares)",
            "empresas que reportaron problemas de cobranza/incumplimiento; nacional",
            "recurrió a acuerdo entre particulares",
            t19[1], t19[2], t19[4],
            "mecanismo de resolución declarado por la empresa; no identifica crédito al consumo ni daño al deudor",
        ),
        registro_encrige(
            "t1_15", "4.3 (tribunales)",
            "empresas pequeñas, medianas y grandes; excluye micro; nacional",
            "tuvo problemas de cobranza o incumplimiento de contratos",
            t115[1], t115[2], t115[3],
            "subuniverso distinto de t1_5: INEGI excluye micro por variabilidad alta",
        ),
        registro_encrige(
            "t1_15", "4.3 (tribunales)",
            "empresas pequeñas, medianas y grandes con problemas; excluye micro; nacional",
            "acudió a tribunales",
            t115[2], t115[4], t115[5],
            "no es un hecho judicial del consumidor; es el mecanismo declarado por la empresa encuestada",
        ),
        registro_encrige(
            "t1_19", "4.4 (juicio)",
            "empresas pequeñas, medianas y grandes que acudieron a tribunales; nacional",
            "reportó juicio mercantil",
            t119[1], t119[2], t119[3],
            "respuesta múltiple; incluye juicio oral, ejecutivo u ordinario mercantil",
        ),
        registro_encrige(
            "t1_19", "4.4 (conciliación)",
            "empresas pequeñas, medianas y grandes que acudieron a tribunales; nacional",
            "reportó conciliación",
            t119[1], t119[4], t119[5],
            "respuesta múltiple: no sumar con juicio ni interpretar como partición exhaustiva",
        ),
    ]
    asegura_unicos(filas, ("tabla", "indicador"), "ENCRIGE")
    return list(filas[0]), filas


def renderiza_csv(campos: list[str], filas: list[dict]) -> bytes:
    salida = io.StringIO(newline="")
    escritor = csv.DictWriter(salida, fieldnames=campos, lineterminator="\n")
    escritor.writeheader()
    escritor.writerows(filas)
    return salida.getvalue().encode("utf-8")


def filas_por_fuente_adquisicion(filas: Iterable[dict]) -> dict[str, dict]:
    """Indexa por fuente; ``fila_origen`` no es única en el registro legado."""
    objetivos = {
        "CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO",
        "ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF",
        "BANXICO_IMOR_CONSUMO_POR_PRODUCTO_MENSUAL",
        "ENSAFI_2023_N34_CONSUMIDOR_DEUDOR",
    }
    por_fuente: dict[str, dict] = {}
    for fila in filas:
        fuente = fila["fuente_canonica"]
        if fuente in por_fuente and fuente in objetivos:
            raise ValueError(f"fila de adquisición duplicada: {fuente}")
        por_fuente[fuente] = fila
    return por_fuente


def actualiza_registro_adquisicion() -> None:
    """Actualiza por fuente estable y añade las dos fuentes de continuación."""
    from curador_registro.tsv_crudo import leer_dicts, upsert_fila

    campos = [
        "fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
        "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
        "ids_manifiesto", "origen", "nota",
    ]
    filas = leer_dicts(REGISTRO_ADQUISICION)
    por_fuente = filas_por_fuente_adquisicion(filas)
    entradas = carga_manifiesto()
    condusef_ids = sorted(
        str(e["id"]) for e in entradas
        if str(e.get("archivo", "")).startswith((PREFIJO_CONDUSEF, CARPETA_CONDUSEF))
    )
    encrige_ids = [
        ID_ENCRIGE_DATOS,
        "encrige2020_cuestionario",
        "gen2_encrige2020_diseno_muestral",
        *condusef_ids,
    ]
    cambios = {
        "CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO": {
            "estado_A4A5": "OBTENIDO-PARCIAL",
            "url_conocida": URL_CNBV,
            "ids_manifiesto": f"{ID_CNBV};{ID_BANXICO_IMOR}",
            "adenda": (
                "ACTO GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA "
                "(11/sep/2026): la fuente CNBV R16 conserva OBTENIDO-PARCIAL, pero "
                "su necesidad científica de historia mensual queda cubierta por la "
                "publicación oficial equivalente de Banxico, 2016-01..2026-03, cinco "
                "productos. No es R16: banca comercial con Sofomes ER subsidiarias, "
                "CI Banco excluido y ruptura IFRS9 desde 2022-01."
            ),
        },
        "ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF": {
            "estado_A4A5": "OBTENIDO",
            "url_conocida": "https://www.inegi.org.mx/programas/encrige/2020/",
            "ids_manifiesto": ";".join(encrige_ids),
            "adenda": (
                "ACTO GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA "
                "(11/sep/2026): esta fuente conserva su alcance empresa/administrativo; "
                "el residual consumidor-deudor se atiende por una identidad separada "
                "ENSAFI_2023_N34_CONSUMIDOR_DEUDOR, sin reinterpretar ENCRIGE ni quejas."
            ),
        },
        "BANXICO_IMOR_CONSUMO_POR_PRODUCTO_MENSUAL": {
            "nueva": True,
            "estado_A4A5": "OBTENIDO",
            "prioridad": "3",
            "url_conocida": URL_BANXICO_IMOR,
            "ids_manifiesto": ID_BANXICO_IMOR,
            "origen": ENCARGO_CONTINUACION,
            "nota": (
                "Publicación oficial equivalente con 123 meses (2016-01..2026-03) "
                "y cinco productos de consumo. IMOR es porcentaje de saldos; desde "
                "2022-01 el numerador es cartera etapa 3 por IFRS9. Universo distinto "
                "de R16: banca comercial, incluye Sofomes ER subsidiarias y excluye "
                "CI Banco. Extracción descriptiva; ningún parámetro adoptado."
            ),
        },
        "ENSAFI_2023_N34_CONSUMIDOR_DEUDOR": {
            "nueva": True,
            "estado_A4A5": "OBTENIDO",
            "prioridad": "3",
            "url_conocida": "https://www.inegi.org.mx/programas/ensafi/2023/",
            "ids_manifiesto": ";".join([
                ID_ENSAFI_DATOS,
                ID_ENSAFI_FD,
                ID_ENSAFI_CUESTIONARIO,
                ID_ENSAFI_DISENO,
                ID_ENSAFI_RESULTADOS,
            ]),
            "origen": ENCARGO_CONTINUACION,
            "nota": (
                "Microdato, descriptor, cuestionario, diseño y resultados oficiales. "
                "Entrega prevalencias descriptivas con población y denominador: atraso "
                "por cuatro clases amplias de deuda del hogar y atraso/estrategias ante "
                "ingreso insuficiente de personas de 18+. Reproduce 27.3% oficial. "
                "No identifica BNPL/CAT ni un efecto causal de baja fricción o usura."
            ),
        },
    }
    for fuente, cambio in cambios.items():
        if cambio.get("nueva"):
            fila = {
                "fila_origen": ENCARGO_CONTINUACION,
                "fuente_canonica": fuente,
                "fuente_canonica_normalizada": fuente,
                "discordancia_alias": "",
                "estado_A4A5": cambio["estado_A4A5"],
                "prioridad": cambio["prioridad"],
                "url_conocida": cambio["url_conocida"],
                "ids_manifiesto": cambio["ids_manifiesto"],
                "origen": cambio["origen"],
                "nota": cambio["nota"],
            }
        else:
            if fuente not in por_fuente:
                raise ValueError(f"fila de adquisición ausente: {fuente}")
            fila = dict(por_fuente[fuente])
            fila["estado_A4A5"] = cambio["estado_A4A5"]
            fila["url_conocida"] = cambio["url_conocida"]
            fila["ids_manifiesto"] = cambio["ids_manifiesto"]
            if cambio["adenda"] not in fila["nota"]:
                fila["nota"] = fila["nota"].rstrip() + " " + cambio["adenda"]
        # Varias fuentes históricas comparten fila_origen; la identidad de
        # esta tabla para una actualización de adquisición es la fuente.
        upsert_fila(REGISTRO_ADQUISICION, fila, campos, clave="fuente_canonica")
        print(f"registro actualizado: {fuente} -> {cambio['estado_A4A5']}")


def actualiza_reservas() -> None:
    """Concilia sólo NC-0163/0164 por identidad estable."""
    from curador_registro.tsv_crudo import leer_dicts, upsert_fila

    campos = [
        "id", "fecha", "acto", "pr", "pieza", "que_no_se_corrio", "razon",
        "impacto", "sucesor", "estado", "cerrado_por", "fecha_cierre",
    ]
    por_id = {fila["id"]: fila for fila in leer_dicts(NO_CORRIDO)}
    requeridos = {"NC-0163", "NC-0164"}
    if not requeridos <= por_id.keys():
        raise ValueError(f"reservas de #717 ausentes: {sorted(requeridos - por_id.keys())}")

    imor = dict(por_id["NC-0163"])
    imor.update({
        "razon": "EJECUTADA-POR-PUBLICACION-OFICIAL-EQUIVALENTE",
        "impacto": (
            "Banxico aporta IMOR mensual 2016-01..2026-03 para consumo total, "
            "tarjeta, ABCD, nomina y personales, con denominador de cartera del "
            "mismo producto y ruptura IFRS9 explicita; no es la exportacion R16."
        ),
        "sucesor": (
            "ninguno para la historia mensual solicitada; obtener R16 exacto queda "
            "como mejora opcional de comparabilidad institucional"
        ),
        "estado": "CERRADA",
        "cerrado_por": "ACTO GEN2-FUENTES-FINANCIERAS-CONTINUACION-EFECTIVA",
        "fecha_cierre": "2026-09-11",
    })
    upsert_fila(NO_CORRIDO, imor, campos, clave="id")

    n34 = dict(por_id["NC-0164"])
    n34.update({
        "razon": "EJECUTADA-PARCIAL-CONSUMIDOR-Y-DENOMINADORES",
        "impacto": (
            "ENSAFI 2023 aporta prevalencia descriptiva poblacional del lado "
            "consumidor-deudor, atraso por cuatro clases amplias de deuda y "
            "estrategias ante ingreso insuficiente. No enlaza en una observacion "
            "causa de baja friccion/usura/BNPL, producto exacto y dano."
        ),
        "sucesor": (
            "spec prospectiva solo si mesa acepta los estimandos descriptivos; para "
            "el mecanismo completo, fuente o instrumento que enlace producto exacto, "
            "exposicion, costo/CAT o friccion, atraso/cobranza/venta de activos y pesos"
        ),
        "estado": "ABIERTA",
        "cerrado_por": "NO-APLICA-MIENTRAS-ABIERTA",
        "fecha_cierre": "NO-APLICA-MIENTRAS-ABIERTA",
    })
    upsert_fila(NO_CORRIDO, n34, campos, clave="id")
    print("reservas conciliadas: NC-0163 -> CERRADA; NC-0164 -> ABIERTA-PARCIAL")


def construye() -> dict[str, bytes]:
    entradas = carga_manifiesto()
    por_id = indice_por_id(entradas)
    raices = mapa_raices()
    condusef = [
        e for e in entradas
        if str(e.get("archivo", "")).startswith((PREFIJO_CONDUSEF, CARPETA_CONDUSEF))
    ]
    if not condusef:
        raise ValueError("no se encontraron CSV CONDUSEF manifestados")
    for identificador in (
        ID_ENSAFI_FD,
        ID_ENSAFI_CUESTIONARIO,
        ID_ENSAFI_DISENO,
        ID_ENSAFI_RESULTADOS,
    ):
        entrada = por_id[identificador]
        verifica_payload(entrada, ruta_payload(entrada, raices))
    productos: dict[str, tuple[list[str], list[dict]]] = {
        "cnbv-imor-consumo.csv": extrae_cnbv(por_id[ID_CNBV], raices),
        "banxico-imor-consumo-mensual.csv": extrae_banxico_imor(
            por_id[ID_BANXICO_IMOR], raices
        ),
        "condusef-inventario.csv": inventario_condusef(condusef, raices),
        "condusef-acciones-defensa.csv": agrega_acciones(condusef, raices),
        "condusef-reclamaciones-clase.csv": agrega_reclamaciones_clase(condusef, raices),
        "condusef-reclamaciones-producto.csv": agrega_reclamaciones_producto(condusef, raices),
        "encrige2020-cumplimiento-contratos.csv": extrae_encrige(por_id[ID_ENCRIGE_DATOS], raices),
        "ensafi2023-atraso-deuda-producto-hogar.csv": extrae_ensafi_hogar(
            por_id[ID_ENSAFI_DATOS], raices
        ),
        "ensafi2023-deuda-y-afrontamiento-persona.csv": extrae_ensafi_persona(
            por_id[ID_ENSAFI_DATOS], raices
        ),
    }
    return {nombre: renderiza_csv(*producto) for nombre, producto in productos.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=SALIDA_PREDETERMINADA)
    parser.add_argument("--verifica", action="store_true", help="no escribe; compara con salidas existentes")
    parser.add_argument(
        "--actualiza-registro", action="store_true",
        help="actualiza fuentes por identidad estable con tsv_crudo.upsert_fila",
    )
    args = parser.parse_args(argv)
    productos = construye()
    if args.verifica:
        distintos = []
        for nombre, contenido in productos.items():
            ruta = args.salida / nombre
            if not ruta.is_file() or ruta.read_bytes() != contenido:
                distintos.append(nombre)
        if distintos:
            print("salidas ausentes o distintas: " + ", ".join(distintos), file=sys.stderr)
            return 1
        print(f"COINCIDE: {len(productos)} tablas reproducidas byte a byte")
        return 0
    args.salida.mkdir(parents=True, exist_ok=True)
    for nombre, contenido in productos.items():
        (args.salida / nombre).write_bytes(contenido)
        filas = contenido.count(b"\n") - 1
        print(f"{nombre}: {filas} filas")
    if args.actualiza_registro:
        actualiza_registro_adquisicion()
        actualiza_reservas()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
