CREATE OR REPLACE PACKAGE group_management AS
    is_deleting_groups BOOLEAN := FALSE;
    is_updating_count BOOLEAN := FALSE;
END group_management;
/

CREATE OR REPLACE TRIGGER GROUPS_CASCADE_DELETE
AFTER DELETE ON GROUPS
FOR EACH ROW
BEGIN
    group_management.is_deleting_groups := TRUE;
    DELETE FROM STUDENTS WHERE GROUP_ID = :OLD.ID;
    group_management.is_deleting_groups := FALSE; 
END;
/

CREATE OR REPLACE TRIGGER GROUPS_KEY
BEFORE INSERT ON STUDENTS
FOR EACH ROW
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM GROUPS
    WHERE ID = :NEW.GROUP_ID;

    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'ID should exist.');
    END IF;
END;