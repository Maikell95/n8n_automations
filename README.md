# Automatizaciones n8n

Flujos de n8n en uso real. Cada carpeta tiene el JSON para importar y su explicación.

| Flujo | Qué hace |
|---|---|
| [Lector de correos](lector-correos-clientes/) | Filtra el correo y avisa por Telegram solo cuando escribe un posible cliente. Reglas + IA gratuita. |
| [Vigilante de errores](vigilante-errores/) | Flujo de errores: reintenta los fallos de conexión (2, 10 y 30 min) y avisa por Telegram del resto, sin spam. |
| [Monitor de conexión](monitor-conexion/) | Cuando vuelve internet tras una caída, reinicia los flujos y relanza lo que falló. |
| [Captación de clientes](captacion-clientes/) | Formulario del portafolio → lead puntuado con IA, guardado, respuesta automática al cliente y aviso. |
| [Respaldo diario](respaldo-diario/) | Copia nocturna de todos los flujos y tablas a GitHub (solo si cambió algo) y `.zip` a Telegram. |
| [Resumen semanal](resumen-semanal/) | Cada lunes: clientes, prospección, salud de n8n y actividad en GitHub, por Telegram. |
| [Asistente de Telegram](asistente-telegram/) | Le pregunto al bot por mi n8n y responde con datos reales. Sin exponer n8n a internet. |
| [Atención al cliente (RAG)](atencion-rag/) | Chatbot que responde solo con la información del negocio (Supabase + pgvector) y avisa por Telegram cuando el cliente pide una persona. |
| [Devoluciones](devoluciones/) | Formulario de devolución: comprueba el pedido y el plazo, la IA clasifica el motivo, avisa al equipo y notifica al cliente la resolución. |
| [Inventario con stock bajo](inventario-stock/) | Registra ventas y entradas, avisa al momento cuando un producto baja del mínimo y cada mañana envía el pedido sugerido por proveedor. |
| [Lector de documentos](lector-documentos/) | Sube un PDF, DOCX o TXT y devuelve un resumen con lo importante: fechas, importes, riesgos y lo que conviene revisar. |

## Levantar n8n

n8n + Postgres con Docker:

```bash
cp .env.example .env    # rellenar
docker compose up -d
```

Editor en `http://localhost:5678`. El puente del Asistente de Telegram es opcional: `docker compose --profile asistente up -d`.

## Importar un flujo

En n8n: **Workflows → Import from File** → `workflow.json`. Luego asignar las credenciales en cada nodo.

Recomendado: importar primero el Vigilante y asignarlo como *Error workflow* en el resto de flujos.

---

¿Necesitas una automatización para tu negocio? [maikell95.github.io/Portfolio](https://maikell95.github.io/Portfolio)
