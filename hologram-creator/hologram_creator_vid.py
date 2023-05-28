import cv2 as cv
import numpy as np


# IMG Rotation function 
def rotate(img, angle):
    height, width = img.shape[:2]
    rotation_matrix = cv.getRotationMatrix2D((width/2, height/2), angle, 1.0)
    cos_theta = np.abs(rotation_matrix[0, 0])
    sin_theta = np.abs(rotation_matrix[0, 1])

    new_width = int(width * cos_theta + height * sin_theta)
    new_height = int(width * sin_theta + height * cos_theta)

    rotation_matrix[0, 2] += (new_width - width) / 2
    rotation_matrix[1, 2] += (new_height - height) / 2

    rotated_img = cv.warpAffine(img, rotation_matrix, (new_width, new_height), borderMode=cv.BORDER_REPLICATE)

    return rotated_img

# Open the input video
cap = cv.VideoCapture(r'Video Path')

# Check if the video was opened correctly
if not cap.isOpened():
    print("Error al abrir el video")
    exit()

# read the input video dimensions 
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))//3
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))//3
fps = cap.get(cv.CAP_PROP_FPS)



# Create the VideoWriter output object
out = cv.VideoWriter('video_salida.avi', cv.VideoWriter_fourcc(*'mp4v'), int(fps), (2*frame_height + frame_width, 2*frame_height + frame_width))

#We will apply the necessary changes to each frame of the video
while True:
    ret, base_img = cap.read()
    if not ret:
        break

    #Set the new video dimensions 
    x = base_img.shape[1]//3
    y = base_img.shape[0]//3

    hologram_coor = 2*y + x 

    base_hologram = np.zeros((hologram_coor, hologram_coor, 3), dtype="uint8")

    #Create the four imgs for every frame
    img1=cv.resize(base_img, (x, y))

    img2=rotate(img1, 90)

    img3=rotate(img1, 180)

    img4=rotate(img1, 270)

    #Combine them into one single img
    base_hologram[0:y, y:x+y] = img1
    base_hologram[y:x+y, x+y:] = img4
    base_hologram[x+y:, y:x+y] = img3
    base_hologram[y:x+y, 0:y] = img2
    

    #Write the hologram frame on our output video
    out.write(base_hologram)

    
    if cv.waitKey(1) == ord('q'):
        break


cap.release()
out.release()
cv.destroyAllWindows()