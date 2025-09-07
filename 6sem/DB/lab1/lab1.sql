
-------------------TASK 1 CREATE-----------------------

CREATE TABLE MyTable (
    id NUMBER,
    val NUMBER
);

----------------TASK 2 INSERT RANDOM-------------------

BEGIN
    FOR i IN 1..10000 LOOP
        INSERT INTO MyTable (id, val)
        VALUES (i, FLOOR(DBMS_RANDOM.VALUE(1, 100000)));
    END LOOP;
    COMMIT;
END;

----------------TASK 3 IS EVEN ODD--------------------

CREATE OR REPLACE FUNCTION check_even_odd RETURN VARCHAR2 IS
    even_count NUMBER;
    odd_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO even_count FROM MyTable WHERE MOD(val, 2) = 0;
    SELECT COUNT(*) INTO odd_count FROM MyTable WHERE MOD(val, 2) = 1;
    
    IF even_count > odd_count THEN
        RETURN 'TRUE';
    ELSIF odd_count > even_count THEN
        RETURN 'FALSE';
    ELSE
        RETURN 'EQUAL';
    END IF;
END;

--------------TASK 4 GENETATE INSERT-------------------

CREATE OR REPLACE FUNCTION generate_insert(p_id IN NUMBER) RETURN VARCHAR2 IS
    v_val NUMBER;
    v_sql VARCHAR2(100);
BEGIN
    SELECT val INTO v_val FROM MyTable WHERE id = p_id;
    v_sql := 'INSERT INTO MyTable VALUES (' || p_id || ', ' || v_val || ');';
    RETURN v_sql;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL; 
END;

-----------TASK 5 INSERT UDPDATE DELETE----------------

CREATE OR REPLACE PROCEDURE insert_mytable(p_id NUMBER, p_val NUMBER) IS
BEGIN
    INSERT INTO MyTable (id, val) VALUES (p_id, p_val);
END;

CREATE OR REPLACE PROCEDURE update_mytable(p_id NUMBER, p_val NUMBER) IS
BEGIN
    UPDATE MyTable SET val = p_val WHERE id = p_id;
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'No record found with id ' || p_id);
    END IF;
END;

CREATE OR REPLACE PROCEDURE delete_mytable(p_id NUMBER) IS
BEGIN
    DELETE FROM MyTable WHERE id = p_id;
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'No record found with id ' || p_id);
    END IF;
END;

-------------TASK 6 CALCULATE REWARD------------------

CREATE OR REPLACE FUNCTION calculate_total_reward(
    monthly_salary IN NUMBER,
    bonus_percent IN INTEGER
) RETURN NUMBER IS
    v_total NUMBER;
BEGIN
    IF monthly_salary < 0 OR bonus_percent < 0 THEN
        RAISE_APPLICATION_ERROR(-20003, 'Salary and bonus percent must be non-negative');
    END IF;
    
    v_total := (1 + bonus_percent / 100) * 12 * monthly_salary;
    RETURN v_total;
EXCEPTION
    WHEN OTHERS THEN
        RAISE;
END;

--------TESTS-------

-------TASK 3-------
DECLARE
    result VARCHAR2(5);
BEGIN
    result := check_even_odd();
    DBMS_OUTPUT.PUT_LINE('Result: ' || result);
END;

-------TASK 4-------
DECLARE
    result VARCHAR2(100);
BEGIN
    result := generate_insert(5);
    DBMS_OUTPUT.PUT_LINE('Insert SQL: ' || result);
END;

-------TASK 5-------
CALL insert_mytable(10001, 3424);
SELECT * 
	FROM MYTABLE m 
	WHERE m.ID = 10001;

CALL update_mytable(10001, 4321);
SELECT * 
	FROM MYTABLE m 
	WHERE m.ID = 10001;

CALL delete_mytable(10001);
SELECT * 
	FROM MYTABLE m 
	WHERE m.ID = 10001;

-------TASK 6-------
DECLARE
    result NUMBER;
BEGIN
    result := calculate_total_reward(10423.32, 34);
    DBMS_OUTPUT.PUT_LINE('Bonus: ' || result);
EXCEPTION
    WHEN OTHERS THEN
		DBMS_OUTPUT.PUT_LINE('ERROR: ' || SQLERRM);
END;
