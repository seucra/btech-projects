import tkinter as tk

def on_click(char) :
	current = entry.get()
	entry.delete(0, tk.END)
	entry.insert(0, current+char)

def clear():
	entry.delete(0,tk.END)

def calculate():
	try:
		result = eval(entry.get)
		entry.delete(0, tk.END)
		entry.insert(0, str(result))
	except:
		entry.delete(0, tk.END)
		entry.insert(0, "Error")

# Setup the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")
root.resizable(False, False)

# Entry box
entry = tk.Entry(root, font=('Arial', 24), borderwidth=2, relief="ridge", justify="right")
entry.pack(padx=10, pady=10, fill="x")

# Button layout
# Button layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', 'C', '+'],
    ['=']
]

# Create buttons dynamically
for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    for btn in row:
        if btn == 'C':
            action = clear
        elif btn == '=':
            action = calculate
        else:
            action = lambda x=btn: on_click(x)

        tk.Button(frame, text=btn, font=('Arial', 18), command=action).pack(
            side="left", expand=True, fill="both"
        )


# Start the GUI loop
root.mainloop()

