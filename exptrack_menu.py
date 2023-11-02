from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import tkinter.messagebox as mb
import sv_ttk
import sqlite3

# Connecting to the Database
connector = sqlite3.connect("Expense Tracker Expenses.db")
cursor = connector.cursor()

cursor.execute(
    'CREATE TABLE IF NOT EXISTS Expenses '
    '(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
    'Date DATETIME, '
    'Payee TEXT, '
    'Note TEXT, '
    'Amount FLOAT, '
    'ModeOfPayment TEXT, '
    'Category VARCHAR(20),'
    'CONSTRAINT unique_exp UNIQUE (Date, Note))'
)
connector.commit()

money_app = CTk()
money_app.resizable(False, False)
money_app.geometry("1250x700")
money_app.title("Expense Tracker")

set_appearance_mode("light")
sv_ttk.set_theme("light")

# Functions
# Menu Functions
def light_dark_mode(): # Switch between light/dark mode
    ld = lightdark.get()

    if ld:
        set_appearance_mode("dark")
        sv_ttk.set_theme("dark")
        mainframe1left.configure(fg_color="#952f00")
    else:
        set_appearance_mode("light")
        sv_ttk.set_theme("light")
        mainframe1left.configure(fg_color="#E64900")

def addexp_frame():
    mainframe1.pack_forget()
    mainframe1left.pack_forget()
    mainframe2.pack(fill='both', expand='true')

def home_frame():
    mainframe2.pack_forget()
    mainframe1.pack(fill='both', side='right', expand='true')
    mainframe1left.pack(fill='both', side='left', expand='true')
    list_all_expenses()
    show_expsum()

# Functions for 'Expenses' menu
def list_all_expenses():
    global connector, table

    table.delete(*table.get_children())

    all_data = connector.execute('SELECT * FROM Expenses')
    data = all_data.fetchall()

    for values in data:
        table.insert('', END, values=values)

def view_expense_details():
    global table
    global date, payee, note, amnt, MoP, cate
    if not table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']
    expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
    date.set_date(expenditure_date)
    payee.set(values[2])
    note.set(values[3])
    amnt.set(values[4])
    MoP.set(values[5])
    cate.set(values[6])

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
        connector.execute('DELETE FROM Expenses WHERE ID=%d' % values_selected[0])
        connector.commit()

        list_all_expenses()
        mb.showinfo('Record deleted successfully!',
                    'The record you wanted to delete has been deleted successfully')

# def remove_all_expenses():
#     surety = mb.askyesno('Are you sure?',
#                          "Are you sure that you want to delete all the expense items from the database?",
#                          icon='warning')
#
#     if surety:
#         table.delete(*table.get_children())
#
#         connector.execute('DELETE FROM Expenses')
#         connector.commit()
#
#         clear_fields()
#         list_all_expenses()
#         mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
#     else:
#         mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

def clear_fields():
    global note, payee, amnt, MoP, date, table, cate

    today_date = datetime.datetime.now().date()

    note.set('')
    payee.set('')
    amnt.set(0.0)
    MoP.set('Select Method'), cate.set('Select Method'), date.set_date(today_date)
    table.selection_remove(*table.selection())

def adding_expense():
    global date, payee, note, amnt, MoP, cate
    global connector

    try:
        float(amnt.get())
    except:
        mb.showerror('Inappropriate Value', 'Please enter numbers in the expense entry.')

    try:
        if not date.get() or not payee.get() or not note.get() or not amnt.get() or not MoP.get() or not cate.get():
            mb.showerror('Fields empty!',
                     "Please fill all the missing fields before pressing the add button!")
        else:
            connector.execute('INSERT INTO Expenses (Date, Payee, Note, Amount, ModeOfPayment, Category) '
                          'VALUES (?,?,?,ROUND(?,1),?,?)', (date.get_date(), payee.get(), note.get(),
                                                   amnt.get(), MoP.get(), cate.get()))
            connector.commit()
            clear_fields()
            list_all_expenses()
            mb.showinfo('Expense Added',
                    'The expense  has been added to the database.')
    except sqlite3.IntegrityError:
        mb.showerror("Error", "Expense already exists. Try Again.")


def edit_expense():
    global table

    def edit_existing_expense():
        global date, amnt, note, payee, MoP, cate
        global connector, table
        current_selected_expenditure = table.item(table.focus())
        contents = current_selected_expenditure['values']
        connector.execute(
            'UPDATE Expenses SET Date = ?, Payee = ?, Note = ?, Amount = ROUND(?,1),'
            ' ModeOfPayment = ?, Category = ? WHERE ID = ?',
            (date.get_date(), payee.get(), note.get(), amnt.get(), MoP.get(), cate.get(), contents[0]))
        connector.commit()
        clear_fields()
        list_all_expenses()
        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
        return

    if not table.selection():
        mb.showerror('No expense selected!',
                     'You have not selected any expense in the table for us to edit; please do that!')
        return
    view_expense_details()
    saveedit_button = CTkButton(master=frame_5, text='Save Edit', command=edit_existing_expense,
                            corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13),
                            fg_color="#000000", )
    saveedit_button.place(relx=0.75, rely=0.30)
    saveedit_button.destroy()

# UI Display Function

def show_expsum():
    cursor.execute('SELECT Amount FROM Expenses')
    result = cursor.fetchall()

    total = sum(float(row[0]) for row in result)
    moneycounter.configure(text="RM {:.2f}".format(total))

# Left mainframe (Home)
mainframe1left = CTkFrame(master=money_app, height=700, width=350, corner_radius=0)
mainframe1left.pack(fill='both', side='left', expand='true')
mainframe1left.configure(fg_color="#E64900")

lightdark = CTkSwitch(master=mainframe1left, text="Dark Mode", command=light_dark_mode,
                      onvalue=1, offvalue=0)
lightdark.place(relx=0.05, rely=0.93)

# Right mainframe (Home)
mainframe1 = CTkFrame(master=money_app, fg_color="#000000", height=700, width=900, corner_radius=0)
mainframe1.pack(fill='both', side='right', expand='true')

# Frame 1 (invisible)

frame_1 = CTkFrame(master=mainframe1, fg_color="#000000", height=150)
frame_1.pack(fill='x', padx=2, pady=2)

frame_1_1 = CTkFrame(master=frame_1, height=150)
frame_1_1.pack(fill='x')

welclabel = CTkLabel(master=frame_1_1, text='Welcome, User', font=('Microsoft YaHei UI Light', 18))
welclabel.place(anchor='center', relx=0.5, rely=0.2)

Balancecounter = CTkLabel(master=frame_1_1, text='Expenses', font=('Microsoft YaHei UI Light', 18))
Balancecounter.place(relx=0.02, rely=0.33)

moneycounter = CTkLabel(master=frame_1_1, text="", font=('Microsoft YaHei UI Light', 50))
moneycounter.place(relx=0.02, rely=0.5)

# Frame 2 (invisible)

frame_2 = CTkFrame(master=mainframe1, fg_color="#000000", height=200)
frame_2.pack(fill='x', padx=2, pady=2)

# Left Frame in Frame 2

frame_2_1 = CTkFrame(master=frame_2, height=100, width=450)
frame_2_1.pack(side='left', padx=1, pady=1)

addexpbut = CTkButton(master=frame_2_1, text='Add Expense', height=50, font=('Microsoft YaHei UI Light', 15), hover_color="#808080",
                      fg_color="#000000", command=addexp_frame)
addexpbut.place(anchor='center', relx=0.3, rely=0.5)
addincbut = CTkButton(master=frame_2_1, text='Add Income', height=50, font=('Microsoft YaHei UI Light', 15),
                      hover_color="#808080", fg_color="#000000", command=show_expsum)
addincbut.place(anchor='center', relx=0.7, rely=0.5)

# Right Frame in Frame 2

frame_2_2 = CTkFrame(master=frame_2, height=100, width=450)
frame_2_2.pack(side='right', padx=1, pady=1)

Balancecounter = CTkLabel(master=frame_2_2, text='Set A Budget', font=('Microsoft YaHei UI Light', 20), corner_radius=20, )
Balancecounter.place(relx=0.05, rely=0.07)

setbudget = CTkEntry(master=frame_2_2, height=25, width=150, font=('Arial', 15), corner_radius=10)
setbudget.place(relx=0.1, rely=0.5)

budget_button = CTkButton(master=frame_2_2, text='Save', corner_radius=20, hover_color="#808080", fg_color="#000000")
budget_button.place(relx=0.5, rely=0.4)

# Frame 3_1

frame_3_1 = CTkFrame(master=mainframe1, fg_color="#FFFFFF", width=450, height=650, border_width=2)
frame_3_1.pack(fill='x', padx=20, pady=20)

# Treeview Frame (Homepage)
table = ttk.Treeview(frame_3_1, selectmode=BROWSE,
                     columns=('ID', 'Date', 'Payee', 'Note', 'Amount', 'Mode of Payment', 'Category'))

X_Scroller = CTkScrollbar(table, orientation=HORIZONTAL, command=table.xview)
Y_Scroller = CTkScrollbar(table, orientation=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Note', text='Note', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table.heading('Category', text='Category', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=270, stretch=NO)  # Note column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=205, stretch=NO)  # Mode of Payment column
table.column('#7', width=105, stretch=NO)  # Category column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()

# Main Frame (Expenses)
mainframe2 = CTkFrame(master=money_app, fg_color="#ebebeb", height=700, width=900)
mainframe2.pack()

# StringVar and DoubleVar variables (Add Expense)
note = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar()
cate = StringVar()

# Frame 5
frame_5 = CTkFrame(master=mainframe2, fg_color="#FFFFFF", height=150)
frame_5.pack(fill='x', padx=2, pady=2)

# New Expense heading
heading = CTkLabel(master=frame_5, text='EXPENSES', fg_color="#FFFFFF", font=('Microsoft YaHei UI Light', 23, 'bold'), corner_radius=30)
heading.place(relx=0.50, rely=0.20, anchor='center')

# Add or Edit Expense

def clear_addexp_entry(event):
    if addexp_entry.get() == '0.0':
        addexp_entry.delete(0, 'end')

def reset_addexp_entry(event):
    if addexp_entry.get() == '':
        addexp_entry.insert(0, 0.0)


addexp_entry = CTkEntry(master=frame_5, fg_color="#FFFFFF", width=250, height=40,
                        corner_radius=10, justify="center", textvariable=amnt)
addexp_entry.place(relx=0.36, rely=0.35)
addexp_entry.insert(0, '')
addexp_entry.bind('<FocusIn>', clear_addexp_entry)
addexp_entry.bind('<FocusOut>', reset_addexp_entry)

# Button in Frame 5
save_button = CTkButton(master=frame_5, text='Save', command=adding_expense,
                        corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000", )
save_button.place(relx=0.75, rely=0.30)

homepage_button = CTkButton(master=frame_5, command=home_frame, text='Back to Home Page',
                            corner_radius=5, hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
homepage_button.place(relx=0.0, rely=0.0)

delexp_button = CTkButton(master=frame_5, text='Delete Expense', command=remove_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
delexp_button.place(relx=0.75, rely=0.70)

selexp_button = CTkButton(master=frame_5, text='Edit Selected Expense', command=edit_expense,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
selexp_button.place(relx=0.42, rely=0.70)

senexp_button = CTkButton(master=frame_5, text='Convert Expense to a sentence', command=selected_expense_to_words,
                          hover_color="#808080", font=('Microsoft YaHei UI Light', 13), fg_color="#000000")
senexp_button.place(relx=0.10, rely=0.70)

# Frame6_1
frame_6_1 = CTkFrame(master=mainframe2, fg_color="#FFFFFF", height=600, width=450, border_width=2)
frame_6_1.pack(side='left')

Date = CTkLabel(master=frame_6_1, text='Date (MM/DD/YY):')
Date.place(x=10, y=50)

date = DateEntry(master=frame_6_1, date=datetime.datetime.now().date())
date.place(x=160, y=65)

Payee_Label = CTkLabel(master=frame_6_1, text='Payee : ')
Payee_Label.place(x=10, y=260)

Payee_Entry = CTkEntry(master=frame_6_1, textvariable=payee)
Payee_Entry.place(x=55, y=260)

Note_Label = CTkLabel(frame_6_1, text='Note  :').place(x=10, y=130)
Note_Entry = CTkEntry(frame_6_1, textvariable=note, width=200, height=100).place(x=50, y=130)

CTkLabel(master=frame_6_1, text='Mode of Payment:').place(x=10, y=310)
dd1 = OptionMenu(frame_6_1, MoP,
                 *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Google Pay',
                   'E-Wallet'], )
dd1.place(x=160, y=390)
dd1.configure(width=10)

CTkLabel(master=frame_6_1, text='Category:').place(x=10, y=350)
category = OptionMenu(frame_6_1, cate,
                      *['Automotive', 'Grocery', 'Hobby', 'Utility'])
category.place(x=160, y=440)
category.configure(width=10)

# Frame6_2 (Expense Table)
frame_6_2 = CTkFrame(master=mainframe2, fg_color="#FFFFFF", height=600, width=450, border_width=2)
frame_6_2.pack(side='right')

table = ttk.Treeview(frame_6_2, selectmode=BROWSE,
                     columns=('ID', 'Date', 'Payee', 'Note', 'Amount', 'Mode of Payment', 'Category'))

X_Scroller = CTkScrollbar(table, orientation=HORIZONTAL, command=table.xview)
Y_Scroller = CTkScrollbar(table, orientation=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Note', text='Note', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table.heading('Category', text='Category', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=255, stretch=NO)  # Title column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=105, stretch=NO)  # Mode of Payment column
table.column('#7', width=105, stretch=NO)  # Category column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()
show_expsum()

# Let Home Menu appear first
mainframe2.pack_forget()
money_app.mainloop()



connector.close()



