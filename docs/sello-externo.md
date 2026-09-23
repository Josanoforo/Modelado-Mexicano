# Sello externo de las emisiones GEN2 — receta de verificación por un tercero

Este documento explica, para alguien que **no confía en este repositorio ni en
GitHub**, cómo comprobar que un conjunto de emisiones selladas (`sello.json`
por `CALC`, sidecar `.sha256` por spec congelada) ya existía en la fecha que
decimos. No demuestra autoría — demuestra existencia-antes-de.

## Qué archivo tomar

`forense/sellos/manifiesto-sellos-<fecha>.tsv`. Cada fila es un sello:

```
tipo  id  ruta  sha256  commit  fecha_commit  pr  merged_at  firma_gpg_estado  firma_gpg_keyid
```

- `sha256` es el hash del archivo de sello en `ruta`, tal como está en ese
  commit del repo — no del contenido que el sello protege (eso ya lo cubre
  `sello.json`/`.sha256` por su cuenta).
- La última línea del archivo (`# sha256-manifiesto\t<hash>`) es el sha256
  del propio manifiesto (todas las líneas anteriores, tal cual).

## Qué comando correr, y qué tiene que salir

### Mecanismo (a) — OpenTimestamps (preferido; ancla en Bitcoin)

Si existe un archivo `.ots` junto al manifiesto (`manifiesto-sellos-<fecha>.tsv.ots`):

```
pip install --break-system-packages opentimestamps-client   # o pipx
ots verify forense/sellos/manifiesto-sellos-<fecha>.tsv.ots
```

Salida esperada una vez que el calendario ancló (puede tardar horas desde el
sellado): `Success! Bitcoin block <n> attests existence as of <fecha>`. Antes
de anclar, `ots verify` dice `Pending confirmation in Bitcoin blockchain` —
eso demuestra que se envió, no que ancló; hay que reintentar más tarde
(`ots upgrade` lo actualiza).

### Mecanismo (b) — TSA RFC 3161

Si existe `manifiesto-sellos-<fecha>.tsv.tsr` (respuesta) y se declara la
cadena de la autoridad (`.tsq` es la solicitud, no hace falta para verificar):

```
openssl ts -verify -in manifiesto-sellos-<fecha>.tsv.tsr \
  -data forense/sellos/manifiesto-sellos-<fecha>.tsv \
  -CAfile <cadena-de-la-TSA-declarada-en-la-nota-de-cierre>
```

Salida esperada: `Verification: OK`. Esto certifica que la TSA vio ese
hash exacto en ese instante — confías en la TSA, no en nosotros.

### Mecanismo (c) — Fallback sin red: firma GPG del merge + tag firmado por mesa

Cuando ninguno de (a)/(b) tuvo egress al sellar (es el caso del 23/sep/2026:
ver la nota de cierre del acto `GEN2-TUBERIA-SELLO-EXTERNO-1` — la política
de red de la sesión de nube deniega los calendarios OTS y las TSA públicas),
el manifiesto trae dos columnas adicionales por fila:

- `firma_gpg_keyid`: la key id que firmó el **merge commit** que introdujo
  ese sello a `origin/main` (`git log --format=%GK <commit>`).
- `firma_gpg_estado`: el estado que `git` reporta para esa firma sin tener
  la llave pública importada (`E` = no se puede comprobar sin la llave; no
  es lo mismo que una firma inválida).

Esto por sí solo **no** es una atestación de un tercero — GitHub firma sus
merges con su propia llave, así que hoy este mecanismo demuestra "GitHub
dice que esto se fusionó en tal fecha", que es lo mismo que ya sabíamos
(§1 del acto). Lo que sí añade valor de terceros es el paso siguiente, que
mesa corre **fuera de esta sesión, en una máquina con su propia llave**:

```
git clone https://github.com/Josanoforo/Modelado-Mexicano.git
cd Modelado-Mexicano
git fetch origin <rama-de-este-acto>
git tag -s sellos-<fecha> <sha-del-commit-que-trae-este-manifiesto> \
  -m "Atestigua forense/sellos/manifiesto-sellos-<fecha>.tsv sha256=<sha256-manifiesto>"
git push origin sellos-<fecha>
```

Un tercero verifica ese tag con la llave pública de mesa (publicada donde
mesa decida — no es parte de este acto) y con eso tiene: (1) el sha256 del
manifiesto, dentro del mensaje del tag firmado; (2) la fecha de la firma
(`git log -1 --format=%ai sellos-<fecha>`); (3) que la llave que firmó es de
mesa, no de GitHub — el activo que sí es nuevo. Sigue sin ser tan fuerte
como (a)/(b) (mesa podría, en teoría, firmar retroactivamente si controla el
reloj de su propia máquina), pero es lo único que no exige más red que la
API/objetos de git.

## Qué demuestra cada mecanismo, y qué no

| Mecanismo | Demuestra | No demuestra |
|---|---|---|
| (a) OpenTimestamps | El hash existía antes del bloque de Bitcoin que lo confirma (reloj de la red Bitcoin, nadie lo controla) | Quién generó el archivo |
| (b) TSA RFC 3161 | El hash existía antes del instante que certifica la TSA | Nada si no confías en esa TSA en particular |
| (c) tag GPG de mesa | El hash existía antes de la fecha del tag, **si confías en la llave y el reloj de mesa** | Que sea anterior a algo que mesa no controle |
| Firma GPG del merge de GitHub (columna del manifiesto) | Que GitHub registró ese commit fusionado en esa fecha | Nada ante quien no confíe en GitHub — es el estado actual, el problema que este acto existe para superar |

## Prueba de esta receta, desde un clon limpio

Corrida en esta misma sesión, sin usar el checkout de trabajo:

```
$ rm -rf /tmp/verifica-sello && git clone -q /home/user/Modelado-Mexicano /tmp/verifica-sello
$ cd /tmp/verifica-sello && git checkout -q acto/gen2-tuberia-sello-externo-1
$ sha256sum forense/sellos/manifiesto-sellos-2026-09-23.tsv
<pegado en la nota de cierre>
$ git log -1 --format="%G? %GK" $(git log --diff-filter=A --format=%H -1 -- data/corrida0/CALC-0001/sello.json)
E B5690EEEBB952194
```

(El clon es local porque esta sesión de nube no tiene egress a
`github.com` fuera del remoto ya configurado del worktree; el comando
`git clone <url-https>` es el mismo para un tercero con red normal.)
