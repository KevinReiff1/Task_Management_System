import mysql.connector
from tkinter import *
from tkinter import messagebox
import os
from Functions import History, Encrypt, WelcomePage

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="MaristTask"
)

# Function to check login credentials and determine role
def check_login(username, input_password):
    cursor = db.cursor()
    encrypted_input_password = Encrypt.encrypt_password(input_password)

    # Check if user is a regular user
    user_query = "SELECT UserID, Name, Password FROM User WHERE Username = %s"
    cursor.execute(user_query, (username,))
    user_result = cursor.fetchone()

    if user_result and encrypted_input_password == user_result[2]:
        return True, 'user', user_result[0], user_result[1]

    # Check if user is an admin
    admin_query = "SELECT AdminID, Name, Password FROM Admin WHERE Username = %s"
    cursor.execute(admin_query, (username,))
    admin_result = cursor.fetchone()

    if admin_result and encrypted_input_password == admin_result[2]:
        return True, 'admin', admin_result[0], admin_result[1]

    return False, None, None, None

# Function to open the welcome page
def open_welcome_page(role, user_id, name, db):
    window.destroy()  # Close the login window
    WelcomePage.show_welcome_page(role, user_id, name, db)  # Open the welcome page with additional details

# Function to handle the login button click
# Function to handle the login button click
def on_login_click(event=None):
    username = entry_username.get()
    password = entry_password.get()
    login_success, role, user_id, name = check_login(username, password)

    if login_success:
        messagebox.showinfo("Login Success", f"You have successfully logged in as {role}!")
        is_admin = role == 'admin'
        History.record_login(db, user_id, is_admin)  # Record the login time
        open_welcome_page(role, user_id, name, db)  # Pass the 'db' argument here
    else:
        messagebox.showwarning("Login Failed", "Incorrect username or password")




# Create the main window
window = Tk()
window.title("Marist Task Login")
window.geometry("400x450")  # Adjust the size as needed
window.configure(bg='white')  # Set the background color to white

# Define the relative path to the images directory
# Note that 'Images' is capitalized as per your folder structure
image_path = os.path.join(os.path.dirname(__file__), 'Images')

# Load the logo image using a relative path
logo_image_path = os.path.join(image_path, 'logo.png')  # 'logo.png' is the image file in the Images directory
logo_image = PhotoImage(file=logo_image_path)
logo_image = logo_image.subsample(2, 2)  # Adjust the subsample factors as needed

# Use the scaled image in the Label widget
logo_label = Label(window, image=logo_image, bg='white')  # Set the background color to white
logo_label.pack(side=TOP, pady=(10, 0))

# Welcome label
welcome_text = Label(window, text="MaristTask Login", fg="blue", bg='white', font=("Helvetica", 16))
welcome_text.pack(side=TOP, pady=(0, 20))  # Adjust padding as needed

# Create and place the login form
form_frame = Frame(window, bg='white')  # Set the background color to white
form_frame.pack(side=TOP, pady=10)

label_username = Label(form_frame, text="Username", bg='white')
label_username.grid(row=0, column=0, sticky=W)

entry_username = Entry(form_frame, bg='#D3D3D3')
entry_username.grid(row=0, column=1, padx=10)

label_password = Label(form_frame, text="Password", bg='white')
label_password.grid(row=1, column=0, sticky=W)

entry_password = Entry(form_frame, show="*", bg='#D3D3D3')
entry_password.grid(row=1, column=1, padx=10)

# Modified login button with new properties
button_login = Button(form_frame, text="Login", command=on_login_click,
                      fg="black",  # Text color
                      bg="#ADD8E6",  # Background color
                      font=("Helvetica", 10, "bold"),  # Font settings (size, weight)
                      highlightthickness=4,  # Border thickness
                      width=10, height=1)  # Button size
button_login.grid(row=2, column=0, columnspan=2, pady=10)


# Bind the enter key to the login function
window.bind('<Return>', on_login_click)

# Start the GUI loop
window.mainloop()
