#! /bin/bash
airflow db init

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email airflow@airflow.com \
    --password $AIRFLOW_PASSWORD


nohup airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &
airflow webserver --port 8080
