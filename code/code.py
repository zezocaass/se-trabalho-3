import network
import socket
import time
from machine import Pin

# --- Configuração Wi-Fi ---
ssid = 'zezocas'
password = '123456789'

led = Pin(22, Pin.OUT)  # LED onboard do ESP32 (pino 2) ou "22" para o led externo
led.off()  # Começa desligado

# --- Conectar ao Wi-Fi ---
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)

print('Conectado ao Wi-Fi. IP:', station.ifconfig()[0])

# --- Função para gerar HTML dinâmico ---
def gerar_html(estado_led):
    estado_texto = "Ligado" if estado_led else "Desligado"
    return f"""<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Trabalho 3 - Controlo do Hardware</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    html, body {{
      height: 100%;
    }}

    body {{
      font-family: sans-serif;
      background-color: #f9f9f9;
      display: flex;
      flex-direction: column;
    }}

    header {{
      background-color: #ffffff;
      padding: 1rem;
      border-bottom: 1px solid #ddd;
    }}

    header h1 {{
      font-size: 1.2rem;
      font-weight: normal;
      margin-left: 1rem;
    }}

    .container {{
      display: flex;
      flex: 1;
    }}

    aside {{
      width: 220px;
      background-color: #b5a556;
      padding: 1rem;
      color: black;
    }}

    aside h2 {{
      font-weight: bold;
      margin-bottom: 1rem;
    }}

    aside p {{
      margin-bottom: 0.5rem;
    }}

    main {{
      flex: 1;
    }}

    .header-bar {{
      background-color: #666;
      color: white;
      padding: 1rem;
    }}

    .header-bar h2 {{
      font-size: 1.8rem;
      font-weight: bold;
    }}

    .estado-led {{
      background-color: #e9ecef;
      margin: 2rem;
      padding: 2rem;
      border-radius: 10px;
      text-align: center;
    }}

    .estado-led h3 {{
      font-size: 3rem;
      margin-bottom: 1.5rem;
    }}

    .botoes {{
      display: flex;
      justify-content: center;
      gap: 1rem;
    }}

    .ligar {{
      background-color: #b5a556;
      color: black;
      border: none;
      padding: 0.5rem 1rem;
      font-weight: bold;
      cursor: pointer;
      border-radius: 5px;
    }}

    .desligar {{
      background-color: black;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      font-weight: bold;
      cursor: pointer;
      border-radius: 5px;
    }}

    .info {{
      display: flex;
      justify-content: space-around;
      padding: 2rem;
    }}

    .info div {{
      width: 30%;
    }}

    .info h3 {{
      font-family: monospace;
      font-size: 1.6rem;
      margin-bottom: 1rem;
    }}

    .info p {{
      font-size: 0.95rem;
      line-height: 1.5;
      color: #333;
    }}

    footer {{
      background-color: #ccc;
      text-align: center;
      padding: 0.5rem;
      font-size: 0.8rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Trabalho 3</h1>
  </header>

  <div class="container">
    <aside>
      <h2>Grupo:</h2>
      <p><strong>José João - a55827</strong></p>
      <p><strong>Johnny Alves - 55817</strong></p>
      <p><strong>Miguel Carneiro - 63424</strong></p>
    </aside>

    <main>
      <section class="header-bar">
        <h2>Controlo do Hardware</h2>
      </section>

      <section class="estado-led">
        <h3 id="estado-led-texto">LED {estado_texto}</h3>
        <div class="botoes">
          <form method="get" action="/">
            <button class="ligar" name="led" value="on" type="submit">Ligar</button>
            <button class="desligar" name="led" value="off" type="submit">Desligar</button>
          </form>
        </div>
      </section>

      <section class="info">
        <div>
          <h3>ESP 32</h3>
          <p>O ESP32 é um microcontrolador moderno, potente e versátil [...]</p>
        </div>
        <div>
          <h3>LED</h3>
          <p>O LED (Díodo Emissor de Luz) é um componente eletrónico [...]</p>
        </div>
        <div>
          <h3>Resistência</h3>
          <p>A resistência (ou resistor) é usada em série com o LED para limitar [...]</p>
        </div>
      </section>
    </main>
  </div>

  <footer>
    <p>Copyright 2025</p>
  </footer>
</body>
</html>
"""

# --- Servidor Web ---
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Servidor web ativo em http://%s' % station.ifconfig()[0])

while True:
    conn, addr = s.accept()
    print('Cliente conectado de', addr)
    request = conn.recv(1024).decode()
    print('Requisição:', request)
    
    # Controlo do LED via parâmetros GET
    if 'led=on' in request:
        led.on()
    elif 'led=off' in request:
        led.off()
    
    # Gera HTML dinâmico com estado atual do LED
    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + gerar_html(led.value())
    conn.send(response)
    conn.close()

