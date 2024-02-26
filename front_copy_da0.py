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

            def handle_playback_rate_change(e):
                video.playback_rate = e.control.value
                page.update()
                print(f"Video.playback_rate = {e.control.value}")

            sample_media = [
                VideoMedia(
                    "https://github.com/nadayoung/storage/raw/main/trimmed/197898_(1080p).mp4"
                ),
            ]

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
                                        width=400,
                                        # wrap=True,
                                        alignment = MainAxisAlignment.CENTER,
                                        controls=[
                                        # ElevatedButton("Play Or Pause", icon=icons.PLAY_ARROW, on_click=handle_play_or_pause, width=200,),
                                        # ElevatedButton("Stop", icon=icons.STOP, on_click=handle_stop, width=200,),
                                        ElevatedButton("Save file", icon=icons.SAVE, on_click=print('save_trimmed_file'), width=200,),
                                        ],
                                    ),
                                    Container(height=10),
                                    Row(
                                        width=400,
                                        controls=[
                                            # pr,
                                            Container(width=90),
                                            ElevatedButton(
                                                "돌아가기", 
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