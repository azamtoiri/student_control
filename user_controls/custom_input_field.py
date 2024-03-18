import time
from typing import Optional

import flet_material as fm
from flet import (UserControl,
                  Text,
                  TextField,
                  TextStyle,
                  colors,
                  Container,
                  Animation,
                  ProgressBar,
                  animation,
                  FontWeight,
                  Stack,
                  Column,
                  Offset,
                  BoxShadow
                  )

from constants import BORDER_COLOR, PRIMARY, BG_COLOR


class CustomInputField(UserControl):
    """
    Custom Input Field uses for more beautiful input data on TextField
    """

    def __init__(self, password: bool, title: str):
        super().__init__()

        self.error = Text()
        self.error.value = 'Incorrect login or password'
        self.error.color = colors.RED_300
        self.error.visible = False

        # region: content for input box
        self.input_box_content = TextField(col={"md": 6, "lg": 4})
        self.input_box_content.hint_text = title
        self.input_box_content.hint_style = TextStyle(color=BORDER_COLOR)
        self.input_box_content.focused_border_color = colors.ON_SURFACE_VARIANT
        self.input_box_content.border_width = 1
        self.input_box_content.cursor_width = 0.5
        self.input_box_content.border_radius = 8
        self.input_box_content.cursor_color = colors.BLACK
        self.input_box_content.text_size = 14
        self.input_box_content.border_color = colors.SURFACE_TINT
        self.input_box_content.bgcolor = BG_COLOR
        self.input_box_content.password = password
        self.input_box_content.can_reveal_password = password
        self.input_box_content.on_focus = self.focus_shadow
        self.input_box_content.on_blur = self.blur_shadow
        self.input_box_content.on_change = self.set_loader_animation
        # endregion

        self.input_box: Container = Container()
        self.input_box.content = self.input_box_content
        self.input_box.animate = Animation(300, animation.AnimationCurve.EASE)

        # region: Loader
        self.loader = ProgressBar()
        self.loader.value = 0
        self.loader.bar_height = 1.25
        self.loader.color = PRIMARY
        self.loader.bgcolor = colors.TRANSPARENT
        # endregion

        self.status: fm.CheckBox = fm.CheckBox(shape="circle", value=False, disabled=True)
        self.status.offset = Offset(1, 0)
        self.status.bottom = 0
        self.status.right = 1
        self.status.top = 1
        self.status.animate_opacity = Animation(200, animation.AnimationCurve.LINEAR)
        self.status.animate_offset = Animation(300, animation.AnimationCurve.EASE)
        self.status.opacity = 0

        # region: Build
        title_text = Text()
        title_text.value = title
        title_text.size = 11
        title_text.weight = FontWeight.BOLD
        title_text.color = BORDER_COLOR

        stack_ = Stack()
        stack_.expand = True
        stack_.controls.append(self.input_box)
        # stack_.controls.append(self.status)  # check box status

        self.obj = Container(height=80)
        self.obj.content = Column(
            spacing=0,
            controls=[title_text, self.input_box, self.loader, ]
        )
        self.obj.spacing = 5
        self.object = self.obj

    def set_ok(self) -> None:
        """does not work yet"""
        self.loader.value = 0
        self.loader.update()

        self.status.offset = Offset(-0.5, 0)
        self.status.opacity = 1
        self.update()
        time.sleep(1)

        self.status.content.value = True
        self.status.animate_checkbox(e=None)
        self.status.update()

    def set_fail(self, message: Optional[str] = "Error") -> None:
        self.loader.value = 0
        self.loader.update()

        self.input_box_content.error_text = message
        self.input_box_content.update()
        time.sleep(1)
        self.update()

    def set_loader_animation(self, e) -> None:
        # function starts the loader if the text field lengths ore not 0
        if len(self.input_box.content.value) != 0:
            self.loader.value = None
        else:
            self.loader.value = 0

        self.loader.update()

    def focus_shadow(self, e) -> None:
        """Focus shadow when focusing"""
        self.error.visible = False
        # self.input_box.content.border_color = BORDER_COLOR
        # self.input_box.border_color = BORDER_COLOR
        self.input_box_content.error_text = None
        self.input_box.shadow = BoxShadow(
            spread_radius=6,
            blur_radius=8,
            color=colors.with_opacity(0.25, BORDER_COLOR),
            offset=Offset(4, 4)
        )
        self.update()
        self.set_loader_animation(e=None)

    def blur_shadow(self, e):
        """ Blur when the textfield loses focus"""
        self.input_box.shadow = None
        self.update()
        self.set_loader_animation(e=None)

    def build(self):
        return self.object
