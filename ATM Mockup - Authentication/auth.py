# Author  : Dharatiben Shah
# Date    : 04-17-2021

import os
import sqlite3
import random
from getpass import getpass

# create a database - sqllite3 as it comes with python installation
# this will create a database called "auth.sqlite3" in the same directory as the script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "auth.sqllite3")


def init():
    print("****** Welcome to bankPHP *******")

    have_account = int(
        input("Do you have an account with us ? Select 1(yes), 2(No) \n")
    )

    if have_account == 1:
        login()
    elif have_account == 2:
        # run the function to create the user_info table in sqlite3 database
        create_db_object(db_connect())
        register()
    else:
        print(
            f"You have selected - {have_account} which is NOT a valid option ! Try again"
        )
        init()


def db_connect(db_path=DEFAULT_PATH):
    """Returns a connection string back
    with sqlite3 database
    """
    con = sqlite3.connect(db_path)
    return con


def generation_account_number():
    """Generate 10 digit random integer account number"""
    return random.randrange(1111111111, 9999999999)


def create_db_object(con):
    """Creates a table in sqlite3 database"""
    sql = """CREATE table if not exists user_info (account_number INT, first_name TEXT, last_name TEXT, email TEXT, password TEXT, balance int default 0);"""
    try:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return True
    except:
        con.rollback()
        raise RuntimeError(
            "There is a problem creating user_info table in the sqlite database"
        )


def create_new_login_in_db(con, first_name, last_name, email, password):
    """Given first_name, last_name, email, password - this function generates a random account number
    and inserts the values in the user_info table in sqlite3 database"""
    sql = """
        INSERT INTO user_info (account_number, first_name, last_name, email, password)
        values (?, ?, ?, ?, ?);"""
    # open cursor
    cur = con.cursor()
    try:
        account_number = generation_account_number()
        cur.execute(sql, (account_number, first_name, last_name, email, password))
        # commit the transaction
        con.commit()
        con.close()
        return account_number
    except:
        con.rollback()
        raise RuntimeError("There is a problem inserting record in sqlite database")


def register():
    """Asks new users their email, first_name, last_name, password
    and provides them with an account number
    """
    email = input("What is your email address? \n")
    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    password = getpass("Create a password for yourself \n")
    account_created = create_new_login_in_db(
        db_connect(), first_name, last_name, email, password
    )
    if account_created:
        print("Your Account Has been created with the password you provided")
        print(" == ==== ====== ===== ===")
        print(f"Your account number is: {account_created}")
        print("Make sure you keep it safe and remember your password")
        print(" == ==== ====== ===== ===")
        # take the user to login
        login()
    else:
        print("Account registration failed .. please try again")
        register()


def is_account_number_valid(con, account_number):
    """This function checks if a given account number is valid or not by querying the sqlite3 database"""
    cur = con.cursor()
    cur.execute(
        "select  account_number, password, first_name, last_name, balance from user_info where account_number=?",
        (account_number,),
    )
    results = cur.fetchone()
    # this will be a tuple
    con.close()
    return results


def login():
    """This function facilitates the login process
    given a valid account number and password"""

    print("****** Welcome to Bank Login ******")
    user_account_number = input("Please provide your account number to login: \n")
    user_password = getpass("What is your password ? \n")

    valid_account = is_account_number_valid(db_connect(), user_account_number)

    if valid_account is not None and (user_password == valid_account[1]):
        print(
            f"Account number {user_account_number} matches the account number {valid_account[0]} found in database "
        )
        bank_operation(valid_account)
    else:
        print(
            f"Try Again -- Account number - {user_account_number} and/or  Password are incorrect \n"
        )
        # send back to login to try again
        login()


# bank operations
def bank_operation(valid_account):
    print(f"Welcome {valid_account[2]}  {valid_account[3]}")
    operation_selected = int(
        input(
            "What would you like to do ? (1) deposit, (2) withdrawl, (3) Logout, (4) Exit \n"
        )
    )

    if operation_selected == 1:
        deposit_operation(valid_account)
    elif operation_selected == 2:
        withdrawal_operation(valid_account)
    elif operation_selected == 3:
        logout()
    elif operation_selected == 4:
        exit()
    else:
        print("Invalid option selected")
        bank_operation(valid_account)


def update_database(con, valid_account, amount, operation):
    account_details = is_account_number_valid(db_connect(), valid_account[0])
    account_number = account_details[0]
    current_balance = account_details[4]
    if operation == "deposit":
        new_balance = current_balance + amount
    elif operation == "withdraw":
        new_balance = current_balance - amount
    else:
        print("invalid operation - has to be deposit or withdraw")

    cur = con.cursor()
    cur.execute(
        "UPDATE user_info SET balance =? WHERE account_number=?",
        (new_balance, account_number),
    )
    con.commit()
    print(f"updated current_balance: {current_balance} to new_balance: {new_balance} for account number : {account_number}")
    con.close()


def withdrawal_operation(valid_account):
    print("withdrawal")
    # get current balance
    account_details = is_account_number_valid(db_connect(), valid_account[0])
    current_balance = account_details[4]
    print(f"Your current balance is $ {current_balance}")
    # get amount to withdraw
    withdraw_amount = int(input("How much you want to withdraw from your account ?\n"))
    # check if current balance > withdraw balance
    # deduct withdrawn amount form current balance
    # display current balance
    if current_balance >= withdraw_amount:
        update_database(db_connect(), account_details, withdraw_amount,"withdraw")
        print(f"Thank you for withdrawing {withdraw_amount}")
        print(f"Your current balance is :{current_balance - withdraw_amount}")
        bank_operation(valid_account)
    else:
        print(
            f"Sorry, you cant withdraw more money than you have in your account. You have {current_balance}."
        )
        bank_operation(valid_account)
    # deduct withdrawn amount form current balance
    # display current balance


def deposit_operation(valid_account):
    print("Deposit Operations")
    # get current balance
    account_details = is_account_number_valid(db_connect(), valid_account[0])
    current_balance = account_details[4]
    print(f"Your current balance is $ {current_balance}")
    # get amount to deposit
    deposit_amount = int(input("How much you want to deposit in your account ?\n"))
    # add deposited amount to current balance
    # display current balance
    update_database(db_connect(), account_details, deposit_amount, "deposit")
    print(f"Thank you for depositing  {deposit_amount}")
    print(f"Your NEW balance is :{current_balance + deposit_amount}")
    bank_operation(valid_account)


def logout():
    print("You are successfully logged out")
    login()

# Run the init function
init()
