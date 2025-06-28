# Bot Amazon
Esse Bot serve para verificar a disponibilidade de até dois produtos na Amazon. Ele possui integração com o Telegram para enviar os status e as disponibilidades dos produtos. Ele também possui três tratativas para evitar ficar caindo em CAPTCHA.


## Como configurar o(s) Produto(s):
Para buscar por um produto colete a URL dele na Amazon e o título do anúncio, cole esses valores entre as aspas das variáveis "produto_1_url" e "produto_1_titulo" respectivamente.

Caso queira buscar pela disponibilidade de mais um produto, basta fazer o mesmo nas variáveis "produto_2_url" e "produto_2_titulo".

O programa não vai buscar por um produto caso você não tenha fornecido a url E o título do anúncio, caso falte uma dessas duas informações o programa é impedido de executar.


## Como configurar o Telegram:
Pesquise na internet como criar um Bot no telegram, por fim, colete o "Token" e o "Chat ID" do seu Bot criado e cole dentro das aspas das variáveis "TELEGRAM_TOKEN" e "TELEGRAM_CHAT_ID" respectivamente.

O Token do Telegram deve ser um valor semelhante a este(Alterei os valores reais): "0123456789:XXXX-A1A1A1A1A1-A1A1A1A1A1A1A1A1A1A"

O Chat ID do Telegram deve ser um valor semelhante a este(Alterei os valores reais): "9876543210"

(Essas informações são confidenciais, portanto guarde-os bem)


## Instruções para Executar:
(Certifique de ter o pyhton instalado em sua máquina)

1 - Abra o projeto na IDE de sua preferência

2 - Abra o terminal na IDE e digite os comandos abaixos

Caso queira instalar uma máquina virtual:

2.1 - Para criar a máquina virtual digite o comando:
    `python -m venv venv`

2.2 - Para executá-la depois da máquina ter sido criada digite o comando:
    `venv\Scripts\activate`

3 - Para instalar as dependências necessárias digite o comando:
    `pip install -r requirements.txt`

4 - Por fim, execute o programa com o comando:
    `python verifica_estoque.py`


## Instruções para executar após reiniciar o Computador

1 - Abra a IDE e nela abra o terminal

2 - Como a máquina virtual já esta criada, basta ativá-la:
    `venv\Scripts\activate`

4 - Por fim, execute o programa com o comando:
    `python verifica_estoque.py`