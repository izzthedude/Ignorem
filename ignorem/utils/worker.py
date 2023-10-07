import traceback
from functools import wraps
from typing import Any, Callable, Iterable, Mapping, Optional, ParamSpec, TypeVar

from gi.repository import GObject, Gio

P = ParamSpec("P")
T = TypeVar("T")


class _TaskData:
    values: dict[tuple[Any, Any], Any] = {}


def run_task(
    source: GObject.Object,
    func: Callable[P, T],
    args: Optional[Iterable[Any]] = None,
    kwargs: Optional[Mapping[str, Any]] = None,
    callback: Optional[Callable[[T], object]] = None,
    error_callback: Optional[Callable[[BaseException], T]] = None,
) -> Gio.Task:
    key = (source, func)

    def func_(*_: Any) -> None:
        name = func.__name__

        try:
            print(f"[WORKER]: Running '{name}' {args=} {kwargs=}")
            args_ = args if args else tuple()
            kwargs_ = kwargs if kwargs else dict()
            result = func(*args_, **kwargs_)

        except Exception as err:
            print(f"[WORKER]: Failed to run '{name}' due to error:")
            traceback.print_exc()
            result = err  # type: ignore

        finally:
            _TaskData.values[key] = result

    def on_finish(*_: Any) -> None:
        result = _TaskData.values.pop(key)

        if isinstance(result, Exception) and error_callback:
            err_name = error_callback.__name__
            print(f"[WORKER]: Running '{err_name}' args={result}.")
            error_callback(result)

        if callback:
            name = callback.__name__
            print(f"[WORKER]: Running '{name}' args={result}")
            callback(result)

    task: Gio.Task = Gio.Task.new(source, None, None, None)
    task.set_check_cancellable(True)
    task.set_return_on_cancel(True)
    task.return_error_if_cancelled()

    if callback:
        task.connect("notify::completed", on_finish)

    task.run_in_thread(func_)
    return task


def run(
    callback_name: str = "",
    error_callback_name: str = "",
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(method_: Callable[P, T]) -> Callable[P, T]:
        @wraps(method_)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self = args[0]
            callback = getattr(self, callback_name)
            error_callback = getattr(self, error_callback_name)
            return run_task(  # type: ignore
                self,
                method_,
                args=args,
                kwargs=kwargs,
                callback=callback,
                error_callback=error_callback,
            )

        return wrapper

    return decorator
