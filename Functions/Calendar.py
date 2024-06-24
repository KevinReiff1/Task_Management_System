import mysql.connector
from tkinter import Tk, Label, Button, Frame, Toplevel, ttk
from tkcalendar import Calendar
from tkinter.ttk import Treeview, Scrollbar
import datetime

# Function to display a calendar and associated tasks for a specific user and calendar ID.
def show_calendar(db, user_id, calendar_id):
    # Fetches calendar IDs associated with the user from the database.
    def fetch_calendar_ids():
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT CalendarID FROM Calendar WHERE UserID = %s", (user_id,))
        calendar_ids = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        return calendar_ids

    # Updates the dropdown list of calendar IDs and highlights task dates on the calendar.
    def update_calendar_id_combobox():
        calendar_ids = fetch_calendar_ids()
        calendar_id_var['values'] = calendar_ids
        if str(calendar_id) in calendar_ids:
            calendar_id_var.set(str(calendar_id))
            highlight_task_dates(int(calendar_id))
        elif calendar_ids:
            calendar_id_var.set(calendar_ids[0])
            highlight_task_dates(int(calendar_ids[0]))

    # Displays a detailed view of tasks for a selected date.
    def view_task_details_for_date(date, calendar_id):
        formatted_date = datetime.datetime.strptime(date, '%m/%d/%y').date()

        # Create a new window to show task details.
        details_window = Toplevel(calendar_window)
        details_window.title("Detailed Task View")
        details_window.geometry("800x600")
        details_window.configure(bg='white')

        # Query the database for tasks on the selected date.
        cursor = db.cursor(buffered=True)
        cursor.execute("""
            SELECT TaskID, Title, Time, Duration, Description FROM Task 
            WHERE UserID = %s AND Calendar_CalendarID = %s AND DATE(ADDDATE(Time, INTERVAL Duration MINUTE)) = %s
        """, (user_id, calendar_id, formatted_date))
        tasks = cursor.fetchall()
        cursor.close()

        # Setting up a table (treeview) to display the task details.
        tree = Treeview(details_window, columns=("TaskID", "Title", "Start Time", "Duration (Days)", "Description"), show='headings')
        # Configure columns and headings for the table.
        tree.heading("TaskID", text="TaskID")
        tree.heading("Title", text="Title")
        tree.heading("Start Time", text="Start Time")
        tree.heading("Duration (Days)", text="Duration (Days)")
        tree.heading("Description", text="Description")
        tree.column("TaskID", width=50, anchor='center')
        tree.column("Title", width=150, anchor='center')
        tree.column("Start Time", width=150, anchor='center')
        tree.column("Duration (Days)", width=100, anchor='center')
        tree.column("Description", width=300, anchor='center')
        tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Inserting task data into the table.
        for task in tasks:
            task_id, title, start_time, duration, description = task
            duration_days = duration // 1440
            tree.insert("", "end", values=(task_id, title, start_time, duration_days, description))

        # Adding a scrollbar to the table.
        scrollbar = Scrollbar(details_window, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    # Highlights the dates with tasks on the calendar.
    def highlight_task_dates(calendar_id):
        cal.calevent_remove('all', 'task')
        cursor = db.cursor(buffered=True)
        cursor.execute("""
            SELECT DISTINCT DATE(ADDDATE(Time, INTERVAL Duration MINUTE)) AS EndDate FROM Task 
            WHERE UserID = %s AND Calendar_CalendarID = %s
        """, (user_id, calendar_id))
        task_dates = cursor.fetchall()
        cursor.close()

        # Add calendar events for each task date.
        for task_date in task_dates:
            cal.calevent_create(task_date[0], 'Task', 'task')
            cal.tag_config('task', background='red', foreground='white')

    # Handler for date selection from the calendar.
    def on_date_select(event):
        selected_date = cal.get_date()
        view_task_details_for_date(selected_date, int(calendar_id_var.get()))

    # Setting up the main calendar window.
    calendar_window = Tk()
    calendar_window.title("View Calendars")
    calendar_window.geometry("450x450")
    calendar_window.configure(bg='white')

    # Dropdown for selecting a calendar ID.
    calendar_id_var = ttk.Combobox(calendar_window)
    calendar_id_var.pack(pady=10)
    calendar_id_var.bind("<<ComboboxSelected>>", lambda event: highlight_task_dates(int(calendar_id_var.get())))

    # Calendar widget setup.
    cal = Calendar(calendar_window, selectmode='day', year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    cal.pack(pady=20)
    cal.bind("<<CalendarSelected>>", on_date_select)

    # Function to close the calendar window.
    def return_to_main_menu():
        calendar_window.destroy()

    # Initial update of calendar IDs in the dropdown.
    update_calendar_id_combobox()

    # Button to return to the main menu.
    return_button = Button(calendar_window, text="Return To Main Menu", fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"), command=return_to_main_menu)
    return_button.pack(side='left', padx=10, pady=10)

    calendar_window.mainloop()
