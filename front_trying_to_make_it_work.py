import flet as ft
from moviepy.editor import *
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Dict
import preprocessing as pre
from time import sleep

def main(page: ft.Page):
    def items_image(count):
        items_image = []
        for i in range(1, count + 1):
            items_image.append(
                ft.Container(
                    content=ft.Image("assets\cartoon_caps.jpg"),
                    alignment=ft.alignment.center,
                    # width=50,
                    # height=50,
                    expand=True,
                )
            )
        return items_image
    
    def items_button_select_file(count):
        items_button_select_file = []
        for i in range(1, count + 1):
            items_button_select_file.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        "Select files",
                        icon=ft.icons.FOLDER_OPEN,
                        on_click=lambda _: 
                    )
                )
            )

    def items_button_upload(count):

    def items_button_chosen(count):

    def items_text(count):

    def column_with_horiz_alignment_image(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items_image(1),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    # bgcolor=ft.colors.AMBER_100,
                    # width=100,
                ),
            ]
        )
    
    def column_with_horiz_alignment_rest(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    bgcolor=ft.colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        [
            ft.AppBar(title=ft.Text("영상 선택"), bgcolor=ft.colors.BLUE_200),
            ft.Row(
                [
                    column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                    column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                    column_with_horiz_alignment(ft.CrossAxisAlignment.END),
                ],
                spacing=30,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
    )

ft.app(target=main)