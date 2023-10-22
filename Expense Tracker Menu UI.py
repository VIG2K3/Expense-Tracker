from customtkinter import *
import PIL

money_app = CTk()
money_app.geometry("900x700")
money_app.resizable(False, False)

set_appearance_mode("light")


# Button definition

def save_text():
    edited_text = addexp_entry.get()
    selected_option = optionmenu_var.get()
    print(f"Edited Text: {edited_text}")

def optionmenu_callback(choice):
    print(f"Selected Option: {choice}")

def button_command(category):
    print(f"Button clicked for category: {category}")


def save_text():
    edited_text = addexp_entry.get()
    selected_option = optionmenu_var.get()
    print(f"Edited Text: {edited_text}, Selected Option: {selected_option}, Button clicked for category: {category}")

# Frame 1
frame_1 = CTkFrame(master=money_app, fg_color="#dec0ff", height=200)
frame_1.pack(fill='x', padx=2, pady=2)

# New Expense heading
heading = CTkLabel(master=frame_1, text='New Expenses', fg_color="#dec0ff", font=('Arial', 23))
heading.place(x=450, y=40, anchor='center')

# Add New Expense

def clear_addexp_entry(event):
    if addexp_entry.get() == 'Add New Expense Amount':
        addexp_entry.delete(0, 'end')

def reset_addexp_entry(event):
    if addexp_entry.get() == '':
       addexp_entry.insert(0, 'Add New Expense Amount')

Expense_box = CTkFrame(master=frame_1, fg_color="#FFFFFF", width=400, height=50)
Expense_box.place(relx=0.28, rely=0.40)

addexp_entry = CTkEntry(master=Expense_box, fg_color="#FFFFFF", width=400, height=50,
                          border_width=2, corner_radius=10, justify="center")
addexp_entry.place(relx=0.28, rely=0.40)
addexp_entry.pack(fill="both", expand=True)
addexp_entry.insert(0, "Add New Expense Amount")
addexp_entry.bind('<FocusIn>', clear_addexp_entry)
addexp_entry.bind('<FocusOut>', reset_addexp_entry)

# Currency Box
optionmenu_var = StringVar()

currency_box = CTkOptionMenu(master=frame_1, values=["MYR", "USD", "SGD", "AUD", "RMB", "EUR", "POUND"],
               text_color='#000000', fg_color="#FFFFFF", width=100, height=40
                            ,command=optionmenu_callback, variable=optionmenu_var)
currency_box.place(relx=0.10, rely=0.40)

# Frame 2
frame_2 = CTkFrame(master=money_app, fg_color="#CCCCCC", height=500)
frame_2.pack(fill='x', padx=2, pady=2)

# Category button (car)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='CAR', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.04, rely=0.05)

# Category button (bills)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='BILLS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.29, rely=0.05)

# Category button (Shopping)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='SHOPPING', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.54, rely=0.05)

# Category button (House)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='HOUSE', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.79, rely=0.05)

# Category button (F&B)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='F&B', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.04, rely=0.35)

# Category button (Entertainment)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='ENTERTAINMENT',
                          text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.29, rely=0.35)

# Category button (Transport)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='TRANSPORT', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.54, rely=0.35)

# Category button (Pets)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='PETS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.79, rely=0.35)

# Category button (Deposit)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='DEPOSIT', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.04, rely=0.65)

# Category button (Salary)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='SALARY', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.29, rely=0.65)

# Category button (Savings)
catcar_button = CTkButton(master=frame_2, compound="top", width=150, height=100, text='SAVINGS', text_color='#000000',
                          fg_color="#FFFFFF", border_width=0, command=lambda cat='CAR': button_command(category))
catcar_button.place(relx=0.54, rely=0.65)


save_button = CTkButtonsave_button = CTkButton(master=frame_1,text='Save', command=save_text)
save_button.place(relx=0.75, rely=0.45)

# Start the tkinter main loop
money_app.mainloop()

