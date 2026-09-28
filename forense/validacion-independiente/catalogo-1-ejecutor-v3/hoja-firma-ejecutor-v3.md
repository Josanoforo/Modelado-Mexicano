# Hoja de decisiones materiales · ASTRA6 C1 ejecutor v3

PROPUESTO-POR-EJECUTOR. El merge de este PR puede recibir el producto técnico; la firma de contenido del contrato y la autorización de acceso se registran por sus circuitos propios. Ninguna opción altera números, tolerancias, sellos v2 o permisos existentes.

| Decisión | Opciones | Recomendación y efecto |
|---|---|---|
| Firmar el contrato de estados v3 antes de un C1 real | Firmar `CONTRATO-v3.md` con hash `821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb`; devolver con corrección material | **Firmar tras revisión del mapa v2→v3.** Habilita codificar denominador cero e incertidumbre no identificada sin mentir. Una corrección material exige versión sucesora y nuevo sello, nunca cambiar este hash retrospectivamente. |
| Acreditar contexto nuevo de proveedor | Provisionar un broker de la cuenta ya autorizada con sesión nueva, prompt/archivos allowlist y recibo atestado; mantener gate pendiente | **Provisionar y probar el broker antes de cualquier C1 real.** `session_request.py` y la prueba sintética cubren protocolo, no acreditan proveedor/memoria real. Si no se provisiona, el gate sigue pendiente. |
| Abrir paquete real | Autorizar por paquete y cohorte luego de los cuatro gates; conservar reserva | **Conservar reserva hasta autorización específica.** Este acto solo usó sintéticos y no solicita acceso global. |

No se solicita firma nueva para la cláusula de autonomía ni para el «Acordado» de la misión: ya constan en el archivo de fuentes.
