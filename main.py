import tkinter as tk
import api_key
from search import Search

S = Search('stockdata', '', api_key.key)

def search():
    S.ticker = entry.get()
    print(f'Ticker: {S.get_ticker()}')

# Create the main window
root = tk.Tk()
root.title("Stock Analizer")
root.geometry("800x600")        # Set the window size

# Create a frame for the main menu
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Create a label for the main menu
label = tk.Label(main_frame, text="Ticker:")
label.pack(anchor='center')

# Create a textbox for the main menu
entry = tk.Entry(main_frame)
entry.pack(anchor='center')

# Create a search button for the main menu
search_button = tk.Button(main_frame, text="Search", command=search)
search_button.pack(anchor='center')











# Run the Tkinter event loop
root.mainloop()