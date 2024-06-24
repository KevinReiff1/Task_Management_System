import re
import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox, Frame

def settings_window(db, user_id, role):
    # Function to create and manage UI elements based on user settings
    def create_ui_elements(current_notification_setting, current_phone_number):
        # Update label to show current notification status
        label_current_status.config(text=f"Current Status: {'SMS' if current_notification_setting == 'SMS' else 'Off'}")

        # Conditionally display phone number UI based on current notification setting
        if current_notification_setting == 'SMS':
            # Display phone number entry and update button if SMS is enabled
            label_phone.pack(pady=10)
            entry_phone.delete(0, 'end')
            entry_phone.insert(0, current_phone_number)
            entry_phone.pack()
            button_update_phone.pack(pady=20)
        else:
            # Hide phone number entry and update button if SMS is disabled
            label_phone.pack_forget()
            entry_phone.pack_forget()
            button_update_phone.pack_forget()

    # Function to fetch current notification settings from database
    def fetch_current_settings():
        # SQL query differs based on role (admin/user)
        if role == 'admin':
            # Fetch admin settings
            cursor.execute("SELECT NotificationSettings, PhoneNumber FROM AdminSettings JOIN Admin ON Admin.AdminID = AdminSettings.AdminID WHERE Admin.AdminID = %s", (user_id,))
        else:
            # Fetch user settings
            cursor.execute("SELECT NotificationSettings, PhoneNumber FROM UserSettings JOIN User ON User.UserID = UserSettings.UserID WHERE User.UserID = %s", (user_id,))
        # Retrieve and return fetched settings
        result = cursor.fetchone()
        return (result[0], result[1]) if result else (None, '')
    
    # Function to validate phone number format
    def is_valid_phone_number(phone_number):
        # Define regex pattern for phone number validation
        pattern = re.compile(r"^\d{3}-\d{3}-\d{4}$")
        return pattern.match(phone_number)

    # Function to update notification settings in the database
    def update_settings(notification_preference, phone_number):
        # Validate phone number if notification preference is SMS
        if notification_preference == 'SMS' and not is_valid_phone_number(phone_number):
            messagebox.showerror("Invalid Phone Number", "Please enter a valid phone number in the format XXX-XXX-XXXX.")
            return
        # Update settings in the database based on user role
        if role == 'admin':
            # Update admin settings
            cursor.execute("UPDATE AdminSettings SET NotificationSettings = %s WHERE AdminID = %s", (notification_preference, user_id))
            cursor.execute("UPDATE Admin SET PhoneNumber = %s WHERE AdminID = %s", (phone_number, user_id))
        else:
            # Update user settings
            cursor.execute("UPDATE UserSettings SET NotificationSettings = %s WHERE UserID = %s", (notification_preference, user_id))
            cursor.execute("UPDATE User SET PhoneNumber = %s WHERE UserID = %s", (phone_number, user_id))

        # Commit changes to the database
        db.commit()
        messagebox.showinfo("Success", "Settings updated successfully")
        # Fetch and display updated settings
        new_notification_setting, new_phone_number = fetch_current_settings()
        create_ui_elements(new_notification_setting, new_phone_number)

    # Initialize settings window
    settings_win = Tk()
    settings_win.title(f"{role.capitalize()} Settings")
    settings_win.geometry("500x400")
    settings_win.configure(bg='white')

    cursor = db.cursor()

    # Retrieve and display current settings
    current_notification_setting, current_phone_number = fetch_current_settings()

    # UI Elements
    label_main_title = Label(settings_win, text="Would you like to turn on SMS notifications?", bg='white', fg='blue', font=("Helvetica", 16, "bold"))
    label_main_title.pack(pady=(10, 20))

    label_current_status = Label(settings_win, bg='white', font=("Helvetica", 12))
    label_current_status.pack(pady=10)

    button_frame = Frame(settings_win, bg='white')
    button_frame.pack(pady=10)

    # Buttons for toggling SMS notifications on and off
    button_on = Button(button_frame, text="On", fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"), highlightthickness=4,
                       command=lambda: update_settings('SMS', current_phone_number))
    button_on.pack(side="left", padx=10)

    button_off = Button(button_frame, text="Off", fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"), highlightthickness=4,
                        command=lambda: update_settings(None, current_phone_number))
    button_off.pack(side="left", padx=10)

    label_phone = Label(settings_win, text="Verify your phone number:", bg='white')
    entry_phone = Entry(settings_win, bg='#D3D3D3')

    # Function to close settings window
    def close_window():
        settings_win.destroy()

    # Button to update phone number
    button_update_phone = Button(settings_win, text="Update Phone Number", fg="black", bg="#ADD8E6",
                                 font=("Helvetica", 10, "bold"), highlightthickness=4,
                                 command=lambda: update_settings('SMS', entry_phone.get()))
    
    # Button to return to the main menu
    button_return_main = Button(settings_win, text="Return To Main Menu", fg="black", bg="#ADD8E6",
                                font=("Helvetica", 10, "bold"), highlightthickness=4, command=close_window)
    button_return_main.pack(side="bottom", anchor="w", padx=10, pady=10)

    # Initialize UI with current settings
    create_ui_elements(current_notification_setting, current_phone_number)

    # Start the main loop of the settings window
    settings_win.mainloop()
