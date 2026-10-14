# Atención al cliente con IA (RAG)

Asistente que responde a los clientes de un negocio usando **solo** su propia información (horarios, precios, políticas, preguntas frecuentes…). Si no sabe algo o el cliente pide una persona, me avisa por Telegram.

Son dos flujos: uno responde y otro carga la información. La base de datos es Supabase (Postgres + pgvector).

```
Chat de n8n ─┐
             ├→ conversación de la sesión → últimos 8 mensajes → config del negocio
Webhook ─────┘   → embedding de la pregunta → buscar fragmentos parecidos → prompt
                 → IA → guardar mensajes → ¿necesita persona? ─ sí → marcar + Telegram ─┐
                                                              └ no ─────────────────────┴→ respuesta

Formulario (.txt / .md / .pdf o texto pegado) → extraer texto → trocear (800 caracteres, 100 de solape)
            → embeddings en lotes de 20 → crear documento → guardar fragmentos
```

## Cómo funciona

- **Dos entradas, una lógica**: el chat integrado de n8n (público, para probarlo) y un webhook `POST /webhook/atencion-rag` para conectar un widget en la web del cliente.
- **Solo con los datos del negocio**: busca los 5 fragmentos más parecidos a la pregunta y la IA responde únicamente con eso y con la configuración del negocio (nombre, horario, contacto, tono, instrucciones). No inventa precios ni datos.
- **Memoria corta por sesión**: lee los últimos 8 mensajes de la conversación. Si la pregunta es corta (*"¿y el domingo?"*), la busca junto con la anterior para entender el seguimiento.
- **Pasa a una persona**: si el cliente la pide o la IA no tiene la respuesta, la conversación queda marcada `necesita_humano` y llega un aviso a Telegram con la pregunta y lo que se respondió.
- **Responde en el idioma del cliente**, corto. IA gratuita de OpenRouter.
- **Embeddings `gte-small` (384 dimensiones)** calculados en una función de Supabase (`embed`), porque n8n no trae ese modelo. Así la base es compatible con la versión del mismo asistente hecha solo con Supabase.
- **Todo queda guardado**: cada conversación y sus mensajes (canal `n8n`), con las fuentes usadas.

## Ejemplo

```
Cliente: ¿Abrís los sábados?
Asistente: Sí, abrimos los sábados de 10:00 a 14:00.
Cliente: ¿y el domingo?
Asistente: Los domingos y festivos permanecemos cerrados.
Cliente: Quiero hablar con una persona, por favor
Asistente: Puedo ayudarte a contactar con un agente humano. Escribe a hola@negocio-ejemplo.test o llama al +00 000 000 000.
```

Aviso en Telegram:

```
🙋 Un cliente necesita una persona (Atención RAG · n8n)
Sesión: chat-1 · chat

Cliente: Quiero hablar con una persona, por favor

Asistente: Puedo ayudarte a contactar con un agente humano. Escribe a hola@negocio-ejemplo.test o llama al +00 000 000 000.
```

## Webhook

```
POST /webhook/atencion-rag
{ "mensaje": "¿Abrís los sábados?", "sesion": "id-del-visitante" }
→ { "respuesta": "...", "sesion": "...", "conversacion_id": "...", "fuentes": [{ "titulo": "...", "similitud": 0.83 }], "necesita_humano": false }
```

Si no se manda `sesion`, se crea una y se devuelve para reutilizarla en los siguientes mensajes.

## Requisitos

| Credencial | Tipo en n8n | Valor | Para qué |
|---|---|---|---|
| Supabase service role | Custom Auth | `{"headers": {"apikey": "<service_role>", "Authorization": "Bearer <service_role>"}}` | Leer y escribir en la base (API REST de Supabase) |
| Supabase ADMIN_KEY | Header Auth | Nombre `x-admin-key`, valor: el secreto `ADMIN_KEY` del proyecto | Función `embed` |
| IA | OpenRouter | | Responder |
| Telegram | Telegram API | | Aviso |

La `service_role` está en **Supabase → Project Settings → API Keys** (pestaña *Legacy API keys*, clave `service_role`). Si el proyecto solo tiene las claves nuevas, usa la *Secret key* (`sb_secret_…`) y solo la cabecera `apikey`: `{"headers": {"apikey": "sb_secret_…"}}`. Cualquiera de las dos salta el RLS: guárdala solo en la credencial de n8n, nunca en el flujo ni en la web.

## Configurar

1. En Supabase, ejecutar el esquema de la base (tablas `config`, `documentos`, `fragmentos`, `conversaciones`, `mensajes`, funciones `buscar_fragmentos` y `obtener_conversacion`, canal `n8n`) y desplegar la función `embed` con el secreto `ADMIN_KEY`.
2. Importar `workflow-atencion.json` y `workflow-conocimiento.json`. Cambiar `TU_PROYECTO` (ref del proyecto de Supabase) y `TU_CHAT_ID`.
3. Crear las dos credenciales de Supabase con esos nombres exactos y asignarlas en los nodos HTTP.
4. Activar los dos flujos. Abrir el formulario de **Cargar conocimiento**, subir la información del negocio y probar en el chat del flujo de atención.
5. Los datos del negocio (nombre, horario, contacto, tono…) se editan en la tabla `config`.
