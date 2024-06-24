CREATE DATABASE IF NOT EXISTS MaristTask;
USE MaristTask;

SET FOREIGN_KEY_CHECKS=0;
-- User table remains unchanged
CREATE TABLE IF NOT EXISTS User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(45) NOT NULL UNIQUE,
    Password VARCHAR(60) NOT NULL,
    Name VARCHAR(45) NOT NULL,
    Address VARCHAR(45),
    PhoneNumber VARCHAR(45),
    Birthday DATE
);

-- UserSettings table remains unchanged
CREATE TABLE IF NOT EXISTS UserSettings (
    SettingsID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    NotificationSettings TEXT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- Modified Calendar table to remove potential 2NF violation
CREATE TABLE IF NOT EXISTS Calendar (
	CalendarID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);


-- Modified Task table to address 2NF concerns
CREATE TABLE IF NOT EXISTS Task (
    TaskID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Title VARCHAR(45) NOT NULL,
    Time TIMESTAMP,
    Duration INT,
    Description TEXT,
    Calendar_CalendarID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (Calendar_CalendarID) REFERENCES Calendar(CalendarID) ON DELETE CASCADE
);


-- Create the User Alert table
CREATE TABLE IF NOT EXISTS UserAlert (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    AlertMessage TEXT,
    Alert_Info_AlertID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- UserLogin table remains unchanged
CREATE TABLE IF NOT EXISTS UserLogin (
    LoginID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    LoginTime TIMESTAMP,
    LogoutTime TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- Create the Alert Info table
CREATE TABLE IF NOT EXISTS AlertInfo (
    InfoID INT AUTO_INCREMENT PRIMARY KEY,  -- New auto-increment primary key
    AlertID INT,                            -- Foreign key to UserAlert
    UserID INT,
    AlertHistory TEXT,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (AlertID) REFERENCES UserAlert(AlertID) ON DELETE CASCADE
);


-- Admin table remains unchanged
CREATE TABLE IF NOT EXISTS Admin (
	AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(45) NOT NULL UNIQUE,
    Password VARCHAR(60) NOT NULL,
    Name VARCHAR(45) NOT NULL,
    Certification VARCHAR(45),
    Address VARCHAR(100),
    PhoneNumber VARCHAR(45),
    Birthday DATE
);

-- AdminLogin table remains unchanged
CREATE TABLE IF NOT EXISTS AdminLogin (
	LoginID INT AUTO_INCREMENT PRIMARY KEY,
    AdminID INT,
    LoginTime TIMESTAMP,
    LogoutTime TIMESTAMP,
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID) ON DELETE CASCADE
);

-- AdminSettings table remains unchanged
CREATE TABLE IF NOT EXISTS AdminSettings (
    SettingsID INT AUTO_INCREMENT PRIMARY KEY,
    AdminID INT,
    NotificationSettings TEXT,
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
);



