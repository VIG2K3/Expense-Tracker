from customtkinter import *
from tkinter import OptionMenu
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import tkinter.messagebox as mb
import sv_ttk
import sqlite3

# Connecting to the Database
connector = sqlite3.connect("Expense Tracker ccc.db")
cursor1 = connector.cursor()
cursor2 = connector.cursor()

# Create the Expenses table
cursor1.execute(
    'CREATE TABLE IF NOT EXISTS Expenses '
    '(ID_EXP INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'Date_EXP DATETIME, '
    'Payee TEXT, '
    'Note_EXP TEXT, '
    'Amount_EXP FLOAT, '
    'ModeOfPayment_EXP TEXT, '
    'Category_EXP VARCHAR(20),'
    'CONSTRAINT unique_exp UNIQUE (Date_EXP, Note_EXP))'
)

# Create the Income table
cursor2.execute(
    'CREATE TABLE IF NOT EXISTS Income '
    '(ID_INC INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'Date_INC DATETIME, '
    'Payer_INC TEXT, '
    'Note_INC TEXT, '
    'Amount_INC FLOAT, '
    'ModeOfPayment_INC TEXT, '
    'Category_INC VARCHAR(20))'
)

# Commit the changes to the database
connector.commit()

# GUI
money_app = CTk()
money_app.resizable(False, False)
money_app.geometry("1500x750")
money_app.title("Expense Tracker")
money_app.configure(bg='black')

set_appearance_mode("light")
sv_ttk.set_theme("light")


# Menu Functions
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


def addexp_frame():
    mainframe1left.pack_forget()
    mainframe1.pack_forget()
    mainframe3left.pack_forget()
    frame_3_1.pack_forget()
    frame_3_2.pack_forget()
    mainframe1.pack(fill='both', side='right', expand='true')
    frame_6_1.pack(padx=13, pady=10)
    mainframe2left.pack(fill='both', side='left', expand='true')


# Add the Income button and switch back to homepage
def addinc_frame():
    mainframe1.pack_forget()
    mainframe1left.pack_forget()
    mainframe2left.pack_forget()
    frame_3_1.pack_forget()
    frame_3_2.pack_forget()
    mainframe1.pack(fill='both', side='right', expand='true')
    frame_8_1.pack(padx=13, pady=10)
    mainframe3left.pack(fill='both', side='left', expand='true')


def home_frame():
    mainframe2left.pack_forget()
    mainframe3left.pack_forget()
    frame_6_1.pack_forget()
    frame_8_1.pack_forget()
    clear_fields()
    income_clear_fields()
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
def list_all_expenses():
    global connector, table

    table.delete(*table.get_children())

    all_data1 = connector.execute('SELECT * FROM Expenses')
    data = all_data1.fetchall()

    for values in data:
        table.insert('', END, values=values)


def list_all_expenses1():
    global connector, table3

    table3.delete(*table3.get_children())

    all_data3 = connector.execute('SELECT * FROM Expenses')
    data = all_data3.fetchall()

    for values in data:
        table3.insert('', END, values=values)


def view_expense_details():
    global table
    global date_exp, payee, note_exp, amnt_exp, MOP_exp, cate_exp
    if not table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']
    expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
    date_exp.set_date(expenditure_date)
    payee.set(values[2])
    note_exp.set(values[3])
    amnt_exp.set(values[4])
    MOP_exp.set(values[5])
    cate_exp.set(values[6])


def selected_expense_to_words():
    global table

    if not table.selection():
        mb.showerror('No expense selected!',
                     'Please select an expense from the table for us to read')
        return

    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']

    message = (f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} '
               f'for {values[3]} on {values[1]} via {values[5]} on{values[6]}"')

    mb.showinfo('Here\'s how to read your expense', message)


def remove_expense():
    if not table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return

    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']

    surety = mb.askyesno('Are you sure?',
                         f'Are you sure that you want to delete the record of {values_selected[2]}')

    if surety:
        connector.execute('DELETE FROM Expenses WHERE ID_EXP=%d' % values_selected[0])
        connector.commit()

        list_all_expenses()
        show_expsum()
        show_balance()
        mb.showinfo('Record deleted successfully!',
                    'The record you wanted to delete has been deleted successfully')


def clear_fields():
    global note_exp, payee, amnt_exp, MOP_exp, date_exp, table, cate_exp

    today_date = datetime.datetime.now().date()

    note_exp.set('')
    payee.set('')
    amnt_exp.set(0.0)
    MOP_exp.set(''), cate_exp.set(''), date_exp.set_date(today_date)
    table.selection_remove(*table.selection())


def adding_expense():
    global date_exp, payee, note_exp, amnt_exp, MOP_exp, cate_exp
    global connector

    try:
        float(amnt_exp.get())
    except:
        mb.showerror('Inappropriate Value', 'Please enter numbers in the expense entry.')
        return

    try:
        if (not date_exp.get() or not payee.get() or not note_exp.get() or not amnt_exp.get()
                or not MOP_exp.get() or not cate_exp.get()):
            mb.showerror('Fields empty!',
                         "Please fill all the missing fields before pressing the add button!")
        else:
            connector.execute('INSERT INTO Expenses (Date_EXP, Payee, Note_EXP, Amount_EXP, ModeOfPayment_EXP, '
                              'Category_EXP)'
                              'VALUES (?,?,?,ROUND(?,1),?,?)', (date_exp.get_date(), payee.get(), note_exp.get(),
                                                                amnt_exp.get(), MOP_exp.get(), cate_exp.get()))
            connector.commit()
            clear_fields()
            list_all_expenses()
            show_expsum()
            show_balance()
            mb.showinfo('Expense Added',
                        'The expense  has been added to the database.')
    except sqlite3.IntegrityError:
        mb.showerror("Error", "Expense already exists. Try again.")


def edit_expense():
    global table

    def edit_existing_expense():
        global date_exp, amnt_exp, note_exp, payee, MOP_exp, cate_exp
        global connector, table
        current_selected_expenditure = table.item(table.focus())
        contents = current_selected_expenditure['values']

        try:
            float(amnt_exp.get())
        except:
            mb.showerror('Inappropriate Value', 'Please enter numbers in the expense entry.')
            return

        try:
            if (not date_exp.get() or not payee.get() or not note_exp.get() or not amnt_exp.get()
                    or not MOP_exp.get() or not cate_exp.get()):
                mb.showerror('Fields empty!',
                             "Please fill all the missing fields before pressing the add button!")
            else:
                connector.execute(
                    'UPDATE Expenses SET Date_EXP = ?, Payee = ?, Note_EXP = ?, Amount_EXP = ROUND(?,1),'
                    'ModeOfPayment_EXP = ?, Category_EXP = ? WHERE ID_EXP = ?',
                    (date_exp.get_date(), payee.get(), note_exp.get(), amnt_exp.get(),
                     MOP_exp.get(), cate_exp.get(), contents[0]))
                connector.commit()
                clear_fields()
                list_all_expenses()
                show_expsum()
                show_balance()
                mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
                saveedit_button1.destroy()
                return
        except sqlite3.IntegrityError:
            mb.showerror("Error", "Expense already exists. Try again.")

    if not table.selection():
        mb.showerror('No expense selected',
                     'You have not selected any expense in the table to edit; please do that!')
        return

    view_expense_details()
    saveedit_button1 = CTkButton(master=mainframe2left, text='Save Edit', command=edit_existing_expense,
                                 corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                                 fg_color="#000000")
    saveedit_button1.place(relx=0.3, rely=0.7)

    # if clear_fields():
    #     saveedit_button1.destroy()


# UI Display Function

def show_expsum():
    cursor1.execute('SELECT Amount_EXP FROM Expenses')
    result1 = cursor1.fetchall()

    total1 = sum(float(row[0]) for row in result1)
    moneycounter.configure(text="RM {:.2f}".format(total1))


##############################################################################
# Functions for 'Income' menu
##############################################################################

def list_all_income():
    global connector, table2

    table2.delete(*table2.get_children())

    all_data2 = connector.execute('SELECT * FROM Income')
    data = all_data2.fetchall()

    for values in data:
        table2.insert('', END, values=values)


def list_all_income1():
    global connector, table4

    table4.delete(*table4.get_children())

    all_data4 = connector.execute('SELECT * FROM Income')
    data = all_data4.fetchall()

    for values in data:
        table4.insert('', END, values=values)


def selected_income_to_words():
    global table2

    if not table2.selection():
        mb.showerror('No income selected!',
                     'Please select an income from the table for us to read')
        return

    current_selected_income = table2.item(table2.focus())
    values = current_selected_income['values']

    message = (f'Your income can be read like: \n"{values[2]} paid to you {values[4]}'
               f' for {values[3]} on {values[1]} via {values[5]} on {values[6]}"')

    mb.showinfo('Here\'s how to read your income', message)


def remove_income():
    if not table2.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return

    current_selected_income = table2.item(table2.focus())
    values_selected = current_selected_income['values']

    surety = mb.askyesno('Are you sure?',
                         f'Are you sure that you want to delete the record of {values_selected[2]}')

    if surety:
        connector.execute('DELETE FROM Income WHERE ID_INC=%d' % values_selected[0])
        connector.commit()

        list_all_income()
        show_incsum()
        show_balance()
        mb.showinfo('Record deleted successfully!',
                    'The record you wanted to delete has been deleted successfully')


def income_clear_fields():
    global note_inc, payer, amnt_inc, MOP_inc, table2, date_inc, cate_inc

    today_date = datetime.datetime.now().date()

    note_inc.set('')
    payer.set('')
    amnt_inc.set(0.00)
    MOP_inc.set(''), cate_inc.set(''), date_inc.set_date(today_date)
    table2.selection_remove(*table2.selection())


def adding_income():
    global note_inc, payer, amnt_inc, MOP_inc, date_inc, table2, cate_inc
    global connector

    try:
        float(amnt_inc.get())
    except ValueError:
        mb.showerror('Inappropriate Value', 'Please enter numbers in the income entry.')
        return

    try:
        # Check if any of the required fields are empty
        if (not date_inc.get() or not payer.get() or not note_inc.get() or not amnt_inc.get()
                or not MOP_inc.get() or not cate_inc.get()):
            mb.showerror('Fields empty!',
                         "Please fill all the missing fields before pressing the add button!")
        else:
            # If all fields are filled, insert the data into the database
            connector.execute('INSERT INTO Income (Date_INC, Payer_INC, Note_INC, Amount_INC, '
                              'ModeOfPayment_INC, Category_INC) VALUES (?, ?, ?, '
                              'ROUND(?,1), ?, ?)',
                              (date_inc.get_date(), payer.get(), note_inc.get(), amnt_inc.get(),
                               MOP_inc.get(), cate_inc.get()))
            connector.commit()

            income_clear_fields()
            list_all_income()
            show_incsum()
            show_balance()
            # Show an info message
            mb.showinfo('Income added',
                        'The income whose details you just entered has been added to the database')
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


def edit_income():
    global table2

    def edit_existing_income():
        global date_inc, amnt_inc, note_inc, payee, MOP_inc, cate_inc
        global connector, table2

        current_selected_income = table2.item(table2.focus())
        contents = current_selected_income['values']

        try:
            float(amnt_inc.get())
        except ValueError:
            mb.showerror('Inappropriate Value', 'Please enter numbers in the income entry.')
            return

        try:
            if (not date_inc.get() or not payer.get() or not note_inc.get() or not amnt_inc.get()
                    or not MOP_inc.get() or not cate_inc.get()):
                mb.showerror('Fields empty!',
                             "Please fill all the missing fields before pressing the add button!")
            else:

                connector.execute(
                    'UPDATE Income SET Date_INC = ?, Payer_INC = ?, Note_INC = ?, Amount_INC = ROUND(?,1), '
                    'ModeOfPayment_INC = ?,'
                    'Category_INC = ? WHERE ID_INC = ?',
                    (date_inc.get_date(), payer.get(), note_inc.get(), amnt_inc.get(),
                     MOP_inc.get(), cate_inc.get(), contents[0]))
                connector.commit()
                income_clear_fields()
                list_all_income()
                show_balance()
                mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
                saveedit_button2.destroy()
                return
        except sqlite3.IntegrityError:
            mb.showerror("Error", "Income already exists. Try again.")

    if not table2.selection():
        mb.showerror('No income selected!',
                     'You have not selected any income in the table for us to edit; please do that!')
        return

    view_income_details()
    saveedit_button2 = CTkButton(master=mainframe3left, text='Save Edit', command=edit_existing_income,
                                 corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                                 fg_color="#000000")
    saveedit_button2.place(relx=0.3, rely=0.7)


def show_incsum():
    cursor2.execute('SELECT Amount_INC FROM Income')
    result2 = cursor2.fetchall()

    total2 = sum(float(row[0]) for row in result2)
    inccounter.configure(text="RM {:.2f}".format(total2))


# Display Balance
def show_balance():
    cursor1.execute('SELECT Amount_EXP FROM Expenses')
    result3 = cursor1.fetchall()
    total3 = sum(float(row[0]) for row in result3)

    cursor2.execute('SELECT Amount_INC FROM Income')
    result4 = cursor2.fetchall()
    total4 = sum(float(row[0]) for row in result4)

    total5 = total4 - total3

    balancecounter.configure(text="RM {:.2f}".format(total5))


##############################################################################
# Right mainframe (Home)
##############################################################################
mainframe1 = CTkFrame(master=money_app, fg_color="#000000", height=750, width=1150, corner_radius=0)
mainframe1.pack(fill='both', side='right', expand='true')

##############################################################################
# Frame 1 (invisible)
##############################################################################
frame_1 = CTkFrame(master=mainframe1, fg_color="#000000", height=150)
frame_1.pack(fill='x', padx=10, pady=10)

frame_1_1 = CTkFrame(master=frame_1, height=150)
frame_1_1.pack(fill='x')

welclabel = CTkLabel(master=frame_1_1, text='Welcome, User', font=('Microsoft YaHei UI Light', 18))
welclabel.place(anchor='center', relx=0.5, rely=0.2)

Bcounter = CTkLabel(master=frame_1_1, text='Balance', font=('Microsoft YaHei UI Light', 18))
Bcounter.place(relx=0.02, rely=0.33)

balancecounter = CTkLabel(master=frame_1_1, text="", font=('Microsoft YaHei UI Light', 50))
balancecounter.place(relx=0.02, rely=0.5)
show_balance()

##############################################################################
# Frame 2 (invisible)
##############################################################################

frame_2 = CTkFrame(master=mainframe1, fg_color="#000000", height=200)
frame_2.pack(fill='x', padx=10, pady=10)

##############################################################################
# Left Frame in Frame 2
##############################################################################

frame_2_1 = CTkFrame(master=frame_2, height=100, width=575)
frame_2_1.pack(side='left', padx=1, pady=1)

Mcounter = CTkLabel(master=frame_2_1, text='Expenses', font=('Microsoft YaHei UI Light', 18))
Mcounter.place(relx=0.02, rely=0.2)

moneycounter = CTkLabel(master=frame_2_1, text="", font=('Microsoft YaHei UI Light', 25))
moneycounter.place(relx=0.02, rely=0.5)

##############################################################################
# Right Frame in Frame 2
##############################################################################

frame_2_2 = CTkFrame(master=frame_2, height=100, width=575)
frame_2_2.pack(side='right', padx=1, pady=1)

Icounter = CTkLabel(master=frame_2_2, text='Income', font=('Microsoft YaHei UI Light', 18))
Icounter.place(relx=0.02, rely=0.2)

inccounter = CTkLabel(master=frame_2_2, text="", font=('Microsoft YaHei UI Light', 25))
inccounter.place(relx=0.02, rely=0.5)

##############################################################################
# Frame 3_1
##############################################################################

frame_3_1 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", width=575, height=650, border_width=2)
frame_3_1.pack(side='left', padx=13, pady=10)

##############################################################################
# Expenses Treeview Frame (Homepage)
##############################################################################

table3 = ttk.Treeview(frame_3_1, selectmode=BROWSE,
                      columns=('ID', 'Date', 'Payee', 'Note', 'Amount', 'Mode of Payment', 'Category'))

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
table3.column('#1', width=50, stretch=NO)
table3.column('#2', width=95, stretch=NO)  # Date column
table3.column('#3', width=150, stretch=NO)  # Payee column
table3.column('#4', width=255, stretch=NO)  # Title column
table3.column('#5', width=135, stretch=NO)  # Amount column
table3.column('#6', width=105, stretch=NO)  # Mode of Payment column
table3.column('#7', width=105, stretch=NO)  # Category column

table3.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses1()
show_expsum()

##############################################################################
# Frame 3_2
##############################################################################

frame_3_2 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", width=575, height=650, border_width=2)
frame_3_2.pack(side='right', padx=13, pady=10)

##############################################################################
# Income Treeview Frame (Homepage)
##############################################################################

table4 = ttk.Treeview(frame_3_2, selectmode=BROWSE, columns=('ID', 'Date', 'Payer', 'Note', 'Amount',
                                                             "Mode of Payment", 'Category'))

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
table4.column('#1', width=50, stretch=NO)
table4.column('#2', width=95, stretch=NO)  # Date column
table4.column('#3', width=150, stretch=NO)  # Payer column
table4.column('#4', width=255, stretch=NO)  # Title column
table4.column('#5', width=135, stretch=NO)  # Amount column
table4.column('#6', width=105, stretch=NO)  # Mode of Payment column
table4.column('#7', width=105, stretch=NO)  # Category column

table4.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_income1()
show_incsum()

##############################################################################
# Left mainframe (Home)
##############################################################################

mainframe1left = CTkFrame(master=money_app, height=750, width=350, corner_radius=0)
mainframe1left.pack(fill='both', side='left', expand='true')
mainframe1left.configure(fg_color="#E64900")

addexpbut = CTkButton(master=mainframe1left, text='Add Expense', height=50, font=('Microsoft YaHei UI Light', 15),
                      hover_color="#808080",
                      fg_color="#000000", command=addexp_frame)
addexpbut.place(anchor='center', relx=0.5, rely=0.1)
addincbut = CTkButton(master=mainframe1left, text='Add Income', height=50, font=('Microsoft YaHei UI Light', 15),
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
##############################################################################
# Functions to clear the text in the entry exp_amount
##############################################################################
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
                        corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                        fg_color="#000000", )
save_button.place(relx=0.3, rely=0.7)

homepage_button = CTkButton(master=mainframe2left, text='Back to Home Page', command=home_frame,
                            corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                            fg_color="#000000")
homepage_button.place(relx=0.3, rely=0.75)

delexp_button = CTkButton(master=mainframe2left, text='Delete Expense', command=remove_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
delexp_button.place(relx=0.3, rely=0.80)

selexp_button = CTkButton(master=mainframe2left, text='Edit Selected Expense', command=edit_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
selexp_button.place(relx=0.3, rely=0.85)

senexp_button = CTkButton(master=mainframe2left, text='Convert Expense to a Sentence',
                          command=selected_expense_to_words,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
senexp_button.place(relx=0.22, rely=0.90)

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

table = ttk.Treeview(frame_6_1, selectmode=BROWSE,
                     columns=('ID', 'Date', 'Payee', 'Note', 'Amount', 'Mode of Payment', 'Category'))

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
table.column('#1', width=50, stretch=NO)
table.column('#2', stretch=YES)  # Date column
table.column('#3', stretch=YES)  # Payee column
table.column('#4', width=300, stretch=NO)  # Note column
table.column('#5', stretch=YES)  # Amount column
table.column('#6', stretch=YES)  # Mode of Payment column
table.column('#7', stretch=YES)  # Category column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()
show_expsum()

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
##############################################################################
# Functions to clear the text in the entry inc_amount
##############################################################################
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

save_button = CTkButton(master=mainframe3left, text='Save', command=adding_income,
                        corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                        fg_color="#000000")
save_button.place(relx=0.3, rely=0.7)

homepage_button = CTkButton(master=mainframe3left, text='Back to Home Page', command=home_frame,
                            corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                            fg_color="#000000")
homepage_button.place(relx=0.3, rely=0.75)

delinc_button = CTkButton(master=mainframe3left, text='Delete Income', command=remove_income,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
delinc_button.place(relx=0.3, rely=0.80)

selinc_button = CTkButton(master=mainframe3left, text='Edit Selected Income', command=edit_income,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
selinc_button.place(relx=0.3, rely=0.85)

seninc_button = CTkButton(master=mainframe3left, text='Convert Income to a Sentence', command=selected_income_to_words,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
seninc_button.place(relx=0.22, rely=0.90)

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

table2 = ttk.Treeview(frame_8_1, selectmode=BROWSE, columns=('ID', 'Date', 'Payer', 'Note', 'Amount',
                                                             "Mode of Payment", 'Category'))

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
table2.column('#1', width=50, stretch=NO)
table2.column('#2', stretch=YES)  # Date column
table2.column('#3', stretch=YES)  # Payer column
table2.column('#4', width=300, stretch=NO)  # Note column
table2.column('#5', stretch=YES)  # Amount column
table2.column('#6', stretch=YES)  # Mode of Payment column
table2.column('#7', stretch=YES)  # Category column

table2.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_income()

# Let the Home Menu appear first

frame_6_1.pack_forget()
frame_8_1.pack_forget()

money_app.mainloop()

cursor1.close()
cursor2.close()
connector.close()
