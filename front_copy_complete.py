from flet import *
from moviepy.editor import *
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Dict
import preprocessing as pre
from time import sleep

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
    page.title = "TAT"
    page.window_width = 500
    page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER

    def route_change(route):
        global select_file_name, end_point, start_point

        page.views.clear()

        files = Ref[Column]()

        if page.route == "/":
            prog_bars: Dict[str, ProgressRing] = {}
            upload_button = Ref[ElevatedButton]()
            next_button = Ref[ElevatedButton]()

            pr = ProgressRing(width=20, height=20, visible=False)

            # def file_picker_result(e: FilePickerResultEvent):
            #     global select_file_name
            #     upload_button.current.disabled = True if e.files is None else False
            #     prog_bars.clear()
            #     files.current.controls.clear()
            #     if e.files is not None:
            #         for f in e.files:
            #             prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            #             prog_bars[f.name] = prog
            #             files.current.controls.append(Row([prog, Text(f.name)]))
            #             select_file_name = f.name
            #     page.update()

            def file_picker_result(e: FilePickerResultEvent):
                global select_file_name
                upload_button.current.disabled = True if e.files is None else False
                if e.files is not None:
                    for f in e.files:
                        prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                        files_content = files.current.controls if files.current else []
                        files_content.append(Row([prog, Text(f.name)]))
                        if files.current:
                            files.current.controls = files_content
                        else:
                            files.current = Column(controls=files_content)
                        select_file_name = f.name
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
                                upload_url=page.get_upload_url('original_video.mp4', 600),
                            )
                        )
                    file_picker.upload(uf)
                    pr_visible()
                    # video_path = 'original/' + select_file_name
                    # print(video_path)
                    # clip=VideoFileClip(video_path)
                    # clip.write_videofile('original/original_video.mp4')
                    # clip.close()
                print("upload to original folder")

                upload_github_check()
            
            def pr_visible():
                sleep(0.7)
                pr.visible=True
                page.update()
            
            def upload_github_check():
                global upload_complete, video_length, select_file_name
                file_name_github = select_file_name.replace(" ", "%20")
                pre.upload_github_check('original/'+file_name_github)
                upload_complete = True
                next_button.current.disabled = True if upload_complete is False else False
                video_length = pre.set_video_length('original/'+select_file_name)
                pr.visible = False
                page.update()

            page.overlay.append(file_picker)
            page.views.append(
                View("/", 
                    [
                AppBar(title=Text("안녕하수꽈!"), bgcolor=colors.BLUE_200),
                Row(
                    [
                        Column(
                            [
                        
                    Container(
                        cl := Column(
                            width=1060,
                            height=590,
                            alignment=MainAxisAlignment.START,
                            expand=True,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                Container(
                                    Image("assets\\home_screen.png"),
                                    height=590,
                                    width=1060,
                                    key="A",
                                ),
                                Container(
                                    Image("assets\\howto.png"),
                                    height=590,
                                    width=1060,
                                    key="B",
                                ),
                                Container(
                                    Image("assets\\end_screen.png"),
                                    height=590,
                                    width=1060,
                                    key="C",
                                ),
                            ],
                        ),
                        border=border.all(1),
                    ),
                    Column([
                        Container(
                            Row(
                                width=1060,
                                height=50,
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    TextButton(
                                        "Home",
                                        width=130,
                                        on_click=lambda _: cl.scroll_to(key="A", duration=500),
                                    ),
                                    TextButton(
                                        "How to use TAT",
                                        width=130,
                                        on_click=lambda _: cl.scroll_to(key="B", duration=500),
                                    ),
                                    TextButton(
                                        "About TAT",
                                        width=130,
                                        on_click=lambda _: cl.scroll_to(key="C", duration=500),
                                    ),
                                ]
                            ),
                            ),
                        ]
                    ),
                    ]),
                    Column(
                        [
                            Container(
                                width=400,
                                content=Column(
                                    controls=[
                                        Container(height=40),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Text("변환하고 싶은 영상을 넣어주세요.", size=18),
                                            ]
                                        ),
                                        Container(height=10),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton(
                                                    "Select files",
                                                    icon=icons.FOLDER_OPEN,
                                                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=260,
                                                ),
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                pr,
                                                ElevatedButton(
                                                    "Upload",
                                                    ref=upload_button,
                                                    icon=icons.UPLOAD,
                                                    on_click=upload_files,
                                                    disabled=True,
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=260,
                                                ),
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                pr,
                                                ElevatedButton(
                                                    "선택완료",
                                                    ref=next_button,
                                                    on_click=lambda _: page.go("/select"),
                                                    disabled=True,
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=260,
                                                ),
                                            ]
                                        ),
                                        Container(height=20),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("1. 자연스러운 사투리 구사하고 싶은 사람!"),
                                            ]
                                        ),
                                        Container(height=15),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("2. 여기다 뭘 써야할까!?"),
                                                Container(width=105),
                                            ]
                                        ),
                                        Container(height=15),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("3. 3개이상 쓸 게 있을까!?"),
                                                Container(width=95),
                                            ]
                                        ),
                                    ]
                                )
                            )
                        ]
                    )
                    ]
                
                )
                ]
                ))

        ###############################################(2번째 화면입니다.)#########################################################
        if page.route == "/select":
            subclip_slider = Ref[RangeSlider]()
            next_button = Ref[ElevatedButton]()
                
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
                video.seek(int(float(start_point)*1000))
                page.update()
                print(f"Video.seek_start: {start_point}")

            def end_seek(e):
                global end_point, video_length
                video.seek(int(float(end_point)*1000))
                page.update()
                print(f"Video.seek_end: {end_point}")
            
            def make_subclip():
                pr.visible=True
                subclip_slider.current.disabled = False if pr.visible is False else True
                page.update()
                global start_point, end_point, video_length, select_file_name
                print(f'select_file_name: {select_file_name}')
                print(f"cut out from {start_point}s to {end_point}s and entire time is {video_length}s")

                pre.make_subclip(start_point, end_point)
                print("success make subclip")
                pre.extract_audio_from_video('trimmed/video.mp4', 'trimmed/audio.wav')
                pre.reduce_noise('trimmed/audio.wav', 'trimmed/denoised_audio.wav')
                pre.rebuild_video('trimmed/video.mp4', 'trimmed/denoised_audio.wav')
                pre.upload_github()

            def execute_multiple_functions():
                make_subclip()
                page.go("/modified")

            pr = ProgressRing(width=20, height=20, visible=False)

            range_slider = RangeSlider(
                ref=subclip_slider,
                min=0,
                max=video_length,
                start_value=0,
                end_value=video_length,
                divisions=50,
                width=280,
                inactive_color=colors.GREEN_300,
                active_color=colors.GREEN_700,
                overlay_color=colors.GREEN_100,
                label="{value}초",
                on_change_start=slider_change_start,
                on_change=slider_is_changing,
                on_change_end=slider_change_end,
                disabled=False
            )

            original_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/original/"+select_file_name,
                ),
            ]

            video = Video(
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
            )
            
            page.views.append(
                View(
                    "/select",
                    [
                        AppBar(title = Text("변환할 부분 선택"), bgcolor=colors.SURFACE_VARIANT),
                        # video := Video(
                        #     expand=True,
                        #     playlist=original_media,
                        #     playlist_mode=PlaylistMode.SINGLE,
                        #     fill_color=colors.BLACK,
                        #     aspect_ratio=16/9,
                        #     volume=100,
                        #     autoplay=False,
                        #     filter_quality=FilterQuality.HIGH,
                        #     muted=False,
                        #     on_loaded=lambda e: print("Video loaded successfully!"),
                        #     on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
                        #     on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
                        # ),
                        Row(
                            controls=[
                                video,
                                Column(
                                    controls=[
                                        Row(
                                            controls=[
                                                Container(width=45),
                                                Text("변환하고 싶은 영역을 선택해 주세요.", size=18),
                                            ]
                                        ),
                                        Row(
                                            wrap=True,
                                            width=400,
                                            controls=[
                                                ElevatedButton("시작점", on_click=start_seek, width=45, style = ButtonStyle(padding=0)),
                                                range_slider,
                                                ElevatedButton("끝점", on_click=end_seek, width=45, style = ButtonStyle(padding=0)),
                                            ],
                                        ),
                                        Row(
                                            controls=[
                                                Container(width=80),
                                                pr,
                                                ElevatedButton(
                                                    "변환하기",
                                                    ref=next_button,
                                                    on_click=lambda _: execute_multiple_functions(),
                                                    width=200,
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            )

        ###############################################(3번째 화면입니다.)#########################################################
        # 동영상 변환이 끝난 뒤 화면
        if page.route == "/modified":
            modified_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/trimmed/"+select_file_name,
                ),
            ]

            video = Video(
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
            )

            def save_trimmed_file(e):
                global select_file_name
                pre.save_video_url("https://github.com/nadayoung/storage/raw/main/trimmed/"+select_file_name, select_file_name)

            page.views.append(
                View( # 변형된 화면
                    "/modified",
                    [
                        AppBar(title=Text("변환 완료"), bgcolor=colors.SURFACE_VARIANT),
                        # video := Video(
                        #     expand=True,
                        #     playlist=modified_media,
                        #     playlist_mode=PlaylistMode.SINGLE,
                        #     fill_color=colors.BLACK,
                        #     aspect_ratio=16/9,
                        #     volume=100,
                        #     autoplay=False,
                        #     filter_quality=FilterQuality.HIGH,
                        #     muted=False,
                        #     on_loaded=lambda e: print("Video loaded successfully!"),
                        #     on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
                        #     on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
                        # ),
                        Row(
                            controls=[
                                video,
                                Column(
                                    width=400,
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton("Save file", icon=icons.SAVE, on_click=save_trimmed_file, width=250),
                                            ]
                                        ),
                                        Container(),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton("돌아가기", on_click=lambda _: page.go("/"), width=250, bgcolor=colors.INDIGO_ACCENT_700, color=colors.WHITE),
                                            ]
                                        )
                                    ],
                                )
                            ]
                        ),
                    ]
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