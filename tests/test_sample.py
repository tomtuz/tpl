def func(x):
    return x + 1


def test_one():
    assert func(4) == 5


def test_two():
    assert func(1) != 5
