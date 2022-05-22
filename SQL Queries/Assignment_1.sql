WITH Table1 AS (

    SELECT `dsba-head-of-data-101.group_7_dataset.synthetic_deliveroo_plus_group_7`.*,

             LEAD(is_free_delivery, 1) OVER(PARTITION BY id_customer_synth ORDER BYorder_datetime_synth) as next_1,

             LEAD(is_free_delivery, 2) OVER(PARTITION BY id_customer_synth ORDER BYorder_datetime_synth) as next_2,

             LAG(is_free_delivery, 1) OVER(PARTITION BY id_customer_synth ORDER BYorder_datetime_synth) as prev_1,

             LAG(is_free_delivery, 2) OVER(PARTITION BY id_customer_synth ORDER BYorder_datetime_synth) as prev_2

     FROM `dsba-head-of-data-101.group_7_dataset.synthetic_deliveroo_plus_group_7`  

),

Table2 AS (

    SELECT id_customer_synth, order_datetime_synth, is_free_delivery, next_1, next_2, prev_1, prev_2, 

    CASE

        WHEN next_1 = 1 

            AND next_2 = 1 

            AND is_free_delivery = 1 THEN 1

        WHEN next_1 = 1

            AND prev_1 = 1

            AND is_free_delivery = 1 THEN 1

        WHEN prev_1 = 1

            AND prev_2 = 1

            AND is_free_delivery  = 1 THEN 1  

    ELSE 0 END AS is_order_made_during_subscription

    FROM Table1

),

Table3 AS (

  SELECT id_customer_synth, order_datetime_synth, is_free_delivery, next_1, next_2, prev_1, prev_2, is_order_made_during_subscription,

  CASE WHEN is_order_made_during_subscription = 1 THEN FIRST_VALUE(order_datetime_synth) OVER(PARTITION BY id_customer_synth, is_order_made_during_subscription ORDER BYorder_datetime_synth)

  ELSE NULL END AS current_subscription_start_datetime,

  CASE WHEN is_order_made_during_subscription = 1 THEN FIRST_VALUE(order_datetime_synth) OVER(PARTITION BY id_customer_synth, is_order_made_during_subscription ORDER BYorder_datetime_synth DESC)

  ELSE NULL END AS current_subscription_end_datetime,

  FROM Table2

)

SELECT id_customer_synth, order_datetime_synth,is_free_delivery,is_order_made_during_subscription,current_subscription_start_datetime,current_subscription_end_datetimeFROM Table3

ORDER BY Table3.id_customer_synth, Table3.order_datetime_synth ASC