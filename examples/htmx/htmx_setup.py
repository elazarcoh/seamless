import typing as t

from fastapi import Request
from seamless.context.base import ContextBase, PropertyMatcher, PropertyTransformer
from seamless.core import JavaScript
from seamless.extra.components import ComponentsFeature
from seamless.extra.transformers.dash_transformer import dash_transformer
from seamless.extra.transformers.html_events_transformer import html_events_transformer
from seamless.extra.transformers.simple_transformer import simple_transformer
from seamless.extra.transformers.style_transformer import style_transformer
from seamless.html import Script
from seamless.types.html import HTMLScriptElement

from utils.utils import ensure_awaitable

if t.TYPE_CHECKING:
    from seamless.types import ChildType


class PartialScript(Script):
    def __init__(self, *children: "ChildType", **kwargs: t.Unpack["HTMLScriptElement"]):
        super().__init__(*children, **kwargs)

    def __call__(self, **more: t.Unpack[HTMLScriptElement]) -> Script:
        props_not_in_self: dict = {k: v for k, v in more.items() if k not in self.props}
        final_props = {**self.props, **props_not_in_self}
        return Script(**final_props)


class HTMX:
    script = PartialScript(
        src="https://unpkg.com/htmx.org@2.0.2",
        integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ",
        cross_origin="anonymous",
    )
    unminified_script = PartialScript(
        src="https://unpkg.com/htmx.org@2.0.2/dist/htmx.js",
        integrity="sha384-yZq+5izaUBKcRgFbxgkRYwpHhHHCpp5nseXp0MEQ1A4MTWVMnqkmcuFez8x5qfxr",
        cross_origin="anonymous",
    )


class HTMXExtension(t.Protocol):
    name: str
    script: PartialScript
    mapping: t.Dict[str, str]
    link: t.Optional[str] = None

    def transformer(self) -> tuple[PropertyMatcher, PropertyTransformer]:
        def matcher(key, _):
            return key in self.mapping

        def transformer(key, value, element):
            element.props[self.mapping[key]] = value
            del element.props[key]

        return matcher, transformer


class HTMXSSEExtension(HTMXExtension):
    name = "sse"
    script = PartialScript(src="https://unpkg.com/htmx-ext-sse@2.2.2/sse.js")
    mapping = {
        "sse_connect": "hx-sse-connect",
        "sse_swap": "hx-sse-swap",
        "sse_close": "hx-sse-close",
    }
    link = "https://github.com/bigskysoftware/htmx-extensions/tree/main/src/sse"


class HTMXJsonEncExtension(HTMXExtension):
    name = "json_enc"
    script = PartialScript(src="https://unpkg.com/htmx-ext-json-enc@2.0.1/json-enc.js")
    mapping = {}
    link = "https://github.com/bigskysoftware/htmx-extensions/tree/main/src/json-enc"


class HtmxExtensions:
    sse = HTMXSSEExtension()
    json_enc = HTMXJsonEncExtension()


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
                prefix = "hx-on:htmx:"
                event = key.removeprefix("hx_on_htmx_")

            elif key.startswith("hx_on__"):
                # Special case for htmx events: hx-on::*
                prefix = "hx-on::"
                event = key.removeprefix("hx_on__")

            else:  # key.startswith("hx_on_")
                # regular events: hx-on:*
                prefix = "hx-on:"
                event = key.removeprefix("hx_on_")

            if "__" in event:
                # some events uses : as a separator, in python we use __ to indicate that
                event = event.replace("__", ":")

            event = event.replace("_", "-")

            new_key = f"{prefix}{event}"

            element.props[new_key] = value
            del element.props[key]

    return matcher, transformer


def _test_htmx_transformer():
    htmx_attributes = {
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
    htmx_events = {
        "hx_on_htmx_abort": "hx-on:htmx:abort",
        "hx_on_htmx_after_on_load": "hx-on:htmx:after-on-load",
        "hx_on_htmx_after_process_node": "hx-on:htmx:after-process-node",
        "hx_on_htmx_after_request": "hx-on:htmx:after-request",
        "hx_on_htmx_after_settle": "hx-on:htmx:after-settle",
        "hx_on_htmx_after_swap": "hx-on:htmx:after-swap",
        "hx_on_htmx_before_cleanup_element": "hx-on:htmx:before-cleanup-element",
        "hx_on_htmx_before_on_load": "hx-on:htmx:before-on-load",
        "hx_on_htmx_before_process_node": "hx-on:htmx:before-process-node",
        "hx_on_htmx_before_request": "hx-on:htmx:before-request",
        "hx_on_htmx_before_swap": "hx-on:htmx:before-swap",
        "hx_on_htmx_before_send": "hx-on:htmx:before-send",
        "hx_on_htmx_config_request": "hx-on:htmx:config-request",
        "hx_on_htmx_confirm": "hx-on:htmx:confirm",
        "hx_on_htmx_history_cache_error": "hx-on:htmx:history-cache-error",
        "hx_on_htmx_history_cache_miss": "hx-on:htmx:history-cache-miss",
        "hx_on_htmx_history_cache_miss_error": "hx-on:htmx:history-cache-miss-error",
        "hx_on_htmx_history_cache_miss_load": "hx-on:htmx:history-cache-miss-load",
        "hx_on_htmx_history_restore": "hx-on:htmx:history-restore",
        "hx_on_htmx_before_history_save": "hx-on:htmx:before-history-save",
        "hx_on_htmx_load": "hx-on:htmx:load",
        "hx_on_htmx_no_sse_source_error": "hx-on:htmx:no-sse-source-error",
        "hx_on_htmx_on_load_error": "hx-on:htmx:on-load-error",
        "hx_on_htmx_oob_after_swap": "hx-on:htmx:oob-after-swap",
        "hx_on_htmx_oob_before_swap": "hx-on:htmx:oob-before-swap",
        "hx_on_htmx_oob_error_no_target": "hx-on:htmx:oob-error-no-target",
        "hx_on_htmx_prompt": "hx-on:htmx:prompt",
        "hx_on_htmx_pushed_into_history": "hx-on:htmx:pushed-into-history",
        "hx_on_htmx_response_error": "hx-on:htmx:response-error",
        "hx_on_htmx_send_error": "hx-on:htmx:send-error",
        "hx_on_htmx_sse_error": "hx-on:htmx:sse-error",
        "hx_on_htmx_sse_open": "hx-on:htmx:sse-open",
        "hx_on_htmx_swap_error": "hx-on:htmx:swap-error",
        "hx_on_htmx_target_error": "hx-on:htmx:target-error",
        "hx_on_htmx_timeout": "hx-on:htmx:timeout",
        "hx_on_htmx_validation__validate": "hx-on:htmx:validation:validate",
        "hx_on_htmx_validation__failed": "hx-on:htmx:validation:failed",
        "hx_on_htmx_validation__halted": "hx-on:htmx:validation:halted",
        "hx_on_htmx_xhr__abort": "hx-on:htmx:xhr:abort",
        "hx_on_htmx_xhr__loadend": "hx-on:htmx:xhr:loadend",
        "hx_on_htmx_xhr__loadstart": "hx-on:htmx:xhr:loadstart",
        "hx_on_htmx_xhr__progress": "hx-on:htmx:xhr:progress",
    }
    htmx_events_short = {
        k.replace("hx_on_htmx_", "hx_on__"): v.replace("hx-on:htmx:", "hx-on::")
        for k, v in htmx_events.items()
    }
    some_normal_events = {
        "hx_on_click": "hx-on:click",
        "hx_on_mouseover": "hx-on:mouseover",
        "hx_on_mouseout": "hx-on:mouseout",
        "hx_on_mouseenter": "hx-on:mouseenter",
        "hx_on_mouseleave": "hx-on:mouseleave",
        "hx_on_focus": "hx-on:focus",
    }

    content = HTMXSupportedContext.default()

    from seamless.html import Div
    from seamless.rendering.props import transform_props
    from seamless.rendering.tree import ElementNode

    def test_transformer(key, value, expected):
        element = Div(**{key: value})
        element = ElementNode(
            tag_name=element.tag_name, props=element.props, children=[]
        )
        element_dict = transform_props(element, context=content)
        assert (
            expected in element_dict
        ), f"Expected key {expected} not found ({element_dict}, {key=}, {value=})"

    for key, expected in htmx_attributes.items():
        test_transformer(key, "value", expected)

    for key, expected in htmx_events.items():
        test_transformer(key, "alert('hello')", expected)

    for key, expected in htmx_events_short.items():
        test_transformer(key, "alert('hello')", expected)

    for key, expected in some_normal_events.items():
        test_transformer(key, "alert('hello')", expected)


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

    def add_extensions(self, *extensions: HTMXExtension):
        for extension in extensions:
            match, transform = extension.transformer()
            self.add_prop_transformer(match, transform)


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


if __name__ == "__main__":
    _test_htmx_transformer()
