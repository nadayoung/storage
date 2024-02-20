from flet import *
from moviepy.editor import *
from urllib.parse import quote
from typing import Dict
import preprocessing as pre
from time import sleep

url = "https://github.com/nadayoung/storage/tree/main/"

global select_file_name, select_file_name_m
select_file_name = ""
select_file_name_m = ""
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
        global select_file_name, select_file_name_m, end_point, start_point, video_length

        # 화면을 띄우기 위함
        # page.overlay.append(file_picker)
        page.views.clear()

        files = Ref[Column]()

        if page.route == "/":
            prog_bars: Dict[str, ProgressRing] = {}
            upload_button = Ref[ElevatedButton]()
            next_button = Ref[ElevatedButton]()

            pr = ProgressRing(width=20, height=20, visible=False)

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
                    pr_visible()
                print("upload to original folder")
                file_check()
            
            def pr_visible():
                sleep(0.7)
                pr.visible=True
                page.update()
            
            def file_check():
                global upload_complete, video_length, select_file_name, select_file_name_m
                # 공백을 _로, 한글을 변화하여 file_name 호출에 문제가 없도록 함
                # select_file_name_m = select_file_name.replace(" ", "_")
                select_file_name_m = select_file_name.replace(" ", "%20")
                select_file_name_m = quote(select_file_name)
                print(f"file.name_m: {select_file_name_m}")
                # 만약 file_name에 공백이나 한글이 존재한다면, 비디오를 하나 더 저장
                # if select_file_name != select_file_name_m:
                #     clip = VideoFileClip('original/'+select_file_name)
                #     print(f"file.name_m: {select_file_name_m}")
                #     clip.write_videofile("original/"+select_file_name_m)
                #     clip.close()
                pre.upload_github_check('original', select_file_name_m)
                upload_complete = True
                next_button.current.disabled = True if upload_complete is False else False
                video_length = pre.set_video_length('original/' + select_file_name)
                pr.visible = False
                page.update()

            page.overlay.append(file_picker)
            page.views.append( 
            
                View( # 첫번째 화면
                    "/",
                    [
                        AppBar(title=Text("영상 선택"), bgcolor=colors.SURFACE_VARIANT),
                        Column(
                            [
                                Image("assets\cartoon_caps.jpg"),
                                Text("사투리의 멋있음을 보여주세요!"),                            
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            width = 500,
                        ),
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
                                pr,
                                ElevatedButton(
                                    "선택완료",
                                    ref=next_button,
                                    on_click=lambda _: page.go("/select"),
                                    disabled=True,
                                    width=200,
                                    bgcolor=colors.INDIGO_ACCENT_700,
                                    color=colors.WHITE,
                                ),
                            ],
                            # alignment=MainAxisAlignment.CENTER
                        ),
                    ]
                )
            )

        ###############################################(2번째 화면입니다.)#########################################################
        if page.route == "/select":
            next_button = Ref[ElevatedButton]()
            subclip_slider = Ref[RangeSlider]()

            # def handle_play_or_pause(e):
            #     video.play_or_pause()
            #     print("Video.play_or_pause()")

            # def handle_volume_change(e):
            #     video.volume = e.control.value
            #     page.update()
            #     print(f"Video.volume = {e.control.value}")
                
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
            
            def modified_video():
                pr.visible=True
                subclip_slider.current.disabled = False if pr.visible is False else True
                next_button.disabled = True
                page.update()

                global start_point, end_point, video_length, select_file_name, select_file_name_m
                print(f'select_file_name: {select_file_name}')
                print(f"cut out from {start_point}s to {end_point}s and entire time is {video_length}s")

                pre.make_subclip(start_point, end_point, select_file_name, select_file_name_m)
                pre.make_clear_audio(select_file_name)
                pre.upload_github_check('trimmed', select_file_name_m)

            pr = ProgressRing(width=20, height=20, visible=False)

            range_slider = RangeSlider(
                ref=subclip_slider,
                min=0,
                max=video_length,
                start_value=0,
                end_value=video_length,
                divisions=50,
                width=300,
                inactive_color=colors.RED_100,
                active_color=colors.INDIGO_ACCENT_700,
                overlay_color=colors.INDIGO_ACCENT_100,
                label="{value}초",
                on_change_start=slider_change_start,
                on_change=slider_is_changing,
                on_change_end=slider_change_end,
                disabled=False
            )

            original_media = [
                VideoMedia(
                    url + "original/" + select_file_name_m,
                ),
            ]
            
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
                        # Row(
                        #     wrap=True,
                        #     alignment=MainAxisAlignment.CENTER,
                        #     controls=[
                        #         ElevatedButton("Play Or Pause", on_click=handle_play_or_pause),
                        #     ],
                        # ),
                        
                        Column(
                            alignment=CrossAxisAlignment.CENTER,
                            controls = [
                                Row(
                                    
                                ),
                                Text("변환하고 싶은 영역을 선택해 주세요.", text_align=TextAlign.CENTER),
                                Row(
                                    wrap=True,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls = [
                                        Container(height=30),
                                        ElevatedButton("Start", on_click=start_seek, width=80,),
                                        range_slider,
                                        ElevatedButton("End", on_click=end_seek, width=80,),
                                    ],
                                ),
                            ],    
                        ),
                        # Row(
                        #     wrap=True,
                        #     alignment=MainAxisAlignment.CENTER,
                        #     controls=[
                        #         Container(content=Text("Volume: "),),
                        #         Slider(
                        #         min=0,
                        #         value=100,
                        #         max=100,
                        #         label="Volume = {value}%",
                        #         divisions=10,
                        #         width=400,
                        #         on_change=handle_volume_change,
                        #         ),
                        #     ],
                        # ),
                        Row(
                            # wrap=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                pr,
                                ElevatedButton(
                                "변환하기", 
                                ref = next_button,
                                on_click = lambda _: [modified_video(), page.go("/modified")],
                                width=200,
                                bgcolor=colors.INDIGO_ACCENT_700,
                                color=colors.WHITE,
                                ),
                            ],
                        ),
                    ]
                )
            )

        ###############################################(3번째 화면입니다.)#########################################################
        # 동영상 변환이 끝난 뒤 화면
        if page.route == "/modified":
            next_button = Ref[ElevatedButton]()

            modified_media = [
                VideoMedia( # https://github.com/nadayoung/storage/raw/da0/trimmed/infinite_challenge.mp4
                    url + "trimmed/" + select_file_name_m,
                ),
            ]
            def save_trimmed_file(e):
                pr.visible=True
                next_button.current.disabled = True
                page.update()

                global select_file_name_m
                pre.save_video_url(video.playlist[0].resource, select_file_name_m)
                
                pr.visible=False
                next_button.current.disabled = False 
                page.update()

            # def handle_play_or_pause(e):
            #     video.play_or_pause()
            #     print("Video.play_or_pause()")

            # def handle_stop(e):
            #     video.stop()
            #     print("Video.stop()")

            # def handle_volume_change(e):
            #     video.volume = e.control.value
            #     page.update()
            #     print(f"Video.volume = {e.control.value}")
                
            pr = ProgressRing(width=20, height=20, visible=False)

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
                            # wrap=True,
                            alignment = MainAxisAlignment.CENTER,
                            controls=[
                            # ElevatedButton("Play Or Pause", icon=icons.PLAY_ARROW, on_click=handle_play_or_pause, width=200,),
                            # ElevatedButton("Stop", icon=icons.STOP, on_click=handle_stop, width=200,),
                            ElevatedButton("Save file", icon=icons.SAVE, on_click=save_trimmed_file, width=200,),
                            ],
                        ),
                        # Row(
                        #     alignment = MainAxisAlignment.CENTER,
                        #     controls=[
                        #         Text("Volume: "),
                        #         Slider(
                        #             min=0,
                        #             value=100,
                        #             max=100,
                        #             label="Volume = {value}%",
                        #             divisions=10,
                        #             width=400,
                        #             on_change=handle_volume_change,
                        #         ),
                        #     ],
                        # ),
                        Row(
                            alignment = MainAxisAlignment.CENTER,
                            controls=[
                                pr,
                                ElevatedButton(
                                "돌아가기", 
                                ref = next_button,
                                on_click=lambda _: page.go("/"),
                                bgcolor=colors.INDIGO_ACCENT_700,
                                color=colors.WHITE,
                                disabled=False,
                                ),
                            ],
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