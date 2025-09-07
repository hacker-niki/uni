CREATE OR REPLACE TRIGGER STUDENTS_COUNT_IN_GROUPS_UPDATE
AFTER INSERT OR DELETE ON STUDENTS
FOR EACH ROW
BEGIN
    IF NOT group_management.is_deleting_groups THEN
        group_management.is_updating_count := TRUE;
        IF INSERTING THEN
            UPDATE GROUPS
            SET C_VAL = C_VAL + 1
            WHERE ID = :NEW.GROUP_ID;
        ELSIF DELETING THEN
            UPDATE GROUPS
            SET C_VAL = C_VAL - 1
            WHERE ID = :OLD.GROUP_ID;
        END IF;
        group_management.is_updating_count := FALSE;
    END IF;
END;
/