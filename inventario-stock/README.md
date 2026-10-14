# Inventario con stock bajo

Cada entrada, venta o ajuste actualiza el stock y queda registrado. Si un producto baja del mínimo, avisa al momento. Cada mañana manda un resumen con lo que falta, cuántos días quedan y qué pedir a cada proveedor.

```
POST /webhook/inventario/movimiento → validar → stock nuevo → tabla movimientos
                                    → ¿cruzó el mínimo o se agotó? ─ sí → Telegram (1 vez al día por producto)

Cada día 8:00 → inventario → en el mínimo o por debajo → cobertura y pedido por proveedor
             → ¿hay algo nuevo? ─ sí → Telegram
                                └ no → nada
```

## Cómo funciona

- **Movimiento**: `{"sku":"CAF-002","tipo":"venta","cantidad":3}`. `entrada` y `venta` en positivo; `ajuste` con signo (`-2` por rotura, `+3` por recuento). Responde con el stock antes y después.
- **Errores claros**: `400` si faltan datos, `404` si el SKU no existe, `409` si no hay stock suficiente (nunca queda negativo).
- **Aviso al momento** solo cuando cruza el mínimo (estaba por encima y queda igual o por debajo) o cuando se agota.
- **Sin spam**: como mucho un aviso por producto y día (`ultimo_aviso`). El resumen de la mañana cuenta como aviso, y si se relanza el mismo día no se repite.
- **Cobertura**: días que aguanta el stock con las ventas de los últimos 30 días.
- **Pedido sugerido**: lo que falta para cubrir 30 días de ventas por encima del mínimo (el doble del mínimo si no hay ventas), agrupado por proveedor con el coste.
- **Todo bien = ningún mensaje.**

## Avisos

```
🟠 Stock bajo · ACC-002 Cafetera italiana 6 tazas
Quedan 7 (mínimo 8) tras venta de 5
Cobertura ≈ 10 días · TecnoHogar
Sugerido pedir: 21 u (325,50 €)
```

```
📦 Stock · 14/10
6 de 15 productos en el mínimo o por debajo

🔴 LIM-001 Pastillas de limpieza x8 — 0 / mín 12 · agotado
🟠 CAF-002 Café molido 250 g — 18 / mín 25 · 4 días
🟡 ENV-001 Bolsas kraft con válvula (100 u) — 6 / mín 10 · 22 días

Pedido sugerido (30 días de ventas sobre el mínimo)

Café Origen S.L. · 528,00 €
• CAF-002 Café molido 250 g: 127 u
• CAF-004 Café descafeinado 500 g: 19 u

Total estimado: 1487,80 €
```

## Tablas

| Tabla | Columnas |
|---|---|
| `inventario` | `sku`, `nombre`, `stock` (número), `stock_minimo` (número), `proveedor`, `precio_coste` (número), `ventas_30d` (número), `ultimo_aviso`, `actualizado` (fecha) |
| `movimientos` | `fecha` (fecha), `sku`, `tipo`, `cantidad` (número), `stock_antes` (número), `stock_despues` (número), `aviso` (sí/no), `nota` |

`ventas_30d` suma cada venta que entra por el webhook. En una tienda real conviene recalcularla desde las ventas (ERP o tienda online).

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` | Leer y guardar en las tablas |
| Telegram | Telegram API | Avisos |

## Configurar

1. Crear las tablas `inventario` y `movimientos` con las columnas de arriba y cargar los productos.
2. Importar `workflow.json`. Cambiar `ID_TABLA_INVENTARIO`, `ID_TABLA_MOVIMIENTOS` y `TU_CHAT_ID`.
3. Asignar credenciales y activar. La hora del resumen se cambia en el nodo **Cada mañana 8:00**.
4. Conectar la tienda o el TPV para que llame al webhook en cada venta. Sin autenticación: si n8n está expuesto, ponle Header Auth.
