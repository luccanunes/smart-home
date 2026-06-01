import os
import sys
import time
import argparse
import tinytuya
from dotenv import load_dotenv

load_dotenv()

def inicializar_lampada(prefixo):
    """Helper para instanciar as lâmpadas usando o .env"""
    dev_id = os.getenv(f'LAMPADA_{prefixo}_ID')
    ip = os.getenv(f'LAMPADA_{prefixo}_IP')
    key = os.getenv(f'LAMPADA_{prefixo}_KEY')
    
    if not all([dev_id, ip, key]):
        print(f"[ERRO] Configurações para LAMPADA_{prefixo} incompletas no .env")
        return None
        
    luz = tinytuya.BulbDevice(dev_id, ip, key)
    luz.set_version(3.5) 
    return luz

def executar_amanhecer(cabeceira, mesa, modo_teste = False):
    print("[INFO] Iniciando simulação de amanhecer (30 minutos)...")
    
    # 1. Garante o estado inicial: Cabeceira liga no mínimo e ultra amarela
    if cabeceira:
        cabeceira.turn_on()
        cabeceira.set_white(brightness=10, colourtemp=0)
    
    # Mesa começa desligada nos primeiros 15 minutos
    if modo_teste:  # Se for teste rápido
        passos = 10
        tempo_espera = 2  # 20 segundos totais para testar visualmente
    else:
        passos = 60
        tempo_espera = 30  # 30 minutos totais (60 * 30s = 1800s)

    print(f"tempo de espera: {tempo_espera}")

    for i in range(1, passos + 1):
        progresso = i / passos
        
        # Lógica da Cabeceira: Transiciona do passo 1 ao fim
        if cabeceira:
            # Brilho vai de 10 a 1000 | Temperatura vai de 0 (quente) a 800 (neutro)
            brilho_cab = int(10 + (990 * progresso))
            temp_cab = int(800 * progresso)
            cabeceira.set_white(brightness=brilho_cab, colourtemp=temp_cab)
            
        # Lógica da Mesa: Só entra em ação na metade do tempo (progresso > 0.5)
        if mesa and progresso > 0.5:
            # Normaliza o progresso da mesa para ir de 0.0 a 1.0 na segunda metade
            progresso_mesa = (progresso - 0.5) * 2
            
            # Se estava desligada, liga
            if i == (passos // 2) + 1:
                mesa.turn_on()
                
            brilho_mesa = int(10 + (990 * progresso_mesa))
            temp_mesa = int(1000 * progresso_mesa) # Termina em branco frio pra dar energia
            mesa.set_white(brightness=brilho_mesa, colourtemp=temp_mesa)
            
        print(f"[Progresso {int(progresso*100)}%] Passo {i}/{passos}")
        time.sleep(tempo_espera)
        
    print("[INFO] Amanhecer concluído! Bom dia!")

def executar_anoitecer(cabeceira, mesa, modo_teste = False):
    print("[INFO] Iniciando rotina de anoitecer...")
    
    # 1. Mesa desliga imediatamente (sinal de fim de expediente/estudo)
    if mesa:
        print("[-] Desligando luz da mesa de trabalho.")
        mesa.turn_off()
        
    # 2. Cabeceira assume tom âmbar/quente relaxante em brilho médio
    if cabeceira:
        print("[+] Ajustando luz de cabeceira para modo noturno.")
        cabeceira.turn_on()
        cabeceira.set_white(brightness=400, colourtemp=0)
        
        # Fade out suave de 15 minutos até apagar
        if modo_teste:
            passos, tempo_espera = 5, 2
        else:
            passos, tempo_espera = 30, 30 # 15 minutos totais
            
        for i in range(1, passos + 1):
            progresso = i / passos
            # Brilho cai de 400 até 10
            brilho_atual = int(400 - (390 * progresso))
            cabeceira.set_white(brightness=brilho_atual, colourtemp=0)
            time.sleep(tempo_espera)
            
        cabeceira.turn_off()
    print("[INFO] Bons sonhos! Rotina de anoitecer finalizada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automação Solar do Quarto")
    parser.add_argument('--modo', choices=['amanhecer', 'anoitecer'], required=True)
    parser.add_argument('--teste', action='store_true', help="Executa em modo rápido para validação visual")
    args = parser.parse_args()
    
    # Inicializa o hardware baseado nas chaves do seu .env
    luz_cabeceira = inicializar_lampada('CABECEIRA')
    luz_mesa = inicializar_lampada('MESA')
    
    if args.modo == 'amanhecer':
        executar_amanhecer(luz_cabeceira, luz_mesa, modo_teste=args.teste)
    elif args.modo == 'anoitecer':
        executar_anoitecer(luz_cabeceira, luz_mesa, modo_teste=args.teste)