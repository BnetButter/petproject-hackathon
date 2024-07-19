#! /bin/bash
airflow db init

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email airflow@airflow.com \
    --password airflow


nohup airflow webserver --port 8080 > ~/airflow/logs/webserver.log 2>&1 &
nohup airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &

bash
