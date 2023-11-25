import openai
from dotenv import load_dotenv
import os


def openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai):
    print("Estou transcrevendo com o Whisper…")

    audio = open(caminho_audio, "rb")

    resposta = openai.Audio.transcribe(
        api_key=openai.api_key, model=modelo_whisper, file=audio
    )

    transcricao = resposta.text

    with open(
        f"texto_completo_{nome_arquivo}.txt", "w", encoding="utf-8"
    ) as arquivo_texto:
        arquivo_texto.write(transcricao)

        return transcricao


def openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": transcricao_completa + prompt_usuario},
        ],
        temperature=0.6,
    )

    resumo_instagram = resposta["choices"][0]["message"]["content"]

    with open(
        f"resumo_instagram_{nome_arquivo}.txt", "w", encoding="utf-8"
    ) as arquivo_texto:
        arquivo_texto.write(resumo_instagram)


def openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai):
    print("Gerando as hashtags com a open ai ... ")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.
    - A saída deve conter 5 hashtags.

    """

    prompt_usuario = f'Aqui está um resumo de um texto "{resumo_instagram}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil '

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario},
        ],
        temperature=0.6,
    )

    hashtags = resposta["choices"][0]["message"]["content"]

    with open(f"hashtag_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(hashtags)

    return hashtags


def openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai):
    print("Gerando a saida de texto para criacao de imagens com o GPT ...")

    prompt_sistema = """

    - A saída deve ser uma única, do tamanho de um tweet, que seja capaz de descrever o conteúdo do texto para que possa ser transcrito como uma imagem.
    - Não inclua hashtags

    """

    prompt_usuario = f"Reescreva o texto a seguir, em uma frase, para que descrever o texto abaixo em um tweet: {resumo_instagram}"
    
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
                {
                        "role": "system",
                        "content" : prompt_sistema
                },
                {
                        "role": "user",
                        "content": prompt_usuario
                }
        ],
        temperature = 0.6
    )

    texto_para_imagem = resposta["choices"][0]["message"]["content"]

    with open(f"texto_para_geracao_imagem_{nome_arquivo}.txt", "w",encoding='utf-8') as arquivo_texto:
            arquivo_texto.write(texto_para_imagem)

    return texto_para_imagem


def ferramenta_ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


def main():
    load_dotenv()

    caminho_audio = "audios/hipsters_154_testes_short.mp3"
    nome_arquivo = "hipsters_154_testes_short"
    url_podcast = "https://www.hipsters.tech/testes-de-software-e-inteligencia-artificial-hipsters-154/"

    api_openai = os.getenv("API_KEY_OPENAI")
    openai.api_key = api_openai

    modelo_whisper = "whisper-1"

    transcricao_completa = ferramenta_ler_arquivo("texto_completo_hipsters_154_testes_short.txt")
    resumo_instagram = ferramenta_ler_arquivo("resumo_instagram_hipsters_154_testes_short.txt")
    hashtags = ferramenta_ler_arquivo("hashtag_hipsters_154_testes_short.txt")
    resumo_imagem_instagram = openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai)


if __name__ == "__main__":
    main()
