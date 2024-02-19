from moviepy.editor import VideoFileClip, concatenate_videoclips

def make_clip_video(path,save_path, start_t, end_t):
    clip_video = VideoFileClip(path).subclip(start_t, end_t)
    clip_video.write_videofile(save_path)
    

if __name__ == "__main__":
    make_clip_video('original/197898_(1080p).mp4','trimmed/output.mp4','00:00:05', '00:00:10')


    

    # Import everything needed to edit video clips  
from moviepy.editor import *
     
# loading video dsa gfg intro video  
clip = VideoFileClip('original\infinite_challenge.mp4')  
      
# getting only first 15 seconds  
clip = clip.subclip(0, 15)  
   
# showing  clip  
clip.write_videofile("video.mp4")