import os
from tkinter import Tk, Label, Frame

def show_about_us():
    # Create the About Us window
    about_window = Tk()
    about_window.title("Marist Task Management System - About Us")

    # Set the window size
    about_window.geometry("600x300")  # Adjust the size as needed
    about_window.configure(bg='white')  # Set the background color to white

    # About Us label
    about_label = Label(about_window, text="About Us",
                        fg="blue", bg='white', font=("Helvetica", 16))
    about_label.pack(pady=(10,5))

    # About Us Information
    about_text = ("MaristTask is a Task Management System created by Kevin Reiff, "
                  "a computer science student at Marist College. This Task Management "
                  "system was created as a project for CMPT 308 - 201, Database Management. "
                  "Kevin Reiff is a computer science major and is minoring in creative "
                  "writing and cybersecurity. He has also been working on a high fantasy "
                  "novel and is currently in discussion with several publishers.")

    # Information Label
    info_label = Label(about_window, text=about_text,
                       fg="black", bg='white', font=("Helvetica", 12), wraplength=550, justify='left')
    info_label.pack(pady=10)

    # Start the GUI loop
    about_window.mainloop()

# Uncomment the following line to test the window independently
# show_about_us()
