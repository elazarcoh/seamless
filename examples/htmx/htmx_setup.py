import typing as t

from fastapi import Request
from seamless import Script
from seamless.context.base import ContextBase
from seamless.core import JavaScript
from seamless.extra.components import ComponentsFeature
from seamless.extra.transformers.dash_transformer import dash_transformer
from seamless.extra.transformers.html_events_transformer import html_events_transformer
from seamless.extra.transformers.simple_transformer import simple_transformer
from seamless.extra.transformers.style_transformer import style_transformer

from utils.utils import ensure_awaitable


HTMX_SCRIPT = Script(
    src="https://unpkg.com/htmx.org@2.0.2/dist/htmx.js",
    integrity="sha384-yZq+5izaUBKcRgFbxgkRYwpHhHHCpp5nseXp0MEQ1A4MTWVMnqkmcuFez8x5qfxr",
    cross_origin="anonymous",
)

_RIn = t.TypeVar("_RIn")
_ROut = t.TypeVar("_ROut")
_MaybeAwaitable = t.Union[t.Awaitable[_RIn], _RIn]


def js_transformer():
    def matcher(key: str, value):
        return key.startswith("on_") and isinstance(value, JavaScript)

    def transformer(key: str, source: JavaScript, element):
        dash_key = key.replace("on_", "on")
        element.props[dash_key] = source.code
        del element.props[key]

    return matcher, transformer


def htmx_transformer():
    NORMAL_KEYS = {
        "hx_get": "hx-get",
        "hx_post": "hx-post",
        "hx_push_url": "hx-push-url",
        "hx_select": "hx-select",
        "hx_select_oob": "hx-select-oob",
        "hx_swap": "hx-swap",
        "hx_swap_oob": "hx-swap-oob",
        "hx_target": "hx-target",
        "hx_trigger": "hx-trigger",
        "hx_vals": "hx-vals",
        "hx_boost": "hx-boost",
        "hx_confirm": "hx-confirm",
        "hx_delete": "hx-delete",
        "hx_disable": "hx-disable",
        "hx_disabled_elt": "hx-disabled-elt",
        "hx_disinherit": "hx-disinherit",
        "hx_encoding": "hx-encoding",
        "hx_ext": "hx-ext",
        "hx_headers": "hx-headers",
        "hx_history": "hx-history",
        "hx_history_elt": "hx-history-elt",
        "hx_include": "hx-include",
        "hx_indicator": "hx-indicator",
        "hx_inherit": "hx-inherit",
        "hx_params": "hx-params",
        "hx_patch": "hx-patch",
        "hx_preserve": "hx-preserve",
        "hx_prompt": "hx-prompt",
        "hx_put": "hx-put",
        "hx_replace_url": "hx-replace-url",
        "hx_request": "hx-request",
        "hx_sync": "hx-sync",
        "hx_validate": "hx-validate",
        "hx_vars": "hx-vars",
    }

    def matcher(key: str, value):
        return key.startswith("hx_")

    def transformer(key: str, value, element):
        if key in NORMAL_KEYS:
            element.props[NORMAL_KEYS[key]] = value
            del element.props[key]

        # hx-on:*
        elif key.startswith("hx_on_"):
            if key.startswith("hx_on_htmx_"):
                # Special case for htmx events: hx-on:htmx:*
                key = key.replace("hx_on_htmx_", "hx-on:htmx:", 1)
            elif key.startswith("hx_on__"):
                # Special case for htmx events: hx-on::*
                key = key.replace("hx_on__", "hx-on:", 1)
            elif key.startswith("hx_on_"):
                # regular events: hx-on:*
                key = key.replace("hx_on_", "hx-on:", 1)

            # replace _ with - in the event name
            key = key.replace("_", "-")
            element.props[key] = value
            del element.props[key]

    return matcher, transformer


def class_transformer():
    def matcher(key, _):
        return key in ("class_name", "class_")

    def transformer(key, class_name, element):
        if not isinstance(class_name, str):
            class_name = " ".join(class_name)

        element.props["class"] = " ".join(str(class_name).split())
        del element.props[key]

    return matcher, transformer


class HTMXSupportedContext(ContextBase):
    @classmethod
    def default(cls) -> "HTMXSupportedContext":
        ctx = cls()

        ctx.add_feature(ComponentsFeature)

        # Order matters
        ctx.add_prop_transformer(*class_transformer())
        ctx.add_prop_transformer(*simple_transformer())
        ctx.add_prop_transformer(*htmx_transformer())
        ctx.add_prop_transformer(*html_events_transformer())
        ctx.add_prop_transformer(*dash_transformer())
        ctx.add_prop_transformer(*js_transformer())
        ctx.add_prop_transformer(*style_transformer())
        return ctx


def wrap_non_htmx(non_htmx_wrapper: t.Callable[[_RIn], _ROut]):
    def decorator(handler: t.Callable[..., _MaybeAwaitable[_RIn]]):
        async def wrapper(request: Request, **kwargs):
            if handler_need_request:
                kwargs["request"] = request
            inner = await ensure_awaitable(handler(**kwargs))

            if request.headers.get("HX-Request") == "true":
                # is an htmx request, return the inner component
                return inner
            else:
                # not an htmx request, wrap the inner component
                return await ensure_awaitable(non_htmx_wrapper(inner))

        import inspect

        # ensure:
        # - wrapper has the request parameter
        # - wrapper has the same signature as the handler
        # - no duplicate parameters in the signature
        params: t.Dict[inspect.Parameter, None] = {}
        params |= dict.fromkeys(inspect.signature(handler).parameters.values())

        # check if the handler needs the request parameter, so we know to pass it when calling the handler
        handler_need_request = any(p.name == "request" for p in params)

        params |= dict.fromkeys(
            filter(
                lambda p: p.kind
                not in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                ),
                inspect.signature(wrapper).parameters.values(),
            )
        )

        wrapper.__signature__ = inspect.Signature(
            parameters=list(params.keys()),
            return_annotation=inspect.signature(handler).return_annotation,
        )

        return wrapper

    return decorator
