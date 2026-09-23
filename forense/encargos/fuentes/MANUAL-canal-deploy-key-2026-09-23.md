# MANUAL · Llave de despliegue para que el canal de publicación pueda escribir en `main`
**Para: mesa (Jonás) · escrito por dirección 23/sep/2026 · tiempo: ~5 minutos · se hace una sola vez · no requiere clon ni terminal del repo, solo PowerShell y el navegador.**

## Por qué
El job de CI que publica la vista (`verify.yml`, pasos «Re-deriva por comando y commitea [deriva]» y «Canal de publicación») empuja a `main` con el token automático de GitHub Actions, y la regla **main protegida** lo rechaza (`GH013: Required status check "check" is expected`). Ese token no se puede exentar: en la lista de bypass de un ruleset no existe «GitHub Actions». Lo que sí se puede exentar es una **deploy key**. El canal firmará con ella; la regla la deja pasar; y un push hecho con deploy key sí dispara el workflow (los del token no). Nada más cambia: el check `check` sigue siendo obligatorio para todo PR, y nadie —ni admin— empuja directo.

## Antes de empezar (1 minuto)
En **Settings → Rulesets → main protegida**, confirma que la fila *Repository admin* diga **Allow for pull requests only** (no «Always allow»). Si dice «Always allow», cámbialo con los `···` de la fila y guarda. Si en algún momento marcaste *Claude* o *Copilot* como bypass, quítalos.

## Paso 1 · Generar la llave (PowerShell, en tu máquina)
```powershell
cd $env:USERPROFILE\Desktop
ssh-keygen -t ed25519 -C "canal-deriva" -f canal_deriva -N '""'
```
Quedan dos archivos en el Escritorio: `canal_deriva` (**privada**, no se comparte) y `canal_deriva.pub` (pública). Si PowerShell no encuentra `ssh-keygen`, instálalo con `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0` (como administrador) y repite.

## Paso 2 · Registrar la pública como deploy key
**Settings → Deploy keys → Add deploy key**
- Title: `canal-deriva`
- Key: abre `canal_deriva.pub` con el Bloc de notas y pega todo su contenido (una línea que empieza con `ssh-ed25519`).
- Marca **Allow write access**. Sin esa casilla no sirve.
- **Add key**.

## Paso 3 · Guardar la privada como secreto del repo
**Settings → Secrets and variables → Actions → New repository secret**
- Name: `CANAL_DERIVA_SSH_KEY` (exacto, mayúsculas).
- Secret: abre `canal_deriva` (sin extensión) con el Bloc de notas y pega **todo**, incluidas las líneas `-----BEGIN OPENSSH PRIVATE KEY-----` y `-----END OPENSSH PRIVATE KEY-----`.
- **Add secret**.
Después borra `canal_deriva` del Escritorio (la pública puede quedarse). El secreto no se puede volver a leer desde GitHub; si se pierde, se repite el manual con otra llave.

## Paso 4 · Exentar la deploy key en la regla
**Settings → Rulesets → main protegida → Add bypass** → marca **Deploy keys** → en su fila elige **Always allow** → baja y **Save changes**.
Resultado esperado en Bypass list: `Repository admin · Allow for pull requests only` y `Deploy keys · Always allow`. Nada más.

## Paso 5 · Avisar
Escribe en el chat de dirección: «deploy key y secreto listos». Con eso se lanza `GEN2-TUBERIA-CANAL-REPARACION-1` (nube), que cambia los dos pasos de push del workflow para usar la llave, agrega el evento `merge_group`, y prueba con un push real. Tú no haces nada más.

## Cómo saber que funcionó (después del encargo)
En **Actions**, el run del siguiente push a `main` muestra el paso «Re-deriva por comando y commitea [deriva]» en verde y el paso «Canal de publicación» ejecutado (no `skipped`). En `main` aparece un commit cuyo mensaje empieza por `[deriva]`. Y `python3 tools/corrida0.py status` en un clon fresco muestra `N_resultados_gen2_adoptados_activos` en 87 y `celdas_validadas` por encima de 92.

## Si algo sale mal
- Push rechazado con GH013 aunque la llave esté: la fila *Deploy keys* quedó en «pull requests only». Cámbiala a «Always allow».
- El workflow no arranca tras el push `[deriva]`: es lo esperado, `verify.yml` excluye `[deriva]` para no entrar en bucle; el canal ya corrió en el job anterior.
- Quieres revocarlo: borra la deploy key en **Settings → Deploy keys**. El canal deja de publicar; no rompe nada más.

## Lo que este manual NO hace
No activa la cola de fusión (D4): eso va en el mismo encargo, después de que `verify.yml` tenga `merge_group`, y se activa desde **Rulesets → main protegida → Require merge queue** en un segundo viaje. No cambia quién fusiona los PR que miden: sigues siendo tú.
