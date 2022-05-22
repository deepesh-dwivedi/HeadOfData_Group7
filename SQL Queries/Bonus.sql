Declare industry,table_val string;
set (industry,table_val) = (
  select as struct REGEXP_EXTRACT(ddl,r'configuration_name\b.{4}(.*)"'),table_name
  from assignment_data.INFORMATION_SCHEMA.TABLES tables
  Where ddl like "%validated%"
  order by table_name desc limit 1
);

EXECUTE IMMEDIATE 
Format('create or replace table `dsba-head-of-data-101.group_7_dataset.last_validated_%s` as select * from `dsba-head-of-data-101.assignment_data.%s`',industry,table_val)
