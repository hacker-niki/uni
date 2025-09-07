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
            DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || other_object.object_name || ' находится только в ' || dev_schema);

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
            DBMS_OUTPUT.PUT_LINE(objects_arr(i) || ' ' || other_object.object_name || ' находится только в ' || prod_schema);

            temp_string := delete_object(objects_arr(i), other_object.object_name, prod_schema);
            query_string := query_string || CHR(10) || temp_string;           
        END LOOP;
            
    END LOOP;
END compare_schemas_objects;