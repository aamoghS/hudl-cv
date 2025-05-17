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

def get_slider_value(val):
    print(val)

root = create_window()

videos_folder_path = Path('data/videos')
videos_path_list = [x for x in videos_folder_path.iterdir() if x.is_file()]

cap = cv2.VideoCapture(videos_path_list[0])
list_of_frame_images = create_list_of_frame_images(cap)

slider = tk.Scale(
        root,
        from_ = 0,
        to = max,
        orient = tk.HORIZONTAL,
        command = get_slider_value
    )
slider.pack()

label = tk.Label(
        root, 
        text = '100', 
        font = ('Arial', 40, 'bold'), 
        fg = 'red',
        image = list_of_frame_images[100],
        compound = tk.CENTER
    )
label.pack()

root.mainloop()