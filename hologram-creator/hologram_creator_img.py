import cv2 as cv
import os
import numpy as np
import random

base_img = cv.imread(r"Image Path")

#Set the new img dimensions 
x = base_img.shape[1]//3
y = base_img.shape[0]//3

hologram_coor = 2*y + x

base_hologram = np.zeros((hologram_coor, hologram_coor, 3), dtype="uint8")

img1=cv.resize(base_img, (x, y))

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

#Create the rest of the imgs
img2=rotate(img1, 90)

img3=rotate(img1, 180)

img4=rotate(img1,270)


#Combine them into one single img
base_hologram[0:y, y:x+y] = img1
base_hologram[y:x+y, x+y:] = img4
base_hologram[x+y:, y:x+y] = img3
base_hologram[y:x+y, 0:y] = img2
cv.imshow('Imagen combinada', base_hologram)

#Save the new img
name = str(random.randint(1,100000000000))+".jpg"
path = r"Directory Path"
filename = os.path.join(path, name)
cv.imwrite(filename, base_hologram)

cv.waitKey(0)