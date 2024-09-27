import cv2
import numpy as np

# Output video size (updated from GUI)
x_Screen, y_Screen = 1920, 1080

# Bouncing image properties (updated from GUI)
imgSize, input_path = 200, "img.png"

# Video properties, vidLength is in seconds (updated from GUI)
fps, vidLength = 30, 10

# Starting position of image (updated from GUI)
x_Img, y_Img = 1,1

# Movement properties (updated from GUI)
moveSpeed = 3

# Output path (updated from GUI)
output_path = "bounce.mp4"

percentComplete = 0

# Starting direction
x_Direction = 1
y_Direction = 1

# Define the animation function
def animate(t):
  global x_Img, y_Img, x_Direction, y_Direction

  # Change direction if image reaches edge of screen
  if x_Img <= 0:
    y_Img -= x_Img
    x_Img -= x_Img
    x_Direction = 1
  elif x_Img >= x_Screen - imgSize:
    y_Img -= x_Img-(x_Screen - imgSize)
    x_Img -= x_Img-(x_Screen - imgSize)
    x_Direction = -1

  if y_Img <= 0:
    x_Img -= y_Img
    y_Img -= y_Img
    y_Direction = 1
  elif y_Img >= y_Screen - imgSize:
    x_Img -= y_Img-(y_Screen - imgSize)
    y_Img -= y_Img-(y_Screen - imgSize)
    y_Direction = -1

  # Update position based on direction
  x_Img += x_Direction * moveSpeed
  y_Img += y_Direction * moveSpeed

  # Create a new blank frame
  frame = np.zeros((y_Screen, x_Screen, 3), dtype=np.uint8)  # black background
  # frame = np.full((y_Screen, x_Screen, moveSpeed), 255, dtype=np.uint8)  # white background

  
  # Calculate the visible portion of the image to be drawn
  x_start_frame = max(x_Img, 0)  # Make sure not to have negative indices
  y_start_frame = max(y_Img, 0)

  x_end_frame = min(x_Img + imgSize, x_Screen)
  y_end_frame = min(y_Img + imgSize, y_Screen)

  # Calculate the corresponding portion of the image
  x_start_image = 0 if x_Img >= 0 else -x_Img  # Offset if the image is partially off-screen
  y_start_image = 0 if y_Img >= 0 else -y_Img

  x_end_image = x_start_image + (x_end_frame - x_start_frame)
  y_end_image = y_start_image + (y_end_frame - y_start_frame)

  # Copy the visible part of the image onto the frame
  frame[y_start_frame:y_end_frame, x_start_frame:x_end_frame] = image[y_start_image:y_end_image, x_start_image:x_end_image]

  return frame

# Define the generate_video function
def generate_video():
  global image
  
  percentComplete = 0
  image = cv2.imread(input_path)
  image = cv2.resize(image, (imgSize, imgSize))

  # Ensure the frame has 3 channels (for RGB)
  frame = np.zeros((y_Screen, x_Screen, 3), dtype=np.uint8)  # black background
  
  # Create the video clip (assuming output name is also set in the GUI)
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  video_clip = cv2.VideoWriter(output_path, fourcc, fps, (x_Screen, y_Screen))

  frameTotal = vidLength * fps  # Claculates total number of frames
  count = 0
  mult = 1
  # Write the video frames to file
  for t in np.arange(0, vidLength, 1/fps):
    frame = animate(t)
    video_clip.write(frame)
    percentComplete = t / vidLength

    out = int(percentComplete * 100)
    count += 1
    if count == (frameTotal/100) * mult:
      print(out, "%")
    mult += 1


  # Release resources
  video_clip.release()
  cv2.destroyAllWindows()