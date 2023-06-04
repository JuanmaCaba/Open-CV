import cv2 as cv
import numpy as np
import time
import os
import imageio as img
import requests



#Some global variables
with open("info_token.txt", "r")as file:
    checker_bot_token = file.read()

fondo = None
frames_checked = 0
media = []
testing = True
running = True

# Function to transform all the images in a folder into a GIF
def make_GIF():
    archivos = os.listdir("images")

    img_array = []

    for file in archivos[1:]:
        path = f"images\{file}"
        
        imagen = cv.imread(path)
        imagen = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
        img_array.append(imagen)

    img.mimwrite("Movement.gif", img_array, "GIF")


#Function to send the GIF made to a certain user by her/his chat id
def send_video(caption, user_id):
    global checker_bot_token

    url = "https://api.telegram.org/bot" + checker_bot_token + "/sendDocument"
    params = {"chat_id": user_id, "caption": caption}

    files = {"document": open("Movement.gif", "rb")} 
    response = requests.post(url, params=params, files=files)
    if response.status_code == 200:
        print("Archivo enviado exitosamente.")
    else:
        print("Error al enviar el archivo:", response.text)



#Main Function that will capture a webcam, apply some img editting to every frame (Basically getting a contours map for each frame and comparing it with a periodically updating background) and checking if something is moving (background and frame captured have different ammount of contours). Once movement is detected it will capture 20 frames in 10 seconds (It could record a video, but I personally think there is no need to use all those resources), then It will call the "make_Gif" func to make a GIF from these 20 imgs and finally send it to the desired user. Finally it will restart all the variables, empty the images folder, delete de GIF made and start the function again. 
def start(user_id):
    global fondo, frames_checked, media, testing, running
    
    print("Alerta iniciandose en 5 segundos")
    time.sleep(5)
    running = True
    vid = cv.VideoCapture(0)
    while running:
        isTrue, frame = vid.read()
        if isTrue == False:
            print("No se puede utilizar la camara correctamente")
            break

        if len(os.listdir("images"))>0:
            num = len(os.listdir("images"))
            path = f"images\{num}.jpg"
            cv.imwrite(path, frame)
            time.sleep(0.2)
            if len(os.listdir("images"))==20:
                make_GIF()
                send_video("Movimiento Detectado", user_id)
                for img in os.listdir("images"):
                    path = f"images\{img}"
                    os.remove(path)
                os.remove("Movement.gif")  
                frames_checked = 0
                media.clear()  
        else: 
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blurred = cv.GaussianBlur(gray, (5,5), 1)
            contours = cv.Canny(blurred, 100, 175)
            # cv.imshow("contornos", contours)
            
            if fondo is None or frames_checked == 150:
                if frames_checked == 150:
                    testing = False
                fondo = contours.copy()
                frames_checked = 0
                media.clear()
                print("Reseteando fondo estatico")               

            # cv.imshow("background",fondo)
            resta = cv.absdiff(contours, fondo)
            media_inmediata = np.mean(resta) 
            frames_checked += 1
            # cv.imshow("resta", resta)
            # print("media Inmediata", media_inmediata)
            if len(media)<20:
                media.append(media_inmediata)

            elif media_inmediata > np.mean(media) + 0.8 and testing == False:
                cv.imwrite(r"images\0.jpg", frame)
            # print("media fondo", np.mean(media)  
            
                
    vid.release()
                   

#Function that will stop the camara and reset all the variables
def stop():
    global running, frames_checked
    running = False
    print("La camara se ha detenido")
    if len(os.listdir("images"))>0:
        for img in os.listdir("images"):
            path = f"images\{img}"
            os.remove(path)
    try:
        os.remove("Movement.gif")  
    except FileNotFoundError:
        pass
    frames_checked = 0
    media.clear()
    return

#This function will take 20 frames and send them to the make_GIF func and send the GIF to the desired user. Finally it will reset all the variables
def test(user_id):
    vid = cv.VideoCapture(0)
    for i in range(20):
        time.sleep(0.2)
        isTrue,frame = vid.read()
        if isTrue == False:
            print("No se puede utilizar la camara correctamente")
            break
        num = len(os.listdir("images"))
        path = f"images\{num}.jpg"
        cv.imwrite(path, frame)
    vid.release()
    make_GIF()
    send_video("Video de prueba", user_id)
    for img in os.listdir("images"):
        path = f"images\{img}"
        os.remove(path)
    os.remove("Movement.gif")