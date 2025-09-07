-- Task 1
CREATE TABLE Students (
    Id NUMBER,
    Name VARCHAR2(100),
    GroupId NUMBER
);

CREATE TABLE Groups (
    Id NUMBER, 
    Name Varchar2(100),
    C_Val Number
);



-- Task 2
-- Создание последовательностей для генерации ID
CREATE SEQUENCE groups_seq START WITH 1 INCREMENT BY 1;
/
CREATE SEQUENCE students_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER auto_increment_id_groups
BEFORE INSERT ON Groups
FOR EACH ROW
BEGIN
    IF :NEW.Id IS NULL THEN
        :NEW.Id := groups_seq.NEXTVAL;
    END IF;
END;


CREATE OR REPLACE TRIGGER auto_increment_id_students
BEFORE INSERT ON Students
FOR EACH ROW
BEGIN
    IF :NEW.Id IS NULL THEN
        :NEW.Id := students_seq.NEXTVAL;
    END IF;
END;

CREATE OR REPLACE TRIGGER students_bi_trg
BEFORE INSERT ON Students
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT NVL(MAX(id), 0) + 1 INTO :NEW.id FROM GROUPS;
    ELSE
        SELECT COUNT(*) INTO v_count FROM Students WHERE Id = :NEW.Id;
        IF v_count > 0 THEN
            RAISE_APPLICATION_ERROR(-20001, 'Duplicate student ID');
        END IF;
    END IF;
END;

CREATE OR REPLACE TRIGGER groups_bi_trg
BEFORE INSERT ON Groups
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    IF :NEW.Id IS NULL THEN
        SELECT groups_id_seq.NEXTVAL INTO :NEW.Id FROM DUAL;
    ELSE
        SELECT COUNT(*) INTO v_count FROM Groups WHERE Id = :NEW.Id;
        IF v_count > 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'Duplicate group ID');
        END IF;
    END IF;
    SELECT COUNT(*) INTO v_count 
    FROM Groups 
    WHERE Name = :NEW.Name 
        AND Id != NVL(:NEW.Id, -1); 
    IF v_count > 0 THEN
        RAISE_APPLICATION_ERROR(-20003, 'Group name must be unique');
    END IF;
END;



INSERT INTO Groups (Name, C_Val) VALUES ('Group A', 0);
INSERT INTO Groups (Id, Name, C_Val) VALUES (2, 'Group B', 0);
SELECT * FROM Groups;

INSERT INTO Students (Name, GroupId) VALUES ('Student A', 1);
INSERT INTO Students (Id, Name, GroupId) VALUES (1, 'Student B', 1);
SELECT * FROM Students;

-- Task 3
CREATE OR REPLACE TRIGGER students_fk_check
BEFORE INSERT OR UPDATE ON Students
FOR EACH ROW
DECLARE
    v_group_exists NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_group_exists 
    FROM Groups 
    WHERE Id = :NEW.GroupId;

    IF v_group_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'GroupId ' || :NEW.GroupId || ' does not exist in Groups');
    END IF;
END;

CREATE OR REPLACE TRIGGER groups_cascade_delete
BEFORE DELETE ON Groups
FOR EACH ROW
BEGIN
    DELETE FROM Students WHERE GroupId = :OLD.Id;
END;

INSERT INTO Students (Name, GroupId) VALUES ('Alice', 999);

DELETE FROM Groups WHERE Id = 1;

-- Task 4
CREATE TABLE Students_Audit (  
"LOG_ID" NUMBER, 
"ACTION_TYPE" VARCHAR2(10) NOT NULL ENABLE, 
"STUDENT_ID" NUMBER, 
"STUDENT_NAME" VARCHAR2(50), 
"GROUP_ID" NUMBER, 
"ACTION_TIME" TIMESTAMP (6) DEFAULT CURRENT_TIMESTAMP, 
"GROUP_NAME" VARCHAR2(100), 
PRIMARY KEY ("LOG_ID")
);

create or replace TRIGGER log_delete_student
BEFORE DELETE ON STUDENTS
FOR EACH ROW
DECLARE
    v_group_name VARCHAR2(50); -- Переменная для хранения имени группы
BEGIN
    -- Проверяем, была ли удалена группа для этого студента
    BEGIN
        -- Читаем имя группы из временной таблицы temp_deleted_groups_names
        SELECT t.group_name
        INTO v_group_name
        FROM temp_deleted_groups t
        WHERE t.group_id = :OLD.group_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
           -- Если имя группы нигде не найдено, записываем "UNKNOWN"
                    v_group_name := 'UNKNOWN GROUP' || :OLD.group_id;
    END;

    -- Вставка записи в STUDENT_LOG с автоинкрементом log_id и именем группы
    INSERT INTO Students_Audit (log_id, action_type, student_id, student_name, group_id, group_name)
    VALUES (student_log_seq.NEXTVAL, 'DELETE', :OLD.id, :OLD.name, :OLD.group_id, v_group_name);
END;

create or replace TRIGGER log_insert_student
AFTER INSERT ON STUDENTS
FOR EACH ROW
DECLARE
    v_group_name VARCHAR2(100); -- Переменная для хранения имени группы
BEGIN
     -- Получаем имя группы из таблицы GROUPS
    SELECT name
    INTO v_group_name
    FROM GROUPS
    WHERE id = :NEW.group_id;

    -- Вставка записи в STUDENT_LOG с автоинкрементом log_id
    INSERT INTO STUDENT_LOG (log_id, action_type, student_id, student_name, group_id, group_name)
    VALUES (student_log_seq.NEXTVAL, 'INSERT', :NEW.id, :NEW.name, :NEW.group_id, v_group_name);
END;


create or replace TRIGGER log_update_student
AFTER UPDATE ON STUDENTS
FOR EACH ROW
DECLARE
    v_group_name VARCHAR2(100); -- Переменная для хранения имени группы
BEGIN
     -- Получаем имя группы из таблицы GROUPS
    SELECT name
    INTO v_group_name
    FROM GROUPS
    WHERE id = :OLD.group_id;
    -- Вставка записи в STUDENT_LOG с автоинкрементом log_id
    INSERT INTO Students_Audit (log_id, action_type, student_id, student_name, group_id, group_name)
    VALUES (student_log_seq.NEXTVAL, 'UPDATE', :OLD.id, :OLD.name, :OLD.group_id, v_group_name);
END;


-- Task 6
CREATE OR REPLACE TRIGGER update_group_cval
AFTER INSERT OR DELETE OR UPDATE OF GroupId ON Students
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        UPDATE Groups 
        SET C_Val = C_Val + 1 
        WHERE Id = :NEW.GroupId;
    END IF;

    IF DELETING THEN
        UPDATE Groups 
        SET C_Val = C_Val - 1 
        WHERE Id = :OLD.GroupId;
    END IF;

    IF UPDATING THEN
        IF :OLD.GroupId != :NEW.GroupId THEN
            UPDATE Groups 
            SET C_Val = C_Val - 1 
            WHERE Id = :OLD.GroupId;

            UPDATE Groups 
            SET C_Val = C_Val + 1 
            WHERE Id = :NEW.GroupId;
        END IF;
    END IF;
END;

INSERT INTO Students (Id, Name, GroupId) VALUES (3, 'Alice', 2);

UPDATE Students SET GroupId = 5 WHERE Id = 1;

DELETE FROM Students WHERE Id = 1;

SELECT * FROM Groups;
