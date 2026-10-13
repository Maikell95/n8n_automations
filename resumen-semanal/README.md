# Resumen semanal

Cada lunes a las 9:00 me llega por Telegram cómo fue la semana: clientes, prospección, salud de n8n y actividad en GitHub.

```
Lunes 9:00 → Leads · Prospección · Flujos · Ejecuciones (n8n) · Eventos y repos (GitHub) → Armar resumen → Telegram
```

## Qué incluye

- **Clientes**: leads de la semana (de [Captación de clientes](../captacion-clientes/)), cuántos son buenos, los 5 mejores y los que siguen sin respuesta.
- **Prospección**: cuántos contactos hay en cada estado y los seguimientos de los próximos 7 días. Los vencidos salen en rojo.
- **n8n**: ejecuciones y errores por flujo, y cuántas veces se reintentó.
- **GitHub**: commits, repos tocados, repos nuevos y estrellas (API pública, sin token).

## Aviso

```
Resumen semanal · 06/10 – 13/10

📬 Clientes
3 leads · 1 bueno
• Raul · web · 8/10

🎯 Prospección
respondio: 1 · pendiente: 1
🔴 12/10 · Servidor A (pendiente) — Enviar el ticket…
• 20/10 · Servidor B (respondio) — Le gustó el diseño…

⚙️ n8n
38 ejecuciones guardadas · 2 con error
• Lector de correos: 14 ok

🐙 GitHub
15 commits en 5 repos públicos · ⭐ 1 en total
```

## Tablas que usa

Dos tablas de datos de n8n (**Overview → Data tables**):

- `leads`: la llena el flujo de captación.
- `prospeccion`: la llevo a mano. Columnas: `servidor`, `pais`, `canal`, `contacto`, `estado` (pendiente / enviado / respondio / negociando / ganado / perdido), `fecha_contacto`, `proximo_seguimiento`, `nota`, `maqueta`.

## Configurar

1. Crear las tablas e importar `workflow.json`.
2. Cambiar `ID_TABLA_LEADS`, `ID_TABLA_PROSPECCION`, `TU_USUARIO` (GitHub) y `TU_CHAT_ID`.
3. Asignar las credenciales de n8n API y Telegram, y activar.
