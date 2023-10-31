from customtkinter import *
import PIL

money_app = CTk()
money_app.geometry("900x700")
money_app.resizable(False, False)

set_appearance_mode("light")


# Button definition

def save_text():
    edited_text = addin_entry.get()
    selected_option = optionmenu_var.get()
    print(f"Edited Text: {edited_text}")


def optionmenu_callback(choice):
    print(f"Selected Option: {choice}")


def button_command(category):
    print(f"Button clicked for category: {category}")


def save_text():
    edited_text = addin_entry.get()
    selected_option = optionmenu_var.get()
    print(f"Edited Text: {edited_text}, Selected Option: {selected_option}")


def switch_to_homepage():
    money_app.place_forget()
    homepage_button.place(relx=0.0, rely=0.0)


# Frame 1
frame_1 = CTkFrame(master=money_app, fg_color="#000000", height=200)
frame_1.pack(fill='x', padx=2, pady=2)

# New Expense heading
heading = CTkLabel(master=frame_1, text='NEW INCOME', fg_color="#FFFFFF", font=('Arial', 23), corner_radius=30)
heading.place(x=450, y=40, anchor='center')


# Add New Income

def clear_addin_entry(event):
    if addin_entry.get() == 'Add New Income Amount':
        addin_entry.delete(0, 'end')


def reset_addin_entry(event):
    if addin_entry.get() == '':
        addin_entry.insert(0, 'Add New Income Amount')


addin_entry = CTkEntry(master=frame_1, fg_color="#FFFFFF", width=400, height=50,
                       corner_radius=10, justify="center")
addin_entry.place(relx=0.28, rely=0.40)
addin_entry.insert(0, "Add New Income Amount")
addin_entry.bind('<FocusIn>', clear_addin_entry)
addin_entry.bind('<FocusOut>', reset_addin_entry)

# Currency Box
optionmenu_var = StringVar()

currency_box = CTkOptionMenu(master=frame_1, values=["MYR", "USD", "SGD", "AUD", "RMB", "EUR", "POUND"],
                             text_color='#000000', bg_color="#000000", fg_color="#FFFFFF", width=100, height=40
                             , command=optionmenu_callback, variable=optionmenu_var)
currency_box.place(relx=0.10, rely=0.40)

# Frame 2
frame_2 = CTkFrame(master=money_app, fg_color="#CCCCCC", height=500)
frame_2.pack(fill='x', padx=2, pady=2)

# Category button (Deposit)
catdep_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='DEPOSIT', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catdep_button.place(relx=0.04, rely=0.05)

# Category button (Salary)
catsal_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='SALARY', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catsal_button.place(relx=0.29, rely=0.05)

# Category button (Savings)
catsav_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='SAVINGS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0)
catsav_button.place(relx=0.54, rely=0.05)

save_button = CTkButton(master=frame_1, text='Save', command=save_text)
save_button.place(relx=0.75, rely=0.45)

homepage_button = CTkButton(master=frame_1, text="Switch to Home Page", command=switch_to_homepage)
homepage_button.place(relx=0.0, rely=0.0)
# Start the tkinter main loop
money_app.mainloop()
