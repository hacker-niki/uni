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
    name VARCHAR(50)
);

DROP TABLE diff_table;
DROP TABLE foreign_table;
DROP TABLE common_table;


CREATE OR REPLACE PROCEDURE proc AS
BEGIN
  DBMS_OUTPUT.PUT_LINE('qwer');
END;

CREATE OR REPLACE FUNCTION func
RETURN VARCHAR AS
BEGIN
  RETURN 'qwe';
END;


DROP PROCEDURE proc;
DROP FUNCTION func;


CREATE TABLE cycle1 (
    id INT PRIMARY KEY,
    cycle2_id INT
);

CREATE TABLE cycle2 (
    id INT PRIMARY KEY,
    cycle1_id INT,
    FOREIGN KEY (cycle1_id) REFERENCES cycle1(id)
);

ALTER TABLE cycle1
ADD CONSTRAINT fk_cycle2_id
FOREIGN KEY (cycle2_id) REFERENCES cycle2(id);

alter table cycle1
drop constraint fk_cycle2_id;

drop table CYCLE1;

