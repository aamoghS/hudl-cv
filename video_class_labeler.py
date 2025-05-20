from pathlib import Path
import cv2
import tkinter as tk
from PIL import Image, ImageTk


def create_window():
    root = tk.Tk()
    root.title("Window")

    return root

def draw_window(video_path):
    cap = cv2.VideoCapture(video_path)
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
            command = lambda value: get_slider_value(value, frame_num_str, label, list_of_frame_images)
        )
    slider.pack()

    def print_slider():
        print(slider.get())

    start_snap_button = tk.Button(
        root,
        text = 'Start Snap',
        width = 10,
        command = print_slider
    )
    start_snap_button.pack(pady = 10)

    end_snap_button = tk.Button(
        root,
        text = 'End Snap',
        width = 10,
        command = print_slider
    )
    end_snap_button.pack(pady = 10)

    clear_button = tk.Button(
        root,
        text = 'Clear',
        bg = 'red',
        width = 10,
        command = print_slider
    )
    clear_button.pack(pady = 10)

    label = tk.Label(
            root, 
            textvariable = frame_num_str, 
            font = ('Arial', 40, 'bold'), 
            fg = 'red',
            image = list_of_frame_images[0],
            compound = tk.CENTER
        )
    label.pack()

    root.mainloop()

def create_list_of_frame_images(cap):
    list_of_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = Image.fromarray(frame)
        img = img.resize((960, 540))
        img = ImageTk.PhotoImage(img)
        list_of_frames.append(img)
    return list_of_frames

def get_slider_value(val, frame_num_str, label, list_of_frame_images):
    frame_num_str.set(val)
    label.config(image = list_of_frame_images[int(val)])

root = create_window()

videos_folder_path = Path('data/videos')
videos_path_list = [x for x in videos_folder_path.iterdir() if x.is_file()]

draw_window(videos_path_list[0])
