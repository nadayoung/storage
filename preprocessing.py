from moviepy.editor import *
import whisper 
# pip install -U openai-whisper
# ffmpge 다운로드 필요(https://stackoverflow.com/questions/73845566/openai-whisper-filenotfounderror-winerror-2-the-system-cannot-find-the-file)
import soundfile as sf
from os import system
from urllib.request import urlretrieve

# 영상에서 음성 추출
def extract_audio_from_video(video_file_path, audio_file_path):
    # mp4 등 비디오 파일 불러오기
    video = VideoFileClip(video_file_path)
    # 오디오를 추출하여 mp3 파일로 저장
    video.audio.write_audiofile(audio_file_path, codec='pcm_s16le')
    # video = VideoFileClip(video_file_path[:9]+"extract_audio_" + video_file_path[9:])
    print("extract audio from video.")

def reduce_noise(audio_file_path, audio_file_path_dn):
    data, samplerate = sf.read(audio_file_path)
    sf.write(audio_file_path_dn, data, samplerate, 'PCM_24')
    print("success reducing a noise.")

def rebuild_video(video_file_path, audio_file_path_dn):
    # model 적용 후 audio와 video 합쳐서 저장
    video_clip = VideoFileClip(video_file_path)
    audio_clip = AudioFileClip(audio_file_path_dn) # 나중에 변환된 파일로 변경
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile("finish/post.mp4")
    video_clip.close()
    print("rebuild the video!")

def set_video_length(sample_media):
    video_clip = VideoFileClip(sample_media)
    video_length = video_clip.duration
    video_clip.close()
    print(f"video length: {video_length}")
    return video_length

def upload_github():
    system('git add .')
    system('git commit -m "Video change"')
    system('git push origin main')
    print('success github upload!')

# def save_video_url(video_url, file_name):
#     urlretrieve(video_url, 'finish/' + file_name)
#     print(f"save video_url: {video_url}")
#     print("save by url success")

def main():
    video_file = 'original/197898_(1080p).mp4'  # 변환하고 싶은 비디오 파일의 경로
    audio_file = 'original/audio.wav'  # 저장할 오디오 파일의 경로, 이름 지정
    audio_file_dn = 'trimmed/denoised_audio.wav'

    extract_audio_from_video(video_file, audio_file)
    reduce_noise(audio_file, audio_file_dn)

    # model에 적용
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_dn)
    print(result["text"])

    rebuild_video(video_file, audio_file)
    

if __name__ == "__main__":
    main()