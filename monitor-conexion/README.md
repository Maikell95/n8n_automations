# Monitor de conexión

n8n en local tiene un problema: si se va internet, los flujos fallan y nadie los relanza. Este flujo comprueba la conexión cada minuto y, cuando vuelve, lo pone todo en marcha otra vez.

```
Cada minuto → ¿hay internet? → ¿volvió tras una caída?
                                  └─ sí → reiniciar flujos activos
                                        → relanzar ejecuciones que fallaron por conexión
                                        → aviso por Telegram
```

## Cómo funciona

- **Caída** = 2 comprobaciones fallidas seguidas (los microcortes no cuentan). El estado se guarda entre ejecuciones.
- **Al volver la conexión**:
  - Reinicia todos los flujos activos (menos él mismo y el vigilante), para que disparadores como IMAP vuelvan a conectar limpios.
  - Relanza las ejecuciones que fallaron por conexión durante la caída, salvo las que ya gastaron sus 3 reintentos.
  - Avisa: `Conexión recuperada tras 12 min. Reinicié 2 flujos. Relancé 5 ejecuciones.`
- No guarda las ejecuciones correctas, para no llenar n8n con una cada minuto.
- Comprueba contra `api.telegram.org`, que es lo que hace falta para avisar.

Pensado para usarse junto al [Vigilante de errores](../vigilante-errores/).

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` + tu clave | Listar flujos y ejecuciones, reiniciar y relanzar |
| Telegram | Telegram API | Aviso de recuperación |

## Configurar

1. Importar `workflow.json` y asignar las credenciales.
2. Nodo **Avisar por Telegram**: cambiar `TU_CHAT_ID`.
3. En los nodos **Elegir flujos** y **Elegir ejecuciones**: cambiar `ID_DEL_VIGILANTE` por el ID de tu Vigilante (está en su URL).
4. Si n8n no corre en `localhost:5678`, cambiar la URL en los nodos HTTP.
5. Settings → Error workflow → Vigilante de errores. Activar.
