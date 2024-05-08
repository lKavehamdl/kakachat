CREATE TABLE contacts(
phoneNumber1 INT,
phoneNumber2 INT,
PRIMARY KEY(phoneNumber1, phoneNumber2),
FOREIGN KEY(phoneNumber2) REFERENCES users(phoneNumber)
);

