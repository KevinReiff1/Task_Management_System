import mysql.connector
from tkinter import Radiobutton, Tk, Label, Entry, Button, messagebox, StringVar, Frame
import datetime

def add_task(db, user_id):
    # Function to handle the task submission process.
    def submit_task(event=None):
        # Retrieve values from the form fields.
        title = entry_title.get()
        start_date = entry_start_date.get()
        start_time = entry_start_time.get() + " " + am_pm.get()
        duration = entry_duration.get()
        description = entry_description.get()
        calendar_id = entry_calendar_id.get()

        # Attempt to format and validate the start date and time.
        try:
            formatted_start_time = datetime.datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %I:%M %p')
            formatted_start_time_str = formatted_start_time.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return

        # Check if all form fields are filled.
        if not title or not start_date or not start_time or not duration or not description or not calendar_id:
            messagebox.showerror("Error", "All fields are required")
            return

        # Create a database cursor for executing SQL queries.
        cursor = db.cursor()
        # SQL query to insert a new task into the database.
        insert_query = """
            INSERT INTO Task (UserID, Title, Time, Duration, Description, Calendar_CalendarID) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            # Execute the insert query with user-provided values.
            cursor.execute(insert_query, (user_id, title, formatted_start_time_str, int(duration) * 1440, description, calendar_id))
            db.commit()
            messagebox.showinfo("Success", "Task added successfully")
            add_window.destroy()  # Close the window after successful task addition.
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        finally:
            cursor.close()

    # Set up the GUI window for adding a task.
    add_window = Tk()
    add_window.title("Add a Task")
    add_window.geometry("400x500")
    add_window.configure(bg='white')

    label_main_title = Label(add_window, text="Add a Task!", bg='white', fg='blue', font=("Helvetica", 16, "bold"))
    label_main_title.pack(pady=(10, 20))

    # Widgets for task title input.
    label_title = Label(add_window, text="Title", bg='white')
    label_title.pack(pady=(5, 5))
    entry_title = Entry(add_window, bg='#D3D3D3')
    entry_title.pack()

    # Widgets for task start date input.
    label_start_date = Label(add_window, text="Start Date (YYYY-MM-DD)", bg='white')
    label_start_date.pack(pady=5)
    entry_start_date = Entry(add_window, bg='#D3D3D3')
    entry_start_date.pack()

    # Frame for time input and AM/PM selection.
    time_frame = Frame(add_window, bg='white')
    time_frame.pack(pady=5)

    label_start_time = Label(time_frame, text="Start Time (HH:MM)", bg='white')
    label_start_time.pack(side="left")
    entry_start_time = Entry(time_frame, bg='#D3D3D3', width=10)
    entry_start_time.pack(side="left")

    # Radio buttons for AM/PM selection.
    am_pm = StringVar(value="AM")
    rb_am = Radiobutton(time_frame, text="AM", variable=am_pm, value="AM", bg='white')
    rb_am.pack(side="left")
    rb_pm = Radiobutton(time_frame, text="PM", variable=am_pm, value="PM", bg='white')
    rb_pm.pack(side="left")

    # Widgets for task duration input.
    label_duration = Label(add_window, text="Duration (days)", bg='white')
    label_duration.pack(pady=5)
    entry_duration = Entry(add_window, bg='#D3D3D3')
    entry_duration.pack()

    # Widgets for task description input.
    label_description = Label(add_window, text="Description", bg='white')
    label_description.pack(pady=5)
    entry_description = Entry(add_window, bg='#D3D3D3')
    entry_description.pack()

    # Widgets for calendar ID input.
    label_calendar_id = Label(add_window, text="Calendar ID", bg='white')
    label_calendar_id.pack(pady=5)
    entry_calendar_id = Entry(add_window, bg='#D3D3D3')
    entry_calendar_id.pack()

    # Button to submit the task information.
    button_submit = Button(add_window, text="Add Task", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=submit_task)
    button_submit.pack(pady=20)

    # Button to close the add task window.
    button_return = Button(add_window, text="Return to Main Page", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=add_window.destroy)
    button_return.place(x=10, y=450)

    # Enable submission of the task by pressing the Enter key.
    add_window.bind('<Return>', submit_task)

    add_window.mainloop()
