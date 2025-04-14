print("--------------------------------ffmpeg Frames to video to frames converter GUI-----------------------------------------")
print("---------------------------------------------Created by MushieKings----------------------------------------------------")

import customtkinter
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import threading
import winsound

########____GUI____##########
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1200x290")
        self.title("FFMPEG Frames2Vid2Frames GUI")

        # Configure grid weights
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(3, weight=2)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(padx=7, pady=7, row=8, column=2, sticky="nsew")
        
        #First Column GUI
        self.labelvideo2frames = customtkinter.CTkLabel(master=self.frame, text="Video to Frames", font=("Impact", 18), text_color="deep sky blue")
        self.labelvideo2frames.grid(row=1, column=1, pady=3, padx=6)
        #Browse for video file button
        self.video_file_button = customtkinter.CTkButton(master=self.frame, width=200, hover=False, fg_color="blue", text="Get Video File", font=("Impact", 18), text_color="cyan", command=self.browse_video_file)
        self.video_file_button.grid(row=2, column=1, pady=3, padx=6)
        self.video_file_path = "" #Default setting
        #TEXT ENTRY
        self.labelvidpath = customtkinter.CTkLabel(master=self.frame, text="Video Path:", font=("Impact", 18), text_color="deep sky blue")
        self.labelvidpath.grid(row=3, column=1, pady=3, padx=6)
        self.entry_vid_path= customtkinter.CTkEntry(master=self.frame, width=580, placeholder_text=r"Video path")
        self.entry_vid_path.grid(row=4, column=1, pady=3, padx=6)
        #Vid Folder Name ENTRY
        self.labelvidfn = customtkinter.CTkLabel(master=self.frame, text="New Folder Name", font=("Impact", 18), text_color="deep sky blue")
        self.labelvidfn.grid(row=5, column=1, pady=3, padx=6)
        self.entry_frames_foldername= customtkinter.CTkEntry(master=self.frame, width=300, placeholder_text=r"New folder name")
        self.entry_frames_foldername.grid(row=6, column=1, pady=3, padx=6)
        #PNG OR JEPG SWITCH
        self.png_jepg_switch = customtkinter.CTkSwitch(master=self.frame, text="png", font=("Impact", 18), text_color="green", onvalue="jpeg", offvalue="png", command=self.png_jpeg_switch_update)
        self.png_jepg_switch.grid(row=7, column=1, padx=3, pady=6)
        self.png_jpeg = "png" #Default variable setting
        #Start stop button
        self.render_frames_button = customtkinter.CTkButton(master=self.frame, width=200, hover=False, fg_color="teal", text="Render Frames", font=("Impact", 18), text_color="cyan", command=self.generate_frames_button_event)
        self.render_frames_button.grid(row=8, column=1, pady=3, padx=6)


        #Second Column GUI
        self.labelframes2video = customtkinter.CTkLabel(master=self.frame, text="Frames to Video", font=("Impact", 18), text_color="deep sky blue")
        self.labelframes2video.grid(row=1, column=2, pady=3, padx=6)
        #Browse for frames folder button
        self.frames_folder_button = customtkinter.CTkButton(master=self.frame, width=200, hover=False, fg_color="blue", text="Get frames folder", font=("Impact", 18), text_color="cyan", command=self.browse_frames_folder)
        self.frames_folder_button.grid(row=2, column=2, pady=3, padx=6)
        self.frames_folder_path = "" #Default setting
        #Frames folder text entry
        self.labelframespath = customtkinter.CTkLabel(master=self.frame, text="Frames Folder Path:", font=("Impact", 18), text_color="deep sky blue")
        self.labelframespath.grid(row=3, column=2, pady=3, padx=6)
        self.entry_frames_path= customtkinter.CTkEntry(master=self.frame, width=580, placeholder_text=r"Folder containing frames path")
        self.entry_frames_path.grid(row=4, column=2, pady=3, padx=6)
        #FRAME RATE
        self.label_frame_rate = customtkinter.CTkLabel(master=self.frame, text="Frame Rate: 24", font=("Impact", 18), text_color="deep sky blue")
        self.label_frame_rate.grid(row=5, column=2, pady=3, padx=6)
        self.frame_rate_slider = customtkinter.CTkSlider(self.frame, width=590, from_=1, to=60, number_of_steps=590, command=self.frame_rate_slider_update)
        self.frame_rate_slider.grid(row=6, column=2, padx=0, pady=6)
        self.frame_rate_slider.set(24)
        self.frame_rate = 24
        #Drop down box for video formats
        self.video_format_optionmenu = customtkinter.CTkOptionMenu(self.frame, values=["mp4", "avi", "mkv", "wmv", "flv", "mov"], command=self.change_video_format_event)
        self.video_format_optionmenu.grid(row=7, column=2, pady=3, padx=6)
        self.video_format_optionmenu.set("mp4")
        self.video_format = "mp4"
        #Start stop button
        self.render_video_button = customtkinter.CTkButton(master=self.frame, width=200, hover=False, fg_color="teal", text="Render Video", font=("Impact", 18), text_color="cyan", command=self.stitch_video_button_event)
        self.render_video_button.grid(row=8, column=2, pady=3, padx=6)
    
    # First Column gui functions
    def browse_video_file(self):
        self.video_file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.wmv;*.flv;*.mov"), ("All Files", "*.*")]
        )

        if self.video_file_path:
            print(f"Selected video file: {self.video_file_path}")
            # Add path to entry field
            self.entry_vid_path.delete(0, tk.END)
            self.entry_vid_path.insert(0, str(self.video_file_path))
            # Get filename and add to text entry
            self.entry_frames_foldername.delete(0, tk.END)
            base_name = os.path.basename(self.video_file_path)
            filename, _ = os.path.splitext(base_name)
            self.entry_frames_foldername.insert(0, filename)
        else:
            print("No file selected.")

    # Select PNG or JPEG switch
    def png_jpeg_switch_update(self):
        self.png_jpeg = self.png_jepg_switch.get()
        print(self.png_jpeg)
        self.png_jepg_switch.configure(text=self.png_jpeg)

    # Execution button for video to frames conversion
    def generate_frames_button_event(self):
        threading.Thread(target=self.run_ffmpeg_extract_frames).start()

    def run_ffmpeg_extract_frames(self):
        self.render_frames_button.configure(state="disabled")
        
        video_path = self.entry_vid_path.get()
        output_folder = os.path.join(os.path.dirname(video_path), self.entry_frames_foldername.get())
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            winsound.Beep(400, 100)
            print("Output folder already exists.")
            self.render_frames_button.configure(state="enabled")
            return
        
        command = [
            "ffmpeg",
            "-i", video_path,
            f"{output_folder}/frame_%d.{self.png_jpeg}"
        ]
        
        try:
            subprocess.run(command, check=True)
            print("Frames extracted successfully!")
        except subprocess.CalledProcessError as e:
            print(f"FFMPEG error: {e}")
        
        self.render_frames_button.configure(state="enabled")
    
    # Second Column gui functions
    def browse_frames_folder(self):
        self.frames_folder_path = filedialog.askdirectory(title="Select a Frames Folder")
        if self.frames_folder_path:
            print(f"Selected frames folder: {self.frames_folder_path}")
            # Add path to entry field
            self.entry_frames_path.delete(0, tk.END)
            self.entry_frames_path.insert(0, str(self.frames_folder_path))
    # Frame rate
    def frame_rate_slider_update(self, value):
        self.label_frame_rate.configure(text=f"Frame Rate: {value:.1f}") # Update the label with the current slider value
        self.frame_rate = value

    def change_video_format_event(self, value):
        self.video_format = value
        print(self.video_format)

    def stitch_video_button_event(self):
        threading.Thread(target=self.run_ffmpeg_stitch_frames).start()

    def run_ffmpeg_stitch_frames(self):
        self.render_video_button.configure(state="disabled")
        
        frames_folder_path = self.entry_frames_path.get()
        frame_rate = self.frame_rate
        output_video_path = os.path.join(frames_folder_path, f"output.{self.video_format}")
        
        # Check if the output video already exists
        if os.path.exists(output_video_path):
            winsound.Beep(400, 100)
            print("Output video already exists. Please choose a different name or location.")
            self.render_video_button.configure(state="enabled")
            return
        
        command = [
            "ffmpeg",
            "-framerate", str(frame_rate),
            "-i", f"{frames_folder_path}/frame_%d.{self.png_jpeg}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]
        
        try:
            subprocess.run(command, check=True)
            print("Video created successfully!")
        except subprocess.CalledProcessError as e:
            print(f"FFMPEG error: {e}")
        
        self.render_video_button.configure(state="enabled")

if __name__ == "__main__":
    app = App()   
    app.mainloop()