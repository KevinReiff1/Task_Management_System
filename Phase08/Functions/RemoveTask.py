import mysql.connector
from tkinter import Tk, Label, Button, Frame, Listbox, Scrollbar, messagebox

def remove_task(db, user_id):
    # Function to update the task list in the GUI
    def refresh_task_list():
        # Clear existing items in the listbox
        listbox_tasks.delete(0, 'end')
        # Clear the list that tracks task IDs
        task_ids.clear()
        # Create a database cursor for querying
        cursor = db.cursor()
        # Retrieve tasks specific to the given user ID
        cursor.execute("SELECT TaskID, Title, Time FROM Task WHERE UserID = %s", (user_id,))
        # Populate the listbox with tasks and store their IDs
        for task_id, title, time in cursor:
            listbox_tasks.insert("end", f"Task ID: {task_id}, Title: {title}, Time: {time}")
            task_ids.append(task_id)
        # Close the cursor to free database resources
        cursor.close()

    # Function to handle task removal
    def select_task_to_remove():
        # Get the selected item's index from the listbox
        selected_index = listbox_tasks.curselection()
        # Check if an item is selected
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a task to remove")
            return
        # Retrieve the task ID corresponding to the selected item
        task_id = task_ids[selected_index[0]]

        # Ask for confirmation before deleting the task
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this task?"):
            cursor = db.cursor()
            delete_query = "DELETE FROM Task WHERE TaskID = %s"
            try:
                # Execute the deletion query
                cursor.execute(delete_query, (task_id,))
                db.commit()
                messagebox.showinfo("Success", "Task removed successfully")
                # Refresh the list to reflect the deletion
                refresh_task_list()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                # Always close the cursor after the operation
                cursor.close()

    # Create the main window using Tkinter
    main_window = Tk()
    main_window.title("Remove Task")
    main_window.geometry("500x400")
    main_window.configure(bg='white')

    # Setup the title label
    label_main_title = Label(main_window, text="Remove a Task", bg='white', fg='blue', font=("Helvetica", 16, "bold"))
    label_main_title.pack(pady=(10, 20))

    # Initialize a scrollbar for the listbox
    scrollbar = Scrollbar(main_window)
    scrollbar.pack(side="right", fill="y")

    # Create a listbox to display tasks and attach the scrollbar to it
    listbox_tasks = Listbox(main_window, yscrollcommand=scrollbar.set)
    task_ids = []  # List to store task IDs
    refresh_task_list()  # Populate the listbox with tasks

    listbox_tasks.pack(fill="both", expand=True)
    scrollbar.config(command=listbox_tasks.yview)

    # Button to trigger task removal
    button_remove = Button(main_window, text="Remove Task", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=select_task_to_remove)
    button_remove.pack(pady=20)

    # Button to return to the main menu
    button_return = Button(main_window, text="Return To Main Menu", fg="black", bg="#ADD8E6",
                           font=("Helvetica", 10, "bold"), highlightthickness=4, command=main_window.destroy)
    button_return.pack(side='left', padx=10, pady=10)

    # Start the Tkinter event loop
    main_window.mainloop()
