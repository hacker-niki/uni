GRANT CREATE ANY TABLE TO ROOT;
GRANT DROP ANY TABLE TO ROOT;
GRANT ALTER ANY TABLE TO ROOT;
GRANT CREATE ANY TRIGGER TO ROOT;
GRANT DROP ANY TRIGGER TO ROOT;
GRANT EXECUTE ANY PROCEDURE TO ROOT;
GRANT CREATE ANY SEQUENCE TO ROOT;

DROP TABLE Employe1;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "CREATE",
        "table": "department1",
        "primary": "Id",
        "columns": [
            {"name": "Id", "datatype": "NUMBER", "constraint": "NOT NULL"},
            {"name": "Name", "datatype": "VARCHAR2(100)"}
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "CREATE",
        "table": "Employe1",
        "primary": "Id",
        "columns": [
            {"name": "Id", "datatype": "NUMBER"},
            {"name": "Name", "datatype": "VARCHAR2(100)", "constraint": "UNIQUE", "constraint": "NOT NULL"},
            {"name": "department1Id", "datatype": "NUMBER"}
        ],
        "foreign": [
            {"column": "department1Id", "reftable": "department1", "refcolumn": "Id"}
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/


DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "INSERT",
        "table": "department1",
        "columns": ["Id", "Name"],
        "values": [
            ["11", "Sales"],
            ["22", "Marketing"]
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "INSERT",
        "table": "Employe1",
        "columns": ["Name", "department1Id"],
        "values": [
            ["John Doe", "11"],
            ["Jane Smith", "22"]
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "UPDATE",
        "table": "Employe1",
        "set": [
            {"column": "Name", "value": "John Smith"},
            {"column": "department1Id", "value": "11"}
        ],
        "filters": [
            {
                "type": "WHERE",
                "body": ["Id = 2"]
            }
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "DELETE",
        "table": "Employe1",
        "filters": [
            {
                "type": "WHERE",
                "operator": "AND",
                "body": ["department1Id = 11", "Name LIKE ''%Doe%''"]
            }
        ]
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
    emp_id NUMBER;
    emp_name VARCHAR2(100);
    dept_name VARCHAR2(100);
BEGIN
    json_data := '{
        "type": "SELECT",
        "columns": ["e.Id", "e.Name", "d.Name AS department1Name"],
        "tables": ["Employe1 e"],
        "joins": [
            {
                "table": "department1 d",
                "condition": ["e.department1Id = d.Id"]
            }
        ],
        "filters": {
            "type": "WHERE",
            "operator": "AND",
            "body": [
                "e.Id > 0",
                "d.Name NOT LIKE ''%Test%''"
            ]
        }
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
    
    LOOP
        FETCH v_cursor INTO emp_id, emp_name, dept_name;
        EXIT WHEN v_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(emp_id || ', ' || emp_name || ', ' || dept_name);
    END LOOP;
    CLOSE v_cursor;
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
    emp_id NUMBER;
    emp_name VARCHAR2(100);
    dept_count NUMBER;
BEGIN
    json_data := '{
        "type": "SELECT",
        "columns": [
            "d.Id",
            "d.Name",
            {
                "type": "SELECT",
                "columns": ["COUNT(*)"],
                "tables": ["Employe1 e"],
                "filters": {
                    "type": "WHERE",
                    "operator": "AND",
                    "body": ["d.Id = e.department1Id"]
                }
            }
        ],
        "tables": ["department1 d"],
        "filters": {
            "type": "WHERE",
            "operator": "AND",
            "body": ["d.Id > 0"]
        }
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE('Сгенерированный SQL: ' || sql_result);
    
    LOOP
        FETCH v_cursor INTO emp_id, emp_name, dept_count;
        EXIT WHEN v_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(emp_id || ', ' || emp_name || ', ' || dept_count);
    END LOOP;
    CLOSE v_cursor;
END;
/

DECLARE
    json_data CLOB;
    sql_result VARCHAR2(4000);
    v_cursor SYS_REFCURSOR;
BEGIN
    json_data := '{
        "type": "DROP",
        "table": "Employe1"
    }';
    
    JSON_PARSE(json_data, sql_result, v_cursor);
    DBMS_OUTPUT.PUT_LINE(sql_result);
END;
/

