from seamless import A, JS, Component, Div, Nav, Button
from seamless.extensions import State
from pages import HomePage, CounterPage, BasePage
from components.loading import Loading


class App(Component):
    def render(self):
        return BasePage(
            State.init(),
            Div(class_name="d-flex flex-column h-100")(
                Div(class_name="d-flex justify-content-between")(
                    Nav(class_name="navbar navbar-expand-lg navbar-light bg-light")(
                        A(href="/", class_name="navbar-brand")("Home"),
                        A(href="/counter", class_name="navbar-brand")("Counter"),
                    ),
                    Div(
                        Button(on_click=self.foo(), class_name="btn btn-primary")(
                            "Click me!"
                        )
                    )
                ),
            ),
            title="Seamless",
        )

    def foo(self):
        return JS("console.log('foo')")