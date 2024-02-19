from flet import *
import urllib.request
from typing import Dict
from os import system
import flet as ft
from moviepy.editor import *

global select_file_name
select_file_name = ""
def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "Project Modified voice"
    page.window_width = 500
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    def route_change(route):
        global select_file_name

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
                prog_bars.clear()
                files.current.controls.clear()
                upload_button.current.disabled = True if e.files is None else False
                next_button.current.disabled = True if e.files is None else False
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
                print(prog_bars[e.file_name])

            file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

            def upload_files(e):
                # next_button.current.disabled = True if file_picker.result is None else False
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
                upload_github()

            def upload_github():
                #system('git pull')
                system('git add .')
                system('git commit -m "Video change"')
                system('git push origin main')
                print("upload success")

            page.overlay.append(file_picker)
            page.views.append( 
            
                View( # 첫번째 화면
                    "/",
                    [
                        AppBar(title=Text("Select video"), bgcolor=colors.SURFACE_VARIANT),
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
                                    on_click=upload_files,
                                    disabled=True,
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
                                ),
                            ]
                        ),
                    ]
                )
            )

        if page.route == "/select":
            original_media = [
                VideoMedia(
                    # "https://github.com/nadayoung/storage/raw/da0/original/dog.mp4"
                    "https://github.com/nadayoung/storage/tree/main/original/"+select_file_name,
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

            def handle_playback_rate_change(e):
                video.playback_rate = e.control.value
                page.update()
                print(f"Video.playback_rate = {e.control.value}")
            
            page.views.append(
                View(
                    "/select",
                    [
                        AppBar(title = Text("Select video"), bgcolor=colors.SURFACE_VARIANT),
                        video := Video(
                            expand=True,
                            playlist=original_media,
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
                        ElevatedButton(
                            "변환하기", 
                            on_click = lambda _:page.go("/modified"),
                        ),
                    ]
                )
            )

        # 동영상 변환이 끝난 뒤 화면
        if page.route == "/modified":
            modified_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/tree/main/original/197898_(1080p).mp4",
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

            def handle_playback_rate_change(e):
                video.playback_rate = e.control.value
                page.update()
                print(f"Video.playback_rate = {e.control.value}")

            def save_video_url(video_url):
                savename = 'save_completed_video.mp4'
                urllib.request.urlretrieve(video_url, 'finish/' + savename)
                print(video_url)
                print("save by url success")

            page.views.append(
                View( # 변형된 화면
                    "/modified",
                    [
                        AppBar(title=Text("Modified video"), bgcolor=colors.SURFACE_VARIANT),
                        video := Video(
                            expand=True,
                            playlist=modified_media,
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
                                on_click=save_video_url(video.playlist[0].resource),
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
                    Slider(
                        min=1,
                        value=1,
                        max=3,
                        label="PlaybackRate = {value}X",
                        divisions=6,
                        width=400,
                        on_change=handle_playback_rate_change,
                    ),
                    ElevatedButton(
                        "돌아가기", 
                        on_click=lambda _: page.go("/"),
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