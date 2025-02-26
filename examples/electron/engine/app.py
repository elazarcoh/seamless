import seamless.html as d
from seamless.context.context import Context
from seamless.styling import StyleObject
from seamless.extensions import State, SocketIOTransport
from seamless.components.router import Router, Route, RouterLink
from .pages.base import BasePage
from .components.loading import Loading
from .components.usage import Usage


def App():
    router_link_class = "text-gray-700 hover:text-gray-900 hover:bg-gray-300 px-3 py-2"
    return BasePage(
        State.init(),
        SocketIOTransport.init(),
        d.Div(class_name="flex flex-col h-[100px]")(
            d.Div(class_name="flex justify-between")(
                d.Nav(class_name="flex gap-4 bg-gray-200")(
                    RouterLink(to="/", class_name=router_link_class)("Home"),
                    RouterLink(to="/counter", class_name=router_link_class)("Counter"),
                ),
                d.Div(
                    d.Button(
                        on_click=foo,
                        style=StyleObject(border_radius="5px", background_color="red"),
                    )("Click me!")
                ),
            ),
            d.Div(class_name="content flex-grow-1")(
                Router(loading_component=Loading)(
                    Route(path="/usage", component=Usage),
                )
            ),
        ),
        title="Seamless",
    )


def foo(event, context: Context):
    print("foo")
