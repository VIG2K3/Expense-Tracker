from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

money_app = CTk()
money_app.geometry("900x700")
money_app.resizable(False, False)

set_appearance_mode("light")

# Button definition

def exphover(a):
    addexpbut.configure(fg_color= "#6500C3")
def expnothover(a):
    addexpbut.configure(fg_color= '#7d57f8')

def inchover(a):
    addincbut.configure(fg_color="#6500C3")

def incnothover(a):
    addincbut.configure(fg_color="#7d57f8")

# Frame 1

frame_1 = CTkFrame(master=money_app, fg_color="#dec0ff", height=150)
frame_1.pack(fill='x', padx=2, pady=2)

# Frame 2 (invisible)

frame_2 = CTkFrame(master=money_app, fg_color="#ebebeb", height=125)
frame_2.pack(fill='x', padx=2, pady=2)

# Left Frame in Frame 2

frame_2_1 = CTkFrame(master=frame_2, fg_color="#e9d6ff", height=125, width=446)
frame_2_1.pack(side='left')

addexpbut = CTkButton(master=frame_2_1, text='Add Expenses', fg_color='#7d57f8')
addexpbut.place(anchor='center', relx=0.3, rely=0.5)
addincbut = CTkButton(master=frame_2_1, text='Add Income', fg_color="#7d57f8")
addincbut.place(anchor='center', relx=0.7, rely=0.5)

# Right Frame in Frame 2

frame_2_2 = CTkFrame(master=frame_2, fg_color="#e9d6ff", height=125, width=446)
frame_2_2.pack(side='right')

catlabel = CTkLabel(master=frame_2_2, text='Categories', font=('Arial', 17))
catlabel.place(relx=0.05, rely=0.07)


placeholder1 = CTkButton(master=frame_2_2, text='placeholder', fg_color='#7d57f8')
placeholder1.place(anchor='center', relx=0.3, rely=0.5)
placeholder2 = CTkButton(master=frame_2_2, text='placeholder', fg_color="#7d57f8")
placeholder2.place(anchor='center', relx=0.7, rely=0.5)

frame_3 = CTkFrame(master=money_app, fg_color="#dec0ff", height=300)
frame_3.pack(fill='x', padx=2, pady=2)

frame_4 = CTkFrame(master=money_app, fg_color="#e9d6ff", height=125)
frame_4.pack(fill='x', padx=2, pady=2)

# Button Binds
addexpbut.bind('<Enter>', exphover)
addexpbut.bind('<Leave>', expnothover)
addincbut.bind('<Enter>', inchover)
addincbut.bind('<Leave>', incnothover)

money_app.mainloop()
