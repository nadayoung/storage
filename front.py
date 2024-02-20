# front.py
from flet import *
import urllib.request
from typing import Dict
from os import system
import preprocessing as pre
from moviepy.editor import VideoFileClip

global select_file_name
select_file_name = ""
global upload_complete
upload_complete = False

global start_point, end_point, video_length
start_point = 0
end_point = 100
video_length = 0

def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "Project Modified voice"
    page.window_width = 500
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    def route_change(route):
        global select_file_name, end_point, start_point

        # 화면을 띄우기 위함
        # page.overlay.append(file_picker)

        page.views.clear()

        files = Ref[Column]()

        if page.route == "/":
            prog_bars: Dict[str, ProgressRing] = {}
            upload_button = Ref[ElevatedButton]()
            next_button = Ref[ElevatedButton]()

            def file_picker_result(e: FilePickerResultEvent):
                global select_file_name
                upload_button.current.disabled = True if e.files is None else False
                # next_button.current.disabled = True if e.files is None else False
                prog_bars.clear()
                files.current.controls.clear()
                if e.files is not None:
                    for f in e.files:
                        prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                        prog_bars[f.name] = prog
                        files.current.controls.append(Row([prog, Text(f.name)]))
                        select_file_name = f.name
                page.update()

            def on_upload_progress(e: FilePickerUploadEvent):
                prog_bars[e.file_name].value = e.progress
                prog_bars[e.file_name].update()
                # print(prog_bars[e.file_name])

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
                print("upload to original folder")
                pre.extract_audio_from_video('original/'+select_file_name, 'original/audio.wav')
                pre.reduce_noise('original/audio.wav', 'trimmed/denoised_audio.wav')
                upload_github()
            
            def upload_github():
                global upload_complete
                upload_complete = True
                # print(upload_complete, next_button.current.disabled)
                next_button.current.disabled = True if upload_complete is False else False
                # print(upload_complete, next_button.current.disabled)
                # system('git pull')
                system('git add .')
                system('git commit -m "Video change"')
                system('git push origin main')
                print("upload success")
                set_video_length('original/'+select_file_name)
                page.update()
            
            def set_video_length(sample_media):
                global video_length
                video_clip = VideoFileClip(sample_media)
                video_length = video_clip.duration
                video_clip.close()

            page.overlay.append(file_picker)
            page.views.append( 
            
                View( # 첫번째 화면
                    "/",
                    [
                        AppBar(title=Text("영상 선택"), bgcolor=colors.SURFACE_VARIANT),
                        Image("assets\cartoon_satoori.jpg"),
                        Text("사투리의 멋있음을 보여주세요!"),
                        Row(
                            [
                                ElevatedButton(
                                    "Select files",
                                    icon=icons.FOLDER_OPEN,
                                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                                    width=200,
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
                                    on_click=upload_files,
                                    disabled=True,
                                    width=190,
                                ),   
                            ]
                        ),
                        Row(
                            [
                                ElevatedButton(
                                    "선택완료",
                                    ref=next_button,
                                    on_click=lambda _: page.go("/select"),
                                    disabled=True,
                                    width=200,
                                    bgcolor=colors.PURPLE_200,
                                    color=colors.WHITE,
                                ),
                            ],
                            # alignment=MainAxisAlignment.CENTER
                        ),
                    ]
                )
            )

        if page.route == "/select":
            next_button = Ref[ElevatedButton]()

            def handle_play_or_pause(e):
                video.play_or_pause()
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
                global start_point, video_length
                start_trim = video.seek(int(float(start_point)*video_length*10))
                page.update()
                print(f"Video.seek")
                print(start_point)

            def end_seek(e):
                global end_point, video_length
                end_trim = video.seek(int(float(end_point)*video_length*10))
                print(f"Video.seek")
                print(end_point)

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

            original_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/original/"+select_file_name,
                ),
            ]

            def handle_play_or_pause(e):
                video.play_or_pause()
                print("Video.play_or_pause()")
                print(select_file_name)

            def handle_stop(e):
                video.stop()
                print("Video.stop()")

            def handle_volume_change(e):
                video.volume = e.control.value
                page.update()
                print(f"Video.volume = {e.control.value}")
            
            def make_clip_video(path,save_path, start_t, end_t):
                clip_video = VideoFileClip(path).subclip(start_t, end_t)
                clip_video.write_videofile(save_path)
    
            if __name__ == "__main__":
                make_clip_video("https://github.com/nadayoung/storage/raw/main/original/"+select_file_name,'trimmed/output.mp4','00:00:05', '00:00:10')
    
                print("Trimmed video saved successfully")
            
            page.views.append(
                View(
                    "/select",
                    [
                        AppBar(title = Text("변환할 부분 선택"), bgcolor=colors.SURFACE_VARIANT),
                        video := Video(
                            expand=True,
                            playlist=original_media,
                            playlist_mode=PlaylistMode.SINGLE,
                            fill_color=colors.BLACK,
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
                        # Slider(
                        #     min=1,
                        #     value=1,
                        #     max=3,
                        #     label="PlaybackRate = {value}X",
                        #     divisions=6,
                        #     width=400,
                        #     on_change=handle_playback_rate_change,
                        # ),
                        ElevatedButton(
                            "변환하기", 
                            ref = next_button,
                            on_click=lambda _: (lambda: (make_clip_video("https://github.com/nadayoung/storage/raw/main/original/"+select_file_name, 'trimmed/output.mp4', '00:00:05', '00:00:10'), page.go("/modified"))),
                            width=200,
                            bgcolor=colors.PURPLE_200,
                            color=colors.WHITE,
                            # disabled=True,
                        ),
                    ]
                )
            )

        # 동영상 변환이 끝난 뒤 화면
        if page.route == "/modified":
            modified_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/original/197898_(1080p).mp4",
                ),
            ]

            def handle_play_or_pause(e):
                video.play_or_pause()
                print("Video.play_or_pause()")
                print(select_file_name)

            def handle_stop(e):
                video.stop()
                print("Video.stop()")

            def handle_volume_change(e):
                video.volume = e.control.value
                page.update()
                print(f"Video.volume = {e.control.value}")

            # def handle_playback_rate_change(e):
            #     video.playback_rate = e.control.value
            #     page.update()
            #     print(f"Video.playback_rate = {e.control.value}")

            def save_video_url(video_url):
                savename = 'save_completed_video.mp4'
                urllib.request.urlretrieve(video_url, 'finish/' + savename)
                print(video_url)
                print("save by url success")

            page.views.append(
                View( # 변형된 화면
                    "/modified",
                    [
                        AppBar(title=Text("변환 완료"), bgcolor=colors.SURFACE_VARIANT),
                        video := Video(
                            expand=True,
                            playlist=modified_media,
                            playlist_mode=PlaylistMode.SINGLE,
                            fill_color=colors.BLACK,
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
                            ElevatedButton("Play Or Pause", on_click=handle_play_or_pause, width=200,),
                            ElevatedButton("Stop", on_click=handle_stop, width=200,),
                            ],
                        ),
                        Row(
                            [
                            ElevatedButton(
                                "Save file",
                                icon=icons.SAVE,
                                on_click=save_video_url(video.playlist[0].resource),
                                width=200,
                            ),
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
                    # Slider(
                    #     min=1,
                    #     value=1,
                    #     max=3,
                    #     label="PlaybackRate = {value}X",
                    #     divisions=6,
                    #     width=400,
                    #     on_change=handle_playback_rate_change,
                    # ),
                    ElevatedButton(
                        "돌아가기", 
                        on_click=lambda _: page.go("/"),
                        bgcolor=colors.PURPLE_200,
                        color=colors.WHITE,
                    ),
                ],
            )
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


app(target=main, upload_dir="original", view=AppView.WEB_BROWSER)