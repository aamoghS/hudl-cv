from pathlib import Path
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import random

class VideoClassLabeler:
    def __init__(self, root):
       self.root = root
       self.root.title('Video Class Labeler')
       self.start_frame = 0
       self.end_frame = 0
       self.list_of_frames = []
       self.list_of_frames_pil = []

       self.read_video()

       self.draw_ui_elements()


    def read_video(self):
        videos_folder_path = Path('data/videos')
        videos_path_list = [x for x in videos_folder_path.iterdir() if x.is_file()]

        cap = cv2.VideoCapture(videos_path_list[0])
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
            img = img.resize((960, 540))
            self.list_of_frames_pil.append(img)
            img = ImageTk.PhotoImage(img)
            self.list_of_frames.append(img)
        
        cap.release

    def draw_ui_elements(self):
        # Create the Frame for displaying frames
        self.vid_frame = tk.Frame(self.root)
        self.vid_frame.pack()

        # Create the Label for displaying frames
        self.label = tk.Label(self.vid_frame, image = self.list_of_frames[0])
        self.label.pack(expand = True)

        #Create the Frame for user input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady = 10)

        #Create the Button for setting the starting frame
        self.start_frame = tk.Button(self.input_frame, text = 'Start Frame', command = self.set_start_frame)
        self.start_frame.pack()

        #Create the Button for setting the ending frame
        self.end_frame = tk.Button(self.input_frame, text = 'End Frame', command = self.set_end_frame)
        self.end_frame.pack()

        #Create the Button for submitting frame selections
        self.submit = tk.Button(self.input_frame, text = 'Submit', command = self.submit)
        self.submit.pack()

        #Create the Scale for navigating through frames
        self.video_nav = tk.Scale(self.input_frame, from_ = 0, to = len(self.list_of_frames) - 1, orient = 'horizontal', width = 25, command = self.update_video_frame)
        self.video_nav.pack(pady = 10)

    def set_start_frame(self):
        self.start_frame = self.video_nav.get()

    def set_end_frame(self):
        self.end_frame = self.video_nav.get()

    def update_video_frame(self, video_frame):
        self.label.config(image = self.list_of_frames[int(video_frame)])

    def submit(self):
        if (int(self.start_frame) > int(self.end_frame)) or  self.start_frame == 0 or self.end_frame == 0:
            return
        self.save_frames()
        self.root.destroy()

    def save_frames(self):
        presnap_frames = self.list_of_frames_pil[:int(self.start_frame)]
        random.shuffle(presnap_frames)

        presnap_frames_len = len(presnap_frames)

        presnap_train = presnap_frames[:int(.80 * presnap_frames_len)]
        presnap_test = presnap_frames[int(.80 * presnap_frames_len):int(.90 * presnap_frames_len)]
        presnap_val = presnap_frames[int(.90 * presnap_frames_len):]

        for idx, frame in zip(range(len(presnap_train)), presnap_train):
            frame.save(f'data/images/train/pre/{idx}_presnap.png')

        for idx, frame in zip(range(len(presnap_test)), presnap_test):
            frame.save(f'data/images/test/pre/{idx}_presnap.png')

        for idx, frame in zip(range(len(presnap_val)), presnap_val):
            frame.save(f'data/images/val/pre/{idx}_presnap.png')

        postsnap_frames = self.list_of_frames_pil[int(self.end_frame):]
        random.shuffle(postsnap_frames)

        postsnap_frames_len = len(postsnap_frames)

        postsnap_train = postsnap_frames[:int(.80 * postsnap_frames_len)]
        postsnap_test = postsnap_frames[int(.80 * postsnap_frames_len):int(.90 * postsnap_frames_len)]
        postsnap_val = postsnap_frames[int(.90 * postsnap_frames_len):]

        for idx, frame in zip(range(len(postsnap_train)), postsnap_train):
            frame.save(f'data/images/train/post/{idx}_postsnap.png')

        for idx, frame in zip(range(len(postsnap_test)), postsnap_test):
            frame.save(f'data/images/test/post/{idx}_postsnap.png')

        for idx, frame in zip(range(len(postsnap_val)), postsnap_val):
            frame.save(f'data/images/val/post/{idx}_postsnap.png')


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoClassLabeler(root)
    root.geometry("900x700")
    root.mainloop()