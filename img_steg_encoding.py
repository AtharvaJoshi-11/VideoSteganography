import string
from PIL import Image
import numpy as np
import os
import shutil

def decimal_to_binary(val):
    bin = 0
    counter = 0
    temp = val
    while (temp > 0):
        bin = ((temp % 2) * (10 ** counter)) + bin
        temp = int(temp / 2)
        counter += 1
    return bin


def encode(img_path, input_text):

    im = Image.open(img_path, 'r')

    pix = np.array(im, dtype = object)


    x = np.vectorize(np.binary_repr)(pix, width=8)

    y = np.reshape(x,(x.shape[0] * x.shape[1],3))


    length_of_text = len(input_text)

    length_of_text = str(length_of_text)


    while (len(length_of_text) < 10):
        length_of_text = '0' + length_of_text

    def convert_text(ip_text):
        final_array = []
        for char in ip_text:
            correction_factor = str(decimal_to_binary(ord(char)))
            while (len(correction_factor) < 8):
                correction_factor = '0' + correction_factor
            final_array.append(correction_factor)
        return final_array

    length_array = convert_text(length_of_text)

    array_of_binary_values = convert_text(input_text)

    def replace_two(np_array, array_of_bin):
        for i in range (2 * len(array_of_bin)):
            if (i%2 == 0):
                temp = extract_from_main_array(array_of_bin[i//2])
            for j in range (2):
                if (i % 2 == 0):
                    if(j == 0):
                        np_array[i,j] = np_array[i,j][:6] + temp[0]
                    else:
                    
                        np_array[i,j] = np_array[i,j][:6] + temp[1]
                    
                else:
                    if (j == 0):
                    
                        np_array[i,j] = np_array[i,j][:6] + temp[2]
                    
                    else:
                    
                        np_array[i,j] = np_array[i,j][:6] + temp[3]
                    
    
        for i in range (4*10):
            if (i%4 == 0):
                temp = extract_from_main_array(length_array[i//4])
            
            if (i%4 == 0):
            
                np_array[i,2] = np_array[i,2][:6] + temp[0]
            
            elif (i%4 == 1):
            
                np_array[i,2] = np_array[i,2][:6] + temp[1]
            
            elif (i%4 == 2):
            
                np_array[i,2] = np_array[i,2][:6] + temp[2]
            
            elif (i%4 == 3):
            
                np_array[i,2] = np_array[i,2][:6] + temp[3]
            

        return np_array


    def extract_from_main_array(main_array):
        temp = []
        temp.append(main_array[0:2])
        temp.append(main_array[2:4])
        temp.append(main_array[4:6])
        temp.append(main_array[6:])
        return temp


    y = replace_two(y, array_of_binary_values)


    h, w = im.size
    z = np.zeros((w,h,3),dtype=object)
    z.flags.writeable = True
    z = np.reshape(y, (w, h, 3))


    for i in range (im.height):
        for j in range (im.width):
            for k in range (3):
                z[i,j,k] = int(z[i,j,k],2)


    z = z.astype(np.uint8)

    reconstructed_image = Image.fromarray(z)

    reconstructed_image.save(img_path)
