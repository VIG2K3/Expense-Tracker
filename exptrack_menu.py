from customtkinter import *
from tkinter import OptionMenu, ttk
from tkcalendar import DateEntry
import datetime
import tkinter.messagebox as mb
from PIL import Image
from winotify import Notification, audio
import sv_ttk
import hashlib
import sqlite3

# Database Connection
connector = sqlite3.connect("Expense Tracker ccc.db")
cursor1 = connector.cursor()
cursor2 = connector.cursor()
cursor3 = connector.cursor()
cursor10 = connector.cursor()

# Creating the Users table
cursor10.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        User_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        User_username VARCHAR UNIQUE NOT NULL,
        User_password VARCHAR NOT NULL
    )
''')

# Creating the Expenses table
cursor1.execute(
    'CREATE TABLE IF NOT EXISTS Expenses '
    '(ID_EXP INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'Date_EXP DATE, '
    'Payee VARCHAR(50), '
    'Note_EXP VARCHAR(100), '
    'Amount_EXP FLOAT, '
    'ModeOfPayment_EXP VARCHAR(20), '
    'Category_EXP VARCHAR(20),'
    'User_ID INTEGER,'
    'FOREIGN KEY (User_ID) REFERENCES Users(User_ID)'
    'CONSTRAINT unique_exp UNIQUE (Date_EXP, Note_EXP, User_ID))'
)

# Creating the Income table
cursor2.execute(
    'CREATE TABLE IF NOT EXISTS Income '
    '(ID_INC INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'Date_INC DATE, '
    'Payer_INC VARCHAR(50), '
    'Note_INC VARCHAR(100), '
    'Amount_INC FLOAT, '
    'ModeOfPayment_INC VARCHAR(20), '
    'Category_INC VARCHAR(20),'
    'User_ID INTEGER,'
    'FOREIGN KEY (User_ID) REFERENCES Users(User_ID)'
    'CONSTRAINT unique_inc UNIQUE (Date_INC, Note_INC, User_ID))'
)

# Creating the Budget table
cursor3.execute(
    'CREATE TABLE IF NOT EXISTS Budget '
    '(Budget_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'User_ID INTEGER,'
    'Budget_amount FLOAT,'
    'FOREIGN KEY (User_ID) REFERENCES Users(User_ID))'
)

# Commit the changes to the database
connector.commit()

# Set CTk appearance to light mode
set_appearance_mode("light")


##############################################################################
# Sign In / Sign Up Page Functions
##############################################################################
def toggle_password_visibility():  # Toggles the password visibility in the password entry
    if show_password_var.get():
        password_entry.configure(show="")
        register_confirm_password_entry.configure(show="")
        register_username_password_entry.configure(show="")
    else:
        password_entry.configure(show="*")
        register_confirm_password_entry.configure(show="*")
        register_username_password_entry.configure(show="*")


def user_login():  # Logs in the user (SQLite DQL)
    entered_username = user_entry.get()
    entered_password = hash_password(password_entry.get())
    if entered_username and entered_password:
        # Retrieve the stored password for the entered username
        cursor10.execute('SELECT User_ID FROM Users WHERE User_username = ? AND User_password = ?',
                         (entered_username, entered_password))
        user_id = cursor10.fetchone()

        if user_id:
            logged_in_user[0] = user_id[0]
            mb.showinfo("Login Successful", "Welcome, " + entered_username + "!")
            root.destroy()

        else:
            mb.showerror("Login Error", "Invalid username or password.")
    else:
        mb.showerror("Login Error", "Please enter both a username and password.")


def switch_to_login_page():  # Switches to Login page
    register_frame.place_forget()
    login_frame.place(x=480, y=70)


def switch_to_register_page():  # Switches to Register page
    login_frame.place_forget()
    register_frame.place(x=480, y=50)


def clear_username_entry(event):  # Clears out the text outline 'Username'
    if user_entry.get() == 'Username':
        user_entry.delete(0, 'end')


def reset_username_entry(event):  # Inserts the text outline 'Username'
    if user_entry.get() == '':
        user_entry.insert(0, 'Username')


def clear_password_entry(event):  # Clears out the text outline 'Password'
    if password_entry.get() == 'Password':
        password_entry.delete(0, 'end')
        password_entry.configure(show='*')


def reset_password_entry(event):  # Inserts the text outline 'Password'
    if password_entry.get() == '':
        password_entry.configure(show='')
        password_entry.insert(0, 'Password')


def hash_password(password):  # Hashes the password
    return hashlib.sha256(password.encode()).hexdigest()


def register():  # Registers a new user into the system (SQLite DML)
    username = register_username_entry.get()
    password = hash_password(register_username_password_entry.get())
    confirm_password = hash_password(register_confirm_password_entry.get())
    if username and password:
        if password != confirm_password:
            mb.showerror("Registration Error", "Passwords do not match.")
        else:
            try:
                cursor10.execute('INSERT INTO Users (User_username, User_password) VALUES (?, ?)',
                                 (username, password))
                connector.commit()
                mb.showinfo("Registration Successful", "You are now registered.")
                register_username_entry.delete(0, END)
                register_username_password_entry.delete(0, END)
                register_confirm_password_entry.delete(0, END)
                switch_to_login_page()
            except sqlite3.IntegrityError:
                mb.showerror("Registration Error", "Username already exists. Please choose another.")

    else:
        mb.showerror("Registration Error", "Please enter both a username and password.")


# Initialize the logged-in user as None
logged_in_user = [None]

##############################################################################
# The Sign In / Sign Up Page
##############################################################################

# Sign In / Sign Up Page Setup
root = CTk()
root.title('Acre Expense Tracker')
root.geometry('925x500+300+200')
root.configure(fg_color="#E64900")
root.resizable(False, False)

login_frame = CTkFrame(root, width=350, height=350)
login_frame.place(x=480, y=70)

heading = CTkLabel(login_frame, text='Sign In', font=('Microsoft YaHei UI Light', 30, 'bold'))
heading.place(relx=0.5, rely=0.1, anchor='center')

user_entry = CTkEntry(login_frame, width=290, font=('Microsoft YaHei UI Light', 11))
user_entry.place(x=30, y=80)
user_entry.insert(0, 'Username')
user_entry.bind('<FocusIn>', clear_username_entry)
user_entry.bind('<FocusOut>', reset_username_entry)

show_password_var = BooleanVar()
show_password_checkbox = CTkCheckBox(login_frame, text="Show Password", variable=show_password_var,
                                     command=toggle_password_visibility)
show_password_checkbox.place(relx=0.5, rely=0.85, anchor='center')

password_entry = CTkEntry(login_frame, width=290, font=('Microsoft YaHei UI Light', 11))
password_entry.place(x=30, y=130)
password_entry.insert(0, 'Password')
password_entry.configure(show='')
password_entry.bind('<FocusIn>', clear_password_entry)
password_entry.bind('<FocusOut>', reset_password_entry)

login_button = CTkButton(login_frame, width=39, text='Sign In', fg_color="green", hover_color="#005300",
                         command=user_login)
login_button.place(relx=0.5, rely=0.55, anchor='center')
label = CTkLabel(login_frame, text="Don't have an account?", font=('Microsoft YaHei UI Light', 12))
label.place(x=75, y=220)
sign_up = CTkButton(login_frame, width=6, text='Sign Up', fg_color='green', hover_color="#005300",
                    command=switch_to_register_page)
sign_up.place(x=215, y=220)

# Image in UI
acre_image = CTkImage(light_image=Image.open("Acre Logo White.png"), size=(340, 182))

label1 = CTkLabel(root, image=acre_image, text='')
label1.place(x=60, y=130)

# Sign Up frame
register_frame = CTkFrame(root, width=350, height=390)
heading = CTkLabel(register_frame, text='Sign Up', font=('Microsoft YaHei UI light', 30, 'bold'), )
heading.place(relx=0.5, rely=0.1, anchor='center')


# Username frame
def reset_username_signup(event):  # Same as reset_username_entry but in the Sign-Up page
    register_username_entry.delete(0, "end")


def clear_username_signup(event):  # Same as clear_username_entry but in the Sign-Up page
    name = register_username_entry.get()
    if name == '':
        register_username_entry.insert(0, 'Username')


register_username_entry = CTkEntry(register_frame, width=290,
                                   font=('Microsoft YaHei UI light', 11))
register_username_entry.place(x=30, y=100)
register_username_entry.insert(0, 'Username')
register_username_entry.bind('<FocusIn>', reset_username_signup)
register_username_entry.bind('<FocusOut>', clear_username_signup)


# Password frame
def clear_password1_entry(event):
    if register_username_password_entry.get() == 'Password':
        register_username_password_entry.delete(0, 'end')
        register_username_password_entry.configure(show='*')


def reset_password1_entry(event):
    if register_username_password_entry.get() == '':
        register_username_password_entry.configure(show='')
        register_username_password_entry.insert(0, 'Password')


register_username_password_entry = CTkEntry(register_frame, width=290,
                                            font=('Microsoft YaHei UI light', 11))
register_username_password_entry.place(x=30, y=150)
register_username_password_entry.insert(0, 'Password')
register_username_password_entry.bind('<FocusIn>', clear_password1_entry)
register_username_password_entry.bind('<FocusOut>', reset_password1_entry)


# Confirm Password frame
def clear_password2_entry(event):  # Clears out the text outline 'Confirm Password'
    if register_confirm_password_entry.get() == 'Confirm Password':
        register_confirm_password_entry.delete(0, 'end')
        register_confirm_password_entry.configure(show='*')


def reset_password2_entry(event):  # Inserts the text outline 'Confirm Password'
    if register_confirm_password_entry.get() == '':
        register_confirm_password_entry.configure(show='')
        register_confirm_password_entry.insert(0, 'Confirm Password')


register_confirm_password_entry = CTkEntry(register_frame, width=290,
                                           font=('Microsoft YaHei UI light', 11))
register_confirm_password_entry.place(x=30, y=200)
register_confirm_password_entry.insert(0, 'Confirm Password')
register_confirm_password_entry.bind('<FocusIn>', clear_password2_entry)
register_confirm_password_entry.bind('<FocusOut>', reset_password2_entry)

# Sign Up Button
CTkButton(register_frame, width=39, text='Sign Up', fg_color="green", hover_color="#005300", command=register).place(
    relx=0.5, rely=0.68, anchor='center')
label = CTkLabel(register_frame, text='I have an account.', font=('Microsoft YaHei UI Light', 12))
label.place(x=90, y=310)
signin = CTkButton(register_frame, width=6, text='Sign In', cursor='hand2', fg_color="green", hover_color="#005300",
                   command=switch_to_login_page)
signin.place(x=200, y=310)

show_password_checkbox2 = CTkCheckBox(register_frame, text="Show Password", variable=show_password_var,
                                      command=toggle_password_visibility)
show_password_checkbox2.place(relx=0.5, rely=0.93, anchor='center')

root.mainloop()

##############################################################################
# Home Menu
##############################################################################

# Home Menu Setup
money_app = CTk()
money_app.resizable(False, False)
money_app.geometry("1500x750")
money_app.title("Acre Expense Tracker")
money_app.configure(bg='black')

sv_ttk.set_theme("light")


##############################################################################
# Home Menu Functions
##############################################################################
def light_dark_mode():  # Switch between light/dark mode
    ld = lightdark.get()

    if ld:
        set_appearance_mode("dark")
        sv_ttk.set_theme("dark")
        mainframe1left.configure(fg_color="#952f00")
        mainframe2left.configure(fg_color="#952f00")
        mainframe3left.configure(fg_color="#952f00")

    else:
        set_appearance_mode("light")
        sv_ttk.set_theme("light")
        mainframe1left.configure(fg_color="#E64900")
        mainframe2left.configure(fg_color="#E64900")
        mainframe3left.configure(fg_color="#E64900")


def addexp_frame():  # Adds only the Expense Tracker UI Frame
    mainframe1left.pack_forget()
    mainframe1.pack_forget()
    mainframe3left.pack_forget()
    frame_3_1.pack_forget()
    frame_3_2.pack_forget()
    mainframe1.pack(fill='both', side='right', expand='true')
    frame_6_1.pack(padx=13, pady=10)
    mainframe2left.pack(fill='both', side='left', expand='true')


def addinc_frame():  # Adds only the Income Tracker UI Frame
    mainframe1.pack_forget()
    mainframe1left.pack_forget()
    mainframe2left.pack_forget()
    frame_3_1.pack_forget()
    frame_3_2.pack_forget()
    mainframe1.pack(fill='both', side='right', expand='true')
    frame_8_1.pack(padx=13, pady=10)
    mainframe3left.pack(fill='both', side='left', expand='true')


def home_frame():  # Adds only the Home UI Frame
    mainframe2left.pack_forget()
    mainframe3left.pack_forget()
    frame_6_1.pack_forget()
    frame_8_1.pack_forget()
    mainframe1left.pack(fill='both', side='left', expand='true')
    frame_3_1.pack(side='left', padx=13, pady=10)
    frame_3_2.pack(side='right', padx=13, pady=10)
    show_expsum()
    show_incsum()
    show_balance()
    list_all_expenses1()
    list_all_income1()


##############################################################################
# Functions for 'Expenses' menu
##############################################################################
def list_all_expenses():  # Lists all expenses into the expense table UI in the expense page
    global connector, table

    table.delete(*table.get_children())

    all_data1 = connector.execute('SELECT * FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
    data = all_data1.fetchall()

    for values in data:
        table.insert('', END, values=values)


def list_all_expenses1():  # Lists all expenses into the expense table UI in the home page
    global connector, table3

    table3.delete(*table3.get_children())

    all_data3 = connector.execute('SELECT * FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
    data = all_data3.fetchall()

    for values in data:
        table3.insert('', END, values=values)


def view_expense_details():  #
    global table
    global date_exp, payee, note_exp, amnt_exp, MOP_exp, cate_exp
    if not table.selection():
        mb.showerror('No Expense Selected', 'Please select an expense from the table to view its details.')
    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']
    expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
    date_exp.set_date(expenditure_date)
    payee.set(values[2])
    note_exp.set(values[3])
    amnt_exp.set(values[4])
    MOP_exp.set(values[5])
    cate_exp.set(values[6])


def selected_expense_to_words():  # Reads out the expense in sentence form
    global table

    if not table.selection():
        mb.showerror('No Expense Selected',
                     'Please select an expense from the table for Acre to read.')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    message = (f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} '
               f'for {values[3]} on {values[1]} via {values[5]} on {values[6]}"')

    mb.showinfo('Expense Sentence', message)


def remove_expense():  # Deletes the selected expense
    if not table.selection():
        mb.showerror('No Record Selected', 'Please select a record to delete.')
        return

    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']

    surety = mb.askyesno('Confirmation',
                         f'Are you sure about deleting the record of {values_selected[2]}?')

    if surety:
        connector.execute('DELETE FROM Expenses WHERE ID_EXP = ? AND User_ID = ?',
                          (values_selected[0], logged_in_user[0]))
        connector.commit()

        list_all_expenses()
        show_expsum()
        show_balance()
        mb.showinfo('Record Deletion Successful!', 'The record has been deleted successfully.')
        show_budget()


def delete_all_expenses():
    surety = mb.askyesno('Confirmation', 'Are you sure about deleting all expense records?', icon='warning')

    if surety:
        table.delete(*table.get_children())

        connector.execute('DELETE FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
        connector.commit()

        clear_fields()
        list_all_expenses()
        show_expsum()
        show_balance()
        mb.showinfo('All Expenses Deleted', 'All expense records were successfully deleted.')
        show_budget()
    else:
        mb.showinfo('Task Abortion', 'The task was aborted.')


def clear_fields():  # Clears all input fields
    global note_exp, payee, amnt_exp, MOP_exp, date_exp, table, cate_exp

    today_date = datetime.datetime.now().date()

    note_exp.set('')
    payee.set('')
    amnt_exp.set(0.0)
    MOP_exp.set(''), cate_exp.set(''), date_exp.set_date(today_date)
    table.selection_remove(*table.selection())


def adding_expense():  # Adds a new expense
    global date_exp, payee, note_exp, amnt_exp, MOP_exp, cate_exp
    global connector

    try:
        float(amnt_exp.get())
        if float(amnt_exp.get()) <= 0.0:
            mb.showerror('Inappropriate Value', 'Values 0 or less are not accepted.')
            return
    except:
        mb.showerror('Inappropriate Value', 'Please enter numbers in the expense entry.')
        return

    try:
        if (not date_exp.get() or not payee.get() or not note_exp.get() or not amnt_exp.get()
                or not MOP_exp.get() or not cate_exp.get()):
            mb.showerror('Fields empty!',
                         "Please fill all missing fields before pressing the save button!")
        else:
            (connector.execute('INSERT INTO Expenses (Date_EXP, Payee, Note_EXP, Amount_EXP, ModeOfPayment_EXP, '
                               'Category_EXP, User_ID)'
                               'VALUES (?,LTRIM(RTRIM(?)),LTRIM(RTRIM(?)),ROUND(?,1),?,?,?)',
                               (date_exp.get_date(), payee.get(), note_exp.get(),
                                amnt_exp.get(), MOP_exp.get(), cate_exp.get(),
                                logged_in_user[0])))

            connector.commit()
            clear_fields()
            list_all_expenses()
            show_expsum()
            show_balance()
            mb.showinfo('Expense Added',
                        'The expense has been added to the database.')
            show_budget()
    except sqlite3.IntegrityError:
        mb.showerror("Error", "Expense already exists. Try again.")


def edit_expense():  # Edits selected expense
    global table

    if not table.selection():
        mb.showerror('No Expense Selected',
                     'You have not selected an expense in the table to edit.')
        return

    delexp_button.place_forget()
    delallexp_button.place_forget()
    selexp_button.place_forget()
    senexp_button.place_forget()

    def edit_existing_expense():
        global date_exp, amnt_exp, note_exp, payee, MOP_exp, cate_exp
        global connector, table
        current_selected_expenditure = table.item(table.focus())
        contents = current_selected_expenditure['values']

        try:
            float(amnt_exp.get())
            if float(amnt_exp.get()) <= 0.0:
                mb.showerror('Inappropriate Value', 'Values 0 or less are not accepted.')
                return
        except:
            mb.showerror('Inappropriate Value', 'Please enter numbers in the expense entry.')
            return

        try:
            if (not date_exp.get() or not payee.get() or not note_exp.get() or not amnt_exp.get()
                    or not MOP_exp.get() or not cate_exp.get()):
                mb.showerror('Empty Fields',
                             "Please fill all the missing fields before saving the edit!")
            else:
                connector.execute(
                    'UPDATE Expenses SET Date_EXP = ?, Payee = LTRIM(RTRIM(?)), Note_EXP = LTRIM(RTRIM(?)), '
                    'Amount_EXP = ROUND(?,1),'
                    'ModeOfPayment_EXP = ?, Category_EXP = ? WHERE ID_EXP = ? AND User_ID = ?',
                    (date_exp.get_date(), payee.get(), note_exp.get(), amnt_exp.get(),
                     MOP_exp.get(), cate_exp.get(), contents[0], logged_in_user[0]))
                connector.commit()
                clear_fields()
                list_all_expenses()
                show_expsum()
                show_balance()
                mb.showinfo('Record Edited Successfully', 'The record has been updated successfully!')
                saveedit_button1.destroy()
                delexp_button.place(relx=0.5, rely=0.80, anchor='center')
                delallexp_button.place(relx=0.5, rely=0.95, anchor='center')
                selexp_button.place(relx=0.5, rely=0.85, anchor='center')
                senexp_button.place(relx=0.5, rely=0.90, anchor='center')
                show_budget()
                return
        except sqlite3.IntegrityError:
            mb.showerror("Error", "Expense already exists. Try again.")

    view_expense_details()
    saveedit_button1 = CTkButton(master=mainframe2left, text='Save Edit', command=edit_existing_expense,
                                 corner_radius=5, hover_color="#00456D", font=('Microsoft YaHei UI Light', 13, 'bold'),
                                 fg_color="#007CC2")
    saveedit_button1.place(relx=0.5, rely=0.75, anchor='center')


def show_expsum():  # Displays the sum of expenses of the user
    cursor1.execute('SELECT Amount_EXP FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
    result1 = cursor1.fetchall()

    total1 = sum(float(row[0]) for row in result1)
    moneycounter.configure(text="RM {:.2f}".format(total1))


##############################################################################
# Functions for 'Income' menu
##############################################################################

def list_all_income():  # Lists all income into the income table UI in the income page
    global connector, table2

    table2.delete(*table2.get_children())

    all_data2 = connector.execute('SELECT * FROM Income WHERE User_ID = ?', (logged_in_user[0],))
    data = all_data2.fetchall()

    for values in data:
        table2.insert('', END, values=values)


def list_all_income1():  # Lists all income into the income table UI in the home page
    global connector, table4

    table4.delete(*table4.get_children())

    all_data4 = connector.execute('SELECT * FROM Income WHERE User_ID = ?', (logged_in_user[0],))
    data = all_data4.fetchall()

    for values in data:
        table4.insert('', END, values=values)


def selected_income_to_words():  # Reads out income in sentence form
    global table2

    if not table2.selection():
        mb.showerror('No Income Selected',
                     'Please select an income from the table for Acre to read.')
        return

    current_selected_income = table2.item(table2.focus())
    values = current_selected_income['values']

    message = (f'Your income can be read like: \n"{values[2]} paid to you {values[4]}'
               f' for {values[3]} on {values[1]} via {values[5]} on {values[6]}"')

    mb.showinfo('Income Sentence', message)


def remove_income():  # Deletes the selected income
    if not table2.selection():
        mb.showerror('No Record Selected', 'Please select a record to delete.')
        return

    current_selected_income = table2.item(table2.focus())
    values_selected = current_selected_income['values']

    surety = mb.askyesno('Confirmation',
                         f'Are you sure about deleting the record of {values_selected[2]}?')

    if surety:
        connector.execute('DELETE FROM Income WHERE ID_INC = ? AND User_ID = ?',
                          (values_selected[0], logged_in_user[0]))
        connector.commit()

        list_all_income()
        show_incsum()
        show_balance()
        mb.showinfo('Record deletion successful!',
                    'The record has been deleted successfully.')


def delete_all_income():
    surety = mb.askyesno('Confirmation', 'Are you sure about deleting all income records?', icon='warning')

    if surety:
        table2.delete(*table2.get_children())

        connector.execute('DELETE FROM Income WHERE User_ID = ?', (logged_in_user[0],))
        connector.commit()

        income_clear_fields()
        list_all_income()
        show_incsum()
        show_balance()
        mb.showinfo('All Income Deleted', 'All income records were successfully deleted.')
    else:
        mb.showinfo('Task Abortion', 'The task was aborted.')


def income_clear_fields():  # Clears all input fields
    global note_inc, payer, amnt_inc, MOP_inc, table2, date_inc, cate_inc

    today_date = datetime.datetime.now().date()

    note_inc.set('')
    payer.set('')
    amnt_inc.set(0.00)
    MOP_inc.set(''), cate_inc.set(''), date_inc.set_date(today_date)
    table2.selection_remove(*table2.selection())


def adding_income():  # Adds a new income
    global note_inc, payer, amnt_inc, MOP_inc, date_inc, table2, cate_inc
    global connector

    try:
        float(amnt_inc.get())
        if float(amnt_inc.get()) <= 0.0:
            mb.showerror('Inappropriate Value', 'Values 0 or less are not accepted.')
            return
    except:
        mb.showerror('Inappropriate Value', 'Please enter numbers in the income entry.')
        return

    try:
        # Check if any of the required fields are empty
        if (not date_inc.get() or not payer.get() or not note_inc.get() or not amnt_inc.get()
                or not MOP_inc.get() or not cate_inc.get()):
            mb.showerror('Empty Fields',
                         "Please fill all missing fields before pressing the save button!")
        else:
            # If all fields are filled, insert the data into the database
            connector.execute('INSERT INTO Income (Date_INC, Payer_INC, Note_INC, Amount_INC, '
                              'ModeOfPayment_INC, Category_INC, User_ID) VALUES (?, LTRIM(RTRIM(?)), LTRIM(RTRIM(?)), '
                              'ROUND(?,1), ?, ?, ?)',
                              (date_inc.get_date(), payer.get(), note_inc.get(), amnt_inc.get(),
                               MOP_inc.get(), cate_inc.get(), logged_in_user[0]))
            connector.commit()
            income_clear_fields()
            list_all_income()
            show_incsum()
            show_balance()
            # Show an info message
            mb.showinfo('Income Added',
                        'The income has been added to the database.')
    except sqlite3.IntegrityError:
        mb.showerror("Error", "Income already exists. Try again.")


def view_income_details():
    global table2
    global date_inc, payer, note_inc, amnt_inc, MOP_inc, cate_inc
    if not table2.selection():
        mb.showerror('No expense selected', 'Please select an income from the table to view its details')
    current_selected_income = table2.item(table2.focus())
    values = current_selected_income['values']
    income_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
    date_inc.set_date(income_date)
    payer.set(values[2])
    note_inc.set(values[3])
    amnt_inc.set(values[4])
    MOP_inc.set(values[5])
    cate_inc.set(values[6])


def edit_income():  # Edits the selected income
    global table2

    if not table2.selection():
        mb.showerror('No Income Selected',
                     'You have not selected any income in the table to edit.')
        return

    delinc_button.place_forget()
    delallinc_button.place_forget()
    selinc_button.place_forget()
    seninc_button.place_forget()

    def edit_existing_income():
        global date_inc, amnt_inc, note_inc, payee, MOP_inc, cate_inc
        global connector, table2

        current_selected_income = table2.item(table2.focus())
        contents = current_selected_income['values']

        try:
            float(amnt_inc.get())
            if float(amnt_inc.get()) <= 0.0:
                mb.showerror('Inappropriate Value', 'Values 0 or less are not accepted.')
                return
        except ValueError:
            mb.showerror('Inappropriate Value', 'Please enter numbers in the income entry.')
            return

        try:
            if (not date_inc.get() or not payer.get() or not note_inc.get() or not amnt_inc.get()
                    or not MOP_inc.get() or not cate_inc.get()):
                mb.showerror('Empty Fields',
                             "Please fill all missing fields before saving the edit!")
            else:

                connector.execute(
                    'UPDATE Income SET Date_INC = ?, Payer_INC = LTRIM(RTRIM(?)), Note_INC = LTRIM(RTRIM(?)), '
                    'Amount_INC = ROUND(?,1),'
                    'ModeOfPayment_INC = ?,'
                    'Category_INC = ? WHERE ID_INC = ? AND User_ID = ?',
                    (date_inc.get_date(), payer.get(), note_inc.get(), amnt_inc.get(),
                     MOP_inc.get(), cate_inc.get(), contents[0], logged_in_user[0]))
                connector.commit()
                income_clear_fields()
                list_all_income()
                show_incsum()
                show_balance()
                mb.showinfo('Record Edited Successfully', 'The record has been updated successfully!')
                saveedit_button2.destroy()
                delinc_button.place(relx=0.5, rely=0.80, anchor='center')
                delallinc_button.place(relx=0.5, rely=0.95, anchor='center')
                selinc_button.place(relx=0.5, rely=0.85, anchor='center')
                seninc_button.place(relx=0.5, rely=0.90, anchor='center')
                return
        except sqlite3.IntegrityError:
            mb.showerror("Error", "Income already exists. Try again.")

    view_income_details()
    saveedit_button2 = CTkButton(master=mainframe3left, text='Save Edit', command=edit_existing_income,
                                 corner_radius=5, hover_color="#00456D", font=('Microsoft YaHei UI Light', 13, 'bold'),
                                 fg_color="#007CC2")
    saveedit_button2.place(relx=0.5, rely=0.75, anchor='center')


def show_incsum():  # Displays the sum of income of the user
    cursor2.execute('SELECT Amount_INC FROM Income WHERE User_ID = ?', (logged_in_user[0],))
    result2 = cursor2.fetchall()

    total2 = sum(float(row[0]) for row in result2)
    inccounter.configure(text="RM {:.2f}".format(total2))


# Display Balance
def show_balance():  # Displays the balance (Total Income - Total Expenses)
    cursor1.execute('SELECT Amount_EXP FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
    result3 = cursor1.fetchall()
    total3 = sum(float(row[0]) for row in result3)

    cursor2.execute('SELECT Amount_INC FROM Income WHERE User_ID = ?', (logged_in_user[0],))
    result4 = cursor2.fetchall()
    total4 = sum(float(row[0]) for row in result4)

    total5 = total4 - total3

    balancecounter.configure(text="RM {:.2f}".format(total5), text_color='green')

    if total5 < 0:
        balancecounter.configure(text="RM {:.2f}".format(total5), text_color='red')
    else:
        balancecounter.configure(text="RM {:.2f}".format(total5), text_color='green')


def show_username():  # Displays the logged-in user's username
    cursor10.execute('SELECT User_username FROM Users WHERE User_ID = ?', (logged_in_user[0],))
    dispuser = cursor10.fetchone()
    cleaned_data = [''.join(map(str, item)).replace("(", "").replace(")", "").replace("'", "").replace(",", "") for item
                    in dispuser]

    for item in cleaned_data:
        welclabel.configure(text="Welcome, {}".format(item))


def load_budget():  # Loads the saved budget if there is one
    cursor3.execute('SELECT Budget_amount FROM Budget WHERE User_ID = ?', (logged_in_user[0],))
    bdata = cursor3.fetchone()
    budget_button = CTkButton(master=mainframe1left, text="Save Budget", fg_color='green', hover_color="#005300",
                              font=('Microsoft YaHei UI Light', 13, 'bold'), command=save_budget)
    budget_entry1 = CTkEntry(master=mainframe1left, height=30, width=80)

    if bdata is None:
        budget_button.place(relx=0.5, rely=0.8, anchor='center')
        budget_label.configure(text='Set A Budget')
        budget_entry1.destroy()
    else:
        budget_button.destroy()
        show_budget()

        def edit_budget():  # Edits the existing budget amount
            try:
                budget_amount1 = int(budget_entry1.get())
                if budget_amount1 <= 0:
                    mb.showerror('Invalid Budget', 'Please enter a valid budget amount.')
                else:
                    connector.execute('UPDATE Budget SET Budget_amount = ? WHERE User_ID = ?',
                                      (budget_amount1, logged_in_user[0],))
                    connector.commit()
                    mb.showinfo('Budget Updated', 'Budget has been updated successfully.')
                    show_budget()
            except ValueError:
                mb.showerror('Invalid Budget', 'Please enter a valid budget amount.')

        budget_entry1.place(relx=0.5, rely=0.75, anchor='center')
        editbudget_button = CTkButton(master=mainframe1left, text="Reset Budget", hover_color="#00456D",
                                      font=('Microsoft YaHei UI Light', 13, 'bold'),
                                      fg_color="#007CC2", command=edit_budget)
        editbudget_button.place(relx=0.5, rely=0.8, anchor='center')

    def delete_budget():  # Deletes the user's budget
        cursor3.execute('SELECT Budget_amount FROM Budget WHERE User_ID = ?', (logged_in_user[0],))
        bdata1 = cursor3.fetchone()

        if bdata1 is None:
            mb.showerror('Error', 'No budget to be deleted.')
        else:
            surety1 = mb.askyesno('Confirmation', 'Are you sure about deleting your budget?', icon='warning')

            if surety1:
                connector.execute('DELETE FROM Budget WHERE User_ID = ?', (logged_in_user[0],))
                connector.commit()
                load_budget()
                budget_entry1.destroy()

                mb.showinfo('Budget Deleted', 'Budget was successfully deleted.')
            else:
                mb.showinfo('Task Abortion', 'The task was aborted.')

    buddel_button = CTkButton(master=mainframe1left, text="Delete Budget", fg_color='black', hover_color="#808080",
                              font=('Microsoft YaHei UI Light', 13, 'bold'), command=delete_budget)
    buddel_button.place(relx=0.5, rely=0.85, anchor='center')


def save_budget():  # Saves a new budget
    try:
        budget_amount = int(budget_entry.get())
        budget_button = CTkButton(master=mainframe1left, text="Save Budget", fg_color='green', hover_color="#005300",
                                  font=('Microsoft YaHei UI Light', 13, 'bold'), command=save_budget)
        budget_button.place(relx=0.5, rely=0.8, anchor='center')
        if budget_amount <= 0:
            mb.showerror('Invalid Budget', 'Please enter a valid budget amount.')
        else:
            connector.execute('INSERT INTO Budget (Budget_amount, User_ID) VALUES (?,?)',
                              (budget_amount, logged_in_user[0]))
            connector.commit()
            mb.showinfo('Budget Saved', 'Budget has been set successfully.')
            budget_button.destroy()
            load_budget()
    except ValueError:
        mb.showerror('Invalid Budget', 'Please enter a valid budget amount.')


def show_budget():  # Displays the user's budget
    cursor3.execute('SELECT Budget_amount FROM Budget WHERE User_ID = ?', (logged_in_user[0],))
    b_label = cursor3.fetchall()
    bud1 = sum(float(row[0]) for row in b_label)

    budget_label.configure(text='Budget: RM {}'.format(bud1))

    cursor1.execute('SELECT Amount_EXP FROM Expenses WHERE User_ID = ?', (logged_in_user[0],))
    result10 = cursor1.fetchall()

    total10 = sum(float(row[0]) for row in result10)

    budbalance = (total10 / bud1) * 100

    def notify_budget60():
        toast = Notification(app_id="Acre ",
                             title="Expenses Approaching Budget Amount",
                             msg="Your total expenses are more than 60% of your set budget.",
                             duration="short",
                             icon=r"C:\Users\LIM TZE TA\PycharmProjects\project1\Acre Symbol.png")

        toast.set_audio(audio.SMS, loop=False)
        toast.show()

    def notify_budget80():
        toast = Notification(app_id="Acre ",
                             title="Expenses Approaching Budget Amount",
                             msg="Your total expenses are more than 80% of your set budget.",
                             duration="short",
                             icon=r"C:\Users\LIM TZE TA\PycharmProjects\project1\Acre Symbol.png")

        toast.set_audio(audio.SMS, loop=False)
        toast.show()

    def notify_budget95():
        toast = Notification(app_id="Acre ",
                             title="Expenses Approaching Budget Amount",
                             msg="Your total expenses are more than 95% of your set budget.",
                             duration="short",
                             icon=r"C:\Users\LIM TZE TA\PycharmProjects\project1\Acre Symbol.png")

        toast.set_audio(audio.SMS, loop=False)
        toast.show()

    def notify_budget100():
        toast = Notification(app_id="Acre ",
                             title="Expenses Has Exceeded Budget Amount",
                             msg="Your total expenses have exceeded your set budget.",
                             duration="short",
                             icon=r"C:\Users\LIM TZE TA\PycharmProjects\project1\Acre Symbol.png")

        toast.set_audio(audio.SMS, loop=False)
        toast.show()

    if b_label is not None:
        if 60.0 <= budbalance < 80.0:
            notify_budget60()
        elif 80.0 <= budbalance < 95.0:
            notify_budget80()
        elif 95.0 <= budbalance < 100.0:
            notify_budget95()
        elif budbalance >= 100.0:
            notify_budget100()


def treeview_sort_column(tv, col, reverse):  # Sorts columns in ascending or descending order
    # Retrieve values and their data types
    data = [(tv.set(k, col), k, type(tv.set(k, col))) for k in tv.get_children('')]

    # Define a custom sorting function
    def custom_sort(item):
        value, _, data_type = item
        try:
            # Try to convert to float, if possible
            value = float(value)
            return 0, value  # Sort floats first
        except ValueError:
            return 1, value  # Sort strings and other types second

    # Sort based on the custom sorting function
    data.sort(key=custom_sort, reverse=reverse)

    # Rearrange items in sorted positions
    for index, (_, k, _) in enumerate(data):
        tv.move(k, '', index)

    # Reverse sort next time (toggle between ascending and descending)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


# Exits the program completely when the 'x' button is clicked
if logged_in_user == [None]:
    sys.exit()
else:
    print('Login Successful.')

##############################################################################
# Right mainframe (Home)
##############################################################################
mainframe1 = CTkFrame(master=money_app, fg_color="#000000", height=750, width=1150, corner_radius=0)
mainframe1.pack(fill='y', side='right')

# Frame 1 (invisible; support frame for frame_1_1)
frame_1 = CTkFrame(master=mainframe1, fg_color="#000000", height=150)
frame_1.pack(fill='x', padx=10, pady=10)

# Frame 1_1
frame_1_1 = CTkFrame(master=frame_1, height=150)
frame_1_1.pack(fill='x')

welclabel = CTkLabel(master=frame_1_1, text="", font=('Microsoft YaHei UI Light', 18))
welclabel.place(anchor='center', relx=0.5, rely=0.2)
show_username()

Bcounter = CTkLabel(master=frame_1_1, text='Balance', font=('Microsoft YaHei UI Light', 18))
Bcounter.place(relx=0.02, rely=0.33)

balancecounter = CTkLabel(master=frame_1_1, text="", font=('Microsoft YaHei UI Light', 50))
balancecounter.place(relx=0.02, rely=0.5)
show_balance()

# Frame 2 (invisible; support frame for frame 2_1 and frame 2_2)

frame_2 = CTkFrame(master=mainframe1, fg_color="#000000", height=200)
frame_2.pack(fill='x', padx=10, pady=10)

# Left Frame in Frame 2 (2_1)

frame_2_1 = CTkFrame(master=frame_2, height=100, width=575)
frame_2_1.pack(side='left', padx=1, pady=1)

Mcounter = CTkLabel(master=frame_2_1, text='Expenses', font=('Microsoft YaHei UI Light', 18))
Mcounter.place(relx=0.02, rely=0.2)

moneycounter = CTkLabel(master=frame_2_1, text="", font=('Microsoft YaHei UI Light', 25))
moneycounter.place(relx=0.02, rely=0.5)

# Right Frame in Frame 2 (2_2)

frame_2_2 = CTkFrame(master=frame_2, height=100, width=575)
frame_2_2.pack(side='right', padx=1, pady=1)

Icounter = CTkLabel(master=frame_2_2, text='Income', font=('Microsoft YaHei UI Light', 18))
Icounter.place(relx=0.02, rely=0.2)

inccounter = CTkLabel(master=frame_2_2, text="", font=('Microsoft YaHei UI Light', 25))
inccounter.place(relx=0.02, rely=0.5)

# Frame 3_1

frame_3_1 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", width=575, height=650, border_width=2)
frame_3_1.pack(side='left', padx=13, pady=10)

# Expenses Treeview Frame (Homepage)
columns3 = ('ID', 'Date', 'Payee', 'Note', 'Amount', "Mode of Payment", 'Category')
table3 = ttk.Treeview(frame_3_1, selectmode=BROWSE,
                      columns=columns3)

X_Scroller = CTkScrollbar(table3, orientation=HORIZONTAL, command=table3.xview)
Y_Scroller = CTkScrollbar(table3, orientation=VERTICAL, command=table3.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table3.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table3.heading('ID', text='No.', anchor=CENTER)
table3.heading('Date', text='Date', anchor=CENTER)
table3.heading('Payee', text='Payee', anchor=CENTER)
table3.heading('Note', text='Note', anchor=CENTER)
table3.heading('Amount', text='Amount', anchor=CENTER)
table3.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table3.heading('Category', text='Category', anchor=CENTER)

table3.column('#0', width=0, stretch=NO)
table3.column('#1', width=0, stretch=NO)
table3.column('#2', width=95, stretch=NO)  # Date column
table3.column('#3', width=0, stretch=NO)  # Payee column
table3.column('#4', width=255, stretch=YES)  # Title column
table3.column('#5', width=150, stretch=NO)  # Amount column
table3.column('#6', width=0, stretch=NO)  # Mode of Payment column
table3.column('#7', width=130, stretch=NO)  # Category column

table3.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses1()
show_expsum()
for col in columns3:
    table3.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(table3, _col, False))

# Frame 3_2

frame_3_2 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", width=575, height=650, border_width=2)
frame_3_2.pack(side='right', padx=13, pady=10)

# Income Treeview Frame (Homepage)
columns4 = ('ID', 'Date', 'Payer', 'Note', 'Amount', "Mode of Payment", 'Category')
table4 = ttk.Treeview(frame_3_2, selectmode=BROWSE, columns=columns4)

X_Scroller_inc = CTkScrollbar(table4, orientation=HORIZONTAL, command=table4.xview)
Y_Scroller_inc = CTkScrollbar(table4, orientation=VERTICAL, command=table4.yview)
X_Scroller_inc.pack(side=BOTTOM, fill=X)
Y_Scroller_inc.pack(side=RIGHT, fill=Y)

table4.config(yscrollcommand=Y_Scroller_inc.set, xscrollcommand=X_Scroller_inc.set)

table4.heading('ID', text='No.', anchor=CENTER)
table4.heading('Date', text='Date', anchor=CENTER)
table4.heading('Payer', text='Payer', anchor=CENTER)
table4.heading('Note', text='Note', anchor=CENTER)
table4.heading('Amount', text='Amount', anchor=CENTER)
table4.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table4.heading('Category', text='Category', anchor=CENTER)

table4.column('#0', width=0, stretch=NO)
table4.column('#1', width=0, stretch=NO)
table4.column('#2', width=95, stretch=NO)  # Date column
table4.column('#3', width=0, stretch=NO)  # Payer column
table4.column('#4', width=255, stretch=YES)  # Title column
table4.column('#5', width=150, stretch=NO)  # Amount column
table4.column('#6', width=0, stretch=NO)  # Mode of Payment column
table4.column('#7', width=130, stretch=NO)  # Category column

table4.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_income1()
show_incsum()

for col in columns4:
    table4.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(table4, _col, False))

##############################################################################
# Left mainframe (Home)
##############################################################################

mainframe1left = CTkFrame(master=money_app, height=750, width=350, corner_radius=0)
mainframe1left.pack(fill='y', side='left', expand='true')
mainframe1left.pack_propagate(False)
mainframe1left.configure(fg_color="#E64900")

budget_label = CTkLabel(master=mainframe1left, text="", font=('Microsoft YaHei UI Light', 18, 'bold'))
budget_label.place(relx=0.5, rely=0.7, anchor='center')

budget_entry = CTkEntry(master=mainframe1left, height=30, width=80)
budget_entry.place(relx=0.5, rely=0.75, anchor='center')
load_budget()

addexpbut = CTkButton(master=mainframe1left, text='Add Expense', height=50,
                      font=('Microsoft YaHei UI Light', 15, 'bold'),
                      hover_color="#808080",
                      fg_color="#000000", command=addexp_frame)
addexpbut.place(anchor='center', relx=0.5, rely=0.1)
addincbut = CTkButton(master=mainframe1left, text='Add Income', height=50,
                      font=('Microsoft YaHei UI Light', 15, 'bold'),
                      hover_color="#808080", fg_color="#000000", command=addinc_frame)
addincbut.place(anchor='center', relx=0.5, rely=0.2)

lightdark = CTkSwitch(master=mainframe1left, text="Dark Mode", command=light_dark_mode,
                      onvalue=1, offvalue=0)
lightdark.place(relx=0.05, rely=0.93)

##############################################################################
# Mainframe 2 (Expenses)
##############################################################################
mainframe2left = CTkFrame(master=money_app, height=750, width=350, corner_radius=0)
mainframe2left.pack()
mainframe2left.configure(fg_color="#E64900")
mainframe2left.pack_forget()

# StringVar and DoubleVar variables (Add Expense)

note_exp = StringVar()
amnt_exp = DoubleVar()
payee = StringVar()
MOP_exp = StringVar()
cate_exp = StringVar()

# New Expense heading
heading = CTkLabel(master=mainframe2left, text='EXPENSES', font=('Microsoft YaHei UI Light', 30, 'bold'), )
heading.place(relx=0.25, rely=0.03, anchor='center')


# Add or Edit Expense
# Functions to clear the text in the entry exp_amount
def clear_addexp_entry(event):
    if addexp_entry.get() == '0.0':
        addexp_entry.delete(0, 'end')


def reset_addexp_entry(event):
    if addexp_entry.get() == '':
        addexp_entry.insert(0, 0.0)


addexp_label = CTkLabel(mainframe2left, text='Amount  :').place(x=10, y=90)

addexp_entry = CTkEntry(master=mainframe2left, justify="center", textvariable=amnt_exp)
addexp_entry.place(x=70, y=90)
addexp_entry.insert(0, '')
addexp_entry.bind('<FocusIn>', clear_addexp_entry)
addexp_entry.bind('<FocusOut>', reset_addexp_entry)

# Buttons in Mainframe 2

save_button = CTkButton(master=mainframe2left, text='Save', command=adding_expense,
                        corner_radius=5, hover_color="#005300", font=('Microsoft YaHei UI Light', 13, 'bold'),
                        fg_color="green", )
save_button.place(relx=0.5, rely=0.75, anchor='center')

homepage_button = CTkButton(master=mainframe2left, text='Home', command=home_frame, width=60,
                            corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'),
                            fg_color="#000000")
homepage_button.place(relx=0.8, rely=0.01)

delexp_button = CTkButton(master=mainframe2left, text='Delete Expense', command=remove_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
delexp_button.place(relx=0.5, rely=0.80, anchor='center')

selexp_button = CTkButton(master=mainframe2left, text='Edit Selected Expense', command=edit_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
selexp_button.place(relx=0.5, rely=0.85, anchor='center')

senexp_button = CTkButton(master=mainframe2left, text='Read Expense as Sentence',
                          command=selected_expense_to_words,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
senexp_button.place(relx=0.5, rely=0.90, anchor='center')

delallexp_button = CTkButton(master=mainframe2left, text='Delete All Expenses',
                             hover_color="#808080", command=delete_all_expenses,
                             font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
delallexp_button.place(relx=0.5, rely=0.95, anchor='center')

# Labels/Entries in Mainframe 2

Date = CTkLabel(master=mainframe2left, text='Date (MM/DD/YY):')
Date.place(x=10, y=50)

date_exp = DateEntry(master=mainframe2left, date=datetime.datetime.now().date())
date_exp.place(x=160, y=65)

Payee_Label = CTkLabel(master=mainframe2left, text='Payee : ')
Payee_Label.place(x=10, y=260)

Payee_Entry = CTkEntry(master=mainframe2left, textvariable=payee)
Payee_Entry.place(x=55, y=260)

Note_Label = CTkLabel(mainframe2left, text='Note  :').place(x=10, y=130)
Note_Entry = CTkEntry(mainframe2left, textvariable=note_exp, width=200, height=100).place(x=50, y=130)

CTkLabel(master=mainframe2left, text='Mode of Payment:').place(x=10, y=310)
dd1 = OptionMenu(mainframe2left, MOP_exp,
                 *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'E-Wallet', 'Google Pay'
                   ])
dd1.place(x=160, y=390)
dd1.configure(width=10)

CTkLabel(master=mainframe2left, text='Category:').place(x=10, y=350)
category = OptionMenu(mainframe2left, cate_exp,
                      *['Automotive', 'Bills', 'Food', 'Hobbies', 'Healthcare', 'Shopping', 'Other'])
category.place(x=160, y=440)
category.configure(width=10)

# Frame 6 (Expense Table)

frame_6_1 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", height=650, width=1150, border_width=2)
frame_6_1.pack()

columns1 = ('ID', 'Date', 'Payee', 'Note', 'Amount', 'Mode of Payment', 'Category')
table = ttk.Treeview(frame_6_1, selectmode=BROWSE,
                     columns=columns1)

X_Scroller = CTkScrollbar(table, orientation=HORIZONTAL, command=table.xview)
Y_Scroller = CTkScrollbar(table, orientation=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Note', text='Note', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table.heading('Category', text='Category', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=0, stretch=NO)
table.column('#2', stretch=YES)  # Date column
table.column('#3', stretch=YES)  # Payee column
table.column('#4', width=300, stretch=NO)  # Note column
table.column('#5', stretch=YES)  # Amount column
table.column('#6', stretch=YES)  # Mode of Payment column
table.column('#7', stretch=YES)  # Category column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()
show_expsum()
for col in columns1:
    table.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(table, _col, False))

##############################################################################
# Main Frame3 (Add Income)
##############################################################################

mainframe3left = CTkFrame(master=money_app, height=750, width=350, corner_radius=0)
mainframe3left.pack()
mainframe3left.configure(fg_color="#E64900")
mainframe3left.pack_forget()

# StringVar and DoubleVar variables (Add Expense)
note_inc = StringVar()
amnt_inc = DoubleVar()
payer = StringVar()
MOP_inc = StringVar()
cate_inc = StringVar()

# New Income heading

heading1 = CTkLabel(master=mainframe3left, text='INCOME', font=('Microsoft YaHei UI Light', 30, 'bold'), )
heading1.place(relx=0.22, rely=0.03, anchor='center')


# Add or Edit Income
# Functions to clear the text in the entry inc_amount
def clear_addinc_entry(event):
    if addinc_entry.get() == '0.0':
        addinc_entry.delete(0, 'end')


def reset_addinc_entry(event):
    entry_value = addinc_entry.get()

    if entry_value == '':
        entry_value = '0.0'

    try:
        float_value = round(float(entry_value), 2)
        addinc_entry.delete(0, 'end')
        addinc_entry.insert(0, float_value)
    except ValueError:
        print("Invalid input. Please enter a valid number.")


addinc_label = CTkLabel(mainframe3left, text='Amount  :').place(x=10, y=90)

addinc_entry = CTkEntry(master=mainframe3left, justify="center", textvariable=amnt_inc)
addinc_entry.place(x=70, y=90)
addinc_entry.insert(0, '')
addinc_entry.bind('<FocusIn>', clear_addinc_entry)
addinc_entry.bind('<FocusOut>', reset_addinc_entry)

# Button in Frame 8

save_button_inc = CTkButton(master=mainframe3left, text='Save', command=adding_income,
                            corner_radius=5, hover_color="#005300", font=('Microsoft YaHei UI Light', 13, 'bold'),
                            fg_color="green")
save_button_inc.place(relx=0.5, rely=0.75, anchor='center')

homepage_inc_button = CTkButton(master=mainframe3left, text='Home', command=home_frame, width=60,
                                corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'),
                                fg_color="#000000")
homepage_inc_button.place(relx=0.8, rely=0.01)

delinc_button = CTkButton(master=mainframe3left, text='Delete Income', command=remove_income,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
delinc_button.place(relx=0.5, rely=0.80, anchor='center')

selinc_button = CTkButton(master=mainframe3left, text='Edit Selected Income', command=edit_income,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
selinc_button.place(relx=0.5, rely=0.85, anchor='center')

seninc_button = CTkButton(master=mainframe3left, text='Read Income as Sentence', command=selected_income_to_words,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
seninc_button.place(relx=0.5, rely=0.90, anchor='center')

delallinc_button = CTkButton(master=mainframe3left, text='Delete All Income',
                             hover_color="#808080", command=delete_all_income,
                             font=('Microsoft YaHei UI Light', 13, 'bold'), fg_color="#000000")
delallinc_button.place(relx=0.5, rely=0.95, anchor='center')

# Labels/Entries in Mainframe 3

incomedate = CTkLabel(master=mainframe3left, text='Date (MM/DD/YY):')
incomedate.place(x=10, y=50)

date_inc = DateEntry(master=mainframe3left, date=datetime.datetime.now().date())
date_inc.place(x=160, y=65)

Payer_inc_Label = CTkLabel(master=mainframe3left, text='Payer : ')
Payer_inc_Label.place(x=10, y=260)

Payer_inc_Entry = CTkEntry(master=mainframe3left, textvariable=payer)
Payer_inc_Entry.place(x=55, y=260)

Note_inc_Label = CTkLabel(mainframe3left, text='Note  :').place(x=10, y=130)
Note_inc_Entry = CTkEntry(mainframe3left, textvariable=note_inc, width=200, height=100).place(x=50, y=130)

CTkLabel(master=mainframe3left, text='Mode of Payment:').place(x=10, y=310)
dd1_inc = OptionMenu(mainframe3left, MOP_inc,
                     *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'E-Wallet', 'Google Pay'
                       ])
dd1_inc.place(x=160, y=390)
dd1_inc.configure(width=10)

CTkLabel(master=mainframe3left, text='Category:').place(x=10, y=350)
category_inc = OptionMenu(mainframe3left, cate_inc,
                          *['Deposit', 'Salary', 'Savings', 'Other'])
category_inc.place(x=160, y=440)
category_inc.configure(width=10)

# Frame8_1 (Income Table)

frame_8_1 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", height=650, width=1150, border_width=2)
frame_8_1.pack(side='right')

columns2 = ('ID', 'Date', 'Payer', 'Note', 'Amount', "Mode of Payment", 'Category')
table2 = ttk.Treeview(frame_8_1, selectmode=BROWSE, columns=columns2)

X_Scroller_inc = CTkScrollbar(table2, orientation=HORIZONTAL, command=table2.xview)
Y_Scroller_inc = CTkScrollbar(table2, orientation=VERTICAL, command=table2.yview)
X_Scroller_inc.pack(side=BOTTOM, fill=X)
Y_Scroller_inc.pack(side=RIGHT, fill=Y)

table2.config(yscrollcommand=Y_Scroller_inc.set, xscrollcommand=X_Scroller_inc.set)

table2.heading('ID', text='No.', anchor=CENTER)
table2.heading('Date', text='Date', anchor=CENTER)
table2.heading('Payer', text='Payer', anchor=CENTER)
table2.heading('Note', text='Note', anchor=CENTER)
table2.heading('Amount', text='Amount', anchor=CENTER)
table2.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table2.heading('Category', text='Category', anchor=CENTER)

table2.column('#0', width=0, stretch=NO)
table2.column('#1', width=0, stretch=NO)
table2.column('#2', stretch=YES)  # Date column
table2.column('#3', stretch=YES)  # Payer column
table2.column('#4', width=300, stretch=NO)  # Note column
table2.column('#5', stretch=YES)  # Amount column
table2.column('#6', stretch=YES)  # Mode of Payment column
table2.column('#7', stretch=YES)  # Category column

table2.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_income()
for col in columns2:
    table2.heading(col, text=col, command=lambda _col=col: \
        treeview_sort_column(table2, _col, False))

# Let the Home Menu appear first

frame_6_1.pack_forget()
frame_8_1.pack_forget()

money_app.mainloop()

cursor1.close()
cursor2.close()
cursor3.close()
cursor10.close()
connector.close()
