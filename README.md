# Automatizaciones n8n

Flujos de n8n en uso real. Cada carpeta tiene el JSON para importar y su explicación.

| Flujo | Qué hace |
|---|---|
| [Lector de correos](lector-correos-clientes/) | Filtra el correo y avisa por Telegram solo cuando escribe un posible cliente. Reglas + IA gratuita. |
| [Vigilante de errores](vigilante-errores/) | Flujo de errores: reintenta los fallos de conexión (2, 10 y 30 min) y avisa por Telegram del resto, sin spam. |
| [Monitor de conexión](monitor-conexion/) | Cuando vuelve internet tras una caída, reinicia los flujos y relanza lo que falló. |

## Levantar n8n

n8n + Postgres con Docker:

```bash
cp .env.example .env    # rellenar
docker compose up -d
```

Editor en `http://localhost:5678`.

## Importar un flujo

En n8n: **Workflows → Import from File** → `workflow.json`. Luego asignar las credenciales en cada nodo.

Recomendado: importar primero el Vigilante y asignarlo como *Error workflow* en el resto de flujos.

---

¿Necesitas una automatización para tu negocio? [maikell95.github.io/Portfolio](https://maikell95.github.io/Portfolio)
