DECLARE NAME String;

SET NAME = (WITH Metadata AS

(

  SELECT * FROM assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS table_options ORDER BYtable_name

),

T_2 AS

(

  SELECT * 

  FROM Metadata

  WHERE option_value LIKE "%validated%"

)

SELECT table_name

FROM T_2

ORDER BY table_name DESC LIMIT 1);

EXECUTE IMMEDIATE "CREATE OR REPLACE TABLE `dsba-head-of-data-101.group_7_dataset.last_validated_ecom` AS (SELECT * FROM `dsba-head-of-data-101.assignment_data.*` WHERE _TABLE_SUFFIX = @String)" USING NAME as String;