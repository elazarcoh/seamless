from typing_extensions import TypedDict, Union
from seamless.styling import StyleObject
from seamless.core.javascript import JS

class HTMLElement(TypedDict, total=False, closed=True):
    access_key: str
    auto_capitalize: str
    class_name: str
    content_editable: str
    # data: dict[str, str]  # add this if needed in the future
    dir: str
    draggable: str
    hidden: str
    id: str
    input_mode: str
    lang: str
    role: str
    spell_check: str
    style: Union[str, "StyleObject"]
    tab_index: str
    title: str
    translate: str

    init: "JS"

    __extra_items__: str
