from typing import Any, Callable, Iterable, Optional, ParamSpec, Type, TypeVar

from gi.repository import Adw, GObject, Gio, Gtk

P = ParamSpec("P")
T = TypeVar("T")


def create_action(
    app: Adw.Application | Gtk.Application,
    action_name: str,
    callback: Callable[P, T],
    shortcuts: Optional[list[str]] = None,
) -> None:
    action = Gio.SimpleAction.new(action_name, None)
    action.connect("activate", callback)
    app.add_action(action)
    if shortcuts:
        app.set_accels_for_action(f"app.{action_name}", shortcuts)


def register_type(class_: Type[Any]) -> None:
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
