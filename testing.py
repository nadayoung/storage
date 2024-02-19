import random
from flet import *
from moviepy.editor import VideoFileClip

global start_point, end_point, video_length
start_point = 0
end_point = 100
video_length = 0

def main(page: Page):
    global start_point, end_point

    page.theme_mode = ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    page.window_always_on_top = True
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    def set_video_length(sample_media):
        global video_length
        video_clip = VideoFileClip(sample_media)
        video_length = video_clip.duration
        video_clip.close()

    def handle_play_or_pause(e):
        video.play_or_pause()
        set_video_length("C:\dev\storage\original\dog.mp4")
        print("Video.play_or_pause()")

    def handle_volume_change(e):
        video.volume = e.control.value
        page.update()
        print(f"Video.volume = {e.control.value}")
        
    def slider_change_start(e):
        global start_point, end_point
        start_point = e.control.start_value
        end_point = e.control.end_value
        print(
            f"Slider change start, values are {e.control.start_value}, {e.control.end_value}"
        )
        print(start_point, end_point)

    def slider_is_changing(e):
        global start_point, end_point
        start_point = e.control.start_value
        end_point = e.control.end_value
        print(
            f"Slider is changing, values are {e.control.start_value}, {e.control.end_value}"
        )
        print(start_point, end_point)

    def slider_change_end(e):
        global start_point, end_point
        start_point = e.control.start_value
        end_point = e.control.end_value
        print(
            f"Slider change end, values are {e.control.start_value}, {e.control.end_value}"
        )
        print(start_point, end_point)

    def start_seek(e):
        global start_point
        video.seek(int(float(start_point)*video_length*10))
        page.update()
        print(f"Video.seek")
        print(start_point)

    def end_seek(e):
        global end_point
        video.seek(int(float(end_point)*video_length*10))
        print(f"Video.seek")
        print(end_point)

    sample_media = [
        VideoMedia(
            "https://github.com/nadayoung/storage/raw/main/original/dog.mp4"
        ),
    ]

    range_slider = RangeSlider(
            
                min=0,
                max=100,
                start_value=0,
                end_value=100,
                divisions=100,
                width=400,
                inactive_color=colors.GREEN_300,
                active_color=colors.GREEN_700,
                overlay_color=colors.GREEN_100,
                # label="{value}%",
                on_change_start=slider_change_start,
                on_change=slider_is_changing,
                on_change_end=slider_change_end,
            
        )
    
    page.add(
        video := Video(
            expand=True,
            playlist=sample_media[0:2],
            playlist_mode=PlaylistMode.LOOP,
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
            ],
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
        Row(
            controls = [
                Container(height=30),
                ElevatedButton("Start", on_click=start_seek, width=80,),
                range_slider,
                ElevatedButton("End", on_click=end_seek, width=80,),
            ],
            
        ),
    )

app(target=main)