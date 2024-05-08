CREATE TABLE authentication(
ID VARCHAR(255),
phoneNumber INT UNIQUE NOT NULL,
IP VARCHAR(15),
saveLogin BIT,
PRIMARY KEY(ID, phoneNumber),
FOREIGN KEY(ID, phoneNumber) REFERENCES users(ID, phoneNumber)
);