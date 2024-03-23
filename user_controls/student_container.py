from typing import Optional

from flet import UserControl, LinearGradient, alignment, Control, Container, Scale, animation, AnimationCurve


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
            colors=["#D64511", "#B63621"]
        )

        self.main_container = Container(*args, **kwargs, on_hover=self.on_hover)
        self.main_container.gradient = self.container_linear_gradient
        self.main_container.width = 300
        self.main_container.height = 150
        self.main_container.border_radius = 8
        self.main_container.content = content
        self.main_container.scale = Scale(scale=1)
        self.main_container.animate_scale = animation.Animation(800, AnimationCurve.BOUNCE_OUT)

    def build(self):
        return self.main_container

    @staticmethod
    async def on_hover(e):
        if e.control.scale != 1.120:
            e.control.scale = 1.120
        else:
            e.control.scale = 1
        await e.control.update_async()
