# Captación de clientes

El formulario de contacto de mi portafolio manda un correo (EmailJS). Este flujo lo convierte en un lead: lo puntúa con IA, lo guarda, le responde al cliente al momento y me avisa.

```
Correo nuevo → ¿es del formulario? → ¿ya procesado? → IA: tipo, presupuesto, plazo, puntuación
            → guardar en la tabla leads → ¿responder? ─ sí → respuesta automática → Telegram
                                                      └ no (spam / malo) ─────────→ Telegram
```

## Cómo funciona

- **Por qué por correo y no un webhook**: n8n corre en mi PC. Si está apagada, el mensaje espera en Gmail y se procesa al volver. No se pierde ningún lead.
- **Lee el formato de EmailJS**: llega desde mi propia dirección, con el cliente en `Reply-To` y los campos `Nombre`, `Email` y `Mensaje`.
- **IA gratuita** (OpenRouter) para el tipo de trabajo, el presupuesto, el plazo, un resumen y una nota del 1 al 10. Si la IA falla, puntúa con reglas simples.
- **Responde en el idioma del cliente**, corto: *"Hola Raul, recibí tu mensaje sobre una web para tu negocio. Te respondo en menos de 24 h con una propuesta."* No responde al spam.
- **Sin duplicados**: cada correo se guarda por su `Message-ID`. Si una ejecución se relanza, no vuelve a guardarlo ni responde dos veces.

## Aviso

```
🟢 Lead bueno · 8/10 · web
Raul <raul@ejemplo.com>
Quiere una web, presupuesto de 200 USD
💰 200 USD

hola me gustaría hablarte sobre una web…

✉️ Ya le llegó la respuesta automática
```

## Plantilla de EmailJS

- **To Email**: tu correo · **Reply To**: `{{email}}` · **Subject**: `Nuevo mensaje desde el portafolio: {{name}}`
- **Contenido**: líneas `Nombre: {{name}}`, `Email: {{email}}`, `Mensaje:` y `{{message}}`.

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| Correo | IMAP | Leer el formulario |
| Respuesta | SMTP (Gmail: `smtp.gmail.com:465` + contraseña de aplicación) | Responder al cliente |
| IA | OpenRouter | Puntuar |
| API de n8n | Header Auth | Guardar en la tabla `leads` |
| Telegram | Telegram API | Aviso |

## Configurar

1. Crear la tabla `leads` con las columnas `fecha`, `nombre`, `correo`, `mensaje`, `tipo`, `presupuesto`, `plazo`, `resumen`, `puntuacion`, `calidad`, `respondido_auto`, `estado`, `origen` y `mensaje_id`.
2. Importar `workflow.json`. Cambiar `ID_TABLA_LEADS`, `tu-correo@gmail.com`, `TU_NOMBRE` (firma) y `TU_CHAT_ID`.
3. Asignar credenciales y activar.
