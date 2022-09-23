import pandas as pd
from VendingM.item import Item
from VendingM.inventory import Inventory
from VendingM.money import Money
import datetime

class VendingMachine:

    def __init__(self):
        self._item_price = None
        self._item_name = None
        self.inventory = None
        self.money = None
        self.__initialize_inventory()
        self.__initialize_wallet()
        self._user_amount = 0
        self._curr_inventory = None
        self._state = 'Not Found'
        self._log = pd.read_csv('log_file.csv')
        self._temp_df = pd.DataFrame(columns=['Time', 'Product', 'Price', 'State'])

    def __initialize_inventory(self):
        inventory_df = pd.read_csv('./Inventory.csv')
        inventory = Inventory()
        for row in range(len(inventory_df)):
            inventory.add_new_product(inventory_df.loc[row, 'Product_Name'],
                                      inventory_df.loc[row, 'Price'],
                                      inventory_df.loc[row, 'Quantity'])
        self.inventory = inventory

    # def __export_inventory(self):
    #     export_inventory_df = pd.DataFrame(columns=['Product_Name', 'Price', 'Quantity'])
    #     for item in self.inventory.item_inventory:
    #         export_inventory_df = export_inventory_df.append(
    #             {'Product_Name': item.name, 'Price': item.price, 'Quantity': item.quantity}, ignore_index=True)
    #     self.__curr_inventory = export_inventory_df
    #     export_inventory_df.to_csv('Inventory.csv', index=False)

    def __current_inventory(self, export: bool = False) -> None:
        prod_name = []
        prod_price = []
        prod_quantity = []
        for item in self.inventory.item_inventory:
            prod_name.append(item.name)
            prod_price.append(item.price)
            prod_quantity.append(item.quantity)
        export_inventory_df = pd.DataFrame(columns=['Product_Name', 'Price', 'Quantity'])
        export_inventory_df['Product_Name'] = prod_name
        export_inventory_df['Price'] = prod_price
        export_inventory_df['Quantity'] = prod_quantity
        self._curr_inventory = export_inventory_df
        if export == True:
            export_inventory_df.to_csv('Inventory.csv', index=False)

    def __initialize_wallet(self):
        money = Money(coin_10bani=10,
                      coin_50bani=10,
                      banknote_1leu=10,
                      banknote_5lei=10,
                      banknote_10lei=10)
        self.money = money

    def select_item(self, name: str) -> float:
        item = self.inventory.return_item_by_name(name)
        self._item_price = item.price
        self._item_name = item.name
        return item

    def insert_money(self, input_dict={}):
        curr_amount = self.money.total_amount
        for currkey in input_dict.keys():
            self.money.update_number_of_money(currkey, input_dict[currkey])
        self._user_amount = self.money.total_amount - curr_amount

    def has_sufficient_money(self) -> bool:
        if self._user_amount >= self._item_price:
            return True
        return False

    def pay_money(self) -> str:
        self._user_amount -= self._item_price
        return f'You current balance is: {self._user_amount}'

    def collect_item(self):
        self.inventory.modify_item_quantity(self._item_name, -1)
        print(self.inventory)

    def collect_change(self):
        if self._user_amount > 0:
            self.money.total_amount -= self._item_price
            print(f'Your change is {round(self._user_amount, 2)}')
            self._user_amount -= self._item_price
        else:
            print("No change to get.")

    def money_back(self):
        self.money.total_amount -= self._user_amount
        print(f"Here is your money back {round(self._user_amount, 2)}")
        self._user_amount = 0

    def update_total_amount(self) -> None:
        self.money.update_number_of_money()

    def cancel_transaction_get_money_back(self) -> None:
        self.money.total_amount -= self._user_amount

    def cancel_transaction_before_adding_money(self) -> None:
        raise ValueError('Cancelled by user.')

    # def __initialize_log_state(self) -> pd.DataFrame:
    #     self._log = pd.read_csv('log_file.csv')

    def __export_log_state(self) -> None:
        if isinstance(self._log, pd.DataFrame):
            self._log.to_csv('log_file.csv', index=False)

    @staticmethod
    def __current_time():
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time

    def __concat_state(self):
        self._temp_df['Time'] = self.__current_time()
        self._temp_df['Product'] = self._item_price
        self._temp_df['Price'] = self._item_price
        self._temp_df['State'] = self._state
        self._log = pd.concat([self._log, self._temp_df], ignore_index=True)
        print(self._temp_df)


    def run_vending_machine(self):
        # TODO: initialize and export for money, give change from money, more interactive
        while (True):
            command_vm = input('Please enter the action you would like to perform: (buy/cancel):\n')
            print(self.__current_time())
           # self.__initialize_log_state()
            if command_vm == 'buy':
                print('Welcome to the vending machine!')
                print('Please select the item that you would like to buy:')
                self.__current_inventory()
                print(self._curr_inventory)
                name = input("Please enter the name of the product: ")
                product_details = self.select_item(name)
                sure = input("Are you sure?")
                print(f'Please insert the money! The product costs {product_details.price} lei.')
                user_dict = {'coin_10bani': 0, 'coin_50bani': 0, 'banknote_1leu': 0, 'banknote_5lei': 0,
                             'banknote_10lei': 0}

                for key in user_dict.keys():
                    money_amount = input(f'Please insert {key} amount:')
                    user_dict[key] += int(money_amount)
                self.__concat_state()
                self.insert_money(user_dict)

                print(f'Money inserted! Your balance is {round(self._user_amount, 2)}.')

                if self.has_sufficient_money():
                    self.pay_money()
                    self.collect_item()
                    print(f'You can now retrieve your {self._item_name}')
                    self.collect_change()
                    self._state = "Transaction finalised"
                    self.__current_inventory(export=True)
                else:
                    print(f"Insufficient money!\n Please pick up your money: {round(self._user_amount, 2)} lei and try again.")
                    self._state = "Insufficient money"
                    self.money_back()


                self.__export_log_state()
            else:
                break

            # # self.inventory.add_new_product('Apa Plata', 2, 15)


if __name__ == '__main__':
    vm = VendingMachine()
    print(vm.inventory)
    vm.run_vending_machine()
