from seamless.types.html_element import HTMLElement
from seamless.types.html_event_props import HTMLEventProps
from seamless.types.aria_props import AriaProps

class HTMLElementProps(HTMLElement, AriaProps, HTMLEventProps, closed=True):
    pass