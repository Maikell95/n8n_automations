# Respaldo diario

Copia de seguridad de n8n todas las noches: todos los flujos y las tablas de datos. Va a un repo privado de GitHub con historial y además me llega el `.zip` por Telegram.

```
Cada día 3:00 → Flujos + Tablas (API de n8n) → un archivo por flujo y por tabla
             → GitHub: árbol nuevo → ¿cambió algo? ─ sí → commit "Respaldo AAAA-MM-DD"
                                                     └ no → nada
             → .zip → Telegram
```

## Cómo funciona

- **Un archivo por flujo** (`flujos/nombre.json`) y por tabla (`tablas/nombre.json`). En GitHub se ve qué cambió cada día.
- **Solo hace commit si algo cambió.** Sube el árbol completo con la API de Git; si GitHub devuelve el mismo árbol que ayer, no crea commit.
- **Quita lo que cambia solo** (`staticData` de cada ejecución) para que el historial muestre únicamente cambios reales.
- **Un flujo borrado desaparece también del respaldo**: cada día se sube la foto completa, no solo lo nuevo.
- Si falla por conexión, el [Vigilante](../vigilante-errores/) lo relanza. Relanzarlo no duplica commits.

## Aviso

```
Respaldo de n8n · 2026-10-13
7 flujos · 2 tablas
GitHub: cambios guardados (ver commit)
```
+ `respaldo-n8n-2026-10-13.zip`

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` | Leer flujos y tablas |
| GitHub | GitHub API (token *fine-grained* solo para el repo de respaldo, permiso **Contents: Read and write**) | Guardar el respaldo |
| Telegram | Telegram API | Enviar el `.zip` |

## Configurar

1. Crear un repo **privado** con un README (necesita al menos un commit).
2. Importar `workflow.json`, asignar credenciales y cambiar `TU_USUARIO/TU_REPO_DE_RESPALDO` y `TU_CHAT_ID`.
3. Activar. La hora se cambia en el primer nodo.
