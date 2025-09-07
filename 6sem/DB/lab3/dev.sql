-- создаем схемы
CREATE USER dev_schema IDENTIFIED BY dev;

-- Инициализируем dev схему
CREATE TABLE dev_schema.common_table (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE dev_schema.foreign_table (
    id INT PRIMARY KEY,
    common_id INT,
    FOREIGN KEY (common_id) REFERENCES dev_schema.common_table(id)
);

CREATE TABLE dev_schema.diff_table (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(100)
);

CREATE TABLE dev_schema.new_table (
    id INT PRIMARY KEY,
    name VARCHAR(200)
);

CREATE OR REPLACE PROCEDURE dev_schema.my_procedure AS
BEGIN
  NULL;
END;
/


CREATE OR REPLACE FUNCTION dev_schema.my_function
RETURN NUMBER AS
BEGIN
  RETURN 1;
END;
/