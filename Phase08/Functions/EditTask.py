import mysql.connector
from tkinter import Radiobutton, Tk, Label, Entry, Button, messagebox, StringVar, Frame, Listbox, Scrollbar, Toplevel
import datetime

def edit_task(db, user_id):
    # Function to refresh the task list displayed in the main window.
    def refresh_task_list():
        listbox_tasks.delete(0, 'end')  # Clear existing items in the listbox.
        task_ids.clear()  # Clear the task ID list.
        cursor = db.cursor()  # Create a new cursor for database operations.
        cursor.execute("SELECT TaskID, Title, Time FROM Task WHERE UserID = %s", (user_id,))
        # Populate the listbox with tasks and store their IDs for later use.
        for task_id, title, time in cursor:
            listbox_tasks.insert("end", f"Task ID: {task_id}, Title: {title}, Time: {time}")
            task_ids.append(task_id)
        cursor.close()

    # Function to handle the selection of a task to edit.
    def select_task_to_edit():
        selected_index = listbox_tasks.curselection()  # Get the index of the selected task.
        if not selected_index:  # Check if a task is selected.
            messagebox.showwarning("Warning", "Please select a task to edit")
            return
        task_id = task_ids[selected_index[0]]  # Retrieve the ID of the selected task.
        edit_window = Toplevel(main_window)  # Create a new top-level window for editing.
        edit_selected_task(edit_window, task_id)  # Call function to handle editing.

    # Function to edit the selected task.
    def edit_selected_task(edit_window, task_id):
        cursor = db.cursor()
        # Fetch existing details of the selected task from the database.
        cursor.execute("SELECT Title, Time, Duration, Description, Calendar_CalendarID FROM Task WHERE TaskID = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()

        # Unpack the task details.
        title, time, duration, description, calendar_id = task
        # Format the start date and time for display.
        start_date = time.strftime('%Y-%m-%d')
        start_time = time.strftime('%I:%M %p')
        duration_days = duration // 1440  # Convert duration from minutes to days.

        # Function to finalize and save the edits to the task.
        def finalize_edits():
            # Fetch new task details from the entry fields.
            new_title = entry_title.get()
            new_start_date = entry_start_date.get()
            new_start_time = entry_start_time.get() + " " + am_pm.get()
            new_duration_days = entry_duration.get()
            new_description = entry_description.get()
            new_calendar_id = entry_calendar_id.get()

            # Attempt to format and validate the new start time.
            try:
                formatted_start_time = datetime.datetime.strptime(f"{new_start_date} {new_start_time}", '%Y-%m-%d %I:%M %p')
                formatted_duration = int(new_duration_days) * 1440  # Convert days back to minutes.
            except ValueError:
                messagebox.showerror("Error", "Invalid date or time format")
                return

            # Prepare the SQL query for updating the task.
            update_query = """
                UPDATE Task SET Title = %s, Time = %s, Duration = %s, Description = %s, Calendar_CalendarID = %s 
                WHERE TaskID = %s
            """
            try:
                cursor = db.cursor()
                # Execute the update query with the new task details.
                cursor.execute(update_query, (new_title, formatted_start_time, formatted_duration, new_description, int(new_calendar_id), task_id))
                db.commit()  # Commit the changes to the database.
                messagebox.showinfo("Success", "Task updated successfully")
                edit_window.destroy()  # Close the edit window.
                refresh_task_list()  # Refresh the task list to show updated details.
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                cursor.close()

        # Setting up the edit window layout with entry fields for task details.
        edit_window.title("Edit Task")
        edit_window.geometry("500x500")
        edit_window.configure(bg='white')

        # Main title caption
        label_main_title = Label(edit_window, text="Edit a Task!", bg='white', fg='blue', font=("Helvetica", 16, "bold"))
        label_main_title.pack(pady=(10, 20))

        # Task Title
        label_title = Label(edit_window, text="Title", bg='white')
        label_title.pack(pady=(5, 5))
        entry_title = Entry(edit_window, bg='#D3D3D3')
        entry_title.insert(0, title)
        entry_title.pack()

        # Task Start Date
        label_start_date = Label(edit_window, text="Start Date (YYYY-MM-DD)", bg='white')
        label_start_date.pack(pady=5)
        entry_start_date = Entry(edit_window, bg='#D3D3D3')
        entry_start_date.insert(0, start_date)
        entry_start_date.pack()

        # Time Frame
        time_frame = Frame(edit_window, bg='white')
        time_frame.pack(pady=5)

        # Task Start Time
        label_start_time = Label(time_frame, text="Start Time (HH:MM)", bg='white')
        label_start_time.pack(side="left")
        entry_start_time = Entry(time_frame, bg='#D3D3D3', width=10)
        entry_start_time.insert(0, start_time.split()[0])
        entry_start_time.pack(side="left")

        # AM/PM Selection
        am_pm = StringVar(value=start_time.split()[1])
        Radiobutton(time_frame, text="AM", variable=am_pm, value="AM", bg='white', command=lambda: am_pm.set("AM")).pack(side="left")
        Radiobutton(time_frame, text="PM", variable=am_pm, value="PM", bg='white', command=lambda: am_pm.set("PM")).pack(side="left")

        # Task Duration in Days
        label_duration = Label(edit_window, text="Duration (days)", bg='white')
        label_duration.pack(pady=5)
        entry_duration = Entry(edit_window, bg='#D3D3D3')
        entry_duration.insert(0, duration_days)
        entry_duration.pack()

        # Task Description
        label_description = Label(edit_window, text="Description", bg='white')
        label_description.pack(pady=5)
        entry_description = Entry(edit_window, bg='#D3D3D3')
        entry_description.insert(0, description)
        entry_description.pack()

        # Calendar ID
        label_calendar_id = Label(edit_window, text="Calendar ID", bg='white')
        label_calendar_id.pack(pady=5)
        entry_calendar_id = Entry(edit_window, bg='#D3D3D3')
        entry_calendar_id.insert(0, calendar_id)
        entry_calendar_id.pack()

        # Finalize Edits button
        button_finalize = Button(edit_window, text="Finalize Edits", fg="black", bg="#ADD8E6",
                                 font=("Helvetica", 10, "bold"), highlightthickness=4, command=finalize_edits)
        button_finalize.pack(pady=20)

    # Main window for task selection
    main_window = Tk()
    main_window.title("Choose a Task to Edit")
    main_window.geometry("500x400")
    main_window.configure(bg='white')

    # Title caption
    label_main_title = Label(main_window, text="Choose a Task to Edit", bg='white', fg='blue', font=("Helvetica", 16, "bold"))
    label_main_title.pack(pady=(10, 20))

    # Listbox with tasks
    scrollbar = Scrollbar(main_window)
    scrollbar.pack(side="right", fill="y")

    listbox_tasks = Listbox(main_window, yscrollcommand=scrollbar.set)
    task_ids = []
    refresh_task_list()

    listbox_tasks.pack(fill="both", expand=True)
    scrollbar.config(command=listbox_tasks.yview)

    # Select Task button
    button_select = Button(main_window, text="Select Task", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=select_task_to_edit)
    button_select.pack(pady=20)

    def return_to_main_menu():
        main_window.destroy()

    button_return = Button(main_window, text="Return To Main Menu", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=return_to_main_menu)
    button_return.pack(side='bottom', anchor='w', padx=10, pady=10)  # Placed at bottom left

    main_window.mainloop()
