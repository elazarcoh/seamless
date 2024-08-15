from typing_extensions import TypedDict

from seamless.types.stub_utils import generate


class HTMXProps(TypedDict, total=False, closed=True):
    hx_get: str
    hx_post: str


# %%

generate(
    module_path="seamless.types.html_element_props",
    name="HTMLElementProps",
    more_bases=[HTMXProps],
    stubs_root="./typings",
)
