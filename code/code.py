import network           # Biblioteca para rede Wi-Fi
import socket            # Biblioteca para comunicação de rede (servidor web)
from machine import Pin  # Controlo de GPIOs (entradas/saídas digitais)
import time              # Biblioteca para pausas e contagem de tempo

# Função para LIGAR o ESP32 ao Wi-Fi
def conecta_wifi(ssid, senha):
    wlan = network.WLAN(network.STA_IF)  # Cria interface de rede no modo Station (cliente Wi-Fi)
    wlan.active(True)                    # Ativa a interface Wi-Fi

    # Se ainda não está a ligar, continua a tentar
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(ssid, senha)

        # Aguarda até obter ligação
        while not wlan.isconnected():
            time.sleep(1)

    # Exibe o IP recebido via DHCP
    print("Ligado! IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]  # Retorna o IP para uso posterior

# LED interno
led = Pin(2, Pin.OUT)
led.off()  # Começa desligado

# Função que gera a página HTML conforme o estado atual do LED
def gerar_html(estado_led):
    botao_texto = "Desligar" if estado_led else "Ligar"  # texto botão
    botao_valor = "off" if estado_led else "on"          # valor enviado
    return f"""<!DOCTYPE html>
<html>
<head><title>Controlo LED ESP32</title></head>
<body>
    <h1>Controlo do LED</h1>
    <p>Estado atual: {"Ligado" if estado_led else "Desligado"}</p>
    <form method="get" action="/">
        <button type="submit" name="led" value="{botao_valor}">{botao_texto}</button>
    </form>
</body>
</html>"""

# Liga ao Wi-Fi
ip = conecta_wifi("NOME_REDE", "PASSWORD")

# Inicializa servidor
s = socket.socket()
s.bind((ip, 80))
s.listen(1)

print(f"Servidor a rodar em http://{ip}")

# Loop principal
while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    print('Requisição de:', addr)

    # Processa o parâmetro da URL
    if 'led=on' in request:
        led.on()
    elif 'led=off' in request:
        led.off()

    # Atualiza o HTML com o estado atual do LED
    html = gerar_html(led.value())

    # Envia resposta HTTP
    cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    cl.send(html)
    cl.close()
