# Lector de correos — posibles clientes

Recibo mucho correo. Este flujo lo lee todo y solo me avisa por Telegram cuando escribe alguien que puede ser cliente.

```
Correo nuevo → Descartar automáticos → Detectar cliente → ¿Es cliente?
                                                          ├─ sí → Telegram
                                                          └─ dudoso → IA ─ cliente → Telegram
                                                                        └ no → descarta
```

## Cómo decide

1. **Descarta lo automático.** `no-reply`, notificaciones, boletines (cabeceras `List-Unsubscribe`, `Precedence: bulk`, `Auto-Submitted`). Excepción: mensajes e invitaciones de Workana y LinkedIn.
2. **Reglas.** Busca señales en remitente, asunto y primeras líneas: presupuesto, web, app, automatización, bot, servidor, plugin… (español e inglés). Con señales → aviso directo, sin gastar IA.
3. **IA solo para dudosos.** Personas sin señales claras ("Hola", "Consulta"). Un modelo gratuito de OpenRouter decide si es cliente.
4. **Si la IA falla**, reintenta 3 veces. Si sigue fallando, avisa igual marcado como *sin clasificar*. No se pierde ningún correo.

No marca nada como leído y recuerda el último correo procesado: si n8n se cae, al volver revisa lo que llegó mientras tanto. Además guarda el `Message-ID` de los últimos 300 avisos (solo cuando el aviso salió bien): si el monitor reinicia el flujo o se relanza una ejecución, no avisa dos veces del mismo correo.

## Aviso

```
Posible cliente (IA)
De: Roberto Díaz <roberto@ejemplo.com>
Asunto: Consulta
Buenas, vi tu trabajo en GitHub y quería saber si haces sistemas de reservas…
```

## Requisitos

| Credencial | Tipo en n8n | Dónde se saca |
|---|---|---|
| Correo | IMAP | Gmail: `imap.gmail.com:993` + contraseña de aplicación |
| Telegram | Telegram API | Bot creado con @BotFather |
| IA | OpenRouter | openrouter.ai → Keys (modelos `:free`, sin coste) |

## Configurar

1. Importar `workflow.json`.
2. Asignar las tres credenciales.
3. Nodo **Descartar automáticos**: cambiar `tu-correo@ejemplo.com` por tu correo.
4. Nodo **Avisar por Telegram**: cambiar `TU_CHAT_ID` (te lo da @userinfobot). Escríbele `/start` a tu bot antes.
5. Activar.

Las señales y las plataformas se ajustan en los nodos de código, al principio de cada uno.
