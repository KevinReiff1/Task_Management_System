import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox
from Functions import Encrypt  # Import custom encryption module for password handling

def change_password(db, user_id, role):
    # Function to update user's password in the database
    def update_password(event=None):  # Accepts an optional event parameter for key binding
        # Retrieve and compare the new password and its confirmation
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        # Check for password match and minimum length
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            return

        # Encrypt the new password before storing it
        encrypted_password = Encrypt.encrypt_password(new_password)

        # Create a database cursor for executing SQL commands
        cursor = db.cursor()
        # Determine the appropriate table for updating password based on user role
        if role == 'admin':
            update_query = "UPDATE Admin SET Password = %s WHERE AdminID = %s"
        else:
            update_query = "UPDATE User SET Password = %s WHERE UserID = %s"

        # Execute the update query and handle potential database errors
        try:
            cursor.execute(update_query, (encrypted_password, user_id))
            db.commit()
            messagebox.showinfo("Success", "Password updated successfully")
            change_window.destroy()  # Close the window on successful update
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        finally:
            cursor.close()  # Ensure the cursor is closed after operation

    def return_to_main():
        # Function to close the password change window and return to main menu
        change_window.destroy()

    # Setup the password change window using Tkinter
    change_window = Tk()
    change_window.title("Change Password")
    change_window.geometry("300x250")
    change_window.configure(bg='white')

    # User interface elements for password input
    label_new_password = Label(change_window, text="New Password", bg='white')
    label_new_password.pack(pady=(10, 5))

    entry_new_password = Entry(change_window, show="*", bg='#D3D3D3')
    entry_new_password.pack()

    label_confirm_password = Label(change_window, text="Confirm Password", bg='white')
    label_confirm_password.pack(pady=5)

    entry_confirm_password = Entry(change_window, show="*", bg='#D3D3D3')
    entry_confirm_password.pack()

    # Button to trigger password update process
    button_change = Button(change_window, text="Change Password",
                           fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"),
                           highlightthickness=4, command=update_password)
    button_change.pack(pady=20)

    # Bind the enter key to update_password function for convenience
    change_window.bind('<Return>', update_password)

    # Button to return to the main menu
    button_return = Button(change_window, text="Return To Main Menu",
                           fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"),
                           highlightthickness=4, command=return_to_main)
    button_return.pack(side='left', padx=10, pady=10)

    change_window.mainloop()  # Start the Tkinter event loop
