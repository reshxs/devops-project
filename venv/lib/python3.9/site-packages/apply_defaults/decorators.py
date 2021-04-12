from configparser import ConfigParser
from functools import wraps
from inspect import signature
from typing import Any, Callable, Dict, Optional


def apply_self(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        for name in signature(function).parameters:
            if name in self.__dict__ and name not in kwargs:
                kwargs[name] = getattr(self, name)
        return function(self, *args, **kwargs)

    return wrapper


def apply_config(
    config: ConfigParser, section: str = "general", converters: Optional[Dict] = None
) -> Callable:
    def real_decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for name, param in signature(function).parameters.items():
                if config.has_option(section, name) and name not in kwargs:
                    # If name is specified in converters dict
                    if converters is not None and name in converters.keys():
                        kwargs[name] = getattr(config, converters[name])(section, name)
                    # Try to infer the type from the parameter's annotation
                    elif param.annotation is int:
                        kwargs[name] = config.getint(section, name)
                    elif param.annotation is float:
                        kwargs[name] = config.getfloat(section, name)
                    elif param.annotation is bool:
                        kwargs[name] = config.getboolean(section, name)
                    else:
                        kwargs[name] = config.get(section, name)
            return function(*args, **kwargs)

        return wrapper

    return real_decorator
