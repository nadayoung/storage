import flet
from flet import *
import cv2
import urllib.request
import os

def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "TheCompletedScreen"
    page.window_always_on_top = True
    page.window_width = 500
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER

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

    def save_video_url(video_url):
        savename = 'save_completed_video.mp4'
        urllib.request.urlretrieve(video_url, 'uploads/' + savename)
        print("save success")
        upload_github()
        print("upload success")

    def upload_github():
        os.system('git add .')
        os.system('git commit -m "Video change"')
        os.system('git push')

    sample_media = [
        VideoMedia(
            "https://github.com/nadayoung/storage/raw/main/assets/197898_(1080p).mp4",
        ),
    ]

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
                    "Save file",
                    icon=icons.SAVE,
                    on_click=save_video_url(video.playlist[0].resource) #lambda _: saveme.save_file(),
                    # disabled=page.web,
                ),
                # save_file_path,
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
app(target=main, view=WEB_BROWSER)