import mysql.connector
from tkinter import Checkbutton, IntVar, Tk, Label, Entry, Button, Frame, messagebox, StringVar, Radiobutton, Toplevel
import re
import datetime
from Functions import Encrypt

def user_administration(db):
    # Styling options for labels, entries, and buttons used in the user interface.
    label_style = {'fg': "blue", 'font': ("Helvetica", 12, "bold")}
    entry_style = {'bg': '#D3D3D3'}
    button_style = {'fg': "black", 'bg': "#ADD8E6", 'font': ("Helvetica", 10, "bold"), 
                    'highlightthickness': 4, 'width': 15, 'height': 1}

    # Function to validate phone number and birthday formats.
    def validate_format(phone_number, birthday):
        # Regular expression to validate phone number format.
        phone_pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
        valid_phone = phone_pattern.match(phone_number) is not None

        # Attempt to parse and validate the birthday date format.
        try:
            year, month, day = map(int, birthday.split('-'))
            datetime.datetime(year, month, day)  # This will raise ValueError if the date is not valid
            valid_birthday = True
        except ValueError:
            valid_birthday = False

        return valid_phone, valid_birthday

    # Function to add a 'Back' button to a given window, with a command to destroy/close the window.
    def add_back_button(window):
        Button(window, text="Back", command=window.destroy, **button_style).pack(side='left', padx=10, pady=10)

    # Global variable to track the selected user role (User or Admin).
    global selected_role
    selected_role = 'user'

    # Function to open a window for adding new users.
    def open_add_user_window():
        global selected_role

        # Create and configure a new window for adding users.
        add_window = Toplevel(admin_window)
        add_window.title("Add User")
        add_window.geometry("400x500")
        add_window.configure(bg='white')

        # Add a label to the add user window.
        Label(add_window, text="Fill in the user's information", **label_style).pack(pady=(10, 5))

        # Fields for user input: username, password, name, address, phone number, and birthday.
        fields = ['Username', 'Password', 'Name', 'Address', 'PhoneNumber', 'Birthday']
        entries = {}
        for field in fields:
            label_text = field + (" (EX: 982-292-1027)" if field == "PhoneNumber" else 
                                " (EX: 2002-10-23)" if field == "Birthday" else "")
            Label(add_window, text=label_text, bg='white').pack(pady=2)
            entry = Entry(add_window, **entry_style)
            entry.pack(pady=2)
            entries[field] = entry

        # Function to set the selected role based on the radiobutton selection.
        def set_role(role):
            global selected_role
            selected_role = role

        # Radiobuttons for selecting user role (User/Admin).
        frame_role = Frame(add_window, bg='white')
        frame_role.pack(pady=10)
        Radiobutton(frame_role, text="User", variable=selected_role, value='user', bg='white', command=lambda: set_role('user')).pack(side='left')
        Radiobutton(frame_role, text="Admin", variable=selected_role, value='admin', bg='white', command=lambda: set_role('admin')).pack(side='left')

        # Function to process and add a new user to the database.
        def add_user():
            # Collecting user data from input fields.
            user_data = {field: entries[field].get() for field in fields}
            role = selected_role

            # Validating phone number and birthday formats.
            valid_phone, valid_birthday = validate_format(user_data['PhoneNumber'], user_data['Birthday'])
            # Various data validation checks.
            if not all(user_data.values()):
                messagebox.showwarning("Warning", "All fields are required!")
                return
            if not valid_phone:
                messagebox.showwarning("Warning", "Invalid phone number format! Use XXX-XXX-XXXX")
                return
            if not valid_birthday:
                messagebox.showwarning("Warning", "Invalid birthday format! Use YYYY-MM-DD")
                return
            if len(user_data['Password']) < 8:
                messagebox.showwarning("Warning", "Password must be at least 8 characters long")
                return

            # Encrypting the password before storing in the database.
            encrypted_password = Encrypt.encrypt_password(user_data['Password'])

            # Execute SQL commands to add user/admin to the database.
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            try:
                success_message = "User added successfully"
                if role == 'admin':
                    # For admin, prepend 'a-' to the username.
                    admin_username = f"a-{user_data['Username']}"
                    cursor.execute("INSERT INTO Admin (Username, Password, Name, Address, PhoneNumber, Birthday, Certification) "
                                "VALUES (%s, %s, %s, %s, %s, %s, 'Certified')", 
                                (admin_username, encrypted_password, user_data['Name'], user_data['Address'], user_data['PhoneNumber'], user_data['Birthday']))
                    success_message = "Admin added successfully"
                else:
                    # SQL command to insert a new user.
                    cursor.execute("INSERT INTO User (Username, Password, Name, Address, PhoneNumber, Birthday) "
                                "VALUES (%s, %s, %s, %s, %s, %s)", (user_data['Username'], encrypted_password, user_data['Name'], user_data['Address'], user_data['PhoneNumber'], user_data['Birthday']))
                db.commit()
                messagebox.showinfo("Success", success_message)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                cursor.close()

            # Close the add user window after successful operation.
            add_window.destroy()

        # Button to initiate the add user process.
        Button(add_window, text="Add User", command=add_user, **button_style).pack(pady=10)
        add_back_button(add_window)



        

    # Function to open a window for removing users.
    def open_remove_user_window():
        # Create and configure a new window for removing users.
        remove_window = Toplevel(admin_window)
        remove_window.title("Remove User")
        remove_window.geometry("400x250")  # Increased size
        remove_window.configure(bg='white')

        # Label prompting for the username of the user to be removed.
        Label(remove_window, text="Input the Username of the user you'd like to remove", **label_style).pack(pady=10)
        entry_username = Entry(remove_window, **entry_style)
        entry_username.pack(pady=5)

        # Function to process and remove a user from the database.
        def remove_user():
            username = entry_username.get()
            # Validation check for empty username input.
            if not username:
                messagebox.showwarning("Warning", "Username is required!")
                return

            # Execute SQL commands to remove user/admin from the database.
            cursor = db.cursor()
            try:
                # SQL commands to delete user and admin records.
                cursor.execute("DELETE FROM User WHERE Username = %s", (username,))
                cursor.execute("DELETE FROM Admin WHERE Username = %s", (username,))
                db.commit()
                messagebox.showinfo("Success", "User removed successfully")
                # Close the remove user window after successful operation.
                remove_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                cursor.close()

        # Button to initiate the remove user process.
        Button(remove_window, text="Remove User", command=remove_user, **button_style).pack(pady=10)
        add_back_button(remove_window)

    # Function to open a window for updating user information.
    def open_update_user_window():
        # Create and configure a new window for updating users.
        update_window = Toplevel(admin_window)
        update_window.title("Update User")
        update_window.geometry("400x800")  # Adjusted size for additional fields
        update_window.configure(bg='white')

        # Label and entry field for searching the user to be updated.
        Label(update_window, text="Update the User's Information", **label_style).pack(pady=(10, 5))
        Label(update_window, text="Enter the User's Username, UserID, or AdminID", bg='white').pack(pady=5)

        search_entry = Entry(update_window, **entry_style)
        search_entry.pack(pady=5)
        Button(update_window, text="Search", command=lambda: search_user(search_entry.get()), **button_style).pack(pady=10)

        # Frame to display and edit the found user's information.
        info_frame = Frame(update_window, bg='white')
        info_frame.pack(pady=10)

        # Fields for user and admin information.
        user_fields = ['UserID', 'Username', 'Password', 'Name', 'Address', 'PhoneNumber', 'Birthday']
        admin_fields = ['AdminID', 'Username', 'Password', 'Name', 'Address', 'PhoneNumber', 'Birthday']
        current_values = {}
        new_entries = {}
        # Entry field to indicate whether the user is an admin. Initialized here for scope reasons.
        is_admin_field = Entry(info_frame, **entry_style)

        # Function to search and display the user's information for updating.
        def search_user(identifier):
            nonlocal is_admin_field  # Use nonlocal to refer to the outer scope variable
            cursor = db.cursor(buffered=True)
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            try:
                # SQL query to find an admin using AdminID or Username.
                cursor.execute("SELECT AdminID, Username, Password, Name, Address, PhoneNumber, Birthday, Certification FROM Admin WHERE AdminID = %s OR Username = %s", (identifier, identifier))
                admin_data = cursor.fetchone()
                is_admin = admin_data is not None

                # If not found as admin, attempt to find as a user.
                if not admin_data:
                    cursor.execute("SELECT UserID, Username, Password, Name, Address, PhoneNumber, Birthday FROM User WHERE UserID = %s OR Username = %s", (identifier, identifier))
                    user_data = cursor.fetchone()
                    admin_data = user_data

                # Clear previous widgets in info frame.
                for widget in info_frame.winfo_children():
                    widget.destroy()

                # If a user/admin is found, display their current information for editing.
                if admin_data:
                    fields = admin_fields if is_admin else user_fields
                    for i, field in enumerate(fields):
                        current_values[field] = admin_data[i]
                        if field != 'Password':
                            label_text = f"Current {field}: {current_values[field]}"
                            Label(info_frame, text=label_text, bg='white').pack(pady=2)
                        else:
                            # Display label for password field without showing actual password.
                            Label(info_frame, text="Password:", bg='white').pack(pady=2)
                        new_entry = Entry(info_frame, **entry_style)
                        new_entry.pack(pady=2)
                        new_entries[field] = new_entry

                    # Entry field to indicate admin status of the user.
                    Label(info_frame, text="Is Admin:", bg='white').pack(pady=2)
                    is_admin_field = Entry(info_frame, **entry_style)
                    is_admin_field.insert(0, "Yes" if is_admin else "No")
                    is_admin_field.pack(pady=2)
                else:
                    messagebox.showwarning("Warning", "User not found")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                cursor.close()

        # Function to process and update the user's information.
        def update_user():
            nonlocal is_admin_field  # Use nonlocal to refer to the outer scope variable
            new_user_data = {field: new_entries[field].get() for field in (admin_fields if current_values.get('AdminID') is not None else user_fields) if new_entries.get(field) and new_entries[field].get()}
            is_admin_changed = (is_admin_field.get() == "Yes" and not current_values.get('AdminID')) or (is_admin_field.get() == "No" and current_values.get('AdminID'))

            # Handle role change if admin status is altered.
            if is_admin_changed:
                handle_role_change(is_admin_field.get(), new_user_data, current_values)
            else:
                update_within_role(new_user_data, current_values, "admin" if current_values.get('AdminID') else "user")

            # Close the update user window after successful operation.
            update_window.destroy()

        # Button to initiate the update user process.
        Button(update_window, text="Update User", command=update_user, **button_style).pack(pady=10)

        # Function to handle user role changes (User to Admin or vice versa).
        def handle_role_change(new_admin_status, new_user_data, current_values):
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            try:
                old_role = 'admin' if current_values.get('AdminID') else 'user'
                new_role = 'admin' if new_admin_status == "Yes" else 'user'
                new_id = new_user_data.get('AdminID' if new_role == 'admin' else 'UserID', None)

                # Delete old records from the database.
                delete_query = f"DELETE FROM {old_role.title()} WHERE {'AdminID' if old_role == 'admin' else 'UserID'} = %s"
                cursor.execute(delete_query, (current_values['AdminID' if old_role == 'admin' else 'UserID'],))

                # Insert updated information into the new role (Admin/User).
                if new_role == 'admin':
                    admin_username = f"a-{current_values['Username']}" if not current_values['Username'].startswith('a-') else current_values['Username']
                    cursor.execute("INSERT INTO Admin (AdminID, Username, Password, Name, Address, PhoneNumber, Birthday, Certification) VALUES (%s, %s, %s, %s, %s, %s, %s, 'Certified')", 
                                (new_id, admin_username, new_user_data.get('Password', current_values['Password']), 
                                    new_user_data.get('Name', current_values['Name']), new_user_data.get('Address', current_values['Address']),
                                    new_user_data.get('PhoneNumber', current_values['PhoneNumber']), new_user_data.get('Birthday', current_values['Birthday'])))
                else:
                    user_username = current_values['Username'][2:] if current_values['Username'].startswith('a-') else current_values['Username']
                    cursor.execute("INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                                (new_id, user_username, new_user_data.get('Password', current_values['Password']), 
                                    new_user_data.get('Name', current_values['Name']), new_user_data.get('Address', current_values['Address']),
                                    new_user_data.get('PhoneNumber', current_values['PhoneNumber']), new_user_data.get('Birthday', current_values['Birthday'])))
                
                db.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred during role change: {err}")
            finally:
                cursor.close()

        # Function to update the user's information within their current role (User or Admin).
        def update_within_role(new_user_data, current_values, role):
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            # Validate phone


        def update_within_role(new_user_data, current_values, role):
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            # Validate phone number and birthday
            valid_phone, valid_birthday = True, True
            if 'PhoneNumber' in new_user_data:
                valid_phone, _ = validate_format(new_user_data['PhoneNumber'], current_values['Birthday'])
            if 'Birthday' in new_user_data:
                _, valid_birthday = validate_format(current_values.get('PhoneNumber', ''), new_user_data['Birthday'])

            try:
                if new_user_data:
                    # Check for password length
                    if 'Password' in new_user_data and len(new_user_data['Password']) < 8:
                        messagebox.showwarning("Warning", "Password must be at least 8 characters long")
                        return

                    # Encrypt new password if provided
                    if 'Password' in new_user_data:
                        new_user_data['Password'] = Encrypt.encrypt_password(new_user_data['Password'])

                    # Check phone number and birthday validity
                    if not valid_phone:
                        messagebox.showwarning("Warning", "Invalid phone number format! Use XXX-XXX-XXXX")
                        return
                    if not valid_birthday:
                        messagebox.showwarning("Warning", "Invalid birthday format! Use YYYY-MM-DD")
                        return

                    update_query = f"UPDATE {role.title()} SET {', '.join(f'{k} = %s' for k in new_user_data)} WHERE {'AdminID' if role == 'admin' else 'UserID'} = %s"
                    cursor.execute(update_query, list(new_user_data.values()) + [current_values['AdminID' if role == 'admin' else 'UserID']])
                    db.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")
            finally:
                cursor.close()

        add_back_button(update_window)



    # Main User Administration Window
    admin_window = Tk()
    admin_window.title("User Administration")
    admin_window.geometry("400x200")
    admin_window.configure(bg='white')
    admin_window.protocol("WM_DELETE_WINDOW", admin_window.destroy)

    Label(admin_window, text="What action would you like to perform", **label_style).pack(pady=(10, 20))

    frame_buttons = Frame(admin_window, bg='white')
    frame_buttons.pack(pady=10)
    Button(frame_buttons, text="Add User", command=open_add_user_window, **button_style).pack(side='left', padx=5)
    Button(frame_buttons, text="Remove User", command=open_remove_user_window, **button_style).pack(side='left', padx=5)
    Button(frame_buttons, text="Update User", command=open_update_user_window, **button_style).pack(side='left', padx=5)

    admin_window.mainloop()

