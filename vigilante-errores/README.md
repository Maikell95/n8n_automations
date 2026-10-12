# Vigilante de errores

Flujo de errores para n8n. Cuando cualquier otro flujo falla, decide si reintentarlo o avisarme por Telegram, sin llenarme el móvil de avisos repetidos.

```
Error en un flujo → Clasificar → Historial de reintentos → ¿Reintentar?
                                                          ├─ sí → ¿hay internet?
                                                          │        ├─ sí → esperar → relanzar la ejecución
                                                          │        └─ no → nada (lo relanza el Monitor de conexión)
                                                          └─ no → aviso (con anti-spam) → Telegram
```

## Cómo decide

- **Errores de conexión** (timeout, sin red, 429, 5xx…): relanza la ejecución original hasta **3 veces**, esperando **2, 10 y 30 minutos**. Los reintentos se cuentan en el historial de n8n, así que nunca pasa de 3 aunque otro flujo también relance.
- **Reintentos agotados**: aviso final con el enlace a la ejecución. Este aviso nunca se silencia.
- **Sin internet en ese momento**: no gasta reintentos. Lo deja para el [Monitor de conexión](../monitor-conexion/).
- **Otros errores** (credencial caducada, fallo de código…): aviso inmediato, sin reintentos.
- **Anti-spam**: el mismo fallo (flujo + nodo + error) avisa una vez cada 30 minutos; el siguiente aviso dice cuántas veces se repitió.

## Aviso

```
Fallo en n8n
Flujo: Lector de correos
Nodo: Avisar por Telegram
Error: ETIMEDOUT
Falló por conexión 4 veces (original + 3 reintentos). Queda para revisión manual.
```

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` + tu clave (Settings → n8n API) | Leer el historial y relanzar ejecuciones |
| Telegram | Telegram API | Avisos |

## Configurar

1. Importar `workflow.json` y asignar las credenciales.
2. Nodo **Avisar por Telegram**: cambiar `TU_CHAT_ID`.
3. Si n8n no corre en `localhost:5678`, cambiar la URL en los nodos HTTP.
4. **Activarlo** (en n8n 2.x un flujo de errores tiene que estar publicado).
5. En cada flujo a vigilar: **Settings → Error workflow → Vigilante de errores**.

Esperas, número de reintentos y ventana anti-spam se cambian al principio de los nodos de código.
