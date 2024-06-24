import mysql.connector

def caesar_cipher(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]

        # Shift uppercase characters within ASCII range for uppercase letters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Shift lowercase characters within ASCII range for lowercase letters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)

        # Keep non-alphabetic characters as is
        else:
            result += char

    return result

def encrypt_password(password):
    # Apply Caesar cipher with a right shift of 3
    return caesar_cipher(password, 3)

def decrypt_password(encrypted_password):
    # Decrypt by applying Caesar cipher with a left shift of 3
    return caesar_cipher(encrypted_password, -3)

def encrypt_existing_passwords():
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="MaristTask"
    )
    cursor = db.cursor()

    # Update passwords in the User table
    cursor.execute("SELECT UserID, Password FROM User")
    users = cursor.fetchall()
    for user_id, password in users:
        encrypted_password = encrypt_password(password)
        # Execute update query for each user
        cursor.execute("UPDATE User SET Password = %s WHERE UserID = %s", (encrypted_password, user_id))

    # Update passwords in the Admin table
    cursor.execute("SELECT AdminID, Password FROM Admin")
    admins = cursor.fetchall()
    for admin_id, password in admins:
        encrypted_password = encrypt_password(password)
        # Execute update query for each admin
        cursor.execute("UPDATE Admin SET Password = %s WHERE AdminID = %s", (encrypted_password, admin_id))

    # Commit changes and close database connection
    db.commit()
    db.close()

if __name__ == "__main__":
    encrypt_existing_passwords()
