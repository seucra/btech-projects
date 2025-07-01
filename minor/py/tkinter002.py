import tkinter as tk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=200, bg="lime")
        self.pack()
        self.pack_propagate(False)

        self.entrythingy = tk.Entry(self)
        self.entrythingy.pack(pady=20)

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)

    def print_contents(self, event):
        # Get all text from Text widget
        print("Hi. The current entry content is:", self.contents.get())

root = tk.Tk()
myapp = App(root)
myapp.mainloop()
