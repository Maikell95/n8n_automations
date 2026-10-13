"""Puente Telegram → n8n.

n8n corre solo en local, así que Telegram no puede mandarle los mensajes por webhook.
Este proceso pide los mensajes nuevos a Telegram (long polling) y se los pasa al
webhook interno de n8n. Solo reenvía los mensajes del chat permitido.
"""
import json, os, time, urllib.parse, urllib.request

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT = str(os.environ['CHAT_PERMITIDO'])
DESTINO = os.environ.get('N8N_WEBHOOK', 'http://n8n:5678/webhook/bot-telegram')


def log(*a):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), *a, flush=True)


def main():
    offset = None
    log('puente arrancado')
    while True:
        try:
            q = {'timeout': 50, 'allowed_updates': json.dumps(['message'])}
            if offset:
                q['offset'] = offset
            url = f'https://api.telegram.org/bot{TOKEN}/getUpdates?' + urllib.parse.urlencode(q)
            with urllib.request.urlopen(url, timeout=70) as r:
                updates = json.load(r).get('result', [])
        except Exception as e:
            log('telegram no responde:', type(e).__name__)
            time.sleep(10)
            continue
        for u in updates:
            offset = u['update_id'] + 1
            chat = str(u.get('message', {}).get('chat', {}).get('id', ''))
            if chat != CHAT:
                log('ignorado mensaje de otro chat')
                continue
            for intento in range(3):
                try:
                    req = urllib.request.Request(DESTINO, data=json.dumps(u).encode(), headers={'Content-Type': 'application/json'})
                    urllib.request.urlopen(req, timeout=30).read()
                    break
                except Exception as e:
                    log('n8n no responde:', type(e).__name__, f'intento {intento + 1}')
                    time.sleep(3)


if __name__ == '__main__':
    main()
