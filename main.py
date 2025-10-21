import os
import requests
import pygame
import time
import speech_recognition as sr
from dotenv import load_dotenv
import tempfile

load_dotenv()

print("🔍 Verificando configurações...")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# verifica se a API do GROQ e ElevenLabs foi encontrada.
if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY não encontrada!")
    exit()

if not ELEVENLABS_API_KEY:
    print("❌ ELEVENLABS_API_KEY não encontrada!")
    exit()

print("✅ APIs configuradas!")

# =============================================================================
# SISTEMA DE VOZ - ELEVENLABS
# =============================================================================

class SistemaVoz:
    def __init__(self): #inicia a reprodução e gravação de mp3 da voz.
        pygame.mixer.init()
        self.falando = False
        self.voice_id = "iP95p4xoKVk53GoZ742B"  # Chris
        
    def falar(self, texto):
        if self.falando:
            return
            
        self.falando = True
        print(f"🎙️  JARVIS: {texto}")
        
        # Tenta ElevenLabs Chris(ou voz de sua escolha) primeiro
        if self._usar_elevenlabs(texto):
            self.falando = False
            return
            
        # Fallback para gTTS
        self._usar_gtts(texto)
        self.falando = False
            
    def _usar_elevenlabs(self, texto): #busca a API com base no URL que é enviado um prompt com o que foi dito para retonar as informações
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            data = {
                "text": texto,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.3,
                    "similarity_boost": 0.8
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10) #faz a conversão do JSON para o que vai ser dito

            #reproduz o aúdio
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                    temp_path = f.name
                    f.write(response.content)
                
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.music.unload()
                time.sleep(0.1)
                
                try:
                    os.unlink(temp_path)
                except:
                    pass
                return True
            else:
                print(f"❌ ElevenLabs: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ ElevenLabs: {e}")
            return False


    #USO DO GTTS PARA CORREÇÃO DE ERRO (caso a API não funcione, será usada a voz que estiver no seu computador)
    def _usar_gtts(self, texto):
        try:
            from gtts import gTTS
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_file = f.name
            
            tts = gTTS(text=texto, lang='pt-br', slow=False)
            tts.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            time.sleep(0.1)
            
            try:
                os.remove(temp_file)
            except:
                pass
                
        except Exception as e:
            print(f"❌ gTTS: {e}")

# =============================================================================
# CÉREBRO GROQ - DIRETO AO PONTO
# =============================================================================

#define onde vai ser buscado as informações da API
class CerebroJarvis:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.modelos = ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]

    #envia informações para API
    def pensar(self, pergunta):
        for modelo in self.modelos:
            resposta = self._tentar_modelo(pergunta, modelo)
            if resposta and resposta.strip():
                return resposta
        return "Processando."

    #define como vai ser organizado as informações que seram enviadas para API
    def _tentar_modelo(self, pergunta, modelo):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é JARVIS. Seja conciso e direto. Sempre chame o usuário de 'Chefe'." #Prompt que define personalidade do Jarvis e pode ser alterado.
                    },
                    {
                        "role": "user",
                        "content": pergunta
                    }
                ],
                "model": modelo,
                "temperature": 0.7,
                "max_tokens": 100
            }

            response = requests.post(self.url, headers=headers, json=payload, timeout=15)

            #define a resposta que irá ser retornada (exclui o formato JSON e deixa apenas a resposta)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            return None
                
        except:
            return None

# =============================================================================
# MICROFONE
# =============================================================================

#inicia a função do microfone
class OuvidosJarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microfone configurado!") #verifica se consegue encontrar um microfone no computador para usar
        except Exception as e:
            print(f"❌ Microfone: {e}") #caso não ache
            self.microphone = None
    
    def escutar(self):
        if not self.microphone:
            return None
            
        try:
            print("🎤 Escutando...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
            
            texto = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"👂 {texto}") #caso ache o microfone, e funcione, irá retornar o texto que foi escutado no terminal.
            return texto.lower()
            
        except:
            return None

# =============================================================================
# SISTEMA PRINCIPAL
# =============================================================================

#classe que gerencia o Jarvis por intero
class Jarvis:
    def __init__(self):
        self.voz = SistemaVoz()
        self.cerebro = CerebroJarvis()
        self.ouvidos = OuvidosJarvis()
        self.rodando = True
    
    def iniciar(self):
        print("\n" + "="*40)
        print("🤖 JARVIS - SISTEMA ATIVO") #mensagem de inicialização do Jarvis
        print("="*40)
        
        self.voz.falar("Sistemas online.") #frase inicial do Jarvis ao inicializar o código
        
        while self.rodando:
            if not self.voz.falando:
                comando = self.ouvidos.escutar()
                
                if comando:
                    if comando in ['sair', 'parar']: #define comandos para parar o funcionamento do Jarvis.
                        self.voz.falar("Encerrando sistemas.")
                        break
                    else:
                        resposta = self.cerebro.pensar(comando)
                        self.voz.falar(resposta)
            
            time.sleep(0.1)

# =============================================================================
# EXECUÇÃO
# =============================================================================

#puxa as funções principais para rodar o código
if __name__ == "__main__":
    try:
        jarvis = Jarvis()
        jarvis.iniciar()
    except KeyboardInterrupt:
        print("\nEncerrado.") #mensagem de encerramento.
    except Exception as e:

        print(f"Erro: {e}") #tratamento de erros gerais, caso tudo funcione e de algum erro mais específico.
