import sqlite3

#open the database and set the cursor ready for use
try:
    db = sqlite3.connect('data/ebookstore_db')
    cursor = db.cursor()
    # if a table does not already exist then make one
    cursor.execute('''CREATE TABLE IF NOT EXISTS books(
        ID VARCHAR(4) PRIMARY KEY NOT NULL, 
        TITLE VARCHAR(25) NOT NULL, 
        AUTHOR VARCHAR(15), 
        QTY INTEGER(2))
        ''')
    db.commit
# if the database is not found then display an error
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close


def add_book():
    '''Add book allows the user to input new information about an item
    and add the item to the datebase. criteria are fullfilled through 
    a series of questions put to the user and the information is then
    implimented in an INSERT function to add the new data to the database
    '''
    # information for each field is requested from the user
    stock_id = input('Please enter the stock ID for new entry:\n').lower()
    book_title = input('Please enter the book Title:\n').lower()
    author = input("Please enter the Author:\n").lower()
    stock_on_hand = int(input('Please state the amount of copies to add:\n'))
    # new information is then commited to the database using sqlite3 INSERT
    # the values are taken from the previously input data.
    cursor.execute('''INSERT INTO books(ID,TITLE,AUTHOR,QTY)
    VALUES(?,?,?,?)''',(stock_id,book_title,author,stock_on_hand))
    db.commit()
    # confirm success to user
    return print("\n- NEW ITEM SUCCESSFULLY ADDED -\n")

def update_info():
    '''Update info allows the user to change the value in a 
    certain feild for a particualar entry
    The user is asked to input the code of the book they wish 
    to update and is shown their selection for confirmation. 
    A follow up question
    is asked as to which field they wish to update.
    New information is then gathered through the user interface 
    and the appropriate field is then updated via the UPDATE sqlite3 function.
    '''
    # the user is asked to identify the book to update
    book_to_update = input(
        "Please enter the Unique code of the book you wish to update.\n"
        +"(If you do not know the code type 'not known' to search records - "
        +"You must restart the update process after search):").lower()
    # if the ID is not know the user is promted to search for the ID and start
    # again. this is to ensure the correct item is updated
    if book_to_update == 'not known':
        search_book()
    else:
        # the books details are shown to the user for confirmation
        cursor.execute('''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?''',(book_to_update,))
        data = cursor.fetchall()
        for row in data:
            print("\n- BOOK FOUND - \n")
            print(f"ID:{row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"QTY: {row[3]}")
        # user is then asked to specify the feild to be updated
        selection_pending = True
        while selection_pending:
            field_to_update = input("\nPlease enter the field you wish to update.\n"
                +"ID - to update ID code.\n"
                +"Title - to change a books title.\n"
                +"Author - to change the Author.\n"
                +"QTY - to update stock quantities.\n"
                +"Type Selection here: "
                ).upper()
            # after a field has been selected the user is asked for 
            # the new information and the book is updated using UPDATE
            if field_to_update == 'ID':
                update_critera = input(
                    "Please enter the new unique ID code for this book:\n")
                cursor.execute(
                    '''UPDATE books SET ID = ? WHERE ID = ?''',
                    (update_critera,book_to_update,))
                db.commit
                selection_pending = False

            elif field_to_update == 'TITLE':
                update_critera = input(
                    "Please enter the updated title for this book:\n")
                cursor.execute('''UPDATE books SET TITLE = ? WHERE ID = ?''',
                (update_critera,book_to_update,))
                db.commit
                selection_pending = False

            elif field_to_update == 'AUTHOR':
                update_critera = input(
                    "Please type the updated author name:\n")
                cursor.execute('''UPDATE books SET AUTHOR = ? WHERE ID = ?''',
                (update_critera,book_to_update,))
                db.commit
                selection_pending = False

            elif field_to_update == 'QTY':
                update_critera = input(
                    "Please enter the new total stock quantitiy:\n")
                cursor.execute('''UPDATE books SET QTY = ? WHERE ID = ?''',
                (update_critera,book_to_update))
                db.commit
                selection_pending = False
            # if the user makes a mistake on the field entry 
            # they will be asked again
            else:
                print("That request was not recognised please try again")
    # confirm success to user
    return print("\n - UPDATE SUCCESSFUL - \n")
        



def delete_book():
    '''delete book allows the user to remove an entry from the database
    The user is asked to enter the code of the book they wish to delete.
    The user is then shown the full entry for this book 
    and asked to confirm if they wish to delete this item
    '''
    # the user is asked to identify the book for deletion
    selection_pending = True
    while selection_pending:
        entry_to_remove = input(
            "Please enter the ID code for the book you with to remove.\n"
            +"(If you do not know the code for this book type"
            +" 'not known' to search by title.):\n").lower()
        # if the user does not know the code they can search by title
        if entry_to_remove == 'not known':
            entry_to_remove = input(
                "Please enter the Title of the book you wish to remove:\n"
                ).lower()
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE TITLE = ?''',
            (entry_to_remove,))
            data = cursor.fetchall()
            # the book is shown to the user for confirmation
            for row in data:
                print("\n")
                print(f"ID:{row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"QTY: {row[3]}")
            # user is warned of commitment
            correct_entry = input("Delete this item?(cannot be undone)"
            +"Type yes to delete:\n").lower()

            if correct_entry =='yes':
                # book id is saved and DELETE function is executed
                book_id = row[0]
                selection_pending = False 
            # if the user does not type yes they are taken back to the 
            # main menu
            else:
                return print("\n- RETURNING TO MAIN MENU -\n")
        # if the user knows the id of the book 
        # the book details are shown for confirmation
        else:
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?''',
                (entry_to_remove,))
            data = cursor.fetchall()
            for row in data:
                print("\n")
                print(f"ID:{row[0]}")
                print(f"Title: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"QTY: {row[3]}")
            # a warning is displayed
            correct_entry = input(
                "\nDelete this item?(cannot be undone)"
                +"Type yes to delete:\n").lower()

            if correct_entry =='yes':
                # book id is saved and DELETE function is executed
                book_id = row[0]
                selection_pending = False
            else:
                return print("\n- RETURNING TO MAIN MENU - \n")
    # delete entry using prepared book_id info
    cursor.execute('''DELETE FROM books WHERE ID = ?''',(book_id,))
    # commit the update
    db.commit
    # confim success to user
    return print("\n- ITEM REMOVED FROM RECORDS -\n")

def search_book():
    '''Search allows the user to search based on a chosen criteria.
    the search results will show all items that have associate feilds
    for example if the user chooses to search by author,
    all books written by the search author will be displayed, 
    however if the user chooses to search by code
    then only the book with that code will be displayed. 
    '''
    # user is first ask how they wish to search the database
    selection_pending = True
    while selection_pending:
        search_object = input(
            "Please enter the method with which you wish to search.\n"
            +"ID - to search by ID code.\n"
            +"Title - to search by book title.\n"
            +"Author - to search by Author.\n"
            +"Type Selection here: "
            ).upper()
        # each selection option will activate a particular method
        # based on the search criteria
        if search_object == 'ID':
            # the user is asked for the relevant info
            search_critera = input(
                "Please enter the unique ID"
                +"code for the book you wish to search:\n")
            # this info is then used in a SELECT function to retrieve
            # the other information associated with this item
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE ID = ?'''
                ,(search_critera,))
            # the infomation is saved in data
            data = cursor.fetchall()
            selection_pending = False

        elif search_object == 'TITLE':
            search_critera = input("Please enter the Title of the book you "
            +"wish to search for:\n")
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE TITLE = ?'''
                ,(search_critera,))
            data = cursor.fetchall()
            selection_pending = False

        elif search_object == 'AUTHOR':
            search_critera = input("Please type the name of the Author:\n")
            cursor.execute(
                '''SELECT ID,TITLE,AUTHOR,QTY FROM books WHERE AUTHOR = ?'''
                ,(search_critera,))
            data = cursor.fetchall()
            selection_pending = False

        else:
            print("That request was not recognised please try again")
            selection_pending = True
    # the data variable is then used to iterate thrgouh to present the 
    #information to the user
    for row in data:
        print('\n')
        print(f"ID:{row[0]}")
        print(f"Title: {row[1]}")
        print(f"Author: {row[2]}")
        print(f"QTY: {row[3]}")
        print('\n')
    # a confirmation is returned to advise the user
    # that all records have been displayed. if no records are found
    # the console will only display this message.
    return print('\n- END OF RECORDS -\n')

def view_all():
    cursor.execute('''SELECT ID,TITLE,AUTHOR,QTY FROM books''')
    for row in cursor:
            print("\n- ----- - \n")
            print(f"ID:{row[0]}")
            print(f"Title: {row[1]}")
            print(f"Author: {row[2]}")
            print(f"QTY: {row[3]}")

#==========Main Menu=============
# username : admin
# password : adm1n

username_required = True
password_required = True
# open a loop for authenticating the username using username_required booleon
while username_required:
    with open('user.txt', 'r') as users:
        username = input("Please enter a valid username:\n")
        for lines in users:
            # I chose not to use a list here because I dont want
            # to create a passwords list aswell and store it
            # inside the active program. i just want to take
            # the password that is needed.
            # if a match is found
            if username in lines:
                    print('User confirmed')
                    username_required = False
                    # once a valid username is entered
                    # a username is no longer required
                    # the password for this user will always be 
                    # the next word on the same line.
                    # save the password using a split and an integer selection
                    true_password = [lines.split()[1]]
# once the username loop is closed a password is requested
# entered password must match true_password exactly
# start a loop for password authentiacation
while password_required:
    password = input("Please enter your password:\n")
    if password in true_password:  # if the password matches true_password
        print("\n- Login Successful. -")
        # once the correct password is entered 
        # password_required becomes false and closes the loop
        # login success becomes true
        password_required = False
        login_success = True
    # or else keep asking for password
    else:
        print("Password is incorrect, Please try again.")

# once login sequence has been completed the menu is presented to the user
while login_success:
    menu = input('''Select one of the following:

    add - Add new items to inventory
    update - Update a books record
    search - Search for an item
    delete - Delete an item from invetory
    view - View all Database entries
    exit - Exit

    Type Selection here: ''').lower()

    if menu == "add":
        add_book()

    elif menu == "update":
        update_info()
    
    elif menu == "search":
        search_book()

    elif menu == "delete":
        delete_book()

    elif menu == "view":
        view_all()
    
    elif menu == "exit":
        print("GOODBYE")
        exit()

    else:
        print("\n- Entry not recognised, Please Try again. -")