from seamless import A, JS, Div, Link, Script, Style
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

    def body(self):
        yield Script("""{
            document.body.addEventListener('htmx:sseClose', function (e) {
                const reason = e.detail.type
                switch(reason) {
                    case "nodeMissing":
                        // Parent node is missing and therefore connection was closed
                        console.log("Parent node is missing and therefore connection was closed"); break;  
                    case "nodeReplaced":
                        // Parent node replacement caused closing of connection
                        console.log("Parent node replacement caused closing of connection"); break;
                    case "message":
                        // connection was closed due to reception of message sse-close
                        console.log("connection was closed due to reception of message sse-close"); break;
                }
            });
        }""")
        yield Div(class_name="flex flex-col h-svh")(
            Div(class_name="navbar bg-base-300")(
                A(hx_boost="", href="/", class_name="btn btn-ghost")("Home"),
            ),
            Div(class_name="flex flex-row h-full justify-center")(
                Div(
                    class_name="container h-full",
                    id="main",
                )(
                    *super().body(),
                ),
            ),
        )
