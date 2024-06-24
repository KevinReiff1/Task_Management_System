# Importing necessary modules
import mysql.connector
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox
from tkinter.ttk import Treeview, Scrollbar
import datetime

# Function to record a user or admin login event in the database
def record_login(db, user_id, is_admin):
    # Establishing a new database cursor for executing queries
    cursor = db.cursor()
    # Getting the current datetime for login timestamp
    login_time = datetime.datetime.now()
    # Deciding the table and column names based on the user type (admin or regular user)
    table = "AdminLogin" if is_admin else "UserLogin"
    column = "AdminID" if is_admin else "UserID"
    # SQL query for inserting a new login record
    insert_query = f"INSERT INTO {table} ({column}, LoginTime) VALUES (%s, %s)"
    # Executing the query with parameters
    cursor.execute(insert_query, (user_id, login_time))
    # Committing the transaction to the database
    db.commit()
    # Closing the cursor after operation is completed
    cursor.close()

# Function to record a user or admin logout event in the database
def record_logout(db, user_id, is_admin):
    cursor = db.cursor()
    logout_time = datetime.datetime.now()
    table = "AdminLogin" if is_admin else "UserLogin"
    column = "AdminID" if is_admin else "UserID"
    # SQL query for updating the logout time of the most recent login record
    update_query = f"UPDATE {table} SET LogoutTime = %s WHERE {column} = %s AND LogoutTime IS NULL ORDER BY LoginID DESC LIMIT 1"
    cursor.execute(update_query, (logout_time, user_id))
    db.commit()
    cursor.close()

# Function to display the login history for a user or admin
def show_login_history(db, user_id, is_admin):
    # Creating a new window using Toplevel for displaying login history
    history_window = Toplevel()
    history_window.title("Your Login History")
    history_window.geometry("600x400")

    # Adding labels, treeview, and scrollbar for showing login history
    Label(history_window, text="Your Login History", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=(10, 10))
    tree = Treeview(history_window, columns=("LoginID", "Login Time", "Logout Time"), show='headings')
    # Configuring columns for the Treeview
    tree.heading("LoginID", text="Login ID")
    tree.heading("Login Time", text="Login Time")
    tree.heading("Logout Time", text="Logout Time")
    tree.column("LoginID", width=100, anchor='center')
    tree.column("Login Time", width=250, anchor='center')
    tree.column("Logout Time", width=250, anchor='center')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    scrollbar = Scrollbar(history_window, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Retrieving login history from the database
    cursor = db.cursor()
    table = "AdminLogin" if is_admin else "UserLogin"
    column = "AdminID" if is_admin else "UserID"
    cursor.execute(f"SELECT LoginID, LoginTime, LogoutTime FROM {table} WHERE {column} = %s", (user_id,))
    records = cursor.fetchall()
    cursor.close()

    # Adding a return button to the window
    Button(history_window, text="Return To Main Menu", command=history_window.destroy, 
           fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"),
           highlightthickness=4).pack(side='bottom', anchor='sw', padx=10, pady=10)

    # Inserting records into the Treeview
    for record in records:
        tree.insert("", "end", values=record)

# Function to display login records for both users and admins (accessible by admin)
def show_admin_login_records(db):
    # Function for executing search based on the input from search_entry
    def search():
        query = search_entry.get()
        cursor = db.cursor()
        # SQL query for searching in both UserLogin and AdminLogin tables
        search_query = """
            SELECT 'User' AS Type, UserLogin.LoginID, UserLogin.LoginTime, UserLogin.LogoutTime 
            FROM UserLogin 
            JOIN User ON User.UserID = UserLogin.UserID 
            WHERE User.UserID = %s OR User.Username = %s
            UNION ALL
            SELECT 'Admin' AS Type, AdminLogin.LoginID, AdminLogin.LoginTime, AdminLogin.LogoutTime 
            FROM AdminLogin 
            JOIN Admin ON Admin.AdminID = AdminLogin.AdminID 
            WHERE Admin.AdminID = %s OR Admin.Username = %s
        """
        cursor.execute(search_query, (query, query, query, query))
        records = cursor.fetchall()
        cursor.close()

        # Clearing existing records in the treeview before inserting new ones
        for i in tree.get_children():
            tree.delete(i)
        
        # Inserting the fetched records into the treeview
        for record in records:
            tree.insert("", "end", values=record)

    # Creating a new window for displaying admin's search functionality
    records_window = Toplevel()
    records_window.title("Search Login Records")
    records_window.geometry("800x500")

    # Adding UI elements for search functionality
    Label(records_window, text="Search Login Records", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=(10, 10))
    search_entry = Entry(records_window, width=50, bg='#D3D3D3')
    search_entry.pack(pady=5)
    Button(records_window, text="Search", command=search, bg="#ADD8E6", fg="black", font=("Helvetica", 10, "bold"), highlightthickness=4).pack(pady=10)

    # Setting up Treeview and Scrollbar for displaying search results
    tree = Treeview(records_window, columns=("Type", "LoginID", "Login Time", "Logout Time"), show='headings')
    tree.heading("Type", text="Type")
    tree.heading("LoginID", text="Login ID")
    tree.heading("Login Time", text="Login Time")
    tree.heading("Logout Time", text="Logout Time")
    tree.column("Type", width=100, anchor='center')
    tree.column("LoginID", width=100, anchor='center')
    tree.column("Login Time", width=300, anchor='center')
    tree.column("Logout Time", width=300, anchor='center')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    scrollbar = Scrollbar(records_window, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
