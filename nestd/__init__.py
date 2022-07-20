"""Gain access to the code objects of inner functions for testing purposes."""
import types
from pprint import pprint


def free_var(val):
    """A function that wraps free variables."""

    def nested():
        return val

    return nested.__closure__[0]


# class function(object)
#  |  function(code, globals, name=None, argdefs=None, closure=None)
#  |
#  |  Create a function object.
#  |
#  |  code
#  |    a code object
#  |  globals
#  |    the globals dictionary
#  |  name
#  |    a string that overrides the name from the code object
#  |  argdefs
#  |    a tuple that specifies the default argument values
#  |  closure
#  |    a tuple that supplies the bindings for free variables
#  |
#  |  Methods defined here:
#  |
#  |  __call__(self, /, *args, **kwargs)
#  |      Call self as a function.
#  |
#  |  __get__(self, instance, owner, /)
#  |      Return an attribute of instance, which is of type owner.
#  |
#  |  __repr__(self, /)
#  |      Return repr(self).
#  |
#  |  ----------------------------------------------------------------------
#  |  Static methods defined here:
#  |
#  |  __new__(*args, **kwargs) from builtins.type
#  |      Create and return a new object.  See help(type) for accurate signature.
#  |
#  |  ----------------------------------------------------------------------
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
    """Return all nested functions of a function."""
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


__version__ = "0.1.0"
