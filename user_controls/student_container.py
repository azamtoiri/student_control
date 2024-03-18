from typing import Optional
import flet as ft
from flet import UserControl, LinearGradient, alignment, Control, Container, Scale, animation, AnimationCurve, colors


class STContainer(UserControl):
    """
    This Custom Student container
    Usage: On navigation View Within Button, for moving on pages
    """

    def __init__(self, content: Optional[Control] = None, *args, **kwargs):
        super().__init__()

        self.container_linear_gradient = LinearGradient(
            begin=alignment.top_left,
            end=alignment.top_right,
            # colors=["#D64511", "#B63621"]
            colors=[colors.SURFACE_TINT, colors.ON_INVERSE_SURFACE],
            rotation=0.8
        )

        self.main_container = Container(*args, **kwargs)
        self.main_container.gradient = self.container_linear_gradient
        # self.main_container.bgcolor = colors.WHITE
        self.main_container.width = 300
        self.main_container.height = 150
        self.main_container.border_radius = 8
        self.main_container.content = content
        self.main_container.scale = Scale(scale=1)
        self.main_container.animate_scale = animation.Animation(800, AnimationCurve.BOUNCE_OUT)
        self.main_container.on_hover = self.on_hover

    def build(self):
        return self.main_container

    @staticmethod
    def on_hover(e):
        if e.control.scale != 1.120:
            e.control.scale = 1.120
        else:
            e.control.scale = 1
        e.control.update()
