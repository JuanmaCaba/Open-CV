import telebot
import alarma_silenciosa


#First we get our bot token and our allowed user's id
with open("info_token.txt", "r")as file:
    checker_bot_token = file.read()

allowed_ids = []
with open("allowed_ids.txt", "r")as file:
    for user_id in file.readlines():
        allowed_ids.append(int(user_id))

#Create a teleBot object
bot = telebot.TeleBot(checker_bot_token)


running = False
exit_requested = False

#Create a function to use the movement detector script and interact with the user messages.
@bot.message_handler(func=lambda message: True)
def on_off(message):
    if message.from_user.id not in allowed_ids:
        bot.reply_to(message, "Lo siento, no tienes acceso a este bot.")
        return

    global running, exit_requested
    
    if message.text.lower() == "start":
        if running == False:
            running = True
            bot.reply_to(message, "La cámara se iniciará en 5 segundos.")
            alarma_silenciosa.start(str(message.from_user.id))
        elif running == True:
            bot.reply_to(message, "¡La cámara ya está funcionando!")

    elif message.text.lower() == "stop":
        if running == True:
            running=False
            bot.reply_to(message, "Cámara detenida. Para volver a ejecutarla, escriba: start")
            alarma_silenciosa.stop()
        elif running == False:
            bot.reply_to(message, "¡La cámara ya está apagada! Escriba start para activarla")

    elif message.text.lower() == "exit":
        if not exit_requested:
            exit_requested = True
            bot.reply_to(message, "El programa se va a apagar. Para volver a ejecutarlo, tendrás que hacerlo manualmente en la base central.\n¿Estás seguro de que quieres apagarlo?\nY/N")
        else:
            bot.reply_to(message, "La opción exit ya ha sido solicitada. Si deseas apagar el programa, por favor, responde con 'y'")

    elif message.text.lower() == "y":
        if exit_requested:
            bot.reply_to(message, "Apagando el programa...")
            alarma_silenciosa.stop()
            bot.stop_polling()
        else:
            bot.reply_to(message, "La opción 'y' solo puede ser utilizada después de solicitar la opción 'exit'")

    elif message.text.lower() == "n":
        bot.reply_to(message, "Okey makey")
        exit_requested = False

    elif message.text.lower() == "test":
        bot.reply_to(message, "Cargando test...")
        alarma_silenciosa.stop()
        alarma_silenciosa.test(str(message.from_user.id))
        
        if running == True:
            bot.reply_to(message, "Test Finalizado, la alarma vuelve a estar activa")
            alarma_silenciosa.start(str(message.from_user.id))
        else:
            bot.reply_to(message, "Test Finalizado. La alarma está en pausa actualmente. Si desea activarla escriba 'start'")

    elif message.text.lower() == "help":
        bot.reply_to(message, "A continuación se muestra la lista de comandos disponibles para este bot:\nStart-->Inicia la alarma con detección de movimiento.\nStop-->Detiene la alarma\nExit-->Finaliza mi ejecución y por tanto desconecta la alarma. Necesitaré una confirmación adicional con este comando.\nTest-->Ejecutaré una pequeña prueba para comprobar el funcionamiento de la cámara\n<b>Help</b>-->Te explicaré las veces que hagan falta como funcionan los comandos :)")

#Dont forget to keep reading the new incoming messages
bot.infinity_polling()