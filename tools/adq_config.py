#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/adq_config.py -- lector de `data/adq-config.yaml` (P6, ACTO
ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE, 7/sep/2026).

Antes de este acto, `tools/adquiere_cron.sh` traía cableadas a mano las
URLs, las claves física/lógica y los ids de referencia de manifiesto de la
PDN. Un archivo de configuración pequeño y versionado permite auditarlas
sin leer el shell y reutilizarlas desde `tools/adq_doctor.py` -- este
módulo es el único lector, para que shell y Python nunca diverjan sobre
qué significa cada clave.

No decide nada: si una clave falta, error explícito -- nunca un default
inventado que enmascare un `data/adq-config.yaml` mal editado.

Uso:
    python3 tools/adq_config.py <ruta.punteada>
        Imprime el valor (str/num tal cual; dict/list como JSON) en stdout.
        Exit 1 y mensaje en stderr si la ruta no existe.

    from adq_config import cargar, obten
        cargar()             -> dict completo
        obten("pdn.sistemas.s1.url", cfg=None)  -> valor resuelto
"""
import json
import datetime
import os
import re
import sys

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CONFIG = os.path.join(RAIZ, "data", "adq-config.yaml")

CALENDARIO_RESPALDO = {
    "hora": "07:30",
    "dias_semana": ["lunes", "martes", "miercoles", "jueves", "viernes"],
    "zona_iana": "America/Mexico_City",
    "zona_windows": "Central Standard Time (Mexico)",
    "ventana_observacion_minutos": 45,
}
_DIA_A_WEEKDAY = {
    "lunes": 0, "martes": 1, "miercoles": 2, "jueves": 3,
    "viernes": 4, "sabado": 5, "domingo": 6,
}
_DIA_A_WINDOWS = {
    "lunes": "Monday", "martes": "Tuesday", "miercoles": "Wednesday",
    "jueves": "Thursday", "viernes": "Friday", "sabado": "Saturday",
    "domingo": "Sunday",
}
_RE_HORA = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


class ConfiguracionError(ValueError):
    """Configuración presente pero inválida, con causa apta para reporte."""


def cargar(ruta=RUTA_CONFIG):
    with open(ruta, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ConfiguracionError("la raíz YAML debe ser un mapa")
    return cfg


def obten(ruta_punteada, cfg=None, config_path=None):
    """Resuelve `a.b.c` sobre el dict de configuración. Lanza KeyError con
    el tramo exacto que faltó -- nunca devuelve None por una clave ausente.

    `config_path=None` (default real, no ligado en tiempo de definición)
    resuelve `RUTA_CONFIG` en tiempo de LLAMADA -- así un llamador que
    parcha `adq_config.RUTA_CONFIG` (pruebas) sí lo ve; un default de
    parámetro (`config_path=RUTA_CONFIG`) se congela en el import y nunca
    vería el parche."""
    if cfg is None:
        cfg = cargar(config_path if config_path is not None else RUTA_CONFIG)
    valor = cfg
    recorrido = []
    for parte in ruta_punteada.split("."):
        recorrido.append(parte)
        if not isinstance(valor, dict) or parte not in valor:
            raise KeyError(f"{'.'.join(recorrido)} (dentro de {ruta_punteada!r})")
        valor = valor[parte]
    return valor


def _entero_positivo(valor, nombre, minimo=1, maximo=86400):
    if isinstance(valor, bool):
        raise ConfiguracionError(f"{nombre}={valor!r}: se esperaba entero")
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ConfiguracionError(f"{nombre}={valor!r}: se esperaba entero") from None
    if str(valor).strip() != str(numero) or not minimo <= numero <= maximo:
        raise ConfiguracionError(
            f"{nombre}={valor!r}: debe estar entre {minimo} y {maximo}")
    return numero


def calendario(cfg=None, config_path=None):
    """Calendario validado y normalizado para Python, shell y PowerShell."""
    if cfg is None:
        cfg = cargar(config_path if config_path is not None else RUTA_CONFIG)
    crudo = obten("calendario", cfg=cfg)
    if not isinstance(crudo, dict):
        raise ConfiguracionError("calendario debe ser un mapa")
    faltantes = [k for k in CALENDARIO_RESPALDO if k not in crudo]
    if faltantes:
        raise ConfiguracionError(f"calendario: faltan {', '.join(faltantes)}")
    hora = crudo["hora"]
    if not isinstance(hora, str) or not _RE_HORA.fullmatch(hora):
        raise ConfiguracionError(f"calendario.hora={hora!r}: se esperaba HH:mm (00:00-23:59)")
    dias = crudo["dias_semana"]
    if not isinstance(dias, list) or not dias:
        raise ConfiguracionError("calendario.dias_semana debe ser una lista no vacía")
    if any(not isinstance(d, str) or d not in _DIA_A_WEEKDAY for d in dias):
        raise ConfiguracionError(f"calendario.dias_semana={dias!r}: contiene un día inválido")
    if len(set(dias)) != len(dias):
        raise ConfiguracionError(f"calendario.dias_semana={dias!r}: contiene duplicados")
    zona_iana = crudo["zona_iana"]
    zona_windows = crudo["zona_windows"]
    if not isinstance(zona_iana, str) or not zona_iana.strip():
        raise ConfiguracionError(f"calendario.zona_iana={zona_iana!r}: se esperaba texto")
    if not isinstance(zona_windows, str) or not zona_windows.strip():
        raise ConfiguracionError(f"calendario.zona_windows={zona_windows!r}: se esperaba texto")
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(zona_iana)
    except Exception as e:
        raise ConfiguracionError(f"calendario.zona_iana={zona_iana!r}: no disponible ({e})") from None
    ventana = _entero_positivo(crudo["ventana_observacion_minutos"],
                               "calendario.ventana_observacion_minutos", 0, 1440)
    return {
        "hora": hora,
        "dias_semana": list(dias),
        "weekdays": [_DIA_A_WEEKDAY[d] for d in dias],
        "dias_windows": [_DIA_A_WINDOWS[d] for d in dias],
        "zona_iana": zona_iana,
        "zona_windows": zona_windows,
        "ventana_observacion_minutos": ventana,
    }


def calendario_resuelto(cfg=None, config_path=None):
    """Siempre devuelve un calendario y declara si aplicó el respaldo."""
    try:
        valor = calendario(cfg=cfg, config_path=config_path)
        return {**valor, "degradada": False, "causa": None, "fuente": "config"}
    except Exception as e:
        valor = calendario(cfg={"calendario": CALENDARIO_RESPALDO})
        return {**valor, "degradada": True,
                "causa": f"{type(e).__name__}: {e}", "fuente": "respaldo-compatible"}


def entero_resuelto(clave, env_var, respaldo, *, entorno=None, cfg=None,
                    config_path=None, minimo=1, maximo=86400):
    """Resuelve override > YAML > respaldo, validando y declarando degradación."""
    entorno = os.environ if entorno is None else entorno
    causas = []
    valor_config = None
    try:
        valor_config = _entero_positivo(
            obten(clave, cfg=cfg, config_path=config_path), clave, minimo, maximo)
    except Exception as e:
        causas.append(f"config inválida: {type(e).__name__}: {e}")
    if env_var in entorno:
        try:
            valor = _entero_positivo(entorno[env_var], env_var, minimo, maximo)
            return {"valor": valor, "fuente": f"env:{env_var}",
                    "degradada": bool(causas), "causa": "; ".join(causas) or None}
        except Exception as e:
            causas.append(f"override inválido: {type(e).__name__}: {e}")
    if valor_config is not None:
        return {"valor": valor_config, "fuente": f"config:{clave}",
                "degradada": bool(causas), "causa": "; ".join(causas) or None}
    valor = _entero_positivo(respaldo, "respaldo", minimo, maximo)
    return {"valor": valor, "fuente": "respaldo-compatible", "degradada": True,
            "causa": "; ".join(causas)}


def _entero_compat(nueva_clave, nueva_env, clave_antigua, env_antigua,
                    respaldo, *, entorno=None, cfg=None, config_path=None):
    """Autoridad nueva con lectura explícita, y aliases antiguos sólo si falta.

    Orden: env nueva > YAML nuevo > env antiguo > YAML antiguo > respaldo. Una
    clave nueva presente nunca compite con la antigua.
    """
    entorno = os.environ if entorno is None else entorno
    cfg = cargar(config_path if config_path is not None else RUTA_CONFIG) if cfg is None else cfg
    if nueva_env in entorno:
        r = entero_resuelto(nueva_clave, nueva_env, respaldo, entorno=entorno,
                            cfg=cfg, minimo=1, maximo=86400)
        return r
    try:
        valor = _entero_positivo(obten(nueva_clave, cfg=cfg), nueva_clave)
        return {"valor": valor, "fuente": f"config:{nueva_clave}",
                "degradada": False, "causa": None}
    except KeyError:
        pass
    if env_antigua in entorno:
        valor = _entero_positivo(entorno[env_antigua], env_antigua)
        return {"valor": valor, "fuente": f"compat-env:{env_antigua}",
                "degradada": False, "causa": "alias histórico"}
    try:
        valor = _entero_positivo(obten(clave_antigua, cfg=cfg), clave_antigua)
        return {"valor": valor, "fuente": f"compat-config:{clave_antigua}",
                "degradada": False, "causa": "alias histórico"}
    except KeyError:
        valor = _entero_positivo(respaldo, "respaldo")
        return {"valor": valor, "fuente": "respaldo-compatible",
                "degradada": True,
                "causa": f"faltan {nueva_clave} y alias {clave_antigua}"}


def ejecutor_resuelto(cfg=None, config_path=None, entorno=None):
    """Configuración validada del único ejecutor seleccionado."""
    entorno = os.environ if entorno is None else entorno
    cfg = cargar(config_path if config_path is not None else RUTA_CONFIG) if cfg is None else cfg
    nombre = str(cfg.get("ejecutor", "claude")).strip().lower()
    if nombre not in ("codex", "claude"):
        raise ConfiguracionError(f"ejecutor={nombre!r}: se esperaba codex o claude")
    timeout = _entero_compat(
        "ejecutor_timeout_segundos", "ADQ_TIMEOUT_SEGUNDOS",
        "claude_timeout_segundos", "CLAUDE_TIMEOUT_SEGUNDOS", 1800,
        entorno=entorno, cfg=cfg)
    kill_after = _entero_compat(
        "ejecutor_kill_after_segundos", "ADQ_KILL_AFTER_SEGUNDOS",
        "claude_kill_after_segundos", "CLAUDE_KILL_AFTER_SEGUNDOS", 60,
        entorno=entorno, cfg=cfg)
    maximo = _entero_positivo(cfg.get("maximo_filas", 5), "maximo_filas", 1, 5)
    resultado = {
        "nombre": nombre,
        "timeout": timeout,
        "kill_after": kill_after,
        "maximo_filas": maximo,
    }
    if nombre == "codex":
        codex = cfg.get("codex")
        if not isinstance(codex, dict):
            raise ConfiguracionError("codex debe ser un mapa cuando ejecutor=codex")
        requeridas = ("binario", "modelo", "sandbox", "aprobaciones",
                      "red_workspace_write", "busqueda_web", "directorio_adicional",
                      "esquema_resultado")
        faltan = [k for k in requeridas if k not in codex]
        if faltan:
            raise ConfiguracionError(f"codex: faltan {', '.join(faltan)}")
        if codex["sandbox"] != "workspace-write":
            raise ConfiguracionError("codex.sandbox debe ser workspace-write")
        if codex["aprobaciones"] != "never":
            raise ConfiguracionError("codex.aprobaciones debe ser never para el job no interactivo")
        if codex["red_workspace_write"] is not True:
            raise ConfiguracionError("codex.red_workspace_write debe ser true")
        if codex["busqueda_web"] is not True:
            raise ConfiguracionError("codex.busqueda_web debe ser true para descubrimiento externo")
        resultado["codex"] = dict(codex)
    return resultado


def proxima_ejecucion(ahora, cal=None):
    """Próxima hora del calendario, calculada en su zona y no en la del host."""
    cal = calendario() if cal is None else cal
    from zoneinfo import ZoneInfo
    zona = ZoneInfo(cal["zona_iana"])
    local = ahora.astimezone(zona)
    hh, mm = map(int, cal["hora"].split(":"))
    for delta in range(8):
        fecha = local.date() + datetime.timedelta(days=delta)
        candidata = datetime.datetime.combine(fecha, datetime.time(hh, mm), tzinfo=zona)
        if fecha.weekday() in cal["weekdays"] and candidata > local:
            return candidata
    raise ConfiguracionError("calendario sin próxima ejecución en ocho días")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--calendario-json"]:
        print(json.dumps(calendario_resuelto(), ensure_ascii=False))
        return 0
    if argv == ["--ejecutor-json"]:
        print(json.dumps(ejecutor_resuelto(), ensure_ascii=False))
        return 0
    if len(argv) == 4 and argv[0] == "--entero-json":
        clave, env_var, respaldo = argv[1:]
        print(json.dumps(entero_resuelto(clave, env_var, respaldo), ensure_ascii=False))
        return 0
    if len(argv) != 1:
        print("uso: adq_config.py <ruta.punteada> | --calendario-json | --ejecutor-json | "
              "--entero-json <clave> <env> <respaldo>", file=sys.stderr)
        return 2
    try:
        valor = obten(argv[0])
    except (KeyError, ConfiguracionError) as e:
        print(f"ERROR: configuración inválida en {RUTA_CONFIG}: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"ERROR: no existe {RUTA_CONFIG}", file=sys.stderr)
        return 1
    if isinstance(valor, (dict, list)):
        print(json.dumps(valor, ensure_ascii=False))
    else:
        print(valor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
