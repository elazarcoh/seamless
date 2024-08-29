import asyncio
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from seamless import Button, Div, render
from seamless.context.context import set_global_context
from sse_starlette.sse import EventSourceResponse

from components.app import App, FormComponent, MyForm
from htmx_setup import HtmxExtensions, HTMXSupportedContext
from seamless_response import seamless_response

ctx = HTMXSupportedContext.default()
ctx.add_extensions(
    HtmxExtensions.sse,
    # HtmxExtensions.json_enc,
)
set_global_context(ctx)

HERE = Path(__file__).parent
RETRY_TIMEOUT = 15000  # milisecond


app = FastAPI()


@app.get("/static/{file_path:path}")
def read_static(file_path: str):
    return FileResponse(HERE / "static" / file_path)


@app.get("/sse")
async def get_sse(request: Request):
    async def event_publisher():
        i = 0

        try:
            while i < 4:
                # yield dict(id=..., event=..., data=...)
                i += 1

                message_id = uuid.uuid4().hex

                yield {
                    "event": "counter",
                    "id": message_id,
                    "retry": RETRY_TIMEOUT,
                    "data": render(
                        Div(f"Counter: {i}"),
                    ),
                }
                await asyncio.sleep(1)

            yield {
                "event": "counter",
                "id": uuid.uuid4().hex,
                "retry": RETRY_TIMEOUT,
                "data": render(
                    Div(class_="flex flex-row items-center gap-2")(
                        Div(class_="text-md font-semibold text-green-500")("Counter is done."),
                        Button(
                            hx_get="/sse/counter",
                            hx_swap="outerHTML",
                            class_="btn btn-circle btn-ghost",
                        )("↺"),
                    )
                ),
            }
            await asyncio.sleep(0.1)

            yield {
                "event": "close",
                "id": uuid.uuid4().hex,
                "retry": RETRY_TIMEOUT,
                "data": "",
            }
            await asyncio.sleep(0.1)

        except asyncio.CancelledError as e:
            # Do any other cleanup, if any
            raise e

    # simulate delay
    # await asyncio.sleep(2)

    return EventSourceResponse(event_publisher())


@app.get("/sse/counter")
@seamless_response
async def get_sse_counter(request: Request):
    return Div(
        sse_swap="counter",
        class_="border border-neutral p-4",
        sse_connect="/sse",
        sse_close="close",
    )(
        "Waiting for server counter...",
    )


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
