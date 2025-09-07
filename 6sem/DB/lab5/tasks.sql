-- Журналирование + откат

CREATE TABLE Tab1Log(
    id NUMBER PRIMARY KEY,
    operation VARCHAR2(10),
    op_time TIMESTAMP,
    n_id NUMBER,
    o_id NUMBER,
    n_name VARCHAR2(20),
    o_name VARCHAR2(20),
    n_val NUMBER,
    o_val NUMBER
);
/
CREATE SEQUENCE tab1_id_seq
START WITH 1
INCREMENT BY 1;
/
CREATE TABLE Tab2Log(
    id NUMBER PRIMARY KEY,
    operation VARCHAR2(10),
    op_time TIMESTAMP,
    n_id NUMBER,
    o_id NUMBER,
    n_name VARCHAR2(20),
    o_name VARCHAR2(20),
    n_time TIMESTAMP,
    o_time TimeSTAMP
);
/
CREATE SEQUENCE tab2_id_seq
START WITH 1
INCREMENT BY 1;
/
CREATE TABLE Tab3Log(
    id NUMBER PRIMARY KEY,
    operation VARCHAR2(10),
    op_time TIMESTAMP,
    n_id NUMBER,
    o_id NUMBER,
    n_name VARCHAR2(20),
    o_name VARCHAR2(20),
    n_fk INT,
    o_fk INT
);
/
CREATE SEQUENCE tab3_id_seq
START WITH 1
INCREMENT BY 1;
/
CREATE TABLE TabsLog(
    id NUMBER PRIMARY KEY,
    op_time TIMESTAMP,
    tab_id NUMBER,
    tab_type NUMBER
);
/
CREATE SEQUENCE tabs_id_seq
START WITH 1
INCREMENT BY 1;
/
CREATE OR REPLACE TRIGGER Tabs_1_logger
BEFORE INSERT OR DELETE 
ON Tab1Log FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO TabsLog (id, op_time, tab_id, tab_type) 
        VALUES (tabs_id_seq.nextval, CURRENT_TIMESTAMP, :NEW.id, 1);
    ELSIF DELETING THEN
        DELETE FROM TabsLog WHERE tab_id = :OLD.id AND tab_type = 1;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER Tabs_2_logger
BEFORE INSERT OR DELETE 
ON Tab2Log FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO TabsLog (id, op_time, tab_id, tab_type) 
        VALUES (tabs_id_seq.nextval, CURRENT_TIMESTAMP, :NEW.id, 2);
    ELSIF DELETING THEN
        DELETE FROM TabsLog WHERE tab_id = :OLD.id AND tab_type = 2;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER Tabs_3_logger
BEFORE INSERT OR DELETE 
ON Tab3Log FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO TabsLog (id, op_time, tab_id, tab_type) 
        VALUES (tabs_id_seq.nextval, CURRENT_TIMESTAMP, :NEW.id, 3);
    ELSIF DELETING THEN
        DELETE FROM TabsLog WHERE tab_id = :OLD.id AND tab_type = 3;
    END IF;
END;
/


CREATE OR REPLACE TRIGGER Tab1_logger
BEFORE INSERT OR UPDATE OR DELETE 
ON Tab1 FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO Tab1Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_val, o_val) 
        VALUES (tab1_id_seq.nextval, 'INSERT', CURRENT_TIMESTAMP, :NEW.id, NULL, :NEW.name, NULL, :NEW.val, NULL);
    ELSIF UPDATING THEN
        INSERT INTO Tab1Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_val, o_val) 
        VALUES (tab1_id_seq.nextval, 'UPDATE', CURRENT_TIMESTAMP, :NEW.id, :OLD.id, :NEW.name, :OLD.name, :NEW.val, :OLD.val);
	END IF;
END;
/

CREATE OR REPLACE TRIGGER Tab1_logger_Del
AFTER DELETE 
ON Tab1 FOR EACH ROW
DECLARE
BEGIN
    INSERT INTO Tab1Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_val, o_val) 
    VALUES (tab1_id_seq.nextval, 'DELETE', CURRENT_TIMESTAMP, NULL, :OLD.id, NULL, :OLD.name, NULL, :OLD.val);
END;
/

CREATE OR REPLACE TRIGGER Tab2_logger
BEFORE INSERT OR UPDATE OR DELETE 
ON Tab2 FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO Tab2Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_time, o_time) 
        VALUES (tab2_id_seq.nextval, 'INSERT', CURRENT_TIMESTAMP, :NEW.id, NULL, :NEW.name, NULL, :NEW.time, NULL);
    ELSIF UPDATING THEN
        INSERT INTO Tab2Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_time, o_time) 
        VALUES (tab2_id_seq.nextval, 'UPDATE', CURRENT_TIMESTAMP, :NEW.id, :OLD.id, :NEW.name, :OLD.name, :NEW.time, :OLD.time);
    ELSIF DELETING THEN
        INSERT INTO Tab2Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_time, o_time) 
        VALUES (tab2_id_seq.nextval, 'DELETE', CURRENT_TIMESTAMP, NULL, :OLD.id, NULL, :OLD.name, NULL, :OLD.time);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER Tab3_logger
BEFORE INSERT OR UPDATE
ON Tab3 FOR EACH ROW
DECLARE
BEGIN
    IF INSERTING THEN
        INSERT INTO Tab3Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_fk, o_fk) 
        VALUES (tab3_id_seq.nextval, 'INSERT', CURRENT_TIMESTAMP, :NEW.id, NULL, :NEW.name, NULL, :NEW.Tab1_Id, NULL);
    ELSIF UPDATING THEN
        INSERT INTO Tab3Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_fk, o_fk) 
        VALUES (tab3_id_seq.nextval, 'UPDATE', CURRENT_TIMESTAMP, :NEW.id, :OLD.id, :NEW.name, :OLD.name, :NEW.Tab1_Id, :OLD.Tab1_Id);
	END IF;
END;
/

CREATE OR REPLACE TRIGGER Tab3_logger_Del
AFTER DELETE 
ON Tab3 FOR EACH ROW
DECLARE
BEGIN
    INSERT INTO Tab3Log (id, operation, op_time, n_id, o_id, n_name, o_name, n_fk, o_fk) 
        VALUES (tab3_id_seq.nextval, 'DELETE', CURRENT_TIMESTAMP, NULL, :OLD.id, NULL, :OLD.name, NULL, :OLD.Tab1_Id);
END;
/


CREATE OR REPLACE PACKAGE recovery_package AS
    PROCEDURE Tabs_recovery(p_datetime TIMESTAMP);
    PROCEDURE Tabs_recovery(p_seconds INT);
END recovery_package;
/

CREATE OR REPLACE PACKAGE BODY recovery_package AS

    PROCEDURE Tabs_recovery(p_datetime TIMESTAMP) AS
        tab1_record Tab1Log%ROWTYPE;
        tab2_record Tab2Log%ROWTYPE;
        tab3_record Tab3Log%ROWTYPE;
    BEGIN
        FOR action IN (SELECT * FROM TabsLog WHERE p_datetime < op_time ORDER BY id DESC)
        LOOP
            -- Если действие для первой таблицы
            IF action.tab_type = 1 THEN
                SELECT * INTO tab1_record FROM Tab1Log WHERE id = action.tab_id;

                IF tab1_record.operation = 'INSERT' THEN
                    DELETE FROM Tab1 WHERE id = tab1_record.n_id;
                END IF;

                IF tab1_record.operation = 'UPDATE' THEN
                    UPDATE Tab1 SET
                        id = tab1_record.o_id,
                        name = tab1_record.o_name,
                        val = tab1_record.o_val
                    WHERE id = tab1_record.n_id;
                END IF;

                IF tab1_record.operation = 'DELETE' THEN
                    INSERT INTO Tab1 VALUES (tab1_record.o_id, tab1_record.o_name, tab1_record.o_val);
                END IF;

            -- Если действие для второй таблицы
            ELSIF action.tab_type = 2 THEN
                SELECT * INTO tab2_record FROM Tab2Log WHERE id = action.tab_id;

                IF tab2_record.operation = 'INSERT' THEN
                    DELETE FROM Tab2 WHERE id = tab2_record.n_id;
                END IF;

                IF tab2_record.operation = 'UPDATE' THEN
                    UPDATE Tab2 SET
                        id = tab2_record.o_id,
                        name = tab2_record.o_name,
                        time = tab2_record.o_time
                    WHERE id = tab2_record.n_id;
                END IF;

                IF tab2_record.operation = 'DELETE' THEN
                    INSERT INTO Tab2 VALUES (tab2_record.o_id, tab2_record.o_name, tab2_record.o_time);
                END IF;
            -- Если действие для третьей таблицы
            ELSIF action.tab_type = 3 THEN
                SELECT * INTO tab3_record FROM Tab3Log WHERE id = action.tab_id;

                IF tab3_record.operation = 'INSERT' THEN
                    DELETE FROM Tab3 WHERE id = tab3_record.n_id;
                END IF;

                IF tab3_record.operation = 'UPDATE' THEN
                    UPDATE Tab3 SET
                        id = tab3_record.o_id,
                        name = tab3_record.o_name,
                        Tab1_Id = tab3_record.o_fk
                    WHERE id = tab3_record.n_id;
                END IF;

                IF tab3_record.operation = 'DELETE' THEN
                    INSERT INTO Tab3 VALUES (tab3_record.o_id, tab3_record.o_name, tab3_record.o_fk);
                END IF;
            END IF;
        END LOOP;

        DELETE FROM Tab1Log WHERE op_time > p_datetime;
        DELETE FROM Tab2Log WHERE op_time > p_datetime;
        DELETE FROM Tab3Log WHERE op_time > p_datetime;
    END Tabs_recovery;


    PROCEDURE Tabs_recovery(p_seconds INT) AS
    BEGIN
        Tabs_recovery(CURRENT_TIMESTAMP - INTERVAL '1' SECOND * p_seconds);
    END Tabs_recovery;

END recovery_package;
/




CREATE OR REPLACE PACKAGE otchet_packege AS
    -- Функция для генерации HTML-отчёта
    FUNCTION get_html(
        p_title IN VARCHAR2,
        p_insert_count IN NUMBER,
        p_update_count IN NUMBER,
        p_delete_count IN NUMBER
    ) RETURN VARCHAR2;

    -- Процедуры отчётов для каждой таблицы с указанием времени
    PROCEDURE Tab1_report(p_datetime IN TIMESTAMP);
    PROCEDURE Tab2_report(p_datetime IN TIMESTAMP);
    PROCEDURE Tab3_report(p_datetime IN TIMESTAMP);

    -- Процедуры отчётов для каждой таблицы с последнего отчёта
    PROCEDURE Tab1_report;
    PROCEDURE Tab2_report;
    PROCEDURE Tab3_report;

    -- Процедура для общего отчёта по всем таблицам
    PROCEDURE Tabs_report(p_datetime IN TIMESTAMP);
    PROCEDURE Tabs_report;
END otchet_packege;
/



CREATE OR REPLACE PACKAGE BODY otchet_packege AS
    -- Вспомогательная функция для генерации HTML
    FUNCTION get_html(
        p_title IN VARCHAR2,
        p_insert_count IN NUMBER,
        p_update_count IN NUMBER,
        p_delete_count IN NUMBER
    ) RETURN VARCHAR2 IS
        v_result VARCHAR2(4000);
    BEGIN
        v_result := '<!DOCTYPE html>' || CHR(10) ||
                    '<html lang="en">' || CHR(10) ||
                    '<head><meta charset="UTF-8"></head>' || CHR(10) || -- Добавлена кодировка
                    '<body>' || CHR(10) ||
                    '<h2>' || p_title || '</h2>' || CHR(10) ||
                    '<table border="1">' || CHR(10) || -- Добавлена рамка для таблицы
                    '    <tr>' || CHR(10) ||
                    '        <th>Операция</th>' || CHR(10) ||
                    '        <th>Количество</th>' || CHR(10) ||
                    '    </tr>' || CHR(10) ||
                    '    <tr>' || CHR(10) ||
                    '        <td>INSERT</td>' || CHR(10) ||
                    '        <td>' || NVL(p_insert_count, 0) || '</td>' || CHR(10) || -- NVL для NULL
                    '    </tr>' || CHR(10) ||
                    '    <tr>' || CHR(10) ||
                    '        <td>UPDATE</td>' || CHR(10) ||
                    '        <td>' || NVL(p_update_count, 0) || '</td>' || CHR(10) ||
                    '    </tr>' || CHR(10) ||
                    '    <tr>' || CHR(10) ||
                    '        <td>DELETE</td>' || CHR(10) ||
                    '        <td>' || NVL(p_delete_count, 0) || '</td>' || CHR(10) ||
                    '    </tr>' || CHR(10) ||
                    '</table>' || CHR(10) ||
                    '</body>' || CHR(10) ||
                    '</html>';
        DBMS_OUTPUT.PUT_LINE(v_result); -- Вывод для отладки
        RETURN v_result;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в get_html: ' || SQLERRM);
            RAISE;
    END get_html;

    -- Отчёт для Tab1 с указанием времени
    PROCEDURE Tab1_report(p_datetime IN TIMESTAMP) AS
        v_file_handle UTL_FILE.FILE_TYPE;
        v_title VARCHAR2(100);
        v_insert_count NUMBER := 0;
        v_update_count NUMBER := 0;
        v_delete_count NUMBER := 0;
        v_result VARCHAR2(4000);
    BEGIN
        v_title := 'Таблица 1 с ' || TO_CHAR(p_datetime, 'DD.MM.YYYY HH24:MI:SS');
        
        -- Подсчёт операций
        SELECT COUNT(*) INTO v_insert_count 
        FROM Tab1Log 
        WHERE operation = 'INSERT' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_update_count 
        FROM Tab1Log 
        WHERE operation = 'UPDATE' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_delete_count 
        FROM Tab1Log 
        WHERE operation = 'DELETE' AND p_datetime <= op_time;

        -- Генерация HTML
        v_result := get_html(v_title, v_insert_count, v_update_count, v_delete_count);

        -- Запись в файл
        v_file_handle := UTL_FILE.FOPEN('MY_DIRECTORY', 'tab1.html', 'W');
        UTL_FILE.PUT_LINE(v_file_handle, v_result);
        UTL_FILE.FCLOSE(v_file_handle);

        -- Обновление времени последнего отчёта
        UPDATE LastOtchet 
        SET Time = p_datetime 
        WHERE TableName = 'Tab1';
        
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO LastOtchet (TableName, Time) 
            VALUES ('Tab1', p_datetime);
        END IF;
    EXCEPTION
        WHEN UTL_FILE.INVALID_PATH THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка: Неверный путь к директории MY_DIRECTORY');
            RAISE;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в Tab1_report: ' || SQLERRM);
            IF UTL_FILE.IS_OPEN(v_file_handle) THEN
                UTL_FILE.FCLOSE(v_file_handle);
            END IF;
            RAISE;
    END Tab1_report;

    -- Отчёт для Tab1 с последнего отчёта
    PROCEDURE Tab1_report AS
        v_time TIMESTAMP;
    BEGIN
        BEGIN
            SELECT Time INTO v_time 
            FROM LastOtchet 
            WHERE TableName = 'Tab1';
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_time := NULL;
        END;

        IF v_time IS NULL THEN
            SELECT MIN(op_time) INTO v_time 
            FROM Tab1Log;
            IF v_time IS NULL THEN
                v_time := CURRENT_TIMESTAMP; -- Если логов нет, берём текущее время
            END IF;
        END IF;

        Tab1_report(v_time);
    END Tab1_report;

    -- Отчёт для Tab2 с указанием времени
    PROCEDURE Tab2_report(p_datetime IN TIMESTAMP) AS
        v_file_handle UTL_FILE.FILE_TYPE;
        v_title VARCHAR2(100);
        v_insert_count NUMBER := 0;
        v_update_count NUMBER := 0;
        v_delete_count NUMBER := 0;
        v_result VARCHAR2(4000);
    BEGIN
        v_title := 'Таблица 2 с ' || TO_CHAR(p_datetime, 'DD.MM.YYYY HH24:MI:SS');
        
        -- Подсчёт операций
        SELECT COUNT(*) INTO v_insert_count 
        FROM Tab2Log 
        WHERE operation = 'INSERT' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_update_count 
        FROM Tab2Log 
        WHERE operation = 'UPDATE' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_delete_count 
        FROM Tab2Log 
        WHERE operation = 'DELETE' AND p_datetime <= op_time;

        -- Генерация HTML
        v_result := get_html(v_title, v_insert_count, v_update_count, v_delete_count);

        -- Запись в файл
        v_file_handle := UTL_FILE.FOPEN('MY_DIRECTORY', 'tab2.html', 'W');
        UTL_FILE.PUT_LINE(v_file_handle, v_result);
        UTL_FILE.FCLOSE(v_file_handle);

        -- Обновление времени последнего отчёта
        UPDATE LastOtchet 
        SET Time = p_datetime 
        WHERE TableName = 'Tab2';
        
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO LastOtchet (TableName, Time) 
            VALUES ('Tab2', p_datetime);
        END IF;
    EXCEPTION
        WHEN UTL_FILE.INVALID_PATH THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка: Неверный путь к директории MY_DIRECTORY');
            RAISE;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в Tab2_report: ' || SQLERRM);
            IF UTL_FILE.IS_OPEN(v_file_handle) THEN
                UTL_FILE.FCLOSE(v_file_handle);
            END IF;
            RAISE;
    END Tab2_report;

    -- Отчёт для Tab2 с последнего отчёта
    PROCEDURE Tab2_report AS
        v_time TIMESTAMP;
    BEGIN
        BEGIN
            SELECT Time INTO v_time 
            FROM LastOtchet 
            WHERE TableName = 'Tab2';
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_time := NULL;
        END;

        IF v_time IS NULL THEN
            SELECT MIN(op_time) INTO v_time 
            FROM Tab2Log;
            IF v_time IS NULL THEN
                v_time := CURRENT_TIMESTAMP;
            END IF;
        END IF;

        Tab2_report(v_time);
    END Tab2_report;

    -- Отчёт для Tab3 с указанием времени
    PROCEDURE Tab3_report(p_datetime IN TIMESTAMP) AS
        v_file_handle UTL_FILE.FILE_TYPE;
        v_title VARCHAR2(100);
        v_insert_count NUMBER := 0;
        v_update_count NUMBER := 0;
        v_delete_count NUMBER := 0;
        v_result VARCHAR2(4000);
    BEGIN
        v_title := 'Таблица 3 с ' || TO_CHAR(p_datetime, 'DD.MM.YYYY HH24:MI:SS');
        
        -- Подсчёт операций
        SELECT COUNT(*) INTO v_insert_count 
        FROM Tab3Log 
        WHERE operation = 'INSERT' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_update_count 
        FROM Tab3Log 
        WHERE operation = 'UPDATE' AND p_datetime <= op_time;
        
        SELECT COUNT(*) INTO v_delete_count 
        FROM Tab3Log 
        WHERE operation = 'DELETE' AND p_datetime <= op_time;

        -- Генерация HTML
        v_result := get_html(v_title, v_insert_count, v_update_count, v_delete_count);

        -- Запись в файл
        v_file_handle := UTL_FILE.FOPEN('MY_DIRECTORY', 'tab3.html', 'W');
        UTL_FILE.PUT_LINE(v_file_handle, v_result);
        UTL_FILE.FCLOSE(v_file_handle);

        -- Обновление времени последнего отчёта
        UPDATE LastOtchet 
        SET Time = p_datetime 
        WHERE TableName = 'Tab3';
        
        IF SQL%ROWCOUNT = 0 THEN
            INSERT INTO LastOtchet (TableName, Time) 
            VALUES ('Tab3', p_datetime);
        END IF;
    EXCEPTION
        WHEN UTL_FILE.INVALID_PATH THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка: Неверный путь к директории MY_DIRECTORY');
            RAISE;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в Tab3_report: ' || SQLERRM);
            IF UTL_FILE.IS_OPEN(v_file_handle) THEN
                UTL_FILE.FCLOSE(v_file_handle);
            END IF;
            RAISE;
    END Tab3_report;

    -- Отчёт для Tab3 с последнего отчёта
    PROCEDURE Tab3_report AS
        v_time TIMESTAMP;
    BEGIN
        BEGIN
            SELECT Time INTO v_time 
            FROM LastOtchet 
            WHERE TableName = 'Tab3';
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_time := NULL;
        END;

        IF v_time IS NULL THEN
            SELECT MIN(op_time) INTO v_time 
            FROM Tab3Log;
            IF v_time IS NULL THEN
                v_time := CURRENT_TIMESTAMP;
            END IF;
        END IF;

        Tab3_report(v_time);
    END Tab3_report;

    -- Общий отчёт для всех таблиц с указанием времени
    PROCEDURE Tabs_report(p_datetime IN TIMESTAMP) AS
    BEGIN
        Tab1_report(p_datetime);
        Tab2_report(p_datetime);
        Tab3_report(p_datetime);
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в Tabs_report (с временем): ' || SQLERRM);
            RAISE;
    END Tabs_report;

    -- Общий отчёт для всех таблиц с последнего отчёта
    PROCEDURE Tabs_report AS
    BEGIN
        Tab1_report;
        Tab2_report;
        Tab3_report;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка в Tabs_report (без времени): ' || SQLERRM);
            RAISE;
    END Tabs_report;

END otchet_packege;
/


