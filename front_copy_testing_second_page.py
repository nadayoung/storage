import random
# import flet as ft
from flet import *


def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    # page.window_always_on_top = True
    # page.spacing = 20
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment=MainAxisAlignment.CENTER
    # page.width = 500
    def route_change(route):
        page.views.clear()
        if page.route == "/":

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

            sample_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/original/197898_(1080p).mp4",
                ),
            ]

            range_slider = RangeSlider(
                # ref=subclip_slider,
                min=0,
                max=54,
                start_value=0,
                end_value=54,
                divisions=50,
                width=260,
                inactive_color=colors.RED_100,
                active_color=colors.INDIGO_ACCENT_700,
                overlay_color=colors.INDIGO_ACCENT_100,
                label="{value}초",
                on_change_start=slider_change_start,
                on_change=slider_is_changing,
                on_change_end=slider_change_end,
                disabled=False
            )

            video = Video(
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
            )

            page.views.append(
                View(
                    "/",
                    [
                        Row(
                            controls=[
                                video,
                                Column(
                                    controls=[
                                    Row(
                                        controls=[
                                            Container(width=30),
                                            Text("변환하고 싶은 영역을 선택해 주세요.", size=18),
                                        ]
                                    ),
                                    Row(
                                        wrap=True,
                                        width=400,
                                        controls = [
                                            ElevatedButton("시작점", on_click=print('start_seek'), width=50, 
                                                style = ButtonStyle(padding=0,)),
                                            range_slider,
                                            ElevatedButton("끝점", on_click=print('end_seek'), width=50,
                                            style = ButtonStyle(padding=0)),
                                        ],
                                    ),
                                    Row(
                                        controls=[
                                            # pr,
                                            Container(width=80),
                                            ElevatedButton(
                                                "변환하기", 
                                                # ref = next_button,
                                                on_click = lambda _: [page.go("/modified")],
                                                width=200,
                                                bgcolor=colors.INDIGO_ACCENT_700,
                                                color=colors.WHITE,
                                                ),
                                            ],
                                    ),
                                ]),
                            ]
                        )
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