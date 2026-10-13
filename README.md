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
