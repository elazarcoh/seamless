from seamless import Link, Script, Style, __version__
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
