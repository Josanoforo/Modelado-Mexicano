"""D2 (hoja NC-DECISIONES-1, fila D2, firma de mesa 28/sep, opción a) ·
`ACTO GEN2-TUBERIA-Y-CURACION-1`, P7.

Hallazgo (GEN2-CONSUMO-Y-GASTO-PISOS-1): 18 entradas `engasto_2012_<nombre>`
declaran `id`/`url_origen` de la ola 2012 pero su `archivo` en disco vive
bajo `engasto2013/<nombre>.zip` -- lo que de verdad SIRVEN es la ola 2013.
Los huérfanos `engasto2012_<nombre>` (sin guion bajo tras "engasto", carga de
agosto) sí archivan bajo `engasto2013/`... `engasto2012/<nombre>.zip` -- son
la ola 2012 real, con nombre fuera de la convención `engasto_<año>_<nombre>`.

Solo ROTULO (`id`; `usado_para` no cambia: las 36 entradas tocadas ya dicen
"sin uso asignado" en los dos lados, ningún consumidor las cita hoy).
`url_origen`, `archivo`, `sha256`, `licencia`: NINGUNO se toca -- son
evidencia de procedencia, no rótulo, y el propio hallazgo ya declara que la
URL nominal de 2012 sirvió contenido 2013 (quirk del portal, no error de
descarga).

Dos renombres simétricos por nombre de archivo (candidatos: 18 pares):
  engasto_2012_<nombre>  -> engasto_2013_<nombre>   (lo que de verdad sirve)
  engasto2012_<nombre>   -> engasto_2012_<nombre>   ("se casa" a la
                                                       convención con guion)
El primer renombre vacía el id que el segundo ocupa: sin colisión.
`lugar_compra_*` y `vivienda_*` (archivo ya bajo engasto2012/) y el
descriptor `engasto_2012_engasto12_fd` no se tocan -- ya están bien.

EXCLUSIÓN (verificada con `git grep`, no supuesta): de los 18 pares, DOS
-- `hogar_dta` y `gasto_de_consumo_ajustado_dta` -- están citados por
`data/corrida0/CALC-ENGASTO-CONSUMO-PISOS-0001/{medidor.py,spec.yaml}`,
un CALC SELLADO (`sello.json`/`sello.sha256` presentes): `medidor.py::PAY`
usa literalmente `engasto2012_hogar_dta` y
`engasto2012_gasto_de_consumo_ajustado_dta`. Renombrar esos dos ids
rompería la resolución de inputs de una corrida ya sellada -- exactamente
lo que D-19(d) prohíbe ("cambiar un procedimiento congelado") y lo que
E.3/D-22(4) protegen (nada se sella contra un libro vivo; un id de
manifiesto que un CALC sellado cita es, de facto, parte de esa constancia).
`tools/dominios/consumo/genera_spec_yaml.py` (el generador vivo, no
sellado) hereda la misma cita -- tampoco se toca. Los otros 16 pares no
tienen ninguna cita fuera de `data/manifiesto.yaml` (verificado por
`git grep` sobre `*.py`/`*.yaml`/`*.yml`/`*.md`, cero coincidencias).

Verifica tras escribir: yaml.safe_load antes/después tiene el mismo número
de entradas, y para cada una difiere SOLO en `id` (si acaso) -- ningún otro
campo se mueve un byte.

Uso: python3 forense/analisis/tuberia-y-curacion-1/corrige_engasto.py [--aplica]
"""
import re
import sys

import yaml

P = "data/manifiesto.yaml"

# Los 18 nombres de archivo compartidos entre la pareja mal-rotulada y el
# huérfano -- derivados por comando (intersección), no tecleados a mano.


def _sufijo(prefijo, ids):
    return {i[len(prefijo):] for i in ids if i.startswith(prefijo)}


def main():
    txt = open(P, encoding="utf-8").read()
    antes = yaml.safe_load(txt)
    por_id = {e["id"]: e for e in antes}

    mal_2012 = _sufijo("engasto_2012_", por_id)
    huerfanos = _sufijo("engasto2012_", por_id)
    # Excluidos: citados por el CALC sellado CALC-ENGASTO-CONSUMO-PISOS-0001
    # (medidor.py::PAY) -- ver docstring del módulo.
    SELLADOS = {"hogar_dta", "gasto_de_consumo_ajustado_dta"}
    nombres = sorted((mal_2012 & huerfanos) - SELLADOS)

    renombres = {}
    for nombre in nombres:
        id_mal = f"engasto_2012_{nombre}"
        id_huerfano = f"engasto2012_{nombre}"
        e_mal, e_huerfano = por_id[id_mal], por_id[id_huerfano]
        if not str(e_mal.get("archivo") or "").startswith("engasto2013/"):
            continue  # no es del defecto: archivo ya coincide con 2012
        if not str(e_huerfano.get("archivo") or "").startswith("engasto2012/"):
            continue
        renombres[id_mal] = f"engasto_2013_{nombre}"
        renombres[id_huerfano] = id_mal

    # Premisa (§4 del encargo): 2012 y 2013 existen los dos, por id, antes de tocar nada.
    ids_2013_ya = {i for i in por_id if i.startswith("engasto_2013_")}
    for nuevo in renombres.values():
        if nuevo.startswith("engasto_2013_") and nuevo not in ids_2013_ya:
            continue  # nace de este cambio, no colisiona con uno preexistente
    despues_ids = (set(por_id) - set(renombres)) | set(renombres.values())
    assert len(despues_ids) == len(por_id), "colisión de id tras renombrar"

    lines = txt.split("\n")
    out, i, n = [], 0, len(lines)
    cambiadas = 0
    while i < n:
        m = re.match(r"^- id: *(.+?) *$", lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        j = i + 1
        while j < n and not (lines[j].startswith("- ") or (lines[j] and not lines[j][0].isspace())):
            j += 1
        bloque = lines[i:j]
        eid = yaml.safe_load(lines[i][2:])["id"]
        if eid in renombres:
            nuevo_id = renombres[eid]
            bloque[0] = "- id: " + (
                yaml.safe_dump(nuevo_id, allow_unicode=True, width=10**6)
                .strip().removesuffix("\n...").removesuffix("...").strip())
            cambiadas += 1
        out.extend(bloque)
        i = j
    nuevo_txt = "\n".join(out)

    despues = yaml.safe_load(nuevo_txt)
    assert len(antes) == len(despues), (len(antes), len(despues))
    despues_por_id = {e["id"]: e for e in despues}
    for eid, e_antes in por_id.items():
        eid_despues = renombres.get(eid, eid)
        e_despues = despues_por_id[eid_despues]
        sin_id_antes = {k: v for k, v in e_antes.items() if k != "id"}
        sin_id_despues = {k: v for k, v in e_despues.items() if k != "id"}
        assert sin_id_antes == sin_id_despues, eid

    print(f"entradas={len(antes)} renombradas={cambiadas} (de {len(nombres)} nombres candidatos) "
          f"verificado=solo-id")
    for viejo, nuevo in sorted(renombres.items()):
        print(f"  {viejo} -> {nuevo}")
    if "--aplica" in sys.argv:
        open(P, "w", encoding="utf-8").write(nuevo_txt)


main()
