import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
 
def test_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hello'=='world') is False

def test_type():
    assert type('Hello' is str)
    assert type('World' is not int)

def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False,False]

    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)  ## The all function returns True if all elements in the iterable (in this case, num_list) are true (or if the iterable is empty).
                          ## Since num_list contains [1, 2, 3, 4, 5], and all these numbers are considered true in a boolean context, all(num_list) returns True.

    assert not any(any_list)  ##  The any function returns True if any element in the iterable (in this case, any_list) is true.
                               ## Since any_list contains [False, False], and all elements are False, any(any_list) returns False.
                              ##   The not operator negates this result, so not any(any_list) returns True.

class Student:
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name=first_name
        self.last_name=last_name
        self.major =major
        self.years = years

## to test the Student we can create an instance of student wherever we need to use it or ...
def test_person_initialization():
    p = Student('John','Doe','Computer Science',3)
    assert p.first_name== 'John', 'First name should be John'
    assert p.last_name== 'Doe', 'Last name should be Doe'
    assert p.major== 'Computer Science'
    assert p.years == 3

## ... we can create what is called a pytest fixture, instantiated it once and use wherever needed
## reusing this component.
## ( to use this we need to import pytest library)
@pytest.fixture
def default_employee():
    return Student('John','Doe','Computer Science',3)

def test_person_initialization_2(default_employee):   
    assert default_employee.first_name== 'John', 'First name should be John'
    assert default_employee.last_name== 'Doe', 'Last name should be Doe'
    assert default_employee.major== 'Computer Science'
    assert default_employee.years == 3