import requests
from bs4 import BeautifulSoup
import os

# Pega configurações do ambiente
AMAZON_URL = os.environ.get("AMAZON_URL")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def verifica_estoque():
    response = requests.get(AMAZON_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Verifica se o aviso de "Não disponível" está presente
    indisponivel = soup.find("span", class_="a-color-price a-text-bold", string="Não disponível.")
    
    # Se NÃO encontrar esse aviso, significa que pode estar disponível
    return indisponivel is None

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': texto
    }
    requests.post(url, data=payload)

if verifica_estoque():
    enviar_mensagem(f'🚨 Produto disponível! Veja: {AMAZON_URL}')
else:
    print("Produto indisponível no momento.")
