import mysql.connector
from tkinter import END, LEFT, Tk, Label, Button, Entry, Toplevel, messagebox, Frame, Scrollbar, Text
import datetime

def calculate_end_date(start_time, duration):
    # Convert string to datetime object if needed
    if isinstance(start_time, str):
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # Return the end date by adding duration to the start time
    return start_time + datetime.timedelta(minutes=duration)

def welcome_alerts(db, user_id):
    current_date = datetime.datetime.now()
    cursor = db.cursor(buffered=True)

    # Fetch tasks for the given user from the database
    cursor.execute("""
        SELECT TaskID, Title, Time, Duration, Description, Calendar_CalendarID FROM Task 
        WHERE UserID = %s
    """, (user_id,))
    tasks = cursor.fetchall()

    for task in tasks:
        task_id, title, start_time, duration, description, calendar_id = task
        end_date = calculate_end_date(start_time, duration)
        days_until_due = (end_date - current_date).days

        # Filter tasks due within the next 7 days
        if 0 <= days_until_due <= 7:
            alert_message = f"{title} is due in {days_until_due} days"
            full_alert_message = f"{alert_message} (Alert sent on {current_date.strftime('%Y-%m-%d')})"

            # Avoid sending duplicate alerts on the same day
            cursor.execute("""
                SELECT AlertHistory FROM AlertInfo 
                WHERE UserID = %s AND AlertHistory LIKE %s
            """, (user_id, f"%{full_alert_message}%"))
            alert_exists = cursor.fetchone()

            if not alert_exists:
                display_task_details(db, task_id, title, start_time, duration, description, calendar_id, days_until_due)
                
                # Insert new alert messages into the database
                cursor.execute("INSERT INTO UserAlert (UserID, AlertMessage) VALUES (%s, %s)", (user_id, alert_message))
                db.commit()
                alert_id = cursor.lastrowid
                cursor.execute("INSERT INTO AlertInfo (AlertID, UserID, AlertHistory) VALUES (%s, %s, %s)", (alert_id, user_id, full_alert_message))
                db.commit()
    cursor.close()

def display_task_details(db, task_id, title, start_time, duration, description, calendar_id, days_until_due):
    # Creating a new window to display task details
    details_window = Toplevel()
    details_window.title(f"{title} Due: {days_until_due} days")
    details_window.geometry("400x500")
    details_window.configure(bg='white')

    duration_days = duration // 1440  # Convert minutes to days for display
    end_date = calculate_end_date(start_time, duration)

    # Layout for displaying header information
    header_frame = Frame(details_window, bg='white')
    header_frame.pack(pady=(10, 20), padx=10, fill='x')
    Label(header_frame, text=f"{title} - Due in {days_until_due} days", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(side='left')

    # Frame for displaying task details like start time, end time, etc.
    details_frame = Frame(details_window, bg='white')
    details_frame.pack(pady=(5, 10), padx=10, fill='x')

    labels = ["Title", "Start Time", "End Time", "Duration (days)", "Description", "Calendar ID", "Task ID"]
    values = [title, start_time.strftime('%Y-%m-%d %H:%M'), end_date.strftime('%Y-%m-%d %H:%M'), str(duration_days), description, str(calendar_id), str(task_id)]

    for i in range(len(labels)):
        row_frame = Frame(details_frame, bg='white')
        row_frame.pack(fill='x', pady=2)
        Label(row_frame, text=f"{labels[i]}:", width=15, anchor='w', bg='white', font=("Helvetica", 10, "bold")).pack(side='left')
        Label(row_frame, text=values[i], width=25, anchor='w', bg='white', font=("Helvetica", 10)).pack(side='left')

    button_frame = Frame(details_window, bg='white')
    button_frame.pack(fill='x', pady=10)
    
# Function to create a window displaying user-specific alerts
def show_user_alerts(db, user_id):
    # Setup for the alerts display window
    alerts_window = Toplevel()
    alerts_window.title("Your Alerts")
    alerts_window.geometry("500x550")
    alerts_window.configure(bg='white')

    # Header for the alerts window
    Label(alerts_window, text="Your Alerts", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=10)

    # Adding a scrollbar for the text box
    scrollbar = Scrollbar(alerts_window)
    scrollbar.pack(side='right', fill='y')

    # Text box for displaying alerts
    text_box = Text(alerts_window, yscrollcommand=scrollbar.set, wrap="word", bg="#f0f0f0", font=("Helvetica", 12))
    text_box.pack(expand=True, fill='both', padx=10, pady=5)
    scrollbar.config(command=text_box.yview)

    # Fetch and display alerts from the database
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT AlertHistory FROM AlertInfo WHERE UserID = %s", (user_id,))
    alerts = cursor.fetchall()
    cursor.close()

    for alert in alerts:
        if alert[0] != "History 1":  # Skip any placeholder text
            text_box.insert('end', alert[0] + "\n\n")

    text_box.config(state='disabled')

    # Layout for the return button
    button_frame = Frame(alerts_window, bg='white')
    button_frame.pack(fill='x', pady=10)

    # Button to close the alerts window and return to the main menu
    Button(button_frame, text="Return To Main Menu",
           fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"),
           highlightthickness=4, command=alerts_window.destroy).pack(side='left', padx=10)

# Function to display alert information for admins
def show_user_alert_info(db):
    def search_alerts():
        # Function to handle search functionality in the admin window
        search_term = entry_search.get().strip()
        if not search_term:
            messagebox.showerror("Error", "Please enter a UserID or Username")
            return

        # Query to fetch alerts based on UserID or Username
        if search_term.isdigit():
            query = "SELECT AlertHistory FROM AlertInfo WHERE UserID = %s"
            params = (search_term,)
        else:
            query = """
                SELECT AlertHistory FROM AlertInfo 
                INNER JOIN User ON User.UserID = AlertInfo.UserID 
                WHERE User.Username = %s
            """
            params = (search_term,)

        cursor = db.cursor(buffered=True)
        cursor.execute(query, params)
        alerts = cursor.fetchall()
        cursor.close()

        # Displaying the fetched alerts in the text box
        text_alerts.delete('1.0', END)
        if not alerts:
            text_alerts.insert('1.0', "No alerts found.")
        else:
            alert_text = "\n\n".join([alert[0].replace('History 1', '').strip() for alert in alerts])
            text_alerts.insert('1.0', alert_text)

    # Window setup for user alert information
    user_alert_window = Toplevel()
    user_alert_window.title("User Alert Info")
    user_alert_window.geometry("600x450")
    user_alert_window.configure(bg='white')

    # Header for the admin window
    Label(user_alert_window, text="User Alert Info", bg='white', fg='blue', font=("Helvetica", 16, "bold")).pack(pady=10)

    # Search functionality layout
    search_frame = Frame(user_alert_window, bg='white')
    search_frame.pack(pady=5)

    Label(search_frame, text="Enter User ID or Username:", bg='white', font=("Helvetica", 12)).pack(side=LEFT)
    entry_search = Entry(search_frame, bg='#D3D3D3', width=30)
    entry_search.pack(side=LEFT, padx=10)

    Button(search_frame, text="Search", command=search_alerts, fg="black", bg="#ADD8E6", font=("Helvetica", 10, "bold"), highlightthickness=4).pack(side=LEFT)

    # Text box with scrollbar for displaying alerts
    text_alerts = Text(user_alert_window, wrap="word", bg="#f0f0f0", font=("Helvetica", 12), height=15)
    text_alerts.pack(expand=True, fill='both', padx=10, pady=5)

    scrollbar = Scrollbar(user_alert_window, command=text_alerts.yview)
    scrollbar.pack(side='right', fill='y')
    text_alerts.config(yscrollcommand=scrollbar.set)
