from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from seamless import render
from seamless.context.base import ContextBase
from seamless.context.context import set_global_context
from seamless.core import JavaScript
from seamless.extra.components import ComponentsFeature
from seamless.extra.transformers.class_transformer import class_transformer
from seamless.extra.transformers.dash_transformer import dash_transformer
from seamless.extra.transformers.html_events_transformer import html_events_transformer
from seamless.extra.transformers.simple_transformer import simple_transformer
from seamless.extra.transformers.style_transformer import style_transformer

from components.app import App


def js_transformer():
    def matcher(key: str, value):
        return key.startswith("on_") and isinstance(value, JavaScript)

    def transformer(key: str, source: JavaScript, element):
        dash_key = key.replace("on_", "on")
        element.props[dash_key] = source.code
        del element.props[key]

    return matcher, transformer


class BareHTMLContext(ContextBase):
    @classmethod
    def default(cls) -> "BareHTMLContext":
        ctx = cls()

        ctx.add_feature(ComponentsFeature)

        # Order matters
        ctx.add_prop_transformer(*class_transformer())
        ctx.add_prop_transformer(*simple_transformer())
        ctx.add_prop_transformer(*html_events_transformer())
        ctx.add_prop_transformer(*dash_transformer())
        ctx.add_prop_transformer(*js_transformer())
        ctx.add_prop_transformer(*style_transformer())
        return ctx


set_global_context(BareHTMLContext.default())

HERE = Path(__file__).parent

app = FastAPI()


@app.get("/static/{file_path:path}")
def read_static(file_path: str):
    return FileResponse(HERE / "static" / file_path)


@app.get("/counter", response_class=HTMLResponse)
def get_counter():
    from pages.counter import CounterPage

    return render(CounterPage())


@app.get("/{full_path:path}", response_class=HTMLResponse)
def read_root():
    return render(App())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
