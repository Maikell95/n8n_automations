# Automatizaciones n8n

Flujos de n8n en uso real. Cada carpeta tiene el JSON para importar y su explicación.

| Flujo | Qué hace |
|---|---|
| [Lector de correos](lector-correos-clientes/) | Filtra el correo y avisa por Telegram solo cuando escribe un posible cliente. Reglas + IA gratuita. |

## Levantar n8n

n8n + Postgres con Docker:

```bash
cp .env.example .env    # rellenar
docker compose up -d
```

Editor en `http://localhost:5678`.

## Importar un flujo

En n8n: **Workflows → Import from File** → `workflow.json`. Luego asignar las credenciales en cada nodo.

---

¿Necesitas una automatización para tu negocio? [maikell95.github.io/Portfolio](https://maikell95.github.io/Portfolio)
