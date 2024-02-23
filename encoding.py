import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip,AudioFileClip
import wave
import sys
import glob
import time
import re
import random_frames
import shutil
import img_steg_encoding
import img_steg_decoding
import time

def extract_audio_from_video(video_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("test-1.wav")
    video_clip.close()
    audio_clip.close()


def encode(input_audio):
    audio = wave.open(input_audio,mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    string1 = "and121and83and212and311and55"
    string1 = string1 + int((len(frame_bytes)-(len(string1)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string1])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    # for i in range(0,10):
    # 	print(frame_bytes[i])
    newAudio =  wave.open('testStego.wav', 'wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified)

    newAudio.close()
    audio.close()

extract_audio_from_video("test-1.mp4")
encode("test-1.wav")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def main(video_file):

    filename = "separated_frames"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)

    saving_frames_per_second = fps
    # get the list of duration spots to save

    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)

    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration,
            # then save the frame
            cv2.imwrite(os.path.join(filename,f"frame_{count}.png"),frame)
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1

def get_video_back_from_frames(video_file):
    # video.release()
    image_folder = remove_suffix(video_file,".mp4")
    image_folder = image_folder + "-reconstructed"

    image_folder = "separated_frames"

    video_name = remove_suffix(video_file,".mp4")
    video_name = video_name + "_output.mp4"


    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, main_fps, (width,height))

    for i in range(len(images)):
        video.write(cv2.imread(os.path.join(image_folder, 'frame_'+str(i)+'.png')))

    cv2.destroyAllWindows()
    video.release()

def images_to_video(input_folder, video_name):
    cap = cv2.VideoCapture(video_name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_name =remove_suffix(video_file,".mp4")
    video_name = video_name + "_output.mp4"
    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    image_files.sort()  # Ensure files are sorted

    # Get the first image to determine dimensions
    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = first_image.shape

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')  # Change codec as needed (e.g., 'XVID')

    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Write frames to video
    for image_file in image_files:
        image_path = os.path.abspath.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        video.write(frame)

    # Release video writer
    video.release()


def get_num_images_in_file(file_path):
    os.listdir(file_path)
    num_imgs = 0
    for path in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, path)):
            num_imgs += 1
    return num_imgs


def split_text(text):
    text_length = len(text)

    if text_length % 4 == 0:
        part_length = text_length // 4
        parts = [text[i:i+part_length] for i in range(0, text_length, part_length)]
        remainder = None
    else:
        part_length = text_length // 4
        parts = [text[i:i+part_length] for i in range(0, text_length - (text_length % 4), part_length)]
        remainder = text[-(text_length % 4):]

    return parts, remainder


def merge_audio_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Set the audio of the video file to the audio from the audio file
    video = video.set_audio(audio)

    # Write the video file with the combined audio
    video.write_videofile(output_path, codec='libx264', audio_codec='libvorbis')



video_file = "test-5.mp4"


start_time = time.time()
extract_audio_from_video(video_file)
encode("test-1.wav")
print("Encoded inside audio")

print("Now splitting video into frames...")
main(video_file)
print("Splitting successful!")

final_input_array = []
input_text = input("Enter text to be hidden:")

input_text_array, rem = split_text(input_text)

for ele in input_text_array:
    final_input_array.append(ele)
if rem == None:
    final_input_array.append(" ")
else:
    final_input_array.append(rem)


main_fps = cv2.VideoCapture(video_file).get(cv2.CAP_PROP_FPS)

image_folder = "separated_frames"

n = get_num_images_in_file(image_folder)

used_indices = []

lst = [i for i in range(n)]

for j in range(5):
    rand_index = random_frames.select_random_frame(lst, j)
    if rand_index not in used_indices and rand_index != n // 2 and rand_index != 35:
        used_indices.append(rand_index)
    else:
        rand_index = random_frames.select_random_frame(lst, j + 10)
        used_indices.append(rand_index)

print("Used indices:")
print(used_indices)

final_frames = []

files = os.listdir(image_folder)

for index in used_indices:
    for file in files:
        if "frame_" + str(index) + ".png" == file:
            final_frames.append(file)

print("Final frames:")
print(final_frames)

returned_images_array = []

for embed_frames in range(5):
    img_steg_encoding.encode(image_folder + "/" + str(final_frames[embed_frames]), final_input_array[embed_frames])
    print("Progress: ", str((embed_frames + 1) * 20), "%")

info_frames = ""

for index in used_indices:
    info_frames += "and" + str(index)


img_steg_encoding.encode(image_folder + "/frame_" + str(n // 2) + ".png", info_frames)

print("Building video...")
get_video_back_from_frames(video_file)
merge_audio_to_video("test-1_output.mp4", "testStego.wav", "final_video_with_audio.mp4")



