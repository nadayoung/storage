import flet
from flet import *
import cv2
import urllib.request
import os
from typing import Dict

def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "TheCompletedScreen"
    page.window_always_on_top = True
    page.window_width = 500
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    def upload_github():
        os.system('git pull')
        os.system('git add .')
        os.system('git commit -m "Video change"')
        os.system('git push')
        print("upload success")

    def handle_play_or_pause(e):
        video.play_or_pause()
        print("Video.play_or_pause()")
        # print(video.playlist[0].resource)
        
    def handle_stop(e):
        video.stop()
        print("Video.stop()")

    def handle_volume_change(e):
        video.volume = e.control.value
        page.update()
        print(f"Video.volume = {e.control.value}")

    def handle_playback_rate_change(e):
        video.playback_rate = e.control.value
        page.update()
        print(f"Video.playback_rate = {e.control.value}")


    def file_picker_result(e: FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)
            upload_github()



    sample_media = [
        VideoMedia(
            "https://github.com/nadayoung/storage/raw/main/original/dog.mp4"
        ),
    ]

    page.overlay.append(file_picker)

    page.add(

        video := Video(
            expand=True,
            playlist=sample_media,
            playlist_mode=PlaylistMode.SINGLE,
            fill_color=colors.BLUE_400,
            aspect_ratio=16/9,
            volume=100,
            autoplay=False,
            filter_quality=FilterQuality.HIGH,
            muted=False,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
            on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
        ),
        Row(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                ElevatedButton("Play Or Pause", on_click=handle_play_or_pause),
                ElevatedButton("Stop", on_click=handle_stop),
            ],
        ),
        Row(
            [
                ElevatedButton(
                    "Select files",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                )
            ]
        ),
        Row(
            [
                Column(ref=files),
                ElevatedButton(
                    "Upload",
                    ref=upload_button,
                    icon=icons.UPLOAD,
                    on_click= upload_files,
                    disabled=True,
                )
            ]
        ),
        Slider(
            min=0,
            value=100,
            max=100,
            label="Volume = {value}%",
            divisions=10,
            width=400,
            on_change=handle_volume_change,
        ),
        Slider(
            min=1,
            value=1,
            max=3,
            label="PlaybackRate = {value}X",
            divisions=6,
            width=400,
            on_change=handle_playback_rate_change,
        ),
    )

# app(target=main)
app(target=main, upload_dir="original", view=WEB_BROWSER)