from tkinter import *


root = Tk()

names = ["weight", "bodyfat", "hydration", "muscle", "bones"]
entry = {}
label = {}

i = 0
for name in names:
    e = Entry(root)
    e.grid(sticky=E)
    entry[name] = e

    lb = Label(root, text=name)
    lb.grid(row=i, column=1)
    label[name] = lb
    i += 1

def print_all_entries():
    for name in names:
        print(name)
        print(entry[name].get())

b = Button(root, text="Print all", command=print_all_entries)
b.grid(sticky=S)

mainloop()