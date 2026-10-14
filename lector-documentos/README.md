# Lector de documentos

Subes un contrato, factura o informe (PDF, DOCX o TXT) y en pantalla aparece un resumen con puntos clave, fechas, importes, riesgos y preguntas para hacer. También llega por Telegram y queda guardado.

```
Formulario → ¿PDF, DOCX o TXT con contenido? ─ no → error claro
          → sacar el texto → ¿escaneado o vacío? ─ sí → error claro
          → ¿largo? ─ sí → resumir por partes → unir ─┐
                     └ no ───────────────────────────┴→ IA: análisis → tabla → Telegram → pantalla final
```

## Cómo funciona

- **Tres formatos**: PDF con el nodo *Extract From File*; DOCX descomprimiendo el `.docx` (es un zip) y leyendo `word/document.xml`; TXT en UTF-8 (o Latin-1 si viene de Windows antiguo).
- **Errores claros** en la misma pantalla: archivo vacío, formato no soportado (los `.doc` antiguos piden guardarse como `.docx`), PDF protegido o dañado, y **PDF escaneado** (imagen sin texto: se detecta por la poca cantidad de texto por página).
- **Documentos largos**: más de 12.000 caracteres se trocean en partes de ~8.000 (cortando en párrafos), la IA resume cada parte y luego analiza los resúmenes juntos. Máximo 10 partes (~80.000 caracteres); si hay más, se avisa de que se recortó.
- **Lo que devuelve la IA**: resumen en 5 líneas, puntos clave, fechas y plazos, importes, riesgos (cláusulas, penalizaciones, renovaciones, lo que falta) y preguntas recomendadas. Se puede indicar el tipo de documento y qué interesa ("penalizaciones si cancelo") para que lo priorice.
- **Si la IA falla**, saca fechas, importes y cláusulas típicas con reglas y lo indica.
- **Telegram** se corta por líneas antes del límite (nunca a mitad de una etiqueta). Lo completo queda en la tabla.

## Ejemplo (contrato de 2 páginas)

```
📄 Contrato desarrollo y mantenimiento web
contrato_servicios.pdf · PDF · 2 pág. · 4247 caracteres · analizado con IA

Resumen
• El precio total es de 18.500 € IVA no incluido, con pagos fraccionados por hitos
• El mantenimiento cuesta 450 €/mes con 8 horas incluidas, renovable automáticamente salvo aviso de 60 días
• Si el cliente cancela el mantenimiento antes de los 12 meses debe abonar el 50 % de las cuotas pendientes

Fechas
• 15 de febrero de 2027 — Entrega final como máximo
• 60 días — Preaviso mínimo para no renovar el mantenimiento

Riesgos
⚠️ La responsabilidad del proveedor queda limitada a lo cobrado en los 12 meses anteriores

Preguntas
❓ ¿Se firmarán los anexos (encargo del tratamiento y especificaciones) antes de empezar?
```

## Tabla

`documentos_leidos`: `fecha` (fecha), `archivo`, `formato`, `tipo_indicado`, `tipo_detectado`, `titulo`, `interes`, `paginas` (número), `caracteres` (número), `partes` (número), `resumen`, `puntos_clave`, `fechas`, `importes`, `riesgos`, `preguntas`, `origen`.

## Requisitos

| Credencial | Tipo en n8n | Para qué |
|---|---|---|
| API de n8n | Header Auth: `X-N8N-API-KEY` | Guardar en la tabla |
| IA | OpenRouter | Resumir y analizar |
| Telegram | Telegram API | Enviar el resultado |

## Configurar

1. Crear la tabla `documentos_leidos` con las columnas de arriba.
2. Importar `workflow.json`. Cambiar `ID_TABLA_DOCUMENTOS` y `TU_CHAT_ID`.
3. Asignar credenciales y activar. El formulario queda en `/form/lector-documentos`.

Con el modelo gratuito, un contrato corto tarda 1-3 minutos y uno largo bastante más: la pantalla espera sola. Con un modelo de pago baja a segundos.
