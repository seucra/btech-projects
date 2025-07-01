import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=100, height=100)
        self.pack()
        self.button = tk.Button(self, text="Hover over me")
        self.button.pack(pady=20)

        # Bind mouse enter event to the button
        self.button.bind("<Enter>", self.turn_red)


    def turn_red(self, event):
        event.widget["activeforeground"] = "red"

# create the application
root = tk.Tk()
myapp = App(master=root)

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()
