from typing import Any, Callable

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


def run_async(
    source: GObject.Object,
    func: Callable,
    callback: Callable | None = None,
    func_args: tuple = (),
    callback_args: tuple = (),
) -> Gio.Task:
    def _func(
        task: Gio.Task,
        source: GObject.Object,
        data: Any,
        cancellable: Gio.Cancellable | None,
    ):
        func_name = func.__name__

        try:
            print(f"Running task: {func_name}")
            func(*func_args)
            print(f"Finished task: {func_name}")
        except Exception as err:
            print(f"An error has occurred while running task '{func_name}':", err)

    def _callback(task: Gio.Task, status: GObject.ParamSpecBoolean):
        callback_name = callback.__name__

        try:
            print(f"Running callback: {callback_name}")
            callback(*callback_args)
            print(f"Finished callback: {callback_name}")
        except Exception as err:
            print(f"An error has occurred while running task '{callback_name}':", err)

    task: Gio.Task = Gio.Task.new(source, None, None, None)
    task.set_check_cancellable(True)
    task.set_return_on_cancel(True)
    task.return_error_if_cancelled()
    if callback:
        task.connect("notify::completed", _callback)

    task.run_in_thread(_func)
    return task
