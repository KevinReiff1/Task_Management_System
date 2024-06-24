import mysql.connector
from tkinter import Tk, Label, Button, Toplevel
from tkinter.ttk import Treeview
from tkinter import Scrollbar

def record_view(db):
    # Function to display table data in a new window
    def show_table_data(table_name, columns):
        # Function to fetch and populate data into the treeview
        def populate_data():
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")  # SQL query to fetch all records from the specified table
            records = cursor.fetchall()  # Fetching all records from the table
            for row in records:
                tree.insert('', 'end', values=row)  # Inserting each record into the treeview
            cursor.close()  # Closing the cursor

        # Creating a new window to display the data of a specific table
        data_window = Toplevel()
        data_window.title(f"{table_name} Records")
        data_window.geometry("1000x600")

        # Displaying a label at the top of the data window
        Label(data_window, text=f"{table_name} Records", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=(10, 10))

        # Setting up the treeview for displaying table data
        tree = Treeview(data_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)  # Configuring column headers
            tree.column(col, width=100, anchor='center')  # Setting column width and alignment

        tree.pack(expand=True, fill='both', padx=10, pady=10)  # Placing the treeview in the window

        # Adding a scrollbar to the treeview
        scrollbar = Scrollbar(data_window, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)  # Linking the scrollbar to the treeview
        scrollbar.pack(side='right', fill='y')  # Placing the scrollbar

        populate_data()  # Populating the treeview with data

    # Main window for selecting which table records to view
    record_window = Tk()
    record_window.title("Record View")
    record_window.geometry("600x600")
    record_window.configure(bg='white')

    # Main label for the record window
    Label(record_window, text="Which Records would you like to view?", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=(10, 10))

    # Button style configuration
    button_style = {'fg': "black", 'bg': "#ADD8E6", 'font': ("Helvetica", 10, "bold"), 'highlightthickness': 4, 'width': 20, 'height': 1}

    # Dictionary containing table names and their respective columns
    tables = {
        'User': ['UserID', 'Username', 'Password', 'Name', 'Address', 'PhoneNumber', 'Birthday'],
        'UserSettings': ['SettingsID', 'UserID', 'NotificationSettings'],
        'Calendar': ['CalendarID', 'UserID'],
        'Task': ['TaskID', 'UserID', 'Title', 'Time', 'Duration', 'Description', 'Calendar_CalendarID'],
        'UserAlert': ['AlertID', 'UserID', 'AlertMessage', 'Alert_Info_AlertID'],
        'UserLogin': ['LoginID', 'UserID', 'LoginTime', 'LogoutTime'],
        'AlertInfo': ['InfoID', 'AlertID', 'UserID', 'AlertHistory'],
        'Admin': ['AdminID', 'Username', 'Password', 'Name', 'Certification', 'Address', 'PhoneNumber', 'Birthday'],
        'Admin Login': ['LoginID', 'AdminID', 'LoginTime', 'LogoutTime'],
        'Admin Settings': ['SettingsID', 'AdminID', 'NotificationSettings']
    }

    for i, (table_name, columns) in enumerate(tables.items()):
        Button(record_window, text=table_name, **button_style, command=lambda name=table_name, cols=columns: show_table_data(name, cols)).pack(pady=5)

    Button(record_window, text="Return To Main Menu", **button_style, command=record_window.destroy).pack(side='left', padx=10, pady=10)

    record_window.mainloop()

