import os
from tkinter import PhotoImage, Tk, Label, Button, Frame, messagebox
from Functions import ChangePassword, UserAdministration, AddTask, EditTask, RemoveTask, SearchTask, Calendar, Alerts, Settings, History, Records, AboutUs

def show_welcome_page(role, user_id, name, db):
    # Create the main window
    welcome_window = Tk()
    welcome_window.title("Marist Task Management System - Welcome")

    # Adjust the size based on the role
    if role == 'admin':
        welcome_window.geometry("500x650")  # Smaller size for admin
    else:
        welcome_window.geometry("600x750")  # Larger size for regular user

    welcome_window.configure(bg='white')  # Set the background color to white

    # Welcome label (updated text)
    welcome_label = Label(welcome_window, text=f"Welcome To",
                          fg="blue", bg='white', font=("Helvetica", 16))
    welcome_label.pack(pady=(10,5))

    image_path = os.path.join(os.path.dirname(__file__), '../Images', 'MaristTask.png')
    logo_image = PhotoImage(file=image_path)
    logo_label = Label(welcome_window, image=logo_image, bg='white')
    logo_label.pack(pady=(5, 10))

    # User's name label
    name_label = Label(welcome_window, text=name,
                       fg="black", bg='white', font=("Helvetica", 14))
    name_label.pack(pady=10)

    # Button frame
    button_frame = Frame(welcome_window, bg='white')
    button_frame.pack(pady=20)

    # Define a common button style
    button_style = {'fg': "black", 'bg': "#ADD8E6", 'font': ("Helvetica", 10, "bold"),
                    'highlightthickness': 4, 'width': 20, 'height': 1}
    
    def on_close():
        """ Function to handle window close event """
        is_admin = role == 'admin'
        History.record_logout(db, user_id, is_admin)  # Record the logout time
        messagebox.showinfo("Thank You", "Thank you for using the MaristTask software!")
        welcome_window.destroy()  # Close the window

    welcome_window.protocol("WM_DELETE_WINDOW", on_close)  # Bind the close event

    # Role-specific features and buttons
    if role == 'admin':
        # Admin-specific buttons
        btn_admin_settings = Button(button_frame, text="Admin Settings", **button_style,
                                    command=lambda: Settings.settings_window(db, user_id, role))
        btn_admin_settings.grid(row=0, column=0, padx=10, pady=5)

        btn_admin_login_history = Button(button_frame, text="Login Records", **button_style,
                                 command=lambda: History.show_admin_login_records(db))
        btn_admin_login_history.grid(row=1, column=0, padx=10, pady=5)

        btn_user_alert_info = Button(button_frame, text="User Alert Info", **button_style, 
                                     command=lambda: Alerts.show_user_alert_info(db))
        btn_user_alert_info.grid(row=2, column=0, padx=10, pady=5)

        btn_user_admin = Button(button_frame, text="User Administration", **button_style, 
                                command=lambda: UserAdministration.user_administration(db))
        btn_user_admin.grid(row=3, column=0, padx=10, pady=5)

        btn_record_view = Button(button_frame, text="Record View", **button_style,
                         command=lambda: Records.record_view(db))
        btn_record_view.grid(row=4, column=0, padx=10, pady=5)


    else:
        # User-specific buttons
        btn_add_task = Button(button_frame, text="Add Task", **button_style, 
                            command=lambda: AddTask.add_task(db, user_id))
        btn_add_task.grid(row=0, column=0, padx=10, pady=5)

        btn_edit_task = Button(button_frame, text="Edit Task", **button_style,
                           command=lambda: EditTask.edit_task(db, user_id))
        btn_edit_task.grid(row=1, column=0, padx=10, pady=5)

        btn_remove_task = Button(button_frame, text="Remove Task", **button_style, 
                             command=lambda: RemoveTask.remove_task(db, user_id))
        btn_remove_task.grid(row=2, column=0, padx=10, pady=5)

        btn_search_task = Button(button_frame, text="Search Task", **button_style, 
                             command=lambda: SearchTask.search_task(db, user_id))
        btn_search_task.grid(row=3, column=0, padx=10, pady=5)

        default_calendar_id = 1 
        btn_calendar = Button(button_frame, text="Calendar", **button_style, 
                              command=lambda: Calendar.show_calendar(db, user_id, default_calendar_id))
        btn_calendar.grid(row=4, column=0, padx=10, pady=5)

        btn_alerts = Button(button_frame, text="Alerts", **button_style, 
                            command=lambda: Alerts.show_user_alerts(db, user_id))
        btn_alerts.grid(row=5, column=0, padx=10, pady=5)

        btn_user_settings = Button(button_frame, text="User Settings", **button_style,
                                   command=lambda: Settings.settings_window(db, user_id, role))
        btn_user_settings.grid(row=6, column=0, padx=10, pady=5)

        btn_user_login_history = Button(button_frame, text="User Login History", **button_style, 
                                command=lambda: History.show_login_history(db, user_id, False))
        btn_user_login_history.grid(row=7, column=0, padx=10, pady=5)

    # Change Password Button (for all users)
    btn_change_password = Button(button_frame, text="Change Password", **button_style, 
                                 command=lambda: ChangePassword.change_password(db, user_id, role))
    btn_change_password.grid(row=8 if role == 'admin' else 9, column=0, padx=10, pady=5)

    # ...
    btn_about_us = Button(button_frame, text="About Us", **button_style, command=AboutUs.show_about_us)
    btn_about_us.grid(row=9 if role == 'admin' else 11, column=0, padx=10, pady=5)


    # Exit button
    btn_exit = Button(button_frame, text="Exit", command=on_close, **button_style)
    btn_exit.grid(row=10 if role == 'admin' else 12, column=0, padx=10, pady=5)

    # Check for alerts (if user)
    if role != 'admin':
        Alerts.welcome_alerts(db, user_id)

    # Start the GUI loop
    welcome_window.mainloop()
