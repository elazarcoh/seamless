from seamless import A, Div, Link, Style
from seamless.components import Page
from seamless.styling import CSS

from htmx_setup import HTMX, HtmxExtensions

# TODO: get this from environment
IS_DEV = True


class BasePage(Page):
    def __init__(self):
        super().__init__()
        self._body_props = {
            **self._body_props,
            "height-viewport": True,
            "class": "h-svh p-0 overflow-hidden",
            "hx-ext": "sse",
            "sse-connect": "/sse",
        }

    def head(self):
        yield from super().head()
        yield Link(
            rel="stylesheet",
            href="/static/main.css",
        )

        if IS_DEV:
            yield HTMX.unminified_script(defer=True)
        else:
            yield HTMX.script(defer=True)

        yield HtmxExtensions.sse.script(defer=True)

        yield Style("html, body { height: 100%; }" + CSS.to_css_string(minified=True))

    def body(self):
        return Div(class_name="flex flex-col h-svh")(
            Div(class_name="navbar bg-base-300")(
                A(hx_boost="", href="/", class_name="btn btn-ghost")("Home"),
            ),
            Div(
                class_name="container flex flex-col items-center justify-center h-full",
                id="main",
            )(
                *super().body(),
            ),
        )
