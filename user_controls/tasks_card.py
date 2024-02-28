import flet as ft


class TasksCard(ft.UserControl):
    def __init__(self, title_text: str, more_info: str, url: str):
        super().__init__()
        self.title_text = title_text
        self.more_info = more_info
        self.url = url

        self.show_course = ft.ElevatedButton('Посмотреть курс')

    def on_click(self, e: ft.ControlEvent) -> None:
        self.page.go(self.url)

    def build(self) -> ft.Card:
        list_tile = ft.ListTile()
        list_tile.leading = ft.Icon(ft.icons.ALBUM)
        list_tile.title = ft.Text(self.title_text)
        list_tile.subtitle = ft.Text(self.more_info)

        _card = ft.Card(col={"md": 12, "lg": 4})
        _card.content = ft.Container(content=ft.Column([
            list_tile, ft.Row(alignment=ft.MainAxisAlignment.END, controls=[self.show_course])
        ]), width=400, padding=10)

        return _card
