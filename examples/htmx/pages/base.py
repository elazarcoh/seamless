from seamless import A, Div, Link, Script, Style, __version__
from seamless.components import Page
from seamless.styling import CSS

from htmx_setup import HTMX_SCRIPT


class BasePage(Page):
    def head(self):
        yield from super().head()
        yield Link(
            rel="stylesheet",
            href="/static/main.css",
        )

        yield HTMX_SCRIPT
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
