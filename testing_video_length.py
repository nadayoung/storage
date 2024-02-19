from moviepy.editor import VideoFileClip

clip = VideoFileClip("C:\dev\storage\original\dog.mp4")
print(clip.duration)