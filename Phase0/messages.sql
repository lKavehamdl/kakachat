CREATE TABLE messages(
phoneNumber1 INT,
phoneNumber2 INT,
groupID INT,
groupName VARCHAR(255),
message VARCHAR(2047),
FOREIGN KEY (phonenumber2, groupId) REFERENCES chats(phoneNumber2, groupID)
);

