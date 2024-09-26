from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import Bounce  # Import your Bounce script
import os

import sv_ttk

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

# Create the main window
window = Tk()
window.title("Bouncing Idle Screen")
icon = PhotoImage(file="python_logo.png")
window.iconphoto(True, icon)
window.geometry("400x550")
# window.config(background="#abf1ff")

Top_Frame = Frame(window)
Top_Frame.grid(padx=10, pady=10)

# Image Path:
# Label
ttk.Label(Top_Frame, text="Image Path:").grid(row=0, column=0, columnspan=2)
# Entry
image_entry = ttk.Entry(Top_Frame, textvariable=current_dir).grid(row=0, column=0, columnspan=2)
# Button
ttk.Button(Top_Frame, text="Browse", command=get_image_path).grid(row=0, column=0, columnspan=2)

# Image path label and entry
# image_label = ttk.Label(window, text="Image Path:")
# image_label.grid(row=0, column=0, columnspan=2)
# input_path = ""
# image_entry = ttk.Entry(window)
# image_entry.grid(row=0, column=0, columnspan=2)
# image_button = ttk.Button(window, text="Browse", command=get_image_path)
# image_button.grid(row=0, column=0, columnspan=2)

# Screen size labels and entries
screen_width_label = ttk.Label(window, text="Screen Width:")
screen_width_label.grid(row=0, column=0)
screen_width_entry = ttk.Entry(window)
screen_width_entry.pack()

screen_height_label = ttk.Label(window, text="Screen Height:")
screen_height_label.grid(row=0, column=2)
screen_height_entry = ttk.Entry(window)
screen_height_entry.pack()

# Image size label and entry
image_size_label = ttk.Label(window, text="Image Size:")
image_size_label.pack()
image_size_entry = ttk.Entry(window)
image_size_entry.pack()

# FPS label and entry
fps_label = ttk.Label(window, text="FPS:")
fps_label.pack()
fps_entry = ttk.Entry(window)
fps_entry.pack()

# Video length label and entry
video_length_label = ttk.Label(window, text="Video Length (seconds):")
video_length_label.pack()
video_length_entry = ttk.Entry(window)
video_length_entry.pack()

# Starting position labels and entries
starting_x_label = ttk.Label(window, text="Starting X Position:")
starting_x_label.pack()
starting_x_entry = ttk.Entry(window)
starting_x_entry.pack()

starting_y_label = ttk.Label(window, text="Starting Y Position:")
starting_y_label.pack()
starting_y_entry = ttk.Entry(window)
starting_y_entry.pack()

# Output name label and entry
output_name_label = ttk.Label(window, text="Output Video Name:")
output_name_label.pack()
output_name_entry = ttk.Entry(window)
output_name_entry.pack()

# Generate video button
generate_button = ttk.Button(window, text="Generate Video", command=run_code)
generate_button.pack()

if (Bounce.percentComplete > 0):
  T = Text(window, height=2, width=10)
  T.pack()
  T.insert(END, 'Percent Complete: ' + Bounce.percentComplete)

sv_ttk.set_theme("dark")

# Run the main event loop
window.mainloop()