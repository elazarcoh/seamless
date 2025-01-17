from typing import Generic, TypeVar, Unpack, TYPE_CHECKING
from seamless.rendering.transformers import transformer_for

if TYPE_CHECKING:
    from seamless.types.styling.css_properties import CSSProperties

T = TypeVar("T")


class StyleObject:
    class _StyleProperty(Generic[T]):
        def __init__(self, instance: "StyleObject", name: str):
            self.instance = instance
            self.name = name.replace("_", "-")

        def __call__(self, value: T):
            self.instance.style[self.name] = value
            return self.instance

    def __init__(
        self, *styles: "StyleObject | CSSProperties", **kwargs: Unpack["CSSProperties"]
    ):
        self.style: dict[str, object] = {}
        for style in styles:
            if isinstance(style, StyleObject):
                style = style.style
            self.style.update(style)
        self.style.update(kwargs)
        self.style = {
            k.replace("_", "-"): v for k, v in self.style.items() if v is not None
        }

    def copy(self):
        return StyleObject(self)

    def to_css(self):
        return "".join(map(lambda x: f"{x[0]}:{x[1]};", self.style.items()))

    def __str__(self):
        return self.to_css()

    def __getattr__(self, name: str):
        return StyleObject._StyleProperty(self, name)


@transformer_for(lambda _, value: isinstance(value, StyleObject))
def style_transformer(key, value: StyleObject, props):
    props[key] = value.to_css()
