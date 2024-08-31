import tkinter as tk
import mysql.connector as sql
import datetime as dt

# Function to show the welcome message using Tkinter
def show_welcome_message():
    root = tk.Tk()
    root.title("Welcome")

    # Set the window size
    root.geometry("400x200")

    # Create a label with the welcome message in blue color
    welcome_label = tk.Label(root, text="Welcome To London Bank", fg="blue", font=("Helvetica", 16), padx=20, pady=20)
    welcome_label.pack()

    # Add a button to close the window
    close_button = tk.Button(root, text="Continue", command=root.destroy, padx=10, pady=5)
    close_button.pack()

    # Run the GUI event loop
    root.mainloop()

# Database connection function
def connect_db():
    return sql.connect(host='localhost', user='root', passwd='root', database='Bank')

# Create tables if they don't exist
def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bank1_table (
            username VARCHAR(25) PRIMARY KEY,
            passwrd VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_details (
            acct_no INT PRIMARY KEY,
            acct_name VARCHAR(25),
            phone_no BIGINT CHECK(phone_no > 0),
            address VARCHAR(25),
            cr_amt FLOAT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bank2_table (
            acct_no INT,
            date DATE,
            withdrawal_amt BIGINT,
            amount_added BIGINT,
            FOREIGN KEY (acct_no) REFERENCES customer_details(acct_no)
        )
    ''')

# Function to register a user
def register_user(cursor, conn, username, password):
    cursor.execute('SELECT * FROM Bank1_table WHERE username = %s', (username,))
    if cursor.fetchone():
        print('Account already exists.')
        return
    
    cursor.execute('INSERT INTO Bank1_table (username, passwrd) VALUES (%s, %s)', (username, password))
    conn.commit()
    print('User created successfully!')

# Function to log in a user
def login_user(cursor, username, password):
    cursor.execute('SELECT * FROM Bank1_table WHERE username = %s AND passwrd = %s', (username, password))
    return cursor.fetchone() is not None

# Function to create a new bank account
def create_account(cursor, conn, acct_no, acct_name, phone_no, address, cr_amt):
    cursor.execute('''
        INSERT INTO customer_details (acct_no, acct_name, phone_no, address, cr_amt)
        VALUES (%s, %s, %s, %s, %s)
    ''', (acct_no, acct_name, phone_no, address, cr_amt))
    conn.commit()
    print('Account Created Successfully!')

# Function to perform transactions (deposit/withdrawal)
def perform_transaction(cursor, conn, acct_no, amount, transaction_type):
    cursor.execute('SELECT * FROM customer_details WHERE acct_no = %s', (acct_no,))
    if cursor.fetchone() is None:
        print('Account Number Invalid. Try Again Later.')
        return

    if transaction_type == 'withdraw':
        cursor.execute('UPDATE customer_details SET cr_amt = cr_amt - %s WHERE acct_no = %s', (amount, acct_no))
        cursor.execute('''
            INSERT INTO Bank2_table (acct_no, date, withdrawal_amt, amount_added)
            VALUES (%s, %s, %s, 0)
        ''', (acct_no, dt.datetime.today(), amount))
    elif transaction_type == 'deposit':
        cursor.execute('UPDATE customer_details SET cr_amt = cr_amt + %s WHERE acct_no = %s', (amount, acct_no))
        cursor.execute('''
            INSERT INTO Bank2_table (acct_no, date, withdrawal_amt, amount_added)
            VALUES (%s, %s, 0, %s)
        ''', (acct_no, dt.datetime.today(), amount))
    
    conn.commit()
    print('Account Updated Successfully!')

# Function to view customer details
def view_customer_details(cursor, acct_no):
    cursor.execute('SELECT * FROM customer_details WHERE acct_no = %s', (acct_no,))
    data = cursor.fetchone()
    if data:
        details = f'''
        ACCOUNT NO = {data[0]}
        ACCOUNT NAME = {data[1]}
        PHONE NUMBER = {data[2]}
        ADDRESS = {data[3]}
        CREDIT AMOUNT = {data[4]}
        '''
        print(details)
    else:
        print('Invalid Account Number.')

# Function to view transaction details
def view_transaction_details(cursor, acct_no):
    cursor.execute('SELECT * FROM Bank2_table WHERE acct_no = %s', (acct_no,))
    data = cursor.fetchall()
    if data:
        details = '\n'.join([f'''
        ACCOUNT NO = {row[0]}
        DATE = {row[1]}
        WITHDRAWAL AMOUNT = {row[2]}
        AMOUNT ADDED = {row[3]}
        ''' for row in data])
        print(details)
    else:
        print('No transactions found for this account.')

# Function to delete an account
def delete_account(cursor, conn, acct_no):
    cursor.execute('SELECT * FROM customer_details WHERE acct_no = %s', (acct_no,))
    if cursor.fetchone() is None:
        print('Account does not exist.')
        return

    cursor.execute('DELETE FROM Bank2_table WHERE acct_no = %s', (acct_no,))
    cursor.execute('DELETE FROM customer_details WHERE acct_no = %s', (acct_no,))
    conn.commit()
    print('Account Deleted Successfully!')

# Function to display the transaction menu
def transaction_menu(cursor, conn):
    while True:
        print()
        print('1.WITHDRAW AMOUNT')
        print('2.ADD AMOUNT')
        print()
        choice = int(input('Enter your CHOICE: '))

        if choice == 1:
            amt = float(input('Enter withdrawal amount: '))
            acct_no = int(input('Enter Your Account Number: '))
            perform_transaction(cursor, conn, acct_no, amt, 'withdraw')
        
        elif choice == 2:
            amt = float(input('Enter amount to be added: '))
            acct_no = int(input('Enter Your Account Number: '))
            perform_transaction(cursor, conn, acct_no, amt, 'deposit')
        
        else:
            print('Invalid choice. Please try again.')

        # Ask if the user wants to continue with transactions
        cont = input('Do you want to perform another transaction? (y/n): ').lower()
        if cont != 'y':
            break

# Function to display the terminal menu
def menu():
    conn = connect_db()
    cursor = conn.cursor()
    create_tables(cursor)

    while True:
        print()
        print('1.CREATE BANK ACCOUNT')
        print('2.TRANSACTION')
        print('3.CUSTOMER DETAILS')
        print('4.TRANSACTION DETAILS')
        print('5.DELETE ACCOUNT')
        print('6.QUIT')
        print()
        choice = int(input('Enter your CHOICE: '))

        if choice == 1:
            acct_no = int(input('Enter your ACCOUNT NUMBER: '))
            acct_name = input('Enter your ACCOUNT NAME: ')
            phone_no = int(input('Enter your PHONE NUMBER: '))
            address = input('Enter your ADDRESS: ')
            cr_amt = float(input('Enter your CREDIT AMOUNT: '))
            create_account(cursor, conn, acct_no, acct_name, phone_no, address, cr_amt)
        
        elif choice == 2:
            transaction_menu(cursor, conn)
        
        elif choice == 3:
            acct_no = int(input('Enter your ACCOUNT NUMBER: '))
            view_customer_details(cursor, acct_no)
        
        elif choice == 4:
            acct_no = int(input('Enter your ACCOUNT NUMBER: '))
            view_transaction_details(cursor, acct_no)
        
        elif choice == 5:
            acct_no = int(input('Enter your ACCOUNT NUMBER: '))
            delete_account(cursor, conn, acct_no)
        
        elif choice == 6:
            print('Thank you! Please visit again.')
            conn.close()
            break

        else:
            print('Invalid choice. Please try again.')

# Function to handle registration and login
def main():
    conn = connect_db()
    cursor = conn.cursor()
    create_tables(cursor)
    
    # Show welcome message
    show_welcome_message()
    
    while True:
        print()
        print('1. REGISTER')
        print('2. LOGIN')
        print()
        choice = int(input('Enter your choice: '))
        
        if choice == 1:
            username = input('Enter a Username: ')
            password = input('Enter a Password: ')
            register_user(cursor, conn, username, password)
        
        elif choice == 2:
            username = input('Enter your Username: ')
            password = input('Enter your Password: ')
            if login_user(cursor, username, password):
                print('Login successful!')
                menu()
                break
            else:
                print('Invalid Username or Password.')
        
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main()
