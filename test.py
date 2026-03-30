
import ttkbootstrap as ttk

root = ttk.Window(themename="flatly", minsize=(300, 200))

date_entry = ttk.DateEntry(root)
date_entry.entry.configure(textvariable=ttk.StringVar(value='2024-06-15'))


date_entry.pack()

root.mainloop()



