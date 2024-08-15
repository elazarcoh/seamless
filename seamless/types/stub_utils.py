from pathlib import Path
import importlib
import re
import textwrap

import typing as t
from typing_extensions import TypedDict

from seamless.core.javascript import JavaScript
from seamless.styling import StyleObject

CONTEXT = {
    "JS": JavaScript,
    "StyleObject": StyleObject,
}

THIS_DIR = Path(__file__).parent
ROOT_DIR = THIS_DIR.parent.parent


def repr_type_hint(hint):
    if isinstance(hint, t._SpecialForm):
        return repr(hint)
    if isinstance(hint, type):
        return hint.__name__
    return repr(hint)


def typeddict_to_str(typeddict):
    class_name = typeddict.__name__
    hints = t.get_type_hints(typeddict, CONTEXT)
    content = ""
    for name, annotation in hints.items():
        content += f"{name}: {repr_type_hint(annotation)}\n"
    content += "\n"
    content += "__extra_items__: str\n"
    class_code = f"class {class_name}(TypedDict, total=False, closed=True):\n{textwrap.indent(content, '    ')}"
    return class_code


def new_empty_class_to_str(name: str, bases_names: t.List[str]):
    return f"class {name}({', '.join(bases_names)}): pass"


def imports():
    constant_imports = textwrap.dedent(
        """
        import typing
        from typing import *
        from typing import TypeVar, Generic, Unpack, NotRequired, TypedDict
        from types import NoneType
        """
    )

    more = []
    for module in []:
        names = get_module_names(module)
        assert "HTMLDivElement" in names
        assert "HTMLButtonElement" in names
        for name in names:
            more.append(f"from {module} import {name} as {name}")

    more_imports = "\n".join(more)
    return constant_imports + "\n" + more_imports


def get_module_names(module):
    from importlib import import_module

    module = import_module(module)
    names = dir(module)
    return names


def _is_typed_dict(cls: type) -> bool:
    from typing import _TypedDictMeta

    if isinstance(cls, _TypedDictMeta):
        return True
    try:
        from typing_extensions import _TypedDictMeta
    except ImportError:
        return False
    return isinstance(cls, _TypedDictMeta)


def generate(
    module_path: str,
    name: str,
    more_bases: t.List[t.Type[TypedDict]] = [],
    stubs_root: Path | str = ROOT_DIR / "typings",
):
    if not re.match(r"seamless\.types\..+", module_path):
        raise ValueError(
            f"currently only supports seamless.types modules, got {module_path}"
        )

    module = importlib.import_module(module_path)
    module_file = module.__file__
    if module_file is None:
        raise ValueError(f"module {module_path} does not have __file__ attribute")
    module_filepath = Path(module_file)
    content = module_filepath.read_text()

    code = ""

    code += imports()
    code += "\n\n"

    code += content
    code += "\n\n"

    value = getattr(module, name)
    if not _is_typed_dict(value):
        raise NotImplementedError(f"Currently only supports TypedDict, got {value}")

    current_bases = getattr(value, "__orig_bases__", [])

    names = [base.__name__ for base in current_bases]
    for typeddict in more_bases:
        class_name = typeddict.__name__
        if class_name in names:
            continue
        names.append(class_name)
        code += typeddict_to_str(typeddict)
        code += "\n\n"

    code += new_empty_class_to_str(name, names)
    code += "\n\n"

    module_relapath = module_filepath.relative_to(ROOT_DIR)
    stub_path = stubs_root / module_relapath
    pyi_file = stub_path.with_suffix(".pyi")

    pyi_file.parent.mkdir(parents=True, exist_ok=True)
    with open(pyi_file, "w") as f:
        f.write(code)
