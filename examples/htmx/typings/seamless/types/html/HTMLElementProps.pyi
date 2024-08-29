from typing_extensions import TypedDict
from seamless.types.html.AriaProps import AriaProps
from seamless.types.html.HTMLElement import HTMLElement
from seamless.types.html.HTMLEventProps import HTMLEventProps

class HTMXProps(TypedDict, total=False):
    hx_get: str
    hx_post: str
    hx_get: str
    hx_post: str
    hx_push_url: str
    hx_select: str
    hx_select_oob: str
    hx_swap: str
    hx_swap_oob: str
    hx_target: str
    hx_trigger: str
    hx_vals: str
    hx_boost: str
    hx_confirm: str
    hx_delete: str
    hx_disable: str
    hx_disabled_elt: str
    hx_disinherit: str
    hx_encoding: str
    hx_ext: str
    hx_headers: str
    hx_history: str
    hx_history_elt: str
    hx_include: str
    hx_indicator: str
    hx_inherit: str
    hx_params: str
    hx_patch: str
    hx_preserve: str
    hx_prompt: str
    hx_put: str
    hx_replace_url: str
    hx_request: str
    hx_sync: str
    hx_validate: str
    hx_vars: str

    # TODO: events
    # hx-on:htmx:*
    # hx-on::*
    # hx-on:*

class HTMXSSE(TypedDict, total=False):
    sse_connect: str
    sse_swap: str
    sse_close: str

class HTMXExtensions(HTMXSSE):
    pass

class CustomAttributes(TypedDict, total=False):
    class_: str

# fmt:off
class HTMLElementProps(
    HTMLElement, AriaProps, HTMLEventProps,
    HTMXProps, HTMXExtensions,
    CustomAttributes
):
    pass
# fmt:on
