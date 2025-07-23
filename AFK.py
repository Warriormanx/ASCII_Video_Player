import cv2
import os
import time
import sys

ASCII_CHARS = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNW%&@"

def get_terminal_width():
    #Gets the current width of the terminal in characters.
    try:
        return os.get_terminal_size().columns
    except OSError:
        # A fallback for environments where getting size is not supported
        return 80

def resize_frame(frame, new_width):
    #Resizes a frame to a new width while maintaining the aspect ratio.
    
    (old_height, old_width, _) = frame.shape
    aspect_ratio = old_height / float(old_width)
    
    new_height = int(aspect_ratio * new_width * 0.55)
    return cv2.resize(frame, (new_width, new_height))

def frame_to_ascii(frame):
    # Converts a single grayscale frame to an ASCII string.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ascii_str = ""
    for row in gray_frame:
        for pixel_brightness in row:
            # Map the 0-255 pixel value to an index in ASCII_CHARS
            index = int((pixel_brightness / 255) * (len(ASCII_CHARS) - 1))
            ascii_str += ASCII_CHARS[index]
        ascii_str += "\n"
        
    return ascii_str

def play_video(video_path):
    #Opens a video file and plays it as ASCII art in the terminal.
    try:
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print(f"Error: Could not open video file at {video_path}")
            return
            
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_time = 1 / fps if fps > 0 else 0.033 # Handle case where fps is 0

        terminal_width = get_terminal_width()

        while True:
            success, frame = video.read()
            if not success:
                break # End of video

            resized = resize_frame(frame, new_width=terminal_width)
            ascii_frame = frame_to_ascii(resized)

            # Move cursor to top-left corner instead of clearing screen
            sys.stdout.write("\033[H") 
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            # Wait for the correct amount of time to maintain FPS
            time.sleep(frame_time)

    except KeyboardInterrupt:
        print("\nPlayback stopped.")
    finally:
        if 'video' in locals() and video.isOpened():
            video.release()
        # Clear the screen one last time on exit
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_video_file>")
    else:
        video_file = sys.argv[1]
        play_video(video_file)