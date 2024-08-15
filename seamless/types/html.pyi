from typing import Callable, Concatenate, TypeVar, Union

from seamless.types.html_element_props import HTMLElementProps

from .. import JS
from .events import *

EventProps = TypeVar("EventProps", bound=Event)
EventFunction = Union[Callable[Concatenate[EventProps, ...], None], "JS", str]

class HTMLAnchorElement(HTMLElementProps, total=False, closed=True):
    download: str
    href: str
    href_lang: str
    ping: str
    referrer_policy: str
    rel: str
    target: str
    type: str

class HTMLAreaElement(HTMLElementProps, total=False, closed=True):
    alt: str
    coords: str
    download: str
    href: str
    href_lang: str
    ping: str
    referrer_policy: str
    rel: str
    shape: str
    target: str

class HTMLAudioElement(HTMLElementProps, total=False, closed=True):
    auto_play: str
    controls: str
    loop: str
    muted: str
    preload: str
    src: str

class HTMLBRElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLBaseElement(HTMLElementProps, total=False, closed=True):
    href: str
    target: str

class HTMLBodyElement(HTMLElementProps, total=False, closed=True):
    background: str

class HTMLButtonElement(HTMLElementProps, total=False, closed=True):
    auto_focus: str
    disabled: str
    form: str
    form_action: str
    form_enctype: str
    form_method: str
    form_no_validate: str
    form_target: str
    name: str
    type: str
    value: str

    __extra_items__: str

class HTMLCanvasElement(HTMLElementProps, total=False, closed=True):
    height: str
    width: str

class HTMLDataElement(HTMLElementProps, total=False, closed=True):
    value: str

class HTMLDataListElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLDetailsElement(HTMLElementProps, total=False, closed=True):
    open: str

class HTMLDialogElement(HTMLElementProps, total=False, closed=True):
    open: str

class HTMLDivElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLEmbedElement(HTMLElementProps, total=False, closed=True):
    height: str
    src: str
    type: str
    width: str

class HTMLFieldSetElement(HTMLElementProps, total=False, closed=True):
    disabled: str
    form: str
    name: str

class HTMLFormElement(HTMLElementProps, total=False, closed=True):
    accept_charset: str
    action: str
    auto_complete: str
    enctype: str
    method: str
    name: str
    no_validate: str
    target: str

class HTMLHRElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLHeadElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLHeadingElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLHtmlElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLIFrameElement(HTMLElementProps, total=False, closed=True):
    allow: str
    allow_fullscreen: str
    csp: str
    frame_border: str
    height: str
    importance: str
    loading: str
    name: str
    referrer_policy: str
    sandbox: str
    scrolling: str
    seamless: str
    src: str
    srcdoc: str
    width: str

class HTMLImageElement(HTMLElementProps, total=False, closed=True):
    alt: str
    cross_origin: str
    decoding: str
    height: str
    importance: str
    intrinsicsize: str
    ismap: str
    loading: str
    referrer_policy: str
    sizes: str
    src: str
    srcset: str
    usemap: str
    width: str

class HTMLInputElement(HTMLElementProps, total=False, closed=True):
    accept: str
    alt: str
    auto_complete: str
    auto_focus: str
    capture: str
    checked: str
    cross_origin: str
    disabled: str
    form: str
    form_action: str
    form_enctype: str
    form_method: str
    form_no_validate: str
    form_target: str
    height: str
    list: str
    max: str
    max_length: str
    min: str
    min_length: str
    multiple: str
    name: str
    pattern: str
    placeholder: str
    readonly: str
    required: str
    selection_direction: str
    selection_end: str
    selection_start: str
    size: str
    src: str
    step: str
    type: str
    value: str
    width: str

class HTMLListItemElement(HTMLElementProps, total=False, closed=True):
    value: str

class HTMLLabelElement(HTMLElementProps, total=False, closed=True):
    html_for: str

class HTMLLegendElement(HTMLElementProps, total=False, closed=True):
    align: str

class HTMLLinkElement(HTMLElementProps, total=False, closed=True):
    html_as: str
    cross_origin: str
    disabled: str
    href: str
    hreflang: str
    media: str
    referrer_policy: str
    rel: str
    sizes: str
    type: str

class HTMLMapElement(HTMLElementProps, total=False, closed=True):
    name: str

class HTMLDocumentMetaElement(HTMLElementProps, total=False, closed=True):
    name: str
    content: str

class HTMLPragmaMetaElement(HTMLElementProps, total=False, closed=True):
    http_equiv: str

class HTMLCharsetMetaElement(HTMLElementProps, total=False, closed=True):
    charset: str

class HTMLUserMetaElement(HTMLElementProps, total=False, closed=True):
    itemprop: str

class HTMLMeterElement(HTMLElementProps, total=False, closed=True):
    form: str
    high: str
    low: str
    max: str
    min: str
    optimum: str
    value: str

class HTMLModElement(HTMLElementProps, total=False, closed=True):
    cite: str
    datetime: str

class HTMLObjectElement(HTMLElementProps, total=False, closed=True):
    data: str
    form: str
    height: str
    name: str
    type: str
    usemap: str
    width: str

class HTMLOrderedListElement(HTMLElementProps, total=False, closed=True):
    reversed: str
    start: str

class HTMLOptGroupElement(HTMLElementProps, total=False, closed=True):
    disabled: str
    label: str

class HTMLOptionElement(HTMLElementProps, total=False, closed=True):
    disabled: str
    label: str
    selected: str
    value: str

class HTMLOutputElement(HTMLElementProps, total=False, closed=True):
    html_for: str  # 'for' is a reserved keyword in Python, so using 'html_for'
    form: str
    name: str

class HTMLParagraphElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLParamElement(HTMLElementProps, total=False, closed=True):
    name: str
    value: str

class HTMLPictureElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLPreElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLProgressElement(HTMLElementProps, total=False, closed=True):
    max: str
    value: str

class HTMLQuoteElement(HTMLElementProps, total=False, closed=True):
    cite: str

class HTMLScriptElement(HTMLElementProps, total=False, closed=True):
    async_: bool  # 'async' is a reserved keyword in Python, so using 'async_'
    cross_origin: str
    defer: bool
    integrity: str
    nonce: str
    referrer_policy: str
    src: str
    type: str

class HTMLSelectElement(HTMLElementProps, total=False, closed=True):
    auto_complete: str
    auto_focus: str
    disabled: str
    form: str
    multiple: str
    name: str
    required: str
    size: str

class HTMLSlotElement(HTMLElementProps, total=False, closed=True):
    name: str

class HTMLSourceElement(HTMLElementProps, total=False, closed=True):
    media: str
    sizes: str
    src: str
    srcset: str
    type: str

class HTMLSpanElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLStyleElement(HTMLElementProps, total=False, closed=True):
    media: str
    nonce: str
    scoped: str

class HTMLTableCaptionElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLTableCellElement(HTMLElementProps, total=False, closed=True):
    abbr: str
    colspan: str
    headers: str
    rowspan: str
    scope: str

class HTMLTableColElement(HTMLElementProps, total=False, closed=True):
    span: str

class HTMLTableDataCellElement(HTMLTableCellElement):
    pass  # Inherits attributes from HTMLTableCellElement

class HTMLTableElement(HTMLElementProps, total=False, closed=True):
    border: str
    cellpadding: str
    cellspacing: str
    frame: str
    rules: str
    summary: str
    width: str

class HTMLTableHeaderCellElement(HTMLTableCellElement):
    pass  # Inherits attributes from HTMLTableCellElement

class HTMLTableRowElement(HTMLElementProps, total=False, closed=True):
    align: str
    bgcolor: str
    ch: str
    choff: str
    v_align: str

class HTMLTableSectionElement(HTMLElementProps, total=False, closed=True):
    align: str
    ch: str
    choff: str
    v_align: str

class HTMLTemplateElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLTextAreaElement(HTMLElementProps, total=False, closed=True):
    auto_complete: str
    auto_focus: str
    cols: str
    dirname: str
    disabled: str
    form: str
    max_length: str
    min_length: str
    name: str
    placeholder: str
    readonly: str
    required: str
    rows: str
    wrap: str

class HTMLTimeElement(HTMLElementProps, total=False, closed=True):
    datetime: str

class HTMLTitleElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLTrackElement(HTMLElementProps, total=False, closed=True):
    default: str
    kind: str
    label: str
    src: str
    srclang: str

class HTMLUnorderedListElement(HTMLElementProps, total=False, closed=True):
    pass  # No additional attributes

class HTMLVideoElement(HTMLElementProps, total=False, closed=True):
    auto_play: str
    controls: str
    cross_origin: str
    height: str
    loop: str
    muted: str
    plays_inline: str
    poster: str
    preload: str
    src: str
    width: str
