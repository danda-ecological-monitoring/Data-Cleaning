"""A gui for uploading and downloading data from the environmental database.
This addresses the graphical end, which will be glued to the functions in
a seperate script
Key windows include a user login, a place to check current data, an upload tool,
and a download tool """

import tkinter as tk

# layout constants
padding = 5
root = tk.Tk()
entry_width = 30

entries = tk.Frame(root)
buttons = tk.Frame(root)
header = tk.Frame(root)

domain = tk.Entry(entries, width = entry_width)
database = tk.Entry(entries, width = entry_width)
user = tk.Entry(entries,width = entry_width)
password = tk.Entry(entries, show = "*",width = entry_width)

head_text= tk.Label(header, text = "Login for Air Quality Database", \
                    pady = padding, padx = padding, font = "TKdefaultfont 15")


def dosomething():
    print (user.get())

submit = tk.Button(buttons, text = "Submit" , command = dosomething)
help_button = tk.Button(buttons, text = "Help")
about = tk.Button(buttons, text = "About")

header.grid(row = 0)

head_text.grid()

entries.grid(row = 1)

tk.Label(entries, text="Database").grid(row=1, sticky = 'E')
tk.Label(entries, text="Domain").grid(row=2, sticky = 'E')
tk.Label(entries, text="User").grid(row=3, sticky = 'E')
tk.Label(entries, text="Password").grid(row=4, sticky = 'E')

buttons.grid(row = 2)

database.grid(row=1, column=1, pady = padding, padx = padding, columnspan = 2)
domain.grid(row=2, column=1, pady = padding, padx = padding,  columnspan = 2) 
user.grid(row=3, column=1, pady = padding, padx = padding,  columnspan = 2)
password.grid(row=4, column=1, pady = padding, padx = padding,  columnspan = 2)
submit.grid(row = 5, column = 1, pady = padding, padx= padding)
#about.grid(row = 5, column = 2, pady = padding, padx= padding)
#help_button.grid(row = 5, column = 3, pady = padding, padx= padding)


root.mainloop()
