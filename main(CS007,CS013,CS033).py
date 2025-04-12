import datetime
from abc import ABC, abstractmethod

class ViewCart(ABC):  #Abstract class and method
    @abstractmethod
    def view_cart(self):
        pass

class Inventory_Manager:
    """
    Displays The Product list, Stock and manages products
    """
    def __init__(self):
        self.brand_name = "AFA"            #Define brand name
        self.phones = {}                   #Initialize an empty dictionary
        self.phones_file = "phones.txt"    #Define the file name
        self.stock_file = "stock.txt"      #Define the file name
        self.stock={}                      #Initialize empty dictionary
        self.load_phones_from_file()      #populate the phone dictionary
        self.load_stock_from_file()       #populate the stock file

    def load_phones_from_file(self):
        """
        Load phone data from a text file and populate the phones dictionary.
        """
        try:
            with open(self.phones_file, 'r') as file:
                file.seek(0)
                for line in file:
                    name, price = line.strip().split(',')
                    self.phones[name] = eval(price)  
        #Incase file not found or isnt in the right directory
        except FileNotFoundError:  
            print("Phone data file not found.")
    
    def load_stock_from_file(self):
        """
        Load available stock from a text file and populate the stock dictionary.
        """
        try:
            with open(self.stock_file, 'r') as file:
                file.seek(0)
                for line in file:
                    name, stock = line.strip().split(',')
                    self.stock[name] = int(stock)  # Assuming stock is an integer
        #Incase file not found or isnt in the right directory
        except FileNotFoundError:  
            print("Stock data file not found.")
        
    def save_phones(self):
        """
        Save/update the current phones to the file
        """
        with open(self.phones_file, 'w') as file:
            for phone, price in self.phones.items():
                file.write(f"{phone},{price}\n")
    
    def update_stock(self):
        """
        Update the stock to the file
        """
        with open(self.stock_file, 'w') as file:
            for phone, stock in self.stock.items():
                file.write(f"{phone},{stock}\n")

    def display_phones(self):
        """
        Displays phones in a formatted manner.
        """
        print('\n==================================================\nAVAILABLE PHONES\n==================================================')
        print(f"{'Name':<29} | {'Price':<15}")
        print('----------------------------------------')
        count = 1
        for phone, price in self.phones.items():
            print(f'{count:<3} - {phone:<23} | ${price:<10}')
            count += 1
        print()
    
    def display_stock(self):
        """
        Displays stock in a formatted manner.
        """
        print('\n==================================================\nAVAILABLE STOCK\n==================================================')
        print(f"{'Name':<29} | {'In Stock':<15}")
        print('------------------------------------------')
        count = 1
        for phone, stock in self.stock.items():
            print(f'{count:<3} - {phone:<23} | {stock:<10}')
            count += 1
        print()

    def add_product(self):  # For Admin Use only
        """
        Adds a new phone to the product list.
        """
        while True:
            product_name = input("Enter the name of the phone (without the brand name): ").strip().title()
            # Check if the product name contains the brand name
            if self.brand_name.lower() in product_name.lower().split():
                print(f"Please do not include the brand name '{self.brand_name}' in the product name!\n")
                continue
            # Ensure the product name is alphabetic, not numeric, and not already in the list
            product_full_name = f'{self.brand_name} {product_name}'
            if product_full_name not in self.phones:
                if not product_name.isdigit() and len(product_name) >= 4:
                    break
                else:
                    print("Please enter a valid phone name that is longer than 3 characters and not numeric!")
            else:
                print(f'{product_full_name} already exists.')

        while True:
            price = input(f'Enter the price for {product_full_name}: ').strip()
            try:
                if isinstance(eval(price),int) or isinstance(eval(price),float):  #Ensuring entered price is a integer or float
                    break
            except:
                print("Invalid entry!")
                
        self.phones[product_full_name] = price
        self.stock[product_full_name] = 100
        self.save_phones()  #Update the product list
        self.update_stock()  #Update the new product in stock
        print(f'\nProduct {product_full_name} added successfully with a price of ${price}.\n')

    def remove_product(self):  # For Admin Use only
        """
        Removes a phone from the product list.
        """

        if not self.phones: #if no products available or file didn't load properly
            print("No products available to remove.")
            return

        self.display_phones()  #display products
        while True:
            product_name = input("Enter the name of the phone to remove (without brand name): ").strip().title()
            # Check if the product name contains the brand name
            if self.brand_name.lower() in product_name.lower().split():
                print(f"Please do not include the brand name '{self.brand_name}' in the product name!\n")
                continue
            else:
                product_full_name = f'{self.brand_name} {product_name}'
            if product_full_name in self.phones:
                del self.phones[product_full_name]
                del self.stock[product_full_name]
                self.save_phones()  #Update the product list
                self.update_stock()  #Update the stock 
                print(f'\nProduct {product_full_name} removed successfully.\n')
                break
            else:
                print("Product not found. Please enter a valid product name.")
    
    def change_stock(self):  #For Admin Use Only
        """
        Increase or decrease the available stock of phones
        """
        self.display_stock()
        while True:
            product_name = input("Enter the name of the phone to update stock of (without brand name): ").strip().title()
            # Check if the product name contains the brand name
            if self.brand_name.lower() in product_name.lower().split():
                print(f"Please do not include the brand name '{self.brand_name}' in the product name!\n")
                continue
            else:
                product_full_name = f'{self.brand_name} {product_name}'
                break
        if product_full_name in self.stock:
            while True:
                option = input(
                    'Would you like to add or remove stock?\n'
                    'Press "a" to add or "r" to remove: ').strip()
                if option.lower() == 'a':
                    while True:
                        quantity = input(f'Enter the quantity of stock for {product_full_name}: ').strip()
                        print()
                        if quantity.isdigit():
                            quantity = int(quantity)
                            self.stock[product_full_name]+=quantity
                            print(f"Successfully added {quantity} phone/phones to {product_full_name}'s stock\n")
                            self.update_stock()
                            break
                        else:
                            print("Please enter a valid quantity (Integer numeric value)!")
                            print()
                    break #break out of the loop after removing successfully
                        
                elif option.lower()== 'r':
                    while True:
                        quantity = input(f'Enter the quantity of stock you want to remove of {product_full_name}: ').strip()
                        if quantity.isdigit():
                            if int(quantity)<=self.stock[product_full_name]:
                                quantity = int(quantity)
                                self.stock[product_full_name]-=quantity
                                print(f"Successfully removed {quantity} phone/phones from {product_full_name}'s stock\n")
                                self.update_stock()
                                break
                            else:
                                print("Stock cannot be negative!\n")
                        else:
                            print("Please enter a valid quantity (Integer numeric value)!\n")
                            print()
                    break  #break out of the loop after removing successfully
                else:
                    print('Invalid option! Please press "a" to add or "r" to remove.')
        else:
            print("Product not found. Please enter a valid product name.\n")
                
class User:
    """
    Handles user login and account creation.
    """
    current_user = ''
    user_data_file = 'user_data.txt'
    delimiter = ','

    def __init__(self, username=None, password=None, first_name=None, last_name=None, phone=None, address=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.shopping_history = {}


    def login_page(self):
        """
        Displays the login page and handles user login or account creation.
        """
        while True:
            print('\n\t\033[4m Welcome to Login Page\033[0m\n')  # Underlining
            print('\t1. Create account\n\t2. Login into an existing account')  # Aligned options
            choice = input('\tEnter choice number (1 or 2): ')
            if choice == '1':
                self.create_account()
            elif choice == '2':
                User.current_user = self.login()
                if User.current_user:
                    break  # Exit the loop if login is successful
            else:
                print('\nInvalid choice!')

    def create_account(self):
        """
        Creates a new user account
        """
        while True:
            username = input("Enter your username: ").strip()
            if self._username_exists(username) or username=="Admin":
                print("\nUsername already exists. Please choose a different username.\n")
            else:
                if (username.isalnum() or username.isascii()) and len(username)>3:
                    break
                else:
                    print("Please input a valid username having more than 3 characters")

        while True:
            while True:
                pswd = input("Enter your password: ").strip()
                if len(pswd) < 5:
                    print("Password requires a minimum of 5 characters")
                else:
                    break
            while True:
                first_name = input("Enter your first name: ").strip()
                if not first_name.isalpha():
                    print("Please enter correct info")
                else:
                    break
            while True:
                last_name = input("Enter your last name: ").strip()
                if not last_name.isalpha():
                    print("Please enter correct info")
                else:
                    break
            address = input("Enter your address: ").strip()
            if pswd and first_name and last_name and address:
                break
            else:
                print("\nEntering required information is mandatory!\n")

        while True:
            phone = input('Enter your phone number: ').strip()
            if len(phone) == 11 and phone.isdigit():
                print("\nAccount created successfully\n")
                break
            else:
                print('\nPhone number must be of 11 digits with no special characters\n')

        self.username = username
        self.password = pswd
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address

        self._save_user_data() #Save all of the data entered in file

    def login(self):
        """
        Authenticates the user
        """
        username_input = input('Enter username: ').strip()
        password_input = input('Enter password: ').strip()
        if self._authenticate_user(username_input, password_input):
            self.username = username_input

            print(f'\nLogin successful, Welcome {self.username}!')
            return username_input
        else:
            print('\nInvalid username or password!')
            return False

    def _username_exists(self, username):
        """
        Checks from stored data if same username already exists
        """
        try:
            with open(self.user_data_file, mode='r') as file:
                for line in file:
                    stored_username, _, _, _, _, _ = line.strip().split(self.delimiter)
                    if stored_username == username:
                        return True
            return False
        except FileNotFoundError:
            return False

    def _save_user_data(self):
        """
        Saves user info in a text file
        """
        with open(self.user_data_file, mode='a') as file:
            file.write(self.delimiter.join(
                [self.username, self.password, self.first_name, self.last_name, self.phone, self.address]) + '\n')

    def _authenticate_user(self, username, password):
        """
        Checks if the entered username and password match up
        """
        if username == 'Admin' and password == "admin":  # Special admin access authentication
            self.load_shopping_history()
            return True
        try:
            with open(self.user_data_file, mode='r') as file:
                for line in file:
                    stored_username, stored_password, _, _, _, _ = line.strip().split(self.delimiter)
                    if stored_username == username and stored_password == password:
                        self.load_shopping_history()
                        return True
            return False
        except FileNotFoundError:
            return False

    def load_shopping_history(self):
        """
        Fetch and load the history of the user.
        """
        try:
            with open('shopping_history.txt', 'r') as shopping_history_file:
                lines = shopping_history_file.readlines()
                self.shopping_history = {}
                for line in lines:
                    parts = line.strip().split(';')
                    if len(parts) == 2:
                        username, transaction_str = parts
                        try:
                            transaction_dict = eval(transaction_str) 
                        except:
                            continue
                        if username not in self.shopping_history:
                            self.shopping_history[username] = []
                        self.shopping_history[username].append(transaction_dict)
        except FileNotFoundError:
            self.shopping_history = {}

class AddToCart:
    """
    Adds product to cart
    """
    
    def __init__(self, cart, phones, stock, method):
        self.cart = cart         #User's cart
        self.phones = phones     #The phones dictionary
        self.stock = stock       #The stock dictionary
        self.update = method     #The update stock method

    def add_to_cart(self, serial_num):
        try:
            # Get the list of phones and the selected phone
            self.phone_lst = list(self.phones.keys())
            selected_phone = self.phone_lst[serial_num - 1]
            self.available = self.stock[selected_phone]
            if self.available==0:
                print(f'{selected_phone} is currently out of stock\nNew stock arriving soon')
            else:
                if selected_phone in self.phones:
                    quantity = input(f'Enter quantity for {selected_phone}, In stock {self.available}: ').strip()
                    if quantity.isdigit() and int(quantity) > 0 and int(quantity)<=self.available:
                        quantity = int(quantity)
                        self.cart[selected_phone] = self.cart.get(selected_phone, 0) + quantity
                        print(f'\n{quantity} {selected_phone}(s) added to your cart')
                        self.stock[selected_phone] = int(self.available-quantity)
                        self.update()
                    else:
                        print("\nEnter a valid integer greater than 0 and within the available amount of stock!")
                else:
                    print('\nInvalid phone, please try again!')
        except IndexError:
            print('\nInvalid serial number, please try again!')
        except Exception as e:
            print(f'\nAn error occurred: {e}')
        input("\nEnter any key to continue...")

class RemoveFromCart:
    """
    Removes product from cart
    """
    def __init__(self, cart, phones, stock, method):
        self.cart = cart      #User's cart
        self.phones = phones  #The phones dictionary
        self.stock= stock     #The stock dictionary
        self.update= method   #The update stock method

    def remove_from_cart(self):
        self.phone_lst = list(self.phones.keys())  #storing all phone names in list
        while True:
            #Displaying cart in a proper format
            print('\n==================================================\nYour Cart\n==================================================')
            if not self.cart:
                print("Your cart is empty!")
                input("\nEnter any key to continue....")
                break
            temp={}
            for idx, (phone, quantity) in enumerate(self.cart.items(), start=1):
                serial_number = self.phone_lst.index(phone) + 1
                print(f'{idx}. {quantity} {phone} (Serial Number: {serial_number})')
                temp[phone]= quantity
                self.available=self.stock[phone] #stock of selected phone
            rem_choice = input(
                '\n* Enter the serial number(1,2,3..) of the phone you wish to remove\n'
                '* Type "del" to empty your cart\n'
                '* Type "e" to exit remove cart \nYour choice: ').strip()

            if rem_choice.lower() == "e":
                break
            elif rem_choice.lower() == "del":
                print("\n* Your cart is now empty")
                for i in temp:
                    self.stock[i] += temp[i]  #Re-adding the removed products back to stock
                self.cart.clear()
                self.update()
                break
            else:
                try:
                    rem_choice_int = int(rem_choice)
                    if 1 <= rem_choice_int <= len(self.phone_lst):
                        selected_phone = self.phone_lst[rem_choice_int - 1]
                        if selected_phone in self.cart:
                            qnty = input(f'Enter the number of {selected_phone} you want to remove: ').strip()
                            if qnty.isdigit():
                                qnty = int(qnty)
                                if qnty > self.cart[selected_phone]:
                                    print("\nYou can't remove more than what you have")
                                else:
                                    self.cart[selected_phone] -= qnty
                                    self.stock[selected_phone] += qnty
                                    if self.cart[selected_phone] == 0:
                                        del self.cart[selected_phone]
                                    print(f'{qnty} {selected_phone}(s) removed from your cart')
                                    self.update()
                            else:
                                print("\nEnter a valid integer!")
                        else:
                            print(f"\nYou don't have {selected_phone} in your cart")
                    else:
                        print("\nInvalid serial number!")
                except ValueError:
                    print("\nInvalid choice! Please enter a valid serial number or command.")
            
            #exit prompt
            exit_choice = input("\nDo you want to exit remove cart? (y/n): ").strip().lower()
            if exit_choice == "y":
                break
            elif exit_choice != "n":
                print("\nInvalid Choice! \nExiting remove cart")
                break

class ShowHistory:
    """
    Shows the shopping history
    """
    def __init__(self, shopping_history, current_user):
        self.shopping_history = shopping_history
        self.current_user = current_user

    def show_history(self):
        if self.current_user in self.shopping_history and self.shopping_history[self.current_user]:
            print(f'\nShopping history for {self.current_user}:')

            # Sort transactions by timestamp in descending order
            sorted_transactions = sorted(self.shopping_history[self.current_user], key=lambda x: x['timestamp'], reverse=True)

            for entry in sorted_transactions:
                try:
                    print()
                    print(f"Timestamp: {entry['timestamp']}")
                    print('Items:')
                    for item in entry['items']:
                        print(f"{item['quantity']} {item['phone']} - ${item['item_amount']:.2f}")
                    print(f'Total Amount: ${entry["total_amount"]:.2f}')
                    print(f'Final amount: ${entry["final_amount"]:.2f}')
                    promo_code = entry.get('promo_code', 'N/A')
                    print(f'Promo Code: {promo_code}')
                    review = entry.get('review', 'No review')
                    print(f'Review: {review}')
                except KeyError as e:
                    print(f"Error: Missing expected data {e}")

            input("Press Enter to continue...")
        else:
            print(f'\n{self.current_user} has no shopping history currently.\n')
            input("Press Enter to continue...")

class Cart(ViewCart):
    """
    Manages the shopping cart
    """
    def __init__(self, user, inventory):
        self.user = user  #User type object
        self.inventory = inventory  
        self.cart = {}  #Initializing the cart
        self.shopping_history = self.user.shopping_history  # Use user's loaded shopping history
        print("Today's promo code is 'cis'")

    def choice(self):
        add_to_cart = AddToCart(self.cart, self.inventory.phones, self.inventory.stock, self.inventory.update_stock)
        remove_from_cart = RemoveFromCart(self.cart, self.inventory.phones, self.inventory.stock, self.inventory.update_stock)
        show_history = ShowHistory(self.shopping_history, self.user.username)
    
        while True:
            self.inventory.display_phones()  # Display the phones
            serial_num = input(
                '* Enter the serial number (1,2,3..) of the phone you want to buy:\n'
                '* Enter "view" to view your cart:\n'
                '* Enter "rem" to remove item from your cart\n'
                '* Enter "done" to checkout\n'
                '* Enter "history" to view past shopping history\nYour choice: ').strip()

            if serial_num.lower() == 'view':
                self.view_cart()
            elif serial_num.lower() == 'rem':
                remove_from_cart.remove_from_cart()
            elif serial_num.lower() == 'history':
                show_history.show_history()
            elif serial_num.lower() == 'done':
                checkout = CheckOut(self.user.username, self.shopping_history, self.cart, self.inventory.phones)
                checkout.checkout()
                break
            else:
                try:
                    # Check if the input is a valid integer
                    serial_num_int = int(serial_num)
                    if 1 <= serial_num_int <= len(self.inventory.phones):
                        add_to_cart.add_to_cart(serial_num_int)
                    else:
                        print('Enter a valid serial number within the range.')
                except ValueError:
                    print('Enter a valid choice.')
                    input("Enter any key to continue...")

    def view_cart(self):
        """
        Displays the contents of the shopping cart.
        """
        print('\n==================================================\nYour Cart\n==================================================')
        print(f"{'Name':<26} | {'Quantity':<10} | {'Price':<15}")
        print('--------------------------------------------------')
        count = 1
        total=0
        for phone, quantity in self.cart.items():
            if quantity>0:
                print(f'{count:<3} - {phone:<20} | {quantity:<10} | ${self.inventory.phones[phone]*quantity}')
                count += 1
                total+=self.inventory.phones[phone]*quantity
        print()
        print(f'Total bill: ${total}')
        if not self.cart:
            print("Your cart is empty!")
        print()
        input("Enter any key to continue... ")
        
class CheckOut:
    """
    Handles the checkout process.
    """
    def __init__(self, username, shopping_history,cart, phones):
        self.current_user = username                 #Username of current user
        self.shopping_history = shopping_history     #user's loaded shopping history
        self.cart=cart                               #User's cart
        self.phones= phones                          #The phone dictionary
        if self.current_user not in self.shopping_history:
            self.shopping_history[self.current_user] = []  

        self.update_shopping_history() 

    def update_shopping_history(self):
        total_amount = 0  # Initialize total amount
        items_in_cart = []

        for phone, quantity in self.cart.items():
            if quantity > 0:
                item_amount = quantity * self.phones[phone]
                print(f'{phone:<30} | {quantity:<10} | ${item_amount}')
                total_amount += item_amount
                items_in_cart.append({'phone': phone, 'quantity': quantity, 'item_amount': item_amount})

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.shopping_history[self.current_user].append({'timestamp': timestamp, 'items': items_in_cart, 'total_amount': total_amount})

    def get_last_transaction(self):
        if self.shopping_history[self.current_user]:
            return self.shopping_history[self.current_user][-1]
        else:
            return {'timestamp': 'N/A', 'items': [], 'total_amount': 'N/A'}

    def apply_promo_code(self, total_amount, promo_code):
        if promo_code.lower() == "cis":
            discount = 0.10  # 10% discount for the promo code "cis"
            discounted_amount = total_amount * (1 - discount)
            saved_amount = total_amount - discounted_amount  # Calculate the amount saved
            print(f'10% Discount applied! You saved: ${saved_amount:.2f}')
            print(f'Total Amount after discount: ${discounted_amount:.2f}')
            return discounted_amount
        return total_amount

    def print_last_transaction(self, last_transaction):
        initial_amount = last_transaction.get("total_amount", "N/A")
        discounted_amount = last_transaction.get("discounted_amount", "N/A")
        saved_amount = initial_amount - discounted_amount if initial_amount != "N/A" and discounted_amount != "N/A" else "N/A"

        print(f'\nShopping history for {self.current_user} (Last Transaction):')
        print(f"Timestamp: {last_transaction['timestamp']}")
        print('Items:')
        for item in last_transaction['items']:
            print(f"{item['quantity']} {item['phone']} - ${item['item_amount']:.2f}")
        print(f'Initial Amount: ${initial_amount}')
        print(f'Final Amount: ${discounted_amount}')
        if saved_amount != "N/A":
            print(f'Saved Amount: ${round(saved_amount, 2)}')
        else:
            print('Saved Amount: N/A')
        print()  # for aesthetic purposes

    def leave_review(self, last_transaction):
        review_choice = input('Do you want to leave a review on our products (y/n): ')
        if review_choice.lower() == 'y':
            review = input('Your Review: ')
            last_transaction['review'] = review
            self.save_shopping_history()
            print('\n\t Hope you Liked our shopping marvel :)')
        else:
            self.save_shopping_history()
            print('\n\t Hope you Liked our shopping marvel :)\n')

    def checkout(self):
        self.last_transaction = self.get_last_transaction()
        total_amount = self.last_transaction.get("total_amount", "N/A")
        if total_amount>0:
            promo_code = input("Do you have a promo code? Enter it here (or press Enter to skip): ").strip()
            total_amount = self.apply_promo_code(total_amount, promo_code)

            self.last_transaction['promo_code'] = promo_code
            self.last_transaction['discounted_amount'] = total_amount

        self.print_last_transaction(self.last_transaction)
        self.leave_review(self.last_transaction)

    def save_shopping_history(self):
        with open('shopping_history.txt', 'a+') as shopping_history_file:
            timestamp = self.last_transaction['timestamp']
            items = self.last_transaction['items']
            total_amount = self.last_transaction['total_amount']
            promo_code = self.last_transaction.get('promo_code', 'N/A')
            review = self.last_transaction.get('review', 'N/A')
            
            if promo_code:
                discount = 0.10  # 10% discount for the promo code "cis"
                final_amount = total_amount * (1 - discount)
            else:
                final_amount = self.last_transaction.get('final_amount', total_amount)

            if final_amount>0:
            
            # Convert items to a string for saving
                items_str = ', '.join([f"{{'phone': '{item['phone']}', 'quantity': {item['quantity']}, 'item_amount': {item['item_amount']}}}" for item in items])

                # Write the transaction details to the file
                shopping_history_file.write(f"{self.current_user};{{'timestamp': '{timestamp}', 'items': [{items_str}], 'total_amount': {total_amount}, 'promo_code': '{promo_code}', 'final_amount': {final_amount}, 'review': '{review}'}}\n")

class Admin(User):
    """
    Admin Access features

    """
    def __str__(self) : #method overriding
        return "\t\033[4m ADMIN PANEL \033[0m\n"

    def admin_panel(self):
        """
        Displays the Admin page and handles functions related to it
        """
        inventory = Inventory_Manager()
        while True:
            option = input(
                '* Enter "users" to view all users\n'
                '* Enter "update" to update the stock\n'
                '* Enter "view" to view the product list or available stock\n'
                '* Enter "add" to add products\n'
                '* Enter "rem" to remove products\n'
                '* Enter "done" to logout\nYour choice: ').strip()
            
            if option.lower() == 'users':
                self.__view_users()
            elif option.lower() == 'update':
                inventory.change_stock()
            elif option.lower() == 'view':
                while True:
                    choice= input('\nEnter "p" to view phones or "s" to view available stock\nYour choice: ').strip()
                    if choice.lower()== "p":
                        inventory.display_phones()
                        break
                    elif choice.lower()== "s":
                        inventory.display_stock()
                        break
                    else:
                        print("Please enter valid option!")
            elif option.lower() == 'add':
                inventory.add_product()
            elif option.lower() == 'rem':
                inventory.remove_product()
            elif option.lower() == 'done':
                inventory.save_phones()
                inventory.load_phones_from_file()
                print("\nLogging out...\n")
                break
            else:
                print("Enter a valid choice!\n")

    def __view_users(self):
        """
        Private method to view user database
        """
        try:
            with open(self.user_data_file, mode='r') as file:
                print('\n==================================================\nALL USERS\n==================================================')
                for line in file:
                    stored_username, _, stored_first_name, stored_last_name, stored_phone, stored_address = line.strip().split(self.delimiter)
                    print(f'Username: {stored_username}, Name: {stored_first_name} {stored_last_name}, Phone: {stored_phone}, Address: {stored_address}\n')
        except FileNotFoundError:
            print('No user data found.\n')

#Client Code
def main():
    print('\t\U0001F30CWelcome to AFA Accessories\n\tGood service is our utmost priority!\U0001F30C\n\t')

    inventory = Inventory_Manager()  # Initialize Inventory_Manager and User instances
    user= User()

    while True:
        print("\t\t\033[4m MAIN MENU \033[0m")
        print("\t1. Enter The Application")
        print("\t2. Exit")
        choice = input("\tEnter your choice (1 or 2): ").strip()
        
        if choice == '1':
            # Recreating Inventory_Manager instance to reflect any changes made by admin
            inventory = Inventory_Manager()
            user.login_page()
            if User.current_user == 'Admin':
                admin = Admin()
                print(admin) #method overriding
                admin.admin_panel()
            else:
                cart = Cart(user, inventory)  #Aggregation
                cart.choice()
        elif choice == '2':
            print("\n Exiting application...")
            print("\n\t\U0001F30CThank you for visiting us! Come back again!\U0001F30C\n\tGood bye!\n")
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")

try:
    main()
except KeyboardInterrupt:
    print('\nProgram interrupted by User\nExiting...')
except Exception as e:
    print(f'\nAn unexpected error occurred: {e}\nExiting...')