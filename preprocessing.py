from moviepy.editor import VideoFileClip, AudioFileClip
import soundfile as sf
from os import system
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.error import HTTPError
from time import sleep
from pydub import AudioSegment
import ffmpeg
from moviepy.video.fx.accel_decel import accel_decel
import wave
import numpy as np
import scipy.io as sio
import scipy.io.wavfile
import matplotlib.pyplot as plt
import sounddevice as sd

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

# 영상에서 음성 추출하고 간단한 노이즈를 제거함
def make_clear_audio(file_name):
    extract_audio_from_video('trimmed/'+file_name, 'trimmed/audio.wav')
    reduce_noise('trimmed/audio.wav', 'trimmed/denoised_audio.wav')

# video의 영상 길이를 확인
def set_video_length(sample_media):
    video_clip = VideoFileClip(sample_media)
    video_length = video_clip.duration
    video_clip.close()
    print(f"video length: {video_length}")
    return video_length

def set_audio_length(sample_media):
    audio_clip = AudioFileClip(sample_media)
    audio_length = audio_clip.duration
    audio_clip.close()
    print(f"audio length: {audio_length}")
    return audio_length

def upload_github():
    system('git add .')
    system('git commit -m "project assets update"')
    system('git push -u')
    print('success github upload!')

# github upload하고, 확인해서 올라가지 않은 경우 재업로드
def upload_github_check(file_path):
    upload_github()
    check_url = "https://github.com/nadayoung/storage/tree/main/" + file_path
    print(f"checking url: {check_url}")
    try:
        res = urlopen(check_url)
        print(f"res.status: {res.status}")
    except HTTPError as e:
        err = e.read()
        code = e.getcode()
        print(f"error code: {code}")
        print("try again to upload github")
        sleep(2)
        upload_github_check(file_path)
        # upload_github()

# video url로 로컬 파일에 video 저장하기
def save_video_url(video_url, path):
    urlretrieve(video_url, path)
    print(f"save video_url: {video_url}")
    print("save by url success")

# video clip을 저장
def make_subclip(start, end, file_name):
    clip = VideoFileClip('original/' + file_name)
    print(1)
    clip = clip.subclip(start, end)
    print(2)
    clip.write_videofile("trimmed/"+file_name)
    print(3)
    clip.close()
    print("success make subclip")

# 비디오와 audio를 합쳐서 저장
def rebuild_video(video_file_path, audio_file_path):
    audio_length = set_audio_length(audio_file_path)
    video_length = set_video_length(video_file_path)
    rate = float(audio_length/float(video_length))
    print(f'speed rate: {rate}')
    cmd_rate = 'ffmpeg -i ' + video_file_path + ' -filter:v "setpts=' + str(rate) + '*PTS" trimmed/rate_change.mp4'
    system(cmd_rate)
    cmd_merge = 'ffmpeg -y -i ' + audio_file_path + ' -r 30 -i trimmed/rate_change.mp4 -filter:a aresample=async=1 -c:a flac -c:v copy  finish/output.mp4'  
    system(cmd_merge)
    print("rebuild the video complete")

# def do_model(video_file, audio_file):


#     model_stt = whisper.load_model("medium")
#     stt_result = model_stt.transcribe(audio_file)
#     print(f"stt result: {stt_result}")

#     os.environ['OPENAI_API_KEY'] = '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'
#     chatgpt = OpenAI()
#     completion = chatgpt.chat.completions.create(
#         model="ft:gpt-3.5-turbo-1106:personal::8pFueF1K",
#         messages=[
#         {"role": "system", "content": "You translate Korean to Jeju dialect"},
#         {"role": "user", "content": "Translate from Korean to Jeju dialect the following text: {stt_result}"}
#         ]
#     )

#     chatgpt_result = completion.choices[0].message
#     print(f"chatgpt result: {chatgpt_result}")

#     tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
#     tts.tts_to_file(text=chatgpt_result, speaker_wav="trimmed/denoised_audio.wav", language="ko", file_path="finish/output.wav")

#     rebuild_video(video_file, 'finish/output.wav')

def main():
    video_file = 'trimmed/infinite_challenge.mp4'  # 변환하고 싶은 비디오 파일의 경로
    audio_file = 'trimmed/audio.wav'  # 저장할 오디오 파일의 경로, 이름 지정
    audio_file_dn = 'trimmed/denoised_audio.wav'

    # extract_audio_from_video(video_file, audio_file)
    # reduce_noise(audio_file, audio_file_dn)

    # # model에 적용
    # model = whisper.load_model("medium")
    # result = model.transcribe(audio_file_dn)
    # print(result["text"])
    
    # print("start")
    # set_video_length(video_file)
    # set_audio_length(audio_file_dn)

    rebuild_video('original\demo_video.mp4', audio_file_dn)


if __name__ == "__main__":
    main()