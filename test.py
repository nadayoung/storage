# import ffmpeg

# input_file = ffmpeg.input('original\original_video.mp4')
# output_file = ffmpeg.output(input_file.trim(start_frame=100, end_frame=200), 'output.mp4')
# ffmpeg.run(output_file)

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
ffmpeg_extract_subclip("original\original_video.mp4", 60.222, 75.564, targetname="output.mp4")

# Import everything needed to edit video clips
from moviepy.editor import *
# loading video gfg
clip = VideoFileClip("original/original_video.mp4")
# getting only first 5 seconds
clip = clip.subclip(4.333, 2.4444)
# showing clip
clip.ipython_display(width = 360)

clip.write_videofile("clip.mp4")