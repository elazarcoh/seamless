import asyncio
import functools
import typing as t

from fastapi import Response
from seamless import render
from seamless.types import Primitive, Renderable

from utils.utils import ensure_awaitable


class SeamlessResponse(Response):
    media_type = "text/html"

    def __init__(self, content: "Renderable | Primitive", *args, **kwargs):
        super().__init__(content=content, *args, **kwargs)
        self.content = content
        self._rendered_body = None

    @property
    def body(self) -> bytes:
        if self._rendered_body is None:
            try:
                html = render(self.content)
            except Exception as e:
                import traceback    
                e = traceback.format_exc()
                html = f"<pre>{e}</pre>"
            self._rendered_body = super().render(html)
        return self._rendered_body

    @body.setter
    def body(self, value: bytes):
        # No-op, we don't want to set the body directly
        pass

    def render(self, content: "Renderable | Primitive") -> t.Any:
        # No-op, we want to render on-demand
        return content


def seamless_response(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        value = await ensure_awaitable(func(*args, **kwargs))
        return SeamlessResponse(value)

    return wrapper
