import openai
from dotenv import load_dotenv
import os

def openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai):
    print("Estou transcrevendo com o Whisper…")
    
    audio = open(caminho_audio, "rb")
    
    resposta = openai.Audio.transcribe(
        api_key=openai.api_key,
        model = modelo_whisper,
        file = audio
    )
    
    transcricao = resposta.text
    
    with open(f"texto_completo_{nome_arquivo}.txt", "w",encoding='utf-8') as arquivo_texto:
        arquivo_texto.write(transcricao)

        return transcricao

def main():
    load_dotenv()
    
    caminho_audio = "audios/hipsters_154_testes_short.mp3"
    nome_arquivo = "hipsters_154_testes_short"
    url_podcast = "https://www.hipsters.tech/testes-de-software-e-inteligencia-artificial-hipsters-154/"
    
    api_openai = os.getenv("API_KEY_OPENAI")
    openai.api_key = api_openai
        
    modelo_whisper = "whisper-1"
         
    transcricao_completa = openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai)
    
if __name__ == "__main__":
    main()
