from nestd import nested, get_all_nested


def dummy_function():
    test_variable = "hello, world"
    def inner_function():
        nonlocal test_variable
        return test_variable


def dummy_function_with_two_inner_functions():
    test_variable = "hello, world"
    test_array = [1, 2, 3]
    def inner_function():
        nonlocal test_variable
        return test_variable

    def inner_function_2():
        nonlocal test_array
        return test_array[1:]


def test_nested_function():
    inner_function = nested(dummy_function, "inner_function", test_variable="hello" )
    assert "hello" == inner_function()

def test_2_nested_functions():
    all_inner_functions = get_all_nested(dummy_function_with_two_inner_functions, "hello_world", [1,2])
    inner_function, inner_function_2 = all_inner_functions

    assert inner_function[0] == "inner_function"
    assert inner_function[1]() == "hello_world"

    assert inner_function_2[0] == "inner_function_2"
    assert inner_function_2[1]() == [2]
