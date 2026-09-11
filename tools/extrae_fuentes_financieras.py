#!/usr/bin/env python3
"""Extrae los objetos financieros del Encargo GEN2 20.

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

ID_CNBV = "gen2_cnbv_040_1a_r16_imor_tipo_cartera"
ID_ENCRIGE_DATOS = "conjunto_de_datos_encrige_2020_csv"
PREFIJO_CONDUSEF = "A6_CONDUSEF_DATOS_ABIERTOS/"
CARPETA_CONDUSEF = "condusef_redeco_reune/"

URL_CNBV = (
    "https://portafolioinfdoctos.cnbv.gob.mx/Documentacion/"
    "minfo/XLS/40/040_1a_R16.xls"
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
    }
    por_fuente: dict[str, dict] = {}
    for fila in filas:
        fuente = fila["fuente_canonica"]
        if fuente in por_fuente and fuente in objetivos:
            raise ValueError(f"fila de adquisición duplicada: {fuente}")
        por_fuente[fuente] = fila
    return por_fuente


def actualiza_registro_adquisicion() -> None:
    """Actualiza sólo las dos filas del encargo mediante el escritor canónico."""
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
            "ids_manifiesto": ID_CNBV,
            "adenda": (
                "ACTO GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES (11/sep/2026): "
                "OBTENIDO-PARCIAL. El flujo vigente ReportViwer/Agrupados entrega "
                "el XLS oficial 040-1A-R16, verificado curl+wget, pero sólo con la "
                "foto cacheada 202112. La macro lee su conexión desde "
                r"\\sector5\DGAIN\MINFO\dgaex.txt y ejecuta sp_obtiene_reporte, "
                "ruta interna no alcanzable públicamente: la serie histórica sigue "
                "como barrera externa demostrada; queda utilizable el corte y el "
                "extractor, no un parámetro del motor."
            ),
        },
        "ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF": {
            "estado_A4A5": "OBTENIDO",
            "url_conocida": "https://www.inegi.org.mx/programas/encrige/2020/",
            "ids_manifiesto": ";".join(encrige_ids),
            "adenda": (
                "ACTO GEN2-CNBV-CONDUSEF-FUENTES-Y-SERIES (11/sep/2026): "
                "OBTENIDO en la capa de adquisición. La ola ENCRIGE 2020 existe: "
                "paquete tabulado, cuestionario y diseño muestral oficiales quedaron "
                "verificados; se leyeron 29/29 CSV CONDUSEF ya manifestados. ENCRIGE "
                "observa a la empresa frente a contrapartes privadas y CONDUSEF no "
                "trae denominador de clientes ni causa/BNPL: la demanda científica "
                "N34 no queda satisfecha ni se adopta parámetro por este estado."
            ),
        },
    }
    for fuente, cambio in cambios.items():
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
    productos: dict[str, tuple[list[str], list[dict]]] = {
        "cnbv-imor-consumo.csv": extrae_cnbv(por_id[ID_CNBV], raices),
        "condusef-inventario.csv": inventario_condusef(condusef, raices),
        "condusef-acciones-defensa.csv": agrega_acciones(condusef, raices),
        "condusef-reclamaciones-clase.csv": agrega_reclamaciones_clase(condusef, raices),
        "condusef-reclamaciones-producto.csv": agrega_reclamaciones_producto(condusef, raices),
        "encrige2020-cumplimiento-contratos.csv": extrae_encrige(por_id[ID_ENCRIGE_DATOS], raices),
    }
    return {nombre: renderiza_csv(*producto) for nombre, producto in productos.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=SALIDA_PREDETERMINADA)
    parser.add_argument("--verifica", action="store_true", help="no escribe; compara con salidas existentes")
    parser.add_argument(
        "--actualiza-registro", action="store_true",
        help="actualiza las dos filas de adquisición con tsv_crudo.upsert_fila",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
