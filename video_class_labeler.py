from pathlib import Path
import cv2
import tkinter as tk
from PIL import Image, ImageTk


def create_window():
    root = tk.Tk()
    root.title("Window")

    return root

def create_list_of_frame_images(cap):
    list_of_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        list_of_frames.append(img)
    return list_of_frames

root = create_window()

videos_folder_path = Path('data/videos')
videos_path_list = [x for x in videos_folder_path.iterdir() if x.is_file()]

cap = cv2.VideoCapture(videos_path_list[0])
list_of_frame_images = create_list_of_frame_images(cap)

label = tk.Label(root, 
                 text = '0', 
                 font = ('Arial', 40, 'bold'), 
                 fg = 'red',
                 image = list_of_frame_images[0],
                 compound = tk.CENTER)
label.pack()

root.mainloop()

'''for i, frame in zip(range(len(list_of_frames)), list_of_frames):
    cv2.imshow(str(i), frame)
    cv2.waitKey(0)'''

