# coding: utf-8
import functools
import inspect
import warnings

string_types = (type(b''), type(u''))


def deprecated(reason):
    """ A decorator which can be used to mark functions as deprecated. """

    if isinstance(reason, string_types):
        def wrapper(func):

            if inspect.isclass(func):
                fmt = "Call to deprecated class `{name}` ({reason})."
            else:
                fmt = "Call to deprecated function `{name}` ({reason})."

            @functools.wraps(func)
            def inner(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt.format(name=func.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func(*args, **kwargs)

            return inner

        return wrapper

    elif inspect.isclass(reason) or inspect.isfunction(reason):

        func = reason

        if inspect.isclass(func):
            fmt = "Call to deprecated class `{name}`."
        else:
            fmt = "Call to deprecated function `{name}`."

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt.format(name=func.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    raise TypeError(repr(type(reason)))
