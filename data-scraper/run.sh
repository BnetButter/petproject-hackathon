docker run --rm -it  --env-file $(pwd)/.env -p 8080:8080 -v $(pwd):/app -v $(pwd)/airflow.cfg:/home/seluser/airflow/airflow.cfg selenium /app/start.sh
