import requests
import os
import re
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

AMAZON_URL_Zelda_BOTW = "https://www.amazon.com.br/Jogo-Legend-Zelda-Breath-Wild/dp/B0F6DFZTD7/ref=zg_bs_g_16253312011_d_sccl_18/133-0259660-9610166"
AMAZON_URL_Pro_Controle = "https://www.amazon.com.br/dp/B0F6CY514C/?coliid=I2HZFZQ8CDXL89&colid=32KPQT0UZVH83&psc=0&ref_=list_c_wl_lv_ov_lig_dp_it"
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

def verifica_estoque(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    indisponivel = soup.find(string=re.compile(r"Não temos previsão de quando este produto estará disponível novamente"))
    return indisponivel is None

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': texto}
    requests.post(url, data=payload)

if verifica_estoque(AMAZON_URL_Zelda_BOTW):
    enviar_mensagem(f"🚨 Zelda - Breath of the Wild disponível! Veja: {AMAZON_URL_Zelda_BOTW}")
else:
    enviar_mensagem(f"⚔️ Zelda - BOTW indisponível no momento.")

if verifica_estoque(AMAZON_URL_Pro_Controle):
    enviar_mensagem(f"🚨 Pro Controle 2 disponível! Veja: {AMAZON_URL_Pro_Controle}")
else:
    enviar_mensagem(f"🕹️ Pro Controle 2 indisponível no momento")

time.sleep(120)