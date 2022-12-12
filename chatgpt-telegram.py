import telebot
import openai
import boto3
import config
from revChatGPT.revChatGPT import Chatbot
from libs.stabilityApi import text_to_image
from pathlib import Path


# Uso de ChatGPT web sin API
if config.openai_mode == 'web':
    chatgpt_config = {
        # Email and password were deprecated use session_token
        #"email": config.openai_email,
        #"password": config.openai_password
        "session_token": config.openai_session,
        "cf_clearance": config.openai_clearance,
        "user_agent": config.openai_useragent
    }
    chatbot = Chatbot(chatgpt_config, conversation_id=None)

    # Función para generar una respuesta sin usar la API de ChatGPT
    def generate_response_noapi(prompt):
        response = chatbot.get_chat_response(prompt, output="text")
        return response['message']
# Uso de ChatGPT con API
else:
    # Inicializar la biblioteca openai utilizando tu secret key
    openai.api_key = config.openai_api_key

    # Función para generar una respuesta utilizando la API de ChatGPT
    def generate_response(prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.7,
        )

        # Devolver la primera respuesta generada por ChatGPT
        return response["choices"][0]["text"]

if config.voice_enabled:
    # Crear un cliente de Amazon Polly
    polly_client = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.region_name
    ).client('polly')

    # Crear una carpeta llamada "audio" en la carpeta en la que se está ejecutando el script
    Path("audio").mkdir(parents=True, exist_ok=True)
    open("audio/response.mp3", "a").close()

# Obtener el token del bot de Telegram y crear un bot
bot = telebot.TeleBot(token=config.telegram_token)

# Inicializar parámetros de stability.ai
engine_id = config.sd_engine_id
api_host = config.sd_api_host
api_key = config.sd_api_key

# Función para generar una imagen utilizando la API de stability-sdk
def generate_image(prompt):
    image = text_to_image(engine_id, api_host, api_key, prompt)

    # Devolver la primera imagen generada
    return image

# Establecer los comandos que el bot de Telegram puede aceptar
bot.set_my_commands([
    {
        "command": "/chatgpt",
        "description": "Enviar un mensaje al bot para que genere una respuesta utilizando la API de ChatGPT"
    },
    {
        "command": "/draw",
        "description": "Dibujar una imagen utilizando el API de stability-sdk"
    },
    {
        "command": "/voice",
        "description": "Devuelve la respuesta de ChatGPT, pero adjunta una transcripción como nota de voz generada por Amazon Polly"
    },
    {
        "command": "/resetchat",
        "description": "Reinicia la conversación a cero"
    }
])

# Procesar mensajes recibidos por el bot de Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Lista de IDs de usuarios autorizados
    AUTHORIZED_USER_IDS = config.telegram_users
    # Verificar si el ID del usuario que envió el mensaje coincide con el ID del usuario autorizado
    if message.from_user.id in AUTHORIZED_USER_IDS:
        # Obtener el texto del mensaje recibido
        text = message.text

        if text.startswith("/draw"):
            # Generar una imagen utilizando la API de stability-sdk
            image = generate_image(text[len("/draw"):].strip())
            # Enviar la imagen generada al remitente del mensaje
            bot.send_photo(chat_id=message.chat.id, photo=image)
        else:
            if text.startswith("/resetchat") and config.openai_mode == "web":
                chatbot.reset_chat()
                bot.send_message(chat_id=message.chat.id, text='_Se ha reiniciado la conversación_', parse_mode='MarkdownV2')
            else:
                # Generar una respuesta utilizando la API de ChatGPT
                #response = generate_response(text)
                if config.openai_mode == 'web':
                    response = generate_response_noapi(text)
                else:
                    response = generate_response(text)

                # Enviar la respuesta generada en texto al remitente del mensaje
                bot.send_message(chat_id=message.chat.id, text=response)

                # Generar una nota de audio la API de Amazon Polly
                if text.startswith("/voice"):
                    audio = polly_client.synthesize_speech(
                        Text=response,
                        VoiceId='Lucia',
                        Engine = 'neural',
                        OutputFormat="mp3"
                    )

                    # Obtener el contenido del archivo de audio generado
                    audio_stream = audio["AudioStream"]
                    # Guardar el contenido del archivo de audio en un archivo local
                    with open("audio/response.mp3", "wb") as file:
                        file.write(audio_stream.read())
                    #  Enviar nota de voz
                    with open("audio/response.mp3", "rb") as f:
                        bot.send_voice(chat_id=message.chat.id, voice=f)
    else:
        # Enviar un mensaje al usuario indicando que no está autorizado a recibir respuestas del bot
        bot.send_message(chat_id=message.chat.id, text='[Ah ah ah, ¡no has dicho la palabra mágica](https://media.giphy.com/media/owRSsSHHoVYFa/giphy.gif)', parse_mode='MarkdownV2')

# Iniciar el bot de Telegram

bot.polling()
