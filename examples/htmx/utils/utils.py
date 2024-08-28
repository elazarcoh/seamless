import typing as t


T = t.TypeVar("T")


async def ensure_awaitable(v: t.Union[T, t.Awaitable[T]]) -> T:
    if isinstance(v, t.Awaitable):
        return await v
    else:
        return v
