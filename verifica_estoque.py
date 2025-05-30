import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Pega configurações do ambiente
#AMAZON_URL = "https://www.amazon.com.br/Jogo-Legend-Zelda-Breath-Wild/dp/B0F6DFZTD7/ref=zg_bs_g_16253312011_d_sccl_18/133-0259660-9610166"
#AMAZON_URL = os.environ.get("https://www.amazon.com.br/Jogo-Legend-Zelda-Kingdom-Nintendo/dp/B0F6DDZMZY/ref=zg_bs_g_16253312011_d_sccl_19/133-0259660-9610166")
AMAZON_URL = os.environ.get("AMAZON_URL_Zelda_BOTW")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
}

def verifica_estoque():
    session = requests.Session()
    response = session.get(AMAZON_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Procura o texto exato (ou parte dele) na página
    indisponivel = soup.find(string=re.compile(r"Não temos previsã de quando este produto estará disponível novamente"))

    if indisponivel:
        return False
    else:
        return True

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': texto
    }
    requests.post(url, data=payload)

if verifica_estoque():
    enviar_mensagem(f'🚨 Produto disponível! Veja: {AMAZON_URL}')
    print("Produto disponível.")
else:
    enviar_mensagem(f'😢 Produto disponível!')
    print("Produto indisponível no momento.")
    