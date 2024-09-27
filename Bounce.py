from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, ttk
import cv2, os, sv_ttk, pywinstyles, sys
import numpy as np

# Output video size
x_Screen, y_Screen = 1920, 1080

# Bouncing image properties
img_size, img_path = 200, "img.png"

# Video properties, vidLength is in seconds
fps, video_length = 30, 10

# Starting position of image
x_img, y_img = 1, 1

# Movement properties
move_speed = 5

# Output path
output_path = "mp4"

progress = 0
percent_complete = 0

# Starting direction
x_direction, y_direction = 1, 1

bg_color = "white"

# Create the main root
root = Tk()
root.title("Bouncing Idle Screen")
icon = PhotoImage(file="python_logo.png")
root.iconphoto(True, icon)

current_dir = os.getcwd()  # This will get the current directory path
img_path = os.path.join(current_dir, img_path)
output_path = os.path.join(current_dir, output_path)
output_name = "bounce"

# Define the animation function
def animate(t):
  global x_img, y_img, x_direction, y_direction, bg_color, image, move_speed

  real_speed = round(move_speed*60 / fps)
  if real_speed == 0:
    real_speed = 1

  # Change direction if image reaches edge of screen
  if x_img <= 0:
    y_img -= x_img
    x_img -= x_img
    x_direction = 1
  elif x_img >= x_Screen - img_size:
    y_img -= x_img-(x_Screen - img_size)
    x_img -= x_img-(x_Screen - img_size)
    x_direction = -1

  if y_img <= 0:
    x_img -= y_img
    y_img -= y_img
    y_direction = 1
  elif y_img >= y_Screen - img_size:
    x_img -= y_img-(y_Screen - img_size)
    y_img -= y_img-(y_Screen - img_size)
    y_direction = -1

  # Update position based on direction
  x_img += x_direction * real_speed
  y_img += y_direction * real_speed

  # Create a new blank frame
  if (bg_color == "black"):
    frame = np.zeros((y_Screen, x_Screen, 3), dtype=np.uint8)  # black background
  elif (bg_color == "white"):
    frame = np.full((y_Screen, x_Screen, 3), 255, dtype=np.uint8)  # white background
  
  # Calculate the visible portion of the image to be drawn
  x_start_frame = max(x_img, 0)  # Make sure not to have negative indices
  y_start_frame = max(y_img, 0)

  x_end_frame = min(x_img + img_size, x_Screen)
  y_end_frame = min(y_img + img_size, y_Screen)

  # Calculate the corresponding portion of the image
  x_start_image = 0 if x_img >= 0 else -x_img  # Offset if the image is partially off-screen
  y_start_image = 0 if y_img >= 0 else -y_img

  x_end_image = x_start_image + (x_end_frame - x_start_frame)
  y_end_image = y_start_image + (y_end_frame - y_start_frame)

  # Copy the visible part of the image onto the frame
  frame[y_start_frame:y_end_frame, x_start_frame:x_end_frame] = image[y_start_image:y_end_image, x_start_image:x_end_image]
  return frame


# Define the generate_video function
def generate_video():
  global percent_complete, progress, image
  
  percent_complete = 0
  progress["value"] = 0
  done.grid_forget()
  root.update_idletasks()
  
  image = cv2.imread(img_path)
  if image is None:
    raise FileNotFoundError(f"Image at {img_path} could not be loaded. Check the file path.")
  image = cv2.resize(image, (img_size, img_size))

  # Create a new blank frame
  if (bg_color == "black"):
    frame = np.zeros((y_Screen, x_Screen, 3), dtype=np.uint8)  # black background
  elif (bg_color == "white"):
    frame = np.full((y_Screen, x_Screen, 3), 255, dtype=np.uint8)  # white background
  
  # Create the video clip (assuming output name is also set in the GUI)
  fourcc = cv2.VideoWriter_fourcc(*"mp4v")
  video_clip = cv2.VideoWriter(output_path, fourcc, fps, (x_Screen, y_Screen))

  frame_total = video_length * fps  # Claculates total number of frames
  count = 0
  mult = 1
  # Write the video frames to file
  for t in np.arange(0, video_length, 1/fps):
    frame = animate(t)
    video_clip.write(frame)
    percent_complete = (t / video_length) * 100
    progress["value"] = percent_complete
    root.update_idletasks()

    out = int(percent_complete * 100)
    count += 1
    if count == (frame_total/100) * mult:
      print(out, "%")
    mult += 1

  progress["value"] = 100
  done.grid(row=4, column=0, padx=pad2, pady=pad3)
  root.update_idletasks()
  
  # Release resources
  video_clip.release()
  cv2.destroyAllWindows()
  
  
# Function to get the image path
def get_image_path():
  global img_path
  img_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.png")])
  image_entry.delete(0, END)
  image_entry.insert(0, img_path)
  
# Function to get the video path
def set_video_path():
  global output_path, output_name
  output_name = output_name_entry.get()
  
  output_path = filedialog.asksaveasfilename(
    initialfile=output_name,
    initialdir=current_dir,
    title="Select Video Path",
    defaultextension=".mp4",
    filetypes=[("Video Files", "*.mp4")])
  
  if (output_path.endswith(".mp4") == False):
    output_path = output_path + ".mp4"

# Get user inputs from GUI
def run_code():
  global screen_width, screen_height, img_size, fps, video_length, starting_x, starting_y, move_speed
  set_video_path()
  
  screen_width = int(screen_width_entry.get())
  screen_height = int(screen_height_entry.get())
  img_size = int(img_size_entry.get())
  fps = int(fps_entry.get())
  video_length = int(video_length_entry.get())
  starting_x = int(starting_x_entry.get())
  starting_y = int(starting_y_entry.get())
  move_speed = int(img_speed_entry.get())

  # Call the animation function from py
  generate_video()


def apply_theme_to_titlebar(root):
  version = sys.getwindowsversion()

  if version.major == 10 and version.build >= 22000:
    # Set the title bar color to the background color on roots 11 for better appearance
    pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
  elif version.major == 10:
    pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

    # A hacky way to update the title bar's color on roots 10 (it doesn't update instantly like on roots 11)
    root.wm_attributes("-alpha", 0.99)
    root.wm_attributes("-alpha", 1)
    
    
# Padding for grid()
frameX = 16
frameY = 12
pad2 = 8
pad3 = 2
width1 = 26
width2 = 14

# Create the frames
top_frame = Frame(root)
top_frame.grid(row=0, column=0, padx=frameX, pady=frameY)

screen_frame = Frame(root)
screen_frame.grid(row=1, column=0, padx=frameX, pady=frameY)

video_frame = Frame(root)
video_frame.grid(row=2, column=0, padx=frameX, pady=frameY)

img_frame = Frame(root)
img_frame.grid(row=3, column=0, padx=frameX, pady=frameY)

position_frame = Frame(root)
position_frame.grid(row=4, column=0, padx=frameX, pady=frameY)

output_frame = Frame(root)
output_frame.grid(row=5, column=0, padx=frameX, pady=frameY)

# Image Path / Top Frame
ttk.Label(top_frame, text="Image Path:").grid(row=0, column=0, padx=pad2, pady=pad3)
image_entry = ttk.Entry(top_frame, width=width1)
image_entry.insert(0, img_path)
image_entry.grid(row=1, column=0, padx=pad2, pady=pad3)
ttk.Button(top_frame, text="Browse", command=get_image_path).grid(row=2, column=0, padx=pad2, pady=pad3+10)

# Screen size / Screen Frame
# Width
ttk.Label(screen_frame, text="Screen Width:").grid(row=0, column=0, padx=pad2, pady=pad3)
screen_width_entry = ttk.Entry(screen_frame, width=width2)
screen_width_entry.insert(0, x_Screen)
screen_width_entry.grid(row=1, column=0, padx=pad2, pady=pad3)
# Height
ttk.Label(screen_frame, text="Screen Height:").grid(row=0, column=1, padx=pad2, pady=pad3)
screen_height_entry = ttk.Entry(screen_frame, width=width2)
screen_height_entry.insert(0, y_Screen)
screen_height_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Video length / Video Frame
ttk.Label(video_frame, text="Video Length (s):").grid(row=0, column=0, padx=pad2, pady=pad3)
video_length_entry = ttk.Entry(video_frame, width=width2)
video_length_entry.insert(0, video_length)
video_length_entry.grid(row=1, column=0, padx=pad2, pady=pad3)

# FPS / Video Frame
ttk.Label(video_frame, text="FPS:").grid(row=0, column=1, padx=pad2, pady=pad3)
fps_entry = ttk.Entry(video_frame, width=width2)
fps_entry.insert(0, fps)
fps_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Image size / Image Frame
ttk.Label(img_frame, text="Image Size:").grid(row=0, column=0, padx=pad2, pady=pad3)
img_size_entry = ttk.Entry(img_frame, width=width2)
img_size_entry.insert(0, img_size)
img_size_entry.grid(row=1, column=0, padx=pad2, pady=pad3)

# Image Speed / Image Frame
ttk.Label(img_frame, text="Image Move Speed:").grid(row=0, column=1, padx=pad2, pady=pad3)
img_speed_entry = ttk.Entry(img_frame, width=width2)
img_speed_entry.insert(0, move_speed)
img_speed_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Starting position / Position Frame
ttk.Label(position_frame, text="Starting Position X:").grid(row=0, column=0, padx=pad2, pady=pad3)
starting_x_entry = ttk.Entry(position_frame, width=width2)
starting_x_entry.insert(0, x_img)
starting_x_entry.grid(row=1, column=0, padx=pad2, pady=pad3)
ttk.Label(position_frame, text="Starting Position Y:").grid(row=0, column=1, padx=pad2, pady=pad3)
starting_y_entry = ttk.Entry(position_frame, width=width2)
starting_y_entry.insert(0, y_img)
starting_y_entry.grid(row=1, column=1, padx=pad2, pady=pad3)

# Output name / Output Frame
ttk.Label(output_frame, text="Output Video Name:").grid(row=0, column=0, padx=pad2, pady=pad3)
output_name_entry = ttk.Entry(output_frame, width=width1)
output_name_entry.insert(0, output_name)
output_name_entry.grid(row=1, column=0, padx=pad2, pady=pad3)

progress = ttk.Progressbar(output_frame, orient = HORIZONTAL, length = 120, mode = "determinate")
progress.grid(row = 3, column = 0, padx = pad2, pady = pad3)
progress["value"] = 0
root.update_idletasks()

done = ttk.Label(output_frame, text="Done")

# Generate video button / Output Frame
ttk.Button(output_frame, text="Generate Video", command=run_code).grid(row=2, column=0, padx=pad2, pady=pad3+12)

sv_ttk.set_theme("dark")
apply_theme_to_titlebar(root)

# Run the main event loop
root.mainloop()