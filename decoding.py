import numpy as np
import os
import sys
import img_steg_decoding
import cv2
import glob

frame_array = []

def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def main(video_file):
    filename = "reconstructed_separated_frames"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file    
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_per_second = fps
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            cv2.imwrite(os.path.join(filename,f"frame_{count}.png"),frame)
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


def get_num_images_in_file(file_path):
    os.listdir(file_path)
    num_imgs = 0
    for path in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, path)):
            num_imgs += 1
    return num_imgs

video_name = input("Enter video file name containing hidden text: ")
main(video_name)
image_folder = "separated_frames"

n = get_num_images_in_file(image_folder)

info_frames = ""
info_frames += img_steg_decoding.decode(image_folder+"/frame_"+str(n//2)+".png")

temp_array = []
main_array = []
final_array = []

for char in info_frames:
    if char.isdigit() == True:
        temp_array.append(char)
    if char.isdigit() == False:
        main_array.append(temp_array)
        temp_array = []

main_array.append(temp_array)

for array in main_array:
    if array != []:
        final_array.append(array)

print(final_array)

test_final_frames = []
frame1 = ""
frame2 = ""
frame3 = ""
frame4 = ""
frame5 = ""

number_array = 1
for array in final_array:
    for ele in array:
        if number_array == 1:
            frame1 += ele
        elif number_array == 2:
            frame2 += ele
        elif number_array == 3:
            frame3 += ele
        elif number_array == 4:
            frame4 += ele
        elif number_array == 5:
            frame5 += ele
    number_array += 1

test_final_frames.append(frame1)
test_final_frames.append(frame2)
test_final_frames.append(frame3)
test_final_frames.append(frame4)
test_final_frames.append(frame5)

for ele in test_final_frames:
    frame_array.append(int(ele))

final_frames = []

files = os.listdir(image_folder)

for frame in frame_array:
    for file in files:
        if "frame_"+str(frame)+".png" == file:
            final_frames.append(file)

all_frames = []

print("Final frames:")
print(final_frames)

final_text = []
progress_counter = 1
for image in final_frames:
    final_text.append(img_steg_decoding.decode(image_folder+"/"+image))
    print("Progress: ", str(progress_counter*20), "%")
    progress_counter += 1

print("Final text:")
print(''.join(map(str, final_text)))