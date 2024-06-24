use MaristTask;

SET FOREIGN_KEY_CHECKS=0;

/* Single line insertions take a total time of 0.016 seconds
Explain INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (1, 'johndoe', 'password123', 'John Doe', '123 Main St', '123-456-7890', '1990-01-01');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (2, 'janedoe', 'pass456', 'Jane Doe', '124 Main St', NULL, '1992-02-02');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (3, 'mikeb', 'mikepass', 'Mike Brown', '125 Main St', '123-456-7891', '1988-03-03');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (4, 'emmagreen', 'emma1234', 'Emma Green', NULL, '123-456-7892', '1995-04-04');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (5, 'samw', 'samspass', 'Sam Wilson', '126 Main St', '123-456-7893', '1991-05-05');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (6, 'lucyp', 'lucyword', 'Lucy Parker', '127 Main St', '123-456-7894', '1989-06-06');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (7, 'davidt', 'davidpwd', 'David Taylor', NULL, '123-456-7895', '1993-07-07');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (8, 'sarahc', 'sarahpass', 'Sarah Connor', '128 Main St', '123-456-7896', '1994-08-08');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (9, 'rickg', 'rick123', 'Rick Grimes', '129 Main St', NULL, '1996-09-09');
INSERT INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES (10, 'annak', 'anna456', 'Anna Klein', '130 Main St', '123-456-7897', '1990-10-10');
*/

-- Optimized bulk insertions take a total time of 0.000 seconds (I assume this means a number 
-- smaller than 0.000 but too small to be displayed with 3 signficant figures
Insert INTO User (UserID, Username, Password, Name, Address, PhoneNumber, Birthday) VALUES
(1, 'KevinR', 'KevinReiff1', 'Kevin Reiff', '123 Main St', '123-456-7890', '2002-10-23'),
(2, 'janedoe', 'password456', 'Jane Doe', '124 Main St', NULL, '1992-02-02'),
(3, 'mikeb', 'mikepassword1', 'Mike Brown', '125 Main St', '123-456-7891', '1988-03-03'),
(4, 'emmagreen', 'emmapassword1234', 'Emma Green', NULL, '123-456-7892', '1995-04-04'),
(5, 'samw', 'samspasswprd1', 'Sam Wilson', '126 Main St', '123-456-7893', '1991-05-05'),
(6, 'lucyp', 'lucywordpass3', 'Lucy Parker', '127 Main St', '123-456-7894', '1989-06-06'),
(7, 'davidt', 'davidpwd439', 'David Taylor', NULL, '123-456-7895', '1993-07-07'),
(8, 'sarahc', 'sarahpass4937', 'Sarah Connor', '128 Main St', '123-456-7896', '1994-08-08'),
(9, 'rickg', 'rickpass123', 'Rick Grimes', '129 Main St', NULL, '1996-09-09'),
(10, 'annak', 'annapassword456', 'Anna Klein', '130 Main St', '123-456-7897', '1990-10-10');


INSERT INTO UserSettings (SettingsID, UserID, NotificationSettings) VALUES
(1, 1, 'SMS'),
(2, 2, NULL),
(3, 3, 'SMS'),
(4, 4, NULL),
(5, 5, 'SMS'),
(6, 6, NULL),
(7, 7, NULL),
(8, 8, 'SMS'),
(9, 9, 'SMS'),
(10, 10, 'SMS');

INSERT INTO Calendar (CalendarID, UserID) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3),
(5, 4),
(6, 5),
(7, 6),
(8, 1),
(9, 8),
(10, 9),
(11, 10);

INSERT INTO Task (TaskID, UserID, Title, Time, Duration, Description, Calendar_CalendarID) VALUES
(1, 1, 'Task 1', '2023-11-19 09:00:00', 1440, 'Description for Task 1', 1),
(2, 1, 'Task 2', '2023-11-19 10:00:00', 2880, 'Description for Task 2', 1),
(3, 2, 'Task 3', '2023-11-11 09:00:00', 200, 'Description for Task 3', 2),
(4, 2, 'Task 4', '2023-11-11 10:15:00', 1000, 'Description for Task 4', 2),
(5, 3, 'Task 5', '2023-11-12 09:00:00', 300, 'Description for Task 5', 3),
(6, 3, 'Task 6', '2023-11-12 10:00:00', 45, 'Description for Task 6', 3),
(7, 4, 'Task 7', '2023-11-13 09:00:00', 120, 'Description for Task 7', 4),
(8, 4, 'Task 8', '2023-11-13 10:00:00', 180, 'Description for Task 8', 4),
(9, 5, 'Task 9', '2023-11-14 09:00:00', 90, 'Description for Task 9', 5),
(10, 5, 'Task 10', '2023-11-14 10:15:00', 365, 'Description for Task 10', 10);

INSERT INTO UserAlert (AlertID, UserID, AlertMessage, Alert_Info_AlertID) VALUES
(1, 1, 'Alert Message 1', 1),
(2, 2, 'Alert Message 2', 2),
(3, 3, 'Alert Message 3', 3),
(4, 4, 'Alert Message 4', 4),
(5, 5, 'Alert Message 5', 5),
(6, 6, 'Alert Message 6', 6),
(7, 7, 'Alert Message 7', 7),
(8, 8, 'Alert Message 8', 8),
(9, 9, 'Alert Message 9', 9),
(10, 10, 'Alert Message 10', 10);

INSERT INTO UserLogin (LoginID, UserID, LoginTime, LogoutTime) VALUES
(1, 1, '2023-11-10 08:00:00', '2023-11-10 17:00:00'),
(2, 2, '2023-11-10 09:00:00', '2023-11-10 18:00:00'),
(3, 3, '2023-11-11 08:30:00', '2023-11-11 17:30:00'),
(4, 4, '2023-11-11 09:30:00', '2023-11-11 18:30:00'),
(5, 5, '2023-11-12 08:00:00', '2023-11-12 17:00:00'),
(6, 6, '2023-11-12 09:00:00', '2023-11-12 18:00:00'),
(7, 7, '2023-11-13 08:30:00', '2023-11-13 17:30:00'),
(8, 8, '2023-11-13 09:30:00', '2023-11-13 18:30:00'),
(9, 9, '2023-11-14 08:00:00', '2023-11-14 17:00:00'),
(10, 10, '2023-11-14 09:00:00', '2023-11-14 18:00:00');

INSERT INTO AlertInfo (AlertID, UserID, AlertHistory) VALUES
(1, 1, 'History 1'),
(2, 2, 'History 2'),
(3, 3, 'History 3'),
(4, 4, 'History 4'),
(5, 5, 'History 5'),
(6, 6, 'History 6'),
(7, 7, 'History 7'),
(8, 8, 'History 8'),
(9, 9, 'History 9'),
(10, 10, 'History 10');

INSERT INTO Admin (Username, Password, Name, Certification, Address, PhoneNumber, Birthday) VALUES
('a-KevinReiff', 'adminpass1', 'Kevin Reiff', 'Certified', '123 Admin St', '111-222-3333', '1980-01-01'),
('a-janedoe', 'adminpass2', 'Admin Two', 'Certified', '124 Admin St', '111-222-3334', '1982-02-02'),
('a-mikeb', 'adminpass3', 'Admin Three', 'Certified', '125 Admin St', '111-222-3335', '1978-03-03'),
('a-emmagreen', 'adminpass4', 'Admin Four', 'Certified', '126 Admin St', '111-222-3336', '1985-04-04'),
('a-samw', 'adminpass5', 'Admin Five', 'Certified', '127 Admin St', '111-222-3337', '1981-05-05'),
('a-lucyp', 'adminpass6', 'Admin Six', 'Certified', '128 Admin St', '111-222-3338', '1979-06-06'),
('a-davidt', 'adminpass7', 'Admin Seven', 'Certified', '129 Admin St', '111-222-3339', '1983-07-07'),
('a-sarahc', 'adminpass8', 'Admin Eight', 'Certified', '130 Admin St', '111-222-3340', '1984-08-08'),
('a-rickg', 'adminpass9', 'Admin Nine', 'Certified', '131 Admin St', '111-222-3341', '1986-09-09'),
('a-annak', 'adminpass10', 'Admin Ten', 'Certified', '132 Admin St', '111-222-3342', '1980-10-10');


INSERT INTO AdminLogin (LoginID, AdminID, LoginTime, LogoutTime) VALUES
(1, 1, '2023-11-10 08:00:00', '2023-11-10 17:00:00'),
(2, 2, '2023-11-10 09:00:00', '2023-11-10 18:00:00'),
(3, 3, '2023-11-11 08:30:00', '2023-11-11 17:30:00'),
(4, 4, '2023-11-11 09:30:00', '2023-11-11 18:30:00'),
(5, 5, '2023-11-12 08:00:00', '2023-11-12 17:00:00'),
(6, 6, '2023-11-12 09:00:00', '2023-11-12 18:00:00'),
(7, 7, '2023-11-13 08:30:00', '2023-11-13 17:30:00'),
(8, 8, '2023-11-13 09:30:00', '2023-11-13 18:30:00'),
(9, 9, '2023-11-14 08:00:00', '2023-11-14 17:00:00'),
(10, 10, '2023-11-14 09:00:00', '2023-11-14 18:00:00');

INSERT INTO AdminSettings (SettingsID, AdminID, NotificationSettings) VALUES
(1, 1, 'Email'),
(2, 2, 'SMS'),
(3, 3, 'Email, SMS'),
(4, 4, NULL),
(5, 5, 'Email'),
(6, 6, 'SMS'),
(7, 7, NULL),
(8, 8, 'Email, SMS'),
(9, 9, 'Email'),
(10, 10, 'SMS');

SET FOREIGN_KEY_CHECKS=0;

select * from User;
select * from UserSettings;
select * from Admin;
select * from Task;
select * from Calendar;
select * from UserAlert;
select * from UserLogin;
select * from AlertInfo;
