import os
import cv2
import numpy as np

image = cv2.imread(r'C:\Users\shuai\Documents\GitHub\BsiUI\develop\GE90_1.png', -1)
image = cv2.resize(image, (320,260))

image_list = [image, image, image]
image_list = tuple(image_list)

C = np.hstack(image_list)
print(C.shape)
cv2.imshow('image', C)
cv2.waitKey()



