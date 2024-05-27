DELIMITER //
CREATE TRIGGER chats_check
BEFORE INSERT ON chats
FOR EACH ROW
BEGIN
    DECLARE flag INT;
    SELECT COUNT(*) INTO flag
    FROM chats
    WHERE (phoneNumber1 = NEW.phoneNumber1 AND phoneNumber2 = NEW.phoneNumber2)
    OR (phoneNumber2 = NEW.phoneNumber1 AND phoneNumber2 = NEW.phoneNUmber1);
    IF flag > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate record found. Transaction rolled back.';
    END IF;
END //
DELIMITER ;


