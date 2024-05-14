DELIMITER //

CREATE TRIGGER chats_check
BEFORE INSERT ON chats
FOR EACH ROW
BEGIN
    DECLARE duplicate_count INT;

    -- Check if the new message already exists
    SELECT COUNT(*) INTO duplicate_count
    FROM chats
    WHERE phoneNumber1 = NEW.phoneNumber1 AND phoneNumber2 = NEW.phoneNumber2;

    -- If a duplicate is found, raise an error and rollback the transaction
    IF duplicate_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate record found. Transaction rolled back.';
    END IF;
END //

DELIMITER ;
