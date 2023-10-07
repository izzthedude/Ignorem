from typing import Callable, Optional, ParamSpec, TypeVar

from gi.repository import Adw, Gio

P = ParamSpec("P")
T = TypeVar("T")


def create_action(
    source: Adw.Application | Adw.ApplicationWindow,
    action_name: str,
    callback: Callable[P, T],
    shortcuts: Optional[list[str]] = None,
) -> None:
    action = Gio.SimpleAction.new(action_name, None)
    action.connect("activate", callback)
    source.add_action(action)

    if shortcuts:
        app = source
        origin = "app"

        if isinstance(source, Adw.ApplicationWindow):
            app = source.get_application()
            origin = "win"

        app.set_accels_for_action(f"{origin}.{action_name}", shortcuts)
