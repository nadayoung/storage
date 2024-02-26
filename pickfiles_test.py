import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
from moviepy.editor import VideoFileClip, AudioFileClip
from os import system


def main(page: Page):
    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        video_path = e.files[0].path
        video_name = e.files[0].name
        print(f'path: {video_path}')
        print(f'name: {video_name}')
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(video_path)
        video_clip.write_videofile('original/' + video_name, temp_audiofile="temp-audio.m4a", fps=30, remove_temp=True, codec = 'libx264', audio_codec='aac')
        audio_clip.write_audiofile('original/audio.mp3')
        video_clip.close()
        audio_clip.close()
        cmd_merge = 'ffmpeg -y -i original/audio.mp3 -r 30 -i original/' + video_name + ' -filter:a aresample=async=1 -c:a flac -c:v copy  original/original_video.mp4'  
        system(cmd_merge)
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    # # Save file dialog
    # def save_file_result(e: FilePickerResultEvent):
    #     save_file_path.value = e.path if e.path else "Cancelled!"
    #     save_file_path.update()

    # save_file_dialog = FilePicker(on_result=save_file_result)
    # save_file_path = Text()

    # # Open directory dialog
    # def get_directory_result(e: FilePickerResultEvent):
    #     directory_path.value = e.path if e.path else "Cancelled!"
    #     directory_path.update()

    # get_directory_dialog = FilePicker(on_result=get_directory_result)
    # directory_path = Text()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog,])

    page.add(
        Row(
            [
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=['mp4'],
                    ),
                ),
                selected_files,
            ]
        ),
        # Row(
        #     [
        #         ElevatedButton(
        #             "Save file",
        #             icon=icons.SAVE,
        #             on_click=lambda _: save_file_dialog.save_file(),
        #             disabled=page.web,
        #         ),
        #         save_file_path,
        #     ]
        # ),
        # Row(
        #     [
        #         ElevatedButton(
        #             "Open directory",
        #             icon=icons.FOLDER_OPEN,
        #             on_click=lambda _: get_directory_dialog.get_directory_path(),
        #             disabled=page.web,
        #         ),
        #         directory_path,
        #     ]
        # ),
    )


flet.app(target=main)