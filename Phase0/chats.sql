CREATE TABLE chats(
phoneNumber1 INT NOT NULL,
phoneNumber2 INT,
groupName VARCHAR(255),
groupID INT UNIQUE AUTO_INCREMENT,
PRIMARY KEY(phoneNumber2, groupId),
FOREIGN KEY(phoneNumber1) REFERENCES authentication(phoneNumber)
);