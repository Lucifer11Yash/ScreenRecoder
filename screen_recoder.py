import cv2
import pyautogui
import tkinter as tk
from tkinter import ttk, filedialog
from threading import Thread
import numpy as np
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("800x600")  # Set the window size to a normal size

        self.recording = False
        self.paused = False
        self.start_time = None
        self.out = None
        self.file_path = None  # Added variable for file path

        self.create_widgets()

    def create_widgets(self):
        style = ThemedStyle(self.root)
        style.set_theme("plastik")

        self.start_button = ttk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.pause_button = ttk.Button(self.root, text="Pause", command=self.pause_recording, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=10, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=10, pady=10)

        # Added label for live preview
        self.live_preview_label = tk.Label(self.root, width=800, height=450, bg='white', bd=2, relief='solid')
        self.live_preview_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Added menu button for file location selection
        self.menu_button = ttk.Button(self.root, text="Select File Location", command=self.select_file_location)
        self.menu_button.grid(row=2, column=0, columnspan=3, pady=10)

    def start_recording(self):
        self.recording = True
        self.start_time = cv2.getTickCount()
        timestamp = self.start_time
        self.file_path = f'recording_{timestamp}.avi'
        self.out = cv2.VideoWriter(self.file_path, cv2.VideoWriter_fourcc(*'XVID'), 10, (1920, 1080))

        self.start_button["state"] = tk.DISABLED
        self.pause_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.NORMAL

        self.record_thread = Thread(target=self.record_screen)
        self.record_thread.start()

    def record_screen(self):
        while self.recording:
            if not self.paused:
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                self.out.write(frame)

                # Resize the frame to fit the label
                frame = cv2.resize(frame, (800, 450))

                # Update live preview label with the current frame
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.live_preview_label.configure(image=img)
                self.live_preview_label.image = img

                self.root.update()  # Update the GUI

    def pause_recording(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button["text"] = "Resume"
        else:
            self.pause_button["text"] = "Pause"

    def stop_recording(self):
        self.recording = False
        self.out.release()

    def select_file_location(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])

        if self.file_path:
            print(f"Selected File Location: {self.file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorder(root)
    root.mainloop()
