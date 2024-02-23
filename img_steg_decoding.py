import string
from PIL import Image
import numpy as np

def binary_to_ascii(binary):
    decimal = int(binary, 2)
    ascii_char = chr(decimal)
    return ascii_char

def check_if_integer(string):
    for char in string:
        if char.isdigit() == False:
            return False
        else:
            return True

def decode(img_path):

    img = Image.open(img_path, 'r')

    x = np.array(img, dtype = object)

    y = np.reshape(x,(x.shape[0] * x.shape[1],3))


    def decimal_to_binary(val):
        bin = 0
        counter = 0
        temp = val
        while (temp > 0):
            bin = ((temp % 2) * (10 ** counter)) + bin
            temp = int(temp / 2)
            counter += 1
        return bin


    length_decoding_array = []

    # Initialising temp as string for use in following loop
    temp = ''

    # Converting the Blue column of pixel value to binary and extracting last two bits of it to store in array
    for i in range (4 * 10):
        temp = str(decimal_to_binary(y[i,2]))
        while (len(temp) < 8):
            temp = '0' + temp
        length_decoding_array.append(temp[6:8])


    # Initialising final_decoding_array and temp_array for further use
    final_decoding_array = []
    temp_array = []


    # Joining 4 lower bits together to form one character and appending to final array
    for i in range (len(length_decoding_array)):
        if (i+1)%4 == 0:
            temp_array.append(length_decoding_array[i])
            final_decoding_array.append(temp_array)
            temp_array = []
        else:
            temp_array.append(length_decoding_array[i])


    # Converting the binary values in final array to character values
    for i in range (len(final_decoding_array)):
        final_decoding_array[i] = ''.join(final_decoding_array[i])
        final_decoding_array[i] = chr(int(final_decoding_array[i], 2))
        # print(final_decoding_array[i])


    # Initialising length_of_text variable to store final length in integer
    length_of_text = ''
    length_of_text = ''.join(final_decoding_array)

    length_of_text = int(length_of_text)

    # Initialising array for final extracted text
    final_extracted_text = []

    # Extracting last two bits necessary using length_of_text variable
    for i in range(2*length_of_text):
        for j in range(2):
            y[i,j] = str(decimal_to_binary(y[i,j]))
            while (len(y[i,j]) < 8):
                y[i,j] = '0' + y[i,j]
            final_extracted_text.append(y[i, j][6:8])

    # Joining the pieces together to form final text
    def concate(extracted):
        temp = ''
        for i in range(0, len(extracted), 4):  # Concatenate every 4 strings
            temp += ''.join(extracted[i:i+4])
        return temp


    hidden_text=concate(final_extracted_text)

    #Printing the decoded message by taking 8-bit chunks of binary and converting into corresponding ascii characters
    decoded_text = ''.join(binary_to_ascii(hidden_text[i:i+8]) for i in range(0, len(hidden_text), 8))

    return decoded_text

