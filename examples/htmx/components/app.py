from typing import Sequence
from fastapi import Request
from seamless import H2, JS, A, P, Button, Component, Div, Form, Fragment, Span
from starlette_wtf import StarletteForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from pages import BasePage


class MyForm(StarletteForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1)])

    submit = SubmitField("Submit")

    async def async_validate_name(self, field: StringField):
        if not field.data:
            raise ValidationError("Name cannot be empty.")
        if field.data.lower() == "admin":
            raise ValidationError("Name cannot be 'admin'.")
        if len(field.data) < 3:
            raise ValidationError("Name must be at least 3 characters long.")
        return


class ErrorsComponent(Component):
    def __init__(self, *, errors: Sequence[str]):
        self.errors = errors

    def render(self):
        return Div(
            *[Span(error) for error in self.errors],
            class_="text-red-500",
        )


class FormComponent(Component):
    def __init__(self, *, form: MyForm):
        self.form = form

    def render(self):
        return Form(hx_post="/", hx_swap="outerHTML")(
            self.form.name(
                placeholder="Name",
                class_="input input-bordered w-full max-w-xs",
            ),
            ErrorsComponent(errors=self.form.name.errors)
            if self.form.name.errors
            else None,
            self.form.submit(class_="btn btn-primary"),
        )


class FeatureContainer(Component):
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def render(self):
        return Div(
            class_="container flex flex-col bg-base-200 shadow-md p-4 rounded-md"
        )(
            H2(class_="font-bold text-lg")(self.title),
            P(class_="text-sm text-pretty text-base-content")(self.description),
            Div(class_="divider")(),
            Div(
                class_="bg-base-100 p-4 rounded-md w-full h-full flex flex-col items-center justify-center"
            )(
                *self.children,
            ),
        )


class App(Component):
    def __init__(self, form: MyForm):
        super().__init__()
        self.form = form

    def render(self):
        return BasePage()(
            # Server counter
            Div(class_="p-4 grid grid-cols-2 gap-4")(
                FeatureContainer(
                    title="Server Counter",
                    description="This counter is updated by the server using Server-Sent Events.",
                )(
                    Button(
                        hx_get="/sse/counter",
                        hx_swap="outerHTML",
                        class_="btn btn-primary",
                    )("Start Counter"),
                ),
                FeatureContainer(
                    title="Form",
                    description="This form is submitted via htmx and uses wtforms.",
                )(
                    FormComponent(form=self.form),
                ),
            )
        )
