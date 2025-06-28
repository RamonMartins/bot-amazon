import requests
import re
import time
import random
from bs4 import BeautifulSoup

produto_1_url = "https://www.amazon.com.br/dp/B0F8RFWW53/?coliid=I30RJVB054DRQ1"
produto_1_titulo = "Jogo, Donkey Kong Bananza, Nintendo Switch 2"
produto_2_url = ""
produto_2_titulo = ""

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
def verifica_estoque(produto_url, produto_titulo):
    headers = get_headers()
    response = requests.get(produto_url, headers=headers)

    if "Desculpe pelo inconveniente. Para continuar realizando suas compras, digite as" in response.text:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Verificação do texto de indisponibilidade
    indisponivel = soup.find(string=re.compile(r"Não temos previsão de quando este produto estará disponível novamente"))

    # Verificação extra: produto está mencionado na página
    produto_mencionado = soup.find(string=re.compile(produto_titulo))

    # Se não achou o texto de indisponibilidade, consideramos que pode estar disponível
    if indisponivel is None:
        # Mas, se mesmo assim o nome do produto está na página, é certeza que carregou certo
        if produto_mencionado:
            return True  # Produto pode estar disponível
        else:
            # Página carregou, mas nome do produto não encontrado — pode ser problema técnico
            #print("⚠️ Página carregada, mas o nome do produto não foi encontrado.")
            return None
    else:
        return False  # Texto de indisponibilidade presente


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
        print("Operando corretamente!")
    

    # Verifica a disponibilidade do Produto 1
    if produto_1_url != "" and produto_1_titulo != "":
        produto_1_resultado = verifica_estoque(produto_1_url, produto_1_titulo)
        if produto_1_resultado is None:
            #enviar_mensagem(f"⚠️ Falha ao verificar - possível CAPTCHA.")
            #print("⚠️ Falha ao verificar - possível CAPTCHA.")
            pass
        elif produto_1_resultado:
            enviar_mensagem(f"🚨 {produto_1_titulo} disponível! Veja: {produto_1_url}")
            print("Produto 1 disponível!")
        else:
            #enviar_mensagem("Produto 1 indisponível no momento.")
            print("Produto 1 indisponível no momento.")
            pass


    # Verifica a disponibilidade do Produto 2
    if produto_2_url != "" and produto_2_titulo != "":
        produto_2_resultado = verifica_estoque(produto_2_url, produto_2_titulo)
        if produto_2_resultado is None:
            #enviar_mensagem(f"⚠️ Falha ao verificar - possível CAPTCHA.")
            #print("⚠️ Falha ao verificar - possível CAPTCHA.")
            pass
        elif produto_2_resultado:
            enviar_mensagem(f"🚨 {produto_2_titulo} disponível! Veja: {produto_2_url}")
            print("Produto 2 disponível!")
        else:
            #enviar_mensagem("Produto 2 indisponível no momento.")
            print("Produto 2 indisponível no momento.")
            pass
    

    # Incrementa o contador de ciclos
    cont += 1
    # Gera um intervalo aleatório para uma nova verificação. Evita cair em um Captcha
    time.sleep(random.randint(90, 150))