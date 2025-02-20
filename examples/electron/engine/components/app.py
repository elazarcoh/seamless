import seamless.html as d
from seamless.context.context import Context
from seamless.styling import StyleObject
from seamless.extensions import State, SocketIOTransport
from seamless.components.router import Router, Route, RouterLink
from pages.base import BasePage
from components.loading import Loading
from components.usage import Usage


def App():
    return BasePage(
        State.init(),
        SocketIOTransport.init(),
        d.Div(class_name="flex flex-col h-[100px]")(
            d.Div(class_name="flex justify-between")(
                d.Nav(class_name="navbar navbar-expand-lg navbar-light bg-light")(
                    RouterLink(to="/", class_name="navbar-brand")("Home"),
                    RouterLink(to="/counter", class_name="navbar-brand")("Counter"),
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
