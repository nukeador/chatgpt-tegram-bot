# chatgpt-telegram-bot

Este es un script de Python que permite a un usuario enviar mensajes a un bot de Telegram y recibir respuestas generadas utilizando la API de ChatGPT. También permite a los usuarios generar imágenes utilizando la API de stability.ia y obtener una transcripción de la respuesta de ChatGPT en formato de nota de voz generada por Amazon Polly.

<img src="images/example.png" width=500px />

## Requisitos

Para utilizar este script, necesitarás:

* Una cuenta de OpenAI y una [clave de API](https://beta.openai.com/account/api-keys)
* Un bot de Telegram y un [token de autenticación](https://core.telegram.org/bots#how-do-i-create-a-bot)
* (Opcional) Una cuenta de Amazon Web Services y [credenciales de acceso](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials)
* (Opcional) Una cuenta en stability.ai y [credenciales de acceso](https://beta.dreamstudio.ai/membership?tab=apiKeys)

Todos estos servidios dan créditos gratuitos de inicio, a Diciembre de 2022, estos son los costes de sus APIs:

- OpenIA: 0,004$/petición
- Stability IA: 0,002$/petición (con 30 steps)
- Amazon Polly: Aprox. 0,0125$/minuto de audio

## Instalación

Para instalar las dependencias necesarias para ejecutar este script en Python, se puede utilizar el administrador de paquetes pip.

Primero, asegúrate de tener pip instalado en tu sistema. Puedes verificar si ya lo tienes ejecutando el siguiente comando en una terminal:


```
pip --version
```


Si no tienes pip instalado, puedes instalarlo siguiendo las instrucciones en [la página oficial de pip](https://pip.pypa.io/en/stable/installation/)


Para instalar las dependencias, ejecuta el siguiente comando en una terminal en el mismo directorio que el archivo `requirements.txt`:


```
pip install -r requirements.txt
```


Esto instalará todos los paquetes necesarios en tu sistema. Una vez que se hayan instalado, podrás ejecutar el script sin problemas.

## Configuración

Antes de ejecutar el script, necesitarás configurar las credenciales de acceso para OpenAI, AWS, Telegram y stability.ai. Para hacerlo, renombra el archivo llamado `config.py.sample` en el mismo directorio que el script Python a `config.py` y rellena las variables con tus credenciales de acceso.

## Ejecución

Para ejecutar el script, asegúrate de estar en el mismo directorio que el archivo `chatgpt-telegram.py` y ejecuta el siguiente comando en una terminal:

```
python chatgpt-telegram.py
```

Esto iniciará el bot de Telegram. Una vez que esté en ejecución, puedes enviarle mensajes utilizando la aplicación de Telegram.

El bot acepta los siguientes comandos:

- `/chatgpt`: Enviar un mensaje al bot para que genere una respuesta utilizando la API de ChatGPT
- `/draw`: Dibujar una imagen utilizando el API de stability.ia
- `/voice`: Devuelve la respuesta de ChatGPT, pero adjunta una transcripción como nota de voz generada por Amazon Polly

El bot puede ser también incluido en grupos, pero solo responderá a los usuarios autorizados que hayas configurado. Ten cuidado dando acceso a otras personas ya que el bot estará usando tus APIs de los servicios y estas suelen tener un coste.

Puedes parar el script en cualquier momento pulsando Ctrl+D

## Configurar el bot como un servicio en tu servidor Linux

Para configurar el script ``chatgpt-telegram.py`` como un servicio en un servidor Linux, puedes seguir los siguientes pasos:

***Nota:*** Las siguientes instrucciones están optimizadas para un servidor Ubuntu Linux, pueden ser diferentes para otras distribuciones.

1. Crea un archivo de configuración para el servicio en el directorio ``/etc/systemd/system``. Puedes hacerlo con el comando ``sudo nano /etc/systemd/system/chatgpt-telegram.service``.
2. Agrega el siguiente contenido al archivo, reemplazando <RUTA_DEL_SCRIPT> con la ruta completa del script ``chatgpt-telegram.py`` en tu servidor:

```
[Unit]
Description=ChatGPT Telegram Bot Service

[Service]
Type=simple
WorkingDirectory=<RUTA_DEL_SCRIPT>
ExecStart=<RUTA_DEL_SCRIPT>/chatgpt-telegram.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

3. Guarda y cierra el archivo.
4. Haz que el sistema operativo cargue la configuración del nuevo servicio con el comando ``sudo systemctl daemon-reload``.
5. Inicia el servicio con el comando ``sudo systemctl start chatgpt-telegram``.
6. Opcionalmente, puedes habilitar el servicio para que se inicie automáticamente cada vez que se inicie el servidor con el comando ``sudo systemctl enable chatgpt-telegram``.

Una vez que hayas seguido estos pasos, el script ``chatgpt-telegram.py`` se ejecutará como un servicio en tu servidor. Puedes verificar el estado del servicio con el comando ``sudo systemctl status chatgpt-telegram``.
