# Bank System - J. Ekpo
import random

CHOICES = ["1: Create an account",
           "2: Log into account",
           "1: Balance",
           "2: Log out",
           "0: Exit",
           ]


class AccountPinGenerator:
    IIN = "400000"
    checksum = "1"
    random.seed()

    def get_pin(self):
        x = random.randint(0000, 9999)
        if x < 1000:
            x += 1000
        return x

    # All cards have same 6 initial digits and are missing a 10 additional digits
    # The last digit is a special checksum used for verification
    # Generates 9 random numbers by using character conversion:
    # chr(48) = 0, chr(57) = 9
    def get_number(self):
        while len(self.IIN) <= 14:
            new_digit = str(chr(random.randint(48, 57)))
            self.IIN += new_digit

        self.IIN += self.checksum
        return self.IIN, self.get_pin()


class AccountStorage:
    total_accounts = 0
    account_data = {}

    def add_account(self, acc_num, data): #type(data) == List
        self.account_data[acc_num] = data
        self.total_accounts += 1

    def check_account(self, acc_num, pin):
        if acc_num in self.account_data:
            x = self.account_data[acc_num]
            return x[0] == pin
        else:
            return False

    def get_acc_balance(self, account_number):
        if account_number in self.account_data:
            bal = self.account_data[account_number]
        return bal[1]


class Account:

    def __init__(self):
        accountant = AccountPinGenerator()
        storage = AccountStorage()

        self.account_number = accountant.get_number()[0]
        self.pin_number = accountant.get_number()[1]
        self.balance = 0
        data = [self.pin_number, self.balance]
        storage.add_account(acc_num=self.account_number, data=data)

    def get_info(self):
        info = [self.account_number, self.pin_number, self.balance]
        return info


def get_choice(menu):
    logged_in_options = f"{CHOICES[2]}\n{CHOICES[3]}\n{CHOICES[4]}\n"
    logged_out_options = f"{CHOICES[0]}\n{CHOICES[1]}\n{CHOICES[4]}\n"

    if menu < 0:
        return int(input(logged_out_options))
    else:
        return int(input(logged_in_options))


def create_account():
    new_account = Account()
    acc_info = new_account.get_info()
    print("Your card has been created")
    print("Your card number: \n{}\nYour card PIN: \n{}\n".format(acc_info[0], acc_info[1]))


def account_login():
    # print("Log into existing account!\n")

    account_num = input("Acc #: ")
    pin_num = int(input("****: "))

    acc_chkr = AccountStorage()
    if acc_chkr.check_account(account_num, pin_num):
        pass
    else:
        print("Wrong card number or PIN!\n")
        return False

    return account_num


def main():
    logged_in = False
    choice = -1
    user_data = None

    while choice != 0:

        if logged_in:  # User is logged into account
            choice = get_choice(1)
            if choice == 1:  # Check Balance
                acc = AccountStorage()
                print(f"Balance: {acc.get_acc_balance(user_data)}\n")
            elif choice == 2:  # Log Out
                logged_in = False
                print("\nYou have successfully logged out!\n")
            elif choice == 0:
                exit(0)
        else:  # User is NOT logged into account
            choice = get_choice(-1)
            if choice == 1:  # Create an account
                create_account()
            elif choice == 2:  # Log into account
                x = account_login()
                if x:
                    logged_in = True
                    user_data = x
                    print("\nYou have successfully logged in!\n")
            elif choice == 0:
                exit(0)
            # else:
            #     for x in AccountStorage.account_data:
            #         print(x, " ", AccountStorage.account_data[x])


main()
