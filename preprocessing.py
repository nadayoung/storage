from moviepy.editor import *
import whisper 
# pip install -U openai-whisper
# ffmpge 다운로드 필요(https://stackoverflow.com/questions/73845566/openai-whisper-filenotfounderror-winerror-2-the-system-cannot-find-the-file)
import soundfile as sf
from os import system
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.error import HTTPError
from time import sleep


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

# 비디오와 audio를 합쳐서 저장
def rebuild_video(video_file_path, audio_file_path):
    # model 적용 후 audio와 video 합쳐서 저장
    video_clip = VideoFileClip(video_file_path)
    audio_clip = AudioFileClip(audio_file_path) # 나중에 변환된 파일로 변경
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile("finish/post.mp4")
    video_clip.close()
    print("rebuild the video!")

# video의 영상 길이를 확인
def set_video_length(sample_media):
    video_clip = VideoFileClip(sample_media)
    video_length = video_clip.duration
    video_clip.close()
    print(f"video length: {video_length}")
    return video_length

def upload_github():
    system('git pull')
    system('git add .')
    system('git commit -m "project assets update"')
    system('git push -u')
    print('success github upload!')

# github upload하고, 확인해서 올라가지 않은 경우 재업로드
def upload_github_check(storage_name, file_name):
    upload_github()
    # https://github.com/nadayoung/storage/blob/da0/original/front_%25EA%25B9%25A1%25ED%2586%25B5%25EC%2593%25B0.mp4
    # https://github.com/nadayoung/storage/blob/da0/trimmed/front%20%EA%B9%A1%ED%86%B5%EC%93%B0.mp4
    check_url = "https://github.com/nadayoung/storage/tree/main/" + storage_name + "/" + file_name
    print(f"checking url: {check_url}")
    try: # https://github.com/nadayoung/storage/blob/da0/original/dog.mp4
        res = urlopen(check_url)
        print(f"res.status: {res.status}")
    except HTTPError as e:
        err = e.read()
        code = e.getcode()
        print(f"error code: {code}")
        print("try again to upload github")
        sleep(2)
        upload_github_check(storage_name, file_name)
        # upload_github()

# video url로 로컬 파일에 video 저장하기
def save_video_url(video_url, file_name):
    urlretrieve(video_url, 'finish/' + file_name)
    print(f"save video_url: {video_url}")
    print("save by url success")

def make_subclip(start, end, file_name, file_name_m):
    clip = VideoFileClip('original/' + file_name)
    clip = clip.subclip(start, end)
    clip.write_videofile("trimmed/"+file_name)
    clip.close()
    print("success make subclip")

def main():
    video_file = 'original/infinite_challenge.mp4'  # 변환하고 싶은 비디오 파일의 경로
    audio_file = 'original/audio.wav'  # 저장할 오디오 파일의 경로, 이름 지정
    audio_file_dn = 'original/denoised_audio.wav'

    extract_audio_from_video(video_file, audio_file)
    reduce_noise(audio_file, audio_file_dn)

    # model에 적용
    model = whisper.load_model("medium")
    result = model.transcribe(audio_file_dn)
    print(result["text"])

    rebuild_video(video_file, audio_file)
    

if __name__ == "__main__":
    main()