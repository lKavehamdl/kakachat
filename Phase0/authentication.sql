CREATE TABLE authentication(
ID VARCHAR(255),
phoneNumber INT,
IP VARCHAR(15),
saveLogin BIT,
PRIMARY KEY(ID, phoneNumber),
FOREIGN KEY(ID, phoneNumber) REFERENCES users(ID, phoneNumber)
);