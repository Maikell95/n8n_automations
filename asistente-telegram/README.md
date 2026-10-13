# Asistente de Telegram

Le pregunto a mi bot de Telegram por mi n8n y me responde con datos reales: qué hace cada flujo, qué falló, cuántos leads llegaron o qué seguimientos tengo pendientes.

```
Telegram → puente (long polling) → webhook de n8n → solo mi chat
        → foto de n8n: flujos, ejecuciones, errores, tablas → IA con memoria → respuesta
```

## Por qué un puente

Telegram solo manda los mensajes a una URL pública, y mi n8n es local (`127.0.0.1`). En vez de exponerlo a internet, el [puente](puente/puente.py) (un contenedor de Python de 60 líneas) pide los mensajes a Telegram y se los pasa al webhook interno de n8n. **Solo reenvía los mensajes de mi chat**; los demás se descartan antes de llegar a n8n.

## Qué sabe

- **Flujos**: si están activos, cuándo se disparan, sus pasos y lo que dicen los comentarios de su código.
- **Ejecuciones**: la última de cada flujo y las correctas y fallidas de 7 días.
- **Errores**: los últimos 8, con flujo, nodo y mensaje.
- **Tablas**: todas las filas de las tablas de datos (leads, prospección…).
- **Memoria**: los últimos 12 mensajes de la conversación. Con `/nuevo` empieza de cero.

Solo lee: si le pido cambiar algo, me explica cómo hacerlo. Nunca muestra credenciales. Si la IA gratuita no responde, avisa en vez de quedarse callado.

## Ejemplo

```
Yo: ¿hubo errores esta semana?
Bot: Sí, 2:
• 12/10 22:01 · Vigilante de errores · "Avisar por Telegram" · sin DNS (se cayó internet)
• 13/10 10:52 · Resumen semanal · "Leads" · parámetro mal formado (ya corregido)
```

## Configurar

1. Añadir al `.env` el token del bot y tu chat: `TELEGRAM_BOT_TOKEN=…` y `TELEGRAM_CHAT_ID=…`.
2. `docker compose --profile asistente up -d` (servicio incluido en el [`docker-compose.yml`](../docker-compose.yml)).
3. Importar `workflow.json`, asignar n8n API, OpenRouter y Telegram, cambiar `TU_CHAT_ID` y activar.
4. Cambiar el texto del sistema en el nodo **Responder con IA** para describir tu propio montaje.
