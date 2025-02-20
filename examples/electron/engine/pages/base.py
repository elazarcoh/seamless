from seamless import Script, Style
from seamless.components import Page


class BasePage(Page):
    def head(self):
        yield from super().head()
        yield Script(src="https://unpkg.com/@tailwindcss/browser@4", defer=True)
        yield Script(
            src="https://cdn.jsdelivr.net/npm/python-seamless@0.9.3/umd/seamless.init.js",
            defer=True,
        )
        yield Style("html, body { height: 100%; }" )
