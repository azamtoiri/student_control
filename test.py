import flet as ft
import flet_fastapi as fapi

from user_controls.student_container import STContainer


async def main(page: ft.Page):
    page.title = 'Student Control'
    page.theme_mode = 'light'

    async def on_hover(e: ft.ControlEvent):
        if e.control.scale != 1.120:
            e.control.scale = 1.120
        else:
            e.control.scale = 1
        await e.page.update_async()

    container = STContainer(
        width=200,
        height=200,
        content=ft.Column([
            ft.Text(expand=1, value='IN container')
        ], ), bgcolor=ft.colors.GREY, on_hover=on_hover
    )

    await page.add_async(
        ft.Text('Hello World!'),
        container,
    )


app = fapi.app(main)
