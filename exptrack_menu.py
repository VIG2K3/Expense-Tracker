from customtkinter import *
from PIL import ImageTk, Image
import time

money_app = CTk()
money_app.geometry("900x700")
money_app.resizable(False, False)

set_appearance_mode("light")

img = ImageTk.PhotoImage(file='profile_icon_adjusted.png')

# Functions for Home Menu

def exphover(a):
    addexpbut.configure(fg_color= "#6500C3")
def expnothover(a):
    addexpbut.configure(fg_color= '#7d57f8')

def inchover(a):
    addincbut.configure(fg_color="#6500C3")

def incnothover(a):
    addincbut.configure(fg_color="#7d57f8")

def addexp_frame():
    mainframe1.pack_forget()
    mainframe2.pack(fill='both', expand='true')

def home_frame():
    mainframe2.pack_forget()
    mainframe1.pack()

# Main Frame (Home)
mainframe1 = CTkFrame(master=money_app, fg_color="#ebebeb", height=700, width=900)
mainframe1.pack(fill='both')

# Frame 1 (invisible)

frame_1 = CTkFrame(master=mainframe1, fg_color="#ebebeb", height=150)
frame_1.pack(fill='x', padx=2, pady=2)

frame_1_1 = CTkFrame(master=frame_1, fg_color="#dec0ff", height=150)
frame_1_1.pack(fill='x')

welclabel = CTkLabel(master=frame_1_1, text='Welcome, User', font=('Arial', 15))
welclabel.place(relx=0.025, rely=0.07)
moneycounter = CTkLabel(master=frame_1_1, text=f'RM XXXX.XX', fg_color='#7d57f8', width=400 , height=50, font=('Arial', 15), corner_radius=20)
moneycounter.place(anchor='center', relx=0.5, rely=0.5)
# profile = CTkButton(master=frame_1_1, image=img)
# profile.place(relx=0.9, rely=0.1)

# Frame 2 (invisible)

frame_2 = CTkFrame(master=mainframe1, fg_color="#ebebeb", height=125)
frame_2.pack(fill='x', padx=2, pady=2)

# Left Frame in Frame 2

frame_2_1 = CTkFrame(master=frame_2, fg_color="#e9d6ff", height=125, width=446)
frame_2_1.pack(side='left')

addexpbut = CTkButton(master=frame_2_1, text='Add Expenses', fg_color='#7d57f8', height=50, font=('Arial', 15), command=addexp_frame)
addexpbut.place(anchor='center', relx=0.3, rely=0.5)
addincbut = CTkButton(master=frame_2_1, text='Add Income', fg_color="#7d57f8", height=50, font=('Arial', 15))
addincbut.place(anchor='center', relx=0.7, rely=0.5)

# Right Frame in Frame 2

frame_2_2 = CTkFrame(master=frame_2, fg_color="#e9d6ff", height=125, width=446)
frame_2_2.pack(side='right')

catlabel = CTkLabel(master=frame_2_2, text='Categories', font=('Arial', 15))
catlabel.place(relx=0.05, rely=0.07)

placeholder1 = CTkButton(master=frame_2_2, text='pholder', fg_color='#7d57f8', width=30)
placeholder1.place(anchor='center', relx=0.25, rely=0.5)
placeholder2 = CTkButton(master=frame_2_2, text='pholder', fg_color="#7d57f8", width=30)
placeholder2.place(anchor='center', relx=0.5, rely=0.5)
placeholder3 = CTkButton(master=frame_2_2, text='pholder', fg_color="#7d57f8", width=30)
placeholder3.place(anchor='center', relx=0.75, rely=0.5)

# Frame 3

frame_3 = CTkFrame(master=mainframe1, fg_color="#dec0ff", height=300)
frame_3.pack(fill='x', padx=2, pady=2)

# Frame 4

frame_4 = CTkFrame(master=mainframe1, fg_color="#e9d6ff", height=125)
frame_4.pack(fill='x', padx=2, pady=2)

# Button Binds
addexpbut.bind('<Enter>', exphover)
addexpbut.bind('<Leave>', expnothover)
addincbut.bind('<Enter>', inchover)
addincbut.bind('<Leave>', incnothover)

# Functions for 'Add Expenses' menu

def save_text():
    edited_text = addexp_entry.get()
    # selected_option = optionmenu_var.get()
    print(f"Edited Text: {edited_text}")


def optionmenu_callback(choice):
    print(f"Selected Option: {choice}")


def button_command(category):
    print(f"Button clicked for category: {category}")


# def save_text():
#     edited_text = addexp_entry.get()
#     # selected_option = optionmenu_var.get()
#     print(f"Edited Text: {edited_text}, Selected Option: {selected_option}")



# Main Frame (Add Expense)
mainframe2 = CTkFrame(master=money_app, fg_color="#ebebeb", height=700, width=900)
mainframe2.pack()

# Frame 5
frame_5 = CTkFrame(master=mainframe2, fg_color="#dec0ff", height=200)
frame_5.pack(fill='x', padx=2, pady=2)

# New Expense heading
heading = CTkLabel(master=frame_5, text='NEW EXPENSE', fg_color="#FFFFFF", font=('Arial', 23), corner_radius=30)
heading.place(x=450, y=40, anchor='center')

save_button = CTkButton(master=frame_5, text='Save', command=save_text)
save_button.place(relx=0.75, rely=0.45)

homepage_button = CTkButton(master=frame_5, text="Switch to Home Page", command=home_frame)
homepage_button.place(relx=0.0, rely=0.0)

# Add New Expense

def clear_addexp_entry(event):
    if addexp_entry.get() == 'Add New Expense Amount':
        addexp_entry.delete(0, 'end')


def reset_addexp_entry(event):
    if addexp_entry.get() == '':
        addexp_entry.insert(0, 'Add New Expense Amount')


addexp_entry = CTkEntry(master=frame_5, fg_color="#FFFFFF", width=400, height=50,
                        corner_radius=10, justify="center")
addexp_entry.place(relx=0.28, rely=0.40)
addexp_entry.insert(0, "Add New Expense Amount")
addexp_entry.bind('<FocusIn>', clear_addexp_entry)
addexp_entry.bind('<FocusOut>', reset_addexp_entry)

# Currency Box
optionmenu_var = StringVar()

currency_box = CTkOptionMenu(master=frame_5, values=["MYR", "USD", "SGD", "AUD", "RMB", "EUR", "POUND"],
                             text_color='#000000', bg_color="#000000", fg_color="#FFFFFF", width=100, height=40
                             , command=optionmenu_callback, variable=optionmenu_var)
currency_box.place(relx=0.10, rely=0.40)

# Frame 6
frame_6 = CTkFrame(master=mainframe2, fg_color="#e9d6ff", height=500)
frame_6.pack(fill='x', padx=2, pady=2)

# Category button (Car)
catcar_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='CAR', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catcar_button.place(relx=0.04, rely=0.05)

# Category button (Bills)
catbills_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='BILLS', text_color='#000000',
                            fg_color="#FFFFFF", border_width=0)
catbills_button.place(relx=0.29, rely=0.05)

# Category button (Shopping)
catshop_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='SHOPPING', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catshop_button.place(relx=0.54, rely=0.05)

# Category button (House)
cathouse_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='HOUSE', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
cathouse_button.place(relx=0.79, rely=0.05)

# Category button (F&B)
catfnb_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='F&B', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catfnb_button.place(relx=0.04, rely=0.35)

# Category button (Entertainment)
catenter_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='ENTERTAINMENT',
                          text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catenter_button.place(relx=0.29, rely=0.35)

# Category button (Transport)
cattran_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='TRANSPORT', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
cattran_button.place(relx=0.54, rely=0.35)

# Category button (Pets)
catpets_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='PETS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catpets_button.place(relx=0.79, rely=0.35)

# Category button (Deposit)
catdep_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='DEPOSIT', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catdep_button.place(relx=0.04, rely=0.65)

# Category button (Salary)
catsal_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='SALARY', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catsal_button.place(relx=0.29, rely=0.65)

# Category button (Savings)
catsav_button = CTkButton(master=frame_6, compound="top", width=150, height=100, text='SAVINGS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catsav_button.place(relx=0.54, rely=0.65)


# Let Home Menu appear first
mainframe2.pack_forget()

money_app.mainloop()
