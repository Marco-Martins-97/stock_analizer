import tkinter as tk
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import api_key
from search import Search

TICKER = ''
S = Search('stockdata', api_key.key)



def load_data_from_file(filename):
        filepath = f"stockdata/{TICKER}/{filename}.json"
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            text_frame.showerror("Error", f"Data file for {TICKER} not found.")
            return None
        except json.JSONDecodeError:
            text_frame.showerror("Error", "Invalid JSON format in data file.")
            return None

def search():
    global TICKER
    TICKER = entry.get()
    if TICKER != '':
        if S.get_ticker(TICKER):
            display_overview()
        else: print('error!!')

def display_overview():
    data = load_data_from_file('overview')
    if data:
        text_frame.delete(1.0, tk.END)  # Clear the text widget
        relevant_info = [
            "Name", "Currency", "LatestQuarter", "MarketCapitalization",
            "EBITDA", "PERatio", "DividendPerShare", "DividendYield",
            "EPS", "RevenueTTM", "Beta", "DividendDate", "ExDividendDate"
        ]
        for key in relevant_info:
            if key in data:
                text_frame.insert(tk.END, f"{key}: {data[key]}\n")
                # Hide text frame
                graph_frame.pack_forget()
                # Show graph frame
                text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def display_graph(file, key_data):
    data = load_data_from_file(file)
    if data:
        # Destroy the existing canvas widget if it exists
        for widget in graph_frame.winfo_children():
            widget.destroy()
        # Extract annual reports and quarterly reports
        annual_reports = data['annualReports']
        #quarterly_reports = data['quarterlyReports']
        # Extract totalAssets from annual reports and put into an array
        #annual = [float(report[key_data]) for report in annual_reports]
        annual = [float(report[key_data]) if report[key_data] != 'None' else 0.0 for report in annual_reports]
        years = [report['fiscalDateEnding'][:4] for report in annual_reports]
        # Extract totalAssets from quarterly reports and put into another array
        #quarterly = [float(report[key_data]) for report in quarterly_reports]
        #quarter = [report['fiscalDateEnding'] for report in quarterly_reports]
        
        # Reverse the order of the data arrays
        annual.reverse()
        years.reverse()

        # Create Matplotlib figure
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.bar(years, annual, color='skyblue')
        ax.set_xlabel('Year')
        ax.set_ylabel(key_data)
        ax.set_title(f'{key_data} Over Years')

        # Format y-axis ticks as currency values
        def currency_formatter(x, pos):
            if x >= 1e12:
                return '${:.1f}T'.format(x * 1e-12)
            elif x >= 1e9:
                return '${:.1f}B'.format(x * 1e-9)
            elif x >= 1e6:
                return '${:.1f}M'.format(x * 1e-6)
            elif x >= 1e3:
                return '${:.1f}K'.format(x * 1e-3)
            else:
                return '${:.0f}'.format(x)

        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

        # Create Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Hide text frame
        text_frame.pack_forget()
        # Show graph frame
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

def button_click(btn_name):
    if btn_name == 'investments': display_graph('balance_sheet', 'investments')
    if btn_name == 'totalLiabilities': display_graph('balance_sheet', 'totalLiabilities')
    if btn_name == 'currentDebt': display_graph('balance_sheet', 'currentDebt')
    if btn_name == 'operatingCashflow': display_graph('cash_flow', 'operatingCashflow')
    if btn_name == 'netIncome': display_graph('cash_flow', 'netIncome')
    if btn_name == 'grossProfit': display_graph('income_statement', 'grossProfit')
    if btn_name == 'totalRevenue': display_graph('income_statement', 'totalRevenue')
    if btn_name == 'operatingIncome': display_graph('income_statement', 'operatingIncome')
    if btn_name == 'operatingExpenses': display_graph('income_statement', 'operatingExpenses')
    if btn_name == 'ebitda': display_graph('income_statement', 'ebitda')
    else: print(btn_name)

# WINDOW
# Create the main window
root = tk.Tk()
root.title("Stock Analizer")
root.geometry("1600x900")        # Set the window size

# FRAMES
# Create frames for menu and display
menu_frame = tk.Frame(root, width=200, bg='lightgray')
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

display_frame = tk.Frame(root, bg='white')
display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# MENU
# Create a label for the main menu
label = tk.Label(menu_frame, text="Ticker:", width=25, bg='lightgray')
label.pack(anchor='center')

# Create a textbox for the main menu
entry = tk.Entry(menu_frame)
entry.pack(anchor='center', pady=3)

# Create a search button for the main menu
search_button = tk.Button(menu_frame, text="Search", command=search)
search_button.pack(anchor='center',  pady=3)

# Create text widget to display stock data
text_frame = tk.Text(display_frame)
text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
# Create graph widget to display stock data
graph_frame = tk.Frame(display_frame)
#graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Menu buttons
buttons = ['investments', 'totalLiabilities', 'currentDebt', 'operatingCashflow', 'netIncome', 'grossProfit', 'totalRevenue', 'operatingIncome', 'operatingExpenses', 'ebitda', '', '', '', '']

for btn_name in buttons:
    btn = tk.Button(menu_frame, text=btn_name, command=lambda btn_name=btn_name: button_click(btn_name))
    btn.pack(fill=tk.X, padx=5, pady=1)











# Run the Tkinter event loop
root.mainloop()