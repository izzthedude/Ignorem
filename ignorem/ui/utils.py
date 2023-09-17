from gi.repository import Adw, GObject, Gio


def create_action(
    source: Adw.Application | Adw.ApplicationWindow,
    action_name: str,
    callback,
    shortcuts: list | None = None,
):
    action = Gio.SimpleAction.new(action_name, None)
    action.connect("activate", callback)
    source.add_action(action)

    if shortcuts:
        app = source
        origin = "app"
        if isinstance(app, Adw.ApplicationWindow):
            app = source.get_application()
            origin = "win"

        app.set_accels_for_action(f"{origin}.{action_name}", shortcuts)


def create_signal(source: GObject.Object, signal_name: str, param_types: tuple = ()):
    GObject.signal_new(
        signal_name,  # Signal name
        source,  # A Python GObject instance or type that the signal is associated with
        GObject.SIGNAL_RUN_FIRST,  # Signal flags
        GObject.TYPE_NONE,  # Return type of the signal handler
        param_types,  # Parameter types
    )
