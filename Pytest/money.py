import pytest
from VendingM.money import Money


@pytest.fixture
def empty_money():
    return Money()


@pytest.fixture
def money():
    return Money(1, 2, 3, 4, 5)


def test_default_total_amount(empty_money):
    assert empty_money.total_amount == 0

def test_total_amount(money):
    money.update_total_amount()
    assert money.total_amount == 74.1

def test_get_number_of_money(money):
    # Testing if functioning properly
    assert money.get_number_of_money(money_type='coin_10bani') == 1

    # Testing if it throws error
    with pytest.warns():
        money.get_number_of_money(money_type='test')

def test_update_number_of_money(money):
    money.update_number_of_money('coin_50bani', 10)
    # Testing updating works from coin 50 bani updating it by +10 and checking the total updated amount
    assert money.get_number_of_money('coin_50bani') == 12
    assert money.total_amount == 79.1

    # Check if it throws warning when less than 0
    with pytest.warns():
        money.update_number_of_money('coin_50bani', -15)

    # Check if it throws warning when name is wrong
    with pytest.warns():
        money.update_number_of_money('lalaland', 15)
