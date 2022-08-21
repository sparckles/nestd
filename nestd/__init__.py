"""Gain access to the code objects of inner functions for testing purposes."""
import types
from pprint import pprint


def free_var(val):
    """A function that wraps free variables."""

    def nested():
        return val

    return nested.__closure__[0]


def nested(outer, inner_name, **free_vars):
    """Find the code object of an inner function and return it as a callable object.

    Arguments:
        outer (function or method): A function object with an inner function.
        inner_name (str): The name of the inner function we want access to
        **free_vars (dict(str: any)): A dictionary with values for the free
            variables in the context of the inner function.
    Returns:
        A function object for the inner function, with context variables set.
    """
    if not isinstance(outer, (types.FunctionType, types.MethodType)):
        raise Exception("Outer function is not a function or a method type")

    outer = outer.__code__

    for const in outer.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == inner_name:
            # just need to check why the free_var call is required
            # update the documentation of the free_var call
            return types.FunctionType(
                const,
                globals(),
                None,
                None,
                tuple(free_var(free_vars[name]) for name in const.co_freevars),
            )


def get_all_nested(fx, *context_vars):
    """Return all nested functions of a function.

    Arguments:
        fx (function or method): A function object with inner function(s).
        *context_vars: context variables corressponding inner functions in the order of occurence.

    Returns:
        A list of tuples, with the first element as the function name and the second element as function object.
        e.g. [("inner_function", <class function....>), ....]
    """
    if not isinstance(fx, (types.FunctionType, types.MethodType)):
        raise Exception("Supplied param is not a function or a method type")

    fx = fx.__code__
    context_variables = list(context_vars)

    output = []
    for const in fx.co_consts:
        if isinstance(const, types.CodeType):
            context = tuple(
                free_var(context_variables[0]) for name in const.co_freevars
            )
            context_variables = context_variables[1:]
            output.append(
                (
                    const.co_name,
                    types.FunctionType(const, globals(), None, None, context),
                )
            )

    return output


def get_all_deep_nested(fx, dict={}, **free_vars):
    """Find the code object of an inner function recursively and  return it as a callable object.

    Arguments:
        fx (function or method): A function object with an inner function.
        dict a Dictionary by default set to be empty to storing the values in recursion.
        **free_vars (dict(str: any)): A dictionary with values for the free
            variables in the context of the inner function.
    Returns:
        A dictionary with Key as Function Name and Value as Function Object
        e.g. {"inner_funciton":<class funtions....>,.....}
    """
    if not isinstance(fx, (types.FunctionType, types.MethodType)):
        raise Exception("Supplied param is not a function or a method type")

    fx = fx.__code__
    for const in fx.co_consts:
        if isinstance(const, types.CodeType):
            fun = types.FunctionType(
                const,
                globals(),
                None,
                None,
                tuple(free_var(free_vars[name]) for name in const.co_freevars),
            )
            dict[const.co_name] = fun
            get_all_deep_nested(fun, dict, **free_vars)

    return dict


__version__ = "0.3.0"
