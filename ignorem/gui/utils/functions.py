from __future__ import annotations

from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    ParamSpec,
    TypeVar,
)

from gi.repository import Adw, GObject, Gdk, Gio, Gtk

from ignorem.constants import Data

if TYPE_CHECKING:
    from ignorem.utils.types_ import PathLike

P = ParamSpec("P")
T = TypeVar("T")


def create_action(
    app: Adw.Application | Gtk.Application,
    action_name: str,
    callback: Callable[P, T],
    shortcuts: list[str] | None = None,
) -> None:
    action = Gio.SimpleAction.new(action_name, None)
    action.connect("activate", callback)
    app.add_action(action)
    if shortcuts:
        app.set_accels_for_action(f"app.{action_name}", shortcuts)


def register_type(class_: type[Any]) -> None:
    # Created as a workaround for untyped-def errors
    GObject.type_register(class_)  # type: ignore


def register_signal(
    name: str,
    source: GObject.Object | type[GObject.Object],
    flags: GObject.SignalFlags | int,
    return_type: Any,
    param_types: Iterable[type[Any]],
) -> None:
    # Wrapper function for typing
    GObject.signal_new(name, source, flags, return_type, param_types)  # type: ignore


def copy_to_clipboard(text: str) -> None:
    clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())  # type: ignore
    clipboard.set(text)


def save_template(text: str, path: PathLike) -> None:
    file_path = Path(path)
    file_path.write_text(text)


def open_logs() -> None:
    Gio.app_info_launch_default_for_uri(f"file://{Data.LOGS_FILE}")
