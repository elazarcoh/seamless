from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from seamless import Div
from seamless.context.context import set_global_context

from components.app import App, FormComponent, MyForm
from htmx_setup import HTMXSupportedContext, wrap_non_htmx
from pages.base import BasePage
from seamless_response import seamless_response

set_global_context(HTMXSupportedContext.default())

HERE = Path(__file__).parent

app = FastAPI()


@app.get("/static/{file_path:path}")
def read_static(file_path: str):
    return FileResponse(HERE / "static" / file_path)


# @app.get("/counter")
# @seamless_response
# @wrap_non_htmx(BasePage)
# def get_counter():
#     from pages.counter import CounterPage
#     return CounterPage()


@app.get("/")
@seamless_response
async def get_root(request: Request):
    form = await MyForm.from_formdata(request)
    return App(form=form)


@app.post("/")
@seamless_response
async def post_root(request: Request):
    form = await MyForm.from_formdata(request)

    if await form.validate_on_submit():
        return Div(
            f"Hello, {form.name.data}!",
        )

    return FormComponent(form=form)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
