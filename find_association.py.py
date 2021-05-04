import cv2
import os
import json

#To write the data to a JSON file
def writeToJSONFile(fileName, data):
    with open(fileName, 'w') as fp:
        json.dump(data, fp)
data = {}

img_path = './images'
for filename in os.listdir(img_path):
    img = cv2.imread(img_path + '/' + filename)
    my_list = []
    path = './crops'
    for filename1 in os.listdir(path):
        crop = cv2.imread(path + '/' + filename1)
        h = crop.shape[0]
        w = crop.shape[1]

        #Used for matching crop with img
        method = eval('cv2.TM_CCOEFF_NORMED')

        if ( h <= img.shape[0]) & (w <= img.shape[1]):
            result = cv2.matchTemplate(img,crop,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            #extract cropped region from img and compare it with crop
            compare_img = img[top_left[1]: bottom_right[1], top_left[0]: bottom_right[0]]
            flag = count = 0
            if (h == compare_img.shape[0]) & (w == compare_img.shape[1]):
                for i in range(0, h):
                    for j in range(0, w):
                        for k in range(0, 3):
                            count += 1
                            if abs(int(compare_img[i][j][k]) - int(crop[i][j][k])) > 15:
                                flag = flag +1
                
                #There can be upto 750 values that don't match
                if flag <1500:
                    str_file1 = filename1[:-4]
                    my_list.append([str_file1, [top_left[0],top_left[1], bottom_right[0], bottom_right[1]]])

                #Median blur used to correct crops with salt and pepper noise
                elif (flag < count/8):
                    flag = count = 0
                    crop = cv2.medianBlur(crop, 3)
                    for i in range(0, h):
                        for j in range(0, w):
                            for k in range(0, 3):
                                count += 1
                                if abs(int(compare_img[i][j][k]) - int(crop[i][j][k])) > 50 :
                                    flag = flag +1
                                    
                    
                    if(flag < count/20):
                        str_file1 = filename1[:-4]
                        my_list.append([filename1, [top_left[0],top_left[1], bottom_right[0], bottom_right[1]]])
        
        str_file = filename[:-4]         
        if not my_list:
            data[str_file] = "No crop association"
        else:
            data[str_file] = my_list
        writeToJSONFile('./output.json',data)