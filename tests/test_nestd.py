from nestd import nested, get_all_nested,nested_deep_search
import random

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

def dummy_function_with_nested_inner_functions():
    
    test_array=[1,2,3]
    def math():
        nonlocal test_array
        def sum():
            nonlocal test_array
            def sum_of_array():
                nonlocal test_array
                inside_arr=[random.randint(1,10)]*len(test_array)
                return test_array+inside_arr
            def multi_of_array():
                nonlocal test_array
                inside_arr=[random.randint(1,10)]*len(test_array)
                for i in range(len(test_array)):
                    inside_arr[i]=inside_arr[i]*test_array[i]
                return inside_arr
            
            ans=0
            for i in test_array:
                ans+=i
            return ans
        

        def multiply():
            nonlocal test_array
            ans=1
            for i in test_array:
                ans=ans*i
            
            return ans


        return test_array
    def stats():
        nonlocal test_array
        def mean():
            nonlocal test_array
            return sum(test_array)/len(test_array)
        
        return test_array


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
def test_3_nested_functions():
    inner_functions=nested_deep_search(dummy_function_with_nested_inner_functions,test_variable="hello_world",test_array=[1,2,3])
    if(inner_functions==None):
        return None

    assert inner_functions['math']()==[1,2,3]
    assert inner_functions['sum']()==6
    assert inner_functions['mean']()==2.0
    