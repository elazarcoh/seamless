from typing import Sequence
from fastapi import Request
from seamless import JS, A, Button, Component, Div, Form, Fragment, Span
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


class App(Component):
    def __init__(self, form: MyForm):
        super().__init__()
        self.form = form

    def render(self):
        return BasePage()(
            # Server counter
            Div(sse_swap="counter", class_="border border-neutral p-4")(
                "Waiting for server counter...",
            ),
            FormComponent(form=self.form),
        )
