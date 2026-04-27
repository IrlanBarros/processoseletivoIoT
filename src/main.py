print("Teste")
from machine import ADC, Pin, SoftI2C, PWM
import machine
import time
import network
import urequests
import ujson
import gc

# Ajuste de frequência para economia de energia (80MHz é o mínimo para Wi-Fi estável)
machine.freq(80000000)

# ===========================================================
# 1. CONFIGURAÇÕES E CONSTANTES
# ===========================================================
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

BOT_TOKEN = "8728927536:AAHqVBxaiQSK2mQiXsATxJQVo7jG89y89oE"
CHAT_ID   = "5461814823"

# Limiares de detecção e tempo
THRESHOLD_TILT     = 3000  
TIME_FATIGUE_MS    = 3000
ALPHA              = 0.2 # Fator do filtro passa-baixa (EMA)
CALIBRATION_SAMPLES = 20

# Gerenciamento de bateria
THRESHOLD_LOW_BATTERY = 2000 
BATTERY_COOLDOWN_MS   = 300000 # 5 minutos para evitar spam no Telegram

# Duty Cycling (Amostragem adaptativa)
SLEEP_NORMAL   = 800  
SLEEP_CRITICAL = 50   
ALERT_MARGIN   = 0.7

# Configuração de tempo para normalização após reset
COOLDOWN_RESET_MS      = 3000
MAX_NORMALIZATION_MS   = 10000 

# Emojis via Unicode Escape (para estabilidade de codificação)
EMOJI_ALERT    = "\u26A0"
EMOJI_SIREN    = "\U0001F6A8"
EMOJI_CHART    = "\U0001F4CA"
EMOJI_RECYCLE  = "\U0001F504"
EMOJI_CHECK    = "\u2705"
EMOJI_GEAR     = "\u2699"
EMOJI_ERROR    = "\u274C"
EMOJI_BELL     = "\U0001F514"

# Variáveis globais de controle
offset_y = 0
last_update_id = 0
filtered_y = 0
is_first_reading = True
alert_active = False
needs_normalization = False
fatigue_start_ms = 0
last_battery_alert = 0
last_heartbeat = time.ticks_ms()
reset_timestamp = 0
normalization_start_ms = 0

# ===========================================================
# 2. CONFIGURAÇÃO DE HARDWARE
# ===========================================================
try:
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
    mpu_addr = 0x68
    i2c.writeto_mem(mpu_addr, 0x6B, b'\x00') # Acorda o MPU6050

    led_alert = Pin(5, Pin.OUT)
    btn_reset = Pin(4, Pin.IN, Pin.PULL_UP)
    buzzer    = PWM(Pin(18))
    buzzer.duty(0)
    
    battery_pin = ADC(Pin(34))
    battery_pin.atten(ADC.ATTN_11DB) 
except Exception as e:
    print(f"[ERRO] Configuração de Hardware: {e}")

# ===========================================================
# 3. FUNÇÕES DO SISTEMA
# ===========================================================

def connect_wifi():
    """Realiza a conexão com a rede Wi-Fi configurada."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    print(f"[REDE] Conectando a {WIFI_SSID}", end="")
    attempts = 0
    while not wlan.isconnected() and attempts < 20:
        print(".", end="")
        time.sleep(0.5)
        attempts += 1
    if wlan.isconnected():
        print(f"\n[REDE] Conectado! IP: {wlan.ifconfig()[0]}")

def send_telegram(message):
    """Envia uma mensagem para o Telegram usando codificação manual de bytes."""
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        connect_wifi()
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    try:
        payload_bytes = ujson.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        r = urequests.post(url, data=payload_bytes, headers=headers)
        r.close()
        gc.collect()
    except Exception as e:
        print(f"[ERRO] Falha no envio Telegram: {e}")

def trigger_alarm(active):
    """Ativa ou desativa o buzzer e o LED de alerta."""
    try:
        if active:
            # Pino 18 para o Buzzer
            buzzer.freq(1000) 
            # 32768 é o duty cycle de 50% em 16 bits
            buzzer.duty_u16(32768) 
            # Pino 5 para o LED
            led_alert.value(1)
            print("[HW] Atuadores ligados")
        else:
            buzzer.duty_u16(0)
            led_alert.value(0)
            print("[HW] Atuadores desligados")
    except Exception as e:
        print(f"[ERRO HW] Falha no acionamento: {e}")

def calibrate_sensor():
    """Calcula o offset do sensor com base na posição atual do motorista."""
    global offset_y
    print("[CALIBRAÇÃO] Mantenha a cabeça reta...")
    total = 0
    count = 0
    while count < CALIBRATION_SAMPLES:
        try:
            data = i2c.readfrom_mem(0x68, 0x3D, 2)
            raw = int.from_bytes(data, 'big')
            if raw > 32767: raw -= 65536
            total += raw
            count += 1
            time.sleep_ms(50)
        except:
            continue
    offset_y = total / CALIBRATION_SAMPLES
    print(f"[CALIBRAÇÃO] Offset definido: {offset_y:.2f}")

def perform_system_reset(source_name):
    """Unifica o comportamento de reset (físico ou remoto)."""
    global fatigue_start_ms, alert_active, needs_normalization, reset_timestamp, normalization_start_ms
    print(f"[SISTEMA] Reset solicitado via: {source_name}")
    
    trigger_alarm(False)
    calibrate_sensor()
    
    fatigue_start_ms = 0
    alert_active = False
    needs_normalization = True
    reset_timestamp = time.ticks_ms()
    normalization_start_ms = time.ticks_ms()
    
    msg = f"{EMOJI_BELL} Sistema resetado e recalibrado via {source_name}."
    send_telegram(msg)

def check_battery():
    """Monitora o nível da bateria e envia alerta se estiver baixo."""
    global last_battery_alert
    reading = battery_pin.read()
    if reading < THRESHOLD_LOW_BATTERY:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_battery_alert) > BATTERY_COOLDOWN_MS:
            percentage = (reading / 4095) * 100
            msg = f"{EMOJI_ALERT} Bateria fraca ({percentage:.1f}%) no sensor de fadiga!"
            send_telegram(msg)
            last_battery_alert = now

def process_telegram_commands():
    """Verifica e executa comandos recebidos via bot do Telegram."""
    global last_update_id, THRESHOLD_TILT, alert_active, analysis_value
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=1"
    try:
        r = urequests.get(url)
        if r.status_code == 200:
            updates = r.json()
            for update in updates.get("result", []):
                last_update_id = update["update_id"]
                message = update.get("message", {})
                text = message.get("text", "").lower()
                sender_chat_id = str(message.get("chat", {}).get("id", ""))

                if sender_chat_id != CHAT_ID:
                    continue

                if text == "/status":
                    battery_reading = battery_pin.read()
                    perc = (battery_reading / 4095) * 100
                    status_msg = (f"{EMOJI_CHART} STATUS ATUAL:\n"
                                 f"• Bateria: {perc:.1f}%\n"
                                 f"• Inclinação: {analysis_value:.0f}\n"
                                 f"• Alerta: {'ATIVADO' if alert_active else 'Normal'}")
                    send_telegram(status_msg)

                elif text == "/recalibrar":
                    send_telegram(f"{EMOJI_RECYCLE} Iniciando recalibragem remota...")
                    calibrate_sensor()
                    send_telegram(f"{EMOJI_CHECK} Sensor recalibrado com sucesso!")

                elif text == "/reset":
                    perform_system_reset("Comando Remoto")

                elif text.startswith("/limiar "):
                    try:
                        new_value = int(text.split(" ")[1])
                        THRESHOLD_TILT = new_value
                        send_telegram(f"{EMOJI_GEAR} Novo limiar de inclinação: {new_value}")
                    except:
                        send_telegram(f"{EMOJI_ERROR} Erro: use /limiar [número]")
        r.close()
    except:
        pass

# ===========================================================
# 4. EXECUÇÃO PRINCIPAL
# ===========================================================
connect_wifi()
calibrate_sensor()
print("[SISTEMA] Monitoramento iniciado...")

while True:
    current_time = time.ticks_ms()
    
    # Rotinas de 10 segundos (Heartbeat, Bateria e Comandos Telegram)
    if time.ticks_diff(current_time, last_heartbeat) > 10000:
        print("[SISTEMA] Operando...")
        process_telegram_commands()
        check_battery()
        last_heartbeat = current_time

    try:
        # Verificação do botão físico
        if btn_reset.value() == 0:
            perform_system_reset("Botão do Operador")
            time.sleep_ms(500) # Debounce
            continue

        # Cooldown após qualquer reset
        if time.ticks_diff(current_time, reset_timestamp) < COOLDOWN_RESET_MS:
            continue

        # Leitura e Processamento do Sinal
        data = i2c.readfrom_mem(mpu_addr, 0x3D, 2)
        raw_y = int.from_bytes(data, 'big')
        if raw_y > 32767: raw_y -= 65536 

        corrected_reading = raw_y - offset_y

        if is_first_reading:
            filtered_y = corrected_reading
            is_first_reading = False
        else:
            filtered_y = (ALPHA * corrected_reading) + ((1 - ALPHA) * filtered_y)

        analysis_value = abs(filtered_y)

        # Lógica de Normalização (garantir que o motorista está reto antes de monitorar)
        if needs_normalization:
            if analysis_value < THRESHOLD_TILT:
                print("[SISTEMA] Posição normalizada.")
                needs_normalization = False
            elif time.ticks_diff(current_time, normalization_start_ms) > MAX_NORMALIZATION_MS:
                print("[SISTEMA] Timeout de normalização.")
                needs_normalization = False
            else:
                time.sleep_ms(200)
                continue

        # Detecção de Fadiga
        if analysis_value > THRESHOLD_TILT:
            if fatigue_start_ms == 0:
                fatigue_start_ms = current_time
            elif time.ticks_diff(current_time, fatigue_start_ms) > TIME_FATIGUE_MS:
                if not alert_active:
                    alert_active = True
                    trigger_alarm(True)
                    send_telegram(f"{EMOJI_SIREN} ALERTA: Fadiga detectada no operador!")
        else:
            fatigue_start_ms = 0

    except Exception as e:
        print(f"[ERRO] Loop: {e}")
    
    # Amostragem Adaptativa (Duty Cycling)
    if analysis_value > (THRESHOLD_TILT * ALERT_MARGIN) or alert_active:
        sleep_interval = SLEEP_CRITICAL 
    else:
        sleep_interval = SLEEP_NORMAL   

    time.sleep_ms(sleep_interval)
    gc.collect() # Manutenção preventiva de memória