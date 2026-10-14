# Devoluciones

Formulario público para pedir una devolución. Comprueba el pedido, la IA clasifica el motivo y propone qué hacer, se guarda, el cliente recibe su número de solicitud y el equipo un aviso. Un segundo disparador aprueba o rechaza la solicitud y avisa al cliente.

```
Formulario → ¿pedido + correo correctos? ─ no → "No encontramos ese pedido"
          → ¿ya hay una solicitud abierta? ─ sí → "Ya tienes la DEV-…"
          → IA: motivo y propuesta → reglas de la tienda (plazo de 30 días)
          → tabla devoluciones → correo al cliente → Telegram → "Tu número es DEV-…"

POST /webhook/devoluciones/estado → actualizar estado → correo al cliente → respuesta JSON
```

## Cómo funciona

- **Valida contra la tabla `pedidos`**: el número tiene que existir y el correo coincidir. Si algo falla, el mensaje es el mismo (no revela qué pedidos existen). Acepta `PED-1004`, `ped 1004` o `1004`.
- **Plazo de 30 días** desde la fecha del pedido. Fuera de plazo se guarda como `rechazada` y el cliente ve el motivo al momento.
- **La IA clasifica el motivo**: defectuoso, talla/medida, no es lo esperado, llegó tarde u otro. También detecta si el cliente pide cambio o reembolso.
- **Las reglas deciden la propuesta**, no la IA: defectuoso → reembolso (o cambio si lo pide), talla → cambio, no es lo esperado → reembolso, llegó tarde → reembolso, otro → lo que proponga la IA. Si la IA falla, clasifica con palabras clave.
- **Avisa de lo raro**: producto que no aparece en el pedido o "defectuoso" sin fotos.
- **Sin duplicados**: si ya hay una solicitud abierta del mismo producto, no crea otra.
- **Correo al cliente** con su número (`DEV-AAMMDD-XXXX`). No se envía a direcciones de ejemplo (`@ejemplo.com`, `@example.com`).
- **Fotos opcionales**: se guarda cuántas y sus nombres.

## Aviso

```
📦 Devolución nueva · DEV-261014-GBA7
Pedido PED-1004 · Laura Gómez · 45,50 € · hace 16 días
Producto: Lámpara de escritorio LED
Motivo: Defectuoso — Llegó con el brazo roto y no enciende.
📷 1 foto(s)
💡 Propuesta: Reembolso — Lámpara defectuosa, el cliente pide reembolso.
Para decidir: POST /webhook/devoluciones/estado {"solicitud":"DEV-261014-GBA7","estado":"aprobada"}
✉️ confirmación enviada al cliente
```

## Cambiar el estado

```bash
curl -X POST http://localhost:5678/webhook/devoluciones/estado \
  -H 'Content-Type: application/json' \
  -d '{"solicitud":"DEV-261014-GBA7","estado":"aprobada","resolucion":"cambio","nota":"Te enviamos la talla M"}'
```

- `estado`: `aprobada`, `rechazada` o `pendiente`. `resolucion` (`reembolso` o `cambio`) y `nota` son opcionales. Al rechazar, la `nota` es el motivo que lee el cliente.
- Respuesta: `{"ok":true,"estado":"aprobada","antes":"pendiente","cliente_avisado":true}`. Errores con `400` (datos mal) o `404` (no existe).
- Repetir la misma llamada no reenvía el correo.

## Tablas

| Tabla | Columnas |
|---|---|
| `pedidos` | `pedido`, `fecha` (fecha), `cliente`, `correo`, `productos`, `importe` (número) |
| `devoluciones` | `solicitud`, `fecha` (fecha), `pedido`, `cliente`, `correo`, `producto`, `motivo`, `categoria`, `resolucion`, `explicacion`, `estado`, `motivo_rechazo`, `nota`, `fotos` (número), `fotos_nombres`, `importe_pedido` (número), `dias_desde_compra` (número), `origen`, `fecha_estado` (fecha) |

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` | Leer y guardar en las tablas |
| IA | OpenRouter | Clasificar el motivo |
| Correo | SMTP | Confirmación y resolución al cliente |
| Telegram | Telegram API | Aviso al equipo |

## Configurar

1. Crear las tablas `pedidos` y `devoluciones` con las columnas de arriba. En una tienda real, `pedidos` se cambia por la API de la tienda (Shopify, WooCommerce…).
2. Importar `workflow.json`. Cambiar `ID_TABLA_PEDIDOS`, `ID_TABLA_DEVOLUCIONES`, `tu-correo@gmail.com` y `TU_CHAT_ID`.
3. Asignar credenciales y activar. El formulario queda en `/form/devoluciones`.
4. El webhook de estado no lleva autenticación: si n8n está expuesto a internet, ponle Header Auth.
