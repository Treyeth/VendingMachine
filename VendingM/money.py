import warnings


class Money:
    def __init__(self, coin_10bani: int = 0, coin_50bani: int = 0,
                 banknote_1leu: int = 0, banknote_5lei: int = 0,
                 banknote_10lei: int = 0):
        # TODO: can be adapted with enum type
        self._amount = {'coin_10bani': coin_10bani, 'coin_50bani': coin_50bani, 'banknote_1leu': banknote_1leu,
                        'banknote_5lei': banknote_5lei, 'banknote_10lei': banknote_10lei}
        self._total_amount = 0
        self.update_total_amount()

    def __repr__(self) -> str:
        return 'Money()'

    def __str__(self) -> str:
        message = f"10 bani coins: {self._amount['coin_10bani']}\n" \
                  f"50 bani coins: {self._amount['coin_50bani']}\n" \
                  f"1 leu banknotes: {self._amount['banknote_1leu']}\n" \
                  f"5 lei banknotes: {self._amount['banknote_5lei']}\n" \
                  f"10 lei banknotes: {self._amount['banknote_10lei']}\n\n" \
                  f"Total amount is: {self._total_amount}\n"
        return message

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, value):
        self._total_amount = value

    def update_total_amount(self):
        amount = self._amount
        sum_money = amount['coin_10bani'] * 0.10 + amount['coin_50bani'] * 0.50 + amount['banknote_1leu'] * 1 + \
                    amount['banknote_5lei'] * 5 + amount['banknote_10lei'] * 10
        self._total_amount = sum_money

    def get_number_of_money(self, money_type: str) -> int:
        if money_type in self._amount:
            return self._amount[money_type]
        else:
            warnings.warn('Money type doesn\'t exist.')

    def update_number_of_money(self, money_type: str, quantity: int):
        # TODO: another function to remove and add by money amount
        if money_type in self._amount:
            if self._amount[money_type] + quantity >= 0:
                self._amount[money_type] += quantity
                self.update_total_amount()
            else:
                warnings.warn('Trying to remove more money than it is available.')
        else:
            warnings.warn('Money type doesn\'t exist.')
