import requests
import re
import time
import random
from bs4 import BeautifulSoup

AMAZON_URL_Zelda_BOTW = "https://www.amazon.com.br/Jogo-Legend-Zelda-Breath-Wild/dp/B0F6DFZTD7/ref=zg_bs_g_16253312011_d_sccl_18/133-0259660-9610166"
AMAZON_URL_Pro_Controle = "https://www.amazon.com.br/dp/B0F6CY514C/?coliid=I2HZFZQ8CDXL89&colid=32KPQT0UZVH83&psc=0&ref_=list_c_wl_lv_ov_lig_dp_it"
TELEGRAM_TOKEN="COLE_AQUI_O_TOKEN_DO_SEU_BOT_DO_TELEGRAM"   # Altere os dados
TELEGRAM_CHAT_ID="COLE_AQUI_O_ID_DO_SEU_BOT_DO_TELEGRAM"    # Altere os dados
cont = 0


# Configs de navegadores diferentes para a seção
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
]


# Gera uma seção aleatória a cada acesso. Evita cair em um Captcha
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive"
    }


# Função de verificação de disponibilidade do produto
def verifica_estoque(url):
    headers = get_headers()
    response = requests.get(url, headers=headers)

    #print("======CORPO DA RESPOSTA======")     # Usar apenas para debug
    #print(response.text)

    if "Desculpe pelo inconveniente. Para continuar realizando suas compras, digite as" in response.text:
        #enviar_mensagem(f"⚠️ CAPTCHA detectado. Aguardando para tentar novamente.")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    indisponivel = soup.find(string=re.compile(r"Não temos previsão de quando este produto estará disponível novamente"))      # Busca o texto de indisponibilidade na página
    return indisponivel is None


# Envia a mensagem para o Telegram
def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': texto}
    requests.post(url, data=payload)


# Função principal do programa para solicitar as verificações
while True:
    # Verifica um intervalo de 40 ciclos para informar que o programa continua em execução
    if (cont == 40):
        cont = 0
        enviar_mensagem(f"Operando corretamente!")
    
    # Verifica a disponibilidade do Produto 1
    resultado_zelda = verifica_estoque(AMAZON_URL_Zelda_BOTW)
    if resultado_zelda is None:
        enviar_mensagem(f"⚠️ Falha ao verificar Zelda - possível CAPTCHA.")
    elif resultado_zelda:
        enviar_mensagem(f"🚨 Zelda - Breath of the Wild disponível! Veja: {AMAZON_URL_Zelda_BOTW}")
    else:
        #enviar_mensagem("⚔️ Zelda - BOTW indisponível no momento.")
        pass

    # Verifica a disponibilidade do Produto 2
    resultado_controle = verifica_estoque(AMAZON_URL_Pro_Controle)
    if resultado_controle is None:
        enviar_mensagem(f"⚠️ Falha ao verificar Pro Controle - possível CAPTCHA.")
    elif resultado_controle:
        enviar_mensagem(f"🚨 Pro Controle 2 disponível! Veja: {AMAZON_URL_Pro_Controle}")
    else:
        #enviar_mensagem("🕹️ Pro Controle 2 indisponível no momento.")
        pass
    
    # Incrementa o contador de ciclos
    cont += 1
    # Gera um intervalo aleatório para uma nova verificação. Evita cair em um Captcha
    time.sleep(random.randint(90, 150))