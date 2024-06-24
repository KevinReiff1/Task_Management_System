import mysql.connector
from tkinter import Tk, Label, Entry, Button, Frame, Toplevel, messagebox
from tkinter.ttk import Treeview, Scrollbar
import datetime

def search_task(db, user_id):
    # Function to calculate the end time of a task based on its start time and duration
    def calculate_end_date(start_time, duration):
        end_time = start_time + datetime.timedelta(minutes=duration)
        return end_time

    # Function to display detailed information of a specific task in a new window
    def display_task_details(task_id):
        # Creating a new top-level window for task details
        details_window = Toplevel(main_window)
        details_window.title("Task Information")
        details_window.geometry("400x500")
        details_window.configure(bg='white')

        # Querying the database for task details using the task ID
        cursor = db.cursor()
        cursor.execute("SELECT Title, Time, Duration, Description, Calendar_CalendarID FROM Task WHERE TaskID = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()

        # Checking if task details are found and displaying them
        if task:
            title, time, duration, description, calendar_id = task
            duration_days = duration // 1440  # Converting duration from minutes to days
            end_date = calculate_end_date(time, duration)

            # Creating and configuring frames and labels to display task details
            header_frame = Frame(details_window, bg='white')
            header_frame.pack(pady=(10, 20), padx=10, fill='x')
            Label(header_frame, text="Task Information", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(side='left')

            details_frame = Frame(details_window, bg='white')
            details_frame.pack(pady=(5, 10), padx=10, fill='x')

            # Labels and values for each task detail
            labels = ["Title", "Start Time", "End Time", "Duration (days)", "Description", "Calendar ID", "Task ID"]
            values = [title, time.strftime('%Y-%m-%d %H:%M'), end_date.strftime('%Y-%m-%d %H:%M'), str(duration_days), description, str(calendar_id), str(task_id)]

            # Displaying each label and its corresponding value
            for i in range(len(labels)):
                row_frame = Frame(details_frame, bg='white')
                row_frame.pack(fill='x', pady=2)
                Label(row_frame, text=f"{labels[i]}:", width=15, anchor='w', bg='white', font=("Helvetica", 10, "bold")).pack(side='left')
                Label(row_frame, text=values[i], width=25, anchor='w', bg='white', font=("Helvetica", 10)).pack(side='left')

    # Function to execute search based on user input and display results
    def search():
        # Getting user input for the search
        query = search_entry.get()

        # Preparing and executing the search query
        cursor = db.cursor()
        search_query = """
            SELECT TaskID, Title, Time, Duration, Description, Calendar_CalendarID FROM Task 
            WHERE UserID = %s AND 
            (Title LIKE %s OR 
             Description LIKE %s OR 
             Calendar_CalendarID LIKE %s OR 
             TaskID LIKE %s OR 
             Time LIKE %s OR 
             Duration LIKE %s OR 
             ADDDATE(Time, INTERVAL Duration MINUTE) LIKE %s)
        """
        cursor.execute(search_query, (user_id, f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        tasks = cursor.fetchall()
        cursor.close()

        # Clearing previous search results from the treeview
        for i in tree.get_children():
            tree.delete(i)

        # Populating the treeview with the search results
        for task in tasks:
            task_id, title, start_time, duration, description, calendar_id = task
            duration_days = duration // 1440  # Convert minutes to days
            end_time = calculate_end_date(start_time, duration)
            tree.insert("", "end", values=(task_id, title, start_time, end_time, duration_days, description, calendar_id))

    # Setting up the main window for task search
    main_window = Tk()
    main_window.title("Search Tasks")
    main_window.geometry("900x600")
    main_window.configure(bg='white')

    # Configuring and placing search bar, entry, and button in the main window
    Label(main_window, text="Search Tasks", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=(10, 10))
    search_entry = Entry(main_window, width=50)
    search_entry.pack(pady=5)
    Button(main_window, text="Search", command=search, bg="#ADD8E6", fg="black", font=("Helvetica", 10, "bold"), highlightthickness=4).pack(pady=10)

    # Configuring and adding a treeview for displaying search results
    tree = Treeview(main_window, columns=("TaskID", "Title", "Start Time", "End Time", "Duration (Days)", "Description", "Calendar ID"), show='headings')
    tree.heading("TaskID", text="TaskID")
    tree.heading("Title", text="Title")
    tree.heading("Start Time", text="Start Time")
    tree.heading("End Time", text="End Time")
    tree.heading("Duration (Days)", text="Duration (Days)")
    tree.heading("Description", text="Description")
    tree.heading("Calendar ID", text="Calendar ID")
    tree.column("TaskID", width=50, anchor='center')
    tree.column("Title", width=75, anchor='center')
    tree.column("Start Time", width=150, anchor='center')
    tree.column("End Time", width=150, anchor='center')
    tree.column("Duration (Days)", width=100, anchor='center')
    tree.column("Description", width=200, anchor='center')
    tree.column("Calendar ID", width=80, anchor='center')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Adding a scrollbar for the treeview
    scrollbar = Scrollbar(main_window, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Button to view detailed information of a selected task
    Button(main_window, text="View Task Details", command=lambda: display_task_details(tree.item(tree.selection())['values'][0]), bg="#ADD8E6", fg="black", font=("Helvetica", 10, "bold"), highlightthickness=4).pack(pady=10)

    # Button to return to the main menu
    Button(main_window, text="Return To Main Menu", command=main_window.destroy, bg="#ADD8E6", fg="black", font=("Helvetica", 10, "bold"), highlightthickness=4).pack(side='left', pady=10)

    # Initiating the main window's event loop
    main_window.mainloop()
