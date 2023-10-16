import logging
from functools import wraps
from typing import (
    Any,
    Callable,
    ClassVar,
    Optional,
    ParamSpec,
    TypeVar,
)

from gi.repository import GObject, Gio

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


class _TaskData:
    values: ClassVar[dict[tuple[Any, Any], Any]] = {}


def run(
    source: GObject.Object,
    func: Callable[P, T],
    args: P.args = None,
    kwargs: P.kwargs = None,
    callback: Optional[Callable[[T], None]] = None,
    error_callback: Optional[Callable[[BaseException], None]] = None,
) -> Gio.Task:
    key = (source, func)

    def func_(*_: Any) -> None:
        name = func.__name__

        try:
            logger.debug(f"Running task '{name}'")
            args_ = args or ()
            kwargs_ = kwargs or {}
            _TaskData.values[key] = func(*args_, **kwargs_)
            logger.debug(f"Successfully run task '{name}'")

        except Exception as err:
            logger.warning(f"Failed to run task '{name}'")
            _TaskData.values[key] = err

    def on_finish(*_: Any) -> None:
        result = _TaskData.values[key]

        if isinstance(result, Exception) and error_callback:
            err_name = error_callback.__name__
            logger.debug(f"Running error callback '{err_name}'")
            error_callback(result)

        elif callback:
            name = callback.__name__
            logger.debug(f"Running callback '{name}'")
            callback(result)

    task: Gio.Task = Gio.Task.new(source, None, None, None)
    task.set_check_cancellable(True)
    task.set_return_on_cancel(True)
    task.return_error_if_cancelled()

    if callback:
        task.connect("notify::completed", on_finish)

    task.run_in_thread(func_)
    return task


def run_decorator(
    callback_name: str = "",
    error_callback_name: str = "",
) -> Callable[[Callable[P, T]], Callable[P, Gio.Task]]:
    def decorator(method_: Callable[P, T]) -> Callable[P, Gio.Task]:
        @wraps(method_)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Gio.Task:
            self = args[0]
            callback = getattr(self, callback_name) if callback_name else None
            error_callback = (
                getattr(self, error_callback_name) if error_callback_name else None
            )
            return run(
                self,  # type: ignore
                method_,
                args=args,
                kwargs=kwargs,
                callback=callback,
                error_callback=error_callback,
            )

        return wrapper

    return decorator
