CREATE OR REPLACE PROCEDURE RESTORE_STUDENTS(
    p_restore_time TIMESTAMP,
    p_time_offset INTERVAL DAY TO SECOND DEFAULT NULL
) AS
    v_restore_time TIMESTAMP := p_restore_time;
BEGIN
    IF p_time_offset IS NOT NULL THEN
        v_restore_time := SYSTIMESTAMP - p_time_offset;
    END IF;

    DELETE FROM STUDENTS;

    FOR log_rec IN (
        SELECT * FROM STUDENTS_LOG
        WHERE ACTION_DATE <= v_restore_time
        ORDER BY ACTION_DATE
    ) LOOP
        IF log_rec.ACTION = 'INSERT' THEN
            INSERT INTO STUDENTS (ID, NAME, GROUP_ID)
            VALUES (log_rec.STUDENT_ID, log_rec.STUDENT_NAME, log_rec.GROUP_ID);
        ELSIF log_rec.ACTION = 'UPDATE' THEN
            UPDATE STUDENTS
            SET NAME = log_rec.STUDENT_NAME, GROUP_ID = log_rec.GROUP_ID
            WHERE ID = log_rec.STUDENT_ID;
        ELSIF log_rec.ACTION = 'DELETE' THEN
            DELETE FROM STUDENTS
            WHERE ID = log_rec.STUDENT_ID;
        END IF;
    END LOOP;
END;
/