import flet as ft
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

def main(page: ft.Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "Project Modified voice"
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

            def file_picker_result(e: FilePickerResultEvent):
                global select_file_name
                upload_button.current.disabled = True if e.files is None else False
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
                upload_github_check()
            
            def pr_visible():
                sleep(0.7)
                pr.visible=True
                page.update()
            
            def upload_github_check():
                global upload_complete, video_length, select_file_name
                pre.upload_github()
                try:
                    res = urlopen("https://github.com/nadayoung/storage/tree/main/original/"+select_file_name)
                    print(f"res.status: {res.status}")
                except HTTPError as e:
                    err = e.read()
                    code = e.getcode()
                    print(f"error code: {code}")
                    print("try again to upload github")
                    pre.upload_github()
                upload_complete = True
                next_button.current.disabled = True if upload_complete is False else False
                video_length = pre.set_video_length('original/'+select_file_name)
                pr.visible = False
                page.update()

            page.overlay.append(file_picker)
            page.views.append(
                View("/", 
                    [
                AppBar(title=Text("Welcome!"), bgcolor=colors.BLUE_200),
                Row(
                    [
                        Column(
                            [
                        
                    Container(
                        cl := Column(
                            width=1200,
                            height=530,
                            alignment=MainAxisAlignment.START,
                            expand=True,
                            scroll=ScrollMode.ALWAYS,
                            controls=[
                                Container(
                                    Image("assets\\ew.png"),
                                    height=page.height,
                                    width=page.width,
                                    key="A",
                                ),
                                Container(
                                    Image("assets\\cartoon_caps.jpg"),
                                    height=page.height,
                                    width=page.width,
                                    key="B",
                                ),
                                Container(
                                    Image("assets\\cartoon_satoori.jpg"),
                                    height=page.height,
                                    width=page.width,
                                    key="C",
                                ),
                            ],
                        ),
                        border=border.all(1),
                    ),
                    Column([
                        Container(
                            Row(
                                width=1200,
                                height=40,
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    TextButton(
                                        "Home",
                                        width=150,
                                        on_click=lambda _: cl.scroll_to(key="A", duration=500),
                                    ),
                                    TextButton(
                                        "How To?",
                                        width=150,
                                        on_click=lambda _: cl.scroll_to(key="B", duration=500),
                                    ),
                                    TextButton(
                                        "About TAT",
                                        width=150,
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
                                bgcolor=colors.GREY_300,
                                height=page.height,
                                width=300,
                                content=Column(
                                    # alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Container(height=40),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Text("변환할 영역을 선택하세요.", size=18),
                                            ]
                                        ),
                                        Container(height=10),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton(
                                                    "파일 선택",
                                                    icon=icons.FOLDER_OPEN,
                                                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=200,
                                                ),
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton(
                                                    "업로드",
                                                    ref=upload_button,
                                                    icon=icons.UPLOAD,
                                                    on_click=upload_files,
                                                    disabled=True,
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=200,
                                                ),
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                ElevatedButton(
                                                    "선택 완료",
                                                    ref=next_button,
                                                    on_click=lambda _: page.go("/select"),
                                                    disabled=True,
                                                    bgcolor=colors.INDIGO_ACCENT_700,
                                                    color=colors.WHITE,
                                                    width=200,
                                                ),
                                            ]
                                        ),
                                        Container(height=30),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("1. sldfa;sldkjf!"),
                                            ]
                                        ),
                                        Container(height=30),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("2. ㅁㄴㅇㄻㄴㅇㄹ! \n ㅓㅏㅓㅓㅏㅣㅑ \n asdfasdf \n asdfasdf \n asfasdfadsf"),
                                            ]
                                        ),
                                        Row(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Icon(name=icons.CHECK_BOX_OUTLINED, color=colors.GREEN),
                                                Text("3. 2141553!"),
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

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view=page.views[-1]
        page.go(top_view.route)

    page.on_route_change=route_change
    page.on_view_pop=view_pop
    page.go(page.route)


app(target=main, upload_dir="original", view=AppView.WEB_BROWSER)