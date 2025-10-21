## Bom dia/Boa tarde/Boa noite!!

Esse projeto visa criar um simples assistente virtual com respostas independentes e que gere um pouco de entretenimento.
Como essa é sua versão 1.0, ele não possuí features muito complexas nem comandos que faça ou automatize qualquer tarefa.
Contudo, o código está estruturado para se tornar livre a qualquer adição complexa ou simples que for fazer sem alterar
ou danificar o funcionamento dele.
Vamos ao básico:

## 🧠 Funcionalidades
- 🎤 Ouve e responde comandos de voz  
- 💬 Aceita entrada por texto no terminal  
- 🗣️ Fala usando a voz **Chris (ElevenLabs)**  
- 🔊 Alterna automaticamente para **gTTS** caso o ElevenLabs falhe  
- ⚙️ Usa modelos **Llama 3.1 (GROQ)** para gerar respostas  
- 🧩 Usa variáveis de ambiente (`.env`) para chaves de API

# Primeiro de tudo:
Neste caso, precisamos garantir que voce tenha ambas chaves API'S para funcionamento do Jarvis. Portanto, é preciso
a busca dessas chaves no:

## API GROQ: https://console.groq.com/home
## API ELEVEN_LABS: https://elevenlabs.io/app/developers/api-keys

O GROQ e o ElevenLabs são completamente gratúitos. E afins de curiosidades e conhecimento, Groq é uma API que utiliza
de comandos json para retirar informações de uma IA (no caso do GROQ, as ia's disponíveis são bem variáveis) e envia
a informação de volta, a qual o código decompõe, e retorna apenas a resposta dela que a API do ElevenLabs lê e retorna
em formato de audio ou "GGTs".

# Sobre a ElevenLabs:
Para fins de entreterimento, devo alertar de como alterar a voz da API para uma de sua escolha. Após fazer login e alterar
o .env com sua chave, você pode olhar no catálogo (gratuíto, ou se de sua escolha, pagar) para buscar um novo código e
alterar a voz. 
O passo a passo é:

    localize no código onde temos a 30 e a 34 linha, onde estamos criando a classe/objeto da sintetização da voz do Jarvis.

    Ele estará assim:

    class SistemaVoz:
    def __init__(self):
        pygame.mixer.init()
        self.falando = False
        self.voice_id = "iP95p4xoKVk53GoZ742B"  # Chris

        Essa ultima línha, deve ser alterada pelo código escolhido dentro dos parênteses.

Após essa alteração, vale ressaltar que como qualquer IA, Jarvis segue apenas um padrão que adicionamos de ínicio a ele, ou seja, 
o seu prompt.Caso queira alterar a sua personalidade, nome (e o gênero também) pode fazer alteração no prompt para o que tiver afim de fazer.
Entre a linha 150 e 159, temos o código:

    payload = {
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é JARVIS. Seja conciso e direto. Sempre chame o usuário de 'Chefe'." Entre os parenteses, está o Prompt que 
                        é enviado junto com a sua pergunta, ele define a personalidade do Jarvis. Precisa apenas alterar e escrever como você quer
                        que ele aja.
                    },
                    {
                        "role": "user",
                        "content": pergunta
                    }


Para uso, você pode clonar o repositório ou simplesmente copiar os códigos para sua IDE de uso. Recomendo utilizar o VSCode,
IDE onde foi feito este projeto.

## Instalação de bibliotecas

Para instalar as bibliotecas utilizadas, deve-se abrir o terminal do VSCode e utilizar o seguinte comando:

    pip install requests pygame speechrecognition python-dotenv gtts

ou

    python -m pip install requests pygame speechrecognition python-dotenv gtts


Este comando irá instalar automaticamente as bibliotecas que o código necessita para rodar.
Caso queira aprender sobre cada uma, recomendo a documentação ou tutoriais das mesmas, ou pesquise pelo ChatGPT e outras IA'S.
(sinta-se livre para usar o Jarvis hahaha)

Foi utilizado IA (DeepSeek e Phind) para tratamentos de erros (try, except, fallbacks e afins) e organização do código, de forma didática, para que eu pudesse
publicar da melhor maneira.

de resto, execute o comando - python main.py no terminal, ou apenas rode o código.

## Diga ou digite SAIR para encerrar o Jarvis, ou use CTRL+C.


Por fim, divirta-se!



