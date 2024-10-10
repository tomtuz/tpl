import functools
import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def validate_args(min_args: int, error_class: type, error_message: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(args: list[str], *func_args, **func_kwargs) -> Any:
            if len(args) < min_args:
                raise error_class(error_message)
            return func(args, *func_args, **func_kwargs)

        return wrapper

    return decorator


def handle_command_errors(error_class: type) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise error_class(f"Error in {func.__name__}: {str(e)}")

        return wrapper

    return decorator


def log_command_args(title: str, arg_names: list[str], args: list[str]) -> None:
    """
    Log the arguments passed to a command function.

    Args:
        title (str): The title of the log entry.
        arg_names (List[str]): The names of the arguments.
        args (List[str]): The actual argument values.
    """
    logger.info(f"\n{title}:")
    logger.info("---------")
    for idx, name in enumerate(arg_names):
        value = args[idx] if idx < len(args) else None
        logger.info(f'{idx}: {name} = "{value}"')
    logger.info("---------\n")
