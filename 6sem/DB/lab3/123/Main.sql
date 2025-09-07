CREATE TABLE comparison_result(
    table_name VARCHAR2(100),
    is_different NUMBER(1) DEFAULT 0,
    is_only_in_dev_schema NUMBER(1) DEFAULT 0,
    is_only_in_prod_schema NUMBER(1) DEFAULT 0
);


CREATE TABLE sorted_tables (
    table_name VARCHAR2(100)
);

-- сортирует таблицы по внешнему ключу
CREATE OR REPLACE PROCEDURE sort_tables_in_schema(schema_name IN VARCHAR2) 
AS
BEGIN
    -- Проходимся циклом по всем таблицам, начиная с тех, у которых нет зависимостей
    FOR rec IN (
        -- Делаем рекурсивный запрос. Т.е. начинаем с таблиц без внешних ключей, а затем
        -- рекурсивное соединяет с другими таблицами через внешние ключи
        WITH DEPENDENCYTREE(table_name, lvl) AS (
            SELECT table_name, 1 AS lvl
            FROM all_tables
            WHERE owner = schema_name
            AND NOT EXISTS (
                SELECT 1
                FROM all_constraints
                WHERE constraint_type = 'R'
                AND r_constraint_name = constraint_name
            )
            UNION ALL
            SELECT a.table_name, b.lvl + 1
            FROM all_constraints a
            JOIN DEPENDENCYTREE b ON a.r_constraint_name = b.table_name
            WHERE a.owner = schema_name
            AND a.constraint_type = 'R'
        )
        SELECT table_name
        FROM DEPENDENCYTREE
        -- Сортируем по уровню вложенности
        ORDER BY lvl
    ) LOOP
        -- Вставляем имена всех таблиц
        BEGIN
            INSERT INTO sorted_tables (table_name) VALUES (rec.table_name);
        END;
    END LOOP;
END sort_tables_in_schema;


CREATE TABLE schema_dependencies(
    child_obj VARCHAR2(100), 
    parent_obj VARCHAR2(100)
);

-- Поиск циклических зависимостей
CREATE OR REPLACE PROCEDURE check_cyclic_dependencies(schema_name in VARCHAR2) 
AS
    result VARCHAR2(100);
BEGIN
    -- Перебираем все таблицы схемы          
    FOR schema_table IN (SELECT schema_tables.table_name name FROM all_tables schema_tables WHERE owner = schema_name) 
    LOOP
        -- Вставляем в таблицу уникальные пары родитель - ребенок по внешним ключам
        INSERT INTO schema_dependencies (child_obj, parent_obj)
            SELECT DISTINCT a.table_name, c_pk.table_name r_table_name FROM all_cons_columns a
            JOIN all_constraints c ON a.owner = c.owner AND a.constraint_name = c.constraint_name
            JOIN all_constraints c_pk ON c.r_owner = c_pk.owner AND c.r_constraint_name = c_pk.constraint_name
        WHERE c.constraint_type = 'R' AND a.table_name = schema_table.name;
    END LOOP;

    WITH Paths AS (
        SELECT child_obj, parent_obj, SYS_CONNECT_BY_PATH(child_obj, ',') AS path
        FROM schema_dependencies
        START WITH child_obj IN (SELECT DISTINCT child_obj FROM schema_dependencies)
        CONNECT BY NOCYCLE PRIOR parent_obj = child_obj
        AND LEVEL > 1
    )
    SELECT CASE 
             WHEN EXISTS (
               SELECT 1 
               FROM Paths 
               WHERE REGEXP_COUNT(path, ',') > 1
             ) THEN 'В схеме есть циклические зависимости' 
             ELSE 'В схеме нету циклических зависимостей' 
           END
    INTO result
    FROM dual;
    
    DBMS_OUTPUT.PUT_LINE(result);
    
    EXECUTE IMMEDIATE 'DELETE FROM schema_dependencies';
  
END check_cyclic_dependencies;


-- сравнивает схемы
CREATE OR REPLACE PROCEDURE compare_schemas(dev_schema in VARCHAR2, prod_schema in VARCHAR2) 
AS
    diff NUMBER := 0;
    query_string VARCHAR2(4000) := '';
    temp_string VARCHAR2(4000) := '';
BEGIN     
    FOR same_table IN 
        (SELECT table_name FROM all_tables dev_tables WHERE OWNER = dev_schema
        INTERSECT
        SELECT prod_tables.table_name FROM all_tables prod_tables WHERE OWNER = prod_schema) 
    LOOP
        -- Сравниваем структуру столбцов общих схем и записываем разницу в переменную
        SELECT COUNT(*) INTO diff FROM
        (SELECT dev_table.COLUMN_NAME name, dev_table.DATA_TYPE FROM all_tab_columns dev_table 
        WHERE OWNER=dev_schema AND TABLE_NAME = same_table.table_name) dev_columns
        FULL JOIN
        (SELECT prod_table.COLUMN_NAME name, prod_table.DATA_TYPE FROM all_tab_columns prod_table
        WHERE OWNER = prod_schema AND TABLE_NAME = same_table.table_name) prod_columns
        ON dev_columns.name = prod_columns.name
        WHERE dev_columns.name IS NULL OR prod_columns.name IS NULL;

        -- Если есть различия, то заносим в таблиц с соответсвущим флагом
        IF diff > 0 THEN
            INSERT INTO comparison_result (table_name, is_different) VALUES (same_table.table_name, 1);
        ELSE
            INSERT INTO comparison_result (table_name) VALUES (same_table.table_name);
        END IF;
    END LOOP;
        
    -- Проходимся по таблицам, которые только в дев
    FOR other_table IN 
        (SELECT dev_tables.table_name name FROM all_tables dev_tables WHERE dev_tables.OWNER = dev_schema
        MINUS 
        SELECT prod_tables.table_name FROM all_tables prod_tables WHERE prod_tables.OWNER = prod_schema) 
    LOOP
        INSERT INTO comparison_result (table_name, is_only_in_dev_schema) VALUES (other_table.name, 1);
    END LOOP;
    
    -- Проходимся по таблицам, которые тольок в прод
    FOR other_table IN 
        (SELECT prod_tables.table_name name FROM all_tables prod_tables WHERE prod_tables.OWNER = prod_schema
        MINUS
        SELECT dev_tables.table_name FROM all_tables dev_tables WHERE dev_tables.OWNER = dev_schema) 
    LOOP
        INSERT INTO comparison_result (table_name, is_only_in_prod_schema) VALUES (other_table.name, 1);
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('Таблицы схемы ' || dev_schema || ':');
    check_cyclic_dependencies(dev_schema);
    sort_tables_in_schema(dev_schema);
    
    FOR rec IN (
        SELECT comparison_result.*
        FROM sorted_tables 
        JOIN comparison_result 
        ON sorted_tables.table_name = comparison_result.table_name
    ) LOOP
        IF rec.is_different = 1 THEN
            DBMS_OUTPUT.PUT_LINE('Таблица ' || rec.table_name || ' имеет различия');
        ELSIF rec.is_only_in_dev_schema = 1 THEN
            DBMS_OUTPUT.PUT_LINE('Таблица ' || rec.table_name || ' существует только в ' || dev_schema);

            temp_string := create_object('TABLE', rec.table_name, prod_schema, dev_schema);
            query_string := query_string || CHR(10) || temp_string;
        ELSE
            DBMS_OUTPUT.PUT_LINE('Таблица ' || rec.table_name || ' одинаковая');
        END IF;            
    END LOOP; 
            
    EXECUTE IMMEDIATE 'DELETE FROM sorted_tables';
    
    DBMS_OUTPUT.PUT_LINE(CHR(10) || 'Таблицы схемы ' || prod_schema || ':');
    check_cyclic_dependencies(prod_schema);
    sort_tables_in_schema(prod_schema);
    
    FOR rec IN (
        SELECT comparison_result.*
        FROM sorted_tables 
        JOIN comparison_result 
        ON sorted_tables.table_name = comparison_result.table_name
    ) LOOP
        IF rec.is_different = 1 THEN
            DBMS_OUTPUT.PUT_LINE('Tаблица ' || rec.table_name || ' имеет различия');

            temp_string := update_object('TABLE', rec.table_name, prod_schema, dev_schema);
            query_string := query_string || CHR(10) || temp_string;


        ELSIF rec.is_only_in_prod_schema = 1 THEN
            DBMS_OUTPUT.PUT_LINE('Таблица ' || rec.table_name || ' существует только в ' || prod_schema);

            temp_string := delete_object('TABLE', rec.table_name, prod_schema);
            query_string := query_string || CHR(10) || temp_string;
        ELSE
            DBMS_OUTPUT.PUT_LINE('Таблица ' || rec.table_name || ' одинаковая');
        END IF;            
    END LOOP; 
            
    EXECUTE IMMEDIATE 'DELETE FROM sorted_tables';
    
    EXECUTE IMMEDIATE 'DELETE FROM comparison_result';
   
    DBMS_OUTPUT.PUT_LINE(CHR(10) || 'DDL скрипт:' || CHR(10));
    DBMS_OUTPUT.PUT_LINE(query_string);

    query_string := '';

    compare_schemas_objects(dev_schema, prod_schema, query_string);

    DBMS_OUTPUT.PUT_LINE(CHR(10) || 'DDL скрипт:' || CHR(10));
    DBMS_OUTPUT.PUT_LINE(query_string);
END compare_schemas;


-- сравниваем объекты схем
CREATE OR REPLACE PROCEDURE compare_schemas_objects(
    dev_schema IN VARCHAR2,
    prod_schema IN VARCHAR2,
    query_string out VARCHAR2
) AS
  dev_text VARCHAR2(32767);
    prod_text VARCHAR2(32767);
    temp_string VARCHAR2(4000) := '';
    TYPE objarray IS VARRAY(4) OF VARCHAR2(10); 
    objects_arr objarray; 
  total INTEGER;
BEGIN
  objects_arr := objarray('PROCEDURE', 'FUNCTION', 'VIEW', 'PACKAGE');
  total := objects_arr.COUNT;
  DBMS_OUTPUT.PUT_LINE(CHR(10) || 'Сравнение объектов:');
  FOR i IN 1..total LOOP
        FOR same_object IN (
            SELECT dev_objects.object_name
            FROM all_objects dev_objects
            WHERE owner = dev_schema
            AND object_type = objects_arr(i)
            INTERSECT
            SELECT prod_objects.object_name 
            FROM all_objects prod_objects 
            WHERE owner = prod_schema AND object_type = objects_arr(i)
        ) LOOP  
          
          SELECT REGEXP_REPLACE(LISTAGG(text, ' ') WITHIN GROUP (ORDER BY line), ' {2,}', ' ') 
            INTO dev_text
            FROM all_source
            WHERE owner = dev_schema AND name = same_object.object_name;
          
          SELECT REGEXP_REPLACE(LISTAGG(text, ' ') WITHIN GROUP (ORDER BY line), ' {2,}', ' ') 
            INTO prod_text
            FROM all_source
            WHERE owner = prod_schema AND name = same_object.object_name;
          
          IF dev_text != prod_text THEN
                DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || same_object.object_name || ' имеют различную структуру');
                temp_string := update_object(objects_arr(i), same_object.object_name, prod_schema, dev_schema);
                query_string := query_string || CHR(10) || temp_string;
            ELSE
                DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || same_object.object_name || ' одинаковые');
            END IF; 
        END LOOP;
        
        FOR other_object IN 
            (SELECT dev_objects.object_name 
            FROM all_objects dev_objects 
            WHERE owner = dev_schema AND object_type = objects_arr(i)
            MINUS
            SELECT prod_objects.object_name 
            FROM all_objects prod_objects 
            WHERE owner = prod_schema AND object_type = objects_arr(i)) 
        LOOP
            DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || other_object.object_name || ' существует только в ' || dev_schema);


            temp_string := create_object(objects_arr(i), other_object.object_name, prod_schema, dev_schema);
            query_string := query_string || CHR(10) || temp_string;
        END LOOP;
            
        FOR other_object IN 
            (SELECT prod_objects.object_name 
            FROM all_objects prod_objects 
            WHERE owner = prod_schema AND object_type = objects_arr(i)
            MINUS
            SELECT dev_objects.object_name 
            FROM all_objects dev_objects 
            WHERE owner = dev_schema AND object_type = objects_arr(i)) 
        LOOP
            DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || other_object.object_name || ' существует только в ' || prod_schema);

            temp_string := delete_object(objects_arr(i), other_object.object_name, prod_schema);
            query_string := query_string || CHR(10) || temp_string;           
        END LOOP;
            
    END LOOP;
END compare_schemas_objects;



-- создает строку для создания объекта
CREATE OR REPLACE FUNCTION create_object (
    object_type IN VARCHAR2,
    object_name IN VARCHAR2,
    main_schema IN VARCHAR2,
    aux_schema IN VARCHAR2
) RETURN VARCHAR2
AUTHID CURRENT_USER -- Переключаем на права вызывающего
IS
    result VARCHAR2(4000);
BEGIN
    IF object_type = 'TABLE' THEN
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'SQLTERMINATOR', TRUE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'PRETTY', TRUE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'SEGMENT_ATTRIBUTES', FALSE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'STORAGE', FALSE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'TABLESPACE', FALSE);
    END IF;

    result := DBMS_METADATA.GET_DDL(object_type, object_name, aux_schema);
    result := REPLACE(result, aux_schema, main_schema);

    RETURN result;
END create_object;

-- создает строку для изменеия объекта
CREATE OR REPLACE FUNCTION update_object (
    object_type IN VARCHAR2,
    object_name IN VARCHAR2,
    main_schema IN VARCHAR2,
    aux_schema IN VARCHAR2
) RETURN VARCHAR2
AUTHID CURRENT_USER -- Переключаем на права вызывающего
IS
    result VARCHAR2(4000);
BEGIN
    IF object_type = 'TABLE' THEN
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'SQLTERMINATOR', TRUE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'PRETTY', TRUE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'SEGMENT_ATTRIBUTES', FALSE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'STORAGE', FALSE);
        DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM, 'TABLESPACE', FALSE);
    END IF;

    result := DBMS_METADATA.GET_DDL(object_type, object_name, aux_schema);
    result := REPLACE(result, aux_schema, main_schema);

    IF object_type = 'TABLE' THEN
        result := 'DROP ' || object_type || ' ' || main_schema || '.' || object_name || ';' || CHR(10) || result;
    END IF;

    RETURN result;
END update_object;


-- создаем строку для удаления
CREATE OR REPLACE FUNCTION delete_object (object_type IN VARCHAR2, object_name IN VARCHAR2, main_schema IN VARCHAR2) 
RETURN VARCHAR2 IS
BEGIN
    RETURN 'DROP ' || main_schema || '.' || object_type || ' ' || object_name || ';';
END delete_object;

SELECT table_name 
FROM all_tables 
WHERE owner = 'DEV' AND table_name = 'DIFF_TABLE';

SELECT table_name 
FROM all_tables 
WHERE owner = 'DEV' 
AND table_name = 'DIFF_TABLE';


DECLARE
  	temp_string VARCHAR2(4000);
BEGIN
    temp_string := update_object('TABLE', 'DIFF_TABLE', 'PROD', 'DEV');
 	DBMS_OUTPUT.PUT_LINE(temp_string);
END;



DECLARE
  current_time VARCHAR2(10);
BEGIN
  current_time := TO_CHAR(SYSDATE, 'HH24:MI:SS');
  DBMS_OUTPUT.PUT_LINE(current_time);

  DBMS_OUTPUT.PUT_LINE('======================================================================');
    compare_schemas('DEV', 'PROD');
  DBMS_OUTPUT.PUT_LINE('======================================================================');
END;

SELECT USER FROM DUAL;

GRANT EXECUTE ANY PROCEDURE TO LAB3;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA DEV TO LAB3;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA PROD TO LAB3;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA SYSTEM TO LAB3;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA LAB3 TO SYSTEM;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA LAB3 TO DEV;
GRANT EXECUTE ANY PROCEDURE ON SCHEMA LAB3 TO PROD;
GRANT SELECT ANY TABLE TO LAB3;
GRANT SELECT ANY TABLE ON SCHEMA DEV TO LAB3;
GRANT SELECT ANY TABLE ON SCHEMA PROD TO LAB3;
GRANT SELECT ANY DICTIONARY TO LAB3;
GRANT INHERIT PRIVILEGES ON USER LAB3 TO SYSTEM;
GRANT INHERIT PRIVILEGES ON USER SYSTEM TO LAB3;
GRANT INHERIT PRIVILEGES ON USER LAB3 TO SYSTEM;

-- Если SYSTEM вызывает функцию LAB3.UPDATE_OBJECT
GRANT INHERIT PRIVILEGES ON USER SYSTEM TO LAB3;

-- Также предоставьте привилегии для других пользователей схем DEV и PROD
GRANT INHERIT PRIVILEGES ON USER DEV TO LAB3;
GRANT INHERIT PRIVILEGES ON USER PROD TO LAB3;
-- Предоставляем права на select и execute к словарям данных
GRANT SELECT_CATALOG_ROLE TO LAB3;
GRANT EXECUTE_CATALOG_ROLE TO LAB3;
ALTER USER LAB3 QUOTA UNLIMITED ON USERS;

GRANT INHERIT PRIVILEGES ON USER LAB3 TO PUBLIC;

GRANT SELECT_CATALOG_ROLE TO LAB3 WITH ADMIN OPTION;
GRANT SELECT_CATALOG_ROLE TO SYSTEM WITH ADMIN OPTION;

GRANT SELECT_CATALOG_ROLE TO FUNCTION create_object;
GRANT SELECT_CATALOG_ROLE TO FUNCTION update_object;



CREATE TABLE "PROD"."COMMON_TABLE" 
   (	"ID" NUMBER(*,0), 
	"NAME" VARCHAR2(50), 
	 PRIMARY KEY ("ID")
  USING INDEX  ENABLE
   ) ;

  CREATE TABLE "PROD"."FOREIGN_TABLE" 
   (	"ID" NUMBER(*,0), 
	"COMMON_ID" NUMBER(*,0), 
	 PRIMARY KEY ("ID")
  USING INDEX  ENABLE, 
	 FOREIGN KEY ("COMMON_ID")
	  REFERENCES "PROD"."COMMON_TABLE" ("ID") ENABLE
   ) ;
DROP TABLE "PROD".CYCLE1;
DROP TABLE "PROD".CYCLE2;
