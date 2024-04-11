import asyncio
import random

import flet as ft


def get_random_color() -> str:
    colors: list = ['blue', "red", "yellow", "green", "purple", "orange", "pink"]
    return random.choice(colors)


def get_random_pos() -> int:
    return random.randint(-100, 2000)


def get_random_offset() -> int:
    return random.randint(1, 5)


def get_random_wait() -> int:
    return random.randrange(500, 700, 100)


def get_random_size() -> int:
    return random.randint(30, 50)


class Thing(ft.Container):
    def __init__(self):
        color: str = get_random_color()
        super(Thing, self).__init__(
            width=2.5,
            height=2.5,
            shape=ft.BoxShape(ft.BoxShape.CIRCLE),
            left=get_random_pos(),
            top=get_random_pos(),
            bgcolor=color,
            opacity=0,
            offset=ft.transform.Offset(0, 0),
            shadow=ft.BoxShadow(
                spread_radius=20,
                blur_radius=100,
                color=color,
            )
        )

        self.wait = get_random_wait()

        self.animate_opacity = ft.Animation(self.wait, "ease")
        self.animate_offset = ft.Animation(self.wait, "ease")

    async def animate_thing(self, event=None):
        self.opacity = 1
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2,
            get_random_offset() ** 2
        )
        self.update()
        await asyncio.sleep(self.wait / 1000)
        self.opacity = 0
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2,
            get_random_offset() ** 2
        )
        self.update()
        await asyncio.sleep(self.wait / 1000)
        await self.animate_thing()


class ThingLightMode(Thing):
    def __init__(self):
        color = get_random_color()
        super(Thing, self).__init__(
            width=25,
            height=20,
            shape=ft.BoxShape(ft.BoxShape.CIRCLE),
            left=get_random_pos(),
            top=get_random_pos(),
            opacity=0,
            bgcolor=color,
            offset=ft.transform.Offset(0, 0),
        )
        self.wait = get_random_wait()

        self.animate_opacity = ft.Animation(self.wait, "ease")
        self.animate_offset = ft.Animation(self.wait, "ease")

    async def animate_thing(self, event=None):
        self.opacity = 1
        self.height = get_random_size()
        self.width = get_random_size()
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2,
            get_random_offset() ** 2
        )
        self.update()
        await asyncio.sleep(self.wait / 500)
        self.opacity = 0
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2,
            get_random_offset() ** 2
        )
        self.update()
        await asyncio.sleep(self.wait / 500)
        await self.animate_thing()
