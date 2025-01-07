from src.main import get_greeting
import pytest

@pytest.mark.parametrize("name", ["Alice", "Bob", "Charlie"])
def test_print_hello(name):
    result = get_greeting(name)
    assert result == f"Hello, {name}!"