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
    frame_num_str.set(val)
    label.config(image = list_of_frame_images[int(val)])

root = create_window()

videos_folder_path = Path('data/videos')
videos_path_list = [x for x in videos_folder_path.iterdir() if x.is_file()]

cap = cv2.VideoCapture(videos_path_list[0])
list_of_frame_images = create_list_of_frame_images(cap)

frame_num_str = tk.StringVar()
frame_num_str.set('0')

slider = tk.Scale(
        root,
        from_ = 0,
        to = len(list_of_frame_images) - 1,
        orient = tk.HORIZONTAL,
        length = 400,
        width = 25,
        command = get_slider_value
    )
slider.pack()

label = tk.Label(
        root, 
        textvariable = frame_num_str, 
        font = ('Arial', 40, 'bold'), 
        fg = 'red',
        image = list_of_frame_images[0],
        compound = tk.CENTER
    )
label.pack()

entry = tk.Entry(
    root,
    width = 10
)
entry.pack()


def print_text():
    print(entry.get())

button = tk.Button(
    root,
    command = print_text
)
button.pack()

root.mainloop()