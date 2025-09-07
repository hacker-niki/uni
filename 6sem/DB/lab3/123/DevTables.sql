CREATE TABLE common_table (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE foreign_table (
    id INT PRIMARY KEY,
    common_id INT,
    FOREIGN KEY (common_id) REFERENCES common_table(id)
);

CREATE TABLE diff_table (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(100)
);

DROP TABLE diff_table;
DROP TABLE foreign_table;
DROP TABLE common_table;
DROP TABLE new_table;

CREATE TABLE new_table (
    id INT PRIMARY KEY,
    name VARCHAR(200)
);

CREATE OR REPLACE PROCEDURE proc AS
BEGIN
  DBMS_OUTPUT.PUT_LINE('qwe');
END;

CREATE OR REPLACE PROCEDURE proc2 AS
BEGIN
  DBMS_OUTPUT.PUT_LINE('qwe2');
END;

CREATE OR REPLACE FUNCTION func
RETURN VARCHAR AS
BEGIN
  RETURN 'qwe';
END;


DROP PROCEDURE proc;
DROP FUNCTION func;


