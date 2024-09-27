from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import Bounce  # Import your Bounce script
import os

import sv_ttk
import pywinstyles, sys





current_dir = os.getcwd()  # This will get the current directory path

# Global variable to store image path
global input_path

# Function to get the image path
def get_image_path():
  global input_path
  input_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.png")])
  image_entry.delete(0, END)
  image_entry.insert(0, input_path)

# Function to generate the video
def run_code():
  # Get user input from GUI entries
  screen_width = int(screen_width_entry.get())
  screen_height = int(screen_height_entry.get())
  image_size = int(image_size_entry.get())
  fps = int(fps_entry.get())
  video_length = int(video_length_entry.get())
  starting_x = int(starting_x_entry.get())
  starting_y = int(starting_y_entry.get())
  output_name = output_name_entry.get()

  # Combine filename and directory (modify path as needed)
  output_path = os.path.join(current_dir, output_name)

  # Update Bounce.py script variables
  Bounce.x_Screen = screen_width
  Bounce.y_Screen = screen_height
  Bounce.imgSize = image_size
  Bounce.inputPath = input_path
  Bounce.fps = fps
  Bounce.vidLength = video_length
  Bounce.x_Img = starting_x
  Bounce.y_Img = starting_y
  Bounce.outputPath = output_path  # Set output name

  # Call the animation function from Bounce.py
  Bounce.generate_video()


def apply_theme_to_titlebar(window):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(window, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(window, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        window.wm_attributes("-alpha", 0.99)
        window.wm_attributes("-alpha", 1)



# Create the main window
window = Tk()
window.title("Bouncing Idle Screen")
icon = PhotoImage(file="python_logo.png")
window.iconphoto(True, icon)
# window.geometry("450x600")
# window.config(background="#abf1ff")

# Create the frames
pad1 = 16
pad2 = 8
pad3 = 2
width1 = 30
width2 = 16
width3 = 6


top_frame = Frame(window)
top_frame.grid(row=0, column=0, padx=pad1, pady=pad1)

screen_frame = Frame(window)
screen_frame.grid(row=1, column=0, padx=pad1, pady=pad1)

video_frame = Frame(window)
video_frame.grid(row=2, column=0, padx=pad1, pady=pad1)

img_frame = Frame(window)
img_frame.grid(row=3, column=0, padx=pad1, pady=pad1)

output_frame = Frame(window)
output_frame.grid(row=4, column=0, padx=pad1, pady=pad1)

# Image Path / Top Frame
ttk.Label(top_frame, text="Image Path:").grid(row=0, column=0, padx=pad2, pady=pad3)
image_entry = ttk.Entry(top_frame, width=width1)
image_entry.insert(0, Bounce.inputPath)
image_entry.grid(row=1, column=0, padx=pad2, pady=pad3)
ttk.Button(top_frame, text="Browse", command=get_image_path).grid(row=2, column=0, padx=pad2, pady=pad3)

# Screen size / Screen Frame
# Width
ttk.Label(screen_frame, text="Screen Width:").grid(row=0, column=0, padx=pad2, pady=pad3)
screen_width_entry = ttk.Entry(screen_frame, width=width2)
screen_width_entry.insert(0, Bounce.x_Screen)
screen_width_entry.grid(row=1, column=0, padx=pad2, pady=pad3)
# Height
ttk.Label(screen_frame, text="Screen Height:").grid(row=0, column=1, padx=pad2, pady=pad3)
screen_height_entry = ttk.Entry(screen_frame, width=width2)
screen_height_entry.insert(0, Bounce.y_Screen)
screen_height_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Video length / Video Frame
ttk.Label(video_frame, text="Video Length (seconds):").grid(row=0, column=0, padx=pad2, pady=pad3)
video_length_entry = ttk.Entry(video_frame, width=width2)
video_length_entry.insert(0, Bounce.vidLength)
video_length_entry.grid(row=1, column=0, padx=pad2, pady=pad3)

# FPS / Video Frame
ttk.Label(video_frame, text="FPS:").grid(row=0, column=1, padx=pad2, pady=pad3)
fps_entry = ttk.Entry(video_frame, width=width2)
fps_entry.insert(0, Bounce.fps)
fps_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Image size / Image Frame
ttk.Label(img_frame, text="Image Size:").grid(row=0, column=0, padx=pad2, pady=pad3, columnspan=2)
image_size_entry = ttk.Entry(img_frame, width=width2)
image_size_entry.insert(0, Bounce.imgSize)
image_size_entry.grid(row=1, column=0, padx=pad2, pady=pad3, columnspan=2)

# Starting position / Image Frame
ttk.Label(img_frame, text="Starting Position (X,Y):").grid(row=0, column=2, padx=pad2, pady=pad3, columnspan=2)
starting_x_entry = ttk.Entry(img_frame, width=width3)
starting_x_entry.insert(0, Bounce.x_Img)
starting_x_entry.grid(row=1, column=2, padx=pad2, pady=pad3, columnspan=1)
starting_y_entry = ttk.Entry(img_frame, width=width3)
starting_y_entry.insert(0, Bounce.y_Img)
starting_y_entry.grid(row=1, column=3, padx=pad2, pady=pad3, columnspan=1)

# Output name / Output Frame
ttk.Label(output_frame, text="Output Video Name:").grid(row=0, column=0, padx=pad2, pady=pad3)
output_name_entry = ttk.Entry(output_frame, width=width1)
output_name_entry.insert(0, Bounce.outputPath)
output_name_entry.grid(row=1, column=0, padx=pad2, pady=pad3)

# Generate video button / Output Frame
ttk.Button(output_frame, text="Generate Video", command=run_code).grid(row=2, column=0, padx=pad2, pady=pad3+16)

if (Bounce.percentComplete > 0):
  T = Text(output_frame, height=2, width=10).grid(row=3, column=0, padx=pad2, pady=pad3)
  T.insert(END, 'Percent Complete: ' + Bounce.percentComplete)

sv_ttk.set_theme("dark")
apply_theme_to_titlebar(window)

# Run the main event loop
window.mainloop()