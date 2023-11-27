import openai
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from PIL import Image
from instabot import Bot
import shutil


# def openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai):
#     print("Estou transcrevendo com o Whisper…")

#     audio = open(caminho_audio, "rb")

#     resposta = openai.Audio.transcribe(
#         api_key=openai.api_key, model=modelo_whisper, file=audio
#     )

#     transcricao = resposta.text

#     with open(
#         f"texto_completo_{nome_arquivo}.txt", "w", encoding="utf-8"
#     ) as arquivo_texto:
#         arquivo_texto.write(transcricao)

#         return transcricao


# def openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai):
#     print("Resumindo com o gpt para um post do instagram ...")

#     prompt_sistema = """
#     Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

#     Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

#     - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
#     - Você deve utilizar o gênero neutro na construção do seu texto
#     - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
#     - O texto deve ser escrito em português do Brasil.

#     """
#     prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

#     resposta = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-16k",
#         messages=[
#             {"role": "system", "content": prompt_sistema},
#             {"role": "user", "content": f"{transcricao_completa} {prompt_usuario}"},
#         ],
#         temperature=0.6,
#     )

#     resumo_instagram = resposta["choices"][0]["message"]["content"]

#     with open(
#         f"resumo_instagram_{nome_arquivo}.txt", "w", encoding="utf-8"
#     ) as arquivo_texto:
#         arquivo_texto.write(resumo_instagram)


# def openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai):
#     print("Gerando as hashtags com a open ai ... ")

#     prompt_sistema = """
#     Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

#     Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

#     - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
#     - Você deve utilizar o gênero neutro na construção do seu texto
#     - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
#     - O texto deve ser escrito em português do Brasil.
#     - A saída deve conter 5 hashtags.

#     """

#     prompt_usuario = f'Aqui está um resumo de um texto "{resumo_instagram}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil '

#     resposta = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": prompt_sistema},
#             {"role": "user", "content": prompt_usuario},
#         ],
#         temperature=0.6,
#     )

#     hashtags = resposta["choices"][0]["message"]["content"]

#     with open(f"hashtag_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
#         arquivo_texto.write(hashtags)

#     return hashtags


# def openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai):
#     print("Gerando a saida de texto para criacao de imagens com o GPT ...")

#     prompt_sistema = """

#     - A saída deve ser uma única, do tamanho de um tweet, que seja capaz de descrever o conteúdo do texto para que possa ser transcrito como uma imagem.
#     - Não inclua hashtags

#     """

#     prompt_usuario = f"Reescreva o texto a seguir, em uma frase, para que descrever o texto abaixo em um tweet: {resumo_instagram}"

#     resposta = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": prompt_sistema},
#             {"role": "user", "content": prompt_usuario},
#         ],
#         temperature=0.6,
#     )

#     texto_para_imagem = resposta["choices"][0]["message"]["content"]

#     with open(
#         f"texto_para_geracao_imagem_{nome_arquivo}.txt", "w", encoding="utf-8"
#     ) as arquivo_texto:
#         arquivo_texto.write(texto_para_imagem)

#     return texto_para_imagem


def openai_dalle_gerar_imagem(
    resolucao, resumo_para_imagem, nome_arquivo, openai, qtd_imagens=1
):
    print("Criando uma imagem utilizando a API do DALL-E ...")

    prompt_user = (
        f"Uma pintura ultra futurista, textless, 3d que retrate: {resumo_para_imagem}"
    )

    resposta = openai.Image.create(prompt=prompt_user, n=qtd_imagens, size=resolucao)

    return resposta["data"]


def ferramenta_download_imagem(nome_arquivo, imagem_gerada, qtd_imagens=1):
    lista_nome_imagens = []
    try:
        for contador_imagens in range(0, qtd_imagens):
            caminho = imagem_gerada[contador_imagens].url
            imagem = requests.get(caminho)

            with open(f"{nome_arquivo}_{contador_imagens}.png", "wb") as arquivo_imagem:
                arquivo_imagem.write(imagem.content)

            lista_nome_imagens.append(f"{nome_arquivo}_{contador_imagens}.png")
        return lista_nome_imagens
    except:
        print("Ocorreu um erro!")
        return None


def ferramenta_ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


# def ferramenta_transcrever_audio_em_partes(caminho_audio_podcast, nome_arquivo):
#     print("Iniciando corte .. ")
#     audio = AudioSegment.from_mp3(caminho_audio_podcast)

#     dez_minutos = 10 * 60 * 1000

#     contador_pedaco = 1
#     arquivos_exportados = []

#     while len(audio) > 0:
#         pedaco = audio[:dez_minutos]
#         nome_pedaco_audio = f"{nome_arquivo}_parte_{contador_pedaco}.mp3"
#         pedaco.export(nome_pedaco_audio, format="mp3")
#         arquivos_exportados.append(nome_pedaco_audio)
#         audio = audio[dez_minutos:]
#         contador_pedaco += 1

#     return arquivos_exportados


# def openai_whisper_transcrever_em_partes(
#     caminho_audio, nome_arquivo, modelo_whisper, openai
# ):
#     print("Estou transcrevendo com o whispers ...")

#     lista_arquivos_de_audio = ferramenta_transcrever_audio_em_partes(
#         caminho_audio, nome_arquivo
#     )
#     lista_pedacos_de_audio = []

#     for um_pedaco_audio in lista_arquivos_de_audio:
#         audio = open(um_pedaco_audio, "rb")

#         resposta = openai.Audio.transcribe(
#             api_key=openai.api_key, model=modelo_whisper, file=audio
#         )

#         transcricao = resposta.text
#         lista_pedacos_de_audio.append(transcricao)

#     transcricao = "".join(lista_pedacos_de_audio)


# def selecionar_imagem(lista_nome_imagens):
#     return lista_nome_imagens[
#         int(
#             input(
#                 "Qual imagem você deseja selecionar, informe o numero do sufixo da imagem gerada?"
#             )
#         )
#     ]


def ferramenta_converter_png_para_jpg(caminho_imagem_escolhida, nome_arquivo):
    img_png = Image.open(caminho_imagem_escolhida)
    img_png.save(caminho_imagem_escolhida.split(".")[0] + ".jpg")

    return caminho_imagem_escolhida.split(".")[0] + ".jpg"


def postar_instagram(caminho_imagem, texto, user, password):
    if os.path.exists("config"):
        shutil.rmtree("config")
    bot = Bot()

    bot.login(username=user, password=password)

    resposta = bot.upload_photo(caminho_imagem, caption=texto)


def confirmacao_postagem(caminho_imagem_convertida, Legenda_postagem):
    print("f\nCaminho Imagem: (caminho_imagem_convertida}")
    print(f"\Legenda: {Legenda_postagem}")

    print(
        "\n\nDeseja postar os dados acima no seu instagram? Digite 's' para sim e 'n' para não."
    )
    return input()


def ferramenta_conversao_binario_para_string(texto):
    if isinstance(texto, bytes):
        return str(texto.decode())
    return texto


def main():
    load_dotenv()

    caminho_audio = "audios/output.mp3"
    nome_arquivo = "output"
    url_podcast = "https://www.emitte.com.br"
    resolucao = "1024x1024"
    qtd_imagens = 1

    usuario_instagram = os.getenv("USER_INSTAGRAM")
    senha_instagram = os.getenv("PASSWORD_INSTAGRAM")
    api_openai = os.getenv("API_KEY_OPENAI")
    openai.api_key = api_openai

    modelo_whisper = "whisper-1"

    # openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai) # 1
    # transcricao_completa = ferramenta_ler_arquivo(
    #     "texto_completo_output.txt"
    # )
    
    # openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai) #2
    resumo_instagram = ferramenta_ler_arquivo(
        "resumo_instagram_output.txt"
    )
    
    # # openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai) #3
    hashtags = ferramenta_ler_arquivo("hashtag_output.txt")
    
    # # openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai) #4
    # resumo_imagem_instagram = ferramenta_ler_arquivo(
    #     "texto_para_geracao_imagem_output.txt"
    # )
    
    # imagem_gerada = openai_dalle_gerar_imagem( #5
    #     resolucao, resumo_imagem_instagram, nome_arquivo, openai, qtd_imagens
    # )
    # print(imagem_gerada)
    
    # lista_imagens_geradas = ferramenta_download_imagem( #6
    #     nome_arquivo, imagem_gerada, qtd_imagens
    # )
    # print(lista_imagens_geradas)
    
    # caminho_imagem_escolhida = selecionar_imagem(lista_imagens_geradas)
    caminho_imagem_escolhida = 'img-IZHlSifTDISE3ZYndzG64iZd.png'
    caminho_imagem_convertida = ferramenta_converter_png_para_jpg( #7
        caminho_imagem_escolhida, nome_arquivo
    )

    legenda_imagem = f"Link do Podcast: {ferramenta_conversao_binario_para_string(url_podcast)} \n {ferramenta_conversao_binario_para_string(resumo_instagram)} \n {ferramenta_conversao_binario_para_string(hashtags)}"

    if confirmacao_postagem(caminho_imagem_convertida, legenda_imagem).lower() == "s":
        postar_instagram(
            caminho_imagem_convertida,
            legenda_imagem,
            usuario_instagram,
            senha_instagram,
        )


if __name__ == "__main__":
    main()
