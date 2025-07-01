import tkinter as tk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=300, bg="lime")
        self.pack()
        self.pack_propagate(False)

        # Create a multi-line text area with size in characters
        self.entrythingy = tk.Text(self, width=50, height=10)  # width and height in characters
        self.entrythingy.pack(pady=20)

        # Optional: pre-fill the text area manually
        self.entrythingy.insert("1.0", "this is a variable")

        # Bind Enter key (Return) to function
        self.entrythingy.bind('<Return>', self.print_contents)

    def print_contents(self, event):
        # Get all text from Text widget
        content = self.entrythingy.get("1.0", "end-1c")  # From start to just before the last newline
        print("Hi. The current entry content is:", content)
        return "break"  # Prevent default newline behavior on Enter

root = tk.Tk()
myapp = App(root)
myapp.mainloop()
