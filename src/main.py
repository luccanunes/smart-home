import os
import time
import tinytuya
from dotenv import load_dotenv

load_dotenv()

DEVICE_ID = os.getenv('LAMPADA_CABECEIRA_ID')
IP_ADDRESS = os.getenv('LAMPADA_CABECEIRA_IP')
LOCAL_KEY = os.getenv('LAMPADA_CABECEIRA_KEY')
VERSION = 3.5

if not all([DEVICE_ID, IP_ADDRESS, LOCAL_KEY]):
    print("[Erro] Variáveis de ambiente não foram carregadas. Verifique o arquivo .env")
    exit(1)

print(f"Conectando à lâmpada no IP: {IP_ADDRESS}...")
lampada = tinytuya.BulbDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
lampada.set_version(VERSION)

try:
    print("Desligando a lâmpada...")
    lampada.turn_off()

    time.sleep(3)

    print("Ligando a lâmpada...")
    lampada.turn_on()


except Exception as e:
    print(f"Ocorreu um erro na comunicação local: {e}")

print("Fim do script!")